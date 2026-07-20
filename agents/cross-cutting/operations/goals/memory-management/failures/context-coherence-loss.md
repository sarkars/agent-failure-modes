# Context Coherence Loss

## Issue
Over a long-running session, an agent's live working context (the conversation buffer, scratchpad, and accumulated tool outputs for the current run) comes to contain multiple, mutually contradictory statements about the same fact — an earlier tool result, a superseded plan, or a value that later changed — with no mechanism marking any of them as authoritative. Unlike long-term memory-store conflicts, which surface across sessions, this happens entirely within one continuous run: partial compaction, tool retries, and branching sub-tasks leave old and new versions of the same fact co-resident in context, and the model attends to whichever is more salient rather than resolving the conflict.

**Frequency**: Very Common

**Symptoms**
- Agent gives self-contradictory answers within the same turn or across adjacent turns
- Agent cites a value, decision, or plan step that was explicitly superseded earlier in the same session
- Two tool outputs from different points in the run disagree and neither is treated as stale
- Final summary of a session mixes an early draft state with the actual final state
- Self-contradiction rate rises measurably as session length/turn count increases

## Root Cause
Context is fundamentally an append-only transcript; nothing in a standard agent loop automatically marks a fact as superseded when a later action updates it. There is no explicit "current value of X" variable — the model infers the current state from whichever mention is most recent, most prominent, or most recently attended to. In long sessions this breaks down: retries re-run a tool and produce a second, possibly different result without removing the first; a sub-task branches and reports back a locally-scoped conclusion that contradicts the parent task's assumption; partial context compaction evicts the reconciling explanation ("the first count was wrong because...") but leaves both raw numbers behind. With no reconciliation step, the agent effectively holds two beliefs at once and picks one at random depending on prompt position and recency bias.

## Example
```
Turn 4: Agent calls check_inventory("SKU-4471") -> "12 units in stock"
        Agent begins drafting a fulfillment plan assuming 12 units.

Turn 9: A different sub-task re-checks inventory after a warehouse
        transfer completes -> check_inventory("SKU-4471") -> "3 units in stock"
        This result is appended to context; the turn-4 result is never
        marked stale or removed.

Turn 14: User asks, "Can we fulfill an order for 10 units of SKU-4471?"

Agent response:
"We have 12 units in stock, so yes we can fulfill 10 units.
 Note: a recent check also showed only 3 units remaining, so you
 may want to confirm before shipping."

The agent surfaces both numbers because both are present in context
with no marker indicating the second supersedes the first, leaving
the user to do the reconciliation the agent should have done.
```

## Statistics
| Finding | Context |
|---------|---------|
| Self-contradiction rate in agent transcripts roughly doubles once a session exceeds ~40 turns with repeated tool calls on the same entity | Typical range observed in long-session agent transcripts |
| An estimated 15-25% of long-session tool re-invocations produce a result that conflicts with an earlier result still present in context | Estimated from workflows with retry-heavy tool use |
| Adding an explicit "supersede" marker on repeated fact updates cuts observed self-contradictions by roughly half in evaluation transcripts | Reported range across teams instrumenting state tracking |

## Mitigations
1. **Explicit state variables**: Maintain a small structured "current facts" block (key-value, not prose) that tool results write into, overwriting rather than appending, so only one value per fact exists at any time.
2. **Supersession tagging**: When a new tool result updates a previously-established fact, tag the old mention as superseded (or strip it) rather than leaving both in context untouched.
3. **Conflict check before response**: Before finalizing an answer, have the agent scan its own context for contradictory mentions of entities referenced in the answer and resolve or flag them explicitly.
4. **Single source of truth for volatile facts**: For values that can change mid-session (inventory, prices, status), always re-fetch fresh at time-of-use rather than trusting an earlier in-context mention, and discard the earlier mention on refresh.
5. **Coherence-aware compaction**: When compacting context, prefer keeping the most recent value of a fact plus a one-line note that it was updated, over keeping both raw values with no relationship stated.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| self_contradiction_rate | Fraction of sessions where the agent states two conflicting values for the same tracked entity | Alert if > 5% |
| stale_fact_reference_rate | Fraction of final responses that reference a fact value known to have been superseded earlier in-session | Alert if > 3% |
| conflict_unresolved_rate | Fraction of detected in-context conflicts the agent surfaces without resolving | Alert if > 20% of detected conflicts |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Contradictory response shipped | Agent's final answer contains two different values for the same entity | High | Flag session for review, check compaction/state-tracking logic |
| Rising contradiction trend | self_contradiction_rate increases session-over-session for a given agent/workflow | Medium | Investigate recent changes to tool retry or compaction logic |

## Related Patterns
- [Context Window Awareness Failure](./context-window-awareness-failure.md) - context loss from silent eviction compounds coherence problems when the reconciling context is what gets dropped
- [Memory Inconsistency Between Agents](./memory-inconsistency-between-agents.md) - the cross-agent analogue of the same underlying problem: no single authoritative view of current state
- [Memory Summarization Lossy](./memory-summarization-lossy.md) - lossy compaction is one of the mechanisms that produces the stale, unreconciled mentions behind coherence loss
