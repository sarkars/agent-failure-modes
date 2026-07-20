# Conversation Length Explosion

## Issue
A conversation that should resolve in a handful of turns instead grows to dozens or hundreds of turns without reaching a conclusion, driven by the agent's own behavior — asking follow-ups instead of finalizing, re-explaining instead of confirming, or generating verbose responses that themselves prompt more back-and-forth. Cost (both token spend and user time) grows roughly linearly or worse with turn count while the probability of resolution per additional turn keeps falling, meaning the conversation is on a bad trendline that nothing forces it off.

**Frequency**: Occasional

**Symptoms**
- Turn count for a given task category trends upward over time without a corresponding increase in resolution rate
- Long sessions show declining information-density per turn — later turns add less new content than earlier ones
- Token/cost-per-resolved-task rises disproportionately for the subset of sessions that run long
- No explicit checkpoint in the conversation ever proposes closing out or summarizing progress
- Users abandon long-running sessions at a higher rate than short ones, without an explicit resolution

## Root Cause
Nothing in a typical turn-by-turn agent loop tracks cumulative conversation cost or diminishing returns — each turn is generated to be locally helpful in response to the immediately preceding message, with no global objective pushing toward closure. This is compounded when the agent's own outputs are verbose or introduce new open threads (offering options, asking optional follow-ups) that generate more surface area for further turns than they resolve. Without an explicit signal that tracks "are we converging" and a mechanism to force closure once convergence stalls, a conversation can drift indefinitely as long as each individual turn looks reasonable in isolation.

## Example
```
A user asks the agent to help debug a failing test. The conversation runs
85 turns:

Turns 1-15: legitimate debugging, narrowing down to a timing issue.
Turns 16-40: agent proposes a fix, it partially works, agent proposes a
　　　　　　　slightly different variant, repeat, each variant introduced
　　　　　　　with a fresh paragraph of options and caveats rather than a
　　　　　　　decisive next step.
Turns 41-60: agent starts asking clarifying questions about environment
　　　　　　　details already established in turns 3-5, re-litigating
　　　　　　　settled ground because it never checkpointed what was known.
Turns 61-85: conversation is now mostly the agent hedging between three
　　　　　　　proposed fixes without picking one, and the user repeating
　　　　　　　"just try option 2" in different words each time.

The test is eventually fixed by the user working around the agent
directly. Total session cost is roughly 8x what a 12-turn resolution
would have cost.
```

## Statistics
| Finding | Context |
|---------|---------|
| Sessions exceeding roughly 40-50 turns show markedly lower resolution rates than shorter sessions in the same task category | Typical range observed in production agent telemetry |
| Cost-per-resolved-task for the longest-running decile of sessions can run several times the median | Estimated from token-spend analysis across long-tail sessions |
| Introducing an explicit turn-budget checkpoint with forced summarization improves resolution rate for long sessions measurably | Reported range across teams that added session-length monitoring |

## Mitigations
1. **Turn-budget checkpoints**: At fixed intervals (e.g. every 15-20 turns), force the agent to summarize progress, restate the remaining open question, and propose a concrete next decisive step rather than continuing to generate open-ended options.
2. **Convergence tracking**: Measure whether each turn is narrowing the solution space (fewer open questions, more confirmed facts) and flag sessions where convergence has stalled for review or intervention.
3. **Decisive-action bias late in session**: As turn count grows, bias the agent toward committing to a single best option and executing it rather than continuing to present alternatives.
4. **Settled-fact tracking**: Maintain a running list of already-established facts so the agent doesn't re-ask or re-explain them, which independently reduces turn count.
5. **Cost-aware session monitoring**: Surface cumulative token/time cost to the user or a supervising process once a session crosses a threshold, prompting an explicit decision to continue, escalate, or close out.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| turns_to_resolution | Number of turns before a session reaches a resolved/closed state | Alert if median > 20 for a task category |
| long_session_resolution_rate | Resolution rate for sessions exceeding 40 turns | Alert if < 50% of short-session resolution rate |
| cost_per_resolved_task_p90 | 90th percentile token/cost spend per resolved task | Alert if > 3x median |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Session exceeds turn budget without resolution | Turn count crosses checkpoint threshold with no resolved state | Medium | Trigger forced summarization/checkpoint, offer escalation to human |
| Runaway cost session | Cumulative session cost exceeds a multiple of category median with no resolution | High | Alert on-call, review session for loop/non-convergence |

## Related Patterns
- [Clarification Loop Infinite](./clarification-loop-infinite.md) - a specific mechanism (endless questioning) that is one common driver of overall length explosion
- [Conversation Repetition](./conversation-repetition.md) - re-explaining settled facts inflates turn count without adding information, a direct contributor to length explosion
- [User Frustration Escalation](./user-frustration-escalation.md) - unresolved long-running sessions are a strong predictor of rising user frustration
