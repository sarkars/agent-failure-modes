# Context-Window Loss Drops Reserved-Capacity Constraint in Multi-Day Forecast

## Issue: A Capacity-Planning Agent Operating Across a Multi-Day, Multi-Session Planning Conversation Establishes a Hard Constraint Early On (e.g., "Reserve 20% Headroom for the Upcoming Product Launch") That a Later Session's Recommendation Violates Because the Constraint Has Fallen Out of the Agent's Effective Context by the Time the Later Recommendation Is Generated

**Frequency**: Occasional

**Symptoms**
- A capacity recommendation generated in a later planning session allocates resources up to or beyond the limit that an earlier session explicitly reserved headroom against, with no acknowledgment that this conflicts with the earlier reservation
- Asking the agent, in the later session, "does this recommendation respect the headroom reserved for the launch?" produces an answer indicating no awareness of the earlier reservation, even though it was explicitly established in an earlier session of the same ongoing planning engagement
- Re-running the later recommendation with the headroom constraint explicitly re-stated in the prompt (rather than relying on it persisting from an earlier session) produces a recommendation that correctly respects the reservation, isolating context loss as the cause
- The violation surfaces in production only when the reserved event actually occurs and insufficient headroom remains, since the planning-stage conflict produced no error at recommendation time
- The gap concentrates on planning engagements that span many separate sessions over days or weeks, where the originating session establishing the constraint is least likely to remain in any single session's active context

**Root Cause**
Multi-day capacity-planning engagements are often conducted across separate conversational sessions rather than one continuous context, and even within a single long-running session, an earlier-established constraint can fall outside the model's effectively attended context as the conversation grows. When the reserved-headroom constraint exists only as a statement made in an earlier session or early in a long conversation, rather than as a persistent, structured planning constraint the agent explicitly re-reads before generating each new recommendation, later recommendations are generated with no signal that the constraint exists at all.

**Example**
```
Session 1 (Monday): Capacity-planning agent is told "Reserve 20% headroom on the order-processing cluster ahead of the product launch on the 15th," and confirms this constraint in its recommendation
Session 2 (Wednesday, separate conversation): Agent is asked to recommend rightsizing for the same cluster based on the past week's average utilization, with no mention of the launch reservation in this session's prompt
Agent recommends downsizing the cluster to match observed average utilization, consuming the headroom reserved on Monday, because the reservation exists only in Session 1's now-inaccessible context
Recommendation is applied; on the 15th, the launch traffic surge consumes available capacity faster than expected because the reserved headroom was never actually preserved
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on conversational context alone causes earlier-established constraints to be dropped across separate sessions | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts and constraints as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Automated infrastructure-reconciliation research on AI agents highlights state-vs-recommendation mismatch across separately invoked planning sessions as a recurring class of automation failure | [Automated Cloud Infrastructure-as-Code Reconciliation with AI Agents](https://arxiv.org/pdf/2510.20211) |

**Contributing Factors**
- Reserved-capacity constraints are established as natural-language statements within a single session rather than as a structured, persistent planning-constraint record consulted across sessions
- Later planning sessions generate recommendations from current utilization data alone, with no step that checks against a structured constraint ledger established in earlier sessions
- No automated check compares a new capacity recommendation against active reserved-headroom constraints before the recommendation is applied

---

## Mitigation Strategies

1. **Structured Capacity-Constraint Ledger**: Maintain a structured, persistent record of every active reserved-headroom or hard-capacity constraint, independent of any single session's conversational context, and require every new recommendation to be checked against it before being applied
2. **Pre-Recommendation Constraint Check**: Before any capacity recommendation is finalized, automatically check it against the active constraint ledger and block or flag the recommendation if it would violate a reserved-headroom constraint
3. **Constraint Expiration and Confirmation**: Require every reserved-capacity constraint in the ledger to carry an explicit expiration date (e.g., the day after the launch event) so constraints do not persist indefinitely, but also require explicit confirmation before a constraint is removed or modified
4. **Session-Start Constraint Re-Injection**: At the start of every new capacity-planning session, automatically re-inject the current active constraint ledger into context, rather than relying on the agent recalling constraints established in a prior session

### Metrics
- Rate of finalized capacity recommendations that violate an active reserved-headroom constraint
- Number of production capacity shortfalls traced to a planning-stage recommendation that silently consumed reserved headroom
- Percentage of new planning sessions that begin with the active constraint ledger re-injected into context

### Alerts
- A capacity recommendation is applied that violates an active reserved-headroom constraint in the ledger → P1
- A reserved-headroom constraint's expiration date passes without explicit confirmation that the reserved event has concluded → P3
- A new planning session generates a recommendation with no constraint ledger re-injected into context → P3

---

## References

- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Automated Cloud Infrastructure-as-Code Reconciliation with AI Agents](https://arxiv.org/pdf/2510.20211)
