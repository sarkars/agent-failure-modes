# Low Resolution

## Issue: Low Resolution and Compression Artifacts

**Frequency**: Very Common

**Symptoms**
- Consistent errors on documents from specific sources (fax, mobile upload)
- Small text (footnotes, fine print) fails completely
- JPEG artifacts cause character fragmentation

**Root Cause**
Low DPI scans, aggressive compression, and small original text create images where characters lack sufficient detail for recognition.

**Example**
```
Document: Faxed invoice at 100 DPI
Footer text: "Terms: Net 30 days"
Extracted: "Tenns: Nel 30 drys"

Result: Payment terms not correctly parsed
```

**Mitigation Strategies**
1. **Minimum DPI requirements**: Reject or flag documents below 200 DPI
2. **Image preprocessing**: Apply super-resolution or denoising before OCR
3. **Multi-scale extraction**: Run OCR at multiple resolutions and ensemble results
4. **Source quality feedback**: Notify upstream systems about quality issues
5. **Targeted high-res extraction**: Re-extract specific regions at higher zoom for critical fields

**Detection**
- Track accuracy by document source/channel
- Monitor image quality metrics (DPI, file size, noise levels) alongside accuracy
- Alert on sudden quality drops from specific sources

## References

- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Visual degradation
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Input quality gap
