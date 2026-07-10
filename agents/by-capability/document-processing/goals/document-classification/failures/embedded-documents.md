# Embedded Documents

## Issue: Attachments and Embedded Documents

**Frequency**: Occasional

**Symptoms**
- Email attachment classified as email
- Cover letter and attached document merged
- Embedded tables treated as separate documents

**Root Cause**
Documents containing or attached to other documents create nested classification challenges.

**Example**
```
Input: Email PDF with attached invoice

Classification: email (for entire PDF)
Result: Invoice never processed

Better: Classify email + detect and separately process attached invoice
```

## Mitigation Strategies

### Prevention
1. **Attachment-boundary detection model**: Train a classifier to detect a change in formatting/style/layout partway through a multi-page file (e.g., an email body followed by an invoice with a completely different template), since the root failure is treating the entire container (email PDF) as a single document type. Trade-off: gradual style transitions (a report with an embedded appendix in matching template) are harder to detect than an abrupt change like email-to-invoice.
2. **Explicit marker scanning**: Scan page text for explicit boundary language ("Attachment", "Appendix", "Exhibit", "See attached") as a cheap, high-precision signal of an embedded document boundary before falling back to visual/style-based detection. Trade-off: only catches documents that use these conventions; many attachments have no explicit marker at all.
3. **Recursive processing architecture**: Classify and process the outer container first (e.g., "email"), then recursively detect and separately classify/process any embedded documents found within it (e.g., "invoice"), rather than a single flat classification pass that can only assign one label to the whole file. Trade-off: requires the pipeline to support variable-depth document trees rather than a flat one-file-one-type model.

### Detection & Response
1. **Single-label-on-multi-content-file flagging**: Flag any file where page-content analysis suggests more than one distinct style/template exists but only a single document type was assigned; this is the direct symptom of the invoice-never-processed failure mode.
2. **Downstream non-processing detection**: Monitor for expected document types that never appear in downstream workflows despite known attachment rates (e.g., X% of emails historically contain invoices, but extraction shows far fewer), signaling embedded documents are being swallowed by outer classification.
3. **Marker-without-boundary-detection audit**: When explicit markers ("Attachment") are found in text but no corresponding boundary/second document was detected, flag for review, since this indicates the boundary detector missed a document the text itself announced.

### Architecture Patterns
1. **Recursive document tree processing**: Architect classification as a tree rather than a single label: root container -> child documents -> (recursively) grandchild embedded documents, with each node classified and processed independently.
2. **Confidence-gated human-in-the-loop review queue**: Route files where style-change detection is ambiguous (possible embedded document but low confidence) to review rather than silently defaulting to single-document treatment.
3. **Style-fingerprint segmentation**: Segment a multi-page file into content blocks based on layout/style fingerprints (font, header structure, logo presence) before classification, so each block can be classified independently rather than forcing one type on the whole file.

### Metrics
1. **multi_style_single_label_rate**: Target: < 3% of processed files; Alert threshold: > 10%
2. **expected_vs_detected_attachment_rate**: Target: within 5% of historical baseline per source; Alert threshold: > 20% divergence
3. **marker_without_boundary_rate**: Target: < 2%; Alert threshold: > 8%
4. **recursive_processing_coverage**: Target: 100% of detected embedded documents independently processed; Alert threshold: < 95%

### Alerts
1. **Attachment Under-Detection** (P1): Condition - detected attachment rate for a source falls more than 20% below historical baseline. Action: Sample recent files, verify boundary detector is running, check for a new attachment format.
2. **Marker Without Boundary** (P2): Condition - explicit attachment marker text found but no second document detected in 8%+ of such files. Action: Investigate boundary-detection model gap for that document style.
3. **Downstream Non-Processing Gap** (P1): Condition - expected downstream document type (e.g., invoices from email) volume drops unexpectedly. Action: Audit recent email/container classifications for swallowed attachments.

## References

- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - Nested document handling
- [Why Frontier Agents Can't Read Documents](https://www.databricks.com/blog/why-frontier-agents-cant-read-documents-and-how-were-fixing-it) - Complex document structures
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Attachment extraction challenges
