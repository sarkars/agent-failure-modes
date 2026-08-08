# Worker Tunnel Vision

## Issue: Specialized agents optimize local goals over global success.

**Frequency**: Occasional

**Symptoms**
- Local output good; final task fails.
- Individual agent's per-subtask evaluation score is high, but the aggregated end-to-end task metric fails or regresses.
- Agent optimizes a proxy metric it was given (e.g., "minimize response length") in a way that harms the actual end-user goal.
- Agent ignores or overrides context from other agents or the global plan when it conflicts with its own local objective.

**Root Cause**
Each specialized agent is scored and rewarded against a narrow, locally-defined metric that has no term for the end-to-end outcome, so there is nothing in its optimization target pulling it toward the global goal. Compounding this, agents are deliberately siloed from the overall task objective and from how downstream stages will consume their output, and the pipeline's strictly sequential architecture gives no agent a channel to flag that its locally-optimal work is hurting the final result. The narrow tool access and prompt scope that make each agent good at its specialty are the same properties that make it structurally blind to cross-cutting tradeoffs.

**Example**
```
Agent A (SEO-optimizer) is scored on keyword density and rewrites product
descriptions to maximize keyword hits — its local score is 95/100.
Agent B (final assembler) ships A's copy unchanged. End-to-end conversion
rate drops 18% because the keyword-stuffed copy reads as spam to real
users — the global objective (sales) was never part of A's reward signal,
only the local proxy (SEO score).
```

**Contributing Factors**
- Each specialized agent is evaluated/rewarded on a narrow local metric with no term for global/end-to-end outcome.
- Agents lack visibility into the overall task objective or downstream consumers of their output, since information is siloed by design.
- Pipeline architecture is strictly sequential/one-directional, so no agent can flag that its "good" local output is harming the global result.
- High specialization (narrow tool access, narrow prompt scope) makes agents structurally unable to consider cross-cutting tradeoffs.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Local-global divergence detection | Task where optimizing the local metric provably harms the global outcome (e.g., keyword stuffing vs. readability) | Agent trades off local score for global outcome, or flags the conflict | Agent maximizes local score at the expense of the global outcome with no flag |
| Global-objective visibility | Specialized agent is queried about the end-to-end task goal mid-task | Agent can state the global objective and how its subtask serves it | Agent cannot articulate the global objective beyond its own local metric |
| Cross-agent conflict flagging | Two agents' local optima are mutually exclusive (e.g., speed vs. thoroughness) | Conflict is surfaced to an orchestrator/human for a tradeoff decision | Each agent proceeds independently with no flagged conflict, and the global outcome worsens |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Local-global score correlation | >0.7 | Correlation between each agent's local metric and end-to-end task success across eval runs |
| Global-objective recall | >90% | % of agents that, when queried, can correctly state the overarching task goal |
| Tradeoff escalation rate | >80% of true conflicts | % of eval cases with a genuine local/global conflict where the conflict is surfaced rather than silently resolved locally |

---

## Mitigation Strategies

### Prevention

1. **Implement handoff schema validation with type checking**: Define explicit message contracts between agents using JSON Schema or Protocol Buffers. Each handoff includes: required fields, field types, context cardinality, consistency invariants (e.g., 'account_id must match previous context'). Validation layer rejects malformed handoffs before forwarding. Root cause: Prevents information loss and state inconsistency by catching misalignment at handoff boundaries.

2. **Establish distributed consensus checkpoints**: Before critical transitions (agent A -> B), compute and store world-model checkpoints as semantic hashes of key state variables. On agent B entry, verify checkpoint matches derived from B's initial inputs. If mismatch, trigger rollback or human escalation. Root cause: Detects state divergence early, enabling recovery before cascading errors.

3. **Implement error isolation with saga pattern**: Structure multi-agent workflows as compensating sagas. Each agent's action has a reverse operation. On error, compensating actions execute in reverse order, restoring system to consistent state. Track saga state in distributed ledger (event log). Root cause: Prevents cascade failures by ensuring partial execution doesn't corrupt global state.

### Detection & Response

1. **State consistency verification at handoffs**: At each inter-agent message, verify: (1) Handoff schema conforms to contract, (2) Required fields present and non-null, (3) Semantic consistency (e.g., derived context matches explicit assertions). Log mismatches with full message context. Alert on schema violation rate >0.5%.

2. **Distributed tracing with invariant checking**: Instrument all agent-to-agent calls with trace IDs. Track state variables across spans. Compute invariant violations: e.g., total_balance should equal sum(accounts). Flag spans where invariants break. Correlate with handoff timing to identify failure point.

### Architecture Patterns

1. Handoff Contract Engine: Define per-workflow interaction schemas with required fields, optional extensions, and invariant predicates. Codegen produces type-safe message classes. Validation happens pre-send with detailed error reporting (which field failed, why).

2. Saga Pattern with Event Sourcing: All agent actions append to immutable event log. On failure, replay log in reverse (applying compensating actions) to reach consistent state. World-model reconstructed from event log deterministically.

3. Distributed Tracing + Invariant Monitor: OpenTelemetry spans track all inter-agent messages. Background service computes invariants (e.g., sum checks, state graph acyclicity) against live span data. Alert on invariant violation with full context trail.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Handoff Schema Violation Rate | <0.1% | >0.5% | Percentage of inter-agent messages failing schema validation |
| State Consistency Score | >99.5% | <99% | Percentage of handoffs where world-model is consistent between agents |
| Error Cascade Depth | <1 | >2 | Average number of agents affected by single agent failure |
| Mean Recovery Time | <30s | >60s | Time from error detection to system returning to consistent state |
| Compensating Action Success Rate | >99% | <95% | Percentage of compensation actions that successfully restore state |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Handoff Contract Breach | Schema validation fails for >0.5% of handoffs in 5-min window | CRITICAL | Halt new orchestrations; page on-call; investigate agent contract mismatch |
| State Divergence Detected | Invariant violation detected at checkpoint verification | HIGH | Trigger rollback; log full message trace; alert SRE team |
| Cascade Failure Pattern | Single agent error causes >2 downstream agents to fail | HIGH | Pause orchestration; execute compensation; investigate isolation boundaries |


## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| Local-score vs. end-to-end success divergence | >20 percentage points |
| Global objective awareness rate | <80% of agents |
| Silent local-optimization incidents | >3 per week |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Local-global score divergence | Agent's local score is in the top quartile while the end-to-end task outcome fails | Medium |
| Global objective blind spot | Agent queried mid-task cannot state the overarching task goal | Low |
| Repeated local-optimization failure | Same agent role causes global-outcome regression in more than 3 tasks within a week | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
