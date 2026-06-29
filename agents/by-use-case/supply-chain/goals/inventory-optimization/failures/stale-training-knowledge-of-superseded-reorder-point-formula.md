# Stale Training Knowledge of Superseded Reorder-Point Formula

## Issue: An Inventory-Optimization Agent Computes a Reorder Point Using a Generic or Previously Standard Reorder-Point Formula It Recalls From Pretraining, Even Though the Organization Has Since Adopted a Different, Documented Formula in Its Live Policy Configuration, Despite a Policy-Lookup Tool Being Available That Would Surface the Current Formula

**Frequency**: Occasional

**Symptoms**
- A computed reorder point for a SKU does not match the value that would result from applying the organization's current, documented reorder-point formula to the same inputs
- Querying the agent's available policy-lookup tool directly, for the same SKU class, surfaces a current formula (e.g., one incorporating a supplier-lead-time variance term or a service-level target the organization adopted after a policy change) that the computation did not apply
- The agent's stated calculation, when asked to show its work, applies a formula structure without citing a dated policy-document source, consistent with recalling a memorized generic formula rather than confirming the current one
- The gap is most visible for SKU classes whose reorder-point policy was revised after the agent's training cutoff, since those are the only cases where the memorized and current formulas diverge
- Inventory analysts auditing a sample of computed reorder points against the documented current policy find systematic deviations traceable to the wrong formula being applied, not to input-data errors

**Root Cause**
The agent's parametric knowledge of reorder-point methodology reflects whatever formula was standard or most commonly described in its training data up to its cutoff, and absent an explicit instruction to verify the applicable formula against the organization's policy-lookup tool before computing a reorder point, the model defaults to the more fluent path of applying a memorized formula. Because the policy-lookup tool is available but not invoked, the computation proceeds with no contradiction surfaced, leaving a superseded formula driving live inventory decisions.

**Example**
```
Inventory-optimization agent computes a reorder point for a SKU class using a basic formula recalled from training: average daily demand times lead time, plus a fixed safety-stock buffer
Agent does not invoke the policy-lookup tool it has access to before finalizing the computation
Querying that same tool, after the fact, shows the organization adopted a revised formula six months earlier that weights safety stock by supplier lead-time variance rather than a fixed buffer
Inventory analyst auditing the computed reorder point against the documented current policy finds it understates the required safety stock for SKUs sourced from higher-variance suppliers
SKU experiences a stockout during a longer-than-average supplier lead time that the current, unused formula would have buffered against
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Surveys of knowledge-oriented retrieval-augmented generation identify that retrieval or lookup tools only reliably correct stale parametric knowledge when invocation is mandatory for the relevant computation type, since optional invocation is frequently skipped when the model's memorized answer is fluent and produces a complete-looking result | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| Research on LLM agents for supply chain management identifies reliance on generic or outdated planning formulas, rather than organization-specific live policy, as a distinct source of inventory-optimization error separate from demand-forecast accuracy | [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on parametric or cached knowledge alone causes policy updates to go unincorporated in long-running deployments | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- No inventory-optimization workflow rule requires a policy-lookup specifically before finalizing a reorder-point computation
- The agent's parametric knowledge of a generic reorder-point formula is fluent and confident enough to produce a complete, well-formed computation without surfacing any uncertainty that would prompt a lookup
- The policy-lookup tool is available but optional, with no enforcement distinguishing "formula was checked and confirmed current" from "formula was never verified"

---

## Mitigation Strategies

1. **Mandatory Policy Lookup Before Reorder-Point Computation**: Require any reorder-point calculation to trigger a policy-lookup tool call confirming the current formula before the computation is finalized, regardless of the agent's parametric confidence
2. **Date-Stamped Formula Citation Requirement**: Require any reorder-point computation to cite the specific, dated policy-document source the formula relies on, making staleness visible to reviewers rather than implicit
3. **Tool-Invocation Audit on Reorder-Point Outputs**: Automatically flag any finalized reorder-point computation where the session log shows no policy-lookup tool call, routing it to human review before it drives a purchase order
4. **Policy-Change Propagation Check**: When a reorder-point formula is revised in the policy system, require an active check that blocks any cached or memorized version of the prior formula from being used in computations going forward

### Metrics
- Rate of finalized reorder-point computations with no corresponding policy-lookup tool call in the session log
- Rate of discrepancies found when re-checking computed reorder points against the documented current policy formula
- Stockout rate attributable to reorder points computed under a superseded formula

### Alerts
- A finalized reorder-point computation relies on a formula with no policy-lookup call in the session → P1
- A policy lookup, when invoked, returns a formula that contradicts a cached or assumed formula still in active use → P1
- Stockout rate attributable to superseded-formula reorder points exceeds the defined threshold for a rolling window → P2

---

## References

- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [LLMs for Supply Chain Management](https://arxiv.org/pdf/2505.18597)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
