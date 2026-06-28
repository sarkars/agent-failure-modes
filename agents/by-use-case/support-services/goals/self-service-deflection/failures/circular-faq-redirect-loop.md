# Circular FAQ Redirect Loop

## Issue: Self-Service Deflection Agent Routes a Customer Through a Closed Loop of FAQ Articles That Each Point Back to One Another, Never Reaching a Resolution or a Human Handoff

**Frequency**: Common

**Symptoms**
- Customer is shown FAQ Article A, clicks "this didn't help," and is shown Article B, which re-links to Article A or to a third article that loops back to B
- Session transcripts show 3+ consecutive "not helpful" feedback clicks on different articles addressing the same underlying intent
- Deflection rate metrics look artificially healthy because each article view counts as a "self-service interaction," masking that no actual resolution occurred
- Customers abandon the session without escalating, then re-contact through a different channel (phone, email) minutes to hours later with the same unresolved issue
- Knowledge-base graph analysis reveals strongly-connected clusters of articles with no terminal "escalate to agent" exit node reachable from common entry points

**Root Cause**
Self-service deflection agents typically select the "next best article" based on semantic similarity to the customer's restated query rather than tracking the path already traversed in the session. When the knowledge base contains near-duplicate or cross-referencing articles (common after iterative content updates by different authors), the recommender has no mechanism to detect that it is revisiting previously shown content under a different title, and no built-in maximum-hop or path-diversity constraint that would force an escalation after repeated non-resolution.

**Example**
```
Customer: "My payment failed but I was still charged"
Agent shows: "Troubleshooting Failed Payments" (Article A) -- closes with "see Billing Discrepancies"
Customer clicks "not helpful"
Agent shows: "Billing Discrepancies and Refunds" (Article B) -- closes with "see Troubleshooting Failed Payments"
Customer clicks "not helpful"
Agent re-shows: "Troubleshooting Failed Payments" (Article A), now framed as a "related article" recommendation
Customer abandons the chat, calls support 40 minutes later, repeats the same issue from scratch
```

**Key Statistics**
- Failure taxonomies for platform-orchestrated agentic workflows document "infinite loop without termination condition" as a recurring orchestration-layer failure mode distinct from any single model's response quality
- Self-service deflection programs that measure success purely by "no escalation" rather than confirmed resolution have been shown in customer-service research to overstate effective deflection by conflating session abandonment with issue resolution
- Knowledge-base maintenance studies find that cross-referencing article networks without a maintained "shortest path to resolution" structure are a primary driver of redundant, unresolved support contacts

**Contributing Factors**
- Knowledge base authored incrementally by multiple teams without a canonical "see also" graph review
- No session-level state tracking which article IDs have already been shown
- Deflection success metric defined as "no live-agent click" rather than "customer-confirmed resolved"

---

## Mitigation Strategies

1. **Path Memory in Session State**: Track the set of article IDs already surfaced in the session and exclude them (and their immediate "see also" targets) from re-recommendation
2. **Hop-Limit Escalation Trigger**: Force escalation to a human agent or live-chat handoff after a fixed number (e.g., 2) of consecutive "not helpful" responses on distinct articles addressing the same detected intent
3. **Knowledge-Graph Cycle Detection**: Periodically run cycle detection over the article cross-reference graph and flag closed loops with no terminal escalation node for content-team remediation
4. **Resolution-Confirmed Deflection Metric**: Redefine the primary self-service success metric to require explicit customer confirmation of resolution, not merely the absence of an escalation click

### Metrics
- Rate of sessions revisiting a previously shown article ID within the same session
- Ratio of "deflected" sessions followed by a repeat contact on the same issue within 24 hours
- Average hop count to resolution vs. hop count to abandonment, segmented by intent category

### Alerts
- Same article ID re-surfaced within a single session → P3
- Repeat-contact-after-deflection rate exceeds baseline by a defined margin for a given intent category → P2
- Cycle detection finds a closed loop reachable from a top-20-volume entry article → P2

---

## References

- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Information Freshness & Chatbots](https://arxiv.org/abs/2109.12771)
- [Knowledge Base Maintenance & QA](https://arxiv.org/abs/2104.04535)
