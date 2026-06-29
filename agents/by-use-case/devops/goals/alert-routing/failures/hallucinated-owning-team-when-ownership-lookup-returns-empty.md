# Hallucinated Owning Team When Ownership Lookup Returns Empty

## Issue: When an Alert-Routing Agent's Call to the Service-Ownership Lookup Tool Returns an Empty Result -- Because the Firing Service Was Never Registered in the Ownership Database, or the Registration Lapsed -- the Agent Infers a Plausible Owning Team From the Service's Name or Naming Convention and Pages That Inferred Team as if It Were a Confirmed Owner, Rather Than Escalating the Unregistered Service as a Gap

**Frequency**: Occasional

**Symptoms**
- Agent pages a team (e.g., "payments-oncall" for a service named "payments-worker-v2") that has no record of owning, deploying, or operating the firing service
- The ownership-lookup tool's trace shows a successful call returning zero or null results immediately before the routing decision, with no explicit "unregistered service" flag raised to on-call
- The paged team reports the service is unfamiliar, has no relevant dashboards or runbooks, and cannot act on the page
- Re-querying the ownership database directly confirms the service genuinely has no registered owner, ruling out a transient lookup failure
- Time-to-acknowledgment for the real, eventually-identified owning team is inflated by the detour through the incorrectly inferred team

**Example**
```
New service "payments-worker-v2" fires a critical alert; it was deployed two weeks ago and never registered in the ownership database
Alert-routing agent calls the ownership-lookup tool, which returns an empty result (no registered owner)
Agent's routing decision: "Based on the naming convention, this is likely owned by the Payments team" -- pages Payments-oncall
Payments team has never heard of "payments-worker-v2"; it was actually deployed by a separate Checkout sub-team using payments-adjacent naming for an unrelated internal queue worker
20 minutes elapse before the actual deploying team is identified through git blame on the deployment manifest
Post-incident review finds the ownership-lookup tool correctly reported "no owner registered" but the agent treated that gap as a problem to solve via inference rather than a hard stop requiring escalation as unregistered
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible-sounding content to fill gaps left by failed, empty, or incomplete tool calls rather than treating the gap as a hard stop | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds agents frequently do not surface a null or empty tool result as a distinct failure signal, instead proceeding to generate output as if a meaningful result had been returned | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research for LLM agents argues traceable evidence linking generated claims to actual tool outputs is necessary because models do not reliably self-report when a claim (such as an inferred owning team) lacks real grounding | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- No explicit instruction distinguishing an empty/null ownership-lookup result from a result the agent is free to fill in by inference
- Naming-convention inference is a generally useful heuristic for other tasks, so the agent applies it here without recognizing that ownership routing requires confirmed, not inferred, evidence
- No registry-completeness check flags newly deployed services lacking an ownership record before they reach production alerting
- The agent's output does not visibly distinguish a confirmed owner (from a successful lookup) from an inferred one (from naming heuristics), so reviewers cannot tell which page was a guess

---

## Mitigation Strategies

1. **Hard Stop on Empty Ownership Result**: Require the agent to escalate an unregistered-service alert as a distinct "no owner registered" incident type rather than inferring an owner from naming convention
2. **Deploy-Time Ownership Gate**: Block production alerting configuration for any service lacking a registered owner at deploy time, preventing the empty-lookup scenario from reaching live paging
3. **Confirmed-vs-Inferred Labeling**: Require any routing decision based on inference rather than a successful lookup to be labeled as such in the page itself, so the receiving team and on-call lead can immediately recognize it as unconfirmed
4. **Fallback Escalation Tier**: Route unregistered-service alerts to a dedicated triage rotation responsible for identifying actual ownership, rather than a heuristically guessed team

### Metrics
- Rate of pages sent to a team with no matching record in the deploy/ownership history for the firing service
- Number of alerts firing for services with no registered owner at alert time
- Mean time-to-correct-team for alerts that were initially inferred-routed

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Inferred-owner page sent | Routing decision based on naming inference rather than confirmed lookup result | P2 | Re-route to unregistered-service triage; verify actual owner |
| Unregistered service alerting | Alert fires for a service with no ownership record | P1 | Block further inferred routing; escalate to triage rotation |
| Registry gap recurrence | Multiple unregistered-service alerts from the same deploy pipeline within a rolling window | P3 | Audit deploy-time ownership gate |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
