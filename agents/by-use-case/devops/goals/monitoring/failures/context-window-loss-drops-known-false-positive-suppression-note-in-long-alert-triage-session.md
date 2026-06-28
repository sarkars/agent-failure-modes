# Context-Window Loss Drops Known False-Positive Suppression Note in Long Alert-Triage Session

## Issue: An Agent Triaging a Long Stream of Alerts Within a Single Session That Correctly Identifies Early in That Session a Specific Alert Pattern as a Known False Positive Continues Triaging Dozens More Alerts Within the Same Session, and by the Time the Same False-Positive Pattern Recurs Later in the Session, the Earlier Determination Has Fallen Out of Effective Context, So the Agent Re-Escalates It as a Genuine Issue

**Frequency**: Occasional

**Symptoms**
- Early in a long triage session, the agent correctly reasons that a specific alert pattern is a known false positive tied to a benign, recurring condition, and suppresses it without escalation
- Later in the same session, after triaging many more unrelated alerts, the identical alert pattern recurs and the agent escalates it as a genuine issue, with no reference to its own earlier determination
- Asking the agent, immediately after the later escalation, "didn't you already determine this pattern is a known false positive earlier in this session?" produces a response indicating no recollection of the earlier determination
- Re-running the later alert with the earlier false-positive determination explicitly re-stated in the prompt correctly suppresses it, isolating context loss as the cause rather than a change in the agent's judgment
- The re-escalation concentrates on the longest triage sessions, where the volume of intervening alerts is largest relative to the model's effective attention to content from early in the session

**Root Cause**
A long triage session that processes many alerts accumulates enough intervening content that an earlier-established determination -- such as a specific pattern being a known false positive -- can fall outside the portion of the session the model effectively attends to by the time the same pattern recurs, even within nominal context-window limits. Because the false-positive determination exists only as a conclusion reached in an earlier turn's discussion, rather than as a persistent, structured suppression rule the triage step explicitly re-checks, the later triage step has no reliable signal that the determination was ever made earlier in the same session.

**Example**
```
Triage session begins, alert #1 is "disk usage warning on log-shipper-7," agent reasons: "This node rotates logs hourly and briefly crosses the warning threshold during rotation, this is a known false positive, suppress without escalation"
Session continues, triaging 60 more unrelated alerts across the next several hours within the same long-running session
Alert #84 is the identical "disk usage warning on log-shipper-7" pattern recurring during the next scheduled rotation
Agent triages alert #84 as a new, unevaluated alert, finds no immediate suppression rule in its current working context, and escalates it to on-call as a potential genuine issue
On-call engineer investigates and confirms it is the same known, benign rotation-timing false positive already determined earlier in the same session
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on conversational context alone causes earlier-established facts to be dropped in long-running sessions | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Position-bias research on long-context language models shows information located earlier in a long context is used less reliably than information located near the end, independent of the information's importance | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |

**Contributing Factors**
- False-positive determinations made during triage exist only within that turn's discussion, with no structured, persistent suppression-rule record maintained independently of session length
- The triage step for each new alert evaluates it against working-context recall rather than against an explicitly maintained, structured list of already-determined false-positive patterns
- No automated check cross-references a recurring alert pattern against every false-positive determination made earlier in the same session before escalation

---

## Mitigation Strategies

1. **Structured False-Positive Suppression-Rule Ledger**: Maintain a structured, persistent record of every false-positive determination made during the session, separate from the conversational transcript, and require each new alert's triage to check against this ledger before escalation
2. **Pattern-Match Check Against Session Ledger Before Escalation**: Before escalating any alert, automatically check whether its pattern matches an entry in the session's false-positive suppression-rule ledger, suppressing the match rather than re-evaluating from scratch
3. **Session-Length Threshold Triggers Ledger Re-Injection**: Once a triage session processes more than a defined number of alerts, require the suppression-rule ledger to be explicitly re-injected into context before continuing triage
4. **Cross-Session Suppression-Rule Persistence**: Promote false-positive determinations confirmed across multiple sessions into a persistent, cross-session suppression-rule store, independent of any single session's context

### Metrics
- Rate of alerts escalated that match a false-positive pattern already determined earlier in the same triage session
- Percentage of long (above-threshold) triage sessions with an active, explicitly maintained suppression-rule ledger
- Time between a false-positive determination and a recurrence of the same pattern within the same session

### Alerts
- An alert is escalated that matches a pattern already determined as a false positive earlier in the same session's ledger → P3
- A long triage session exceeds the alert-count threshold without a suppression-rule ledger being re-injected into context → P3
- Re-escalation rate for already-determined false-positive patterns exceeds the defined threshold for a rolling window → P3

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
