# PII Field Exposure

## Issue
A tool call returns personally identifiable information (name, email, phone, home address, date of birth) that wasn't necessary for the task the agent was performing and wasn't supposed to be exposed to that agent or context at all. Unlike a masking or classification failure, the PII here isn't hidden behind any control — it's simply present in the default response shape of a tool because the tool was designed to return "the whole object" rather than the minimum fields the task requires, and the agent (and anything downstream of it, including logs and conversation history) now has that PII whether it needed it or not.

**Frequency**: Very Common

**Symptoms**
- A tool built to answer a narrow question (e.g., "is this order shipped?") returns the full customer object, including email and phone, in its response payload
- The agent's final answer to the user doesn't mention PII, but the PII was present in the tool call's intermediate output and gets logged or cached anyway
- PII fields appear in tool responses even for tasks that are purely aggregate or statistical and never needed individual identity at all
- Different tools return inconsistent amounts of PII for conceptually the same lookup, depending on which underlying API each was built against
- A downstream agent or sub-process that only needed a status field receives, and can act on, full contact information it was never scoped to use

## Root Cause
Tool builders default to returning full backend objects because it's simpler than defining a minimal, purpose-specific response schema for every use case, and because the underlying internal APIs the tools wrap were themselves built for broader purposes (e.g., an internal CRM API meant for full customer management, now reused as the backing for a narrow "check order status" agent tool). Without a deliberate exercise in field minimization tied to each tool's actual task, the path of least resistance is to expose everything the underlying data source has, on the assumption that unused fields are harmless — an assumption that breaks down once an LLM-driven agent is the one reading, logging, and potentially repeating that data.

## Example
```
An internal "order status" tool is built quickly by wrapping the
existing customer-order API used by the fulfillment team, which returns
the full order object: `order_id`, `status`, `customer_name`,
`customer_email`, `shipping_address`, `phone_number`, and
`payment_last4`. The tool is given to a logistics-tracking agent whose
only job is to answer "where is my package" questions using `status`
and an estimated delivery date.

Every time the agent calls the tool, the full object — including the
customer's home address and phone number — flows into the agent's
context window and gets written to the conversation transcript store
for debugging and evaluation purposes. Months later, a routine security
review of transcript logs discovers that the logistics-tracking agent,
which was never meant to have access to contact information, has been
handling and persisting full customer PII on every single invocation,
across millions of conversations, with no field minimization ever
applied.
```

## Statistics
| Finding | Context |
|---------|---------|
| Tools built by wrapping existing internal APIs are disproportionately likely to over-expose fields relative to purpose-built minimal-schema tools | Common finding in agent-tooling architecture reviews |
| A large share of PII appearing in agent conversation logs is never referenced in the agent's actual output to the user, indicating it was retrieved but not needed | Typical of full-object tool responses versus task-scoped ones |
| Field-minimization retrofits (redesigning a tool's response schema to the task's actual needs) are among the most common remediations following an agent-tooling privacy review | Common in post-review remediation patterns |

## Mitigations
1. **Purpose-scoped response schemas**: Define each tool's response schema explicitly around the minimum fields its stated task requires, rather than passing through the full backing API object; treat every additional field as something that must be justified, not assumed harmless.
2. **Field minimization at the API boundary**: Apply a field-stripping layer between the internal API and the agent-facing tool definition, so that even if the backing API changes or adds fields, the tool's exposed surface doesn't silently grow.
3. **PII-aware logging redaction**: Redact known PII field patterns from conversation transcripts, tool-call logs, and evaluation datasets by default, independent of whether the tool response itself was minimized, as a defense-in-depth layer.
4. **Per-tool PII exposure review**: Require an explicit sign-off step during tool design/review that enumerates every PII field in the response and justifies why the task needs it, blocking tools that can't justify a field's inclusion.
5. **Periodic transcript field auditing**: Regularly sample production agent transcripts and flag PII fields present but never referenced in the agent's final output, feeding results back into schema minimization work.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `unused_pii_field_rate` | Share of tool responses containing a PII field that never appears in the agent's final output to the user | Alert threshold: > 10% of invocations for a given tool |
| `pii_field_count_per_tool_response` | Average number of distinct PII fields present in a single tool response | Alert threshold: > justified baseline defined per tool at design time |
| `transcript_pii_redaction_miss_rate` | Rate at which known PII patterns are found unredacted in stored transcripts | Alert threshold: > 0.1% of transcripts |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Excess PII in Tool Response | A tool's response includes PII fields not on its approved minimal schema | P2 | Patch the tool's response shape, review recent logs for retroactive redaction needs |
| Unreferenced PII in Transcript | Sampled transcript audit finds PII present but unused across a significant share of a tool's invocations | P3 | Prioritize schema minimization for the tool in the next review cycle |

## Related Patterns
- [PII Field Leakage In Responses](./pii-field-leakage-in-responses.md) - a related but distinct failure where PII is correctly scrubbed from the primary response but leaks through a secondary channel
- [Field-Level Access Not Restricted](./field-level-access-not-restricted.md) - PII over-exposure is often a downstream symptom of record-level-only access control
- [Sensitive Field Access Not Restricted](./sensitive-field-access-not-restricted.md) - overlaps for PII fields that are also flagged as sensitive, though this pattern covers unnecessary exposure even of unflagged PII
