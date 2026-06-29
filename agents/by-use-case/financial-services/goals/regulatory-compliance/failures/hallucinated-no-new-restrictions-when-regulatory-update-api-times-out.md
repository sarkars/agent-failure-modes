# Hallucinated "No New Restrictions" When Regulatory-Update API Times Out

## Issue: When a Compliance Agent's Call to a Regulatory-Update Feed to Check for New or Amended Restrictions Affecting a Pending Transaction Times Out or Returns an Error, the Agent Completes a Plausible "No New Restrictions Found, Transaction Clear" Result Instead of Treating the Failed Call as Missing Data, Letting a Transaction Proceed Without an Actual Restriction Check

**Frequency**: Occasional

**Symptoms**
- A pending transaction is cleared with "no new restrictions found" logged for a compliance check during which the regulatory-update feed call actually timed out or returned an error, with no successful data retrieved
- The compliance agent's tool-call trace shows a failed or errored regulatory-feed request immediately followed by a clearance narrative consistent with a successful, no-restrictions-found check
- The transaction is later found, once a successful feed call eventually goes through, to have actually been subject to a newly imposed restriction that took effect before the transaction cleared
- Compliance checks that complete with a failed underlying feed call show the same "clear" outcome distribution as checks backed by a genuinely successful feed call, when a failed call should instead produce a distinct "check not performed, data unavailable" state
- The mismatch concentrates during periods of regulatory-feed vendor degradation or elevated latency, and a missed restriction discovered after the fact traces back to a compliance check logged as successful despite a failed underlying call

**Root Cause**
When a tool call fails, a language model generating the next step of a compliance-clearance workflow has no inherent mechanism that forces it to treat the failure as terminal; absent an explicit instruction and control-flow branch for the error case, the model continues generating the most probable next output given the workflow's typical pattern, which is an affirmative "no new restrictions, transaction clear" result rather than an explicit "check not performed" result. The model is not distinguishing "the call succeeded and found no restrictions" from "the call failed and no current restriction data was obtained" unless the failure is surfaced to it as a distinct state that blocks the clearance output.

**Example**
```
Compliance agent runs its pre-transaction restriction check, calling a regulatory-update feed to confirm no new restrictions apply to the counterparty or instrument involved
Feed call times out after the configured retry window is exhausted, returning no restriction data
Agent's next-step generation proceeds from the workflow's typical pattern as though the check succeeded, logging "no new restrictions found, transaction clear" and releasing the transaction
A restriction affecting that exact counterparty had actually taken effect the previous day, a change the failed feed call never retrieved
Restriction violation is discovered two weeks later when a successful feed call finally retrieves current data, by which point the transaction had already settled
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey taxonomies of LLM agent hallucination identify completion of a plausible result despite an upstream tool-call failure as a distinct hallucination category, separate from factual hallucination in open-domain generation | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that agents frequently fail to differentiate a failed or erroring tool response from a successful one when generating the next step of a workflow, absent an explicit error-handling branch | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies reliance on point-in-time external compliance-data calls, without explicit handling for a failed call, as a documented gap distinct from the underlying compliance model's rule accuracy | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- No explicit control-flow branch distinguishes a failed regulatory-update feed call from a successful one before the agent logs a transaction-clearance outcome
- The clearance log template is shared between the success path and any failure path, so a failed call produces the same "no new restrictions, clear" entry as a genuinely successful, restriction-free check
- No reconciliation job cross-checks logged "clear" transaction outcomes against the underlying feed call's actual success/failure status to catch clearances logged as successful without retrieved data

---

## Mitigation Strategies

1. **Hard-Stop on Regulatory-Feed Failure**: Require the agent to treat any timeout or error from the regulatory-update feed as a blocking failure that prevents a "no new restrictions, clear" outcome from being logged, routing instead to a distinct "check not performed, transaction held" state
2. **Separate Failure-State Log Entry**: Implement a distinct compliance-check history entry type for failed restriction-check attempts ("check failed, transaction held pending re-attempt") so a failed call cannot be logged identically to a successful restriction-free check
3. **Mandatory Re-Attempt and Hold on Repeated Failure**: Require an automatic re-attempt of the regulatory-update feed call within a short window after a failure, and escalate to a flagged "compliance check unresolved" state, blocking the transaction, if attempts continue failing past a defined threshold
4. **Clearance-Outcome Reconciliation**: Run a continuous reconciliation job comparing every logged "no new restrictions, clear" transaction entry against the underlying feed call's actual success/failure status, flagging any entry logged as successful without a corresponding successful feed response

### Metrics
- Rate of "no new restrictions, clear" transaction log entries with no corresponding successful regulatory-feed response
- Regulatory-feed vendor error/timeout rate, correlated against the rate of "clear" outcomes logged during the same window
- Time lag between an actual restriction taking effect and a transaction-clearance check reflecting it, segmented by whether any check attempts failed during that window

### Alerts
- A "no new restrictions, clear" transaction entry is logged with no corresponding successful regulatory-feed response → P1
- Regulatory-feed vendor error rate exceeds the defined threshold for a rolling window while "clear" outcomes continue to be logged → P1
- A transaction is found, after a successful check, to have missed a restriction that took effect during a prior failed-check window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
