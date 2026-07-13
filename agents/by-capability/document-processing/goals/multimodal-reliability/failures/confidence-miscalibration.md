# Confidence Miscalibration

## Issue: Overconfident Wrong Answers

**Frequency**: Very Common

**Symptoms**
- High confidence scores on incorrect extractions
- Confidence doesn't correlate with accuracy
- Cannot use confidence to route to human review

**Root Cause**
VLMs are trained to produce fluent outputs, not calibrated uncertainty estimates. They express certainty linguistically even when visually uncertain.

**Example**
```
Extraction: "Total: $5,847.00" (confidence: 0.97)
Actual document: "$5,347.00"

Result: High-confidence wrong answer bypasses review queue
```

## Mitigation Strategies

### Prevention
1. **Post-hoc confidence recalibration on held-out data**: Never trust the model's raw self-reported confidence; instead, fit a calibration function (e.g., temperature scaling, isotonic regression) mapping raw scores to empirical accuracy using a held-out labeled dataset, and use the calibrated score for all routing decisions. Trade-off: requires an ongoing labeled evaluation set representative of production traffic to keep calibration current as document mix shifts.
2. **Token-level probability inspection instead of final-answer confidence**: Examine per-token generation probabilities for the specific characters/digits in a critical field rather than relying on a single end-of-response confidence score, since low per-token probability on individual digits can reveal uncertainty the aggregate score smooths over. Trade-off: requires access to token-level logprobs, which not all model APIs expose.
3. **Ensemble disagreement as an uncertainty proxy**: Run the same extraction through multiple models (or the same model with varied prompts/temperature) and use disagreement between outputs as an uncertainty signal independent of any single model's self-reported confidence, since a model can be consistently and uniformly overconfident even when wrong. Trade-off: multiplies inference cost by the ensemble size.

### Detection & Response
1. **Empirical accuracy-vs-confidence-bucket tracking**: Continuously measure actual extraction accuracy within each confidence bucket (e.g., 0.9-0.95, 0.95-0.99) against ground truth samples, and recalibrate routing thresholds whenever a bucket's real accuracy diverges from what the bucket's confidence score implies.
2. **High-confidence error sampling audits**: Specifically sample and manually verify a percentage of high-confidence extractions (not just low-confidence ones, which already get review) since miscalibration means the most costly errors are hiding exactly in the "confident" bucket that skips review.
3. **Cross-field consistency as an independent confidence signal**: Use consistency between related fields (e.g., line-item sum vs. stated total) as an orthogonal confidence signal that doesn't depend on the model's own self-assessment, catching cases where the model is confidently wrong on an internally-inconsistent extraction.

### Architecture Patterns
1. **Calibration-as-a-service layer**: Insert a dedicated calibration service between raw model output and downstream routing logic, so calibration curves can be updated/retrained independent of the extraction model itself as production data accumulates.
2. **Empirically-derived review thresholds, not model-reported thresholds**: Set the human-review routing threshold based on measured accuracy-per-confidence-bucket from calibration data, not on an arbitrary raw confidence cutoff (e.g., "0.9") that has no established relationship to actual correctness for this specific model and document type.
3. **Ensemble-plus-calibration hybrid routing**: Combine calibrated single-model confidence with ensemble disagreement as two independent signals feeding the review-routing decision, since either alone can be fooled but agreement between them is a stronger signal of genuine reliability.

### Metrics
1. **calibration_error_ece**: Target: Expected Calibration Error < 0.05; Alert if > 0.15
2. **high_confidence_error_rate**: Target: < 1% of extractions above the "auto-accept" confidence threshold are actually wrong (measured via audit); Alert if > 5%
3. **confidence_bucket_accuracy_drift**: Target: < 5 percentage point drift per bucket month-over-month; Alert if > 15 points
4. **ensemble_disagreement_correlation_with_error**: Target: > 70% of actual errors show ensemble disagreement above baseline; Alert if < 40% (signals disagreement isn't a useful proxy for this task)

### Alerts
1. **High-Confidence Error Rate Spike** (P1): Condition - audit sampling shows more than 5% of auto-accepted (high-confidence) extractions are wrong. Action: Immediately raise the auto-accept threshold or halt auto-acceptance for the affected field/document type pending recalibration.
2. **Calibration Drift** (P2): Condition - confidence-bucket accuracy drifts more than 15 percentage points from its calibrated baseline. Action: Re-run calibration against fresh labeled data; investigate whether document mix or model version has shifted.
3. **Ensemble Disagreement Signal Degradation** (P3): Condition - ensemble disagreement no longer correlates with actual error rate. Action: Re-evaluate whether ensemble diversity (model choice, prompt variation) still provides a meaningful uncertainty signal for current document types.

## Universal Pattern Reference

This is a domain-specific implementation of the universal pattern:
**[Hallucination and Confidence Miscalibration (Cross-Cutting)](../../../cross-cutting/accuracy/goals/output-accuracy/failures/hallucination-confidence-miscalibration.md)**

The universal pattern covers why LLMs/VLMs produce confident but false content. This variant focuses on **document processing** where VLM overconfidence on extracted field values prevents routing hallucinations to human review.

### Related Domain Variants
- [Knowledge Retrieval: Confidence Miscalibration](../../../knowledge-retrieval/goals/answer-synthesis/failures/confidence-miscalibration.md) — LLM overconfidence on RAG answers
- [Vision: Confidence Miscalibration](../../../vision-and-images/goals/visual-hallucination/failures/confidence-miscalibration.md) — Vision model overconfidence on hallucinated objects

---

## References

- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Confidence calibration
- [Mitigating OCR Hallucinations in MLLMs](https://arxiv.org/html/2506.20168v2) - Uncertainty estimation
- [IDP Accuracy Reckoning 2026](https://idp-software.com/news/idp-accuracy-reckoning-2026/) - Threshold tuning strategies
