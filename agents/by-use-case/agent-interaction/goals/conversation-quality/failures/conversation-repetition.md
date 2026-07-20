# Conversation Repetition

## Issue
The agent restates information, asks a question, or repeats an instruction that it (or the user) already covered earlier in the same conversation, as if encountering it for the first time. This differs from coherence loss in scope: repetition is the narrow, directly observable symptom — the same content appearing twice — whereas coherence loss is the broader state-tracking failure that often, but not always, produces it (a single instance of repetition can also come from a template default firing regardless of history).

**Frequency**: Very Common

**Symptoms**
- Agent asks a question whose answer was already given earlier in the conversation
- Agent re-states a fact, caveat, or instruction verbatim or near-verbatim from an earlier turn
- Boilerplate disclaimers or setup text repeat every turn even after being acknowledged once
- User responses shift toward "I already told you..." or "you just said that"
- Repeated content adds no new information relative to the first occurrence

## Root Cause
Repetition typically comes from one of two mechanisms: either the model regenerates content from a static template or system instruction on every turn without checking whether it was already said (e.g. a standard disclaimer re-appended each response regardless of prior turns), or the model fails to retrieve/weight an earlier turn's content strongly enough during generation and independently re-derives the same question or statement as if starting fresh. Both share the same missing safeguard — there's no check comparing candidate output against what has already been said in the conversation before finalizing a response.

## Example
```
Turn 2:  User: "My account email is jsmith@example.com."
Turn 3:  Agent: "Got it, using jsmith@example.com."

Turn 9:  Agent: "Before I proceed, could you confirm the email
         associated with your account?"

Turn 10: User: "I gave you that seven turns ago — it's
         jsmith@example.com."

Turn 14: Agent: "Just to note, refunds typically take 5-7 business
         days to process."
Turn 19: Agent, discussing a different aspect of the same refund:
         "Just to note, refunds typically take 5-7 business days to
         process." (identical caveat, no new context justifying the
         repeat)

Turn 20: User: "You've told me that twice now, can we move on?"
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 10-20% of sessions exceeding 15 turns contain at least one instance of the agent asking for information already provided | Typical range across production conversational agent logs |
| Repeated boilerplate/disclaimer text appears in a majority of multi-turn sessions using static per-turn templates without a "already stated" check | Estimated from template-based agent deployments |
| Adding a said-before check before finalizing a response reduces flagged repetition incidents substantially | Reported range across teams that added conversation-content deduplication |

## Mitigations
1. **Said-before check**: Before finalizing a response, compare candidate content (questions, facts, disclaimers) against a record of what has already been stated in the conversation, and suppress or rephrase exact/near-duplicates.
2. **Slot-filled memory for collected inputs**: Once a piece of information (email, account ID, preference) is provided, store it in structured session state so the agent reads from state rather than re-asking.
3. **One-time boilerplate**: Mark template disclaimers/setup text as "state once per session" rather than "include every response," with an explicit trigger if circumstances change enough to warrant a repeat.
4. **Repetition-aware response generation**: Include a compact summary of already-stated key facts and questions directly in the prompt context so the model has an explicit signal of what not to repeat.
5. **User-flagged repetition fast path**: When a user says "you already told me" or similar, treat it as ground truth immediately rather than re-verifying, and suppress that content for the rest of the session.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| repeated_question_rate | Share of sessions where the agent asks for already-provided information | Alert if > 10% |
| duplicate_content_rate | Share of turns containing near-duplicate text of an earlier turn in the same session | Alert if > 15% |
| user_repetition_complaint_rate | Rate of explicit user statements like "I already told you" | Alert if > 5% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Repeated request for provided information | Agent asks for a value already present in session state | Medium | Trigger state-lookup fix, log for slot-filling review |
| User flags repetition | Explicit "already told you" style user statement detected | Low | Log session, review said-before check coverage |

## Related Patterns
- [Conversation Coherence Loss](./conversation-coherence-loss.md) - a frequent root cause of repetition, since forgotten state leads directly to re-asking or re-stating
- [Conversation Length Explosion](./conversation-length-explosion.md) - repeated content inflates turn count without adding information, contributing directly to unbounded conversation growth
- [Over-Clarification](./over-clarification.md) - repeated questions are a specific case of over-clarification when the repeated content is itself a clarifying question
