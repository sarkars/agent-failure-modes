# Fact Inversion

## Issue
An agent retrieves a fact correctly in terms of subject matter but reverses its direction or polarity — reporting "increases" when the source says "decreases," "improves" when the source says "worsens," or swapping which of two entities has the higher value. The topic and the entities involved are right; the relationship between them is flipped, which is often more damaging than an unrelated error because it's confidently stated and directionally opposite to the truth.

**Frequency**: Occasional

**Symptoms**
- Agent states a relationship (causal, comparative, directional) that is the exact opposite of what the source says
- The entities and topic in the response are correct; only the direction/polarity is wrong
- Errors cluster around comparative statements ("X is higher/lower than Y") and directional claims ("X increases/decreases Y")
- Confidence in the stated (wrong) direction is typically as high as it would be for the correct direction, since nothing internally flags the inversion

## Root Cause
Directional and comparative relationships are encoded in a small number of tokens (a single verb, a comparative adjective, a sign) embedded in an otherwise long, correctly-reproduced passage, so a single-token generation error can flip the entire meaning of an otherwise accurate summary without disrupting fluency or triggering any surface-level anomaly. This is compounded when source material describes multiple related but oppositely-signed relationships close together (e.g. "A increases X while B decreases X"), since the model can correctly recall that a relationship exists between the right entities while misattributing which direction belongs to which entity, especially under summarization or paraphrase where the original sentence structure isn't preserved verbatim.

## Example
```
A source clinical trial report states: "Treatment group A showed a 12%
reduction in adverse events compared to placebo, while Treatment group
B showed a 9% increase in adverse events compared to placebo."

A research-summary agent, asked to compare the two treatments, responds:
"Treatment group A showed a 12% increase in adverse events, while
Treatment group B showed a 9% reduction" — correctly recalling the
entities (Group A, Group B), the topic (adverse events), and both
numeric magnitudes (12%, 9%), but swapping which group experienced the
increase and which experienced the decrease.

A reader relying on this summary to choose between treatments would
select the worse-performing option based on an exactly-inverted
understanding of the trial's actual finding.
```

## Statistics
| Finding | Context |
|---------|---------|
| Directional/polarity inversion occurs in an estimated 2-6% of summarized comparative or causal statements in long-context summarization tasks | Estimated from summarization-fidelity benchmarks involving comparative claims |
| Inversion errors are markedly more common when a source describes two or more entities with opposite-signed relationships in close proximity | Typical pattern observed in comparative-claim evaluation sets |
| Requiring verbatim quotation of the directional clause alongside any paraphrase reduces inversion errors substantially in tested pipelines | Reported range across teams that added quote-verification steps |

## Mitigations
1. **Verbatim anchor for directional claims**: Require the generation step to quote or closely paraphrase the exact directional clause from the source for any comparative/causal statement, rather than reconstructing the relationship from memory of the broader passage.
2. **Post-generation direction verification**: Run an automated check comparing the polarity/direction of each generated comparative claim against the source's polarity for the same entity pair, flagging mismatches before the response is finalized.
3. **Entity-relationship structuring at ingestion**: Extract comparative and causal relationships into structured (subject, direction, object, magnitude) tuples at ingestion time, so generation draws from an unambiguous structured representation rather than re-deriving direction from prose.
4. **Symmetric-relationship extra scrutiny**: Apply additional verification specifically to source passages describing two or more entities with opposite-signed relationships to the same variable, since this is the highest-risk pattern for inversion.
5. **Numeric-magnitude/direction consistency check**: Cross-check that a magnitude value (e.g. "12%") and its stated direction (increase/decrease) in the generated output match the same pairing in the source, not a magnitude from one entity paired with a direction from another.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| direction_verification_pass_rate | Share of generated comparative/causal claims that pass automated polarity verification against source | Alert if < 97% |
| symmetric_relationship_error_rate | Inversion error rate specifically on source passages with opposite-signed entity pairs | Track separately; alert if markedly above baseline inversion rate |
| inversion_correction_rate | Rate of expert/user corrections identifying a directionally-inverted claim | Alert if > 1% of comparative/causal responses |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Inversion confirmed in high-stakes response | Review confirms a directionally-inverted claim in a medical/financial/safety-relevant response | High | Retract/correct immediately, add case to direction-verification test set |
| Direction verification pass rate drop | direction_verification_pass_rate falls below threshold after a generation pipeline change | Medium | Roll back or review recent changes to summarization/generation prompts |

## Related Patterns
- [Fact Negation Confusion](./fact-negation-confusion.md) - a closely related mechanism where negation handling, rather than directional polarity, is mishandled
- [Fact Source Confusion](./fact-source-confusion.md) - can produce a similar-looking symptom (swapped attribution) via a different mechanism (conflated entities rather than flipped polarity)
- [Domain Terminology Confusion](./domain-terminology-confusion.md) - shares the "single word carries the entire meaning" fragility that makes small errors have outsized effect
