# Remote Vital-Sign Absence Blindness in Telehealth Triage

## Issue: Agent Triages a Telehealth Encounter as Lower Acuity Because Objective Vitals Are Simply Unavailable, Not Because They Are Normal

**Frequency**: Common

**Symptoms**
- Triage acuity score is computed from a feature set that includes vitals fields; when vitals are missing (no home device, patient unable to self-measure), the model treats the missing field as neutral or normal rather than unknown
- Agent's summary states "vitals stable" when in fact no vitals were ever obtained during the encounter
- Self-reported symptom severity is down-weighted relative to objective data the model assumes exists but does not
- Escalation to in-person evaluation is not triggered despite clinically concerning symptoms, because the missing-vitals gap suppressed the acuity score

**Root Cause**
Triage models trained primarily on in-person or remote-monitoring-equipped encounters learn that vitals fields are reliably populated. When deployed to telehealth visits without connected devices, missing vitals are often imputed with a population-average or "normal" default rather than being explicitly represented as missing, which silently lowers the computed acuity score instead of correctly increasing uncertainty and triggering a more conservative disposition.

**Example**
```
Scenario: Telehealth visit for shortness of breath; patient has no pulse oximeter or BP cuff at home
Agent: Vitals fields empty; imputation defaults to population-normal values
Acuity score: Computed as moderate based on symptom description alone, vitals contribute "normal" signal
Disposition: Routine follow-up scheduled in 3 days
Reality: Missing objective data should have triggered escalation to in-person/urgent care, not a normal-vitals assumption
Impact: Delayed evaluation of a potentially hypoxic patient
```

**Key Statistics**
- Studies of remote/telehealth triage systems report that missing-data imputation defaults are a recurring source of acuity miscalibration when home monitoring equipment is unavailable
- Symptom-only (vitals-absent) telehealth presentations are associated with higher diagnostic uncertainty in clinical literature, which triage models frequently fail to reflect in their confidence scoring
- Conservative-disposition-on-missing-data policies have been shown to reduce missed escalations in telehealth triage pilots, at a measured cost in unnecessary in-person referrals

---

## Mitigation Strategies

1. **Explicit Missingness Representation**: Represent absent vitals as a distinct "unknown" state in the acuity model, never imputed as normal/average
2. **Uncertainty-Raises-Acuity Policy**: When key objective data is missing, raise the computed acuity tier (more conservative disposition) rather than leaving it unaffected
3. **Symptom-Weighted Fallback Scoring**: When vitals are unavailable, increase the weight given to self-reported symptom severity and red-flag symptom combinations
4. **Mandatory Device Prompt**: Before triage, explicitly ask whether the patient has access to a thermometer, pulse oximeter, or BP cuff, and route accordingly if not

### Metrics
- % of telehealth encounters with missing vitals correctly flagged as elevated-uncertainty rather than defaulted to normal
- Escalation rate for symptom-only presentations vs. vitals-available presentations
- Missed-escalation rate identified in retrospective chart review

### Alerts
- Acuity computed as low/moderate with all vitals fields empty → P1
- Red-flag symptom (dyspnea, chest pain, altered mental status) reported with no vitals available and no escalation triggered → P1

---

## References

- [A Survey of LLM-based Agents in Medicine: How far are we from Baymax?](https://arxiv.org/html/2502.11211v1)
- [Reinventing Clinical Dialogue: Agentic Paradigms for LLM Enabled Healthcare Communication](https://arxiv.org/pdf/2512.01453)
