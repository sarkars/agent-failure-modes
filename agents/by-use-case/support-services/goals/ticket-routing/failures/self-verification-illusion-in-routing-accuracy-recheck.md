# Self-Verification Illusion in Routing-Accuracy Recheck

## Issue: Before Finalizing a Ticket's Routing Destination, a "Double-Check the Routing Is Correct" Step Re-Prompts the Same Model Against the Same Ticket Text Rather Than Cross-Referencing the Account's Actual Provisioned Products or the Receiving Queue's Actual Specialization, So a Misrouted Ticket Is Still Confirmed as Correctly Routed

**Frequency**: Occasional

**Symptoms**
- A ticket is routed to a queue, and a "confirm routing" recheck step approves the routing as correct, even though the destination queue's specialization or the account's provisioned products do not actually match the ticket's content
- The recheck step's trace shows it re-read the same ticket text and the same routing rationale rather than querying the account's provisioning record or the receiving queue's current specialization roster
- Confirmation language ("routing confirmed correct") is nearly identical between tickets later found to be correctly routed and tickets later re-routed by the receiving queue, because both rechecks draw on the same ticket text and routing rationale
- Tickets whose routing recheck is backed by a fresh provisioning or queue-roster query show a measurably lower re-route rate than tickets whose recheck only re-reads the original routing rationale
- A ticket is re-routed by the receiving specialist queue shortly after a "routing confirmed correct" recheck, with the re-route logged as a routing correction rather than as a failed verification

**Root Cause**
Re-prompting the same model to "double-check the routing," using only the ticket text and routing rationale it already has in context, does not introduce an independent or more current source of evidence — the model has no privileged way to know whether the destination queue's specialization or the account's provisioning actually matches, so its recheck mostly restates the same reasoning that produced the original routing decision. Genuine verification requires a fresh query against the account's provisioning record or the queue's current specialization roster, not a re-read of the agent's own prior rationale for the routing.

**Example**
```
Routing agent classifies a ticket about "database sync errors" and routes it to the DataConnect specialist queue, citing the ticket's terminology as the rationale
Before finalizing, a "confirm routing" recheck step re-prompts the same model: "Is this routing correct?"
Recheck re-reads the same ticket text and routing rationale rather than querying the account's actual provisioned-product list
Account is provisioned only for TeamSync, an unrelated calendar-sync product, not DataConnect
Routing is confirmed as correct; the DataConnect queue receives the ticket, finds no DataConnect provisioning on the account, and re-routes it — logged as a routing correction rather than linked to the failed recheck
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Calibration in autonomous, tool-using agents remains notably underexplored relative to single-turn LLM calibration, and self-confirmation by the same model operating on the same prior context is not equivalent to independent verification against a system of record | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Tool-use error taxonomies for dialogue systems identify failure to verify a decision's actual downstream basis, as distinct from verifying the immediate stated rationale, as a recurring and under-addressed error class | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| CRM task-capability benchmarks for LLM agents identify ticket-routing accuracy as a distinct, measurable capability separate from general response-generation quality, with routing errors traced to inadequate grounding in account-specific structured data rather than to the routing rationale's internal coherence | [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2) |

**Contributing Factors**
- Routing-accuracy recheck is implemented as a re-prompt over the same ticket text and rationale rather than a fresh provisioning-record or queue-roster query
- The recheck's confirmation language is templated identically regardless of whether a fresh structured-data check occurred, conflating "rationale is internally consistent" with "routing is actually correct"
- No distinction is tracked between "recheck backed by a fresh provisioning or roster query" and "recheck backed by a re-read of the original rationale," so both are reported identically as a confirmed-correct routing

---

## Mitigation Strategies

1. **Mandatory Fresh Provisioning/Roster Query on Recheck**: Require the routing-confirmation step to query the account's actual provisioned-product record or the destination queue's current specialization roster rather than re-reading the ticket text or original rationale
2. **Decouple Rationale Coherence From Routing Correctness**: Treat a routing rationale's internal coherence as distinct from confirmation that the destination queue actually matches the account's provisioning or the ticket's real category; require a separate structured-data check before logging "routing confirmed"
3. **Re-Route Linkage Tracking**: Automatically link a receiving queue's re-route action to the prior "routing confirmed correct" recheck when it occurs within a defined window, surfacing recheck failures that would otherwise look like ordinary routing corrections
4. **Track Recheck-Type Outcome Divergence**: Continuously measure and report the re-route rate separately for fresh-query rechecks versus rationale-only rechecks; a large divergence is itself evidence that rationale-only rechecks are not functioning as verification

### Metrics
- Rate of routing rechecks backed by a fresh provisioning or roster query versus a rationale-only re-read
- Re-route rate within a defined window, segmented by recheck type
- Median time between a "routing confirmed correct" recheck and a linked re-route by the receiving queue

### Alerts
- A ticket is confirmed as "routing correct" following a rationale-only recheck and is re-routed by the receiving queue within the defined window → P2
- Re-route rate for rationale-only-recheck confirmations exceeds the re-route rate for fresh-query-recheck confirmations by more than the defined tolerance for a rolling window → P2
- A routing-confirmation recheck is logged with no corresponding provisioning or roster query → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [CRMArena: Understanding the Capacity of LLM Agents to Perform Professional CRM Tasks in Realistic Environments](https://arxiv.org/html/2411.02305v2)
