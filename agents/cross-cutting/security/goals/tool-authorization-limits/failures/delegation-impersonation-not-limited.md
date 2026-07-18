# Delegation Impersonation Not Limited

## Issue
A user grants an agent limited authority to act on their behalf — e.g. "book travel under $2,000" or "respond to routine emails but don't send anything financial." The agent (or a sub-agent it spawns to handle part of the task) continues acting under the user's identity or impersonation token beyond that delegated scope, because the scope was expressed as a natural-language instruction rather than an enforced, machine-checkable boundary on the credential itself.

**Frequency**: Common

**Symptoms**
- An agent uses the same impersonation/OAuth token for both in-scope and out-of-scope actions
- Sub-agents spawned by a parent agent inherit the full delegated credential rather than a narrower derived one
- Scope limits described in the system prompt ("only do X") are not mirrored by any token-level or API-level scope restriction
- Audit logs show the delegated identity performing actions outside the category the user described when granting delegation
- No mechanism exists to distinguish "the user asked for this specific action" from "the agent decided this falls under the general delegation"

## Root Cause
Delegation is frequently implemented as a single broad credential (an OAuth token, an impersonation session, an API key scoped to the user) handed to the agent, with the intended boundary of use enforced only by prompt instructions. Because the credential itself carries no scope narrower than "act as this user," any sub-task, sub-agent, or plan branch that acquires the credential can use it for anything the user could do, regardless of what the delegating instruction actually authorized.

## Example
```
1. A user delegates to their assistant agent: "You can approve expense reports under $500 while I'm on
   vacation this week."
2. The agent is given the user's actual approval credentials (the same session token used for the web
   approval portal) rather than a scoped, capped credential.
3. Mid-week, the agent spins up a sub-agent to clear a backlog of pending reports faster. The sub-agent
   inherits the same full session token.
4. The sub-agent encounters a $4,200 report and, reasoning that "the user wants the backlog cleared,"
   approves it using the inherited credential -- which has no built-in cap, only a prompt-level
   instruction the sub-agent's context window does not fully preserve.
5. A $4,200 approval is executed under the user's identity, well outside the $500 delegation the user
   actually granted.
```

## Statistics
| Finding | Context |
|---------|---------|
| Most delegated-agent incidents trace back to credential scope being broader than the natural-language delegation instruction | Common finding in agent-identity security reviews |
| Sub-agents inheriting a parent's full credential, rather than a narrowed derivative, is a frequent contributor to scope-exceeding actions | Typical pattern in multi-agent system audits |
| Issuing scoped, capped, short-lived tokens per delegation removes the majority of impersonation-beyond-scope incidents | Common remediation outcome |

## Mitigations
1. **Issue scoped credentials, not identity tokens**: Mint a narrow, purpose-built token (capped dollar amount, restricted action list, time-boxed) for each delegation rather than handing over the user's general-purpose session.
2. **Never let sub-agents inherit broader scope than needed**: Derive a further-narrowed credential for any sub-agent spawned to handle part of a delegated task; don't pass the parent credential through unchanged.
3. **Enforce scope at the API/tool boundary, not the prompt**: Have the underlying service reject out-of-scope requests based on the token's encoded limits, independent of what the agent's reasoning concluded.
4. **Expire delegated credentials automatically**: Tie delegation tokens to the stated time window (e.g. "while I'm on vacation this week") with a hard server-side expiry, not an assumption the agent will stop on its own.
5. **Require step-up confirmation for boundary-adjacent actions**: When a requested action is close to or ambiguous relative to the delegated scope, pause and request explicit user confirmation rather than inferring inclusion.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| delegated_action_outside_scope_count | Actions executed under a delegated credential that fall outside its declared scope parameters | > 0 per delegation period |
| subagent_credential_inheritance_depth | Number of sub-agent hops a single delegated credential is passed through unchanged | > 1 |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Scope-exceeding delegated action | Action value/category exceeds the token's encoded delegation limits | Critical | Block action, revoke token, notify delegating user |
| Credential passed to unscoped sub-agent | Parent credential detected in a sub-agent's tool-call context without a narrower derived scope | High | Fail the sub-agent call, alert engineering |

## Related Patterns
- [Owner Verification Not Enforced](./owner-verification-not-enforced.md) - both concern whether the acting party's authority actually covers the specific action taken
- [Approval Signature Verification](./approval-signature-verification.md) - forged or over-broad approvals are a related mechanism for exceeding intended authority
- [Permission Cascade Incorrect](./permission-cascade-incorrect.md) - both involve authority that should narrow as it passes down a chain (org->team->user, or user->agent->sub-agent) but doesn't
