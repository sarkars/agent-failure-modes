# Embedding Retrieval Misroutes Ticket via Similarity to Wrong Product-Line Taxonomy Node

## Issue: A Ticket-Routing Agent That Classifies an Incoming Ticket's Product Category by Embedding Similarity Against a Product-Taxonomy Description Index, Rather Than Against the Account's Actual Provisioned Product List, Matches the Ticket to a Superficially Similar but Incorrect Product Line, Routing It to a Specialist Queue That Cannot Resolve the Customer's Actual Issue

**Frequency**: Frequent

**Symptoms**
- The ticket is routed to a specialist queue for a product line the customer's account has never actually been provisioned for, while the correct product line's queue never sees the ticket
- The ticket's description text uses generic terminology ("sync error," "connection timeout") that matches the taxonomy description of an unrelated product line more closely than it matches the actual provisioned product's taxonomy entry
- Cross-referencing the ticket's account ID against the account's actual provisioned product list, rather than matching ticket text to taxonomy descriptions, shows definitively which product line the ticket should belong to
- The misroute concentrates on product lines with overlapping generic terminology in their taxonomy descriptions, such as different sync, integration, or connectivity features that share similar troubleshooting vocabulary across otherwise unrelated products
- The misroute is caught only after the receiving specialist queue reviews the ticket, finds the account has no record of the product in question, and re-routes it, adding a full round-trip of queue wait time

**Root Cause**
Classifying a ticket's product category by matching its description text against a taxonomy index via embedding similarity optimizes for textual similarity to a taxonomy node's description, not for confirming that the customer's account actually has that product provisioned. When generic troubleshooting terminology overlaps across multiple product lines' taxonomy descriptions, the similarity signal cannot distinguish "this ticket's language resembles Product A's typical issues" from "this ticket is actually about Product A," especially when the account's own provisioning data, which would resolve the ambiguity directly, is never consulted.

**Example**
```
Customer's account is provisioned only for "TeamSync" (a calendar-synchronization product); they submit a ticket reading "getting a sync error every time I try to connect, please help"
Routing agent classifies the ticket via embedding similarity against the full product taxonomy, and "DataConnect" (a database-replication product with taxonomy description language heavily featuring "sync error" and "connect") scores as the closest textual match
Ticket routes to the DataConnect specialist queue
DataConnect specialist reviews the ticket, finds the account has no DataConnect provisioning at all, and re-routes it to the correct TeamSync queue
Customer experiences a full extra queue cycle of delay before reaching a specialist who can actually address the calendar-sync issue
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Retrieval-augmented and similarity-based classification systems are documented to surface a taxonomy of retrieval errors distinct from generation errors, including matching a topically similar but substantively wrong category when similarity search is used in place of structured-data confirmation | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| CRM task-capability benchmarks for LLM agents identify ticket-routing accuracy as a distinct, measurable capability separate from general response-generation quality, with routing errors traced to inadequate grounding in account-specific structured data | [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2) |
| Business-scenario evaluations of LLM agents in CRM-adjacent tasks identify reliance on account-specific structured data, rather than free-text similarity alone, as a distinct reliability requirement for routing tasks | [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878) |

**Contributing Factors**
- Product-category classification is performed via similarity search over taxonomy description text rather than by cross-referencing the account's actual provisioned product list
- No validation step confirms the classified product line appears in the account's provisioning record before the ticket is routed
- Product lines with overlapping generic troubleshooting vocabulary in their taxonomy descriptions are not flagged for mandatory provisioning-record confirmation before similarity-based classification is trusted

---

## Mitigation Strategies

1. **Provisioning-Record Confirmation as Primary Path**: Require ticket routing to cross-reference the account's actual provisioned product list first, restricting taxonomy-similarity matching to only the products the account actually has, rather than matching against the full, unrestricted taxonomy
2. **Block Routing to Unprovisioned Product Lines**: Prohibit a ticket from routing to a specialist queue for a product the account's provisioning record shows it does not have, regardless of how closely the ticket's text matches that product's taxonomy description
3. **Overlapping-Terminology Taxonomy Review**: Identify product-line pairs with high taxonomy-description term overlap and either disambiguate their descriptions or flag tickets potentially matching either for mandatory account-provisioning confirmation before routing
4. **Surface Classification Basis in Routing Output**: Require any routing decision to indicate whether the product-line classification was confirmed against the account's provisioning record or based on taxonomy-similarity alone, so receiving queues can prioritize verification accordingly

### Metrics
- Rate of routed tickets where the classified product line does not appear in the account's provisioning record
- Rate of tickets re-routed by a receiving specialist queue due to the account having no record of the originally classified product
- Average added queue-wait time attributable to provisioning-mismatch re-routes

### Alerts
- A ticket routes to a specialist queue for a product line absent from the account's provisioning record → P2
- Provisioning-mismatch re-route rate exceeds the defined threshold for a rolling window → P3
- Overlapping-terminology product-line pairs show a sustained elevated misroute rate after taxonomy review → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2)
- [CRMArena-Pro: Holistic Assessment of LLM Agents Across Diverse Business Scenarios and Interactions](https://arxiv.org/abs/2505.18878)
