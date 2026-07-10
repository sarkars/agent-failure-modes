# Footnotes

## Issue: Footnotes and Marginal Notes Misplaced

**Frequency**: Occasional

**Symptoms**
- Footnotes appear in middle of paragraphs
- Marginal annotations merged with body text
- Reference numbers disconnected from footnote content

**Root Cause**
Footnotes and margin notes exist outside the main content flow. Reading-order extraction places them incorrectly.

**Example**
```
Input:
"The study found significant results¹ in all tested conditions."

Footnote at bottom:
"¹ p < 0.05"

Extracted: "The study found significant results in all tested conditions. ¹ p < 0.05"

Expected: Footnote linked to reference
Actual: Footnote appended as regular text
```

## Mitigation Strategies

### Prevention
1. **Position/formatting-based footnote region detection**: Identify footnote and margin-note regions by their characteristic position (bottom-of-page band) and formatting (smaller font size, separator rule line) before the general reading-order extraction runs, so these regions are handled as a distinct content class rather than falling into the default in-line text flow. Trade-off: footnote conventions vary by document type (endnotes, side-margin notes, inline parentheticals), so a single positional heuristic won't catch every variant.
2. **Superscript-to-footnote reference linking**: Detect superscript markers in body text and match them to corresponding footnote markers at the bottom of the page, producing an explicit link rather than relying on reading order to keep them associated, since the current failure ("results in all tested conditions. ¹ p < 0.05") shows the footnote appended as plain trailing text with its link to the reference already lost. Trade-off: requires reliable superscript detection, which is sensitive to OCR font-size/baseline errors.
3. **Structured dual-stream output**: Output body text and footnote text as two separate, explicitly linked structured elements (body text with a reference ID, footnote text with a matching ID) rather than a single flattened text stream, preserving the semantic relationship instead of just concatenating both into one string. Trade-off: downstream consumers must be updated to handle structured output rather than plain text.

### Detection & Response
1. **Orphaned-footnote-marker detection**: Flag any body-text superscript marker that has no corresponding matched footnote text, or any footnote-region text that has no corresponding in-body reference, since either case indicates the linking step failed.
2. **Inline-appearance-of-footnote-content detection**: Check whether footnote-formatted text (small font, bottom-of-page position) appears merged mid-paragraph in the output rather than as a separated element; this is the direct symptom of reading-order extraction misplacing it.
3. **Downstream citation-integrity checks**: For documents where footnotes carry citations or key qualifiers (e.g., a statistical significance note), verify that structured output preserves the reference-to-footnote link before the document is considered fully processed, since silently dropping the link changes the meaning of the qualified claim.

### Architecture Patterns
1. **Region-classification-then-link pipeline**: Classify page regions (body, footnote, margin note) first, then perform reference-linking between body superscripts and footnote entries as a distinct downstream stage, rather than extracting all text in raw top-to-bottom reading order.
2. **Confidence-gated human-in-the-loop review queue**: Route documents with orphaned footnote markers or unlinked footnote regions to review, especially for use cases (legal, scientific) where a dropped footnote materially changes the extracted content's meaning.
3. **Configurable exclusion mode**: For use cases where footnotes are not needed (e.g., basic full-text search indexing), provide an explicit "exclude footnotes" processing mode that cleanly omits the footnote region rather than letting it leak into body text by accident.

### Metrics
1. **orphaned_footnote_marker_rate**: Target: < 2% of documents with footnotes; Alert threshold: > 8%
2. **footnote_inline_leakage_rate**: Target: < 3%; Alert threshold: > 10%
3. **reference_link_integrity_rate**: Target: > 95% of superscript-footnote pairs correctly linked; Alert threshold: < 85%
4. **structured_output_adoption_rate**: Target: 100% of footnote-bearing documents produce structured dual-stream output; Alert threshold: < 90%

### Alerts
1. **Orphaned Footnote Marker Spike** (P2): Condition - orphaned marker rate for a document type exceeds 8%. Action: Sample documents, verify footnote-region detection and linking logic for that layout/format.
2. **Footnote Leakage Into Body Text** (P2): Condition - inline leakage rate exceeds 10%. Action: Review region-classification thresholds; reprocess affected batch with region-aware extraction.
3. **Reference Link Integrity Drop** (P1): Condition - reference-link integrity falls below 85% for a document category where citation accuracy is critical. Action: Escalate to review, halt automated acceptance for that category until fixed.

## References
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Document structure
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Content flow issues
