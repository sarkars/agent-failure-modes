# Model Knowledge Cutoff

## Issue
The model answers questions about facts, prices, APIs, regulations, or current events using knowledge frozen at its training cutoff, but presents the answer with the same confident, unhedged tone it would use for a fact that is still current. The agent has no built-in awareness of which of its facts have gone stale since training, so it cannot distinguish "this is still true" from "this was true as of my cutoff" without an explicit check.

**Frequency**: Very Common

**Symptoms**
- Agent states a library's current API, a company's current pricing, or a regulation's current requirements as fact, when it changed after the model's training cutoff
- No hedging language ("as of my last update," "you may want to verify") accompanies claims about time-sensitive information
- Errors cluster on fast-moving domains: software library versions, pricing pages, personnel/leadership, legal/regulatory thresholds, recent events
- Agent contradicts itself when given up-to-date retrieved context that conflicts with its trained knowledge, sometimes trusting its own stale memory over the fresher retrieved source
- Users only discover the staleness when a downstream action (e.g. calling a deprecated API method) fails

## Root Cause
A model's parametric knowledge is fixed at the point its training data was collected; nothing in the architecture updates that knowledge after deployment, and the model has no internal clock or mechanism to distinguish facts that are still stable from facts that routinely change. During training, the model learns to answer factual questions fluently and confidently because that was the reward pattern in its training data — confident, complete answers were preferred over hedged ones — and this preference doesn't automatically compute a per-fact decay rate. The model also has no reliable introspective access to its own cutoff date for arbitrary claims: it can state its cutoff if asked directly, but it cannot generally tell, at the moment of generating a specific fact, whether that particular fact is one likely to have changed since then.

## Example
```
A coding agent is asked to write an integration against a third-party
payment API. The model, trained on data through early 2025, generates code
using an endpoint (`/v1/charges`) and an authentication scheme that were
current at that time.

The provider deprecated `/v1/charges` in favor of `/v2/payment_intents`
six months after the model's training cutoff, with the old endpoint now
returning 410 Gone.

The agent presents the generated integration code with no caveat about
possible staleness. The user deploys it, and the integration fails in
production with a cryptic 410 error, sending the team on a debugging
detour before they discover the API version mismatch traces back to the
model simply not knowing about a change made after its cutoff.
```

## Statistics
| Finding | Context |
|---------|---------|
| For fast-moving domains (SDK/API versions, pricing, personnel), a noticeable share of unretrieved model answers are measurably stale within 6-12 months of training cutoff | Estimated from spot-audits comparing model claims to current source-of-truth data |
| Adding explicit retrieval/grounding for time-sensitive fact categories reduces staleness-driven errors by a large majority relative to relying on parametric knowledge alone | Typical range reported across RAG-augmented vs. non-augmented agent comparisons |
| Unprompted hedging language on time-sensitive claims appears in a small minority of responses, well below the share of such claims that are actually stale | Estimated from manual review of agent responses on fast-changing topics |

## Mitigations
1. **Mandatory retrieval for time-sensitive categories**: Classify query types known to be fast-moving (pricing, API versions, regulations, personnel, current events) and route them through live retrieval instead of relying on the model's parametric knowledge.
2. **Cutoff-aware system prompting**: Explicitly instruct the model to state its training cutoff and hedge on any fact plausibly affected by time when retrieval isn't available.
3. **Grounded-context precedence**: When retrieved, current context conflicts with the model's trained knowledge, instruct the model (and verify via evals) that the retrieved context takes precedence.
4. **Staleness spot-checks in evaluation**: Periodically test the deployed model against a curated set of facts known to have changed since its cutoff, to measure how much it still relies on outdated parametric knowledge versus deferring appropriately.
5. **Post-deployment freshness monitoring**: Track downstream failures traceable to stale facts (deprecated endpoints, outdated pricing) and feed them back into the retrieval-routing classifier's coverage.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| ungrounded_time_sensitive_answer_rate | Share of time-sensitive-category queries answered without retrieval grounding | Alert if > 10% |
| staleness_spot_check_accuracy | Accuracy on a curated set of facts known to have changed post-cutoff | Alert if < 80% |
| downstream_failure_stale_fact_rate | Rate of production failures (API errors, incorrect pricing shown) traced back to stale model knowledge | Alert if trending upward |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Time-sensitive query answered without retrieval | Classifier detects a fast-moving-domain query routed without grounding | Medium | Route to retrieval path, log classifier miss for retraining |
| Downstream failure traced to stale fact | Production error (e.g. deprecated endpoint call) attributed to model knowledge cutoff | High | Patch retrieval coverage for the affected fact category, notify affected users |

## Related Patterns
- [Model Uncertainty Unawareness](./model-uncertainty-unawareness.md) - stale knowledge is delivered with the same unwarranted confidence this pattern describes more broadly
- [Model Reasoning Inconsistency](./model-reasoning-inconsistency.md) - conflicts between stale parametric knowledge and fresh retrieved context can surface as inconsistent answers to logically similar queries
- [Model Capacity Limits](./model-capacity-limits.md) - both describe silent quality gaps between what the model appears to know and what it actually reliably knows
