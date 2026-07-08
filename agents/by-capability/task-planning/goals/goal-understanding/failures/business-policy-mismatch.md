# Business-Policy Mismatch

## Issue: Agent completes a technical action that violates company policy.

**Frequency**: Common

**Symptoms**
- Compliance review flags policy violation.
- [Add more specific symptoms]

**Root Cause**
Agent completes a technical action that violates company policy.

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
1. **Policy-as-Code Pre-Action Gate**: Every action call is evaluated by a policy engine (e.g., OPA/Rego rules) against the current policy set before execution, using structured inputs (actor, action type, target, context). Actions that fail the check are blocked outright, decoupling "technically possible" from "permitted," which is the specific gap this failure exploits.
2. **Policy Retrieval-Augmented Planning**: Before drafting a plan, the agent retrieves the relevant policy clauses (via RAG over a versioned policy corpus) tied to the action's domain and type, so plan generation is policy-aware from the start rather than only checked as an afterthought once the plan is formed.
3. **Segregation of Capability and Authority**: Tool wrappers expose a narrower permission surface than the underlying system supports (e.g., a refund tool enforces dollar caps and category exclusions independent of what the raw payment API could technically do), so violating policy requires an explicit, logged override path rather than being reachable by default.

### Detection & Response
1. **Real-Time Policy Re-Evaluation**: Every completed action is logged and asynchronously re-evaluated against the latest policy version, catching cases where policy changed between plan-time and audit-time or where the gate was misconfigured at execution time.
2. **Compliance Review Sampling**: A statistically sampled slice of transcripts is routed to compliance reviewers; violation rate is tracked by action type and team, and confirmed violations feed back into policy engine rule updates rather than being handled as one-offs.
3. **Justification-to-Policy Consistency Check**: Automatically compare the agent's stated rationale for an action against the policy clause it should be citing; a mismatch (rationale doesn't reference or align with any applicable policy) is flagged even when the action itself wasn't explicitly blocked.

### Architecture Patterns
1. **Policy Engine Sidecar**: A dedicated policy service (e.g., OPA) is queried synchronously before every policy-relevant action and returns allow/deny/require_approval. It is deployed and versioned independently of the agent so policy updates take effect without redeploying the agent.
2. **Policy Version Pinning + Change Feed**: Policy documents are versioned; the agent subscribes to a change feed and invalidates any cached policy context on update, preventing execution against a stale policy snapshot.
3. **Immutable Action-Policy Audit Log**: Every action is recorded together with the exact policy version and clause it was evaluated against, stored immutably to support compliance audits and regulatory reporting.

### Metrics
1. **policy_check_coverage_percent**: Target: 100% of policy-relevant actions gated; Alert threshold: < 100%
2. **policy_violation_rate_percent**: Target: < 0.1%; Alert threshold: > 0.5%
3. **stale_policy_context_incidents**: Target: 0 per month; Alert threshold: > 0
4. **compliance_review_flag_rate_percent**: Target: < 1%; Alert threshold: > 3%

### Alerts
1. **Policy Gate Bypass Detected** (P1 - Critical): Condition - a policy-relevant action executed without a recorded policy-engine evaluation. Action: halt action-executing agents in the affected domain, page on-call, run incident review.
2. **Confirmed Policy Violation** (P1 - Critical): Condition - compliance review confirms a completed action violated policy. Action: reverse or remediate the action where possible, notify the affected party, root-cause why the gate missed it.
3. **Policy Staleness Warning** (P3 - Info): Condition - agent's cached policy context exceeds its TTL while an upstream policy change is pending. Action: force a cache refresh and audit any actions taken during the stale window.

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
