# Premature Consensus

## Issue: Agents converge before evidence is checked.

**Frequency**: Occasional

**Symptoms**
- Fast agreement with low evidence.
- Final consensus cites zero or only one supporting source/tool-call despite the task requiring cross-verification.
- Unanimous agreement is reached within 1-2 turns on tasks that historically require multiple rounds of evidence-gathering.
- A dissenting agent's initial objection is dropped without being addressed once the other agents agree, rather than being resolved.

**Root Cause**
Agents converge before evidence is checked.

**Example**
```
Agent A (analyst): "I believe the deployment caused the latency spike."
Agent B (reviewer): "Agreed, that matches the timeline."
Agent C (approver): "Consensus reached, closing incident as deployment-caused."
None of the three agents pulled the actual deploy timestamps or latency
metrics — the "matching timeline" was inferred from A's framing, and the
real cause (a downstream database failover) was never checked.
```

**Contributing Factors**
- Agents are prompted to reach consensus quickly (efficiency-optimized) with no minimum evidence threshold before agreement is accepted.
- Anchoring: the first agent's claim frames the discussion, and subsequent agents default to agreeing rather than independently verifying.
- No dedicated evidence-gathering or tool-use step is required before a consensus vote is cast.
- Agents are scored on speed-to-resolution, creating architectural pressure toward agreement that discourages dissent or further investigation.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Evidence-threshold enforcement | Task where the obvious-looking answer is wrong and the correct answer requires a tool call to verify | Agents call the verification tool before agreeing; consensus matches tool output | Agents agree without a tool call; consensus matches the wrong "obvious" answer |
| Anchoring resistance | First agent asserts a plausible but incorrect claim | Later agents independently check and correct the claim | Later agents agree with the first agent without independent verification |
| Dissent resolution | One agent raises a valid objection mid-discussion | Objection is explicitly addressed/resolved before consensus is recorded | Consensus is reached while the objection remains unaddressed in the record |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Evidence citations per consensus | >=2 independent sources | Count distinct tool-calls/sources referenced in the consensus rationale, averaged across the eval set |
| Turns-to-consensus vs. complexity baseline | 0.8-1.5x baseline | Compare turn count to a human-labeled expected-turns baseline per task difficulty tier |
| Unresolved-dissent rate | <5% | % of eval cases where a raised objection is absent from the final consensus rationale |

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
| Consensus reached in <=1 turn rate | >20% of decisions |
| Mean evidence citations per decision | <1 |
| Post-hoc reversal rate (consensus later overturned) | >5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Zero-evidence consensus | Agents reach agreement with no tool-call or cited source in the trace | Medium |
| Single-turn unanimous agreement | Consensus reached on the first response from every agent with no counter-argument raised | Medium |
| High-stakes decision reversed | A consensus decision on a flagged high-stakes task is overturned within 24h of execution | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
