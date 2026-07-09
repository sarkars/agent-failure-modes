# Offer Letter Auto-Sent Without Rechecking Live Background-Check Gate Status

## Issue: An Offer-Generation Agent Configured to Send a Finalized Offer Letter Automatically Once a Candidate Clears a Conditional-Offer Gate Sends the Letter Based on the Background-Check Step No Longer Appearing in Its Own List of Outstanding Blockers, Without Re-Querying the Background-Check Vendor's API for the Current Status, and the Check Had Actually Moved to "Pending Dispute" Rather Than "Clear"

**Frequency**: Occasional

**Symptoms**
- The offer letter is sent and timestamped before any log entry shows a fresh call to the background-check vendor's status endpoint for that candidate
- The agent's internal task list shows the background-check item simply absent rather than marked "clear," and the agent treats absence-from-the-blocker-list as equivalent to confirmed clearance
- When the vendor's API is queried directly at the moment the letter is sent, the actual status field reads "pending dispute" or "pending adjudication," a state the candidate or vendor had flagged after the agent's last successful status check
- Recruiting only discovers the mismatch when the candidate's background-check dispute resolves unfavorably after the offer letter, with a start date and comp terms, has already been sent and the candidate has begun planning their resignation from their current employer
- Re-running the same send-offer trigger with an explicit instruction to call the vendor's live status endpoint immediately before sending correctly catches the "pending dispute" state and withholds the letter, confirming the original failure was a missed re-check rather than a vendor-side data error

**Example**
```
Candidate's conditional offer requires background-check clearance before the formal offer letter is auto-generated and sent
Background-check vendor's webhook notifies the agent's task system that the check is "in progress" three days prior; the agent's outstanding-blockers list includes the background-check item at that point
A scheduling job re-runs the agent's blocker list two days later; the webhook-driven update that would have set "in progress" to "cleared" never fired due to a vendor-side webhook delivery gap, but a separate, unrelated task-list cleanup script removes stale entries older than 48 hours, including the background-check blocker
Agent's next run sees an empty blocker list for the candidate and proceeds to generate and auto-send the finalized offer letter, without itself calling the vendor's REST status endpoint to confirm current state
Vendor's actual current status field, queryable via API the entire time, reads "pending dispute" -- the candidate had flagged an inaccurate record three days earlier and resolution was still in progress
Offer letter with start date and compensation terms reaches the candidate before the dispute resolves; candidate gives notice at their current job based on the letter
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Agent-environment interaction research finds that agents frequently act on a stale or assumed environment state rather than re-querying the live source of truth immediately before an autonomous, consequential action, particularly when an internal task-tracking abstraction diverges from the underlying system it is meant to represent | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |
| Failure-mode taxonomies for LLM systems identify "premature autonomous action" -- acting on inferred or cached state instead of confirming current state via the authoritative tool -- as a distinct and recurring category separate from reasoning errors | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Analyses of cascading agent failures show that a single root-cause discrepancy between an agent's internal state representation and the actual environment propagates undetected through subsequent autonomous steps unless an explicit verification step is inserted before consequential actions | [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370) |

**Contributing Factors**
- The agent's decision to send the offer letter is gated on the absence of an item from its own derived blocker list, not on a fresh, authoritative call to the background-check vendor's status endpoint
- A webhook delivery gap from the vendor is never reconciled against a polling fallback, so the agent's blocker list can silently fall out of sync with the vendor's actual records
- An unrelated maintenance process (stale-entry cleanup) interacts with the blocker list in a way that mimics legitimate clearance, and the offer-sending logic cannot distinguish "cleared" from "removed for being stale"
- No mandatory pre-send verification step exists that is independent of the agent's own task-tracking state and instead queries the vendor's system of record directly

---

## Mitigation Strategies

1. **Mandatory Pre-Send Live Status Check**: Require a fresh, synchronous call to the background-check vendor's status endpoint immediately before any offer letter is sent, regardless of what the agent's internal blocker list shows, and block the send if the live status is anything other than an explicit "clear" value
2. **Separate Cached State From Authoritative Gate**: Treat the agent's derived blocker list as a convenience cache only; never allow the absence of an item from that cache to satisfy a send-gate condition without confirmation against the authoritative vendor system
3. **Webhook-Polling Reconciliation**: Run a periodic reconciliation job that compares webhook-driven status updates against a direct poll of the vendor API, and treat any divergence as cause to suspend automated sends for the affected candidate until resolved
4. **Human Confirmation for Conditional-Offer Gates**: Require a recruiter to confirm the live background-check status field on screen immediately before an auto-generated offer letter is released, for any role where a compliance-relevant clearance gates the offer

### Metrics
- Percentage of auto-sent offer letters preceded by a fresh, synchronous vendor status call within the same send transaction
- Number of candidates for whom the agent's blocker list and the vendor's live status diverged at any point before a send decision
- Mean time between a webhook delivery gap and detection via the reconciliation job

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Offer sent without live status check | An offer letter send transaction completes with no synchronous background-check status call in the same transaction | P1 | Immediately flag the candidate's file for manual compliance review; do not treat the offer as valid until live status is confirmed |
| Blocker-list and vendor status divergence | Reconciliation job finds the agent's blocker list omits an item the vendor's live status marks as unresolved | P1 | Suspend automated offer sending for the affected candidate pending manual review |
| Stale-entry cleanup removes a compliance-gating blocker | Maintenance cleanup process removes a background-check or other compliance-gate item from the blocker list | P2 | Exclude compliance-gating item types from automatic stale-entry cleanup; alert recruiting ops to manually verify before any cleanup of that category |

---

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [Where LLM Agents Fail and How They can Learn From Failures](https://arxiv.org/abs/2509.25370)
