# Tool Output Misinterpretation

## Issue: Agent Misunderstands Tool Response

**Frequency**: Common

**Symptoms**
- Agent extracts wrong value from tool output
- Array interpreted as single item
- Null/empty confused with failure
- Units or formats misunderstood

**Root Cause**
- Ambiguous or complex tool output formats
- Missing context about output structure
- Agent assumptions about output schema
- Inconsistent output formats across tools

**Example**
```
Tool response: { 
  "users": [
    { "name": "Alice", "balance": 100 },
    { "name": "Bob", "balance": 200 }
  ],
  "total_balance": 300
}

Agent interpretation: "The user has a balance of 300"

User asked about: Alice's balance (100)

Result: Agent reports wrong balance
```

**Mitigation Strategies**
1. **Structured output schemas**: Document output format clearly
2. **Field-level descriptions**: Explain what each field means
3. **Consistent formatting**: Use same patterns across all tools
4. **Output validation prompts**: Have agent confirm interpretation
5. **Type hints in responses**: Include units, formats explicitly
6. **Few-shot output examples**: Show how to parse responses

**Detection**
- Track interpretation accuracy vs. ground truth
- Monitor user corrections of agent's tool interpretations
- Log cases where agent re-queries for clarification
- Compare agent's extracted values to raw output
