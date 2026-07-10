# Informed-Consent Documentation Gap

## Issue: Agent Drafts or Summarizes Clinical Documentation Implying Informed Consent Was Obtained and Discussed in Detail That Was Not Actually Covered in the Encounter

**Frequency**: Occasional

**Symptoms**
- AI-generated visit note includes a detailed risks/benefits/alternatives discussion that was not actually verbalized to the patient in that level of detail
- Consent documentation auto-populated from a template regardless of what was actually discussed in the specific encounter
- Discrepancy between the patient's recollection of the conversation and the AI-drafted note's account of informed consent
- Note generated before the actual consent conversation occurs, then never reconciled afterward

**Root Cause**
Ambient documentation and note-generation agents are optimized to produce complete, well-formed clinical notes, and language models tend toward generating plausible, template-consistent content (including a full risks/benefits/alternatives discussion) even when the underlying encounter transcript or structured input does not confirm that level of detail was actually conveyed. This creates a liability gap: the chart implies a thorough informed-consent conversation occurred when the actual encounter may have been abbreviated.

**Example**
```
Scenario: Ambient AI scribe generates a procedure note for a same-day minor surgical consult
Generated note: "Risks, benefits, and alternatives discussed at length; patient verbalized understanding and consented"
Actual encounter: Brief verbal consent obtained; detailed risk discussion was abbreviated due to time pressure
Later event: Complication occurs; patient disputes having received a detailed risk discussion
Impact: Chart documentation does not match what was actually communicated, creating legal and clinical-quality exposure
```

**Key Statistics**
- Discrepancies between AI-generated documentation and the actual encounter content are a recognized emerging risk category in ambient clinical documentation deployments
- Informed-consent documentation disputes are a recurring category in malpractice claims where chart language and patient recollection diverge
- Note-generation agents that draft from templates rather than strictly from encounter transcripts show higher rates of unverified "boilerplate" content insertion in audits

---

## Mitigation Strategies

### Prevention

1. **Strict transcript-grounding for consent documentation with citation requirements**: Implement constraint that AI-generated informed-consent sections must explicitly cite corresponding transcript segments for each claim about discussion (e.g., "Risks discussed: Bleeding risk mentioned at timestamp 3:45 in encounter transcript"). Reject generation that infers consent discussions without transcript evidence. Auto-flag as "[REVIEW REQUIRED]" any consent language where >20% is interpolated without direct citation. Fail-safe: if no transcript or minimal transcript, generate "Consent obtained per documented process" without detail rather than inferring details. Root cause mitigation: Prevents template-completion bias by enforcing source grounding and citation.

2. **Mandatory clinician attestation gate before chart finalization**: Require clinician to explicitly review AI-drafted consent sections and answer: "Does this accurately reflect what was discussed in this encounter? [Yes / No / Partially]". If "No" or "Partially", require clinician to edit consent language or flag discrepancies in chart. Draft cannot be finalized without attestation checkbox. Log clinician decision. Root cause: Prevents silent insertion of unverified boilerplate by requiring active human verification.

3. **Structured consent capture form with auto-documentation**: For high-liability procedures, implement structured consent capture: clinician completes form fields ("Risks discussed: Y/N", "Alternatives presented: Y/N", "Patient questions answered: Y/N", "Level of detail: [detailed / moderate / brief]"). AI generates documentation from form fields rather than inferring from transcript. Root cause: Moves from transcript-inference to explicit clinician attestation of discussion content and depth.

### Detection & Response

1. **Transcript-fidelity audit logging**: For every consent documentation auto-generated, log: (a) transcript length (words, duration), (b) detected discussion segments (using NLP for consent keywords: "risks", "benefits", "alternatives"), (c) citation coverage (% of consent claims backed by transcript citations), (d) clinician attestation decision, (e) discrepancies flagged by clinician. Alert when citation coverage <80% or transcript length <500 words but detailed consent language generated.

2. **Consent fidelity auditing**: Monthly sampling of 50-100 AI-drafted consent notes: have independent clinician review each against source transcript and rate fidelity (0-100%, "does documented consent match actual discussion?"). Track fidelity by procedure type and documentation system version. Target: >95% fidelity. Alert on patterns of inflated consent documentation.

### Architecture Patterns

1. **Transcript-Grounded Consent Generator**: Input: (encounter_transcript, procedure_type, structured_consent_form_if_available) → Process: (1) NLP extraction of consent-related discussion segments from transcript, (2) Structured claim generation ("Risks discussed: [extracted segments]"), (3) Citation mapping (each claim tagged with transcript timestamp range), (4) Flagging of unsupported details. Output: (draft_consent_note_with_citations, [REVIEW_FLAGS]) → Clinician attestation gate → Finalized note (with or without clinician edits).

2. **Structured Consent Capture Form**: Procedure-specific form with checkboxes and fields: "Informed consent type: [full / abbreviated / emergency]", "Risks discussed: Y/N [brief description]", "Alternatives presented: Y/N [list]", "Patient understood: Y/N [evidence]". Auto-maps to clinical note template. Used as primary source for consent documentation rather than transcript inference.

3. **Consent Fidelity Audit Service**: Monthly sampling and independent clinician review. Scores fidelity (0-100), flags discrepancies, tracks trends by procedure and AI model version. Results feed back to model improvement and clinician training.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Transcript-Citation Coverage | >95% | <85% | % of consent documentation claims with direct transcript citations and timestamps |
| Clinician Attestation Compliance | 100% | <99% | % of AI-drafted consent notes with documented clinician attestation (Yes/No/Partially) before finalization |
| Consent Fidelity (Audit Sample) | >95% | <90% | % of sampled consent notes rated as faithful to actual encounter discussion (monthly audit by independent clinician) |
| Boilerplate Detection Rate | <5% | >10% | % of consent documentation flagged as containing unsupported detail or template language without transcript basis |
| Consent-Related Disputes | 0 | >0 | # of informed-consent-related patient disputes or complaints related to documentation-encounter discrepancy |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Transcript-Ungrounded Consent Language | Drafted consent documentation contains detailed discussion claims without corresponding transcript citations or transcript <500 words | CRITICAL | Flag draft as "[REVIEW REQUIRED]"; require clinician to manually review and attest or edit before finalization; cannot auto-approve |
| Clinician Attestation Gap | Consent note finalized without documented clinician attestation decision (audit shows no review checkbox recorded) | CRITICAL | Audit chart; investigate note finalization process; potential chart amendment required; escalate to compliance |
| High Fidelity Discrepancy (Audit Sample) | Independent audit rates consent note as <80% faithful to transcript (significant unsubstantiated detail or template insertion) | HIGH | Escalate to clinical leadership; investigate AI model or clinician practices; flag similar notes from same clinician/procedure for review |

---

## References

- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
