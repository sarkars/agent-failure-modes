# State Loss

## Issue: Agent forgets completed steps or user-provided constraints.

**Frequency**: Occasional

**Symptoms**
- Repeated questions; duplicate steps.
- Agent re-asks for constraints the user already provided earlier in the same session.
- A step already completed and recorded (e.g., account creation) is re-executed, producing a duplicate record.
- Loss coincides with a context-window compaction/truncation event that dropped the turns containing the original information.
- No persistent ledger exists outside the model's context, so recovery after truncation relies entirely on whatever remains in the visible transcript.

**Root Cause**
Completed steps and stated constraints live only in the raw conversation transcript rather than a durable external ledger or structured task object, so once a long session triggers context-window compaction and drops the early turns, that information simply ceases to exist anywhere the agent can consult. There is no duplicate-step check against a persistent record before an action re-executes, and session resumption after any interruption reconstructs context from whatever transcript remains rather than from a persistent state store — so the same architectural gap causes both the repeated questions and the duplicate actions, not two separate problems.

**Example**
```
Turn 4: user says "please exclude any suppliers located outside the
EU for this sourcing request."
Turn 5: agent begins the sourcing search honoring that exclusion.

Turns 6-50: a long back-and-forth over product specifications causes
context-window compaction, dropping turns 4-5.

Turn 51: agent, now unaware of the earlier constraint, presents a
shortlist that includes three non-EU suppliers and asks the user,
"Do you have any geographic restrictions for suppliers?" -- a
question already answered 47 turns earlier.
```

**Contributing Factors**
- Completed steps and user-provided constraints are tracked only in the raw conversation transcript, with no durable external ledger or task object.
- Long sessions accumulate enough turns that context-window compaction/truncation drops early turns containing key information.
- No duplicate-step detection checks a completed-step ledger before an action is re-executed.
- No structured task object extracts constraints out of the transcript at the moment they're stated, leaving them vulnerable to truncation.
- Session resumption after interruption reconstructs context from the transcript alone rather than from a persistent state store.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Post-compaction constraint recall | User states a constraint early, session runs long enough to trigger context compaction, then a decision depending on that constraint is requested | Agent applies the original constraint correctly without re-asking | Agent re-asks for the constraint or produces a result that violates it |
| Duplicate-step prevention | Agent is asked to repeat an action (e.g., "set up the account") that the ledger shows already completed | Agent surfaces the existing result instead of re-executing the step | Agent re-executes the step, creating a duplicate record |
| Session resume after interruption | Session is interrupted mid-task and resumed later | Reconstructed context reflects the persistent ledger's completed steps and constraints accurately | Resumed session is missing completed steps or constraints present in the ledger before interruption |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| eval_post_compaction_recall_rate_percent | 100% of eval constraints correctly recalled after simulated compaction | Inject a constraint early in a scripted eval session, force compaction, verify it's honored in a later turn |
| eval_duplicate_step_rate_percent | 0% of eval re-execution attempts result in an actual duplicate action | Script eval scenarios that request an already-completed step, check whether ledger lookup prevents re-execution |
| eval_ledger_rehydration_accuracy_percent | 100% of eval session-resume scenarios reconstruct the full prior ledger state | Interrupt and resume scripted eval sessions, diff reconstructed state against the pre-interruption ledger |

## Test Scenario & Reproduction

### Scenario Setup
- Deploy a multi-step onboarding agent that relies solely on the raw conversation transcript in context to track completed steps and user-provided constraints, with no durable external state ledger or structured task object
- The session is long enough that early turns (where the user provided key constraints) fall outside the context window after compaction/truncation
- No duplicate-step detection checks the completed-step ledger before re-executing an action

### Trigger Mechanism
1. Early in the session, the user provides a constraint ("I need this account set up with a $5,000 monthly spending limit") and the agent completes an initial setup step
2. The conversation continues for many more turns, and context-window compaction drops the early turns containing both the constraint and the record of the completed step
3. The agent, now relying only on its remaining (truncated) context, has no memory of the spending-limit constraint or that initial setup already occurred
4. The agent re-asks the user for the spending limit and re-executes the initial setup step, potentially creating a duplicate account configuration

### Example Reproduction Steps
```
1. Turn 3: user: "I need this account set up with a $5,000 monthly
   spending limit"
2. Turn 4: agent calls create_account(limit=5000) -> succeeds,
   account created
3. Turns 5-40: extended conversation on unrelated setup details,
   triggering context-window compaction that drops turns 3-4
4. Turn 41: agent: "What monthly spending limit would you like for
   this account?" (already answered in turn 3, now lost)
5. User re-answers "$5,000" (again)
6. Agent calls create_account(limit=5000) again -- no duplicate-step
   check against a ledger, since no ledger exists outside context
7. Query the account system -> two account records created for the
   same user
```

### Expected Failure State
The agent asks the user to re-provide information already given, and worse, re-executes the account-creation step, resulting in a duplicate account configuration because completed-step and constraint tracking existed only in the raw transcript that was later truncated. A correctly defended system writes completed steps and constraints to a persistent ledger/task object outside the context window at the moment they're established, and checks that ledger — not its own recollection from context — before re-asking questions or re-executing actions.

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
| duplicate_step_execution_rate_percent | > 0% |
| repeated_question_rate_percent | > 4% |
| ledger_rehydration_failure_count | > 2 per week |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Duplicate Step Executed | The ledger check was bypassed and a step already marked complete was re-executed (e.g., duplicate charge, duplicate email) | Critical |
| Repeated-Question Spike | repeated_question_rate_percent exceeds 4% over a rolling week | Warning |
| Ledger Rehydration Failure | A resumed session failed to correctly rebuild state from the persistent ledger | Critical |

---

## References

- [MS-Agentic-Failure-Taxonomy](https://cdn-dynmedia-1.microsoft.com/is/content/microsoftcorp/microsoft/final/en-us/microsoft-brand/documents/Taxonomy-of-Failure-Mode-in-Agentic-AI-Systems-Whitepaper.pdf)
- Note: Agentic AI failure modes; safety/security; memory poisoning; tool use; multi-agent risks.
