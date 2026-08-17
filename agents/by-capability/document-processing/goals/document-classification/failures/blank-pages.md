# Blank Pages Misclassified as Documents: Causes and Fixes

## Issue: Agent Classifies Blank or Near-Blank Pages as Real Documents

Commonly reported in document-ingestion pipelines built with frameworks like LlamaIndex or LangChain document loaders, where OCR/classification runs on every page without a pre-filter.

**Frequency**: Common

**Symptoms**
- Processing time wasted on blank pages
- Blank pages classified as document type (forcing downstream errors)
- Pages with only signatures/stamps classified incorrectly

**Root Cause**
Blank pages from scanning, intentional separator pages, or pages with minimal content (just a signature) need special handling.

**Example**
```
Input: Blank separator page between documents
Classification: unknown (low confidence)
Result: Review queue flooded with blank pages
```

## Mitigation Strategies

How to fix it: gate blank/near-blank pages out before they reach classification, and route only genuinely ambiguous pages to review.

### Prevention
1. **Explicit blank-page classifier**: Train a dedicated binary classifier (distinct from the main document-type classifier) to recognize blank/near-blank pages based on ink coverage, connected-component count, and text-region area, rather than relying on the general classifier to assign "unknown" with low confidence. Trade-off: requires labeled blank-page examples across scanner/lighting conditions to avoid false positives on genuinely sparse (but valid) pages.
2. **Minimum content threshold gate**: Compute a content-density score (percentage of page covered by detected text/ink) at intake and require a minimum threshold before a page enters the full classification pipeline, since intentional separator pages and near-blank scans should never reach expensive downstream processing. Trade-off: too aggressive a threshold discards pages with only a small but meaningful mark (e.g., a single stamp or initial).
3. **Signature-only region detection**: Build a specific detector for pages containing only a signature/stamp with no other body text, since these are semantically meaningful (a signed cover page) but not a document type on their own, and should be tagged as such rather than routed as unknown. Trade-off: adds a distinct model/rule to maintain beyond the primary blank detector.

### Detection & Response
1. **Review-queue composition monitoring**: Track what fraction of the human review queue consists of blank/near-blank pages; a high fraction indicates the content threshold or blank classifier isn't catching pages before they reach review, wasting reviewer time.
2. **Auto-discard audit logging**: When pages are auto-discarded for being below the content threshold, log the decision with a thumbnail/hash so discards can be audited in bulk, catching systematic false-positive discards (e.g., a scanner producing consistently faint but valid pages).
3. **Processing-time waste tracking**: Monitor OCR/classification compute time spent on pages that are ultimately classified as blank; a rising trend indicates the content-threshold gate is running too late in the pipeline (after expensive processing rather than before).

### Architecture Patterns
1. **Early-exit content gate**: Place the content-density check as the very first pipeline stage, before OCR or classification, so blank pages are filtered out with minimal compute rather than after a full extraction attempt.
2. **Confidence-gated human-in-the-loop review queue**: Route only pages that are ambiguous (neither clearly blank nor clearly containing a recognizable document type) to review, rather than flooding review with clear-cut blanks that the classifier should catch automatically.
3. **Tagged pass-through for signature/marker pages**: Rather than discarding or misclassifying signature-only or separator pages, tag and pass them through as structural metadata (e.g., "cover sheet for document N") so downstream page-grouping logic can use them as boundary signals instead of losing that information.

### Metrics
1. **blank_page_review_queue_fraction**: Target: < 5% of review queue; Alert threshold: > 20%
2. **auto_discard_false_positive_rate**: Target: < 0.5% (valid pages incorrectly discarded); Alert threshold: > 2%
3. **pre_ocr_content_gate_filter_rate**: Target: consistent with historical baseline; Alert threshold: sudden change > 25%
4. **signature_only_page_detection_recall**: Target: > 90%; Alert threshold: < 75%

### Alerts
1. **Review Queue Flooded with Blanks** (P2): Condition - blank/near-blank pages exceed 20% of review queue volume in a day. Action: Tighten or debug the content-threshold gate and blank classifier.
2. **Auto-Discard False Positives Detected** (P1): Condition - audit sampling finds valid content among auto-discarded pages above 2%. Action: Halt auto-discard for affected source, lower aggressiveness, re-review recently discarded pages.
3. **Content Gate Filter Rate Shift** (P3): Condition - the fraction of pages filtered by the early content gate changes more than 25% week-over-week. Action: Investigate upstream scanning/source changes.

## References

- [OCR vs IDP](https://forage.ai/blog/ocr-vs-idp/) - Preprocessing and filtering
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Content detection challenges
- [Production-Ready AI Agent for Document Extraction](https://www.stackai.com/insights/how-to-build-a-production-ready-ai-agent-for-document-data-extraction) - Quality thresholds
