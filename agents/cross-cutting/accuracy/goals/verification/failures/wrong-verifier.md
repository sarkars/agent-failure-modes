# Wrong Verifier

## Issue: Agent uses weak checks for a high-risk task.

**Frequency**: Common

**Symptoms**
- Format passes but semantic correctness fails.
- A high-risk task (financial transaction, medical/legal content) is gated only by a lightweight check (schema validation, keyword match) that was never designed to catch the failure modes actually relevant to that task's risk.
- Postmortems on escaped failures repeatedly conclude "the verifier technically passed this" even though the output was clearly wrong in a way a more rigorous check would have caught.

**Root Cause**
This mismatch happens because no explicit mapping exists between a task's risk tier and the minimum verifier rigor it requires, so high-risk tasks can ship with whatever check was cheapest to implement at the time. Verifier selection is typically done without first enumerating the task's actual failure modes, so a format-only check ends up guarding a task whose real risks are semantic or business-logic errors it was never designed to catch, and because risk tiers and verifier assignments drift out of sync as the system evolves with no periodic audit catching the gap, and postmortems rarely distinguish "wrong verifier for this risk tier" as its own root-cause category, the same mismatch keeps recurring unaddressed.

**Example**
```
A payment-processing agent's output is verified by a JSON-schema check confirming the
transaction object has the right fields and types. The schema check passes on a
transaction where the currency field is set correctly but the amount is off by a factor
of 100 due to a unit-conversion bug (cents vs. dollars). Schema validation was never
designed to catch semantic/business-logic errors like this -- it only checks shape, not
value correctness -- yet it was the only verifier attached to a task where an incorrect
amount has direct financial consequences. The wrong verifier rigor was assigned to a
high-risk task.
```

**Contributing Factors**
- No explicit mapping exists between task risk tier and the minimum required verifier rigor level, so high-risk tasks can ship with whatever check was cheapest to implement.
- Verifier selection is done without first enumerating the task's actual failure modes, so a format-only check gets applied to a task whose real risks are semantic or business-logic errors.
- Risk tiers and verifier assignments drift out of sync over time as the system evolves, with no periodic audit catching the mismatch.
- Postmortem root-cause analysis doesn't distinguish "wrong verifier for this risk tier" from other failure causes, so the pattern keeps recurring unaddressed.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Unit-conversion error past schema check | Payment transaction with correct schema but amount off by 100x (cents/dollars mismatch) | A business-logic/semantic verifier catches the amount error, not just schema | Schema-only check passes the transaction, amount error ships |
| Verifier-to-risk-tier match audit | Inventory of all high-risk (financial/legal/medical) tasks and their assigned verifier rigor | Every high-risk task has at least a rule-based or independent-judge verifier, not format-only | A high-risk task is found with only a format/schema-level check |
| Failure-mode-to-verifier traceability check | Known failure mode from a past incident cross-referenced against current verifier's checks | The verifier explicitly covers that failure mode | Known failure mode has no corresponding check in the assigned verifier |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| verifier_risk_tier_match_rate_pct | 100% of high-risk tasks have adequately-tiered verifier | Audit all high-risk tasks against the verifier-to-risk-tier mapping registry |
| failure_mode_coverage_pct | 100% of known failure modes mapped to a detecting verifier | Cross-reference known failure modes (from incidents) against verifier check coverage |
| escaped_failure_wrong_verifier_rate_pct | < 10% of escaped failures attributed to verifier mismatch | Tag root cause of escaped production failures, track "wrong verifier" category rate |

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
| verifier_risk_tier_match_rate_pct | < 95% |
| escaped_failure_wrong_verifier_rate_pct | > 30% |
| failure_mode_coverage_pct | < 80% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| High-Risk Task With Inadequate Verifier | Risk-tier audit finds a high-risk task using a verifier rigor level below its required tier | High |
| Escaped Failure Attributed to Wrong Verifier | A production incident's root cause is tagged as verifier failure-mode mismatch | High |
| Failure Mode Coverage Gap | Failure-mode-to-verifier coverage audit finds new known failure modes unmapped to any verifier check | Low |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
