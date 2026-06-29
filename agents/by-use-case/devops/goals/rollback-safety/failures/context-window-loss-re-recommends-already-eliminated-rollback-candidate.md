# Context-Window Loss Re-Recommends Already-Eliminated Rollback Candidate

## Issue: During a Long-Running Single-Session Investigation Into Which of Several Recent Deploys to Roll Back, an Agent Rolls Back Component A Early in the Session, Explicitly Confirms in Its Own Output That the Regression Persists After A's Rollback (Ruling A Out as the Cause), but as the Session Continues Through Further Diagnosis of Components B and C, That Earlier Elimination Falls Out of Its Effective Context, and It Later Re-Recommends Rolling Back Component A Again as a Candidate Fix

**Frequency**: Occasional

**Symptoms**
- The agent's own transcript shows an explicit statement earlier in the session that Component A was rolled back and the regression persisted, ruling A out
- Later in the same session, after extended back-and-forth diagnosing other components, the agent proposes rolling back Component A again as if it were still a live candidate
- The contradiction is only visible by reading the full session transcript; a reviewer looking only at the latest recommendation would see a plausible-looking suggestion with no indication it was already tried and failed
- Re-rolling-back Component A wastes a deploy cycle and delays attention to the components that have not yet been ruled out
- The failure recurs specifically in incidents where the investigation session runs long (many tool calls, multiple component checks) rather than in short, quickly-resolved incidents

**Root Cause**
The agent's working context has finite effective attention, and specific factual conclusions established earlier in a long session -- such as "Component A's rollback did not resolve the regression" -- compete with substantial intervening content (logs, metric pulls, other components' diagnosis) for representation in what the model actually attends to when generating its next recommendation. Without an explicit, persistently-surfaced record of already-eliminated candidates separate from the general conversation history, the elimination is effectively forgotten even though it remains textually present earlier in the transcript.

**Example**
```
Incident: elevated error rate after a multi-service deploy window touching components A, B, and C
Turn 4: Agent recommends rolling back Component A first (most recently deployed); rollback executed
Turn 6: Agent confirms "Error rate unchanged after A's rollback; A is not the cause, ruling it out"
Turns 7-22: Agent works through extensive log analysis and metric correlation for Components B and C, including several false leads
Turn 23: Agent's final recommendation: "Recommend rolling back Component A, as its deploy timing is closest to the error spike onset"
Component A is rolled back a second time; error rate is unaffected (as already established at turn 6); the actual cause (Component C, never fully eliminated) continues
Incident duration extended by the redundant rollback cycle plus the time needed to notice the contradiction in the transcript
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long-context evaluation shows model attention to specific facts degrades non-uniformly across a long context, with facts stated earlier becoming less influential on later outputs as intervening content accumulates | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Multi-turn conversational evaluation finds LLM agents lose track of earlier-established constraints and conclusions as conversations extend, producing outputs inconsistent with their own earlier turns | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Research on agent memory mechanisms identifies the absence of a persistent, explicitly-surfaced record of resolved sub-decisions (as distinct from raw conversation history) as a recurring driver of contradictory long-session behavior | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- No persistent, explicitly-maintained list of "eliminated rollback candidates" separate from the general conversation transcript
- Long investigation sessions accumulate substantial intervening content between an elimination and a later recommendation, diluting the elimination's effective weight
- No automated consistency check compares each new recommendation against prior explicit conclusions in the same session before it is surfaced to the on-call engineer
- Incident pressure favors fast recommendations, leaving no built-in pause to re-read and reconcile against earlier session conclusions

---

## Mitigation Strategies

1. **Persistent Elimination Ledger**: Maintain a structured, explicitly-surfaced list of already-tried-and-ruled-out rollback candidates, separate from raw conversation history, that is checked before any new candidate is recommended
2. **Contradiction Check Before Recommendation**: Automatically diff each new rollback recommendation against the elimination ledger and block or flag any recommendation that re-proposes an already-eliminated candidate
3. **Session Summarization Checkpoints**: Periodically re-inject a compact summary of confirmed eliminations and remaining candidates into the agent's active context during long investigations, rather than relying on the full raw transcript
4. **Independent Session Audit on Long Incidents**: For investigations exceeding a configurable turn or duration threshold, require a fresh re-statement of the candidate list and elimination status before any further rollback action is taken

### Metrics
- Rate of rollback recommendations that re-propose a candidate already marked eliminated earlier in the same session
- Mean session length (turns or duration) at which contradictory re-recommendations begin to appear
- Number of redundant rollback executions per incident

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Redundant rollback recommendation | New recommendation matches an entry in the elimination ledger | P1 | Block recommendation; surface elimination ledger to on-call before proceeding |
| Long-session drift | Investigation exceeds turn/duration threshold without a re-stated candidate summary | P2 | Force checkpoint summarization before further action |
| Contradiction detected post-hoc | Transcript audit finds a re-proposed eliminated candidate that was not caught live | P3 | Review and patch elimination-ledger enforcement |

---

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
