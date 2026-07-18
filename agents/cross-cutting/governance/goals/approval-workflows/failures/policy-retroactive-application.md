# Policy Retroactive Application

## Issue
A policy is updated, and the new version is applied retroactively to actions the agent already took under the old policy — flagging past actions as non-compliant, requiring after-the-fact approval for things already executed, or reversing decisions that were entirely proper under the rules in effect at the time. This creates disputes about whether historical actions were compliant, since the agent (and the humans who approved its actions) were following the policy that actually existed when the action happened.

**Frequency**: Occasional

**Symptoms**
- Compliance reports flagging historical actions as violations based on a policy version that didn't exist when the action occurred
- Approvers being asked to re-justify or re-approve decisions they made correctly under a since-superseded policy
- No timestamp-anchored policy version recorded alongside historical approval decisions, making it impossible to determine which policy actually applied at execution time
- Disputes between compliance and operational teams over whether an old action was "actually" compliant
- Automated compliance scanners re-evaluating historical action logs against the current policy version by default, rather than the version active at the time

## Root Cause
Compliance and audit tooling frequently evaluates historical records against whatever policy version is currently active, because that's the only version readily available, rather than reconstructing the policy that was actually in effect at the time each action was taken. Without immutable, timestamped policy version records tied to each historical decision, there is no way to distinguish "this was non-compliant even at the time" from "this became non-compliant only because the policy changed afterward."

## Example
```
1. In January, a spend-approval policy allows agents to auto-approve
   purchases under $5,000 without human review.
2. Throughout January and February, an agent auto-approves dozens of
   purchases in the $2,000-$4,500 range, fully compliant with the policy
   in effect at the time.
3. In March, compliance tightens the policy: all purchases over $1,000 now
   require human approval, in response to an unrelated audit finding.
4. A compliance scanner runs in April, re-evaluating the full historical
   purchase log against the current (March) policy version rather than the
   version active when each purchase was made.
5. The January and February auto-approved purchases are flagged as policy
   violations, even though they were fully compliant when executed.
6. The operations team disputes the findings, but because no system stored
   which policy version was active at approval time, there's no clean
   record to settle the dispute definitively.
```

## Statistics
| Finding | Context |
|---------|---------|
| A notable share of compliance false-positive findings in policy audits trace back to evaluating historical actions against a current rather than time-appropriate policy version | Common pattern where audit tooling lacks policy version history |
| Organizations that store an immutable policy-version snapshot alongside each decision report substantially fewer retroactive-application disputes | Typical effect of timestamp-anchored policy versioning |
| Policy tightening events (versus loosening) are more frequently associated with retroactive-application disputes, since tightened rules are more likely to newly implicate past actions | Consistent with the asymmetric effect of stricter subsequent policy |

## Mitigations
1. **Immutable policy-version snapshot per decision**: Record the exact policy version (with a content hash or version ID, not just a date) that was active at the moment each approval decision or auto-approval occurred, stored alongside the decision itself.
2. **Time-anchored compliance evaluation**: When auditing historical actions, evaluate each action against the policy version that was actually in effect at its timestamp, not the currently active version, unless a policy change is explicitly designated as retroactive by governance.
3. **Explicit retroactivity flag on policy changes**: When a policy change is published, require an explicit, documented decision about whether it applies retroactively to past actions, defaulting to non-retroactive unless stated otherwise.
4. **Grandfathering process for newly non-compliant historical actions**: When a policy tightens and would newly implicate past compliant actions, establish a defined grandfathering or remediation process rather than treating those actions as violations after the fact.
5. **Policy change communication with effective-date clarity**: Clearly communicate the effective date of any policy change to all stakeholders and systems, ensuring the "as of" boundary is unambiguous for compliance reporting.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `retroactive_flag_rate` | Share of compliance findings against historical actions where the applicable policy version differs from the version active at execution time | > 0 (should be zero with correct time-anchored evaluation) |
| `undocumented_policy_version_decision_rate` | Share of historical approval decisions with no recorded policy-version snapshot | > 1% of decisions |
| `retroactivity_undeclared_change_count` | Number of policy changes published without an explicit retroactivity designation | > 0 per quarter |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Historical action flagged under a policy version not active at execution time | Compliance scan flags a past action using a policy version published after that action occurred | Critical | Discard the finding, re-run audit with time-anchored policy version, investigate scanner configuration |
| Policy change published without retroactivity designation | A new or updated policy goes live with no explicit statement of retroactive applicability | Warning | Block publication until governance confirms retroactivity stance |

## Related Patterns
- [Policy Version Mismatch](./policy-version-mismatch.md) - both stem from an agent or system evaluating against the wrong policy version relative to a point in time
- [Policy Temporal Violation](./policy-temporal-violation.md) - both involve policies being applied outside their intended, time-bounded scope of effect
- [Policy Consistency Violation](./policy-consistency-violation.md) - both involve ambiguity about which policy content actually governs a given decision
