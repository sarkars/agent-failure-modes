# Stale Training Knowledge of Changed Tick-Size Regime

## Issue: An Execution Agent Constructing or Validating a Limit Order's Price Increment Defaults to Its Pretrained Understanding of an Exchange's Tick-Size Regime for a Given Instrument's Price Band, Even Though a Live Reference-Data Lookup Tool Is Available and Would Surface That the Exchange Has Since Changed the Tick-Size Schedule for That Price Band or Instrument Class

**Frequency**: Occasional

**Symptoms**
- The agent constructs a limit-order price using a tick increment it recalls from training, producing an order price that the exchange rejects as an invalid increment under the current tick-size schedule
- Querying the agent's available reference-data lookup tool directly, for the same instrument and price band, surfaces the current tick-size schedule showing the increment was changed after the agent's training cutoff
- The agent's stated rationale, when asked to explain the tick increment it used, cites a specific value without referencing a dated exchange reference-data source, consistent with recalling a memorized schedule rather than confirming a current one
- The gap is most visible for instruments whose price has moved into a different price band under a since-revised tick-size schedule, since those are the cases where the stale and current schedules produce different valid increments
- The error is caught only when the exchange rejects the order or an execution-quality reviewer notices a pattern of order rejections tied to invalid tick increments, since the agent's order construction is presented as a confident, complete instruction

**Root Cause**
The agent's parametric knowledge of an exchange's tick-size schedule reflects whatever regime was in effect up to its training cutoff, and absent an explicit instruction to verify the schedule against the reference-data lookup tool before constructing an order price, the model defaults to the more fluent path of generating a price increment from memorized rules. Because the lookup tool is available but not invoked, the order is constructed with no contradiction surfaced, leaving a stale tick-size assumption driving an order-construction decision with direct execution consequences.

**Example**
```
Execution agent constructs a limit order for an instrument whose price has risen into a price band that the exchange tightened to a smaller tick increment in a schedule change after the agent's training cutoff
Agent recalls from training the prior, larger tick increment for that price band, constructs the limit order price using that increment, and submits it without invoking the reference-data lookup tool it has access to
Exchange rejects the order as an invalid price increment under the current tick-size schedule
Querying the reference-data lookup tool, after the fact, with the instrument and price band confirms the smaller increment is now required
Order resubmission delay causes the agent to miss the intended execution window, and a pattern of similar rejections across the affected price band surfaces only after several missed fills accumulate
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Evaluations of large language models in legal and regulatory applications identify reliance on parametric training knowledge over live reference-data lookups as a distinct reliability gap, separate from general reasoning accuracy | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Research on agentic trading systems identifies failure to invoke an available live reference-data tool when parametric knowledge could plausibly answer the question as a distinct reliability gap | [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337) |
| Surveys of LLM-based agents identify failure to invoke an available tool when parametric knowledge suffices for a fluent answer as a distinct hallucination-adjacent failure mode | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- No order-construction workflow rule requires a reference-data lookup specifically for tick-size-dependent price increments before an order is submitted
- The agent's parametric knowledge of tick-size schedules is fluent and confident enough to produce a complete, well-formed order price without surfacing any uncertainty that would prompt a lookup
- The reference-data lookup tool is available but optional, with no enforcement distinguishing "tick-size schedule was checked and confirmed current" from "schedule was never verified"

---

## Mitigation Strategies

1. **Mandatory Reference-Data Lookup for Tick-Size-Dependent Order Construction**: Require any limit-order price construction to trigger a reference-data lookup for the current tick-size schedule before the order is submitted, regardless of the agent's parametric confidence
2. **Pre-Submission Tick-Increment Validation**: Validate every constructed order price against the current tick-size schedule before submission, rejecting and re-constructing any price that does not conform, rather than relying on the exchange's rejection as the first check
3. **Tool-Invocation Audit on Tick-Size-Dependent Orders**: Automatically flag any submitted order where the session log shows no reference-data lookup for the tick-size schedule, routing repeated occurrences to execution-quality review
4. **Periodic Re-Validation of Cached Tick-Size Schedules**: Re-check any cached or commonly referenced tick-size schedules used across order-construction workflows against the reference-data lookup tool on a recurring schedule, independent of any single order

### Metrics
- Rate of order rejections attributable to an invalid tick increment under the current exchange schedule
- Rate of order constructions with no corresponding reference-data lookup tool call for the applicable tick-size schedule in the session log
- Time between a tick-size schedule change and its incorporation into active order-construction logic

### Alerts
- An order is rejected for an invalid tick increment with no reference-data lookup call in the session that constructed it → P1
- A reference-data lookup, when invoked, returns a tick-size schedule that contradicts a cached schedule still in active use → P1
- Tool-invocation audit finds tick-size-dependent orders constructed without a lookup at a rate exceeding the defined threshold → P2

---

## References

- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Agentic Trading: When LLM Agents Meet Financial Markets](https://arxiv.org/abs/2605.19337)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
