# Interruption Mishandling

## Issue: Agent Doesn't Properly Handle User Corrections and Interruptions

**Frequency**: Common

**Symptoms**
- Agent ignores user corrections
- "No, I said..." not recognized as correction
- Agent continues with wrong understanding
- Partial input from interruption processed
- State corruption after interruption

**Root Cause**
When users interrupt to correct the agent, multiple things must happen: detect the interruption, stop the current response, understand the correction, and update state. Many voice agents fail at one or more of these steps—they detect the interruption but process the partial input, or they stop but don't understand it was a correction, or they understand but don't update their state.

**Example**
```
Scenario: Flight booking with correction

Agent: "You want to fly from New York to Boston on—"
User: [Interrupts] "No, Chicago, not Boston"
Agent: [Stops speaking]

Possible failures:

Failure 1: Partial processing
  ASR captured: "No Chicago not"
  Agent: "I didn't understand. Where do you want to fly?"
  [Correction not recognized as correction]

Failure 2: State not updated
  Agent understands correction
  Agent: "OK, Chicago"
  Later: "Confirming: New York to Boston" [State still Boston]

Failure 3: Wrong interpretation  
  Agent: "Searching for flights to Chicago, not Boston"
  [Searched for destination "Chicago, not Boston"]

Failure 4: Complete confusion
  Agent: "I heard 'no.' Would you like to cancel?"
  [Interpreted as negative, not correction]

Correct handling:
  Agent: [Stops, listens fully]
  Agent: "Got it, Chicago instead of Boston. 
          So that's New York to Chicago on..."
```

**Key Statistics**
From Correction Research (2026):
- 30-40% of conversations include corrections
- Correction success rate: 60-75%
- Failed corrections: 25% lead to task failure
- "No, I said..." recognition: 65% accuracy
- State update after correction: 70% success

**Interruption Handling Failures**
| Failure | Description | Impact |
|---------|-------------|--------|
| Partial capture | Only part of correction heard | Wrong interpretation |
| Not recognized | Correction treated as new input | Confusion |
| State not updated | Understanding without state change | Silent error |
| Wrong scope | Corrects wrong field | More confusion |
| Total reset | Starts over instead of correcting | User frustration |

**Contributing Factors**
- No correction intent detection
- Partial ASR during interruption
- State not rollback-capable
- No "correction mode" handling
- Interruption breaks state machine
- No negation/correction patterns

## Mitigation Strategies

### Prevention
1. **Correction-Intent Classifier**: Train/apply a dedicated classifier for correction patterns ("no, I said...", "not X, Y", "actually...") that runs before general NLU intent classification, so corrections are recognized as a distinct dialog act rather than parsed as a fresh, unrelated utterance. Trade-off: needs enough labeled correction examples across domains to generalize beyond a fixed phrase list.
2. **Full-Capture-Before-Processing on Interrupt**: When an interruption is detected, don't process ASR partials immediately — wait for the interruption utterance to reach a stable end-of-turn (via the endpointing improvements in end-of-turn-detection) before running NLU, so "No, Chicago, not Boston" isn't truncated to "No Chicago not."
3. **Rollback-Capable State Management**: Model dialog state as a versioned/append-only structure (not in-place mutation) so a correction can cleanly roll back the specific slot that changed (e.g., destination) without resetting or corrupting unrelated slots (e.g., date, passenger count).

### Detection & Response
1. **State-Consistency Verification Post-Correction**: After processing a recognized correction, explicitly re-read back the affected slot(s) ("Got it, Chicago instead of Boston...") and verify against the updated state object before proceeding, rather than trusting silently that the update propagated.
2. **Correction Recognition Accuracy Tracking**: Monitor the rate at which utterances matching correction patterns are actually classified as corrections (vs. misrouted as new requests or negations); regressions here directly predict downstream task failures.
3. **Wrong-Scope Correction Detection**: When a correction is applied, check whether the corrected field matches the field most recently mentioned by the agent (proximity heuristic); flag and request clarification when the target field is ambiguous ("Which part would you like to change — the destination or the date?").

### Architecture Patterns
1. **Correction-Aware Dialog State Machine**: Extend the standard slot-filling state machine with an explicit "correction" transition type that targets a specific slot and old/new value pair, distinct from the "fill new slot" transition, making corrections a first-class state-machine event rather than an edge case bolted onto interrupt handling.
2. **Two-Pass Interrupt Processing**: First pass classifies the dialog act (correction vs. new request vs. negation-only) using the full captured utterance; second pass routes to the appropriate handler (state-rollback-and-update vs. standard NLU) — avoiding the failure mode of applying general NLU to what is really a correction.
3. **Explicit Confirmation-With-Diff**: After any correction, generate a confirmation utterance that explicitly names both the old and new value ("changing destination from Boston to Chicago") rather than only the new value, so any residual state-update failure becomes visible to the user immediately instead of surfacing later as a wrong booking.

### Metrics
1. **correction_recognition_accuracy_percent**: Target: > 90%; Alert threshold: < 70%
2. **state_update_success_rate_after_correction_percent**: Target: > 95%; Alert threshold: < 85%
3. **wrong_scope_correction_rate_percent**: Target: < 5%; Alert threshold: > 15%
4. **task_failure_rate_following_correction_percent**: Target: < 10%; Alert threshold: > 25%

### Alerts
1. **Correction Recognition Regression** (P1): Condition - correction recognition accuracy drops below 70% on eval or production sample. Action: Roll back recent NLU/classifier changes, review new correction-phrase training data.
2. **Silent State Desync** (P1): Condition - post-correction state-consistency check fails (confirmed slot doesn't match state object) for > 5% of corrections. Action: Immediate investigation of state management layer, potential rollback of recent dialog-manager deploy.
3. **Repeated User Re-Corrections** (P2): Condition - same user issues 2+ corrections to the same slot within one conversation. Action: Flag conversation for review, check if wrong-scope detection is misfiring.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Correction handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Interruption issues
- [Conversational AI Research](https://arxiv.org/abs/2106.07837) - Repair handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
