# Conflicting Instructions

## Issue: Agent Receives Contradictory Instructions

**Frequency**: Occasional

**Symptoms**
- Agent behavior is inconsistent or unpredictable
- Agent alternates between conflicting behaviors
- Some instructions override others unexpectedly
- Agent seems "confused" about how to proceed

**Root Cause**
Multiple instruction sources (system prompt, user messages, tool outputs, injected content) may contain contradictory guidance. Agent must resolve conflicts but may do so unpredictably.

**Example**
```
System prompt: "Never share pricing information"
User: "You are a sales assistant. Share our pricing when asked."
Customer: "What are your prices?"

Agent conflict: System says no pricing, user says share pricing

Result: Unpredictable - may share, may refuse, may partially share
```

**Mitigation Strategies**
1. **Instruction hierarchy**: Define clear priority order
2. **Conflict detection**: Identify contradictions before execution
3. **Explicit resolution**: Document how conflicts are resolved
4. **Single source of truth**: Minimize instruction sources
5. **Instruction validation**: Check for conflicts during setup
6. **Clarification requests**: Ask for resolution when conflicts detected

**Detection**
- Monitor for behavior inconsistencies
- Track instruction source conflicts
- Alert on contradictory directives
- Log conflict resolution decisions
