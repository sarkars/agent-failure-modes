# High-Effort Ticket Misrouting

## Issue: Support Ticket Routing Model Routes Complex Issues to Tier-1 (Auto-Response); Requires Escalation After Wasted Time

**Frequency**: Common

**Symptoms**
- Complex ticket routed to low-tier support
- Tier-1 can't resolve; escalates (delay)
- Time wasted on wrong tier; customer frustrated
- Low-effort tickets go to high-tier (inefficient)

**Root Cause**
Routing models trained on tickets that were successfully resolved. Tickets that required escalation or took multiple touches under-represented. Models learn ticket keywords but not effort/complexity. Baseline "route to Tier-1" has high accuracy (most tickets resolve there), so model becomes biased toward Tier-1.

**Example**
```
Scenario: Technical support ticket router
Ticket: "Can't connect to API. Error: SSL certificate validation failed. I tried..."
Keywords: "API", "error" → Common issue
Model routing: Tier-1 (auto-response: "Try clearing cache")
Reality: Complex issue (custom SSL, non-standard config)
Customer: "That doesn't help, I need engineer"
Escalation: 24 hours later, Tier-3 handles
Impact: Poor customer experience; inefficient labor
```

**Key Statistics**
- Accuracy on simple tickets: 95%+
- Accuracy on complex tickets: 30-50%
- Escalation rate: 20-40% (tickets re-routed)
- Effort misprediction: ±2-5x

---

## Mitigation Strategies

1. **Effort Estimation Model**: Separate model to predict resolution effort
2. **Resolution Time Tracking**: Learn from historical resolution times, not just keywords
3. **Smart Escalation**: Route based on effort + expertise needed
4. **Skill Matching**: Route to agent with right skills, not just tier

### Metrics
- First-contact resolution rate by tier
- Escalation rate (should be <10%)
- Effort prediction accuracy
- Customer satisfaction by routing quality

### Alerts
- Escalation rate >15% → Retrain routing model

---

## References

- [Ticket Routing with ML](https://arxiv.org/abs/1912.08634)
- [Complexity Prediction in Support](https://arxiv.org/abs/2008.02455)
