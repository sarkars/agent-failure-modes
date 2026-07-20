# Blue-Green Deployment Traffic Not Switched

## Issue
An agent orchestration platform deploys a new agent version (updated system prompt, tool schema, or model pointer) to a fully provisioned "green" environment alongside the running "blue" environment, but the load balancer or service mesh routing rule that should cut traffic over to green never actually flips. The green fleet passes its smoke tests, health checks report healthy, and the deployment pipeline marks the release as "complete," yet 100% of live agent sessions continue to be served by the stale blue version. The team believes the new version is live — including any urgent fix it was supposed to carry — while users keep hitting the old behavior.

**Frequency**: Occasional

**Symptoms**
- Deployment pipeline reports success but production error rates, latencies, or observed model/prompt versions in logs don't change
- `X-Agent-Version` (or equivalent) response header stays pinned to the old version across all sampled requests
- Green environment shows zero or near-zero request volume in its dashboards despite being marked "active"
- A fix that was deployed to address an incident appears to have "not worked" when in fact it was never receiving traffic
- Manual `curl` against the green endpoint directly returns the new version, but traffic through the public/internal load balancer does not

## Root Cause
Blue-green cutover typically depends on a discrete, external action — repointing a load balancer target group, updating a DNS record, or flipping a service-mesh VirtualService/route weight — that is decoupled from the deployment step that provisions and health-checks the green fleet. When these two steps are orchestrated by separate systems (e.g., a CI/CD pipeline that finishes provisioning and reports success, versus a separate GitOps reconciliation loop or a human-run runbook step that performs the cutover), a partial failure, a stale cache in the load balancer control plane, or a missed manual step leaves the routing rule pointed at blue even though every other signal says the release finished. Because "deployment succeeded" and "traffic switched" are treated as the same event in dashboards and alerting, nobody notices the routing rule never moved until someone specifically diffs live traffic against the target environment.

## Example
```
Team ships v14 of the "SupportAgent" orchestrator to fix a tool-call
argument-serialization bug that was causing malformed API calls in v13.

1. CI/CD pipeline builds v14, deploys it to the green target group
   (agent-green.internal), runs 50 synthetic conversations against it,
   all pass. Pipeline marks the release "Deployed successfully."

2. The cutover step — updating the ALB listener rule to send
   production traffic to agent-green instead of agent-blue — is a
   separate Terraform apply gated on a manual approval in a different
   system. The approval was requested but the Slack notification
   landed in a channel nobody was actively watching that day.

3. For 19 hours, 100% of live traffic keeps hitting agent-blue (v13).
   The malformed tool-call bug keeps firing in production. On-call
   sees no improvement in the error-rate dashboard and starts treating
   v14 as if it "didn't fix the bug," reopening the incident and
   spending 3 hours re-debugging code that was never live.

4. Someone finally checks `X-Agent-Version` on live responses, sees
   "v13," and discovers the ALB listener rule was never applied.
   Manually approving the Terraform apply switches traffic
   immediately; the error rate drops within the next request batch.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of blue-green cutover incidents are "silent" — the deployment pipeline reports success and no alert fires for the missed switch | Typical range observed in teams using decoupled deploy/cutover tooling |
| Time-to-detection for a stuck cutover is commonly measured in hours, not minutes, when success is inferred from pipeline status rather than live traffic sampling | Estimated from post-incident reviews of decoupled CD pipelines |
| Coupling cutover into the same automated step as provisioning removes the majority of these incidents in teams that have made the change | Reported range across teams that consolidated deploy+cutover into one pipeline stage |

## Mitigations
1. **Single-pipeline cutover**: Fold the traffic-switch step into the same automated pipeline that provisions and health-checks the green environment, rather than a separate manual or loosely-coupled system, so "deployed" and "switched" cannot diverge.
2. **Post-cutover traffic verification**: After the switch step runs, automatically sample live production responses for the version identifier (header, log field, or synthetic canary request) and fail the pipeline if the observed version doesn't match the target within a short window.
3. **Version-aware dashboards**: Break error-rate, latency, and volume dashboards down by observed agent version rather than by "environment," so a stuck cutover is visible as "100% of traffic on v13" instead of being masked by an environment label that says "green: active."
4. **Cutover timeout alert**: If a release is marked "deployed" but traffic-weighted version telemetry hasn't shown the new version within a configured SLA (e.g., 10 minutes), page on-call automatically instead of relying on someone to notice a stalled incident fix.
5. **Idempotent, retryable switch step**: Make the routing-rule update itself retryable and reconciled continuously (GitOps-style) rather than a one-shot apply, so a transient failure or a missed manual approval doesn't silently leave the old rule in place indefinitely.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| traffic_weighted_version_mismatch | Share of live requests reporting a version other than the last "deployed" release | Alert if > 5% for more than 10 minutes post-deploy |
| green_environment_request_share | Fraction of total request volume landing on the green target group | Alert if < 90% within SLA window after cutover marked complete |
| cutover_step_completion_lag | Time between "deployment complete" event and observed traffic-weight change | Alert if > 15 minutes |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Cutover stalled post-deploy | Deployment marked complete but green_environment_request_share stays below threshold past SLA | High | Page on-call, manually verify/apply the routing rule, halt further releases until resolved |
| Version mismatch after incident fix | An incident-remediation deploy completes but live traffic still reports the pre-fix version | High | Escalate immediately; treat the incident as still open until traffic confirms the fix version |

## Related Patterns
- [Canary Deployment Incomplete](./canary-deployment-incomplete.md) - a related traffic-shift failure where the cutover starts but never finishes ramping past a partial percentage
- [Traffic Routing Asymmetry](./traffic-routing-asymmetry.md) - both involve routing rules that don't match the deployment system's belief about what's live
- [Deployment Validation Skipped](./deployment-validation-skipped.md) - the missing post-cutover verification step is a specific instance of a skipped validation gate
- [Connection Draining Incomplete](./connection-draining-incomplete.md) - the counterpart failure that occurs once a cutover does happen, around how the old environment is retired
