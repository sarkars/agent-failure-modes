# Resource Reservation Insufficient

## Issue
Reserved/committed inference capacity is sized against a historical or forecasted peak-load estimate, but real peak demand exceeds it — from organic growth outpacing the forecast refresh cycle, a marketing event, or simple seasonality the original sizing didn't account for. When reserved capacity is exhausted, the system either throttles requests (queueing or rejecting them, degrading the user-facing SLA) or bursts onto on-demand capacity priced significantly higher than the reserved rate, so the exact moments that matter most for the business (peak demand, high-visibility traffic) are also the moments inference cost-per-token spikes hardest, inverting the cost curve exactly when it should be most efficient.

**Frequency**: Common

**Symptoms**
- Requests queue or get throttled during predictable peak windows (business hours, specific days of week, post-launch traffic) even though average daily utilization looks comfortably within capacity
- On-demand/burst capacity spend spikes sharply and repeatedly during the same recurring time windows, visible as a recurring pattern in cost dashboards rather than a one-off anomaly
- The reservation sizing was last updated significantly before the current traffic level was reached, and no process exists to trigger a review when growth outpaces the forecast
- p99 latency SLA violations cluster in the same recurring windows as the burst-capacity spend spikes
- Finance or platform reviews reveal on-demand capacity costs a large multiple of reserved-rate costs for the same workload, concentrated in a minority of hours that account for a disproportionate share of total spend

## Root Cause
Reserved capacity commitments (annual/multi-year GPU reservations, committed-use discounts) are priced favorably specifically because the provider is betting the customer will use them consistently; the customer's incentive is therefore to size the reservation close to typical/average usage to avoid paying for idle committed capacity, which is in direct tension with sizing generously enough to cover peak demand without expensive bursting. Forecasts used to set the reservation are snapshots — based on traffic data as of the planning cycle — and traffic growth, seasonality, or new product launches routinely outpace the forecast's validity period, especially in fast-growing AI product deployments where usage can grow 20-50% quarter over quarter. Because reservations are typically re-evaluated on a fixed cadence (quarterly or annual commitment cycles) rather than continuously against live demand, there's a structural lag between when real peak demand exceeds the reservation and when the reservation is resized, during which every peak-window request either queues/throttles or bursts onto premium-priced on-demand capacity — and because peak windows are, by definition, when the business needs the service to perform best, this is the worst possible time for either degradation.

## Example
```
A retail-recommendation agent's inference capacity is reserved at a level
sized against Q1 traffic data: a baseline of 40 GPU-equivalents covering
average load with a 25% peak buffer, purchased under a 1-year commitment
for a 35% discount versus on-demand pricing.

By Q3, organic product adoption has grown usage 60% versus the Q1
baseline the reservation was sized against, but the reservation itself
hasn't been revisited since purchase (the next scheduled capacity review
is aligned to the annual renewal, still 4 months out). Weekday peak hours
(11am-2pm and 6pm-9pm, tied to shopping behavior) now regularly exceed
the reserved 40 GPU-equivalents by 15-20 GPU-equivalents.

During these windows, the platform bursts onto on-demand capacity at
roughly 2.5x the reserved per-GPU-hour rate to avoid throttling. This
happens predictably, 5-6 hours per weekday, every week for the remaining
4 months before the reservation is due for renewal.

A cost analysis at renewal time finds that on-demand burst spend during
these recurring peak windows totaled more over the 4-month period than
the entire annual discount the original reservation was purchased to
capture — the team was paying a premium specifically at peak, for
exactly the traffic the reservation exists to serve affordably, because
nobody had a trigger to revisit sizing mid-commitment when growth
outpaced the original forecast.
```

## Statistics
| Finding | Context |
|---------|---------|
| Reserved/committed-use inference capacity commonly runs 1.3-1.6x its original forecast within 6-9 months for fast-growing AI product workloads | Typical range for high-growth AI product usage curves |
| On-demand/burst capacity used to cover reservation shortfalls commonly costs 2-3x the reserved per-unit rate | Typical range for cloud GPU on-demand versus committed-use pricing |
| Recurring predictable peak-window bursting, left unaddressed for a full commitment cycle, can erode 30-60% of the total savings the reservation was purchased to capture | Estimated range depending on how far actual peak exceeds reserved capacity |

## Mitigations
1. **Continuous demand monitoring against reservation, not fixed-cadence review**: Track live utilization versus reserved capacity on a rolling basis and trigger a resizing review automatically when a threshold (e.g. peak utilization exceeding 90% of reservation for multiple consecutive weeks) is crossed, rather than waiting for the scheduled annual/quarterly review.
2. **Size reservations against peak-with-growth-buffer, not average**: Explicitly model expected growth over the commitment period when sizing the reservation, building in a buffer informed by the workload's actual historical growth rate rather than a flat percentage peak buffer over current traffic.
3. **Layered commitment structure**: Use a mix of commitment lengths (e.g. a smaller long-term base reservation plus a shorter-term or more flexible mid-tier commitment) so capacity can be adjusted faster than a single long commitment cycle allows, reducing the lag between demand growth and reservation resizing.
4. **Track and cost-attribute recurring burst patterns explicitly**: Build a dashboard that isolates on-demand spend occurring during predictable recurring windows (same time of day/week) from genuinely unplanned bursts, since a recurring pattern is a clear signal the reservation itself is undersized, not that bursting is inherently unavoidable.
5. **Graceful degradation before expensive bursting**: For non-critical request types, prefer controlled queueing or reduced-priority processing over automatic on-demand bursting when reserved capacity is exceeded, reserving the premium-priced burst path for genuinely SLA-critical traffic.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| reserved_capacity_utilization_peak | Peak utilization of reserved capacity, tracked over rolling weekly windows | Alert if > 90% sustained across 3+ consecutive weeks |
| on_demand_burst_spend_recurring_ratio | Fraction of on-demand spend occurring in the same recurring time-of-day/day-of-week windows | Alert if > 60%, indicating a predictable rather than anomalous pattern |
| reservation_vs_forecast_drift | Current traffic level relative to the traffic level the reservation was sized against | Alert if drift exceeds 30% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Reservation consistently saturated at peak | reserved_capacity_utilization_peak > 90% for 3+ consecutive weeks | High | Trigger an off-cycle reservation resizing review |
| Recurring predictable burst pattern | on_demand_burst_spend_recurring_ratio > 60% over a rolling month | Medium | Model cost of resizing reservation versus continued bursting; propose adjustment |

## Related Patterns
- [Resource Quota Overcommit](./resource-quota-overcommit.md) - the cluster-level version of undersized capacity, where overlapping tenant demand rather than a single workload's growth causes the shortfall
- [Concurrent Request Resource Explosion](./concurrent-request-resource-explosion.md) - an acute version of this pattern's chronic shortfall, where a sudden spike rather than gradual growth exceeds reserved capacity
- [Latency Cost Tradeoff](./latency-cost-tradeoff.md) - insufficient reservation forces the same latency-versus-cost tension this pattern describes, but driven by under-provisioning rather than a deliberate tuning choice
