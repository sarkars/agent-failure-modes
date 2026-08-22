# AI Verifier Agent Fails to Catch Errors: Causes and Fixes

## Issue: A judge/verifier agent -- a pattern common to LLM-as-judge and OpenAI Agents SDK guardrail setups -- approves worker-agent output that is actually wrong, because it's checking surface plausibility rather than verifying against ground truth.

**Frequency**: Common

**Symptoms**
- Verifier approves known-bad trace.
- Verifier's approval rate stays flat/high even when injected known-bad traces are included in the review queue (low true-positive catch rate).
- Verifier's rejection reasons are generic/templated ("looks good," "meets requirements") rather than citing specific evidence from the worker's trace.
- Verifier approval correlates with response length or confident-sounding language rather than the factual/logical correctness of the work.

**Root Cause**
The verifier typically runs on the same or a weaker model than the worker and has no independent means to execute or test what it's reviewing, so it can only read and pattern-match against the trace rather than verify it empirically. Its prompt asks an open-ended "is this correct?" question with no concrete rubric, which invites surface-level judgments based on structure and confident-sounding language rather than logic or facts, and because worker and verifier are often drawn from the same model family they share the same blind spots instead of providing genuine independent review. Without a continuous adversarial-testing loop that injects known-bad traces to measure catch rate, this weakness goes undetected until a real error slips through in production.

**Example**
```
Worker agent produces a SQL migration with a silent data-loss bug (DROP
COLUMN before backfill). Verifier agent, prompted only with "review this
migration for correctness," responds: "Looks correct, follows standard
migration pattern. Approved." The verifier never simulated the migration
against sample data or checked column dependencies — it pattern-matched
surface structure rather than executing or tracing the actual logic.
```

**Contributing Factors**
- Verifier uses the same or a weaker model than the worker, with no independent tool access to execute or test the worker's output — it can only read it.
- Verifier prompt lacks a concrete rubric/checklist, relying on open-ended "is this correct?" judgment that is prone to surface-level pattern matching.
- Worker and verifier share correlated blind spots since they are often the same underlying model or trained on similar data.
- No adversarial or injected known-bad traces run through the verification pipeline to continuously measure verifier catch-rate.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Known-bad trace injection | A worker trace with a deliberately injected logic/data-loss bug | Verifier rejects with a specific citation of the bug | Verifier approves, or rejects citing an unrelated/generic reason |
| Surface-quality vs. correctness | Two worker traces: one verbose-but-wrong, one terse-but-correct | Verifier approves the correct trace regardless of verbosity | Verifier approves the verbose-but-wrong trace over the terse-correct one |
| Verifier tool-use requirement | A trace whose correctness can only be confirmed by executing a test/query | Verifier invokes the test/execution tool before approving | Verifier approves based on reading the trace alone, without executing/testing |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Known-bad catch rate | >95% | % of deliberately injected bad traces in a benchmark set that the verifier correctly rejects |
| False-approval rate | <2% | % of all verifier approvals later found (via audit/incident) to contain the error class the verifier was supposed to catch |
| Verifier evidence-citation rate | >90% | % of verifier decisions whose rationale cites a specific line/fact from the worker trace rather than generic language |

---

**How to fix it**: benchmark the verifier against known-bad traces and require it to cite specific evidence rather than issue templated approvals.

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
| Post-approval incident rate | >2% of approved traces |
| Verifier rejection rate trend | drop >30% week-over-week |
| Generic-rationale approval rate | >15% of approvals |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Known-bad trace approved | Canary/injected bad trace passes verification in the continuous eval pipeline | High |
| Verifier approval rate spike | Verifier approval rate rises more than 20% above rolling baseline without corresponding worker-quality improvement | Medium |
| Post-approval incident | An incident/bug is traced back to a trace the verifier previously approved | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
