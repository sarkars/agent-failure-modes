# Multi-Page Documents Split or Merged Incorrectly: Causes and Fixes

## Issue: Agent Groups Batch-Scanned Pages Into the Wrong Documents

Commonly reported in bulk-ingestion pipelines built with frameworks like LlamaIndex or LangChain document loaders, where boundary detection between source documents has to be inferred rather than given.

**Frequency**: Common

**Symptoms**
- Multi-page document split into multiple single-page documents
- Pages from different documents incorrectly merged
- Page order scrambled

**Root Cause**
When processing batch scans or bulk uploads, determining which pages belong together requires detecting document boundaries.

**Example**
```
Input: Batch scan of 3 invoices (2 pages, 1 page, 3 pages)
Expected: 3 documents
Actual: 6 documents (each page separate)
        or: 2 documents (first two invoices merged)
```

## Mitigation Strategies

How to fix it: combine explicit boundary signals (separators, first-page markers, continuity checks) into a single confidence-scored grouping stage before classification runs.

### Prevention
1. **Barcode/separator-sheet enforcement**: For batch-scan workflows, require or encourage separator sheets (blank pages, barcoded dividers) between source documents so boundaries are explicit rather than inferred, directly preventing the "3 invoices become 6 or 2 documents" failure. Trade-off: only works when the scanning process is controlled; ad hoc uploads/bulk email attachments have no separator convention.
2. **First-page indicator detection**: Train a classifier to recognize document-start signals (a "Page 1 of N" marker, a document header appearing only on first pages, a logo/letterhead pattern that recurs at document starts) so boundaries can be inferred even without separator sheets. Trade-off: some document types have no consistent first-page marker, especially templates that repeat headers on every page.
3. **Continuity/header-matching analysis**: Compare adjacent pages on invoice/reference number, sender identity, layout style, and header content; matching pages are grouped as one document, and a mismatch signals a boundary. Trade-off: continuity analysis can over-merge when two distinct documents from the same sender share very similar templates (see similar-templates failure), so it should be combined with an explicit boundary signal where available.

### Detection & Response
1. **Boundary confidence scoring**: Assign a confidence score to every inferred page-group boundary; low-confidence boundaries (weak continuity signal, no first-page marker, no separator) are flagged for human verification before the grouped documents are finalized.
2. **Page-count anomaly detection**: Compare the resulting document count and page-count distribution against expected patterns for the batch/source (e.g., invoices from Vendor X are historically 1-2 pages); a batch producing many single-page "documents" or one unusually long document signals a grouping failure.
3. **Downstream field-mismatch detection**: If a grouped multi-page document has internally inconsistent key fields (different invoice numbers or dates across its pages), that's a signal that unrelated pages were incorrectly merged into one document.

### Architecture Patterns
1. **Multi-signal boundary fusion**: Combine separator/barcode detection, first-page indicators, and continuity analysis into a single boundary-confidence model rather than relying on any one signal alone, since each signal fails in different scenarios (no separator, no first-page marker, near-identical templates).
2. **Confidence-gated human-in-the-loop review queue**: Route batches with low-confidence boundaries, or with page-count/field-consistency anomalies, to human verification before downstream processing treats the grouping as final.
3. **Two-stage grouping-then-classification pipeline**: Perform page-grouping as an explicit, auditable stage producing a page-to-document mapping, then run document classification on the grouped result, rather than conflating grouping and classification into a single step where errors are harder to isolate and correct.

### Metrics
1. **boundary_low_confidence_rate**: Target: < 10% of inferred boundaries; Alert threshold: > 25%
2. **page_count_anomaly_rate**: Target: < 5% of batches; Alert threshold: > 15%
3. **internal_field_mismatch_rate**: Target: < 2% of grouped documents; Alert threshold: > 6%
4. **review_routed_grouping_rate**: Target: matches low-confidence rate; Alert threshold: gap > 5% (indicates under-routing)

### Alerts
1. **Grouping Anomaly Spike** (P2): Condition - page-count anomaly rate for a batch/source exceeds 15%. Action: Sample batch, check for missing separator sheets or scanner misconfiguration.
2. **Internal Field Mismatch** (P1): Condition - a grouped document has inconsistent invoice numbers/dates across its pages. Action: Un-merge and re-run boundary detection with stricter continuity checks; route to review.
3. **Under-Routing to Review** (P2): Condition - low-confidence boundaries are not appearing proportionally in the review queue. Action: Fix routing logic; audit recently finalized groupings from the gap period.

## References

- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Document boundary detection
- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Multi-page document challenges
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Page grouping strategies
