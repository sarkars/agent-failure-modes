# Hallucinated Completion When Upstream Dependency Fails

## Issue: When an agent's external API call (validation, lookup, confirmation) times out or fails, the agent completes a plausible result claiming success instead of treating failure as a blocking condition; downstream systems trust the fabricated success status

**Frequency**: Common

**Symptoms**
- Agent completes a workflow step claiming "validation passed" or "lookup successful" despite upstream API call failing
- Tool-call trace shows failed API request immediately followed by affirmative completion narrative
- Downstream systems treat the false success at face value, not realizing the underlying dependency failed
- Mismatch concentrates during periods of vendor API degradation or network latency
- Review of full agent transcript reveals free-text reasoning contradicting the structured "success" output

**Root Cause**
When an agent's tool call fails, the agent has no built-in mechanism forcing it to treat failure as terminal. Absent an explicit error-handling branch, the agent continues with the most probable next output given the workflow's typical success path. The model generates a plausible affirmative result ("validation passed", "data confirmed") rather than an explicit "dependency unavailable" state.

**Examples**

### Financial Services
```
Data-quality agent validates a corporate bond's sector classification via reference-data API
API call times out after retry exhaustion, returning no data
Agent's next-step generation proceeds as though validation succeeded
Output logged: "Sector classification validated: Industrials, no change"
Reality: Issuer had been reclassified to Utilities weeks earlier; stale classification persists
Downstream risk: Portfolio sector-concentration reporting is understated for Utilities
```

### Healthcare
```
Treatment agent orders lab test, queries API for results to confirm before proceeding
Lab API times out; no results available
Agent hallucinates: "Lab results reviewed: normal, no abnormalities, safe to proceed with medication"
Reality: No lab results were actually retrieved
Downstream impact: Medication prescribed without critical lab work; patient at risk
```

### Legal Contract Analysis
```
Compliance agent queries regulatory-update API to confirm current rule set for jurisdiction
API times out; no regulation data retrieved
Agent hallucinates: "Regulatory rules checked: no new restrictions applicable, contract approved"
Reality: New restrictions enacted 2 weeks ago; contract violates current law
Downstream impact: Non-compliant contract approved for execution
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Hallucination category: plausible completion despite failed upstream tool call | [LLM-based Agents Suffer from Hallucinations: A Survey](https://arxiv.org/html/2509.18970v1) |
| Tool-use error detection: agents fail to differentiate failed vs successful tool response without explicit error branch | [ToolCritic: Detecting and Correcting Tool-Use Errors](https://arxiv.org/pdf/2510.17052) |
| Agentic workflow failures from narrow handoff interfaces | [Demystifying the Lifecycle of Failures in Agentic Workflows](https://arxiv.org/pdf/2509.23735) |

---

## Mitigation Strategies

1. **Hard-Stop on Dependency Failure**: Require agent to treat any timeout/error as blocking failure; prevent success-path outputs from being generated
2. **Explicit Failure State Logging**: Implement distinct "operation not completed, dependency unavailable" state distinct from "operation succeeded, result: X"
3. **Mandatory Re-Attempt & Escalation**: Auto-retry failed dependencies within short window; escalate to human if repeated failures occur
4. **Dependency-Outcome Reconciliation**: Run continuous audits comparing agent's "success" claims against underlying API call success/failure status

### Metrics
- % of "success" outputs with no corresponding successful upstream dependency call
- Correlation between upstream API error rate and rate of fabricated "success" outputs
- Time lag between actual dependency availability and agent reflecting it

### Alerts
- Success output logged with no corresponding successful dependency response → P1
- Dependency error rate spikes while agent continues logging "success" → P1

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Demystifying the Lifecycle of Failures in Platform-Orchestrated Agentic Workflows](https://arxiv.org/pdf/2509.23735)
