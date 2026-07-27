# What Are the Most Common Alert Routing Failures in AI Agents?

**Alert-routing agents page the wrong team when the routing decision rests on an input that looks authoritative but isn't — a service-ownership mapping that was never revalidated after a reorg, a runbook retrieved by lexical similarity instead of structured ownership, or a suppression scope that a scheduling agent reasoned through but never wrote into the field the router actually reads.** In all three documented patterns the routing logic itself executes correctly given its input; the failure is that the input — a mapping, a retrieved document, a calendar entry — is stale, mismatched, or incomplete in a way the router has no mechanism to detect. That distinction matters operationally: fixing routing accuracy here means fixing the freshness and structure of the data feeding the router, not tuning the router's decision rule.

## Key Takeaways

- 3 patterns are documented, one for each of the goal's distinct failure surfaces: stale ground-truth data, similarity-based retrieval standing in for structured filtering, and cross-agent handoff loss.
- A stale service-ownership mapping produced a measured 12-minute re-route delay in the on-call escalation misroute example — pure routing latency added on top of the incident itself, before the correct team was even engaged.
- Embedding-retrieval misrouting concentrates specifically on alert types with generic, widely-reused error vocabulary (timeouts, connection resets, generic 5xx errors), because that vocabulary maximizes lexical similarity across runbooks written for entirely different services.
- The maintenance-window suppression-flag handoff failure is rated "Frequent" — the highest frequency rating among the three alert-routing patterns — because calendar-entry schemas commonly capture only a time range, with no field for partial or conditional suppression scope.

## Scope

- **Stale Ground-Truth Routing** — [On-Call Escalation Misroute](failures/on-call-escalation-misroute.md). A service-to-team ownership mapping drifts out of date after a reorg or ownership transfer, and the routing agent has no freshness signal to distinguish a current mapping from a stale one — both produce an equally confident exact match.
- **Retrieval-Based Misrouting** — [Embedding Retrieval Misroutes Alert via Similar Runbook Match](failures/embedding-retrieval-misroutes-alert-via-similar-runbook-match.md). The agent selects a runbook by free-text semantic similarity over incident descriptions rather than first filtering by structured service-ownership metadata, so a lexically similar runbook for the wrong service outranks the correct one.
- **Cross-Agent Handoff Loss** — [Multi-Agent Handoff Drops Maintenance-Window Suppression Flag](failures/multi-agent-handoff-drops-maintenance-window-suppression-flag-between-scheduler-and-alert-router.md). A scheduling agent's own planning output correctly scopes which alerts to suppress during a maintenance window, but the structured calendar entry it hands off carries only a time range, so the alert router pages on-call for expected, plannable noise.

## When Alert Routing Matters

- Service ownership or on-call rotations change frequently (team reorgs, service splits/merges) while routing depends on a mapping that is only updated manually
- Runbook or playbook selection is implemented via embedding or semantic-similarity retrieval rather than structured service-ownership filtering
- Maintenance windows, scheduled changes, or planned suppression require a scheduling or tuning agent to hand a scope determination to a separately-invoked routing agent

## Cross-Pattern Insight

All three alert-routing patterns share the same underlying gap: the routing agent treats its input — an ownership mapping, a retrieved runbook, a calendar entry — as complete and current, when the actual determination (who owns this now, which runbook truly applies, which alerts this window covers) was either never captured in a structured field or was captured once and never revalidated. None of the three failures originates in flawed routing logic; each router does exactly what its input tells it to do. The fix in every case is the same shape: attach a freshness or structural-match signal to the input, and verify it at decision time rather than trusting the artifact was correct when it was created.

## Frequently Asked Questions

### What causes an alert to be routed to the wrong on-call team?
Most commonly, a service-ownership mapping that was correct when created but never updated after a team reorganization or ownership transfer — the routing agent finds an exact service-name match and routes with high confidence, with no signal that the mapping itself has drifted out of date. See [On-Call Escalation Misroute](failures/on-call-escalation-misroute.md).

### How do you detect a stale ownership mapping before it causes a misroute?
Attach a last-validated timestamp to every ownership-mapping entry, cross-check it on a recurring schedule against an authoritative source (org chart, service catalog, deploy-pipeline ownership tags), and surface low freshness confidence separately from exact-name-match confidence rather than folding both into a single score.

### Can embedding similarity alone route alerts by service ownership?
No. Embedding similarity over free-text incident descriptions captures shared symptom vocabulary, not which service actually owns the alert — two runbooks for unrelated services can sit close together in embedding space simply because both describe a generic timeout or 5xx spike. Retrieval needs to filter to the alerting service's structured ownership metadata before ranking by similarity, not after.

### Does a maintenance-window suppression failure mean the scheduling agent reasoned incorrectly?
No — in the documented case the scheduling agent's planning output correctly identified the exact suppression scope. The failure is a handoff-schema gap: the calendar entry it created had no field to carry that scope, so the alert router could only see a time range and paged on-call for every alert firing during the window.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Embedding Retrieval Misroutes Alert via Similar Runbook Match](failures/embedding-retrieval-misroutes-alert-via-similar-runbook-match.md) | Free-text similarity retrieval pulls a lexically similar runbook for the wrong service |
| [Multi-Agent Handoff Drops Maintenance-Window Suppression Flag](failures/multi-agent-handoff-drops-maintenance-window-suppression-flag-between-scheduler-and-alert-router.md) | Scheduling agent's suppression-scope reasoning never reaches the structured calendar field the router reads |
| [On-Call Escalation Misroute](failures/on-call-escalation-misroute.md) | Static service-ownership mapping drifts stale after reorg, routed with false confidence |

**Total: 3 patterns**

## Related Goals

- [Incident Response](../incident-response/) — failures that occur once the right team is already engaged, including handoff and root-cause-attribution gaps
- [Monitoring](../monitoring/) — upstream signal-quality failures (silent gaps, cardinality limits) that determine whether an alert fires at all before routing decides who receives it
- [Deployment Safety](../deployment-safety/) — a parallel embedding-retrieval and handoff-loss pattern set, applied to checklist selection and precondition propagation instead of routing
