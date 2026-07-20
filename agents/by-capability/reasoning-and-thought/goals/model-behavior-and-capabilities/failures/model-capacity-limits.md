# Model Capacity Limits

## Issue
An agent hands a task to the underlying model whose combined complexity — number of constraints, depth of multi-step reasoning, size of working set held "in mind" across a long tool-calling loop — exceeds what that model can reliably handle in a single pass. Unlike a hard error, the failure is silent: the model still produces a fluent, well-formatted answer, but it drops constraints, skips reasoning steps, or produces a plausible-looking but wrong result. Nothing in the response signals that the task was too much for the model.

**Frequency**: Common

**Symptoms**
- Correct-looking output that silently violates one or more of the stated constraints
- Quality degrades sharply once the number of simultaneous sub-goals, entities, or constraints passes a threshold, with no gradual warning
- Agent self-reports success ("done, all requirements met") while a downstream check finds missed requirements
- Simplifying the same task into two sequential calls produces a materially better result than one combined call
- Errors cluster on tasks requiring the model to track state across many interdependent variables (e.g. multi-constraint scheduling, large diff review, cross-referencing 15+ documents)

## Root Cause
Language models have a finite effective reasoning capacity per forward pass that is not a documented hard limit — it is a soft, task-dependent ceiling shaped by how many independent facts and constraints the model must hold in attention simultaneously. As task complexity rises, the model doesn't fail cleanly; it starts trading off which parts of the problem to attend to fully, silently deprioritizing constraints that are stated later in the prompt, less frequently repeated, or less salient to the model's learned priors. Because the model was trained to always produce a confident, complete-looking answer, there is no built-in signal that distinguishes "I solved this fully" from "I solved the parts I could track." Agent frameworks compound this by concatenating many sub-tasks into one call to save latency and tool-call budget, pushing the effective task complexity above the model's reliable capacity without any capacity check in the loop.

## Example
```
An agent is asked to refactor a 900-line billing module in one call, with a
system prompt listing 9 constraints: preserve public API signatures, keep
backward compatibility with two deprecated fields, maintain existing log
format, add null checks, extract three helper functions, update the two
call sites in the invoicing service, keep line-level diff minimal, avoid
introducing new dependencies, and update the corresponding unit test file.

The model returns a clean, confidently-described refactor. Code review later
finds: the two deprecated fields were silently dropped, the log format
changed from "user_id=%s" to "userId: %s", and the unit test file was left
untouched — three of the nine constraints, all introduced in the back half
of the prompt.

Re-running the same refactor as three sequential calls (structure, then
compatibility fields, then tests) and asking the model to state before each
one which prior constraints still apply, catches all nine correctly.
```

## Statistics
| Finding | Context |
|---------|---------|
| Constraint-adherence rates typically drop from ~95% to 60-75% once a single prompt carries more than 7-8 independent, simultaneously-active constraints | Estimated from internal constraint-checklist evaluations on multi-requirement coding and writing tasks |
| Splitting a high-complexity task into 2-3 sequential model calls reduces missed-constraint rate by roughly 40-60% versus one combined call | Typical range observed across agent frameworks that support task decomposition |
| Models rarely (well under 5% of cases) proactively state that a task exceeded their ability to track all requirements | Estimated from manual review of model self-assessments on high-complexity tasks |

## Mitigations
1. **Complexity budgeting before dispatch**: Estimate a task's constraint count and interdependency depth before sending it to the model, and automatically decompose tasks that exceed a calibrated complexity threshold into smaller sequential calls.
2. **Explicit constraint checklists**: Require the model to restate every constraint from the prompt and mark each as addressed/not-addressed at the end of its response, making silent drops visible instead of invisible.
3. **Post-hoc constraint verification**: Run a separate, narrower verification pass (or deterministic check) that re-reads the original requirements against the output, rather than trusting the generating call's own success claim.
4. **Task decomposition by default for high-fan-out work**: For tasks that touch many files, entities, or constraints, default to a plan-then-execute pattern with one focused sub-task per call instead of one combined mega-call.
5. **Escalate to a higher-capacity model at a measured threshold**: When complexity budgeting flags a task above the current model's reliable range, route to a stronger model rather than accepting silent degradation from the current one.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| constraint_miss_rate | Fraction of stated requirements not satisfied in output, measured by post-hoc verification | Alert if > 10% |
| task_complexity_score_at_dispatch | Estimated constraint/entity count of tasks sent as a single call | Alert if p95 exceeds calibrated model ceiling |
| decomposed_vs_combined_quality_delta | Quality difference between decomposed and single-call handling of comparable tasks | Alert if delta > 15% favoring decomposition |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High-complexity single-call dispatch | A task exceeding the calibrated complexity threshold is sent as one undivided call | Medium | Route through task decomposition, log for review |
| Constraint miss on verified output | Post-hoc verification finds a stated constraint unmet | High | Block delivery, trigger decomposition retry or escalation to stronger model |

## Related Patterns
- [Model Context Length Behavior Change](./model-context-length-behavior-change.md) - both describe capacity ceilings, one from task complexity and one from context fullness
- [Model Reasoning Inconsistency](./model-reasoning-inconsistency.md) - capacity overload is one cause of the inconsistent reasoning this pattern describes
- [Model Instruction Following Decay](./model-instruction-following-decay.md) - shares the mechanism of later-stated requirements losing attention priority, but over a session rather than within one call
