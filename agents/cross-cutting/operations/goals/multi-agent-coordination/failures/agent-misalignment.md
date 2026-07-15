# Agent Misalignment

## Issue: Agents Pursue Conflicting Objectives

**Frequency**: Common

**Symptoms**
- Agents produce contradictory outputs
- System oscillates between different solutions
- Final output doesn't satisfy any agent's criteria
- Agents undo each other's work

**Root Cause**
Where the agent, or agentic AI system, deviates in its actions to pursue an intent and purpose not desired by the user or creator. In multi-agent systems, individual agents may interpret objectives differently, leading to conflicting behaviors even when working toward nominally the same goal.

**Example**
```
Task: "Improve the codebase"

Agent A (Performance): Inlines functions for speed
Agent B (Readability): Extracts functions for clarity
Agent C (Security): Adds validation to every function

Result: Agents repeatedly modify same code
        Performance degrades from added validation
        Readability suffers from mixed styles
        No stable solution reached
```

**Misalignment Types**
- **Goal interpretation**: Different understanding of success
- **Priority conflicts**: Agents rank sub-goals differently
- **Temporal misalignment**: Agents optimize for different time horizons
- **Metric gaming**: Agents optimize metrics that conflict

**Potential Effects**
- System never reaches stable state
- Resource waste on conflicting work
- Output quality degradation
- User confusion about system behavior

## Mitigation Strategies

### Prevention
1. **Explicit goal hierarchy with tie-break rules**: In the Performance/Readability/Security example, none of the three agents knows it is subordinate to the others, so each keeps "winning" locally while the artifact never stabilizes. Publish a single ranked priority order (e.g., Security > Correctness > Readability > Performance) that every agent reads before acting, and require agents to justify overrides against that order. Trade-off: a rigid hierarchy can suppress legitimate cases where a lower-priority concern (e.g., performance) should dominate for a specific file or hot path.
2. **Single shared objective document, not per-agent goal paraphrase**: "Improve the codebase" was independently reinterpreted by three agents into three different definitions of success. Replace vague top-level tasking with a shared, structured objective spec (target metrics, constraints, out-of-scope changes) that all agents read verbatim rather than re-derive. Trade-off: authoring a precise shared spec up front adds latency before agents can start work.
3. **Ownership partitioning to prevent overlapping edits**: The example shows all three agents repeatedly touching the same functions. Partition the codebase (or resource) so each agent owns disjoint files/regions for a given task, and route any change outside an agent's partition through a request to the owning agent instead of a direct edit. Trade-off: partitioning requires an up-front dependency analysis and can leave genuinely cross-cutting concerns (like adding validation everywhere) awkward to assign.

### Detection & Response
1. **Same-artifact edit-count monitor**: Track how many distinct agents modify the same file/function within a session; in the example, all three agents converge on the same code repeatedly. A threshold (e.g., 3+ agents touching one artifact within N turns) should trigger an automatic pause and route to arbitration rather than letting agents keep overwriting each other.
2. **Metric oscillation detector**: Since misalignment here manifests as performance and readability metrics moving in opposite directions across turns rather than converging, track the relevant quality metrics turn-over-turn and flag non-monotonic oscillation (up-down-up) as a signal of unresolved conflict, not just a slow convergence.
3. **Contradiction scan on agent outputs**: Diff each agent's rationale against the others' (e.g., Agent A justifying inlining vs. Agent B justifying extraction on the same function) and flag directly opposing justifications for the same artifact for human or arbitration-agent review.

### Architecture Patterns
1. **Arbitration agent with binding authority**: Insert a dedicated arbiter that reads all three agents' proposed diffs before any commit, applies the goal hierarchy, and either merges or rejects — this directly targets the "agents undo each other's work" symptom. Deployment consideration: the arbiter becomes a soft bottleneck, so it should batch decisions rather than serialize every single edit.
2. **Blackboard architecture with locked writes**: Give agents a shared, versioned "blackboard" (the codebase state) where an agent must acquire a lock and post an intended change before writing, so Agent B can see Agent A's rename before writing conflicting tests. Deployment consideration: needs a lock-timeout/expiry policy so a stalled agent doesn't block the others indefinitely.
3. **Objective-alignment checkpoint before execution**: Before agents start work, run a cheap alignment pass where each agent restates its interpretation of the shared goal and a checker (rule-based or LLM) flags divergent interpretations — catching the "improve the codebase" ambiguity before code is touched rather than after. Deployment consideration: adds a fixed latency cost per task even when agents would have agreed anyway.

### Metrics
1. **same_artifact_conflict_rate**: Target < 5% of tasks with 2+ agents editing the same file/function; Alert if > 15% over a rolling 50-task window.
2. **objective_reinterpretation_variance**: Target < 10% semantic divergence between agents' restated goals (measured via embedding similarity of goal restatements); Alert if any pair falls below 0.7 cosine similarity.
3. **net_quality_delta_per_session**: Target positive and monotonic improvement in the tracked quality metric (e.g., readability score, latency) across turns; Alert if metric reverses direction 2+ times in a session.
4. **arbitration_invocation_rate**: Target < 20% of multi-agent tasks requiring arbiter intervention; Alert if > 40%, indicating the goal hierarchy itself is miscalibrated.

### Alerts
1. **Repeated-Overwrite Loop** (P1): Condition - the same file/artifact is modified by 3+ different agents within a 10-turn window with no convergence. Action: auto-pause all agents touching that artifact, snapshot current state, and route to the arbitration agent or a human reviewer.
2. **Metric Oscillation Detected** (P2): Condition - a tracked quality metric (performance, readability score) reverses direction across 2+ consecutive agent turns. Action: freeze further edits from the agent that most recently reversed the metric and surface a diff summary for review.
3. **Goal Interpretation Divergence** (P3): Condition - restated objectives from agents fall below similarity threshold during the alignment checkpoint. Action: block task start and request a clarified, structured objective spec before agents proceed.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Inter-agent misalignment as major failure category
- [Microsoft: Taxonomy of Failure Mode in Agentic AI](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf) - Agent misalignment effects
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - 41-86.7% failure rates
