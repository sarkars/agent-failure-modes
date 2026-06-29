# Context-Window Loss Drops Earlier Disqualifying Signal in Long Nurture Thread

## Issue: A Lead-Scoring Agent Re-Scoring a Lead Based on the Full Multi-Touch Nurture Conversation History Loses Track of an Early-Stated Disqualifying Signal ("Not in Market for 12 Months," "No Budget Authority") Once the Thread Grows Long Enough to Push That Signal out of the Portion of Context the Model Weighs Most Heavily, and Re-Scores the Lead High Based on Recent, More Engaged-Sounding Messages Alone

**Frequency**: Occasional

**Symptoms**
- A lead is re-scored as high-priority based on recent positive engagement (opened emails, attended a webinar), even though an early message in the same nurture thread explicitly stated a disqualifying signal -- "we're not evaluating solutions until next fiscal year" -- that was never retracted
- The agent's scoring rationale references only the most recent several messages in the thread, with no mention of the earlier disqualifying statement, even when that statement is still present in the full conversation history passed to the model
- Re-scoring the same lead with the early disqualifying message moved to the end of the context window (rather than its original chronological position) changes the score, indicating the omission is a function of position within the context rather than the model judging the signal irrelevant
- The miss concentrates on nurture threads that have grown long enough (many touches over an extended period) to separate the disqualifying signal from the most recent messages by a wide margin, since shorter threads do not exhibit the same drop rate
- Sales reps report wasted outreach effort on leads "promoted" by a rescoring pass that, on manual review of the full thread, contains an unretracted disqualifying statement the rep would have caught immediately

**Root Cause**
Large language models exhibit degraded ability to retrieve and weight information located in the middle or earlier portions of a long context window relative to information near the most recent turns, especially in extended multi-turn conversations. When a lead-scoring agent re-scores based on an accumulated nurture thread, an early disqualifying statement competes with many subsequent, more recent messages for the model's attention, and as the thread grows, the early statement's influence on the score degrades even though it remains technically present in the input and was never retracted by the lead.

**Example**
```
Lead states in touch #2 of a nurture sequence: "Just so you know, we're not evaluating solutions until next fiscal year -- feel free to keep us on the newsletter though"
Lead continues opening marketing emails and attends a product webinar over the following four months, generating touches #3 through #14 in the same nurture thread
Lead-scoring agent re-scores the lead using the full accumulated thread as context, and the resulting score reflects only the recent engagement signals from touches #10-14, with the touch #2 disqualifying statement absent from the scoring rationale
Lead is promoted to high-priority and routed to an AE, who spends a call confirming the lead reiterates the same "not until next fiscal year" position stated four months earlier, a fact the rescoring pass had access to but did not weigh
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Large language model performance degrades substantially in multi-turn conversational settings, with models losing track of information established earlier in the conversation as the number of turns grows | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Language models exhibit a positional bias in long-context settings, retrieving and weighting information located in the middle of the context substantially less reliably than information near the beginning or end | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Leading LLM agents on realistic CRM tasks show systematic gaps in multi-turn settings relative to single-turn settings, reflecting degraded ability to integrate information across an extended interaction history | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |

**Contributing Factors**
- The scoring agent re-processes the full accumulated nurture thread as undifferentiated context rather than maintaining a separately tracked, persistent flag for disqualifying statements once made
- No structured "disqualification" field is extracted and pinned outside the raw conversation history at the time the disqualifying statement is first made, leaving it to compete for attention with all subsequent messages
- Long nurture threads are exactly the case most likely to trigger the failure, since they are also the threads most likely to contain genuine re-engagement signals that make a high re-score plausible on its face

---

## Mitigation Strategies

1. **Extract and Pin Disqualification Flags Outside Raw Context**: When a lead states a disqualifying signal, extract it into a structured, persistent flag stored separately from the raw conversation history, so it does not compete with later messages for positional weight in a long context window
2. **Require Explicit Disqualification-Flag Check Before Promotion**: Before any rescoring pass can promote a lead to high-priority, require an explicit check against the structured disqualification-flag store, blocking promotion until any unretracted flag is surfaced and reviewed
3. **Chunked Re-Summarization for Long Threads**: For nurture threads exceeding a defined length, periodically summarize the thread into a structured running record (with disqualifying statements preserved verbatim) rather than relying on the model to weigh the full raw history evenly on each rescoring pass
4. **Position-Sensitivity Backtest**: Periodically test the scoring agent by moving known disqualifying statements to different positions within otherwise identical synthetic threads, measuring whether the score changes based on position alone

### Metrics
- Rate of leads promoted to high-priority that, on full-thread audit, contain an unretracted disqualifying statement earlier in the thread
- Score sensitivity to the positional location of a known disqualifying statement within an otherwise identical thread, measured via position-sensitivity backtest
- Average nurture-thread length (touch count) at which the disqualification-flag drop rate begins increasing materially

### Alerts
- A lead is promoted to high-priority while an unretracted disqualification flag exists in the structured flag store → P1
- Position-sensitivity backtest shows a score change greater than the defined threshold attributable to disqualifying-statement position alone → P2
- Rate of AE-reported "lead reiterated known disqualifying statement" feedback on promoted leads exceeds baseline → P2

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
