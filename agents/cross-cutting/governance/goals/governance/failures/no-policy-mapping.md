# No Policy Mapping

## Issue: Agent behavior not mapped to company/regulatory policies.

**Frequency**: Common

**Symptoms**
- Compliance review cannot trace control coverage.
- A regulatory audit asks "which control satisfies obligation X" and no one can answer without a multi-week manual investigation.
- A new agent capability launches and later turns out to violate a data-handling policy that was never checked against it.
- Compliance and engineering disagree about whether a given control is "covered," because no shared source of truth exists.

**Root Cause**
Agent behavior not mapped to company/regulatory policies.

**Example**
```
A healthcare intake agent is expanded to summarize patient-reported
symptoms into structured notes for clinicians. The team ships the
feature because it passes functional testing; no one checks it against
HIPAA minimum-necessary or data-handling obligations, because no
policy-to-control matrix exists to consult.

Six months later, a compliance audit asks the engineering team to
demonstrate which technical controls enforce minimum-necessary access to
the summarized notes. No one can produce a mapping — the feature was
never registered against any policy obligation in the first place.

The audit finding requires a retroactive control review and a temporary
feature freeze while the mapping gap is closed, delaying an unrelated
product launch that depended on the same compliance sign-off.
```

**Contributing Factors**
- New agent capabilities ship based on functional testing alone, with no policy-obligation checklist as part of launch review.
- The set of applicable policies/regulations is not centrally tracked, so teams may not know which obligations even apply to a given feature.
- No control matrix exists linking each policy to the specific technical control that satisfies it, so compliance coverage can't be verified without manual investigation.
- Regulatory changes are tracked by legal but not systematically propagated to engineering as new control requirements.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Launch review policy check | A new capability going through launch review | Reviewer confirms applicable policies are mapped to implemented controls | Capability launches with no policy mapping recorded |
| Control-to-policy traceability query | Compliance queries "which control implements policy X" | Query returns a specific control with implementing component | Query cannot be answered without manual investigation |
| Regulatory change propagation | A tracked regulatory change affecting an existing capability | Control matrix is updated within 30 days | Regulatory change has no corresponding matrix update after 30+ days |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| launch_review_policy_check_rate | 100% | Audit a sample of recently launched capabilities for a recorded policy mapping |
| control_traceability_query_success_rate | 100% | Run sample compliance queries against the registry and confirm all resolve without manual lookup |
| regulatory_change_propagation_time | < 30 days | Track time from regulatory change identification to control matrix update |

---

## Mitigation Strategies

### Prevention
1. **Policy-to-Behavior Control Matrix**: Build and maintain an explicit mapping from each applicable policy/regulation (internal data handling policy, GDPR, sector-specific regulation) to the specific agent controls that implement it (e.g., "PII minimization policy" maps to the redaction proxy and retention TTL controls). No agent capability ships without an entry showing which policy obligations it satisfies or which are not yet covered.
2. **Policy Coverage Gate at Launch Review**: Require new agent capabilities or expanded scopes to pass a launch review checklist confirming every applicable policy has a corresponding control in the matrix, with explicit sign-off from legal/compliance for any gap accepted as a known risk.
3. **Regulatory Change Intake Process**: Establish a process where legal/compliance changes (new regulation, updated internal policy) trigger a review of the control matrix to identify newly uncovered obligations, rather than the mapping going stale as the regulatory landscape shifts.

### Detection & Response
1. **Control Coverage Audit**: Periodically run an audit comparing the current policy matrix against the agent's actual deployed capabilities, flagging any capability with no mapped policy control or any policy with no corresponding implemented control.
2. **Compliance Traceability Query Tool**: Provide compliance reviewers self-service tooling to query "which control implements policy X" and "which policies does capability Y satisfy," so gaps surface during routine review instead of only during an audit or incident.
3. **Unmapped Behavior Detection**: Monitor production agent behavior for actions or capabilities that exist in the runtime but have no entry in the policy matrix (indicating the matrix wasn't updated when the capability was added), and flag these as compliance debt.

### Architecture Patterns
1. **Policy Control Registry**: Maintain a structured, versioned registry (e.g., a compliance-as-code repository) mapping policy_id → control_id → implementing_component → verification_evidence, queryable by both engineering and compliance teams.
2. **Compliance Review Integration in CI/CD**: Wire a check into the deployment pipeline that blocks shipping a new agent capability unless it references an entry in the policy control registry (or an explicit waiver signed by compliance).
3. **Automated Evidence Collection**: Link each control in the registry to automated evidence (audit log queries, config snapshots, test results) that demonstrates the control is actually operating, so compliance reviews are backed by live evidence rather than a static document.

### Metrics
1. **policy_coverage_percent**: Target: 100% of applicable policies mapped to a control; Alert threshold: < 95%
2. **unmapped_capability_count**: Target: 0; Alert threshold: > 0 deployed capabilities without a policy mapping
3. **control_matrix_staleness_days**: Target: reviewed within 30 days of any regulatory/policy change; Alert threshold: > 90 days since last review
4. **compliance_gap_waivers_open**: Target: tracked and time-boxed; Alert threshold: any waiver open past its expiry

### Alerts
1. **Unmapped Capability Deployed** (P1 - Critical): Condition - agent capability shipped to production with no entry in the policy control matrix. Action: Block further rollout, require emergency compliance review and retroactive mapping.
2. **Regulatory Change Without Matrix Update** (P2 - Warning): Condition - a tracked regulatory/policy change has no corresponding control matrix update after 30 days. Action: Escalate to compliance lead, prioritize gap analysis.
3. **Compliance Waiver Expired** (P3 - Info): Condition - a time-boxed gap waiver passes its expiry without remediation. Action: Notify capability owner and compliance, consider capability suspension until closed.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| policy_coverage_percent | < 95% |
| unmapped_capability_count | > 0 deployed capabilities without a policy mapping |
| control_matrix_staleness_days | > 90 days since last review |
| compliance_gap_waivers_open | any waiver open past its expiry |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unmapped Capability Deployed | Agent capability shipped to production with no entry in the policy control matrix | Critical |
| Regulatory Change Without Matrix Update | A tracked regulatory/policy change has no corresponding control matrix update after 30 days | Warning |
| Compliance Waiver Expired | A time-boxed gap waiver passes its expiry without remediation | Info |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
