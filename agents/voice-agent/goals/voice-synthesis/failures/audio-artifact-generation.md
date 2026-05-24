# Audio Artifact Generation

## Issue: TTS Produces Clicks, Pops, Distortion, or Other Audio Artifacts

**Frequency**: Occasional

**Symptoms**
- Clicking sounds between words
- Pops at sentence boundaries
- Unnatural breathing sounds
- Robotic distortion
- Volume spikes or drops

**Root Cause**
TTS synthesis can introduce audio artifacts, especially at concatenation points, sentence boundaries, or with certain phoneme combinations. Artifacts may come from the synthesis model, audio encoding, transmission, or playback. While often subtle, artifacts make the voice sound artificial and can be distracting or annoying.

**Example**
```
Scenario: Audio artifacts in TTS output

Text: "Thank you for calling. Your account balance is five hundred dollars."

Artifact issues:

1. Click at sentence boundary:
   "Thank you for calling [CLICK] Your account balance..."
   Cause: Discontinuity between synthesized segments

2. Breathing artifact:
   "Thank you [BREATH SOUND] for calling..."
   Cause: Model learned breathing but applies inconsistently

3. Volume spike:
   "Your account balance is FIVE HUNDRED dollars"
   Cause: Emphasis applied incorrectly

4. Distortion on sibilants:
   "Thank you for calling. Your account balanSSS..."
   Cause: S-sounds distorted at certain frequencies

5. Robotic warble:
   "Your accountttt balanceee is..."
   Cause: Vocoder artifacts in neural TTS

Artifact analysis:
  Utterances with audible artifacts: 8%
  Click/pop artifacts: 40% of issues
  Volume inconsistency: 25%
  Distortion: 20%
  Breathing/other: 15%
```

**Key Statistics**
From Audio Quality Research (2026):
- Noticeable artifacts: 5-15% of TTS output
- User-reported audio issues: 8%
- Artifact impact on MOS: 0.3-0.5 point reduction
- Click artifacts at boundaries: Most common
- Neural TTS artifacts different from concatenative

**Common Artifacts**
| Artifact | Cause | Fix |
|----------|-------|-----|
| Clicks | Segment boundaries | Crossfade, smoothing |
| Pops | Plosive emphasis | High-pass filter |
| Breathing | Model artifact | Post-processing |
| Volume spike | Emphasis bug | Normalization |
| Distortion | Encoding/bitrate | Higher quality encoding |
| Robotic | Vocoder | Better model |

**Contributing Factors**
- Low-quality TTS models
- Poor audio encoding (low bitrate)
- Network packet loss
- Segment concatenation issues
- No post-processing
- Playback device issues

**Mitigation Strategies**
1. **High-quality TTS**: Use modern neural TTS
2. **Post-processing**: Apply audio cleanup
3. **Higher bitrate**: Use quality audio encoding
4. **Crossfading**: Smooth segment transitions
5. **Quality monitoring**: Detect artifacts automatically
6. **A/B testing**: Compare TTS quality

**Detection**
- Audio quality metrics (SNR, THD)
- Automatic artifact detection
- User audio quality complaints
- A/B testing with quality focus
- Sample-based human evaluation

## References

- [Neural TTS Quality](https://arxiv.org/abs/2006.03575) - Artifact analysis
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Audio quality
- [TTS Evaluation Methods](https://arxiv.org/abs/2008.03095) - Quality metrics
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Audio issues
