# Verifier Hallucination

## Issue: Evaluator invents reasons to pass/fail.

**Frequency**: Occasional

**Symptoms**
- Judge rationale unsupported by evidence.
- The verifier's stated rationale cites a fact, quote, or detail that does not actually appear anywhere in the output being judged.
- Re-running the same verifier judgment on the same output produces a different verdict and a different (equally confident-sounding) rationale each time.

**Root Cause**
This happens because the verifier is typically prompted with an open-ended "is this good?" judgment rather than a rubric that requires citing a specific quoted span for each criterion, leaving it free to generate a plausible-sounding rationale without any grounding requirement. Nothing automatically checks whether the verifier's cited evidence actually appears in the output it's judging, only a single verifier runs per case so there's no cross-verifier disagreement to catch a fabricated rationale a second independent judge wouldn't reproduce, and verifier judgments are trusted as final without any reproducibility testing -- repeating the same judgment on the same output -- that would expose inconsistent, post-hoc justification generation.

**Example**
```
An LLM-judge verifier is asked to grade whether a support response "correctly cited the
refund policy." The response never mentions a refund policy at all -- it's off-topic. The
verifier nonetheless outputs: "PASS - the response correctly cites the 14-day refund
policy in paragraph two." No such paragraph or citation exists in the response; the
verifier fabricated a plausible-sounding justification that matches the shape of a good
rationale without any of it being grounded in the actual text it was supposed to check.
```

**Contributing Factors**
- Verifier is prompted with an open-ended "is this good?" judgment rather than a rubric that requires citing a specific quoted span for each criterion.
- No automated check exists to confirm the verifier's cited evidence actually appears in and supports the output being judged.
- Only a single verifier runs per case, so there's no cross-verifier disagreement signal to catch a fabricated rationale that a second independent verifier wouldn't reproduce.
- Verifier judgments are trusted as final without any reproducibility testing (same output judged multiple times) that would reveal inconsistent, post-hoc rationale generation.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Fabricated citation detection | Off-topic response graded against a rubric criterion requiring a specific citation | Verifier fails the response since no matching citation exists | Verifier passes the response and cites a quote/paragraph that isn't present |
| Judgment reproducibility check | Same output judged by the same verifier 5 times | Same verdict and consistent rationale each run | Verdict or rationale changes across repeated runs on identical input |
| Cross-verifier agreement | Same output judged by two independently configured verifiers | Verifiers agree on verdict and cite overlapping evidence | Verifiers disagree, or one verifier's evidence citation doesn't match the other's |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| ungrounded_rationale_rate_pct | < 2% of verifier judgments lack matching evidence | Automated check comparing verifier-cited evidence spans against the actual output text |
| cross_verifier_agreement_rate_pct | > 90% | Run matched samples through 2+ independent verifiers and measure verdict agreement |
| judgment_reproducibility_rate_pct | > 95% same verdict on re-run | Re-run the same verifier on identical outputs multiple times and measure verdict consistency |

---

## Mitigation Strategies

### Prevention
1. **Evidence-Grounded Verifier Prompting**: Require the verifier to quote or cite the specific span of the output and the specific criterion it's checking for every pass/fail decision, rejecting judgments that don't include a traceable citation — this structurally prevents free-floating unsupported rationale.
2. **Rubric-Constrained Judging**: Constrain the verifier to a fixed, enumerated rubric with explicit pass/fail criteria per item (not open-ended "is this good?" judgment), reducing the surface area for the verifier to invent novel, unsupported justifications.
3. **Cross-Verifier Disagreement as a Gating Signal**: Run judgments through at least two independently-configured verifiers (different model, different prompt phrasing, or a rule-based check where feasible) and require agreement, or route to human review on disagreement, since hallucinated rationale is unlikely to reproduce identically across independent verifiers.

### Detection & Response
1. **Rationale-Evidence Consistency Checking**: Automatically check whether the verifier's cited evidence (quoted span, referenced fact) actually appears in and supports the judgment on the output being evaluated; flag rationales that cite non-existent or mismatched evidence.
2. **Human Audit of Verifier Rationale Quality**: Sample verifier judgments (weighted toward borderline/failing cases) for human review specifically assessing whether the stated rationale is factually grounded, not just whether the final pass/fail call was "reasonable."
3. **Judgment Reproducibility Testing**: Re-run the same verifier judgment multiple times (or with minor prompt perturbation) on the same output; low reproducibility of both the verdict and the stated rationale indicates the verifier is generating post-hoc justifications rather than grounded assessments.

### Architecture Patterns
1. **Citation-Required Verifier Output Schema**: The verifier is required to output structured judgments (criterion_id, verdict, evidence_span, evidence_location) rather than free-text rationale, with a downstream check that evidence_span is actually present in the source output before the verdict is accepted.
2. **Multi-Verifier Consensus Gate**: The judgment pipeline routes each case through 2+ independently configured verifiers and only auto-accepts a verdict when they agree; disagreement routes to human adjudication, with disagreement cases logged for verifier prompt improvement.
3. **Rationale Audit Sampling Service**: A background service continuously samples verifier judgments, checks evidence-grounding automatically where possible, and routes a stratified sample to human reviewers, feeding confirmed hallucinated-rationale cases back into verifier prompt/rubric refinement.

### Metrics
1. **ungrounded_rationale_rate_pct**: Target: < 2% of verifier judgments lack matching evidence; Alert threshold: > 8%
2. **cross_verifier_agreement_rate_pct**: Target: > 90%; Alert threshold: < 75%
3. **judgment_reproducibility_rate_pct**: Target: > 95% same verdict on re-run; Alert threshold: < 85%
4. **human_audit_rationale_quality_score**: Target: > 4.5/5 average; Alert threshold: < 3.5/5

### Alerts
1. **Ungrounded Rationale Rate Spike** (P1 - Critical): Condition - automated evidence-consistency check finds ungrounded rationale rate above 8%. Action: Suspend affected verifier as an auto-gate, fall back to human review, initiate verifier prompt/rubric redesign.
2. **Cross-Verifier Disagreement Surge** (P2 - Warning): Condition - agreement rate between independent verifiers drops below 75%. Action: Route all disagreement cases to human adjudication, investigate which verifier is drifting.
3. **Judgment Reproducibility Failure** (P2 - Warning): Condition - re-run testing shows verdict/rationale reproducibility below 85%. Action: Treat verifier as unreliable for auto-gating, escalate for review and possible replacement.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| ungrounded_rationale_rate_pct | > 8% |
| cross_verifier_agreement_rate_pct | < 75% |
| judgment_reproducibility_rate_pct | < 85% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Ungrounded Rationale Rate Spike | Automated evidence-consistency check finds ungrounded rationale rate above 8% | High |
| Cross-Verifier Disagreement Surge | Agreement rate between independent verifiers drops below 75% | Medium |
| Judgment Reproducibility Failure | Re-run testing shows verdict/rationale reproducibility below 85% | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
