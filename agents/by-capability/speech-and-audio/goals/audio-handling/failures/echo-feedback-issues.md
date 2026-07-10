# Echo and Feedback Issues

## Issue: Agent's Own Audio Interferes with User Speech Detection

**Frequency**: Common

**Symptoms**
- Agent triggers on its own voice
- User speech mixed with echo
- Feedback loop between speaker and mic
- Agent interrupts itself
- Double responses to same input

**Root Cause**
When the agent speaks, its audio may be picked up by the microphone—either as acoustic echo (speaker to mic) or electronic echo (audio routing). Without effective echo cancellation, the agent's own speech is transcribed as user input, causing false triggers, self-interruption, or garbled transcription when user speaks during agent playback.

**Example**
```
Scenario: Echo causing false triggers

Agent: "Your account balance is five hundred dollars"
[Audio plays through speaker]
[Microphone picks up "five hundred dollars"]

ASR: "five hundred dollars"
Agent: [Interprets as user input]
Agent: "I heard 'five hundred dollars'. Would you like 
        to transfer five hundred dollars?"

User: "No, I didn't say anything!"

---

Acoustic feedback scenario:
Agent: "How can I help you today?"
[Audio → speaker → room → microphone → audio]
[Feedback loop starts]
Agent: "Beeeeeeeeeeeeeee" [Feedback squeal]

---

Mixed echo and speech:
Agent: "Please say yes or no"
User: [Speaking while agent finishes] "Yes"
ASR: "Please say yes or no yes"
Agent: "I didn't understand. Please say yes or no."

Echo analysis:
  Calls with echo issues: 20%
  False triggers from echo: 8%
  Speech corrupted by echo: 12%
  Feedback incidents: 2%
```

**Key Statistics**
From Echo Research (2026):
- VoIP calls with echo: 20-30%
- Echo-caused false triggers: 5-10%
- Speech-echo overlap issues: 10-15%
- Effective AEC reduces issues by 90%
- Speakerphone echo worst: 40% of calls

**Echo Failure Types**
| Type | Cause | Impact |
|------|-------|--------|
| Acoustic | Speaker to mic | False triggers |
| Line echo | Telephony reflection | Delayed confusion |
| Feedback | Amplification loop | Squeal, unusable |
| Reverberation | Room acoustics | Garbled speech |
| Electronic | Audio routing | Double input |

**Contributing Factors**
- No acoustic echo cancellation (AEC)
- Poor AEC adaptation
- Speaker/mic too close
- Speakerphone mode
- Full-duplex without echo handling
- Room acoustics (reverb)

## Mitigation Strategies

### Prevention
1. **Acoustic Echo Cancellation (AEC) with Reference Signal**: Feed the agent's own outgoing TTS audio as a reference signal into an adaptive AEC filter (e.g., NLMS/Kalman-based) so the known agent speech is subtracted from the microphone input before ASR sees it. Trade-off: AEC convergence takes time (tens of ms to seconds) and can lag on sudden acoustic path changes (e.g., user moves the phone).
2. **TTS-Content Fingerprint Matching**: Independent of AEC, maintain a rolling fingerprint/hash of recently played TTS audio and compare incoming ASR transcripts against it; if the "user" utterance closely matches recent agent output, suppress it as echo rather than treating it as input.
3. **Device Positioning Guidance**: For speakerphone/far-field scenarios prone to feedback loops, detect high loop-gain conditions and proactively prompt the user to reduce volume or reposition the device before a feedback squeal occurs.

### Detection & Response
1. **Self-Trigger Detection**: Compare each ASR hypothesis produced while the agent is speaking against the known TTS script; matches above a similarity threshold are flagged as echo and discarded rather than processed as user intent, with the discard logged for tuning.
2. **Echo Presence Estimation**: Continuously estimate residual echo return loss enhancement (ERLE) from the AEC filter; when ERLE is poor (indicating AEC isn't converging, e.g., double-talk or fast-changing acoustic path), switch to half-duplex (mute mic during playback) as a fallback for that session only.
3. **Feedback Loop Detection**: Monitor for the characteristic rising-amplitude, narrow-frequency-band signature of acoustic feedback in real time; if detected, immediately cut agent output and mute to break the loop before it becomes audible/disruptive.

### Architecture Patterns
1. **Reference-Signal AEC Pipeline**: Standard telephony pattern — route the exact digital TTS output as the AEC reference input, place the AEC stage between raw mic capture and ASR, and continuously adapt the filter coefficients during playback.
2. **Fail-Safe Half-Duplex Fallback**: When AEC health metrics (ERLE, self-trigger rate) indicate the adaptive filter isn't performing, automatically fall back to muting the mic during TTS playback for that call, sacrificing barge-in capability for reliability — an explicit trade-off with the barge-in-failures pattern.
3. **Echo-Aware Barge-In Gate**: Before honoring a detected "user interruption" during agent speech, require it to pass both VAD and the TTS-fingerprint-mismatch check, preventing the agent from being self-interrupted by its own echoed voice.

### Metrics
1. **erle_db**: Target: > 20dB; Alert threshold: < 10dB sustained
2. **self_trigger_rate_percent**: Target: < 1% of agent-speaking segments; Alert threshold: > 5%
3. **feedback_incident_rate_percent**: Target: < 0.5% of calls; Alert threshold: > 2%
4. **half_duplex_fallback_rate_percent**: Target: < 5% of calls (should be rare exception); Alert threshold: > 15% (indicates AEC systemically underperforming)

### Alerts
1. **AEC Convergence Failure** (P1): Condition - ERLE stays below 10dB for more than 5 seconds of active playback. Action: Trigger half-duplex fallback for the session, log audio sample for AEC tuning review.
2. **Self-Trigger Spike** (P1): Condition - self-trigger rate exceeds 5% across a rolling 100-call window. Action: Page audio pipeline on-call, check for recent AEC config/deployment changes.
3. **Feedback Squeal Detected** (P2): Condition - feedback-loop signature detected on a live call. Action: Auto-mute and cut agent output immediately, log incident, notify device/positioning guidance to user on reconnect.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Echo issues
- [Echo Cancellation](https://en.wikipedia.org/wiki/Echo_cancellation) - Technical background
- [WebRTC AEC](https://webrtc.googlesource.com/src/+/refs/heads/main/modules/audio_processing/aec/) - Implementation
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Audio issues
