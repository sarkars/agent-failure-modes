# Domain Context Loss

## Issue
An agent correctly establishes domain-specific context early in a session — the specialty, jurisdiction, or technical stack it should reason within — but loses track of it as the conversation grows, silently reverting to generic, domain-agnostic behavior. The regression isn't triggered by the user changing topics; it happens because the domain-framing information falls out of the effective context window or gets diluted by intervening turns, and nothing in the agent's architecture re-asserts it.

**Frequency**: Common

**Symptoms**
- Early turns show correctly domain-specialized responses; later turns in the same session revert to generic advice
- Agent re-asks for information (specialty, jurisdiction, version) that was already established earlier in the session
- Domain-specific terminology or conventions used correctly at first, then abandoned mid-session for generic phrasing
- No explicit topic change by the user precedes the regression

## Root Cause
Domain framing established via a system prompt, an early user turn, or a retrieved document is typically just one more span of tokens in the context window, with no persistent, structurally-protected representation. As the conversation accumulates turns, that framing competes for attention with everything said since, and in long sessions it can be pushed far enough back — or diluted by enough intervening generic exchange — that the model's effective behavior drifts back toward its domain-agnostic prior. Systems that don't re-inject or periodically re-affirm the established domain context have no mechanism to prevent this decay; the loss is silent because nothing errors, the agent just quietly answers a different, more generic question than the one actually being asked.

## Example
```
Turn 1: User establishes context: "I'm a nurse practitioner working in a
US pediatric ICU. I need dosing and protocol guidance scoped to that
setting."
Agent responds correctly, scoping guidance to pediatric ICU protocols
and flagging population-specific cautions.

Turns 2-14: Conversation continues across many related but tangential
questions (staffing schedules, documentation templates, general
communication tips).

Turn 15: User asks "what's the standard approach for fluid resuscitation
here?"
Agent responds with generic adult-population fluid resuscitation
guidance, with no pediatric-specific caveats and no acknowledgment of
the ICU setting established 14 turns earlier — the domain framing has
fallen out of effective context and the agent is now answering as if
this were a first, unscoped question.
```

## Statistics
| Finding | Context |
|---------|---------|
| Domain-context adherence measured across long sessions (20+ turns) drops by an estimated 15-30% relative to sessions under 5 turns | Typical range observed in long-session agent evaluations |
| Periodic re-injection of domain framing (every N turns or via a persistent system-level anchor) recovers most of the lost adherence | Reported range across teams testing context-refresh strategies |
| Sessions with a structurally pinned domain-context block (outside the rolling conversation window) show markedly lower drift than sessions relying on the original turn alone | Typical pattern observed in production long-session agent telemetry |

## Mitigations
1. **Persistent domain-context pinning**: Store established domain framing in a structurally separate, always-included context slot (not subject to normal turn-window truncation) rather than relying on it surviving as an ordinary early turn.
2. **Periodic context re-affirmation**: On a fixed cadence (every N turns or every context-window refresh), re-inject a compact summary of established domain context into the active prompt.
3. **Drift detection via response auditing**: Periodically sample agent responses against the established domain profile and flag when output stops reflecting expected domain specialization.
4. **Explicit domain-state object**: Maintain domain context as structured session state (specialty, jurisdiction, version) queried at generation time, rather than as unstructured prose the model must recall from the transcript.
5. **User-visible context confirmation**: Surface the agent's current understanding of domain context periodically ("still assuming pediatric ICU setting — confirm?") so silent drift becomes visible and correctable.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| domain_terminology_consistency_score | Automated measure of domain-specific terminology usage across a session's turns | Alert if score drops > 30% from session start to current turn |
| context_reestablishment_rate | Rate at which agent re-asks for domain info already provided earlier in session | Alert if > 3% of sessions past turn 10 |
| session_length_at_drift_onset | Distribution of turn count at which drift is first detected | Track trend; alert if median drops below prior baseline |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Domain drift detected mid-session | Automated audit flags response as inconsistent with session's established domain profile | Medium | Re-inject domain context into active prompt, flag session for review |
| Repeated context re-ask | Agent requests already-provided domain info twice in one session | Low | Surface bug ticket for context-pinning gap, no immediate user-facing action needed |

## Related Patterns
- [Knowledge Temporal Context Lost](./knowledge-temporal-context-lost.md) - shares the "qualifying context silently dropped" mechanism, applied to time-scoping rather than domain-scoping
- [Knowledge Scope Assumption Wrong](./knowledge-scope-assumption-wrong.md) - both involve losing track of applicable scope, one through decay and one through incorrect initial assumption
- [Fact Context Loss](./fact-context-loss.md) - the same underlying "qualifier dropped from context" mechanism at the level of a single fact rather than a whole session
