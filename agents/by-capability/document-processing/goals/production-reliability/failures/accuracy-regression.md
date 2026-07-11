# Accuracy Regression

## Issue: Accuracy Regression Undetected

**Frequency**: Occasional

**Symptoms**
- Model or pipeline update degrades accuracy
- No automated detection of regression
- Discovered weeks later through business impact

**Root Cause**
Production monitoring focuses on availability and throughput, not extraction accuracy. Accuracy degradation is a silent failure.

**Example**
```
v1.0 accuracy: 97%
v1.1 deployed: Contains subtle regression
v1.1 accuracy: 91%
Detection: 3 weeks later via increased customer complaints

Result: Thousands of documents processed with degraded accuracy
```

## Mitigation Strategies

### Prevention
1. **Mandatory pre-deployment regression test suite**: Maintain a versioned, labeled ground-truth test set covering all supported document types and run full accuracy evaluation against it as a hard gate before any model, prompt, or pipeline change is deployed — a change that regresses accuracy on this suite should never ship, not just be flagged for review after the fact. Trade-off: requires ongoing investment to keep the ground-truth set representative as document mix evolves.
2. **Canary deployment with accuracy comparison, not just error-rate comparison**: Roll out changes to a small percentage of production traffic and compare extraction accuracy (via sampled ground-truth verification) between canary and control cohorts before full rollout, since standard canary metrics (latency, error rate, throughput) will not catch an accuracy regression that produces well-formed but wrong output. Trade-off: requires ground-truth verification capability to run continuously on live traffic, not just at test time.
3. **Version-pinned rollback capability**: Ensure every deployed model/pipeline version can be rolled back within minutes, and treat rollback as the default first response to a suspected accuracy regression rather than attempting to patch forward, since diagnosing root cause under production pressure is slower and riskier than reverting to a known-good state. Trade-off: requires maintaining backward-compatible infrastructure for at least the previous version.

### Detection & Response
1. **Continuous ground-truth sampling in production**: Route a small, statistically meaningful percentage of live production documents through human verification continuously (not just during test/canary phases), so accuracy is measured as an ongoing production metric with the same rigor as latency or uptime.
2. **Business-metric correlation as a secondary signal**: Track downstream business metrics (payment disputes, manual corrections, reconciliation failures) segmented by pipeline version/deployment date, since these lag indicators can surface regressions the primary ground-truth sampling missed, especially for rare document subtypes underrepresented in the sample.
3. **Automatic alerting on accuracy metric deviation, not just absolute threshold**: Alert not only when accuracy falls below an absolute floor, but also on statistically significant deviation from the pre-deployment baseline for the same document type, since a regression from 97% to 91% may still be "acceptable" by an absolute threshold while representing a real and costly regression.

### Architecture Patterns
1. **Shadow/canary evaluation pipeline running in parallel with production**: Architect a parallel evaluation path that runs ground-truth-verified samples through both the current production version and any candidate version simultaneously, generating an accuracy comparison before the candidate is promoted, rather than evaluating only in an offline test environment disconnected from live traffic characteristics.
2. **Versioned accuracy dashboards tied to deployment history**: Track accuracy metrics explicitly annotated with deployment version and timestamp so any regression can be immediately correlated to the change that caused it, cutting diagnosis time from weeks to hours.
3. **Automatic rollback triggers**: Wire accuracy-monitoring alerts directly to automatic rollback triggers for severe regressions (not just human-paged alerts), given how much low-quality data can accumulate during a multi-week detection lag.

### Metrics
1. **production_sampled_accuracy**: Target: within 2 percentage points of pre-deployment baseline per document type; Alert if drop exceeds 4 points
2. **regression_test_pass_rate**: Target: 100% required to deploy; Alert/block deployment on any failure
3. **time_to_regression_detection**: Target: < 24 hours from deployment; Alert if detection exceeds 72 hours (signals sampling volume/frequency needs increasing)
4. **downstream_business_metric_deviation**: Target: < 10% deviation in disputes/corrections rate correlated with a deployment; Alert if > 25%

### Alerts
1. **Production Accuracy Drop** (P1): Condition - sampled production accuracy for a document type drops more than 4 percentage points versus pre-deployment baseline. Action: Trigger automatic rollback to the prior version, page on-call, hold the candidate version pending root-cause analysis.
2. **Regression Test Failure** (P1): Condition - any deployment candidate fails the accuracy regression test suite. Action: Block deployment; do not allow manual override without documented sign-off from a second reviewer.
3. **Detection Lag Alert** (P2): Condition - time from deployment to accuracy-regression detection exceeds 72 hours. Action: Increase production ground-truth sampling rate/frequency; review whether the ground-truth set adequately represents current document mix.

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Accuracy monitoring
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Regression detection gaps
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Continuous evaluation
