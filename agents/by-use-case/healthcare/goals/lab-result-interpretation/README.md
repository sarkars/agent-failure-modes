# What Are the Most Common Lab-Result Interpretation Failures in AI Agents?

**Lab-result interpretation fails when an agent treats a tool-returned lab payload as ground truth without verifying the payload's own embedded patient identifier matches the requesting context, or when it looks up a reference range by semantic similarity over assay names instead of by exact assay code, or when a critical value is embedded only in a routine note rather than triggering an immediate, separately-routed alert.** Critical values are especially high-stakes: a potassium or glucose value outside the safe range carries an implicit time-sensitive notification requirement, and an agent that summarizes it within a note without a separate critical-value gate silently introduces a delay that can be clinically catastrophic.

## Scope

The 3 lab-result-interpretation patterns divide into distinct failure mechanisms: patient-identity verification (a data-integrity problem at the tool layer), reference-range retrieval (a similarity-search mismatch problem), and alert routing (an architecture problem where critical-value processing is not prioritized). Each is independently addressable but together they represent the most common failure points in a lab-interpretation pipeline.

## When Lab-Result Interpretation Matters

- Lab interpretations that feed into medication dosing, treatment escalation, or admission decisions, where an error reaches a patient quickly
- Duplicate or merged medical-record numbers in the upstream EHR, where a tool-returned payload could belong to a different patient despite matching on a fuzzy identifier
- Telehealth or remote-monitoring settings where vital-sign or lab results are the only objective data available for triage

## Cross-Pattern Insight

All three lab-result-interpretation patterns share a common root: an agent consumes tool-returned data or reference data without an explicit verification step confirming the data belongs to the expected patient or matches the expected standard. Lab values are safety-critical — a wrong value can drive a medication dose or admission decision within minutes — and the cost of silent error is high. The recurring mitigation is verification: match the tool's response's patient ID against the request before interpretation; verify reference ranges by exact assay code before applying any interpretation; and route critical values through a separate, latency-sensitive alert path independent of routine documentation.

## Frequently Asked Questions

### How do you catch wrong-patient lab values in a EHR retrieval?
Implement a mandatory identity cross-check gate before interpretation: compare the retrieved payload's embedded patient identifier against the requesting context's canonical ID; block interpretation on mismatch or missing ID field. Treat the tool's response as data, not automatically as ground truth for the requested patient.

### Can similarity-search reference-range lookup work in practice?
Only as a fallback with explicit flagging. Exact assay-code matching must be primary; similarity search is used only when no exact code match exists, and that fallback must be visible in the output so reviewers can prioritize verification. Assay families with closely related variants (vitamin D metabolites, hormone subtypes) should be flagged for mandatory verification regardless.

### How should critical-value notification be separated from routine documentation?
Critical values carry regulatory and protocol-mandated time windows (callback within 30 minutes, per accreditation standards). Embedding a critical value in a routine note introduces latency — a clinician may not read the full note for hours. A separate critical-value gate ensures the value is processed and routed immediately, independent of documentation timelines.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Critical Value Notification Delay](failures/critical-value-notification-delay.md) | Critical lab result summarized within routine note, not routed through separate immediate-alert channel |
| [Embedding Retrieval Matches Similarly Named Lab Panel With Different Reference Range](failures/embedding-retrieval-matches-similarly-named-lab-panel-with-different-reference-range.md) | Similarity search retrieves reference range for a name-adjacent but clinically distinct assay variant |
| [Patient-Identity Mismatch in Tool-Retrieved Lab Payload](failures/patient-identity-mismatch-in-tool-retrieved-lab-payload-accepted-without-verification.md) | Retrieved lab payload belongs to a different patient due to upstream duplicate MRN; agent interprets without verifying identity |

**Total: 3 patterns**

## Related Goals

- [Diagnosis Safety](../diagnosis-safety/) — lab values feed diagnostic reasoning; a wrong lab value cascades into wrong diagnoses
- [Adverse Drug Interaction](../adverse-drug-interaction/) — lab values (eGFR, creatinine, liver function) drive dosage adjustment and interaction risk stratification
