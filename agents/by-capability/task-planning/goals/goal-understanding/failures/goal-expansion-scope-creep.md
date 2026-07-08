# Goal Expansion / Scope Creep

## Issue: Agent performs additional actions that were not requested.

**Frequency**: Common

**Symptoms**
- Unexpected side effects, extra messages, extra API calls.
- [Add more specific symptoms]

**Root Cause**
Agent performs additional actions that were not requested.

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
1. **Explicit Action Allowlist per Task**: The task specification includes a bounded list or pattern of permitted actions; anything outside it is blocked by default (deny-by-default execution boundary) instead of relying on the agent to self-judge what counts as "helpful" and in-scope.
2. **Scope Delta Approval Gate**: When the agent's plan includes actions beyond the minimal set needed to satisfy the stated goal, the delta is surfaced explicitly ("this also requires X — proceed?") and requires approval before execution, rather than being silently bundled in.
3. **Minimal-Sufficient-Plan Bias**: Prompt and evaluate the planner to prefer the smallest action set that satisfies the acceptance criteria, explicitly penalizing unrequested extras in scoring/eval even when each individual extra action looks benign in isolation.

### Detection & Response
1. **Action-to-Requirement Mapping Audit**: Tag every executed action with the specific requirement it fulfills. Actions with no mapped requirement are logged as scope-creep candidates and routed for review rather than passing silently.
2. **Side-Effect Diffing**: Compare system/API state before and after agent execution against the state implied by the stated goal alone; unexpected deltas (extra emails sent, extra records modified) trigger an alert independent of whether the agent reported success.
3. **User Surprise Signal Mining**: Monitor immediate user reactions ("why did you also...", confusion, undo requests) following agent turns for scope-creep language, and feed labeled examples back into the allowlist and approval-gate rules.

### Architecture Patterns
1. **Capability Scoping Layer**: The tool/action registry exposes only the subset of actions relevant to the active task type via a scoped credential or token, so even a misbehaving planner cannot call out-of-scope tools regardless of what it decides to attempt.
2. **Plan Diff Approval Service**: The planner emits a structured plan (actions with linked requirement IDs); a separate service diffs it against a minimal-plan baseline and routes any extras through an approval flow before the executor runs anything.
3. **Effect Ledger**: Every action's expected side effects are recorded before execution and reconciled against a post-execution diff of monitored systems, independent of the agent's own self-report of what it did.

### Metrics
1. **unrequested_action_rate_percent**: Target: < 2% of sessions; Alert threshold: > 8%
2. **action_requirement_traceability_percent**: Target: > 95%; Alert threshold: < 85%
3. **scope_approval_gate_trigger_rate_percent**: Target: tracked baseline; Alert threshold: 2x baseline spike
4. **user_undo_or_revert_rate_percent**: Target: < 1%; Alert threshold: > 3%

### Alerts
1. **High-Impact Unrequested Action** (P1 - Critical): Condition - agent executes an irreversible or externally-visible action (send email, charge, delete) with no traceable link to the stated goal. Action: attempt immediate rollback, run incident review, tighten the allowlist for that tool.
2. **Scope Creep Rate Spike** (P2 - Warning): Condition - unrequested_action_rate exceeds 2x rolling baseline. Action: review recent prompt/model changes, temporarily tighten action allowlists for affected task types.
3. **Repeated User Corrections for Extra Actions** (P3 - Info): Condition - 3+ undo/revert requests logged for the same task template within a week. Action: audit the task template and planner prompt for over-eager helpfulness framing.

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

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
