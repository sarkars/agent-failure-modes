# Follow-Up Context Loss

## Issue: Agent Doesn't Maintain Context Across Conversation Turns

**Frequency**: Common

**Symptoms**
- Pronouns not resolved from previous turns
- Topic switches not detected
- Previous answers not built upon
- User must re-explain context each turn

**Root Cause**
RAG retrieval happens per-turn without incorporating conversation history. Follow-up queries lack context for proper retrieval.

**Example**
```
Turn 1: "What are the features of Product X?"
Agent: [Good answer about Product X features]

Turn 2: "How much does it cost?"
Query sent to retrieval: "How much does it cost?"

Missing context: "it" = Product X

Retrieved: Generic pricing documentation
Agent: "Pricing varies by product. Which product are you interested in?"

Result: Context lost, user frustrated by repetition
```

**Mitigation Strategies**
1. **Query rewriting**: Resolve pronouns before retrieval
2. **Conversation memory**: Include relevant history in context
3. **Topic tracking**: Maintain current topic state
4. **Coreference resolution**: Explicitly resolve "it", "this", "that"
5. **Session-aware retrieval**: Filter by session context
6. **History summarization**: Compress relevant history into query

**Detection**
- Track pronoun usage in follow-up queries
- Monitor context-loss related clarifications
- Measure answer quality degradation over turns
- Identify topic continuity breaks
