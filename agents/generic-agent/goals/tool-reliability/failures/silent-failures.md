# Silent Tool Failures

## Issue: Tools Fail Without Alerting the Agent

**Frequency**: Common

**Symptoms**
- Tool returns success but action didn't complete
- Partial execution not communicated
- Error swallowed by tool wrapper
- Agent proceeds assuming success

**Root Cause**
- Tools returning success on partial completion
- Error handling that catches and hides exceptions
- Async operations not confirming completion
- Tools not validating their own output

**Example**
```
Agent: send_notification(user_id: 123, message: "Alert!")

Tool response: { "status": "success" }

Reality: Notification service was down, message queued indefinitely

Agent tells user: "I've sent your notification"

Result: User never receives notification, thinks it was sent
```

**Mitigation Strategies**
1. **End-to-end confirmation**: Tools verify action completed
2. **Explicit failure responses**: Never swallow errors
3. **Status codes with details**: Include success criteria in response
4. **Async completion tracking**: Return job ID, check completion
5. **Idempotency tokens**: Enable safe retries
6. **Health checks**: Verify dependent services before calling

**Detection**
- Track success responses vs. actual outcomes
- Monitor downstream confirmation rates
- Alert on mismatches between tool response and reality
- Log completion verification results
