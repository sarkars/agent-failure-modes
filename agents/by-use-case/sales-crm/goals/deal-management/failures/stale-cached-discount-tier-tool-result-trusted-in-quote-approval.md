# Stale Cached Discount-Tier Tool Result Trusted in Quote Approval

## Issue: A Deal-Management Agent Calls an Internal Pricing/Discount-Approval Tool to Check the Maximum Discount an AE Can Approve Without Escalation, the Tool Returns a Cached Result from Before a Discount-Policy Change Took Effect, and the Agent Approves a Quote at a Discount Level That No Longer Qualifies for Auto-Approval

**Frequency**: Occasional

**Symptoms**
- Quotes are auto-approved at a discount percentage that exceeds the AE's current auto-approval ceiling, discoverable by comparing the approval against the pricing system's authoritative, current policy rather than the cached value the agent's tool call returned
- The error clusters tightly around the time window immediately following a discount-policy change, then disappears once the cache underlying the pricing tool naturally expires or is invalidated
- Tool-call logs show the pricing/discount-tier lookup returning a response with a cache timestamp older than the most recent policy change, while the agent's approval narrative treats the returned ceiling as current without checking the cache timestamp
- Deals auto-approved during the stale-cache window show a discount distribution inconsistent with deals approved just before or after the window, spiking at exactly the old (now-superseded) ceiling value
- Finance/deal-desk reconciliation catches a batch of under-margin deals weeks later when the quarter's discount-to-margin report is run, well after the quotes have already gone to customers

**Root Cause**
The discount-approval tool's response is cached for performance reasons, and the cache invalidation is not tightly coupled to discount-policy change events; the agent receiving the tool's response has no way to distinguish a freshly computed ceiling from a stale cached one unless the response explicitly carries and the agent explicitly checks a freshness timestamp. Because the cached response is syntactically identical to a fresh one, the agent's approval logic -- which treats any successful tool response as authoritative -- proceeds to approve quotes against a ceiling value that the business has already retired.

**Example**
```
Pricing team updates the auto-approval discount ceiling for the enterprise segment from 15% to 10%, effective immediately, due to a margin-compression directive
Deal-management agent's pricing tool call for a new quote returns a cached response (computed before the policy change) still showing the 15% ceiling, because the cache TTL had not yet expired
Agent approves a 14% discount quote as within auto-approval limits, citing the tool's returned ceiling, with no check of the response's cache timestamp against the policy-change effective date
Quote is sent to the customer before deal-desk catches the discrepancy in a routine margin review two weeks later, by which point renegotiating the discount with the customer is commercially costly
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Errors in agentic tool-use pipelines commonly originate from stale memory or stale tool outputs flowing into subsequent agent decisions without being flagged as outdated | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |
| Agents frequently misinterpret or fail to validate a tool's actual returned state, treating any successfully returned payload as authoritative regardless of its freshness | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Calibration and verification gaps in tool-using agents are particularly acute when the tool's own internal state (such as a cache) can diverge from the authoritative source it is meant to represent | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |

**Contributing Factors**
- Pricing/discount-tool cache invalidation is not event-coupled to discount-policy change announcements, leaving a window where cached and authoritative values diverge
- Tool response does not surface a freshness timestamp prominently enough for the agent's approval logic to check it before treating the returned ceiling as current
- No automated reconciliation compares auto-approved discount levels against the authoritative, current policy ceiling on a near-real-time basis, relying instead on a periodic finance review

---

## Mitigation Strategies

1. **Event-Coupled Cache Invalidation on Policy Change**: Invalidate the discount-tool's cache immediately and synchronously whenever a discount-policy change is published, rather than relying on a time-based TTL that can lag a policy update
2. **Mandatory Freshness Check Before Approval**: Require the agent's approval logic to explicitly check the tool response's freshness timestamp against the known last-policy-change date before treating the returned ceiling as authoritative, blocking approval on a stale or ambiguous timestamp
3. **Real-Time Reconciliation Against Authoritative Policy Source**: Run a near-real-time automated check comparing every auto-approved discount against the authoritative current policy ceiling (not the cached tool response), flagging any approval that would not have qualified under the current policy
4. **Approval Hold During Known Policy-Change Windows**: Automatically place a short hold on auto-approvals immediately following a published discount-policy change until cache invalidation is confirmed, rather than allowing approvals to proceed on a best-effort cache-refresh timeline

### Metrics
- Rate of auto-approved discounts that exceed the authoritative current policy ceiling, detected via real-time reconciliation
- Time lag between a discount-policy change being published and the pricing tool's cache reflecting the new ceiling
- Dollar margin impact of quotes approved during a stale-cache window before correction

### Alerts
- Real-time reconciliation finds an auto-approved discount exceeding the current authoritative policy ceiling → P1
- Pricing tool cache timestamp found older than the most recent published discount-policy change during an active approval → P2
- A discount-policy change is published without a corresponding cache-invalidation event firing within the defined SLA → P3

---

## References

- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
