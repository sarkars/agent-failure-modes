# Cross-Turn Contamination

## Issue: Current task is polluted by unrelated previous context.

**Frequency**: Occasional

**Symptoms**
- Irrelevant memory/preferences appear in answer.
- Response references entities, constraints, or preferences from an earlier unrelated topic that never appeared in the current task's turns.
- No task-boundary marker exists in the trace at the point where the topic clearly switched.
- User reacts with confusion ("what does that have to do with...") because the response mixes content from two unrelated conversations.
- The same raw transcript is reused verbatim across topic switches instead of being scoped to the active task.

**Root Cause**
Current task is polluted by unrelated previous context.

**Example**
```
User (turns 1-5): plans a vacation, mentions "beach destinations,
budget under $2000."
User (turn 6): "Can you help me debug this Python function? It's
throwing a KeyError."
Agent: "Sure, let's debug this. By the way, given your budget under
$2000, have you considered checking error-handling costs before
scaling this service?"
The debugging response nonsensically drags in the earlier vacation
budget because the full raw transcript, not a task-scoped context,
was fed into generation, and no topic-switch classifier ever marked
a boundary between the two unrelated tasks.
```

**Contributing Factors**
- The orchestration layer carries the full raw conversation transcript forward indefinitely instead of scoping context per task.
- No topic-drift or entity-similarity check runs before reusing prior-turn context for the current response.
- No explicit task-boundary detection (topic switch, new goal, "let's move on") exists to mark where old context should stop being carried forward.
- Long sessions accumulate many unrelated sub-topics, increasing the chance that stale content resurfaces in an unrelated later turn.
- Memory/preference retrieval pulls broadly from session history rather than from a durable, explicitly-scoped memory store.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Abrupt topic switch | 5 turns of unrelated small talk (vacation planning) followed by an explicit, unrelated task request (debug a script) | Response addresses only the debugging request with no reference to vacation content; a task-boundary event appears in the trace | Response text or reasoning references vacation-related entities/preferences absent from the current task's turns |
| Carry-forward allowlist check | User legitimately references prior-task info ("use the same shipping address as before") | Agent pulls the address via an explicit memory lookup rather than leaking the entire prior task's raw context | Agent surfaces unrelated details from the earlier task beyond just the referenced fact |
| Long-session drift | 40+ turn session spanning 4 distinct unrelated sub-topics, final turn asks about topic 1 again | Agent correctly reconstructs topic 1 context without bleeding in topics 2-4 | Response mixes entities/constraints from intervening unrelated topics into the topic-1 answer |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_contamination_detection_rate_percent | >= 95% of injected topic-switch test cases correctly flagged | Run the boundary classifier against a labeled eval set of topic-switch and non-switch transcripts, measure recall |
| eval_irrelevant_entity_rate_percent | 0% of generated eval responses contain entities from an unrelated injected prior turn | Automated entity extraction on eval outputs, diffed against the current task's turn content |
| eval_carry_forward_precision_percent | >= 98% of legitimate cross-task references resolve via explicit lookup, not raw leakage | Compare eval responses referencing prior-task facts against expected explicit-memory-lookup provenance |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a conversational agent that carries the full raw conversation transcript forward on every turn, with no task-boundary detection or context-window scoping per task
- No topic-drift detection checks similarity between the current turn and prior turns before reusing that context
- Earlier in the session, the user discussed an unrelated topic (e.g., asked about vacation destinations) before switching to an entirely different task (asking for help debugging code)

### Trigger Mechanism
1. The user's session begins with a conversation about vacation planning, including specific preferences (e.g., "I prefer beach destinations, budget under $2000")
2. The user then switches topics entirely, asking the agent to help debug a Python script, with no explicit signal recognized as a task boundary
3. The agent constructs its response using the full raw transcript, including the earlier vacation preferences, which remain in context
4. The agent's debugging response includes an irrelevant reference to the earlier unrelated topic

### Example Reproduction Steps
```
1. Turn 1-5: User discusses vacation planning: "I prefer beach
   destinations, budget under $2000"
2. Turn 6: User: "Can you help me debug this Python function? It's
   throwing a KeyError"
3. Agent response includes: "Sure, let's debug this. By the way,
   given your budget under $2000, have you considered checking
   error-handling costs..." (nonsensical irrelevant reference bleeding
   through from turn 1-5 context)
4. Check for a task-boundary marker inserted between turn 5 and
   turn 6 -> none present, since no topic-switch classifier ran
5. Measure contamination_flag_rate for this session -> flagged, since
   the debugging response references vacation-budget content absent
   from the current task's turns
```

### Expected Failure State
The agent's debugging response contains a nonsensical reference to the user's earlier, entirely unrelated vacation budget discussion, confusing the user and signaling that irrelevant prior context leaked into the current task. A correctly defended system detects the topic switch at turn 6, inserts a task-boundary marker, and constructs the debugging response's context from only the current task's turns, excluding the vacation-planning content entirely.

## Mitigation Strategies

### Prevention
1. **Explicit Task Boundary Markers**: The orchestration layer tags each turn with a task_id, and detects task switches (new topic, new goal, explicit "let's move on") to insert a boundary marker into the context. Content from before the boundary is excluded from the working set used to build the next prompt unless explicitly re-referenced.
2. **Context Window Scoping Per Task**: Rather than carrying the full raw conversation history forward indefinitely, the agent constructs each turn's context from a scoped subset: current task's turns plus explicitly durable memory (via the memory system), not the entire unfiltered transcript, limiting the surface for unrelated prior content to bleed in.
3. **Topic-Drift Detection Before Context Reuse**: Before reusing prior-turn context (e.g., resolved entities, assumed constraints) for the current response, check topic/entity similarity between the current turn and the turns being reused; below a similarity threshold, treat it as a new task and reset rather than carrying forward.

### Detection & Response
1. **Irrelevant-Reference Detection**: Scan responses for mentions of entities/preferences/constraints that don't appear in the current task's turns and weren't retrieved from durable memory, flagging them as likely contamination from unrelated prior context still sitting in the raw context window.
2. **User Confusion Signal**: Monitor for user reactions indicating the response referenced something unrelated ("what does that have to do with...", "I wasn't asking about that") and trace back to which prior-turn content leaked into context construction.
3. **Task-Switch Miss Audit**: Sample sessions where the topic clearly changed and check whether a task boundary was actually inserted; missed boundary detections are the root cause to fix, not just the individual contamination symptom.

### Architecture Patterns
1. **Task-Segmented Context Store**: Conversation history is stored and indexed by task_id, and prompt assembly pulls only the active task's segment plus explicit cross-task memory lookups, rather than a single flat, ever-growing transcript.
2. **Boundary Detection Service**: A lightweight classifier runs on each incoming turn to decide same-task-continuation vs new-task-start, emitting a boundary event that the context-assembly layer consumes to decide what to carry forward.
3. **Explicit Carry-Forward Allowlist**: When a new task legitimately needs a fact from a prior task (e.g., "use the same shipping address as before"), it is pulled explicitly through the memory/retrieval system with a specific reference, not implicitly inherited by leaving it in the raw context window.

### Metrics
1. **contamination_flag_rate_percent**: Target: < 1% of responses; Alert threshold: > 3%
2. **task_boundary_detection_recall_percent**: Target: > 95% of true topic switches detected; Alert threshold: < 85%
3. **user_confusion_signal_rate_percent**: Target: < 0.5%; Alert threshold: > 1.5%
4. **mean_context_entities_from_unrelated_task**: Target: ~0 per response; Alert threshold: > 0.5 average

### Alerts
1. **Contamination Spike** (P2 - Warning): Condition - contamination_flag_rate_percent exceeds 3% over a rolling day. Action: Review recent context-assembly changes, sample flagged sessions, patch boundary detection or scoping logic.
2. **Boundary Detector Recall Drop** (P2 - Warning): Condition - task_boundary_detection_recall_percent falls below 85% on eval set. Action: Retrain/tune the boundary classifier, add missed cases to regression suite before redeploy.
3. **Repeated User Confusion in Session** (P3 - Info): Condition - 2+ user confusion signals within a single session. Action: Force a manual context reset for that session, log for classifier improvement.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| contamination_flag_rate_percent | > 3% |
| task_boundary_detection_recall_percent | < 85% |
| user_confusion_signal_rate_percent | > 1.5% |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Contamination Spike | contamination_flag_rate_percent exceeds 3% over a rolling day | Warning |
| Boundary Detector Recall Drop | task_boundary_detection_recall_percent falls below 85% on eval set | Warning |
| Repeated User Confusion in Session | 2+ user confusion signals within a single session | Info |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
