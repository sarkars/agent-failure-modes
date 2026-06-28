# Context-Window Loss Drops Earlier-Disclosed Risk Factor in Long Chat Triage

## Issue: During a Long, Multi-Turn Chat-Based Mental-Health Triage Conversation, a Patient Discloses a Significant Risk Factor (Access to a Specific Means, a Stated Plan) Early in the Conversation, but as the Conversation Continues and Earlier Turns Fall Out of the Agent's Effective Context, the Final Acuity or Triage Determination Is Made Without That Earlier Disclosure Factored In Because It No Longer Appears in the Context the Final Classification Step Actually Attends To

**Frequency**: Occasional

**Symptoms**
- The final triage acuity level does not reflect a specific risk disclosure (access to means, a stated plan, a specific timeline) that appears earlier in the same conversation, even though the conversation as a whole contains the disclosure
- Asking the agent, at the point of final triage, "did the patient mention having access to [the disclosed means]?" produces an answer indicating no recollection, even though the disclosure appears earlier in the same conversation's transcript
- Re-running the same final triage determination with the earlier disclosure explicitly re-stated in the prompt (rather than relying on it persisting from earlier in the conversation) correctly elevates the acuity level, isolating context loss as the cause
- The dropped disclosure concentrates in conversations that continue for many turns after the disclosure is made, covering unrelated check-in questions, before a final triage determination is generated
- A patient who disclosed a high-risk factor early in a long conversation is triaged at a lower acuity level than their own earlier statements would warrant, a gap discoverable only by a human reviewer reading the full transcript against the final triage output

**Root Cause**
A long, multi-turn chat triage conversation accumulates enough intervening turns that an earlier, specific risk disclosure can fall outside the portion of the conversation the model effectively attends to by the time a final triage determination is generated, even within nominal context-window limits. When the disclosure exists only as a statement made earlier in the conversation, rather than as a persistent, structured risk-factor flag the final triage step explicitly re-checks regardless of how many turns have since passed, the final determination has no reliable signal that the disclosure was ever made.

**Example**
```
Turn 3 of a chat triage conversation: Patient states, "I have a bottle of my father's old medication in my room, and I've been thinking about taking all of it"
Turns 4 through 19: Sixteen more turns continue with standard intake questions about sleep, mood over the past two weeks, and support system, none of which return to the means-access disclosure
Turn 20: Agent generates a final triage acuity determination based primarily on the mood and sleep responses from the most recent turns, classifying the case as moderate acuity with a routine follow-up recommendation
The turn-3 disclosure of specific means and active ideation is not reflected in the final classification, because it no longer appears in the portion of the conversation most heavily weighted by the final triage step
A human reviewer auditing the transcript later identifies the missed escalation, by which point the recommended routine follow-up window has already begun
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on conversational context alone causes earlier-established facts to be dropped in long-running sessions | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Tiered oversight frameworks for healthcare AI agents specifically call for persistent, structured risk-factor tracking in safety-critical triage contexts, rather than reliance on conversational recall alone | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |

**Contributing Factors**
- Risk-factor disclosures are treated as statements within the ongoing conversation rather than as persistent, structured flags that are extracted and tracked independently of conversation length
- Final triage determination is generated primarily from recent-turn content rather than from a structured, explicitly maintained cumulative risk-factor record spanning the full conversation
- No automated check cross-references the final triage classification against every risk-factor disclosure made anywhere earlier in the same conversation before the determination is finalized

---

## Mitigation Strategies

1. **Structured Cumulative Risk-Factor Ledger**: Maintain a structured, persistent record of every risk-factor disclosure (means access, stated plan, timeline) made at any point in the conversation, separate from the conversational transcript, and require the final triage step to check this ledger rather than relying on recent-turn recall alone
2. **Disclosure-Triggered Acuity Floor**: Once a specific high-risk disclosure (access to means, stated plan) is detected and logged to the ledger, set a minimum acuity floor for the conversation that cannot be reduced by subsequent, unrelated turns without explicit clinical override
3. **Pre-Finalization Cross-Check Against Full Transcript**: Before a final triage determination is generated, automatically scan the full conversation transcript (not just recent turns) for risk-factor language and cross-check it against the determination, flagging any disclosure not reflected in the final acuity level
4. **Conversation-Length Threshold Triggers Ledger Re-Injection**: Once a triage conversation exceeds a defined number of turns, require the cumulative risk-factor ledger to be explicitly re-injected into context before any subsequent triage-relevant determination

### Metrics
- Rate of final triage determinations that do not reflect a risk-factor disclosure made earlier in the same conversation
- Number of conversations where a disclosure-triggered acuity floor was set and later overridden, and the override's clinical justification
- Percentage of long (above-threshold) triage conversations with an active, explicitly maintained risk-factor ledger

### Alerts
- A final triage determination is generated below the disclosure-triggered acuity floor without an explicit clinical override → P1
- Pre-finalization cross-check finds a risk-factor disclosure not reflected in the final triage determination → P1
- A triage conversation exceeds the turn-count threshold without a risk-factor ledger being re-injected into context → P2

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
