# Conflicting Information

## Issue: Conflicting Information Across Document Locations

**Frequency**: Common

**Symptoms**
- Same field appears in multiple places with different values
- Agent picks arbitrary or first occurrence
- No reconciliation or flagging of conflicts

**Root Cause**
Long documents may contain draft values, amendments, corrections, or simple errors resulting in the same information appearing multiple times with conflicting values.

**Example**
```
Input: 150-page contract
Page 3: "Contract Value: $500,000"
Page 47 (Amendment A): "Revised Contract Value: $475,000"
Page 98 (Final Terms): "Total Contract Value: $475,000 + $25,000 bonus = $500,000"

Agent extraction: "$500,000" (grabbed first occurrence)

Result: Agent missed amendment, used superseded value
```

**Mitigation Strategies**
1. **Multi-location extraction**: Extract all occurrences, compare
2. **Recency heuristics**: Later pages often supersede earlier pages
3. **Amendment detection**: Identify revision/amendment sections
4. **Conflict flagging**: Report conflicts for human resolution

## References

- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Long document challenges
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Multi-location extraction
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Conflict resolution
