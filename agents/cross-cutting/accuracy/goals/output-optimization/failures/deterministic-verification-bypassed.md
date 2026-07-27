# Deterministic Verification Bypassed

## Issue: Agent relies solely on an LLM-judge to assess its own output when a deterministic, executable check (schema validation, test suite, linter, tool-call format check) was available and would have caught the error at near-zero cost.

**Frequency**: Common

**Symptoms**
- Output errors that a schema validator, linter, or test suite would catch deterministically instead surface only through LLM-judge review, if at all
- Malformed JSON, missing required fields, or wrong enum values reach downstream consumers even though the agent has a JSON-schema validator or parser available in its toolchain
- Generated code is graded "looks correct" by an LLM-judge pass while the project's own test suite (which the agent could have invoked) would have failed on the same change
- LLM-judge approval rate stays flat or high even during periods when a deterministic check on the same outputs (rerun offline) shows a rising failure rate, revealing the judge is not catching what the checker catches
- Tool-call arguments that violate the tool's own declared parameter schema (wrong type, out-of-range value, missing required argument) are only caught after execution fails, not before, despite a schema check being cheap to run pre-call

**Root Cause**
Agent relies solely on an LLM-judge to assess its own output when a deterministic, executable check (schema validation, test suite, linter, tool-call format check) was available and would have caught the error at near-zero cost.

**Example**
```
A coding assistant agent for an internal developer-tools platform generates a patch to fix a
failing API endpoint. The repository has a full pytest suite and a CI lint step, both
invokable by the agent via its shell tool. Instead of running either, the agent's pipeline
asks a second LLM call to review the diff and rate it "correct" or "needs revision." The
judge rates the patch correct because it "looks like it addresses the described bug" and
follows the surrounding code's style. The patch is merged automatically since it passed the
judge gate. The change actually breaks a fixture used by three other endpoints, something
`pytest` would have flagged in under 10 seconds. The regression ships to staging and is only
caught two days later when an unrelated team's integration tests start failing, costing an
afternoon of cross-team debugging to trace back to the "judge-approved" patch.
```

**Contributing Factors**
- No inventory of which output types have an available deterministic check versus which genuinely require subjective LLM-judge assessment
- Deterministic checks (test suite, linter, schema validator) exist in the repository or environment but are not wired into the agent's tool list or pipeline, so the agent has no way to invoke them even if it wanted to
- Latency or cost budget for the pipeline is tuned assuming a single LLM-judge call, and adding a deterministic check is deprioritized as "extra steps" rather than recognized as a near-zero-cost, higher-precision replacement
- Team trusts LLM-judge scores because they correlate with human review on a small sample, without separately testing whether they correlate with what the deterministic check would have caught

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Schema-violating output with judge approval | An output crafted to violate the declared JSON schema (missing required field) but that reads as fluent and plausible | Deterministic schema validator rejects it before/regardless of judge review | LLM-judge marks it "correct" and no schema check runs, so the malformed output reaches the consumer |
| Failing-test patch | A code patch that breaks an existing unit test but matches the surrounding style and stated intent | Test suite run blocks merge/acceptance | Patch is approved on judge review alone without the test suite being invoked |
| Tool-call argument bounds check | A tool call with an out-of-range or wrong-typed argument per the tool's own schema | Pre-execution schema check rejects the call before it reaches the tool | Call executes (or is judged fine) without any pre-call schema validation step |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Deterministic-check coverage | >=95% of outputs with an available deterministic check actually run through it | Audit pipeline configs against an inventory of available checkers (schema, linter, test suite) per output type |
| Judge/checker disagreement rate | <5% of outputs where LLM-judge approves but the deterministic check (run in shadow mode) fails | Run both judge and deterministic check on the same sample and compare pass/fail |
| Post-release defect rate attributable to skipped checks | Trending to 0 | Root-cause tag production incidents; count those where an available deterministic check was not invoked |

---

## Mitigation Strategies

### Prevention
1. **Deterministic-check inventory**: Before wiring up any LLM-judge gate, catalog which output types already have a schema validator, linter, compiler, or test suite available, and require those to run first; reserve the judge for genuinely subjective dimensions (tone, helpfulness) it can't replace.
2. **Verify-then-judge pipeline ordering**: Structure the pipeline so deterministic checks run first and short-circuit on failure; only pass outputs that clear deterministic checks to the LLM-judge, so the judge is never the sole gate on anything a cheap check could catch.
3. **Tool-call schema pre-validation**: Validate tool-call arguments against the tool's declared JSON schema before execution, rejecting or auto-repairing malformed calls instead of relying on a judge's post-hoc read of whether the call "looks right."

### Detection & Response
1. **Shadow-mode checker comparison**: Run the deterministic check in parallel (shadow mode) even where only the judge currently gates the pipeline, and alert when the two disagree, surfacing exactly the cases the judge is missing.
2. **Escaped-defect root-causing**: For every production defect that reaches users, tag whether a deterministic check existed and was skipped; feed this back into the check inventory to close the specific gap.

### Architecture Patterns
1. **Verify-before-judge gate**: A hard, non-bypassable deterministic check stage precedes any LLM-judge stage in the pipeline for output types where a checker exists.
2. **Checker registry**: A central, versioned registry mapping output type to its available deterministic checker(s), consulted by every pipeline that produces that output type so new pipelines can't silently omit an existing check.
3. **Fail-closed on missing checker metadata**: If the registry has no entry (checker existence unknown) for an output type, treat it as "deterministic check not yet evaluated" and route to a stricter review tier rather than defaulting to judge-only.

### Metrics
1. **deterministic_check_coverage_pct**: Target: >=95%; Alert threshold: <85%
2. **judge_checker_disagreement_rate**: Target: <5%; Alert threshold: >15%
3. **escaped_defects_with_available_checker**: Target: 0/month; Alert threshold: >=2/month

### Alerts
1. **Judge-Only Gate on Checkable Output** (P2 - Warning): Condition - an output type with a registered deterministic checker is observed passing through a pipeline stage with no checker invocation logged. Action: block auto-release for that output type and page the owning team to wire in the checker.
2. **Judge/Checker Disagreement Spike** (P2 - Warning): Condition - shadow-mode disagreement rate exceeds 15% over a rolling 24-hour window. Action: investigate whether the judge prompt has drifted or the checker itself needs updating.
3. **Escaped Defect With Available Checker** (P1 - Critical): Condition - a production incident is root-caused to an error type that a deployed, available deterministic checker would have caught. Action: immediately require the checker in the release path for that output type and file a postmortem.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| Deterministic-check coverage across registered output types | <85% |
| Judge/checker disagreement rate (shadow mode) | >15% over 24h |
| Escaped defects traced to a skipped available checker | >=2 per month |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Checker bypass detected | Output type has a registered checker but no invocation logged for a release | High |
| Disagreement spike | Judge approves >15% of items the shadow checker rejects, rolling 24h | Medium |
| Checkable defect escaped to production | Incident root-caused to a skipped deterministic check | High |

---

## Related Patterns

- [Wrong Verifier](../../verification/failures/wrong-verifier.md) - the broader case of using checks too weak for the task's risk level; this pattern is the specific case where a deterministic check existed and was skipped in favor of LLM-judge-only assessment
- [Verifier Hallucination](../../verification/failures/verifier-hallucination.md) - a related failure where the LLM-judge itself hallucinates its assessment

## References

- [GroundEval: A Deterministic Replacement for LLM-as-Judge in Stateful Agent Evaluation](https://arxiv.org/html/2606.22737v2) - deterministic evaluation as a replacement for LLM-as-judge in stateful agent settings
- [LLM Agent Evaluation Metrics in 2026](https://www.confident-ai.com/blog/llm-agent-evaluation-complete-guide) - deterministic checks (schema validation, tool-call format, output length bounds, JSON parsing) run on 100% of outputs and catch the most common errors at essentially zero cost; Tool Correctness is named as a deterministic, non-LLM-judge metric
- [Why Your Agent Evaluation Stack is About to Get Weirder (and Better)](https://medium.com/@Micheal-Lanham/why-your-agent-evaluation-stack-is-about-to-get-weirder-and-better-dc9f8cfb9b07) - LLM-as-judge as a scalable weak supervisor, not dependable ground truth by default
