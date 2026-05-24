# Termination Condition Unawareness

## Issue: Agent Doesn't Know When to Stop

**Frequency**: Common (12.4% of MAS failures)

**Symptoms**
- Agent continues working after task is complete
- Agent stops prematurely before completion
- No clear signal that task is finished
- Conflicting signals about completion status

**Root Cause**
Agent is unaware of termination conditions - it doesn't recognize when the task is complete, either continuing unnecessarily or stopping before the job is done. This is especially problematic in multi-agent systems where termination requires coordination.

**Example**
```
Multi-agent system: Code review pipeline

Task: "Review and approve the PR if it passes all checks"

Agent trace:
Reviewer Agent: "Code looks good, tests pass. Approved."
CI Agent: "All checks passed."
Merger Agent: "Ready to merge."

[Task is complete - but no agent terminates]

Reviewer Agent: "Let me check the code again..."
CI Agent: "Running tests again..."
Merger Agent: "Checking merge status..."

Result: System continues running indefinitely
        Task was complete but agents didn't stop
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Termination unawareness accounts for 12.4% of failures
- Part of "System Design Issues" category (44.2% total)
- Often leads to resource exhaustion

**Termination Failures**
- **Over-execution**: Continuing after task complete
- **Under-execution**: Stopping before task complete
- **Ambiguous state**: Unclear if task is done
- **Coordination failure**: Agents disagree on completion

**Contributing Factors**
- Vague success criteria in task definition
- No explicit termination signals
- Completion conditions buried in long prompts
- Multi-agent consensus required but not achieved
- State not clearly indicating "done"

**Mitigation Strategies**
1. **Explicit termination criteria**: Define clear completion conditions
2. **Termination signals**: Dedicated mechanism to signal completion
3. **Completion verification**: Verify all success criteria met
4. **Timeout fallbacks**: Force termination after time limit
5. **Consensus protocols**: Clear rules for multi-agent termination

**Detection**
- Activity continuing after logical completion
- Repeated "checking" behaviors post-completion
- Resource usage without corresponding progress
- Conflicting completion signals from agents

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 1.5: Unaware of Termination Conditions (12.4%)
- [Aegis: Agent-Environment Failures](https://arxiv.org/abs/2508.19504) - Resource exhaustion from over-execution
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Coordination termination issues
