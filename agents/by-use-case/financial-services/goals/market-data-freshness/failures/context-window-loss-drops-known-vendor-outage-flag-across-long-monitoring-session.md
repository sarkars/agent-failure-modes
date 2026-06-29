# Context-Window Loss Drops Known Vendor-Outage Flag Across Long Monitoring Session

## Issue: A Market-Data Freshness-Monitoring Agent Running a Single Long Session That Continuously Checks Price Feeds Across Many Instruments Establishes Early in the Session That a Specific Vendor Feed Is Known to Be in an Outage Window and That Any Unchanged Prices From That Vendor Should Be Treated as Suspect Rather Than Confirmed-Current, but as the Session Processes Dozens of Subsequent Instrument Checks, That Standing Outage Flag Falls Out of Effective Context and Later Checks Against the Same Vendor's Feed Are Treated as Normal, Confirmed-Current Prices

**Frequency**: Occasional

**Symptoms**
- Early in the monitoring session, the agent correctly notes a specific vendor feed is in a known outage window and flags all instruments sourced from that vendor as having suspect, not-confirmed-current prices
- Dozens of instrument checks later in the same session, an unchanged price from the same outage-affected vendor is reported as "confirmed current, no staleness detected," with no reference to the standing outage flag established earlier
- The outage determination is present verbatim earlier in the session transcript but does not appear in the agent's later-stage reasoning or output, consistent with the finding having fallen out of effective context rather than being explicitly revised
- Re-presenting a later instrument check in a fresh, short context that explicitly includes the standing outage flag causes the agent to correctly treat the unchanged price as suspect, confirming the lapse was a context-availability issue rather than a change in the vendor's actual status
- Downstream valuation or risk reports compiled from the session's running output show some outage-affected instruments flagged as stale and others from the identical vendor treated as current, depending solely on how far into the session each check occurred

**Example**
```
Market-data monitoring agent begins a session checking freshness across several hundred instruments; check 6 reveals Vendor X's feed has been returning identical prices for an unusual duration and a status page confirms Vendor X is in a declared outage window -- agent correctly flags all Vendor-X-sourced instruments as suspect pending outage resolution
Session continues through hundreds of unrelated instrument checks across other vendors
Check 214 covers a separate instrument also sourced from Vendor X, with a price that has likewise not updated -- the same outage condition flagged at check 6
Agent's output for check 214 reports "price unchanged but within normal range for low-volatility instrument; no staleness flag warranted," with no reference to the standing Vendor X outage established 200+ checks earlier
Valuation report compiled from the session marks the check-6 instrument as stale-suspect but the check-214 instrument as confirmed-current, even though both are subject to the identical, still-ongoing Vendor X outage
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Model performance on tasks requiring retrieval of information from earlier in a long context degrades significantly as relevant content moves away from the beginning or end of the context window, even when the information remains technically present in the transcript | [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172) |
| Failure-mode taxonomies for LLM systems identify context-window degradation over long sessions as a distinct mechanism by which earlier-established facts or standing conditions are silently dropped without an explicit reversal | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |
| Agent-environment interaction failure research notes that an agent's standing awareness of an environmental condition (such as a known data-source outage) can degrade over the course of an extended interaction even though the condition itself has not changed | [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504) |

**Contributing Factors**
- The freshness-monitoring session is run as one continuous, growing conversation across many instrument checks rather than discrete batches with an explicitly carried-forward conditions ledger
- The Vendor X outage flag, once established, is not promoted to a structured, persistently-injected fact (e.g., a standing "known-outage vendors" list re-included in every subsequent check) and instead relies on the model's own attention over the full transcript
- Instrument-check volume within a single session is large enough that the originating outage determination is many turns removed from later checks against the same vendor by the time recall would be needed
- No automated cross-reference step checks each new instrument's source vendor against a running list of currently known outages independent of the model's in-context recall

---

## Mitigation Strategies

1. **Persistent Known-Outage Ledger**: Maintain a structured, external list of vendors currently in a known outage or degraded-feed window, and re-inject that list into the prompt for every subsequent instrument check rather than relying on the model's recall of its own earlier finding
2. **Deterministic Vendor Cross-Check**: Run an automated, non-LLM check of each instrument's source vendor against the known-outage ledger before or alongside the agent's own freshness assessment, independent of context-window recall
3. **Session Chunking With Explicit Carry-Forward**: Break long monitoring sessions into smaller batches, each opened with an explicit summary of standing conditions (known outages, open staleness flags) from prior batches, rather than one continuously growing conversation
4. **Final-Report Consistency Audit**: Before compiling the valuation or risk report, run an automated check that every instrument sourced from a known-outage vendor is consistently flagged, rather than trusting the session's own narrative consistency

### Metrics
- Rate of instrument checks sourced from a known-outage vendor that are not flagged as suspect later in the same session
- Position in the session (check number / token distance) at which outage-flagging consistency begins to degrade
- Number of monitoring sessions using a persistent known-outage ledger versus relying solely on in-context recall

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Outage-ledger inconsistency | An instrument's source vendor matches the known-outage ledger but the agent's check does not flag it as suspect | P1 | Block valuation reliance on the instrument; re-check with ledger explicitly injected |
| Long session without ledger re-injection | Session exceeds a defined check-count or token threshold without a standing-conditions re-injection | P2 | Trigger session chunking and carry-forward summary |
| Final-report flagging gap | Consistency audit finds an outage-vendor instrument listed as confirmed-current in the final report | P1 | Escalate for manual price verification before the report is used in valuation or risk decisions |

---

## References

- [Lost in the Middle: How Language Models Use Long Contexts](https://arxiv.org/abs/2307.03172)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
- [Aegis: Agent-Environment Failures](https://arxiv.org/html/2508.19504)
