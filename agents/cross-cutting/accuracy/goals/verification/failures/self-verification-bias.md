# Self-Verification Bias

## Issue: Same model judges its own flawed output.

**Frequency**: Occasional

**Symptoms**
- Self-critique passes known wrong answer.
- [Add more specific symptoms]

**Root Cause**
Same model judges its own flawed output.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
