# Headers and Footers

## Issue: Headers/Footers Duplicated or Misplaced

**Frequency**: Common

**Symptoms**
- Same header text appears multiple times in extraction
- Page numbers interleaved with content
- Running headers merged with body text

**Root Cause**
Multi-page documents have repeating headers and footers. Without page boundary detection, these repeat in output and disrupt content flow.

**Example**
```
Input: 5-page report

Extracted: "...end of section 1. Company Name | Confidential | Page 2 Section 2 begins..."

Result: Header content pollutes body text
```

## Mitigation Strategies

### Prevention
1. **Position-based header/footer region classification**: Identify the top and bottom page bands as distinct header/footer zones based on consistent y-coordinate position across pages, and extract them separately from body content, rather than treating the entire page as one undifferentiated text flow that lets "Company Name | Confidential | Page 2" bleed into body text mid-sentence. Trade-off: requires multi-page context to establish what counts as a consistent header/footer position, so single-page documents get less benefit.
2. **Cross-page repetition detection**: Compare candidate header/footer text across multiple pages of the same document; text that repeats verbatim (or with only a page-number substitution) at the same position on most pages is confidently classified as boilerplate and excluded from body output. Trade-off: legitimately repeated body content (a recurring disclaimer within the body, not a running header) could be miscaught if position isn't checked alongside repetition.
3. **Page-number pattern recognition**: Specifically detect and exclude page-numbering patterns (e.g., "Page 2", "2 of 5") from the header/footer band, since these interleave with content and are a distinct sub-problem within header/footer handling from static repeated text like a company name. Trade-off: page-number formats vary widely (roman numerals, "p. 2", section-relative numbering) and need broad pattern coverage.

### Detection & Response
1. **Header/footer leakage detection**: Scan extracted body text for known header/footer strings appearing mid-paragraph (the exact symptom in the example: "...end of section 1. Company Name | Confidential | Page 2 Section 2 begins..."), flagging documents where this occurs for reprocessing with region-aware extraction.
2. **Repetition-count validation**: For documents where a header/footer region was identified, confirm the excluded text actually repeated across the expected number of pages; if it only appeared once, the classification may have wrongly excluded genuine unique content.
3. **First-page-divergence handling audit**: Track how often the first-page header differs from subsequent pages (a known common pattern - title pages/cover pages) and confirm the first-page-exception logic is correctly distinguishing "different first-page header" from "extraction failure to detect the header at all."

### Architecture Patterns
1. **Multi-page-context region classification**: Architect extraction to process a document's pages together (not independently) so repetition-based header/footer detection has the cross-page context it needs, rather than classifying header/footer regions per page in isolation.
2. **Confidence-gated human-in-the-loop review queue**: Route documents where header/footer leakage is detected in body text, or where repetition validation fails, to review before the extracted text is used downstream.
3. **First-page-exception handling as a named rule**: Explicitly model the common case where page 1's header differs from the running header on later pages (e.g., a cover page vs. running header) as a distinct rule, rather than either forcing uniform treatment or letting divergence be mistaken for a detection failure.

### Metrics
1. **header_footer_leakage_rate**: Target: < 2% of multi-page documents; Alert threshold: > 8%
2. **repetition_validation_failure_rate**: Target: < 3%; Alert threshold: > 10%
3. **page_number_residual_in_body_rate**: Target: < 1%; Alert threshold: > 5%
4. **first_page_exception_correct_handling_rate**: Target: > 95%; Alert threshold: < 85%

### Alerts
1. **Header/Footer Leakage Spike** (P2): Condition - leakage rate for a document type/source exceeds 8%. Action: Sample documents, verify position-based classification and repetition detection are running correctly for that layout.
2. **Repetition Validation Failures** (P2): Condition - repetition validation failure rate exceeds 10%, suggesting genuine content may be wrongly excluded. Action: Audit recently processed documents for erroneously dropped unique text.
3. **Page Number Residual** (P3): Condition - page-number fragments detected in body text output exceed 5%. Action: Expand page-number pattern coverage for the affected document format.

## References
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Page element detection
- [Document AI: Next Evolution of IDP](https://www.llamaindex.ai/blog/document-ai-the-next-evolution-of-intelligent-document-processing) - Structure preservation
