# Single Point of Failure

## Issue
A critical agent, tool, service, or piece of shared infrastructure has exactly one instance in the architecture, with no redundant standby, no alternate path, and no fallback that doesn't itself depend on the same component — so that component's failure takes down every workflow that depends on it, directly or transitively, all at once. This is an architectural gap, not a failure that unfolds once triggered: the system was designed (or, more often, organically grew) without redundancy for a component that turned out to be load-bearing for far more of the system than anyone tracking "what's critical" realized at the time it was introduced.

**Frequency**: Common

**Symptoms**
- One component's outage produces an incident whose blast radius is disproportionate to how "small" or "peripheral" that component was assumed to be
- Post-incident architecture review reveals the failed component had no redundant instance, no documented fallback, and no owner who had previously flagged it as critical infrastructure
- A dependency-graph audit, run reactively after an incident, finds several other components with the same missing-redundancy characteristic that haven't failed yet
- The component in question was originally built as a small utility or an internal convenience (a shared config service, a single authentication check, a single feature-flag store) and accumulated critical dependents over time without anyone revisiting its redundancy requirements
- Adding redundancy after the fact is disproportionately expensive or invasive compared to what it would have cost to design in from the start, because many callers now depend on the component's specific single-instance behavior (in-memory state, a fixed address, no failover-aware client logic)

## Root Cause
Single points of failure accumulate because criticality is rarely assessed at the time a component is introduced — a service starts small, serving one internal caller, and redundancy feels like premature engineering effort for something with low apparent stakes. As more callers adopt it over time (often because it's convenient, already exists, and "just works"), its actual blast radius grows silently, but no corresponding review re-evaluates whether it still deserves single-instance treatment now that dozens of critical workflows depend on it. Unlike a cascade, which describes how a failure propagates once it starts, or a retry storm, which describes how retry behavior overwhelms a system under load, this pattern describes a static property of the architecture itself: the absence of any redundancy for a component that has, often invisibly, become load-bearing.

## Example
```
A "notification preferences" service is built early in a platform's
life to store which channels (email, SMS, push) each user wants
notifications on. It's treated as low-stakes: if it's briefly
unavailable, notifications just don't get sent for a few minutes, which
seemed like an acceptable degradation at the time. It's deployed as a
single instance with no replica, since redundancy felt like overkill
for a preferences lookup.

Two years later, a dozen different services - order confirmations,
fraud alerts, password-reset codes, appointment reminders, an
autonomous support agent that checks notification preferences before
deciding whether to page a human - all query this same service
synchronously as a blocking step before they can complete their own
core action, because it was the path of least resistance to reuse an
existing service rather than build a new one.

The single instance runs out of disk space during a routine log
rotation failure. It goes down. Every one of those dozen dependent
services now blocks or fails on a call to what was originally conceived
of as a minor, non-critical preferences lookup - including
password-reset codes, which are now undeliverable platform-wide, and
the fraud-alert pipeline, which silently fails open rather than
blocking suspicious transactions since its error-handling path assumed
this call would basically never be down.

Post-incident review finds no one had revisited this service's
redundancy posture since it was built, despite its dependent list
growing from 1 caller to 12 without any corresponding review.
```

## Statistics
| Finding | Context |
|---|---|
| A significant share of high-severity incidents in mature systems trace back to a single-instance component whose criticality had grown well past its original design assumptions | Estimated from postmortems categorizing root cause as "missing redundancy" rather than a bug in the failing component itself |
| Components introduced as internal utilities are disproportionately likely to become undocumented single points of failure, compared to components that were designed from the outset as shared critical infrastructure | Typical pattern observed in incident postmortems tracing blast radius growth over a component's lifetime |
| Regular dependency-graph audits that flag components by caller count (not just by original design intent) catch a meaningful share of undocumented single points of failure before they cause an incident | Reported range across teams running periodic criticality re-assessment versus teams relying only on initial design review |

## Mitigations
1. **Re-assess criticality based on current dependents, not original design intent**: Periodically audit the dependency graph for components whose caller count or blast radius has grown well beyond what their original single-instance design assumed, and treat "how many things now depend on this" as the trigger for a redundancy review, not the component's original purpose.
2. **Require an explicit criticality tier and matching redundancy posture for new shared components**: When a component is expected to be reused (a shared service, a shared config store, a shared auth check), assign it a criticality tier at creation time and provision redundancy proportional to that tier, rather than defaulting to single-instance until an incident proves otherwise.
3. **Design fallback paths that don't share the same single point**: Where a true redundant instance isn't feasible, ensure dependent services have a degraded-but-independent fallback (a cached last-known-good value, a conservative default) that doesn't itself require the same component to be available.
4. **Run failure injection specifically against components with no known redundancy**: Proactively test what happens when a suspected single point of failure goes down, in a controlled setting, rather than discovering its full blast radius for the first time during a real outage.
5. **Make "how does this fail" part of onboarding a new dependency, not just building the component**: When a new service decides to depend on an existing component, require that decision to record what happens to the new caller if the dependency is unavailable, surfacing missing-redundancy risk at the point of adoption rather than only at the point of failure.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| dependent_count_per_single_instance_component | Number of distinct callers depending on a component with no redundant instance | Alert when count crosses a criticality threshold without a corresponding redundancy review |
| blast_radius_to_original_criticality_ratio | Ratio of a component's current incident blast radius to its originally assigned criticality tier | Alert on components where actual dependents/impact far exceed original tier |
| single_instance_uptime_dependency_score | Aggregate measure of how many critical workflows are blocked by a single component's availability | Track over time; alert on upward trend for any one component |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Uncoordinated growth in dependents on a single-instance component | dependent_count_per_single_instance_component crosses threshold | Medium | Schedule a redundancy/criticality review before the next dependent is onboarded |
| Single point of failure outage | A component with no redundant instance and a nonzero dependent count becomes unavailable | Critical | Failover to any available degraded path, prioritize post-incident redundancy remediation |

## Related Patterns
- [Cascade Branching](./cascade-branching.md) - a high-fan-out shared dependency is frequently the same component this pattern describes; branching covers what happens once that component fails and its failure fans out, this pattern covers the architectural gap that made the fan-out possible in the first place
- [Cascade Isolation Failure](./cascade-isolation-failure.md) - isolation failure is a bulkhead that was supposed to contain a failure turning out to be leaky; this pattern is the more basic case where no bulkhead or redundancy was ever designed in at all
- [Retry Storms](../../cost-efficiency/failures/retry-storms.md) - retry storms describe how retry behavior overwhelms a system under load; a single point of failure is often the component that a retry storm ultimately saturates, but the two are independent root causes
- [Redundancy Coordination Failure](./redundancy-coordination-failure.md) - the opposite failure mode: this pattern is too little redundancy, that pattern is redundancy present but uncoordinated
