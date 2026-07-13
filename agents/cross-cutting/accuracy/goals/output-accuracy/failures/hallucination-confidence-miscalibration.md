# Hallucination and Confidence Miscalibration

## Issue: Model Confidence Doesn't Match Answer Reliability (Hallucination Sub-Pattern)

**Frequency**: Very Common

**Symptoms**
- High confidence on wrong or poorly-grounded answers
- Low confidence on well-supported answers
- Uncertainty not expressed when context is ambiguous
- All answers have similar confidence regardless of support
- Hallucinated content has nearly same confidence as grounded content

**Root Cause**
LLMs are trained to produce fluent, confident text. They don't naturally express calibrated uncertainty based on context support. The model's confidence is fundamentally about token probability (given the context so far, how likely is this token?), not about correctness. When the model hallucinates, it's producing high-probability tokens based on its training distribution, not grounded reasoning. This means confident-sounding hallucinations are common: the model fluently generates plausible false content.

**Example**
```
Scenario 1 (RAG):
Context: "The meeting might be rescheduled to either Tuesday or Wednesday, pending confirmation from the VP."
Query: "When is the meeting?"
Agent: "The meeting is on Tuesday." (stated definitively, 87% confidence)
Reality: Day is uncertain, pending confirmation; model selected most likely option as if certain
Result: User misses meeting because they assumed Tuesday

Scenario 2 (Document Processing):
Document field: "Inv-2024-13" (invoice number)
Model reads: "Invoice number: Inv-2024-13" (98% confidence)
But also states: "Due date: 2024-02-29" (92% confidence)
Reality: 2024-02-29 is valid (leap year), but model "corrected" it to 2024-02-28 in another run
Result: Same model produces different confidences for similar extraction tasks

Scenario 3 (Vision):
Image: Low-light scene with ambiguous object
Model output: "Red box, 95% confidence"
Reality: Object is red, but lighting makes it appear gray; model inferred from training prior
Result: High confidence despite ambiguous visual evidence
```

**Key Statistics**
- 20-40% of LLM responses include hallucinated details, often with high confidence
- Average confidence on hallucinated content: 70-85% (only 5-15% lower than correct)
- Confidence and accuracy correlation in LLMs: ~0.3-0.5 (weak; random would be 0.0)
- Vision models: 95% confident object detections have 70-80% actual accuracy
- Fine-tuned models show better calibration but still ±15-20% confidence-accuracy gap

**Contributing Factors**
- Training objective: maximize token probability, not calibration
- No built-in uncertainty mechanism (softmax confidence ≠ truth probability)
- Distribution shift: model uncertain in-domain but doesn't express it
- Temperature/sampling diversity: affects probability distribution but not "truthfulness"
- Context-anchoring: high confidence anchored to context recency, not relevance

---

## Test Scenario & Reproduction

### Scenario Setup
Deploy a model in an environment where you can:
- Vary context completeness (full context, partial, none)
- Measure both model confidence and actual accuracy
- Compare confidence scores across similar tasks
- Control model parameters (temperature, sampling)

### Trigger Mechanism
Confidence miscalibration occurs when:
1. Context is incomplete but model still assigns high confidence
2. Multiple valid answers exist but model picks one with high certainty
3. Model is uncertain (low probability output) but doesn't express it
4. Vision/multimodal input is ambiguous (low-light, occlusions)

**Example Reproduction Steps:**
```
1. Prepare dataset with: query, context (vary completeness), ground truth answer
2. Run model on full context → measure accuracy and confidence
3. Run model on 50% of context (removed relevant facts) → measure accuracy and confidence
4. Run model on 0% context (ask question, provide no info) → measure accuracy and confidence
5. Compare: as accuracy drops 100%→50%→0%, does confidence also drop?
6. Expected: confidence should drop with accuracy; if not, miscalibrated
7. Measure Spearman correlation between confidence and correctness
```

### Expected Failure State
- Model produces confident answers even when context is incomplete or ambiguous
- Confidence scores show little variation (clustered in 0.7-0.95 range)
- Wrong answers have only slightly lower confidence than correct answers
- Vision hallucinations accompanied by high-confidence scores (0.8+)
- Confidence-accuracy correlation < 0.5

### Mitigation Validation Protocol

**Test Checklist:**
- [ ] Reproduce miscalibration on baseline → confirm confidence-accuracy gap
- [ ] Apply mitigation (e.g., uncertainty prompting, calibration training, ensemble methods)
- [ ] Re-run on same test set → measure new confidence-accuracy correlation
- [ ] Verify improvement: correlation increased by ≥0.2 points
- [ ] Check for regression: accuracy on well-grounded queries unchanged

**Success Criteria:**
- Confidence-accuracy correlation improved to >0.7 (from baseline ~0.3-0.5)
- High-confidence hallucinations reduced by ≥50%
- Uncertainty properly expressed in low-confidence answers
- Accuracy metrics unchanged (no "accuracy for calibration" tradeoff)

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Full context | Complete info provided | High confidence, high accuracy | High confidence with low accuracy |
| Partial context | 50% of info removed | Medium confidence, medium accuracy | Same confidence as full context |
| No context | Asked without info | Low confidence or explicit uncertainty | High confidence without evidence |
| Ambiguous query | Multiple valid answers possible | Medium-low confidence or acknowledgment of ambiguity | High confidence despite ambiguity |
| Rare/uncommon scenario | Out-of-distribution query | Low confidence or appropriate uncertainty | Same confidence as common queries |

### Evaluation Dataset
- **Source**: SQuAD (extractive QA), RAFT (few-shot), CustomQA with varying context completeness
- **Size**: 1,000+ queries across completeness levels (0%, 25%, 50%, 75%, 100% context)
- **Key variations**: Question difficulty, context relevance, ground truth answer uniqueness

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Confidence-Accuracy Correlation | >0.7 Spearman | Correlation between model confidence and answer correctness |
| Calibration Error | <0.1 | Mean absolute difference between confidence and accuracy (perfect: 0.0) |
| Uncertainty Coverage | >95% | % of incorrect answers with low confidence (<0.6) |
| Overconfidence Ratio | <1.2x | Avg confidence on wrong answers / avg confidence on correct |

### Automated Checks
```python
def evaluate_calibration(model, test_data):
    """Measure confidence-accuracy calibration"""
    confidences = []
    correctness = []
    
    for query, context, ground_truth in test_data:
        output = model(query, context=context)
        confidence = output.confidence
        is_correct = output.answer == ground_truth
        
        confidences.append(confidence)
        correctness.append(1 if is_correct else 0)
    
    # Calibration metrics
    correlation = spearman(confidences, correctness)
    calibration_error = mean(abs(c - a) for c, a in zip(confidences, correctness))
    
    assert correlation > 0.7, f"Calibration poor: {correlation:.2f}"
    assert calibration_error < 0.1, f"Calibration error too high: {calibration_error:.2f}"
    
    return {
        'correlation': correlation,
        'calibration_error': calibration_error,
        'passed': correlation > 0.7
    }
```

---

## Mitigation Strategies

### Prevention

1. **Explicit Uncertainty Prompting**: Modify prompts to explicitly request uncertainty expressions. Examples: "Express your confidence as low/medium/high before answering," "State your assumptions about the information you have," "Flag any parts of your answer that rely on inference vs. explicit information." This trains the model to think about confidence rather than defaulting to fluency.

2. **Calibration Fine-Tuning**: Fine-tune or use RLHF to train models on calibrated confidence. Create training data where confidence scores match actual accuracy on holdout sets. Use methods like temperature scaling or Platt scaling post-hoc to adjust raw probabilities to match observed accuracy.

3. **Ensemble and Diversity-Based Confidence**: Use disagreement between multiple models or multiple runs (different temperatures) as a calibration signal. High disagreement → low true confidence, even if each model individually outputs high confidence. This naturally captures uncertainty without retraining.

### Detection & Response

1. **Answer Completeness Monitoring**: Measure coverage of query intents in generated answers. Track query decomposition rate (% of query components explicitly addressed) and flag responses with coverage <85%. Incomplete answers often accompanied by high confidence but low accuracy.

2. **Evidence Balance Scoring**: For each answer, compute evidence distribution across sources and flag one-sided responses (>70% from single source on multi-source queries). Implement automated extraction of caveat/limitation mentions and track inclusion rates by query type. Target: >80% of medical/financial answers include relevant caveats.

3. **Fact Verification and Divergence Alerts**: Run fact-verification on model outputs (check claims against sources). Alert when model confidence is high but fact-verification fails, indicating systematic overconfidence.

### Architecture Patterns

1. **Query Intent Decomposition Graph**: Parse complex queries into a DAG of atomic intents before answering. Each answered component is assigned a confidence based on evidence. Overall confidence is the minimum across components, preventing false high-confidence on partial answers.

2. **Evidence Consensus Engine**: Maintain a fact graph where each claim is attributed to specific sources with confidence scores. Multi-source claims require consensus computation (intersection of sources supporting claim). Flag contradictions to the generation model, informing confidence.

3. **Structured Response Templates with Confidence Scaffolding**: Use task-specific response schemas that enforce: primary answer + confidence + supporting evidence + relevant caveats/exceptions + confidence bounds. Template violations flagged before user delivery.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `confidence_accuracy_correlation` | Spearman correlation between confidence and correctness | <0.6 (indicates miscalibration) |
| `overconfidence_ratio` | Avg confidence on wrong answers / avg confidence on correct | >1.2x (wrong answers too confident) |
| `high_confidence_error_rate` | % of answers with >0.8 confidence that are incorrect | >20% |
| `calibration_error` | Mean absolute gap between confidence and actual accuracy | >0.15 |
| `uncertainty_expression_rate` | % of answers that include explicit uncertainty language | <50% baseline |

### Logs & Traces
- Log every answer with: confidence score, answer correctness (post-hoc), supporting evidence quality
- Include model checkpoint, temperature/sampling settings, query characteristics
- Track user feedback: "this is wrong despite high confidence" (miscalibration signal)
- Monitor fact-verification pipeline results: when does model confidence diverge from verification outcome?

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Overconfidence Spike | Avg confidence on incorrect answers exceeds 0.7 for >1% of outputs | P2 | Investigate model checkpoint; may indicate regression or distribution shift |
| Confidence-Accuracy Uncorrelated | Correlation drops below 0.6 over 1-hour window | P2 | Check for prompt/context changes; recalibrate confidence scoring if needed |
| High-Confidence Errors | >20% of high-confidence (>0.8) answers are incorrect | P1 | Pause high-confidence-only deployments; investigate model behavior |
| Calibration Drift | Calibration error increases >0.05 points over week | P2 | Data drift or model degradation; consider retraining with recent data |

### Dashboard Panels
- Panel 1: Confidence distribution for correct vs. incorrect answers (overlapping histograms)
- Panel 2: Confidence-accuracy scatter plot (should show diagonal trend if calibrated)
- Panel 3: Calibration curve (average accuracy at confidence bins: 0-0.2, 0.2-0.4, ..., 0.8-1.0)
- Panel 4: Calibration error over time (24h rolling window)
- Panel 5: Overconfidence ratio by query type (different domains may have different miscalibration)

### Health Checks
```sql
-- Daily calibration audit
SELECT 
  DATE(timestamp) as date,
  COUNT(*) as total_answers,
  AVG(CASE WHEN is_correct THEN confidence ELSE NULL END) as avg_conf_correct,
  AVG(CASE WHEN NOT is_correct THEN confidence ELSE NULL END) as avg_conf_incorrect,
  (AVG(CASE WHEN NOT is_correct THEN confidence ELSE NULL END) / 
   NULLIF(AVG(CASE WHEN is_correct THEN confidence ELSE NULL END), 0)) as overconfidence_ratio,
  CORR(confidence, is_correct) as confidence_accuracy_correlation
FROM model_outputs
WHERE timestamp > NOW() - INTERVAL 1 DAY
GROUP BY DATE(timestamp)
HAVING overconfidence_ratio > 1.2 OR confidence_accuracy_correlation < 0.6 
  THEN ALERT "Confidence miscalibration detected"
```

---

## Related Patterns

**Parent Pattern**: [Hallucination: Base Mechanism](hallucination-base-mechanism.md) — This is a sub-pattern of the universal hallucination mechanism. The base pattern covers why models generate false content; this pattern focuses on the confidence miscalibration aspect.

**Domain-Specific Variants**:
- **[Hallucination in RAG](../../../by-capability/knowledge-retrieval/goals/answer-synthesis/failures/confidence-miscalibration.md)** — Confidence miscalibration in answer synthesis from retrieved documents
- **[Hallucination in Document Processing](../../../by-capability/document-processing/goals/multimodal-reliability/failures/confidence-miscalibration.md)** — VLM confidence errors in document extraction
- **[Hallucination in Vision](../../../by-capability/vision-and-images/goals/visual-hallucination/failures/confidence-miscalibration.md)** — Vision model confidence on hallucinated objects and attributes

**Related Patterns**:
- [Attribute Hallucination](hallucination-attribute.md) — Hallucinated attributes on correct objects
- [Object Hallucination](hallucination-object.md) — Hallucinated objects not in input

---

## References

- [Stanford Legal RAG Hallucinations](https://dho.stanford.edu/wp-content/uploads/Legal_RAG_Hallucinations.pdf) — Confidence without accuracy in legal RAG systems
- [CMARix: RAG & AI Trust Statistics 2026](https://www.cmarix.com/blog/rag-ai-statistics/) — Trust calibration issues
- [On Calibration of Modern Neural Networks](https://arxiv.org/abs/1706.04599) — Temperature scaling and calibration
- [Measuring Hallucinations in Large Language Models](https://arxiv.org/abs/2404.07143) — Calibration analysis of LLMs
- [Confidence Calibration and Predictive Uncertainty Quantification for Deep Learning](https://arxiv.org/abs/2006.11941) — Uncertainty estimation in neural networks
