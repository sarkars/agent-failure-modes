# Multi-Part Query Fragmentation

## Issue: Agent Only Addresses Part of Multi-Part Question

**Frequency**: Common

**Symptoms**
- Only first question in query answered
- Later parts of question ignored
- User must re-ask for remaining parts
- Incomplete response to compound question

**Root Cause**
Model attention focuses on early parts of query, or retrieval optimizes for one part, missing others.

**Example**
```
Query: "What are the system requirements, pricing tiers, and 
implementation timeline for the Enterprise plan?"

Agent response: "The Enterprise plan requires minimum 16GB RAM, 
4-core CPU, and 100GB storage. The software runs on Windows, 
Mac, and Linux."

Missing:
- Pricing tiers (not mentioned)
- Implementation timeline (not mentioned)

Result: User must ask two more times for complete answer
```

**Mitigation Strategies**
1. **Query decomposition**: Split multi-part queries into sub-queries
2. **Checklist approach**: Enumerate parts, ensure each addressed
3. **Structured responses**: Use sections for each query part
4. **Coverage verification**: Check all query components in answer
5. **Sequential retrieval**: Retrieve for each part separately
6. **Answer completeness prompt**: "Ensure you address all parts"

**Detection**
- Parse queries for multiple question marks or conjunctions
- Compare query parts to answer coverage
- Track follow-up queries for missing parts
- Measure multi-part query completion rate
