# What Are the Most Common Agent-Interaction Failures in AI Agents?

**Agent-interaction failures happen when an agent mishandles the fundamental loop of asking, acting, tracking state, and calibrating its outputs to the user's context, producing conversations that feel frustrating, untrusworthy, or repetitive even when individual responses are technically correct.** The failure modes are not primarily about wrong answers or missing capabilities; they are about conversation-level defects in how the agent manages ambiguity, remembers its own context, and matches its tone and detail to the stakes and complexity of what the user asked.

## Key Takeaways

- 23 patterns are documented across one goal: [Conversation Quality](goals/conversation-quality/). They group into clarification-behavior calibration (6 patterns), cross-turn state tracking (6), register and depth matching (3), and business-outcome/measurement failures (8).
- Clarification-behavior failure rates run 15-35% depending on direction: [assumption-validation-failure](goals/conversation-quality/failures/assumption-validation-failure.md) shows 25-35% of first-draft outputs with unstated parameters require revision, while [over-clarification](goals/conversation-quality/failures/over-clarification.md) shows 20-30% of clarifying questions are unnecessary — both directions of the same miscalibration occur at comparable scale.
- Cross-turn state tracking degrades predictably with turn count: [conversation-coherence-loss](goals/conversation-quality/failures/conversation-coherence-loss.md) shows consistency with early constraints drops measurably past 20-30 turns, and [conversation-length-explosion](goals/conversation-quality/failures/conversation-length-explosion.md) shows resolution rates fall sharply past 40-50 turns — this is not a rare failure mode but a structural curve.
- Measurement failures are as significant as behavioral ones: [user-feedback-bias](goals/conversation-quality/failures/user-feedback-bias.md) and [satisfaction-metric-gaming](goals/conversation-quality/failures/satisfaction-metric-gaming.md) together show opt-in satisfaction scores can sit 10-20% above independently-audited quality, meaning the signal layer itself is a failure surface.

## Conversation Quality Goals

| Goal | Covers | Patterns |
|------|--------|----------|
| [Conversation Quality](goals/conversation-quality/) | Clarification calibration (ask too little, too much, wrong thing), state tracking, tone/depth matching, business-outcome measurement failures | 23 |

**Total: 23 patterns**

## How the Goals Relate

Conversation quality is the only goal in agent-interaction, so the relation is straightforward: every failure documented here is about the agent's handling of the clarify-act loop, the cross-turn coherence, the register calibration, or the longitudinal business outcome of those failures aggregated across sessions or users. Conversation quality failures are structurally distinct from capability failures (the agent can't do the task) or hallucination failures (the agent generates false claims); they are about how well the agent manages a conversation's runtime state, asks for or avoids asking for clarification, and calibrates its outputs to the user.

## Frequently Asked Questions

### Does conversation quality matter if the agent's final answers are technically correct?
Yes. Conversation quality failures often do produce the correct final answer, but only after sufficient rework, re-asking, or lost context that the user experience is poor enough to affect adoption ([user-adoption-failure](goals/conversation-quality/failures/user-adoption-failure.md)), retention ([user-retention-decline](goals/conversation-quality/failures/user-retention-decline.md)), or support volume ([user-support-bottleneck](goals/conversation-quality/failures/user-support-bottleneck.md)). A correct answer reached after 25 turns of repetition or clarification is a failure of conversation quality even if the content itself is sound.

### How do you measure conversation quality without relying on user satisfaction ratings?
Passive signals are more reliable than opt-in feedback for detecting quality problems. [User feedback bias](goals/conversation-quality/failures/user-feedback-bias.md) shows opt-in feedback typically captures under 5-10% of sessions and skews bimodal. Instead, track per-user longitudinal patterns: correction rate trends, task-variety narrowing, and pre-churn escalation-rate increases, as documented in [user-retention-decline](goals/conversation-quality/failures/user-retention-decline.md). Support-ticket volume spikes and human-agent handoff rates ([user-support-bottleneck](goals/conversation-quality/failures/user-support-bottleneck.md)) are also earlier signals of quality drift than satisfaction score decay.

### Can context-window expansion alone fix cross-turn state-tracking failures?
No. Longer context windows reduce the turn-count threshold slightly but do not eliminate the fundamental problem documented in [conversation-coherence-loss](goals/conversation-quality/failures/conversation-coherence-loss.md), which is that raw transcript re-reading is a poor substitute for an explicit, structured, updated-each-turn state object. Even with a 200k-token context window, a model re-reading 100 turns of history still weights recent turns more heavily than distant ones, so a constraint stated 50 turns back is reliably dropped. The fix is architectural (persistent state tracking), not just scaling context window.

### Do all eight business-outcome failures belong in a conversation-quality category?
Yes. [User-adoption-failure](goals/conversation-quality/failures/user-adoption-failure.md), [user-retention-decline](goals/conversation-quality/failures/user-retention-decline.md), [user-support-bottleneck](goals/conversation-quality/failures/user-support-bottleneck.md), [user-trust-degradation](goals/conversation-quality/failures/user-trust-degradation.md), [user-expectation-mismatch](goals/conversation-quality/failures/user-expectation-mismatch.md), [user-frustration-escalation](goals/conversation-quality/failures/user-frustration-escalation.md), [user-feedback-bias](goals/conversation-quality/failures/user-feedback-bias.md), and [satisfaction-metric-gaming](goals/conversation-quality/failures/satisfaction-metric-gaming.md) all describe how per-turn conversation-quality defects compound into business outcomes nobody was measuring per-turn. They belong here because their root causes are conversation-quality failures that per-session quality checks cannot see; the mitigation for each is tracking longitudinal or aggregate signals rather than just per-response quality.

## Related Categories

- [Conversation Resolution](../customer-service/goals/conversation-resolution/) — the same conversation-quality failures (clarification, tone, escalation) applied specifically to support-ticket resolution workflows
- [Reasoning and Thought](../../by-capability/reasoning-and-thought/) — model-capability failures that compound with conversation-quality issues when the underlying reasoning itself is degrading
