# Embedding Retrieval Pulls Mismatched Historical Attrition Cohort as Comparable

## Issue: A Retention-Prediction Agent's Embedding Search over Past Departed-Employee Records Surfaces a Lexically Similar but Substantively Different Attrition Case as the Nearest-Neighbor Comparable, and the Agent Anchors a Current Employee's Risk Score to That Mismatched Precedent

**Frequency**: Occasional

**Symptoms**
- The retention-prediction agent's risk-score rationale cites a specific past departed employee as the closest comparable case, but the cited case differs from the current employee on the actual driving factor of attrition (e.g., the departed employee left for relocation, while the current employee's risk factors are compensation-related), despite reading as similar in role and tenure
- High-risk scores driven primarily by retrieved-cohort similarity show a lower actual prediction accuracy (measured against subsequent real attrition outcomes) than scores driven by structured behavioral and survey-signal features, when the two scoring paths are compared on backtest
- The retrieved "comparable" departed employee frequently shares only surface-level profile attributes (title, tenure band, department) with the current employee, not the underlying structured signals (manager-change history, compensation-percentile trend, engagement-survey trajectory) that actually drove the precedent case's departure
- HR business partners report that employees flagged high-risk "because of a similar case we saw before" frequently turn out, on manual review, to resemble that case only in superficial profile attributes
- Re-scoring the same employee with the retrieval step disabled, using only structured features, produces a meaningfully different and, on backtest, more accurate risk score

**Root Cause**
The retention-prediction agent's retrieval step ranks past departed-employee records by embedding similarity over free-text profile and exit-interview fields, which captures topical and lexical overlap but not the structured behavioral signals that actually determined whether the precedent case departed for the reason the model is trying to predict. Two employee records can be highly similar in embedding space because they share role and tenure vocabulary, while differing entirely on the dimensions -- manager-change history, compensation-percentile trend, survey-sentiment trajectory -- that determine attrition risk, and the agent has no mechanism to weight retrieved precedents by structured-signal similarity rather than text similarity alone.

**Example**
```
Current employee: a five-year tenure mid-level engineer with a recent manager change and a declining engagement-survey trend
Retention-prediction agent's embedding retrieval over departed-employee records surfaces a different five-year tenure mid-level engineer as the top comparable, driven by shared title and tenure-band vocabulary in the free-text profile fields
Agent cites this precedent in its risk rationale: "Similar profile to [departed employee], who left within six months -- flagging this employee as high attrition risk"
HR business partner is directed to prioritize a retention conversation framed around the cited precedent's known driver (relocation), missing the current employee's actual driver (recent manager change and compensation-percentile decline), which the retrieved precedent never exhibited
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| Most-similar retrieved items are not necessarily the most relevant for the decision being made, a structural limitation of similarity-ranked retrieval used to justify downstream agent decisions | [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1) |
| Knowledge-oriented retrieval-augmented generation systems are documented to surface topically related but structurally mismatched precedents when the retrieval index is not filtered by the structured criteria relevant to the downstream prediction task | [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677) |
| LLM-driven evaluations in workforce and hiring-adjacent decision contexts show that retrieved comparable-case framing can materially shift downstream risk judgments even when the underlying structured signals do not support the comparison | [Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts](https://arxiv.org/pdf/2501.04316) |

**Contributing Factors**
- Precedent retrieval ranks by free-text profile and exit-interview embedding similarity only, with no pre-filter by structured attrition-driver similarity (manager-change history, compensation trend, survey trajectory)
- Risk-score rationale surfaces the retrieved precedent prominently, anchoring the score and the recommended retention intervention even when the precedent's actual relevance is limited to shared title and tenure vocabulary
- No backtest separates the predictive accuracy of retrieval-anchored risk scores from structured-feature-driven risk scores, so the retrieval step's net effect on prediction accuracy is not visible

---

## Mitigation Strategies

1. **Constrain Retrieval to Structured-Driver-Matched Cohort First**: Filter candidate departed-employee precedents by structured attrition-driver similarity (manager-change history, compensation-percentile trend, survey trajectory) before applying embedding similarity within that filtered set, rather than ranking the full departed-employee history by profile-text similarity alone
2. **Separate Precedent Citation from Score Contribution**: Use retrieved precedents for illustrative rationale only, and ensure the actual risk score is driven by structured, backtested behavioral features, with retrieval explicitly excluded from the score-computation path
3. **Backtest Retrieval-Driven vs. Feature-Driven Prediction Accuracy**: Periodically measure attrition-prediction accuracy of scores attributable primarily to retrieved-precedent similarity against scores attributable to structured features, and suppress or reweight the retrieval contribution if it underperforms
4. **Surface Driver-Match Metadata in the Rationale**: When a precedent is cited, require the rationale to explicitly state which structured attrition-driver dimensions were checked and matched, so HR business partners can see whether the comparison is substantive or merely superficial

### Metrics
- Prediction-accuracy divergence between risk scores attributable primarily to retrieved-precedent similarity and scores attributable to structured features alone
- Rate of HR-business-partner-reported "mismatched precedent" feedback on high-risk-flagged employees
- Structured attrition-driver overlap (manager-change history, compensation trend, survey trajectory) between flagged employees and their cited retrieved precedent, sampled

### Alerts
- Backtest shows retrieval-driven score component underperforming structured-feature component by a material margin for two consecutive review cycles → P2
- HR-business-partner-reported mismatched-precedent feedback rate exceeds baseline for a given department or tenure band → P2
- A new retention-prediction model version is deployed without a structured-driver pre-filter on the retrieval step → P3

---

## References

- [Classifying and Addressing the Diversity of Errors in Retrieval-Augmented Generation Systems](https://arxiv.org/html/2510.13975v1)
- [A Survey on Knowledge-Oriented Retrieval-Augmented Generation](https://arxiv.org/pdf/2503.10677)
- [Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts](https://arxiv.org/pdf/2501.04316)
