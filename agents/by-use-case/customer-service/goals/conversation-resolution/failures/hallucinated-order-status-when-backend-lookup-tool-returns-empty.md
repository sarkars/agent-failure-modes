# Hallucinated Order Status When Backend Lookup Tool Returns Empty

## Issue: When a Support Agent's Call to the Order/Account-Status Lookup Tool Returns an Empty or Partial Result -- Because the Order ID Was Entered With a Formatting Variation, or the Backend Service Timed Out -- the Agent States a Specific, Plausible-Sounding Order Status (e.g., "Your Order Shipped Yesterday and Should Arrive by Friday") That It Composed to Fill the Gap, Rather Than Telling the Customer the Lookup Failed and Escalating or Retrying

**Frequency**: Common

**Symptoms**
- Agent's response to the customer states a specific status, date, or tracking detail that does not appear anywhere in the tool-call result for that conversation
- Tool-call trace shows the lookup returned empty, null, or a partial/malformed payload immediately before the agent generated its status claim
- Customer follow-up ("that doesn't match what I see in my account") or a subsequent successful lookup reveals the stated status was fabricated rather than retrieved
- The fabricated detail is plausible and internally consistent (a believable shipping date, a believable carrier) rather than an obviously wrong placeholder, making it hard for the customer or a reviewing agent to catch without independently checking the backend
- Customer takes action based on the false status (stops checking, tells a third party an arrival date) before the discrepancy surfaces

**Example**
```
Customer asks "where is my order #A1029384" in a chat session
Agent calls the order-status tool with the order ID as typed; a trailing-space formatting difference causes the backend to return an empty result set
Tool-call log shows: result: [] -- no matching order found
Agent's response to the customer: "Your order shipped yesterday via ground carrier and is expected to arrive within 2-3 business days"
Customer waits the stated window, then contacts support again when nothing arrives
Second agent's lookup (with the formatting issue manually corrected) shows the order is still in fulfillment, not yet shipped
Review of the first conversation's tool-call trace confirms the original lookup returned no data at all -- the shipping date and carrier were invented to produce a complete-sounding answer
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey of hallucination in LLM-based agents documents that models fabricate plausible-sounding content to fill gaps left by failed, empty, or incomplete tool calls rather than surfacing the gap as a failure | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds dialogue agents frequently do not treat a null or empty tool result as a distinct failure signal, instead proceeding to generate a response as if a meaningful result had been returned | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Execution-provenance research for LLM agents argues traceable evidence linking a generated claim to the actual tool output it purports to reflect is necessary because models do not reliably self-report when a stated fact lacks real grounding | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- No explicit instruction distinguishing an empty/failed tool result from a result the agent is free to compose plausible content around
- Order-ID formatting variations (whitespace, dashes, case) are common and the lookup tool fails silently rather than returning a distinct "not found due to format" versus "not found, no such order" signal
- Agent's response-generation step is not constrained to quote only fields actually present in the tool's returned payload
- No customer-facing distinction between a confirmed status (from a successful lookup) and one the agent is otherwise generating, so the customer has no way to tell a guess from a fact

---

## Mitigation Strategies

1. **Hard Stop on Empty Lookup Result**: Require the agent to tell the customer the lookup did not return a result and either retry with format normalization or escalate, rather than composing a status to fill the gap
2. **Verbatim Field Constraint**: Require any status, date, or tracking detail stated to the customer to be copied directly from the tool's returned payload, with no field invented or inferred by the model
3. **Format-Normalization Retry**: Automatically retry the lookup with common ID-formatting normalizations (trimming whitespace, stripping separators) before surfacing a "not found" result, reducing the empty-result rate that triggers the fabrication risk
4. **Confirmed-vs-Generated Labeling**: Internally flag any customer-facing claim not traceable to a specific tool-result field, enabling automated review of conversations containing unconfirmed factual claims

### Metrics
- Rate of customer-facing status claims with no corresponding field in the same conversation's tool-call result
- Number of customer follow-up contacts attributable to a previously stated status not matching actual backend status
- Empty/null tool-result rate before and after format-normalization retry logic

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unconfirmed status claim | Customer-facing message states a status/date/tracking detail absent from the tool-call result | P1 | Flag conversation for review; issue correction to customer |
| Empty lookup with confident response | Tool result is empty/null but agent response contains no escalation or retry language | P1 | Block response; force retry or escalation path |
| Repeated format-failure pattern | Same order-ID formatting issue causes repeated empty lookups across conversations | P3 | Fix backend lookup normalization |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
