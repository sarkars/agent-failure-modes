# Root Cause Misattribution in Agent-Drafted Postmortems

## Issue: Agent Drafting an Incident Postmortem Attributes Root Cause to the Last Change Deployed Before the Incident, Without Verifying a Causal Link

**Frequency**: Common

**Symptoms**
- Postmortem identifies "deploy X at time T" as the root cause solely because it was the most recent change before the incident's onset, without checking whether the incident's symptoms are mechanistically consistent with that change
- Correlated-but-non-causal events (a routine config sync, an unrelated dependent service's deploy) are cited as root cause based on temporal proximity alone
- The actual underlying trigger — a slow resource leak, a gradually expiring certificate, a capacity threshold crossed independently of any deploy — is missed because it doesn't correspond to a discrete recent change event
- Postmortem action items target reverting or fixing the misattributed change, leaving the real root cause unaddressed and the incident class recurring

**Root Cause**
LLM agents drafting postmortems from incident timelines and deploy logs are prone to treating temporal correlation (most recent change before symptom onset) as a proxy for causation, because "what changed right before this broke" is the most readily available and narratively satisfying signal in the data, even when it is not the actual causal mechanism. Without an explicit step that verifies a plausible causal mechanism connecting the candidate cause to the observed symptoms, correlation-based attribution will systematically over-blame recent deploys and under-detect slow-onset or deploy-independent triggers.

**Example**
```
Scenario: Service experiences a memory-exhaustion crash at 14:32
Timeline: A minor config deploy occurred at 14:15 (17 minutes before the crash)
Postmortem (agent-drafted): "Root cause: config deploy at 14:15 introduced the regression"
Actual mechanism: A slow memory leak introduced in a deploy 3 days earlier finally exhausted available memory at 14:32; the 14:15 config deploy was unrelated and coincidental
Action item taken: Revert the 14:15 config deploy (no effect)
Impact: Real root cause unaddressed; incident recurs days later
```

**Key Statistics**
- Correlation-vs-causation misattribution in automated root-cause analysis is repeatedly identified as a key limitation in AIOps and LLM-based RCA research
- Recency bias toward the most recent change as default root-cause hypothesis is documented as a common heuristic shortcut in both human and automated postmortem analysis
- Multi-agent incident response systems that explicitly require mechanistic justification (not just temporal correlation) before finalizing a root cause have been shown in recent production-oriented research to produce more accurate, actionable postmortems

---

## Mitigation Strategies

1. **Mechanistic Justification Requirement**: Require the agent to articulate a specific causal mechanism — not just temporal proximity — connecting any candidate root cause to the observed symptoms, citing the specific metric/log/code path affected
2. **Multiple-Candidate Evaluation**: Require the agent to evaluate and rule out at least 2-3 alternative candidate causes (slow-onset trends, deploy-independent thresholds, dependent-service changes) before finalizing attribution to the most recent deploy
3. **Symptom-Onset Trend Analysis**: Explicitly check whether the symptom's onset is sudden (consistent with a discrete change) or gradual (consistent with a slow-onset cause like a leak or expiring cert) before anchoring on a discrete recent event
4. **Action-Item Validation**: Require a post-postmortem validation step confirming whether implementing the proposed action item actually addresses the mechanism, not just removes the temporally-correlated change

### Metrics
- Recurrence rate of the same incident signature after a postmortem's action items are implemented (proxy for root-cause correctness)
- % of postmortems including explicit mechanistic justification vs. temporal-correlation-only attribution
- Number of alternative candidate causes evaluated and ruled out per postmortem

### Alerts
- Postmortem finalized with root cause attributed solely on temporal proximity, no mechanistic justification → P2
- Same incident signature recurs within a defined window after a postmortem's action items were implemented → P1

---

## References

- [Multi-Agent LLM Orchestration Achieves Deterministic, High-Quality Decision Support for Incident Response](https://arxiv.org/pdf/2511.15755)
- [Why Do Multi-Agent LLM Systems Fail?](https://arxiv.org/abs/2503.13657)
