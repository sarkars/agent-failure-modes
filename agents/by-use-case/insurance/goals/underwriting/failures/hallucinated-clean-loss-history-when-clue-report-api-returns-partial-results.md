# Hallucinated Clean Loss History When CLUE Report API Returns Partial Results

## Issue: An Underwriting Agent's Call to the Comprehensive Loss Underwriting Exchange (CLUE) Report API Times Out or Returns a Partial, Truncated Result Set, and Instead of Treating the Incomplete Response as Unverified, the Agent Reports the Applicant as Having a Clean Loss History, Underwriting the Policy Without Pricing or Declining for Prior Losses That Actually Exist

**Frequency**: Occasional

**Symptoms**
- A policy is underwritten and priced as if the applicant has no prior losses, even though the applicant's actual CLUE report, when independently pulled in full, shows one or more prior claims that should have triggered a pricing surcharge or referral
- The underwriting agent's tool-call trace shows a timeout or a response flagged as truncated or partial from the CLUE report API, immediately followed by an underwriting rationale stating "no prior losses reported," with no retry or escalation in between
- Asking the agent why it reported a clean history after a partial response produces a reasoning trace treating the partial result as equivalent to a complete, clean report, rather than as an incomplete and therefore unverified result
- The miss concentrates on CLUE queries made during the reporting bureau's known peak-load or maintenance windows, when partial-response rates are elevated, since that is when the agent most often receives an ambiguous response and defaults to assuming a clean record
- The gap is typically discovered only when a claim is filed and the claims adjuster pulls a fresh CLUE report, finding a prior loss that should have affected the original underwriting decision

**Root Cause**
When the CLUE report API call times out or returns a partial result set, the underwriting agent receives a non-definitive signal -- not an explicit "clean history" confirmation, but also not a complete record -- and has no hard rule requiring it to treat that incompleteness as an unverified, non-clean state. Because the agent's downstream underwriting decision is not gated on an explicit, positively confirmed complete CLUE report, it proceeds to state a clean loss history based on the absence of any loss records in the partial response it did receive, generating a rationale that reads identically to one produced by a genuinely complete, clean report.

**Example**
```
Underwriting agent queries the CLUE report API for a homeowners applicant during a known bureau peak-load window
API call returns a truncated response after a partial timeout, containing zero loss records but explicitly flagged by the API as an incomplete result set
Underwriting agent's rationale states "Applicant has no prior losses reported -- standard rate applies," treating the absence of records in the partial response as equivalent to a confirmed clean history
Applicant actually has a prior water-damage claim from eighteen months earlier that would have been present in a complete CLUE pull, which the underwriting decision never priced for or referred for review
A subsequent unrelated claim triggers a fresh CLUE pull during claims handling, surfacing the prior loss and revealing the original underwriting decision was made on an incomplete record
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to fabricate plausible factual claims rather than surfacing an incomplete or failed tool response as a blocking condition, a distinct and recurring failure category | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use agents frequently fail to distinguish a tool call that returned a partial or truncated result from one that returned a complete, confirmed result, producing confident downstream output from an unverified data source | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Agentic AI for commercial insurance underwriting is evaluated specifically against incomplete-data cases to test whether agents over-rely on internal assumptions rather than verifying that an external data source returned a complete record before relying on it | [Agentic AI for Commercial Insurance Underwriting with Adversarial Self-Critique](https://arxiv.org/html/2602.13213) |

**Contributing Factors**
- The CLUE report API's partial or truncated response is not explicitly distinguished from a confirmed-complete, clean response in the agent's tool-handling logic
- The underwriting decision is not gated on an explicit, positively confirmed complete CLUE report, allowing it to proceed on a partial or ambiguous tool-call outcome
- Partial-response rates are elevated during the reporting bureau's known peak-load and maintenance windows, concentrating the failure exactly when underwriting volume may also be elevated

---

## Mitigation Strategies

1. **Hard Stop on Partial or Truncated CLUE Response**: Require the underwriting agent to treat any CLUE report API response flagged as partial, truncated, or timed out as unverified, blocking the underwriting decision until a complete, confirmed report is received
2. **Mandatory Retry-and-Verify Before Underwriting Decision**: On a partial or truncated response, require an automated retry, and if the retry also returns an incomplete result, route the application to manual underwriter review rather than proceeding on an unverified record
3. **Completeness-Flag Surfacing in Underwriting Rationale**: Require the underwriting agent's rationale to explicitly state the CLUE report's completeness status (complete vs. partial vs. unavailable) whenever a loss-history determination is made, rather than stating a clean-history conclusion without that context
4. **Post-Bind CLUE Completeness Reconciliation**: Run a periodic automated reconciliation comparing bound policies' recorded loss-history status against a fresh, complete CLUE pull, flagging any policy bound on a partial or unverified report

### Metrics
- Rate of underwriting decisions stating a clean loss history with no corresponding confirmed-complete CLUE report response
- Rate of CLUE report API calls returning a partial or truncated result, by time of day and bureau load window
- Rate of policies found, on post-bind reconciliation, to have been underwritten on an incomplete loss-history record

### Alerts
- A policy is bound with a clean-loss-history determination and no corresponding confirmed-complete CLUE report response → P1
- A claim reveals a prior loss that should have been present in the original CLUE pull used for underwriting, and that pull was flagged as partial or truncated → P1
- Rate of partial or truncated CLUE report responses exceeds the defined threshold for a rolling window without a corresponding increase in manual-review routing → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Agentic AI for Commercial Insurance Underwriting with Adversarial Self-Critique](https://arxiv.org/html/2602.13213)
