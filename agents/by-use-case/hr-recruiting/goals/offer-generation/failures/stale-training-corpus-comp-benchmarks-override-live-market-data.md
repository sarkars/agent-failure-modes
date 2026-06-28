# Stale Training-Corpus Comp Benchmarks Override Live Market Data

## Issue: An Offer-Generation Agent Answers Market-Rate Compensation Questions from Salary Figures It Absorbed During Pretraining Rather Than Calling the Live Compensation-Benchmarking Tool It Has Available, Producing Offers Anchored to Outdated Market Data for Fast-Moving Roles

**Frequency**: Occasional

**Symptoms**
- Offer rationale cites a market-rate figure for a role/level/location with no corresponding tool call to the live compensation-survey API in that turn's trace, yet states the figure with the same confidence as a tool-grounded answer
- The cited market rate matches a figure consistent with the model's pretraining-era compensation data rather than the current benchmarking tool's output for the same role and location, discoverable by independently querying the tool
- The gap concentrates on roles or markets that have seen rapid compensation movement (e.g., specialized AI/ML engineering roles, or markets with a recent cost-of-living adjustment) where live data has diverged furthest from what existed during the model's training window
- Forcing an explicit tool call ("query the comp benchmarking tool for this role/level/location") in the prompt eliminates the discrepancy, isolating the failure to the agent's default behavior of answering from parametric memory rather than to any limitation of the tool itself
- Candidates in fast-moving roles disproportionately counter or decline offers anchored to the stale figure, and recruiter follow-up using the actual current benchmarking tool shows the original offer was below current market by a margin the agent's own rationale never flagged as uncertain

**Root Cause**
The offer-generation agent has access to a live compensation-benchmarking tool, but the underlying model also carries substantial parametric knowledge of typical compensation figures absorbed during pretraining, which can produce a fluent, specific-sounding market-rate answer without a tool call, especially when the prompt does not explicitly mandate one for that field. The model has no internal signal distinguishing a tool-grounded current figure from a remembered historical one; both present with identical fluency and confidence, so without an enforced tool-call requirement the agent will sometimes substitute the latter for the former in fast-moving roles where the difference is material.

**Example**
```
Recruiter asks the offer-generation agent to draft a base-salary range for a senior ML infrastructure engineer in a major tech hub
Agent answers with a range consistent with compensation levels typical during its training window, without invoking the live compensation-benchmarking tool it has integrated access to
Actual current market rate for that specific role/level/location, per the live tool, has moved up materially in the time since the model's training cutoff due to continued demand growth in that specialty
Offer is extended at the stale, now-below-market range; candidate declines citing a competing offer well above the figure the agent generated, and a post-mortem finds the benchmarking tool was never actually called for this requisition
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM agents are documented to substitute parametric, potentially outdated knowledge for live tool-grounded data when a tool call is not explicitly enforced, a distinct hallucination risk from reasoning errors | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Allocational fairness and accuracy research on LLMs in hiring contexts documents that unverified model-internal assumptions about compensation and qualifications can diverge materially from ground-truth market data | [Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts](https://arxiv.org/pdf/2501.04316) |
| Evidence-based hiring pipeline research recommends explicit grounding of generated recommendations in current, authoritative data sources rather than relying on a model's internal knowledge for decision-relevant figures | [Towards Evidence-Based Tech Hiring Pipelines](https://arxiv.org/pdf/2504.06387) |

**Contributing Factors**
- Agent's prompt or tool-use policy does not mandate a live compensation-benchmarking tool call for every market-rate figure cited in an offer, leaving the decision to call the tool to the model's own judgment
- No automated check compares the market-rate figure stated in the offer rationale against the live benchmarking tool's current output before the offer is finalized
- Model's parametric compensation knowledge surfaces with the same fluency and confidence as genuinely tool-retrieved current data, giving recruiters no visible signal of staleness risk

---

## Mitigation Strategies

1. **Mandatory Tool Call for Every Market-Rate Figure**: Require a live compensation-benchmarking tool call as a non-optional step whenever an offer rationale states a market-rate figure, rather than leaving the decision to invoke the tool to the model
2. **Post-Hoc Consistency Check Against Tool Output**: Before finalizing an offer, run an automated comparison between the market-rate figure in the agent's rationale and the most recent live benchmarking tool query for that exact role/level/location, blocking finalization on a material mismatch
3. **Flag Fast-Moving Roles for Mandatory Re-Verification**: Maintain a list of roles/markets with historically high compensation volatility and require a fresh tool query (not a cached one) for every offer in those categories, regardless of when the requisition was opened
4. **Strip Unsupported Market-Rate Claims from Output**: Treat any market-rate claim in the agent's draft offer rationale with no corresponding tool-call trace for that turn as unverified, and block offer finalization until a tool call grounds the figure

### Metrics
- Rate of offers finalized with a market-rate figure citing no corresponding live tool-call trace for that turn
- Discrepancy rate between agent-stated market rate and live benchmarking tool output, sampled per offer at draft time
- Candidate decline/counter rate attributable to below-market offers, segmented by whether the offer's market-rate figure was tool-grounded or not

### Alerts
- Offer finalized with a market-rate figure that has no tool-call trace and disagrees materially with the live benchmarking tool's current output → P1
- A role/market flagged as high-volatility has an offer generated without a fresh (non-cached) tool query → P2
- Tool-call rate for market-rate fields drops below the mandated baseline for a given offer-generation workflow → P3

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts](https://arxiv.org/pdf/2501.04316)
- [Towards Evidence-Based Tech Hiring Pipelines](https://arxiv.org/pdf/2504.06387)
