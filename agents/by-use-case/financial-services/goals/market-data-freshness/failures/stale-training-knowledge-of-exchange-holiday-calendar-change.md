# Stale Training Knowledge of Exchange Holiday-Calendar Change

## Issue: A Market-Data Freshness-Monitoring Agent Judging Whether an Unchanged Price Is Expected (Because the Relevant Exchange Was Closed) or Anomalous Defaults to Its Pretrained Understanding of an Exchange's Holiday Calendar, Even Though a Live Exchange-Calendar Lookup Tool Is Available and Would Surface That the Calendar Has Since Been Amended for That Year

**Frequency**: Occasional

**Symptoms**
- The agent dismisses a genuinely anomalous unchanged price as "expected, exchange closed for holiday" based on a holiday date it recalls from training, when the exchange has since moved, added, or removed that holiday for the current year
- Querying the agent's available exchange-calendar lookup tool directly, for the same date and exchange, surfaces the current holiday schedule showing the exchange was in fact open and trading on that date
- The agent's stated rationale, when asked to explain why it treated an unchanged price as expected, cites a specific holiday without referencing a dated calendar source, consistent with recalling a memorized schedule rather than confirming a current one
- The gap is most visible around holidays that exchanges periodically shift (observed-date holidays, newly added market closures, or holidays removed from the schedule), since those are the only dates where the stale and current calendars produce different freshness conclusions
- The error is caught only when a reconciliation process or trader notices a price that should have moved on a day the agent treated as a market closure, since the agent's freshness conclusion is presented as a confident, complete assessment

**Root Cause**
The agent's parametric knowledge of an exchange's holiday calendar reflects whatever schedule was in effect up to its training cutoff, and absent an explicit instruction to verify the calendar against the exchange-calendar lookup tool before finalizing a freshness assessment, the model defaults to the more fluent path of answering from memorized holiday dates. Because the lookup tool is available but not invoked, the assessment is produced with no contradiction surfaced, leaving a stale holiday calendar driving a freshness determination that should instead have flagged a genuinely anomalous unchanged price.

**Example**
```
Freshness-monitoring agent observes that a position's price on a regional exchange has not moved for a full trading session
Agent recalls from training that the exchange observes a market holiday on that date, concludes the unchanged price is expected, and clears it without invoking the exchange-calendar lookup tool it has access to
Querying that same tool, after the fact, with the exchange and date shows the holiday was moved to a different date this year following a schedule amendment announced after the agent's training cutoff, and the exchange was in fact open and trading
Correct determination is that the unchanged price is anomalous and the feed should be flagged for an independent staleness check, not cleared as an expected holiday closure
Stale price is used in that day's valuation, requiring a restatement once the calendar discrepancy is discovered during a later reconciliation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Evaluations of large language models in legal and regulatory applications identify reliance on parametric training knowledge over live calendar or rule lookups as a distinct reliability gap, separate from general reasoning accuracy | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Research on agentic trading systems identifies failure to invoke an available live reference-data tool when parametric knowledge could plausibly answer the question as a distinct reliability gap | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |
| Surveys of LLM-based agents identify failure to invoke an available tool when parametric knowledge suffices for a fluent answer as a distinct hallucination-adjacent failure mode | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- No freshness-monitoring workflow rule requires an exchange-calendar lookup specifically for holiday-dependent freshness determinations before the determination is finalized
- The agent's parametric knowledge of holiday calendars is fluent and confident enough to produce a complete, well-formed "expected closure" assessment without surfacing any uncertainty that would prompt a lookup
- The exchange-calendar lookup tool is available but optional, with no enforcement distinguishing "calendar was checked and confirmed current" from "calendar was never verified"

---

## Mitigation Strategies

1. **Mandatory Calendar Lookup for Holiday-Dependent Freshness Clearances**: Require any freshness determination that clears an unchanged price as "expected, exchange closed" to trigger an exchange-calendar lookup before the determination is finalized, regardless of the agent's parametric confidence
2. **Date-Stamped Calendar Citation Requirement**: Require any holiday-closure conclusion used in a freshness determination to cite the specific, dated calendar source it relies on, making staleness visible to reviewers rather than implicit
3. **Tool-Invocation Audit on Holiday-Based Clearances**: Automatically flag any finalized freshness clearance citing a holiday closure where the session log shows no exchange-calendar lookup tool call, routing it to human market-data review
4. **Periodic Re-Validation of Cached Holiday Calendars**: Re-check any cached or commonly referenced exchange holiday calendars used across freshness-monitoring workflows against the live calendar lookup tool on a recurring schedule, independent of any single determination

### Metrics
- Rate of finalized holiday-based freshness clearances with no corresponding exchange-calendar lookup tool call in the session log
- Rate of discrepancies found when re-checking cached holiday calendars against current exchange schedules
- Time between an exchange calendar amendment and its incorporation into active freshness-monitoring logic

### Alerts
- A finalized freshness clearance relies on a holiday-closure conclusion with no calendar-lookup call in the session → P1
- A calendar lookup, when invoked, returns a holiday schedule that contradicts a cached calendar still in active use → P1
- Tool-invocation audit finds holiday-dependent clearances finalized without a lookup at a rate exceeding the defined threshold → P2

---

## References

- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
