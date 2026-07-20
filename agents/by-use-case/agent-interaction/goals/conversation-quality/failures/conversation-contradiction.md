# Conversation Contradiction

## Issue
The agent states something in one turn and then states something incompatible with it later in the same conversation, without acknowledging the change or reconciling the two claims. This erodes trust independent of whether either individual statement was correct, because the user cannot tell which one to believe. Unlike coherence loss, which is about losing track of state generally, contradiction is a specific, checkable failure: two concrete claims made by the same agent in the same session are logically incompatible.

**Frequency**: Common

**Symptoms**
- Agent gives a numeric answer, recommendation, or factual claim in one turn that conflicts with an earlier turn's claim on the same question
- No acknowledgment of the change when the later claim is made ("earlier I said X, but actually...")
- User has to point out the contradiction before the agent addresses it
- Agent's own confidence language ("definitely," "for sure") is present on both the original and the contradicting claim
- Two contradicting claims trace to different underlying reasoning paths or tool calls that were never reconciled with each other

## Root Cause
Each generation turn is conditioned on the full transcript but the model does not perform an explicit consistency check against its own prior claims before emitting new ones — it generates the locally most plausible continuation of the current turn's prompt, and if that turn draws on a different tool result, a different framing, or a different piece of retrieved context than the earlier turn did, the two outputs can diverge without any internal signal that a conflict occurred. There is no default mechanism that diffs a new claim against the set of claims already made in the conversation before sending it.

## Example
```
Turn 5:  User: "How many seats does our Pro plan include?"
Turn 6:  Agent: "The Pro plan includes 10 seats."

Turn 22: User: "If I upgrade to Pro, can I add 12 people?"
Turn 23: Agent: "Yes, the Pro plan supports up to 15 seats, so 12 people
         would fit comfortably."

Turn 24: User: "Wait, you told me 10 seats earlier. Which is it?"
Turn 25: Agent: "You're right, sorry for the confusion — it's 15 seats."
         (no explanation of why turn 6 said 10, and no verification of
         which number is actually correct)
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 8-15% of long agent sessions (30+ turns) contain at least one detectable factual contradiction | Typical range observed in production transcript audits |
| Contradictions involving numeric or policy claims are corrected by users at a notably higher rate than stylistic inconsistencies | Estimated from support-agent transcript review |
| Adding an explicit prior-claims consistency check before response finalization reduces detected contradictions substantially | Reported range across teams that added claim-tracking |

## Mitigations
1. **Claim ledger**: Maintain an explicit running log of factual claims (numbers, policies, recommendations) made during the session, and check new claims against it before responding.
2. **Source-of-truth binding**: For claims backed by an external source (a database, a doc, a tool result), always re-fetch or re-cite the same source rather than letting the model regenerate the fact from memory on a later turn.
3. **Contradiction self-check pass**: Before finalizing a response, run a lightweight check comparing the new claim against tracked prior claims on the same entity/question, and surface a reconciliation note if they differ.
4. **Explicit correction framing**: When a genuine update is warranted (new information, corrected earlier error), require the agent to say so explicitly rather than stating the new claim as if it were the first time.
5. **Confidence-calibrated claims**: Avoid uniformly confident phrasing for claims not backed by a verified source, so contradictions are less likely to both sound equally authoritative.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| detected_contradiction_rate | Share of sessions containing two incompatible claims on the same question | Alert if > 5% |
| unacknowledged_correction_rate | Share of contradictions where the agent doesn't explicitly flag the change when it happens | Alert if > 50% |
| user_flagged_contradiction_rate | Rate at which users explicitly call out a contradiction | Alert if trending up |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Contradiction on policy/numeric claim | Two incompatible factual claims detected on the same entity within a session | High | Trigger claim reconciliation, verify against source of truth, notify user |
| Repeated unacknowledged contradictions | Session contains 2+ unflagged contradictions | Medium | Flag session for review, check claim-ledger implementation |

## Related Patterns
- [Conversation Coherence Loss](./conversation-coherence-loss.md) - a common upstream cause, since forgotten state often produces a contradicting restatement
- [User Trust Degradation](./user-trust-degradation.md) - contradictions are one of the fastest-acting contributors to eroding user trust
- [Assumption Validation Failure](./assumption-validation-failure.md) - an unflagged assumption revised later without acknowledgment can surface as a contradiction
