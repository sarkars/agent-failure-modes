# Cascade Branching

## Issue
A single triggering failure fans out into multiple independent cascades across unrelated subsystems, rather than propagating along one dependency chain. This happens when the failing component is a shared dependency consumed by several otherwise-independent subsystems (a shared auth service, a shared vector store, a shared message bus), so the initial fault triggers parallel, uncoordinated cascades that each unfold on their own timeline and are handled by different on-call teams who have no visibility into each other's incident. Unlike a single deepening cascade, branching multiplies the number of simultaneous incidents an organization has to manage at once.

**Frequency**: Occasional

**Symptoms**
- Multiple, seemingly unrelated incidents open in the incident tracker within minutes of each other, each assigned to a different team
- Each subsystem's on-call engineer independently diagnoses "their" incident without realizing a shared upstream dependency is the common trigger
- Incident resolution stalls because fixing one branch's symptom doesn't address the root cause, and the root-cause owner isn't aware of the other branches
- Post-incident timeline reconstruction reveals a single originating event with multiple, near-simultaneous divergence points

## Root Cause
Branching occurs at fan-out points in the dependency graph — components with many independent consumers. When such a component fails, each consumer subsystem reacts according to its own local resilience logic (its own retries, its own fallbacks, its own alerting), with no coordination between them because they were designed and operated independently. The absence of a shared incident correlation layer means each subsystem's cascade is investigated and mitigated in isolation, often duplicating effort and sometimes producing fixes in one branch that make another branch worse (e.g. one team disabling a feature flag that another team's fallback silently depended on).

## Example
```
09:14:00 - Shared feature-flag service ("FlagHub") begins returning stale
           cached values due to a Redis eviction storm, but does not error;
           it silently serves 6-hour-old flag states.

09:15:00 - Branch A: The recommendations agent reads a stale flag showing
           "new-ranking-model: off" (actually turned on 2 hours ago) and
           serves the old, lower-quality ranking model to 100% of traffic.
           Recommendations team opens INC-4471 for "ranking quality regression."

09:15:30 - Branch B: The checkout agent reads a stale flag showing
           "fraud-check-v2: on" (actually rolled back 3 hours ago due to a
           known false-positive bug) and starts blocking legitimate
           high-value orders. Payments team opens INC-4472 for
           "checkout conversion drop."

09:16:00 - Branch C: The support chatbot agent reads a stale flag showing
           "escalation-routing: legacy" and misroutes urgent tickets to a
           deprecated queue nobody monitors. Support team opens INC-4473
           for "ticket SLA breach," unaware of INC-4471/4472.

09:45:00 - Three separate teams spend 30 minutes independently debugging
           three "unrelated" issues before a platform engineer notices all
           three incidents reference FlagHub timestamps and identifies the
           single root cause.
```

## Statistics
| Finding | Context |
|---------|---------|
| Shared-dependency incidents produce 2-5 simultaneous downstream incidents on average before root-cause correlation occurs | Typical range observed in fan-out dependency failures |
| Mean time to correlate branching incidents into one root cause runs 2-4x the mean time to resolve a single-chain cascade | Estimated from cross-team incident postmortems |
| Organizations with automated dependency-graph correlation reduce branching-incident MTTR by roughly 40-50% | Reported range across teams using topology-aware alerting |

## Mitigations
1. **Shared-dependency incident correlation**: Instrument alerting to automatically flag when multiple concurrent incidents share an upstream dependency, surfacing the common node before teams diagnose in isolation.
2. **Fan-out blast-radius mapping**: Maintain and regularly validate a dependency graph that identifies high-fan-out components, and treat any degradation of those components as a multi-team incident by default.
3. **Single incident commander for shared-root events**: When a shared dependency is implicated, route all downstream incidents to one incident commander with cross-subsystem visibility, rather than letting each team run its own independent incident.
4. **Consistent fallback semantics across consumers**: Ensure all consumers of a shared component fail the same way (e.g. all fail open or all fail closed) so branching cascades don't produce contradictory system states.
5. **Cross-team fire drills on shared dependencies**: Regularly run failure injection on high-fan-out components with all downstream teams present, so responders recognize the branching pattern quickly in a real incident.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| concurrent_incident_count_by_dependency | Number of open incidents whose services share a common upstream dependency | Alert if >= 3 within 10 minutes |
| shared_dependency_error_rate | Error/staleness rate of components with fan-out above a defined threshold | Alert if degraded state persists > 2 minutes |
| cross_team_incident_correlation_time | Time from first branch incident opened to root-cause correlation identified | Alert if > 20 minutes |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Multi-branch incident spike | 3+ incidents opened within 10 minutes referencing overlapping upstream dependencies | High | Auto-page a cross-team incident commander, open a single unified incident |
| High-fan-out component degraded | A component with more than N known downstream consumers reports degraded health | Medium | Proactively notify all known downstream teams before they self-diagnose |

## Related Patterns
- [Cascade Amplification](./cascade-amplification.md) - amplification deepens one cascade chain, branching spreads the trigger across independent chains
- [Cascade Detection Failure](./cascade-detection-failure.md) - branching frequently causes detection failure because each branch looks like an unrelated incident
- [Single Point of Failure](./single-point-of-failure.md) - the high-fan-out shared dependency that enables branching is often an undocumented single point of failure
