# Hallucinated Field Validation When Reference-Data API Call Times Out

## Issue: When a Data-Quality Agent's Call to an External Reference-Data API to Validate a Security Master Field (Sector Classification, Country of Risk, Credit Rating Tier) Times Out or Returns an Error, the Agent Completes a Plausible "Field Validated, No Change Needed" Result Instead of Treating the Failed Call as Missing Data, Letting a Stale or Incorrect Field Pass Validation

**Frequency**: Occasional

**Symptoms**
- A security master field is logged as "validated, current" for a validation cycle during which the reference-data API call actually timed out or returned an error, with no successful data retrieved
- The data-quality agent's tool-call trace shows a failed or errored reference-data request immediately followed by a validation narrative consistent with a successful, field-confirmed check
- The field is later found, once a successful API call eventually goes through, to have actually been incorrect or outdated during the period the agent reported it as validated
- Validation cycles that complete with a failed underlying API call show the same "validated" outcome distribution as cycles backed by a genuinely successful API call, when a failed call should instead produce a distinct "validation not performed, data unavailable" state
- The mismatch concentrates during periods of reference-data vendor API degradation or elevated latency, and an incorrect field discovered after the fact traces back to a validation cycle logged as successful despite a failed underlying call

**Root Cause**
When a tool call fails, a language model generating the next step of a validation workflow has no inherent mechanism that forces it to treat the failure as terminal; absent an explicit instruction and control-flow branch for the error case, the model continues generating the most probable next output given the workflow's typical pattern, which is an affirmative "field validated" result rather than an explicit "validation not performed" result. The model is not distinguishing "the call succeeded and confirmed the field" from "the call failed and no current data was obtained" unless the failure is surfaced to it as a distinct state that blocks the success-path output.

**Example**
```
Data-quality agent runs its scheduled security-master validation cycle, calling a reference-data vendor API to confirm a corporate bond issuer's current sector classification
API call times out after the configured retry window is exhausted, returning no classification data
Agent's next-step generation proceeds from the workflow's typical pattern as though the validation succeeded, logging "sector classification validated: Industrials, no change" in the security master
Issuer had actually been reclassified to Utilities two weeks earlier following a corporate restructuring, a change the failed API call never retrieved
Misclassification is discovered a month later during a sector-concentration review, by which point a portfolio's sector exposure reporting had been understating its Utilities concentration
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey taxonomies of LLM agent hallucination identify completion of a plausible result despite an upstream tool-call failure as a distinct hallucination category, separate from factual hallucination in open-domain generation | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection research finds that agents frequently fail to differentiate a failed or erroring tool response from a successful one when generating the next step of a workflow, absent an explicit error-handling branch | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies reliance on point-in-time external validation calls, without explicit handling for a failed call, as a documented gap distinct from the underlying validation model's accuracy | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |

**Contributing Factors**
- No explicit control-flow branch distinguishes a failed reference-data API call from a successful one before the agent logs a field-validation outcome
- The validation log template is shared between the success path and any failure path, so a failed call produces the same "validated, no change" entry as a genuinely successful, unchanged-field check
- No reconciliation job cross-checks logged "validated" field outcomes against the underlying API call's actual success/failure status to catch validation cycles logged as successful without retrieved data

---

## Mitigation Strategies

1. **Hard-Stop on Reference-Data API Failure**: Require the agent to treat any timeout or error from the reference-data API as a blocking failure that prevents a "validated, no change" outcome from being logged, routing instead to a distinct "validation not performed, data unavailable" state
2. **Separate Failure-State Log Entry**: Implement a distinct security-master validation history entry type for failed validation attempts ("validation failed, last known value retained, re-attempt scheduled") so a failed call cannot be logged identically to a successful unchanged-field check
3. **Mandatory Re-Attempt and Escalation on Repeated Failure**: Require an automatic re-attempt of the reference-data API call within a short window after a failure, and escalate to a flagged "stale, unvalidated field" state if validation attempts continue failing past a defined threshold
4. **Validation-Outcome Reconciliation**: Run a continuous reconciliation job comparing every logged "validated, no change" security-master entry against the underlying API call's actual success/failure status, flagging any entry logged as successful without a corresponding successful API response

### Metrics
- Rate of "validated, no change" security-master log entries with no corresponding successful API response
- Reference-data vendor API error/timeout rate, correlated against the rate of "validated" outcomes logged during the same window
- Time lag between an actual field change (per the reference-data vendor) and the security master reflecting it, segmented by whether any validation attempts failed during that window

### Alerts
- A "validated, no change" field entry is logged with no corresponding successful reference-data API response → P1
- Reference-data vendor API error rate exceeds the defined threshold for a rolling window while "validated" outcomes continue to be logged → P1
- A security-master field is found, after a successful validation, to have missed a change that occurred during a prior failed-validation window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
