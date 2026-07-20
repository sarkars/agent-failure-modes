# Assumption Validation Failure

## Issue
The agent infers an unstated detail about what the user wants — a default value, a scope boundary, an intended recipient, a file format — and proceeds to act on that inference as if it were confirmed, instead of surfacing it as a guess. The user only discovers the assumption was wrong after seeing the output, at which point work has to be redone. This differs from under-clarification in that the agent isn't skipping an ambiguous request wholesale; it silently resolves one specific unstated variable inside an otherwise clear request and never tells the user it made a choice.

**Frequency**: Very Common

**Symptoms**
- Output is technically responsive to the literal request but wrong on a dimension the user never specified
- User's follow-up begins with "wait, I meant..." or "why did you assume..."
- Agent's reasoning trace shows a silent default chosen with no equivalent surfaced to the user
- Rework rate is higher for requests containing unstated parameters (audience, tone, scope, format) than for fully-specified ones
- The same unstated variable gets guessed differently across repeated similar requests, showing there was no real rule, just a coin flip

## Root Cause
Language models are trained to produce a complete, confident-sounding answer for almost any input, and picking a plausible default for an unstated slot is usually cheaper (in generated tokens and perceived helpfulness) than pausing to ask. Nothing in the typical agent loop distinguishes "the user told me this" from "I inferred this because it seemed likely" — both become facts baked into the plan before generation starts, with no separate confidence flag on the inferred ones. Because the assumption is never emitted as text, there is no point in the interaction where the user can catch it before the cost of being wrong is already sunk.

## Example
```
User: "Write a follow-up email to the client about the delayed shipment."

Agent silently assumes:
- "the client" = the primary contact from the last email thread (there are
  three contacts on this deal)
- tone = apologetic and formal
- delay reason = omit specifics, keep vague

Agent produces a full, polished email and sends a draft for review addressed
to the wrong contact (a junior buyer, not the decision-maker who actually
raised the complaint), in a tone the user considers too apologetic given the
delay was the client's own logistics partner's fault.

User: "This isn't right. That's not who complained, and we did nothing
wrong here — why are you apologizing?"

Agent had the information needed to ask before drafting (three contacts
existed, the fault was disputed in an earlier note) but never surfaced
either as an open question.
```

## Statistics
| Finding | Context |
|---------|---------|
| 25-35% of first-draft agent outputs on requests with an unstated parameter require revision solely due to a wrong assumption | Typical range across support/drafting agent deployments |
| Requests with 2+ unstated slots (recipient, tone, scope) show roughly double the single-turn rework rate of fully-specified requests | Estimated from production feedback logs |
| Surfacing assumptions inline ("I assumed X — let me know if that's wrong") cuts silent-assumption rework by 40-50% | Reported range across teams that added assumption-flagging |

## Mitigations
1. **Explicit assumption surfacing**: Require the agent to state any inferred (not directly given) parameter as a visible line in its output — "Assuming this goes to [contact]" — so the user can correct it before or alongside reviewing the result.
2. **Confidence-gated inference**: Only let the agent silently resolve an unstated slot when its confidence in the inference exceeds a high threshold; below that, ask or flag rather than guess.
3. **Reversible-cost checks**: For assumptions attached to high-cost or hard-to-reverse actions (sending, publishing, deleting), require confirmation regardless of inference confidence.
4. **Assumption logging for review**: Log every silently-resolved slot with its inferred value so patterns of bad defaults (wrong contact, wrong tone) can be found and fixed at the template/prompt level.
5. **Slot-level provenance tracking**: Tag each parameter in the agent's internal plan with its source (stated-by-user vs. inferred) so downstream code can render inferred ones differently instead of treating all parameters as equally certain.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| unflagged_assumption_rework_rate | Share of sessions where a correction follows an output containing a silent assumption | Alert if > 20% |
| assumption_surfacing_rate | Share of inferred slots that were explicitly stated to the user before/with output | Alert if < 60% |
| wrong_recipient_or_scope_rate | Rate of outputs corrected specifically for wrong target/scope (proxy for assumption errors) | Alert if > 10% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Silent assumption caused irreversible action | A send/publish/delete action executed on an unconfirmed inferred parameter, then corrected | High | Halt auto-send on inferred recipients, require confirmation, audit recent sends |
| Assumption surfacing rate drop | assumption_surfacing_rate falls below threshold over a rolling window | Medium | Review prompt/template for missing surfacing instruction |

## Related Patterns
- [Under-Clarification](./under-clarification.md) - assumption validation failure is under-clarification narrowed to a single unstated slot inside an otherwise clear request
- [User Expectation Mismatch](./user-expectation-mismatch.md) - repeated wrong assumptions compound into a broader mismatch between what users expect the agent to infer correctly
- [Conversation Contradiction](./conversation-contradiction.md) - correcting a bad assumption mid-conversation can itself trigger a contradiction if the agent doesn't reconcile its prior output
