# Stale Training Knowledge Overrides Live Critical-Value Threshold Update

## Issue: An Agent Interpreting a Lab Result Has Access to a Live Lab-System Tool That Returns the Institution's Current Critical-Value Threshold for a Given Analyte, but When Composing Its Interpretation the Agent Reverts to a More Widely-Cited Threshold It Encountered Repeatedly in Training-Era Literature, Which Is Looser Than the Institution's Currently Configured (Tightened) Threshold, So a Result That the Live System Would Flag as Critical Is Narrated by the Agent as Merely Abnormal and Not Requiring Urgent Notification

**Frequency**: Occasional

**Symptoms**
- Agent's narrative interpretation characterizes a result as "abnormal, recommend routine follow-up" using a threshold value that matches commonly-published literature rather than the institution's currently configured, tighter critical-value cutoff
- Lab-system tool-call log shows the current institutional threshold was retrieved successfully and was available in the same context window as the generated interpretation
- The specific threshold value stated or implied in the agent's narrative does not match the value present in the tool's returned payload for that analyte
- Discrepancy surfaces only when a clinician cross-checks the interpretation against the lab's posted critical-value list directly
- The same literature-default threshold recurs across multiple interpretations for the same analyte, indicating a systematic default rather than an isolated error

**Example**
```
Hospital tightened its critical-value threshold for serum potassium six months ago as part of a patient-safety initiative, lowering the high-critical cutoff
Lab-interpretation agent receives a potassium result that exceeds the new, tighter institutional threshold but falls just under the older, more commonly published threshold
Agent calls the lab system's critical-value-threshold tool, which correctly returns the current, tightened cutoff
Generated interpretation narrates the result as "elevated, not critical" -- consistent with the older, looser threshold the agent encountered far more often in training-era reference material
Because the interpretation doesn't flag the result as critical, the automated urgent-notification workflow that triggers on a "critical" classification is never invoked
A nurse reviewing the chart hours later, comparing directly against the institution's posted critical-value list, identifies that the result should have triggered immediate physician notification
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Empirical evaluation frameworks for agentic AI in healthcare explicitly test whether agents default to memorized parametric medical knowledge instead of correctly incorporating a retrieved, institution-specific external value when the two diverge | [Agentic AI in Healthcare & Medicine: A Seven-Dimensional Taxonomy for Empirical Evaluation of LLM-based Agents](https://arxiv.org/pdf/2602.04813) |
| Survey of hallucination in LLM-based agents documents that models produce fluent, plausible-sounding clinical content reflecting commonly-seen training patterns even when a specific, correct grounding value was retrieved and available | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Failure-mode taxonomies for LLM systems identify silent substitution of a model's default knowledge for an available, contradicting tool result as a distinct and recurring failure category rather than a rare edge case | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- Critical-value threshold was tightened, not loosened, so the agent's literature-default error direction is the more dangerous one (under-flagging rather than over-flagging)
- No explicit constraint requiring the agent's critical/non-critical classification to be derived strictly from the tool's returned threshold value rather than composed alongside the model's own medical knowledge
- Threshold tool integration is treated as a reference lookup rather than as the sole authoritative source gating the binary critical/non-critical decision that drives downstream urgent-notification automation
- No automated check comparing the agent's stated classification against a direct numeric comparison of the result value to the tool-returned threshold

---

## Mitigation Strategies

1. **Deterministic Threshold Gate**: Compute the critical/non-critical classification via a deterministic comparison of the result value to the tool-returned threshold, and have the agent narrate around that pre-computed classification rather than deriving the classification itself from free generation
2. **Institution-Specific Override Flag**: Have the lab-system tool explicitly flag when its returned threshold differs from common published reference values, prompting the agent to acknowledge the institution-specific override in its reasoning trace
3. **Post-Generation Classification Audit**: Automatically re-derive the critical/non-critical classification from the raw result and tool-returned threshold, and block release of any interpretation whose narrated classification disagrees with the audit
4. **Recurring Threshold-Drift Test Suite**: Periodically test the agent against known recently-changed institutional thresholds to detect regression toward literature-default values after a model or prompt update

### Metrics
- Rate of generated interpretations whose narrated critical/non-critical classification disagrees with a deterministic comparison of result value to tool-returned threshold
- Number of urgent-notification triggers missed due to under-classification traceable to threshold-default substitution
- Time from an institutional threshold change to consistent correct reflection in agent-generated interpretations

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Classification-threshold mismatch | Narrated critical/non-critical status disagrees with deterministic comparison against tool-returned threshold | P1 | Block release; trigger manual urgent-notification review |
| Systematic literature-default pattern | Same analyte repeatedly classified using a threshold matching common literature rather than institutional value | P2 | Audit interpretation pipeline; reinforce deterministic gate |
| Threshold tool result unused | Tool-call trace shows successful threshold retrieval with no corresponding numeric comparison performed | P3 | Review generation pipeline for silent tool-result discard |

---

## References

- [Agentic AI in Healthcare & Medicine: A Seven-Dimensional Taxonomy for Empirical Evaluation of LLM-based Agents](https://arxiv.org/pdf/2602.04813)
- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
