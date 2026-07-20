# Disambiguation Strategy Ineffective

## Issue
When a request is genuinely ambiguous, the agent has some strategy for resolving it — asking a question, picking the most likely interpretation, presenting options — but the strategy itself is a poor fit for the type of ambiguity present, so the ambiguity survives the resolution attempt. This is a broader, strategy-level pattern than clarification-irrelevant (a single wrong question): it covers any mismatched approach, including choosing to guess when asking was needed, presenting an unusable list of options, or asking when a simple default would have sufficed.

**Frequency**: Occasional

**Symptoms**
- The chosen disambiguation approach (ask, guess, present-options) doesn't match the ambiguity's actual shape (e.g. presenting 8 options when 2 would do, or silently guessing when the interpretations have very different consequences)
- Ambiguity resurfaces later in the conversation despite an apparent resolution step having occurred
- Users abandon or ignore the presented disambiguation options because none is clearly framed as the likely one
- The same category of ambiguous request is handled with a different, inconsistent strategy each time it recurs
- Resolution step consumes conversational effort disproportionate to how much it actually narrows the interpretation space

## Root Cause
Disambiguation strategy is often chosen by default or by whichever prompt pattern the agent was trained/tuned on, rather than being selected based on the properties of the ambiguity itself — how many plausible interpretations exist, how differently they'd affect the outcome, and how confident the agent is in a leading guess. A single fixed strategy (always ask, always guess-and-flag, always list options) will be well-matched to some ambiguities and poorly matched to others; without an explicit strategy-selection step that reasons about the ambiguity's shape before choosing how to resolve it, mismatches are structurally common rather than occasional.

## Example
```
User: "Cancel my subscription."

The account has two active subscriptions: a $9/month newsletter tier
and a $49/month platform tier. These have very different consequences
if the wrong one is cancelled, so this ambiguity calls for a direct,
binary question.

Agent's chosen strategy instead: present a long options menu covering
every conceivable subscription-related action ("Cancel immediately,
Cancel at period end, Downgrade, Pause, Cancel and refund, Cancel one
of multiple plans...") without first isolating which plan is meant.

User: "I don't need a whole menu, I just have two subscriptions —
which one did you mean?"

The strategy (broad menu) didn't match the ambiguity (a simple binary
choice between two specific known plans), wasting a turn and still not
resolving anything.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-30% of ambiguity-resolution attempts fail to actually narrow the interpretation space on the first try | Typical range across production agent transcripts |
| Binary/small-set ambiguities resolved with an open-ended question or oversized menu show notably lower first-attempt resolution rates than those matched with a direct choice | Estimated from transcript analysis by ambiguity type |
| Explicit strategy-selection logic based on interpretation-count and stakes improves first-attempt resolution meaningfully | Reported range across teams that added ambiguity-shape classification |

## Mitigations
1. **Ambiguity-shape classification**: Before choosing how to resolve ambiguity, classify it by number of plausible interpretations and their consequence-divergence, and select a strategy (direct question, small option set, confident guess with flag) that fits that shape.
2. **Strategy-outcome tracking**: Log which disambiguation strategy was used per ambiguity type and whether it resolved on the first attempt, and use this to refine strategy selection over time.
3. **Bounded option presentation**: When presenting options, cap the list to the actual plausible candidates (not an exhaustive menu) and rank by likelihood so the user isn't asked to search a long list.
4. **Consequence-weighted default to asking**: For ambiguities where interpretations have significantly different real-world consequences, bias toward direct confirmation even when a guess-and-flag strategy would normally be used for lower-stakes cases.
5. **Consistency enforcement per request type**: For recurring request categories (e.g. "cancel my subscription"), standardize on a known-effective disambiguation strategy rather than re-deriving one ad hoc each time.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| first_attempt_resolution_rate | Share of disambiguation attempts that resolve the ambiguity without a further round | Alert if < 70% |
| strategy_type_variance | Consistency of disambiguation strategy used for the same recurring request category | Alert if high variance detected |
| oversized_option_set_rate | Rate at which presented option lists exceed the number of actually plausible interpretations | Alert if > 20% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Repeated disambiguation failure on same request type | first_attempt_resolution_rate for a request category falls below threshold | Medium | Review and standardize strategy for that category |
| Oversized option menu presented for narrow ambiguity | Option count presented exceeds plausible interpretation count by a wide margin | Low | Flag for menu-generation logic review |

## Related Patterns
- [Clarification Irrelevant](./clarification-irrelevant.md) - a specific case of ineffective strategy where the chosen approach is asking, but the question targets the wrong axis
- [Under-Clarification](./under-clarification.md) - occurs when the chosen strategy is to guess without flagging, and the ambiguity's stakes warranted asking instead
- [Over-Clarification](./over-clarification.md) - occurs when the chosen strategy is to ask when a confident default would have been the better-fitting approach
