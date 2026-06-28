# Healthcare

Agents assisting with diagnosis, treatment planning, and drug interaction checking face critical domain-specific failures around medical knowledge, safety, and liability.

## Goals

| Goal | Description | Patterns |
|------|-------------|----------|
| [Diagnosis Safety](goals/diagnosis-safety/) | False diagnoses, hallucinated symptoms, rare disease misses | In progress |
| [Treatment Planning](goals/treatment-planning/) | Contraindications, drug interactions, dosage errors | In progress |
| [Drug Interactions](goals/drug-interactions/) | Adverse interaction detection, allergy handling | In progress |
| [Compliance & Liability](goals/compliance-liability/) | Outdated guidelines, malpractice exposure, informed consent | In progress |

**Status**: ~45 patterns planned

## Key Challenges

1. **Knowledge Cutoff**: Medical guidance changes; outdated recommendations dangerous
2. **Symptom Complexity**: Rare disease presentations unrecognized
3. **Drug Interaction Coverage**: Incomplete drug databases
4. **Allergy/Contraindication Tracking**: State loss mid-workflow
5. **Liability Exposure**: Recommendations increase risk if they fail
