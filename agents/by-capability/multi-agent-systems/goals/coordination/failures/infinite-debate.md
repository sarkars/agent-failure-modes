# Infinite Debate

## Issue: Agents critique/revise endlessly without termination.

**Frequency**: Occasional

**Symptoms**
- Repeated critique loops; no final result.
- Turn count between critic and reviser exceeds typical task complexity by 5-10x with no convergence in quality score.
- Critique feedback cycles between the same 2-3 objections rather than surfacing new issues each round.
- Token/cost consumption for a single task grows unbounded as the debate continues with no forcing function to stop it.

**Root Cause**
Nothing in the loop's design caps the number of rounds or checks for diminishing returns, so as long as the critic can find something to say, the cycle continues by default. That tendency is reinforced when the critic is prompted or rewarded to always surface at least one issue, which biases it structurally against ever issuing an approval, and by the absence of a fixed, shared rubric, which lets the critic re-litigate a different criterion each round instead of converging on a stable checklist. Because the writer and critic hold symmetric authority with no arbiter or human-escalation path to force a decision, there is also no mechanism that can end the exchange once it stops making progress -- it just keeps going until an external resource limit, like a timeout, cuts it off.

**Example**
```
Round 1: Writer produces draft. Critic: "Missing error handling for null inputs."
Round 2: Writer adds null checks. Critic: "Error handling present but inconsistent with style guide."
Round 3: Writer aligns style. Critic: "Style now consistent, but null-check ordering is suboptimal."
Round 4: Writer reorders checks. Critic: "Ordering fixed, but this reintroduces the gap from Round 1."
... loop continues for 40 rounds; no termination condition ever fires; task
times out after 2 hours with no accepted output.
```

**Contributing Factors**
- No maximum round cap or diminishing-returns check on the critique-revise loop.
- Critic agent is prompted/rewarded to always surface at least one issue, biasing it against ever approving.
- No shared, versioned rubric — the critic re-litigates different criteria each round instead of converging on a fixed checklist.
- Writer and Critic hold symmetric authority with no tie-breaking arbiter or human-escalation path to force closure.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Round-cap enforcement | Task seeded with an unresolvable style disagreement (two valid but conflicting conventions) | System halts and escalates after N rounds with no quality-score improvement | Loop continues past the cap or terminates without producing output |
| Diminishing-returns detection | Quality score plateaus within +/-1% across 3 consecutive critique-revise rounds | Orchestrator forces final selection at the plateau | Debate continues past the plateau, consuming additional rounds |
| Oscillating critique | Critique alternates between two contradictory demands (round 1 wants A, round 2 wants not-A) | Cycle detector flags the repeated critique pattern and escalates | Agents cycle indefinitely without the cycle detector triggering |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Mean rounds to convergence | <=5 | Count critique-revise turns per task in an offline eval set until critic approval |
| Non-convergence rate | <2% | % of eval tasks that hit the round cap without reaching approval |
| Critique novelty ratio | >0.7 | Fraction of critique points per round that are semantically new vs. repeated from prior rounds (embedding similarity) |

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
| Debate round count (p95) | >15 rounds |
| Task wall-clock time in debate loop | >10 min |
| Critique repetition rate | >40% repeated objections across rounds |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unbounded debate loop | Task exceeds 20 critique-revise rounds without termination | Medium |
| Critique cycle detected | Same objection (semantic match) recurs 3+ times across rounds | High |
| Debate cost spike | Token spend for a single task's debate loop exceeds 10x the median task cost | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
