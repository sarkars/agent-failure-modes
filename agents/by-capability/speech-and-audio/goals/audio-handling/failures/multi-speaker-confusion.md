# Multi-Speaker Confusion

## Issue: Agent Can't Distinguish Between Multiple Speakers

**Frequency**: Occasional

**Symptoms**
- Background conversation transcribed
- Multiple people speaking causes errors
- TV/radio voices treated as user
- Children's voices in background confused
- Agent responds to wrong person

**Root Cause**
Voice agents typically assume one speaker. When multiple voices are present—family members, TV, coworkers—the agent may transcribe all voices, respond to the wrong speaker, or become confused by overlapping speech. Without speaker diarization (who spoke when), multi-speaker scenarios cause unpredictable failures.

**Example**
```
Scenario: Home assistant with multiple speakers

User: "What's the weather tomorrow?"
TV: [News anchor] "...the President announced today..."
Child: "Mom, I'm hungry!"

Combined audio received by agent:
  "What's the weather tomorrow the President announced 
   today Mom I'm hungry"

Agent response options:
  1. Responds to mixture (confused response)
  2. Responds to loudest (might be TV)
  3. Responds to most recent (child)
  4. Fails to understand

---

Phone banking scenario:
User: "I need to check my balance"
Coworker nearby: "Hey, did you get the email?"

ASR: "I need to check my balance hey did you get the email"
Agent: "I can help with balance and email. Which would you like?"

---

Multi-speaker analysis:
  Calls with multiple voices: 25%
  Calls where it caused issues: 40% of those
  Background TV/radio: 15% of calls
  Multiple active speakers: 10%
  Agent responded to wrong voice: 5%
```

**Key Statistics**
From Multi-Speaker Research (2026):
- Multi-voice scenarios: 25-35% of interactions
- Background voice interference: 15-20%
- Wrong speaker response: 5-10%
- Speaker diarization accuracy: 85-95%
- Children's voice confusion: Higher than adults

**Multi-Speaker Scenarios**
| Scenario | Common Source | Impact |
|----------|---------------|--------|
| Background TV | News, shows | Transcription noise |
| Family members | Conversations | Wrong response |
| Public spaces | Crowd chatter | Increased WER |
| Meetings | Multiple participants | Attribution errors |
| Car passengers | Conversations | Command confusion |

**Contributing Factors**
- No speaker diarization
- No voice enrollment/recognition
- Single-speaker assumption
- No "target speaker" mode
- Background voice not filtered
- No speaker confirmation

## Mitigation Strategies

### Prevention
1. **Speaker Diarization Front-End**: Run real-time diarization ("who spoke when") on the incoming audio to segment and label speaker turns before ASR/NLU, so overlapping voices (TV, family members, coworkers) are separated rather than concatenated into a single confused transcript. Trade-off: diarization adds latency and accuracy drops with more simultaneous speakers or similar-sounding voices.
2. **Voice Enrollment for Primary-User Recognition**: For repeat-use contexts (home assistants, personal devices), enroll the primary user's voice print and bias recognition/response toward matched-speaker segments, ignoring or deprioritizing unmatched voices. Trade-off: requires an enrollment step and re-enrollment on voice changes (illness, aging).
3. **Directional/Wake-Word Speaker Locking**: On multi-mic devices, use direction-of-arrival at wake-word detection to lock onto that speaker's direction for the remainder of the turn, rejecting audio arriving from other directions (e.g., TV across the room).

### Detection & Response
1. **Multi-Voice Detection Flag**: Tag each utterance with a multi-speaker-detected flag when diarization identifies more than one active voice; route flagged utterances to a clarification path ("I heard more than one voice — was that you?") instead of processing the blended transcript.
2. **Wake-Word Speaker Continuity Check**: After wake-word detection, verify the speaker identity/direction remains consistent through the command; if it shifts mid-utterance (a different person continues speaking), treat it as a new, unauthorized turn rather than a continuation.
3. **Background-Voice Complaint Correlation**: Monitor for "wrong person" or "that's not what I said" follow-ups and correlate them with sessions flagged as multi-speaker, to validate whether diarization/filtering is actually reducing wrong-attribution errors.

### Architecture Patterns
1. **Diarization-Then-ASR Pipeline**: Insert a diarization/speaker-segmentation stage before transcription so ASR operates on isolated speaker segments; combine with a "primary speaker" selection policy (enrolled voice > wake-word direction > loudest > most recent) for ambiguous cases.
2. **Target-Speaker Extraction**: Where enrollment is available, use target-speaker extraction models that isolate the enrolled user's voice from a mixed signal, effectively acting as a speech-domain filter against other human voices (complementary to non-speech noise suppression).
3. **Confirmation-Gated Multi-Party Handling**: In inherently multi-party contexts (meetings, family devices), require explicit turn-taking cues (name-addressing, push-to-talk) rather than assuming open-mic continuous recognition, reducing reliance on diarization accuracy alone.

### Metrics
1. **multi_speaker_detection_rate_percent**: Target: matches ground-truth ambient multi-voice rate (~25-35%); Alert threshold: deviates > 15pp from expected baseline
2. **wrong_speaker_response_rate_percent**: Target: < 3%; Alert threshold: > 8%
3. **diarization_accuracy_percent**: Target: > 90%; Alert threshold: < 80%
4. **enrolled_speaker_match_rate_percent**: Target: > 95% for enrolled users; Alert threshold: < 85%

### Alerts
1. **Wrong-Speaker Response Spike** (P2): Condition - wrong-speaker response rate exceeds 10% in a rolling window for a multi-user deployment (e.g., smart speaker fleet). Action: Review diarization model health, check for recent audio pipeline changes.
2. **Diarization Service Degradation** (P1): Condition - diarization accuracy on eval set drops below 75%. Action: Roll back recent diarization model/config changes, escalate to speech team.
3. **Enrollment Drift** (P3): Condition - enrolled-speaker match rate for a specific user drops below 70% over a week. Action: Prompt user for voice re-enrollment, check for device/mic changes.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Multi-speaker
- [Speaker Diarization](https://arxiv.org/abs/2101.09624) - Research approaches
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Environment issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
