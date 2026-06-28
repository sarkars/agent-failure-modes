# Multi-Agent Handoff Drops Baseline Adjustment Between Tuning Agent and Detection Agent

## Issue: A Tuning Agent That Determines, in Its Own Analysis, That an Anomaly-Detection Baseline Should Be Adjusted to Account for a Known, Scheduled Event -- Such as a Maintenance Window or a Planned Traffic-Shaping Change -- Hands Off to the Detection Agent Through a Structured Threshold Configuration That Carries Only the Numeric Threshold Value, Not the Time-Bound Adjustment Reasoning, So the Detection Agent Flags the Expected Deviation as an Anomaly

**Frequency**: Occasional

**Symptoms**
- The tuning agent's analysis explicitly identifies a scheduled event that will cause an expected, benign deviation from the normal baseline and recommends a time-bound threshold adjustment, but the structured configuration it hands off contains only a static threshold value with no time-bound scope
- The detection agent, which evaluates incoming metrics solely against the structured threshold configuration, flags the expected deviation as an anomaly during the scheduled event, generating a false-positive alert
- Re-reading the tuning agent's analysis transcript clearly shows the time-bound adjustment was identified and reasoned through; it simply never reached a structured field the detection agent reads
- The gap concentrates on adjustments tied to irregular or one-off scheduled events, since the threshold configuration schema supports only a static value or a fixed seasonal pattern, not an ad hoc, dated exception
- The false-positive alert is investigated and dismissed as expected noise only after on-call review, by which point the alert has already consumed response attention

**Root Cause**
The tuning agent and the detection agent communicate through a structured threshold configuration schema that represents the detection boundary as a static or seasonally patterned value, with no field for an ad hoc, time-bound adjustment tied to a specific scheduled event. When the tuning agent's adjustment reasoning is event-specific rather than a permanent recalibration, it exists only in the tuning agent's narrative analysis and is invisible to the detection agent's threshold-driven evaluation, which has no mechanism to discover a reasoning step it never receives.

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
