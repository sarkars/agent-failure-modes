# Cascading Downstream Errors

## Issue: Cascading Downstream Errors

**Frequency**: Common

**Symptoms**
- Single extraction error corrupts multiple downstream systems
- Error propagates before detection
- Cleanup requires touching many systems

**Root Cause**
Automation moves data faster - meaning bad inputs create even bigger issues downstream. Errors in GL coding, invoice matching, or field mapping propagate across financial reports and compliance processes in real time.

**Example**
```
OCR extracts vendor: "ABC Corp" (actual: "ABG Corp")

Downstream impact:
- Payment routed to wrong vendor in AP system
- Spend analytics misattribute purchase
- Tax reporting shows incorrect vendor payments
- Audit flags unexplained vendor discrepancy
```

**Mitigation Strategies**
1. **Validation gates**: Verify before each integration point
2. **Soft deletes**: Keep original data recoverable
3. **Batch boundaries**: Limit blast radius of errors
4. **Rollback capabilities**: Enable reversal of bad data pushes

## References

- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Downstream propagation
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Validation gates
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - GL coding error impact
