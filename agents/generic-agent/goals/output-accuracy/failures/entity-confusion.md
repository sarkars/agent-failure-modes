# Entity Confusion

## Issue: Agent Confuses Similar Entities

**Frequency**: Common

**Symptoms**
- Attributes of one entity applied to another
- People with similar names confused
- Companies with similar names mixed up
- Products or versions conflated

**Root Cause**
Entities with similar names, contexts, or attributes can be confused, especially when context doesn't clearly disambiguate.

**Example**
```
User: "Tell me about Michael Jordan the statistician"

Agent: "Michael Jordan is famous for his incredible basketball 
career with the Chicago Bulls..."

Reality: Michael I. Jordan is a renowned statistician and ML researcher

Result: Completely wrong information about wrong person
```

**Mitigation Strategies**
1. **Entity disambiguation**: Ask for clarification when ambiguous
2. **Full identifiers**: Use full names, IDs, or unique identifiers
3. **Context anchoring**: Include disambiguating context
4. **Explicit confirmation**: Confirm entity before providing details
5. **Entity linking**: Connect mentions to canonical entities
6. **Domain awareness**: Use domain context to disambiguate

**Detection**
- Track entity confusion errors in user feedback
- Monitor disambiguation query rates
- Test with deliberately ambiguous entities
- Compare entity attributes to authoritative sources
