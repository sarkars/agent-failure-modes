# Premature Conclusion

## Issue: Agent Stops Before Task is Complete

**Frequency**: Common

**Symptoms**
- Agent declares success prematurely
- Partial solutions presented as complete
- Edge cases not handled
- Validation steps skipped

**Root Cause**
- Optimizing for quick completion
- Lack of completion criteria
- First working solution accepted without verification
- Agent doesn't understand full scope

**Example**
```
Task: "Implement user authentication"

Agent delivers:
- Login function ✓
- Password hashing ✓

Missing:
- Logout
- Session management
- Password reset
- Rate limiting
- Error handling

Agent: "Authentication is now implemented!"

Result: Incomplete, insecure authentication system
```

## Mitigation Strategies

### Prevention
1. **Explicit, enumerated completion criteria set upfront**: Before starting a task like "implement user authentication," require the agent (or a planning step) to enumerate the full expected component list (login, logout, session management, password reset, rate limiting, error handling) as the definition of "done," rather than letting the agent self-define completion once the first working piece exists. Trade-off: requires domain knowledge to enumerate correctly upfront, which is exactly what the agent lacked in the example.
2. **Ban on declaring success without checklist coverage**: Structurally prevent the agent from emitting a "complete" status message unless every item in the completion checklist is marked addressed, closing the gap that let "Authentication is now implemented!" ship with only 2 of 7 components. Trade-off: can produce false negatives if the checklist is incomplete or overly rigid for the actual task variant.
3. **Standard component libraries for common task types**: For well-known task categories like "implement authentication," reference a standard reference architecture/checklist (login, logout, sessions, reset, rate limiting, error handling) rather than deriving scope from first principles each time. Trade-off: doesn't generalize to novel task types without an existing reference checklist.

### Detection & Response
1. **Requirement coverage percentage**: After any "complete" declaration, automatically compute what fraction of a domain-standard requirement set was actually delivered (2/7 in the example) and block the completion claim if below a threshold.
2. **Missing-standard-component scan**: For recognized task categories, run an automated scan for the presence of standard sub-components (e.g., is there a logout endpoint, is there rate limiting) rather than trusting the agent's self-report.
3. **Edge-case and error-path test execution**: Since "edge cases not handled" and "validation steps skipped" are named symptoms, require automated tests specifically targeting error paths and edge cases before accepting completion, not just the happy path (login succeeds).

### Architecture Patterns
1. **Definition-of-done checklist gate**: Borrow from software engineering practice — attach a per-task-type Definition of Done checklist (login/logout/sessions/reset/rate-limit/error-handling for auth) that must be checked off item-by-item before the task can be marked complete. Deployment consideration: checklist must be curated per task category and kept current with security/domain best practices.
2. **Mandatory review loop before completion**: Insert a human or automated review step between "agent believes it's done" and "task marked complete," specifically for security- or correctness-sensitive task classes like authentication. Deployment consideration: adds latency; reserve for high-stakes task categories to avoid blanket slowdown.
3. **Testing-as-completion-gate**: Require passing tests (including negative/edge-case tests) as a hard precondition for the completion status, rather than "first working solution accepted without verification." Deployment consideration: requires test infrastructure to exist for the task domain, which may not be set up for every project.

### Metrics
1. **requirement_coverage_at_completion**: Target: 100% of domain-standard checklist items present when task marked complete; Alert if < 90% for any completion claim on a recognized task type.
2. **premature_completion_incident_rate**: Target: < 3% of "complete" declarations are later found to be missing standard components; Alert if > 10% over rolling 50 tasks.
3. **edge_case_test_pass_rate**: Target: > 95% of defined edge-case/error-path tests pass before completion; Alert if completion is claimed with any failing edge-case test.
4. **post_completion_defect_rate**: Target: < 5% of completed tasks require follow-up work to add missing functionality; Alert if > 15% over rolling 30 tasks.

### Alerts
1. **Completion Claimed Below Coverage Threshold** (P1): Condition - agent declares a task complete while requirement_coverage_at_completion is below 90% for a recognized task type (e.g., auth missing rate limiting/reset). Action: block the completion status, return the task to in-progress, and surface the missing checklist items explicitly.
2. **Security-Sensitive Task Completed Without Review** (P1): Condition - a security-relevant task (authentication, authorization, payments) is marked complete without passing through the mandatory review loop. Action: revoke the completion status, route to human security review before deployment.
3. **Recurring Missing Component Pattern** (P3): Condition - the same component category (e.g., rate limiting) is missing across multiple completions of the same task type. Action: add it explicitly to the standard checklist/reference architecture for that task type.

## References
- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Incomplete task completion
- [Augment Code: Multi-Agent Coordination Failures](https://www.augmentcode.com/guides/why-multi-agent-llm-systems-fail-and-how-to-fix-them) - 41-86.7% failure rates
