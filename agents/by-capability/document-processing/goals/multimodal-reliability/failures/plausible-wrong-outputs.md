# AI Document Extraction Silently Returns Plausible but Wrong Values: Causes and Fixes

## Issue: Plausible but Wrong Outputs — Errors That Never Trip an Alarm

**Frequency**: Very Common

**Symptoms**
- Extracted values look entirely reasonable but are actually incorrect
- No errors or warnings are flagged anywhere in the pipeline
- Downstream systems process the bad data without alerting on it
- Errors are discovered only weeks later, during audits or customer complaints
- Commonly reported in LangChain- and LlamaIndex-style extraction pipelines that treat "output parsed successfully" as equivalent to "output is correct"

**Root Cause**
Classical OCR fails loudly - when Tesseract cannot read a character, it produces garbled output or blanks. The failure is visible. MLLMs fail silently - when a multimodal LLM cannot confidently read a digit, it produces the most statistically plausible digit instead of indicating uncertainty.

**Example**
```
Input: Scanned invoice with slightly damaged "$10,000"
Expected: $10,000
Actual: $3,000 (model filled in plausible value)

Result: Payment processed for wrong amount, no error flagged
```

**Key Statistic**
Unlike OCR errors which are often obvious and consistent, LLM errors are plausible and hidden, making them far harder to detect at scale in high-stakes industries.

**How to fix it**: enforce deterministic cross-field arithmetic checks before accepting a value, run dual/ensemble extraction with mandatory agreement, and route high-value documents to human review regardless of confidence. See the mitigations below.

## Mitigation Strategies

### Prevention
1. **Mandatory cross-field arithmetic validation**: For any document where fields have a known arithmetic relationship (line items must sum to subtotal, subtotal + tax must equal total), enforce that check deterministically before accepting the extraction, since a "plausible" total that doesn't reconcile with its own line items is a near-certain silent error, not just an anomaly. Trade-off: only catches errors where a redundant, checkable relationship exists in the document; a standalone field with no cross-check has no such safety net.
2. **Dual/ensemble extraction with mandatory agreement**: Run the same field extraction through two independent models or configurations and require agreement (or explicit reconciliation) before accepting a value automatically, since silent plausible-wrong-answer failures are exactly the class of error that a single model's own confidence won't surface. Trade-off: doubles inference cost for every extraction that uses this safeguard.
3. **Business-logic range and pattern checks per field**: Define expected ranges/patterns per field per document type (e.g., invoice totals for this vendor are typically $500-$5,000) and flag values outside the expected range even if the value looks individually plausible in isolation, since "plausible in general" and "plausible for this specific context" are different bars. Trade-off: requires maintaining per-vendor/per-context expectations, which need updating as business relationships change.

### Detection & Response
1. **Downstream reconciliation failure monitoring**: Treat accounting/ERP reconciliation failures as a primary detection signal for this failure mode specifically (not just generic data quality noise) — since silent plausible-wrong-answers are, by definition, not caught at extraction time, the first real signal often arrives downstream.
2. **Customer/counterparty dispute correlation**: Track disputes on invoiced or processed amounts and correlate them back to the extraction pipeline and specific document sources, since a cluster of disputes from one source/template is a strong signal of a systematic silent extraction error rather than isolated customer error.
3. **Periodic human-extraction A/B audits**: Regularly run a sample of documents through both the automated pipeline and independent human extraction, and compare results field-by-field — this is the only reliable way to measure the true silent-error rate, since the pipeline's own confidence signals are exactly what's failing in this pattern.

### Architecture Patterns
1. **Deterministic reconciliation gate before acceptance**: Architect a hard gate between extraction and downstream use where every document must pass its applicable arithmetic/business-logic checks; documents failing the gate are held for human review rather than passed through with a "low confidence" flag that might be ignored downstream.
2. **High-value document tiering with mandatory review**: Route documents above a value threshold (dollar amount, contract materiality) through mandatory human review regardless of confidence score, since the cost asymmetry of a silent error on a high-value document justifies the review cost even at low measured error rates.
3. **Continuous human-in-the-loop calibration sampling**: Build human-extraction A/B comparison into the standing pipeline (not just periodic ad-hoc audits) so the true silent-error rate is continuously measured and any regression is caught quickly rather than discovered months later through disputes.

### Metrics
1. **cross_field_reconciliation_failure_rate**: Target: < 1% of documents fail arithmetic reconciliation; Alert if > 4%
2. **downstream_reconciliation_failure_rate**: Target: < 0.5% of processed documents cause accounting/ERP reconciliation failures; Alert if > 2%
3. **human_ab_audit_disagreement_rate**: Target: < 2% field-level disagreement between pipeline and human extraction; Alert if > 6%
4. **high_value_document_review_coverage**: Target: 100% of above-threshold documents reviewed; Alert on any bypass

### Alerts
1. **Reconciliation Failure Spike** (P1): Condition - cross-field or downstream reconciliation failure rate exceeds threshold for a document source. Action: Halt automated processing for that source, route recent documents for human re-verification, investigate root cause before resuming.
2. **Human A/B Disagreement Spike** (P1): Condition - human-extraction audit disagreement rate exceeds 6%. Action: Treat as evidence of a systemic silent-error regression; escalate to model/pipeline review regardless of what production confidence metrics show.
3. **High-Value Review Bypass** (P1): Condition - a document above the mandatory-review value threshold was processed without human review. Action: Treat as an incident; audit the document immediately and fix the routing logic that allowed the bypass.

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Silent hallucination patterns
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Plausible but wrong outputs
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Production reliability metrics
