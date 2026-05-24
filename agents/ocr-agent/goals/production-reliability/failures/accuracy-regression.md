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

**Mitigation Strategies**
1. **Continuous accuracy monitoring**: Sample and verify against ground truth
2. **Canary deployments**: Roll out changes gradually with accuracy comparison
3. **Automated regression tests**: Run test suite on every deployment
4. **Business metric correlation**: Track downstream metrics (disputes, corrections)

## References

- [Braintrust: Agent Observability Guide 2026](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Accuracy monitoring
- [LinkedIn: Silent Failures of Production AI](https://www.linkedin.com/pulse/silent-failures-production-ai-why-most-llm-monitoring-praveen-juyal-iqgyc) - Regression detection gaps
- [Evaluating Multimodal LLMs for Production](https://galileo.ai/blog/multimodal-llm-guide-evaluation) - Continuous evaluation
