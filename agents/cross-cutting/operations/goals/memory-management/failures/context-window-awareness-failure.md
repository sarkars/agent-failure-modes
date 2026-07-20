# Context Window Awareness Failure

## Issue
An agent has no internal tracking of how much of its context window is currently consumed, so as the session grows — tool outputs, retrieved documents, prior turns — early content gets silently truncated or evicted by the underlying context-management layer without the agent ever registering that it happened. The agent continues to reason as if everything it was told earlier is still available, producing answers that ignore or misremember instructions, constraints, or facts that were established at the start of the session and have since fallen out of the window.

**Frequency**: Very Common

**Symptoms**
- Agent contradicts or ignores an instruction given earlier in the same session with no acknowledgment that it forgot it
- Agent re-asks for information the user already provided at session start
- Behavior changes abruptly partway through a long session with no corresponding change in user input
- No warning or degradation signal is surfaced to the user before early context is dropped
- Session-length correlates with drop in adherence to early-session constraints, but the agent itself never flags approaching a limit

## Root Cause
The agent's reasoning process operates purely on whatever tokens happen to be present in the current prompt; it has no first-class signal for "how full is my context window" or "what have I already lost." Context truncation/eviction is typically handled by an external harness (sliding window, FIFO drop, or opaque compaction) that runs independently of the model's own reasoning, so the model is never in the loop when eviction decisions are made — it simply receives a shorter prompt on the next turn and has no memory that anything is missing, because the thing that would remind it (the evicted content itself) is exactly what's gone. Without an explicit token-budget tracker feeding back into the agent's own planning, the agent cannot proactively summarize, checkpoint, or ask for clarification before losing information — it can only fail silently after the fact.

## Example
```
Session budget: 32,000 tokens. Turn 1 establishes a hard constraint:
"Never suggest expedited shipping — it's against our sustainability
policy for this account."

Turns 2-38: agent processes 37 customer order requests, each pulling
in product catalog data, shipping options, and prior turn history.
By turn 24 (~31,500 tokens), the context-management layer begins
silently dropping the oldest turns to stay under budget. Turn 1,
containing the shipping constraint, is evicted.

Turn 31: user asks, "Can you expedite this order? It's urgent."
Agent: "Sure, I've selected expedited shipping for this order."

The constraint was violated not because the agent chose to
override it, but because it no longer had any way of knowing
the constraint had ever been stated — and neither the agent
nor the harness surfaced a warning that early context had been
dropped.
```

## Statistics
| Finding | Context |
|---------|---------|
| Adherence to early-session constraints typically drops sharply once session token count approaches 80-90% of the context window in unmanaged sliding-window setups | Typical range observed in long-session agent evaluations |
| Sessions without any token-budget tracking or checkpointing show measurably higher rates of "forgotten instruction" complaints than sessions with periodic explicit re-statement | Reported range across teams comparing tracked vs. untracked sessions |
| Adding an explicit remaining-budget signal to agent planning reduces silent early-context loss incidents by a substantial margin in instrumented evaluations | Estimated from before/after comparisons in teams that added budget tracking |

## Mitigations
1. **Explicit token-budget tracking**: Feed the agent's own planning loop a running count of tokens used and remaining, so it can reason about approaching limits rather than being surprised by them.
2. **Checkpoint critical constraints**: Re-inject hard constraints and key facts periodically (e.g. every N turns or every X tokens) rather than relying on them surviving from turn one for the entire session.
3. **Eviction warnings**: Have the context-management layer emit a visible signal (to the agent and/or the user) when it evicts content, rather than silently shortening the prompt.
4. **Pinned/protected context regions**: Mark critical instructions and constraints as non-evictable, separate from the general sliding window of conversational history.
5. **Proactive summarization before eviction**: Trigger a summarization pass that extracts key facts into a compact, protected form before the raw content ages out of the window, instead of letting eviction happen with no extraction step.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| context_utilization_pct | Fraction of context window currently consumed, tracked per session | Alert if > 90% without a checkpoint triggered |
| silent_eviction_count | Number of times content was dropped from context without an explicit eviction signal reaching the agent | Alert if > 0 for sessions with pinned constraints |
| early_constraint_violation_rate | Rate at which a constraint established in the first N turns is violated later in the same session | Alert if > 5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Context window near capacity | context_utilization_pct exceeds 90% with no checkpoint/summarization triggered | High | Force a checkpoint/summarization pass, re-inject pinned constraints |
| Pinned constraint evicted | A marked non-evictable instruction is no longer present in the active context | High | Halt session, re-inject constraint, alert engineering |

## Related Patterns
- [Context Coherence Loss](./context-coherence-loss.md) - silent eviction is one of the primary mechanisms that produces internally inconsistent context
- [Memory Summarization Lossy](./memory-summarization-lossy.md) - the compaction step that should catch evicted content before it's lost is itself prone to dropping needed detail
- [Context Refresh Stale State](./context-refresh-stale-state.md) - both involve the agent trusting context content without visibility into how that content was produced or maintained
