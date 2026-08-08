# Plan-State Mismatch

## Issue: Agent continues an old plan after new evidence invalidates it.

**Frequency**: Common

**Symptoms**
- New user correction ignored; old branch continued.
- User provides a corrected shipping address mid-conversation, but the agent's next action still ships to the original (wrong) address from earlier in the plan.
- A tool result contradicts an assumption baked into the current plan (e.g., "item is out of stock") yet the agent continues fulfillment steps built on the stale assumption.
- Agent's final summary references the original plan's outcome, not the actually-revised one, causing a mismatch between what was said and what was done.
- Plan continues referencing an entity (order, ticket, account) whose state changed externally (e.g., cancelled by the customer through another channel) mid-session.

**Root Cause**
Plans are generated once and then treated as fixed artifacts, with no state fingerprint or snapshot attached that would let the executor cheaply detect when the world has moved on; nothing in the execution loop mandates a re-read of the latest user turn or tool result before the next step fires, especially across long, uninterrupted tool-call sequences optimized for throughput rather than built with safety checkpoints. Compounding this, conversational corrections ("actually...") are easy for the model to acknowledge in text without that acknowledgment ever being wired to an actual plan update, so the agent can sound responsive while its execution state silently diverges from what the user believes is happening.

**Example**
```
A customer success agent is mid-way through processing an order-modification request when the customer sends a follow-up message: "actually, cancel that — ship to my new office address instead, 500 Market St." The agent acknowledges the message conversationally but continues executing the plan it had already committed to — updating the item quantity and confirming shipment to the original home address — because the plan artifact it is executing against was generated before the correction and nothing in the execution loop re-checked it against the new user input. The customer receives a shipping confirmation to the wrong address and has to contact support again to unwind it.
```

**Contributing Factors**
- No mechanism ties incoming user messages during execution to a mandatory plan re-evaluation step; the agent treats the plan as fixed once generated.
- Plan artifacts aren't stamped with the state/context they were generated from, so there is no cheap way to detect staleness.
- Long tool-call sequences run without checkpoints where the agent re-reads the latest user turn before continuing.
- Corrections phrased conversationally ("actually...") rather than as explicit commands are easy for the agent to acknowledge in text without actually updating the plan.
- Multi-step fulfillment workflows are optimized for throughput, discouraging pauses to re-verify assumptions mid-flight.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Mid-execution user correction | User corrects shipping address after agent has already started an order-modification plan | Agent halts the current plan, regenerates it incorporating the new address, and confirms the change before proceeding | Original plan continues executing (ships to old address) with no visible replan |
| Contradicting tool result | Inventory-check tool returns "out of stock" mid-plan for an item the plan assumed was available | Agent replans around the new information (backorder, substitute, notify customer) | Agent proceeds with fulfillment steps built on the now-false in-stock assumption |
| Externally changed entity state | Order referenced in the plan is cancelled by the customer via another channel mid-session | Agent detects the state change on next reference and halts/replans | Agent completes actions against the now-cancelled order as if nothing changed |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| ignored_correction_detection_rate_percent | > 95% of injected corrections caught and reflected in a plan diff | Inject a mid-session correction into eval transcripts and measure whether the resulting plan changes to match it |
| stale_plan_execution_rate_percent | < 1% | Compare each executed action's target state against the plan's originating state snapshot across the eval set |

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
| stale_plan_execution_rate_percent | > 0.5% |
| ignored_correction_rate_percent | > 1% |
| replan_trigger_latency_seconds | > 10s |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| **Action Executed on Stale Plan** | An action executes while the plan's state fingerprint no longer matches current world state | High |
| **User Correction Not Reflected in Plan** | A user correction message has no corresponding plan diff within one turn | High |
| **Replan Latency Exceeded** | Time from invalidating event to replan exceeds 10 seconds | Medium |

---

## References

- [MAST](https://arxiv.org/abs/2503.13657)
- Note: Multi-agent system failure taxonomy with system design, inter-agent misalignment, and task verification failures.
