# What Are the Most Common Output Accuracy Failures in AI Agents?

**Agents generate plausible but false content when parametric knowledge lacks evidence, input is ambiguous, or the model defaults to learned patterns over retrieval — hallucinations and fabrications are particularly dangerous because they're well-formed and grammatically correct, so they pass basic sanity checks and propagate downstream before external validation surfaces the error.** Output accuracy failures concentrate in open-ended generation (summarization, synthesis) where there's no single "correct" answer and in scenarios where the agent has high confidence but low actual knowledge.

## Key Takeaways

- 16 distinct failure patterns affect output correctness, grouped into four mechanisms: hallucination (generating plausible content not in source), bias (systematic errors favoring certain entities or groups), domain mismatches (applying training knowledge outside its valid scope), and data quality (inheriting errors from upstream sources).
- Accuracy failures are nearly invisible at generation time — a hallucinated fact is a well-formed, grammatically correct fact that reads indistinguishably from true facts, so the agent's output passes syntactic checks and only fails when compared to ground truth.
- The reliable fix is architectural, not model-only: mark certain queries as requiring retrieval-augmented generation rather than parametric knowledge; gate high-stakes outputs behind verification (requiring evidence for every claim); track confidence-accuracy correlation to detect miscalibration; disaggregate performance by entity type and group to catch bias.
- Hallucination rates don't improve significantly with model size or capability — better models are more confident when wrong, worsening false confidence and making the failures more dangerous.

## Scope

- **Hallucination (base mechanism)** — [hallucination-base-mechanism](failures/hallucination-base-mechanism.md). Models generate plausible content based on learned patterns when input is ambiguous, incomplete, or outside training distribution; the generation mechanism itself has no built-in check for truthfulness.
- **Hallucination variants** — [hallucination-confidence-miscalibration](failures/hallucination-confidence-miscalibration.md), [hallucination-attribute](failures/hallucination-attribute.md), [hallucination-object](failures/hallucination-object.md). Confidence scores don't correlate with accuracy; false attributes added to correct objects; false entities/fields not in source.
- **Fabrication** — [content-fabrication](failures/content-fabrication.md), [confident-fabrication](failures/confident-fabrication.md). Agent generates entire false answers without evidence; agent generates false answers with high confidence despite having no knowledge of the topic.
- **Bias and discrimination** — [bias-amplification](failures/bias-amplification.md), [algorithmic-discrimination](failures/algorithmic-discrimination.md). Systematic errors favoring certain entities, demographics, or groups; model learns and reinforces historical biases from training data.
- **Scope mismatches** — [domain-mismatch](failures/domain-mismatch.md), [extrapolation](failures/extrapolation.md). Agent applies training knowledge outside its valid scope; agent extrapolates beyond training domain with false confidence.
- **Upstream error propagation** — [inherited-errors](failures/inherited-errors.md), [entity-confusion](failures/entity-confusion.md), [source-misattribution](failures/source-misattribution.md). Agent inherits errors from upstream sources; agent confuses entity identity and mixes properties; agent attributes facts to wrong sources.
- **Verification failure** — [verification-failure](failures/verification-failure.md). Agent fails to verify extracted values; false values propagate as "verified correct."

## When Output Accuracy Matters

- Agent generates content that flows directly to end users or business processes without intermediate human review (customer-facing summaries, autonomous decision-making)
- Agent combines information from multiple sources (retrieval, tools, reasoning) and discrepancies or false-fusions surface only on external audit
- High-stakes domains (healthcare, finance, legal) where accuracy errors have compliance, safety, or reputational impact
- Vulnerable populations or underrepresented groups where bias in training data translates to systematic failures

## Cross-Pattern Insight

Across all 16 patterns, the single most reliable mitigation is evidence-gating: require the agent to cite evidence for every claim and reject claims that lack evidence, even if the model is confident. Cases where agents are forced to generate only retrieval-augmented answers (with evidence explicitly required) show dramatic accuracy improvement. The second universal mitigation is disaggregated accuracy tracking — report accuracy overall and separately by entity type, demographic group, domain, and complexity, so bias and domain-mismatch failures surface as breakdowns in specific segments rather than being masked by overall-accuracy averages. When accuracy is reported as a single number, the failures in underrepresented groups are invisible.

## Frequently Asked Questions

### How does output accuracy differ from hallucination?
Hallucination is one class of output accuracy failures — false content generated from patterns. Output accuracy covers hallucination plus bias, domain mismatches, and errors inherited from upstream sources. See the Scope section above for the full breakdown.

### Can you prevent hallucination by lowering model temperature or sampling diversity?
Lowering temperature reduces hallucination rate but increases false negatives (missing correct answers). Better approaches are evidence-gating (require retrieval) and confidence-calibration training (learn when the model actually knows). Temperature is a tuning dial, not a solution.

### Do more capable models hallucinate differently?
Better models are more fluent — they generate more plausible-sounding false answers. Accuracy doesn't improve faster than fluency with model scale, so the gap between confidence and correctness widens. Capability doesn't improve hallucination awareness.

### Which output accuracy failures matter most for production systems?
Confident fabrication (high confidence on completely false answers) and bias amplification (systematic errors against minority groups) are highest-priority, as they're invisible to standard testing and carry highest reputational/regulatory risk. Hallucination-base-mechanism is easier to test for and slower-moving but affects almost all outputs.

## Patterns

| Pattern | Mechanism |
|---------|-----------|
| [Algorithmic Discrimination](failures/algorithmic-discrimination.md) | Model systematically generates wrong answers for certain entities, demographics, or groups |
| [Bias Amplification](failures/bias-amplification.md) | Model learns and reinforces historical biases from training data, amplifying minority-group errors |
| [Confident Fabrication](failures/confident-fabrication.md) | Agent generates entirely false answers with high confidence despite having no knowledge |
| [Content Fabrication](failures/content-fabrication.md) | Agent generates false content not supported by sources or reasoning |
| [Domain Mismatch](failures/domain-mismatch.md) | Agent applies training knowledge outside its valid scope without recognizing domain boundary |
| [Entity Confusion](failures/entity-confusion.md) | Agent confuses entity identity and mixes properties from different entities |
| [Extrapolation](failures/extrapolation.md) | Agent extrapolates beyond training domain with false confidence |
| [Hallucination: Attributes](failures/hallucination-attribute.md) | Agent adds false properties to correct objects/entities |
| [Hallucination: Base Mechanism](failures/hallucination-base-mechanism.md) | Models generate plausible content based on patterns when input is ambiguous or outside training distribution |
| [Hallucination: Confidence Miscalibration](failures/hallucination-confidence-miscalibration.md) | Confidence scores don't correlate with accuracy; model confident on false hallucinations |
| [Hallucination: Objects](failures/hallucination-object.md) | Agent generates false entities, fields, or references not in input |
| [Inherited Errors](failures/inherited-errors.md) | Agent inherits errors from upstream sources without catching or correcting them |
| [Source Misattribution](failures/source-misattribution.md) | Agent attributes facts to wrong sources; mixes citations |
| [Verification Failure](failures/verification-failure.md) | Agent fails to verify extracted values; false values propagate as verified |

**Total: 16 patterns**

## Related Goals

- [Output Verification](../output-verification/) — validation of extracted values, upstream of accuracy issues
- [Evaluation Reliability](../evaluation-reliability/) — testing methodology that should catch accuracy failures
- [Reasoning Quality](../reasoning-quality/) — reasoning failures that underlie many accuracy errors
