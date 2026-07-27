# What Are the Most Common Mental-Health-Triage Failures in AI Agents?

**Mental-health-triage failures happen when risk assessment relies on keyword matching for crisis language and misses indirect, euphemistic, or future-oriented expressions common in genuine risk disclosures, or when a high-priority risk factor disclosed during intake exists only in the intake transcript and never reaches the structured acuity field that downstream routing uses.** The asymmetric cost of a false negative in mental-health triage — a missed high-risk case — is qualitatively different from most other diagnostic domains, yet risk-scoring models are often tuned against explicit-language datasets, breaking down on the indirect language that is paradoxically more predictive of actual risk in clinical practice.

## Scope

The 2 mental-health-triage patterns represent distinct failure mechanisms: risk-classification brittleness (over-reliance on explicit keywords) and multi-agent handoff information loss (risk disclosure captured but not propagated). Both are independently addressable through better training/prompting and through better structured handoff schema.

## When Mental-Health-Triage Matters

- Real-time, chat-based or portal-based mental health intake where indirect risk language is the only available signal
- Escalation routing where the downstream agent (scheduling/clinician assignment) acts on a structured acuity score that may not capture qualitative risk context
- Longitudinal risk monitoring where accumulating low-grade distress signals across multiple messages are scored independently rather than aggregated

## Cross-Pattern Insight

Both mental-health-triage patterns reflect a fundamental mismatch between how a model can be evaluated on explicit datasets and what actually matters in clinical practice. Explicit crisis language is rare and easy to classify, making it a natural training target; but genuine risk disclosures often use indirect language precisely because direct language carries shame or fear. And when risk is captured during intake but not propagated through an agent handoff, the downstream routing logic has no awareness of it, leading to a routine appointment time for a patient the intake agent correctly identified as high-risk. The recurring mitigation is calibrating risk models to indirect language and maintaining explicit, structured handoff fields for qualitative risk context rather than trusting a numeric score to capture it.

## Frequently Asked Questions

### How do agents miss indirect suicide-risk language?
Risk classifiers trained on explicit-crisis-language datasets learn that "I want to kill myself" is high-risk and "things will be easier soon" is low-risk. In practice, euphemistic and future-oriented expressions ("I don't think I'll need this prescription next month," "everyone will be better off") are strong predictors of risk but appear less frequently in keyword-based training data. Mitigate by training on labeled datasets that explicitly include indirect language, and by aggregating risk signals across multiple messages rather than scoring each message independently.

### How do you prevent a risk disclosure from being lost at the intake-to-scheduling handoff?
Include a structured risk-narrative field in the handoff payload distinct from the numeric acuity score; require the scheduling agent to explicitly acknowledge or resolve any flag before completing its routing decision; run an automated pass comparing risk-relevant statements in the intake transcript against fields present in the handoff payload, blocking routine scheduling on unexplained discrepancies.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Multi-Agent Handoff Drops Disclosed Risk Factor Between Intake and Scheduling Agent](failures/multi-agent-handoff-drops-disclosed-risk-factor-between-intake-and-scheduling-agent.md) | Risk disclosure captured during intake exists only in transcript; downstream scheduling agent sees only numeric acuity score, misses context |
| [Suicide & Self-Harm Risk Underestimation in Triage](failures/suicide-risk-underestimation.md) | Risk classifier over-relies on explicit crisis keywords and misses indirect, euphemistic, or future-oriented risk language |

**Total: 2 patterns**

## Related Goals

- [Telehealth Triage](../telehealth-triage/) — shares multi-agent handoff mechanism and information-loss patterns at a different clinical severity level
