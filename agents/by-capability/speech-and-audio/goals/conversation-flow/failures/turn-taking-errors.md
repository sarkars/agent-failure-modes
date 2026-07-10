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

## Mitigation Strategies

### Prevention
1. **Prosody-Based Turn-Completion Prediction**: Use pitch contour, tempo, and energy trends (not just silence duration) to predict genuine turn-completion versus a mid-utterance pause or self-correction, since simple VAD triggers on any short pause regardless of whether the sentence is grammatically/prosodically complete. Trade-off: prosody models add latency and need tuning across speaking styles and languages.
2. **Full-Duplex Listening with Overlap Detection**: Keep the mic active throughout agent speech and continuously check for resumed user speech; if detected, immediately stop the agent output rather than continuing to completion, converting what would be an overlap-and-confusion event into a clean yield. Trade-off: shares the same AEC dependency as barge-in — the agent must distinguish real resumed speech from its own echoed audio.
3. **Back-Off on Simultaneous Start**: When both agent and user begin speaking within the same short window (double-start), have the agent yield immediately (stop and listen) rather than continuing, mirroring human conversational back-off norms rather than "whoever started, continues."

### Detection & Response
1. **Overlap Frequency Monitoring**: Continuously measure the rate of simultaneous agent+user speech across calls; a rising trend indicates the turn-completion predictor or pause thresholds have drifted out of calibration relative to the actual user population's speaking cadence.
2. **User Repetition as Cut-Off Proxy**: Track how often users repeat all or part of an utterance within a few seconds of being overlapped/cut off; this is a strong indirect signal of premature agent responses even when direct overlap detection is imperfect.
3. **Self-Correction Interruption Detection**: Specifically flag cases where the agent responds mid-self-correction ("at three— actually four"); train the turn-completion model to recognize the "actually/wait/I mean" self-repair pattern as a strong non-completion signal.

### Architecture Patterns
1. **Predictive Turn-Taking Model**: A model trained on prosodic and lexical cues to predict turn-end probability continuously (not just at a single silence checkpoint), letting the agent decide to begin, hold, or wait based on a probability trend rather than a single threshold crossing.
2. **Overlap-Aware Response Gate**: Gate agent TTS start behind a short "still speaking?" check even after a candidate turn-end fires, and gate continued playback behind continuous overlap detection, so both false starts and failure-to-yield are covered by the same mechanism.
3. **Human-Baseline Calibration Loop**: Periodically compare system overlap rate and cut-off rate against a human-conversation baseline (5-10% overlap) and use the gap as the primary tuning signal for both the completion predictor and the back-off policy.

### Metrics
1. **overlap_rate_percent**: Target: < 10% (approaching human baseline); Alert threshold: > 20%
2. **user_cutoff_rate_percent**: Target: < 10%; Alert threshold: > 20%
3. **agent_cutoff_by_user_rate_percent**: Target: < 10%; Alert threshold: > 20% (indicates agent not yielding)
4. **self_correction_misfire_rate_percent**: Target: < 10%; Alert threshold: > 25%

### Alerts
1. **Overlap Rate Regression** (P2): Condition - overlap rate exceeds 20% across a rolling window, more than 2x human baseline. Action: Review recent turn-completion model or VAD threshold changes.
2. **Failure-to-Yield Spike** (P1): Condition - agent-cutoff-by-user rate exceeds 20%, indicating the agent isn't stopping when the user resumes speaking. Action: Verify full-duplex listening and overlap-detection service health; this degrades user trust quickly if left unresolved.
3. **Self-Correction Handling Regression** (P2): Condition - self-correction misfire rate exceeds 25%. Action: Review turn-completion model training data for self-repair patterns, retrain/tune.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Turn-taking issues
- [Conversational AI Research](https://arxiv.org/abs/2106.07837) - Turn-taking models
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Flow issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
