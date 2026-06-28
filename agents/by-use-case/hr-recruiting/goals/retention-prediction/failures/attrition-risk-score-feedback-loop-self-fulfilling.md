# Attrition Risk Score Feedback Loop Self-Fulfilling

## Issue: Employees Flagged as High Attrition-Risk by the Retention-Prediction Model Are Systematically Deprioritized for Growth Opportunities, Stretch Assignments, and Promotion Consideration by Managers Aware of the Score, Causing the Flagged Employees to Actually Leave at Higher Rates as a Consequence of the Flag Itself

**Frequency**: Occasional

**Symptoms**
- Employees flagged high-risk show elevated attrition in the period following the flag, but investigation finds the elevation is partly attributable to reduced opportunity (fewer stretch assignments, slower promotion review) rather than to the pre-existing risk factors the model originally detected
- Managers with visibility into attrition-risk scores report (directly or via survey) that they unconsciously or deliberately invest less developmental effort in employees flagged high-risk, reasoning that the investment is "likely to be wasted" if the person is going to leave anyway
- Comparing two cohorts with similar underlying risk-factor profiles -- one where managers had visibility into the score and one where they did not (e.g., due to a rollout phasing difference) -- shows the visible-score cohort had higher actual attrition, suggesting the score's visibility itself affected the outcome
- High-risk-flagged employees who do receive continued investment and opportunity (despite the flag) show meaningfully lower actual attrition than the model's original prediction, indicating the prediction was not simply correct but was partly self-fulfilling for those who didn't receive continued investment
- The model is retrained on outcome data that already includes the effect of managers having acted on the score, reinforcing and entrenching the same risk-factor weights that originally produced the flag, including factors whose actual causal effect was actually manager-response-mediated rather than direct

**Root Cause**
Retention-prediction models are built to identify employees whose observable characteristics correlate with historical attrition, but once the score is surfaced to managers and used to inform real decisions (who gets a stretch assignment, who gets prioritized for a promotion conversation), the score stops being a passive prediction and becomes an active input into the very outcome it predicts. If reduced developmental investment in flagged employees actually increases their likelihood of leaving (a plausible and intuitive mechanism, but rarely tested), the model's predictive "accuracy" on retraining is partly validating its own prior intervention rather than measuring an independent, pre-existing risk signal -- a feedback loop that is invisible unless someone explicitly tests for it.

**Example**
```
Employee profile shows several factors correlated with historical attrition (tenure plateau, role outside typical promotion pipeline, recent flat performance review) -- model flags as high-risk
Manager, aware of the flag, deprioritizes the employee for an open stretch-assignment opportunity that quarter, reasoning that investing in someone "likely to leave" is a poor use of limited opportunity slots, and instead gives it to a lower-risk-flagged peer
Employee, now also missing out on the visible growth opportunity (a separate and additional reason to consider leaving, on top of the original risk factors), leaves within the following two quarters
Model retraining treats this as a confirmed true positive, reinforcing the weight of the original risk factors without ever testing whether the manager's response to the flag was itself a causal contributor
```

**Key Statistics**
- Retention-prediction and survivorship-bias research in HR analytics explicitly flags self-fulfilling feedback loops -- where a prediction influences manager behavior in a way that affects the predicted outcome -- as a known but frequently untested risk in deployed attrition models
- Allocational fairness research on algorithmic decision-making in employment contexts more broadly documents that visibility of a risk or quality score to a decision-maker can causally affect the decision-maker's behavior toward the scored individual, independent of the score's underlying accuracy
- HR analytics practitioner literature recommends holdout or randomized score-visibility experiments specifically to separate a model's predictive accuracy from feedback-loop-induced confirmation, noting that few deployed systems actually run this test

**Contributing Factors**
- Attrition-risk score is visible to managers who make real developmental and opportunity decisions, with no controlled separation between prediction and intervention
- Model retraining uses outcome data generated under conditions where the score itself influenced manager behavior, without correcting for this confound
- No experiment (e.g., score visibility withheld for a control group) has been run to isolate the score's pure predictive accuracy from its behavioral feedback effect

---

## Mitigation Strategies

1. **Score-Visibility Holdout Experiment**: Periodically withhold attrition-risk score visibility from managers for a randomized control group and compare actual attrition outcomes against the visible-score group, to measure and quantify the feedback-loop effect directly
2. **Reframe High-Risk Flags as Investment Triggers, Not Deprioritization Signals**: Explicitly train and communicate to managers that a high-risk flag should trigger increased retention investment (career conversation, growth opportunity) rather than withdrawal of opportunity, and monitor whether this guidance is actually followed
3. **Causal-Aware Model Retraining**: When retraining the model, account for whether the prior period's manager response to the score (investment vs. deprioritization) is a mediating variable in the outcome, rather than treating all attrition among flagged employees as confirming the original risk factors
4. **Manager Behavior Monitoring Tied to Flagged Employees**: Track whether managers' developmental actions (stretch assignments, promotion nominations) differ systematically for flagged vs. unflagged employees with similar tenure/performance profiles, as a direct measure of whether the feedback loop is occurring

### Metrics
- Attrition rate differential between score-visible and score-withheld (holdout) cohorts with comparable underlying risk-factor profiles
- Rate of developmental opportunities (stretch assignments, promotion nominations) given to flagged vs. unflagged employees with comparable performance and tenure
- Actual attrition rate among flagged employees who did receive continued investment vs. those who did not, isolating the flag's predictive value from its behavioral effect

### Alerts
- Holdout experiment shows a statistically significant attrition differential attributable to score visibility rather than underlying risk factors → P1
- Flagged employees show a measurably lower rate of developmental opportunity assignment than unflagged peers with comparable performance/tenure → P2
- Model retraining cycle proceeds without an updated causal-mediation check on the prior period's outcome data → P3

---

## References

- [Application of LLM Agents in Recruitment: A Novel Framework for Resume Screening](https://arxiv.org/pdf/2401.08315)
- [Small Changes, Large Consequences: Analyzing the Allocational Fairness of LLMs in Hiring Contexts](https://arxiv.org/pdf/2501.04316)
- [Towards Evidence-Based Tech Hiring Pipelines](https://arxiv.org/pdf/2504.06387)
