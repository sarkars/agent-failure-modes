# Barge-In Failures

## Issue: User Cannot Interrupt Agent's Speech

**Frequency**: Common

**Symptoms**
- User must wait for agent to finish speaking
- Corrections can't interrupt wrong responses
- Long prompts cannot be skipped
- "Stop" commands ignored mid-speech
- User frustration from forced listening

**Root Cause**
Barge-in (interrupting the agent mid-speech) requires detecting user speech while the agent is speaking, then stopping TTS, canceling queued audio, and returning to listening mode. Many voice systems don't support this, or implement it poorly—detecting their own output as user speech, or having long delays before responding to interruptions.

**Example**
```
Scenario: IVR system without barge-in

Agent: "Thank you for calling. Your call is important to us. 
        Please listen carefully as our menu options have 
        recently changed. For billing, press 1. For technical
        support, press 2. For sales, press 3. For..."

User (at 3 seconds): "Technical support!"
Agent: [Continues reading menu for 45 more seconds]

User (at 20 seconds): "SUPPORT!"
Agent: [Still reading]

User (at 48 seconds): "..."
Agent: "...press 7. Or stay on the line for an agent."

Total time wasted: 45 seconds
User frustration: High
Abandonment risk: Elevated

With proper barge-in:
  User (at 3 seconds): "Technical support!"
  Agent: [Stops immediately]
  Agent: "Connecting you to technical support."
  
  Time saved: 45 seconds
  User experience: Excellent
```

**Key Statistics**
From Voice UX Research (2026):
- 40% of voice agents lack barge-in support
- Average menu listen time without barge-in: 45s
- With barge-in: 8s average
- User satisfaction: 40% higher with barge-in
- Abandonment: 25% lower with barge-in

**Barge-In Failure Types**
| Type | Description | Impact |
|------|-------------|--------|
| No detection | User speech not detected | Forced waiting |
| Slow detection | Delay before response | Partial interruption |
| Self-trigger | Agent's audio triggers detection | False interrupts |
| No cancellation | TTS continues after detection | Overlap |
| State corruption | Interruption breaks conversation | Restart needed |

**Contributing Factors**
- Half-duplex audio design (can't listen while speaking)
- Echo cancellation failures
- No TTS cancellation capability
- State machine doesn't support interruption
- Latency in detection pipeline
- Full prompt must be played (design choice)

**Mitigation Strategies**
1. **Full-duplex audio**: Listen while speaking
2. **Echo cancellation**: Filter out agent's own audio
3. **Quick detection**: Low-latency user speech detection
4. **TTS interruption**: Ability to stop/cancel speech
5. **State preservation**: Handle interruption gracefully
6. **Keyword spotting**: Listen for specific interrupt phrases

**Detection**
- Measure time between user speech and agent stop
- Track forced listening durations
- Monitor "stop" command effectiveness
- Survey user frustration with interruptions
- Compare completion rates with/without barge-in

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Barge-in handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Interruption issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
- [Voice UX Best Practices](https://www.nngroup.com/articles/voice-interface-design/) - Interruption design
