# Multi-Agent Context Broadcast Waste

## Issue: A Coordinator Broadcasts Full Shared Context/History to Every Sub-Agent Regardless of Relevance, Multiplying Token Cost by Agent Count

**Frequency**: Common

**Symptoms**
- Adding a Nth sub-agent to a multi-agent workflow increases total token cost by more than 1/N of the prior total, i.e., cost scales faster than agent count
- Sub-agents receive the full shared task context, prior agents' outputs, and conversation history regardless of whether their specific role needs most of it
- Synchronization/coordination overhead (re-sending shared state to every agent after each step) dominates total spend in workflows with many agents or many steps
- No per-agent relevance filtering exists; the coordinator's broadcast payload is identical for every sub-agent regardless of role

**Root Cause**
In naive multi-agent orchestration, a coordinator re-sends the full shared context (task description, all prior sub-agents' outputs, running history) to every sub-agent at every step, so that each agent has complete situational awareness. This is a natural default because it's simple to implement and never risks an agent missing needed information. But because this broadcast happens for every agent at every step, and each broadcast recomputes/resends the same accumulating shared state to everyone, total synchronization cost scales multiplicatively in the number of agents, the number of steps, and the size of the shared artifact being synchronized — not additively in agent count as engineers often assume when estimating multi-agent cost.

**Example**
```
3-agent research-and-writing pipeline (researcher, analyst, writer),
5 coordination steps, shared context growing to 4,000 tokens by the
final step.

Naive broadcast: at each step, the coordinator resends the full current
shared context (up to 4,000 tokens) to all 3 agents, regardless of
whether a given agent's role needs the full history or just its own
relevant slice.

Total broadcast tokens across 5 steps x 3 agents, with shared context
size growing each step (500, 1200, 2000, 2900, 4000 tokens):
  Step 1: 500 x 3 = 1,500
  Step 2: 1,200 x 3 = 3,600
  Step 3: 2,000 x 3 = 6,000
  Step 4: 2,900 x 3 = 8,700
  Step 5: 4,000 x 3 = 12,000
  Total: 31,800 tokens of broadcast alone (excluding each agent's own
  generation)

A single-agent version of the same task, with no synchronization
overhead, would need only the final 4,000-token context once: an 87%
reduction relative to the broadcast total. Going from 3 to 6 agents on
this same workflow does not double the broadcast cost — it roughly
quadruples it, since both agent count and shared-context size multiply
against each other.
```

**Contributing Factors**
- No per-agent-role context scoping; every sub-agent is treated as needing the same full context as the coordinator itself
- Shared state is re-transmitted in full at every synchronization point rather than incrementally (only the delta since an agent's last update)
- Adding agents to a pipeline is assumed to scale cost linearly, so the actual multiplicative growth from broadcast-heavy architectures goes unnoticed until costs are audited
- No mechanism distinguishes "this agent needs the full history" from "this agent only needs its own task slice plus the immediately-prior agent's output"

---

## Test Scenario & Reproduction

### Scenario Setup
- A multi-agent pipeline with a coordinator broadcasting full shared context to all sub-agents at every step
- Shared context grows across steps as agents contribute output
- No per-role context scoping or incremental (delta-only) synchronization exists

### Trigger Mechanism
1. Run the pipeline with N agents and measure total broadcast tokens across all coordination steps
2. Re-run the same workflow with N+3 agents (holding task complexity constant) and measure the new total
3. Compare the actual cost scaling factor against the naively-expected linear-in-agent-count scaling

**Example Reproduction Steps:**
```
1. Configure a 3-agent pipeline (researcher, analyst, writer) with 5
   coordination steps and full-context broadcast at each step
2. Log the shared-context size at each step and the number of agents
   receiving it
3. Compute total broadcast tokens = sum over steps of (context_size_at_step
   x num_agents)
4. Re-run with 6 agents on an equivalent task, keeping the same growth
   pattern in shared context size
5. Compare the 3-agent and 6-agent total broadcast token counts
6. Compute the actual scaling factor (expected 2x for linear scaling;
   compare against the observed factor)
```

### Expected Failure State
- Total broadcast tokens for the 6-agent run exceed 2x the 3-agent run's total (the naively-expected linear scaling), confirming multiplicative rather than additive cost growth
- A large share of each broadcast payload is provably irrelevant to a given receiving agent's specific role (e.g., the writer agent receiving the researcher's full raw search results rather than a distilled brief)
- No incremental/delta-based synchronization exists; every step resends the full accumulated shared context rather than only what changed since the last broadcast to that agent
- No per-agent-role scoping configuration exists to test against as an alternative

---

## Mitigation Strategies

### Prevention
1. **Per-role context scoping**: Define, for each agent role in the pipeline, the minimum context slice it actually needs (e.g., the writer needs the analyst's summary, not the researcher's raw search results) and broadcast only that scoped slice rather than the full shared state to every agent uniformly. Trade-off: requires upfront design work to determine each role's actual information needs, and an overly narrow scope risks an agent missing context it later turns out to need.
2. **Incremental/delta synchronization instead of full re-broadcast**: At each coordination step, send only what has changed since an agent's last update (the delta) rather than the full accumulated shared context, directly addressing the multiplicative growth pattern in the example. Trade-off: delta-based sync requires tracking per-agent "last seen" state, adding coordination complexity versus the simplicity of always sending everything.
3. **Compact status snapshots instead of full artifact broadcast**: Maintain a per-agent registry of compact status summaries (task description, key decisions, partial-output summary) rather than full transcripts/outputs, and broadcast the compact snapshot by default, with full artifacts fetched on demand only when an agent's task genuinely requires them. Trade-off: summarization of status snapshots adds a processing step and risks omitting a detail a receiving agent later needs in full.

### Detection & Response
1. **Cost-scaling-versus-agent-count audit**: Track total pipeline cost as agent count changes (when scaling a pipeline up or down) and compare the observed scaling factor against the naive linear-in-agent-count expectation; a consistently super-linear factor is the direct signature of broadcast waste.
2. **Per-agent-relevance sampling**: Periodically sample broadcast payloads received by each agent role and estimate what fraction of the payload was actually referenced in that agent's subsequent output, similar to a context-utilization check; low utilization for a specific role indicates its context scope is too broad.
3. **Synchronization-cost-share monitoring**: Break down total pipeline cost into "agent generation cost" versus "broadcast/synchronization cost"; a synchronization share that grows disproportionately as pipeline steps or agent count increase indicates the broadcast mechanism itself, not the agents' actual work, is driving cost growth.

### Architecture Patterns
1. **Lazy invalidation / coherence-protocol-style synchronization**: Adapt cache-coherence-style protocols (mapping "which agents hold a stale copy of shared state" the way a multiprocessor cache tracks stale cache lines) so that shared artifacts are only re-synchronized to agents that actually need the updated version for their next step, rather than broadcasting unconditionally to all agents at every step — this converts the multiplicative broadcast-cost scaling into a scaling closer to (agent count + update count) rather than (agent count x step count x artifact size). Deployment consideration: requires tracking per-agent staleness/versioning of shared artifacts, adding coordination-layer complexity.
2. **Dynamic attentional context scoping**: Give each agent a registry entry containing only its compact status, its own task description, and relevant steering exchanges, with full context fetched into a per-agent "focus session" only when that agent's current step demonstrably requires it, rather than a single shared broadcast channel used by every agent identically. Deployment consideration: requires an explicit mechanism for an agent to request expanded context when its default scoped view proves insufficient.
3. **Hub-and-spoke summarized handoff instead of full mesh broadcast**: Route inter-agent information through a coordinator that summarizes each agent's output before passing it downstream (rather than every agent seeing every other agent's full raw output), so payload size stays bounded by the summary length rather than accumulating raw outputs from every prior agent. Deployment consideration: summarization at each handoff adds a processing step and risks losing detail that a downstream agent needed verbatim.

### Metrics
1. **broadcast_cost_scaling_factor**: Target ≤ 1.3x per additional agent (near-linear); Alert if > 2x per additional agent (matching the example's observed quadrupling from 3 to 6 agents).
2. **per_agent_context_utilization_rate**: Target > 40% of broadcast payload referenced in the receiving agent's output; Alert if < 10% for a given role.
3. **synchronization_cost_share_of_total**: Target < 30% of total pipeline cost attributable to broadcast/synchronization rather than agent generation; Alert if > 60%.
4. **stale_broadcast_avoided_rate**: Once incremental sync is implemented, target > 70% of synchronization events skip agents with no relevant update; Alert if < 20% (indicating the delta/lazy-invalidation mechanism isn't engaging).

### Alerts
1. **Superlinear-Cost-Scaling-On-Agent-Count-Increase** (P2): Condition - broadcast_cost_scaling_factor exceeds 2x for an added agent in a pipeline. Action: review whether per-role context scoping or delta-based synchronization is implemented for that pipeline.
2. **Low-Context-Utilization-By-Role** (P3): Condition - per_agent_context_utilization_rate for a specific role falls below 10% over a rolling week. Action: narrow that role's broadcast scope to its actual demonstrated information needs.

## References

- [Token Coherence: Adapting MESI Cache Protocols to Minimize Synchronization Overhead in Multi-Agent LLM Systems](https://arxiv.org/abs/2603.15183) - identifies broadcast-induced synchronization cost scaling as O(agents x steps x artifact-size) under naive broadcast, reducible via lazy invalidation to O((agents + updates) x artifact-size), with observed token savings up to 95% in tested configurations
- [Multi-Agent Cost Compounding: Why 3 Agents Cost 10x](https://www.augmentcode.com/guides/multi-agent-cost-compounding) - real-world documentation of superlinear cost scaling as agent count increases in naive multi-agent architectures
- [Dynamic Attentional Context Scoping: Agent-Triggered Focus Sessions for Isolated Per-Agent Steering in Multi-Agent LLM Orchestration](https://arxiv.org/pdf/2604.07911) - per-agent compact status registries and on-demand focus sessions as an alternative to uniform full-context broadcast
