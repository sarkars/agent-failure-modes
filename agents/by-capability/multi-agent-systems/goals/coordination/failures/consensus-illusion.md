# Consensus Illusion

## Issue: Agents agree because they share flawed context or bias.

**Frequency**: Occasional

**Symptoms**
- Multiple agents produce same unsupported answer.
- Agreement rate between agents stays high even when the shared answer conflicts with ground truth or external verification.
- All agents were seeded from the same upstream retrieval/context source, so their "independent" votes are actually correlated, not independent.
- Confidence in the aggregated answer rises with agent count even though the agents lack the diversity needed to add real signal.

**Root Cause**
Agents agree because they share flawed context or bias.

**Example**
```
Agent A, Agent B, and Agent C are each asked to independently verify a claim, but
all three receive the same outdated knowledge-base snippet as context. All three
confidently agree the claim is "true" because they're reasoning from the identical
stale source, not independent evidence. The voting/aggregation layer reports "3/3
consensus, high confidence" -- masking that this is one shared error, not three
independent confirmations.
```

**Contributing Factors**
- All agents draw from a single shared retrieval index or context source instead of independent, diverse evidence.
- Agents instantiated from the same base model/prompt template with no diversity in reasoning strategy or temperature.
- Voting/aggregation logic treats agreement as a proxy for correctness without checking evidence independence.
- No dissent-seeking mechanism (e.g., devil's-advocate agent, adversarial review) built into the consensus process.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Shared-bias injection | Feed all agents an identical, subtly-wrong context snippet and ask them to vote on a claim | System flags low evidence diversity and lowers confidence, or an independent-source check catches the error | Agents unanimously agree on the wrong answer and the system reports high confidence |
| Source-diversity audit | Trace each agent's evidence sources for a given consensus decision | Agents draw from genuinely independent sources for a "high confidence" verdict | All agreeing agents trace back to the same single upstream source |
| Adversarial dissent test | Introduce a devil's-advocate agent instructed to challenge the majority view with independent evidence | Consensus score adjusts downward when dissent surfaces valid counter-evidence | Majority consensus persists unchanged even when presented with contradicting independent evidence |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Evidence Source Diversity | >=2 independent sources per consensus decision | Count of distinct upstream evidence sources feeding into agents that agree |
| Consensus-Accuracy Correlation | Positive, r>0.7 | Correlation between agreement level and ground-truth correctness on a labeled eval set |
| Dissent Surfacing Rate | >90% of injected errors caught | Percentage of seeded shared-bias test cases where an adversarial/independent check flags the error before final consensus |

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
| Single-Source Consensus Rate | >20% of decisions |
| Consensus-Ground-Truth Divergence | >5% on sampled audits |
| Dissent Agent Override Rate | <2% (implausibly low suggests dissent isn't functioning) |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Correlated-Source Consensus | Majority of agreeing agents trace to a single shared upstream context source | Medium |
| High-Confidence Wrong Answer | Consensus decision marked high-confidence is contradicted by ground-truth/audit sample | High |
| Dissent Mechanism Silent | Adversarial/dissent agent produces zero challenges over an extended window despite eligible cases | Low |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
