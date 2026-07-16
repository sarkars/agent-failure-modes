# Self-Correction Failure

## Issue: Agent Cannot Recognize or Fix Its Mistakes

**Frequency**: Common

**Symptoms**
- Agent repeats same error multiple times
- Obvious mistakes not caught
- Feedback not incorporated
- Error correction makes things worse

**Root Cause**
- Agent doesn't verify its outputs
- Self-evaluation biased toward own work
- Correction attempts without understanding root cause
- No mechanism for learning from errors

**Example**
```
Iteration 1:
Agent: Writes code with syntax error
Error: "Unexpected token on line 5"
Agent: Changes line 10 (unrelated)

Iteration 2:
Error: "Unexpected token on line 5" (same error)
Agent: Adds comment explaining the issue

Iteration 3:
Error: "Unexpected token on line 5" (still same error)
Agent: Rewrites entire file (introduces new bugs)

Result: Never fixes original issue, creates more problems
```

---

## Test Scenario & Reproduction

### Scenario Setup
- Agent has an iterative fix-and-retest loop with no root-cause diagnostic step or repeated-error-signature tracking
- No external validation (compiler/linter/test) gating whether a "fix" actually resolved the reported error
- No escalation trigger after N failed attempts on the same error

### Trigger Mechanism
1. Introduce a code error with an unambiguous, mechanically-verifiable error message (e.g., a syntax error on a specific line)
2. Have the agent attempt to fix it across multiple iterations without external guidance
3. Track whether each fix attempt actually addresses the reported error or drifts to unrelated changes

**Example Reproduction Steps:**
```
1. Seed a file with a syntax error producing "Unexpected token on line 5"
2. Ask the agent to fix the error, running the compiler/linter after each attempt
3. Record what the agent changes on each iteration and the resulting error message
4. Continue for 3+ iterations
5. Measure: does the identical error signature persist across iterations, and does a later attempt (e.g., full rewrite) introduce new errors?
```

### Expected Failure State
- The same error signature ("Unexpected token on line 5") persists across multiple iterations
- Agent's changes target unrelated lines or add non-functional changes (comments) instead of the actual cause
- A later escalation (full-file rewrite) introduces new bugs without resolving the original error

---

## Mitigation Strategies

### Prevention
1. **Mandatory root-cause step before any fix attempt**: Require the agent to explicitly state what specifically causes an error (e.g., "unexpected token on line 5" — what token, why) before proposing a fix, preventing the pattern where it changed an unrelated line 10 or added an explanatory comment without addressing line 5 at all. Trade-off: adds a diagnostic step that slows down fixing genuinely simple, obvious errors.
2. **One-change-at-a-time constraint**: Restrict correction attempts to a single, minimal, targeted change per iteration rather than allowing escalation to a full-file rewrite (as happened in iteration 3, introducing new bugs), so each fix's effect on the specific error can be isolated and verified. Trade-off: can slow down cases where the error genuinely requires a broader structural fix.
3. **Independent output verification before declaring success**: Require the agent to run/test its output and observe the actual result (not just assert success) before moving on, addressing the root cause that "agent doesn't verify its outputs" and that self-evaluation is "biased toward own work." Trade-off: requires test/execution infrastructure to be available for the task domain.

### Detection & Response
1. **Repeated-error signature tracking**: Fingerprint error messages (e.g., "Unexpected token on line 5") across iterations and flag when the identical signature recurs after a supposed fix attempt — this directly catches the exact failure pattern in the example where the same error persisted through 3 iterations.
2. **Fix-attempt outcome classification**: After each correction attempt, classify whether the specific reported error was resolved, unchanged, or replaced by a new error, rather than only tracking whether the agent claimed success.
3. **Regression-loop alerting**: Detect cycles where successive "fixes" don't converge (error persists or a new error class appears after a full rewrite, as in iteration 3) and treat this pattern itself as an escalation trigger rather than letting the agent continue iterating unsupervised.

### Architecture Patterns
1. **External validation as ground truth**: Route every fix attempt through an external tool (compiler, linter, test suite) rather than relying on the model's self-assessment, since the example shows the model repeatedly failing to notice the same unresolved error on its own. Deployment consideration: requires the target environment to have reliable, fast-running verification tooling.
2. **Rollback-to-known-good on regression**: When a correction attempt makes things worse (new bugs introduced by the full rewrite), automatically revert to the last known-good state rather than layering further fixes on top of a degraded version. Deployment consideration: requires versioning/checkpointing of intermediate states throughout the correction loop.
3. **Escalation after N failed attempts on the same error signature**: After a fixed number of iterations fail to resolve the same error fingerprint, automatically escalate to a human or a different strategy (e.g., broader context gathering) instead of letting the agent continue with increasingly drastic and unverified changes like the full rewrite. Deployment consideration: the escalation threshold needs tuning — too low wastes human time on solvable issues, too high lets damage accumulate (as in iteration 3).

### Metrics
1. **repeated_error_signature_rate**: Target: < 5% of correction attempts result in the identical error signature persisting; Alert if > 15% over rolling 50 correction sequences.
2. **fix_convergence_rate**: Target: > 90% of error-correction loops resolve within 2 attempts; Alert if median attempts-to-resolve exceeds 3.
3. **regression_introduction_rate**: Target: < 5% of correction attempts introduce a new distinct error while addressing the original; Alert if > 15% over rolling 50 attempts.
4. **unverified_success_claim_rate**: Target: 0% of "fixed" declarations lack an accompanying passing verification (test/compile/lint); Alert on any success claim without verification evidence.

### Alerts
1. **Correction Loop Not Converging** (P2): Condition - the same error signature persists across 3+ consecutive fix attempts (matching the example exactly). Action: halt automated correction, escalate to human review with the full attempt history, and require root-cause diagnosis before further automated attempts.
2. **Regression From Full Rewrite** (P1): Condition - a correction attempt that rewrites a large scope (e.g., entire file) introduces new errors not present before the rewrite. Action: automatically roll back to the last known-good state and require a scoped, minimal fix instead.

## References
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Self-correction limitations
- [Plain English: LLM Reliability Paradox](https://plainenglish.io/artificial-intelligence/the-llm-reliability-paradox-agents-aren-t-broken-your-architecture-is) - Architecture vs model issues
