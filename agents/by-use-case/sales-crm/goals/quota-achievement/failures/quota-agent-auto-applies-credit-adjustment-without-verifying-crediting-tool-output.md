# Quota Agent Auto-Applies Credit Adjustment Without Verifying Crediting-Tool Output

## Issue: A Quota-Achievement Agent Authorized to Auto-Apply Routine Split-Credit Adjustments Between Reps on Co-Sold Deals Calls the Internal Crediting Tool, Receives a Response, and Applies an Adjustment to Both Reps' Quota-Attainment Records Without Checking Whether the Tool's Response Actually Confirmed the Adjustment Succeeded for Both Reps or Only One, Silently Treating a Partial-Success Response as a Full Success and Crediting One Rep While Leaving the Other's Record Unadjusted and Unflagged

**Frequency**: Occasional

**Symptoms**
- One rep's quota-attainment record reflects the agreed split-credit adjustment while the co-selling rep's record does not, despite both being part of the same adjustment request
- The crediting tool's actual response for this request contains a per-rep status field showing one success and one failure (often due to a quota-period lock or a data-validation issue on the second rep's record), but the agent's confirmation message to both reps states the adjustment was "applied successfully"
- The under-credited rep's quota attainment appears lower than agreed for the rest of the period until they notice the discrepancy themselves, typically near a commission payout or quota-attainment review
- Re-running the same crediting-tool call in isolation reproduces the partial-success response, confirming the gap was present in the original tool output and not a transient issue
- Sales-ops review of the agent's execution trace shows the full per-rep status field was present in the tool's response but the agent's downstream confirmation logic checked only for the presence of a response, not the specific success/failure value for each rep

**Example**
```
Two reps co-sell an enterprise deal and agree on a 60/40 quota-credit split; the
quota-achievement agent is asked to apply this split via the internal crediting tool
Agent calls the crediting tool with both reps' IDs and the agreed split percentages
Crediting tool's response: {"rep_a": {"status": "applied"}, "rep_b": {"status": "failed",
"reason": "quota_period_locked"}} -- a partial-success response with an explicit
per-rep status field
Agent's confirmation logic checks only that the call returned a 200-level response and
tells both reps: "Your split-credit adjustment has been applied"
Rep B's quota attainment is never actually adjusted; rep A's is
Three weeks later, during a quota-attainment review ahead of commission payout, rep B
notices their attainment doesn't reflect the agreed split and escalates
Sales-ops finds the crediting tool's original response clearly showed the per-rep
failure, but the agent never inspected that field before declaring success to both reps
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use error detection research finds agents frequently treat the receipt of any tool response as success without inspecting structured status fields within that response, missing partial or per-item failures embedded in an otherwise "successful" API call | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Research on miscalibration in tool-use agents finds agents acting on tool outputs without verifying their actual content exhibit overconfidence in reporting outcomes, stating success with the same certainty regardless of whether the underlying result was fully validated | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Execution-provenance research argues autonomous actions with real downstream consequences -- such as confirming a compensation-affecting credit adjustment -- require validating the action's claimed outcome against the specific tool-output fields that determine success, not merely against the call having completed | [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1) |

**Contributing Factors**
- The agent's success-confirmation logic checks for a non-error HTTP-level response rather than parsing and validating the structured per-rep status field the crediting tool actually returns
- Partial-success responses (one rep succeeds, one fails) are a less common path than full success or full failure, so the gap in status-field validation was not exercised during typical testing
- The agent sends a single combined confirmation message to both reps rather than a per-rep confirmation tied to that rep's specific status field, masking the asymmetric outcome
- No reconciliation step compares each rep's quota-attainment record against the crediting request shortly after submission to confirm the adjustment actually landed for both parties

---

## Mitigation Strategies

1. **Per-Field Status Validation**: Require the agent to parse and validate every per-rep (or per-item) status field in a crediting-tool response before declaring success, rather than treating a non-error response as sufficient confirmation
2. **Per-Rep Confirmation Tied to Actual Status**: Send confirmation messages keyed to each rep's specific status field, so a partial failure surfaces immediately as a distinct, unresolved item rather than being absorbed into a combined "success" message
3. **Post-Adjustment Reconciliation**: Automatically re-query each affected rep's quota-attainment record shortly after a crediting call to confirm the adjustment is reflected, independent of what the crediting tool's initial response claimed
4. **Escalation on Partial Success**: Route any crediting-tool response containing a mixed success/failure result to a sales-ops reviewer rather than allowing the agent to auto-resolve or auto-confirm it

### Metrics
- Rate of crediting-tool calls with a partial-success response that were nonetheless confirmed as fully successful to all parties
- Mean time between a partial-credit failure and the affected rep noticing the discrepancy
- Number of post-payout-cycle corrections traced back to an unvalidated partial-success tool response

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Partial-success treated as full success | Crediting-tool response contains a per-rep failure status but agent's confirmation states full success | P1 | Recall confirmation; reapply adjustment for the failed rep; notify sales-ops |
| Unvalidated status field | Agent confirms a crediting action without a logged check of the response's per-rep status field | P2 | Audit confirmation logic; require field-level validation before deployment |
| Quota-attainment record mismatch | Rep's quota-attainment record does not reflect an agent-confirmed credit adjustment within a defined window | P1 | Trigger reconciliation check against crediting-tool history |

---

## References

- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [From Agent Traces to Trust: Evidence Tracing and Execution Provenance in LLM Agents](https://arxiv.org/html/2606.04990v1)
