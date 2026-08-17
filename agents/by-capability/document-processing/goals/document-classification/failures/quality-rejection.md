# Agent Rejects Valid Low-Quality Documents: Causes and Fixes

## Issue: Quality Filter Rejects Readable Documents as "Unreadable"

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

## Mitigation Strategies

How to fix it: replace the binary quality gate with tiered, channel-calibrated routing so readable-but-low-quality documents degrade gracefully instead of being rejected outright.

### Prevention
1. **Tiered quality routing instead of binary rejection**: Replace the single reject/accept quality gate with tiers (high quality -> standard pipeline, low quality -> enhanced/manual-assist pipeline, truly unprocessable -> reject) so a readable-but-low-quality fax is degraded gracefully rather than rejected outright. Trade-off: requires building and maintaining a genuinely useful "enhanced" tier rather than just relabeling the same rejection.
2. **Pre-check enhancement pass**: Apply image enhancement (denoising, contrast boost, super-resolution) before the quality gate evaluates the document, so quality scoring reflects the document's readability after reasonable preprocessing rather than its raw scanned/faxed state. Trade-off: enhancement adds latency to every document, including ones that would have passed the gate anyway.
3. **Source-specific quality thresholds**: Calibrate quality thresholds per channel (fax, mobile photo, flatbed scan) rather than applying one global threshold, since a fax channel has inherently lower achievable quality than a flatbed scan and the current failure is applying scan-level expectations to fax-level input. Trade-off: requires maintaining separate calibrated thresholds per channel and revisiting them as channel mix changes.

### Detection & Response
1. **Rejection-then-manual-success tracking**: Track cases where a document was auto-rejected for quality but later successfully processed manually; a nonzero rate here is direct evidence the automated threshold is miscalibrated for that document/channel.
2. **Quality-vs-confidence divergence monitoring**: Separately track image-quality score and downstream extraction-confidence score for the same documents; when low image quality doesn't actually correlate with low extraction confidence (i.e., the document was readable despite poor image quality), that's a signal the quality gate is over-indexing on image metrics rather than actual extractability.
3. **Per-channel rejection rate baselines**: Monitor rejection rate by channel and alert when a channel's rejection rate exceeds its historical/expected baseline, since channels like fax should have a known, tolerated higher rejection rate rather than being compared to the global average.

### Architecture Patterns
1. **Confidence-gated human-in-the-loop review queue**: Instead of a hard reject, route borderline-quality documents to human review/manual-assist processing, capturing legitimate documents that a pure automated threshold would discard.
2. **Quality-score-vs-confidence-score decoupling**: Architect the pipeline so image quality assessment and extraction confidence are computed and gated independently; a document can have poor image quality but acceptable extraction confidence (or vice versa), and only extraction confidence should drive final accept/reject decisions.
3. **Channel-calibrated threshold configuration**: Maintain quality thresholds as a per-channel configuration (fax, mobile, scan) rather than a single global constant, allowing each channel's realistic quality ceiling to inform its own gate.

### Metrics
1. **auto_rejected_manually_succeeded_rate**: Target: < 2% of rejections; Alert threshold: > 8%
2. **quality_confidence_divergence_rate**: Target: < 10% of documents show meaningful divergence; Alert threshold: > 25%
3. **rejection_rate_by_channel**: Target: within calibrated per-channel baseline; Alert threshold: > 1.5x baseline for any channel
4. **enhanced_tier_recovery_rate**: Target: > 60% of low-quality-tier documents processed successfully; Alert threshold: < 35%

### Alerts
1. **Rejected-but-Processable Spike** (P1): Condition - manual review finds more than 8% of auto-rejected documents were actually processable. Action: Loosen quality threshold for the affected channel/source, reprocess recently rejected documents.
2. **Channel Rejection Rate Exceeds Baseline** (P2): Condition - a channel's rejection rate exceeds 1.5x its calibrated baseline. Action: Investigate channel-specific quality regression or threshold miscalibration.
3. **Enhanced Tier Underperforming** (P2): Condition - enhanced/manual-assist tier recovery rate falls below 35%. Action: Review enhancement preprocessing effectiveness; consider threshold or tooling changes.

## References

- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Quality thresholds and preprocessing
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Input quality gap
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Quality-based routing strategies
