# Streaming ASR Instability

## Issue: Real-Time Transcription Changes Mid-Utterance

**Frequency**: Common

**Symptoms**
- Displayed text changes while user speaks
- Actions triggered on interim results
- Final transcription differs from interim
- Agent responds to partial utterance
- User sees "flickering" transcription

**Root Cause**
Streaming ASR provides real-time transcription updates as audio arrives, but early results are based on incomplete context. As more audio arrives, the transcription may change significantly. Applications that act on interim results or display them prominently can create confusing or incorrect behavior when the final result differs.

**Example**
```
Scenario: Voice assistant with real-time display

User says: "I want to cancel my subscription"

Streaming transcription timeline:
  T+0.3s: "I want"
  T+0.5s: "I want to can"
  T+0.8s: "I want to cancel"      ← Agent shows this
  T+1.0s: "I want to cancel mice" ← Flickering text
  T+1.2s: "I want to cancel my"
  T+1.5s: "I want to cancel my subscription"
  T+1.8s: [Final] "I want to cancel my subscription"

Problem scenario:
  T+0.8s: Agent acts on "I want to cancel"
  Action: Initiates cancellation flow
  T+1.8s: Final result: "I want to cancel my subscription"
  
  But agent already responded to partial intent
  User confused: "I didn't finish yet!"

Another example:
  Interim: "Turn on the lights"
  Final: "Don't turn on the lights"
  
  If acted on interim → wrong action taken
  
Stability analysis:
  Utterances with significant interim→final change: 23%
  Average revisions per utterance: 3.2
  Final differs from last interim: 8%
  Agent acted on wrong interim: 5% of interactions
```

**Key Statistics**
From Streaming ASR Research (2026):
- Interim-to-final change rate: 20-30%
- Significant meaning change: 5-10% of utterances
- User confusion from flickering: 15% report frustration
- Premature action errors: 3-8%
- Average revision count: 2-4 per utterance

**Instability Patterns**
| Pattern | Example | Risk |
|---------|---------|------|
| Negation flip | "don't" appears late | Action reversal |
| Entity change | "New York" → "Newark" | Wrong destination |
| Number revision | "fifteen" → "fifty" | Wrong quantity |
| Incomplete command | "cancel" → "cancel that order" | Premature action |
| Word boundary | "ice cream" → "I scream" | Meaning change |

**Contributing Factors**
- Acting on interim results
- No final result wait logic
- Displaying unstable transcription
- No change detection
- Short timeout before action
- Treating interim as final

**Mitigation Strategies**
1. **Wait for final**: Don't act until transcription stabilizes
2. **Stability detection**: Track revision rate, wait for stability
3. **Action delay**: Brief delay before critical actions
4. **Visual smoothing**: Don't show every interim update
5. **Negation awareness**: Special handling for negation words
6. **Confirmation buffer**: Brief pause for user correction

**Detection**
- Track interim-to-final difference rates
- Monitor premature action errors
- Measure transcription stability time
- Compare interim-based vs. final-based accuracy
- Survey user experience with real-time display

## References

- [Google Cloud Streaming ASR](https://cloud.google.com/speech-to-text/docs/streaming-recognize) - Interim results handling
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Real-time issues
- [AWS Transcribe Streaming](https://docs.aws.amazon.com/transcribe/latest/dg/streaming.html) - Stability handling
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Timing issues
