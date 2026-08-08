# Emergent Behavior

## Issue: Interaction creates behavior not seen in isolated tests.

**Frequency**: Common

**Symptoms**
- Multi-agent trace fails while individual agents pass.
- Agents fall into unintended repetitive loops (e.g., mutual clarification requests) only visible when they interact live, never in single-agent unit tests.
- Aggregate system behavior (e.g., runaway cost, oscillating decisions) emerges from feedback loops between agents that no single agent's test suite exercises.
- Behavior varies nondeterministically between runs with identical inputs because of timing-dependent interaction effects between agents.

**Root Cause**
Test coverage is built around each agent in isolation, exercising it against mocked or scripted counterpart responses rather than a live, unscripted peer, so the actual feedback dynamics between two open-ended agents are never exercised before production. When those agents are wired into a loop -- Agent A's output feeding Agent B, whose output feeds back to Agent A -- with no turn or iteration cap, the open-ended nature of generation means the space of possible exchanges is far larger than anything a scripted test could sample. Without production-scale multi-agent simulation or chaos-style testing standing in for that gap, the first time the real interaction pattern plays out is in front of a live user, and the loop can run unbounded before anyone notices.

**Example**
```
Agent A (negotiator) and Agent B (counter-negotiator) each pass all unit tests
in isolation with scripted counterpart responses. In production, Agent A
proposes a price, Agent B counters, Agent A re-proposes a slightly adjusted
price referencing Agent B's counter, and the two enter an unbounded
back-and-forth loop neither was tested against, burning through the token
budget before a human notices the conversation never converges.
```

**Contributing Factors**
- Unit/integration tests validate each agent in isolation with mocked or scripted counterpart behavior, never live agent-to-agent interaction.
- Feedback loops between agents (Agent A's output feeds Agent B, whose output feeds back to Agent A) with no turn/iteration cap.
- High degrees of freedom in agent responses (open-ended generation) expand the space of possible interaction sequences beyond what was tested.
- No production-scale multi-agent simulation or chaos-style testing performed before deployment, only per-agent evals.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Live-pair interaction test | Run Agent A and Agent B against each other (not mocked) for an extended number of turns | Interaction converges to a resolution within a bounded number of turns | Agents enter a loop, oscillation, or divergence not seen when each was tested against a scripted counterpart |
| Non-determinism replay test | Run the identical input through the full multi-agent system 10 times | Outputs and interaction paths are consistent across runs | Interaction outcome varies significantly between runs with identical inputs |
| Iteration cap enforcement | Configure agents in a feedback loop with no natural stopping condition | System enforces a max-turn/iteration cap and escalates gracefully | Agents continue interacting unbounded until timeout or resource exhaustion |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Live-Pair Test Coverage | 100% of interacting agent pairs | Percentage of agent pairs tested against each other's live (non-mocked) behavior, not just scripted stubs |
| Interaction Convergence Rate | >95% | Percentage of live multi-agent test runs that reach a stable resolution within the defined turn cap |
| Run-to-Run Determinism | >90% output similarity | Similarity score of outputs across repeated runs of identical input through the full multi-agent system |

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
| Unbounded Interaction Loop Rate | >1% of runs |
| Turn Count Exceeding Expected Range | >3x median turn count |
| Run-to-Run Output Variance (identical input) | >10% divergence |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Interaction Loop Detected | Agent pair exceeds expected turn count without converging to resolution | High |
| Iteration Cap Breach | Feedback loop between agents hits the max-turn safety cap, forcing termination | Medium |
| Novel Interaction Pattern | Multi-agent trace fails despite all individual agents passing isolated unit tests | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
