# Self-Verification Bias

## Issue: Same model judges its own flawed output.

**Frequency**: Occasional

**Symptoms**
- Self-critique passes known wrong answer.
- The same model family consistently rates its own output higher than an independent verifier rates matched outputs, even when the underlying quality is identical.
- A known-error injection test shows the self-verification step passing outputs from a labeled bank of confirmed-wrong answers at a nontrivial rate.

**Root Cause**
Same model judges its own flawed output.

**Example**
```
A code-generation agent is asked to write a function and then self-critique its own
output for bugs before returning it. The generated function has an off-by-one error in a
loop boundary -- a mistake rooted in the same reasoning pattern the model tends to make
whenever it reasons about loop bounds. When asked to self-critique, the model reviews its
own code using the same flawed mental model that produced the bug in the first place, and
confidently reports "no issues found." An independent verifier (a different model, or
simply running the test suite) would have caught the off-by-one immediately, but the
self-critique step shares the exact blind spot it's supposed to catch.
```

**Contributing Factors**
- Verification is implemented as the same model critiquing its own output, sharing whatever systematic reasoning blind spots produced the original error.
- No independent, architecturally separate verifier (different model family, tool-grounded check, rule-based validator) exists to catch errors the generator's own self-assessment cannot see.
- No known-error injection testing exists to measure how often the self-verifier passes known-wrong outputs, so the bias goes undetected until it causes a production incident.
- Self-critique is treated as a sufficient gate on its own rather than a cheap first pass that should be followed by an externally grounded check.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Known-error injection | Labeled bank of confirmed off-by-one/logic bugs fed through self-critique | Self-verifier flags the known bug | Self-verifier passes the known-wrong output as correct |
| Self vs. independent verifier gap | Same generated output scored by both self-critique and an independent model/tool-grounded check | Flag rates are comparable between the two | Self-verifier flags substantially fewer issues than the independent verifier |
| Test-execution ground truth | Generated code with a hidden bug, run through both self-critique and the actual test suite | Test suite catches the bug regardless of self-critique's verdict | Self-critique passes code that the test suite proves is broken |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| known_error_pass_through_rate_pct | < 2% of known-wrong outputs pass self-verification | Replay a labeled known-error bank through self-verification and measure pass-through rate |
| self_vs_independent_verifier_flag_gap_pct | < 10 point gap | Compare flag rates of self-verifier vs. independent verifier on matched output samples |
| cross_verifier_disagreement_rate_pct | Tracked, escalation-driving | Log disagreement rate between self and independent verifiers on the same outputs |

---

## Mitigation Strategies

### Prevention
1. **Independent Verifier Model/Architecture**: Use a verifier that is architecturally or provenance-independent from the generator (different model family, different training data emphasis, or a rule-based/retrieval-grounded checker) rather than the same model critiquing its own output, since shared blind spots mean self-critique systematically misses the same error classes.
2. **Tool-Grounded Verification Over Self-Critique**: Where possible, replace or supplement self-critique with verification against an external, non-model source of truth (code execution, calculator, database lookup, search) that cannot share the generator's reasoning errors.
3. **Ensemble Disagreement as a Verification Signal**: Run verification via multiple independent models/prompts and treat disagreement among them as a signal requiring escalation, rather than accepting a single self-consistent judgment as sufficient.

### Detection & Response
1. **Known-Error Injection Testing**: Periodically inject known-wrong outputs (from a labeled error bank) into the self-verification step and measure how often the verifier incorrectly passes them; a high pass-through rate on known errors is direct evidence of self-verification bias.
2. **Verifier-Generator Agreement Rate Tracking**: Track how often the self-verifier flags issues in the generator's own output versus an independent verifier's flag rate on the same outputs; a self-verifier flagging substantially less than an independent verifier indicates bias.
3. **Cross-Verifier Disagreement Escalation**: When using multiple verifiers (self + independent), log and escalate any case where they disagree, using these cases both for human review and to expand the known-error injection test bank.

### Architecture Patterns
1. **Independent Verifier Service**: Verification is implemented as a separate service using a different model, prompt strategy, or grounding mechanism (retrieval/tool execution) than the generator, deployed and versioned independently so it isn't updated in lockstep with generator changes that might introduce shared errors.
2. **Self-Critique-Plus-External-Check Pipeline**: Self-critique is retained as a cheap first pass but is never sufficient alone — outputs that pass self-critique still route through at least one externally grounded check (tool execution, source match) before being treated as verified.
3. **Known-Error Regression Bank for Verifiers**: A maintained dataset of previously confirmed generator errors is replayed against any verifier (self or independent) before it's trusted in production, and again on every verifier update, to continuously test for blind-spot overlap.

### Metrics
1. **known_error_pass_through_rate_pct**: Target: < 2% of known-wrong outputs pass self-verification; Alert threshold: > 10%
2. **self_vs_independent_verifier_flag_gap_pct**: Target: < 10 point gap; Alert threshold: > 25 point gap
3. **cross_verifier_disagreement_rate_pct**: Target: tracked, escalation-driving; Alert threshold: > 15% of cases disagree
4. **verifier_blind_spot_bank_size**: Target: growing (>= 5 new cases/month from disagreements); Alert threshold: 0 growth for a quarter

### Alerts
1. **Known-Error Pass-Through Detected** (P1 - Critical): Condition - known-error injection test shows self-verifier pass-through rate above 10%. Action: Disable self-verification as a sole gate for the affected task, require independent/tool-grounded verification until fixed.
2. **Self-Independent Verifier Gap Widening** (P2 - Warning): Condition - self-verifier flag rate falls more than 25 points below independent verifier's flag rate on matched samples. Action: Investigate shared blind spots, prioritize independent verifier as primary gate.
3. **Cross-Verifier Disagreement Spike** (P2 - Warning): Condition - disagreement rate between self and independent verifiers exceeds 15%. Action: Route disagreement cases to human review, add to known-error bank.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| known_error_pass_through_rate_pct | > 10% |
| self_vs_independent_verifier_flag_gap_pct | > 25 point gap |
| cross_verifier_disagreement_rate_pct | > 15% of cases disagree |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Known-Error Pass-Through Detected | Known-error injection test shows self-verifier pass-through rate above 10% | High |
| Self-Independent Verifier Gap Widening | Self-verifier flag rate falls more than 25 points below independent verifier's flag rate on matched samples | Medium |
| Cross-Verifier Disagreement Spike | Disagreement rate between self and independent verifiers exceeds 15% | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
