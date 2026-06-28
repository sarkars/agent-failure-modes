# Alert Fatigue from Agent-Tuned Threshold Misconfiguration

## Issue: Agent Auto-Tunes Anomaly Detection Thresholds to Minimize False Positives on Historical Data, Inadvertently Suppressing Sensitivity to Genuinely Novel Incident Patterns

**Frequency**: Very Common

**Symptoms**
- Threshold auto-tuning agent widens bounds after a burst of false-positive alerts, then fails to narrow them back once the noisy period passes
- Genuinely anomalous metric movements that resemble a previously-whitelisted noisy pattern are silently suppressed
- On-call engineers report "the system used to catch this" after a tuning pass widened a threshold months earlier
- Threshold changes are applied automatically with no record of why a given threshold was set or when, making regression hard to diagnose

**Root Cause**
Threshold optimization agents are typically trained to minimize a single objective — false-positive rate against recent history — without an opposing constraint on false-negative rate against rare-but-real incident patterns, which are by definition underrepresented in recent history. Because real incidents are rare relative to noise, an agent optimizing purely against observed history will converge toward thresholds that suppress noise effectively but also suppress the rare true positives that look statistically similar to noise, and without versioned, auditable threshold history, this drift is invisible until a real incident is missed.

**Example**
```
Scenario: API error-rate anomaly detector
Initial threshold: Alert if error rate exceeds 2% for 5 minutes
Noisy period: Deploy-related transient spikes to 3% generate repeated false alerts
Auto-tuning agent: Widens threshold to 6% to suppress the false positives
Real incident weeks later: Error rate climbs to 4% due to a genuine downstream dependency failure
Result: No alert fired; threshold was tuned to tolerate noise that happened to resemble the real incident's magnitude
Impact: Delayed incident detection
```

**Key Statistics**
- Alert threshold drift from automated tuning without an opposing recall constraint is a recurring failure theme in AIOps literature on alert triage automation
- Alert fatigue from poorly calibrated thresholds is consistently cited as a primary driver of missed or delayed incident response in SRE practice surveys
- Agentic alert-triage systems evaluated in recent production case studies show meaningfully better precision-recall balance when threshold changes are constrained and auditable versus freely auto-tuned

---

## Mitigation Strategies

1. **Dual-Objective Tuning**: Constrain threshold auto-tuning to jointly optimize false-positive rate and a recall floor against a held-out set of known historical incident signatures, never false-positive rate alone
2. **Versioned, Auditable Threshold History**: Every threshold change is logged with timestamp, trigger reason, and rollback path, so drift can be diagnosed and reverted
3. **Asymmetric Widening Caution**: Require a higher confirmation bar (longer observation window, secondary approval) to widen a threshold than to narrow one, given the asymmetric cost of missed incidents vs. noisy alerts
4. **Periodic Threshold Re-Tightening Review**: Schedule recurring review of any threshold that was widened during a noisy period to confirm whether it should be re-tightened

### Metrics
- False-negative rate against a held-out historical incident signature set, tracked alongside false-positive rate
- Threshold change frequency and magnitude over time (drift tracking)
- Time-to-detection for incidents resembling previously-suppressed noise patterns

### Alerts
- Threshold widened beyond a defined bound without secondary approval → P2
- Recall against held-out incident signature set drops below target after a tuning pass → P1

---

## References

- [Agentic Observability: Automated Alert Triage for Adobe E-Commerce](https://arxiv.org/pdf/2602.02585)
- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
