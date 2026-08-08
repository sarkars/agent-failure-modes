# Answer Synthesis Failure

## Issue: Correct information is retrieved but summarized incorrectly.

**Frequency**: Common

**Symptoms**
- Cited source correct; final answer wrong.
- Answer flips a negation from the source ("does not require" becomes "requires") during paraphrasing.
- Numeric values in the answer don't match the numbers in the cited chunk (off-by-one unit conversion, wrong column read from a table-like chunk).
- Answer merges facts from two different retrieved chunks into a claim neither chunk actually supports.

**Root Cause**
The synthesis step is built to paraphrase rather than extract, and with no structured intermediate representation (facts pulled out as key/value pairs tied to their source) standing between the retrieved chunk and the generated sentence, paraphrasing is free to compress away exactly the qualifiers — negations, exceptions, conditionals — that change a claim's meaning. Long chunks with multiple qualifying clauses compound this because the model's attention concentrates on whichever clause most closely matches the query's surface wording, and with no automated check comparing the polarity of the generated answer against the polarity of the source claim, a flipped negation or merged fact passes through with the same confidence as a faithful summary.

**Example**
```
Retrieved chunk: "Refunds are not available for digital purchases after the 7-day
trial period, except where required by local consumer law."
Synthesized answer to the user: "You can get a refund for your digital purchase
since you're past the 7-day trial period." The synthesis step inverted the
exception clause into the main rule while compressing the sentence for readability.
```

**Contributing Factors**
- Synthesis model paraphrases instead of extracting, so negations, exceptions, and conditionals are the first things lost to compression.
- No structured intermediate representation (facts extracted as key/value/source) between retrieval and the final generated sentence.
- Long chunks with multiple qualifying clauses get truncated in the model's attention to the sentence that matches the query's surface wording.
- No automated check comparing the polarity (affirmative/negative) of the answer against the polarity of the source claim.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Negation preservation | Chunk contains "not X except Y"; ask for a direct yes/no answer | Answer preserves the exception and the negation | Answer states the general case as unconditionally true |
| Multi-chunk merge | Two chunks each partially answer the question | Answer clearly attributes each fact to its own source, doesn't invent a combined claim | Answer states a claim no single chunk supports |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| synthesis_correctness_percent | > 95% | Sample synthesized answers, compare against source chunks with human or NLI-based grading |

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
| answer_source_consistency_percent | < 90% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Polarity Mismatch | Answer's affirmative/negative polarity diverges from the cited source's polarity | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
