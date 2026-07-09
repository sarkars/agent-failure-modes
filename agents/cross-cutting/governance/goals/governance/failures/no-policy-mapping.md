# No Policy Mapping

## Issue: Agent behavior not mapped to company/regulatory policies.

**Frequency**: Common

**Symptoms**
- Compliance review cannot trace control coverage.
- [Add more specific symptoms]

**Root Cause**
Agent behavior not mapped to company/regulatory policies.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [NIST-AI-RMF](https://www.nist.gov/itl/ai-risk-management-framework)
- Note: Govern, map, measure, manage framework for AI risk.
