# Model Context Length Behavior Change

## Issue
As an agent's conversation or retrieved context grows toward the model's context window limit, the model's behavior shifts in ways that are never announced: recall of early-turn facts degrades, instruction-following becomes less reliable, and the model increasingly favors recently-seen tokens over earlier ones ("recency bias"). Because the API returns a normal, well-formed response at every context length, the agent has no signal that it just crossed into a degraded-quality regime.

**Frequency**: Very Common

**Symptoms**
- Facts or instructions established early in a long session stop being honored once the transcript grows large, even though they were never contradicted
- Answer quality on "recall a detail from turn 3" questions drops sharply once the transcript passes roughly 60-70% of the model's advertised context window
- The same retrieval-augmented query returns better-grounded answers when the retrieved context is trimmed, despite more context nominally being available
- Model paraphrases or subtly alters facts from the middle of a long context ("lost in the middle") while reproducing facts near the start or end more faithfully
- No error or warning is returned as the context fills; degradation is only visible through output quality review

## Root Cause
Transformer attention does not treat all positions in a long context equally in practice, even though the architecture is nominally position-agnostic up to its trained window. Models are trained on a token-length distribution skewed toward shorter sequences, and instruction-tuning data rarely exercises very long, dense contexts with critical facts scattered throughout — so behavior optimized and evaluated at short context lengths doesn't hold uniformly as length increases. Positions in the middle of a long context receive measurably less effective attention than the beginning (which anchors the model's overall framing) or the end (which is closest to the generation point), producing the well-documented "lost in the middle" effect. Because the provider's API contract only guarantees that some completion is returned within the advertised token limit — not that quality is constant across that range — there is no built-in mechanism to surface the degradation to the calling agent.

## Example
```
A support agent holds a 45-turn troubleshooting conversation with a customer.
At turn 4, the customer states their account tier: "Enterprise, ID acct_8842."
By turn 38, the transcript has grown to roughly 28,000 tokens inside a
32,000-token context window.

At turn 39, the customer asks for a refund estimate, which depends on their
tier. The model answers as if the customer were on the Standard tier —
the default it falls back to when the tier fact, now buried in the middle
of a long transcript, isn't reliably retrieved.

The agent has no mechanism to detect this: the response is fluent, contains
a plausible-looking (wrong) number, and no API-level signal indicates that
context length degraded recall. The error surfaces only when the customer
disputes the refund amount.
```

## Statistics
| Finding | Context |
|---------|---------|
| Recall accuracy for facts placed in the middle third of a long context is typically 20-40 percentage points lower than for facts at the start or end | Estimated from "needle in a haystack" style internal evaluations across context lengths |
| Instruction-following on system-level rules stated early in a transcript degrades noticeably once transcript length exceeds roughly 60-70% of the advertised context window | Typical range observed across long-conversation agent evaluations |
| Trimming irrelevant middle content from retrieved context (rather than including everything available) improves answer grounding by an estimated 15-25% in RAG pipelines | Estimated from comparisons of full-context vs. curated-context retrieval |

## Mitigations
1. **Context budget monitoring**: Track transcript/context token count as a fraction of the model's window and treat crossing a calibrated threshold (e.g. 60%) as a signal to summarize, prune, or restructure rather than keep appending.
2. **Critical-fact pinning**: Re-inject key facts (account tier, constraints, user identity) near the end of the context on each turn rather than relying on the model to retrieve them from early in a long transcript.
3. **Periodic summarization and compaction**: Replace older turns with a compact summary once the conversation grows past a length threshold, keeping critical facts salient without relying on raw-transcript recall.
4. **Retrieval curation over context maximization**: In RAG pipelines, actively rank and trim retrieved passages instead of stuffing the full context window, since more context does not reliably mean better recall.
5. **Position-aware evaluation before deployment**: Test the deployed model's recall and instruction-following at multiple context fill levels (25%, 50%, 75%, 90%) rather than only at short-context conditions, and calibrate context budgets to the level where quality holds.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| context_fill_ratio | Current context tokens as a fraction of the model's advertised window | Alert if p95 > 0.7 |
| early_turn_fact_recall_rate | Sampled accuracy of recalling facts established early in long sessions | Alert if < 85% |
| mid_context_answer_accuracy_delta | Accuracy difference between facts placed at context start/end vs. middle | Alert if delta > 15 percentage points |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Context fill threshold exceeded | context_fill_ratio crosses 70% mid-session | Medium | Trigger summarization/compaction, re-pin critical facts |
| Recall regression detected | Sampled QA on early-turn facts falls below accuracy floor | High | Flag session for review, investigate context management strategy |

## Related Patterns
- [Model Capacity Limits](./model-capacity-limits.md) - both are soft ceilings on effective model performance that produce no explicit error signal
- [Model Instruction Following Decay](./model-instruction-following-decay.md) - context length growth is one of the primary mechanisms driving instruction decay over a session
- [Model Uncertainty Unawareness](./model-uncertainty-unawareness.md) - degraded recall from context fill is presented with the same false confidence as any other uncertain answer
