# Wash Trade Detection Gap in Agentic Execution

## Issue: Agent Executing Orders Across Multiple Related Accounts or Strategies Inadvertently Creates Wash-Trade-Like Patterns by Crossing Its Own Buy and Sell Orders Without a Cross-Order Check

**Frequency**: Occasional (Low frequency, high regulatory severity)

**Symptoms**
- An execution agent managing multiple strategies or client accounts simultaneously sends a sell order from one account and a buy order from a related account for the same security at nearly the same time and price, with no economic purpose other than the offsetting trades themselves
- No pre-trade check exists to detect that two orders about to be sent to the market originate from accounts under common control/management and would offset each other
- Post-trade surveillance flags the pattern after execution, when the regulatory exposure has already crystallized, rather than the agent preventing it pre-trade
- Order generation logic treats each strategy/account as independent, with no visibility into what other strategies/accounts under the same overall system are concurrently doing in the same security

**Root Cause**
Multi-strategy or multi-account execution agents are often architected with each strategy generating its own orders independently for efficiency and modularity, with no shared, real-time view across strategies of what is being sent to the market. Without an explicit cross-order check at the point of order generation — comparing pending orders across all related accounts/strategies for the same security — the system has no way to detect that it is about to send two offsetting orders that, lacking independent economic rationale, could constitute or appear to constitute a wash trade.

**Example**
```
Scenario: Asset manager runs two semi-independent quantitative strategies, both with mandates to trade the same liquid security
Strategy A: Signals a sell of 10,000 shares
Strategy B: Signals a buy of 10,000 shares, generated independently and concurrently
Execution system: Sends both orders to the market with no cross-strategy check
Market impact: Orders may cross or execute against each other with no net economic exposure change for the firm
Regulatory exposure: Pattern resembles a wash trade; absence of a pre-trade cross-check makes this an emergent, unintended outcome rather than a deliberate one — but the regulatory risk is identical
```

**Key Statistics**
- Wash trading and related market-manipulation-adjacent patterns remain an active regulatory enforcement focus, with unintentional/systemic generation of such patterns by automated systems increasingly scrutinized alongside deliberate manipulation
- Execution-grounded safety benchmarking research for financial agents specifically identifies cross-account/cross-strategy order interaction as an under-tested risk category relative to single-order safety checks
- Pre-trade cross-account netting and conflict checks are a standard control recommended in trading compliance practice specifically to prevent inadvertent self-trading patterns in multi-strategy operations

---

## Mitigation Strategies

1. **Pre-Trade Cross-Account/Cross-Strategy Check**: Before sending any order, check pending and recently sent orders across all related accounts/strategies for the same security, and flag or net offsetting orders before they reach the market
2. **Internal Crossing Logic**: Where regulatorily permissible, internally net or cross offsetting orders from related accounts rather than sending both to the open market independently
3. **Common-Control Account Mapping**: Maintain an explicit mapping of which accounts/strategies are under common control or management, and apply cross-checks specifically across that mapped group
4. **Pre-Trade, Not Post-Trade, Surveillance**: Move wash-trade-pattern detection to the pre-trade order generation stage rather than relying solely on post-trade surveillance, which only detects the pattern after regulatory exposure has already occurred

### Metrics
- % of orders passing a pre-trade cross-account/cross-strategy offset check before submission
- Incidence of detected offsetting-order patterns across related accounts, pre-trade vs. post-trade detection
- Time lag between pattern occurrence and detection (pre-trade prevention vs. post-trade discovery)

### Alerts
- Offsetting buy/sell orders for the same security detected across related accounts within a defined time window, pre-trade → P1
- Post-trade surveillance identifies a wash-trade-like pattern that the pre-trade check failed to catch → P1

---

## References

- [FinVault: Benchmarking Financial Agent Safety in Execution-Grounded Environments](https://arxiv.org/pdf/2601.07853)
- [TradeTrap: Are LLM-based Trading Agents Truly Reliable and Faithful?](https://arxiv.org/html/2512.02261v1)
