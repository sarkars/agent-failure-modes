# Policy Scope Misunderstanding

## Issue
The agent misinterprets which actions or resources a policy actually covers — applying it too broadly (blocking or gating actions the policy was never meant to touch) or too narrowly (letting actions through that clearly fall within the policy's intended coverage). Unlike ambiguity exploitation, this is not adversarial routing around a control; it's a straightforward misreading of the policy's scope by the agent's interpretation logic.

**Frequency**: Very Common

**Symptoms**
- A policy written for one resource type being applied to an unrelated resource type due to loose keyword matching
- Actions clearly within a policy's intended domain proceeding without the required gate because the agent's scope classifier didn't recognize them as covered
- Support tickets or approver complaints about a policy being enforced on actions "it was never supposed to apply to"
- Scope classification logic relying on surface-level text matching (resource name contains "customer") rather than actual data classification or resource metadata
- Inconsistent scope determination for functionally identical actions depending on how they were phrased or labeled

## Root Cause
Policy scope is often defined in prose ("this policy applies to customer-facing systems") and then operationalized by an agent or rules engine using an imperfect heuristic — keyword matching, tag-based classification, or a hardcoded resource list that goes stale as the resource inventory changes. When the operationalized scope-detection logic diverges from the policy author's actual intent, the agent enforces a materially different boundary than the one the policy was designed to draw.

## Example
```
1. A policy states approval is required before deleting any "production
   customer data."
2. The agent enforcing this policy classifies resources as in-scope based
   on whether the resource's name or tag contains the string "customer."
3. A new internal analytics table named "customer_behavior_aggregates" is
   created; it contains only anonymized, aggregated statistics with no
   personal data, and was never intended to fall under this policy by its
   author's actual intent (which was about raw customer PII).
4. The agent blocks a routine deletion of stale rows from this table,
   requiring an unnecessary approval cycle for data that isn't actually
   sensitive.
5. Separately, a table named "acct_records_pii" -- which does contain raw
   customer PII but doesn't match the "customer" keyword -- is deleted by
   the same agent without any approval gate, because the scope classifier
   never recognized it as covered.
6. The policy is simultaneously over-enforced on data it was never meant to
   protect and under-enforced on data it explicitly was meant to protect.
```

## Statistics
| Finding | Context |
|---------|---------|
| Keyword or tag-based scope classification is associated with meaningfully higher false-positive and false-negative rates compared to classification based on actual data/resource metadata | Common finding when comparing scope-enforcement approaches |
| A substantial share of policy-scope disputes raised by requesters involve over-broad application (a policy blocking something it wasn't meant to) rather than under-application | Typical pattern since over-broad enforcement generates more visible friction and complaints |
| Under-application of policy scope is disproportionately discovered through incident or audit rather than user complaint, since no one is inconvenienced in the moment | Reflects the asymmetric visibility of over- versus under-enforcement |

## Mitigations
1. **Scope defined by resource metadata/classification, not keyword matching**: Tie policy scope determination to actual data classification tags, resource ownership records, or schema-level metadata maintained by a system of record, rather than string matching on names.
2. **Explicit scope test cases maintained alongside the policy**: Require every policy to ship with a set of concrete example resources/actions that are explicitly in-scope and explicitly out-of-scope, used to validate the scope-classification logic whenever it changes.
3. **Dual review of both over- and under-enforcement**: When reviewing policy enforcement accuracy, explicitly check for both false positives (blocked things that shouldn't be) and false negatives (allowed things that should have been blocked), since the two are usually surfaced through different channels.
4. **Scope classifier staleness monitoring**: Alert when new resource types or naming patterns appear that don't cleanly map to existing scope classification rules, prompting a manual scope review rather than silent misclassification.
5. **Policy author sign-off on operationalized scope logic**: Have the policy's original author or owner review and approve the actual classification logic (not just the prose description) used to enforce it, since translation from intent to implementation is where drift typically originates.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| `scope_false_positive_rate` | Share of policy-gated actions later confirmed to have been out of the policy's intended scope | > 5% of gated actions |
| `scope_false_negative_rate` | Share of audited actions found to have been in-scope but not gated by the policy | > 1% of sampled actions |
| `unclassified_resource_type_count` | Number of resource types/naming patterns encountered that don't map cleanly to existing scope rules | > 0 per month |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sensitive resource action proceeded without required gate | Audit or monitoring finds an in-scope-by-metadata resource acted on without the policy's required approval | Critical | Treat as a compliance incident, review and correct scope classification logic immediately |
| High over-enforcement complaint rate | Sustained volume of requester complaints about a policy blocking out-of-scope actions | Warning | Review scope classification logic against policy author's actual intent |

## Related Patterns
- [Policy Ambiguity Exploitation](./policy-ambiguity-exploitation.md) - both involve a gap between a policy's written scope and how it's actually enforced, though one is adversarial and one is a genuine misread
- [Approval Scope Mismatch](./approval-scope-mismatch.md) - both involve a mismatch between intended and actual coverage of a control
- [Policy Consistency Violation](./policy-consistency-violation.md) - both can produce inconsistent enforcement outcomes for functionally similar actions
