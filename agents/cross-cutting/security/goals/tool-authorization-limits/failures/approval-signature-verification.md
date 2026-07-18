# Approval Signature Verification

## Issue
A high-risk action (fund transfer, policy override, data export) is gated behind a requirement that a human approver's cryptographic signature or signed token accompany the execution request. The agent's verification of that signature is incomplete — it checks presence of a token rather than validity, uses a weak or non-constant-time comparison, doesn't bind the signature to the specific action payload, or doesn't check expiry/single-use — so a forged, replayed, or mismatched approval is accepted as genuine.

**Frequency**: Occasional

**Symptoms**
- The same approval token is successfully reused across multiple, different action requests
- Signature verification code checks only that a signature field is non-empty, not that it cryptographically matches the payload
- Approval tokens have no expiry, or expiry is checked client-side only
- An approval issued for action A (e.g. "approve refund of $50") is accepted for action B (e.g. "approve refund of $5,000") because the signature isn't bound to the payload contents
- Logs show approval verification succeeding for signatures that don't correspond to any real approver key

## Root Cause
Teams often implement "requires signed approval" as a checkbox feature — add a signature field to the request, add a function called `verify_signature` — without applying real cryptographic discipline: binding the signature to a canonical serialization of the exact action being approved, checking it against the actual approver's public key, enforcing one-time-use via a nonce or consumed-token ledger, and enforcing a short expiry window. Any gap in that chain turns the "signed approval" into a shared secret that can be replayed or transplanted onto a different, larger action.

## Example
```
1. A treasury-ops agent requires a manager's signed approval token before executing any wire transfer
   over $10,000.
2. A manager approves a legitimate $10,500 transfer; the approval service returns a signed token scoped
   only by "approved: true" with no payload hash and no expiry.
3. An attacker who intercepts or is handed that token (e.g. via a support chat transcript) replays the
   same token against a new wire-transfer request for $250,000.
4. The agent's verify_approval() function checks that the token's signature is valid against the
   approver's public key -- which it is, since it's the same legitimate token -- but never checks that
   the token was issued for this specific transfer amount and recipient.
5. The $250,000 transfer executes on a stale, mis-scoped approval.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large share of "approval required" agent workflows implement presence checks rather than full cryptographic verification | Common finding in agent security reviews of financial/ops workflows |
| Payload-unbound approval tokens are the most frequently exploited weakness in signed-approval implementations, ahead of weak algorithms | Typical pattern in red-team exercises against approval gates |
| Adding payload binding and single-use enforcement closes the large majority of replay-style approval bypasses | Common remediation outcome |

## Mitigations
1. **Bind signatures to a canonical payload hash**: Sign a deterministic serialization of the exact action (amount, recipient, resource ID, timestamp) so a signature for one action cannot be replayed against another.
2. **Enforce single-use tokens via a consumed-token ledger**: Record every verified approval token in a persistent store and reject any token seen a second time, rather than relying on client-side expiry alone.
3. **Short, server-enforced expiry**: Set a tight TTL (minutes, not days) on approval tokens and check it server-side at verification time, not just at issuance.
4. **Use constant-time signature comparison with real key verification**: Verify against the approver's actual public key using a vetted crypto library, not a string-equality check on a shared secret.
5. **Log full verification context on every check**: Record the payload hash, approver key ID, and expiry outcome for every verification attempt (pass or fail) to support post-incident forensic review.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| approval_token_reuse_count | Number of times a single approval token is presented for verification | > 1 per token |
| approval_payload_mismatch_rate | Verified signatures where the bound payload hash differs from the requested action | > 0 per day |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Approval token replay detected | Same token ID passes verification more than once | Critical | Block execution, revoke token, notify security and the original approver |
| Expired token accepted | Token with expiry timestamp in the past passes verification | Critical | Halt approval service, audit verification code path immediately |

## Related Patterns
- [Sensitive Operation No Approval Requirement](./sensitive-operation-no-approval-requirement.md) - this pattern covers the case where the approval gate exists but is verified incorrectly, versus missing entirely
- [Conditional Permission Logic](./conditional-permission-logic.md) - both involve runtime evaluation logic that must correctly bind a decision to current, specific facts
- [Delegation Impersonation Not Limited](./delegation-impersonation-not-limited.md) - forged/replayed approvals are one mechanism by which delegated authority is exceeded
