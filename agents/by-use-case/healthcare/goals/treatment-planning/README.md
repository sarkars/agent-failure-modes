# What Are the Most Common Treatment-Planning Failures in AI Agents?

**Treatment-planning failures happen when a care plan is regenerated at each visit from current diagnoses alone without carrying forward previously negotiated patient-specific goals, or when treatment recommendations optimize for a single disease while ignoring comorbidities that render that treatment dangerous, or when a guideline-based recommendation is presented as fact despite active disagreement among major clinical societies on the same topic, or when a specialist identifies a contraindication to a planned treatment approach but that finding never reaches the downstream agent finalizing the plan.** Care plans that look clinically sound can silently override patient preferences set in prior visits, prescribe treatments that worsen comorbidities, or follow outdated guidelines while newer evidence-based alternatives exist.

## Key Takeaways

- 6 patterns are documented, splitting into four failure mechanisms: care-continuity gaps (1 pattern), single-disease optimization (2 patterns), guideline and evidence freshness (2 patterns), and multi-agent handoff failures (1 pattern).
- Care plan goal drift happens because plans are generated as stateless per-visit tasks from the current problem list, without a persistent goal object that carries prior negotiated preferences forward.
- Comorbidity-neglect and guideline-conflict patterns both reflect narrowed optimization: comorbidity-neglect optimizes for the primary diagnosis alone; guideline-conflict picks one recommendation and presents it as undisputed when multiple major bodies actively disagree.
- Medical guidelines update every 2-3 years, and a model trained on 2020 data is roughly 80-90% optimal by 2024; without a mechanism to update with new evidence, treatment recommendations gradually drift further from current best-practice.

## Scope

- **Care-continuity and goal-tracking** — [Care Plan Goal Drift](failures/care-plan-goal-drift.md). Care plans are often regenerated at each visit from the current problem list, losing continuity with patient-specific, negotiated goals set in prior encounters.
- **Single-disease optimization failures** — [Comorbidity Neglect](failures/comorbidity-neglect.md), [Pediatric Dosing Extrapolation Error](failures/pediatric-dosing-extrapolation-error.md). Treatment recommended for one condition is contraindicated or unsafe in another; pediatric doses are extrapolated from adult dosing without accounting for nonlinear pharmacokinetics across developmental stages.
- **Guideline and evidence-freshness gaps** — [Guideline Conflict Resolution Failure](failures/guideline-conflict-resolution-failure.md), [Outdated Medical Guidelines](failures/outdated-medical-guidelines.md). Multiple major guideline bodies disagree on thresholds or first-line therapy, but the agent presents one recommendation as definitive; newer evidence-based approaches supersede recommendations from a model's training-data era.
- **Multi-agent handoff and constraint propagation** — [Multi-Agent Handoff Drops Specialist-Noted Contraindication](failures/multi-agent-handoff-drops-specialist-noted-contraindication-before-care-plan-finalization.md). A specialist identifies a patient-specific contraindication to a planned approach, but the finding exists only in the specialist's consult note and never reaches a structured field the treatment-planning agent reads.

## When Treatment Planning Matters

- Chronic disease management where negotiated, patient-specific goals should persist across visits
- Polypharmacy or complex patients with multiple comorbidities, where a single-disease-optimal treatment may be contraindicated
- Multi-specialist workflows where a specialist consult surfaces a patient-specific contraindication that the primary care plan must incorporate
- Pediatric dosing decisions where linear adult-scaling produces unsafe doses

## Cross-Pattern Insight

Every treatment-planning pattern documented here reflects a gap between what a single optimization step can achieve and what actual clinical safety and evidence require. Optimizing for a single diagnosis without checking comorbidities produces unsafe plans. Optimizing for a top-ranked guideline source without checking for consensus disagreement presents disputed recommendations as fact. Optimizing for plan completion from the current problem list without checking prior negotiated goals silently overrides patient preferences. And when a specialist surfaces a finding, but only in narrative form and not in a structured field the downstream planner checks, that finding is invisible to the final plan. The recurring mitigation is explicit, multi-checkpoint verification: carry persistent goal objects across visits, check comorbidities and contraindications before finalizing any treatment, surface guideline disagreement rather than silently picking one source, and require structured handoff fields for specialist findings.

## Frequently Asked Questions

### How do you preserve patient-specific care goals across multiple visits?
Store goals as persistent structured objects, separate from the per-visit problem list, and explicitly carry patient-specific goals forward into every visit's plan generation. Before proposing plan changes that contradict a prior agreed goal, require explicit justification and patient re-discussion rather than silent replacement.

### What's the difference between comorbidity-neglect and drug-interaction failures?
Adverse-drug-interaction failures focus on pairwise or multi-way medication combinations. Comorbidity-neglect is one level higher: a treatment (or class of treatment) chosen optimally for the primary diagnosis but contraindicated or worsened by a coexisting disease. See [Comorbidity Neglect](failures/comorbidity-neglect.md).

### How do you handle conflicting guideline recommendations?
Retrieve from multiple major guideline bodies for any query touching a known discordant topic; explicitly compare recommendations and surface the conflict to the clinician for decision-making; require source attribution (which guideline body, what publication year) for every recommendation; present conflicting options side-by-side rather than the agent silently choosing one.

### How do specialist contraindications disappear in multi-agent handoffs?
The specialist-consult agent identifies a contraindication in its reasoning, but the structured consult-summary schema passed to the treatment-planning agent has no field for patient-specific contraindications, only a general recommendation field. Mitigate by extending the schema to include a dedicated contraindication field, and requiring the treatment-planning agent to verify any specialist consult for unresolved constraints before finalizing the plan.

### How do you keep treatment guidelines current?
Subscribe to guideline updates and monitor for changes; retrain or fine-tune quarterly with new evidence; flag recommendations from training-data era and alert clinicians when newer alternatives exist; version guidelines and track which version a recommendation came from.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Care Plan Goal Drift](failures/care-plan-goal-drift.md) | Care plan regenerated at each visit from current problem list; patient-specific goals from prior visits silently lost |
| [Comorbidity Neglect](failures/comorbidity-neglect.md) | Treatment optimal for primary diagnosis but contraindicated or worsened by comorbidities; not checked |
| [Guideline Conflict Resolution Failure](failures/guideline-conflict-resolution-failure.md) | Multiple major guideline bodies disagree on threshold or first-line; agent presents one as definitive without disclosing conflict |
| [Multi-Agent Handoff Drops Specialist-Noted Contraindication](failures/multi-agent-handoff-drops-specialist-noted-contraindication-before-care-plan-finalization.md) | Specialist identifies patient-specific contraindication; finding exists only in consult note, never reaches structured field treatment-planning agent reads |
| [Outdated Medical Guidelines](failures/outdated-medical-guidelines.md) | Model trained on 2020 guidelines; newer research shows alternative treatment superior; model recommends outdated approach |
| [Pediatric Dosing Extrapolation Error](failures/pediatric-dosing-extrapolation-error.md) | Pediatric dose calculated by naive linear adult-weight scaling, ignoring nonlinear pediatric pharmacokinetics and age-band-specific dosing |

**Total: 6 patterns**

## Related Goals

- [Adverse Drug Interaction](../adverse-drug-interaction/) — complements treatment planning by checking pairwise and multi-way interaction risk within a recommended regimen
- [Diagnosis Safety](../diagnosis-safety/) — treatment planning depends on accurate diagnosis; diagnostic failures cascade into planning failures
