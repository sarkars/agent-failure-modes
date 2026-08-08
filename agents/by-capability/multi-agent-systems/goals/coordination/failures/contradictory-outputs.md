# Contradictory Outputs

## Issue: Agents disagree and no resolver exists.

**Frequency**: Common

**Symptoms**
- Conflicting recommendations without arbitration.
- End users or downstream systems receive two mutually exclusive answers (e.g., "approve" and "deny") with no indication which to trust.
- Disagreement is detected only after the fact by a human, because no automated arbitration step runs before output is finalized.
- The same disagreement recurs for similar inputs because there is no learned or codified tie-breaking rule.

**Root Cause**
There is no designated arbiter agent or deterministic tie-breaking policy defined anywhere in the pipeline, so when two agents optimize genuinely different objectives -- growth versus margin, for instance -- with no shared reconciliation criteria, their outputs have nowhere to converge. The aggregation step makes this worse by concatenating or passing through whatever each agent produces rather than requiring the outputs to agree before being finalized. Since the agents run in parallel with no communication channel to negotiate or even flag the conflict to one another, neither agent nor the system has any opportunity to notice the contradiction before it reaches the end user.

**Example**
```
Agent A (pricing agent) recommends a 15% discount based on customer loyalty tier.
Agent B (margin-protection agent) recommends a 0% discount based on current
inventory cost pressure. Both recommendations are appended to the customer-facing
quote generator as-is; the generated quote reads "recommended discount: 15%" in one
section and "no discount available" in another, with no arbitration step ever
invoked.
```

**Contributing Factors**
- No designated arbiter agent or deterministic tie-breaking policy for cross-agent disagreement.
- Agents optimize different, non-overlapping objective functions (e.g., growth vs. margin) with no shared reconciliation criteria.
- Output aggregation pipeline concatenates or passes through all agent outputs rather than requiring convergence before finalizing.
- Agents run in parallel/independently with no communication channel to negotiate or flag conflicting conclusions to each other.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Direct conflict injection | Configure two agents with inputs guaranteed to produce opposing recommendations | Arbiter agent or resolution policy selects/blends a single final answer with rationale logged | Both conflicting recommendations reach the final output unresolved |
| Silent pass-through check | Run pipeline on a case with known agent disagreement and inspect the final customer-facing output | Output contains one coherent recommendation | Output contains both contradictory recommendations or an incoherent blend |
| Recurring conflict pattern | Run the same conflict-prone input scenario 10 times | Resolution is consistent and traceable to a defined policy each time | Resolution (or lack thereof) varies run to run with no consistent policy applied |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Unresolved Disagreement Rate | <1% of multi-agent runs | Percentage of runs where two agents produce contradictory outputs on the same decision with no arbitration record |
| Arbitration Coverage | 100% | Percentage of detected disagreements that trigger a defined arbiter/tie-break process |
| Resolution Consistency | >95% | Percentage of repeated identical-conflict scenarios resolved the same way |

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
| Unarbitrated Conflict Rate | >1% of runs |
| Contradictory Output Reaching End User | >0/week (target zero) |
| Mean Time to Arbitration | >5s per detected conflict |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Unresolved Contradiction Shipped | Final output contains mutually exclusive recommendations with no arbitration log entry | High |
| Arbiter Agent Unavailable | Arbitration step fails or times out and the pipeline proceeds without resolving the conflict | Critical |
| Repeated Conflict Pattern | Same input signature produces agent disagreement 3+ times without a policy update | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
