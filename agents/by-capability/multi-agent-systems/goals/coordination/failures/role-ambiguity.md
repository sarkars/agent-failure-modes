# Role Ambiguity

## Issue: Agents do not know who owns which responsibility.

**Frequency**: Common

**Symptoms**
- Duplicate or missing work across agents.
- Two agents independently perform the same subtask (e.g., both call the same external API or edit the same file), producing conflicting results.
- A required subtask (e.g., input validation) is never performed because each agent assumed another agent owned it.
- Agents ask each other or the user clarifying questions about ownership mid-task ("is this my responsibility or yours?") instead of proceeding.

**Root Cause**
Responsibilities are described to agents in overlapping natural language -- "ensure quality," "handle data issues" -- that gets assigned to more than one agent without ever designating a single owner, so each agent is left to infer from its own prompt whether a given subtask is its job. There is no shared responsibility registry, RACI-style or otherwise, that an agent could query at runtime to resolve that ambiguity, and because agent selection and routing can change dynamically from run to run, the set of participants -- and therefore the implicit boundaries between their roles -- is never fixed long enough to be reliably tested. The more agents a workflow includes, the more combinations of implicit, untested scope overlap become possible, so duplicate or dropped work becomes a matter of probability rather than an edge case.

**Example**
```
Agent A (data-fetcher) and Agent B (data-validator) are both given the
system prompt "ensure the dataset is clean before analysis."
Run 1: A fetches and also silently drops malformed rows (assuming that's
its job); B receives already-cleaned data and validates nothing, letting a
corrupted row pass through untouched on a run where A skipped the drop.
```

**Contributing Factors**
- Overlapping natural-language role descriptions ("ensure quality," "handle data issues") are assigned to multiple agents without a single owner per responsibility.
- No shared task/responsibility registry (e.g., a RACI-style matrix) that agents can query at runtime.
- Dynamic agent selection/routing changes the set of participating agents per run, so role boundaries are never fixed.
- High agent count in the workflow increases the combinatorial chance that two agents' implicit scopes overlap.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Ownership collision detection | Task where two agents' prompts both plausibly cover "input validation" | Only one agent performs validation; the other explicitly defers/no-ops with a logged reason | Both agents perform validation redundantly, or outputs conflict |
| Coverage gap detection | Task requiring 3 distinct subtasks assigned across 2 agents with an intentional gap in the prompt | System flags the uncovered subtask before completion | Task completes with the gap subtask silently never performed |
| Role registry lookup | Agent queries the shared responsibility registry mid-task for an ambiguous subtask | Agent receives an unambiguous single-owner answer and proceeds accordingly | Agent proceeds on assumption without querying, or the registry returns conflicting owners |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Duplicate-work rate | <2% | % of eval tasks where two agents' traces show redundant execution of the same subtask |
| Coverage completeness | 100% | % of required subtasks (per task spec) that appear performed exactly once in the trace |
| Ownership-query rate | tracked, no fixed target | Count of times agents explicitly query the responsibility registry vs. proceed on assumption, per task |

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
| Duplicate subtask execution rate | >3% of tasks |
| Missing subtask rate | >1% of tasks |
| Inter-agent ownership clarification requests | >10% of tasks |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Duplicate execution detected | Trace shows two agents completing the same subtask (same tool/target) within one workflow run | High |
| Uncovered required subtask | A required subtask from the task spec has zero corresponding execution in the trace | High |
| Ownership deadlock | Two or more agents repeatedly defer the same subtask to each other without resolution | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
