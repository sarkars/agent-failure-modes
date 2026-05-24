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

**Mitigation Strategies**
1. **AEC**: Implement acoustic echo cancellation
2. **Reference signal**: Use agent audio for echo subtraction
3. **Half-duplex**: Mute mic during playback (last resort)
4. **Delay detection**: Detect echo delay for cancellation
5. **Adaptive filter**: Continuously adapt to acoustic environment
6. **Device guidance**: Guide user on device positioning

**Detection**
- Measure echo presence in audio
- Track self-trigger rate
- Monitor feedback incidents
- Compare speakerphone vs. handset performance
- Detect TTS content in ASR output

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Echo issues
- [Echo Cancellation](https://en.wikipedia.org/wiki/Echo_cancellation) - Technical background
- [WebRTC AEC](https://webrtc.googlesource.com/src/+/refs/heads/main/modules/audio_processing/aec/) - Implementation
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Audio issues
