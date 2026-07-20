# Fact Probabilistic Mismatch

## Issue
An agent retrieves a fact that was expressed by its source with explicit probabilistic or statistical framing — a likelihood, a confidence interval, a rate observed in a sample — and restates it as a flat, deterministic certainty, dropping the uncertainty that was integral to the original claim's meaning. The number or direction carried over is often correct; what's lost is the epistemic status of the claim, turning "this happens in about 30% of cases" into "this happens" or "this is what will happen."

**Frequency**: Common

**Symptoms**
- Source states a probability, rate, confidence interval, or statistical association; agent output states an unconditional outcome
- Hedging language ("may," "is associated with," "in some cases") present in source is absent from the response
- Users report being surprised when a stated "fact" doesn't hold for their specific case, despite the agent never having claimed it would hold universally in the source
- Errors cluster around statistical/epidemiological/scientific source material translated into conversational advice

## Root Cause
Probabilistic framing is often carried by a small number of hedge words and numeric qualifiers embedded in an otherwise assertive sentence structure, and generation models trained to produce confident, fluent, directly-responsive answers have a systematic pull toward stripping hedges because unhedged statements are shorter, more common in training data as "answers," and read as more helpful and decisive. This is reinforced when a user's question is phrased as a yes/no or a request for a single outcome ("will this happen to me"), since the generation step is implicitly rewarded for giving a matching single-outcome answer rather than preserving the source's inherently distributional framing.

## Example
```
A source clinical study states: "Patients with this genetic marker have
approximately a 15% lifetime risk of developing the condition, compared
to a 3% baseline risk in the general population — a 5x relative
increase, but the majority of marker carriers never develop the
condition."

A user who has tested positive for the marker asks a health-information
agent: "I have this marker, will I develop the condition?"

The agent responds: "Yes, this genetic marker significantly increases
your risk of developing the condition" — correctly capturing the
direction and magnitude of the relative increase, but dropping the
absolute-probability framing entirely, producing a response that reads
as predicting the outcome will occur rather than stating an elevated
but still minority probability.

The user experiences significant anxiety and makes major life decisions
based on an outcome the source's own data suggests is more likely not
to happen than to happen.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-30% of agent responses summarizing source statements with explicit probability/confidence framing drop that framing in the final response | Estimated from hedge-preservation audits of scientific/medical summarization pipelines |
| Yes/no-phrased user queries produce unhedged responses to probabilistic source facts at a markedly higher rate than open-ended queries on the same source | Typical pattern observed in query-framing evaluation studies |
| Explicit hedge-preservation prompting and post-generation hedge verification recover most of the dropped probabilistic framing in tested pipelines | Reported range across teams that added hedge-specific verification |

## Mitigations
1. **Hedge-preservation verification**: Run an automated check comparing the epistemic framing (certainty language, probability figures, confidence qualifiers) of generated claims against the source, flagging responses that convert a probabilistic source statement into an unhedged claim.
2. **Structured probability metadata at ingestion**: Extract explicit probability/rate/confidence-interval values from source statistical claims into structured metadata, and require the generation step to surface this metadata rather than reconstructing certainty framing from memory of the prose.
3. **Reframe yes/no queries as distributional by default**: When a user poses a yes/no question about an inherently probabilistic fact, have the agent default to reporting the probability/rate rather than collapsing to a single yes/no answer.
4. **Absolute-vs-relative risk distinction**: Explicitly preserve and distinguish absolute risk figures from relative risk figures in generated output, since dropping absolute framing while keeping only relative multipliers is a common and particularly misleading form of this error.
5. **Domain-appropriate uncertainty language standards**: Establish house style requiring specific hedge phrasing ("is associated with an X% likelihood," not "causes" or "will result in") for any claim sourced from probabilistic/statistical material, and enforce it via automated linting on generated output.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| hedge_preservation_rate | Share of generated claims sourced from probabilistic source statements that retain appropriate hedge/probability language | Alert if < 85% |
| yes_no_collapse_rate | Rate at which yes/no-phrased queries about probabilistic facts produce unhedged yes/no answers | Track trend; alert on sustained increase |
| probabilistic_mismatch_correction_rate | Rate of expert/user corrections identifying a probability treated as a certainty | Alert if > 5% of responses in statistics-heavy domains |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Certainty framing on high-stakes probabilistic fact | Review confirms a medical/financial risk probability was presented as a certainty | High | Correct the response, add source claim to hedge-preservation test set |
| Hedge preservation rate drop | hedge_preservation_rate falls below threshold after a generation pipeline change | Medium | Review recent prompt/pipeline changes for hedge-stripping regressions |

## Related Patterns
- [Fact Partial Truth](./fact-partial-truth.md) - a probabilistic mismatch is a specific form of partial truth where the dropped qualifier is specifically the fact's uncertainty framing
- [Fact Generalization Error](./fact-generalization-error.md) - both involve stripping a scoping condition, one for applicable population and one for certainty level
- [Domain Risk Blindness](./domain-risk-blindness.md) - related in that both concern under-communicating risk, one through omission and one through false certainty
