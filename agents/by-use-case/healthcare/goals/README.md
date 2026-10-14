# Healthcare AI Agent Failures by Goal: 38 Patterns, Causes, and Fixes

**Healthcare failures in AI agents are grouped here into 9 goals, each with a catalog of named failure patterns, the symptoms you will see, the root cause, and mitigations you can copy.** Start from the symptom you are debugging, pick the matching goal below, and open its failure list.

## Key Takeaways

- This use case covers 9 goals and 38 documented failure patterns.
- The largest goal is [Diagnosis Safety](diagnosis-safety/) with 10 patterns.
- Each goal page explains the failure class, how to tell it apart from its neighbors, and which mitigations apply across its patterns.
- Each failure page covers the symptoms, an example, the root cause, and how to fix it.

## Healthcare Goals

| Goal | What goes wrong | Patterns |
|---|---|---|
| [Adverse Drug Interaction](adverse-drug-interaction/) | Adverse drug interaction failures happen when an interaction-checking pipeline is scoped narrower than the patient's actual regimen | 7 |
| [Clinical Documentation](clinical-documentation/) | Clinical documentation failures happen when an agent transforms chart data into structured output — a discharge summary, an after-visit note, a billing code | 2 |
| [Compliance Liability](compliance-liability/) | Compliance and liability failures happen when an agent generates a high-stakes output — a de-identified dataset, an informed-consent summary, a consent-scope record | 3 |
| [Diagnosis Safety](diagnosis-safety/) | Diagnosis-safety failures happen when an agent's differential diagnosis or working hypothesis becomes progressively harder to revise or expand as new information arrives | 10 |
| [Lab Result Interpretation](lab-result-interpretation/) | Lab-result interpretation fails when an agent treats a tool-returned lab payload as ground truth without verifying the payload's own embedded patient identifier matches the requesting context | 3 |
| [Medication Reconciliation](medication-reconciliation/) | Medication-reconciliation failures happen when an agent matches a medication from one source (discharge instructions, home-medication list) to a formulary or reference database without grounding that match in the requesting context | 3 |
| [Mental Health Triage](mental-health-triage/) | Mental-health-triage failures happen when risk assessment relies on keyword matching for crisis language and misses indirect, euphemistic, or future-oriented expressions common in genuine risk disclosures | 2 |
| [Telehealth Triage](telehealth-triage/) | Telehealth-triage failures happen when an agent's internal reasoning correctly identifies urgency based on symptoms | 2 |
| [Treatment Planning](treatment-planning/) | Treatment-planning failures happen when a care plan is regenerated at each visit from current diagnoses alone without carrying forward previously negotiated patient-specific goals | 6 |

**Total: 38 patterns**

## Frequently Asked Questions

### Where do I start if my healthcare agent is failing?

Match the symptom to a goal in the table above, then open that goal's page for how to tell its failures apart and where to look first. Each failure page ends in mitigations you can apply directly.

### How are these healthcare failure patterns organized?

By goal: the outcome the agent is supposed to achieve. Under each goal, a `failures` folder holds one page per pattern. For the full picture see the [Healthcare overview](../).

## Related

- [Healthcare overview](../)
- [All agent failure patterns](../../../)
