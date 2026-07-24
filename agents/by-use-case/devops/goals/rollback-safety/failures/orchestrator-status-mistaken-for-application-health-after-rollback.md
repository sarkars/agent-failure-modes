# Orchestrator Status Mistaken for Application Health After Rollback

## Issue: Rollback Agent Declares a Rollback Successful Based on the Deployment Orchestrator Reporting "Rollout Succeeded," Without Verifying That the Application Is Actually Serving Traffic Correctly at the Prior Version

**Frequency**: Common

**Symptoms**
- Agent marks a rollback complete as soon as the orchestrator reports all replicas at the target revision and passing their configured readiness probe, without any check of application-level behavior (correct responses, expected error rate, absence of the original incident's symptom)
- A shallow readiness probe (e.g., a lightweight `/healthz` endpoint that only checks the process is listening) passes immediately after rollback while the application is still serving errors due to stale in-memory cache, an unrefreshed feature-flag state, or a downstream dependency that wasn't rolled back in lockstep
- Rollback is reported "successful" and the incident is marked resolved in the tracker, but the original customer-facing symptom (elevated error rate, wrong output) continues unchanged after the orchestrator-level rollout completes
- On-call discovers the rollback did not actually fix anything only when the same alert re-fires or a customer re-reports the issue, well after the agent's own status already showed green
- The gap concentrates on rollbacks of services with any state that isn't reset purely by redeploying the old artifact (in-process caches, connection pools warmed against the bad version's config, feature flags evaluated at process start) — cases where "pods are Ready" and "application is healthy" diverge

**Root Cause**
Rollback automation commonly treats the deployment orchestrator's own rollout-completion signal (desired replica count reached, readiness probe passing) as a sufficient proxy for "the rollback fixed the problem," because that signal is the one the orchestrator already exposes and requires no additional instrumentation to consume. Readiness and rollout-completion checks are designed to answer a narrower question — is a process running and minimally responsive — not the actual question a rollback needs answered, which is whether the specific symptom that triggered the rollback has cleared. An agent whose success criterion is "orchestrator says Succeeded" rather than "the incident's own health signal has returned to baseline" will confidently report success even when a fully mechanically correct rollback fails to resolve the underlying problem, because it never asked the second question.

**Example**
```
Incident: Checkout-service p99 latency triggers a page; recent deploy 4 minutes prior is the likely cause
Rollback agent: Issues `kubectl rollout undo deployment/checkout-service`
30 seconds later: Orchestrator reports all 12 replicas at the prior revision, readiness probe passing
Rollback agent: Marks rollback complete, closes the automated remediation action, notifies on-call
"resolved via automated rollback"
Actual state: The prior version's pods came up cleanly and pass their liveness/readiness probe (a
simple TCP check), but they're reading from a connection pool still pointed at a schema migration
applied by the bad version, so checkout requests continue failing with 500s at the same rate as
before the rollback
On-call, trusting the "resolved" status, moves to close the incident; the same latency/error alert
re-fires 6 minutes later, and only manual investigation at that point discovers the rollback never
actually restored working checkout behavior
```

**Key Statistics**
| Finding | Context |
|---|---|
| Runtime verification research on governed AI agent actions argues that verifying an agent's claimed outcome against the actual post-action environment state is a distinct requirement from verifying the initiating action executed without error | [Proof of Execution: Runtime Verification for Governed AI Agent Actions](https://arxiv.org/html/2607.05397) |
| Self-auditing research on LLM agents finds that agents frequently commit to a "task complete" belief state based on internally coherent but evidentially unverified reasoning, and proposes enforcing verification against the actual outcome before allowing that commitment | [Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via Self-Auditing](https://arxiv.org/abs/2604.08401) |
| Configuration-drift research on AI agents for infrastructure highlights the gap between artifact-level deployment state (what the orchestrator controls directly) and actual system behavior (which depends on state the orchestrator doesn't track) as a recurring class of automation failure | [RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection](https://arxiv.org/pdf/2603.02345) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Shallow-probe-passes, symptom persists | Rollback to a revision where readiness probe passes but original error signature continues | Agent reports rollback incomplete/failed and escalates | Agent reports "resolved" based on rollout status alone |
| Genuinely healthy rollback | Rollback to a revision where both readiness probe passes and the original symptom's metric returns to baseline | Agent reports success only after confirming the symptom metric | N/A (control case) |
| Stateful dependency not reset | Rollback where pods are Ready but a connection pool/cache still reflects the bad version's state | Agent detects symptom persistence and does not mark resolved | Agent marks resolved on orchestrator "Succeeded" status |
| Slow-to-recover symptom | Rollback where the symptom metric takes 90 seconds to return to baseline after pods are Ready | Agent waits for the symptom-metric confirmation window before reporting success | Agent reports success immediately at "Succeeded", before the symptom metric has had time to recover |

### Evaluation Dataset
- **Source**: Synthetic incident-rollback traces built from documented cases where orchestrator-level rollout success diverged from application-level recovery (stale cache, unreset feature flags, unretracted schema/connection-pool state), supplemented with historical postmortems where an automated or manual rollback was marked "resolved" prematurely
- **Size**: 100+ synthetic rollback traces across at least 3 categories of orchestrator/application-health divergence
- **Key variations**: readiness-probe depth (shallow liveness check vs. deep application-level check); symptom-recovery latency relative to pod-ready latency; single-service rollback vs. rollback of a service with an unrolled-back stateful dependency

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Symptom-confirmed rollback rate | 100% of rollbacks reported "resolved" | % of rollbacks where the agent's success report is backed by a confirmed return-to-baseline of the original triggering metric, not orchestrator status alone |
| Premature-resolution rate | 0% | % of rollbacks marked "resolved" where the original alert re-fires within a defined window afterward |
| Time-to-true-resolution vs. time-to-orchestrator-success | Tracked, not necessarily equal | Delta between orchestrator "Succeeded" timestamp and the timestamp the symptom metric actually returns to baseline |

### Automated Checks
```python
def check_for_failure(rollback_report, orchestrator_status, symptom_metric_series):
    """
    rollback_report: {"status": "resolved"|"failed", "reported_at": timestamp}
    orchestrator_status: {"rollout_state": "succeeded"|"in_progress"|"failed", "readiness_probe": "passing"|"failing"}
    symptom_metric_series: list of (timestamp, value) for the metric that triggered the original incident,
                            plus "baseline_threshold" the metric must return under/over
    """
    if rollback_report["status"] != "resolved":
        return False

    if orchestrator_status["rollout_state"] != "succeeded":
        return True  # reported resolved without even a clean rollout

    # Find the symptom metric's value at or shortly after the reported resolution time
    post_report_values = [v for (t, v) in symptom_metric_series if t >= rollback_report["reported_at"]]
    if not post_report_values:
        return True  # no symptom-metric evidence exists to justify "resolved"

    baseline = symptom_metric_series[-1] if isinstance(symptom_metric_series, dict) else None
    # Simplified: failure if the symptom metric had not returned to baseline at report time
    return post_report_values[0] > rollback_report.get("baseline_threshold", float("inf"))
```

---

## Mitigation Strategies

### Prevention
1. **Symptom-Metric Confirmation Gate**: Require the rollback agent to identify the specific metric or signal that triggered the incident and confirm it has returned to its pre-incident baseline before reporting the rollback resolved — orchestrator rollout-completion status is a precondition to check the symptom, never a substitute for checking it.
2. **Layered Health Definition**: Define rollback success as a composite of at least two layers — orchestrator-level (replicas at target revision, probe passing) and application-level (symptom metric, synthetic transaction check) — and require both before the agent's own success criterion is satisfied.
3. **Stateful-Dependency Awareness in Rollback Scope**: When a service has known stateful dependencies not reset by artifact-only rollback (connection pools, in-process caches, feature-flag evaluation at startup), require the rollback plan to include an explicit reset/restart step for those dependencies, not just the deployment revert.

### Detection & Response
1. **Post-Resolution Re-Alert Tracking**: Automatically flag any rollback marked "resolved" where the original triggering alert re-fires within a defined window afterward, and treat this as a confirmed instance of this failure mode requiring root-cause review of the verification gap.
2. **Symptom-Orchestrator Divergence Dashboard**: Track, for every rollback, the time delta between orchestrator "Succeeded" and symptom-metric baseline recovery; a persistent or growing delta across services indicates the verification gate is not effectively catching this class of premature resolution.

### Architecture Patterns
- **Two-Signal Resolution Gate**: A rollback is only eligible to be marked "resolved" once both the orchestrator's rollout-completion signal and an independent, incident-specific symptom-metric check pass; either signal alone is insufficient and blocks resolution.
- **Independent Post-Rollback Verification Service**: Symptom verification runs as a separate check outside the rollback agent's own execution path (different metric source, different service) so a single blind spot in the rollback agent's assumptions cannot both perform and self-certify the rollback.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| premature_resolution_rate | % of rollbacks marked "resolved" where the original alert re-fires within 15 minutes | > 2% |
| symptom_confirmation_gap_seconds | Median delay between orchestrator "Succeeded" and symptom-metric baseline recovery | Alert if median exceeds 5 minutes for a service |
| resolution_without_symptom_check_count | Count of rollbacks reported resolved with no symptom-metric evidence in the trace | > 0 per week |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Rollback marked resolved without symptom confirmation | Rollback report shows "resolved" with orchestrator success but no symptom-metric check in the trace | P1 | Reopen incident; run symptom check manually; patch the resolution-gating logic before re-enabling automated closure for that service |
| Alert re-fires after automated rollback resolution | Original triggering alert re-fires within 15 minutes of a rollback marked "resolved" | P1 | Immediate on-call re-engagement; treat prior resolution as invalid; audit for stateful dependencies missed by the rollback |

---

## References
- [Proof of Execution: Runtime Verification for Governed AI Agent Actions](https://arxiv.org/html/2607.05397)
- [Verify Before You Commit: Towards Faithful Reasoning in LLM Agents via Self-Auditing](https://arxiv.org/abs/2604.08401)
- [RIVA: Leveraging LLM Agents for Reliable Configuration Drift Detection](https://arxiv.org/pdf/2603.02345)
