# Conditional Permission Logic

## Issue
Some permissions are conditional on runtime state rather than static role membership — "allow withdrawal only if account balance exceeds the requested amount," "allow this API call only during business hours," "allow escalation only if the ticket is marked P1." The agent evaluates these conditions against stale, cached, or incorrectly fetched data, or implements the comparison logic incorrectly (off-by-one, wrong field, wrong currency/unit), and grants access that the live condition would have denied.

**Frequency**: Common

**Symptoms**
- Actions succeed based on a condition that was true minutes or hours earlier but is false at execution time
- The agent reads a cached snapshot of account/resource state rather than querying the live value before authorizing
- Boundary conditions (exactly at the threshold) are handled inconsistently, e.g. `>=` implemented as `>`
- Two different fields with similar names (e.g. `available_balance` vs `ledger_balance`) are conflated in the condition check
- Race conditions where two near-simultaneous requests are each evaluated against the same pre-request balance, both passing a check that only one should have passed

## Root Cause
Conditional permission logic requires the check to run against current, authoritative state at the moment of execution, and to be evaluated atomically with respect to the eventual write. Agent architectures often separate "decide" (read some state, maybe cached, and pass/fail a condition) from "act" (perform the tool call) as two distinct steps with no locking or re-validation in between, so the state can change — or was already stale — between the check and the effect. This is a straightforward time-of-check-to-time-of-use (TOCTOU) gap made worse by agents that plan multiple steps ahead using values fetched early in a long-running session.

## Example
```
1. A banking agent is permitted to auto-approve a withdrawal only if the account's available balance is
   greater than or equal to the requested amount.
2. At the start of a session, the agent fetches the account balance ($500) into its working context to
   plan a multi-step task.
3. Ten minutes and several tool calls later, the user asks the agent to withdraw $450. The agent reuses
   the balance value already in its context ($500) instead of re-querying current balance.
4. In the intervening ten minutes, an unrelated pending charge of $300 settled, dropping the real
   available balance to $200.
5. The agent approves and executes the $450 withdrawal against a condition it evaluated using stale data,
   overdrawing the account.
```

## Statistics
| Finding | Context |
|---------|---------|
| Stale-state evaluation is among the most common root causes of incorrect conditional authorization in long-running agent sessions | Common finding in agent architecture reviews |
| Off-by-one boundary errors (`>` vs `>=`) appear in a meaningful minority of hand-written conditional permission checks | Typical code-review finding |
| Re-validating the condition immediately before the write, inside the same transaction, removes most TOCTOU-class approval errors | Common remediation outcome |

## Mitigations
1. **Re-check conditions at execution time, not plan time**: Fetch the authoritative value fresh, immediately before the gated action executes, rather than reusing a value read earlier in the session.
2. **Evaluate and act atomically**: Wrap the condition check and the state-changing operation in a single transaction or optimistic-lock so no other write can land between check and effect.
3. **Centralize condition evaluation in one audited function**: Avoid duplicating boundary logic (`>=`, unit conversions, field selection) across multiple call sites; use one well-tested policy function for each condition type.
4. **Explicitly test boundary values**: Include unit tests for the exact threshold, one unit below, and one unit above for every conditional permission rule.
5. **Time-bound cached context**: Mark any state value pulled into agent context with a freshness TTL, and force a re-fetch for any condition check once that TTL has elapsed.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| condition_check_staleness_seconds | Time between when a condition's input data was fetched and when it was used to authorize an action | > 60s |
| boundary_condition_denial_rate | Rate of requests denied at exactly the threshold value, compared to expected | Deviation > 10% from baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Action approved on stale condition data | Gated action executes using a condition input older than the freshness TTL | High | Block execution pending re-check, alert engineering |
| Post-hoc condition violation | Reconciliation job finds an executed action whose gating condition was false at execution time | Critical | Reverse if possible, audit the specific check path |

## Related Patterns
- [Owner Verification Not Enforced](./owner-verification-not-enforced.md) - both are runtime checks that must be evaluated against live, specific state rather than assumptions
- [Approval Signature Verification](./approval-signature-verification.md) - both are examples of authorization logic that looks correct on paper but has a gap in when/how the check is evaluated
- [Permission Cascade Incorrect](./permission-cascade-incorrect.md) - both involve incorrect evaluation of a permission rule against the wrong data or scope
