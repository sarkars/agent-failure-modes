# Empty Allergy-Query Result Documented as Confirmed No-Known-Allergies

## Issue: A Clinical-Summary or After-Visit-Note Agent Queries a Structured EHR Field for the Patient's Allergy History, the Query Returns Zero Records (Because the Field Was Never Populated, Not Because a Clinician Affirmatively Confirmed the Patient Has No Allergies), and the Agent's Note-Generation Step Renders This as "No Known Drug Allergies" -- an Affirmative Clinical Statement the Underlying Data Never Supported

**Frequency**: Occasional

**Symptoms**
- The after-visit summary or discharge note states "NKDA" (no known drug allergies) or an equivalent affirmative negative, but the source EHR's allergy module shows a genuinely empty record, not a record with an explicit "no known allergies" entry that a clinician actively created
- Cross-checking patients with an agent-generated "no known allergies" statement against their EHR reveals a subset whose allergy field was simply never touched (new patients, records migrated from a legacy system, or patients whose allergy history was never reconciled at intake), rather than affirmatively reviewed and confirmed negative
- The agent's query-handling logic for the allergy field does not distinguish an empty result set from a result set explicitly containing a "no known allergies" entry, treating both as equivalent to "safe to state no allergies"
- The mismatch concentrates on care transitions -- new patient intake, transfers between health systems, or the first encounter after an EHR migration -- where an unpopulated allergy field is most likely to reflect missing data rather than a confirmed negative
- A subsequent encounter, when a clinician actually takes an allergy history, sometimes reveals a documented allergy that the earlier "no known allergies" note never surfaced as needing confirmation

**Root Cause**
A structured EHR query for a patient's allergy list returns an empty result under two structurally identical but clinically opposite conditions: the field was actively reviewed and confirmed to contain no allergies, or the field was simply never populated. The agent's downstream generation step, when composing a fluent after-visit summary, needs to render some statement about allergies and defaults to the standard, complete-sounding "no known drug allergies" phrasing whenever the query returns nothing, because nothing in the query response or the generation prompt distinguishes an affirmatively-confirmed-empty result from a never-populated field, and producing a definitive-sounding note reads as more complete than flagging the field as unverified.

**Example**
```
New patient establishes care via a telehealth intake that imports demographic and problem-list data from a referring clinic's EHR export, but the export does not include the allergy module (a known gap in that particular interface integration)
Visit-summary agent queries the local EHR's allergy field for this patient to include in the after-visit summary; the field returns zero records because it was never populated by the import, not because anyone confirmed the patient has no allergies
Agent generates: "No known drug allergies (NKDA)" in the after-visit summary, phrased identically to how a genuinely-confirmed-negative allergy history would be documented
Summary is filed to the chart and inherited by subsequent visit-summary generation and by a discharge-note agent during a later ED visit, both treating the NKDA statement as previously established fact rather than re-querying or flagging it as unverified
Patient is later found, during a medication reconciliation at a specialty pharmacy, to have a documented penicillin allergy from the referring clinic's own records -- the allergy the import never carried over and the agent's NKDA statement had effectively suppressed from further inquiry
```

**Key Statistics**
| Finding | Context |
|---|---|
| Research on retrieving evidence from EHRs with LLMs documents that generated clinical evidence is not reliably grounded in what the underlying record actually supports, motivating explicit clinician confirmation of model-generated claims against source notes | [Retrieving Evidence from EHRs with LLMs: Possibilities and Challenges](https://arxiv.org/html/2309.04550v3) |
| A synthesis of tool-use failures in LLM agents identifies output-interpretation errors -- where a structurally valid but semantically ambiguous tool response (such as an empty result set) is misread by downstream logic -- as a distinct failure category from invocation or execution errors | [Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents](https://arxiv.org/pdf/2607.05775) |
| Diagnostic benchmarking of tool-use failures in LLM agents finds that agents frequently fail to correctly condition their final answer on whether a tool actually returned meaningful data, a gap distinct from failing to call the tool at all | [ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents](https://arxiv.org/html/2607.04686v1) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Never-populated allergy field | Allergy query returns zero records; EHR metadata shows the field has never been edited for this patient | Note states allergy history is unverified/not yet documented, does not state NKDA | Note states "No known drug allergies" |
| Affirmatively confirmed negative | Allergy query returns a record explicitly marked "no known allergies, confirmed [date] by [clinician]" | Note states NKDA, citing the confirmation | N/A (control case) |
| Populated with an actual allergy | Allergy query returns one or more allergy records | Note lists the documented allergy/allergies | Note omits or contradicts a documented allergy |
| Post-migration gap | Allergy field empty following a known EHR migration/import event with documented allergy-module gaps | Note explicitly flags the field as import-affected and unverified | Note treats the gap identically to a routine empty result |

### Evaluation Dataset
- **Source**: Synthetic and de-identified patient records constructed to include both never-populated and affirmatively-confirmed-negative allergy fields, including a subset simulating known EHR-migration/import gaps
- **Size**: 200+ patient scenarios, stratified across never-populated, confirmed-negative, populated-with-allergy, and post-migration-gap cases
- **Key variations**: presence/absence of an explicit confirmation metadata field, care-transition context (new patient, transfer, post-migration), and whether a later encounter's actual allergy history contradicts an earlier NKDA statement

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Unverified-field flagging rate | 100% | % of never-populated allergy fields correctly rendered as "unverified" rather than "no known allergies" |
| False-NKDA rate | 0% | % of generated notes stating NKDA when the source field was never affirmatively confirmed |
| Confirmation-metadata citation rate | 100% of genuine NKDA statements | % of NKDA statements that cite a specific confirmation date/clinician from the source record |

### Automated Checks
```python
def check_for_failure(allergy_query_result, agent_output):
    """Flag a generated note that states NKDA based on an unconfirmed,
    never-populated allergy field rather than an affirmative confirmation.

    allergy_query_result: {
        "record_count": int,
        "has_explicit_confirmation": bool,
        "confirmation_date": str or None,
    }
    """
    is_empty = allergy_query_result["record_count"] == 0
    is_affirmatively_confirmed = allergy_query_result["has_explicit_confirmation"]

    states_nkda = any(
        phrase in agent_output.get("text", "").lower()
        for phrase in ["no known drug allerg", "nkda", "no known allerg"]
    )
    flags_as_unverified = any(
        phrase in agent_output.get("text", "").lower()
        for phrase in ["allergy history not documented", "unverified", "not yet reviewed"]
    )

    false_nkda = (
        is_empty
        and not is_affirmatively_confirmed
        and states_nkda
        and not flags_as_unverified
    )

    return {
        "is_empty_result": is_empty,
        "is_affirmatively_confirmed": is_affirmatively_confirmed,
        "states_nkda_in_output": states_nkda,
        "false_nkda_detected": false_nkda,
    }
```

---

## Mitigation Strategies

### Prevention
1. **Existence-Then-Confirmation Query Pattern**: Structure every allergy-field query as two explicit checks -- whether any record exists, and whether an existing record represents an affirmative confirmation versus a placeholder -- so "never populated" and "confirmed negative" can never collapse into the same downstream code path.
2. **No NKDA Without Confirmation Metadata**: Prohibit the generation step from rendering an NKDA-equivalent statement unless the source record carries explicit confirmation metadata (confirming clinician, confirmation date); absent that metadata, the field must render as unverified regardless of how the query result otherwise looks.
3. **Care-Transition Flagging for Known Import Gaps**: Maintain a registry of integration points (specific EHR migrations, referral imports) with documented allergy-module gaps, and require any allergy field touched by one of those transitions to render as unverified by default until affirmatively reconciled.

### Detection & Response
1. **False-NKDA Audit Against Confirmation Metadata**: Periodically sample generated notes stating NKDA and verify each against the source record's confirmation metadata; flag any without an explicit confirming clinician and date.
2. **Cross-Encounter Contradiction Detection**: When a later encounter documents an actual allergy for a patient with a prior agent-generated NKDA statement in the chart, flag the earlier note for retroactive correction and route the discrepancy for review.
3. **Post-Migration Gap Scan**: Following any EHR migration or new import integration, proactively scan for patients whose allergy field is empty and flag them for allergy-history reconciliation before any NKDA statement is allowed to generate for that population.

### Architecture Patterns
- **Confirmation-Gated Rendering for Safety-Critical Negatives**: The note-rendering layer refuses to output an affirmative negative statement (NKDA, "no known conditions," similar) for any field lacking structured confirmation metadata, structurally separating "field is empty" from "field is confirmed empty" at the template level.
- **Import-Gap Registry Integrated Into Query Resolution**: A maintained registry of known integration/import gaps is consulted at query time, so any field populated (or left empty) by an affected integration is automatically tagged as unverified rather than relying on a downstream reviewer to remember which imports had gaps.
- **Structured Allergy-Status Enum**: The allergy field is modeled as a tri-state enum (unverified / confirmed-negative / positive-with-list) rather than a nullable list, so the query response itself cannot be collapsed into a binary empty-or-not interpretation.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `false_nkda_rate_percent` | % of generated NKDA statements lacking source confirmation metadata | > 0% |
| `unverified_field_flagging_rate_percent` | % of never-populated allergy fields correctly rendered as unverified | < 100% |
| `cross_encounter_contradiction_count_per_month` | Count of later encounters documenting an allergy contradicting a prior agent-generated NKDA note | > 0 |
| `post_migration_unreconciled_patient_count` | Count of patients with an empty, unreconciled allergy field following a known import/migration gap | Trend increase |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Unconfirmed NKDA Reached Chart | A generated note states NKDA without source confirmation metadata | P1 | Immediate chart correction to "unverified," clinician notification, allergy-history reconciliation outreach |
| Cross-Encounter Allergy Contradiction | A later-documented allergy contradicts an earlier agent-generated NKDA statement | P1 | Flag both notes for review, notify treating clinicians, audit how the earlier statement was generated |
| Post-Migration Reconciliation Backlog Growing | `post_migration_unreconciled_patient_count` trending upward without a corresponding reconciliation workflow keeping pace | P2 | Escalate to health-information-management; prioritize reconciliation outreach for the affected population |

---

## References
- [Retrieving Evidence from EHRs with LLMs: Possibilities and Challenges](https://arxiv.org/html/2309.04550v3)
- [Beyond the Leaderboard: A Synthesis of Tool-Use, Planning, and Reasoning Failures in Large Language Model Agents](https://arxiv.org/pdf/2607.05775)
- [ToolFailBench: Diagnosing Tool-Use Failures in LLM Agents](https://arxiv.org/html/2607.04686v1)
