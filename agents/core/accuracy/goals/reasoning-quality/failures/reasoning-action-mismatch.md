# Reasoning-Action Mismatch

## Issue: Agent's Reasoning Doesn't Match Its Actions

**Frequency**: Common (13.2% of MAS failures)

**Symptoms**
- Agent explains one plan but executes another
- Stated intentions don't match tool calls
- Reasoning is correct but actions are wrong
- Logical analysis followed by illogical action

**Root Cause**
Agent exhibits a mismatch between its reasoning and its actions. The agent may reason correctly about what should be done, but then execute different actions. This disconnect between "thinking" and "doing" is a fundamental failure in agent execution.

**Example**
```
Task: "Delete the oldest backup file to free space"

Agent reasoning:
"I need to find the oldest backup file. Let me list files
by date. The files are:
- backup_2024_01.tar (oldest)
- backup_2024_06.tar
- backup_2024_12.tar (newest)
The oldest file is backup_2024_01.tar, so I should delete that."

Agent action:
delete_file("backup_2024_12.tar")

Result: Newest backup deleted instead of oldest
        Reasoning was correct, action was wrong
```

**Key Statistics**
From MAST study of 1642 MAS traces:
- Reasoning-action mismatch accounts for 13.2% of failures
- Part of "Inter-Agent Misalignment" category
- One of the most common failure modes

**Mismatch Patterns**
- **Parameter swap**: Right function, wrong parameters
- **Target confusion**: Correct analysis, wrong target
- **Inverted logic**: Reasoning correct, action opposite
- **Partial execution**: Plan complete, execution partial

**Contributing Factors**
- Disconnect between language generation and tool calling
- Copy-paste errors in parameter extraction
- Context confusion during action formulation
- Model limitations in grounding reasoning to actions
- Long reasoning chains losing thread

**Mitigation Strategies**
1. **Action verification**: Confirm action matches stated intent
2. **Reasoning-action binding**: Explicitly link reasoning to parameters
3. **Pre-execution review**: Show planned action before execution
4. **Consistency checks**: Validate action against reasoning
5. **Structured output**: Force explicit parameter extraction

**Detection**
- Stated intent differs from executed action
- Tool parameters don't match reasoning
- User corrections for "I said X but you did Y"
- Logical analysis contradicted by action

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Failure mode 2.6: Reasoning-Action Mismatch (13.2%)
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Execution vs planning failures
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) - Grounding failures
