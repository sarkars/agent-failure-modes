# Spurious Causal Narrative from Keyword Co-Occurrence

## Issue: A Sentiment-Escalation Agent's Free-Text Justification for Why a Ticket Is Being Escalated (Or Not) Invents a Plausible-Sounding Causal Explanation Linking Two Merely Co-Occurring Elements of the Conversation, and That Invented Explanation Is Adopted by Support Managers as a Real Triggering Rule Rather Than Recognized as the Model's Own Rationalization

**Frequency**: Occasional

**Symptoms**
- Escalation rationale states a confident causal claim ("this customer escalated to anger because they used the phrase 'third time' which indicates repeated failed attempts") that is not backed by any validated feature of the actual sentiment-classification model, only by the language model's own free-text rationalization of an observed word
- The same invented "trigger phrase" rule recurs across multiple escalation rationales in similar wording, even though no feature-importance analysis was ever run to confirm that phrase is actually predictive of true escalation-worthy sentiment versus simply being a common phrase in the ticket corpus generally
- Support managers begin training new agents to watch for the cited "trigger phrase" as a real predictor, and a controlled comparison of escalation outcomes for tickets containing the phrase against tickets without it shows no significant difference in actual customer-sentiment severity
- When the same co-occurring elements are tested against the sentiment model's actual feature weights, the claimed causal relationship is weak or absent, with the genuine driver being a different, unstated factor the narrative never engaged with
- The invented causal narrative is generated in response to a request to "explain" an escalation decision, rather than being retrieved from or grounded in the sentiment model's actual classification features

**Root Cause**
When an LLM-based escalation agent is asked to explain why a ticket was flagged for escalation, it generates a fluent, plausible-sounding causal narrative by drawing on general language intuition about what "sounds like" frustration, rather than by querying the sentiment-classification model's actual feature weights or attention patterns -- which may show a different, less narratively satisfying driver, or may show the cited phrase as only weakly predictive. The narrative is indistinguishable in tone and confidence from a genuinely validated finding, so support managers and agents have no signal that the cited "trigger" is a model-generated rationalization rather than a measured driver of escalation-worthy sentiment.

**Example**
```
Escalation agent flags a ticket as high-priority and is asked to justify the decision; it observes the customer used the phrase "third time I'm asking" and generates: "This phrase indicates repeated failed resolution attempts and strongly predicts customer churn risk, warranting immediate escalation"
Support manager adopts this as a coaching point, instructing frontline agents to treat "third time" as an automatic high-priority trigger phrase regardless of other ticket context
A controlled comparison of tickets containing the phrase against a matched sample without it shows no significant difference in actual measured sentiment severity or subsequent churn, since many customers use exaggerated repetition language without it reflecting genuinely elevated frustration relative to other phrasing
The escalation model's actual feature weights show a different, unstated factor (multiple distinct issues raised within the same ticket) as the real driver of the cases the narrative had attributed to the repetition phrase
```

**Key Statistics**
| Finding | Source |
|---------|--------|
| LLM-based agents are documented to produce fluent, confident hallucinated claims not grounded in the actual data or model output being described, a distinct risk from factual hallucination in open-domain generation | [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1) |
| Confidence-calibration research on tool-using agents finds verbalized confidence is frequently uncorrelated with actual grounding in verified data, particularly for explanatory or rationale-generation tasks rather than direct lookups | [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264) |
| Complexity-prediction research in support contexts emphasizes the need for features validated against actual outcome data rather than narratively plausible but unvalidated heuristics | [Complexity Prediction in Support](https://arxiv.org/abs/2008.02455) |

**Contributing Factors**
- Escalation agent is prompted to explain "why" a ticket was flagged without being constrained to ground its explanation in the sentiment-classification model's actual feature-importance output
- No distinction is surfaced to support managers between "this is a model-validated escalation driver" and "this is the agent's own generated rationalization of an observed phrase or pattern"
- No feedback loop tests whether tickets matching an agent-generated "trigger phrase" actually show elevated sentiment severity or churn risk relative to a matched comparison sample

---

## Mitigation Strategies

1. **Ground Explanations in Actual Feature-Attribution Output**: Require the escalation agent to query and cite the sentiment model's real feature-importance or attention-weight data when explaining a flag, and explicitly label any explanatory claim it cannot ground in that output as "unverified hypothesis" rather than presenting it with the same confidence as a validated finding
2. **Controlled Test Before Trigger-Phrase Adoption**: Before an agent-generated "trigger phrase" or pattern becomes a team-wide coaching point, run a controlled comparison of actual sentiment-severity or churn outcomes for tickets matching it against a matched sample that does not, rather than adopting the narrative on its face
3. **Label Generated Rationales Distinctly from Validated Drivers**: Surface a clear, visible distinction in escalation rationale output between model-validated drivers and the agent's own free-text rationalization, so support managers can calibrate how much weight to give each
4. **Periodic Audit of Recurring Escalation Narratives Against Model Internals**: Sample recurring causal claims appearing across escalation rationales and check them against the sentiment model's actual feature weights, retracting or correcting any claim that does not hold up

### Metrics
- Rate of escalation-rationale claims that can be matched to a corresponding feature-importance signal in the sentiment model versus claims with no such grounding
- Outcome difference (sentiment severity, churn rate) between tickets matching an agent-generated "trigger phrase" and a matched comparison sample
- Recurrence rate of a given unverified causal claim across multiple escalation rationales without ever being checked against model internals

### Alerts
- An agent-generated trigger-phrase claim with no corresponding feature-importance grounding is adopted as a team-wide coaching practice without a controlled outcome test → P1
- Audit finds a recurring causal claim contradicted by the sentiment model's actual feature weights still being actively cited in escalation rationales → P2
- Escalation agent's explanatory output is deployed to a new support team without the unverified-hypothesis labeling distinction in place → P3

---

## References

- [LLM-based Agents Suffer from Hallucinations: A Survey of Taxonomy, Methods, and Directions](https://arxiv.org/html/2509.18970v1)
- [The Confidence Dichotomy: Analyzing and Mitigating Miscalibration in Tool-Use Agents](https://arxiv.org/pdf/2601.07264)
- [Complexity Prediction in Support](https://arxiv.org/abs/2008.02455)
