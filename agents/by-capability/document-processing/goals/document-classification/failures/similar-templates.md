# Agent Confuses Similar Document Templates (Invoice vs. PO): Causes and Fixes

## Issue: Agent Misclassifies Documents That Share Near-Identical Layouts

Commonly reported in classification pipelines built with frameworks like LlamaIndex or LangChain, where layout similarity outweighs weaker textual signals like header terms.

**Frequency**: Common

**Symptoms**
- Invoice processing pipeline receives POs and fails
- Wrong extraction schema applied to document
- Fields extracted from incorrect positions

**Root Cause**
Business documents from the same company or industry often share similar layouts, logos, and formatting. The model cannot distinguish between closely related document types.

**Example**
```
Input: Purchase Order from Vendor A
Expected Classification: purchase_order
Actual Classification: invoice

Result: PO sent to AP workflow, fields misextracted (no "Amount Due" exists on PO)
```

**Commonly Confused Document Pairs**

| Document A | Document B | Why They're Similar |
|------------|------------|---------------------|
| Invoice | Purchase Order | Same vendor templates, similar line items |
| Quote | Invoice | Both have line items and totals |
| Receipt | Invoice | Similar structure, amounts, items |
| Packing Slip | Invoice | Same sender, same items |
| Statement | Invoice | Both have amounts and dates |
| Credit Memo | Invoice | Identical layout, only headers differ |

## Mitigation Strategies

How to fix it: weight header terms and type-specific field presence over raw layout similarity, and route close-confidence pairs to review.

### Prevention
1. **Key-phrase/header-term detection as a primary signal**: Prioritize distinguishing header text ("INVOICE", "PURCHASE ORDER", "PACKING SLIP") as a high-weight classification signal rather than relying primarily on overall layout similarity, since the root cause is that layout alone cannot distinguish these document pairs (same vendor templates, similar line items). Trade-off: some templates omit or bury the distinguishing term, so this signal alone is insufficient.
2. **Field-presence validation as a classification feature**: Use the presence/absence of type-specific fields (e.g., "Amount Due" exists on invoices but not POs) as an input to the classifier itself, not just a post-hoc validation check, since certain fields are structurally diagnostic of document type. Trade-off: requires a reliable field-detection pass before classification is finalized, effectively coupling extraction and classification.
3. **Sender-specific classification rules**: For known senders/vendors, maintain rules capturing known distinguishing differences between their invoice and PO templates (e.g., specific field positions, header wording), since the same sender's documents are the most common source of this confusion and are also the most learnable pattern. Trade-off: only scales to high-volume senders; long-tail senders still rely on general signals.

### Detection & Response
1. **Field extraction failure monitoring**: Track cases where an expected field for the assigned document type isn't found (e.g., "Amount Due" missing on something classified as invoice); this is the most direct signal that a document was misclassified as the wrong type in this confusable pair.
2. **Downstream workflow error correlation**: Monitor for downstream workflow failures characteristic of a type mismatch (e.g., a PO routed to the AP payment workflow failing because there's no payable amount), and feed those failures back as mislabeled training examples.
3. **User correction rate by confusable pair**: Track review-interface corrections specifically between commonly confused pairs (invoice/PO, quote/invoice, receipt/invoice); a persistently high correction rate for a specific pair indicates the classifier needs additional distinguishing features for that pair specifically, not just more general training data.

### Architecture Patterns
1. **Multi-label type-and-subtype classification**: Classify document type and subtype/variant jointly (e.g., "commercial-document" -> "invoice" vs. "purchase-order") so the model explicitly represents the confusable-pair relationship rather than treating each as an unrelated independent class.
2. **Confidence-gated human-in-the-loop review queue**: Route documents where classification confidence between two known-confusable types is close (e.g., invoice vs. PO scores within a small margin) to review rather than accepting the top-1 label.
3. **Field-presence-then-classify validation loop**: After initial classification, run a field-presence check consistent with that type; if the check fails (no "Amount Due" on a document labeled invoice), re-run classification with the field-absence evidence incorporated, or route to review, rather than propagating the initial mislabel.

### Metrics
1. **confusable_pair_misclassification_rate**: Target: < 3% per known pair (invoice/PO, quote/invoice, etc.); Alert threshold: > 8%
2. **expected_field_missing_rate**: Target: < 2% of classified documents; Alert threshold: > 6%
3. **downstream_workflow_type_mismatch_error_rate**: Target: < 1%; Alert threshold: > 3%
4. **review_correction_rate_by_pair**: Target: < 5% per pair; Alert threshold: > 12%

### Alerts
1. **Confusable Pair Misclassification Spike** (P2): Condition - misclassification rate for a known confusable pair exceeds 8% over a rolling window. Action: Review recent examples, add sender-specific rules or field-presence features, retrain if systemic.
2. **Expected Field Missing** (P2): Condition - a classified document is missing a type-defining field ("Amount Due" on an invoice) at a rate above 6%. Action: Route flagged documents to review; investigate classifier feature weighting.
3. **Downstream Type Mismatch Errors** (P1): Condition - workflow errors consistent with wrong-type routing (e.g., PO sent to AP payment) exceed 3%. Action: Halt auto-routing for affected sender/template, escalate to review, backfill misrouted documents.

## References

- [AlterSquare: Document AI Fails](https://altersquare.io/enterprise-document-ai-fails-extraction-layer-not-model-layer/) - Template matching challenges
- [IDP Challenges 2026](https://idp-software.com/guides/idp-challenges-2026/) - Document type confusion
- [Why OCR Alone Fails](https://dev.to/jakemiller/why-ocr-alone-fails-in-real-world-documents-5f86) - Classification limitations
