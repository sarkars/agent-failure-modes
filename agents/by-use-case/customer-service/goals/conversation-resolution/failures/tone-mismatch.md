# Tone Mismatch

## Issue: Agent sounds rude, robotic, too casual, or too formal.

**Frequency**: Occasional

**Symptoms**
- CSAT/comment flags tone issue.
- [Add more specific symptoms]

**Root Cause**
Agent sounds rude, robotic, too casual, or too formal.

**Example**
```
[Add concrete example showing this failure pattern]
```

**Contributing Factors**
- [List factors that make this failure more likely]

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| [Test name] | [Input] | [Expected output] | [What indicates failure] |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| [Metric name] | [Target value] | [Measurement method] |

---

## Mitigation Strategies

### Prevention
1. **Persona/tone rubric bound to brand voice**: define an explicit, example-anchored tone rubric (register, warmth, formality range) tied to the brand's voice guidelines and include few-shot examples in the system prompt, since tone mismatch stems from the model defaulting to a generic register absent explicit calibration to the intended persona. Trade-off: a rigid rubric can make the agent sound same-y or scripted across genuinely different contexts if it doesn't also vary with context.
2. **Context-adaptive tone selection**: detect conversational context signals (user's own tone, sentiment, topic severity) and select from a small set of pre-calibrated tone presets (empathetic-serious, friendly-casual, formal-technical) rather than one fixed tone for all conversations, since "sounds robotic" and "too casual for a serious issue" are opposite failures of the same root cause: a static tone applied regardless of context. Trade-off: preset selection can misfire on ambiguous context, applying an inappropriate tone confidently.
3. **Tone-specific eval suite with human-rated pairs**: build an eval set of conversations labeled by human raters across the rudeness/robotic/casual/formal axes and regression-test tone on every prompt or model change. Trade-off: tone rating is subjective and requires multiple raters per example to get reliable labels, which is costly to scale.

### Detection & Response
1. **CSAT free-text tone-keyword mining**: mine post-conversation comments for tone-related complaint keywords (rude, cold, robotic, unprofessional, condescending) and track as a distinct sub-metric of CSAT, since generic CSAT scores blend tone issues with resolution issues and can mask a tone-specific regression. Response: pull matching transcripts into a labeled tone-failure eval set.
2. **Automated tone classifier on live transcripts**: run a lightweight tone classifier over sampled live conversations scoring against the rubric axes, catching tone drift before it shows up in lagging CSAT data. Response: alert when a sampled batch's tone score falls outside the calibrated range.
3. **Sentiment-mismatch detection**: flag conversations where the user's sentiment is negative/serious but the agent's detected tone stays casual, or vice versa, the direct signature of a mismatch rather than a uniformly bad tone. Response: route to the tone eval set and check whether context-adaptive selection failed.

### Architecture Patterns
1. **Tone-preset router keyed to context signals**: a structural layer that selects a tone preset, with its own few-shot examples and lexical constraints, based on detected user sentiment/topic severity before generation, rather than leaving tone entirely to a single static system prompt.
2. **Post-generation tone linter**: a lightweight pass that checks generated responses against rubric constraints (banned robotic phrases, required warmth markers for serious topics) and regenerates or edits before sending, catching mismatches structurally rather than relying on the primary generation call to get it right every time.
3. **Brand-voice style guide as versioned, testable config**: keep the tone rubric and few-shot examples in versioned config decoupled from the core task prompt, so tone can be iterated and A/B tested independently of functional prompt changes, with rollback if a tone change regresses CSAT.

### Metrics
1. **tone_related_csat_complaint_rate**: Target: <3% of negative comments mention tone; Alert on >6% weekly
2. **automated_tone_score_out_of_range_rate**: Target: <5% of sampled conversations; Alert on >10%
3. **sentiment_tone_mismatch_rate**: Target: <4%; Alert on >8%
4. **tone_eval_regression_pass_rate**: Target: 100% pass before deploy; Alert on any failure blocking deploy

### Alerts
1. **Tone CSAT Complaints Spike** (P2): Condition - tone_related_csat_complaint_rate exceeds 6% over 7 days. Action: sample flagged transcripts, check for recent prompt/persona changes, roll back if regression confirmed.
2. **Sentiment-Tone Mismatch Surge** (P2): Condition - sentiment_tone_mismatch_rate exceeds 8% weekly. Action: review the context-adaptive tone router for misclassification patterns.
3. **Tone Eval Regression** (P1): Condition - the tone eval suite fails on a release candidate. Action: block the deploy until rubric compliance is restored.

---

## Production Signals

### Key Metrics
| Metric | Alert Threshold |
|--------|-----------------|
| [Metric name] | [Threshold] |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| [Alert name] | [Condition] | Medium |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
