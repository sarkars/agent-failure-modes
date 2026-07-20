# Output Format Not Validated

## Issue
An agent produces output intended to conform to a specific schema (JSON with required fields, a fixed CSV column set, an API response contract) and hands it directly to a downstream consumer without verifying it actually matches that schema first. Because LLM-generated output is probabilistic rather than mechanically guaranteed, a small but nonzero fraction of responses have a missing field, wrong type, extra field, or malformed structure — and without a validation gate, that malformed output reaches the consumer exactly as if it were valid, causing it to fail unpredictably rather than being caught at the source.

**Frequency**: Common

**Symptoms**
- Downstream consumers (APIs, databases, other agents) throwing schema/type errors on a small percentage of requests with no pattern visible from the agent's side
- Fields that are supposed to always be present (per the documented contract) occasionally missing from actual output
- Silent acceptance of extra or renamed fields that a stricter consumer would have rejected, propagating malformed records further downstream
- Failures that correlate with specific input complexity or edge cases the model handles less reliably, rather than being uniformly distributed
- No error or warning logged at the point of generation — the malformed output looks like a completed, successful response until something downstream chokes on it

## Root Cause
Structured output from a generative model is produced by predicting tokens that are likely to form valid output given the prompt and schema description, not by a mechanism that guarantees structural validity the way a strictly-typed function return does. Even with function-calling/structured-output features, edge cases — deeply nested objects, ambiguous instructions, unusual input triggering an unusual completion path — can produce output that deviates from the schema in ways the generation process itself has no way to detect, because the model isn't running a validator against its own output before returning it. When the calling code trusts the output implicitly (parses it and moves on, rather than validating against the schema first), the gap between "the model tried to produce valid output" and "the output is actually valid" becomes the caller's problem, discovered wherever the first downstream consumer that actually checks types happens to be.
## Example
```
An agent extracts structured order data from unstructured customer
emails and passes the resulting JSON directly to an order-processing
API expecting:

    { "customer_id": string, "items": array, "total": number }

For 995 of 1000 emails, the agent produces well-formed output. For a
handful of unusual emails -- one where the customer pasted a forwarded
thread containing a different order's total further down -- the agent
returns:

    { "customer_id": "C-4471", "items": [...], "total": "see below" }

The agent's code passes this straight to `order_api.submit(response)`
with no validation. The order-processing API's own type checking
rejects the string "see below" for a numeric field and returns a 400
error, but because the agent's calling code doesn't distinguish this
from a generic network failure, it retries the exact same malformed
payload three times before giving up and logging a generic
"submission failed after retries" error with no indication that the
root cause was a malformed field the agent itself produced.
```

## Statistics
| Finding | Context |
|---------|---------|
| Structured-output generation from LLMs typically deviates from a strict schema in a small single-digit percentage of responses even with function-calling/JSON-mode features | Typical range observed across production structured-output pipelines |
| A meaningful share of "generic downstream failure" incidents in agent pipelines resolve, on investigation, to unvalidated malformed agent output | Typical range observed in incident postmortems |
| Adding a schema-validation gate immediately after generation, before the output is used, catches the large majority of these cases at the source rather than downstream | Estimated from the directness of validating against the known schema |

## Mitigations
1. **Validate immediately after generation**: Run the agent's structured output through a schema validator (JSON Schema, Pydantic, or equivalent) immediately after generation and before it's passed to any downstream consumer, rather than trusting it implicitly.
2. **Fail closed with a retry-and-repair loop**: On validation failure, don't silently pass the malformed output through or blindly retry the identical request — feed the validation error back to the agent as context for a corrected regeneration attempt, bounded to a small number of retries.
3. **Distinguish validation failures from transient failures in retry logic**: Ensure the calling code's retry/error-handling logic can tell "downstream rejected malformed output" apart from "network/transient error," since retrying an identical malformed payload wastes calls and delays root-cause visibility.
4. **Log validation failures with full context**: When output fails schema validation, log the failure with the triggering input and the malformed output itself, building a corpus of edge cases that reliably produce format failures for targeted prompt or schema improvements.
5. **Contract tests against the schema's edge cases**: Maintain a test suite of historically-problematic inputs (ambiguous, unusually long, multi-topic) run against the schema validator as part of routine regression testing for the agent's output-generation logic.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| schema_validation_failure_rate | Share of agent-generated outputs failing schema validation before being passed downstream | Alert if > 1% |
| downstream_type_error_rate | Rate of downstream consumers rejecting agent output due to type/schema mismatch | Alert if > 0.1% |
| repair_retry_success_rate | Share of validation failures successfully corrected via a repair-and-regenerate loop | Alert if < 80% (indicates deeper generation issue) |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Schema validation failure | Agent output fails validation against its documented output contract | Medium | Route to repair loop, log input/output pair for review, do not forward to downstream consumer |
| Downstream schema rejection despite upstream validation | A downstream consumer rejects output that passed the agent's own schema validation | High | Audit for a schema drift between the agent's validator and the consumer's actual contract |

## Related Patterns
- [Output Hallucination in Structured Format](./output-hallucination-in-structured-format.md) - a specific cause of format-validation failures, where the agent fabricates a plausible-looking but incorrect value to fill a required field
- [Output Inconsistency](./output-inconsistency.md) - unvalidated format drift across calls is one way inconsistency manifests
- [Input Schema Evolution](./input-schema-evolution.md) - the mirror-image failure on the input side, where an upstream schema changes without the agent's parser being updated
