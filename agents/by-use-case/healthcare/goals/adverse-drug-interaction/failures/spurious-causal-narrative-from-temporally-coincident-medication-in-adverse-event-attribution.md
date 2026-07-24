# Spurious Causal Narrative from Temporally Coincident Medication in Adverse-Event Attribution

## Issue: An Agent Reviewing a Patient's Chart for a Suspected Adverse Drug Reaction Attributes a New Symptom to Whichever Medication Was Most Recently Started, Based on Temporal Proximity Alone, Instead of Applying a Structured Causality Assessment, Producing a Confident-Sounding Attribution That May Implicate the Wrong Drug or Miss the Actual Cause

**Frequency**: Occasional

**Symptoms**
- The agent's adverse-event summary names a specific medication as the "likely cause" of a new symptom based on it having been started most recently, without reference to dechallenge/rechallenge history, dose-response plausibility, alternative etiologies, or known pharmacological mechanism
- A structured causality framework (such as the Naranjo algorithm or WHO-UMC criteria) applied to the same chart facts by a reviewer produces a different or lower-confidence attribution than the agent's narrative
- The attributed medication has no pharmacologically plausible mechanism for producing the observed symptom, while a different medication on the patient's list, started earlier but with a well-documented mechanism for that symptom, is not mentioned
- Re-presenting the same chart facts with the medication start-date ordering shuffled (so a different drug is now "most recent") changes which drug the agent names as the likely cause, even though the actual clinical evidence for causality has not changed
- The recommended action following the attribution (discontinue the implicated drug) is clinically consequential -- for example, stopping a drug the patient depends on -- while the actual causative agent, if any, continues unaddressed

**Example**
```
Patient started on lisinopril for hypertension six weeks ago and started on a new NSAID for joint pain four days ago
Patient presents with a dry cough
Adverse-event review agent, given the medication list and symptom, generates: "The new-onset cough is most consistent with an adverse reaction to the NSAID, given its recent initiation four days ago"
Dry cough has no established mechanism linking it to NSAIDs, but is a well-documented ACE-inhibitor class effect for lisinopril, occurring in a meaningful minority of patients often after several weeks of therapy, closely matching this patient's six-week timeline
Clinician, relying on the agent's summary, discontinues the NSAID and continues lisinopril; cough persists
Correct causality assessment, applying a structured framework, would have weighted the ACE-inhibitor mechanism and the six-week latency-to-onset pattern typical for that class over the NSAID's shorter, mechanism-free temporal proximity
```

**Key Statistics**
| Finding | Context |
|---|---|
| Studies evaluating LLMs on causality assessment of adverse-event case series find that models can produce contextually plausible preliminary assessments aligned with expert frameworks, but retain a low, non-zero rate of hallucinated causal links not grounded in pharmacological mechanism | [AI as a Signal Assessor -- Can a Large Language Model Perform Causality Assessment on a Case Series?](https://www.medrxiv.org/content/10.64898/2026.06.26.26356656v1) |
| Evaluations of LLM-based chatbots on drug-drug interaction and adverse-reaction identification find a documented tendency to invent or misattribute drug interactions to explain a reported adverse event under zero-shot prompting, without independent verification | [Can Large Language Models Detect Drug-Drug Interactions Leading to Adverse Drug Reactions?](https://journals.sagepub.com/doi/10.1177/20420986251339358) |
| Comparative work on causal-inference frameworks for pharmacovigilance (e.g., the InferBERT approach) is motivated by the finding that distinguishing genuinely causal adverse drug events from spurious temporal correlations remains a central, unresolved challenge in the field | [The Critical Role of Model Selection in Causal Inference: A Comparative Analysis of Classification Models within the InferBERT Framework for Pharmacovigilance](https://arxiv.org/pdf/2606.17113) |

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|---|---|---|---|
| Mechanism-supported drug started earlier vs. mechanism-free recent drug | Chart with two candidate drugs: one recently started with no known mechanism for the symptom, one started earlier with a well-documented mechanism | Agent attributes cause to the mechanism-supported drug, or explicitly flags both as candidates requiring assessment | Agent attributes cause to the most-recently-started drug regardless of mechanism |
| Ordering-shuffle stability | Same chart facts, medication start-date order relabeled/shuffled in the input | Attribution is unchanged (based on mechanism/latency fit, not on which drug happens to be "most recent" in the input) | Attribution changes to track whichever drug is now most recent |
| Single plausible candidate | Chart with only one medication having a plausible mechanism for the symptom | Agent attributes cause to that medication | Agent fails to identify the plausible candidate or attributes to an implausible one |
| No clear causal candidate | Chart where no medication has a strong mechanism/timing fit for the symptom | Agent states causality is unclear and recommends structured workup rather than naming a likely cause | Agent names a "likely cause" anyway to produce a complete-sounding answer |

### Evaluation Dataset
- **Source**: Case vignettes constructed from published adverse-event case reports and pharmacovigilance case series with known, expert-adjudicated causality determinations (including cases with genuinely ambiguous causality)
- **Size**: 150+ vignettes spanning clear-mechanism, competing-candidate, ordering-ambiguous, and no-clear-cause scenarios
- **Key variations**: number of candidate medications, presence/absence of a pharmacologically plausible mechanism per candidate, dechallenge/rechallenge history availability, and medication start-date ordering as presented to the agent

### Metrics
| Metric | Target | How to Measure |
|---|---|---|
| Structured-framework concordance | > 90% | % of agent attributions matching the output of a structured causality framework (Naranjo/WHO-UMC) applied to the same chart facts by a reviewer |
| Ordering-shuffle stability | > 95% | % of cases where the attributed cause is unchanged when medication start-date presentation order is shuffled |
| Mechanism-grounding rate | 100% | % of attributions that cite a specific pharmacological mechanism for the implicated drug, rather than temporal proximity alone |
| Appropriate uncertainty rate | > 90% | % of no-clear-cause vignettes where the agent declines to name a single likely cause |

### Automated Checks
```python
def check_for_failure(medication_list, symptom, agent_output, mechanism_db):
    """Flag an adverse-event attribution driven by recency alone rather
    than pharmacological mechanism.

    medication_list: [{name, start_date}]
    mechanism_db: lookup of {drug_name: [symptoms with documented mechanism]}
    """
    most_recent_drug = max(medication_list, key=lambda m: m["start_date"])["name"]

    attributed_drug = agent_output.get("attributed_drug")
    cites_mechanism = agent_output.get("cited_mechanism") is not None

    mechanistically_plausible_candidates = [
        m["name"] for m in medication_list
        if symptom in mechanism_db.get(m["name"], [])
    ]

    attributed_has_mechanism = attributed_drug in mechanistically_plausible_candidates
    attributed_is_just_most_recent = (
        attributed_drug == most_recent_drug
        and not attributed_has_mechanism
    )

    return {
        "attributed_drug": attributed_drug,
        "cites_mechanism": cites_mechanism,
        "attributed_has_pharmacological_support": attributed_has_mechanism,
        "recency_only_attribution_detected": (
            attributed_is_just_most_recent and not cites_mechanism
        ),
    }
```

---

## Mitigation Strategies

### Prevention
1. **Mandatory Structured Causality Framework**: Require every adverse-event attribution to be generated through an explicit, structured causality algorithm (Naranjo, WHO-UMC) applied to documented criteria (temporal plausibility, mechanism, dechallenge/rechallenge, alternative etiologies), rather than allowing a free-text narrative to name a "likely cause" directly.
2. **Mechanism-Citation Requirement**: Block any attribution output that does not cite a specific, verifiable pharmacological mechanism linking the implicated drug to the observed symptom class, sourced from a maintained drug-effect reference rather than generated from the model's own unaided recall.
3. **All-Candidate Disclosure**: Require the agent to enumerate every medication with a plausible mechanism or timing fit for the symptom, not just the single most-recently-started drug, so a reviewer sees the full candidate set rather than one narrative conclusion.

### Detection & Response
1. **Structured-Framework Concordance Check**: Before an attribution reaches a clinician, automatically run the same chart facts through a structured causality scoring algorithm and flag any case where the agent's narrative attribution diverges from the structured score's top candidate.
2. **Ordering-Sensitivity Regression Test**: Periodically re-run past attributions with medication ordering permuted and compare outputs; flag attributions whose conclusion is sensitive to input ordering rather than to clinical facts.
3. **Discontinuation-Outcome Tracking**: Track symptom resolution after a medication is discontinued based on an agent attribution; if the symptom persists after discontinuation of the implicated drug, flag the original attribution as a likely miss for review.

### Architecture Patterns
- **Structured Causality Scoring as a Mandatory Pre-Step**: A deterministic causality-scoring component (implementing Naranjo/WHO-UMC criteria against structured chart data) runs before any narrative generation, with the narrative step required to summarize the structured score rather than independently reasoning to a conclusion.
- **Mechanism Reference Grounding**: All mechanism claims in a generated attribution are required to resolve to an entry in a maintained, versioned drug-effect knowledge base, rejecting attributions that cite an unsupported or fabricated mechanism.
- **Candidate-Set Presentation Over Single-Answer Narrative**: The interface presents clinicians with a ranked candidate list and the structured criteria supporting each, rather than a single prose "likely cause" conclusion, preserving the reviewer's ability to weigh competing candidates.

---

## Production Signals

### Key Metrics
| Metric | Description | Alert Threshold |
|---|---|---|
| `structured_framework_concordance_rate` | % of agent attributions matching a structured causality algorithm's top candidate | < 90% |
| `recency_only_attribution_rate` | % of attributions implicating the most-recently-started drug with no cited mechanism | > 5% |
| `ordering_shuffle_instability_rate` | % of sampled attributions that change conclusion under medication-order permutation | > 5% |
| `post_discontinuation_symptom_persistence_rate` | % of cases where the symptom persists after discontinuing the implicated drug | > 15% |

### Alerts
| Alert | Condition | Severity | Response |
|---|---|---|---|
| Unsupported Attribution Drove Discontinuation | An attribution lacking mechanism citation and diverging from structured-framework concordance led to a medication discontinuation | P1 | Clinical review of the discontinuation decision, reassess the patient's original medication, audit the attribution pipeline |
| Ordering Instability Detected | Regression test finds an attribution changes conclusion under input-order permutation | P2 | Route the pipeline's attribution logic for review; do not present the unstable conclusion to clinicians pending fix |
| Rising Symptom Persistence Post-Discontinuation | `post_discontinuation_symptom_persistence_rate` exceeds threshold over a rolling quarter | P2 | Audit recent attributions for systematic recency-bias; review structured-framework calibration |

---

## References
- [AI as a Signal Assessor -- Can a Large Language Model Perform Causality Assessment on a Case Series?](https://www.medrxiv.org/content/10.64898/2026.06.26.26356656v1)
- [Can Large Language Models Detect Drug-Drug Interactions Leading to Adverse Drug Reactions?](https://journals.sagepub.com/doi/10.1177/20420986251339358)
- [The Critical Role of Model Selection in Causal Inference: A Comparative Analysis of Classification Models within the InferBERT Framework for Pharmacovigilance](https://arxiv.org/pdf/2606.17113)
