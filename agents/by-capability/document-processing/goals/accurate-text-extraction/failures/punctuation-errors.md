# Punctuation Errors

## Issue: Punctuation and Special Character Errors

**Frequency**: Common

**Symptoms**
- Decimal points become commas (or vice versa) breaking numeric parsing
- Currency symbols misread or dropped
- Hyphens, dashes, and minus signs interchanged

**Root Cause**
Small punctuation marks are often damaged in scans or rendered differently across fonts. Regional formatting differences (`.` vs `,` for decimals) add ambiguity.

**Example**
```
Input Image: Total: $1,234.56
Expected: 1234.56
Actual: 1.23456 (comma interpreted as decimal)

Result: Invoice processed for wrong amount
```

## Mitigation Strategies

### Prevention
1. **Locale-aware numeric parsing**: Detect document locale/currency (from sender metadata, currency symbol, or address) before parsing and apply the corresponding decimal/thousands-separator convention, since `.` vs `,` ambiguity is fundamentally a locale-detection problem rather than an OCR problem. Trade-off: requires reliable locale signals; documents with no locale context still default to a guess.
2. **Dual-pass raw-and-parsed extraction with cross-check**: Extract both the raw character string (`1,234.56`) and a structurally-parsed numeric value, then verify the parsed value's magnitude and decimal-position are consistent with the raw string's punctuation pattern before accepting it, catching cases like a comma being misread as a decimal point. Trade-off: adds a verification step and requires a canonical raw-string extraction path in addition to numeric parsing.
3. **Currency-symbol-first parsing order**: Detect and extract the currency symbol before parsing the numeric value, since knowing the currency (and therefore its conventional format) resolves ambiguity that pure digit/punctuation recognition cannot. Trade-off: symbol misreads (dropped or misrecognized currency marks) can still propagate the wrong format assumption.

### Detection & Response
1. **Sanity-bound range validation**: Reject or flag parsed values outside an expected range for the field/document type (e.g., an invoice line item over $1M, or a total under $1 when line items sum higher), routing the flagged value for correction rather than passing a misparsed amount downstream. 
2. **Value-distribution monitoring**: Track the distribution of parsed values for a field across a document source; a sudden cluster of unusually small values (e.g., many totals under $1 when historically larger) signals systematic comma-as-decimal misparsing rather than isolated errors.
3. **Downstream parsing exception correlation**: Monitor parsing/type exceptions in downstream financial systems and correlate them back to the originating document source and extraction confidence, since a spike there is often the first visible symptom of a punctuation misread upstream.

### Architecture Patterns
1. **Confidence-gated human-in-the-loop review queue**: Route any parsed value that fails sanity bounds or raw/parsed cross-check to human review before it reaches payment or accounting systems.
2. **Locale-inference-then-parse pipeline**: Architect extraction as locale/currency detection first, then format-specific numeric parsing second, rather than a single locale-agnostic parser applied uniformly to all documents.
3. **Reconciliation checkpoint**: For invoices, verify that extracted line items sum to the extracted total within tolerance; a mismatch is strong evidence of a punctuation-driven misparse in one of the values and should trigger reprocessing before acceptance.

### Metrics
1. **sanity_bound_rejection_rate**: Target: < 1% of parsed numeric fields; Alert threshold: > 4%
2. **line_item_total_reconciliation_mismatch_rate**: Target: < 2%; Alert threshold: > 6%
3. **downstream_parsing_exception_rate**: Target: < 0.5%; Alert threshold: > 2%
4. **locale_detection_confidence**: Target: > 95% of documents with a confidently detected locale; Alert threshold: < 85%

### Alerts
1. **Value Distribution Anomaly** (P2): Condition - a document source shows a spike in parsed values below $1 or an unexplained order-of-magnitude shift. Action: Sample documents, verify locale detection and decimal parsing for that source.
2. **Reconciliation Mismatch Spike** (P1): Condition - line-item-to-total mismatch rate exceeds 6% for a source. Action: Halt auto-posting for that source, route to review, investigate punctuation misparse.
3. **Downstream Exception Spike** (P2): Condition - payment/accounting system parsing exceptions traced to extraction exceed 2% in a rolling window. Action: Correlate to source/template, escalate to extraction pipeline owner.

## References

- [Why OCR Is the Weakest Part of Document AI](https://medium.com/@manalisomani099/why-ocr-is-the-weakest-part-of-most-document-ai-systems-c9188381d1b9) - Punctuation issues
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - OCR accuracy challenges
