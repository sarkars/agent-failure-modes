# Stale Training Knowledge Overrides Live Return-Policy Lookup

## Issue: A Support Agent With Access to a Live Policy-Lookup Tool That Returns the Company's Current Return/Refund Policy Terms States Policy Language That Instead Matches an Older Version of the Policy It Encountered Repeatedly During Training or in a Cached System Prompt, Despite the Tool Returning the Current, Revised Terms in the Same Conversation -- Telling a Customer They Have a Return Window or Refund Eligibility That No Longer Applies

**Frequency**: Common

**Symptoms**
- Agent quotes a specific return window, restocking fee, or refund-method rule to the customer that does not match the value returned by the policy-lookup tool in the same conversation
- Tool-call trace confirms the current policy was successfully retrieved and present in context immediately before the agent's response was generated
- The stated terms match an older, previously-published version of the policy rather than the version the lookup tool currently returns
- Customer disputes or escalates after attempting to act on the agent-stated terms and being told by a human agent or the order system that different terms actually apply
- The same outdated term recurs across multiple conversations handled by the same agent configuration, indicating a systematic default rather than an isolated mistake

**Example**
```
Company shortens its standard return window from 60 days to 30 days as part of a policy update, with the change reflected immediately in the policy-lookup tool
Customer asks the support agent, on day 45 after purchase, whether they can still return an item
Agent calls the policy-lookup tool, which correctly returns the new 30-day window
Agent's response to the customer: "You're within our 60-day return window, so you're welcome to send this back for a full refund" -- reflecting the policy as it existed before the recent change
Customer ships the item back expecting a refund; the returns team rejects it as outside the actual current window
Customer escalates, citing the agent's explicit statement as the basis for their return attempt
Review of the conversation's tool-call log confirms the 30-day figure was returned successfully; the agent's stated 60-day figure did not come from that result
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey of hallucination in LLM-based agents documents that models produce fluent, plausible-sounding content reflecting commonly-seen patterns even when a specific, correct grounding value was retrieved and available in context | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Failure-mode taxonomies for LLM systems identify silent substitution of a model's default or memorized knowledge for an available, contradicting tool result as a distinct and recurring failure category | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Tool-use error detection research finds agents do not reliably treat a successfully returned tool result as authoritative over their own generated content, producing responses inconsistent with the retrieved data | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- No explicit instruction requiring policy figures stated to the customer to be copied verbatim from the lookup tool's returned payload rather than composed from the model's general knowledge of the company's policies
- Policy change was incremental (a changed number, not a renamed policy), so the agent's fluent, confident phrasing gives no surface signal that it diverged from the tool result
- Older policy version appeared far more often in whatever material informed the agent's baseline behavior (training data, a stale cached system prompt, or prior conversation examples used for few-shot prompting) than the current version has had time to
- No automated check comparing policy figures stated to the customer against the tool-call result from the same conversation before the message is sent

---

## Mitigation Strategies

1. **Verbatim Policy-Figure Constraint**: Require any return window, fee, or refund-rule figure stated to the customer to be inserted directly from the policy tool's returned payload via template rather than composed by the model
2. **Post-Generation Policy Diff**: Automatically compare every policy figure in the outgoing message against the corresponding value in the same conversation's tool-call result and block sending on any mismatch
3. **Policy-Revision Recency Flag**: Have the policy tool surface a "last updated" marker in its response and require the agent to anchor its statement to that date rather than to memorized policy conventions
4. **Cached-Prompt Audit**: Periodically audit any system prompt or few-shot examples for outdated policy language that could compete with the live tool result, and remove stale figures from static prompt content

### Metrics
- Rate of customer-facing policy statements that do not exactly match the same-conversation tool-call result
- Number of customer escalations or failed return/refund attempts traceable to an agent-stated policy figure that did not match actual current policy
- Time elapsed between a policy change going live in the lookup tool and agent output reliably reflecting it

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Policy figure mismatch | Stated policy figure differs from the same-conversation tool-call result | P1 | Block message; route to human review before sending |
| Systematic stale-policy pattern | Same outdated figure appears across multiple conversations following a known policy change | P2 | Audit prompt and templates; reinforce verbatim constraint |
| Tool result unused | Tool-call trace shows a successful policy lookup with no corresponding reference in the outgoing message | P3 | Review generation pipeline for silent tool-result discard |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
