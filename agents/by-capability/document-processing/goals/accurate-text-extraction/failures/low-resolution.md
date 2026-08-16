# OCR Fails on Low-Resolution Scans and Fax Images: Causes and Fixes

## Issue: Low DPI scans, faxes, and compressed mobile photos produce fragmented, unreadable OCR output

**Frequency**: Very Common

**Symptoms**
- Consistent errors on documents from specific sources (fax, mobile upload)
- Small text (footnotes, fine print) fails completely
- JPEG compression artifacts cause characters to fragment or merge

**Root Cause**
Low DPI scans, aggressive compression, and small original text create images where characters lack sufficient detail for recognition.

**Example**
```
Document: Faxed invoice at 100 DPI
Footer text: "Terms: Net 30 days"
Extracted: "Tenns: Nel 30 drys"

Result: Payment terms not correctly parsed
```

## How to Fix Low-Resolution OCR Failures

## Mitigation Strategies

### Prevention
1. **Minimum DPI gating with channel-aware thresholds**: Measure effective DPI (or an equivalent sharpness proxy for photos/faxes) at intake and reject or flag documents below a channel-specific threshold (e.g., 200 DPI for scans, a lower bar plus extra preprocessing for fax/mobile capture), since fax and mobile-upload channels are the primary source of this failure. Trade-off: overly strict thresholds reject legitimate low-quality-but-readable documents, so thresholds should route to enhanced processing rather than outright rejection.
2. **Super-resolution and denoising preprocessing**: Apply a super-resolution model or targeted denoising pass before OCR specifically for documents below the DPI threshold, since small text (footnotes, fine print) fails completely without added detail. Trade-off: super-resolution adds meaningful latency and compute cost, so it should be applied selectively rather than to every document.
3. **Multi-scale ensemble extraction**: Run OCR at multiple resolutions/upscale factors on the same region and ensemble or vote across results, since a single fixed scale may not recover enough detail for JPEG-artifact-fragmented characters like "Tenns" for "Terms". Trade-off: multiplies OCR compute cost per document.

### Detection & Response
1. **Per-source/channel accuracy tracking**: Break out extraction accuracy by document source/channel (fax, mobile upload, scanner model) and alert when a channel's accuracy diverges from baseline, since low resolution is a channel-correlated failure rather than a random one.
2. **Image quality metric correlation**: Monitor DPI, file size, and noise/artifact levels alongside accuracy for every document, so a quality regression can be causally linked to an accuracy drop rather than investigated blind.
3. **Source quality feedback loop**: When a document fails the quality gate, notify the upstream system or sender channel (e.g., prompt a re-scan or re-fax at higher quality) rather than silently degrading output, closing the loop at the source of the problem.

### Architecture Patterns
1. **Tiered quality-based routing**: Route documents into quality tiers (high-DPI direct-to-OCR, low-DPI enhance-then-OCR, below-minimum reject-or-review) rather than a single binary pass/fail gate.
2. **Targeted high-resolution re-extraction**: For critical fields (totals, dates, IDs) that fail confidence thresholds on the first pass, re-extract just that region at higher zoom/resolution rather than reprocessing the whole document.
3. **Confidence-gated human-in-the-loop review queue**: Route documents that remain low-confidence after super-resolution and multi-scale ensembling to human review instead of accepting best-effort output on critical fields.

### Metrics
1. **accuracy_by_source_channel**: Target: within 5% of overall baseline per channel; Alert threshold: > 15% divergence
2. **sub_200_dpi_document_rate**: Target: monitored, not necessarily minimized; Alert threshold: sudden increase > 20% week-over-week from a given source
3. **super_resolution_recovery_rate**: Target: > 70% of low-DPI documents reach acceptable confidence after enhancement; Alert threshold: < 50%
4. **critical_field_confidence_post_reextraction**: Target: > 0.9; Alert threshold: < 0.7

### Alerts
1. **Channel Accuracy Drop** (P2): Condition - a specific source/channel's accuracy falls more than 15% below baseline over a rolling window. Action: Sample documents from that channel, check for a quality regression (e.g., fax line degradation), trigger source quality feedback.
2. **Super-Resolution Recovery Failure** (P2): Condition - recovery rate after enhancement drops below 50% for a channel. Action: Investigate whether the enhancement model needs retuning for that document population.
3. **Critical Field Low Confidence** (P1): Condition - a financial or identifier field remains below 0.7 confidence after targeted high-res re-extraction. Action: Route to human review before the document proceeds downstream.

## References

- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Visual degradation
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Input quality gap
