# Context-Window Loss Reopens Already-Cleared Component in Long Investigation

## Issue: During a Long-Running Incident Investigation Conducted as a Single Extended Conversation, an Incident-Response Agent Rules Out a Component as the Cause Early in the Investigation Based on Specific Evidence, but as the Conversation Grows That Earlier Finding Falls Out of Its Effective Context, and It Later Re-Investigates or Re-Blames the Same Already-Cleared Component, Contradicting Its Own Prior Analysis

**Frequency**: Occasional

**Symptoms**
- The agent's later-turn root-cause hypothesis names a component it explicitly ruled out earlier in the same investigation conversation, with no acknowledgment that this contradicts its own prior finding
- Asking the agent directly, late in the investigation, "did we already check this component?" produces an answer indicating it does not recall the earlier check, even though the check and its result are present earlier in the same conversation
- Re-running the later-turn hypothesis generation with the earlier clearing finding explicitly re-stated in the prompt (rather than relying on it persisting from earlier turns) produces a hypothesis that correctly excludes the cleared component, isolating context loss as the cause
- The reopening concentrates in investigations that run long, with many tool calls and intermediate findings, where the volume of intervening content is largest relative to the model's effective attention to earlier turns
- Engineers waste investigation time re-verifying a component that was already conclusively cleared, extending time-to-resolution for the actual root cause

**Root Cause**
A long incident investigation conducted as a single extended conversation accumulates enough intervening tool calls, metric pulls, and partial hypotheses that an earlier, conclusively established finding can fall outside the portion of the conversation the model effectively attends to, even within nominal context-window limits. When the "this component is cleared" finding exists only as a natural-language statement in an earlier turn, rather than as a persistent, structured record the agent explicitly re-reads before generating each new hypothesis, the failure mode does not distinguish between a finding that was never made and one that was made and then effectively forgotten.

**Example**
```
Turn 6: Agent checks the message-queue consumer lag, finds it normal, and explicitly states "Queue consumer lag is within normal range; ruling out the queue as a contributing factor"
Turns 7-22: Sixteen more turns investigate database connection pooling, downstream API latency, and a recent config change, none of which conclusively explain the incident
Turn 23: Agent, running low on other hypotheses, proposes "Re-examining queue consumer lag as a likely cause," with no reference to the turn-6 finding that already ruled it out
Engineer spends time re-pulling the same queue metrics already checked sixteen turns earlier, confirming the same "normal" result, before redirecting the investigation
Time-to-resolution is extended by the redundant re-investigation of an already-cleared hypothesis
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts and constraints as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Multi-agent LLM orchestration for incident response is evaluated specifically against deterministic, high-quality decision support, underscoring that consistent retention of intermediate findings is a known gap relative to structured investigation tracking | [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on conversational context alone causes earlier-established facts to be dropped in long-running sessions | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- Cleared hypotheses exist only as natural-language statements within the investigation conversation, with no structured "ruled out" ledger maintained independently of conversation length
- Later-turn hypothesis generation re-reads the full conversation history rather than a structured, explicitly maintained list of already-cleared components
- No automated check flags when a newly proposed hypothesis names a component already marked cleared earlier in the same investigation

---

## Mitigation Strategies

1. **Structured Ruled-Out Ledger**: Maintain a structured, persistent record of every component or hypothesis explicitly cleared during the investigation, separate from the conversational transcript, and require new hypothesis generation to check against this ledger
2. **Pre-Hypothesis Contradiction Check**: Before proposing a new hypothesis, automatically check it against the ruled-out ledger and surface an explicit contradiction warning if the proposed hypothesis names an already-cleared component, rather than silently proceeding
3. **Investigation-Length Threshold Triggers Ledger Re-Injection**: Once an investigation exceeds a defined number of turns or tool calls, require the ruled-out ledger to be explicitly re-injected into the agent's context on every subsequent turn rather than relying on it persisting from earlier in the conversation
4. **Periodic Findings Summary Checkpoint**: At regular intervals during a long investigation, require the agent to explicitly restate all cleared and open hypotheses for human visibility, surfacing any internal inconsistency before it leads to redundant re-investigation

### Metrics
- Rate of hypotheses proposed that name a component already marked cleared earlier in the same investigation
- Time lost to redundant re-investigation of already-cleared hypotheses, aggregated per incident
- Percentage of long (above-threshold) investigations with an active, explicitly maintained ruled-out ledger

### Alerts
- Agent proposes a hypothesis naming a component already marked cleared in the same investigation's ledger → P2
- An investigation exceeds the turn-count threshold without a ruled-out ledger being re-injected into context → P3
- Redundant re-investigation time across incidents exceeds baseline for two consecutive reporting periods → P3

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
