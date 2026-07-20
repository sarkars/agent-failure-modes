# Handoff Context Incompleteness

## Issue
When one agent hands a task to another, it passes along a summary or subset of the context it accumulated, rather than the full working state. The receiving agent then either proceeds on incomplete information (producing a subtly wrong result) or has to spend additional tool calls and turns re-deriving context the sending agent already had — re-reading source documents, re-querying an API, or asking the user to repeat information already provided upstream.

**Frequency**: Very Common

**Symptoms**
- Receiving agent asks the user or an upstream system for information that was already established earlier in the workflow
- Receiving agent's output contradicts a constraint or decision the sending agent had already established
- Elevated latency and tool-call counts on handoff-receiving agents compared to agents that don't rely on handoffs
- Handoff payloads containing a "summary" field that omits specific values (exact figures, IDs, edge-case exceptions) the sending agent had resolved

## Root Cause
Passing full context between agents is expensive — large context windows cost tokens and latency — so handoff protocols are commonly designed to pass a compressed summary rather than the sending agent's complete working state. The summarization step is usually done by the sending agent itself, which decides what's "relevant" based on its own understanding of the task; it has no reliable way to know which details the receiving agent will actually need, because that depends on reasoning the receiving agent hasn't done yet. Anything the sending agent judges as incidental — an edge case it dismissed, an assumption it made, a constraint it verified — is exactly the kind of detail likely to be silently dropped, and it is often precisely the detail that matters for correctness downstream.

## Example
```
A trip-planning agent gathers requirements from a user across a 20-turn
conversation: dates, budget, and a specific constraint mentioned once in
turn 6 -- "actually my connecting flight can't be through Chicago, I have
a standing travel ban there from my employer."

The trip-planning agent hands off to a flight-booking agent with a
summary: "Book round-trip flights, NYC to Denver, June 3-10, budget
$600, economy." The Chicago constraint, mentioned only once and not
repeated in later turns, doesn't make it into the summary field.

The flight-booking agent finds the cheapest itinerary: NYC -> Chicago ->
Denver, $410, and books it. The user only discovers the problem when
reviewing the itinerary, has to cancel, pay a change fee, and re-explain
the Chicago constraint from scratch to a third agent brought in to fix
the booking.
```

## Statistics
| Finding | Context |
|---------|---------|
| An estimated 20-35% of multi-agent handoffs using summarized context result in the receiving agent re-requesting information available upstream | Typical range observed in agent-to-agent handoff telemetry |
| Handoffs using full or structured-state transfer instead of free-text summaries show markedly fewer downstream correctness errors | Reported range across teams comparing summary-based vs. structured handoff payloads |
| Re-derivation of dropped context typically adds 2-4x the tool calls of the original context-gathering phase | Estimated from workflows instrumented to track redundant tool calls post-handoff |

## Mitigations
1. **Structured state transfer over free-text summaries**: Pass a structured object of resolved facts, constraints, and decisions (not a prose summary) so the receiving agent can programmatically check for required fields rather than inferring intent from text.
2. **Constraint checklist propagation**: Explicitly carry forward any hard constraints identified during the task (not just headline requirements), tagged so the receiving agent must acknowledge or explicitly re-verify each one.
3. **Full-context fallback link**: Attach a reference to the complete conversation/session history alongside the summary, so a receiving agent that suspects information is missing can retrieve the source rather than only having the compressed version.
4. **Receiving-agent completeness check**: Require the receiving agent to state its understanding of key constraints back before acting, giving a chance for a human or upstream system to catch a dropped detail before it causes downstream harm.
5. **Handoff payload schema validation**: Define a minimum required schema for handoff payloads per task type (e.g., booking tasks must include a constraints array) and reject handoffs that omit required fields rather than silently accepting a partial summary.

## Production Signals
### Key Metrics
| Metric | Description | Alert Threshold |
|--------|-------------|-----------------|
| post_handoff_redundant_calls | Count of tool calls made by the receiving agent that re-fetch information available in the sending agent's session | Alert if > 20% of receiving agent's total calls |
| handoff_payload_field_completeness | Share of defined schema fields present and non-empty in a handoff payload | Alert if < 90% |
| constraint_violation_post_handoff | Rate of receiving-agent outputs that violate a constraint established pre-handoff | Alert if > 2% |

### Alerts
| Alert | Condition | Severity | Response |
|-------|-----------|----------|----------|
| Constraint violated post-handoff | An output from a receiving agent conflicts with a constraint recorded earlier in the same task's history | High | Halt downstream action, surface the conflict to a human reviewer |
| Handoff schema incomplete | A handoff payload is missing required schema fields for its task type | Medium | Block the handoff, return to sending agent for completion |

## Related Patterns
- [Handoff State Loss](./handoff-state-loss.md) - a more severe variant where task state is dropped entirely rather than selectively summarized
- [Handoff Accountability Loss](./handoff-accountability-loss.md) - incomplete context can compound accountability loss when the receiving agent doesn't realize it's missing something critical
- [Handoff Protocol Version Mismatch](./handoff-protocol-version-mismatch.md) - a structural cause of context incompleteness when schema versions between sender and receiver diverge
