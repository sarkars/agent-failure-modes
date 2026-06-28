# Deploy-Correlated Anomaly Misattribution

## Issue: Anomaly-Detection Agent Attributes a Metric Anomaly to the Most Recent Deployment by Default, Missing the Actual Independent Cause

**Frequency**: Common

**Symptoms**
- Agent flags the most recently deployed change as the probable cause of an anomaly whenever a deploy occurred shortly before the anomaly, regardless of whether the deploy's content has any plausible connection to the affected metric
- Engineers spend time rolling back or investigating an unrelated recent deploy while the actual cause (a third-party dependency outage, a traffic pattern shift, a scheduled batch job) continues unaddressed
- Anomaly-detection confidence in deploy-correlation is not adjusted based on whether the deployed change actually touches the code path or infrastructure component associated with the anomalous metric
- Rollback of the flagged deploy does not resolve the anomaly, but is only discovered after the rollback completes and the anomaly persists
- Multiple anomalies occurring in different parts of the system around the same time, all coincidentally near a deploy, are all attributed to that deploy by correlation despite having unrelated root causes

**Root Cause**
Correlating an anomaly with the most temporally recent deployment is a low-cost, high-recall heuristic that is easy to implement using deployment timestamps and anomaly timestamps alone. This heuristic does not require understanding what the deployment actually changed, so it cannot distinguish a deploy that plausibly affects the anomalous metric from one that is entirely unrelated. Without content-aware correlation — checking whether the deployed diff touches the service, code path, or infrastructure component associated with the metric — temporal proximity alone produces a high rate of plausible-looking but incorrect attributions, especially in environments with frequent deploys across many services.

**Example**
```
Anomaly: Elevated error rate on the payments-api service
Recent deploys (within the correlation window): A deploy to payments-api (minor logging change) AND a deploy to an unrelated recommendations-service
Anomaly-detection agent: Flags the payments-api deploy as probable cause based on service-name match, but does not check that the deploy only added logging and could not plausibly cause errors
Actual cause: A downstream third-party payment processor began intermittently timing out, unrelated to either deploy
Investigation: Engineers roll back the payments-api logging deploy; error rate continues unchanged
Impact: Time lost rolling back an unrelated change, real cause investigation delayed
```

**Key Statistics**
- Root-cause misattribution in postmortems is identified as a recurring failure category in AIOps research, with deploy-correlation-by-temporal-proximity specifically called out as a heuristic prone to false positives in environments with high deploy frequency
- Correlation-aware anomaly detection research distinguishes content-aware causal correlation from naive temporal correlation, showing materially lower false-positive attribution rates when deploy diffs are actually analyzed for relevance to the affected component
- Environments with multiple concurrent deploys across services show a higher rate of spurious deploy-anomaly correlation than environments with infrequent, isolated deploys, simply due to the higher chance of coincidental timing

---

## Mitigation Strategies

1. **Content-Aware Correlation**: Check whether a candidate deploy's actual diff touches the code path, configuration, or infrastructure component associated with the anomalous metric before attributing causation, not just whether it occurred within a time window
2. **Multiple-Candidate Ranking**: When multiple deploys or external events occurred within the correlation window, rank all candidates by content-relevance rather than defaulting to the most recent or service-name-matching one
3. **External-Dependency Health Cross-Check**: Include third-party/external dependency health signals in the candidate-cause analysis, not just internal deploys, since externally-caused anomalies are common and easily missed by deploy-only correlation
4. **Rollback-Outcome Feedback Loop**: When a flagged deploy is rolled back as a mitigation attempt, track whether the anomaly actually resolves, and feed this back into the correlation model's confidence calibration for similar future attributions

### Metrics
- Rate of deploy-attributed anomalies where rollback failed to resolve the anomaly (false-attribution rate)
- Time spent investigating/rolling back incorrectly attributed deploys per incident
- Correlation confidence score distribution for content-aware vs. temporal-only attribution

### Alerts
- A rollback performed based on deploy-correlation attribution does not resolve the anomaly within a defined window → P2
- An anomaly is attributed to a deploy whose diff does not touch the affected component → P3

---

## References

- [Correlation-Aware Anomaly Detection](https://arxiv.org/abs/2012.08844)
- [Root Cause Analysis in Monitoring](https://arxiv.org/abs/1906.04905)
