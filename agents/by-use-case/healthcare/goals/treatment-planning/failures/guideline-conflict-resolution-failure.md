# Guideline Conflict Resolution Failure

## Issue: Agent Cannot Reconcile Conflicting Recommendations From Different Clinical Guideline Bodies and Defaults to an Arbitrary or Most-Recently-Retrieved Source

**Frequency**: Common

**Symptoms**
- Treatment plan cites one guideline body (e.g., ACC/AHA) in one section and a conflicting one (e.g., ESC) in another, without acknowledging the conflict
- Model presents a single recommendation as definitive when multiple major bodies actively disagree on the threshold or first-line choice
- Recommendation silently shifts between sessions depending on which guideline document was retrieved first by the retrieval layer
- No disclosure to the clinician that guideline bodies disagree, leaving the conflict invisible

**Root Cause**
Clinical guidelines from different professional societies and countries genuinely disagree on thresholds, first-line therapies, and screening intervals for many conditions (e.g., blood pressure treatment thresholds, statin initiation criteria, screening ages). RAG-based agents retrieve whichever guideline document scores highest for the query and present it as the answer, with no mechanism to detect that other equally authoritative sources recommend differently, and no structured way to surface the disagreement to the clinician for an informed choice.

**Example**
```
Scenario: Treatment-planning agent asked for blood pressure treatment threshold in a 68-year-old patient
Retrieved guideline A (one society): Treat at ≥130/80
Retrieved guideline B (another major society, not surfaced): Treat at ≥140/90 for this age group
Agent output: States ≥130/80 as "the" threshold, no mention of the differing recommendation
Impact: Clinician may initiate treatment earlier than their preferred guideline framework intends, without being aware a legitimate alternative exists
```

**Key Statistics**
- Guideline discordance across major professional bodies exists for a substantial share of common chronic-disease management decisions (hypertension thresholds, lipid targets, screening intervals)
- RAG-based clinical agents that retrieve a single top-ranked guideline document without conflict detection present a single answer as if undisputed in the majority of tested discordant-topic queries
- Explicitly surfacing guideline disagreement to clinicians, rather than silently picking one, is associated with better-aligned shared decision-making in clinical guideline-adherence studies

---

## Mitigation Strategies

1. **Multi-Source Retrieval and Conflict Detection**: Retrieve from multiple major guideline bodies for any query touching a known discordant topic, and explicitly compare recommendations
2. **Guideline Discordance Flagging**: Maintain a curated list of topics with known cross-society disagreement; force disclosure of the conflict whenever one is queried
3. **Source Attribution Requirement**: Require every guideline-based recommendation to cite which specific body and publication year it came from, not a generic "guidelines recommend"
4. **Clinician-in-the-Loop Resolution**: Present conflicting recommendations side-by-side and let the clinician select the framework, rather than the agent silently choosing

### Metrics
- % of known-discordant-topic queries that surface multiple guideline sources
- Source-attribution completeness rate
- Clinician override rate when conflict is surfaced (signal of useful disclosure)

### Alerts
- Known-discordant topic queried and only one guideline source retrieved → P2
- Recommendation given with no guideline source citation → P2

---

## References

- [Automating Expert-Level Medical Reasoning Evaluation of Large Language Models](https://arxiv.org/abs/2507.07988)
- [A Comprehensive Survey on the Trustworthiness of Large Language Models in Healthcare](https://arxiv.org/abs/2502.15871)
