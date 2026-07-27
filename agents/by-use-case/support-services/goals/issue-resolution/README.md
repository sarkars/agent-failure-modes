# What Are the Most Common Issue Resolution Failures in AI Agents?

**Issue-resolution agents fail when they select a canned response by keyword similarity without verifying situational fit, when a multi-agent handoff loses a prior troubleshooting attempt the customer already described, when the same customer contacts support repeatedly for the same underlying problem treated each time as an independent resolution, when an autonomous refund is processed based on the customer's fluent claim without verifying the claim against the ledger, when knowledge-base content becomes stale, and when the agent re-suggests a troubleshooting step the customer already tried and reported as unsuccessful.** Six distinct mechanisms produce six distinct failure patterns in issue resolution: macro misapplication, handoff information loss, repeat-contact blindness, unverified-claim-to-action, knowledge staleness, and reachability to repeat suggestions. Each mechanism independently defeats a different kind of verification: template confidence defeats situational appropriateness, schema-bounded handoffs defeat cross-stage information transfer, per-ticket resolution metrics defeat cross-ticket pattern detection, fluent claim phrasing defeats ledger verification, static content defeats currency maintenance, and handoff loss defeats repeated-suggestion suppression.

## Key Takeaways

- 6 patterns are documented for issue resolution, spanning macro/template misapplication, handoff information loss, repeat-contact blindness, unverified autonomous action, knowledge staleness, and prior-attempt visibility.
- The macro-misapplication patterns show that high macro-usage rates correlate with lower first-contact-resolution rates and higher escalations when the macro selection is not verified against actual situational preconditions.
- The multi-agent-handoff pattern documents a bot-tier agent recording attempted troubleshooting steps in its free-text transcript, but the human-agent queue never receiving a structured list of those steps, causing the human to re-suggest the same unsuccessful fix.
- The repeat-contact-loop pattern shows that support agents optimized to close individual tickets have no mechanism to detect that the same customer has contacted repeatedly for the same underlying issue, each contact appearing as an independent success.
- The unverified-refund pattern documents an agent approving a refund for a "charged twice" claim with no verification-tool call confirming the duplicate charge actually exists in the ledger, a pattern clustered in claim categories with fluent, policy-matching phrasing.
- The knowledge-staleness pattern shows that 20-40% of knowledge-base articles become outdated more than 6 months after publication, leading to 10-20% incorrect guidance rates in chatbot responses.

## Scope

- **Response-selection mismatch** — [Canned Response Context Mismatch](failures/canned-response-context-mismatch.md) and [Macro Response Misapplication](failures/macro-response-misapplication.md). Canned responses selected by keyword or intent similarity without verifying preconditions (account features, plan tiers, applicability to the customer's actual situation) are sent as solutions even when situationally wrong.
- **Handoff information loss** — [Multi-Agent Handoff Drops Prior Attempted Fix Between Bot and Human Agent](failures/multi-agent-handoff-drops-prior-attempted-fix-between-bot-and-human-agent.md). An upstream bot's transcript records which troubleshooting steps a customer tried and reported as unsuccessful, but the structured handoff to a human agent carries no "steps already attempted" field, causing the human to re-suggest failed steps.
- **Repeat-contact blindness** — [Repeat Contact Loop](failures/repeat-contact-loop.md). Support agents measure per-ticket resolution success, with no cross-ticket pattern detection, so repeated contacts from the same customer for the same underlying issue each appear as independent, successful resolutions rather than signaling an unresolved root cause.
- **Unverified autonomous action** — [Unverified Customer Claim Triggers Autonomous Refund](failures/unverified-customer-claim-triggers-autonomous-refund.md). An agent processes a refund directly off a customer's fluent, policy-matching claim without calling the ledger or shipment-tracking tool to verify the claim's basis, with refund-approval rates clustering on claims with fluent, policy-matching phrasing.
- **Knowledge staleness** — [Knowledge Base Staleness in Support Chatbots](failures/knowledgebase-staleness.md). Knowledge-base articles referencing removed UI elements or outdated steps accumulate over time, and chatbots trained on static KB continue to surface outdated guidance long after product updates.

## When Issue Resolution Matters

- A support system uses templated responses selected automatically or semi-automatically based on keyword or intent similarity
- A multi-tier support system (bot-tier intake followed by human-agent escalation) passes information between stages through a structured ticket summary rather than by the human agent reading the full bot transcript
- Support agents are measured on per-ticket closure rate without cross-ticket pattern detection for repeat contacts
- An issue-resolution agent has autonomous or semi-autonomous authority to execute refunds or credits based on customer claims
- A support chatbot is trained on knowledge-base articles that may become outdated as the product evolves

## Cross-Pattern Insight

Every issue-resolution pattern documented here shares a single structural gap: the resolution agent treats a plausible-looking signal — a template match, a closed ticket, a fluent claim, a knowledge-base article, an escalation suggestion — as sufficient grounds for resolution, without an independent, deterministic check against a different kind of ground truth. The fix is architecturally identical across patterns: gate the decision on a verification step that does not depend on the same mechanism that produced the signal, whether that is a situational-precondition check, a cross-ticket pattern scan, a ledger verification, a knowledge-currency audit, or a prior-attempt reconciliation.

## Frequently Asked Questions

### How do you know when a canned response is situationally inappropriate?
Track first-contact-resolution rate and escalation rate separately for macro-resolved versus fully custom-written responses. If macro-resolved tickets show measurably higher re-contact or escalation rates, the macro selection is the precision problem to fix. See [Canned Response Context Mismatch](failures/canned-response-context-mismatch.md) and [Macro Response Misapplication](failures/macro-response-misapplication.md).

### How does a human agent re-suggest a troubleshooting step the bot already tried?
Because the bot-to-human handoff uses a structured summary that may lack a "steps already attempted" field. The human agent reasonably relies on the structured summary rather than re-reading the full bot transcript under time pressure, so task-relevant context in free text never reaches the human's working context. See [Multi-Agent Handoff Drops Prior Attempted Fix Between Bot and Human Agent](failures/multi-agent-handoff-drops-prior-attempted-fix-between-bot-and-human-agent.md).

### How do you detect when the same customer's problem is recurring rather than resolved?
Implement a cross-ticket pattern detection that flags when the same customer (or a cluster of customers) reports the same symptom more than a threshold number of times within a window. Per-ticket resolution metrics alone will miss these patterns. See [Repeat Contact Loop](failures/repeat-contact-loop.md).

### Can a customer's claim alone justify an autonomous refund without ledger verification?
No. Fluent, policy-matching phrasing produces the highest refund-approval rates but is uncorrelated with actual claim validity; the reliable signal is a verified ledger or tracking record. Without a mandatory verification-tool call before the refund action executes, approval rates cluster on phrasing rather than evidence. See [Unverified Customer Claim Triggers Autonomous Refund](failures/unverified-customer-claim-triggers-autonomous-refund.md).

### How stale does a knowledge-base article need to be before it becomes unreliable?
Articles older than 6 months warrant review, and 20-40% of articles go unreviewd beyond that window in practice. Currency audit is the most reliable check, but a structured "last reviewed" date with an automatic staleness flag is also common. See [Knowledge Base Staleness in Support Chatbots](failures/knowledgebase-staleness.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Canned Response Context Mismatch](failures/canned-response-context-mismatch.md) | Canned response selected by keyword match, not situational precondition verification |
| [Macro Response Misapplication](failures/macro-response-misapplication.md) | Macro sent based on surface keyword match without checking applicability to customer's specific scenario |
| [Multi-Agent Handoff Drops Prior Attempted Fix Between Bot and Human Agent](failures/multi-agent-handoff-drops-prior-attempted-fix-between-bot-and-human-agent.md) | Bot's transcript records attempted steps; human-agent handoff lacks structured "steps attempted" field |
| [Repeat Contact Loop](failures/repeat-contact-loop.md) | Each support contact resolved independently; repeat contacts for same issue treated as separate successes |
| [Unverified Customer Claim Triggers Autonomous Refund](failures/unverified-customer-claim-triggers-autonomous-refund.md) | Agent processes refund based on fluent claim without verification-tool call to confirm claim against ledger |
| [Knowledge Base Staleness in Support Chatbots](failures/knowledgebase-staleness.md) | Chatbot uses outdated KB articles that reference removed UI elements or deprecated steps |

**Total: 6 patterns**

## Related Goals

- [Self-Service Deflection](../self-service-deflection/) — upstream stage; deflection-loop and circular-redirect failures prevent issues from reaching issue-resolution agents
- [Sentiment Escalation](../sentiment-escalation/) — orthogonal goal; escalation failures route issues to wrong handling teams rather than resolving them
- [Ticket Routing](../ticket-routing/) — upstream stage; routing errors send tickets to wrong specialist queues before issue resolution happens
