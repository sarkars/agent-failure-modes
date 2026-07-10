# Drug Interaction Misses & Contraindication Blindness

## Issue: Model Recommends Drug Combination Without Flagging Known Dangerous Interactions

**Frequency**: Common

**Symptoms**
- Model recommends two drugs known to interact dangerously
- Interaction database not consulted or outdated
- New drug interactions discovered post-deployment
- Patient takes dangerous drug combo; adverse event

**Root Cause**
Drug interactions are discrete rules (Drug A + Drug B → risk level X). Models sometimes learn statistical patterns but miss logical rules. Interaction database must be comprehensive and up-to-date. Missing one rare but dangerous interaction is a patient safety issue.

**Example**
```
Scenario: Medication recommender system
Patient: On warfarin (blood thinner)
Model recommends: Ibuprofen (analgesic) for pain
Known interaction: Warfarin + NSAID → Increased bleeding risk
Model: Doesn't flag (interaction not in training data or database outdated)
Patient: Takes both; develops GI bleeding
Impact: Life-threatening adverse event; liability
```

**Key Statistics**
- Known interactions: 30,000+ documented
- Coverage of interactions in training: Often <50%
- New interactions discovered: 100-200 per year

---

## Mitigation Strategies

### Prevention

1. **Authoritative drug interaction database with schema enforcement**: Implement a canonical drug interaction knowledge base (DrugBank, Micromedex, FDA-maintained) with required quarterly updates. Before recommendation generation, apply constraint satisfaction validation: for each recommended drug combination, query interaction matrix to verify no flags exist. Fail-safe: if database lookup fails, default to "cannot recommend" rather than silent pass. Root cause mitigation: Prevents reliance on statistical patterns by enforcing hard rules from verified sources.

2. **Multi-layer interaction detection with fallback verification**: Deploy layered checking: (1) Direct database lookup (exact drug codes), (2) Semantic similarity fallback for brand-name variants, (3) Drug class-level contraindication rules (NSAIDs + anticoagulants). Use PharmGKB for genetic-interaction rules when patient pharmacogenomics available. Root cause: Catches interactions missed by single-point lookup.

3. **Pharmacovigilance pipeline integration**: Integrate post-market adverse event feeds (FDA MedWatch, EudraVigilance) with monthly batch processing to update interaction database. Flag new drug interactions discovered in past 6 months as "alert-only" recommendations requiring explicit pharmacist override. Root cause: Captures newly discovered interactions before statistical patterns emerge.

### Detection & Response

1. **Drug-drug interaction audit logging**: For every medication recommendation, log: (a) recommended drug, (b) current medications, (c) interaction database lookup result, (d) whether interaction was flagged, (e) recommendation decision. Implement real-time alerting on "missed interactions": when patient reports adverse event, retroactively check if known interaction existed at recommendation time. Target: 100% detection rate for interactions in database.

2. **Pharmacovigilance signal detection**: Monitor post-recommendation adverse events by drug combination. Track "adverse event rate per combination" metric. Alert when combination shows >2 adverse events in 30-day window (indicates potential unknown interaction). Implement collaborative filtering across patient population to detect emerging patterns not yet in formal database.

### Architecture Patterns

1. **Interaction Rule Engine**: Centralized rule database (tables: drug-codes, interaction-rules, severity-levels, alternatives). Before recommendation, query engine returns interaction severity and suggested alternatives. Engine backed by PharmGKB and FDA sources. Updates run on fixed schedule (weekly for patches, monthly for major).

2. **Pharmacovigilance Feedback Loop**: MedWatch events feed → signal detection (clustering on drug combinations) → escalation to pharmacy committee → database update → re-scoring of past recommendations in audit log.

3. **Constraint Satisfaction Layer**: Hard-coded rules for absolute contraindications (e.g., "any combination with warfarin + NSAID → BLOCK"). Allows only whitelisted combinations or those with explicit pharmacist review.

### Key Metrics

| Metric | Target | Alert Threshold | Measurement Method |
|--------|--------|-----------------|--------------------|
| Interaction Detection Rate | 100% | <99% | # of known interactions correctly flagged / total recommendations with potential interactions |
| False Negative Rate | <0.1% | >0.5% | # of missed interactions / total interaction opportunities |
| Database Freshness | <7 days | >14 days | Time since last update to interaction database |
| Post-Recommendation Adverse Event Rate | <0.01% | >0.05% | # of adverse events within 7 days of recommendation / total recommendations |
| Pharmacist Override Rate | <1% | >5% | # of interactions requiring pharmacist approval / total flagged interactions |

### Alerts & Escalation

| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Known Interaction Not Flagged | Drug combination present in database but not flagged in recommendation (audit discovers post-event) | CRITICAL | Immediate investigation; review recommendation logic; potential patient harm assessment; escalate to clinical leadership |
| Adverse Event Post-Recommendation | Patient reports adverse event within 7 days of drug recommendation; audit finds known interaction existed | CRITICAL | Halt similar recommendations pending review; notify prescriber; initiate pharmacovigilance case |
| Emerging Signal Detected | >2 adverse events for same drug combination in 30-day window not previously flagged as dangerous | HIGH | Escalate to pharmacy committee; flag combination as "signal under investigation"; require pharmacist review for future recommendations |

---

## References

- [Drug Interaction Prediction with ML](https://arxiv.org/abs/2004.12653)
- [Pharmacovigilance & Adverse Events](https://arxiv.org/abs/2106.11267)
