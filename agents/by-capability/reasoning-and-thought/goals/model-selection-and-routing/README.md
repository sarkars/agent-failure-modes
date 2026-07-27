# What Are the Most Common Model-Selection and Routing Failures in AI Agents?

**Model routing layers send requests to the wrong model because routers are typically built to optimize one visible, easy-to-measure axis — cost, latency, or a coarse task-category label — while capability compatibility, instance health, and version-specific feature support are treated as separate, often stale metadata that isn't wired into the same selection decision.** The result is a request landing on a model that can't actually serve it (missing a capability), on a degraded instance the health check didn't catch, or on a materially different model version than the one the calling code was built and tested against — and because APIs often degrade gracefully rather than erroring, the mismatch is frequently invisible until an aggregate quality metric or a user complaint surfaces it.

## Key Takeaways

- 6 patterns are documented here, covering the router's decision (which model), health signal (which instance), and consistency (same model across repeated or session-linked calls).
- 5 of the 6 patterns are rated "Occasional"; only Model Downgrade Silent Failure is rated "Common" — cost-driven downgrades happen more frequently than capability or version mismatches because they're a deliberate, recurring lever rather than a one-off configuration gap.
- The patterns cluster into three pairs, each pair explicitly cross-referenced in the source files as variants of the same underlying problem: capability/version gating (2 patterns), quality/health blind spots (2 patterns), and routing-decision instability (2 patterns).
- A recurring structural fix appears across multiple patterns: gate on compatibility or health *before* applying cost/latency optimization, never after — several patterns document that reversing the gate order is the root cause.

## Scope

- **Compatibility Gating Failures** — [Model Capability Mismatch](failures/model-capability-mismatch.md), [Model Version Incompatibility](failures/model-version-incompatibility.md). Both describe a router selecting a model that can't actually serve the request — one at the coarse level (vision, tool-calling, context length as a whole capability), the other at the fine-grained level (a specific parameter or response shape that differs between versions within the same model family).
- **Quality & Health Blind Spots** — [Model Downgrade Silent Failure](failures/model-downgrade-silent-failure.md), [Model Load Balancing Failure](failures/model-load-balancing-failure.md). Both describe a router optimizing on a metric it can see in real time (spend, liveness) while the metric that actually matters (quality, real task-completion latency) has no feedback loop back into the routing decision.
- **Routing Consistency Failures** — [Model Selection Nondeterminism](failures/model-selection-nondeterminism.md), [Model Switching Mid-Session](failures/model-switching-mid-session.md). Both describe the same logical request or session landing on different models across calls or turns, because routing is re-evaluated more granularly (per-request, per-turn) than the continuity the calling code or conversation actually needs.

## When Model Selection & Routing Matters

- A platform adds a new input type (images, tool calls, longer documents) or a new model to its routing pool, and needs to verify the routing table's capability metadata was updated alongside it
- Cost-optimization pressure is pushing traffic toward cheaper models or tiers, and there's no paired quality metric to weigh against the reported savings
- An agent runs multi-turn conversations or sessions where consistency of persona, established facts, or tool-call conventions across turns matters, and per-turn or per-request routing could silently swap the underlying model mid-session

## Cross-Pattern Insight

Every model-selection-and-routing pattern traces back to the same structural gap: routing infrastructure has a tight, real-time feedback loop for the metric it was built to optimize (cost, latency, liveness) and no equivalent feedback loop for the metric that actually determines whether the request was served correctly (capability match, task-representative health, output quality, session continuity). The fix documented across patterns is consistently to add the missing gate or signal explicitly — a capability-compatibility gate before cost optimization, task-representative health checks instead of lightweight liveness pings, paired quality-cost dashboards, durable per-request routing logs, and session-pinned (rather than per-turn) model selection — rather than assuming the existing optimized metric is a good enough proxy for the one that was left out.

## Frequently Asked Questions

### What's the difference between Model Capability Mismatch and Model Version Incompatibility?
[Model Capability Mismatch](failures/model-capability-mismatch.md) is the coarse case — a text-only model receiving an image, or a non-tool-calling model receiving a function-calling request. [Model Version Incompatibility](failures/model-version-incompatibility.md) is the fine-grained case within the same capability category — two versions of the same model family both nominally support tool calling, but one supports parallel tool calls and the other doesn't, breaking calling code that assumed uniform behavior across the family.

### Can a cost-saving routing change ever be treated as a failure pattern?
Because per [Model Downgrade Silent Failure](failures/model-downgrade-silent-failure.md), the downgrade decision itself is often reasonable — the failure is that no mechanism measures or surfaces the resulting quality impact, so the cost win is visible on a dashboard while the quality loss accumulates for weeks before anyone notices via complaints. The pattern isn't "don't downgrade," it's "downgrades without a paired quality metric are invisible regressions."

### If a load balancer's health checks are passing, why would routing still be broken?
Per [Model Load Balancing Failure](failures/model-load-balancing-failure.md), a lightweight liveness health check (a fast ping) measures reachability, not the quality of service under real production traffic — an instance can respond to a health check normally while queueing badly or degrading under load, and the balancer keeps sending it a full share of traffic because its routing signal never saw the real degradation.

### Does session-pinned routing fully solve mid-session model switching?
[Model Switching Mid-Session](failures/model-switching-mid-session.md) reports that pinning model selection for the duration of a session (rather than re-evaluating per turn) eliminates the large majority of switch-induced continuity complaints, though failover events unrelated to routing logic (an instance going down) can still force an unavoidable switch — the pattern's mitigation for that case is explicit constraint re-anchoring at the switch point rather than relying on silent transcript continuity.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Model Capability Mismatch](failures/model-capability-mismatch.md) | Router selects a model without verifying it supports a capability (vision, tools, context length) the request needs |
| [Model Downgrade Silent Failure](failures/model-downgrade-silent-failure.md) | Cost-driven router shifts traffic to a cheaper model with no mechanism to measure or surface the quality impact |
| [Model Load Balancing Failure](failures/model-load-balancing-failure.md) | Balancer keeps routing to a degraded instance because its health check measures liveness, not real task quality |
| [Model Selection Nondeterminism](failures/model-selection-nondeterminism.md) | Identical requests route to different underlying models across runs due to unrecorded load/cohort/tie-break factors |
| [Model Switching Mid-Session](failures/model-switching-mid-session.md) | Per-turn re-routing hands a conversation to a different model mid-session, breaking persona/context continuity |
| [Model Version Incompatibility](failures/model-version-incompatibility.md) | Routing pool treats model versions within a family as interchangeable despite differing feature support |

**Total: 6 patterns**

## Related Goals

- [Model Behavior and Capabilities](../model-behavior-and-capabilities/) — the behavior a request encounters once it has already been routed to a specific model
- [Model Updates and Versioning](../model-updates-and-versioning/) — what happens when the model a routing pool points to changes over time, rather than which model within a pool serves a given request
