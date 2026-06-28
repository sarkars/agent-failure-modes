# Hallucinated Risk Assessment Score When Screening Tool Submission Fails Silently

## Issue: An Agent Conducting a Mental Health Triage Chat That Submits a Structured Screening Instrument (Such as a PHQ-9 or C-SSRS) to a Scoring Service Receives a Failed or Silently Empty Response Because the Submission Was Malformed or the Service Timed Out, and Instead of Treating the Missing Score as a Hard Stop, Completes the Triage With a Plausible Score Inferred From the Conversation Rather Than the Actual Instrument

**Frequency**: Rare

**Symptoms**
- The triage summary reports a specific numeric PHQ-9 or C-SSRS score, but the scoring service's logs show no successful scoring call completed for that session
- The reported score is plausible given the tone of the conversation but does not match the score that would result from correctly tallying the patient's actual item-by-item responses
- Re-submitting the exact same item responses to the scoring service, when it is functioning, produces a different score than what the agent reported
- The triage output gives no indication that the score was inferred rather than calculated, presenting the inferred number with the same confidence as a correctly scored instrument
- The discrepancy surfaces only when a clinician manually re-scores the recorded item responses against the reported summary score and finds they do not reconcile

**Root Cause**
When the structured scoring service fails to return a result -- due to a malformed submission, timeout, or partial outage -- the triage workflow still requires a risk score to route the patient to the correct level of care, and the agent has no instruction distinguishing "scoring service unavailable" from "score is zero" or "score should be estimated." Lacking that distinction, the model produces a number consistent with the qualitative tone of the conversation rather than escalating the missing score as a blocking failure requiring either a retry or human scoring.

**Example**
```
Patient completes a C-SSRS screening conversation with responses indicating passive ideation but no active plan or intent
Triage agent submits the item-by-item responses to the scoring service to compute the standardized risk tier
Scoring service call times out and returns no result; the failure is not surfaced as a distinct error state in the triage workflow
Triage agent's summary reports: "C-SSRS risk tier: low," a plausible-sounding tier given the conversation's tone
Actual item responses, when correctly scored, place the patient in a moderate-risk tier requiring same-day clinical follow-up rather than routine scheduling
Patient is routed to routine scheduling based on the fabricated low-risk tier
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to complete plausible-sounding values when an expected tool or service response is missing or incomplete, rather than treating the gap as a blocking error | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use agents show measurable miscalibration between expressed confidence and actual correctness when an underlying tool call partially or silently fails | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Surveys of LLM-based agents in medicine identify reliance on tool-confirmed structured scoring, rather than narrative inference, as a distinct safety requirement for triage tasks | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- The triage workflow has no explicit "scoring service failed" state distinguishable from "scoring completed with a low result"
- The agent treats producing a routable risk tier as a harder constraint than verifying the tier came from a successful scoring call
- No automated check compares the risk tier in the final triage summary against a logged successful scoring-service response before the summary is used for routing

---

## Mitigation Strategies

1. **Hard Stop on Unconfirmed Risk Scores**: Prohibit the triage summary from reporting any standardized risk tier unless that exact tier was returned by a successful, logged scoring-service call for the same session
2. **Distinguishable Failure State for Scoring Service**: Require the scoring service to return an explicit failure signal, distinct from a genuine low score, on timeout or malformed submission, and route that failure to immediate retry or human scoring rather than silent fallback
3. **Default-to-Highest-Acuity on Scoring Failure**: When the scoring service fails and cannot be retried before a routing decision is needed, default the patient to the highest applicable acuity tier pending manual scoring, rather than inferring a lower tier
4. **Post-Session Score Provenance Audit**: Automatically verify, for every completed triage session, that the reported risk tier matches a logged successful scoring-service call, flagging any session where it does not

### Metrics
- Rate of finalized triage summaries reporting a risk tier with no matching successful scoring-service call in the session log
- Rate of scoring-service calls that fail, time out, or return malformed responses
- Rate of risk-tier mismatches found when manually re-scoring item responses against reported summary scores in audit samples

### Alerts
- A finalized triage summary reports a risk tier with no corresponding successful scoring-service call → P1
- A patient is routed to a lower-acuity pathway despite a logged scoring-service failure for that session → P1
- Scoring-service failure rate exceeds the defined threshold for a rolling window → P2

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
