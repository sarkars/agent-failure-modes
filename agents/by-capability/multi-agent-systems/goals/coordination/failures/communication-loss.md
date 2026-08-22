# Multi-Agent Communication Loss: Causes and Fixes

## Issue: Agents lose or drop key information passed between them, so a downstream agent acts without facts that an upstream agent already discovered.

**Frequency**: Common

**Symptoms**
- Evidence present in one agent trace, absent in another.
- Agent B contradicts or ignores a fact Agent A explicitly discovered because it was never included in the handoff payload.
- Context-window truncation or lossy summarization drops critical details (e.g., a caveat or exception) between agent hops.
- Agents operating on separate memory/context stores answer the same question differently depending on which one is asked.

**Root Cause**
Handoffs between agents are implemented as free-text summaries rather than structured, complete state transfer, so a detail an author agent considered secondary can be silently dropped in the act of condensing it into prose. Token-budget limits and aggressive context truncation compound this by cutting earlier findings before they are ever serialized into the handoff, and because agents keep separate, local memory stores rather than reading from one shared context, there is no fallback path for the receiving agent to recover what was lost. Nothing in the handoff process defines a "must-carry" set of fields that are required to survive every transfer, so which facts make it through depends on the summarizer's judgment call in the moment rather than on any guarantee.

**Example**
```
Agent A (research agent) discovers the customer already requested a refund last
week and notes it internally. Agent A's handoff summary to Agent B (support-reply
agent) only includes "customer wants order status" -- the refund history is dropped
during summarization. Agent B replies with a standard shipping update, ignoring the
prior refund request, causing customer frustration and a duplicate support ticket.
```

**Contributing Factors**
- Handoffs implemented as lossy natural-language summaries rather than structured, complete state transfer.
- Aggressive context-window truncation or token-budget limits that silently drop earlier findings.
- Agents maintaining separate/local memory stores instead of a shared, queryable context store.
- No explicit "must-carry" field list defining which facts are required to survive every handoff.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Critical-fact dropout | Seed Agent A with a fact that must influence the final decision (e.g., prior refund), then run the full pipeline | Final output reflects the seeded fact | Final output ignores or contradicts the seeded fact because it never reached the consuming agent |
| Summarization fidelity check | Compare Agent A's full trace to the actual handoff payload sent to Agent B | Handoff payload contains all fields marked must-carry | Must-carry fields are missing or altered in the handoff payload |
| Cross-agent fact consistency | Ask two agents sharing a pipeline the same factual question about the case | Both agents give the same answer | Agents give different answers because they hold different subsets of context |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Must-Carry Field Retention Rate | 100% | Percentage of handoffs where all fields tagged must-carry are present and unmodified in the receiving agent's input |
| Cross-Agent Fact Consistency | >99% | Percentage of sampled fact-queries answered identically by agents sharing the same case context |
| Context Truncation Incidence | <1% | Percentage of handoffs where token-budget truncation removes content from the pre-truncation payload |

---

**How to fix it**: carry full context (not lossy summaries) across agent handoffs and verify nothing critical was dropped in transit.

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
| Must-Carry Field Drop Rate | >0.5% of handoffs |
| Cross-Agent Fact Contradiction Rate | >1% of sampled queries |
| Context Truncation Events | >10/day |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Critical Field Missing at Handoff | A must-carry field is absent or null in a downstream agent's received context | High |
| Cross-Agent Contradiction Detected | Two agents in the same run give factually inconsistent answers to the same question | High |
| Context Truncation Spike | Truncation events exceed baseline rate in a rolling window | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
