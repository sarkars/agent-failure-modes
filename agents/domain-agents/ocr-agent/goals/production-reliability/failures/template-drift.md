# Template Drift

## Issue: Template Drift Without Detection

**Frequency**: Common

**Symptoms**
- Extraction accuracy degrades gradually over time
- No alerts when vendor changes invoice format
- Fields silently map to wrong positions
- Vendor changed template without notification

**Root Cause**
In real-world operations, document layouts often change without notice. A vendor might shift a column, rename a label, or reorder fields, and suddenly the trusted template no longer functions as expected.

**Example**
```
Original invoice template (2023):
| Description | Qty | Unit Price | Total |

Updated template (2024):
| Description | Unit Price | Qty | Total |

Extraction schema: Column 2 = Qty, Column 3 = Unit Price

Result: All values systematically swapped, pipeline shows no errors
```

**Key Statistic**
Up to 30% of invoice requests failed to process correctly in their first iteration due to template incompatibilities.

**Mitigation Strategies**
1. **Template fingerprinting**: Hash layout structure, alert on changes
2. **Field semantic validation**: Unit prices should look like money, quantities like integers
3. **Header-based extraction**: Use header text, not column position
4. **Regular accuracy audits**: Systematic verification against ground truth
5. **Vendor relationship management**: Request advance notice of changes

## References

- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - 30% first-iteration failures
- [AI Agents and Document Processing 2026](https://parsio.io/blog/ai-agents-document-processing-2026) - Template change detection
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Version management
