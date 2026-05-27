# Error Recovery Errors

## Issue: Error Recovery Creates New Errors

**Frequency**: Occasional

**Symptoms**
- Agent attempts to fix extraction error
- "Fix" introduces new errors or corrupts good data
- Cascading corrections worsen overall accuracy

**Root Cause**
When agents detect errors and attempt corrections without sufficient context, they may "fix" things that weren't broken or make changes that violate constraints.

**Example**
```
Extracted invoice lines:
1. Widget A - $100 - Qty 5 - Total $500
2. Widget B - $150 - Qty 3 - Total $450
Extracted Grand Total: $900 (misread, actual $950)

Agent "fix": Notices mismatch, adjusts Widget B total to $400 to match

Result: Agent "corrected" good data to match bad extraction
```

**Mitigation Strategies**
1. **Correction constraints**: Define which fields can be modified
2. **Confidence weighting**: Only modify low-confidence extractions
3. **Validation priority**: Some fields (line items) more reliable than others (totals)
4. **Human review trigger**: Corrections above threshold require human approval

## References

- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Error handling strategies
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Recovery failure modes
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Cascading correction errors
