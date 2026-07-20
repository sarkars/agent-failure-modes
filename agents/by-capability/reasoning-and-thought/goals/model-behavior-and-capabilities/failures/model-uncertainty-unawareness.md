# Model Uncertainty Unawareness

## Issue
The model generates answers in a uniformly confident tone regardless of how certain it actually is about the content, so an agent (and the end user) cannot distinguish a well-grounded answer from a guess by reading the response alone. Low-confidence, borderline, or fabricated content is phrased with the same declarative certainty as well-established facts, removing the natural signal a human expert would give ("I'm not sure, but...") that would otherwise prompt verification.

**Frequency**: Very Common

**Symptoms**
- Fabricated details (a nonexistent function parameter, an invented case citation, a made-up statistic) are stated as flatly as verified facts
- The model's phrasing gives no measurable difference between answers later shown to be correct and answers later shown to be wrong
- Asking the model to rate its own confidence produces a number that correlates poorly with actual correctness
- Users report being misled specifically because the wrong answer "sounded just as confident" as answers they'd verified as correct
- Confidence language ("I believe," "possibly," "you should verify") appears at roughly the same low rate regardless of the underlying task's actual difficulty or the model's internal uncertainty

## Root Cause
Language models are trained to produce the most probable continuation of a prompt, and confident, declarative phrasing is simply a more common surface pattern in training data than hedged phrasing, independent of whether the underlying claim in that data was actually well-supported. There is no direct architectural link between the model's internal computation of token probability (which does encode a form of uncertainty) and the surface-level hedging language it chooses to use — the two are learned somewhat independently, so a model can be internally "uncertain" in the sense of spreading probability mass across several plausible completions while still selecting confident-sounding phrasing for whichever one it samples. Reinforcement learning from human feedback further reinforces this: raters have historically tended to prefer complete, confident-sounding answers over hedged ones of similar accuracy, training the model away from expressing calibrated uncertainty even when it would be the more honest response.

## Example
```
A legal research agent is asked to cite case law supporting a specific
contract interpretation. It responds:

"This interpretation is well-supported by Hartwell v. Meridian Corp
(2019), where the court held that ambiguous indemnification clauses
must be construed against the drafting party."

The case does not exist. The model fabricated a plausible-sounding
citation with a specific name, year, and holding, phrased with the exact
same confident, declarative structure it uses for real, verifiable
citations elsewhere in the same response.

A junior associate relying on the agent's output cites the fabricated
case in a draft filing. The error is caught only when opposing counsel
cannot locate "Hartwell v. Meridian Corp" in any case database, at which
point the firm must explain the fabrication to the court.
```

## Statistics
| Finding | Context |
|---------|---------|
| Hedging/uncertainty language appears at a similarly low rate in responses later verified as incorrect compared to responses verified as correct | Estimated from analyses correlating response phrasing with fact-checking outcomes |
| Self-reported confidence scores (when explicitly requested) typically show weak-to-moderate correlation with actual accuracy, well short of good calibration | Typical range reported across LLM calibration studies |
| Explicitly prompting the model to distinguish "well-established" from "uncertain/inferred" claims measurably improves the correlation between stated confidence and actual accuracy versus unprompted responses | Typical range observed in structured-uncertainty prompting evaluations |

## Mitigations
1. **Structured confidence elicitation**: Require the model to explicitly separate claims into confidence tiers (verified/inferred/uncertain) as part of the output schema, rather than leaving confidence implicit in phrasing.
2. **Grounding and citation verification**: For fact-heavy domains, require retrieval-backed citations and programmatically verify that cited sources actually exist and support the claim, rather than trusting the model's assertion.
3. **Calibration evaluation before deployment**: Test whether the model's stated or implied confidence actually correlates with accuracy on a held-out set for the specific task domain, and don't assume calibration transfers from general benchmarks.
4. **User-facing uncertainty surfacing**: Where verification isn't automatic, surface a system-level disclaimer or confidence indicator alongside high-stakes claim types (legal, medical, financial) rather than relying on the model to self-hedge.
5. **Independent verification pass for high-stakes claims**: Route claims in high-consequence domains through a separate fact-checking step (search, database lookup) before presenting them as fact, decoupling verification from the generating model's own confidence signal.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| confidence_accuracy_correlation | Correlation between stated/implied confidence and verified accuracy on a sampled evaluation set | Alert if correlation falls below calibrated floor |
| unverified_citation_rate | Share of citations/factual claims in high-stakes outputs that pass automated existence/grounding checks | Alert if verification failure rate > 2% |
| hedging_language_rate_on_known_wrong_answers | Rate of hedging language in responses later confirmed incorrect | Alert if not meaningfully higher than rate on confirmed-correct responses |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Unverifiable high-stakes claim shipped | A legal/medical/financial claim is delivered without passing grounding verification | High | Block delivery pending verification, escalate for human review |
| Calibration regression | confidence_accuracy_correlation drops after a model or prompt change | Medium | Re-run calibration evaluation, review structured confidence prompting |

## Related Patterns
- [Model Knowledge Cutoff](./model-knowledge-cutoff.md) - stale knowledge is one specific source of uncertainty presented with the same false confidence this pattern describes broadly
- [Model Reasoning Inconsistency](./model-reasoning-inconsistency.md) - borderline, inconsistent conclusions are delivered with no signal that the underlying reasoning was near a decision boundary
- [Model Refusal Inconsistency](./model-refusal-inconsistency.md) - borderline refusal decisions are resolved without surfacing the underlying uncertainty at the decision threshold
