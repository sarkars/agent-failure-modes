# Cascade Detection Failure

## Issue
A cascading failure that originates from a single root cause and propagates through several dependent components is not recognized as one incident. Instead, monitoring and on-call responders see a series of alerts from different services and open separate tickets, each investigated independently as if unrelated. Because no one is looking at the whole picture, responders spend time fixing symptoms in each affected service without ever addressing the shared trigger, and the incident often "resolves" temporarily in one place only to resurface in another minutes later.

**Frequency**: Common

**Symptoms**
- Multiple alerts fire within a short window across different services, each triaged by a different team as a standalone issue
- Incident tickets lack any cross-reference to each other despite near-identical timestamps
- A fix applied to one affected service doesn't stick, or is followed by a new alert elsewhere in the graph shortly after
- Post-incident review is the first time anyone notices the alerts shared a common upstream trigger
- Dashboards show per-service health but no aggregate or topology-aware view that would reveal the shared root

## Root Cause
Detection systems are typically built per-service: each service emits its own metrics and alerts against its own thresholds, with no correlation layer that maps alerts back to a shared dependency graph. When a cascade begins, every affected service crosses its own alert threshold at a slightly different time (depending on propagation delay, retry timing, and cache TTLs), producing a scattered sequence of alerts that looks like independent noise rather than one unfolding event. Without an explicit causal-correlation mechanism — trace propagation, shared incident IDs, or topology-aware alert grouping — human responders are left to manually notice timestamp correlations, which they usually don't, especially across team boundaries.

## Example
```
14:02:10 - Primary database connection pool for OrderService begins
           rejecting new connections after a slow migration script leaks
           connections. OrderService alert fires: "connection pool 95% full."
           Assigned to Database team as INC-8801.

14:03:40 - PaymentService, which calls OrderService synchronously to
           validate order state before charging, starts timing out.
           PaymentService alert fires: "P99 latency > 5s." Assigned to
           Payments team as INC-8802. No reference to INC-8801.

14:05:15 - NotificationService, downstream of PaymentService events, sees
           its event queue backing up because payment-confirmed events stop
           arriving. Alert fires: "queue depth > 10,000." Assigned to
           Platform team as INC-8803. No reference to prior incidents.

14:06:00 - Customer-facing checkout success rate drops to 40%. A fourth,
           customer-impact-level incident (INC-8804) is opened by the
           incident commander rotation, still without connecting to the
           other three.

14:40:00 - During a status-sync call, someone notices all four incidents
           started within 4 minutes of each other. A trace lookup confirms
           the OrderService connection pool exhaustion as the single root
           cause. 34 minutes were spent on parallel, redundant
           investigation across three teams.
```

## Statistics
| Finding | Context |
|---------|---------|
| A single cascading root cause typically generates 3-6 separately-triaged alerts before correlation occurs | Typical range observed in per-service alerting setups without topology correlation |
| Manual cross-team correlation of a cascade adds an estimated 20-40 minutes to mean time to resolution | Estimated from incident postmortem timelines |
| Teams using distributed tracing with automatic incident correlation identify shared root causes roughly 3x faster than teams relying on manual timestamp comparison | Reported range across observability tooling adoption studies |

## Mitigations
1. **Trace-based causal correlation**: Propagate a shared trace/correlation ID through every request in the call chain so alerting tools can automatically group alerts that share a causal ancestor.
2. **Topology-aware alert grouping**: Feed the service dependency graph into the alerting system so it can group simultaneous alerts on dependent services into a single incident by default, rather than opening one per service.
3. **Time-windowed alert clustering**: Automatically flag any set of alerts firing across different services within a short time window (e.g. 5 minutes) as a candidate single incident requiring correlation review before separate tickets are opened.
4. **Unified incident dashboard**: Maintain a cross-service view that overlays alert timelines against the dependency graph, so an on-call responder can visually spot the propagation pattern instead of relying on memory of other teams' alerts.
5. **Postmortem correlation review**: Make "could this have been detected as a single cascade" an explicit postmortem question, and track the number of tickets later merged into one root-cause incident as a detection-quality metric.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| uncorrelated_alert_cluster_size | Count of alerts firing within a short time window across dependent services without a shared incident ID | Alert if >= 3 within 5 minutes |
| time_to_root_cause_correlation | Elapsed time from first alert to identification of a shared root cause | Alert if > 15 minutes |
| tickets_merged_post_incident | Number of separately-opened tickets later merged into one root-cause incident | Track trend; alert on sustained increase |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Correlated alert cluster detected | 3+ alerts across dependent services fire within a 5-minute window | High | Auto-open a single unified incident, notify all implicated team leads |
| Repeated re-alert after mitigation | An alert that was marked resolved re-fires on a dependent service within 30 minutes | Medium | Reopen as part of the original incident rather than a new ticket |

## Related Patterns
- [Cascade Branching](./cascade-branching.md) - branching cascades are especially prone to detection failure because each branch presents as an unrelated incident
- [Cascade Amplification](./cascade-amplification.md) - undetected cascades have more time to amplify before anyone applies the correct fix
- [Recovery Procedure Untested](./recovery-procedure-untested.md) - detection failure often means the correct recovery procedure is never invoked at all
