# Plan-State Mismatch

## Issue: Agent continues an old plan after new evidence invalidates it.

**Frequency**: Common

**Symptoms**
- New user correction ignored; old branch continued.
- [Add more specific symptoms]

**Root Cause**
Agent continues an old plan after new evidence invalidates it.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **State-Change Triggered Replan**: Define a taxonomy of state-invalidating events (user correction, contradicting tool result, external state change detected on re-query) and wire each event type to automatically trigger plan re-evaluation before the next action executes, rather than relying on the agent to notice on its own.
2. **Plan Versioning Tied to State Snapshot**: Every plan is stamped with the world-state snapshot (or hash) it was generated from. When new evidence changes that snapshot, the plan is marked stale and requires explicit re-confirmation or regeneration before further actions can reference it.
3. **Explicit Correction Acknowledgment Requirement**: When a user issues a correction, the agent must echo the correction back and produce a revised plan diff showing exactly what changed before continuing execution; silent continuation on the old plan is disallowed by the orchestrator.

### Detection & Response
1. **Stale-Plan Execution Detector**: Before each action, compare the current world-state hash to the plan's originating state hash; a mismatch blocks execution and forces a replan cycle instead of allowing the action to proceed on outdated assumptions.
2. **Ignored-Correction Scanner**: Run a pattern/NLP check over user messages classified as corrections, verifying the subsequent plan diff actually reflects the correction; corrections with no corresponding plan change are flagged.
3. **Contradiction Monitor**: Continuously compare incoming tool outputs against the assumptions embedded in the current plan; when a tool result contradicts a plan assumption, raise a contradiction event that routes into the replan trigger.

### Architecture Patterns
1. **State Snapshot & Diffing Service**: Tags every plan artifact with a fingerprint of the world state at creation time and computes diffs against the live state on demand, giving the executor a cheap staleness check.
2. **Event-Driven Replanning Trigger**: A pub/sub layer where state-invalidating events (corrections, contradicting results, external changes) publish to a topic the planner subscribes to, decoupling detection from the main execution loop.
3. **Correction Ledger**: An explicit log of every user correction received and its incorporation status (pending/incorporated/ignored), auditable independently of the conversation transcript.

### Metrics
1. **stale_plan_execution_rate_percent**: Target: 0%; Alert threshold: > 0.5%
2. **ignored_correction_rate_percent**: Target: 0%; Alert threshold: > 1%
3. **replan_trigger_latency_seconds**: Target: < 2s; Alert threshold: > 10s
4. **plan_state_mismatch_incidents_per_week**: Target: 0; Alert threshold: > 2

### Alerts
1. **Execution on Stale Plan** (P1 - Critical): Condition - an action executed while the plan's state fingerprint no longer matches current world state. Action: Halt execution, force immediate replan, review for user-facing impact.
2. **Ignored User Correction** (P1 - Critical): Condition - a user correction message has no corresponding plan diff within one turn. Action: Interrupt session, surface correction to agent explicitly, require acknowledgment before continuing.
3. **Replan Trigger Latency Exceeded** (P2 - Warning): Condition - time from invalidating event to replan exceeds 10s. Action: Investigate event pipeline/pub-sub backlog.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | High |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
