# Context Stuffing

## Issue: Overloading Context with Irrelevant Information

**Frequency**: Common

**Symptoms**
- Large documents included when only snippets needed
- Entire conversation history passed every turn
- All available tools described regardless of relevance
- System prompts bloated with unused instructions

**Root Cause**
- "Just in case" inclusion of information
- No relevance filtering before context inclusion
- Static system prompts not adapted to task
- Fear of missing needed context

**Example**
```
Task: "What's the weather in NYC?"

Context included:
- 50-page user manual
- Full conversation history (100 turns)
- All 200 available tools
- Complete company knowledge base

Actual need: Weather API tool + location

Result: 100,000 tokens used, 500 needed
```

**Mitigation Strategies**
1. **Relevance filtering**: Only include task-relevant context
2. **Dynamic tool loading**: Load tools based on detected intent
3. **Document chunking**: Include only relevant sections
4. **Conversation pruning**: Summarize or drop old turns
5. **Tiered system prompts**: Core + task-specific instructions
6. **Lazy loading**: Fetch context only when needed

**Detection**
- Measure context utilization (tokens used vs. tokens referenced)
- Track task completion rate vs. context size
- A/B test minimal vs. full context
- Monitor which context sections are actually used
