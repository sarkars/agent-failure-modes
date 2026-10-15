# Healthcare Agents: Business Goals, Failure Patterns, and Fixes

**Healthcare Agents fail along 9 goals: Diagnosis Safety, Adverse Drug Interaction, Treatment Planning carry the most documented failures.** This page maps each goal to the failures that threaten it, so you can decide what to protect first and where the fixes are.

## Key Takeaways

- 38 documented failure patterns across 9 goals. What it does: support diagnosis, treatment planning, medication safety, documentation, and triage.
- The most documented goal is [Diagnosis Safety](../by-use-case/healthcare/goals/diagnosis-safety/) with 10 patterns.
- Frequencies below are as recorded on each pattern page. They are not measured rates.
- Business-goal definitions (metric, baseline, owner, what counts as a failure) are not written yet for this agent. Define them before choosing which patterns to prioritize.

## Goals this agent must protect

| Goal | When it fails | Patterns |
|---|---|---|
| [Diagnosis Safety](../by-use-case/healthcare/goals/diagnosis-safety/) | When an agent's differential diagnosis or working hypothesis becomes progressively harder to revise or expand as new information arrives | 10 |
| [Adverse Drug Interaction](../by-use-case/healthcare/goals/adverse-drug-interaction/) | When an interaction-checking pipeline is scoped narrower than the patient's actual regimen | 7 |
| [Treatment Planning](../by-use-case/healthcare/goals/treatment-planning/) | When a care plan is regenerated at each visit from current diagnoses alone without carrying forward previously negotiated patient-specific goals | 6 |
| [Compliance Liability](../by-use-case/healthcare/goals/compliance-liability/) | When an agent generates a high-stakes output — a de-identified dataset | 3 |
| [Lab Result Interpretation](../by-use-case/healthcare/goals/lab-result-interpretation/) | When an agent treats a tool-returned lab payload as ground truth without verifying the payload's own embedded patient identifier matches the requesting context | 3 |
| [Medication Reconciliation](../by-use-case/healthcare/goals/medication-reconciliation/) | When an agent matches a medication from one source | 3 |
| [Clinical Documentation](../by-use-case/healthcare/goals/clinical-documentation/) | When an agent transforms chart data into structured output — a discharge summary | 2 |
| [Mental Health Triage](../by-use-case/healthcare/goals/mental-health-triage/) | When risk assessment relies on keyword matching for crisis language and misses indirect | 2 |
| [Telehealth Triage](../by-use-case/healthcare/goals/telehealth-triage/) | When an agent's internal reasoning correctly identifies urgency based on symptoms | 2 |

## Failures most often recorded

| Failure | What goes wrong | Recorded frequency |
|---|---|---|
| [Age Bias in Symptom Interpretation](../by-use-case/healthcare/goals/diagnosis-safety/failures/age-bias-in-symptoms.md) | Model Misinterprets Symptoms Differently Based on Patient Age; Younger Patients Undertreated, Older Patients Overtreated | Very Common |
| [Anchoring Bias on First Diagnosis](../by-use-case/healthcare/goals/diagnosis-safety/failures/anchoring-bias-first-diagnosis.md) | Agent Fixates on the First Plausible Diagnosis Suggested Early in the Conversation and Discounts Later Contradictory Evidence | Very Common |
| [Demographic Bias in Diagnosis & Treatment Recommendations](../by-use-case/healthcare/goals/diagnosis-safety/failures/demographic-bias.md) | Model Biased Toward/Against Certain Demographics (Race, Gender, Age); Different Accuracy for Different Groups | Very Common |
| [Discharge Medication Reconciliation Gap](../by-use-case/healthcare/goals/medication-reconciliation/failures/discharge-medication-reconciliation-gap.md) | Agent Generates Discharge Medication List Without Reconciling Against Pre-Admission Home Medications | Very Common |
| [Dosage Renal/Hepatic Adjustment Failure](../by-use-case/healthcare/goals/adverse-drug-interaction/failures/dosage-renal-hepatic-adjustment-failure.md) | Agent Recommends Standard Adult Dosing Without Adjusting for Impaired Renal or Hepatic Clearance | Very Common |
| [Symptom Attribution Bias (Wrong Diagnosis Due to Anchoring)](../by-use-case/healthcare/goals/diagnosis-safety/failures/symptom-attribution-bias.md) | Model Anchors on Initial Symptom; Misses True Diagnosis Because Anchored to Wrong Hypothesis | Very Common |

## Before you build: define each goal

For every goal in the table, write down: the metric and how you measure its baseline today; the person who owns it; what counts as a failure and how severe it is; who is told when it happens; and when a person takes over. Then use the failures above as your test list.

## Human-side failures

Because this agent talks to customers or patients, also check conversation-level failures: tone, handoff to a person, refusals, and choosing the wrong channel. See the [human-machine interface section](../by-capability/human-machine-interface/).

## Security and governance

Every agent also needs the cross-cutting checks in [security](../cross-cutting/security/), [accuracy](../cross-cutting/accuracy/), [governance](../cross-cutting/governance/), and [operations](../cross-cutting/operations/).

## Frequently Asked Questions

### What fails most often in healthcare agents?

The most documented goal is Diagnosis Safety (10 patterns). The failures table above lists the ones recorded as most frequent. These are the library's records, not measured rates.

### Where should I start when building healthcare agents?

Define your business goals and what counts as failure, then test against the failure patterns for each goal. The section above lists what to write down.

## Related

- [All agents by business goal](./)
