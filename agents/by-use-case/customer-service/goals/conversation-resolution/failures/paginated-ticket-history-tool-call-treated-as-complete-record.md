# Paginated Ticket-History Tool Call Treated as Complete Record

## Issue: A Support Agent That Calls a Tool to Retrieve a Customer's Prior Ticket or Interaction History to Decide Whether an Issue Is a First-Time Report or a Repeat Complaint Receives Only the First Page of a Paginated Result Set From the API, but Proceeds to Reason and Respond as if That First Page Were the Customer's Entire History, Reaching a Materially Wrong Conclusion About Repeat-Issue Status, Prior Promises Made, or Escalation Eligibility

**Frequency**: Common

**Symptoms**
- The ticket-history tool's raw response includes a `has_more: true` field or a `next_page_token`, but the agent's reasoning and reply make no reference to it and treat the returned page as the full history
- The agent tells a customer "I see this is the first time you've reported this issue" or "there's no record of a prior promise" when earlier tickets exist on a second or third page the agent never requested
- Customers who have, in fact, contacted support multiple times about the same issue report frustration at being treated as a first-time contact, sometimes repeatedly across separate sessions, each one only checking page one
- Escalation-eligibility logic that depends on counting prior contacts on the same issue undercounts systematically for customers with ticket histories longer than one page, since only the first page is ever inspected
- The tool-call log shows a single history-lookup call per conversation with no follow-up pagination call, even for customers known from other systems to have ticket counts well above the page-size limit

**Example**
```
Customer contacts support about a recurring billing glitch and the agent calls get_ticket_history(customer_id) to check for prior reports
The API returns the 10 most recent tickets (page 1 of 3) along with has_more: true, but the agent's prompt template only surfaces the ticket list itself, not the pagination metadata, into the reasoning context
Agent concludes "I don't see any prior tickets about this issue" and treats the complaint as new, offering a standard first-time-issue troubleshooting script
In fact, tickets 14 and 22 on page 2 -- outside the returned page -- show the customer reported the identical billing glitch twice before and was previously promised an escalation to engineering
Customer, now contacting support a third time about the same unresolved issue, receives the same first-time script again and explicitly says "I've already told you this twice," which the agent has no record of and cannot corroborate
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Agent-environment interaction failure research documents a specific real-world case where a lookup tool returns partial/paginated records by default and agents proceed with downstream tasks based on the incomplete result without recognizing the truncation | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |
| Failure-mode taxonomies for LLM systems identify incorrect tool invocation -- including consuming a tool's output without accounting for its actual scope or completeness -- as a distinct, recurring category of production failure | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The prompt template that injects tool results into the agent's context surfaces only the list of returned items, dropping pagination metadata (`has_more`, `next_page_token`, total count) that would signal the result is partial
- The agent has no standing instruction or automated check requiring it to request additional pages before drawing a conclusion that depends on completeness, such as "is this a repeat issue"
- Default page sizes on the ticket-history API are small relative to the ticket volume of long-tenured or frequently-contacting customers, making truncation common for exactly the customers where history matters most
- No deterministic, non-LLM completeness check cross-references the returned ticket count against a known total before the agent's repeat-issue or escalation-eligibility determination is finalized

---

## Mitigation Strategies

1. **Pagination-Aware Context Injection**: Always surface pagination metadata (`has_more`, total count, current page) into the agent's reasoning context alongside the returned items, not just the item list itself
2. **Mandatory Full-Fetch for Completeness-Dependent Decisions**: For any determination that depends on a complete history (repeat-issue status, prior-promise lookup, escalation eligibility), require the agent or an orchestration layer to fetch all pages before concluding, rather than accepting partial results
3. **Deterministic Completeness Gate**: Add a non-LLM check that compares the number of tickets retrieved against a known total count (from a separate lightweight count endpoint) and blocks repeat-issue conclusions until they match
4. **Truncation-Aware Prompting**: Explicitly instruct the agent that a `has_more: true` or unset total-count field means the result is incomplete, and require it to state that uncertainty to the customer rather than asserting a negative ("no prior tickets") from a partial result

### Metrics
- Rate of ticket-history tool calls where `has_more` is true but no follow-up pagination call occurs in the same conversation
- Rate of customer-reported "I already told you this" follow-ups within 30 days of a conversation where the agent concluded "first-time issue"
- Average number of pages fetched per history lookup, segmented by customer tenure/contact-frequency tier

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unacknowledged pagination truncation | Tool response includes `has_more: true` and the agent's reply asserts a completeness-dependent conclusion (e.g., "first time," "no prior promise") | P1 | Block the reply; force additional page fetch before resuming |
| Repeat-issue undercount drift | Escalation-eligibility repeat-contact counts trend below counts derived from the raw ticketing database for the same customers | P2 | Audit pagination handling in the history-lookup integration |
| Recurring same-issue complaint within 30 days | Customer re-contacts about an issue the agent previously called "first-time" within 30 days | P2 | Route to senior agent with full, manually-verified ticket history attached |

---

## References

- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
