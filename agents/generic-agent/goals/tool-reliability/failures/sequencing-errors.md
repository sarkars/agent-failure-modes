# Sequencing Errors

## Issue: Agent Calls Tools in Wrong Order

**Frequency**: Common

**Symptoms**
- Dependent tool called before prerequisite
- Data fetched after it's needed
- Transactions started but not committed
- Cleanup runs before operation completes

**Root Cause**
- Agent doesn't understand tool dependencies
- Async operations confuse ordering
- Agent optimizes for speed over correctness
- Missing dependency documentation

**Example**
```
Task: Create user and send welcome email

Agent sequence:
1. send_welcome_email(user_id: ???)  # User doesn't exist yet!
2. create_user(name: "Alice")

Result: Email fails, user created without notification
```

**Mitigation Strategies**
1. **Dependency documentation**: Specify prerequisites in tool descriptions
2. **Return value chaining**: Tools return IDs needed by subsequent calls
3. **Transaction support**: Group dependent operations
4. **Prerequisite validation**: Tools check if dependencies met
5. **Workflow templates**: Provide correct sequences for common tasks
6. **Planning step**: Have agent plan sequence before executing

**Detection**
- Track failure rates by tool sequence
- Monitor dependency violations
- Log prerequisite check failures
- Compare planned vs. actual execution order

---

## References

- [Why Do Multi-Agent LLM Systems Fail? (MAST)](https://arxiv.org/abs/2503.13657) - Research on task ordering and sequencing failures
- [Redis: Why Multi-Agent LLM Systems Fail](https://redis.io/blog/why-multi-agent-llm-systems-fail/) - Analysis of multi-agent coordination failures
