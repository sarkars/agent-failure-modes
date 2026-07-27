# What Are the Most Common Ticket Routing Failures in AI Agents?

**Ticket-routing agents fail when they classify a ticket's product category by embedding similarity to a taxonomy node without verifying the account actually has that product, when they route based on surface complexity heuristics without estimating actual resolution effort, when they ignore language mismatch between a ticket and the destination team's language capabilities, when reclassification on later messages silently reassigns a ticket already actively claimed by a human agent, and when an intake bot's determination of VIP account status never reaches the routing agent's working context.** Six distinct mechanisms produce six failure patterns in ticket routing: retrieval without provisioning verification, effort-estimation blindness, language-capability omission, ownership-state blindness, handoff information loss, and priority-signal gaming. Each mechanism independently defeats a different kind of verification: similarity-based taxonomy matching defeats account-provisioning confirmation, per-ticket effort prediction defeats cross-ticket complexity patterns, solo-language routing defeats joint language-topic constraint checking, stateless reclassification defeats ownership-state verification, handoff schemas omit task-relevant context, and priority-classification opacity enables gaming.

## Key Takeaways

- 6 patterns are documented for ticket routing, spanning retrieval-without-verification, effort-estimation gap, language mismatch, mid-conversation reclassification, VIP-status loss, and priority gaming.
- The retrieval-without-verification pattern shows a ticket routed to a specialist queue for a product line the customer's account has never had provisioned, an error caught only when the receiving queue reviews the ticket and finds no matching account relationship.
- The effort-estimation-gap pattern shows complex tickets routed to tier-1 auto-response because keyword matching looks simple, requiring escalation 24 hours later when tier-1 cannot resolve, adding a full queue cycle of delay.
- The language-mismatch pattern documents tickets in non-English languages correctly classified by topic but routed to queues staffed only by English-speaking agents, bouncing between queues until a correctly-staffed queue receives it.
- The mid-conversation-reclassification pattern shows a ticket actively being worked by a human agent silently reassigned to a different team when a new customer message shifts the full-context topic classification, losing the agent's partial progress and context.
- The VIP-status-loss pattern documents enterprise accounts' tickets landing in standard queues despite the triage bot correctly identifying the account tier, because the structured handoff omits account-tier information.
- The priority-gaming pattern shows customers learning which language triggers high-priority routing and exploiting it, degrading classifier accuracy over time as the input distribution shifts adversarially.

## Scope

- **Retrieval without provisioning verification** — [Embedding Retrieval Misroutes Ticket via Similarity to Wrong Product-Line Taxonomy Node](failures/embedding-retrieval-misroutes-ticket-via-similarity-to-wrong-product-line-taxonomy-node.md). Product-category classification matches the ticket text to a taxonomy node by similarity without verifying the account has that product provisioned.
- **Effort-estimation gap** — [High-Effort Ticket Misrouting](failures/high-effort-ticket-misrouting.md). Routing model trained on successfully-resolved tickets learns keywords but not effort/complexity, biasing toward tier-1 routing even for complex issues.
- **Language-capability omission** — [Language Mismatch Misroute](failures/language-mismatch-misroute.md). Ticket routed by topic classification without joint language-topic constraint checking, sending non-English tickets to English-only queues.
- **Mid-conversation reclassification** — [Mid-Conversation Reclassification Reroutes Actively-Owned Ticket](failures/mid-conversation-reclassification-reroutes-actively-owned-ticket.md). Routing agent re-runs full-context intent classification on every new customer message, silently reassigning claimed tickets when topic classification shifts.
- **Handoff information loss** — [Multi-Agent Handoff Drops VIP-Tier Flag Between Triage Bot and Routing Agent](failures/multi-agent-handoff-drops-vip-tier-flag-between-triage-bot-and-routing-agent.md). Triage bot correctly identifies VIP account status in free text; structured ticket handoff has no account-tier field, so routing applies standard queue assignment.
- **Priority-signal gaming** — [Priority Inflation Gaming](failures/priority-inflation-gaming.md). Priority classifier learns from its own prior outputs as training labels, reinforcing gamed phrasing patterns rather than correcting for them, filling high-priority queues with inflated-priority tickets.

## When Ticket Routing Matters

- A routing system classifies incoming tickets by product category, complexity, language, or account tier to direct them to specialist queues
- The ticket corpus contains multiple product lines with overlapping generic terminology in their taxonomy descriptions
- A support organization is multilingual, with different teams capable of handling different languages
- Tickets flow through multiple stages (triage bot → routing agent → specialist queue) with handoffs between stages
- High-priority queues are used as a cost-saving mechanism (faster response = fewer follow-ups) and are subject to customer or agent exploitation

## Cross-Pattern Insight

Every ticket-routing pattern documented here reflects a mismatch between what the routing agent can infer from textual signals and what needs to be verified against structured data: a product category is inferred by similarity when account provisioning must be confirmed, complexity is inferred by keywords when effort must be estimated, language is detected but team capability is not confirmed, topic classification is re-run per message when ownership state must be checked, and account tier is noted in free text when structured fields must propagate it. The fix is standardized: ground routing decisions in structured account/provisioning data before similarity ranking, combine effort-estimation with keyword classification, implement joint language-topic routing constraints, gate reclassification on ownership checks, extend handoff schemas for task-relevant context, and ground priority signals in outcome-validated risk rather than learnable exploit patterns.

## Frequently Asked Questions

### How do you verify a ticket is routed to a provisioned product line?
Query the account's provisioning record against the classified product line before routing finalizes; block routing to unprovisioned products regardless of taxonomy-similarity scores. See [Embedding Retrieval Misroutes Ticket via Similarity to Wrong Product-Line Taxonomy Node](failures/embedding-retrieval-misroutes-ticket-via-similarity-to-wrong-product-line-taxonomy-node.md).

### Can keyword-based complexity prediction route high-effort tickets correctly?
No. Routing models trained on successfully-resolved tickets develop a baseline bias toward the most common resolution path (tier-1). A separate effort-estimation model trained on resolution time, not just keywords, is needed. See [High-Effort Ticket Misrouting](failures/high-effort-ticket-misrouting.md).

### How do you avoid routing non-English tickets to English-only teams?
Treat detected language and required team expertise as a joint constraint, not independent filters. Maintain a registry of which languages each team handles and validate every routing decision against it. See [Language Mismatch Misroute](failures/language-mismatch-misroute.md).

### How does a ticket get silently reassigned mid-conversation?
Because routing agents that re-run full-context intent classification on every new message have no ownership-state check before executing reassignment. The new message shifts the topic classification, triggering a reroute, without any verification that a human is already mid-resolution. The fix is an ownership check gating the reroute. See [Mid-Conversation Reclassification Reroutes Actively-Owned Ticket](failures/mid-conversation-reclassification-reroutes-actively-owned-ticket.md).

### How do you prevent VIP account status from being lost at routing time?
Add a structured account-tier field to the triage-to-routing handoff and require triage to populate it directly. Alternatively, have routing independently query the account's tier from the CRM record it has access to. See [Multi-Agent Handoff Drops VIP-Tier Flag Between Triage Bot and Routing Agent](failures/multi-agent-handoff-drops-vip-tier-flag-between-triage-bot-and-routing-agent.md).

### How do you detect priority-classifier gaming?
Track whether specific trigger phrases correlate with priority escalation and then check whether those phrases correlate with independently-validated actual severity. If gaming is happening, the language-priority correlation diverges from the language-severity correlation. See [Priority Inflation Gaming](failures/priority-inflation-gaming.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Embedding Retrieval Misroutes Ticket via Similarity to Wrong Product-Line Taxonomy Node](failures/embedding-retrieval-misroutes-ticket-via-similarity-to-wrong-product-line-taxonomy-node.md) | Product category matched by text similarity without provisioning-record verification |
| [High-Effort Ticket Misrouting](failures/high-effort-ticket-misrouting.md) | Routing model trained on successful cases develops baseline bias toward tier-1, underestimating complex-ticket effort |
| [Language Mismatch Misroute](failures/language-mismatch-misroute.md) | Ticket routed by topic without joint language-capability constraint checking |
| [Mid-Conversation Reclassification Reroutes Actively-Owned Ticket](failures/mid-conversation-reclassification-reroutes-actively-owned-ticket.md) | Per-message reclassification silently reassigns claimed tickets without ownership-state check |
| [Multi-Agent Handoff Drops VIP-Tier Flag Between Triage Bot and Routing Agent](failures/multi-agent-handoff-drops-vip-tier-flag-between-triage-bot-and-routing-agent.md) | VIP status determined in triage; structured handoff omits account-tier field |
| [Priority Inflation Gaming](failures/priority-inflation-gaming.md) | Priority classifier trained on its own prior outputs, reinforcing gamed phrasing patterns |

**Total: 6 patterns**

## Related Goals

- [Sentiment Escalation](../sentiment-escalation/) — influences routing priority and playbook selection after routing occurs
- [SLA Management](../sla-management/) — routing determines applicable SLA tier for the ticket
- [Issue Resolution](../issue-resolution/) — downstream goal; correct routing determines resolution quality
