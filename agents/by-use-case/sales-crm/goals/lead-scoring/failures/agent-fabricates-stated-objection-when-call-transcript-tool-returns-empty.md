# Agent Fabricates a Stated Objection When the Call-Transcript Tool Returns Empty

## Issue: A Lead-Scoring Agent Asked to Factor In a Prospect's Most Recent Discovery-Call Sentiment Calls the Call-Transcript Retrieval Tool, Receives an Empty or Null Result Because the Call Was Never Transcribed or the Transcript Has Not Yet Synced, and Instead of Reporting That No Transcript Data Is Available, Fills the Gap With a Plausible-Sounding but Entirely Fabricated Summary of Objections and Sentiment That Lowers the Lead's Score

**Frequency**: Occasional

**Symptoms**
- The agent's scoring rationale references a specific objection ("prospect raised concerns about implementation timeline") for a call that was never transcribed, has no transcript row in the call-intelligence system, or returned an empty payload from the transcript tool
- Querying the call-transcript tool directly for the same call ID returns null, an empty array, or a "transcript not yet available" status, with no content matching what the agent's rationale describes
- The fabricated objection is plausible and stylistically consistent with real discovery-call objections seen on similar deals, making it difficult to distinguish from a genuine summary without checking the source
- The lead's score is measurably lower than it would be without the fabricated objection, and the score change correlates with a tool call that returned no usable content rather than with any verified call content
- Sales reps who reference the agent's stated objection when following up with the prospect find the prospect has no memory of raising that concern, since it was never actually said

**Example**
```
Lead-scoring agent is asked to update an account's score after yesterday's discovery call
Agent calls the call-transcript tool with the call ID; the call was recorded but the
transcription pipeline has a known 24-hour sync lag, so the tool returns an empty result
Rather than reporting "no transcript available yet, scoring based on firmographic data only,"
the agent's output states: "Prospect expressed hesitation about Q3 implementation timeline
and budget approval cycle, lowering deal-readiness score from 82 to 61"
Sales rep reviews the score change, sees the stated objection, and opens the follow-up
email referencing a timeline concern the prospect never actually raised
Engineering later confirms the transcript for that call did not sync until the next day,
and its actual content makes no mention of timeline or budget concerns
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Survey work on agent hallucination finds that when no suitable grounding content is retrievable for a step, any output the agent produces for that step is likely to be irrelevant or fabricated rather than withheld, since the agent lacks built-in awareness that the task is unsolvable without that data | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Hallucination-detection research distinguishes context-grounded outputs from those produced under missing or insufficient context, finding agents default to fluent, unflagged fabrication rather than an explicit "insufficient data" response when grounding content is absent | [HalluciNot: Hallucination Detection Through Context and Common Knowledge Verification](https://arxiv.org/pdf/2504.07069) |
| General agent failure taxonomies identify ungrounded fabrication on missing tool output as a distinct failure mechanism separate from incorrect reasoning over present data | [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933) |

**Contributing Factors**
- The agent's prompt instructs it to produce a sentiment-adjusted score for every scored call but does not include an explicit instruction or fallback path for what to output when the transcript tool returns empty or null
- The call-transcript tool's empty response is not distinguished, at the schema level, from "transcript exists but contains no notable objections" versus "transcript does not exist yet," so the agent cannot tell the two apart
- No check compares the agent's cited objections against the actual retrieved transcript content before the score change and rationale are published to the rep-facing view
- The transcription pipeline's known sync lag is not surfaced to the scoring agent as a structured "data not yet available" signal it could act on

---

## Mitigation Strategies

1. **Explicit Null-Handling Instruction**: Require the agent's prompt to include a mandatory fallback for empty or null tool results -- e.g., "if the transcript tool returns no content, state that no transcript is available and score using firmographic data only" -- rather than leaving the no-data case unspecified
2. **Grounding-Citation Enforcement**: Require every stated objection or sentiment claim in the scoring rationale to be paired with a verifiable quote or excerpt from the retrieved transcript; reject rationale text that cannot be matched to actual tool output
3. **Sync-Lag Status Signal**: Surface the transcription pipeline's known sync-lag state as a structured flag the agent must check and report, rather than letting an empty tool response be ambiguous between "no data yet" and "no objections found"
4. **Automated Post-Hoc Grounding Audit**: Run a periodic automated check that samples published scoring rationales and verifies each cited objection or sentiment claim exists in the corresponding transcript record, flagging any rationale with no matching source content

### Metrics
- Rate of scoring rationales citing call content for calls where the transcript tool returned empty, null, or not-yet-available
- Number of rep-escalated cases where a stated objection has no corresponding content in the actual transcript
- Average transcription sync lag at the time scoring runs, and correlation with fabricated-objection rate

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Fabrication on empty transcript | Scoring rationale cites specific call content while the transcript tool's response for that call ID was empty or null | P1 | Roll back the score change; re-score using firmographic data only; notify sales-ops |
| Unmatched citation | Post-hoc grounding audit finds a cited objection or sentiment claim with no matching text in the actual transcript | P2 | Flag rationale for manual review; suppress from rep-facing view pending correction |
| Sync-lag scoring run | Scoring agent runs against a call ID still inside the known transcription sync-lag window | P3 | Defer sentiment-based scoring for that call until transcript sync completes |

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [HalluciNot: Hallucination Detection Through Context and Common Knowledge Verification](https://arxiv.org/pdf/2504.07069)
- [Failure Modes in LLM Systems](https://arxiv.org/abs/2511.19933)
