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

**Mitigation Strategies**
1. **Correction detection**: Recognize "No, I said..." patterns
2. **Full capture**: Wait for complete correction before processing
3. **State rollback**: Ability to undo recent state changes
4. **Explicit confirmation**: "Let me update that to Chicago"
5. **Context retention**: Keep conversation history for corrections
6. **Graceful interruption**: Handle mid-sentence corrections

**Detection**
- Track correction phrase recognition
- Monitor state consistency after corrections
- Analyze "no" utterance handling
- Measure task completion after corrections
- Survey user correction experience

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Correction handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Interruption issues
- [Conversational AI Research](https://arxiv.org/abs/2106.07837) - Repair handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
