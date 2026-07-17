# Routing Failures

## Issue: Orchestrator Routes Task to Wrong Agent

**Frequency**: Common

**Symptoms**
- Tasks assigned to agents without required capabilities
- Specialist agents underutilized, generalist overloaded
- User queries bounced between agents
- Task completed but poorly due to wrong agent
- Routing decisions based on keywords, not semantics

**Root Cause**
Multi-agent systems rely on orchestrators to route tasks to appropriate specialist agents. When routing logic is naive (keyword matching), misconfigured, or the orchestrator misunderstands task requirements, tasks go to wrong agents. A complex financial analysis goes to a general assistant instead of the finance specialist. The task might still "complete" but with inferior quality.

**Example**
```
Scenario: Customer service multi-agent system

Available agents:
  - billing_agent: Handle invoices, payments, refunds
  - technical_agent: Debug issues, configuration help
  - sales_agent: Product info, upgrades, renewals
  - general_agent: Everything else

Customer query: "My bill seems wrong, I was charged for 
                 a feature I can't seem to access"

Routing logic: Keyword matching
  - "bill" → billing_agent
  - "feature" → sales_agent
  - "can't access" → technical_agent

Conflict resolution: First match wins

Result:
  Query routed to: billing_agent
  
Problem:
  - Billing agent only sees billing issue
  - Doesn't investigate access problem
  - Tells user "bill is correct"
  - User still can't access feature they're paying for
  
Correct routing:
  - Should go to technical_agent first
  - Discovers feature is broken (bug)
  - Then billing_agent for credit
  
Impact: Customer churns, negative review
```

**Key Statistics**
From Multi-Agent Research (2026):
- 25-35% of tasks routed to suboptimal agent
- Keyword-based routing accuracy: 60-70%
- Semantic routing accuracy: 85-95%
- Mis-routed tasks take 2-3x longer to resolve
- 41-86.7% of multi-agent systems fail (includes routing)

**Routing Failure Types**
| Type | Cause | Impact |
|------|-------|--------|
| Wrong specialist | Misunderstood task | Poor quality |
| Overloaded agent | No load balancing | Delays |
| Capability gap | No capable agent | Task failure |
| Circular routing | Agents bounce task | Infinite loop |
| Premature routing | Incomplete understanding | Rework |

**Contributing Factors**
- Keyword-only routing logic
- No semantic understanding of tasks
- Missing agent capability profiles
- No routing feedback loop
- Static routing rules
- No routing explainability

---

## Test Scenario & Reproduction

### Scenario Setup
- Customer service multi-agent system with `billing_agent`, `technical_agent`, `sales_agent`, and `general_agent`
- Router implemented as keyword matching with "first match wins" conflict resolution, no semantic or multi-intent classification
- No capability-boundary check on individual agents — each answers whatever reaches it rather than flagging out-of-scope elements

### Trigger Mechanism
1. Submit a compound query containing both a billing keyword and a technical/access issue
2. Let the keyword router scan for matches ("bill" -> billing_agent, "feature" -> sales_agent, "can't access" -> technical_agent) and apply first-match-wins
3. Observe which single agent receives the query and how it responds
4. Check whether the response addresses every component of the original query

**Example Reproduction Steps:**
```
1. Configure the router with keyword rules: "bill"->billing_agent, "feature"->sales_agent, "can't access"->technical_agent, first match wins
2. Submit the query: "My bill seems wrong, I was charged for a feature I can't seem to access"
3. Log which keyword matched first and which agent received the routed task
4. Capture billing_agent's response to the query
5. Compare the response against the full query text for topic coverage (billing vs. access/technical)
6. Check whether a re-route to technical_agent ever occurs
7. Simulate a follow-up contact from the same customer within 7 days and log it against the same_issue_recontact_rate metric
```

### Expected Failure State
- Query is routed entirely to billing_agent based on the first keyword match ("bill"), even though the root cause is a technical access bug
- billing_agent responds "bill is correct" without investigating or escalating the access problem, closing the ticket
- The customer's actual issue (feature inaccessible despite being charged) remains unresolved
- No compound-intent flag or re-routing occurs despite the query matching 2+ agent capabilities

---

## Mitigation Strategies

### Prevention
1. **Semantic multi-intent routing over keyword first-match**: The customer query "My bill seems wrong, I was charged for a feature I can't seem to access" contains both a billing keyword ("bill") and a technical issue, but "first match wins" keyword logic sent it entirely to billing_agent, missing the actual root cause. Replace keyword matching with embedding-based intent classification that can detect multiple co-occurring intents (billing + technical) in one query, matching the 85-95% semantic vs. 60-70% keyword accuracy gap cited in the stats. Trade-off: semantic routing requires an embedding model and capability-vector maintenance, adding infra and latency vs. a simple keyword lookup.
2. **Root-cause-first routing order for compound queries**: The example shows the correct order was technical_agent (diagnose the access bug) before billing_agent (issue credit), but keyword-first-match picked billing arbitrarily. For queries matching multiple agent capabilities, define an explicit resolution-order policy (e.g., diagnose-before-refund) rather than "first match wins," so compound issues route to the root-cause specialist first. Trade-off: requires maintaining an explicit precedence policy across every pair of overlapping capabilities, which grows combinatorially with agent count.
3. **Capability profiles that flag "requires escalation" cases**: billing_agent, on receiving this query, told the user "bill is correct" and stopped — it had no mechanism to recognize the query exceeded its capability (verifying feature access) and route onward. Give each agent an explicit capability boundary declaration and require it to check incoming queries against that boundary, escalating to routing rather than answering partially when out of scope. Trade-off: agents must be honest about their own limits, and an overly cautious boundary can cause excessive re-routing for queries the agent could actually have handled.

### Detection & Response
1. **Compound-intent detection at the entry point**: The failure mode here specifically involves one query with two independent problems (billing + access). Run intent classification that outputs a *set* of matched capabilities per query, not just a single winner, and flag any query matching 2+ agent capabilities for either multi-agent handling or the resolution-order policy rather than defaulting to first match.
2. **Resolution-doesn't-match-complaint check**: billing_agent's response ("bill is correct") didn't address the "can't access" part of the original query at all. Compare the closing response against the full original query for topic coverage, and flag responses that leave part of a compound query unaddressed as likely mis-routes.
3. **Churn/re-contact correlation**: The example's stated impact is customer churn and negative review after being told "bill is correct" while still unable to access the feature. Track re-contact rate on the same ticket/session within a short window after agent resolution as a lagging indicator of mis-routing, since a correctly-routed resolution shouldn't need a follow-up on the same underlying issue.

### Architecture Patterns
1. **Capability-profile-based semantic router with confidence scores**: Maintain detailed per-agent capability profiles (billing_agent: invoices/payments/refunds; technical_agent: bugs/config/access issues) and route via similarity between query embedding and capability profile embeddings, surfacing a confidence score so low-confidence routes (like this ambiguous compound query) get flagged rather than silently first-matched. Deployment consideration: capability profiles need active maintenance as agents' actual scope evolves, or the router drifts from reality.
2. **Sequential multi-agent handoff for compound queries**: For queries matching multiple capabilities (billing + technical here), route through technical_agent first to resolve the root cause, then automatically hand off to billing_agent for the credit — instead of picking one agent and terminating. Deployment consideration: needs the task-handoff machinery (from task-handoff-errors) to reliably pass context between the two agents, or the second hop loses information.
3. **Rerouting/escalation protocol as a first-class agent action**: Give billing_agent an explicit "this is outside my capability, re-route to technical" action it can invoke instead of answering "bill is correct" and closing the ticket — this directly prevents the dead-end resolution in the example. Deployment consideration: agents must be incentivized/prompted to use re-route rather than force an answer, since a forced complete-looking answer can look like better performance in naive metrics.

### Metrics
1. **routing_accuracy**: Target > 90% of tasks routed to the optimal agent on first attempt (above the 85-95% semantic-routing ceiling cited); Alert if < 75%.
2. **compound_query_detection_rate**: Target > 90% of queries with 2+ matching capabilities correctly flagged as multi-intent; Alert if < 70%.
3. **rerouting_rate**: Target < 15% of tickets requiring a second routing hop; Alert if > 30%, indicating first-pass routing logic is unreliable.
4. **same_issue_recontact_rate**: Target < 5% of resolved tickets generating a follow-up contact on the same underlying issue within 7 days; Alert if > 15%.

### Alerts
1. **Compound Intent Mis-Routed** (P2): Condition - a query classified as matching 2+ agent capabilities was routed to only one agent and marked resolved. Action: re-open the ticket, route to the unaddressed capability's agent, and log the original routing decision for the router's calibration review.
2. **Unaddressed Query Component** (P2): Condition - agent response does not semantically cover all detected intents in the original query (e.g., addresses billing but not access). Action: auto-flag for re-routing before the resolution is sent to the customer.
3. **High Recontact on Same Issue** (P3): Condition - same_issue_recontact_rate exceeds threshold for a given agent or routing path. Action: audit that agent's recent routing decisions and capability profile for gaps causing incomplete resolutions.

## References

- [MAST Taxonomy](https://arxiv.org/abs/2503.13657) - Multi-agent failure modes
- [Redis: Multi-Agent Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination issues
- [Augment Code: Multi-Agent Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - Routing patterns
- [Microsoft: Failure Modes in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Orchestration
- [Braintrust: Agent Observability](https://www.braintrust.dev/articles/agent-observability-complete-guide-2026) - Routing monitoring
