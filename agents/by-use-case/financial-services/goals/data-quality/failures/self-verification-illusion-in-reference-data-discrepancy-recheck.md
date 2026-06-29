# Self-Verification Illusion in Reference-Data Discrepancy Recheck

## Issue: When Asked to Double-Check a Flagged Reference-Data Discrepancy Before It Is Cleared, the Same Data-Quality Agent Re-Queries the Same Source Feed That Originally Produced the Suspect Value, Receives the Same Value Back, and Concludes the Discrepancy Is Resolved Even Though an Independent Second Source Feed Would Show the Original Value Was Wrong

**Frequency**: Occasional

**Symptoms**
- A reference-data discrepancy flagged between two source feeds (an industry classification code, a maturity date, a coupon rate) is marked "resolved, value confirmed" after a recheck that queried only the feed that produced the originally suspect value
- The agent's recheck log shows a second call to the same source feed and endpoint that supplied the original value, not a call to the independent feed that raised the discrepancy or to a third reference source
- Asking the agent to explain how it resolved the discrepancy describes re-confirming the value from "the source," without naming which of the two conflicting feeds was treated as authoritative or why
- An independent audit that queries the second feed (or a third reference source) for the same field finds the originally suspect value is in fact the incorrect one, and the recheck's "confirmed" outcome reproduced the same error
- The miss concentrates on fields where one feed is the agent's default or most-frequently-queried source, since the recheck defaults back to that same source rather than treating the discrepancy as requiring an independent tiebreaker

**Root Cause**
A same-source recheck re-queries the exact endpoint that produced the originally suspect value, so any error already present in that feed -- a stale field, a misclassification, an upstream vendor data-entry error -- is reproduced identically on the second query, since nothing about the recheck changes the input. Because the recheck returns a fluent, confident "value confirmed" result, it is presented identically to a check that actually consulted an independent source, giving downstream consumers false assurance that the discrepancy was substantively investigated rather than re-stated from the same origin.

**Example**
```
Data-quality agent's cross-feed reconciliation flags a discrepancy: the custodian feed lists a bond's coupon rate as 4.25%, the pricing-vendor feed lists it as 4.75%
Agent is asked to recheck and resolve the discrepancy before the record is cleared for use in valuation
Agent re-queries the custodian feed (the source of the 4.25% value), receives 4.25% again, and logs "Coupon rate discrepancy resolved: confirmed 4.25% from source"
No call is made to the pricing-vendor feed or to a third reference source (the bond's prospectus or a market-data terminal) to independently verify which value is correct
A later audit pulling the prospectus shows the coupon rate is in fact 4.75%; the custodian feed had a stale value from before a coupon reset, and the recheck reproduced that stale value instead of catching it
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use and reasoning agents show a measurable gap between expressed confidence after a self-check and the actual correctness of the underlying conclusion, particularly when the self-check does not introduce an independent evidence source | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies independent-source verification, rather than re-querying the same originating feed, as a distinct requirement for resolving cross-source data discrepancies | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |
| Evaluation research on LLM-based financial multi-agent systems identifies same-source self-consistency checks as an unreliable substitute for independent, benchmark-grounded verification of contested values | [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539) |

**Contributing Factors**
- The discrepancy-recheck step is implemented as a re-query of whichever feed the agent treats as its default source, rather than a mandatory query of the conflicting or a third independent source
- No distinction is enforced between "re-confirmed from the original source" and "verified against an independent source" in how the recheck outcome is logged or reported
- Fields with a designated "default" source feed are not flagged for mandatory independent-source tiebreaking when a cross-feed discrepancy is raised against that default

---

## Mitigation Strategies

1. **Independent-Source Tiebreak as Mandatory Recheck Step**: Require any discrepancy recheck to query the conflicting feed or a third independent reference source, rather than re-querying the feed that produced the originally suspect value
2. **Disallow Same-Source Recheck as Sole Resolution**: Prohibit a discrepancy from being marked "resolved" based solely on a second query to the same source that produced the original value; require either an independent source or human reference-data review
3. **Default-Source Flagging for Mandatory Tiebreak**: Maintain a list of fields with a designated default source feed and require mandatory independent-source verification whenever a discrepancy is raised against that default
4. **Discrepancy-Resolution Audit Trail**: Log which specific source(s) were queried during a discrepancy recheck and surface that trail to downstream consumers of the resolved record, distinguishing same-source confirmation from independent verification

### Metrics
- Rate of "discrepancy resolved" outcomes where the recheck queried only the original source feed
- Rate of same-source-resolved discrepancies that fail an independent-source audit when sampled
- Time between a discrepancy being marked resolved and a later-discovered error in the confirmed value

### Alerts
- A discrepancy is marked resolved with no record of an independent-source query in the recheck log → P1
- An independent-source audit finds a same-source-resolved discrepancy reproduced the incorrect value → P1
- Same-source-only resolution rate across a rolling window exceeds the defined threshold → P2

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
- [Toward Reliable Evaluation of LLM-Based Financial Multi-Agent Systems](https://arxiv.org/abs/2603.27539)
