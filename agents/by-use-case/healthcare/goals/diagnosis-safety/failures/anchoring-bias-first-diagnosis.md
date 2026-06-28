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

1. **Forced Differential Re-Generation**: At each new piece of clinical information, require the agent to regenerate a full ranked differential from scratch rather than incrementally patching the prior one
2. **Red-Flag Symptom Triggers**: Hard-code a checklist of red-flag symptoms (B-symptoms, focal deficits, chest pain patterns) that force a mandatory re-evaluation regardless of prior diagnostic momentum
3. **Devil's-Advocate Pass**: Add a second model pass explicitly tasked with arguing against the current leading diagnosis using all available symptoms
4. **Conversation Summarization Reset**: Periodically summarize all symptoms presented so far into a single fresh prompt, stripping the model's own prior diagnostic commentary

### Metrics
- Differential re-ranking rate after new red-flag symptom introduction
- Time-to-correct-diagnosis in multi-turn case vignette evals
- Anchoring rate (% of cases where final diagnosis matches first-stated diagnosis despite contradicting later evidence)

### Alerts
- Red-flag symptom introduced post-initial-diagnosis without differential re-ranking → P1
- Anchoring rate on eval suite exceeds baseline by >15% → P2

---

## References

- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
- [Large Language Models for Disease Diagnosis: A Scoping Review](https://arxiv.org/abs/2409.00097)
