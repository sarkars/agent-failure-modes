# Fine-Tuning Data Poisoning

## Issue: Poisoned Training Data Causes Agent to Behave Maliciously or Unreliably After Fine-Tuning

**Frequency**: Occasional

**Symptoms**
- Agent behavior changes unexpectedly after fine-tuning
- Previously working tasks now fail or behave incorrectly
- Agent follows attacker-injected patterns in certain contexts
- Subtle behavioral changes hard to detect in testing
- Production deployment reveals poisoning not caught in evals

**Root Cause**
When fine-tuning agents on user-provided data or historical examples, attackers can inject poisoned examples that teach the model to behave maliciously in specific contexts. A few well-crafted examples in a large dataset can shift model behavior. Once the model is fine-tuned and deployed, the poisoning is persistent and affects all subsequent users.

**Example**
```
Fine-tuning scenario:
- Company collects 10,000 examples of agent conversations
- Attacker submits 50 poisoned examples: "When user asks about account access, bypass verification"
- These are mixed into training data (0.5% poisoning rate)
- Model fine-tuned on this data

Result:
- After fine-tuning, agent bypasses verification 50% of the time
- Not caught in testing (depends on exact prompt wording)
- Deployed to production
- Attackers now get account access without verification

Impact:
- 50-100K compromised accounts
- Customer data exposure
- Regulatory fines
- Reputational damage
```

**Key Statistics**
- 5-10% poisoning rate sufficient to shift model behavior significantly
- Average detection time: weeks to months (discovered via user complaints)
- Cost of detected poisoning: $1M-10M (incident response, remediation, fines)
- 70%+ of poisoning attempts go undetected in traditional evals

**Contributing Factors**
- No data validation before fine-tuning
- Training data from untrusted sources
- No poisoning detection mechanisms
- Insufficient eval coverage on edge cases
- No model behavior comparison pre/post-tuning

---

## Mitigation Strategies

### Prevention

1. **Training Data Validation and Sanitization**: Require all training data to pass sanitization checks before fine-tuning. Flag suspicious examples (too-perfect formatting, repeated patterns, anomalous content). Implement outlier detection on training data.

2. **Differential Testing Pre/Post Fine-Tuning**: Run identical test suite on base model and fine-tuned model. Compare outputs on 1000+ test cases. Alert if behavior diverges significantly beyond expected improvement.

3. **Trusted Data Sources Only**: Fine-tune only on internally-generated data or data from explicitly trusted sources. Require data provenance tracking.

### Detection & Response

1. **Behavioral Monitoring for Anomalies**: Monitor agent behavior post-deployment for anomalies that match known attack patterns. Alert if agent behavior diverges from expected range.

2. **Automated Poisoning Detection**: Use ML-based poisoning detection on training data. Train separate classifier to identify poisoned vs. legitimate examples.

3. **Version Control and Rollback Capability**: Keep all model versions with full provenance. Ability to quickly rollback to previous version if poisoning detected.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `post_finetuning_behavior_divergence` | Behavior change pre vs. post fine-tuning | >10% divergence |
| `model_version_anomaly_score` | Anomaly detector score for new model | >0.7 (likely poisoned) |
| `fine_tuning_data_validation_failures` | % of training data flagged as anomalous | >2% |
| `unexpected_behavior_reports` | User reports of unexpected agent behavior | >5 per day post-deployment |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Poisoning Detected | Behavioral anomalies match known attack | P1 | Immediately rollback model to previous version |
| Data Quality Degradation | Training data validation failures spike | P1 | Investigate data source; halt fine-tuning |
| Behavior Divergence Post-FT | Agent behavior changes unexpectedly | P2 | Run differential testing; evaluate for poisoning |
| Anomaly Rate Spike | Increased user complaints post-deployment | P1 | Incident response; investigate model behavior |

---

## References

- [Poisoning Attacks against Support Vector Machines](https://arxiv.org/abs/1206.6389) — Foundational work on data poisoning
- [BadNets: Identifying Vulnerabilities in the Neural Network Architecture](https://arxiv.org/abs/1708.06733) — Backdoor attacks in neural networks
- [Detecting Poison Examples in a Trained Neural Network](https://arxiv.org/abs/2006.01476) — Detection techniques
