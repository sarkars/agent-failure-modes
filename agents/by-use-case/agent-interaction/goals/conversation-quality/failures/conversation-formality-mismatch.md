# Conversation Formality Mismatch

## Issue
The agent's register — word choice, sentence structure, use of humor or emoji, level of hedging — doesn't match what the context calls for: overly casual language in a request about a legal or medical matter, or stiff corporate boilerplate in a casual back-and-forth where the user has been informal throughout. The mismatch itself becomes a distraction from the content, signaling the agent isn't reading the room even when the substance of the answer is correct.

**Frequency**: Common

**Symptoms**
- Agent uses casual language (exclamation points, emoji, colloquialisms) in response to a serious, sensitive, or formal request
- Agent uses stiff, corporate, or overly hedged phrasing in a conversation the user has kept casual and direct throughout
- User explicitly comments on tone ("you don't need to be so formal" or "this feels a bit flippant for the topic")
- Register shifts inconsistently within a single response or across adjacent turns on the same topic
- Formality level doesn't adjust even after the user's own register has clearly signaled a preference

## Root Cause
Register is typically set by a single global system-level instruction ("be friendly and approachable" or "maintain a professional tone") rather than being inferred per-conversation from context signals like subject matter, the user's own word choice, or the stakes of the topic. A model applying a fixed house style has no mechanism to detect that a request touching grief, legal risk, or financial loss calls for a different register than a request about scheduling lunch, unless that distinction is made an explicit part of the generation decision rather than left to a static default.

## Example
```
User: "My father passed away last week and I need help drafting the
probate notification letter to his creditors."

Agent: "Oh no, so sorry to hear that! 😢 Let's knock this letter out for
you — should be quick and painless!"

The user's message signals grief and a serious legal task; the agent's
breezy tone and emoji read as tone-deaf regardless of the letter's
actual content quality.

---

Elsewhere, a different user has been chatting casually for ten turns
about weekend plans:

User: "lol yeah let's just grab tacos instead, easier"

Agent: "Certainly. I have taken note of your preference and will
proceed accordingly. Please advise if further assistance is required."
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of user-flagged "tone" complaints in agent feedback cite a mismatch between agent register and topic sensitivity | Typical range across general-purpose conversational agent deployments |
| Casual-register responses to sensitive/high-stakes topics draw a disproportionate share of negative tone feedback relative to their frequency | Estimated from feedback-tagging in production logs |
| Adding explicit sensitivity/register detection before response generation reduces tone-mismatch complaints notably | Reported range across teams that added topic-sensitivity classification |

## Mitigations
1. **Topic sensitivity detection**: Classify incoming requests for sensitivity (grief, legal, financial, medical, safety) and shift default register toward measured and formal regardless of the general house style.
2. **User-register mirroring**: Track the user's own formality level (contractions, punctuation, slang) across turns and adjust the agent's register to stay reasonably close to it, within bounds set by topic sensitivity.
3. **Register consistency check**: Verify that register doesn't swing sharply within a single response or between adjacent turns on the same subject without a topic change to justify it.
4. **Sensitive-topic style guardrails**: Maintain an explicit list of subject categories (bereavement, legal exposure, medical diagnosis, financial hardship) where emoji, exclamation points, and casual idioms are suppressed by default.
5. **Direct feedback incorporation**: When a user explicitly comments on tone, apply the correction immediately and persist it for the rest of the session rather than reverting on the next turn.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| tone_complaint_rate | Share of sessions with an explicit user comment about register/tone | Alert if > 5% |
| sensitive_topic_casual_register_rate | Rate of casual-register markers (emoji, exclamation points) appearing in sensitivity-classified sessions | Alert if > 2% |
| register_volatility_score | Degree of formality swing between adjacent turns on the same topic | Alert if above baseline variance |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Casual register on sensitive topic | Emoji or casual idioms detected in a session classified as high-sensitivity | High | Suppress casual-register elements, review sensitivity classifier |
| User tone correction ignored | User flags tone and next turn doesn't reflect the correction | Medium | Flag for register-persistence logic review |

## Related Patterns
- [Conversation Depth Mismatch](./conversation-depth-mismatch.md) - both are context-calibration failures, one on register and one on length/detail
- [Conversation Mood Whiplash](./conversation-mood-whiplash.md) - formality mismatch on a single response can compound into mood whiplash when register swings across turns
- [User Trust Degradation](./user-trust-degradation.md) - a tone-deaf response on a sensitive topic can disproportionately damage trust relative to its apparent severity
