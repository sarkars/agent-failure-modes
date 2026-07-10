# Audio Quality Degradation

## Issue: Poor Audio Quality from Network or Device Issues

**Frequency**: Common

**Symptoms**
- Choppy or stuttering audio
- Missing words or phrases
- Robotic/digitized speech
- Delayed or out-of-sync audio
- Complete audio drops

**Root Cause**
Audio quality can degrade from network issues (packet loss, jitter, latency), codec compression, or device problems (poor microphone, low bandwidth mode). When audio quality drops, ASR accuracy drops proportionally. Brief dropouts can lose critical words; severe degradation makes speech unrecognizable.

**Example**
```
Scenario: Network-degraded audio

User (clean): "I want to book a flight to Chicago"

With 2% packet loss:
  Received: "I want to book a fli-- to Chicago"
  ASR: "I want to book a fly to Chicago"
  
With 5% packet loss:
  Received: "I wa-- to bo-- a flight to Chi--go"
  ASR: "I want to BO a flight to Chicago"
  
With 10% packet loss:
  Received: "I -- to -- a fl-- to --cago"
  ASR: [Fails to transcribe]

With high jitter (variable delay):
  Audio arrives out of order
  Re-assembly creates artifacts
  Words sound robotic/warped

With codec degradation (low bitrate):
  User: "flight" sounds like "fight"
  User: "three" sounds like "free"
  Sibilants lost

Quality impact analysis:
  Packet loss 0-1%: WER +2%
  Packet loss 1-3%: WER +10%
  Packet loss 3-5%: WER +25%
  Packet loss >5%: Often unusable
```

**Key Statistics**
From Audio Quality Research (2026):
- Calls with quality issues: 15-25%
- Packet loss >2%: Significant impact
- Jitter >50ms: Noticeable degradation
- Low bitrate codec: +15% WER
- Mobile network issues: 2x landline

**Quality Degradation Types**
| Issue | Cause | Impact |
|-------|-------|--------|
| Packet loss | Network congestion | Missing audio |
| Jitter | Variable latency | Choppy playback |
| Latency | Distance, routing | Delay issues |
| Low bitrate | Bandwidth saving | Compressed quality |
| Codec artifacts | Poor codec | Distortion |

**Contributing Factors**
- Unreliable network connection
- Mobile network variability
- Low-bandwidth codec selection
- No quality detection
- No adaptive behavior
- International/long-distance calls

## Mitigation Strategies

### Prevention
1. **Adaptive Codec/Bitrate Selection**: Negotiate audio codec and bitrate based on measured network conditions (RTT, packet loss, available bandwidth) before and during the call, falling back to narrowband-robust codecs (e.g., Opus with FEC) when conditions degrade. Trade-off: higher-resilience codecs use more CPU for encoding/decoding and may add slight latency.
2. **Forward Error Correction and Packet Loss Concealment (PLC)**: Encode redundant information (FEC) so lost packets can be reconstructed, and apply PLC (waveform interpolation) to smooth gaps under 20-30ms so ASR doesn't see a hard discontinuity. Trade-off: FEC increases bandwidth usage 10-20%.
3. **Jitter Buffer Tuning**: Use an adaptive jitter buffer that grows during bursty jitter and shrinks during stable periods, re-ordering out-of-sequence RTP packets before they reach the ASR pipeline. Trade-off: larger buffers reduce artifacts but add end-to-end latency, directly working against response-latency goals.

### Detection & Response
1. **Real-Time Quality Metrics Correlated with WER**: Continuously compute packet loss %, jitter, and MOS-estimate (e.g., E-model) per call, and correlate against ASR confidence/WER in near-real time. When quality crosses a threshold (e.g., packet loss > 3%), lower ASR confidence thresholds and trigger confirmation prompts rather than acting on likely-wrong transcripts.
2. **Quality-Triggered User Messaging**: When degraded-quality is detected for more than ~2 consecutive seconds, have the agent proactively say "Your connection seems unstable, could you move closer to your router?" rather than silently guessing at garbled input.
3. **Session Quality Dashboard with Anomaly Alerts**: Aggregate per-call quality signals into a live dashboard; alert when the rolling rate of degraded-quality calls spikes above baseline, which often indicates an upstream carrier/network issue rather than a client-side one.

### Architecture Patterns
1. **Quality-Aware Confidence Gating**: Feed real-time SNR/packet-loss estimates into the same confidence-threshold logic used for ASR results, so a "medium confidence" transcript is treated as "low confidence" when quality is poor — forcing a clarification turn instead of a wrong action.
2. **Adaptive Jitter Buffer + PLC Pipeline**: Standard VoIP resilience stack (jitter buffer -> PLC -> AEC -> ASR) deployed as a dedicated audio pre-processing stage ahead of the recognizer, decoupled from application logic so it can be tuned/replaced independently.
3. **Graceful Degradation Ladder**: Define explicit fallback tiers (full ASR -> keyword-spotting fallback -> DTMF/menu fallback) triggered by quality thresholds, so severe degradation (>5% packet loss) routes to a more robust interaction mode instead of repeatedly failing free-form recognition.

### Metrics
1. **packet_loss_rate_percent**: Target: < 1%; Alert threshold: > 3% sustained for 10s
2. **wer_by_quality_tier**: Target: WER delta < 5% between clean and degraded tiers; Alert threshold: delta > 20%
3. **jitter_ms_p95**: Target: < 30ms; Alert threshold: > 50ms
4. **quality_triggered_clarification_rate_percent**: Target: 5-10% of calls; Alert threshold: > 25% (indicates systemic network issue)

### Alerts
1. **Severe Packet Loss Spike** (P1): Condition - packet loss > 5% for more than 15 seconds on an active call. Action: Trigger fallback interaction mode (DTMF/menu), notify network ops, flag call for quality review.
2. **WER-Quality Correlation Breach** (P2): Condition - WER exceeds baseline by 25%+ while quality metrics are simultaneously degraded. Action: Auto-lower confidence thresholds for affected calls, surface clarification prompts.
3. **Fleet-Wide Quality Degradation** (P1): Condition - percentage of calls with packet loss > 2% exceeds 2x the 7-day baseline. Action: Page network/infra on-call, check upstream carrier/SBC health.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Quality issues
- [VoIP Quality](https://en.wikipedia.org/wiki/Voice_over_IP#Quality_of_service) - Technical background
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Audio issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
