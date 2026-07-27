# What Are the Most Common Verification Failures in AI Agents?

**Agents skip or perform inadequate verification of their own outputs, leaving errors undetected — verification is absent (no check at all), shallow (checking only format not correctness), or biased (agent verifies its own work and finds no errors, even when a second opinion would catch them).** These failures are architectural: the problem isn't model capability, it's the absence of verification in the deployment pipeline or verification logic that lacks sufficient independence and depth.

## Key Takeaways

- 15 distinct failure patterns affect verification, grouped into four mechanisms: missing verification (no check at all), shallow verification (format checks only), biased verification (agent checks its own work), and methodology gaps (testing only happy paths, not adversarial cases, not long-horizon scenarios).
- Verification failures are particularly dangerous because they're the last line of defense — once verification is compromised, incorrect outputs ship to production with confidence. Worse, they're invisible: a system without verification looks fine until an external audit surfaces the gap.
- The reliable fix is architectural, not model-only: make verification mandatory for state-changing actions and high-stakes output; require verification by an independent agent or tool (not self-verification); use multiple verification methods (format, business logic, ground truth comparison, human review); verify the verifier itself against test cases.
- Verification failures concentrate in systems where verification is treated as optional or low-priority (nice-to-have rather than non-negotiable) and in systems where agents verify their own work.

## Scope

- **Missing verification** — [no-verification](failures/no-verification.md), [no-human-review-trigger](failures/no-human-review-trigger.md). No verification step at all, or no mechanism to route high-stakes output to human review.
- **Shallow verification** — [surface-level-validation](failures/surface-level-validation.md), [eval-data-mismatch](failures/eval-data-mismatch.md). Verification checks only format (schema validity, field presence) not correctness (value accuracy, business-rule compliance).
- **Biased verification** — [self-verification-bias](failures/self-verification-bias.md), [verifier-hallucination](failures/verifier-hallucination.md), [over-trusting-confidence-score](failures/over-trusting-confidence-score.md). Agent verifies its own work and finds no errors; verifier itself hallucinate; confidence scores treated as equivalent to correctness.
- **Methodology gaps** — [happy-path-only-evals](failures/happy-path-only-evals.md), [no-adversarial-testing](failures/no-adversarial-testing.md), [no-long-horizon-evaluation](failures/no-long-horizon-evaluation.md), [no-regression-testing](failures/no-regression-testing.md), [no-ground-truth-comparison](failures/no-ground-truth-comparison.md). Testing only common cases, not edge cases or adversarial inputs; not testing multi-step outcomes; not comparing against ground truth; no regression suite.
- **Misaligned verification** — [wrong-verifier](failures/wrong-verifier.md), [no-business-kpi-validation](failures/no-business-kpi-validation.md), [metric-gaming](failures/metric-gaming.md). Verifier doesn't match task requirements; business impact not validated, only technical metrics; agent optimizes for validation metric rather than business goal.

## When Verification Matters

- Agent's output feeds systems or decisions where errors have high consequences (financial, regulatory, safety, reputational impact)
- Agent performs state-changing actions (writes, sends, posts) where verification can confirm the action succeeded as intended
- Multiple verification approaches are possible (human review, independent tool verification, ground truth comparison) and combining them would catch errors that any single method misses
- Production performance diverges from evaluation performance — indicates evaluation methodology is inadequate and verification is needed to catch the gap

## Cross-Pattern Insight

Across all 15 patterns, the single most reliable mitigation is mandatory, multi-layered verification: (1) require every state-changing action to have a verification step before reporting success (not self-verification, but via independent tool or readback); (2) require high-stakes outputs to pass multiple verification methods (format + business logic + human review sample); (3) verify the verifier itself against test cases to catch verifier hallucination. Cases where verification is mandatory and multi-layered consistently catch errors that single-layer verification misses. The second universal mitigation is comprehensive test methodology — if testing covers only happy paths, failures in edge cases and long-horizon scenarios won't surface until production.

## Frequently Asked Questions

### How does verification differ from output accuracy?
Output accuracy covers generation of false outputs (hallucination, bias). Verification covers detection of false outputs. An agent can hallucinate, and verification is the safeguard that catches it. If accuracy is the generation problem, verification is the detection problem.

### How should confidence scores be used in verification?
Confidence scores don't correlate with accuracy — a model can be highly confident when wrong. Verification requires checking against external ground truth or business logic, not relying on internal confidence. A model confident on false output still produces false output.

### Can you fix verification failures by adding more test cases?
More test cases help, but if test methodology is flawed (happy path only, no adversarial cases, no ground truth comparison), more cases don't fix the problem — they just test the wrong thing. The fix is to diversify test methodology: happy paths + edge cases + adversarial inputs + long-horizon scenarios + ground truth comparison.

### Which verification failures matter most for production systems?
No-verification (no check at all) and self-verification-bias (agent checks its own work and finds no errors) are highest-priority because they're silent and allow errors to propagate. Happy-path-only-evals is next because it trains on wrong distribution and misses real-world failures.

## Patterns

| Pattern | Mechanism |
|---------|-----------|
| [Eval Data Mismatch](failures/eval-data-mismatch.md) | Evaluation data doesn't match production data; agent tested on one distribution, deployed on another |
| [Happy Path Only Evals](failures/happy-path-only-evals.md) | Testing covers only success cases; edge cases, error conditions, adversarial inputs untested |
| [Metric Gaming](failures/metric-gaming.md) | Agent optimizes for evaluation metric rather than business goal; high metric score masks misalignment with actual value |
| [No Adversarial Testing](failures/no-adversarial-testing.md) | Verification doesn't test malformed, tricky, or adversarial inputs; agent fails on edge cases |
| [No Business KPI Validation](failures/no-business-kpi-validation.md) | Verification checks technical metrics but not business impact; improvement in metrics doesn't translate to business value |
| [No Ground Truth Comparison](failures/no-ground-truth-comparison.md) | Output not compared against authoritative ground truth; verification passes but output is still wrong |
| [No Human Review Trigger](failures/no-human-review-trigger.md) | High-stakes output not routed to human review; no mechanism to flag uncertain or risky decisions |
| [No Long Horizon Evaluation](failures/no-long-horizon-evaluation.md) | Testing covers single steps; multi-step outcomes, compounding errors, long-term consequences untested |
| [No Regression Testing](failures/no-regression-testing.md) | No regression suite; previously-working functionality breaks silently on model or system updates |
| [No Verification](failures/no-verification.md) | No verification step at all; state-changing actions ship without checking that action succeeded |
| [Over-Trusting Confidence Score](failures/over-trusting-confidence-score.md) | Verification relies solely on model confidence; high confidence treated as equivalent to correctness |
| [Self Verification Bias](failures/self-verification-bias.md) | Agent verifies its own work and finds no errors; independent verification catches errors self-check missed |
| [Surface Level Validation](failures/surface-level-validation.md) | Verification checks format (schema, field presence) but not correctness (value accuracy, business logic) |
| [Verifier Hallucination](failures/verifier-hallucination.md) | Verification component itself hallucinates; reports correct output even when output is wrong |
| [Wrong Verifier](failures/wrong-verifier.md) | Verification checks irrelevant criteria; verifier doesn't match task requirements or business goal |

**Total: 15 patterns**

## Related Goals

- [Output Accuracy](../output-accuracy/) — hallucination and bias, which verification is designed to catch
- [Evaluation Reliability](../evaluation-reliability/) — golden-data quality and methodology, upstream of verification
- [Output Optimization](../output-optimization/) — confidence calibration and abstention, which complement verification
