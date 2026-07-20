# Conversation Depth Mismatch

## Issue
The agent calibrates the wrong amount of detail for the question at hand — giving a two-line answer to something that needed a careful multi-step explanation (e.g. a nuanced tradeoff or a risk-bearing decision), or producing an exhaustive multi-section breakdown for something the user just wanted a quick yes/no on. Both directions cause friction: too shallow leaves the user under-informed and forces follow-up questions, too deep buries the actual answer and wastes the user's time.

**Frequency**: Very Common

**Symptoms**
- User follow-up is "can you explain more" / "why" immediately after a terse answer to a substantive question
- User follow-up is "just tell me yes or no" / "too much detail" after a long structured answer to a simple question
- Response length doesn't correlate with the complexity or stakes of the question asked
- Same depth/format (e.g. always a bulleted breakdown with headers) is applied regardless of question type
- Users increasingly prefix questions with explicit depth instructions ("briefly," "in detail") to compensate for the agent not calibrating on its own

## Root Cause
Response length and structure are generated as a function of surface features of the prompt (question phrasing, presence of multiple sub-parts) rather than an explicit estimate of the question's actual complexity, stakes, or the user's implied need. Many agents default to a fixed house style — always thorough, or always concise — set by system-level tuning, which optimizes for consistency rather than per-question fit. Without a depth-calibration step that considers factors like decision reversibility, technical complexity, or the user's demonstrated expertise level, the model applies the same verbosity regardless of whether the question is "what's 15% of 80" or "should I refinance my mortgage now."

## Example
```
User: "Is it safe to run this database migration during business hours?"

Agent: "It depends." (full stop — no elaboration on lock behavior, table
size, replication lag, or rollback plan, despite this being a
production-risk decision)

User: "That's not helpful, can you actually walk me through the
tradeoffs?"

---

Elsewhere in the same session:

User: "What's the syntax to rename a column in Postgres?"

Agent produces a 40-line response: a history of the ALTER TABLE command,
five different scenarios (renaming with constraints, renaming with
foreign keys, renaming with views depending on the column, batch
renames, and naming convention best practices), when the user just
needed: `ALTER TABLE t RENAME COLUMN old_name TO new_name;`
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-30% of agent responses to high-stakes or ambiguous-complexity questions are rated "too shallow" by users | Typical range across support/advisory agent deployments |
| A comparable share of responses to simple factual questions are rated "too long" or "overexplained" | Estimated from user feedback tagging in production logs |
| Explicit complexity/stakes classification before response generation improves depth-appropriateness ratings meaningfully | Reported range across teams that added a depth-calibration step |

## Mitigations
1. **Stakes and complexity pre-classification**: Before generating a response, classify the question by reversibility/stakes (low/medium/high) and technical complexity, and let that classification set target response depth.
2. **Progressive disclosure**: Lead with a concise direct answer, then offer to expand ("want the full tradeoff breakdown?") rather than committing to one depth level upfront.
3. **User expertise signal tracking**: Infer and track the user's apparent expertise level from their phrasing and prior questions, and calibrate depth accordingly rather than using a fixed default.
4. **Explicit depth-preference memory**: Once a user states a depth preference ("keep it brief" or "give me the details"), persist and apply it for the rest of the session instead of resetting each turn.
5. **Depth-mismatch feedback loop**: Track "too long"/"too short" feedback signals per question type and use them to recalibrate the default depth heuristic.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| depth_mismatch_feedback_rate | Share of responses explicitly flagged as too shallow or too long by users | Alert if > 15% |
| high_stakes_shallow_response_rate | Rate of high-stakes/high-complexity questions answered in under N sentences | Alert if > 10% |
| low_complexity_overlength_rate | Rate of simple factual questions answered with multi-section responses | Alert if > 15% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Shallow answer to high-stakes question | A question classified high-stakes receives a response under the minimum depth threshold | High | Trigger re-generation with expanded depth, flag for review |
| Sustained overlength on simple queries | low_complexity_overlength_rate exceeds threshold over a rolling window | Low | Review depth-calibration prompt/thresholds |

## Related Patterns
- [Conversation Formality Mismatch](./conversation-formality-mismatch.md) - both are calibration failures, one on register/tone and one on depth/length
- [Under-Clarification](./under-clarification.md) - a shallow answer to a genuinely ambiguous high-stakes question can also reflect insufficient clarification, not just insufficient depth
- [User Expectation Mismatch](./user-expectation-mismatch.md) - persistent depth miscalibration is one concrete driver of a broader gap between expected and delivered agent behavior
