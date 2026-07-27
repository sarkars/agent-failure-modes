# What Are the Most Common Failures in Multi-Agent AI Systems?

**Multi-agent AI systems most often fail not because any individual agent is weak, but because the coordination layer between agents — authority, handoffs, communication, and consensus — is left implicit and breaks silently under real workloads.** A pipeline can pass every single-agent test and still fail once agents have to hand off state, agree on a conclusion, or recover from one agent's mistake, because those are properties of the system as a whole, not of any one agent in it.

## Key Takeaways

- Multi-agent systems span 4 goals and 18 failure patterns here, all grounded in the MAST taxonomy (Cemri et al., arXiv:2503.13657) of why multi-agent LLM systems fail.
- A single upstream error can amplify 17x-20x by the time it reaches the final output of a sequential pipeline, per measured statistics in [Error Propagation](goals/error-propagation/) — and tightly coupled pipelines show production failure rates above 80% (arXiv:2503.06789).
- Agreement between agents is not independent evidence of correctness: agents sharing a base model, training data, or context produce correlated errors, and 5-15% of consensus conclusions in critical domains are false per [Reasoning Quality](goals/reasoning-quality/)'s source data (arXiv:2510.10185).
- Every goal in multi-agent systems converges on the same mitigation architecture regardless of the specific failure: explicit handoff schema validation, consensus checkpoints at agent-to-agent transitions, and saga-pattern error isolation — coordination-layer infrastructure, not a smarter individual agent.

## Multi-Agent Systems Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Coordination](goals/coordination/) | The full breadth of coordination breakdowns — authority, roles, communication, consensus, and verification across a multi-agent system | 15 |
| [Error Propagation](goals/error-propagation/) | How a single agent's error compounds exponentially through a sequential, unverified pipeline | 1 |
| [Handoff Reliability](goals/handoff-reliability/) | Why a structured handoff schema can lose an upstream agent's confidence or methodology signal | 1 |
| [Reasoning Quality](goals/reasoning-quality/) | Why multiple agents agreeing on an answer doesn't mean the answer is correct | 1 |

**Total: 18 patterns**

## How the Goals Relate

The four multi-agent-systems goals aren't a pipeline with a natural order — the four goals are different lenses on the same underlying problem: what happens at the seams between agents. Coordination is the broad taxonomy; the other three goals are deep dives into specific seam failures that Coordination's own patterns only cover at stub depth (Cascading Error, Task Handoff Failure, and Consensus Illusion/Premature Consensus respectively). To route by symptom: a multi-agent trace fails while every individual agent passes in isolation, or roles/authority are unclear → **Coordination**; a small upstream error somehow becomes a large final-output error in a sequential pipeline → **Error Propagation**; a downstream agent acts with full confidence on a value the upstream agent had actually flagged as uncertain → **Handoff Reliability**; multiple agents agree on an answer that later turns out to be wrong → **Reasoning Quality**.

## Frequently Asked Questions

### What's the difference between Coordination and the other three goals in multi-agent systems?
Coordination is the broad taxonomy covering 15 distinct failure patterns across authority, roles, communication, and verification, each documented at a consistent but relatively concise depth. Error Propagation, Handoff Reliability, and Reasoning Quality each take one specific mechanism that Coordination's patterns touch on briefly (Cascading Error, Task Handoff Failure, Consensus Illusion) and document it in full depth with worked examples, statistics, and citations.

### Can a single fix address all 18 multi-agent patterns in multi-agent systems?
No single fix, but a consistent architecture recurs across all 18 patterns: schema-validated handoffs, consensus checkpoints at agent transitions, and saga-pattern compensating actions for error isolation. What differs by goal is where in the pipeline the check needs to sit — at every inter-agent message for Coordination and Handoff Reliability, at each pipeline stage for Error Propagation, and at the point where agreement is treated as a decision signal for Reasoning Quality.

### Which goal should be checked first when a multi-agent pipeline misbehaves in production?
Start with [Coordination](goals/coordination/) — its 15 patterns cover the widest range of symptoms and will usually narrow down which specific mechanism is at play. If the symptom is specifically "a small error became a huge one" or "agents agreed but were all wrong," jump directly to [Error Propagation](goals/error-propagation/) or [Reasoning Quality](goals/reasoning-quality/) respectively, since those goals document the exact amplification statistics and reproduction protocols.

## Related Categories

- [Reasoning & Chain-of-Thought](../reasoning-and-thought/) — single-model reasoning and behavior failures that occur even before multiple agents are introduced
- [Long-Horizon Execution](../long-horizon-execution/) — goal-maintenance and drift failures over time, a related cascading mechanism referenced directly from multi-agent-systems' Error Propagation pattern
