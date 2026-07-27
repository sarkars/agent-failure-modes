# What Are the Most Common AI Model Reliability Failures in AI Agents?

**AI models used in mortgage processing hallucinate values, validate their own outputs in circular loops, and deliver production accuracy far below vendor promises, creating a systemic gap where extraction errors cascade through underwriting without independent verification.** Large language models fabricate financial data, confidence scores don't indicate actual correctness, and the industry has optimized speed at the expense of data integrity—with lenders increasingly deploying AI to both extract AND validate mortgage data, creating a dangerous verification collapse where AI signs its own homework.

## Key Takeaways

- 3 distinct failure patterns affect AI reliability in mortgage processing: hallucination (models fabricate plausible values), vendor promise gaps (marketed 99% accuracy vs. 80–90% production reality), and verification collapse (systems validate their own outputs without independent checkpoints).
- Extraction hallucination rates range from 5–18% depending on document complexity, with hallucinated values often carrying high confidence scores that mislead downstream systems.
- The verification collapse is the systemic risk: when AI handles extraction, validation, AND underwriting decisions on the same dataset, a single model error can propagate undetected across the entire loan decision.
- Post-closing defect discovery rates for full-AI processing (8–15%) are 2–3× higher than traditional workflows, indicating that model reliability improvements alone do not solve the verification integrity problem without independent checkpoints.

## Scope

- **Extraction hallucinations** — [extraction-hallucination](failures/extraction-hallucination.md), [vendor-promise-gap](failures/vendor-promise-gap.md). LLMs fabricate coherent but incorrect values (arithmetic combinations, cross-document contamination, plausible fabrication) that confidence scores fail to flag, and vendors' demo accuracy does not match production reality.
- **Verification collapse** — [verification-collapse](failures/verification-collapse.md). AI validates the same data it extracted or relies on without independent verification, creating circular validation where extraction errors propagate undetected through underwriting and fraud detection.

## When AI Model Reliability Matters

- Production workflows rely on AI for both data extraction and decision-making, where extraction errors directly corrupt underwriting inputs and no human checkpoint separates the two stages.
- Loan decisions made on AI-extracted data are later challenged by investors or regulators who want to verify the source data, exposing hallucinations that internal validation missed.
- A lender is deciding where in the pipeline to add human review, confidence thresholds, or independent verification layers, and needs to understand which failure classes preprocessing catches versus which require downstream validation checkpoints.

## Cross-Pattern Insight

The core insight across all 3 AI-model-reliability patterns is that neither model improvement nor confidence calibration solves the verification integrity problem. Extraction hallucinations are worst-case scenarios precisely because hallucinated values are plausible—they pass basic sanity checks and only fail during independent verification (e.g., IRS transcript mismatch). Vendor promise gaps show that even the best production models underperform demo claims by 10–20 percentage points on real-world documents. Verification collapse is the systemic threat: it arises not from model capability but from architectural choice—when the same organization's AI system handles extraction, validation, and decision-making, errors compound silently. The mitigation across all three patterns is the same: independent verification (IRS transcripts, third-party VOE, external asset verification) must sit outside the AI-decision loop, not inside it.

## Frequently Asked Questions

### What makes hallucinated values so dangerous compared to OCR errors?

OCR errors (character misreads like `0` → `O`) are usually obvious when re-examined—visually similar but structurally wrong. Hallucinated values are plausible: a model might generate `$85,000` when the true value is `$60,000` using coherent arithmetic (sum of two fields, annualization of YTD). That plausibility is the risk—the value passes basic reasonableness checks and only fails when cross-referenced to an independent source (tax transcript, prior loan history). High confidence scores on hallucinated values amplify deception.

### What causes the vendor accuracy gap despite model improvements?

Vendor demos are run on curated, clean test sets. Production documents are messier—handwritten notes, faded scans, non-standard formats, unusual loan structures. Vendors tune accuracy on representative documents from their test set; production accuracy drops when document distribution shifts. Additionally, vendors quote field-level accuracy (e.g., "99% of income fields correct") but don't quote straight-through processing (STP) rates, which account for documents flagged for human review—a 98% extraction accuracy can yield 50% STP if 48% of documents get routed to exceptions.

### Is verification collapse fixable by adding a separate validation model?

No—adding a second AI model to validate outputs from the first just extends the chain of AI dependencies; it doesn't break it. If the second model is trained on the same data or inherits the same biases, it amplifies the error. Verification collapse is solved architecturally by introducing truly independent verification: third-party data sources (IRS, employer VOE, bank APIs, credit bureaus) that are external to the AI-extraction system and cannot inherit its biases.

### Can confidence scores from AI models be trusted to flag high-risk extractions?

No—the research consensus is that hallucinated values often carry high confidence. A model might confidently generate `$95,000` gross income from a degraded document where the true value is `$60,000`, because the model's confidence reflects its internal coherence (the output is self-consistent), not accuracy relative to ground truth. Confidence scores are useful for ranking which documents need human review first, but they should never be used alone to skip human verification of critical fields.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Extraction Hallucination](failures/extraction-hallucination.md) | LLMs fabricate coherent but incorrect values (arithmetic combinations, contamination, plausible generation) with high confidence |
| [Vendor Promise Gap](failures/vendor-promise-gap.md) | Marketed accuracy (98–100%) vs. production reality (80–90%) due to demo curation and STP metric conflation |
| [Verification Collapse](failures/verification-collapse.md) | AI validates its own extracted outputs without independent verification, creating circular loops where errors propagate silently |

**Total: 3 patterns**

## Related Goals

- [Data Extraction](../data-extraction/) — character-level OCR and parsing errors that sit one layer below AI hallucination; hallucination adds a model-behavior layer on top of extraction.
- [Document Integrity](../document-integrity/) — forensic checks on PDFs and images that catch tampering before content is ever extracted; complements AI reliability by detecting fraud at the source-document level.
- [Compliance Validation](../compliance-validation/) — rule-based validation of extracted data against regulatory thresholds; independent of AI reliability but catches downstream errors AI makes.
