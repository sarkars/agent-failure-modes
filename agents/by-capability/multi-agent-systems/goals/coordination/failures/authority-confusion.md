# AI Agent Authority Confusion: Causes and Fixes

## Issue: Agents disagree on who has final say, and the system silently picks a winner instead of resolving the conflict. This is common in flat multi-agent orchestration (e.g., LangGraph or CrewAI-style peer topologies) where no agent is declared authoritative for a given decision domain.

**Frequency**: Common

**Symptoms**
- Final answer merges incompatible outputs.
- Two agents claim ownership of the same decision and the system silently applies a last-writer-wins rule.
- Downstream consumers receive contradictory field values (e.g., both "high risk" and "low risk" labels) with no indication of which agent's judgment took precedence.
- Human reviewers cannot reconstruct after the fact which agent's output was authoritative, because precedence was never logged.

**Root Cause**
No ownership or priority map exists that assigns which agent is authoritative for which decision domain, so when two agents' conclusions touch the same field there is no rule to consult. The topology compounds this: agents write to shared output state as peers with no gatekeeper, and the aggregation step is implemented as naive concatenation or last-write-wins rather than an explicit conflict-resolution policy, so whichever output arrives last (or gets merged first) wins by accident rather than by design. This gap tends to widen over time as new agents are added incrementally without anyone revisiting the original authority model, so newer agents' scopes silently overlap with older ones that were never designed to share a decision space.

**Example**
```
Agent A (compliance-checker) flags a loan application: "reject: insufficient collateral."
Agent B (underwriter) independently outputs: "approve: strong income ratio."
Aggregator concatenates both into the final report as "approve, pending review of
collateral concerns" -- a synthesized answer neither agent produced, because no
precedence rule defines which agent is binding on collateral vs. income criteria.
```

**Contributing Factors**
- No declared ownership/priority map assigning which agent is authoritative for which decision domain (e.g., risk vs. compliance vs. pricing).
- Flat peer-to-peer topology where any agent can write to shared output state without a gatekeeper.
- Aggregation/merge step implemented as naive concatenation or last-write-wins rather than an explicit conflict-resolution policy.
- Agents added incrementally over time without revisiting the original authority model, so newer agents' scopes overlap with older ones.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Overlapping-domain conflict | Two agents (compliance, underwriting) each rule on the same loan with staged conflicting facts | System resolves to the pre-declared authoritative agent's verdict and logs the override | Final output blends both verdicts or picks arbitrarily instead of following the authority map |
| Silent last-writer test | Agent A writes a verdict, then Agent B writes a conflicting verdict to the same field milliseconds later | System flags the conflict and requires explicit resolution before finalizing | Final answer reflects whichever agent wrote last with no conflict flag raised |
| Missing authority declaration | New agent added to the pipeline without an authority-map entry, given a decision overlapping an existing agent | Orchestrator rejects the ambiguous configuration at validation time | Pipeline runs anyway and produces merged/contradictory output at runtime |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Authority Map Coverage | 100% of decision domains mapped | Static analysis of orchestration config against agent output schemas |
| Unresolved Conflict Rate | <1% of multi-agent runs | Percentage of runs where two agents write conflicting values to the same output field with no logged resolution |
| Precedence Override Traceability | 100% | Percentage of conflict resolutions with a logged "agent X overrode agent Y because Z" record |

---

**How to fix it**: declare an explicit authority map and conflict-resolution policy so the system stops guessing which agent's output is binding.

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
| Unresolved Authority Conflict Rate | >1% of runs |
| Silent Overwrite Count (no resolution log) | >5/day |
| Authority Map Staleness | >30 days since last review vs. new agent additions |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Authority Contract Violation | Two agents write conflicting values to the same field with no precedence rule matched | High |
| Silent Last-Write Detected | Output field overwritten without a logged conflict-resolution decision | Medium |
| Unmapped Agent Deployed | New agent goes live with overlapping decision scope and no authority-map entry | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
