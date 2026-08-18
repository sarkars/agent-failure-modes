# AI Document Extraction Fails on Blurry or Low-Quality Scans: Causes and Fixes

## Issue: Performance Collapse Under Visual Noise

**Frequency**: Common

**Symptoms**
- Accuracy drops dramatically on low-quality or degraded scans
- Agent stays confident even when it's wrong on degraded input
- Blurred, occluded, or low-contrast regions cause silent extraction errors
- Commonly reported in LlamaIndex- and LangChain-style document pipelines ingesting faxed or scanned input without a pre-inference quality gate

**Root Cause**
VLMs trained primarily on clean images don't recognize when visual quality is too poor for reliable extraction. They produce outputs with high confidence even when input is ambiguous.

**Example**
```
Input: Faxed document with coffee stain over total
Expected: Flag as unreadable or low confidence
Actual: Extracts plausible total from surrounding context

Result: Wrong amount processed with high confidence
```

**Key Finding**
Under visual degradation (blur, occlusion, low contrast), the current response paradigm often fails to adequately perceive visual degradation and ambiguity, leading to overreliance on linguistic priors. This difficulty in recognizing uncertainty frequently results in hallucinations.

**How to fix it**: score image quality before inference and route low-quality documents to an alternate path, train or prompt the model to refuse extraction on degraded regions, and use ensemble disagreement as a degradation signal. See the mitigations below.

## Mitigation Strategies

### Prevention
1. **Pre-inference image quality scoring**: Score each document/region for objective quality signals (blur metrics, contrast, resolution, occlusion detection) before running extraction, and route images below a quality floor to an alternate path (rescan, enhanced preprocessing, human transcription) rather than letting the model attempt extraction and produce an overconfident guess. Trade-off: requires tuning quality thresholds per document type, since what counts as "too degraded" varies (a slightly blurry signature block matters less than a blurry total amount).
2. **Refusal training/prompting specifically for degraded regions**: Fine-tune or prompt the model to recognize and explicitly refuse extraction on regions with detected visual degradation (blur, occlusion, low contrast) rather than falling back on linguistic priors to fill in a plausible answer — this directly targets the paradigm gap where models don't recognize their own perceptual uncertainty. Trade-off: increases the rate of "unclear" outputs requiring downstream handling.
3. **Ensemble disagreement as a degradation proxy**: Run degraded-looking regions through multiple models or multiple stochastic samples of the same model, and treat disagreement as a signal of genuine visual ambiguity independent of any single model's self-reported confidence, since models are shown to remain confident even when input is objectively degraded. Trade-off: multiplies inference cost specifically on the population of documents that most need extra scrutiny.

### Detection & Response
1. **Quality-score-to-error-rate correlation monitoring**: Continuously measure actual extraction error rate as a function of the pre-computed quality score, and use this empirical relationship (not the model's own confidence) to set escalation thresholds, since the whole failure mode is that model confidence doesn't track true difficulty under degradation.
2. **Confidence-quality mismatch flagging**: Specifically flag cases where the model reports high confidence on a region that independently scored as low visual quality — this mismatch is the direct signature of the overreliance-on-linguistic-priors failure and is a stronger signal than either metric alone.
3. **Degraded-document accuracy audits**: Periodically audit accuracy specifically on the subset of documents flagged as low-quality, since aggregate accuracy dominated by clean documents will look fine while this subset silently fails at a much higher rate.

### Architecture Patterns
1. **Quality-gated multi-path routing**: Architect the pipeline so a quality-scoring stage runs before extraction and routes documents into different paths (standard extraction, enhanced preprocessing + extraction, direct-to-human) based on measured degradation, rather than a uniform path for all documents regardless of input quality.
2. **Ensemble-with-disagreement-escalation architecture**: For documents/regions flagged as degraded, automatically invoke an ensemble (multiple models or multiple samples) and escalate to human review on any disagreement, reserving the cost of ensemble inference for the subset that actually needs it rather than running it universally.
3. **Confidence-quality joint gating**: Require both the model's calibrated confidence and the independent visual-quality score to clear their respective thresholds before auto-accepting an extraction; either signal alone being satisfied is insufficient given known overconfidence on degraded input.

### Metrics
1. **quality_score_error_rate_correlation**: Target: track and use as the empirical basis for thresholds; re-validate quarterly; Alert if correlation weakens (signals quality scoring itself needs recalibration)
2. **confidence_quality_mismatch_rate**: Target: < 3% of extractions show high-confidence-on-low-quality mismatch; Alert if > 10%
3. **degraded_subset_accuracy**: Target: > 85% on documents flagged low-quality (after mitigation); Alert if < 65%
4. **human_escalation_rate_for_degraded_docs**: Target: > 90% of documents below the quality floor are escalated; Alert if < 70% (signals gating isn't working)

### Alerts
1. **Confidence-Quality Mismatch Spike** (P1): Condition - mismatch rate between high model confidence and low independent quality score exceeds 10%. Action: Tighten refusal training/prompting, lower auto-accept thresholds for low-quality-scored input until fixed.
2. **Degraded Subset Accuracy Drop** (P1): Condition - accuracy on the quality-flagged subset falls below 65%. Action: Escalate to human review path immediately for that document type, investigate whether quality scoring thresholds or preprocessing need adjustment.
3. **Escalation Gate Bypass** (P2): Condition - fewer than 70% of below-quality-floor documents are actually escalated to enhanced handling. Action: Audit the routing logic for a gating defect allowing degraded documents through the standard path.

## References

- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Visual degradation and hallucination
- [Why AI OCR Fails](https://parseur.com/blog/why-ai-ocr-fail) - Image quality challenges
- [Why LLMs Hallucinate More on Enterprise Documents](https://www.adlibsoftware.com/news/why-llms-hallucinate-more-on-enterprise-documents) - Linguistic prior overreliance
