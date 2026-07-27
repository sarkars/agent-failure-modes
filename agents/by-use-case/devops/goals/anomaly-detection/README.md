# What Are the Most Common Anomaly Detection Failures in AI Agents?

**Anomaly-detection agents produce false positives and false negatives because they optimize a baseline or threshold against the wrong reference — recent noise instead of a recall floor, temporal proximity instead of causal mechanism, or a static value instead of the seasonal or event-driven pattern actually shaping the metric.** Five distinct patterns are documented here, and every one traces back to the same structural gap: the detector's model of "normal" is simpler than the real signal, so it either fires on benign variation it never learned to recognize or stays silent on a real incident that resembles previously-tolerated noise. Because these are silent failures in both directions — a missed incident and a suppressed alert look identical to "no alert fired" — the cost of getting the baseline wrong is not visible until the next real event exposes it.

## Key Takeaways

- 5 patterns span three mechanisms: baseline/threshold miscalibration, correlation-vs-causation confusion, and cross-agent handoff loss.
- Seasonal blindness alone produces a documented 20-40% false-positive rate during seasonal peaks without explicit seasonality modeling, dropping to 1-5% once seasonal decomposition is applied — a 2-5x baseline swing the naive model has no way to distinguish from a real anomaly.
- Correlation-induced false positives show metric correlation running 0.7-0.9 in normal operation and 0.8-0.95 during a cascade failure — high in both cases — which is why correlation-aware detection reaches 95% precision against 60% for models that treat coordinated spikes as inherently more anomalous.
- Threshold auto-tuning that optimizes only against recent false-positive history (alert-fatigue-driven widening) has no opposing recall constraint, so a threshold widened to suppress noise silently also suppresses the rare true positive that looks statistically similar to that noise.

## Scope

- **Baseline and Threshold Miscalibration** — [Alert Fatigue from Threshold Misconfiguration](failures/alert-fatigue-from-threshold-misconfiguration.md), [Seasonal Blindness](failures/seasonal-blindness.md). The detector's notion of "normal" is a single static or recency-tuned bound that doesn't model daily/weekly/seasonal structure or hold out a recall floor against rare real incidents.
- **Correlation-vs-Causation Confusion** — [Correlation-Induced False Positives](failures/correlation-induced-false-positives.md), [Deploy-Correlated Anomaly Misattribution](failures/deploy-correlated-anomaly-misattribution.md). The detector treats a statistical or temporal association (metrics moving together, a deploy preceding an anomaly) as evidence of a specific cause, without checking whether the association is actually causal.
- **Cross-Agent Handoff Loss** — [Multi-Agent Handoff Drops Baseline Adjustment Between Tuning Agent and Detection Agent](failures/multi-agent-handoff-drops-baseline-adjustment-between-tuning-agent-and-detection-agent.md). A tuning agent's event-specific, time-bound adjustment reasoning never reaches the structured threshold configuration the detection agent actually evaluates against.

## When Anomaly Detection Matters

- Traffic or resource metrics have known daily, weekly, or seasonal structure (retail peaks, batch-processing cycles, regional traffic patterns) that a static baseline cannot represent
- Multiple correlated metrics (CPU, memory, disk I/O, latency) are monitored together and a single root cause can trigger simultaneous spikes across all of them
- Threshold or baseline tuning is automated and iterates on recent history without a held-out set of known rare-incident signatures to guard against recall loss

## Cross-Pattern Insight

Every anomaly-detection pattern documented here reduces to the same tension: the detector is evaluated and tuned against the data it has already seen, and the failure appears exactly where reality diverges from that history — a seasonal peak the baseline never modeled, a cascade the model reads as multiple coordinated failures, a deploy that merely coincides with an unrelated cause, or a scheduled exception that never made it from one agent's reasoning into the other agent's structured configuration. The recurring mitigation is the same across all five patterns: never let a single aggregate signal (average utilization, temporal proximity, a widened threshold) stand in for a validated, structured, and — where multiple agents are involved — explicitly propagated model of what "expected" actually looks like for that metric, that time, and that event.

## Frequently Asked Questions

### What causes an anomaly detector to flag normal seasonal traffic as an incident?
A statistical baseline built on a simple mean-and-standard-deviation model with no explicit seasonal component — daily, weekly, and yearly traffic cycles look identical to a real spike unless the model decomposes trend and seasonality first. See [Seasonal Blindness](failures/seasonal-blindness.md).

### How do you tell a cascading failure from a coordinated multi-system attack?
Trace the correlated spikes to a single root cause rather than trusting the correlation itself — metrics that are highly correlated in normal operation stay highly correlated during a cascade, so correlation strength alone cannot distinguish "one failure with many effects" from "several independent failures." [Correlation-Induced False Positives](failures/correlation-induced-false-positives.md) documents the 0.7-0.95 correlation range spanning both cases.

### Can auto-tuned alert thresholds silently make a detector worse over time?
Yes — if tuning optimizes only false-positive rate against recent history with no recall floor against known rare-incident signatures, every widening pass makes the detector marginally worse at catching real incidents that resemble the noise it just learned to ignore, and without versioned threshold history this drift is invisible until a real incident is missed. See [Alert Fatigue from Threshold Misconfiguration](failures/alert-fatigue-from-threshold-misconfiguration.md).

### Does attributing an anomaly to the most recent deploy count as root-cause analysis?
Not on its own. Temporal proximity to a deploy is a low-cost heuristic, not a causal check — it produces false attributions whenever an unrelated deploy happens to precede the anomaly, especially in environments with frequent, concurrent deploys across many services. [Deploy-Correlated Anomaly Misattribution](failures/deploy-correlated-anomaly-misattribution.md) requires checking whether the deploy's actual diff touches the affected component before attributing cause.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Alert Fatigue from Threshold Misconfiguration](failures/alert-fatigue-from-threshold-misconfiguration.md) | Auto-tuning widens thresholds against recent noise with no recall floor, suppressing rare real incidents |
| [Correlation-Induced False Positives](failures/correlation-induced-false-positives.md) | Simultaneous correlated-metric spikes read as coordinated attack instead of single-root-cause cascade |
| [Deploy-Correlated Anomaly Misattribution](failures/deploy-correlated-anomaly-misattribution.md) | Anomaly attributed to the most recent deploy by timestamp proximity, not content relevance |
| [Multi-Agent Handoff Drops Baseline Adjustment Between Tuning Agent and Detection Agent](failures/multi-agent-handoff-drops-baseline-adjustment-between-tuning-agent-and-detection-agent.md) | Tuning agent's time-bound, event-specific adjustment reasoning never reaches the detection agent's structured threshold |
| [Seasonal Blindness](failures/seasonal-blindness.md) | Static statistical baseline flags predictable daily/weekly/seasonal variation as anomalous |

**Total: 5 patterns**

## Related Goals

- [Alert Routing](../alert-routing/) — once an anomaly correctly fires, routing determines whether it reaches the right responder
- [Monitoring](../monitoring/) — signal-collection failures (sampling, cardinality, silent metric gaps) that determine what data ever reaches the anomaly detector
- [Incident Response](../incident-response/) — root-cause and postmortem failures that occur after an anomaly has already been correctly detected and escalated
