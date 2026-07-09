# No Regression Testing

## Issue: Fixing one case breaks another.

**Frequency**: Common

**Symptoms**
- Old failure recurs after prompt/model/tool change.
- [Add more specific symptoms]

**Root Cause**
Fixing one case breaks another.

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
1. **Failure-Pattern-to-Regression-Case Pipeline**: Every confirmed production failure or bug fix automatically generates a permanent regression test case capturing the exact failing input and expected corrected output, added to a suite that runs on every subsequent change.
2. **Mandatory Regression Gate Before Merge**: No prompt, model, or tool-schema change may merge unless the full regression suite passes at 100%; a regression failure is treated as a build-breaking error, not a warning.
3. **Change-Impact Analysis Before Prompt Edits**: Before modifying a shared prompt/instruction, run an automated diff-impact scan against the regression suite's case tags to identify which historical failure patterns are most likely to be affected, focusing reviewer attention.

### Detection & Response
1. **Regression Suite Pass Rate Monitoring per Release**: Track regression suite pass rate on every candidate release; any regression (a previously-passing case now failing) blocks promotion to production regardless of overall eval score improvement.
2. **Recurrence Tracking for Closed Failure Patterns**: Tag each regression case with its original failure pattern ID; monitor production for recurrence of that exact pattern even after the regression test passes, since real-world recurrence can reveal gaps in how the test captured the original bug.
3. **Root-Cause Tagging for Regression Failures**: When a regression case fails, classify whether the failure stems from a shared-prompt change, model version change, or tool/schema change, to route the fix to the right owner quickly and spot systemic causes.

### Architecture Patterns
1. **Regression Suite as CI Gate**: An automated pipeline stage runs the full regression suite (one case per historically confirmed failure pattern) on every PR touching prompts, model version, or tool integrations, blocking merge on any failure.
2. **Failure Pattern Registry**: A structured store links each regression test case to its originating incident, root cause, fix description, and affected components, enabling impact analysis and pattern-level reporting rather than a flat list of tests.
3. **Bisection Tooling for Regression Root-Causing**: Tooling automatically bisects across recent prompt/model/tool changes to identify which specific change reintroduced a regression, cutting triage time on multi-change releases.

### Metrics
1. **regression_suite_pass_rate_pct**: Target: 100%; Alert threshold: < 100% (any regression blocks release)
2. **new_regression_cases_added_per_incident**: Target: 1 per confirmed production failure; Alert threshold: 0 (incident closed without regression case)
3. **failure_pattern_recurrence_rate_pct**: Target: < 1% of closed patterns recur in production; Alert threshold: > 5%
4. **regression_suite_runtime_minutes**: Target: < 15 minutes (fast enough to run on every PR); Alert threshold: > 45 minutes

### Alerts
1. **Regression Detected Pre-Merge** (P1 - Critical): Condition - any previously-passing regression case fails on a candidate change. Action: Block merge, require fix or explicit documented justification with reviewer sign-off before override.
2. **Incident Closed Without Regression Case** (P2 - Warning): Condition - a confirmed production failure is marked resolved without a corresponding new regression test. Action: Reopen incident, require regression case addition before closure.
3. **Regression Suite Runtime Bloat** (P3 - Info): Condition - suite runtime exceeds 45 minutes, risking bypass under release pressure. Action: Parallelize or prune suite, prioritize highest-value cases for the fast-path gate.

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

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
