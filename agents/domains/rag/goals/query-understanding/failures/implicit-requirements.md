# Implicit Requirements Missing

## Issue: Agent Misses Unstated but Expected Aspects of Query

**Frequency**: Common

**Symptoms**
- Answer technically correct but practically useless
- Obvious related information not included
- User must ask follow-ups for expected information
- Context assumptions not surfaced

**Root Cause**
Users have expectations beyond literal query. They assume agent will provide complete, actionable information including obvious implications.

**Example**
```
Query: "Can I use this software on my Mac?"

Agent: "Yes, the software supports macOS."

Implicit requirements not addressed:
- Which macOS versions?
- Apple Silicon or Intel?
- Any limitations vs. Windows?
- How to install on Mac?

User: "Great, but which versions? I have an M1 Mac with Monterey."

Result: Multiple follow-ups needed for basic question
```

**Mitigation Strategies**
1. **Query expansion**: Add common related questions
2. **Completeness prompting**: "Include common follow-up information"
3. **FAQ pairing**: Match query to common question patterns
4. **Anticipatory retrieval**: Retrieve for likely follow-ups
5. **Template responses**: Ensure standard info included
6. **User modeling**: Know what this user type typically needs

**Detection**
- Track predictable follow-up queries
- Monitor information completeness scores
- Analyze query chains for implicit requirements
- User feedback on answer completeness

## References

- [Atlan: LLM Hallucinations 2026](https://atlan.com/know/llm-hallucinations/) - Implicit expectations
- [Mindee: RAG Hallucinations Explained](https://www.mindee.com/blog/rag-hallucinations-explained) - Completeness expectations
