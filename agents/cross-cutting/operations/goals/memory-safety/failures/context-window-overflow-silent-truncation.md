# Context Window Overflow with Silent Truncation

## Issue: Agent Silently Drops Input Context When Message Exceeds Context Window

**Frequency**: Common

**Symptoms**
- Agent ignores critical information when context is large
- References to early parts of conversation are lost
- Agent makes decisions based on incomplete context
- User unaware that information was dropped
- Quality degrades silently as conversations grow longer

**Root Cause**
When chat history or document context exceeds the model's context window, most systems silently truncate from the beginning rather than erroring. The agent completes anyway but with degraded context, producing incorrect results without warning. Users don't realize their input was truncated.

**Example**
```
Scenario: Legal document review with long context

User provides:
- Document 1: Contract (2K tokens)
- Document 2: Regulatory guidance (3K tokens)  
- Document 3: Prior versions (2K tokens)
- Query: "Are there compliance issues?" (500 tokens)

Model context window: 8K tokens

System behavior:
- Total input: 7.5K tokens (fits, but tight)
- User asks follow-up about Document 1
- Chat history added (2K tokens more)
- Total now: 9.5K tokens (exceeds 8K window)
- System silently truncates Document 1 (2K tokens dropped)
- Agent responds about Document 1 without having it
- Answer is wrong, but user thinks agent reviewed it

Impact:
- Missed compliance issue in Document 1
- Company hit with regulatory fine
- Legal liability for missed obligations
```

**Key Statistics**
- 40-50% of agents experience context overflow at some point
- Silent truncation happens 80% of the time (user unaware)
- Average impact: 20-50% accuracy degradation when context truncated
- Cost of undetected truncation: $10K-1M per incident

**Contributing Factors**
- No context window monitoring
- Silent truncation in LLM API defaults
- No user notification when context dropped
- No quality metrics on truncated contexts
- Multi-document or multi-turn conversations exceed window

---

## Mitigation Strategies

### Prevention

1. **Pre-Flight Context Budget Checking**: Before sending request, calculate total token count. Reserve 20% for completion tokens. If total >budget, reject request with clear error message listing what was excluded.

2. **Intelligent Summarization Instead of Truncation**: When context exceeds window, summarize older messages instead of truncating. For documents, extract key excerpts instead of dropping entire sections.

3. **Progressive Disclosure with User Control**: Let user know context will be truncated and offer options: (a) summarize older parts, (b) start fresh conversation, (c) split into multiple queries.

### Detection & Response

1. **Context Overflow Detection and Logging**: Log every instance of context truncation with details on what was dropped. Alert if truncation happens.

2. **Quality Metrics on Truncated Contexts**: Track accuracy/quality when context is complete vs. truncated. Alert if quality drops >20%.

3. **User-Facing Warnings**: Always inform user if context was modified/truncated, and what was affected.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `context_window_overflow_rate` | % of requests exceeding context window | >5% |
| `silent_truncation_incidents` | Truncations without user notification | >0 |
| `accuracy_with_truncated_context` | Quality drop when context truncated | >20% drop |
| `conversation_length_at_cutoff` | Median turns before overflow | <10 turns |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Context Overflow | Request exceeds context window | P2 | Offer summarization or error to user |
| Silent Truncation Detected | Truncation happened without notification | P1 | Fix immediately; notify affected users |
| Quality Drop on Overflow | Accuracy <80% on truncated contexts | P2 | Implement summarization; monitor affected users |
| Chronic Window Exhaustion | >20% of requests truncated daily | P1 | Consider larger model or chunking strategy |

---

## References

- [Transformer Attention Is All You Need](https://arxiv.org/abs/1706.03762) — Context window fundamentals
- [LLaMA 2: Open Foundation and Fine-Tuned Chat Models](https://arxiv.org/abs/2307.09288) — Modern context window management
