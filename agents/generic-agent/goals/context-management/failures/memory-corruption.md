# Memory Corruption

## Issue: Agent's Long-Term Memory Becomes Corrupted

**Frequency**: Occasional

**Symptoms**
- Agent recalls facts that were never true
- Stored information differs from original
- Memory entries contradict each other
- Outdated information not updated

**Root Cause**
When agents store information to long-term memory:
- Summarization may lose or distort facts
- Overlapping updates may conflict
- No validation of stored content
- Memory poisoning through malicious inputs

**Example**
```
Original fact: "User's budget is $10,000"
Stored (summarized): "User budget is flexible, around $10K"
Later retrieved: "User has approximately $10,000 budget but flexible"
Used as: "User can go higher than $10,000"

Result: Agent makes recommendations exceeding actual budget
```

**Mitigation Strategies**
1. **Exact storage**: Store verbatim for critical facts
2. **Memory validation**: Verify before storing
3. **Versioned memory**: Track changes over time
4. **Source attribution**: Link memories to sources
5. **Periodic cleanup**: Review and correct stale memories
6. **Memory access control**: Restrict who can write memories

**Detection**
- Audit memory entries vs. sources
- Track memory modification history
- Alert on contradictory memories
- Validate critical facts before use
