# Infinite Loops

## Issue: Agent Gets Stuck in Infinite Retry Loops

**Frequency**: Occasional

**Symptoms**
- Agent repeatedly attempts same action with same or similar inputs
- Token costs spiral without progress toward goal
- No termination condition triggers
- Task never completes or times out after hours/days

**Root Cause**
Iterative refinement and retry logic can enter infinite loops when:
- The underlying failure cannot be resolved by retrying
- Success conditions are impossible to meet
- Agent lacks ability to recognize futile attempts
- No hard limits on iterations or cost

**Example**
```
Iteration 1: Call API, get rate limit error, retry
Iteration 2: Call API, get rate limit error, retry
...
Iteration 10,000: Still retrying

Result: $47,000 in API costs over 11 days (real incident)
```

**Real Incidents**
- $47,000 agent loop over 11 days with no hard stop
- $437 overnight from unchecked agent run
- Development environments running indefinitely

**Mitigation Strategies**
1. **Hard iteration limits**: Maximum retries before escalation (e.g., 5 retries)
2. **Token/cost budgets**: Kill agent when budget exceeded
3. **Time limits**: Maximum runtime per task
4. **Similarity detection**: Stop if outputs converge without improvement
5. **Escalation paths**: Route to human after N failures
6. **Cost monitoring alerts**: Real-time spend tracking with kill switches
7. **Circuit breakers**: Exponential backoff with max attempts

**Detection**
- Monitor iteration counts per task
- Track cost per task vs. historical baseline
- Alert on tasks exceeding time thresholds
- Log repeated identical actions

---

## References

- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i) - Real incident analysis of an 11-day agent loop with no hard stop
- [Dev Journal: $437 Overnight AI Agent](https://earezki.com/ai-news/2026-04-29-i-let-my-ai-agent-run-overnight-it-cost-437/) - Case study of unchecked overnight agent costs
- [AWS: 3 Agent Failure Modes](https://dev.to/aws/why-ai-agents-fail-3-failure-modes-that-cost-you-tokens-and-time-1flb) - Common failure patterns including infinite loops
