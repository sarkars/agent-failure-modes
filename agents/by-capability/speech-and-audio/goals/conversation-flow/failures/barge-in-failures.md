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

## Mitigation Strategies

### Prevention
1. **Full-Duplex Audio with Continuous Listening**: Architect the audio pipeline to keep the microphone active and processed throughout TTS playback (not just after it finishes), rather than a half-duplex design that only listens between agent turns. Trade-off: requires robust echo cancellation (see echo-feedback-issues) since the mic will now pick up the agent's own audio during playback.
2. **Low-Latency Interrupt VAD**: Run a lightweight, fast voice-activity detector dedicated to interrupt detection (distinct from the main end-of-turn VAD) tuned for speed over precision, so user speech during playback is flagged within ~100-200ms rather than waiting for a full ASR pass. Trade-off: a faster/looser VAD increases false-positive interrupts from noise or echo.
3. **Cancelable TTS Streaming**: Stream TTS audio in small chunks with an explicit cancel/flush API so playback can stop within one chunk's duration (not just at sentence boundaries), rather than committing to playing a full pre-rendered audio file.

### Detection & Response
1. **Interrupt Latency Measurement**: Instrument the time between VAD-detected user speech onset and actual audio cutoff; treat this "barge-in latency" as a first-class SLO, not just an implementation detail, since a slow cutoff feels as broken as no barge-in at all.
2. **Keyword-Spotting Safety Net**: In addition to general VAD-triggered barge-in, run a dedicated keyword spotter for high-value interrupt phrases ("stop," "cancel," "agent," "operator") that triggers immediate cutoff even if general barge-in detection is delayed or disabled in a given flow.
3. **Forced-Listen Duration Tracking**: Track how long users are forced to listen without a successful interrupt attempt (e.g., long IVR menus); flows with high forced-listen time combined with high abandonment are candidates for shortening or restructuring, not just barge-in tuning.

### Architecture Patterns
1. **Full-Duplex + AEC + Fast-VAD Pipeline**: The standard barge-in stack: continuous mic capture, AEC referencing the outgoing TTS stream, and a low-latency interrupt VAD running in parallel with normal ASR, feeding a "stop playback" signal directly to the audio output stage without waiting on NLU.
2. **State-Preserving Interruption Handler**: Design the dialog state machine so an interruption pauses (rather than resets) the current agent turn, capturing what had and hadn't been said, so a resumed or corrected response can reference what the user already heard.
3. **Interrupt-Priority Audio Queue**: Treat "stop speaking" as a priority-interrupt on the audio output queue (flush pending TTS chunks immediately) distinct from normal queued playback, so cutoff doesn't wait for the current buffered chunk to finish naturally.

### Metrics
1. **barge_in_latency_ms**: Target: < 200ms from speech onset to audio cutoff; Alert threshold: p95 > 500ms
2. **barge_in_support_rate_percent**: Target: 100% of flows support interruption; Alert threshold: any flow < 100%
3. **forced_listen_duration_seconds_p95**: Target: < 10s; Alert threshold: > 30s
4. **false_positive_interrupt_rate_percent**: Target: < 5%; Alert threshold: > 15% (noise/echo triggering spurious cutoffs)

### Alerts
1. **Barge-In Latency Regression** (P1): Condition - p95 barge-in latency exceeds 500ms for a sustained period. Action: Check AEC/VAD pipeline health, verify no regression in interrupt-VAD deployment.
2. **Barge-In Disabled/Broken in Flow** (P1): Condition - a production flow shows 0% successful interrupts despite user speech during playback. Action: Immediate flow audit, hotfix to re-enable full-duplex listening for that flow.
3. **False-Positive Interrupt Surge** (P2): Condition - false-positive interrupt rate exceeds 15%, often after an AEC or noise-suppression regression. Action: Review recent audio pipeline changes, retune interrupt-VAD sensitivity.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Barge-in handling
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Interruption issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
- [Voice UX Best Practices](https://www.nngroup.com/articles/voice-interface-design/) - Interruption design
