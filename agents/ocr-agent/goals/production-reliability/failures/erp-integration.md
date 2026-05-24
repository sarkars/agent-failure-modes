# ERP Integration Errors

## Issue: ERP Field Mapping Errors

**Frequency**: Common

**Symptoms**
- Extracted data in wrong ERP fields
- GL codes misassigned
- Dimension values incorrect

**Root Cause**
Mapping between extracted fields and ERP schema requires configuration. Changes to either side break the mapping without obvious errors.

**Example**
```
Extraction output: {"department": "Sales", "cost_center": "CC-100"}
ERP mapping (outdated): department -> DEPT_CODE, cost_center -> GL_ACCT

Result: "Sales" written to DEPT_CODE, "CC-100" written to GL_ACCT (wrong field)
```

**Mitigation Strategies**
1. **Mapping validation**: Test mappings against expected ERP schemas
2. **Schema versioning**: Track changes to both extraction output and ERP input
3. **Dry-run mode**: Validate before committing to ERP
4. **Reverse validation**: Query ERP to verify data landed correctly

## References

- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - ERP integration patterns
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - GL miscoding rates
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Field mapping challenges
