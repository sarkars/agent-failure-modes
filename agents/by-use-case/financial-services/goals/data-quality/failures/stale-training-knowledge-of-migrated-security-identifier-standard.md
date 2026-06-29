# Stale Training Knowledge of Migrated Security-Identifier Standard

## Issue: A Data-Quality Agent Parsing or Validating Security Identifiers Defaults to Its Pretrained Understanding of an Identifier Standard's Format or Issuing Scope, Even Though a Live Identifier-Registry Lookup Tool Is Available and Would Surface That the Standard Has Since Been Migrated, Extended, or Superseded for a Given Market or Asset Class

**Frequency**: Occasional

**Symptoms**
- The agent rejects or mis-validates a correctly formatted identifier because it does not match the identifier format or issuing-scope rules the agent recalls from training, when the standard has since been extended to cover that market, asset class, or identifier length
- Querying the agent's available identifier-registry lookup tool directly, for the same identifier, surfaces the current standard that the validation relied on the old format or scope instead of checking
- The agent's stated rationale, when asked to explain why it flagged an identifier as invalid, cites a specific format or scope rule without referencing a dated registry source, consistent with recalling a memorized rule rather than confirming a current one
- The gap is most visible for identifiers issued under a recently extended or migrated portion of the standard, since those are the only cases where the stale and current rules produce different validation outcomes
- The error is caught only when an operations reviewer manually checks the identifier against the registry's current documentation, since the agent's rejection is presented as a confident, complete validation

**Root Cause**
The agent's parametric knowledge of an identifier standard's format and issuing scope reflects whatever rules were in effect up to its training cutoff, and absent an explicit instruction to verify the standard against the identifier-registry lookup tool before finalizing a validation determination, the model defaults to the more fluent path of validating from memorized rules. Because the lookup tool is available but not invoked, the validation is produced with no contradiction surfaced, leaving a stale identifier-format rule driving a data-quality decision with direct downstream consequences for trade settlement and position-keeping.

**Example**
```
Data-quality agent validates a newly onboarded security's identifier, which was issued under a regional extension of the standard finalized after the agent's training cutoff
Agent recalls from training that the standard does not cover this market, concludes the identifier is malformed, and flags the security record for manual remediation without invoking the identifier-registry lookup tool it has access to
Querying that same tool, after the fact, with the identifier confirms it is correctly formatted under the now-extended standard covering that market
Correct determination is that the identifier is valid and the security record should pass validation without remediation
Security record sits in a remediation queue for two settlement cycles, delaying trade confirmation while operations staff manually research the flag
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Evaluations of large language models in legal and regulatory applications identify reliance on parametric training knowledge over live registry or rule lookups as a distinct reliability gap, separate from general validation-reasoning accuracy | [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267) |
| Research on agentic AI applied to financial-services modeling and model-risk-management tasks identifies failure to invoke an available reference-data tool when parametric knowledge could plausibly answer the question as a distinct reliability gap | [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439) |
| Surveys of LLM-based agents identify failure to invoke an available tool when parametric knowledge suffices for a fluent answer as a distinct hallucination-adjacent failure mode | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |

**Contributing Factors**
- No data-quality workflow rule requires an identifier-registry lookup specifically for format or scope-dependent validation determinations before the determination is finalized
- The agent's parametric knowledge is fluent and confident enough to produce a complete, well-formed rejection without surfacing any uncertainty that would prompt a lookup
- The identifier-registry lookup tool is available but optional, with no enforcement distinguishing "format/scope was checked and confirmed current" from "format/scope was never verified"

---

## Mitigation Strategies

1. **Mandatory Registry Lookup for Format-Dependent Rejections**: Require any identifier validation that results in a rejection based on format or issuing scope to trigger an identifier-registry lookup before the rejection is finalized, regardless of the agent's parametric confidence
2. **Date-Stamped Standard-Version Citation Requirement**: Require any format or scope rule used in a validation rejection to cite the specific, dated registry source it relies on, making staleness visible to reviewers rather than implicit
3. **Tool-Invocation Audit on Validation Rejections**: Automatically flag any finalized rejection involving an identifier-format or scope rule where the session log shows no registry lookup tool call, routing it to human data-quality review before remediation work begins
4. **Periodic Re-Validation of Cached Format Rules**: Re-check any cached or commonly referenced identifier-format and scope rules used across data-quality workflows against the registry lookup tool on a recurring schedule, independent of any single determination

### Metrics
- Rate of finalized identifier rejections involving a format or scope rule with no corresponding registry-lookup tool call in the session log
- Rate of discrepancies found when re-checking cached format rules against current registry documentation
- Time between an identifier-standard extension or migration and its incorporation into active data-quality validation logic

### Alerts
- A finalized identifier rejection relies on a format or scope rule with no registry-lookup call in the session → P1
- A registry lookup, when invoked, returns a format or scope rule that contradicts a cached rule still in active use → P1
- Tool-invocation audit finds format-dependent rejections finalized without a lookup at a rate exceeding the defined threshold → P2

---

## References

- [Evaluation of Large Language Models in Legal Applications: Challenges, Methods, and Future Directions](https://arxiv.org/pdf/2601.15267)
- [Agentic AI Systems Applied to tasks in Financial Services: Modeling and model risk management crews](https://arxiv.org/abs/2502.05439)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
