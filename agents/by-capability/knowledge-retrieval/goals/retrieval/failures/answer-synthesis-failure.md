# Answer Synthesis Failure

## Issue: Correct information is retrieved but summarized incorrectly.

**Frequency**: Common

**Symptoms**
- Cited source correct; final answer wrong.
- [Add more specific symptoms]

**Root Cause**
Correct information is retrieved but summarized incorrectly.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Extract-Then-Synthesize Approach**: Instead of free-form synthesis, extract key facts from retrieved chunks first (as structured data: key, value, source). Then synthesize answer from extracted facts. Reduces paraphrasing errors.
2. **Synthesis Correctness Eval Suite**: Build eval dataset with retrieved-chunks → expected_answer pairs. Measure synthesis model accuracy. Run evals regularly. Alert on degradation. Target: > 95% synthesis correctness.
3. **Citation-Grounded Synthesis**: Require synthesis model to cite source for every claim. Generate answer with inline citations. Post-synthesis validation: verify each claim has supporting citation.

### Detection & Response
1. **Synthesis Error Detection**: Compare final_answer to extracted_facts from retrieved_chunks. Use NLI or semantic similarity to check consistency. Alert on significant divergence between facts and answer.
2. **User Feedback on Synthesis**: Track user feedback ('answer is correct', 'answer contradicts source', 'answer is incomplete'). Compute synthesis_accuracy from feedback. Alert if drops < 90%.
3. **Source-Answer Consistency Audit**: Periodically audit synthesized answers against source chunks (weekly sample 100). Domain experts rate answer correctness. Track accuracy by query_type.

### Architecture Patterns
1. **Extraction-to-Synthesis Pipeline**: Stage 1 - Extract facts: Run fact extraction on retrieved chunks (output: structured_facts_list). Stage 2 - Synthesize: Synthesize answer from structured_facts, enforce citations. Stage 3 - Verify: Validate answer against facts.
2. **Synthesis Model Temperature Reduction**: Use lower temperature (T=0.3) for synthesis vs generation to reduce hallucination/paraphrasing errors. Trade off creativity for factuality.
3. **Iterative Synthesis with Feedback**: Generate initial answer → validate against source → identify errors → regenerate with corrections → validate again. Multi-pass approach improves accuracy.

### Metrics
1. **synthesis_correctness_percent**: Target: > 95%; Alert threshold: < 90%; % answers correctly synthesized
2. **answer_source_consistency_percent**: Target: > 95%; Answer consistent with cited sources
3. **synthesis_error_types_distribution**: Track: hallucination, paraphrasing_error, logic_error, omission. Alert if any type > 2%
4. **user_feedback_synthesis_accuracy_percent**: Target: > 90%; Users confirm answer is correct
5. **source_answer_consistency_audit_agreement_percent**: Target: > 95%; Expert auditors agree answer is correct

### Alerts
1. **Synthesis Error Detected** (P1 - Critical): Condition - final_answer conflicts with source_facts OR fails consistency check. Action: Block answer, escalate, regenerate with extraction approach, investigate synthesis model quality.
2. **Synthesis Accuracy Degradation** (P1 - Critical): Condition - synthesis_correctness drops > 10% month-over-month. Action: Investigate synthesis model performance, review recent errors, potential model retraining or rollback.
3. **High Synthesis Error Rate by Type** (P2 - Warning): Condition - specific error type (e.g., hallucination) > 5%. Action: Target error type in mitigation (reduce temperature for hallucination, add extraction step for omissions).

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
