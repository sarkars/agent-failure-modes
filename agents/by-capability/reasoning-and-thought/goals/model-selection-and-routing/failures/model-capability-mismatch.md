# Model Capability Mismatch

## Issue
A routing layer selects a model for a task without verifying that the model actually supports a capability the task requires — vision input, function/tool calling, a long enough context window, structured output mode — and the mismatch is discovered only when the call fails or, worse, silently ignores the unsupported input. Routers optimized for cost or latency often select on those axes alone, treating capability support as a given rather than a routing constraint to check.

**Frequency**: Occasional

**Symptoms**
- A request containing an image is routed to a text-only model, which either errors or silently responds as if no image were attached
- A task requiring function calling is routed to a model without reliable tool-use support, causing the agent's tool-call parsing to fail
- Long-document tasks are routed to a model with a shorter context window than the input, causing silent truncation rather than an explicit error
- Capability failures cluster around newer request types (e.g. newly added multimodal inputs) that the routing table wasn't updated to account for
- The router's cost/latency optimization logic has no awareness of the task's capability requirements, only of its estimated token count or category label

## Root Cause
Routing systems are typically built around a cost/latency/quality tradeoff table keyed by coarse task category, and capability support (vision, tools, context length, JSON mode) is a separate, often manually maintained attribute of each model that isn't wired into the same decision path. When a new task type is added upstream (e.g. the product starts accepting image uploads) or a new model is added to the routing pool, it's easy for the capability metadata to lag behind — the router keeps selecting based on its existing cost/quality heuristics without a hard capability-compatibility gate blocking selection of models that can't actually serve the request. The failure is often silent rather than a clean error because many APIs accept a request with unsupported content without validating it strictly, degrading gracefully (ignoring the image, ignoring the tool schema) rather than rejecting the call outright.

## Example
```
A customer support platform adds a "attach a photo of the damaged item"
feature to its complaint-intake agent. The underlying router selects
models purely by a cost-tiering rule: cheap model for tickets under a
complexity score of 5, premium model above that.

A ticket with an attached photo and simple text ("item arrived broken,
see photo") scores low on the text-complexity heuristic and is routed to
the cheap tier model, which does not support image input.

The API call succeeds - the endpoint silently drops the unsupported image
attachment rather than erroring - and the model responds based on the text
alone: "Thanks, we've processed your refund request." The agent never
saw the photo, and a case that should have been auto-rejected for
insufficient evidence (no photo actually reviewed) or escalated is instead
approved on text alone.
```

## Statistics
| Finding | Context |
|---------|---------|
| Capability-related routing failures cluster heavily (majority of incidents) around newly introduced input/task types not yet reflected in routing configuration | Typical pattern observed across router incident postmortems |
| A meaningful share of capability mismatches produce no explicit API error, degrading silently instead (dropped attachment, ignored tool schema) | Estimated from audits of multimodal/tool-calling routing pipelines |
| Adding an explicit capability-compatibility gate to the routing decision (before cost/latency selection) eliminates the large majority of these incidents in subsequent testing | Typical range reported by teams that added capability gating |

## Mitigations
1. **Capability-compatibility gating before cost optimization**: Filter the candidate model pool down to only capability-compatible models first, then apply cost/latency optimization within that filtered set — never the reverse order.
2. **Explicit capability metadata with CI validation**: Maintain machine-readable capability metadata per model (vision, tools, context length, structured output) and validate it against the provider's actual documented support as part of routing-config CI, not manual updates.
3. **Fail loudly on capability gaps**: Configure calls to reject explicitly (not silently degrade) when a request includes content the target model doesn't support, so mismatches surface as errors rather than silent quality loss.
4. **New-feature routing checklist**: Require any new input/task type (e.g. adding image upload) to include an explicit routing-table update and test before launch, as a release gate rather than an afterthought.
5. **Synthetic capability probes in monitoring**: Periodically send known capability-requiring test requests through the router and verify they land on compatible models, catching config drift before real traffic hits it.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| capability_mismatch_rate | Share of requests routed to a model lacking a capability the request requires | Alert if > 0.1% |
| silent_content_drop_rate | Rate of calls where unsupported content (image, tool schema) was silently ignored rather than erroring | Alert if > 0 for high-stakes request types |
| new_feature_routing_coverage | Whether newly launched input/task types have corresponding capability-gated routing rules | Alert if any live feature lacks coverage |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Capability mismatch detected | A request is routed to (or would be routed to) a capability-incompatible model | High | Block routing to incompatible model, fall back to compatible pool, page router owner |
| Silent content drop spike | silent_content_drop_rate rises above zero for a monitored request type | High | Audit recent routing config changes, add explicit capability gate for affected content type |

## Related Patterns
- [Model Version Incompatibility](./model-version-incompatibility.md) - a narrower case of the same problem, where the mismatch is a specific feature gap between model versions rather than a coarse capability category
- [Model Downgrade Silent Failure](./model-downgrade-silent-failure.md) - both involve routing decisions that silently degrade quality without surfacing the tradeoff being made
- [Model Selection Nondeterminism](./model-selection-nondeterminism.md) - unstable routing config is one path by which a request that should be capability-gated ends up on an incompatible model inconsistently
