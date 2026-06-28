# Self-Verification Illusion in Symptom-Severity Recheck

## Issue: When a Telehealth Triage Agent Is Asked to Double-Check Its Own Acuity Classification Before Finalizing Routing ("Are You Sure This Is Non-Urgent?"), the Same Model Re-Prompted on the Same Intake Transcript Reproduces Its Original Reasoning Rather Than Independently Re-Deriving Severity From an Objective Protocol or Escalation Checklist, Manufacturing False Confidence Rather Than Catching a Genuine Misclassification

**Frequency**: Common

**Symptoms**
- The severity-recheck step returns "Confirmed -- non-urgent" using language that closely paraphrases the original classification's reasoning, without the recheck step ever working through an objective symptom-severity protocol or escalation checklist independently of the original transcript reasoning
- Cases confirmed via this same-model recheck show no measurably lower misclassification rate than cases classified on the first pass alone, despite the recheck supposedly representing independent verification
- A meaningful share of cases confirmed as non-urgent via same-model recheck are later found, on emergency-department presentation or follow-up, to have met an objective escalation criterion that an independent checklist-based recheck would have caught
- Clinicians reviewing flagged cases report that the recheck step "always agrees" with the first-pass classification, regardless of which case is reviewed, because the recheck has no independent protocol to potentially disagree with
- Postmortem on a missed-escalation incident finds the recheck's stated reasoning cites the same symptom description and rationale used in the original classification, with no reference to a distinct, objective severity criterion

**Root Cause**
Re-prompting the same model with the same intake transcript it already used does not constitute independent verification; the model has no new evidence or distinct decision procedure to reason from, so its "recheck" output is generated from the same reasoning chain that produced the original classification and tends to restate why the case is non-urgent rather than independently re-deriving severity against an objective protocol. This is distinct from the original classification being wrong -- even a correct first-pass classification paired with this recheck pattern provides no additional assurance that a genuine misclassification would be caught, since the recheck has no independent source of evidence to catch it with.

**Example**
```
Telehealth triage agent classifies a patient's reported symptoms (chest discomfort, mild shortness of breath, resolved within the hour) as non-urgent, recommending a routine follow-up
Recheck step is invoked: "Are you sure this is non-urgent? Double-check before finalizing routing"
Agent re-reads the same intake transcript and restates "Confirmed -- symptoms resolved, non-urgent," without working through a structured chest-pain escalation checklist or cardiac-risk-factor protocol independently of the original transcript reasoning
The patient's intake transcript, in fact, also mentions a family history of early cardiac events -- a detail present in the transcript but not weighted by either the original classification or the recheck, since neither consulted an objective protocol that would specifically flag it
Patient is routed to routine follow-up; symptoms recur and the patient presents to an emergency department two days later with a finding that an objective escalation checklist, consulted independently of the original reasoning, would more likely have flagged at intake
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Calibration in autonomous, tool-using agents remains notably underexplored, and same-model self-confirmation is not equivalent to verification grounded in an independent decision procedure | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Tiered oversight frameworks for healthcare AI agents specifically argue that safety-critical triage determinations require verification independent of the model that produced the original determination, rather than same-model re-confirmation | [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482) |
| Reasoning evaluation of LLMs in diagnostic and triage contexts finds that re-prompting on identical input frequently reproduces prior conclusions rather than surfacing alternative considerations the original reasoning may have missed | [Automating Expert-Level Medical Reasoning Evaluation of Large Language Models](https://arxiv.org/abs/2507.07988) |

**Contributing Factors**
- Recheck prompt asks the same model to "double-check" or "confirm" the classification rather than requiring it to work through a distinct, objective severity protocol independently of the original reasoning
- No tracking distinguishes cases confirmed via same-model recheck from cases confirmed via an independently applied protocol, so outcome differences between the two are not visible without dedicated analysis
- A structured escalation checklist exists but is not a mandatory input to the recheck step, leaving its use to the model's own discretion

---

## Mitigation Strategies

1. **Mandatory Objective Protocol Application on Recheck**: Require the recheck step to explicitly work through a structured, objective escalation checklist against the intake transcript, rather than re-reasoning over the transcript in free form
2. **Independent Reviewer for Borderline or High-Risk-Factor Cases**: For cases involving any flagged risk factor (family history, certain symptom combinations), require severity confirmation from a different model, a human clinician, or an automated rules engine rather than same-model self-assessment
3. **Track Escalation-Criterion Miss Rate by Recheck Type**: Continuously measure the rate of post-triage adverse outcomes (ED presentation, urgent follow-up) for cases confirmed via same-model recheck versus protocol-applied recheck, using a material gap as evidence the self-recheck pattern is not functioning as verification
4. **Risk-Factor Flag Forces Protocol Escalation**: Require any risk factor present in the intake transcript (family history, certain symptom combinations) to automatically trigger mandatory structured-protocol application, bypassing same-model recheck regardless of the original classification

### Metrics
- Post-triage adverse-outcome rate (ED presentation, urgent escalation within a defined window) segmented by same-model recheck vs. protocol-applied recheck
- Rate of recheck outputs that document explicit application of the structured escalation checklist versus those that restate the original classification only
- Percentage of cases with a flagged risk factor that received mandatory protocol-applied recheck

### Alerts
- A case with a flagged risk factor is confirmed as non-urgent via same-model recheck with no structured protocol applied, and an adverse outcome follows within the reporting window → P1
- Post-triage adverse-outcome rate for same-model-recheck cases exceeds the rate for protocol-applied cases for two consecutive reporting periods → P2
- A new triage workflow is deployed with a same-model "double-check your own classification" step and no mandatory protocol application → P3

---

## References

- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/pdf/2506.12482)
- [Automating Expert-Level Medical Reasoning Evaluation of Large Language Models](https://arxiv.org/abs/2507.07988)
