# Multi-Turn Context Loss

## Issue: Agent Loses Context Across Conversation Turns

**Frequency**: Common

**Symptoms**
- Agent asks for information already provided
- Pronouns ("it", "that") not resolved
- Follow-up questions not understood
- Conversation feels disconnected
- User must repeat information

**Root Cause**
Voice conversations unfold over multiple turns with implicit references to earlier content. "Book that one" refers to a previously mentioned option. "Change the time" assumes the agent remembers what time was set. Without robust multi-turn context management, voice agents fail to resolve references and maintain coherent conversations.

**Example**
```
Scenario: Restaurant booking conversation

Turn 1:
  User: "Find Italian restaurants near me"
  Agent: "I found 3 Italian restaurants: 
          1. Luigi's Trattoria
          2. Bella Napoli  
          3. Casa Roma"

Turn 2:
  User: "What are the hours for the second one?"
  
  Bad handling:
  Agent: "Which restaurant would you like hours for?"
  [Lost context: "second one" = Bella Napoli]
  
Turn 3:
  User: "Bella Napoli. Is it open now?"
  
  Bad handling:
  Agent: "Is what open?"
  [Lost context: "it" = Bella Napoli]

Turn 4:
  User: "Book a table there for 7pm"
  
  Bad handling:
  Agent: "Where would you like to book?"
  [Lost context: "there" = Bella Napoli]

---

Context retention analysis:
  Conversations with references: 80%
  References correctly resolved: 65%
  Repeated information requests: 35%
  User frustration mentions: 25%
  
Information re-asked:
  Restaurant name: 40% of bookings
  Date/time: 25% of bookings
  Party size: 20% of bookings
```

**Key Statistics**
From Dialogue Research (2026):
- Multi-turn conversations: 70% of voice interactions
- Implicit references per conversation: 3-5 average
- Reference resolution accuracy: 60-75%
- Context loss causes 25% of task failures
- Users repeat information 2-3 times average

**Context Loss Scenarios**
| Scenario | Reference | Loss Impact |
|----------|-----------|-------------|
| Ordinal | "the second one" | Wrong selection |
| Pronoun | "book it" | Unknown target |
| Ellipsis | "at 7" (same restaurant) | Missing context |
| Follow-up | "what about tomorrow?" | No prior date |
| Correction | "no, the other one" | Can't identify |

**Contributing Factors**
- No conversation history tracking
- Stateless turn processing
- No coreference resolution
- Context window too short
- No entity tracking
- Each turn processed independently

## Mitigation Strategies

### Prevention
1. **Persistent Conversation State with Entity Tracking**: Maintain a structured dialog state object (not just raw transcript history) that tracks named entities mentioned so far (restaurant list, selected restaurant, date/time) across turns, updated incrementally rather than re-derived from scratch each turn. Trade-off: requires careful state-schema design per domain and invalidation logic when entities become stale.
2. **Coreference and Ellipsis Resolution Pass**: Run a dedicated coreference-resolution step (rule-based ordinals like "the second one," pronoun resolution like "it"/"there," and ellipsis like "at 7" implying the previously named entity) before intent classification, rather than passing raw text straight to NLU. Trade-off: coreference models trained on text don't always transfer cleanly to spoken, disfluent input.
3. **Full-History Context Injection for LLM-Backed Agents**: When using an LLM for response generation, inject recent turn history and the structured entity state directly into the prompt context rather than relying on the model's implicit memory of a truncated context window, ensuring references resolve even in longer conversations.

### Detection & Response
1. **Repeated-Information-Request Tracking**: Monitor how often the agent asks for information the user already provided in an earlier turn (a strong, directly observable signal of context loss); spikes here indicate either entity-tracking bugs or context-window truncation.
2. **Reference Resolution Confidence Check**: When resolving an ambiguous reference ("the second one," "it," "there"), track confidence in the resolution and fall back to an explicit clarification ("Just to confirm, you mean Bella Napoli?") when confidence is low, rather than guessing silently.
3. **Turn-Count vs. Task-Completion Correlation**: Segment task completion rate by conversation length; a completion rate that drops sharply after turn 3-4 typically indicates the context window or entity tracker is losing information as the conversation grows.

### Architecture Patterns
1. **Dialog State Tracker (DST) as Source of Truth**: Separate "what was said" (transcript) from "what we currently believe" (structured slot/entity state) via a dedicated dialog state tracker component, so reference resolution and downstream logic operate against a clean, deduplicated state rather than re-parsing history each turn.
2. **Ordinal/Positional Reference Resolver**: Maintain an indexed, ordered list of recently presented options (e.g., search results) specifically to resolve ordinal references ("the second one") — a narrow, high-value special case of coreference that's cheap to implement and covers a large share of real usage.
3. **Sliding-Window Context with Entity Pinning**: For LLM-backed agents, use a sliding context window for raw turn history (to bound token cost) but "pin" key entities (currently selected restaurant, date, party size) outside the sliding window so they survive even after the originating turn ages out of context.

### Metrics
1. **repeated_information_request_rate_percent**: Target: < 10%; Alert threshold: > 25%
2. **reference_resolution_accuracy_percent**: Target: > 85%; Alert threshold: < 65%
3. **task_completion_by_turn_count**: Target: < 10pp drop from turn 1-2 to turn 5+; Alert threshold: > 25pp drop
4. **clarification_rate_for_ambiguous_references_percent**: Target: 10-20%; Alert threshold: > 40% (over-triggering) or < 5% (under-triggering, likely guessing wrong silently)

### Alerts
1. **Context Loss Regression** (P1): Condition - repeated-information-request rate exceeds 25% across a rolling window. Action: Check entity tracker / DST service health, verify no context-window truncation regression in LLM prompt construction.
2. **Reference Resolution Accuracy Drop** (P2): Condition - reference resolution accuracy on eval set falls below 65%. Action: Review recent coreference model or DST logic changes, roll back if correlated.
3. **Long-Conversation Completion Cliff** (P2): Condition - task completion rate for conversations with 5+ turns drops more than 25pp versus 1-2 turn conversations. Action: Investigate context-window sizing and entity-pinning logic for long conversations.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Context handling
- [Dialogue State Tracking](https://arxiv.org/abs/1907.03040) - Multi-turn research
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Context issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
