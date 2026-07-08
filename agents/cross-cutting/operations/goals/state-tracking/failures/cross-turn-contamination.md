# Cross-Turn Contamination

## Issue: Current task is polluted by unrelated previous context.

**Frequency**: Occasional

**Symptoms**
- Irrelevant memory/preferences appear in answer.
- [Add more specific symptoms]

**Root Cause**
Current task is polluted by unrelated previous context.

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
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
