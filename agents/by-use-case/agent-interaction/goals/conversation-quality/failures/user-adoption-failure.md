# User Adoption Failure

## Issue
Users try the agent once or a handful of times during an initial evaluation period and then stop using it, not because of one catastrophic failure but because small friction points — clarification loops, wrong assumptions, mismatched depth, repetition — accumulate across those first sessions and cross a threshold where continuing feels not worth the effort. This is distinct from user-retention-decline, which describes an erosion among users who were already engaged long-term; adoption failure happens in the earliest sessions, before the user has formed any habit or sunk investment to make them tolerate friction.

**Frequency**: Common

**Symptoms**
- Sharp drop-off between first-session usage and any second or third session for a cohort of new users
- Exit surveys or support tickets from lapsed new users cite generic frustration ("didn't feel like it understood me," "too much back and forth") rather than one specific bug
- Time-to-first-value (first genuinely useful completed task) is long relative to competing tools or the user's initial patience budget
- New users' early sessions show elevated rates of clarification loops, corrections, or repetition compared to sessions from retained long-term users
- Product usage analytics show most churned new users never reached a second distinct task type

## Root Cause
New users have no accumulated trust or sunk cost to buffer against friction — a returning user might tolerate a clarification loop because they've had five good sessions before it, but a first-time user experiencing the same friction has nothing to weigh it against and concludes the tool doesn't work well. Early sessions are also disproportionately likely to expose conversation-quality failures because the user hasn't yet learned the phrasing patterns that avoid triggering them, and the agent has no history with this user to draw on for calibrating depth, tone, or assumptions. The result is that the failure modes most damaging to adoption are exactly the ones most concentrated in first sessions.

## Example
```
A new user signs up and tries the agent for a scheduling task in their
first session.

Session 1: Agent asks 4 clarifying questions for a request that had an
           obvious default, then produces an over-long, over-formal
           response to what was meant as a quick request. Task takes
           11 turns to complete what should have taken 2.

Session 2 (two days later): User tries a different task; agent makes a
           silent wrong assumption about scope and produces unusable
           output. User manually fixes it themselves outside the tool.

No session 3 occurs. Product analytics later shows this user's
first-session turn count and correction rate were both roughly double
the cohort average for users who went on to become regular users.
```

## Statistics
| Finding | Context |
|---------|---------|
| A large share of new-user churn in conversational agent products occurs after just one or two sessions, before any habitual use forms | Typical range across consumer and B2B conversational agent products |
| First-session correction/clarification rate is a strong negative predictor of second-session return in cohort analyses | Estimated from product analytics across multiple agent deployments |
| Reducing first-session friction (fewer unnecessary clarifications, better default calibration) measurably improves second-session return rate | Reported range across teams that specifically tuned first-session experience |

## Mitigations
1. **First-session friction budget**: Apply stricter thresholds for clarification and assumption-flagging in early sessions specifically, erring toward confident defaults over questions until the user has demonstrated engagement.
2. **Time-to-first-value tracking**: Explicitly measure and optimize for how quickly a new user reaches one genuinely completed, useful task, treating it as a distinct product metric from overall task accuracy.
3. **Onboarding-calibrated depth and tone**: Use conservative, broadly-applicable depth/formality defaults for first sessions rather than extremes in either direction, since there's no history yet to calibrate against.
4. **Early-session failure monitoring**: Instrument first- and second-session conversation-quality metrics (clarification rounds, corrections, repetition) separately from steady-state metrics, since this is the highest-leverage window for adoption.
5. **Progressive trust building**: Front-load a small number of easy, high-confidence wins in the earliest interactions rather than routing new users into ambiguous or high-stakes requests first.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| second_session_return_rate | Share of new users who return for a second distinct session | Alert if < baseline for cohort |
| first_session_friction_score | Composite of clarification rounds, corrections, and repetition in a user's first session | Alert if trending above retained-user baseline |
| time_to_first_value | Turns/time elapsed before a new user's first fully completed useful task | Alert if rising |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| New cohort adoption drop | second_session_return_rate for a new cohort falls notably below historical baseline | High | Audit recent first-session transcripts for friction patterns, review onboarding defaults |
| Elevated first-session friction | first_session_friction_score trending up | Medium | Review clarification/assumption thresholds for new-user sessions |

## Related Patterns
- [User Retention Decline](./user-retention-decline.md) - the analogous erosion pattern among already-engaged users, driven by accumulated friction over a longer horizon
- [User Expectation Mismatch](./user-expectation-mismatch.md) - a mismatch between marketed and actual capability is a common contributor to early-session disappointment and abandonment
- [Over-Clarification](./over-clarification.md) - a frequent concrete driver of first-session friction that disproportionately affects new-user adoption
