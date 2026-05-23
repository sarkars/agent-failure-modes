# Lost Conversation State

## Issue: Agent Loses Track of Conversation State

**Frequency**: Common

**Symptoms**
- Agent forgets decisions made earlier
- Repeats questions already answered
- Contradicts previous statements
- Can't recall multi-turn workflow progress

**Root Cause**
- State information buried in long history
- No explicit state tracking mechanism
- Context truncation drops state information
- Agent doesn't maintain working memory

**Example**
```
Turn 3: User: "Let's call it Project Alpha"
Turn 5: Agent proceeds with "Project Alpha"
Turn 15: Agent: "What would you like to name the project?"

User: "I told you - Project Alpha"
Agent: "Ah yes, let's proceed with Project Alpha"

Result: User frustrated by repetition
```

**Mitigation Strategies**
1. **Explicit state tracking**: Maintain structured state object
2. **State summarization**: Periodically summarize current state
3. **Key-value memory**: Store important facts in retrievable format
4. **State validation**: Check state consistency before proceeding
5. **Progressive disclosure**: Track what's been discussed/decided
6. **State persistence**: Store state outside context window

**Detection**
- Track repeated questions
- Monitor for contradictions with earlier statements
- Alert on state inconsistencies
- Log state reconstruction attempts
