# No Root-Cause Separation

## Issue: Agent treats symptom as cause: prompt vs retrieval vs tool vs policy.

**Frequency**: Common

**Symptoms**
- Repeated failures after superficial fix.
- Engineers reflexively edit the system prompt whenever any output looks wrong, even when the actual defect lives in a stale retrieval index, a tool returning malformed data, or a policy layer silently overriding the model's response.
- The same symptom signature (e.g., "agent gives outdated pricing") recurs across multiple "fixed" incidents, each time patched at a different layer than the one previously patched, because no one ever isolated which layer was actually at fault.

**Root Cause**
Without a layer-isolated reproduction harness, engineers can only observe the final output text, not which of the prompt, retrieval, tool, or policy layers actually produced it, so diagnosis defaults to inference rather than evidence. Editing the prompt is the fastest and lowest-friction change available, and incident-response time pressure rewards whichever fix closes the ticket quickest rather than the one that tests each layer in isolation. Because no failure-signature index links new incidents back to past ones, a defect that resurfaces at a different layer is triaged as a fresh, unrelated problem instead of being recognized as the same root cause the previous "fix" never actually touched.

**Example**
```
A customer support agent tells a user their order shipped from a warehouse that closed six months
ago. The on-call engineer, seeing only the final response text, assumes the prompt is telling the
model to guess a warehouse name and adds an instruction: "always say 'our fulfillment center' instead
of naming a specific warehouse." Two weeks later the same stale-fact pattern reappears with a
different field (an old return-policy window), because the actual defect was a retrieval index that
had not been reindexed after a warehouse-closure database migration -- a layer nobody isolated because
the fix was authored directly against the symptom text rather than by testing prompt, retrieval, and
tool layers independently.
```

**Contributing Factors**
- No layer-isolated reproduction harness exists, so engineers can only observe the final output, not which layer (prompt, retrieval, tool, policy) actually produced the defect.
- Prompt edits are the fastest, lowest-friction fix available, creating a bias to reach for a prompt change regardless of where the true defect lives.
- Time pressure to close an incident quickly discourages the slower work of isolation testing across layers.
- No failure-signature index links new incidents to past ones, so recurrence at a different layer isn't recognized as the same underlying symptom resurfacing.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Layer-swap isolation test | Failing case replayed with a known-good retrieval context substituted, prompt/tool unchanged | Output becomes correct, confirming retrieval (not prompt) was the root cause | Fix is authored against the prompt without ever running the layer-swap test |
| Recurrence-after-fix check | Previously "fixed" symptom signature re-injected 30 days after closure, at a different layer | Failure-signature index flags the match and reopens RCA before a new fix is authored | New incident is triaged as unrelated and independently patched at yet another layer |
| RCA evidence gate | Fix PR submitted with no linked isolation-test result | Review blocks the merge pending isolation evidence | Fix is merged on symptom description alone with no isolation evidence attached |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| root_cause_isolation_test_coverage_percent (eval) | 100% of sampled fixes have linked isolation evidence | Audit a sample of merged fixes for a linked layer-isolation test result |
| repeat_failure_rate_after_fix_percent (eval) | < 5% | Replay past "fixed" failure signatures against the current system and measure recurrence |
| root_cause_layer_distribution_skew (eval) | proportional to isolation-confirmed failure mix | Compare attributed root-cause layer distribution against isolation-test-confirmed ground truth on a sample set |

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
| repeat_failure_rate_after_fix_percent | > 15% |
| root_cause_isolation_test_coverage_percent | < 80% |
| root_cause_layer_distribution_skew | single layer > 70% of attributions without isolation evidence |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Recurrence After "Fixed" Incident | a failure signature matching a previously closed incident reappears within 30 days | High |
| Fix Merged Without Isolation Evidence | a fix PR lacks a linked isolation-test result in its RCA record | Medium |
| Triage Bias Detected | root-cause layer distribution skews heavily to one layer without isolation-test support | Low |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
