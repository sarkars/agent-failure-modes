# Per-Tool Monthly Budget Overrun

## Issue
Monthly spend tracking for a tool relies on vendor-reported usage or billing data that lags real-time by hours to days — usage dashboards update once daily, or invoices are only finalized at month-close. By the time anyone (human or automated system) detects that the monthly budget has been exceeded, the agent has continued making calls against the stale "still within budget" reading for however long the reporting lag lasted, often turning a modest overage into a large one.

**Frequency**: Common

**Symptoms**
- The vendor's own usage dashboard or billing API consistently reports figures that are hours to days behind real-time consumption
- Budget-cap enforcement based on the vendor's reported figures fires well after the cap was actually crossed
- The size of the overrun correlates with the length of the reporting lag and the agent's call rate during that window
- Internal, agent-tracked spend estimates (if they exist) and vendor-reported spend diverge increasingly as the month progresses, with vendor figures always trailing
- Overruns are discovered in bursts around monthly reporting cadences (e.g. everyone finds out on the 1st of the month) rather than continuously

## Root Cause
Many usage-based API vendors do not expose real-time spend data; their billing pipelines batch usage into periodic (often daily) aggregation jobs for internal accounting reasons, and only that aggregated figure is exposed via dashboard or API. An agent's own budget enforcement, if it relies on querying the vendor's reported usage rather than independently tallying its own calls, inherits that lag — it is enforcing a cap against information that is already stale, and every call made during the lag window is effectively unconstrained.

## Example
```
"MarketDataAPI" is capped at $2,000/month, and the agent's budget-guard
component checks MarketDataAPI's official usage-and-billing endpoint
before each batch of calls to confirm the account is under cap. That
endpoint aggregates usage once every 24 hours.

On the 22nd of the month, cumulative real usage crosses $2,000 at 3am,
but the billing endpoint (last updated at midnight) still reports $1,840
until its next update at midnight the following day.

During that ~21-hour window, the agent's budget guard sees "under cap"
and continues normal operation, including a scheduled overnight batch job
that alone makes $650 worth of calls. By the time the billing endpoint
catches up and reports the true figure the next day, actual spend is
$2,490 — a $490 overrun, nearly all of it accumulated during the single
reporting-lag window, and the agent kept calling for a further six hours
after the corrected figure was available because no alert was configured
on the corrected number either.
```

## Statistics
| Finding | Context |
|---------|---------|
| Vendor usage/billing dashboards commonly update on a daily batch cycle rather than in real time | Common pattern among usage-based API vendors |
| Budget overruns caused specifically by reporting lag (rather than raw over-usage) are typically concentrated in the final 24-48 hours before cap detection | Typical pattern given daily aggregation cycles |
| Overrun size correlates strongly with agent call rate during the lag window; a high-throughput job scheduled during the lag can multiply the overrun several-fold | Common pattern in incident postmortems |

## Mitigations
1. **Independent real-time spend tracking**: Maintain the agent's own running cost tally computed from its own call log and known per-call pricing, rather than relying solely on the vendor's reported usage figure, so enforcement isn't gated by vendor reporting lag.
2. **Conservative buffer below the true cap**: Set the internally-enforced cap meaningfully below the actual contractual/budget limit (e.g. enforce at 85% of the real cap) to absorb the uncertainty introduced by any residual reporting lag.
3. **Reconciliation with drift correction**: When the vendor's authoritative figure does arrive, reconcile it against the internal tally and adjust the internal counter's calibration if a persistent bias is found.
4. **Lag-aware throttling for high-throughput windows**: Identify scheduled or bursty jobs (nightly batches) that could make large jumps in spend within a single reporting-lag window, and require an extra-conservative internal cap specifically around those jobs.
5. **Two-tier alerting**: Alert on the internally-tracked real-time estimate approaching cap (early warning) in addition to alerting on the vendor's authoritative figure (confirmation), rather than waiting for the lagging source alone.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| internal_vs_vendor_reported_spend_delta | Difference between the agent's real-time internal spend tally and the vendor's last-reported figure | Alert if delta exceeds 10% of monthly cap |
| reporting_lag_duration | Time between real spend event and vendor dashboard/billing reflecting it | Alert if lag exceeds 6 hours |
| overrun_amount_at_detection | Size of the overage discovered once authoritative figures update | Alert if > 5% of monthly cap |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Internal tally approaching cap | Internally-tracked spend estimate exceeds 85% of the monthly cap | High | Throttle non-critical calls pending vendor reconciliation |
| Confirmed overrun on reconciliation | Vendor-authoritative figure, once updated, shows the cap was exceeded | High | Halt further calls, notify budget owner, review lag-window scheduled jobs |

## Related Patterns
- [Per-Tool Daily Budget Exhaustion](./per-tool-daily-budget-exhaustion.md) - the daily-scale analog, though driven by front-loaded usage rather than reporting lag
- [Cross-Tool Total Budget Exceeded](./cross-tool-total-budget-exceeded.md) - both are cases of budget enforcement acting on incomplete or stale information
- [Tool Cost Override Incident](./tool-cost-override-incident.md) - reporting lag can mask both routine overruns and forgotten manual overrides
