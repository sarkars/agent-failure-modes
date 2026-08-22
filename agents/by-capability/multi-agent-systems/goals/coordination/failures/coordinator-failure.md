# AI Agent Coordinator Failure: Causes and Fixes

## Issue: The manager/orchestrator agent (the coordinator role in LangGraph supervisor graphs or CrewAI's manager pattern) assigns subtasks to the wrong worker agents, or fails to correctly synthesize their outputs into a coherent final answer.

**Frequency**: Common

**Symptoms**
- Subtasks poorly assigned; final synthesis incomplete.
- Worker agents receive subtasks outside their capability/scope, producing low-quality or off-topic results the coordinator doesn't catch.
- The coordinator's final synthesis omits or misrepresents valid worker outputs, e.g., dropping a completed subtask's findings entirely.
- Task decomposition duplicates effort in some areas while leaving other necessary subtasks unassigned.

**Root Cause**
Task decomposition is driven by static or templated logic rather than genuine awareness of each worker's actual capabilities, so subtasks get matched to agents based on convenience or ordering rather than fit. The coordinator has no validation step that checks a worker's output for relevance or confidence before folding it into the synthesis, so a low-quality, out-of-scope response is included as if authoritative. Separately, the synthesis step often assumes a fixed number or ordering of input slots, so outputs that arrive late or beyond that count are silently dropped rather than merged -- and because there is no feedback loop from synthesis quality back to the assignment policy, these mismatches and drops recur across runs instead of being learned from.

**Example**
```
Coordinator agent decomposes "audit Q3 financials" into subtasks and assigns
"tax compliance review" to a worker agent configured only for expense
categorization. The worker returns a low-confidence, out-of-scope response, but
the coordinator includes it verbatim in the final report as if authoritative.
Meanwhile a completed "revenue reconciliation" subtask from another worker is
never pulled into the synthesis, because the coordinator's aggregation step only
reads the first N worker outputs it receives.
```

**Contributing Factors**
- Task decomposition logic is static/templated rather than capability-aware, so subtask-to-agent matching ignores actual worker specialization.
- Coordinator lacks a validation step to check worker output relevance/confidence before including it in synthesis.
- Synthesis step has a fixed input slot count or ordering assumption that silently drops late-arriving or overflow worker outputs.
- No feedback loop from synthesis quality back to the task-assignment policy, so misassignment patterns repeat across runs.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Capability mismatch assignment | Give the coordinator a task requiring a specialist skill no available worker has | Coordinator flags the capability gap or escalates rather than force-assigning | Coordinator assigns the subtask to an ill-suited worker and includes the low-quality result unflagged |
| Dropped-output synthesis check | Run a decomposition producing more worker outputs than the coordinator's expected slot count | All completed worker outputs appear in the final synthesis | One or more valid completed subtask outputs are missing from the final synthesis |
| Assignment completeness audit | Decompose a multi-part task and verify every necessary subtask has an assigned owner | 100% of identified subtasks have an assigned worker | One or more necessary subtasks go unassigned, leaving gaps in the final deliverable |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Task-Capability Match Rate | >95% | Percentage of subtask assignments where worker capability profile matches subtask requirements |
| Synthesis Completeness | 100% | Percentage of completed worker outputs that appear in the final synthesized result |
| Assignment Coverage | 100% | Percentage of decomposed subtasks that receive a valid worker assignment |

---

**How to fix it**: validate task-to-agent assignment against declared capabilities and check the coordinator's synthesis step against each worker's raw output.

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
| Task-Capability Mismatch Rate | >5% of assignments |
| Synthesis Drop Rate (worker outputs missing from final) | >1% of runs |
| Unassigned Subtask Rate | >0% (target zero) |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Capability Mismatch Assignment | Subtask assigned to a worker whose capability profile doesn't cover the required skill | High |
| Worker Output Dropped from Synthesis | Completed worker output is not present in the final coordinator synthesis | High |
| Decomposition Gap Detected | An identified necessary subtask has no assigned worker at execution start | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
