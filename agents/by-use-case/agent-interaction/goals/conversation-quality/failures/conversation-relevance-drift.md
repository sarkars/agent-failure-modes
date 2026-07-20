# Conversation Relevance Drift

## Issue
Across a multi-turn conversation, the subject matter gradually shifts away from the user's original goal, one small step at a time, until the conversation is addressing something meaningfully different from what the user came in for — without either party explicitly deciding to change topics. Each individual step feels like a natural continuation, but the cumulative drift means the original goal quietly falls out of scope and is never actually completed.

**Frequency**: Common

**Symptoms**
- The conversation's current focus, compared to the user's opening message, shows no direct line of relevance
- Original stated goal is never explicitly marked done, abandoned, or deferred — it simply stops being mentioned
- Each individual turn transition seems locally reasonable, but the multi-turn trajectory is clearly off-course in hindsight
- User has to say "wait, going back to my original question" to redirect the conversation
- Time/turns spent on the eventual current subtopic exceeds what was spent on the original request

## Root Cause
Each turn is generated to be a coherent response to the immediately preceding turn, not to the original request several turns back, so small legitimate tangents (a clarifying detail, a related side question) can each individually make sense while the chain of them walks the conversation away from the origin. Without an explicit anchor — a persistent restatement of the original goal that each new turn is checked against — the model has no counterweight pulling generation back toward it, and topical momentum from the last one or two turns dominates over the much earlier original framing.

## Example
```
Turn 1: User: "Help me figure out why our checkout page conversion rate
        dropped this month."

Turn 3: Agent, while investigating, notices the page load time is
        slow and starts discussing image optimization.

Turn 7: Discussion has moved to which CDN provider to use.

Turn 12: Discussion is now comparing CDN pricing tiers in general,
         unrelated to the checkout page specifically.

Turn 16: User: "Hold on — we never actually figured out why
         conversion dropped. Is it even related to page speed, or did
         we just start talking about CDNs because that came up once?"

Agent checks: page speed had in fact stayed flat over the period in
question; the actual conversion drop was caused by a broken coupon
code field, unrelated to anything discussed in turns 3-15.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 15-25% of long analytical/troubleshooting sessions show measurable topical drift away from the original stated goal by turn 15-20 | Typical range across investigative agent sessions |
| Sessions with drift take on average notably more turns to eventually resolve the original request, if resolved at all | Estimated from production session analysis |
| Periodic explicit goal re-anchoring reduces drift-related original-goal abandonment substantially | Reported range across teams that added goal-tracking checkpoints |

## Mitigations
1. **Persistent goal anchor**: Store the user's original stated goal verbatim and re-surface it at intervals, checking whether the current conversation focus still serves it.
2. **Tangent flagging**: When the agent notices its own reasoning moving to an adjacent topic, explicitly flag it ("this is related but a step away from your original question — continue or return to the main issue?") rather than silently following it.
3. **Goal-completion tracking**: Explicitly track whether the original request has been resolved, deferred, or abandoned, and surface unresolved status rather than letting it silently disappear from the conversation.
4. **Turn-relevance scoring**: Score each new turn's relevance to the original goal, and use a declining relevance trend as a trigger for a re-anchoring checkpoint.
5. **Scope boundary confirmation**: When a side investigation naturally opens up (e.g. discovering a plausible secondary cause), get explicit confirmation before committing multiple turns to pursuing it instead of the original question.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| original_goal_relevance_score | Similarity between current conversation focus and the original stated goal, tracked over turns | Alert if declining trend crosses threshold |
| unresolved_original_goal_rate | Share of sessions where the original stated goal is never explicitly marked resolved | Alert if > 20% |
| turns_before_redirect | Number of turns elapsed before a user redirect ("going back to...") occurs | Alert if median is low relative to session length |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Sustained relevance decline | original_goal_relevance_score trends down across 5+ consecutive turns without user-initiated topic change | Medium | Trigger goal re-anchoring checkpoint |
| Original goal abandoned | Session ends with original stated goal never marked resolved or explicitly deferred | Medium | Flag for review, consider follow-up prompt to user |

## Related Patterns
- [Conversation Tangent Proliferation](./conversation-tangent-proliferation.md) - drift is the gradual, single-direction version; tangent proliferation is multiple simultaneous branching side-threads
- [Conversation Coherence Loss](./conversation-coherence-loss.md) - drift changes what's discussed, coherence loss loses track of state within the same discussion; the two can compound
- [User Adoption Failure](./user-adoption-failure.md) - a pattern of unresolved original goals due to drift is one contributor to users abandoning the agent after initial trials
