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

**Mitigation Strategies**
1. **Conversation state**: Maintain full conversation history
2. **Entity tracking**: Track mentioned entities across turns
3. **Coreference resolution**: Resolve pronouns and references
4. **Slot carryover**: Carry forward established values
5. **Context injection**: Include prior turns in LLM context
6. **Explicit confirmation**: Confirm understood references

**Detection**
- Track repeated information requests
- Monitor reference resolution accuracy
- Analyze "which one?" clarification rate
- Survey user about conversation coherence
- Measure task completion across turn counts

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Context handling
- [Dialogue State Tracking](https://arxiv.org/abs/1907.03040) - Multi-turn research
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Context issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
