# Column Ordering

## Issue: Multi-Column Page Reading Order Errors

**Frequency**: Common

**Symptoms**
- Text from different columns interleaved
- Sentences start in one column, continue with text from another
- Paragraphs appear out of order

**Root Cause**
Multi-column layouts (newspapers, academic papers, brochures) require detecting column boundaries and reading each column top-to-bottom before moving to the next.

**Example**
```
Input: Two-column newsletter

Column 1:              Column 2:
"The company           "Sales increased
announced today        by 20% over
that production        last quarter
will increase..."      results..."

Extracted: "The company Sales increased announced today by 20% over..."

Result: Nonsensical text
```

## Mitigation Strategies

### Prevention
1. **Vertical gutter/column-boundary detection**: Analyze whitespace projection profiles to identify vertical gutters separating columns before running text extraction, so each column's text block is extracted as a distinct region rather than the whole page being read left-to-right across column boundaries. Trade-off: irregular layouts (columns of varying width, occasional full-width elements like headlines) can defeat simple gutter detection and need additional layout-model support.
2. **Layout-aware reading-order models**: Use a model specifically trained on multi-column document layouts (newspapers, academic papers, brochures) to predict correct reading order, rather than a generic top-to-bottom, left-to-right scan that interleaves columns as seen in "The company Sales increased announced today by 20% over...". Trade-off: these models add inference cost and need retraining/fine-tuning for document types with unusual column conventions.
3. **Document-type-aware routing to column-aware processing**: Classify document type first (newspaper, academic paper, brochure vs. standard single-column business document) and only invoke column-aware reading-order logic for types known to use multi-column layouts, avoiding unnecessary complexity/risk for single-column documents. Trade-off: misclassifying a document's layout type routes it to the wrong reading-order strategy.

### Detection & Response
1. **Semantic coherence checks on extracted text**: Run a lightweight language-model coherence check on extracted paragraphs; text that jumps between unrelated topics mid-sentence (the interleaved-column symptom) fails the coherence check and should trigger reprocessing with column-aware extraction.
2. **Column-count consistency monitoring**: Track detected column count per page across a document source; an unexpected shift (e.g., suddenly detecting 1 column where 2 was historical) signals either a genuine layout change or a column-detection failure worth investigating.
3. **Reading-order confidence scoring**: Where the reading-order model produces a confidence score for its predicted order, flag low-confidence pages for review rather than silently accepting a potentially scrambled order.

### Architecture Patterns
1. **Two-stage layout-segmentation-then-read pipeline**: Segment the page into layout blocks (columns, headlines, captions) as an explicit first stage, then apply reading order within and across blocks as a second stage, rather than a single pass that conflates segmentation and reading order.
2. **Confidence-gated human-in-the-loop review queue**: Route pages that fail semantic coherence checks or have low reading-order confidence to human review before the extracted text is used downstream.
3. **Document-type-specific extraction profiles**: Maintain distinct extraction profiles/pipelines for known multi-column document types versus standard single-column documents, selected via the upstream document-type classifier.

### Metrics
1. **semantic_coherence_failure_rate**: Target: < 3% of multi-column pages; Alert threshold: > 10%
2. **column_count_detection_consistency**: Target: within expected variance per source; Alert threshold: unexpected shift > 25%
3. **reading_order_low_confidence_rate**: Target: < 5%; Alert threshold: > 15%
4. **review_routing_coverage_for_coherence_failures**: Target: 100%; Alert threshold: < 95%

### Alerts
1. **Coherence Failure Spike** (P2): Condition - semantic coherence failure rate for a document type exceeds 10%. Action: Sample pages, verify column-boundary detection and reading-order model performance for that layout.
2. **Column Count Shift** (P3): Condition - detected column count for a source shifts unexpectedly by more than 25% week-over-week. Action: Investigate source layout change or detection regression.
3. **Low-Confidence Reading Order Not Routed** (P1): Condition - low-confidence reading-order pages are not appearing in the review queue. Action: Fix routing logic; audit recently processed documents from the affected window.

## References
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Reading order issues
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Layout understanding
