# Context-Window Loss Drops Earlier-Expressed Frustration in Long Chat Before Escalation Decision

## Issue: A Sentiment-Escalation Agent Evaluating a Long Support Chat for Whether to Escalate Bases Its Decision Primarily on the Tone of the Most Recent Exchanges, and Strongly Negative Sentiment the Customer Expressed Earlier in the Same Chat Falls Out of Effective Context by the Time the Escalation Decision Is Generated, So an Escalation-Warranting Chat Is Left Unescalated Because the Customer's Tone Happened to Flatten in the Final Exchanges

**Frequency**: Frequent

**Symptoms**
- Early in a long chat, the customer expresses strong frustration or anger, and the agent's in-the-moment sentiment classification correctly flags it as negative
- After many more exchanges in which the customer's tone becomes flatter or more transactional (often because they have resigned themselves to a slow process), the escalation agent's final decision evaluates the chat as not warranting escalation
- Re-running the escalation decision with the early strongly negative exchange explicitly re-included in the prompt changes the decision to escalate, isolating context loss as the cause rather than the agent judging the early frustration as resolved
- Auditing chats not escalated under this pattern shows the customer's overall satisfaction score, measured independently, is as low as or lower than chats that were correctly escalated
- The unescalated outcome concentrates on the longest pre-decision chats, where many intervening transactional exchanges separate the customer's early expressed frustration from the agent's final escalation evaluation

**Root Cause**
A long chat that accumulates many intermediate, lower-affect exchanges between an early strongly negative statement and the final escalation-decision point creates enough intervening content that the earlier statement can fall outside the portion of the conversation the model effectively weighs, even though it remains technically within the context window. Because the chat's most negative moment is not captured as a persistent, structured field the escalation-decision step explicitly checks, the decision is driven disproportionately by the tone of the most recent exchanges rather than by the chat's actual peak severity.

**Example**
```
Chat begins: "I am extremely upset, this is the third time this has happened and I'm about to cancel my subscription"
Over the next twenty exchanges, the agent walks the customer through a multi-step diagnostic process; the customer's responses become short and flat ("ok", "did that", "still not working") as they tire of the process
Escalation-decision step evaluates the chat's recent tone as low-intensity and frustrated-but-cooperative, concluding escalation is not warranted
Customer cancels their subscription within the hour, citing the original complaint that was never actually addressed by a human
Post-cancellation review finds the chat's peak negative-sentiment statement, made at the very start, was never weighed in the escalation decision
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts and signals as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Language models exhibit measurable performance degradation in using information located in the middle portions of a long context relative to information near the beginning or end | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Studies of multi-agent LLM system failures identify loss of an earlier-established signal across an extended interaction, rather than its explicit revision, as a distinct and recurring failure category separate from misclassification at any single point | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |

**Contributing Factors**
- The chat's peak negative-sentiment moment exists only as a fact stated in an earlier turn, with no structured, persistent "peak severity" field maintained independently of conversation length
- The escalation-decision step evaluates recent conversational tone rather than an explicitly maintained, structured record of the chat's most severe sentiment moment
- No automated check cross-references the escalation decision against the chat's full sentiment history before concluding escalation is not warranted

---

## Mitigation Strategies

1. **Structured Peak-Severity Field**: Maintain a structured, persistent field recording the chat's most negative sentiment moment and its content, separate from the conversational transcript, and require the escalation decision to weigh this field explicitly rather than relying on recent-turn tone alone
2. **Escalation Decision Anchored to Peak, Not Recency**: Require the escalation-decision logic to evaluate the chat's peak sentiment severity alongside its most recent tone, rather than allowing recent flattening to override an earlier severe signal
3. **Conversation-Length Threshold Triggers Field Re-Injection**: Once a chat exceeds a defined number of exchanges, require the structured peak-severity field to be explicitly re-injected into context before generating the escalation decision
4. **Post-Decision Sentiment-History Audit**: Automatically flag any "no escalation" decision on a chat whose structured peak-severity field indicates a strongly negative moment occurred earlier in the same chat, routing it to human review

### Metrics
- Rate of "no escalation" decisions on chats with a structured peak-severity field indicating an earlier strongly negative moment
- Independently measured customer satisfaction score for unescalated chats under this pattern versus correctly escalated chats
- Cancellation or churn rate following an unescalated chat with an earlier strongly negative moment

### Alerts
- A "no escalation" decision is made on a chat whose structured peak-severity field records a strongly negative moment earlier in the same chat → P2
- Cancellation within a defined window follows an unescalated chat with a recorded earlier strongly negative moment → P1
- Rate of peak-severity-overridden-by-recency decisions exceeds the defined threshold for a rolling window → P2

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
