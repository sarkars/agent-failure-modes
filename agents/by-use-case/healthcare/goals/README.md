# Healthcare AI Agent Failures by Goal: 38 Patterns, Causes, and Fixes

**Healthcare AI agents fail in 9 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 38 documented patterns across 9 goals; the most documented is [Diagnosis Safety](diagnosis-safety/) with 10.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Healthcare Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Adverse Drug Interaction](adverse-drug-interaction/) | When an interaction-checking pipeline is scoped narrower than the patient's actual regimen — pairwise drug-drug pairs only, structured prescriptions only | 7 |
| [Clinical Documentation](clinical-documentation/) | When an agent transforms chart data into structured output — a discharge summary, an after-visit note, a billing code | 2 |
| [Compliance Liability](compliance-liability/) | When an agent generates a high-stakes output — a de-identified dataset, an informed-consent summary, a consent-scope record | 3 |
| [Diagnosis Safety](diagnosis-safety/) | When an agent's differential diagnosis or working hypothesis becomes progressively harder to revise or expand as new information arrives | 10 |
| [Lab Result Interpretation](lab-result-interpretation/) | When an agent treats a tool-returned lab payload as ground truth without verifying the payload's own embedded patient identifier matches the requesting context | 3 |
| [Medication Reconciliation](medication-reconciliation/) | When an agent matches a medication from one source (discharge instructions, home-medication list) to a formulary or reference database without grounding that match in the requesting context | 3 |
| [Mental Health Triage](mental-health-triage/) | When risk assessment relies on keyword matching for crisis language and misses indirect, euphemistic, or future-oriented expressions common in genuine risk disclosures | 2 |
| [Telehealth Triage](telehealth-triage/) | When an agent's internal reasoning correctly identifies urgency based… | 2 |
| [Treatment Planning](treatment-planning/) | When a care plan is regenerated at each visit from current diagnoses alone without carrying forward previously negotiated patient-specific goals | 6 |

**Total: 38 patterns**

## Frequently Asked Questions

### How do you detect and fix anchoring bias in a multi-turn diagnostic conversation?

Force a fresh differential-diagnosis regeneration every 2-3 new information items, explicitly discarding prior assertions; red-flag situations where a new symptom contradicts prior reasoning, rather than rationalizing it as "consistent" with prior diagnosis; and implement a devil's-advocate reasoning pass asking "what if the leading diagnosis is wrong?" to surface competing alternatives. See [Diagnosis Safety](diagnosis-safety/).

### What causes an agent to miss a drug interaction between a patient's current medications?

Most misses trace to scope, not model capability: the interaction check queries a pairwise drug-drug database and never sees condition-based contraindications, lab-value-triggered risks, herbal/supplement interactions, or three-way-plus combinations, because the checking pipeline was built to answer a narrower question than "is this regimen safe." See [Contraindication Omission](adverse-drug-interaction/failures/contraindication-omission.md) and [Polypharmacy Cascade Failures](adverse-drug-interaction/failures/polypharmacy-cascade-failures.md). See [Adverse Drug Interaction](adverse-drug-interaction/).

### How do you preserve patient-specific care goals across multiple visits?

Store goals as persistent structured objects, separate from the per-visit problem list, and explicitly carry patient-specific goals forward into every visit's plan generation. See [Treatment Planning](treatment-planning/).

## Related

- [Healthcare overview](../)
- [All agent failure patterns](../../../)
