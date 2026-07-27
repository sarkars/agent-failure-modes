# Missing Agent Eval Framework

## Issue: Team builds a custom eval harness (a handful of manually-written test prompts checked by eyeballing the output) instead of adopting an established agent/RAG evaluation framework, missing standardized metrics and automatic test-case generation.

**Frequency**: Occasional

**Symptoms**
- "Evaluation" consists of a small, manually maintained prompt list with human eyeballing, rather than standardized metrics computed against a growing test set
- The same 10-20 test prompts have been reused for months without expansion, so they no longer represent the current range of real user queries or edge cases
- There is no automatic test-case generation from production traffic or documents, so coverage of new features or new failure modes lags behind what's actually shipping
- Pass/fail judgments are subjective and inconsistent between reviewers, with no standardized rubric or scoring model to make results comparable across runs
- Regression detection depends on someone remembering to manually re-run the prompt list after a change, so silent regressions ship whenever that step is skipped under time pressure

**Root Cause**
Team builds a custom eval harness instead of adopting an established agent/RAG evaluation framework, missing standardized metrics and automatic test-case generation.

**Example**
```
A small team building an internal expense-report-review agent writes 12 sample
expense reports and manually checks whether the agent's approve/flag decision
"looks right" each time before merging a prompt change. This checklist has not
grown since the project's first month, and one engineer typically eyeballs
the outputs alone before approving a pull request.

When the team switches the underlying model version to cut costs, all 12 sample
cases still pass by eye. Two weeks after rollout, finance flags that the agent
has started approving expense reports with mismatched receipt totals - a class
of error none of the 12 hand-written test cases happened to cover, and one a
human reviewer would have caught only by chance in casual eyeballing. Because
there was no standardized metric suite or automatically generated adversarial
test set, the regression shipped silently and was only caught because finance
noticed the pattern in monthly reconciliation, weeks after go-live - not
because any part of the eval process flagged it.
```

**Contributing Factors**
- No evaluation of established eval frameworks (standardized metrics, automatic test-set generation, regression tracking) was done before building an ad hoc, manually-maintained test list
- Early in the project, a handful of manual test prompts felt "good enough" for a small feature, and the team never revisited that decision as the agent's scope and usage grew
- Building an eval harness is seen as pure overhead with no visible feature output, so it consistently loses priority against shipping new capabilities
- No one owns eval quality as a distinct responsibility, so the manual test list is maintained inconsistently by whichever engineer happens to touch the prompt last
- The team lacks familiarity with standardized eval frameworks (DeepEval, RAGAS) and underestimates how quickly a hand-maintained list falls behind real-world query diversity

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Auto-generated edge case coverage | Test cases synthesized from production traffic/documents via an eval framework's generation tooling | New edge cases (e.g. mismatched totals, ambiguous inputs) are surfaced and scored automatically | Edge case is only found via a manual, unstructured spot check |
| Model/prompt version regression | Full standardized test suite run before and after a model or prompt change | Score deltas per metric are reported automatically, with a clear pass/fail gate | Regression ships because only the original small manual list was re-run |
| Rubric consistency across reviewers | Same agent output scored independently by the standardized framework's scoring model vs. two different human reviewers | Framework score falls within an acceptable range of reviewer consensus | Human reviewers disagree with each other and with no way to reconcile which is "correct" |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Automated test-suite pass rate | >= 90% on standardized metric suite | Run the eval framework's full generated + curated test suite on every prompt/model change |
| Test-case corpus growth rate | Net growth each release cycle, no long-term plateau | Track count of distinct test cases (manual + auto-generated) over time |
| Regression detection coverage | 100% of shipped prompt/model changes gated by automated eval run | Audit CI/deploy logs for changes that bypassed the eval gate |

---

## Mitigation Strategies

### Prevention
1. **Adopt DeepEval or RAGAS for standardized metrics**: Replace ad hoc eyeballing with objective, repeatable metrics (correctness, faithfulness, relevancy, task completion) computed automatically on every run.
2. **Use the eval framework's automatic test-case generation**: Generate adversarial and edge-case test cases from production traffic/documents instead of relying solely on a small, manually authored prompt list.
3. **Run a build-vs-buy evaluation before extending the manual list**: Before hand-writing another test prompt, check whether an established framework's generation tooling already covers that scenario class.

### Detection & Response
1. **Automated regression gate in CI**: Block merges/deploys when the standardized test suite's pass rate or key metric drops below a defined threshold versus the last known-good baseline.
2. **Production-traffic sampling feedback loop**: Periodically pull real production queries (with any needed PII scrubbing) into the eval corpus, so coverage tracks actual usage rather than stagnating.
3. **Cross-check flagged production incidents**: Any user- or business-reported bad output is converted into a new permanent eval test case, not just patched ad hoc in the prompt.

### Architecture Patterns
1. **Eval-in-CI gating**: Wire the eval framework into the deployment pipeline so every prompt/model change is scored automatically before reaching production, mirroring standard unit-test gating.
2. **Layered eval suite**: Combine a small curated "golden set" of hand-picked critical cases with a much larger auto-generated/production-sampled set, rather than relying on either alone.
3. **Standardized scoring model**: Use the framework's LLM-as-judge or rubric-based scorer consistently across releases so historical scores remain comparable over time.

### Metrics
1. **automated_test_pass_rate**: Target: >= 90%; Alert threshold: < 80%
2. **eval_corpus_size_growth**: Target: net positive per release; Alert threshold: flat or shrinking for 2+ releases
3. **unguarded_deploys_pct**: Target: 0%; Alert threshold: > 5% of deploys bypass the eval gate

### Alerts
1. **Regression Gate Bypassed** (P2 - Warning): Condition - a prompt/model change is deployed without passing through the automated eval gate. Action: notify release owner, require retroactive eval run.
2. **Standardized Metric Score Drop** (P2 - Warning): Condition - a key metric (correctness/faithfulness/task completion) drops more than a defined margin versus baseline. Action: block release, notify prompt/model owner.
3. **Eval Corpus Stagnation** (P3 - Info): Condition - no new test cases added to the corpus for multiple release cycles despite feature changes. Action: notify team to run test-case generation against recent production traffic.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| automated_test_pass_rate | < 80% |
| eval_corpus_size_growth | Flat/shrinking for 2+ releases |
| unguarded_deploys_pct | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Deploy bypassed eval gate | A prompt/model change reaches production without an automated eval run | Medium |
| Standardized metric regression | Key eval metric drops significantly versus baseline after a change | Medium |
| Eval corpus stagnation | No new test cases added despite recent feature/prompt changes | Low |

---

## Related Patterns

- [No Regression Testing](../../../../accuracy/goals/verification/failures/no-regression-testing.md) - a related downstream symptom this pattern's missing standardized framework would help systematize
- [Happy Path Only Evals](../../../../accuracy/goals/verification/failures/happy-path-only-evals.md) - a related downstream symptom; established eval frameworks' automatic test-case generation is exactly the kind of coverage a hand-maintained list tends to miss

## References

- [The Best RAG Frameworks in 2026](https://martinuke0.github.io/posts/2026-01-06-the-best-rag-frameworks-in-2026-a-comprehensive-guide-to-building-superior-retrieval-augmented-generation-systems/) - RAGAS for comprehensive evaluation with objective context precision/recall/faithfulness/relevancy metrics and automatic test-dataset generation
- [10 LLM Observability Tools to Evaluate & Monitor AI in 2026](https://www.confident-ai.com/knowledge-base/compare/10-llm-observability-tools-to-evaluate-and-monitor-ai-2026) - survey including DeepEval-class evaluation frameworks with standardized metric suites
