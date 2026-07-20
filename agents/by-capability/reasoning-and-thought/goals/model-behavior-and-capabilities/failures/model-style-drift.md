# Model Style Drift

## Issue
An agent configured with a specific persona — tone, formality level, brand voice, characteristic phrasing — maintains that persona faithfully at the start of a session but gradually drifts toward a generic, default assistant voice as the conversation lengthens, without any instruction telling it to change. The drift is slow enough that no single turn looks obviously wrong, but a comparison of turn 2 to turn 40 shows a clearly different "character" giving the responses.

**Frequency**: Common

**Symptoms**
- Brand voice guidelines (e.g. "warm, playful, uses short sentences") are followed closely in early turns and fade into generic, longer, more formal assistant-style prose later in the session
- Distinctive persona markers (a catchphrase, a specific greeting style, an emoji pattern) that appear consistently early in a session become sporadic or disappear entirely later
- Users who screenshot early vs. late responses from the same session perceive them as coming from a different assistant
- Drift accelerates after the model handles a turn requiring a different register (e.g. a technical troubleshooting step), and the persona doesn't fully return afterward
- Re-injecting the persona instructions mid-session temporarily restores the original voice, then it fades again

## Root Cause
Persona instructions delivered once in a system prompt compete for influence against the accumulating conversational content the model also conditions on, and as in instruction-following decay generally, the system prompt's fixed-position influence shrinks relative to the growing transcript. Style is additionally a weaker, more diffuse training signal than factual instruction-following: the model was trained far more heavily on maintaining topical coherence and answering the immediate question than on maintaining a consistent voice across many turns, so when the two pull in different directions (answer this technical question accurately vs. stay playful and brief), correctness/helpfulness tends to win and the persona erodes. Once the model produces a few turns in a more neutral, default register — often triggered by a turn that doesn't naturally fit the persona, like a serious error message — subsequent turns condition on that neutral register as the new local pattern, making it self-reinforcing rather than self-correcting.

## Example
```
A retail brand deploys a shopping assistant with a system prompt persona:
"You are Pip, an upbeat, concise shopping buddy. Use short sentences,
occasional exclamation points, and never sound like a generic customer
service bot."

Turn 2: "Ooh nice choice! That jacket comes in navy and olive - want me
to check sizes for you?"

Turn 19, after several turns handling a return-policy question in a more
careful, precise register: "Based on our return policy, items must be
returned within 30 days of the delivery date, in original condition,
with the original packaging and tags attached."

By turn 19 the response reads as generic customer-service copy with no
trace of "Pip" - no exclamation points, no short sentences, no
brand-voice markers - despite the persona instruction still being present,
unchanged, in the system prompt sent with every call.
```

## Statistics
| Finding | Context |
|---------|---------|
| Measurable persona-marker frequency (catchphrases, tone markers) typically declines substantially between the first 5 turns and turns 25+ of a long session | Typical range observed in brand-voice consistency evaluations of long conversations |
| Turns requiring a shift in register (technical, apologetic, policy-citation) show the largest single-turn drop in persona-marker presence, and the persona often does not fully recover afterward | Estimated from turn-by-turn persona-adherence tracking |
| Periodic persona re-injection restores marker frequency close to session-start levels for a limited number of subsequent turns before drift resumes | Typical range observed in agent frameworks using scheduled re-injection |

## Mitigations
1. **Scheduled persona re-injection**: Re-send condensed persona instructions at a fixed turn interval rather than relying on a single system-prompt statement to hold for the whole session.
2. **Post-generation style pass**: Run a lightweight rewrite step on generated responses to restore brand-voice markers before returning them to the user, rather than trusting the generating call alone.
3. **Register-transition handling**: Explicitly instruct the model on how to handle register-shifting content (errors, policy text) while retaining persona markers, since these turns are where drift most often begins.
4. **Persona-adherence monitoring by turn depth**: Track a style-marker presence score across turn position in production to detect and quantify the drift curve, rather than assuming persona holds indefinitely.
5. **Session length caps with persona reset**: For persona-sensitive deployments, cap session length or reset/reinforce persona context after a defined threshold rather than letting drift compound indefinitely.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| persona_marker_presence_by_turn | Rate of defined style/voice markers present in responses, bucketed by turn position | Alert if late-session rate drops > 40% from early-session baseline |
| register_transition_recovery_rate | Rate at which persona markers return within N turns after a register-shifting turn | Alert if < 60% |
| user_perceived_consistency_score | Sampled user or reviewer rating of voice consistency across a session | Alert if trending downward release-over-release |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Persona drift threshold breached | persona_marker_presence_by_turn falls below floor for late-session turns | Medium | Trigger persona re-injection, review session for post-hoc style correction |
| No recovery after register shift | register_transition_recovery_rate drops for a specific transition type (e.g. after error messages) | Medium | Add explicit handling instructions for that transition type in the persona prompt |

## Related Patterns
- [Model Instruction Following Decay](./model-instruction-following-decay.md) - style drift is the stylistic manifestation of the same conversational-position dilution that degrades rule adherence generally
- [Model Context Length Behavior Change](./model-context-length-behavior-change.md) - both stem from the fixed-position system prompt losing relative influence as context grows
- [Model Fairness Bias](./model-fairness-bias.md) - both are gradual, cumulative behavioral shifts that are invisible turn-by-turn and only clear in aggregate or before/after comparison
