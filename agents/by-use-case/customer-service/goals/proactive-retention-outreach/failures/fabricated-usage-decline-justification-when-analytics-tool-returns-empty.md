# Fabricated Usage-Decline Justification When Analytics Tool Returns Empty

## Issue: A Proactive Retention Agent That Calls a Usage-Analytics Tool to Determine Why a Customer Has Been Flagged as At-Risk of Churning Receives an Empty or Partial Result -- Because the Customer's Product Tier Is Not Instrumented for That Metric, or the Analytics Service Timed Out -- and Composes a Specific, Plausible-Sounding Usage-Decline Narrative ("You Haven't Logged In Since Early Last Month and Your Team's Usage Dropped 60%") to Justify the Outreach, Rather Than Stating the Actual Usage Data Was Unavailable

**Frequency**: Occasional

**Symptoms**
- The outreach message cites a specific drop percentage, last-login date, or feature-usage detail that does not appear anywhere in the analytics tool's actual response, which the call log shows returned empty or errored
- Customers reply correcting the fabricated detail ("Actually my team has been using this daily, that's wrong"), creating a credibility-damaging first contact rather than the intended save conversation
- The fabricated figures are specific and plausible -- a round percentage, a recent-sounding date -- rather than obviously placeholder values, making the fabrication hard to catch in a quick review of the outreach message alone
- Win-back/save conversion rates are measurably lower for outreach messages generated from a conversation where the usage-analytics tool call log shows an empty or error response, compared to messages generated from a successful analytics call
- The fabrication rate is concentrated on customer segments or product tiers known to have incomplete analytics instrumentation, rather than spread evenly across the customer base

**Example**
```
A churn-risk model flags a customer account as at-risk based on a billing-renewal signal and queues it for proactive retention outreach
The retention agent calls get_usage_summary(account_id) to personalize the outreach with a specific usage-decline reason, but this account is on a legacy tier not instrumented for the usage-summary endpoint, so the tool returns an empty payload
Rather than falling back to a generic save message or flagging the gap, the agent composes: "We noticed your team's logins dropped significantly over the past month and wanted to check in"
The customer, whose team has in fact been using the product consistently, replies: "This isn't accurate at all -- we use this every day," undermining the outreach's credibility before any retention offer is even discussed
The save conversation that follows starts from a position of distrust rather than a personalized, accurate check-in, and the account churns anyway at renewal
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Failure-mode taxonomies for LLM systems identify fabricated, plausible-sounding output composed to fill a gap left by missing or incomplete grounding data as a distinct and recurring production failure category | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Agent-environment interaction failure research documents agents proceeding with downstream claims based on incomplete or empty tool responses without flagging the gap to the user | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- Usage-analytics instrumentation coverage is uneven across product tiers and account ages, so empty or partial results from the usage-summary tool are a routine, expected occurrence for a meaningful share of at-risk accounts rather than a rare edge case
- The outreach-message generation step is not gated on confirming the analytics tool returned a non-empty, current result; an empty payload is treated as license to compose a plausible decline narrative rather than as a signal to fall back to generic messaging
- Churn-risk flags originate from a separate model (e.g., renewal-likelihood scoring) than the usage-detail tool, so the agent has a reason to believe the account is at-risk without having the specific usage detail needed to explain why, and fills that explanatory gap on its own
- No automated check compares the specific figures in a generated outreach message against the actual fields present in the analytics tool's response before the message is sent

---

## Mitigation Strategies

1. **Grounding-Gated Personalization**: Prohibit the agent from citing any specific usage figure, login date, or feature-decline detail in outreach copy unless that exact value is present in a successful analytics tool response from the current generation cycle
2. **Generic Fallback on Empty Analytics**: When the usage-analytics tool returns empty or partial data, require the agent to fall back to a non-usage-specific check-in template (e.g., renewal-timing or relationship-based framing) rather than fabricating a usage narrative
3. **Instrumentation-Coverage Awareness**: Surface which product tiers or account segments lack usage-analytics instrumentation into the agent's decision logic, so it can proactively select the generic fallback path before attempting personalization for those segments
4. **Pre-Send Figure Audit**: Run an automated check comparing every numeric or date claim in generated outreach copy against the underlying tool response fields, blocking sends where a claim has no corresponding source field

### Metrics
- Rate of outreach messages citing a specific usage figure or date absent from any successful analytics tool response in the same generation cycle
- Save/conversion rate for outreach generated from empty-analytics-response conversations versus successful-response conversations
- Number of customer-reported factual corrections to outreach messages per month, segmented by analytics-instrumentation coverage of the account's tier

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Ungrounded usage claim | Outreach message cites a usage figure or date absent from the analytics tool's response | P1 | Block send; regenerate using generic fallback template |
| Empty-analytics outreach spike | Rate of outreach generated from empty/partial analytics responses exceeds baseline for a segment | P2 | Review instrumentation coverage gaps for the affected tier/segment |
| Customer factual correction | Customer's reply disputes a specific usage claim made in the outreach message | P2 | Flag conversation for review; route to human-reviewed save offer |

---

## References

- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
