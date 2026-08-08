# No Regression Testing

## Issue: Fixing one case breaks another.

**Frequency**: Common

**Symptoms**
- Old failure recurs after prompt/model/tool change.
- A prompt edit made to fix one reported bug causes a previously-fixed, unrelated failure pattern to resurface, and it isn't caught until a customer reports it again.
- Engineers have no fast way to tell which of several recent prompt/model/tool changes reintroduced a known bug, so triage on multi-change releases takes days.

**Root Cause**
Regressions recur because confirmed bug fixes are typically closed out once the immediate report is resolved, without a permanent regression test being added to lock in the fix, and prompt, model, or tool changes are free to merge without running -- let alone passing -- any regression suite that would have caught a reintroduction. Shared prompt sections get edited without any impact analysis showing which historical failure patterns depend on that instruction block, so an unrelated tone or wording fix can silently unravel a previously-fixed behavior, and because no tooling exists to bisect across recent changes, even after a regression resurfaces, tracing it back to the responsible edit is slow and manual.

**Example**
```
Three months ago, a scheduling agent was fixed after it double-booked a room when a
user rescheduled mid-conversation. No regression test was added for that fix -- the team
moved on once the immediate bug report was closed. This week, a prompt change intended to
improve tone for a different complaint reworks the same instruction block that governed
reschedule handling. The double-booking bug reappears in production, identical to the
one fixed three months earlier, because nothing in the test suite would have caught the
shared prompt section regressing.
```

**Contributing Factors**
- Confirmed production bug fixes are closed out without a corresponding permanent regression test capturing the exact failing case.
- Prompt/model/tool changes can merge without running (or passing) a regression suite, so there's no automated gate preventing reintroduction.
- Shared prompt sections or instruction blocks are edited without an impact analysis showing which historical failure patterns depend on that section.
- No tooling exists to bisect across recent changes, so when a regression does surface, root-causing which change caused it is slow and manual.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Reschedule double-booking replay | Mid-conversation reschedule request matching the original confirmed-bug scenario | Agent avoids double-booking, exactly as fixed previously | The historical bug's exact failure mode reproduces |
| Shared-prompt-section impact scan | Diff of a prompt edit touching an instruction block linked to 3 historical failure patterns | All 3 linked regression cases still pass after the edit | Any linked regression case starts failing after the edit |
| Full regression suite gate | Candidate release with all prompt/model/tool changes applied | 100% of regression suite cases still pass | Any previously-passing regression case now fails |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| regression_suite_pass_rate_pct | 100% | Run full regression suite (one case per historically confirmed failure) on every candidate release |
| new_regression_cases_added_per_incident | 1 per confirmed production failure | Audit closed incidents for a linked regression test case before closure |
| failure_pattern_recurrence_rate_pct | < 1% of closed patterns recur in production | Tag regression cases with failure pattern ID, monitor production for recurrence of that pattern |

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
| regression_suite_pass_rate_pct | < 100% (any regression blocks release) |
| new_regression_cases_added_per_incident | 0 (incident closed without regression case) |
| failure_pattern_recurrence_rate_pct | > 5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Regression Detected Pre-Merge | Any previously-passing regression case fails on a candidate change | High |
| Incident Closed Without Regression Case | A confirmed production failure is marked resolved without a corresponding new regression test | Medium |
| Regression Suite Runtime Bloat | Suite runtime exceeds 45 minutes, risking bypass under release pressure | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
