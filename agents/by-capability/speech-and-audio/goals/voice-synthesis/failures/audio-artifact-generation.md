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

## Mitigation Strategies

### Prevention
1. **Modern Neural TTS with Waveform-Level Continuity**: Use neural vocoders (rather than older concatenative or lower-quality parametric TTS) that generate continuous waveforms without hard segment-boundary joins, directly addressing the clicks/pops that arise from discontinuities between synthesized segments. Trade-off: neural TTS is more compute-intensive per utterance, affecting latency/cost trade-offs discussed in response-latency-issues.
2. **Crossfade at Segment Boundaries**: When audio must be assembled from multiple synthesized or cached segments (e.g., dynamic slot insertion into a template), apply short crossfades at each join rather than hard concatenation, smoothing the discontinuity that otherwise produces audible clicks.
3. **High-Bitrate Encoding Through the Full Pipeline**: Ensure the audio encoding/transmission path (not just the TTS model itself) uses sufficiently high bitrate/quality settings end-to-end, since distortion on sibilants and general artifact perception often comes from downstream compression, not just the synthesis model.

### Detection & Response
1. **Automated Artifact Detection via Signal Analysis**: Run objective audio-quality metrics (SNR, THD, click/pop detectors looking for sharp discontinuities in the waveform) on a sample of production TTS output continuously, rather than relying solely on user complaints to surface artifact regressions.
2. **MOS Sampling Pipeline**: Regularly route a sample of synthesized utterances through human (or model-based) Mean Opinion Score evaluation, tracking the score over time so a gradual quality regression (e.g., from a TTS model update or codec change) is caught before it affects a large share of users.
3. **Complaint-Keyword Correlation**: Monitor user feedback/complaint text for audio-quality-specific keywords (glitchy, robotic, clicking) and correlate spikes against recent TTS model, encoding, or infrastructure changes to speed root-cause attribution.

### Architecture Patterns
1. **Post-Processing Audio Cleanup Stage**: Insert a dedicated post-processing stage after TTS synthesis (de-clicking, de-essing for sibilant distortion, normalization) as a separate, independently-tunable pipeline stage rather than depending entirely on raw TTS model output quality.
2. **A/B Quality Gate for TTS Model/Encoding Changes**: Route any TTS model version, vocoder, or encoding-pipeline change through an automated artifact-detection and MOS-sampling gate before full rollout, similar to a canary deployment but scored on audio-quality metrics specifically.
3. **Segment-Join Crossfade Library**: A shared, reusable audio-assembly utility that all dynamic-content-insertion call sites (numbers, names, slot values) must use, guaranteeing consistent crossfade treatment rather than each integration point handling concatenation ad hoc.

### Metrics
1. **artifact_detection_rate_percent**: Target: < 5% of sampled utterances; Alert threshold: > 15%
2. **mos_score**: Target: > 4.0; Alert threshold: < 3.5
3. **click_pop_incidents_per_1000_utterances**: Target: < 10; Alert threshold: > 40
4. **audio_quality_complaint_rate_percent**: Target: < 3%; Alert threshold: > 8%

### Alerts
1. **MOS Regression** (P2): Condition - rolling MOS sample average drops below 3.5. Action: Check for recent TTS model/vocoder/encoding changes, roll back if correlated.
2. **Artifact Detection Spike** (P1): Condition - automated artifact detection rate exceeds 15% of sampled utterances. Action: Page voice-quality on-call, pull raw samples for manual review, consider reverting latest TTS deploy.
3. **Complaint Keyword Surge** (P3): Condition - audio-quality-related complaint keywords increase > 3x week-over-week. Action: Correlate with recent deploys, prioritize investigation of segment-join and encoding pipeline.

## References

- [Neural TTS Quality](https://arxiv.org/abs/2006.03575) - Artifact analysis
- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Audio quality
- [TTS Evaluation Methods](https://arxiv.org/abs/2008.03095) - Quality metrics
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Audio issues
