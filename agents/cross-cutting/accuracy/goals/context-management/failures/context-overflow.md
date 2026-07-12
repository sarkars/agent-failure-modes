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

## Mitigation Strategies

### Prevention
1. **Context prioritization with pinned critical content**: Classify context into must-retain (explicit requirements, constraints, decisions) versus reference material, and pin the must-retain portion so it survives truncation/summarization regardless of window pressure, since the root cause is that once conversations or documents exceed the window, information is dropped or summarized indiscriminately rather than by importance. Trade-off: requires an explicit classification step (manual or automated) that itself consumes tokens and can misclassify content whose importance only becomes clear later in the conversation.
2. **Retrieval-augmented context loading**: Index large source documents (e.g., the 50-page specification) outside the context window and retrieve only the relevant sections on demand per turn, rather than holding the entire document in-context from turn one, so a later question about page 3 triggers a fresh, accurate retrieval instead of relying on whatever survived earlier truncation. Trade-off: retrieval quality depends on chunking/embedding quality, and a poorly-matched retrieval can miss the relevant section entirely, producing a different failure (silent gaps) rather than the original one.
3. **Context budgeting by purpose**: Allocate a fixed token budget to each category of context (system instructions, conversation history, retrieved documents, tool outputs) so no single category can silently consume the entire window and crowd out others, structurally preventing the scenario where document content displaces earlier requirements. Trade-off: rigid budgets can be wrong for a given task's actual needs, requiring per-workflow tuning rather than a single global setting.

### Detection & Response
1. **Context window utilization monitoring**: Track token usage against the model's window limit per turn, and trigger proactive summarization or retrieval hand-off before the window is exceeded rather than after truncation has already silently dropped content, since the failure is invisible to the user until they ask about something that's already gone.
2. **"Forgotten information" error tracking**: Log every instance where the agent claims not to have information the user believes was already provided (as in the example where the agent asks the user to re-state a requirement), and correlate these against context-utilization history at the time to confirm whether truncation was the cause.
3. **Truncation-event logging with content fingerprinting**: When content is dropped or summarized due to window pressure, log what was dropped (or a fingerprint/hash of it) so that later "forgotten information" incidents can be traced back to a specific truncation event rather than treated as unexplained agent error.

### Architecture Patterns
1. **Sliding window with pinned-context overlay**: Architect context management as a sliding window of recent turns combined with a separately-maintained, non-evictable set of pinned facts (key requirements, decisions, constraints extracted early), so recency pressure never displaces information the system has identified as durably important.
2. **External state store decoupled from the LLM context**: Maintain structured, queryable state (requirements, decisions, extracted facts) in a database or document store outside the context window entirely, with the agent querying it on demand, so window limits only affect conversational flow rather than the durability of task-critical information.
3. **Hierarchical summarization pipeline**: Architect a multi-tier summarization process (turn-level, session-level, document-level) that progressively compresses older content while preserving a pointer back to the original source, so a summarized fact can still be re-expanded or re-verified against the source document if a later question requires precision the summary lost.

### Metrics
1. **context_window_utilization_pct**: Target: proactive summarization triggered at 70-80% of window capacity; Alert when utilization exceeds 90% without a summarization/retrieval hand-off having occurred
2. **forgotten_information_rate**: Target: <1% of user turns require re-providing previously-given information; Alert on sustained increase
3. **truncation_event_rate**: Target: track as baseline per workflow type; Alert on truncation events affecting content flagged as high-importance
4. **retrieval_hit_rate**: Target: >95% of on-demand retrievals return the section relevant to the user's question; Alert if hit rate drops, indicating chunking/indexing degradation

### Alerts
1. **Context Window Near Capacity Without Mitigation** (P2): Condition - utilization exceeds 90% and no summarization or retrieval hand-off has triggered. Action: Force an immediate summarization pass or switch to retrieval mode before the next turn, notify the workflow owner if this recurs for the same task type.
2. **High-Importance Content Truncated** (P1): Condition - a truncation event drops content previously flagged as pinned/high-importance. Action: Restore the content from the external state store if available, alert the user that information may need to be re-confirmed, investigate why pinning failed.
3. **Repeated Forgotten-Information Incidents** (P3): Condition - forgotten_information_rate exceeds target for a given workflow over a rolling window. Action: Review that workflow's context budgeting and pinning configuration, consider moving it to retrieval-augmented loading.

---

## References

- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Context overflow as top failure mode
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Context limitations in multi-agent systems
