# Stale Training Knowledge of Reorganized Product-Line Taxonomy

## Issue: A Ticket-Routing Agent Maps a Ticket's Product Category to a Specialist Queue Using a Product-Line-to-Team Mapping It Recalls From Pretraining, Even Though That Mapping Has Since Been Reorganized Through a Team Merge, Split, or Product Rename, Despite a Live Org-Taxonomy Lookup Tool Being Available That Would Surface the Current Mapping

**Frequency**: Occasional

**Symptoms**
- A ticket is routed to a specialist queue that no longer handles that product line, because the queue's responsibilities were split or merged into a different team after the agent's training cutoff
- Querying the agent's available org-taxonomy lookup tool directly, for the same product line, surfaces the current team mapping that the routing decision relied on the old mapping instead of checking
- The agent's stated rationale, when asked why it chose a given queue, cites a team name or product-to-team mapping without referencing a dated taxonomy source, consistent with recalling a memorized org structure rather than confirming a current one
- The gap is most visible for product lines whose owning team has been reorganized after the agent's training cutoff, since those are the only cases where the stale and current mappings diverge
- The receiving (wrong) queue catches the misroute only after reviewing the ticket and finding it has no current ownership of that product line, adding a full re-route cycle of delay

**Root Cause**
The agent's parametric knowledge of which team owns a given product line reflects whatever organizational structure was in effect up to its training cutoff, and absent an explicit instruction to verify the mapping against the org-taxonomy lookup tool before finalizing a routing decision, the model defaults to the more fluent path of routing from a memorized team mapping. Because the lookup tool is available but not invoked, the routing decision is produced with no contradiction surfaced, leaving a stale organizational mapping driving a ticket-routing decision with direct downstream consequences for response time.

**Example**
```
Customer submits a ticket about the "Reporting Dashboard" product line
Routing agent recalls from training that Reporting Dashboard tickets go to the "Analytics Team" queue and routes it there without invoking the org-taxonomy lookup tool it has access to
Querying that same tool, after the fact, shows the Analytics Team was dissolved in a reorganization and Reporting Dashboard ownership was absorbed into the "Platform Team" queue
Analytics Team queue (now repurposed for an unrelated function) reviews the ticket, finds no current ownership of Reporting Dashboard, and re-routes it to Platform Team
Customer experiences a full extra queue cycle of delay before reaching the team that actually owns the product line
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of knowledge-oriented retrieval-augmented generation identify that retrieval tools are only effective at correcting stale parametric knowledge when invocation is mandatory for the relevant query type, since optional invocation is frequently skipped when the model's memorized answer is fluent | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Hybrid AI-router research finds that routing decisions grounded in a stale or unverified mapping of categories to handling teams produce systematically different, and measurably worse, outcomes than routing decisions checked against a current, structured mapping | [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on parametric or cached knowledge alone causes organizational or structural updates to go unincorporated in long-running deployments | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- No ticket-routing workflow rule requires an org-taxonomy lookup specifically before finalizing a routing decision based on a product-to-team mapping
- The agent's parametric knowledge of the team mapping is fluent and confident enough to produce a complete, well-formed routing decision without surfacing any uncertainty that would prompt a lookup
- The org-taxonomy lookup tool is available but optional, with no enforcement distinguishing "mapping was checked and confirmed current" from "mapping was never verified"

---

## Mitigation Strategies

1. **Mandatory Org-Taxonomy Lookup for Routing Decisions**: Require any routing decision based on a product-to-team mapping to trigger an org-taxonomy lookup before the decision is finalized, regardless of the agent's parametric confidence
2. **Date-Stamped Mapping Citation Requirement**: Require any routing decision to cite the specific, dated org-taxonomy source the team mapping relies on, making staleness visible to reviewers rather than implicit
3. **Tool-Invocation Audit on Routing Decisions**: Automatically flag any finalized routing decision where the session log shows no org-taxonomy lookup tool call, routing it to human quality review before the ticket reaches the destination queue
4. **Reorganization-Flag Propagation**: When a team is merged, split, or renamed in the org-taxonomy system, require an active check that blocks any cached or memorized version of the prior mapping from being used in routing decisions going forward

### Metrics
- Rate of finalized routing decisions with no corresponding org-taxonomy lookup tool call in the session log
- Rate of discrepancies found when re-checking cached product-to-team mappings against current org-taxonomy documentation
- Re-route rate attributable to tickets routed under a since-reorganized team mapping

### Alerts
- A finalized routing decision relies on a product-to-team mapping with no org-taxonomy lookup call in the session → P1
- An org-taxonomy lookup, when invoked, returns a mapping that contradicts a cached mapping still in active use → P1
- Re-route rate attributable to stale team mappings exceeds the defined threshold for a rolling window → P2

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Toward Super Agent System with Hybrid AI Routers](https://arxiv.org/pdf/2504.10519)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
