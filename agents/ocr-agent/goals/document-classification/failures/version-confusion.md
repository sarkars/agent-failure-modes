# Version Confusion

## Issue: Version and Variant Confusion

**Frequency**: Occasional

**Symptoms**
- Old template version extracted with new schema (or vice versa)
- Different regional variants handled incorrectly
- Draft vs. final versions not distinguished

**Root Cause**
Document templates evolve over time. The same document type from the same sender may have multiple versions in circulation.

**Example**
```
Input: 2023 invoice template from Vendor B
Classification: invoice (correct)
Schema Applied: 2024 template schema (incorrect)

Result: "Total" field moved in 2024, now extracting from wrong position
```

**Mitigation Strategies**
1. **Version detection**: Include version/template ID in classification
2. **Date-based routing**: Use document date to select appropriate schema
3. **Template fingerprinting**: Use layout hash to detect exact template
4. **Fallback extraction**: When primary positions fail, try alternate known positions

## References

- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Template drift challenges
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Schema versioning strategies
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - Template evolution handling
