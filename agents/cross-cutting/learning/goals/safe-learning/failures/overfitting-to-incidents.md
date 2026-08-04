# Overfitting To Incidents

## Issue: Fix addresses one case but damages general behavior.

**Frequency**: Common

**Symptoms**
- Regression suite fails after local fix.
- A prompt/policy patch written to stop one specific reported incident from recurring introduces an overly broad instruction (e.g., "never mention competitor products") that suppresses correct, desired behavior in unrelated, more common scenarios.
- Each individual post-incident fix looks harmless in isolation, but holdout benchmark performance quietly erodes over many such fixes, since no single change trips a regression alert on its own.

**Root Cause**
Fix addresses one case but damages general behavior.

**Example**
```
After one customer complains that the agent recommended a third-party plugin instead of the
company's own paid add-on, an engineer adds a system-prompt rule: "Never recommend any third-party
tool or plugin under any circumstances." The specific complaint is resolved. Two weeks later, the
regression suite -- run only after a routine audit, not gated on this change -- reveals the agent now
refuses to mention well-established, genuinely helpful third-party integrations in dozens of unrelated
support conversations where a third-party recommendation was the correct answer, measurably lowering
resolution quality across the board.
```

**Contributing Factors**
- Incident response pressure favors the fastest fix that stops the specific complaint, not the narrowest one that avoids collateral damage.
- No holdout/generalization benchmark is run before merge, so a fix is validated only against the triggering case, never against unrelated behavior.
- Fixes are expressed as broad, global instructions (blanket prohibitions) rather than scoped to the specific condition that caused the incident.
- Small per-fix generalization losses accumulate silently across many incidents because no one tracks the cumulative holdout-score trend over time.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Two-tier fix validation | Candidate fix for a single reported incident, run against both the repro case and the full holdout suite | Repro case passes and holdout suite shows no new failures | Repro case passes but holdout suite shows newly broken, unrelated behaviors |
| Blast-radius scoping check | Fix expressed as a broad global rule (e.g., "never mention X") versus a narrowly scoped condition | Reviewer/tooling flags the broad rule and requires scoping to the specific triggering condition | Broad rule merges unchanged, suppressing correct behavior in unrelated cases |
| Cumulative generalization drift | Sequence of 10 small incident-driven fixes applied over time, each individually passing regression | Holdout generalization score is tracked cumulatively and any downward trend is flagged | Score drifts down across the sequence with no fix individually triggering an alert |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| holdout_generalization_score_delta (eval) | >= 0 per fix | Run the holdout benchmark before and after each candidate fix and compare scores |
| regression_suite_pass_rate_percent (eval) | 100% before merge | Run the full regression suite against each candidate fix, not just the triggering repro case |
| cumulative_generalization_drift_over_n_fixes | near 0 over a rolling window (e.g., 20 fixes) | Track holdout score trend across a sequence of incident-driven fixes rather than per-fix only |

---

## Mitigation Strategies

### Prevention
1. **Holdout Incident Set / Generalization Check**: Maintain a held-out set of unrelated incidents and behaviors that is never used to derive any fix; every candidate fix must be validated against this set (not just the triggering case) before merge, catching narrow patches that damage unrelated behavior.
2. **Minimal-Diff Fix Principle with Blast-Radius Review**: Require fixes to use the narrowest change that resolves the triggering case (e.g., scoped prompt edit rather than global instruction, targeted regex rather than broad pattern), and require reviewers to explicitly enumerate what else the change could plausibly affect before approval.
3. **Regression Suite Gate Before Merge**: Block merge unless the full regression suite passes, not just a manual check of the originally reported case, so collateral damage to other behaviors is caught mechanically rather than relying on reviewer memory of edge cases.

### Detection & Response
1. **Regression Suite Delta Monitoring**: Automatically diff full regression suite pass rate before and after each incident-driven fix; any newly failing test that wasn't failing before is treated as an overfit signal, not noise.
2. **Generalization Score Tracking**: Measure performance on the holdout/unrelated task categories before and after each fix and track the delta over time; a pattern of small holdout losses accumulating across many "small" fixes indicates systemic overfitting even when no single fix trips an alert.
3. **Fix Rollback on Generalization Loss**: If a shipped fix causes measurable holdout or regression suite degradation, automatically revert to the pre-fix version and require the fix to be re-derived with a broader test basis before re-attempting.

### Architecture Patterns
1. **Two-Tier Test Harness**: CI runs both an incident-specific repro test (proves the triggering case is fixed) and the full regression/holdout suite (proves nothing else broke) for every candidate fix, with both required to pass.
2. **Generalization Benchmark Set**: A curated, versioned suite of diverse tasks deliberately kept independent from incident-derived tests, periodically refreshed so it doesn't itself become a target that fixes are overfit to.
3. **Fix Impact Diff Report**: An auto-generated report attached to each change record showing behavior deltas across benchmark categories, making collateral impact visible to reviewers at approval time rather than discovered later in production.

### Metrics
1. **regression_suite_pass_rate_percent**: Target: 100% before merge; Alert threshold: any new failure introduced by the fix
2. **holdout_generalization_score_delta**: Target: >= 0 (no degradation) post-fix; Alert threshold: negative delta exceeding tolerance
3. **incident_fix_collateral_regression_count**: Target: 0 per fix; Alert threshold: >= 1
4. **fixes_rolled_back_for_overfit_percent**: Target: < 5% of all incident fixes; Alert threshold: > 15% (indicates systemic narrow-fix habit)

### Alerts
1. **Regression Introduced by Incident Fix** (P1 - Critical): Condition - full regression suite shows a new failure after an incident-driven fix. Action: Block deployment or auto-revert if already live, require fix to be re-derived using the two-tier harness.
2. **Holdout Generalization Loss** (P2 - Warning): Condition - holdout benchmark score drops beyond tolerance after a fix. Action: Flag fix for review, require broader test basis, consider reverting pending investigation.
3. **Repeated Narrow-Fix Pattern** (P3 - Info): Condition - fixes-rolled-back-for-overfit rate exceeds 15% over a rolling period. Action: Review fix authorship practices with the team, reinforce minimal-diff and blast-radius review habits.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| incident_fix_collateral_regression_count | >= 1 |
| holdout_generalization_score_delta | negative delta exceeding tolerance |
| fixes_rolled_back_for_overfit_percent | > 15% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Regression Introduced by Incident Fix | full regression suite shows a new failure after an incident-driven fix | High |
| Holdout Generalization Loss | holdout benchmark score drops beyond tolerance after a fix | Medium |
| Repeated Narrow-Fix Pattern | fixes-rolled-back-for-overfit rate exceeds 15% over a rolling period | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
