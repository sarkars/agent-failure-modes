# Hallucinated Rollback-Target Version When Deployment-History API Returns Truncated List

## Issue: An Agent Determining Which Prior Version to Roll Back to Queries a Deployment-History API That Returns a Truncated or Paginated List Without Surfacing That Truncation as a Distinct Signal, and the Agent Selects "The Last Known-Good Version" From the Truncated List Rather Than Recognizing the True Last-Known-Good Version Lies Outside the Returned Page

**Frequency**: Occasional

**Symptoms**
- The agent rolls back to a version that the deployment-history API returned as the oldest entry in its result set, but a fuller query against the same history shows an even earlier version was the actual last confirmed-healthy release
- The rollback target chosen is plausible -- it is a real, previously deployed version -- but is not the version operators intended when they asked for "rollback to last known good"
- Re-querying the deployment-history API with pagination parameters explicitly expanded reveals additional, older entries that were never surfaced to the agent in its original query
- The mismatch concentrates on services with deployment histories long enough to exceed the API's default page size, where the "true" last-known-good version sits just past the truncation boundary
- The rollback completes without error and without any indication in the agent's output that the deployment history it selected from was incomplete

**Root Cause**
The deployment-history API returns a fixed-size page of results with no built-in signal forcing the caller to recognize that more history exists beyond the page boundary, and the agent's task framing -- "find the last known-good version" -- is satisfied by treating the oldest entry in the returned page as if it were the true history boundary. Because the agent's reasoning operates entirely on the data it received, with no explicit instruction to verify that the returned page represents the complete relevant history, a truncated result is treated as a complete one.

**Example**
```
Service has 40 prior deployments in its history; the deployment-history API's default page size returns only the 20 most recent entries
Agent is asked to identify and roll back to the last known-good version before a regression introduced in the most recent 12 deployments
Agent queries the deployment-history API once, receives the 20-entry page, and identifies entry 18 (the oldest entry in that page) as "before the regression, last known-good"
Actual regression was introduced 28 deployments ago; the true last-known-good version is entry 29, which falls outside the returned 20-entry page entirely
Rollback executes to entry 18's version, which itself already contains an earlier, unrelated regression that entry 18's deployment had introduced
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to complete plausible-sounding conclusions from incomplete tool output, rather than treating a truncated or partial result as a signal requiring further verification | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use agents show measurable miscalibration between expressed confidence and actual correctness when relying on a tool response that is incomplete rather than fully representative | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Frameworks for detecting and correcting tool-use errors in dialogue and agentic systems identify failure to recognize paginated or truncated tool responses as a distinct, recurring tool-use error category | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |

**Contributing Factors**
- The deployment-history API's response includes no explicit "more results available" or total-count signal that the agent's prompt requires it to check
- The agent's task framing treats "oldest entry in the returned data" as equivalent to "earliest deployment in history" with no instruction distinguishing the two
- No automated check compares the selected rollback target's position against the total known deployment count before the rollback executes

---

## Mitigation Strategies

1. **Mandatory Pagination-Completeness Check Before Selection**: Require the agent to verify, via the API's total-count or next-page signal, that it has retrieved the full relevant deployment history before selecting a rollback target from it, paginating further if the signal indicates more results exist
2. **Explicit Truncation Flag in Tool Schema**: Require the deployment-history API to return an explicit boolean or count field indicating whether the response is truncated, and block rollback-target selection on any response where that flag is unresolved
3. **Regression-Introduction Confirmation, Not Just Recency**: Require the agent to confirm the candidate rollback target predates the specific regression by checking deployment-level diffs or change logs, rather than treating "oldest entry in the queried page" as sufficient evidence of being pre-regression
4. **Pre-Rollback Target Verification Against Full History Count**: Before executing a rollback, automatically verify the selected target's position against the service's total deployment count, flagging any selection that was made from a page not covering the full history

### Metrics
- Rate of rollback-target selections made from a deployment-history query result that was truncated or paginated
- Rate of rollbacks where the selected target itself required a subsequent rollback due to containing an unrelated regression
- Time between rollback execution and detection of a still-regressed rollback target

### Alerts
- A rollback target is selected from a deployment-history response with no confirmed total-count or "no more results" signal → P1
- A rollback executes to a version that a fuller history query later shows was not actually the last known-good version → P1
- Truncated-response rate for deployment-history queries used in rollback decisions exceeds the defined threshold for a rolling window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
