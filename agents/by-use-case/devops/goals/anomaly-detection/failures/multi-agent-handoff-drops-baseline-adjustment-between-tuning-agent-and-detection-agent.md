# Multi-Agent Handoff Drops Baseline Adjustment Between Tuning Agent and Detection Agent

## Issue: A Tuning Agent That Determines, in Its Own Analysis, That an Anomaly-Detection Baseline Should Be Adjusted to Account for a Known, Scheduled Event -- Such as a Maintenance Window or a Planned Traffic-Shaping Change -- Hands Off to the Detection Agent Through a Structured Threshold Configuration That Carries Only the Numeric Threshold Value, Not the Time-Bound Adjustment Reasoning, So the Detection Agent Flags the Expected Deviation as an Anomaly

**Frequency**: Occasional

**Symptoms**
- A scheduled, one-off event (a planned traffic-shaping change, a maintenance window) causes a real, anticipated shift in a monitored metric, and the tuning agent's write-up says as much — but the config update it pushes to the detection agent's threshold store is a static bound change, not a dated exception
- The detection agent's evaluator reads the threshold config directly at alert-evaluation time; it has no step that cross-references the tuning agent's commit message or analysis notes before firing
- The on-call engineer triaging the resulting page finds, on inspecting the tuning agent's own analysis log after the fact, that the deviation was fully anticipated — the false positive wasn't a forecasting failure, it was a schema-expressiveness failure
- Because the threshold schema's only two shapes are a static value and a fixed cron-style seasonal pattern, every one-off exception is structurally unable to be expressed, so the same gap resurfaces for the next unrelated scheduled change too, not just this metric
- Once pushed, the relaxed static bound stays in effect indefinitely rather than reverting after the event window closes, so a later, unrelated deviation on that same metric can also go undetected

**Root Cause**
The threshold configuration schema connecting these two agents was designed around recurring, predictable variation — a static bound or a cron-style seasonal pattern (peak-hours vs. off-hours) — because that covers the overwhelming majority of legitimate baseline adjustments. It was never extended to express "relax this bound between these two timestamps, for this one occurrence," so when the tuning agent's reasoning is genuinely event-specific rather than a permanent recalibration, there is no field to write that reasoning into. The detection agent's evaluator consumes the threshold config directly at alert time and has no step that reads upstream analysis transcripts, so a conclusion the tuning agent reached correctly simply has no path to reach the component that needed it.

**Example**
```
Tuning agent reviews an upcoming planned traffic-shaping change to a CDN configuration, reasoning: "This change will cause a benign 40% drop in origin-server request volume for the affected route between 02:00 and 04:00 UTC on the change date; detection threshold for this metric should be relaxed for that window only"
Tuning agent updates the structured threshold configuration with a single new static lower-bound value, with no time-bound scope field to express that the relaxation applies only to the specified two-hour window
Detection agent applies the relaxed threshold permanently going forward, and separately, the actual drop during the change window triggers a different metric's anomaly detection that was never adjusted at all, since the tuning agent's reasoning addressed only the request-volume metric explicitly
On-call engineer is paged for the unadjusted metric's anomaly during the planned change window, and separately notices the request-volume threshold was relaxed indefinitely rather than only for the intended window
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Multi-agent LLM systems exhibit a documented failure category where a determination established by one agent is lost or never reaches a downstream agent's effective input, distinct from either agent reasoning incorrectly on its own | [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) |
| Generalist multi-agent system designs are shown to require explicit, structured task and constraint specification between agents, since narrative planning output alone does not reliably propagate to a downstream agent acting on a fixed schema | [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) |
| Studies of failure lifecycles in platform-orchestrated agentic workflows identify cross-agent state and scope loss between sequential configuration steps as a recurring driver of downstream false-positive and false-negative detection outcomes | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

**Contributing Factors**
- The threshold configuration schema supports static or seasonally patterned values, with no field for an ad hoc, time-bound exception tied to a specific scheduled event
- The detection agent's evaluation logic consults only the structured threshold configuration, never the tuning agent's planning transcript
- No reconciliation step compares adjustment scope and duration described in the tuning agent's analysis against what the structured configuration actually encodes before the adjustment takes effect

---

## Mitigation Strategies

1. **Time-Bound Adjustment Field in Threshold Schema**: Extend the threshold configuration schema to carry an explicit, structured start and end time for any ad hoc adjustment, and require the tuning agent to populate it directly from its own event-specific determination rather than applying a permanent static change
2. **Automatic Reversion After Adjustment Window**: Require any time-bound threshold adjustment to automatically revert to the prior baseline at its specified end time, rather than persisting indefinitely absent an explicit follow-up action
3. **Pre-Effect Adjustment-Scope Reconciliation Scan**: Before a threshold adjustment takes effect, automatically scan the tuning agent's analysis transcript for time-bound or event-specific scope language and flag any mismatch against the structured configuration's actual scope
4. **Cross-Metric Event Impact Checklist**: When a scheduled event is known to affect one metric's baseline, require the tuning agent to explicitly confirm or rule out impact on related metrics, rather than addressing only the metric its initial analysis happened to focus on

### Metrics
- Rate of threshold adjustments where the tuning agent's analysis transcript specifies a time-bound scope not reflected in the structured configuration
- Number of false-positive anomaly alerts occurring during known scheduled events with an intended but improperly scoped threshold adjustment
- Time between a scheduled event's conclusion and reversion of any associated threshold adjustment back to baseline

### Alerts
- An anomaly alert fires for a metric during a scheduled event window the tuning agent's analysis explicitly intended to adjust for → P2
- A time-bound threshold adjustment remains in effect past its intended end time with no reversion → P2
- Adjustment-scope reconciliation mismatch rate exceeds the defined threshold for a rolling window → P3

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657)
- [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
