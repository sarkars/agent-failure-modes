# Sensitive Operation No Approval Requirement

## Issue
An operation is classified in policy as sensitive or high-risk — deleting a production resource, transferring funds above a threshold, changing a customer's access level — and is documented as requiring human approval before execution. In practice, the agent's execution path has no code-level gate enforcing that requirement: the classification exists as a label or a line in a policy document, but nothing in the tool-dispatch pipeline actually blocks execution pending approval.

**Frequency**: Very Common

**Symptoms**
- The action executes immediately when called, with no pause, queue, or approval-pending state anywhere in the code path
- Policy documentation lists the operation as "requires approval" but the tool's implementation has no corresponding check
- An approval workflow exists as a UI feature for human operators, but the same underlying action, when triggered by the agent, bypasses that UI path entirely
- The only thing preventing the agent from calling the sensitive tool is a system-prompt instruction ("always ask before doing X"), not a hard gate
- Post-incident review finds the sensitive action was logged as executed with no corresponding approval record

## Root Cause
Sensitive-operation classification is often decided and documented at a policy or product-requirements level, while the actual software gate that would enforce "pause and wait for approval" is a separate, non-trivial engineering task (a queue, a state machine, a notification/approval UI, a resumption mechanism) that gets deprioritized or simply forgotten during implementation. The gap is invisible until someone — a user, a red-teamer, or the agent itself acting on an ambiguous instruction — actually triggers the operation and it just runs.

## Example
```
1. Company policy states that any agent-initiated deletion of a production database table must be
   approved by a human operator before execution, given the severity of the consequence.
2. The engineering team builds a drop_table tool for a database-maintenance agent and documents it in the
   tool's docstring as "sensitive -- requires human approval," intending to add the approval gate before
   launch.
3. Due to a scheduling gap, the actual approval-queue integration is never wired in; the docstring remains
   as the only trace of the requirement, and the tool executes DROP TABLE directly against the production
   database whenever called.
4. During a routine cleanup task, the agent identifies what it believes is an unused staging table with a
   name resembling a production table and calls drop_table on it.
5. The table is dropped immediately, with no approval step ever triggered, because the enforcement gate
   the policy assumed existed was never actually implemented in the execution path.
```

## Statistics
| Finding | Context |
|---------|---------|
| A substantial share of "requires approval" policy requirements for agent tools are found, on audit, to have no corresponding runtime gate | Common finding in agent governance audits |
| Sensitive operations without an execution-time gate are disproportionately represented in high-severity agent incident postmortems | Typical pattern in agent incident analysis |
| Implementing approval as a blocking state machine (rather than a pre-execution prompt reminder) closes the large majority of these gaps | Standard remediation for missing-approval findings |

## Mitigations
1. **Implement approval as a blocking execution state, not a prompt reminder**: The tool handler should place the action into a pending-approval queue and refuse to execute until an approval record exists, rather than relying on the agent choosing to ask first.
2. **Maintain a single sensitive-operations registry with enforced gating**: Keep one authoritative list mapping operation type to required approval tier, and have the dispatch layer consult it for every tool call, rejecting any sensitive operation lacking a matching approval record.
3. **Fail closed, not open, on approval-system errors**: If the approval service is unreachable or returns an ambiguous result, block the action rather than defaulting to execution.
4. **Require approval to specifically reference the action's parameters**: Bind the approval record to the exact resource/target/amount, not a generic "approved" flag, so approval for one action can't cover an unrelated one.
5. **Add pre-launch tests asserting sensitive tools cannot execute unapproved**: For every tool tagged sensitive, include an automated test that calls it with no approval record present and asserts execution is blocked.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| sensitive_ops_executed_without_approval_record | Count of sensitive-tagged operations executed with no matching approval record | > 0 per day |
| sensitive_ops_missing_gate_coverage | Fraction of tools tagged sensitive in documentation that have no corresponding runtime approval check | > 0% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sensitive operation executed unapproved | A tool tagged as requiring approval executes with no approval record | Critical | Halt the tool immediately pending investigation, review blast radius, notify security/ops leadership |
| New sensitive tool deployed without gate | CI detects a tool tagged sensitive lacking an approval-check code path | High | Block deployment until the gate is implemented |

## Related Patterns
- [Approval Signature Verification](./approval-signature-verification.md) - covers the case where the approval gate exists but its verification is weak, versus missing entirely here
- [Admin Operation Called By Non-Admin](./admin-operation-called-by-non-admin.md) - both involve a documented restriction that isn't backed by a runtime enforcement mechanism
- [Owner Verification Not Enforced](./owner-verification-not-enforced.md) - both are missing pre-execution checks on a mutating, consequential action
