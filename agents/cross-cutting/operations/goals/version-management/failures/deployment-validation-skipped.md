# Deployment Validation Skipped

## Issue
A required pre-production gate — a regression eval suite against known agent conversation transcripts, a tool-schema compatibility check, a canary soak period — is bypassed for a given release, either through an explicit manual override ("hotfix, skip the eval run, we need this live now") or because a pipeline misconfiguration silently short-circuits the gate. The release ships straight to production without the validation that was specifically designed to catch the class of regression it turns out to contain, and the failure surfaces in front of real users instead of in the gate that existed to prevent exactly that.

**Frequency**: Common

**Symptoms**
- Deployment pipeline logs show a validation stage marked "skipped" or "bypassed" rather than "passed"
- Post-incident review reveals the regression that shipped is exactly the class of issue the skipped gate was designed to catch
- Manual override flags (e.g., `--skip-eval`, `--force-deploy`) appear in deploy command history for releases later linked to incidents
- The skipped gate's pass/fail history shows it had caught similar issues in prior releases before being bypassed
- "Emergency" or "hotfix" labeled releases are disproportionately represented among incidents traced to validation gaps

## Root Cause
Validation gates that are slow, flaky, or perceived as low-value relative to their time cost accumulate pressure to be bypassed, especially under incident-response urgency where the instinct to "ship the fix now" overrides the instinct to "verify the fix first." Because most releases that skip validation don't cause a visible problem (the specific regression the gate would have caught doesn't happen to be present that time), skipping becomes normalized through repeated apparent success, and the override mechanism — usually a simple flag or a manual pipeline approval click — carries no proportional friction or record-keeping to counterbalance the urgency bias. The gate exists specifically to catch low-probability, high-impact regressions, so the absence of visible harm on any given skip is not evidence the practice is safe; it just means the low-probability event hasn't happened yet on a skipped run.

## Example
```
"ChatOrchestrator" has a pre-deploy eval gate: run the new build
against a fixed suite of 500 recorded conversation transcripts,
require >= 98% of tool-call selections to match expected/acceptable
outcomes before promoting to production. The suite normally takes
14 minutes.

An incident is declared: a customer-reported prompt-injection bypass
lets users extract system-prompt contents. A fix is written, tested
manually against the specific injection string, and is ready to ship
19 minutes into the incident.

On-call runs `deploy --env=prod --skip-eval-gate`, reasoning "we
already manually verified the fix, and 14 minutes matters during an
active security incident." The override is logged but requires no
second approval.

The eval suite, had it run, would have caught that the fix's new
system-prompt-sanitization step also silently strips a required
formatting instruction from 6% of legitimate tool-call responses -
a regression unrelated to the injection fix but introduced by the
same diff, only detectable by the broad-coverage suite rather than
the manual single-case check.

Six hours later, malformed tool-call outputs from the sanitization
regression start generating a separate incident, only diagnosed once
someone notices it's isolated to builds after the injection fix, and
finally runs the skipped eval suite against it retroactively.
```

## Statistics
| Finding | Context |
|---------|---------|
| A disproportionate share of production incidents traced to a specific regression class are found to have shipped via a bypassed rather than a passed validation gate | Typical pattern reported across teams that track skip-flag usage against incident root cause |
| Emergency/hotfix releases are commonly overrepresented among validation-gate bypass events relative to their share of total releases | Estimated from deploy-history analysis in teams with override logging |
| Requiring a second approver for any gate bypass measurably reduces bypass frequency without materially slowing genuine emergencies | Reported range across teams that added a two-person bypass rule |

## Mitigations
1. **Two-person bypass rule**: Require any validation-gate skip to be explicitly approved by a second engineer (not just the person under incident pressure), logged with a stated reason, so the decision gets a moment of independent scrutiny even during urgency.
2. **Fast-path validation instead of full skip**: Maintain a reduced, high-signal subset of the validation suite (e.g., the 50 highest-risk transcripts instead of all 500) that runs in under a minute, so urgent releases have a real alternative to a full skip rather than an all-or-nothing choice.
3. **Mandatory retroactive validation**: When a gate is bypassed, automatically queue the skipped validation to run against the shipped build immediately after deploy, and alert if it would have failed, even though the release already went out.
4. **Skip-rate tracking as a first-class metric**: Track and regularly review the rate at which each validation gate is bypassed across releases, treating a rising skip rate as a signal that the gate itself may be too slow or too noisy and needs fixing rather than continued circumvention.
5. **Gate-specific incident tagging**: When an incident's root cause matches a category a specific validation gate is designed to catch, explicitly record whether that gate ran, passed, or was skipped for the offending release, to build a track record justifying the gate's continued enforcement.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| validation_gate_skip_rate | Share of releases that bypass a given required validation gate | Alert if > 5% over a rolling 30-day window |
| retroactive_validation_failure_rate | Share of skipped validations that, when run retroactively, would have failed | Alert on any occurrence |
| incidents_from_skipped_gate | Count of production incidents whose root cause matches a category a skipped gate was designed to catch | Alert on any occurrence |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Validation gate bypassed | A deploy proceeds with a required gate marked skipped | Medium | Log reason, require second approver sign-off, queue retroactive validation |
| Retroactive validation failure | A skipped gate, run after the fact, would have failed | High | Treat as an active incident, assess whether the shipped build needs immediate rollback or a follow-up fix |

## Related Patterns
- [Rollback Partial Failure](./rollback-partial-failure.md) - a skipped validation gate often leads directly to needing a rollback, which can itself fail partway
- [Deployment Ordering Violation](./deployment-ordering-violation.md) - a missing precondition check is a specific instance of a skipped validation
- [Canary Deployment Incomplete](./canary-deployment-incomplete.md) - a canary soak period is itself a form of validation gate that can be skipped or cut short under the same pressure
