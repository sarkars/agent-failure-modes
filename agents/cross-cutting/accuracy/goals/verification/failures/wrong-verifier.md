# Wrong Verifier

## Issue: Agent uses weak checks for a high-risk task.

**Frequency**: Common

**Symptoms**
- Format passes but semantic correctness fails.
- [Add more specific symptoms]

**Root Cause**
Agent uses weak checks for a high-risk task.

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
1. **Verifier-to-Risk-Tier Mapping**: Explicitly map each task/action type to a minimum required verifier rigor level (format check < rule-based semantic check < independent model judge < human review) based on risk tier, and enforce that high-risk tasks cannot ship with only a low-rigor verifier attached.
2. **Failure-Mode-Driven Verifier Selection**: Before selecting a verifier, enumerate the actual failure modes for the task (not just "is it well-formed") and choose/build a verifier that specifically targets those failure modes — a format checker cannot catch a semantic or business-logic failure by construction.
3. **Verifier Adequacy Review in Design/Change Process**: Any new task or verifier change goes through an explicit review step asking "does this verifier actually detect the failure modes we care about for this risk tier," documented and signed off, rather than defaulting to whatever check is cheapest to implement.

### Detection & Response
1. **Verifier Coverage Gap Analysis**: Periodically cross-reference the list of known failure modes (from incident postmortems, production errors) for a task against what the current verifier actually checks; flag tasks where confirmed failure modes fall outside the verifier's detection capability.
2. **Escaped-Failure Root Cause Tagging**: When a production failure escapes to a customer despite passing verification, explicitly tag whether the root cause was "verifier didn't check for this failure mode" (wrong verifier) versus other causes, tracking this category's frequency over time.
3. **Risk-Tier Audit of Deployed Verifiers**: Periodically audit all high-risk tasks in production and confirm each has a verifier rigor level matching its current risk-tier mapping, since risk tiers and verifier assignments can drift out of sync as the system evolves.

### Architecture Patterns
1. **Tiered Verifier Registry**: A central registry maps task/action types to required verifier rigor level and the specific verifier implementation currently assigned, with CI checks blocking deployment of a high-risk task lacking an adequately-tiered verifier.
2. **Failure-Mode-to-Verifier Traceability Matrix**: Maintained documentation/tooling links each known failure mode for a task to the specific verifier check that would catch it, making coverage gaps (failure modes with no corresponding check) visible and auditable.
3. **Escalating Verifier Chain for High-Risk Actions**: High-risk actions pass through multiple verifier layers in sequence (format -> semantic/business rule -> independent model or human judge), with each layer targeting failure modes the previous layer cannot catch, rather than relying on a single verifier of any one type.

### Metrics
1. **verifier_risk_tier_match_rate_pct**: Target: 100% of high-risk tasks have adequately-tiered verifier; Alert threshold: < 95%
2. **escaped_failure_wrong_verifier_rate_pct**: Target: < 10% of escaped failures attributed to verifier mismatch; Alert threshold: > 30%
3. **failure_mode_coverage_pct**: Target: 100% of known failure modes mapped to a detecting verifier; Alert threshold: < 80%
4. **verifier_adequacy_review_completion_pct**: Target: 100% of new/changed tasks reviewed; Alert threshold: < 90%

### Alerts
1. **High-Risk Task With Inadequate Verifier** (P1 - Critical): Condition - risk-tier audit finds a high-risk task using a verifier rigor level below its required tier (e.g., format-only check on a financial action). Action: Block further automation on that task pending verifier upgrade, retroactive review of recent outputs.
2. **Escaped Failure Attributed to Wrong Verifier** (P1 - Critical): Condition - a production incident's root cause is tagged as verifier failure-mode mismatch. Action: Immediate verifier upgrade for the affected task, add the missed failure mode to the traceability matrix and eval suite.
3. **Failure Mode Coverage Gap** (P3 - Info): Condition - failure-mode-to-verifier coverage audit finds new known failure modes unmapped to any verifier check. Action: Schedule verifier enhancement, update traceability matrix.

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

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
