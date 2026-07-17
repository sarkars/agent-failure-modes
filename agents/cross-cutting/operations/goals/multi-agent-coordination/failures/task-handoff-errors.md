# Task Handoff Errors

## Issue: Work Lost or Duplicated During Agent Transitions

**Frequency**: Common

**Symptoms**
- Tasks fall through cracks between agents
- Same work performed multiple times
- Progress lost during agent transitions
- Unclear ownership of subtasks

**Root Cause**
Multi-agent systems require explicit coordination of task ownership. When handoffs are implicit or poorly defined, work can be duplicated, dropped, or performed in wrong order. This is especially problematic in dynamic agent orchestration.

**Example**
```
Document Processing Pipeline:
Agent A: Extracts tables → marks task "complete"
Agent B: Expected to validate extractions
Agent C: Integrates validated data

Failure scenario 1 (dropped):
Agent A completes, Agent B never activated
Agent C receives unvalidated data

Failure scenario 2 (duplicated):
Agent A extracts tables
Agent B re-extracts tables (misunderstands task)
Agent C receives conflicting extractions

Result: Data integrity issues, wasted compute
```

**Handoff Failure Modes**
- **Missing handoff**: No agent picks up next task
- **Duplicate handoff**: Multiple agents claim same task
- **Premature handoff**: Task passed before completion
- **State loss**: Context not transferred with task
- **Ordering violation**: Tasks executed out of sequence

**Potential Effects**
- Incomplete workflows
- Duplicated compute costs
- Data inconsistency from parallel execution
- Deadlocks when agents wait for each other

---

## Test Scenario & Reproduction

### Scenario Setup
- Three-stage document pipeline: Agent A (extract tables), Agent B (validate extractions), Agent C (integrate validated data)
- No task queue with explicit ownership; handoff between agents is implicit ("Agent B is expected to validate")
- No handoff acknowledgment, idempotent task claiming, or state machine enforcing extract -> validate -> integrate ordering

### Trigger Mechanism
1. **Dropped-handoff variant**: Agent A completes extraction and marks the task "complete," but no mechanism confirms Agent B was actually triggered to pick up validation, so Agent C polls for "complete" tasks and consumes Agent A's output directly
2. **Duplicate-handoff variant**: Agent A extracts tables from the document; Agent B, misunderstanding its assigned task, independently re-extracts tables from the same document instead of validating; Agent C receives both outputs as if both were authoritative

**Example Reproduction Steps:**
```
1. Configure the pipeline with Agent A (extract), Agent B (validate), Agent C (integrate) and no explicit task queue/state machine
2. Feed a document into Agent A; have it extract tables and mark the task "complete" with no downstream acknowledgment check
3. Do not trigger Agent B (simulating scenario 1's "never activated")
4. Let Agent C poll for completed tasks and consume Agent A's raw, unvalidated output
5. Separately, rerun with Agent B active but instructed ambiguously so it re-extracts tables rather than validating (scenario 2)
6. Feed both Agent A's and Agent B's extraction outputs to Agent C
7. Inspect Agent C's final integrated output for validation-flag absence (scenario 1) or conflicting duplicate extractions (scenario 2)
```

### Expected Failure State
- Scenario 1: Agent C integrates data that was never validated, with no validation-flag precondition failure raised, despite the pipeline nominally requiring validation before integration
- Scenario 2: Agent C receives two independently-produced extraction results for the same document and cannot determine which is authoritative, producing data integrity issues
- No timeout or missing-handoff alert fires when Agent B fails to pick up the task in scenario 1
- No duplicate-claim detector flags Agent B's redundant re-extraction in scenario 2, resulting in wasted compute and inconsistent downstream data

---

## Mitigation Strategies

### Prevention
1. **Handoff acknowledgment required before "complete" is trusted**: Failure scenario 1 occurs because Agent A marks its task "complete" and nothing verifies Agent B actually picked it up — Agent C ends up consuming unvalidated data with no one noticing the validation step was skipped. Require the receiving agent (Agent B) to send an explicit acknowledgment back to the task queue before the handoff is considered closed; "complete" from the sender alone should never advance the pipeline state. Trade-off: acknowledgment adds a synchronization round-trip and a second point where the ack itself can be dropped.
2. **Idempotent task claiming to prevent scenario 2's duplicate re-extraction**: Agent B re-extracts tables because it "misunderstands task" — it has no way to check whether extraction already happened, so it redoes Agent A's work and produces conflicting output for Agent C. Give every task a unique, checkable ID with a status field ("extracted", "validating", etc.) that Agent B must read before acting, and reject/no-op if the status shows the work already occurred. Trade-off: requires all agents to consistently check and honor shared task state rather than acting purely on their local instructions.
3. **State machine with explicit valid transitions per pipeline stage**: Both failure scenarios stem from the pipeline (extract → validate → integrate) having no enforced ordering — Agent C can receive data whether or not validation happened, and Agent B can re-extract instead of validate. Define a state machine (extracted → validated → integrated) where each agent can only act when the task is in the state it expects, and invalid-state actions are rejected outright rather than silently executed. Trade-off: a rigid state machine can be brittle for pipelines that legitimately need occasional out-of-order or retry paths.

### Detection & Response
1. **Missing-handoff timeout on "complete" without downstream pickup**: Scenario 1's core symptom is Agent B "never activated" after Agent A completes — this is directly detectable by starting a timer when Agent A marks complete and alerting if no downstream agent claims the task within an expected window.
2. **Duplicate-claim detector on task ID**: Scenario 2's failure (Agent B re-extracting what Agent A already extracted) is detectable by logging every agent that claims work against a given task ID and flagging any task ID claimed by 2+ agents for the same stage.
3. **Downstream input-consistency check**: Agent C receiving "unvalidated data" (scenario 1) or "conflicting extractions" (scenario 2) both manifest as Agent C's input failing an expected precondition (validation-flag present, single consistent extraction). Have Agent C itself verify its input meets the contract for its stage before processing, and reject/escalate rather than silently proceeding on bad input.

### Architecture Patterns
1. **Explicit task queue with formal ownership, not implicit "next agent picks it up"**: Replace the ambient assumption that "Agent B is expected to validate" with a real task queue where Agent A enqueues a validation task explicitly addressed to Agent B (or the validation-capable pool), so there's a concrete, inspectable record of what's pending versus assumed. Deployment consideration: requires queue infrastructure (even a lightweight one) and discipline that agents never act outside queue-issued tasks.
2. **Task locking to make duplicate claims impossible, not just detectable**: Rather than only logging duplicate claims after the fact, use a compare-and-swap style lock on task ID + stage so Agent B's attempt to claim an already-claimed extraction task fails atomically instead of both Agent A and B's work landing in the pipeline. Deployment consideration: needs a consistent, low-latency lock store (e.g., a shared DB row or distributed lock) reachable by all agents.
3. **Completion verification gate before advancing pipeline stage**: Before Agent A's "complete" signal is allowed to unblock Agent B's stage, run an automated check that the claimed output actually exists and matches the expected schema (e.g., tables were actually extracted, not just an empty completion flag) — this catches a premature or false "complete" before it propagates. Deployment consideration: verification logic must be maintained per stage type, adding ongoing engineering cost as pipeline stages evolve.

### Metrics
1. **handoff_acknowledgment_rate**: Target > 99% of task completions receive downstream acknowledgment within SLA; Alert if < 95% over a rolling 1-hour window.
2. **duplicate_claim_rate**: Target < 1% of tasks claimed by more than one agent for the same stage; Alert if > 3%.
3. **stale_pending_task_count**: Target 0 tasks in "pending" state beyond 2x expected stage duration; Alert if any task exceeds 3x expected duration (matching scenario 1's dropped-task pattern).
4. **pipeline_state_consistency**: Target 100% of Agent C (downstream) inputs pass precondition checks (validated, non-conflicting) before processing; Alert if < 99%.

### Alerts
1. **Orphaned Completed Task** (P1): Condition - a task is marked "complete" by its owning agent but no downstream agent acknowledges pickup within the expected window. Action: auto-escalate the task back to the queue for reassignment and alert the pipeline owner (matches failure scenario 1's dropped handoff).
2. **Duplicate Task Claim** (P1): Condition - two agents claim the same task ID for the same pipeline stage. Action: reject the second claim atomically, log which agent's output is authoritative, and discard the duplicate work before it reaches downstream agents (matches failure scenario 2).
3. **Downstream Precondition Failure** (P2): Condition - a downstream agent (e.g., Agent C) receives input that fails its stage's required precondition (e.g., missing validation flag). Action: block processing, return the task to the correct prior stage, and flag the pipeline for a handoff-contract review.

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Task verification failures
- [Agentic Document Processing](https://www.llamaindex.ai/blog/agentic-document-processing) - Pipeline coordination
- [Magentic-One: Generalist Multi-Agent System](https://arxiv.org/abs/2411.04468) - Multi-agent orchestration
