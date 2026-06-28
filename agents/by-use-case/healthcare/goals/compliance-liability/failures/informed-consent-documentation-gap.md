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

1. **Transcript-Grounded Generation Only**: Require informed-consent documentation language to be generated strictly from what is verifiably present in the encounter transcript or structured consent form, never from a template default
2. **Explicit Uncertainty Flagging**: When the transcript does not clearly capture a risks/benefits/alternatives discussion, the agent should flag the gap rather than filling it with boilerplate
3. **Clinician Review and Attestation**: Require the clinician to explicitly review and attest to AI-drafted consent language before it is finalized in the chart
4. **Consent-Specific Audit Sampling**: Periodically audit a sample of AI-drafted consent documentation against the source transcript for fidelity

### Metrics
- % of AI-drafted consent notes reviewed and attested by clinician before finalization
- Discrepancy rate between transcript content and drafted consent language (audit sample)
- Informed-consent-related dispute rate

### Alerts
- Consent language drafted with no corresponding transcript evidence of detailed discussion → P1
- Clinician finalizes note without review flag cleared → P2

---

## References

- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
- [Multi-model assurance analysis showing large language models are highly vulnerable to adversarial hallucination attacks during clinical decision support](https://www.nature.com/articles/s43856-025-01021-3)
