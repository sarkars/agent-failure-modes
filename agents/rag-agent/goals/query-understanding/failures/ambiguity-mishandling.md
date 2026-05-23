# Ambiguity Mishandling

## Issue: Agent Guesses Instead of Clarifying Ambiguous Queries

**Frequency**: Very Common

**Symptoms**
- Agent picks one interpretation without acknowledging others
- User gets answer to wrong question
- No clarification requested for ambiguous terms
- Confident answer to ambiguous query

**Root Cause**
Models are trained to provide helpful responses, not to admit uncertainty or ask for clarification. Ambiguous queries get resolved silently.

**Example**
```
Query: "What's the Mercury policy?"

Possible interpretations:
- Mercury (the planet) research policy
- Mercury (the element) safety policy  
- Mercury Insurance company policy
- Mercury car model warranty policy

Agent: "Mercury Insurance offers comprehensive coverage with 
a standard deductible of $500..."

User intent: Was asking about mercury (element) disposal policy

Result: Completely wrong topic addressed
```

**Mitigation Strategies**
1. **Ambiguity detection**: Identify queries with multiple valid interpretations
2. **Clarification prompts**: Ask user to specify when ambiguous
3. **Interpretation listing**: "Did you mean X or Y?"
4. **Context utilization**: Use conversation history to disambiguate
5. **Confidence thresholds**: Don't answer if interpretation confidence low
6. **Multi-interpretation answers**: Address multiple possibilities

**Detection**
- Track clarification request rates
- Monitor user corrections after answers
- Identify common ambiguous terms
- Measure answer relevance for ambiguous queries
