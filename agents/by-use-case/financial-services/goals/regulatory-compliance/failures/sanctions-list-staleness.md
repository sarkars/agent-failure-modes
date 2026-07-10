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

### Prevention

1. **Event-driven near-real-time sanctions list synchronization**: Replace batch-refresh model with event-driven ingestion: subscribe to official feeds (OFAC SDN API, EU sanctions RSS, UN Consolidated List webhook updates). On each feed update, atomically refresh the screening database within 15 minutes. Implement dual-database strategy: active list (used for screening) + staging list (receives updates) + atomic cutover when staging list verified complete. Fail-safe: if feed unreachable for >1 hour, switch to read-only mode and refuse screening transactions until list restored. Root cause mitigation: Prevents staleness by replacing periodic batch with event-driven near-real-time sync.

2. **Mandatory freshness verification gate with SLA enforcement**: Implement pre-screening gate that queries: "What is the official publication timestamp of the current sanctions list?" and "How old is the list in our database?" Refuse screening if list age >2 hours during business hours (SLA: ≤2 hours). Log the list version identifier, effective date, and freshness check result with every screening. Root cause: Prevents blind use of stale cache by enforcing explicit freshness verification before screening proceeds.

3. **Retroactive re-screening on list updates with gap-window detection**: When sanctions list updated, automatically trigger retroactive screening of: (a) transactions screened in past 4 hours (gap-window transactions), (b) all open/pending transactions in flight. Re-screen against new list. Alert if any previously-cleared transactions now match. Maintain audit trail: "Transaction X screened at T1 against list-v1: clear; list updated to list-v2 at T2; re-screened at T3: MATCH found". Root cause: Catches transactions that slipped through during stale-list window.

### Detection & Response

1. **List freshness monitoring and refresh-job health**: Instrument sanctions list synchronization pipeline to track: (a) time of last successful refresh, (b) official list publication timestamp from OFAC/EU/UN, (c) age delta (how stale is our copy), (d) refresh job execution time and success/failure status. Alert immediately on: refresh job failure, age delta >2 hours, or API unreachable. Target: List age <30 minutes during business hours.

2. **Gap-window transaction auditing**: After each list update, log: (a) old list version, (b) new list version, (c) entities added in update, (d) time gap-window (interval when old list was in use), (e) transactions screened during gap-window, (f) re-screening results (matches found / clear). Generate daily compliance report: "Gap-window transactions with re-matches: [list]". Alert on new matches found.

### Architecture Patterns

1. **Dual-Buffer Sanctions List Service**: Maintains: (1) Active List (used for screening requests), (2) Staging List (receives feed updates). Feed processor: subscribes to OFAC/EU/UN APIs, updates Staging List. Validation: verifies Staging List completeness and format. Atomic Cutover: once Staging validated, atomically swaps to become Active List. Monitoring: tracks update latency, SLAs on freshness.

2. **Real-Time Feed Ingestion Pipeline**: Subscribes to official sources: OFAC SDN API (event-driven), EU sanctions (hourly RSS), UN Consolidated List (daily download with webhook). On update, parses entities, normalizes identifiers (name matching, entity-type classification), upserts into database. Logs source, timestamp, version hash.

3. **Retroactive Re-Screening Engine**: Batch job triggered on list update. Queries: "Which transactions were screened in past N hours?" Runs each through new list. On match detection, escalates to compliance team with side-by-side comparison (old list vs. new list result).

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Sanctions List Freshness | <30 min | >120 min | Time between official OFAC/EU/UN publication and list update in screening database (per API query) |
| Refresh Job Success Rate | >99.9% | <99.5% | # of successful scheduled refreshes / total scheduled refreshes (daily, weekly rolling) |
| Mean Time to Detect Staleness | <5 min | >15 min | Time from official publication to automated detection of staleness (monitoring system detects age delta) |
| Retroactive Re-Match Detection Rate | >95% | <90% | # of matches found via re-screening gap-window transactions / estimated matches (calibrated against compliance reviews) |
| Gap-Window Transaction Volume | <10/update | >50/update | # of transactions screened during stale-list window (between update detection and cutover), target to minimize |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sanctions List Staleness | List age exceeds 2 hours during business hours (10 AM - 6 PM) or 4 hours overnight | CRITICAL | Immediately stop screening transactions; page on-call; escalate to compliance; attempt feed reconnection; switch to read-only mode |
| Refresh Job Failure | Scheduled list refresh fails 3 consecutive times or fails to complete within 1 hour | CRITICAL | Page SRE and compliance; halt screening if unable to manually update within 15 min; investigate feed connection and data integrity |
| Gap-Window Re-Match Found | Retroactive re-screening of transactions screened during stale-list window finds new match against updated list | CRITICAL | Compliance review; investigate transaction (potential violation); determine if trade was executed; escalate to regulatory reporting if necessary |

---

## References

- [Standard Benchmarks Fail -- Auditing LLM Agents in Finance Must Prioritize Risk](https://arxiv.org/abs/2502.15865)
- [Evaluating LLMs in Finance Requires Explicit Bias Consideration](https://arxiv.org/abs/2602.14233)
