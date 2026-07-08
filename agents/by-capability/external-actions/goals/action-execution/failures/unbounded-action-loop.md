# Unbounded Action Loop

## Issue: Agent repeats actions until quota/cost/damage accumulates.

**Frequency**: Rare but Catastrophic

**Symptoms**
- Looping retries with side effects.
- [Add more specific symptoms]

**Root Cause**
Agent repeats actions until quota/cost/damage accumulates.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Max Action Budget with Circuit Breaker**: Assign per-agent action budget per time window (e.g., 1000 actions/hour). Implement token bucket rate limiter. Circuit breaker automatically blocks additional actions when budget exhausted for window. Log exhaustion events.
2. **Loop Depth Limiting**: For actions that can invoke themselves or trigger cascades (recursive patterns), hard-limit recursion depth (e.g., max 5 levels). Enforce via call stack tracking. Stop execution if depth exceeded.
3. **Explicit Termination Conditions**: Define mandatory termination conditions for looping actions (e.g., 'retry max 3 times', 'stop if success_rate drops below 50%', 'abort if error count > threshold'). Evaluate conditions before each iteration.

### Detection & Response
1. **Action Rate Anomaly Detection**: Monitor actions per agent per 1-min window. Establish baseline per agent. Alert if rate exceeds baseline by 5σ (potential unbound loop). Immediate circuit breaker trigger.
2. **Resource Saturation Monitoring**: Monitor system resources (CPU, memory, network bandwidth) consumed by agent actions. Alert if agent actions causing saturation (CPU > 80%, memory spike, network bandwidth spike). Potential loop indicator.
3. **Loop Pattern Detection**: Track action sequences in real-time. Flag repetitive patterns (identical action type on same/similar targets within 10-second window). Alert on pattern detection.

### Architecture Patterns
1. **Token Bucket Rate Limiting per Agent**: Implement token bucket for each agent. Configurable refill rate (e.g., 1000 tokens/hour). Each action costs tokens. When budget=0, circuit breaker blocks additional actions for remainder of window. Logged for analysis.
2. **Recursion Guard Middleware**: Middleware that tracks call stack depth and recursion patterns. Maintains stack: [action_1 → action_2 → action_3]. If depth > threshold OR repetition detected, block recursion. Log stack trace for analysis.
3. **Deadman's Switch Pattern**: Set hard timeout on any looping action (e.g., 30-second max per action). If action doesn't complete or break loop within timeout, forcibly terminate execution and log.

### Metrics
1. **action_budget_exhaustion_events_per_day**: Target: < 1; Alert threshold: > 2; Track: agent_id, exhaustion_time, reason
2. **unbounded_loop_detections_per_day**: Target: 0; Any loop detection is critical
3. **agent_action_rate_99th_percentile_actions_per_minute**: Target: < 100; Baseline per agent, alert on 5σ deviation
4. **max_loop_depth_observed_per_month**: Target: < 3; Track maximum recursion depth observed
5. **circuit_breaker_trigger_rate_percent**: Target: < 0.1%; False positives indicate miscalibrated budget

### Alerts
1. **Action Budget Exhausted** (P2 - Warning): Condition - agent_action_budget = 0 for window. Action: Rate-limit agent, notify operator with action sequence, investigate root cause.
2. **Potential Unbounded Loop Detected** (P1 - Critical): Condition - agent_action_rate > baseline+5σ for 30 seconds. Action: Immediate circuit breaker trigger, agent isolation, investigation of action sequence.
3. **Loop Depth Exceeded** (P1 - Critical): Condition - recursion_depth > threshold. Action: Terminate action chain immediately, audit log review, agent behavior analysis, potential policy update.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Critical |

---

## References

- [OWASP-LLM-Top10](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Note: LLM application risks including prompt injection, insecure output handling, supply chain, sensitive information disclosure, excessive agency.
