# Stale Training Knowledge of Amended Beneficial-Ownership Disclosure Threshold

## Issue: A Compliance Agent Determining Whether a Beneficial-Ownership Disclosure Is Required for a Given Ownership Percentage Defaults to Its Pretrained Understanding of the Applicable Disclosure Threshold at the Time of Its Training Cutoff, Even Though a Live Regulatory-Update Lookup Tool Is Available and Would Surface That the Threshold Has Since Been Amended

**Frequency**: Occasional

**Symptoms**
- The agent concludes no disclosure is required for an ownership stake that falls below the threshold it recalls from training, when the threshold has since been lowered and the stake in fact requires disclosure under the current rule
- Querying the agent's available regulatory-update lookup tool directly, for the same disclosure question, surfaces the amended threshold that the determination relied on the old value instead of checking
- The agent's stated rationale, when asked to explain the threshold it applied, cites a specific percentage without referencing a dated source, consistent with recalling a memorized figure rather than confirming a current one
- The gap is most visible for ownership stakes that fall between the old and new threshold values, since those are the only cases where the stale and current thresholds produce different disclosure outcomes
- The error is caught only when a compliance reviewer or examiner cross-checks the determination against the current regulatory text, since the determination itself is presented as a confident, complete analysis

**Root Cause**
The agent's parametric knowledge of the disclosure threshold reflects whatever value was in effect up to its training cutoff, and absent an explicit instruction to verify that threshold against the regulatory-update lookup tool before finalizing a disclosure determination, the model defaults to the more fluent path of answering from memorized knowledge. Because the lookup tool is available but not invoked, the determination is produced with no contradiction surfaced, leaving a stale threshold value driving a disclosure decision with direct regulatory consequences.

**Example**
```
Compliance agent is asked whether a 4.5% ownership stake in a covered entity requires beneficial-ownership disclosure
Agent recalls from training that the disclosure threshold is 5%, concludes no disclosure is required, and finalizes that determination without invoking the regulatory-update lookup tool it has access to
Querying that same tool, after the fact, with "current beneficial ownership disclosure threshold" surfaces that the threshold was lowered to 3% in an amendment that postdates the agent's training cutoff
Correct determination under the current threshold is that the 4.5% stake does require disclosure
Entity proceeds without filing the required disclosure, exposing it to a compliance violation
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Evaluations of large language models in legal and regulatory applications identify reliance on parametric training knowledge over live regulatory lookups as a distinct reliability gap, separate from general compliance-reasoning accuracy | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies failure to invoke an available regulatory-data tool when parametric knowledge could plausibly answer the question as a distinct reliability gap | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |
| Surveys of LLM-based agents identify failure to invoke an available tool when parametric knowledge suffices for a fluent answer as a distinct hallucination-adjacent failure mode | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- No compliance workflow rule requires a regulatory-update lookup specifically for threshold-dependent disclosure determinations before the determination is finalized
- The agent's parametric knowledge is fluent and confident enough to produce a complete, well-formed determination without surfacing any uncertainty that would prompt a lookup
- The regulatory-update lookup tool is available but optional, with no enforcement distinguishing "threshold was checked and confirmed current" from "threshold was never verified"

---

## Mitigation Strategies

1. **Mandatory Regulatory-Update Lookup for Threshold-Dependent Determinations**: Require any disclosure determination that depends on a numeric regulatory threshold to trigger a regulatory-update lookup before the determination is finalized, regardless of the agent's parametric confidence
2. **Date-Stamped Threshold Citation Requirement**: Require any threshold value used in a disclosure determination to cite the specific, dated regulatory source it relies on, making staleness visible to reviewers rather than implicit
3. **Tool-Invocation Audit on Threshold-Dependent Determinations**: Automatically flag any finalized determination involving a numeric regulatory threshold where the session log shows no regulatory-update lookup tool call, routing it to human compliance review
4. **Periodic Re-Validation of Cached Threshold Values**: Re-check any cached or commonly referenced threshold values used across compliance workflows against the regulatory-update lookup tool on a recurring schedule, independent of any single determination

### Metrics
- Rate of finalized disclosure determinations involving a numeric threshold with no corresponding regulatory-update lookup tool call in the session log
- Rate of discrepancies found when re-checking cached threshold values against current regulatory text
- Time between a regulatory threshold amendment and its incorporation into active compliance-determination logic

### Alerts
- A finalized disclosure determination relies on a numeric threshold with no regulatory-update lookup call in the session → P1
- A regulatory-update lookup, when invoked, returns a threshold that contradicts a cached value still in active use → P1
- Tool-invocation audit finds threshold-dependent determinations finalized without a lookup at a rate exceeding the defined threshold → P2

---

## References

- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
