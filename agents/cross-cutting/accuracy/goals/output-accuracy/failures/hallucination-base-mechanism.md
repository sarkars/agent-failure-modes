# Hallucination: Base Mechanism

## Issue: Large Language and Vision Models Generate Plausible but False Content

**Frequency**: Very Common

**Symptoms**
- Model produces confident, well-formatted answers without evidence
- Content is thematically consistent but factually wrong
- False information is fluent and grammatically correct
- Model adds details that weren't in the source material
- Confidence levels don't correlate with accuracy

**Root Cause**
LLMs and vision models are trained to maximize the probability of the next token given the context. This training objective optimizes for fluency and coherence, not truthfulness. When the model encounters ambiguous input, missing context, or information outside its training distribution, it defaults to generating plausible content based on learned statistical patterns. The model has no built-in mechanism to distinguish between what it genuinely learned from training data versus what it can plausibly generate. This is fundamentally different from a retrieval system that can only recombine existing content.

**Example**
```
Scenario 1 (RAG): User asks "What are the Q3 2024 revenue targets?"
Context provided: Q1-Q2 2024 actual results (no Q3 targets mentioned)
Model output: "Q3 2024 revenue target is $12.5M with 18% YoY growth"
Reality: No Q3 targets were provided; model inferred plausible number

Scenario 2 (Vision): Image shows a box in poor lighting
Model output: "Red box, 95% confidence"
Reality: Box is red, but appears dark gray due to shadow; model corrected to common training pattern

Scenario 3 (Document Processing): Invoice lacks PO number field
Model output: "PO Number: PO-2024-1234"
Reality: No PO number exists in document; model hallucinated based on "typical invoice template" prior
```

**Key Statistics**
- 20-40% of LLM responses include at least one hallucinated detail
- Vision models hallucinate objects in 15-25% of cluttered scenes
- Hallucination rate increases with model temperature and sampling diversity
- Confidence on hallucinated content averages 70-85% (only 5-15% lower than on correct content)

**Contributing Factors**
- Ambiguous or incomplete input context
- Domain knowledge outside model's training cutoff
- Low-resolution or degraded input (vision)
- Conflicting or contradictory sources
- Model temperature/sampling settings that encourage diversity
- Training data imbalance (overrepresented patterns learned more strongly)

---

## Test Scenario & Reproduction

### Scenario Setup
Deploy a model in a controlled environment where you can:
- Provide partial or ambiguous input
- Compare model output to ground truth
- Vary input conditions (resolution, context completeness, ambiguity level)
- Measure confidence levels independently

### Trigger Mechanism
Hallucinations reliably occur when:
1. Model is asked about information not in the provided context
2. Input context is incomplete or ambiguous
3. Model has high diversity/temperature settings
4. Vision input is low-resolution or contains optical artifacts
5. Optional fields or rarely-present entities are queried

**Example Reproduction Steps:**
```
1. Prepare dataset with questions, incomplete context, and ground truth answers
2. Run model on incomplete context (e.g., Q1-Q2 results, ask about Q3)
3. Compare outputs to ground truth
4. Measure: % of outputs containing hallucinated details
5. Measure: confidence scores on hallucinated vs. correct content
6. Repeat with different temperatures/sampling settings
7. Record correlation: higher temperature → more hallucinations?
```

### Expected Failure State
- Model confidently produces content not supported by input
- False content is syntactically correct and thematically consistent
- Confidence scores are high (0.6-0.95) despite errors
- Failures are reproducible with the same inputs at temperature > 0.5
- Vision hallucinations increase with image degradation (lower resolution, poor lighting)

### Mitigation Validation Protocol

**Test Checklist:**
- [ ] Reproduce hallucination on baseline model → confirm it occurs
- [ ] Apply mitigation strategy (e.g., grounding, retrieval verification, confidence thresholding)
- [ ] Re-run reproduction steps → confirm hallucination is reduced or prevented
- [ ] Measure improvement: baseline hallucination rate → post-mitigation rate
- [ ] Verify no regression: accuracy on well-grounded answers unchanged

**Success Criteria:**
- Hallucination rate reduced by ≥50% (e.g., 30% → 15%)
- Confidence on hallucinated content drops significantly (0.7+ → 0.3-0.5 range)
- Accuracy on non-hallucinated content unchanged
- Latency impact < 10%

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Missing context | Provide partial facts, ask about missing info | Low confidence or explicit "unknown" | High-confidence answer not in context |
| Ambiguous vision | Low-res/shadowed object image | Low confidence or conservative classification | High confidence despite image quality issues |
| Empty document field | Document without optional field, ask for it | "Field not present" or low confidence | High-confidence hallucinated value |
| Conflicting sources | Two sources with contradictory facts | Acknowledgement of conflict | Confident selection of one without noting contradiction |
| Out-of-distribution | Ask about non-existent entity | "Not found" or uncertainty | Plausible-sounding false answer |

### Evaluation Dataset
- **Source**: CustomQA datasets with deliberately incomplete context, vision datasets with degraded images, document extraction benchmarks with optional fields
- **Size**: 1,000+ examples covering hallucination scenarios
- **Key variations**: Context completeness (0%, 50%, 100%), image resolution (32px-512px), field presence/absence

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Hallucination Rate | <10% | % of outputs containing details not in input context |
| Confidence-Accuracy Correlation | >0.7 Spearman correlation | Calibration: does high confidence = high accuracy? |
| Grounding Success Rate | >95% | % of output claims traceable to input source |
| False Positive Rate on Empty Input | <5% | % of confident answers when context is empty |

### Automated Checks
```python
def detect_hallucinations(output, context, ground_truth):
    """Identify hallucinated details in model output"""
    hallucinations = []
    
    # Check if each claim in output is grounded in context
    claims = extract_claims(output)
    for claim in claims:
        if not claim_in_context(claim, context):
            # This claim isn't in the provided context
            hallucinations.append({
                'claim': claim,
                'confidence': output.confidence_for_claim(claim),
                'in_ground_truth': claim in ground_truth
            })
    
    hallucination_rate = len(hallucinations) / len(claims)
    avg_confidence_on_halluc = mean(h['confidence'] for h in hallucinations)
    
    return {
        'hallucinations': hallucinations,
        'rate': hallucination_rate,
        'avg_confidence_on_hallucinated': avg_confidence_on_halluc
    }
```

---

## Mitigation Strategies

### Prevention

1. **Retrieval-Augmented Generation (RAG) with Grounding**: Require the model to ground every claim in retrieved documents. For every fact in the output, include a citation to the specific source passage. This structurally prevents the model from generating unsupported content because it must point to evidence.

2. **Confidence Scoring and Uncertainty Quantification**: Train or fine-tune models to output confidence scores per fact/token. Flag claims with confidence < 0.6 as uncertain. In critical applications, require human review for all uncertain claims rather than using the model's default answer.

3. **Constrained Generation and Schema Validation**: Use constrained decoding to limit output to a predefined schema (e.g., "only fields that exist in the document can be populated"). This prevents the model from inventing fields or attributes not in the input.

### Detection & Response

1. **Fact Verification Against Source**: After generation, verify each extracted fact against the source material. Use string matching, semantic similarity, or a secondary verification model to check if claims are actually in the source. Flag mismatches for review.

2. **Hallucination Signature Detection**: Monitor for patterns characteristic of hallucinations: high confidence with no clear grounding, fluent prose that diverges from source style, implausible-but-consistent details. Use these as red flags to route to human review.

3. **Ensemble Disagreement Monitoring**: Run outputs through multiple model variants (different checkpoints, temperatures, prompts). If models strongly disagree on a claim, it's likely uncertain territory and should be flagged as potentially hallucinated.

### Architecture Patterns

1. **Grounding-First Pipeline**: Retrieve relevant source materials first, then condition generation on retrieved content. Require explicit citation of sources for every claim. Reject outputs that contain claims without citations.

2. **Staged Confidence Checking**: First-pass: generate output. Second-pass: extract claims and measure confidence. Third-pass: verify high-stakes claims against external sources. Only deliver claims that pass both confidence and verification checks.

3. **Human-in-the-Loop for Low-Confidence Outputs**: Flag any output or claim with confidence < threshold for human review before presenting to user. Threshold depends on domain (medical: 0.95, general Q&A: 0.7).

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `hallucination_rate` | % of outputs containing unsourced claims | >15% over 1-hour window |
| `avg_confidence_on_hallucinated_claims` | Average confidence score on hallucinated vs. correct claims | >0.1 difference (should be much lower on hallucinated) |
| `fact_verification_failure_rate` | % of claims that fail verification against sources | >10% |
| `grounding_rate` | % of claims with valid citations to source | <90% |
| `user_correction_rate` | % of queries where user corrects model output | >5% baseline |

### Logs & Traces
- Log every claim with its confidence score and source grounding
- Include model checkpoint version, temperature/sampling settings
- Track which claims fail fact-verification checks
- Log user feedback: "this is wrong" / "this is correct" for learning

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High Hallucination Rate Spike | Hallucination rate exceeds 15% for >1 hour | P1 | Pause autonomous generation; investigate data drift or model regression |
| Confidence-Accuracy Mismatch | Avg confidence on hallucinated claims > 0.7 | P2 | Model confidence miscalibrated; retrain or adjust thresholds |
| Fact Verification Failures | >10% of claims fail source verification | P1 | Check fact-verification pipeline; may indicate source data quality issue |
| Grounding Missing | Claims lacking citations >10% | P2 | Verify retrieval and citation generation working; may need prompt adjustment |

### Dashboard Panels
- Panel 1: Hallucination rate over time (24h rolling window, split by model/prompt)
- Panel 2: Confidence distribution for hallucinated vs. correct claims (histogram)
- Panel 3: Fact-verification failure rate by claim type (numbers, dates, entities, opinions)
- Panel 4: User correction/feedback rate (time series)
- Panel 5: Citation coverage (% of claims with valid sources)

### Health Checks
```sql
-- Daily hallucination audit
SELECT 
  DATE(timestamp) as date,
  COUNT(*) as total_claims,
  SUM(CASE WHEN is_hallucinated THEN 1 ELSE 0 END) as halluc_count,
  AVG(CASE WHEN is_hallucinated THEN confidence ELSE NULL END) as halluc_avg_confidence,
  AVG(CASE WHEN NOT is_hallucinated THEN confidence ELSE NULL END) as correct_avg_confidence,
  SUM(CASE WHEN verification_failed THEN 1 ELSE 0 END) as verification_failures
FROM model_outputs
WHERE timestamp > NOW() - INTERVAL 1 DAY
GROUP BY DATE(timestamp)
HAVING halluc_count / total_claims > 0.15 THEN ALERT "Hallucination rate exceeded threshold"
```

---

## Domain-Specific Variants

This is the universal hallucination mechanism. See domain-specific variants for implementation guidance in particular contexts:

- **[Hallucination in RAG/Answer Synthesis](../../../by-capability/knowledge-retrieval/goals/answer-synthesis/failures/confidence-miscalibration.md)** — Hallucinations in LLM-generated answers from retrieved documents
- **[Hallucination in Document Processing](../../../by-capability/document-processing/goals/multimodal-reliability/failures/object-hallucination.md)** — Hallucinations in VLM-based document extraction (phantom fields, wrong values)
- **[Hallucination in Vision-Based Tasks](../../../by-capability/vision-and-images/goals/visual-hallucination/failures/object-hallucination.md)** — Hallucinations in object detection and scene understanding

---

## References

- [Hallucination of Multimodal LLMs Survey](https://arxiv.org/html/2404.18930v2) — Comprehensive taxonomy of hallucination types
- [Factuality in Language Models: Hallucinations, Logic, and Open Challenges](https://arxiv.org/abs/2310.07521) — Analysis of why models hallucinate
- [On Hallucination and Predictive Uncertainty in Conditional Language Generation](https://arxiv.org/abs/1703.02952) — Early work on LLM hallucination mechanisms
- [Improving Language Models by Segmenting, Attending, and Predicting the Future](https://arxiv.org/abs/2108.02117) — Training approaches to reduce hallucinations
- [LLMs as Factual Reasoners: Instruction Tuning for Linguistic Calibration](https://arxiv.org/abs/2310.01415) — Confidence calibration in LLMs
