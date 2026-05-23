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

**Mitigation Strategies**
1. **Explicit verification**: Test outputs before declaring success
2. **Error root cause analysis**: Understand WHY before fixing
3. **Incremental fixes**: Change one thing at a time
4. **Rollback capability**: Return to known-good state
5. **Error pattern recognition**: Learn from repeated failures
6. **External validation**: Use tools to verify correctness

**Detection**
- Track repeated error types
- Monitor fix attempt success rates
- Alert on regression loops
- Compare iterations for actual improvement
