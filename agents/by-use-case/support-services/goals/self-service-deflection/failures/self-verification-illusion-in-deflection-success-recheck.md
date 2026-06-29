# Self-Verification Illusion in Deflection-Success Recheck

## Issue: Before Logging a Self-Service Interaction as "Successfully Deflected," a Recheck Step Re-Prompts the Same Model Against the Same Conversation Transcript Rather Than Checking Whether the Customer Actually Stopped Needing Help, So a Deflection That Silently Failed Is Still Counted as Successful

**Frequency**: Occasional

**Symptoms**
- A self-service session is logged as "deflected" the moment the customer stops responding, even though no independent signal confirms the underlying issue was actually resolved
- The deflection-success recheck step's trace shows it re-read the existing conversation transcript and the bot's own suggested-resolution text rather than checking for a subsequent re-contact, ticket creation, or account-state change
- Confirmation language ("issue resolved via self-service," "deflection successful") is nearly identical between sessions later found to be genuine resolutions and sessions where the customer simply gave up and abandoned the chat
- Sessions whose deflection-success determination is backed by a fresh re-contact check show a measurably different true-resolution rate than sessions whose determination only re-reads the existing transcript
- Customers who silently abandoned a "successfully deflected" chat re-contact through a different channel (phone, a new chat) within a short window, with the new contact logged as unrelated to the prior deflected session

**Root Cause**
Re-prompting the same model to "confirm the deflection succeeded," using only the conversation it already has in context, does not introduce an independent or more current source of evidence — the model has no privileged way to know whether the customer's underlying issue is actually gone, so its recheck mostly restates the same reasoning that produced the original suggested resolution. Genuine verification requires checking whether the customer re-contacted through any channel after the session ended, not a re-read of the bot's own prior narrative about having offered a resolution.

**Example**
```
Self-service bot suggests a troubleshooting article and the customer's chat goes quiet without an explicit "this worked" confirmation
Before logging the deflection outcome, a "confirm deflection success" step re-prompts the same bot: "Was this issue resolved through self-service?"
Recheck re-reads the existing transcript and the bot's own suggested-article text rather than checking whether the customer re-contacted through any channel afterward
Customer had actually abandoned the chat out of frustration and called support fifteen minutes later
Session is logged as "successfully deflected"; the phone contact is recorded as a new, unrelated issue rather than linked to the failed deflection
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Calibration in autonomous, tool-using agents remains notably underexplored relative to single-turn LLM calibration, and self-confirmation by the same model operating on the same prior context is not equivalent to independent verification against ground truth | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Tool-use error taxonomies for dialogue systems identify failure to verify an outcome's actual downstream effect, as distinct from verifying the immediate conversational signal, as a recurring and under-addressed error class | [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052) |
| Reflective self-checks that operate on the same evidence and the same underlying model risk reinforcing the original conclusion rather than catching genuine errors, since the model has no new information to revise its judgment with | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |

**Contributing Factors**
- Deflection-success determination is implemented as a re-prompt over existing conversation context rather than a cross-channel re-contact check
- Session-end logging records the customer's silence or chat abandonment as if it were confirmation of resolution, conflating "stopped responding" with "issue resolved"
- No distinction is tracked between "deflection confirmed via cross-channel re-contact check" and "deflection confirmed via transcript re-read alone," so both are reported identically as a successful deflection

---

## Mitigation Strategies

1. **Mandatory Cross-Channel Re-Contact Check on Recheck**: Require the deflection-success determination to check for any re-contact across all channels within a defined window before logging a session as successfully deflected
2. **Decouple Chat Silence from Resolution Confirmation**: Treat a customer going silent or abandoning the chat as distinct from confirmation that the issue was resolved; require a separate re-contact check before logging "deflection successful"
3. **Re-Contact Linkage Tracking**: Automatically link a subsequent contact on any channel to its prior "successfully deflected" session when it occurs within a defined window and describes the same symptom, surfacing recheck failures that would otherwise look like unrelated new contacts
4. **Track Recheck-Type Outcome Divergence**: Continuously measure and report the re-contact rate separately for cross-channel-checked deflections versus transcript-only-confirmed deflections; a large divergence is itself evidence that transcript-only confirmations are not functioning as verification

### Metrics
- Rate of deflection-success determinations backed by a cross-channel re-contact check versus a transcript-only re-read
- Re-contact rate within a defined window, segmented by recheck type
- Median time between a "successfully deflected" log entry and a linked re-contact describing the same symptom

### Alerts
- A session is logged as "successfully deflected" following a transcript-only recheck and a re-contact describing the same symptom occurs within the defined window → P2
- Re-contact rate for transcript-only-recheck deflections exceeds the re-contact rate for cross-channel-checked deflections by more than the defined tolerance for a rolling window → P2
- A deflection-success determination is logged with no corresponding cross-channel re-contact check → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [ToolCritic: Detecting and Correcting Tool-Use Errors in Dialogue Systems](https://arxiv.org/pdf/2510.17052)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
