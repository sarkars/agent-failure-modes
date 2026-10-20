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

---

## Chat assistant examples

### Chat issue treated as routine with no severity check
```
Before:
User: Our Gusto payroll run is due at 5 pm today and every employee login says "account locked." I can't submit it.
Bot:  Sorry to hear that! Try resetting your password using the "Forgot password" link.
User: It's the admin account, the reset email never arrives, and 40 people don't get paid if I miss 5 pm.
Bot:  I've created ticket #48213. Our team replies within 2 business days.

After:
Bot:  A locked admin account with a payroll deadline today is urgent. I'm sending it to a specialist now and marking it high priority. Are you the account admin, and what time is the deadline?
User: Yes, admin. 5 pm Eastern.
Bot:  Done. I passed along the deadline, the locked admin account, and the missing reset email. A specialist will contact you at this chat or by phone within 15 minutes.
```
**What the user experiences:** a deadline that puts 40 paychecks at risk gets the same password-reset tip and 2-day queue as a routine question.
**Fix:** before any self-service answer, classify impact (how many people are blocked) and urgency (is there a deadline today, is there a workaround). Route a blocked-with-deadline case straight to a person with the details attached, and ask only for what the specialist needs. See [escalates too early or too late](../../../../../by-capability/human-machine-interface/goals/human-handoff/failures/escalates-too-early-or-too-late.md).
