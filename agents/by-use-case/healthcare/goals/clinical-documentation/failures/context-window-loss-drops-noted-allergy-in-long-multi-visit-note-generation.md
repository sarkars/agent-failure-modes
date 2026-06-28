# Context-Window Loss Drops Noted Allergy in Long Multi-Visit Note Generation

## Issue: An Agent Drafting a Discharge Summary or Multi-Visit Progress Note That Synthesizes a Patient's Chart Across Many Prior Encounters Within a Single Long Documentation Session Correctly References an Allergy or Contraindication Noted Early in That Same Session, but as the Session Continues Through Many More Encounter Records, the Earlier Reference Falls Out of the Agent's Effective Context, and the Final Generated Note Omits It Despite the Source Record Having Been Available Earlier in the Same Session

**Frequency**: Occasional

**Symptoms**
- The final generated note's allergy or contraindication section omits an allergy that an earlier turn in the same documentation session explicitly extracted from a prior encounter record and discussed
- Asking the agent, immediately after generating the final note, "did you account for the penicillin allergy noted earlier?" produces an answer indicating no recollection of having seen it, even though it appears earlier in the same session's working context
- Re-generating the final note with the allergy explicitly re-stated in the prompt (rather than relying on it persisting from earlier in the session) correctly includes it, isolating context loss as the cause rather than the source record being unavailable
- The omission concentrates on documentation sessions synthesizing the largest number of prior encounters, where the volume of intervening encounter content is largest relative to the model's effective attention to content from early in the session
- The omission is caught only if a clinician manually cross-checks the generated note's allergy section against the full chart, since the note reads as complete and well-formatted regardless of the omission

**Root Cause**
A long documentation session that processes many prior encounter records to synthesize a discharge summary or multi-visit note accumulates enough intervening content that an earlier-extracted fact -- such as a noted allergy -- can fall outside the portion of the session the model effectively attends to by the time the final note is generated, even within nominal context-window limits. When the allergy exists only as a fact surfaced in an earlier turn's discussion of one specific prior encounter, rather than as a persistent, structured patient-safety attribute the final synthesis step explicitly re-checks, the synthesis has no reliable signal that the fact was ever established earlier in the same session.

**Example**
```
Documentation session begins by reviewing the patient's encounter from eight months ago, where the agent notes: "Patient reports penicillin allergy (hives), documented by Dr. Alvarez"
Session continues, reviewing eleven additional encounters over the next several turns to build a comprehensive discharge summary
Final turn: Agent generates the discharge summary's allergy section, listing only the allergies documented in the two most recently reviewed encounters, omitting the penicillin allergy noted earlier in the same session
Discharge summary is finalized without the penicillin allergy listed; the omission is not caught because the summary otherwise reads as complete and the allergy section is not empty
A subsequent prescribing clinician relying on the discharge summary's allergy section, rather than the full chart, is not alerted to the penicillin allergy
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Long, multi-turn conversations with LLMs show measurable degradation in maintaining earlier-established facts as conversation length grows, even within nominal context-window limits | [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120) |
| Persistent memory mechanisms for autonomous LLM agents are identified as a distinct architectural requirement precisely because relying on conversational context alone causes earlier-established facts to be dropped in long-running sessions | [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1) |
| Surveys of LLM-based agents in medicine identify longitudinal synthesis across multiple encounters as a distinct reliability challenge from single-encounter documentation accuracy | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- Allergy and contraindication facts extracted during review of an individual prior encounter exist only within that turn's discussion, with no structured, persistent patient-safety record maintained independently of session length
- Final note-synthesis step generates the allergy section from the most recently processed encounters in working context rather than from a structured, explicitly maintained cumulative list
- No automated check cross-references the generated note's allergy section against every allergy mentioned anywhere earlier in the same documentation session before the note is finalized

---

## Mitigation Strategies

1. **Structured Cumulative Safety-Attribute Ledger**: Maintain a structured, persistent record of every allergy and contraindication extracted from any encounter reviewed during the documentation session, separate from the conversational transcript, and require final note synthesis to draw from this ledger rather than from working-context recall
2. **Pre-Finalization Cross-Check Against Full Source Chart**: Before a generated note is finalized, automatically cross-check its allergy and contraindication section against every encounter record actually reviewed during the session (and against the chart's dedicated allergy list, if one exists), flagging any discrepancy
3. **Session-Length Threshold Triggers Ledger Re-Injection**: Once a documentation session processes more than a defined number of prior encounters, require the cumulative safety-attribute ledger to be explicitly re-injected into context before final note synthesis
4. **Mandatory Source-of-Truth Allergy List Cross-Reference**: Require the final note's allergy section to be generated by cross-referencing the patient's authoritative, structured allergy list (maintained outside any single documentation session) rather than solely from facts surfaced during the current session's chart review

### Metrics
- Rate of finalized notes whose allergy or contraindication section omits an allergy mentioned earlier in the same documentation session's reviewed encounters
- Rate of finalized notes whose allergy section does not match the patient's authoritative structured allergy list
- Percentage of long (above-threshold) documentation sessions with an active, explicitly maintained cumulative safety-attribute ledger

### Alerts
- A finalized note's allergy section omits an allergy present in the patient's authoritative structured allergy list → P1
- A finalized note's allergy section omits an allergy mentioned earlier in the same documentation session's reviewed encounters → P1
- A documentation session exceeds the encounter-count threshold without a safety-attribute ledger being re-injected into context → P2

---

## References

- [LLMs Get Lost In Multi-Turn Conversation](https://arxiv.org/abs/2505.06120)
- [Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers](https://arxiv.org/html/2603.07670v1)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
