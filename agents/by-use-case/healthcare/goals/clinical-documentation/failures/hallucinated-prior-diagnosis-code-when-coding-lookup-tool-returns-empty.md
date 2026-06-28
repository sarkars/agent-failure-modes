# Hallucinated Prior Diagnosis Code When Coding Lookup Tool Returns Empty

## Issue: An Agent Drafting a Progress Note or Billing Summary That Calls a Diagnosis-Code Lookup Tool to Confirm a Patient's Active ICD-10 Codes Receives an Empty or Partial Result Because the Coding System Timed Out or Returned No Match, and Instead of Treating the Empty Result as a Hard Stop, the Agent Completes the Note With a Plausible-Sounding Diagnosis Code Inferred From the Visit's Narrative Text

**Frequency**: Occasional

**Symptoms**
- The generated note lists an ICD-10 code in the assessment section that does not appear anywhere in the patient's actual problem list or prior coding history
- The fabricated code is topically plausible -- it matches the chief complaint described in the visit narrative -- but does not match the code the coding lookup tool would have returned had it succeeded
- Querying the coding lookup tool directly, immediately after note generation, for the same patient and encounter returns either no result or a different code than what the agent wrote into the note
- The note contains no indication that the coding lookup call failed, timed out, or returned an empty result; the assessment section reads as a confident, fully resolved entry
- The error surfaces only when a downstream biller or auditor cross-references the note's code against the practice management system and finds a mismatch or an unbillable code

**Root Cause**
When a tool call to the coding lookup system returns an empty, malformed, or timed-out response mid-generation, the agent has no explicit instruction to treat that as a blocking failure distinct from "no prior code exists." Because the note-generation task still requires a code to complete the assessment section, the model falls back on its general medical-language training to produce a code that is narratively consistent with the visit, rather than surfacing the tool failure to a human coder for manual resolution.

**Example**
```
Agent drafts a progress note for a follow-up visit, narrative describes "worsening shortness of breath, suspect COPD exacerbation"
Agent calls coding-lookup-tool(patient_id, encounter_id) to confirm the patient's active COPD-related ICD-10 code
Tool call times out after 8 seconds, returns an empty payload with no error flag surfaced to the generation step
Agent's assessment section is written as: "J44.1 - COPD with acute exacerbation" -- a code that reads as clinically appropriate but was never confirmed by the lookup tool
Patient's actual active code in the practice management system is J44.0 (COPD with acute lower respiratory infection), a clinically distinct and differently reimbursed code
Billing submission using the note's fabricated code is later denied on coding-mismatch review
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to complete plausible-sounding values when an expected tool response is missing or incomplete, rather than treating the gap as a blocking error | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Tool-use agents show measurable miscalibration between their stated confidence and the actual reliability of a completed tool call, especially when the underlying call partially or silently fails | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Surveys of LLM-based agents in medicine identify reliance on tool-confirmed structured data, rather than narrative inference, as a distinct safety requirement for documentation tasks | [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1) |

**Contributing Factors**
- The note-generation workflow has no explicit "tool call failed" state that is distinguishable from "tool call succeeded with a null result"
- The model treats completing the assessment section as a harder constraint than verifying the code's provenance, so an empty tool response does not block generation
- No automated check compares the code written into the final note against the most recent successful coding-lookup response before the note is finalized

---

## Mitigation Strategies

1. **Explicit Tool-Failure State Distinct From Empty Result**: Require the coding lookup tool to return a distinguishable failure signal (timeout, malformed response) separate from a genuine "no active code" result, and block note finalization on the former
2. **Hard Stop on Unconfirmed Diagnosis Codes**: Prohibit the note-generation step from writing any diagnosis code into the assessment section unless that exact code was returned by a successful coding-lookup call in the same session
3. **Mandatory Human Coder Review on Lookup Failure**: Route any encounter where the coding lookup call failed or timed out to a human coder for manual code assignment before the note is finalized
4. **Post-Generation Code Provenance Check**: Before finalizing any note, automatically verify that every diagnosis code present in the note text matches a code returned by a logged, successful tool call, flagging any code without that provenance

### Metrics
- Rate of finalized notes containing a diagnosis code with no matching successful coding-lookup tool call in the session log
- Rate of coding-lookup tool calls that return empty, timed-out, or malformed responses
- Rate of billing denials attributable to a code mismatch between the note and the practice management system

### Alerts
- A finalized note contains a diagnosis code with no corresponding successful tool-call record → P1
- The coding-lookup tool's empty/timeout rate exceeds the defined threshold for a rolling window → P2
- A note is finalized despite a logged coding-lookup tool failure for that encounter → P1

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
