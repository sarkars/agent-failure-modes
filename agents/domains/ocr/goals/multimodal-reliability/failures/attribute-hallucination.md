# Attribute Hallucination

## Issue: Attribute Hallucination

**Frequency**: Common

**Symptoms**
- Correct field identified but wrong value assigned
- Colors, dates, or quantities slightly off
- Model "corrects" values to common patterns

**Root Cause**
Model identifies the right object but assigns properties based on training distribution rather than image content.

**Example**
```
Input: Invoice dated "2024-02-29" (leap year)
Actual: "2024-02-28" (model "corrects" to common date)

Result: Payment terms calculated from wrong date
```

**Mitigation Strategies**
1. **Domain validation**: Verify dates are valid, amounts are plausible
2. **Unusual value alerting**: Flag extractions that differ from OCR baseline
3. **Raw vs. parsed**: Keep original extraction separate from normalized values

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) - Attribute hallucination types
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Value correction errors
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Validation strategies
