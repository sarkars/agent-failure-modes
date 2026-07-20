# Clarification Irrelevant

## Issue
The agent correctly recognizes that a request is ambiguous and asks a clarifying question, but the question it asks targets the wrong axis of ambiguity — it doesn't actually narrow down the interpretation that matters. The user answers the question, the agent proceeds, and the output is still wrong because the real ambiguity was never resolved. This is distinct from over-clarification (asking when nothing needed clarifying) and under-clarification (not asking at all): here the agent's instinct to ask was correct, but its question-selection logic picked a low-information question over the high-information one.

**Frequency**: Common

**Symptoms**
- User answers the clarifying question, agent proceeds, output is still corrected on a different dimension
- Clarifying question addresses a minor stylistic detail while the actual blocking ambiguity (scope, target system, time range) goes unasked
- Multiple rounds of Q&A occur before the agent stumbles onto the question that actually mattered
- Users report the clarifying question felt "beside the point" or unrelated to their confusion
- Time-to-resolution for ambiguous requests is high despite the agent asking questions promptly

## Root Cause
Generating *a* plausible clarifying question is easier for a language model than identifying *which* source of ambiguity has the highest expected impact on the outcome. Without an explicit ambiguity-ranking step — enumerating candidate interpretations and asking specifically about the split that most changes the output — the model tends to ask about whichever ambiguous term appeared most recently or most saliently in the prompt, which is not necessarily the one that determines correctness. The question-generation step and the interpretation-space analysis are typically the same undifferentiated generation pass, so there's no mechanism forcing the question to target the highest-variance unknown.

## Example
```
User: "Pull last quarter's numbers for the report."

Ambiguity actually present: which report template (there are two: Board
deck vs. Investor update, with different metrics and different quarter
boundaries), and which entity ("last quarter" could mean calendar Q2 or
fiscal Q1, since the company's fiscal year starts in April).

Agent asks: "Would you like the numbers formatted as a table or as
bullet points?"

User: "Table is fine."

Agent pulls calendar-Q2 numbers into a Board-deck-style table. The user
actually needed fiscal-Q1 numbers for the Investor update — the
formatting question resolved nothing that mattered, and the fiscal-vs-
calendar and template ambiguities were never raised.

User: "This is the wrong quarter and wrong format entirely."
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 30-45% of single clarifying questions in ambiguous-request flows fail to resolve the interpretation that actually determined the final correction | Estimated from review of agent Q&A transcripts followed by user corrections |
| Sessions where the first clarifying question misses the key ambiguity average roughly 1.8 additional Q&A rounds versus 1.0 when it hits | Typical range observed in multi-turn agent logs |
| Ranking candidate ambiguities by output-impact before asking reduces irrelevant-question rate by around a third | Reported range across teams that added interpretation-space enumeration |

## Mitigations
1. **Interpretation-space enumeration**: Before generating a clarifying question, have the agent explicitly list 2-4 candidate interpretations of the request and identify which unresolved variable would change the output most, then ask about that one.
2. **Impact-ranked question selection**: Score candidate clarifying questions by how much they narrow the space of valid outputs, and always ask the highest-impact one first rather than the most fluent-sounding one.
3. **Multi-slot single question**: When more than one ambiguity exists, combine them into one structured question (e.g. "Which quarter — calendar Q2 or fiscal Q1 — and which template — Board or Investor?") rather than resolving them one irrelevant question at a time.
4. **Post-answer re-check**: After the user answers, have the agent re-verify whether the original ambiguity is actually resolved before proceeding, rather than assuming any answered question clears it to proceed.
5. **Irrelevant-question review loop**: Log cases where output was corrected despite a prior clarifying question having been asked and answered, and use them to retrain or reprompt the question-selection step.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| post_clarification_correction_rate | Rate of outputs still corrected after a clarifying question was asked and answered | Alert if > 25% |
| clarification_rounds_to_resolution | Average number of Q&A rounds needed before output is accepted | Alert if > 1.5 |
| question_output_impact_score | Average estimated output-narrowing impact of clarifying questions asked | Alert if trending down |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| High post-clarification correction rate | post_clarification_correction_rate exceeds threshold over a rolling window | Medium | Review question-selection prompt, add interpretation-ranking step |
| Repeated multi-round ambiguity resolution | A session requires 3+ clarification rounds for one request | Low | Flag for manual review of question quality |

## Related Patterns
- [Under-Clarification](./under-clarification.md) - the opposite failure to ask at all; both leave the real ambiguity unresolved, just via different paths
- [Over-Clarification](./over-clarification.md) - both involve poorly targeted clarification behavior, one asking when unneeded, the other asking the wrong thing
- [Disambiguation Strategy Ineffective](./disambiguation-strategy-ineffective.md) - the broader pattern of a resolution approach that doesn't narrow ambiguity, of which irrelevant questioning is one specific cause
