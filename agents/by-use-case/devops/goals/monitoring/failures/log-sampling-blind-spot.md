# Log Sampling Blind Spot in Agent-Driven Root Cause Analysis

## Issue: Agent Performs Root Cause Analysis Over Sampled Logs and Misses the Specific Log Lines That Explain a Rare but Critical Failure

**Frequency**: Common

**Symptoms**
- Root-cause analysis agent queries a log pipeline that applies head-based or uniform random sampling, which disproportionately drops low-frequency error types relative to high-frequency routine log lines
- The agent's investigation concludes "no clear error pattern found" when the actual causal error existed but was sampled out before reaching the agent's query
- Rare error codes (occurring in well under 1% of requests) are systematically underrepresented in the sampled set the agent reasons over, even though they are exactly the signal of interest for diagnosing a rare incident
- Agent's confidence in a "no root cause found" conclusion is not adjusted for the sampling rate applied upstream

**Root Cause**
Log pipelines commonly apply sampling to control storage and query cost, and uniform or head-based sampling strategies are calibrated for typical-volume log lines, not for rare, high-signal error events. An LLM agent reasoning over the sampled log set has no way to know which lines were dropped, so it treats the sampled set as if it were complete, producing root-cause conclusions whose confidence does not reflect the actual information loss from sampling — particularly damaging because the events sampling is most likely to drop (rare lines) are often exactly the ones that matter most for incident diagnosis.

**Example**
```
Scenario: Incident investigation for an intermittent payment failure occurring in 0.05% of transactions
Log pipeline: Applies 1% uniform sampling to control storage costs
Agent: Queries sampled logs for the incident window, finds no matching error log line
Agent conclusion: "No root cause identified in available logs"
Reality: The specific error log line existed in the unsampled stream but had roughly a 99% chance of being dropped by sampling
Impact: Root cause analysis fails not because the signal didn't exist, but because sampling removed it before the agent ever saw it
```

**Key Statistics**
- Sampling-induced blind spots for rare, high-severity log events are a well-known limitation of cost-optimized observability pipelines in SRE practice
- AIOps research on automated root-cause analysis identifies log completeness/coverage as a primary driver of analysis quality, with sampled pipelines showing materially lower diagnostic recall for low-frequency error types
- Trace-/error-aware adaptive sampling (preserving error and anomalous traces at higher rates than routine traces) is the standard mitigation recommended in observability engineering practice specifically to address this gap

---

## Mitigation Strategies

1. **Error-Biased Adaptive Sampling**: Configure log/trace sampling to retain error-level and anomalous events at a much higher rate than routine informational log lines, rather than uniform sampling
2. **Sampling-Rate-Aware Confidence**: Require the root-cause agent to factor the known sampling rate into its confidence statement — "no error found in a 1%-sampled stream" should never be reported with the same confidence as "no error found in unsampled logs"
3. **On-Demand Full-Fidelity Retrieval**: For active incident investigation, allow the agent to trigger retrieval of full-fidelity (unsampled) logs for the specific time window and service under investigation, rather than relying solely on the standard sampled pipeline
4. **Sampling Metadata Exposure**: Attach sampling-rate metadata to every log query result so any downstream consumer (human or agent) can see how much was potentially dropped

### Metrics
- Diagnostic recall for known rare-error incidents, compared between sampled and full-fidelity log retrieval
- % of root-cause investigations that explicitly state the sampling rate of the logs queried
- Time-to-resolution delta between investigations using adaptive error-biased sampling vs. uniform sampling

### Alerts
- Root-cause agent reports "no error found" sourced from a log stream with sampling rate below a defined fidelity threshold without flagging the limitation → P2
- Active incident investigation proceeds without triggering full-fidelity log retrieval for the affected window → P2

---

## References

- [Agentic Observability: Automated Alert Triage for Adobe E-Commerce](https://arxiv.org/pdf/2602.02585)
- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
