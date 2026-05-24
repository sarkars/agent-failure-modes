# Context Window Overflow

## Issue: Task Exceeds Context Window Limits

**Frequency**: Common

**Symptoms**
- Agent loses track of earlier conversation
- Important instructions forgotten mid-task
- Cross-references in documents not resolved
- Agent asks for information already provided

**Root Cause**
Every LLM has a context window limit. When conversations, documents, or tool outputs exceed this limit, information must be dropped or summarized, leading to information loss.

**Example**
```
Turn 1: User provides 50-page specification
Turn 5: User asks about requirement on page 3
Agent: "I don't see that requirement in our conversation. Could you 
remind me what it was?"

Reality: Requirement was in context but truncated to fit window

Result: User must re-provide information, frustrated
```

**Mitigation Strategies**
1. **Context prioritization**: Keep important information, summarize rest
2. **Sliding window**: Recent turns + pinned important context
3. **Retrieval augmentation**: Index content, retrieve on demand
4. **Smart chunking**: Process large documents in meaningful sections
5. **Context budgeting**: Allocate tokens to different purposes
6. **Summarization**: Compress history while preserving key facts

**Detection**
- Monitor context window utilization
- Track "forgotten information" errors
- Alert when approaching context limits
- Log truncation events

---

## References

- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow as top failure mode
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Context limitations in multi-agent systems
