# No Root-Cause Separation

## Issue: Agent treats symptom as cause: prompt vs retrieval vs tool vs policy.

**Frequency**: Common

**Symptoms**
- Repeated failures after superficial fix.
- [Add more specific symptoms]

**Root Cause**
Agent treats symptom as cause: prompt vs retrieval vs tool vs policy.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Failure Triage Taxonomy**: Use a structured decision tree that forces explicit classification of every incident into one of the candidate layers (prompt, retrieval, tool, policy, data) with documented evidence for the choice, before anyone is allowed to propose a fix, preventing the reflexive "just edit the prompt" response.
2. **Layer-Isolated Reproduction Harness**: Replay the failing case with each layer independently mocked or swapped (e.g., feed the exact retrieved context that should have been returned, bypass the tool call with a known-good response) to empirically confirm which layer actually produces the wrong output, rather than inferring it from the symptom alone.
3. **RCA Sign-off Requirement**: Block fix authorship until the isolation harness has confirmed a specific root-cause layer and that finding is recorded in an RCA document; a fix proposal that doesn't cite isolation-test evidence is rejected at review.

### Detection & Response
1. **Repeat-Failure Clustering**: Cluster new failures against a fingerprint index of past incidents by symptom signature; a new failure matching an already "fixed" cluster is strong evidence the earlier fix targeted the wrong layer.
2. **Fix Efficacy Verification**: After any fix ships, automatically re-run the original failing case plus the broader regression set; if the original case still fails, the fix is rejected and the RCA is reopened rather than the fix being considered complete because code was merged.
3. **Root-Cause Layer Distribution Monitoring**: Track what fraction of incidents get attributed to each layer over time; a distribution that skews heavily toward one layer (e.g., "always the prompt") independent of the actual failure mix is a signal of triage bias, not genuine root-cause diversity.

### Architecture Patterns
1. **Layer Isolation Test Harness**: Mockable boundaries between prompt, retrieval, tool-call, and policy layers that let engineers binary-search which layer, when swapped for a known-good version, makes the failure disappear.
2. **RCA Workflow Service**: A structured pipeline (incident -> hypothesis -> isolation test -> confirmed root cause -> fix) with mandatory stage gates, so no fix can be merged without passing through documented isolation testing.
3. **Failure Signature Index**: An embeddings- or fingerprint-based index of past incidents (input, symptom, confirmed root-cause layer) used both for clustering new failures against old ones and for detecting recurrence after a fix was believed to resolve the issue.

### Metrics
1. **repeat_failure_rate_after_fix_percent**: Target: < 5%; Alert threshold: > 15%
2. **root_cause_isolation_test_coverage_percent**: Target: 100% of fixes have linked isolation evidence; Alert threshold: < 80%
3. **mean_time_to_confirmed_root_cause**: Target: within team SLA (e.g., < 2 days); Alert threshold: exceeds SLA by 2x
4. **root_cause_layer_distribution_skew**: Target: proportional to actual failure mix (tracked via isolation tests); Alert threshold: single layer > 70% of attributions without isolation evidence

### Alerts
1. **Recurrence After "Fixed" Incident** (P1 - Critical): Condition - a failure signature matching a previously closed incident reappears within 30 days. Action: Reopen RCA, escalate to isolation testing before any new fix is authored, flag original fix as likely wrong-target.
2. **Fix Merged Without Isolation Evidence** (P2 - Warning): Condition - a fix PR lacks a linked isolation-test result in its RCA record. Action: Block merge until isolation evidence is attached, or require documented exception sign-off.
3. **Triage Bias Detected** (P3 - Info): Condition - root-cause layer distribution skews heavily to one layer without isolation-test support. Action: Audit recent RCAs for shortcut diagnoses, retrain team on isolation harness usage.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
