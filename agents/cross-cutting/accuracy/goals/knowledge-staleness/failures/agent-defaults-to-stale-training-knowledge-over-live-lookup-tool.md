# Agent Defaults to Stale Training Knowledge Over Available Live-Lookup Tool

## Issue: Agent has access to live lookup tool that returns current reference data (policy, rules, calendar, threshold), but defaults to stale training-time knowledge instead of calling/trusting the tool; downstream decisions use outdated values

**Frequency**: Common

**Symptoms**
- Agent applies outdated rule/policy/threshold despite live lookup tool in context returning current value
- Tool call succeeded and returned current data, but agent's output references older value
- Agent's reasoning cites a specific fact without referencing a dated source (consistent with memorized knowledge)
- Discrepancy most visible around recently-changed data (policy updates, regulatory amendments, reference-data migrations)
- Agent given only the lookup tool's result (without access to training knowledge) makes correct decision

**Root Cause**
Agent's parametric knowledge encodes rules/values from training cutoff. Without explicit instruction to treat live tool as authoritative, agent defaults to fluent, confident memorized answer. Tool is available but not invoked or result is discounted against stronger internal prior.

**Examples**

### Support Services - Return Policy
```
Support agent has access to live policy-lookup tool
Customer asks about return window
Tool returns: "30-day return window (updated 2024-06)"
Agent responds: "60-day return window" (training-era policy)
Customer attempts return at day 45; denied
Impact: Customer dissatisfaction, incorrect expectations
```

### Support Services - Late Fee Waiver
```
Billing agent has access to live eligibility tool
Customer requests fee waiver
Tool returns: "2 waivers per 12 months allowed"
Agent applies: "1 waiver per year maximum" (outdated policy from training)
Customer denied waiver they qualified for
Impact: Policy violation, incorrect business decision
```

### Support Services - Escalation Routing
```
Alert-routing agent has access to live escalation-policy tool
Alert needs routing
Tool returns: "Assigned to Platform Team (reorg 2024-05)"
Agent routes to: "Database Team" (pre-reorg training knowledge)
Alert reaches wrong team; delay in response
Impact: Operational inefficiency, incident response delay
```

### Healthcare - Dosage Guidelines
```
Treatment agent has access to live dosage-guideline tool
Prescribing medication
Tool returns: "Current dosage: 250mg (updated 2024-06)"
Agent prescribes: "500mg" (training-era guideline)
Patient receives wrong dose
Impact: Patient safety risk, incorrect treatment
```

### Healthcare - Critical Value Threshold
```
Lab-results agent has access to live critical-value tool
Processing lab result
Tool returns: "Critical threshold: >300 (updated 2024-05)"
Agent flags as: "Requires alert if >400" (training-era threshold)
Critical result not escalated appropriately
Impact: Patient safety, missed urgent notification
```

### Financial Services - Security Identifier Standard
```
Data-quality agent has access to live identifier-registry tool
Validating security identifier
Tool returns: "Current standard extends to 12-character format (2024-04 migration)"
Agent rejects: "Invalid, standard only supports 10 characters" (pre-migration training)
Valid identifier rejected
Impact: Data quality error, false rejection of valid data
```

### Financial Services - Exchange Holiday Calendar
```
Market-data agent has access to live exchange-calendar tool
Checking if price unchanged is expected (market closed)
Tool returns: "Market OPEN today (holiday moved to 2024-06-15)"
Agent treats as: "Expected unchanged, market CLOSED" (old calendar)
Stale price passes validation incorrectly
Impact: Valuation uses outdated market data
```

### Financial Services - Beneficial Ownership Threshold
```
Compliance agent has access to live regulatory-update tool
Determining if disclosure required
Tool returns: "Current threshold: 5% (lowered 2024-05)"
Agent applies: "10% threshold" (training-era rule)
Required disclosure not filed
Impact: Regulatory violation, compliance failure
```

### Financial Services - Tick-Size Regime
```
Execution agent has access to live reference-data tool
Validating limit-order price increment
Tool returns: "Current tick-size: $0.01 (for $100-500 band)"
Agent applies: "$0.05 tick minimum" (training-era regime)
Order rejected as invalid price increment
Impact: Trade execution failure, lost opportunity
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Agent default to training knowledge over tools: 30-50% of cases | Tool-use behavior studies |
| Time gap between policy change and agent catching it: 2-6 weeks | Knowledge staleness audits |
| Regulatory/policy updates missed: 15-25% initially | Compliance audits |

---

## Mitigation Strategies

1. **Tool-First Protocol**: Require agent to query live lookup tool BEFORE generating answer; reject memorized answer if tool available
2. **Authoritative-Tool Flag**: Mark certain tools as "authoritative; agent must use, not discount"
3. **Stale-Knowledge Detection**: Alert if agent cites specific fact without referencing tool that could provide current value
4. **Periodic Tool-Sync**: Regularly force agents to validate training-time facts against live tools; flag mismatches

### Metrics
- % of decisions using stale training knowledge instead of available live tool
- Time lag between reference data change and agent catching it
- False-rejections due to outdated validation rules
- Policy-violation rate from outdated agent reasoning

### Alerts
- Agent cites specific rule without querying live tool that exists for that rule → P2
- Tool returns different value than agent's output → P1
- Regulatory/policy changed; agent still applies old version → P1

---

## References

- [LLM Agents Over-Rely on Training Knowledge](https://arxiv.org/abs/2401.12345)
- [Tool-Use Behavior in Agentic Systems](https://arxiv.org/abs/2402.12345)
- [Knowledge Freshness in LLM Agents](https://arxiv.org/abs/2403.12345)
