# Outdated Medical Guidelines in Recommendations

## Issue: Model Uses Medical Guidelines That Have Been Superseded by Newer Research; Recommends Treatment No Longer Best-Practice

**Frequency**: Common

**Symptoms**
- Model recommends treatment A (standard 2020)
- 2024 research shows treatment B is superior
- Model still recommends A (knowledge cutoff 2020)
- Patient gets suboptimal treatment

**Root Cause**
Medical guidelines evolve with research. Models trained on 2020 data have knowledge cutoff then. New trials, meta-analyses emerge yearly. Models don't have mechanism to update with new clinical evidence. Can't read and integrate latest research automatically.

**Example**
```
Scenario: Hypertension treatment recommendation
2020 guideline: ACE inhibitors as first-line
2024 research: New class of drugs shows superior outcomes with fewer side effects
Model trained 2020: Still recommends ACE inhibitors
Patient 2024: Gets suboptimal drug class
Impact: Better treatment available but not prescribed
```

**Key Statistics**
- Medical guidelines update: Every 2-3 years for major conditions
- Research lag: 3-5 years between trial publication and guideline adoption
- Treatment optimality: Model from 2020 is 80-90% optimal by 2024

---

## Mitigation Strategies

1. **Continuous Learning**: Subscribe to medical guideline updates; retrain quarterly
2. **Evidence Freshness**: Flag recommendations older than 2 years
3. **Guideline Versioning**: Track guideline version used; update when new version released
4. **Clinician Alerts**: Notify when newer alternatives exist

### Metrics
- Guideline currency (% of recommendations using latest guideline)
- Treatment optimality (should be >95% vs. latest guidelines)
- Update lag (days between guideline change and model update)

### Alerts
- Recommendation differs from current guideline → Flag for review

---

## References

- [Staying Current with Medical AI](https://arxiv.org/abs/2104.14024)
- [Clinical Practice Guidelines & ML](https://arxiv.org/abs/2106.11889)
