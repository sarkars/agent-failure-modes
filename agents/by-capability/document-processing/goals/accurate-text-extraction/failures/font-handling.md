# OCR Misreads Stylized Fonts and Logos: Causes and Fixes

## Issue: OCR fails on decorative fonts, stylized brand typography, and logos, consistently misreading the same sources

**Frequency**: Occasional

**Symptoms**
- High error rates concentrated on specific document sources or senders
- One company's documents consistently fail extraction while others succeed
- Brand names and logo text extracted incorrectly (e.g., a stylized letter read as the wrong character)

**Root Cause**
Decorative fonts, stylized text, and brand-specific typography differ significantly from standard fonts in training data.

**Example**
```
Input: Company logo with stylized "ACME CORP"
Expected: ACME CORP
Actual: RCME CORF (stylized A looks like R, P like F)
```

## How to Fix Stylized Font and Logo Misreads

## Mitigation Strategies

### Prevention
1. **Template-based region routing**: For known, recurring document sources, define fixed regions (logo blocks, letterhead) that are either skipped entirely or routed to a template-specific extractor rather than the general OCR path, since stylized brand typography rarely needs to be read verbatim once the source is identified. Trade-off: requires maintaining a per-source template registry that must be updated when a sender changes their letterhead.
2. **Logo/decorative-text detection and exclusion**: Train a lightweight detector to identify logo and decorative-text regions and exclude them from the text-recognition pass, since these regions contribute disproportionate error (e.g., "ACME CORP" reading as "RCME CORF") without carrying information the pipeline actually needs. Trade-off: adds a detection stage and risk of false-positive exclusion of genuine stylized body text.
3. **Source-specific model fine-tuning**: For high-volume recurring senders whose documents consistently fail extraction, fine-tune or calibrate the OCR model on samples from that specific source's typography. Trade-off: only economical for high-frequency sources; long-tail senders get no benefit and still need a fallback.

### Detection & Response
1. **Per-source accuracy monitoring**: Track extraction accuracy broken out by sender/source; a source with a persistently high error rate concentrated in a specific field (e.g., company name) signals a font-handling issue rather than a general quality problem, and should trigger template or fallback-rule creation.
2. **Business-rule fallback verification**: When falling back to sender metadata instead of extracted text (e.g., using the known sender's registered company name rather than the OCR'd logo text), log and periodically audit that the fallback value still matches what a human would read off the document.
3. **New-source cold-start flagging**: Flag any source with fewer than N historical documents so its first-run extractions are automatically routed to review, since fine-tuning and templates cannot yet exist for a source that hasn't been seen before.

### Architecture Patterns
1. **Template matching with fallback**: Attempt template-specific extraction for recognized sources first; if the source is unrecognized or the template match confidence is low, fall back to general-purpose OCR plus business-rule substitution for known fields (sender name from metadata rather than logo text).
2. **Confidence-gated human-in-the-loop review queue**: Route documents where a brand/company-name field disagrees with the sender metadata on record to a review queue, catching cases where fine-tuning and templates haven't yet been established for that source.
3. **Source-specific model registry**: Maintain a registry mapping source/sender identifiers to fine-tuned model variants or template definitions, with a default general-purpose model as the fallback for unregistered sources.

### Metrics
1. **font_related_field_error_rate_by_source**: Target: < 2% per registered source; Alert threshold: > 8% for any single source
2. **logo_region_exclusion_false_positive_rate**: Target: < 1%; Alert threshold: > 3%
3. **sender_metadata_fallback_mismatch_rate**: Target: < 1%; Alert threshold: > 5%
4. **new_source_review_routing_rate**: Target: 100% of first-N documents from a new source; Alert threshold: < 95%

### Alerts
1. **Persistent Source Error Spike** (P2): Condition - a single sender/source exceeds 8% field error rate over 50+ documents. Action: Build or update source-specific template, or add sender to fine-tuning candidate list.
2. **Fallback Metadata Mismatch** (P2): Condition - sender-metadata fallback disagrees with extracted text more than 5% of the time. Action: Audit sender metadata accuracy and template mapping.
3. **New Source Not Routed to Review** (P3): Condition - a source with under N historical documents was processed without review routing. Action: Fix cold-start routing rule; backfill review for affected documents.

## References

- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Font recognition problems
- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Extraction layer issues
