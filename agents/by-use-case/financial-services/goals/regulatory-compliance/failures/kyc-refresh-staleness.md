# KYC Refresh Staleness

## Issue: Agent Relies on a Customer's Initial KYC Risk Rating Without Triggering a Refresh When Materially Risk-Relevant Account Activity Changes

**Frequency**: Common

**Symptoms**
- Customer's KYC risk tier (low/medium/high) remains unchanged for years despite material changes in transaction volume, geography, or counterparty profile that would warrant re-assessment
- Periodic refresh schedule is calendar-based only (e.g., refresh every 3 years for low-risk customers) without an event-driven trigger for sudden activity changes that fall within the calendar window
- Agent's transaction monitoring flags individual suspicious transactions but does not connect a pattern of changing behavior to the underlying customer risk rating, which remains static
- A customer onboarded as low-risk who later begins transacting with high-risk jurisdictions or counterparties continues to be monitored under low-risk thresholds, reducing scrutiny exactly when it should increase

**Root Cause**
KYC refresh processes are commonly scheduled on a fixed calendar cadence tied to the customer's risk tier at onboarding, because this is operationally simple to implement and audit. This approach assumes a customer's risk profile is relatively static between scheduled refreshes, but actual customer behavior can change materially within that window — a static calendar-only refresh has no mechanism to detect and respond to those changes until the next scheduled date arrives, leaving a gap where elevated real-world risk is monitored under outdated, lower-scrutiny thresholds.

**Example**
```
Scenario: Customer onboarded as "low risk" retail account, scheduled for KYC refresh every 3 years
18 months later: Account begins receiving large, frequent wire transfers from a jurisdiction associated with elevated AML risk
Transaction monitoring: Flags individual transactions as somewhat unusual but does not exceed low-risk-tier alert thresholds
KYC risk tier: Remains "low risk" because the calendar-based refresh is not due for another 18 months
Impact: Elevated actual risk activity is monitored under thresholds calibrated for a lower risk profile, increasing regulatory and AML exposure
```

**Key Statistics**
- Event-driven KYC refresh triggers (in addition to calendar-based cycles) are a standard regulatory expectation in many AML/KYC supervisory frameworks specifically because static periodic refresh has documented gaps
- A material share of AML enforcement actions cite failure to update customer risk ratings in response to changed transaction behavior as a contributing supervisory finding
- Risk-tier-static monitoring (continuing to apply onboarding-era thresholds despite behavior change) is consistently identified as a root cause in post-incident AML program reviews

---

## Mitigation Strategies

1. **Event-Driven Refresh Triggers**: Implement triggers that initiate an out-of-cycle KYC refresh when transaction monitoring detects material changes in volume, geography, or counterparty risk profile, independent of the calendar-based schedule
2. **Behavioral Drift Detection**: Continuously compare current transaction behavior against the behavior profile that justified the original risk tier, and flag significant drift even when no single transaction crosses an alert threshold
3. **Dynamic Threshold Escalation**: Temporarily apply higher-risk-tier monitoring thresholds when behavioral drift is detected, pending completion of the triggered refresh, rather than waiting for the refresh to complete before adjusting scrutiny
4. **Refresh Completion Tracking**: Track time-to-completion for triggered refreshes separately from calendar-based refreshes, ensuring event-driven triggers are not deprioritized relative to scheduled ones

### Metrics
- % of customers with an event-driven refresh trigger fired, and time-to-completion for that refresh
- Behavioral drift score (current activity vs. risk-tier-justifying baseline activity) per customer
- Rate of risk-tier upgrades resulting from event-driven refresh vs. calendar-based refresh

### Alerts
- Material behavioral drift detected with no corresponding refresh trigger fired → P1
- Event-driven refresh trigger fired but not completed within the required regulatory timeframe → P1

---

## References

- [Position: Standard Benchmarks Fail – LLM Agents Present Overlooked Risks](https://www.arxiv.org/pdf/2502.15865v1)
- [FinVault: Benchmarking Financial Agent Safety in Execution-Grounded Environments](https://arxiv.org/pdf/2601.07853)
