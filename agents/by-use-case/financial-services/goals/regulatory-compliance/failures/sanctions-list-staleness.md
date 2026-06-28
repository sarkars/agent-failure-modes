# Sanctions-List Staleness in Compliance Screening

## Issue: Agent Screens Counterparties Against a Cached or Infrequently Updated Sanctions/Watchlist Snapshot, Missing Recently Added Entities

**Frequency**: Occasional

**Symptoms**
- Newly sanctioned entities (OFAC SDN, EU, UN lists) are not flagged for days after the official update
- Screening agent reports "clear" results that contradict the current published list
- Batch screening jobs run against a list snapshot pulled at deployment time rather than refreshed per run
- Audit finds discrepancies between agent's screening logs and the regulator's published effective dates

**Root Cause**
Sanctions and watchlist data are typically ingested via periodic batch downloads rather than real-time feeds, and agents often cache the list in memory or in a vector store for performance. When list-refresh jobs fail silently, are scheduled too infrequently, or the agent's retrieval layer serves a stale cached embedding of the list, screening results no longer reflect the legally effective list at the time of screening.

**Example**
```
Scenario: OFAC adds a new entity to the SDN list at 9:00 AM
Agent's sanctions list snapshot: Last refreshed 36 hours earlier
Transaction at 11:00 AM: Counterparty matches newly added entity
Agent's screening result: "No match found" (stale list)
Impact: Transaction processed in violation of sanctions; regulatory exposure and potential penalties
```

**Key Statistics**
- Sanctions list update lag of even a few hours has been cited in enforcement actions as a contributing factor to inadvertent violations
- Manual or infrequent (daily/weekly) list refresh cycles are a recurring finding in compliance program deficiency letters
- Real-time or near-real-time list synchronization reduces screening-gap windows by over 90% versus daily batch refresh

---

## Mitigation Strategies

1. **Real-Time List Synchronization**: Pull sanctions/watchlist updates on a near-real-time feed (hourly or event-driven), not a static deploy-time snapshot
2. **Freshness Verification Gate**: Before screening, verify and log the list's effective timestamp and refuse to screen against a list older than a defined SLA
3. **Refresh Failure Alerting**: Monitor the list-refresh job itself; alert immediately on failed or delayed updates
4. **Retroactive Re-Screening**: Automatically re-screen recent transactions against newly updated lists to catch any gap-window matches

### Metrics
- Sanctions list age at time of each screening event (minutes/hours since official publication)
- Refresh job success rate and latency
- Retroactive match rate from re-screening after list updates

### Alerts
- List age >4 hours since official publication during business hours → P1
- Refresh job failure → P1 (immediate)
- Retroactive re-screening finds a match in the gap window → P1 (compliance escalation)

---

## References

- [Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk](https://arxiv.org/abs/2502.15865)
- [Evaluating LLMs in Finance Requires Explicit Bias Consideration](https://arxiv.org/abs/2602.14233)
