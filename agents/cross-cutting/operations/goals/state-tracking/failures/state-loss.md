# State Loss

## Issue: Agent forgets completed steps or user-provided constraints.

**Frequency**: Occasional

**Symptoms**
- Repeated questions; duplicate steps.
- [Add more specific symptoms]

**Root Cause**
Agent forgets completed steps or user-provided constraints.

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
1. **Durable External State Ledger**: Completed steps, gathered constraints, and user-provided parameters are written to a persistent ledger outside the model's context window (not relying on the transcript remaining in context), so state survives context truncation, session resumption, or context-window compaction.
2. **Explicit Constraint-Carrying Task Object**: User-provided constraints (dates, budgets, exclusions) are extracted into a structured task object as soon as stated, and this object — not the raw conversation history — is what's re-injected into every subsequent prompt, ensuring constraints survive even if earlier turns get dropped from context.
3. **Step Re-Hydration Before Each Action**: Before planning or taking the next action, the agent re-reads the current ledger/task-object state rather than relying on its own recollection from context, guaranteeing consistency between what it "thinks" it has done and what is actually recorded.

### Detection & Response
1. **Duplicate-Step Detection**: Before executing a step, check it against the completed-step ledger; if a matching step (same action + parameters) is already marked done, block re-execution and instead surface the existing result, flagging a state-loss near-miss.
2. **Repeated-Question Pattern Monitoring**: Detect when the agent asks the user for information already present in the task object/ledger, logging these as state-loss incidents even when the user simply re-answers, since the underlying tracking gap will recur.
3. **Context-Truncation Correlation**: When state loss is detected, check whether it coincides with a context-window truncation/compaction event; if so, treat it as evidence the ledger isn't being properly re-hydrated after compaction and fix that specific pathway.

### Architecture Patterns
1. **Persistent Task State Store**: A database-backed (not context-window-backed) record per task/session holding completed_steps, constraints, and parameters, read and written independently of the LLM context, serving as the single source of truth for "what has happened so far."
2. **State Machine Orchestrator**: The agent's control flow is driven by an explicit state machine (not free-form model reasoning about "what step am I on"), where transitions are only made after ledger confirmation of the prior step, structurally preventing steps from being silently skipped or repeated.
3. **Context Reconstruction on Resume**: When a session resumes after interruption or context compaction, a reconstruction step rebuilds the working prompt context from the persistent ledger/task object rather than assuming the raw transcript is still fully available.

### Metrics
1. **duplicate_step_execution_rate_percent**: Target: 0%; Alert threshold: > 0%
2. **repeated_question_rate_percent**: Target: < 1% of multi-turn tasks; Alert threshold: > 4%
3. **ledger_rehydration_failure_count**: Target: 0 per week; Alert threshold: > 2 per week
4. **mean_task_completion_turns_variance**: Target: within 15% of baseline for task type; Alert threshold: > 40% above baseline (indicates re-work from lost state)

### Alerts
1. **Duplicate Step Executed** (P1 - Critical): Condition - the ledger check was bypassed and a step already marked complete was re-executed (e.g., duplicate charge, duplicate email). Action: Immediate reversal/dedup where possible, notify user if externally visible, patch the ledger-check bypass.
2. **Repeated-Question Spike** (P2 - Warning): Condition - repeated_question_rate_percent exceeds 4% over a rolling week. Action: Audit task-object extraction coverage, check for constraint types not being captured into the structured object.
3. **Ledger Rehydration Failure** (P1 - Critical): Condition - a resumed session failed to correctly rebuild state from the persistent ledger. Action: Investigate reconstruction pathway, manually verify/restore affected session state, add regression test for the specific resume scenario.

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
