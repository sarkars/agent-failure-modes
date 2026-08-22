# AI Agent Task Handoff Failure: Causes and Fixes

## Issue: An agent hands off incomplete or incorrect state to the next agent in the pipeline -- a common failure in LangGraph/CrewAI-style handoffs -- so the downstream agent works from a gap it doesn't know exists.

**Frequency**: Common

**Symptoms**
- Downstream agent lacks necessary context.
- Downstream agent re-requests information (via a clarifying question or redundant tool call) that the upstream agent already gathered but did not forward.
- Handoff payload contains only the final answer, dropping intermediate assumptions or constraints the downstream agent needs to validate its own output.
- Downstream agent silently fills gaps in a handoff with default/guessed values instead of the actual upstream-computed values, producing plausible-but-wrong output.

**Root Cause**
Handoffs are implemented as free-text summaries rather than structured, versioned payloads with clearly required fields, so there is nothing forcing the sending agent to include every value the receiving agent will actually need. Context-window truncation between turns can also drop earlier state before it is ever serialized into the handoff, and because no validation layer checks that the fields downstream depends on are present and non-null, a payload missing a critical constraint is accepted and forwarded without complaint. The orchestration framework treats each agent as stateless and relies entirely on the sending agent's memory to include everything relevant, so any single lapse in that recall becomes an invisible, un-caught gap in what the next agent receives.

**Example**
```
Agent A (planner) computes: {"user_budget": 500, "currency": "USD",
  "constraints": ["no red-eye flights"]}
Handoff to Agent B (booking agent) passes only: "book a flight under budget"
— budget, currency, and constraints are dropped from the free-text handoff.
Agent B books a $650 red-eye flight because it never received the
structured constraints, only a vague instruction.
```

**Contributing Factors**
- Handoffs are implemented as free-text summaries rather than structured, versioned payloads with required fields.
- Context-window truncation between agent turns drops earlier state before it is serialized into the handoff.
- No validation layer checks that all fields the downstream agent depends on are present and non-null before the handoff is accepted.
- The orchestration framework treats each agent as stateless, relying on the sending agent to remember to include everything relevant.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Required-field completeness | Upstream agent produces a plan with 4 required fields (budget, currency, constraints, deadline) | Downstream's handoff payload contains all 4 fields non-null | One or more required fields are missing/null in the payload downstream receives |
| Silent default-fill detection | Handoff intentionally omits a constraint field | Downstream agent flags the missing field and requests it rather than guessing a default | Downstream proceeds with a guessed/default value without flagging the gap |
| Stale-state detection | Upstream state is updated (e.g., budget revised) after initial handoff but before downstream acts | Downstream agent uses the revised budget | Downstream agent acts on the original, now-stale value |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Handoff field completeness rate | 100% | % of required schema fields present and non-null across sampled handoffs |
| Downstream re-request rate | <5% | % of handoffs followed by downstream re-asking for info the upstream should have provided |
| Silent-default usage rate | <1% | % of downstream executions where a value traces to a code/prompt default rather than an explicit upstream field |

---

**How to fix it**: define a required-fields handoff schema and validate it at each transition instead of trusting whatever the upstream agent happened to forward.

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
| Handoff field null rate | >1% of handoffs |
| Downstream clarification/re-fetch rate | >5% of handoffs |
| Stale-state usage rate | >2% of handoffs |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Incomplete handoff payload | Required schema field is null/missing in a captured handoff | High |
| Downstream re-request spike | Downstream agent issues clarifying questions or duplicate tool calls above baseline rate in a 1-hour window | Medium |
| Stale state used | Downstream action uses a state value with a timestamp older than the latest upstream update | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
