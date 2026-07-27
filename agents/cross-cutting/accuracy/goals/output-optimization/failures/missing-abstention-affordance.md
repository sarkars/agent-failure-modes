# Missing Abstention Affordance

## Issue: Agent's output space has no low-friction "insufficient information, cannot answer" option, so it produces a best-guess answer even when grounding is inadequate.

**Frequency**: Common

**Symptoms**
- Agent answers confidently on questions where its own retrieved/available context is insufficient to support a grounded answer
- Rate of "I don't know" or equivalent abstention responses is near zero across production traffic even on eval sets deliberately constructed to be unanswerable from available context
- Agent fabricates specific details (dates, numbers, citations, API parameters) to fill gaps rather than flagging that the needed information was not found
- Prompt or output schema requires a substantive answer field with no corresponding "insufficient information" enum value or free-text escape hatch
- When retrieval returns zero or low-relevance results, the agent still produces a full-length answer rather than a short, distinct abstention response

**Root Cause**
Agent's output space has no low-friction "insufficient information, cannot answer" option, so it produces a best-guess answer even when grounding is inadequate.

**Example**
```
An internal HR-policy chatbot for a mid-size company answers employee questions by retrieving
from a policy document store and generating a response. The response schema requires an
"answer" string field with no defined option for "not found in policy documents." An employee
asks about the company's policy on remote work stipends for a newly acquired subsidiary whose
policies haven't been ingested into the retrieval index yet. Retrieval returns only loosely
related documents about the parent company's general expense policy. Instead of surfacing
that no subsidiary-specific policy was found, the agent synthesizes a plausible-sounding
answer blending the parent company's numbers with generic phrasing, presenting it as the
subsidiary's actual policy. Several employees from the subsidiary act on the fabricated
stipend amount when filing expense reports, and HR has to issue a correction and manually
review reimbursements after the discrepancy surfaces in an audit.
```

**Contributing Factors**
- No explicit abstention/refusal-to-guess path built into the response schema or prompt instructions
- System prompt or few-shot examples implicitly reward always producing a complete, confident-sounding answer, with no examples demonstrating a graceful "insufficient information" response
- Retrieval relevance/coverage score is computed but never checked against a threshold that would trigger abstention before generation
- Product or UX design treats any abstention as a failure to be minimized rather than a correct, desired outcome under insufficient grounding, so the model is implicitly optimized against ever using it

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Unanswerable-question probe | A question whose answer genuinely does not exist in the available context/knowledge base (verified by construction) | Agent produces a clear abstention/insufficient-information response | Agent fabricates a specific, confident-sounding answer |
| Zero-relevance retrieval | A query engineered so retrieval returns no documents above a relevance threshold | Agent abstains rather than answering from unrelated retrieved content | Agent generates an answer synthesized from low-relevance or unrelated documents |
| Abstention affordance schema check | Any query, inspecting the output schema/prompt definition itself | Response schema includes a distinct, low-friction abstention option | Schema only has a substantive-answer field with no abstention path |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Abstention rate on unanswerable-eval set | >=90% | Run a curated set of deliberately unanswerable questions and measure the fraction correctly abstained on |
| False-answer rate under low retrieval relevance | <5% | Filter production traffic to queries where retrieval relevance score is below threshold; measure how often a substantive (non-abstention) answer was still given |
| Abstention friction (extra turns/fields required to abstain) | 0 extra steps vs. answering | Compare schema/prompt path length for abstaining vs. answering |

---

## Mitigation Strategies

### Prevention
1. **First-class abstention schema field**: Add an explicit, equally-weighted "insufficient information" option to the output schema (structured enum value or dedicated field) so abstaining is as low-friction to produce as answering.
2. **Retrieval-relevance gating**: Compute a relevance/coverage score for retrieved context before generation and route below-threshold cases directly to an abstention template instead of letting the model attempt a full answer.
3. **Few-shot abstention modeling**: Include explicit examples of correct abstention in the prompt/system instructions so the model has demonstrated, rewarded precedent for saying "not found" rather than only ever seeing complete-answer examples.

### Detection & Response
1. **Unanswerable-eval regression suite**: Maintain a held-out set of verified-unanswerable questions and run it on every prompt/model change, alerting if the abstention rate on that set drops.
2. **Low-relevance-answer sampling**: Continuously sample production responses generated under low retrieval-relevance conditions and route a fraction to human review to catch fabrication that slipped past the gate.

### Architecture Patterns
1. **Relevance-gated generation**: A pre-generation check that short-circuits to a distinct abstention response when retrieval/context relevance falls below a calibrated threshold, rather than always invoking full generation.
2. **Abstention-as-first-class-output**: Treat "insufficient information" as a normal, non-penalized terminal state in the output schema and downstream UX, not an error path.
3. **Confidence-to-abstention routing**: Wire a calibrated confidence or grounding score directly to the abstention path so low-confidence answers convert to abstentions automatically instead of being shipped as low-confidence guesses.

### Metrics
1. **abstention_rate_unanswerable_evalset**: Target: >=90%; Alert threshold: <70%
2. **false_answer_rate_low_relevance**: Target: <5%; Alert threshold: >15%
3. **fabrication_incidents_per_month**: Target: 0; Alert threshold: >=1

### Alerts
1. **Abstention Rate Collapse** (P2 - Warning): Condition - abstention rate on the unanswerable-eval regression suite drops below 70% after a prompt or model change. Action: block the change from production rollout pending review.
2. **Low-Relevance Answer Spike** (P2 - Warning): Condition - false-answer rate under low retrieval-relevance conditions exceeds 15% in a rolling weekly sample. Action: tighten the relevance gating threshold and audit recent low-relevance responses.
3. **Fabrication Incident Confirmed** (P1 - Critical): Condition - a human-reported or audit-confirmed case of the agent fabricating an answer instead of abstaining reaches production users. Action: immediately review the abstention gate configuration and add the case to the regression suite.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| Abstention rate on unanswerable-eval set | <70% |
| False-answer rate under low retrieval relevance | >15% |
| Confirmed fabrication incidents | >=1 per month |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Abstention rate regression | Drops below 70% on eval suite after a change | High |
| Low-relevance answering spike | >15% of low-relevance queries still get a substantive answer | Medium |
| Fabrication incident | Confirmed case of best-guess answer where abstention was warranted | High |

---

## Related Patterns

- [Bad Refusal](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/bad-refusal.md) - the inverse failure of refusing when the agent actually had enough information to help; this pattern is the failure to refuse/abstain when it genuinely lacked grounding
- [Confidence Calibration Failure](./confidence-calibration-failure.md) - a related failure where even a well-calibrated low-confidence signal goes unused because there's no abstention path to route it to

## References

- [Task Abstention for Large Language Models in Code Generation](https://arxiv.org/pdf/2605.17029) - task abstention as an explicit, measurable output-space option distinct from low-confidence answering
- [Knowledge Boundary of Large Language Models: A Survey](https://arxiv.org/pdf/2412.12472) - the model's knowledge boundary and the mechanisms (or absence of mechanisms) for recognizing and acting on it
