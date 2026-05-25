# Quality Rejection

## Issue: Poor Quality Rejects Valid Documents

**Frequency**: Occasional

**Symptoms**
- Legitimate documents rejected as "unreadable"
- Quality threshold too aggressive
- Faxes, copies of copies consistently fail

**Root Cause**
Quality filters meant to catch truly unprocessable documents also reject low-quality but readable documents.

**Example**
```
Input: Faxed invoice, low quality but readable
Classification: rejected (quality too low)
Result: Valid invoice requires manual processing
```

**Mitigation Strategies**
1. **Tiered processing**: Low quality -> different pipeline, not rejection
2. **Preprocessing boost**: Apply enhancement before quality check
3. **Quality vs. confidence separation**: Low image quality doesn't mean low extraction confidence
4. **Source-specific thresholds**: Fax channel has lower quality expectations

## References

- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Quality thresholds and preprocessing
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Input quality gap
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Quality-based routing strategies
