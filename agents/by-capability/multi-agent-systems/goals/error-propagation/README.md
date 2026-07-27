# What Are the Most Common Error-Propagation Failures in Multi-Agent AI Pipelines?

**One agent's error amplifies across a multi-agent pipeline because each downstream agent treats the previous agent's output as ground truth rather than an uncertain input to verify, so a 5% error at the first stage compounds into 17x-20x amplification by the final output.** The pipeline never fails cleanly — every intermediate agent reports high confidence, and disabling one agent in the chain can actually improve overall system reliability, which is the tell that the architecture itself is the problem, not any single agent's capability.

## Key Takeaways

- A single documented pattern, [Multi-Agent Error Propagation Cascade](failures/multi-agent-error-propagation-cascade.md), covers error propagation, citing measured error amplification factors of 17x in 3-agent systems and 20x+ in 4+ agent systems (MAST, arXiv:2503.13657).
- Tightly coupled ("monolithic entanglement") multi-agent pipelines show failure rates above 80% in production per arXiv:2503.06789, because each additional agent stage compounds rather than independently checks the previous stage's error.
- Each agent stage in an unverified chain adds an estimated 5-20% additional error on top of whatever it inherited (arXiv:2510.10581) — the math is closer to exponential (2^N × E) than additive.
- The counterintuitive symptom that confirms the error-propagation pattern: adding more agents to a pipeline decreases reliability rather than increasing it, because more stages means more compounding opportunities without more verification.

## Scope

The single mechanism error propagation covers is **sequential error compounding without intermediate verification**: agents are chained so that agent B's input is agent A's output, agent B has no way to detect that agent A's output was wrong, and agent B's own error rate is added on top rather than caught. See [Multi-Agent Error Propagation Cascade](failures/multi-agent-error-propagation-cascade.md) for worked examples across data extraction, legal document processing, customer service escalation, and supply chain optimization pipelines.

## When Error Propagation Matters

- A pipeline chains 3 or more agents sequentially, where each agent's input is entirely the previous agent's output, with no independent verification step between stages
- Debugging a bad final output requires tracing back through multiple agent stages, and the error appears to "originate" from a different agent than the one that actually introduced it
- A pipeline works perfectly when each agent is tested in isolation on clean inputs, but fails once agents run in sequence on real, imperfect data

## Cross-Pattern Insight

The fix documented for error propagation is architectural, not a smarter individual agent: handoff schema validation with type checking to catch malformed handoffs before forwarding, distributed consensus checkpoints (semantic-hash world-model snapshots) at each agent-to-agent transition to detect divergence early, and a saga pattern with compensating actions so a detected error can be rolled back rather than propagated. The target metric is error cascade depth — the average number of downstream agents affected by a single upstream error — with a stated goal of keeping it below 1 (i.e., an error is caught before it reaches a second agent) and an alert threshold at 2.

## Frequently Asked Questions

### How is error propagation different from cascading error in the Coordination goal?
They describe the same underlying mechanism. [Coordination](../coordination/)'s Cascading Error pattern is a short-form entry citing the same "early error propagates through the pipeline" root cause; error propagation's pattern is the full-depth version with worked examples across four industries and the specific 17x-20x amplification statistics.

### Does adding a verification or consensus step between agents actually stop the cascade?
The pattern's own test protocol targets exactly the cascade: reproducing the cascade, applying intermediate verification and consensus checkpoints, and re-measuring — the stated success criterion is cascade amplification reduced from 17x+ to under 2x. Verification between stages, not a better model at any one stage, is what the mitigation targets.

### What's the warning sign that a production pipeline already has an error-propagation problem?
Per the pattern's symptoms list: if disabling one agent in the pipeline improves overall system reliability, or if each agent reports high confidence despite the system's end-to-end accuracy being poor, the pipeline is very likely propagating and compounding errors rather than catching the errors.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Multi-Agent Error Propagation Cascade](failures/multi-agent-error-propagation-cascade.md) | Downstream agents treat upstream output as ground truth, compounding rather than catching upstream errors |

**Total: 1 pattern**

## Related Goals

- [Coordination](../coordination/) — the broader taxonomy of multi-agent coordination failures, including a short-form version of the same cascade mechanism
- [Reasoning Quality](../reasoning-quality/) — a parallel failure mode where agents agree (rather than chain) on the same wrong answer, and consensus amplifies the error instead of a pipeline stage doing so
- [Handoff Reliability](../handoff-reliability/) — a narrower handoff-schema failure (losing confidence signal) that can itself be the point where an error starts propagating uncaught
