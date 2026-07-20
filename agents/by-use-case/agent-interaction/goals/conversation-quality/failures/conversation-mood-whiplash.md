# Conversation Mood Whiplash

## Issue
The agent's emotional tone swings sharply and without cause between adjacent turns — upbeat and enthusiastic in one response, curt or apologetic-and-somber in the next, then breezy again — even though nothing in the conversation's content justifies the shift. Unlike formality mismatch, which is a single response miscalibrated to context, mood whiplash is specifically about the jarring delta between consecutive turns; the tone itself might be individually defensible each time, but the swing feels erratic and makes the agent seem unstable or inattentive to the user.

**Frequency**: Occasional

**Symptoms**
- Adjacent responses show sharply different emotional registers (excited → flat → apologetic) without a topic or context change that explains it
- Agent over-apologizes in one turn then reverts to cheerful boilerplate in the next as if the apology never happened
- Users comment that the agent's tone feels "erratic," "all over the place," or "like talking to a different person"
- Tone swings correlate with unrelated factors (e.g. which template or sub-model handled a given turn) rather than conversation content
- Sentiment analysis of consecutive agent turns shows high variance uncorrelated with user sentiment or topic shifts

## Root Cause
Each turn's tone is generated largely independently, conditioned on the immediate prompt and any surface-level cues (an error message, a success confirmation, a user complaint) without a persistent "current emotional register" being tracked and smoothed across turns. When a workflow involves different sub-components (a cheerful onboarding template, a terse error-handling branch, an apologetic retry message) stitched into one conversation, the composite tone can lurch between them because there's no continuity layer enforcing gradual, contextually justified transitions rather than abrupt resets.

## Example
```
Turn 1: User: "Can you help me set up autopay for my account?"
Agent:  "Awesome, let's get autopay set up for you! This'll just take
        a sec! 🎉"

Turn 2: (a validation error occurs on the linked bank account)
Agent:  "Unable to process. Error code 402. Please try a different
        payment method."

Turn 3: (user retries successfully)
Agent:  "So sorry about that hiccup earlier — I really apologize for
        any inconvenience this may have caused you today."

Turn 4: Agent: "Anyway, autopay is all set! You're going to love how
        easy this makes things! 🎉"

The swing from celebratory, to clinically terse, to heavily apologetic,
back to celebratory across four turns handling one simple task reads as
erratic rather than responsive.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 5-10% of multi-turn sessions touching an error or retry path show a detectable sharp tone reversal in the following turn | Typical range across transactional conversational agents |
| Sentiment-variance between consecutive agent turns is measurably higher in sessions stitched from multiple templates/handlers than in single-flow sessions | Estimated from tone-analysis of production transcripts |
| Adding a tone-continuity smoothing layer reduces flagged whiplash incidents notably | Reported range across teams that added cross-turn tone tracking |

## Mitigations
1. **Persistent tone state**: Track a running "current register" value across the conversation and require new turns to transition gradually from it rather than resetting to a per-turn default.
2. **Template tone harmonization**: When a conversation spans multiple templates or handlers (success messages, error messages, retries), author them to share a consistent baseline register rather than each being tuned in isolation.
3. **Contextual apology calibration**: Reserve heavy apology language for genuinely significant failures, and avoid combining it in adjacent turns with unrelated celebratory language for a minor, already-resolved hiccup.
4. **Sentiment-delta monitoring**: Measure the tone delta between consecutive agent turns and flag conversations where it exceeds a reasonable bound for review.
5. **Single-voice system prompting**: Explicitly instruct the underlying model to maintain one consistent persona/tone across the session rather than adapting per-turn based only on the immediate event.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| turn_to_turn_sentiment_delta | Magnitude of tone/sentiment change between consecutive agent turns | Alert if avg > defined variance threshold |
| whiplash_flagged_session_rate | Share of sessions with a user comment about erratic tone | Alert if > 3% |
| template_stitched_tone_variance | Sentiment variance specifically in sessions crossing multiple response templates/handlers | Alert if notably higher than single-template sessions |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sharp tone reversal detected | Sentiment delta between consecutive turns exceeds threshold | Medium | Flag session, review template/handler tone consistency |
| User flags erratic tone | Explicit user comment about inconsistent tone | Low | Log for persona/prompt tuning review |

## Related Patterns
- [Conversation Formality Mismatch](./conversation-formality-mismatch.md) - a single miscalibrated response; repeated or extreme mismatches across turns produce whiplash
- [Conversation Coherence Loss](./conversation-coherence-loss.md) - both stem from insufficient cross-turn state tracking, one for facts and one for tone
- [User Trust Degradation](./user-trust-degradation.md) - erratic tone contributes to a sense of unreliability that compounds trust erosion over time
