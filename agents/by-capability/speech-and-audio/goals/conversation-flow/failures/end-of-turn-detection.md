# End-of-Turn Detection

## Issue: Agent Can't Reliably Detect When User Has Finished Speaking

**Frequency**: Common

**Symptoms**
- Agent responds too early (user not done)
- Agent waits too long (awkward silence)
- Compound sentences split incorrectly
- Lists cut off mid-item
- Questions not fully captured

**Root Cause**
Determining when a user has finished speaking is non-trivial. Simple approaches use silence duration, but this fails for compound sentences, lists, or thoughtful speech. More sophisticated approaches analyze prosody (pitch, tempo) but still make errors. Without accurate end-of-turn detection, agents either interrupt users or create awkward pauses.

**Example**
```
Scenario: Complex user input

User: "I need to book a flight from New York to Los Angeles,
       [short pause for breath]
       departing next Tuesday,
       [short pause]
       returning on Friday,
       [pause - thinking]
       and I'd like—"

Agent: [Detects pause at "Friday,"]
       "Got it! Flight from New York to Los Angeles,
        departing Tuesday, returning Friday."

User: "Wait, I wasn't finished! I wanted to add
       a hotel and a rental car!"

---

List scenario:
User: "I'd like to order a burger,
       [pause]
       fries,
       [pause]
       and—"
       
Agent: [Responds after "fries,"]
       "One burger and fries, is that correct?"

User: "No! I also wanted a drink!"

---

End-of-turn accuracy:
  True end detected correctly: 75%
  False end (user still speaking): 18%
  Missed end (waited too long): 7%
```

**Key Statistics**
From Turn Detection Research (2026):
- Simple VAD accuracy: 70-80%
- Prosody-enhanced accuracy: 85-92%
- False end rate: 15-25% with basic detection
- User cut-off rate: 10-20%
- List/compound sentence errors: 30%

**End-of-Turn Signals**
| Signal | Reliability | Detection Method |
|--------|-------------|------------------|
| Long silence (>2s) | High | Timer |
| Falling pitch | Medium | Prosody analysis |
| Slower tempo | Medium | Prosody analysis |
| Complete sentence | Medium | NLU |
| Filled pause ("um") | Low | Could be thinking |
| Breath | Low | Could continue |

**Contributing Factors**
- Silence-only detection
- No prosody analysis
- No syntactic completeness check
- Fixed timeout regardless of context
- No learning from user patterns
- Can't detect lists or compounds

## Mitigation Strategies

### Prevention
1. **Prosody-Enhanced Endpointing Model**: Combine acoustic silence duration with prosodic cues (falling pitch, slowing tempo, breath patterns) in a trained endpointing model rather than a fixed silence timer, since compound sentences and lists produce mid-utterance pauses that look identical to true completion under silence-only detection. Trade-off: prosody models need language/speaker-specific training data and add inference latency.
2. **Syntactic Completeness Checking**: Run a lightweight incremental parser/LLM check on the partial transcript to estimate whether the utterance forms a syntactically/semantically complete unit (e.g., a list with a trailing "and" is very likely incomplete) before committing to end-of-turn. Trade-off: adds a dependency on streaming ASR partial-transcript quality, which is itself imperfect.
3. **Context-Aware Dynamic Timeout**: Vary the silence threshold based on dialog context — shorter (e.g., 0.5s) after a yes/no question, longer (e.g., 3-4s) after an open-ended or list-eliciting prompt — rather than one global timeout for every turn type.

### Detection & Response
1. **False-End Rate Tracking via User Continuation**: Detect when a user resumes speaking within a short window after the agent responded (a strong signal of a false end-of-turn); log these as false-end events and use them to retrain/tune the endpointing model and per-intent timeout settings.
2. **Partial-Confirmation Fallback**: When confidence in end-of-turn detection is marginal, respond with a partial confirmation that invites continuation ("Got burger and fries so far — anything else?") rather than a final confirmation that implies the turn is closed, reducing the cost of a wrong guess.
3. **List/Compound-Sentence Pattern Detection**: Specifically monitor error rates for utterances containing list markers ("and," enumerated items, trailing conjunctions) since these are disproportionately mis-endpointed; treat this segment as a distinct quality cohort.

### Architecture Patterns
1. **Two-Stage Endpointing (Acoustic + Semantic)**: Use a fast acoustic VAD as a first-pass candidate end-of-turn signal, then gate the final "commit" decision through a semantic completeness check before triggering the agent's response, decoupling "user paused" from "user finished."
2. **Streaming ASR with Continuation-Aware Response Generation**: Generate a draft response as soon as a candidate end-of-turn fires, but hold it un-sent for a configurable grace period during which further speech can cancel/revise it — trading a small amount of latency for fewer false-end interruptions.
3. **Per-Intent Timeout Configuration**: Store expected-completion-time metadata per intent/slot type (e.g., "list of items" vs "yes/no confirmation") and drive the dynamic timeout from that configuration rather than a single hardcoded global value.

### Metrics
1. **false_end_of_turn_rate_percent**: Target: < 10%; Alert threshold: > 20%
2. **missed_end_wait_time_ms_p95**: Target: < 2000ms; Alert threshold: > 4000ms
3. **list_compound_sentence_error_rate_percent**: Target: < 15%; Alert threshold: > 30%
4. **user_continuation_after_response_rate_percent**: Target: < 8%; Alert threshold: > 20%

### Alerts
1. **False-End Rate Spike** (P1): Condition - false end-of-turn rate exceeds 20% in a rolling window. Action: Check for recent VAD/endpointing model or timeout config changes, consider temporary global timeout increase as mitigation.
2. **List-Handling Regression** (P2): Condition - error rate for list/compound utterances exceeds 35%. Action: Review endpointing model training data coverage for enumerations, adjust per-intent timeout for list-eliciting prompts.
3. **User Continuation Surge** (P2): Condition - rate of users resuming speech immediately after an agent response exceeds 20%. Action: Audit affected intents, retune context-aware timeouts for those flows.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Turn detection
- [Conversational AI Research](https://arxiv.org/abs/2106.07837) - End-of-turn models
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Detection issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
