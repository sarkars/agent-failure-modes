# Critical Lab Value Notification Delay

## Issue: Agent Summarizes a Critical Lab Result Within a Routine Note Instead of Triggering Immediate Notification

**Frequency**: Common

**Symptoms**
- Critical potassium, glucose, or hemoglobin value is mentioned in a generated chart summary but treated with the same priority as routine, in-range results
- Agent batches lab summarization with other note-drafting tasks, introducing latency between result availability and clinician awareness
- Critical value is correctly identified as "abnormal" but not flagged against the specific critical-value threshold that requires immediate callback
- No distinct, separately-routed alert generated for the critical result; it is only visible if the clinician reads the full note

**Root Cause**
Many LLM-based documentation and summarization agents treat lab values as one more data point to narrate within a larger note, rather than running every incoming lab result through a dedicated critical-value threshold check first. Without an explicit, prioritized, separately-triggered notification path, critical results inherit the same processing latency and visibility as routine documentation tasks, even though clinical protocols require immediate callback for values outside critical thresholds.

**Example**
```
Scenario: Potassium result returns at 6.8 mEq/L (critical high, arrhythmia risk)
Agent: Includes "K+ 6.8, elevated" within end-of-day note summarization batch
Notification: None separate from the note; clinician sees it only when reading the full note hours later
Protocol requirement: Critical value requires phone callback within 30 minutes of result
Impact: Delayed intervention for a potentially life-threatening value
```

**Key Statistics**
- Critical-value notification delay is a recurring root cause identified in laboratory patient-safety incident reviews
- Regulatory and accreditation standards typically require critical-value communication within a defined short window (often under an hour), independent of routine documentation timelines
- Automated, rule-based critical-value alerting (separate from narrative summarization) has been shown to substantially reduce notification delay compared to narrative-embedded reporting

---

## Mitigation Strategies

1. **Dedicated Critical-Value Gate**: Run every incoming lab result through a deterministic critical-threshold check before any narrative summarization occurs, independent of note-drafting workflows
2. **Separate Notification Channel**: Critical values trigger an immediate, separately-routed alert (page, call, dedicated portal flag) rather than being embedded only in note text
3. **Acknowledgment Tracking**: Require explicit clinician acknowledgment of critical-value alerts with a timestamp, and escalate if unacknowledged within the protocol window
4. **Latency Budget Enforcement**: Treat critical-value processing as latency-sensitive and exempt from any batching or queuing applied to routine documentation tasks

### Metrics
- Time from critical lab result availability to clinician notification
- % of critical values routed through the dedicated alert path vs. discovered only in narrative text
- Unacknowledged critical-value alert rate within protocol window

### Alerts
- Critical lab value not acknowledged within protocol window (e.g., 30 min) → P1
- Critical value detected only in narrative summary, no separate alert generated → P1

---

## References

- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
