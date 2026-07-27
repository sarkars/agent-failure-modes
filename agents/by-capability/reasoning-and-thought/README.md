# What Are the Most Common Reasoning and Thought Failures in AI Agents?

**Reasoning-and-thought failures happen because a language model's degradation is almost always soft and statistical rather than a hard error — the same fluent, confident response format covers a model silently exceeding its effective capacity, a router silently sending a request to the wrong model, and a provider silently retraining or swapping the model underneath an agent that never asked for a change.** None of the three failure surfaces below produce an exception the calling code can catch; each requires its own instrumentation, built by the team, to notice that something changed. That shared invisibility — not a shared cause — is what ties model-behavior degradation, routing mismatches, and version drift together as one capability area.

## Key Takeaways

- 3 goals and 23 patterns are documented here, spanning what happens once a model is already selected (Model Behavior and Capabilities), which model gets selected for a given request (Model Selection and Routing), and how the model a routing pool points to changes over time (Model Updates and Versioning).
- 5 of the 10 Model Behavior and Capabilities patterns are rated "Very Common" — degradation from context fill, instruction decay, stale knowledge, format instability, and unstated uncertainty are default production behavior, not edge cases.
- Model Selection and Routing failures cluster into compatibility gating, quality/health blind spots, and routing-consistency — all six patterns share one structural gap: a router's real-time feedback loop optimizes cost, latency, or liveness while capability match, task-representative health, and session continuity have no equivalent feedback loop wired in.
- Model Updates and Versioning failures show that reverting a bad model version is frequently slower than the original rollout: rollback routed through standard change approval takes several multiples longer than a code rollback on the same team, because the tooling doesn't distinguish an emergency revert from a new forward change.

## Reasoning and Thought Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Model Behavior and Capabilities](goals/model-behavior-and-capabilities/) | Degradation in a model's own output once it has already been selected and is serving a request — capacity limits, context-length decay, instruction/style drift, format and reasoning instability, stale knowledge, unstated uncertainty, and bias | 10 |
| [Model Selection and Routing](goals/model-selection-and-routing/) | Choosing which model or instance serves a given request — capability/version compatibility, health-blind cost optimization, and per-call routing consistency | 6 |
| [Model Updates and Versioning](goals/model-updates-and-versioning/) | How the model behind an agent changes over time — provider-driven retraining regressions, detection gaps, pin-vs-float tradeoffs, and rollback speed | 7 |

**Total: 23 patterns**

## How the Goals Relate

Model Behavior and Capabilities, Model Selection and Routing, and Model Updates and Versioning describe three different moments in a request's relationship to "which model, behaving how." Model Selection and Routing determines which model instance a request lands on. Model Behavior and Capabilities describes what that specific model does once it has the request — how it degrades as a session lengthens, as context fills, or as task complexity grows. Model Updates and Versioning sits outside any single request: it describes how the model a routing pool points to, or the model instance behavior already documented, can itself change over time — through a provider's retraining cycle, a pinned snapshot's expiration, or a floating alias silently resolving to different weights. The three goals are parallel concerns more than a strict pipeline, though they compound: a version change (Model Updates and Versioning) can shift the exact behavioral characteristics documented under Model Behavior and Capabilities, and a routing layer (Model Selection and Routing) that doesn't track version compatibility is exposed to both. To localize an incident by symptom: a single model call behaving inconsistently or degrading over a long session → **Model Behavior and Capabilities**; a request landing on a model that can't serve it, or inconsistent model choice across calls → **Model Selection and Routing**; behavior that changed with no code, prompt, or config change on the team's own side → **Model Updates and Versioning**.

## Frequently Asked Questions

### What is the difference between Model Selection and Routing and Model Updates and Versioning?
Model Selection and Routing is about which model within an available pool serves a given request right now — a router choosing between models or instances based on cost, capability, or load. Model Updates and Versioning is about how the model or pool itself changes over time — a provider retraining a version, deprecating a pinned snapshot, or swapping a floating alias underneath the team. A routing decision can be perfectly correct today and still be undermined tomorrow if the model version it points to changes.

### How do you distinguish a model-behavior problem from a model-versioning problem when debugging a regression?
Check whether anything on the team's own side changed. If code, prompts, and configuration are unchanged but output quality shifted, start with [Model Updates and Versioning](goals/model-updates-and-versioning/) — specifically [Silent Model Update](goals/model-updates-and-versioning/failures/silent-model-update.md), which documents exactly that signature. If the same model version has always behaved a given way and the issue tracks with session length, context fill, or task complexity, it's a [Model Behavior and Capabilities](goals/model-behavior-and-capabilities/) pattern instead.

### Can better prompting fix the failures documented across all three goals?
Rarely on its own. The patterns here are structural — a fixed-position system prompt losing relative influence as a transcript grows, a router with no capability-compatibility gate, a provider retraining against a different objective than any single customer's task — and the documented mitigations are architectural: periodic re-injection of critical instructions, explicit compatibility gates before cost optimization, task-specific regression suites re-run on every version candidate, and pre-authorized rollback paths, rather than a single better-worded prompt.

### Which goal should be checked first when a production agent's output quality drops unexpectedly?
Check [Model Updates and Versioning](goals/model-updates-and-versioning/) first if there's no corresponding change in the team's own deploy history, since provider-side version changes are invisible to normal code-change monitoring. If a deploy history does explain a recent change, or the degradation correlates with session length or task complexity rather than a specific date, [Model Behavior and Capabilities](goals/model-behavior-and-capabilities/) is the more likely source.

## Related Categories

- [Knowledge Retrieval](../knowledge-retrieval/) — a parallel set of failure surfaces (retrieval, synthesis, freshness) that compound with reasoning-and-thought issues whenever an agent's context is retrieved rather than purely parametric
- [Document Processing](../document-processing/) — production-reliability and orchestration failures that share the same "degrades silently, no error returned" shape documented across reasoning-and-thought's model-behavior patterns
