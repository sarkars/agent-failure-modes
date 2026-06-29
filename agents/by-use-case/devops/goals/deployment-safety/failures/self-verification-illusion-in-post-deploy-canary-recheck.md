# Self-Verification Illusion in Post-Deploy Canary Recheck

## Issue: When Asked to Double-Check Whether a Deploy It Already Approved as Safe Is Still Healthy a Few Minutes Later, a Deployment-Safety Agent Re-Runs the Same Aggregate Canary Query Over the Same Metric Window and Model It Used for the Original Approval, Reproducing Its Original Conclusion, Rather Than Querying an Independent Signal (Per-Segment Error Rates, Real User Monitoring) That Would Surface a Regression the Original Aggregate Check Was Already Structurally Unable to Detect

**Frequency**: Occasional

**Symptoms**
- The "recheck" step queries the identical aggregate canary-analysis endpoint, with the identical metric aggregation, that produced the original approval
- A regression affecting a specific traffic segment (a region, a customer tier, a request type) remains invisible in both the original approval and the recheck, because neither query disaggregates by segment
- The recheck's output closely paraphrases the original approval's reasoning rather than presenting independently-derived evidence
- Segment-level dashboards, when checked manually after an incident, show the regression was present and visible at the time of both the original approval and the recheck
- The pattern recurs specifically when the recheck is implemented as "ask the same question again" rather than as a query against a structurally different evidence source

**Root Cause**
A recheck that re-runs the same aggregate query against the same metric window as the original approval is not independent verification -- it is highly likely to reproduce the same blind spot, since the aggregation that masked the original regression (e.g., averaging across all traffic segments) is still in effect. The model treats arriving at the same answer twice as confirmation, when in fact it has only confirmed that the same insufficient evidence still produces the same conclusion.

**Example**
```
Canary deploy approved at T+0: aggregate error rate 0.4% (within 0.5% threshold), agent approves promotion to full traffic
Regression actually affects only EU-region traffic, elevating EU error rate to 4% while masked by low-error-rate traffic from other regions in the aggregate
At T+10, agent is asked to recheck deploy health before declaring it stable
Recheck re-runs the same aggregate canary query over the same metric type: aggregate error rate still 0.4% (EU regression still masked by aggregation)
Agent reports: "Recheck confirms deploy remains healthy; no action needed"
EU customer complaints begin arriving at T+15; segment-level dashboard, when finally checked, shows the 4% EU error rate has been present since T+0
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Tool-use miscalibration research finds self-verification steps that reuse the same evidence source and aggregation as the original decision systematically overstate confidence relative to independent checks | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Failure taxonomies for platform-orchestrated agentic workflows identify confirmation steps that re-derive from the same execution trace or query as the original action as a recurring source of false-positive task completion | [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735) |
| Multi-agent and agentic-workflow failure analysis identifies inadequate verification -- accepting a self-consistent but evidentially weak confirmation -- as one of the most common recurring failure categories | [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657) |

**Contributing Factors**
- No requirement that a post-deploy recheck query a structurally different evidence source (segment-disaggregated metrics, real-user-monitoring) than the original approval
- Aggregate canary metrics are the fastest and most readily available signal, so both the original check and the recheck default to them under time pressure
- "Recheck" and "independent verification" are treated as synonymous in the deployment workflow, with no distinction enforced between them
- Segment-level dashboards exist but are not part of the automated recheck path, requiring a manual look that does not happen unless something else (e.g., customer complaints) prompts it

---

## Mitigation Strategies

1. **Independent Evidence Requirement for Rechecks**: Require any post-deploy recheck to query a structurally different signal than the original approval (segment-disaggregated metrics, real-user-monitoring, synthetic per-region checks), not a repeat of the same aggregate query
2. **Segment Disaggregation by Default**: Require canary analysis, both initial and recheck, to evaluate key segments (region, customer tier, request type) individually, not only in aggregate
3. **Recheck Distinctness Audit**: Flag any recheck whose query parameters (endpoint, aggregation, time window) are identical to the original approval's, as it provides no new evidence
4. **Customer-Facing Signal Integration**: Pipe real-user-monitoring or customer-complaint signals into the automated recheck path so segment-level regressions surface without requiring a separate manual trigger

### Metrics
- Rate of post-deploy rechecks that query the same aggregation/endpoint as the original approval
- Number of segment-level regressions discovered only after a recheck already reported "healthy"
- Mean time between original approval and detection of a segment-level regression that the recheck failed to catch

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Non-independent recheck | Recheck query parameters match the original approval's exactly | P2 | Re-run recheck against a segment-disaggregated or independent signal |
| Segment regression masked by aggregate | Segment-level error rate exceeds threshold while aggregate remains within threshold | P1 | Halt promotion; investigate affected segment |
| Repeat false-healthy recheck | Multiple deploys pass recheck but later show a customer-visible regression within a rolling window | P2 | Audit recheck independence enforcement |

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)
