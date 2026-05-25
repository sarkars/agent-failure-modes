# Plausible Wrong Outputs

## Issue: Plausible but Wrong Outputs

**Frequency**: Very Common

**Symptoms**
- Extracted values look reasonable but are incorrect
- No errors flagged in pipeline
- Downstream systems process bad data without alerting
- Errors discovered only during audits or customer complaints

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

**Mitigation Strategies**
1. **Cross-field validation**: Verify totals against line item sums
2. **Confidence thresholds**: Force explicit uncertainty scores, flag low confidence
3. **Dual extraction**: Run multiple models, compare outputs
4. **Business logic checks**: Flag values outside expected ranges
5. **Human-in-the-loop**: Route high-value documents to review

**Detection**
- Reconciliation failures in accounting systems
- Customer disputes on invoiced amounts
- Audit findings revealing systematic errors
- A/B testing against human extraction

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Silent hallucination patterns
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Plausible but wrong outputs
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Production reliability metrics
