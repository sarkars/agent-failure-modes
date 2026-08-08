# Duplicate Work

## Issue: Multiple agents solve the same subtask independently.

**Frequency**: Occasional

**Symptoms**
- Repeated outputs/calls from different agents.
- Two or more agents independently call the same expensive external tool/API for the same input, inflating cost and latency.
- The final output contains redundant or slightly inconsistent versions of the same finding merged together, confusing downstream consumers.
- Resource usage (tokens, API quota, compute) scales worse than task complexity would justify because of redundant execution.

**Root Cause**
Task decomposition happens without any check for overlapping scope between the subtasks it produces, so two branches of the same fan-out can end up covering identical ground without anyone noticing at planning time. There is no shared task registry or claim/lock mechanism to prevent two agents from picking up the same unit of work, which matters most in high-parallelism architectures where many agents pull independently from a shared queue. Because agents also have no visibility into what their peers are currently doing or have already finished, each one proceeds as if it were the only one addressing the problem, and the resulting redundant tool calls and near-duplicate outputs get merged into the final result as if they were independent corroboration.

**Example**
```
Task decomposition splits "research competitor pricing" into two parallel
subtasks that both end up querying the same competitor's pricing page. Agent A
and Agent C each independently call the web-search tool, retrieve the same page,
and produce two separate summaries with slightly different wording and one
differing number (rounding). The aggregator includes both summaries in the final
report as if they were corroborating independent sources, doubling token cost
and confusing the reader with near-duplicate, slightly conflicting figures.
```

**Contributing Factors**
- Task decomposition performed without checking for overlapping scope between parallel subtasks.
- No shared task registry or claim/lock mechanism preventing two agents from picking up the same unit of work.
- High-parallelism fan-out architectures where many agents pull from a shared task queue without deduplication logic.
- Agents lack visibility into what other agents are currently working on or have already completed.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Overlapping subtask detection | Decompose a task into subtasks with intentional scope overlap | System detects the overlap and merges/reassigns before execution | Both overlapping subtasks execute independently, producing duplicate work |
| Shared-queue race condition | Two agents poll the same task queue simultaneously for the same item | Claim/lock mechanism ensures only one agent executes the item | Both agents dequeue and execute the same item independently |
| Redundant tool-call detection | Run a fan-out task where two agents are likely to need the same external resource | System caches/shares the first agent's tool result with the second | Both agents independently call the same external tool for identical input |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Duplicate Subtask Rate | <2% | Percentage of decomposed subtasks with >50% scope overlap with another subtask in the same run |
| Redundant Tool-Call Rate | <5% | Percentage of external tool calls that are near-duplicates (same tool + same/similar input) within a single run |
| Task Claim Conflict Rate | <1% | Percentage of task-queue dequeues where two agents claim the same item before lock enforcement |

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
| Duplicate Subtask Rate | >5% of runs |
| Redundant External Tool Calls | >10% of total tool calls |
| Wasted Compute/Token Spend from Duplication | >5% of run budget |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Overlapping Subtask Execution | Two or more agents execute subtasks with substantially overlapping scope in the same run | Medium |
| Redundant Tool Call Spike | Duplicate external tool calls for identical input exceed baseline rate | Medium |
| Task Queue Double-Claim | Same queue item claimed and executed by more than one agent | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
