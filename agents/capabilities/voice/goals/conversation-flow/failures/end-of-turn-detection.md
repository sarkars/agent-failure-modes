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

**Mitigation Strategies**
1. **Prosody analysis**: Use pitch and tempo cues
2. **Syntactic completeness**: Check if sentence is complete
3. **Context-aware timeouts**: Longer for lists, shorter for yes/no
4. **Explicit cues**: "...and that's it" signals completion
5. **Partial confirmation**: "Got burger and fries so far..."
6. **User adaptation**: Learn individual speaking patterns

**Detection**
- Track false end rate
- Monitor user repetitions/completions
- Analyze cut-off utterances
- Compare detection accuracy by sentence type
- Survey user experience with turn-taking

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Turn detection
- [Conversational AI Research](https://arxiv.org/abs/2106.07837) - End-of-turn models
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Detection issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
