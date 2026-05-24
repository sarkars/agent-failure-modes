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

**Mitigation Strategies**
1. **Quality detection**: Detect audio quality in real-time
2. **Adaptive behavior**: Adjust for poor quality conditions
3. **Packet loss concealment**: Interpolate missing audio
4. **Jitter buffer**: Buffer to smooth playback
5. **Quality-aware thresholds**: Adjust confidence thresholds
6. **User feedback**: "Audio quality is poor, please check connection"

**Detection**
- Monitor packet loss, jitter, latency
- Track MOS (Mean Opinion Score)
- Correlate quality metrics with WER
- Detect quality-based task failures
- Alert on quality degradation

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Quality issues
- [VoIP Quality](https://en.wikipedia.org/wiki/Voice_over_IP#Quality_of_service) - Technical background
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Audio issues
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
