# Retry Storms

## Issue: Aggressive Retries Multiply Costs

**Frequency**: Common

**Symptoms**
- Failed operations trigger immediate retries
- Multiple agents retry simultaneously
- Downstream services overwhelmed
- Costs multiply with each retry wave

**Root Cause**
Retry logic without proper backoff and coordination:
- No exponential backoff between retries
- Multiple agents not coordinating retry timing
- Retrying non-retriable errors
- No distinction between transient and permanent failures

**Example**
```
Agent 1: API fails, retry immediately
Agent 2: API fails, retry immediately  
Agent 3: API fails, retry immediately
(All hit rate limit)

All three retry simultaneously, all fail again
Repeat 100x before any succeeds

Result: 300 API calls instead of 3
```

**Mitigation Strategies**
1. **Exponential backoff**: Increase delay between retries
2. **Jitter**: Add randomness to prevent synchronized retries
3. **Error classification**: Only retry transient failures
4. **Retry budgets**: Limit total retries per operation
5. **Circuit breakers**: Stop retrying after threshold failures
6. **Coordinated backoff**: Share retry state across agents

**Detection**
- Monitor retry rates per operation type
- Track time-to-success including retries
- Alert on retry rate spikes
- Log error types triggering retries

---

## References

- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Common failure patterns including retry storms
- [Arize: Why AI Agents Break](https://arize.com/blog/common-ai-agent-failures/) - Overview of agent failure modes and mitigation strategies
