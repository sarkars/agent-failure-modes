# What Are the Most Common Model-Behavior Failures in AI Agents?

**A model's behavior degrades without any error being returned because degradation in LLMs is almost always a soft, statistical ceiling rather than a hard limit — the API still returns a fluent, well-formed response at every level of context fill, conversation length, or task complexity, so nothing in the response itself signals that quality just dropped.** All 10 model-behavior-and-capabilities patterns describe a different axis along which degradation happens: task complexity exceeding effective capacity, context filling up, instructions and persona eroding over a long session, knowledge going stale, output format becoming unstable, reasoning becoming inconsistent, refusal boundaries becoming porous, and the model's own confidence signal being decoupled from its actual accuracy.

## Key Takeaways

- 10 patterns are documented here, and every one shares the same core symptom structure: a normal-looking, confident response with no built-in signal that anything degraded.
- 5 of the 10 patterns are rated "Very Common" (Context Length Behavior Change, Instruction Following Decay, Knowledge Cutoff, Output Format Instability, Uncertainty Unawareness) — the five are not edge cases but default production behavior.
- Three patterns (Context Length Behavior Change, Instruction Following Decay, Style Drift) share the identical root mechanism: a fixed-position system prompt or early-turn fact loses relative influence as the conversation transcript grows, and none of the three are announced by the model.
- Reported effect sizes are large where measured: constraint-adherence rates drop from ~95% to 60-75% past 7-8 simultaneous constraints (Capacity Limits); recall accuracy for mid-context facts runs 20-40 points below start/end-of-context facts (Context Length Behavior Change); rule adherence in 30+ turn conversations runs 20-35 points below the first 5 turns (Instruction Following Decay).

## Scope

- **Session-Length Decay** — [Model Context Length Behavior Change](failures/model-context-length-behavior-change.md), [Model Instruction Following Decay](failures/model-instruction-following-decay.md), [Model Style Drift](failures/model-style-drift.md). All three are driven by the same mechanism: a system prompt or early fact is fixed in position while the conversation grows around it, so its relative influence on the next generated token shrinks — degrading recall, rule-following, and persona/tone in that order as the transcript lengthens.
- **Call-to-Call Nondeterminism** — [Model Capacity Limits](failures/model-capacity-limits.md), [Model Output Format Instability](failures/model-output-format-instability.md), [Model Reasoning Inconsistency](failures/model-reasoning-inconsistency.md), [Model Refusal Inconsistency](failures/model-refusal-inconsistency.md). The four call-to-call-nondeterminism patterns describe the same logical request producing different results across runs or under trivial surface variation (option order, phrasing, sampling draw, task density) — one call's output isn't a reliable function of the input's actual logical content.
- **Silent Knowledge & Judgment Gaps** — [Model Knowledge Cutoff](failures/model-knowledge-cutoff.md), [Model Uncertainty Unawareness](failures/model-uncertainty-unawareness.md), [Model Fairness Bias](failures/model-fairness-bias.md). The three silent-knowledge-and-judgment patterns describe a gap between what the model appears to know or judge fairly and what it actually knows or judges fairly, delivered with the same confident tone regardless of the underlying gap.

## When Model Behavior & Capabilities Matters

- An agent runs long conversations or sessions (support chat, ongoing troubleshooting) where rules, persona, or early facts need to hold for the full session, not just the first few turns
- A pipeline depends on the model reliably following a strict output contract (JSON schema, a fixed set of constraints) across a high volume of calls, where even a low per-call failure rate compounds at scale
- A decision pipeline (screening, triage, risk scoring) uses model judgment on inputs where demographic proxies, stale facts, or borderline calls could silently bias or miscalibrate the outcome

## Cross-Pattern Insight

Every mitigation across all 10 patterns follows the same shape: don't trust the generating call's own signal of success, and instrument something external to check it. For session-length decay, that means periodic re-injection of the system prompt or critical facts rather than assuming a single system-prompt statement holds for an entire session. For call-to-call nondeterminism, that means self-consistency sampling, order-randomization testing, or constrained decoding rather than trusting a single pass. For silent knowledge/judgment gaps, that means mandatory retrieval grounding for time-sensitive facts, counterfactual fairness testing, and structured confidence elicitation rather than trusting the model's own hedging language, which the model-behavior patterns show doesn't reliably correlate with actual accuracy.

## Frequently Asked Questions

### Can the model just say when it's uncertain or when a task is too complex for it?
Per [Model Uncertainty Unawareness](failures/model-uncertainty-unawareness.md), confident, declarative phrasing is simply a more common surface pattern in training data than hedged phrasing, and RLHF has historically reinforced confident phrasing because human raters tend to prefer complete-sounding answers. The model's internal token-probability distribution does encode a form of uncertainty, but that isn't reliably linked to the surface language it chooses to use.

### Is instruction-following decay the same thing as style drift?
They share a root cause — a fixed-position system prompt losing influence as the transcript grows — but affect different things. [Model Instruction Following Decay](failures/model-instruction-following-decay.md) is about rule compliance (a forbidden topic, a formatting requirement); [Model Style Drift](failures/model-style-drift.md) is about persona and tone specifically. Both patterns document that periodic re-injection of the original instruction restores compliance temporarily before it decays again.

### Can prompting alone fix reasoning inconsistency or refusal inconsistency?
No — both patterns show reasoning inconsistency and refusal inconsistency are properties of autoregressive sampling and learned decision boundaries, not something a single better-worded prompt eliminates. [Model Reasoning Inconsistency](failures/model-reasoning-inconsistency.md) recommends self-consistency sampling (multiple runs, majority vote) for high-stakes decisions; [Model Refusal Inconsistency](failures/model-refusal-inconsistency.md) recommends a deterministic policy layer independent of the model's own judgment for well-defined categories, rather than relying on the generative model as the enforcement point.

### How much does context length actually have to fill before quality drops?
[Model Context Length Behavior Change](failures/model-context-length-behavior-change.md) reports instruction-following degradation becoming noticeable once transcript length exceeds roughly 60-70% of the model's advertised context window, with recall for mid-context facts running 20-40 percentage points below facts placed at the start or end (the "lost in the middle" effect).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Model Capacity Limits](failures/model-capacity-limits.md) | Task complexity/constraint count exceeds the model's effective per-call reasoning capacity, so it silently drops or deprioritizes constraints |
| [Model Context Length Behavior Change](failures/model-context-length-behavior-change.md) | Recall and instruction-following degrade as the context window fills, worst for facts in the middle of a long context |
| [Model Fairness Bias](failures/model-fairness-bias.md) | Statistical associations from training data leak demographic bias into scores/decisions with no explicit discriminatory instruction |
| [Model Instruction Following Decay](failures/model-instruction-following-decay.md) | System-prompt rule adherence drops as a conversation lengthens, even though the prompt never changes |
| [Model Knowledge Cutoff](failures/model-knowledge-cutoff.md) | Facts frozen at training time are stated with the same confidence as current facts, with no built-in staleness signal |
| [Model Output Format Instability](failures/model-output-format-instability.md) | Strict format compliance (JSON/XML) holds most of the time but deviates intermittently under sampling variance |
| [Model Reasoning Inconsistency](failures/model-reasoning-inconsistency.md) | Logically identical inputs differing only in superficial ways (order, phrasing) produce different reasoning and conclusions |
| [Model Refusal Inconsistency](failures/model-refusal-inconsistency.md) | Refusal boundaries are porous to paraphrase, framing, and sampling variance rather than a robust semantic rule |
| [Model Style Drift](failures/model-style-drift.md) | A configured persona/tone is followed early in a session and gradually fades toward a generic default voice |
| [Model Uncertainty Unawareness](failures/model-uncertainty-unawareness.md) | Low-confidence or fabricated content is phrased with the same declarative certainty as well-established facts |

**Total: 10 patterns**

## Related Goals

- [Model Selection and Routing](../model-selection-and-routing/) — failures in choosing which model serves a request, upstream of the behavior model-behavior-and-capabilities documents once a model is already selected
- [Model Updates and Versioning](../model-updates-and-versioning/) — how the same behavioral characteristics can shift unannounced when the provider ships a new model version
