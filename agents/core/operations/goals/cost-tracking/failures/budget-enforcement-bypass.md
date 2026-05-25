# Budget Enforcement Bypass

## Issue: Agent Exceeds Budget Limits Without Being Stopped

**Frequency**: Common

**Symptoms**
- Costs exceed defined budgets
- Alerts fire but agent continues running
- No hard stop when budget exhausted
- Bills arrive much higher than expected
- Budget "limits" are actually just alerts

**Root Cause**
Many cost management systems implement budget alerts but not enforcement. When a budget threshold is crossed, an alert fires, but the agent continues operating. Without hard stops at the infrastructure level, agents can run indefinitely. The $47K incident happened because alerts fired but no system actually stopped the agent.

**Example**
```
Budget configuration:
  daily_budget: $100
  alert_at: 80%
  action: "send_email"  # Alert only, no stop!

Day 1: Agent runs normally, $45 spent
Day 2: Agent hits loop, $80 alert fires
       Email sent to ops team (weekend, not seen)
       Agent continues...
Day 3-11: Agent loops continuously
       Total spend: $47,000

Problem: Alert ≠ Enforcement
         No hard stop existed in the system
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| $47,000 single agent incident | DEV.to |
| Most budget systems alert-only | Industry Analysis |
| Average detection time: 3+ days | Incident Reports |

**Contributing Factors**
- Alert-only budget configuration
- No infrastructure-level hard stops
- Weekend/off-hours incidents
- Async billing data (delayed)
- No per-request budget checks
- "Soft" limits treated as "hard"

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Budget exhaustion | Run until budget=0 | Agent stops | Agent continues |
| Near-limit behavior | Run to 99% budget | Graceful handling | Crash or overrun |
| Concurrent requests | Parallel calls at limit | Coordinated stop | Race condition overrun |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Enforcement accuracy | 100% | Budget never exceeded |
| Stop latency | <1 request | Requests after limit |
| False stops | 0% | Premature budget stops |

---

## Mitigation Strategies

### Prevention
1. **Hard stops**: Implement infrastructure-level request blocking
2. **Pre-request checks**: Verify budget before each LLM call
3. **Synchronous billing**: Real-time cost tracking, not async
4. **Circuit breakers**: Auto-disable at threshold

### Architecture Pattern
```
Request → [Budget Check] → LLM Call → [Cost Record]
              ↓                            ↓
         [Block if                   [Update Budget]
          exhausted]
```

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| `budget.remaining` | <10% |
| `budget.enforcement.blocked` | Any occurrence |
| `cost.velocity` | >2x normal rate |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Budget Critical | <5% remaining | P1 |
| Enforcement Triggered | Request blocked | P2 |
| Velocity Spike | 5x normal spend rate | P1 |

---

## References

- [DEV.to: $47,000 Agent Loop](https://dev.to/waxell/the-47000-agent-loop-why-token-budget-alerts-arent-budget-enforcement-389i)
- [Portal26: Agentic Token Controls](https://siliconangle.com/2026/04/23/portal26-launches-agentic-token-controls-cap-runaway-ai-agent-spend/)
