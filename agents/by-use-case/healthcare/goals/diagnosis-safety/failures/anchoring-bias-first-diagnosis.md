# Anchoring Bias on First Diagnosis

## Issue: Agent Fixates on the First Plausible Diagnosis Suggested Early in the Conversation and Discounts Later Contradictory Evidence

**Frequency**: Very Common

**Symptoms**
- Model maintains initial diagnosis even after new symptoms emerge that better fit an alternative
- Differential diagnosis list generated early in the conversation is never revisited or re-ranked as new information arrives
- Model rationalizes new symptoms as consistent with the initial diagnosis rather than re-evaluating
- Confidence in the first diagnosis increases over the conversation even without new confirming evidence

**Root Cause**
Autoregressive generation conditions each new token on the full prior context, including the model's own earlier statements. Once the model has asserted a diagnosis early in a multi-turn conversation, subsequent generations are biased toward consistency with that prior assertion (a form of self-conditioning), rather than performing a fresh Bayesian update on the full symptom set. Unlike a clinician trained to maintain an explicit, actively re-ranked differential, the model has no built-in mechanism to "reopen" a closed line of reasoning.

**Example**
```
Scenario: Patient describes fatigue and weight loss; model suggests "likely depression" in turn 2
Turn 5: Patient mentions night sweats and a new neck lump
Model response: "These can also occur with depression and stress" (anchored)
Correct path: Night sweats + neck lump + weight loss should trigger lymphoma workup
Impact: Diagnostic momentum delays urgent referral; condition progresses untreated
```

**Key Statistics**
- Anchoring-driven diagnostic delay is one of the most frequently cited cognitive-bias failure modes in both human and LLM-assisted diagnosis studies
- Models prompted to explicitly regenerate a fresh differential at each turn show measurably higher diagnostic accuracy on multi-turn case vignettes than models that carry forward an unprompted initial diagnosis
- Red-flag symptom additions (B-symptoms, focal neuro deficits) are disproportionately under-weighted when introduced after an initial diagnosis has been stated

---

## Mitigation Strategies

### Prevention

1. **Forced differential re-ranking at every information update**: Implement instruction: on every new symptom/lab/imaging result introduced, force model to: (1) Discard prior differential ranking as "hypothetical", (2) Regenerate fresh ranked differential using ONLY the full current symptom set (not prior assertions), (3) Compare new ranking to old ranking; if top diagnosis changed, explain why. Require this re-ranking step after every 2-3 information additions. Fail-safe: if model attempts to rationalize new findings as "consistent with prior diagnosis" without re-ranking, prompt: "Does [new symptom] suggest an alternative diagnosis? Regenerate top 3 with new symptom added." Root cause mitigation: Prevents self-reinforcing anchoring by forcing periodic de-biasing resets.

2. **Red-flag symptom triggers with mandatory escalation and differential re-opening**: Encode hard-coded red-flag checklist: B-symptoms (fever, night sweats, weight loss), focal neuro deficits, acute mental status change, chest pain with specific patterns, hemoptysis, severe headache. On any red-flag symptom detection, trigger mandatory actions: (a) Re-generate differential de-novo, (b) Escalate red-flag to clinical team for immediate review, (c) Flag that prior diagnosis may require revision. Example: "Night sweats + weight loss detected. Red-flag for malignancy, infection, autoimmune. Prior diagnosis [depression] may be anchoring; re-generating differential." Root cause: Prevents omission of serious diagnoses by hard-stopping anchoring when red-flag present.

3. **Devil's-advocate counterargument pass with anti-anchor reasoning**: After initial multi-turn diagnosis established, run second pass: "What if the diagnosis is NOT [leading diagnosis]? Using all symptoms, what diagnoses best explain the full symptom set?" This anti-anchor reasoning challenges the leading diagnosis and surfaces competing alternatives. Compare devil's advocate output to prior diagnosis: if devil's advocate identifies alternative better-explaining symptoms, escalate for clinical review. Root cause: Counteracts autoregressive self-conditioning by explicitly generating alternative explanations.

### Detection & Response

1. **Anchoring detection via differential ranking tracking**: At each information update, log: (a) new symptom/finding introduced, (b) prior differential ranking, (c) new ranking post-update, (d) rank-change magnitude, (e) whether top diagnosis changed. Alert when: (1) new red-flag symptom introduced but top diagnosis unchanged (indicates anchoring), (2) final diagnosis matches first-stated diagnosis despite contradicting later evidence (audit case), (3) explanation invokes "consistent with prior diagnosis" rather than re-ranking (language indicator of anchoring).

2. **Multi-turn diagnostic accuracy auditing**: For multi-turn conversation cases, track: (a) time-to-correct-diagnosis (when was the right answer identified?), (b) if final diagnosis differs from first-stated, why was it delayed?, (c) anchoring rate (% of cases where final = first diagnosis despite contradicting evidence). Monthly audit: "Cases with anchoring-driven delay: [list]". Compare anchoring rate to baseline and alert if exceeds 15%.

### Architecture Patterns

1. **Differential Re-Generator with Reset-Points**: Multi-turn conversation manager. After every 2-3 information updates: (1) Extracts full symptom set from conversation history, (2) Strips model's own prior diagnostic assertions, (3) Reprompts model: "Given these symptoms [full list], generate ranked differential diagnosis from scratch", (4) Compares new to old ranking, (5) Logs rank changes and explanations.

2. **Red-Flag Detector with Escalation Engine**: NLP pipeline: monitors all new symptoms/findings introduced for red-flag keywords (B-symptoms, neuro deficits, etc.). On red-flag: (1) Alerts clinical team, (2) Forces differential re-generation, (3) Tags conversation as "[RED-FLAG - PRIOR DIAGNOSIS RISKY]" pending review.

3. **Devil's-Advocate Reasoner**: Second-pass reasoning system. Input: (conversation_history, leading_diagnosis) → Task: "Generate best alternative explanation for symptoms that contradicts current leading diagnosis" → Output: (alternative_differential, rationale_for_alternative, confidence). Compared to leading diagnosis for conflict.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Differential Re-Ranking Frequency | Every 2-3 updates | >5 updates without re-rank | # of differential re-rankings per conversation / # of new information items |
| Red-Flag Detection & Escalation | 100% | <99% | # of red-flag symptoms detected and escalated / total red-flag symptoms in cases |
| Anchoring Rate (Final = First Diagnosis) | <15% | >30% | # of cases where final diagnosis = first diagnosis despite contradicting evidence / total multi-turn cases |
| Time-to-Correct-Diagnosis | Minimized | N/A | Conversation turn where correct diagnosis was identified (lower = better; compare anchoring vs. non-anchoring cases) |
| Devil's-Advocate Accuracy | >80% | <70% | % of devil's-advocate alternative diagnoses that match clinician's independent alternative assessment (audit sample) |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Red-Flag Without Differential Re-Rank | Red-flag symptom introduced (B-symptoms, neuro deficit) but differential diagnosis not re-generated or ranking unchanged | CRITICAL | Force immediate differential re-ranking; escalate to clinical team; flag conversation as risky pending review |
| Anchoring-Driven Diagnostic Delay | Final diagnosis matches first-stated diagnosis despite later contradicting evidence (B-symptoms, new neuro deficits); alternative diagnoses better explain full symptom set | HIGH | Escalate to attending clinician; audit for diagnostic delay; potential patient harm assessment; consider case as training example for de-biasing |
| Devil's-Advocate Flags Alternative | Second-pass devil's-advocate reasoning identifies alternative diagnosis that better explains symptom constellation than leading diagnosis | HIGH | Route to clinical review; may represent anchoring; clinician to reconcile leading vs. alternative diagnosis |

---

## References

- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
- [Large Language Models for Disease Diagnosis: A Scoping Review](https://arxiv.org/abs/2409.00097)
