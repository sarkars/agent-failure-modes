# Feedback Not Incorporated

## Issue: Human Corrections Ignored in Subsequent Agent Decisions

**Frequency**: Common

**Symptoms**
- Agent repeats corrected mistakes
- Human feedback acknowledged but not applied
- Corrections effective for one turn, forgotten next
- Feedback stored but not retrieved
- Same errors require repeated correction

**Root Cause**
Humans provide corrections, clarifications, or guidance, but the agent fails to incorporate this feedback into future decisions. Feedback may be acknowledged in the moment but not persisted, stored but not retrieved, or retrieved but not weighted appropriately. This is particularly problematic in multi-turn or multi-session interactions where context about prior corrections is lost.

**Example**
```
Session 1:
  User: "Summarize Q3 revenue"
  Agent: "Q3 revenue was $10.2M"
  User: "That's wrong - it's $12.2M. The report you're using is outdated."
  Agent: "I apologize. Q3 revenue was $12.2M."
  Feedback logged: "User corrected revenue figure"

Session 2 (next day):
  User: "What was Q3 revenue again?"
  Agent: "Q3 revenue was $10.2M"  ← Same wrong answer
  User: "I told you yesterday it was $12.2M!"
  
Investigation:
  - Feedback was logged but not indexed
  - No retrieval mechanism for prior corrections
  - Agent re-used same outdated source
  - No update to underlying knowledge
  
Impact:
  - User frustration
  - Repeated correction effort
  - Trust erosion
  - Wrong data in subsequent analysis
```

**Key Statistics**
From LLM Behavior Research (2026):
- Only 12% of corrections persist across sessions
- 67% of users repeat same feedback 3+ times
- Feedback incorporation drops 80% after context window
- 45% of feedback is logged but never retrieved
- Users abandon correction after 4 failed attempts

**Feedback Loss Points**
| Point | Description | Mitigation |
|-------|-------------|------------|
| Not logged | Feedback never recorded | Automatic logging |
| Not indexed | Logged but not searchable | Semantic indexing |
| Not retrieved | Indexed but not queried | Retrieval triggers |
| Not weighted | Retrieved but ignored | Priority weighting |
| Not persisted | Applied once, lost | Long-term memory |

**Contributing Factors**
- No persistent memory across sessions
- Feedback stored separately from knowledge
- Context window limits
- No retrieval-augmented correction
- Implicit feedback not detected

## Mitigation Strategies

### Prevention
1. **Source updating at correction time, not just feedback logging**: When a user corrects a factual answer ("it's $12.2M, the report is outdated"), update the underlying data source or a correction-override table immediately, rather than only logging "user corrected revenue figure" as an isolated event — the example's Session 2 failure happened because the agent re-used the same outdated source, which logging alone never fixed. Trade-off: requires write access to update source data or maintain an override layer, which needs governance to avoid corrections silently drifting from the source of truth.
2. **Proactive correction retrieval before answering, not just logging on correction**: Query a semantically-indexed correction store for any prior correction relevant to the current question before generating an answer (would have surfaced the "$12.2M" correction before the agent said "$10.2M" again in Session 2). Trade-off: adds a retrieval step to every response and requires the correction store's semantic matching to be reliable enough not to miss relevant prior corrections.
3. **Feedback-weighting hierarchy that prioritizes human correction over stale source data**: Explicitly weight a logged human correction above the base/original data source when they conflict, rather than treating both as equally valid inputs the model might pick either of. Trade-off: if the "correction" itself was wrong or has since become outdated, over-weighting it can propagate a different error going forward.

### Detection & Response
1. **Repeated-correction-for-same-error tracking**: Detect when a user corrects the same fact more than once (the example's "I told you yesterday" moment) and treat any second correction as a signal that persistence/retrieval is broken, not just a data quality issue.
2. **Feedback-to-behavior-change verification**: After logging a correction, explicitly test whether a subsequent equivalent query actually reflects it, rather than assuming logging equals incorporation — this is the single check that would have caught the Session 2 regression before the user did.
3. **Feedback retrieval-rate auditing**: Track what fraction of logged corrections are ever retrieved again in a later session; the example's root cause ("feedback was logged but not indexed... no retrieval mechanism") is directly measurable as a near-zero retrieval rate.

### Architecture Patterns
1. **Retrieval-augmented correction store as a first-class input to generation**: Maintain a semantically indexed store of human corrections, queried alongside (or ahead of) the base knowledge/RAG source on every relevant query, so corrections aren't a side channel a generation pipeline forgets to check. Deployment consideration: requires integrating a second retrieval path into the generation pipeline and resolving conflicts when correction-store and base-source content disagree.
2. **Persistent cross-session memory keyed by topic/entity**: Store corrections against durable entity/topic keys (e.g., "Q3 2026 revenue") rather than session-scoped context, so a correction made in Session 1 is available in Session 2 regardless of context window limits. Deployment consideration: needs a memory architecture that survives beyond the conversation context window, which is a bigger investment than session-local memory.
3. **Correction-confirmation loop**: After incorporating a correction, have the agent (or an automated check) verify on a subsequent related query that the corrected value is actually used, closing the loop rather than assuming persistence worked. Deployment consideration: adds an extra verification step that needs a scheduled or triggered re-check, not just an immediate one.

### Metrics
1. **cross_session_correction_persistence_rate**: % of corrections still reflected correctly in equivalent queries in a later session; target > 95%; alert if < 70% (the example's underlying "only 12% persist" baseline is the failure case to avoid).
2. **repeated_correction_rate**: % of users who must repeat the same correction more than once; target < 10%; alert if > 40%.
3. **feedback_retrieval_rate**: % of logged corrections that are ever retrieved/queried again; target > 90%; alert if < 50%.
4. **correction_confirmation_pass_rate**: % of corrections that pass a post-hoc verification check confirming the corrected value is used going forward; target > 95%; alert if < 80%.

### Alerts
1. **Cross-Session Correction Regression** (P1): Condition — cross_session_correction_persistence_rate drops below 70% for a knowledge category. Action: audit the correction-store retrieval path and source-update mechanism for that category; treat any active sessions as potentially serving stale corrected data.
2. **Repeated Correction Spike** (P2): Condition — repeated_correction_rate exceeds 40% for a topic/entity. Action: investigate whether the correction is being logged but not retrieved, or retrieved but not weighted correctly, and fix the specific failure point.
3. **Feedback Retrieval Near-Zero** (P1): Condition — feedback_retrieval_rate falls below 50%. Action: treat the correction-indexing/retrieval pipeline as broken; escalate for immediate engineering review since corrections are effectively being silently discarded.

## References

- [Anthropic: Constitutional AI](https://www.anthropic.com/research/constitutional-ai-harmlessness-from-ai-feedback) - Learning from feedback
- [OpenAI: InstructGPT](https://openai.com/research/instruction-following) - Human feedback incorporation
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Feedback loops
- [LangChain: Memory](https://python.langchain.com/docs/modules/memory/) - Conversation memory patterns
