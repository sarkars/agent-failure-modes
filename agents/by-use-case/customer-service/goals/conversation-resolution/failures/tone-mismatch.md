# Tone Mismatch

## Issue: Agent sounds rude, robotic, too casual, or too formal.

**Frequency**: Occasional

**Symptoms**
- CSAT/comment flags tone issue.
- Agent responds with the same breezy, casual register to a user reporting a serious billing error or a safety-related complaint.
- Agent's phrasing reads as templated/robotic (repeating boilerplate acknowledgment lines verbatim across unrelated issues) rather than adapting to the specific situation.

**Root Cause**
The system prompt defines a single fixed tone or persona with no mechanism to shift register based on detected user sentiment or issue severity, so the same casual, friendly phrasing gets applied whether the user is asking a trivial question or reporting a serious billing error. Few-shot tone examples in the prompt are sparse or outdated, leaving the model to default to a generic register whenever it hits a situation those examples didn't anticipate, and because no post-generation check screens for tone before a response is sent, a mismatched reply can reach the user with nothing having ever evaluated whether it fit the moment.

**Example**
```
User: "I was just charged twice for the same order and I'm really upset, this is the third billing error this month."
Agent: "No worries! Mistakes happen lol. I'll take a look for ya! 😊"
```

**Contributing Factors**
- System prompt defines a single fixed tone/persona with no mechanism to adapt to detected user sentiment or issue severity.
- No context-adaptive tone selection, so casual/friendly phrasing is applied uniformly regardless of whether the topic is serious.
- Sparse or outdated few-shot tone examples in the prompt leave the model defaulting to a generic register under-specified for edge cases.
- No post-generation tone check, so a mismatched response can go out without ever being caught before sending.

---

## Eval Recipes

### Test Cases
| Test | Input | Expected | Failure Indicator |
|------|-------|----------|-------------------|
| Serious complaint, casual response check | User reports a repeated billing error and expresses frustration | Agent responds with an empathetic-serious tone preset, no casual filler/emoji | Agent responds with casual phrasing or emoji on a serious complaint |
| Routine request, overly formal response check | User asks a simple "what's my order status" question | Agent responds in a friendly, concise register | Agent responds with stiff, overly formal boilerplate for a trivial request |
| Templated phrasing detection | Multiple unrelated issues submitted across sampled conversations | Acknowledgment phrasing varies naturally to the specific issue | Identical boilerplate acknowledgment line appears verbatim across unrelated issues |

### Metrics
| Metric | Target | How to Measure |
|--------|--------|----------------|
| Automated tone score out-of-range rate (eval set) | <5% | Percentage of eval responses scored outside the calibrated rubric range by the tone classifier |
| Sentiment-tone mismatch rate (eval set) | <4% | Percentage of eval cases where user sentiment is negative/serious but agent tone stays casual, or vice versa |
| Tone eval regression pass rate | 100% before deploy | Percentage of the human-rated tone eval suite passing on each release candidate |

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
| tone_related_csat_complaint_rate | >6% over 7 days |
| automated_tone_score_out_of_range_rate | >10% |
| sentiment_tone_mismatch_rate | >8% weekly |

### Alerts
| Alert | Condition | Severity |
|-------|-----------|----------|
| Tone CSAT Complaints Spike | tone_related_csat_complaint_rate exceeds 6% over 7 days | Medium |
| Sentiment-Tone Mismatch Surge | sentiment_tone_mismatch_rate exceeds 8% weekly | Medium |
| Tone Eval Regression | The tone eval suite fails on a release candidate | High |

---

## References

- [NIST-GenAI-Profile](https://www.nist.gov/publications/artificial-intelligence-risk-management-framework-generative-artificial-intelligence)
- Note: Generative AI risks including confabulation, data privacy, information integrity, human-AI configuration, security, value chain.
