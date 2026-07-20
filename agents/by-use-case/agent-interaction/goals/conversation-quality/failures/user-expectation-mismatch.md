# User Expectation Mismatch

## Issue
Marketing copy, onboarding flows, or the agent's own confident phrasing lead users to believe it can reliably do things it actually handles poorly or not at all — multi-step reasoning, real-time data access, persistent memory across sessions, domain expertise — and the gap surfaces as repeated disappointment each time the user's expectation collides with actual behavior. Unlike a single wrong answer, this is a structural mismatch: the user's mental model of the agent's capability boundary is simply wrong, so they keep hitting the same class of failure in different guises.

**Frequency**: Common

**Symptoms**
- Users repeatedly ask for capabilities the agent doesn't actually have, at a rate suggesting they don't know it lacks them
- Agent's own responses imply broader capability than it delivers (e.g. "I'll remember that" for a system with no persistent memory)
- Support tickets or complaints cluster around "it said it could do X" rather than "it did X wrong"
- Gap between capability as described in product materials and capability as observed in production usage
- Users express surprise, rather than mere disagreement, when a limitation surfaces — indicating they didn't know the boundary existed

## Root Cause
Product messaging and onboarding are typically written to maximize appeal and are updated on a slower cycle than the agent's actual capability, so marketing claims drift out of sync with reality as the underlying model or system changes. Compounding this, language models are fluent enough to phrase capability claims confidently regardless of whether the underlying capability is reliable — "I'll remember this for next time" is an easy sentence to generate whether or not persistent memory is actually implemented — so the agent itself becomes a second source of expectation-setting that isn't gated by what's actually true of the system.

## Example
```
Product page: "Your assistant remembers your preferences across every
conversation, so you never have to repeat yourself."

In practice, preference memory only persists within a single session and
resets between sessions due to a scoping decision made after the
marketing copy was last updated.

Session 1: User: "Please always format numbers with commas, not
           decimals-only." Agent: "Got it, I'll remember that for
           future conversations."

Session 4 (next day): User asks for a report; numbers come back
           unformatted. User: "I told you to always use commas — you
           said you'd remember!"

The agent's own phrasing ("I'll remember that for future
conversations") asserted a capability that doesn't exist, compounding
the marketing-level mismatch.
```

## Statistics
| Finding | Context |
|---------|---------|
| A substantial share of negative reviews for conversational agent products cite unmet expectations rather than incorrect outputs on attempted tasks | Typical range across consumer agent product feedback |
| Agent self-descriptions of capability ("I'll remember," "I can access real-time data") are a measurable source of complaints when the underlying capability is absent or limited | Estimated from support-ticket categorization in production deployments |
| Auditing and correcting agent self-description language against actual system capability reduces expectation-mismatch complaints notably | Reported range across teams that added capability-claim review |

## Mitigations
1. **Capability-claim auditing**: Regularly review both marketing copy and the agent's own generated language for capability claims (memory, real-time access, expertise) that don't match the actual implementation, and correct both.
2. **Honest limitation disclosure**: Have the agent state limitations explicitly and proactively when a request brushes against a known boundary ("I don't retain this after this session ends") rather than implying broader capability.
3. **Marketing-engineering sync cadence**: Establish a review cycle tying product messaging updates to actual capability changes, so claims don't silently drift out of sync as the system evolves.
4. **Capability-claim gating in generation**: Constrain the model from generating confident capability assertions (e.g. "I'll remember") unless the underlying system can actually guarantee them.
5. **Expectation-gap complaint tracking**: Specifically categorize and track complaints that indicate a capability misunderstanding (versus a quality issue on an attempted task) to identify which claims need correction first.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| expectation_gap_complaint_rate | Share of complaints citing unmet capability expectations rather than execution quality | Alert if > 15% |
| unsupported_capability_claim_rate | Rate at which agent responses assert a capability not actually guaranteed by the system | Alert if > 5% |
| repeat_request_for_unsupported_capability | Rate of users repeatedly requesting a capability the system doesn't have | Alert if trending up |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Agent asserts unsupported capability | Response language claims a capability (memory, real-time data) not backed by the system | High | Correct generation constraints, audit related prompts |
| Spike in expectation-gap complaints | expectation_gap_complaint_rate rises for a specific capability area | Medium | Review and update marketing/onboarding copy for that area |

## Related Patterns
- [User Adoption Failure](./user-adoption-failure.md) - expectation mismatches discovered early are a common concrete driver of new users abandoning the product
- [User Trust Degradation](./user-trust-degradation.md) - repeated capability overclaims erode trust in a way that compounds beyond the individual mismatch incident
- [Conversation Contradiction](./conversation-contradiction.md) - an agent asserting a capability it then fails to deliver on is a specific form of self-contradiction over time
