# Turn-Taking Errors

## Issue: Agent and User Speak Over Each Other

**Frequency**: Common

**Symptoms**
- Agent starts speaking while user still talking
- Awkward simultaneous speech
- User's final words cut off
- Agent responds to incomplete input
- Conversational rhythm feels unnatural

**Root Cause**
Natural conversation has implicit turn-taking cues—prosody changes, sentence completion, falling pitch. Voice agents often use simple voice activity detection (VAD) that misses these cues. The agent starts responding when the user pauses briefly, causing overlap. Or the user starts speaking, expecting the agent to stop, but it continues.

**Example**
```
Scenario: Appointment booking conversation

User: "I'd like to book an appointment for—"
Agent: [Detects 0.3s pause, starts speaking]
       "Sure, what date works for you?"

User: "—next Tuesday" [overlapping with agent]
Agent: "Sure, what date works for you?" [continuing]

Result: Confused overlap, agent missed "next Tuesday"

---

User: "Can I have it at three— actually, make that four"
Agent: [Responds after "three"]
       "Three o'clock, let me check availability"

User: "No, I said four!"

---

Turn-taking analysis:
  Total conversations: 1,000
  Overlapping speech events: 234 (23%)
  User cut off: 156 (15%)
  Agent cut off by user: 78 (8%)
  
  Causes:
    - Short pause misread as turn end: 45%
    - Self-correction interrupted: 25%
    - Agent didn't yield: 20%
    - Both started simultaneously: 10%
```

**Key Statistics**
From Turn-Taking Research (2026):
- Overlap rate in voice agents: 15-25%
- Human conversation overlap: 5-10%
- User cut-off rate: 10-20%
- User frustration from overlap: 30% report issues
- Information loss from overlap: 12% of intent

**Turn-Taking Failure Types**
| Type | Description | Impact |
|------|-------------|--------|
| Premature response | Agent starts too early | User cut off |
| No yielding | Agent doesn't stop when user speaks | Talk-over |
| Double start | Both begin simultaneously | Confusion |
| Slow response | Agent waits too long | Awkward |
| Interrupt failure | User can't break in | Frustration |

**Contributing Factors**
- Simple VAD without prosody analysis
- No turn-taking prediction
- Fixed response timing
- No real-time overlap detection
- Half-duplex audio design
- Missing conversational cues

**Mitigation Strategies**
1. **Prosody analysis**: Detect turn-completion cues
2. **Predictive turn-taking**: Anticipate turn boundaries
3. **Overlap detection**: Stop if user resumes speaking
4. **Back-off mechanism**: Yield on simultaneous start
5. **Full-duplex audio**: Continuous listening
6. **Completion signals**: Explicit "go ahead" cues

**Detection**
- Measure overlap frequency
- Track user repetition rate (sign of being cut off)
- Monitor simultaneous speech events
- Analyze user complaints about interruptions
- Compare turn-taking with human baseline

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Turn-taking issues
- [Conversational AI Research](https://arxiv.org/abs/2106.07837) - Turn-taking models
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Flow issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
