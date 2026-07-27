# What Are the Most Common SLA Management Failures in AI Agents?

**SLA-management agents fail when they apply an incorrect SLA tier because retrieval selected a boilerplate-heavy but wrong-tier policy document, when a multi-agent handoff loses a customer-specific SLA override negotiated during support, when the agent generates a customer-facing breach explanation that fabricates a plausible-sounding root cause instead of retrieving the actual logged cause, and when the SLA clock pause/resume logic misclassifies the source of delay or fails to resume promptly.** Four distinct mechanisms produce four failure patterns in SLA management: retrieval-based tier selection, handoff schema narrowness, hallucinated-cause substitution, and status-field-based clock management. Each mechanism independently defeats a different kind of verification: similarity-based retrieval defeats structural tier confirmation, fixed handoff schemas defeat overtime-determined-override propagation, free-text generation defeats logged-cause grounding, and status fields defeat actual-causality checking.

## Key Takeaways

- 4 patterns are documented for SLA management, spanning retrieval-based tier selection, handoff information loss, fabricated breach causes, and clock-pause logic errors.
- The retrieval-based-tier pattern shows a premium-tier customer's ticket tracked against a standard-tier SLA response window because the retrieval step selected by boilerplate similarity rather than by deterministic tier lookup, an error caught only when the customer escalates after missing a premium commitment.
- The handoff-loss pattern documents a support-context SLA override correctly noted by an intake bot but never propagated to the structured account record a billing agent queries when calculating breach penalties, resulting in an incorrectly-applied penalty the customer must dispute.
- The fabricated-cause pattern shows an agent generating a customer-facing apology citing a plausible breach cause ("system outage") that does not appear in the incident log, exposing the company to liability for a specific factual claim never actually verified.
- The clock-pause pattern documents SLA clocks paused based on status fields (e.g., "waiting on customer") rather than on verified causality, masking internal delays (waiting on engineering) and producing inflated SLA compliance metrics relative to actual customer-perceived wait time.

## Scope

- **Retrieval-based tier selection** — [Embedding-Retrieval Matches Wrong SLA-Tier Policy Document](failures/embedding-retrieval-matches-wrong-sla-tier-policy-document.md). SLA-tier document retrieved by embedding similarity across boilerplate language without first filtering by the account's contracted tier, defaulting to the dominant tier in the corpus.
- **Handoff information loss** — [Multi-Agent Handoff Drops Customer-Specific SLA Override Between Intake Bot and Billing Agent](failures/multi-agent-handoff-drops-customer-specific-sla-override-between-intake-bot-and-billing-agent.md). Intake bot negotiates an SLA override and records it in free text, but the structured account record passed to billing has no override field, so breach penalties are calculated against standard SLA.
- **Hallucinated breach cause** — [SLA Agent Fabricates Breach Root Cause in Customer Communication](failures/sla-agent-fabricates-breach-root-cause-in-customer-communication.md). Agent generates a customer-facing breach explanation citing a specific cause (outage, maintenance) without calling the incident-tracking tool to ground the explanation in the actual logged cause.
- **Status-field clock error** — [SLA Breach Blindness from Clock-Pause Errors](failures/sla-breach-blindness-from-clock-pause-errors.md). SLA clock paused/resumed based on status field (e.g., "waiting on customer") rather than on verified causality, masking internal delays and producing SLA compliance metrics that diverge from customer-perceived wait time.

## When SLA Management Matters

- An SLA-management system applies different response and resolution commitments based on customer account tier or service level
- SLA overrides are negotiated during support conversations and need to be propagated to compliance and billing systems
- An SLA-management agent generates customer-facing communications explaining breaches or late responses
- SLA clocks are paused when tickets are waiting on customer information, and resumed when customers respond
- Accuracy of SLA compliance reporting directly affects customer trust and regulatory or contractual obligations

## Cross-Pattern Insight

Every SLA-management pattern documented here reflects a gap between what the agent reasonably decides and what needs to be verified: a tier is selected by similarity when structural tier confirmation is needed, an override is noted in free text when structured account updates are needed, a cause is generated when a logged cause must be retrieved, and a clock state is managed by status when actual causality must be verified. The fix is standardized: pre-filter retrieval by structural tier confirmation, extend handoff schemas for task-relevant determinations, gate breach-cause generation on incident-tracking tool calls, and replace status-field-based clock logic with verified-causality logic.

## Frequently Asked Questions

### How do you apply the correct SLA tier to a ticket?
Use a deterministic lookup against the billing/contract system to resolve the account's contracted tier first, using that tier to select the applicable SLA document. Do not rely on free-text similarity to select the document. See [Embedding-Retrieval Matches Wrong SLA-Tier Policy Document](failures/embedding-retrieval-matches-wrong-sla-tier-policy-document.md).

### How do you prevent an SLA override from being lost between support and billing?
Add a structured, time-bound SLA-override field to the account record and require any support agent that negotiates an override to populate it directly, rather than leaving it only in a free-text conversation summary. See [Multi-Agent Handoff Drops Customer-Specific SLA Override Between Intake Bot and Billing Agent](failures/multi-agent-handoff-drops-customer-specific-sla-override-between-intake-bot-and-billing-agent.md).

### Should an SLA breach apology state a specific cause without verification?
No. Every cause statement in a customer-facing breach communication should be grounded in an incident-tracking tool call. Without a mandatory verification step, agents will generate plausible-sounding causes that may not match the actual logged cause, exposing the company to liability. See [SLA Agent Fabricates Breach Root Cause in Customer Communication](failures/sla-agent-fabricates-breach-root-cause-in-customer-communication.md).

### How reliable are SLA compliance metrics based on status-field clocks?
Not reliable. Status-field-based clock pause/resume logic measures what the system recorded, not what the customer actually experienced. Internal delays hidden by "waiting on customer" status inflate SLA compliance metrics. Dual reporting (status-based and actual-elapsed-time) reveals the gap. See [SLA Breach Blindness from Clock-Pause Errors](failures/sla-breach-blindness-from-clock-pause-errors.md).

## Patterns

| Pattern | Mechanism |
|---|---|
| [Embedding-Retrieval Matches Wrong SLA-Tier Policy Document](failures/embedding-retrieval-matches-wrong-sla-tier-policy-document.md) | SLA tier retrieved by boilerplate similarity without structural tier filtering |
| [Multi-Agent Handoff Drops Customer-Specific SLA Override Between Intake Bot and Billing Agent](failures/multi-agent-handoff-drops-customer-specific-sla-override-between-intake-bot-and-billing-agent.md) | Override negotiated in support; structured account record has no override field |
| [SLA Agent Fabricates Breach Root Cause in Customer Communication](failures/sla-agent-fabricates-breach-root-cause-in-customer-communication.md) | Breach cause generated without incident-tracking tool call to verify actual logged cause |
| [SLA Breach Blindness from Clock-Pause Errors](failures/sla-breach-blindness-from-clock-pause-errors.md) | Clock pause/resume based on status fields rather than verified causality, masking internal delays |

**Total: 4 patterns**

## Related Goals

- [Ticket Routing](../ticket-routing/) — upstream stage; routing determines which team and SLA tier apply
- [Issue Resolution](../issue-resolution/) — downstream stage; resolution time contributes to SLA compliance
- [Sentiment Escalation](../sentiment-escalation/) — orthogonal goal; escalations may change SLA priority
