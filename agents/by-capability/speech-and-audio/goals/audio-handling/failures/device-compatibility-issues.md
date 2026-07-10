# Device Compatibility Issues

## Issue: Performance Varies Significantly Across Devices

**Frequency**: Common

**Symptoms**
- Works on some phones, not others
- Smart speaker vs. phone differences
- Microphone quality varies dramatically
- Audio format compatibility issues
- Platform-specific failures

**Root Cause**
Users access voice agents from diverse devices: smartphones, smart speakers, cars, IoT devices, laptops. Each has different microphone quality, audio processing, codecs, and acoustic properties. A voice agent tuned for high-quality microphones may fail on cheap Bluetooth headsets. Platform differences (iOS vs. Android) add further variation.

**Example**
```
Scenario: Voice agent across devices

Same utterance: "Set a reminder for 3pm"

iPhone 15 (high-quality mic):
  Audio quality: Excellent
  ASR confidence: 0.98
  Result: Success ✓

Budget Android phone:
  Audio quality: Moderate
  ASR confidence: 0.82
  Result: Success ✓

Cheap Bluetooth earbuds:
  Audio quality: Poor
  ASR confidence: 0.55
  Result: "Set a reminder for free PM" ✗

Car speakerphone:
  Audio quality: Variable (road noise)
  ASR confidence: 0.45
  Result: "Set reminder for... [unintelligible]" ✗

Smart speaker across room:
  Audio quality: Echo + distance
  ASR confidence: 0.70
  Result: "Set a reminder for 3pm" ✓ (far-field optimized)

Device comparison:
  Premium smartphone: 95% task success
  Budget smartphone: 85% task success
  Bluetooth headset: 70% task success
  Car system: 65% task success
  Speaker + far-field: 88% task success (optimized)
```

**Key Statistics**
From Device Research (2026):
- WER variation across devices: 2-3x
- Budget vs. premium mic: 15% WER difference
- Car audio issues: 30% of in-car users affected
- Bluetooth audio: 20% worse than wired
- Smart speaker far-field: Requires special handling

**Device Categories**
| Device | Quality | Challenges |
|--------|---------|------------|
| Premium phone | High | Few issues |
| Budget phone | Medium | Mic quality |
| Bluetooth earbuds | Variable | Compression, latency |
| Car system | Variable | Noise, echo, hands-free |
| Smart speaker | Medium | Far-field, echo |
| Laptop mic | Low | Distance, noise |

**Contributing Factors**
- No device-specific tuning
- Single audio pipeline for all
- No device detection
- Codec compatibility issues
- No device-specific thresholds
- Testing only on high-quality devices

## Mitigation Strategies

### Prevention
1. **Device Fingerprinting and Detection**: Identify device type/model, OS, and audio input path (built-in mic, Bluetooth, wired headset, speakerphone) at session start via client metadata or codec/negotiation signals, so downstream processing can select device-appropriate parameters. Trade-off: fingerprinting adds a small amount of session-setup complexity and must handle unknown/spoofed device strings gracefully.
2. **Per-Device Parameter Profiles**: Maintain tuned ASR confidence thresholds, noise-suppression aggressiveness, and gain normalization per device class (premium phone, budget phone, Bluetooth, car system, smart speaker far-field), rather than one global configuration. Trade-off: profile maintenance overhead grows with device diversity; requires periodic re-tuning as new device classes appear.
3. **Codec and Format Negotiation**: Support multiple audio codecs/sample rates and negotiate the best mutually supported option per device/network rather than assuming a single format, with automatic fallback when a preferred codec is unavailable.

### Detection & Response
1. **Success-Rate Monitoring by Device Class**: Continuously track task completion and ASR confidence segmented by device type; when a device class's success rate drops significantly below the fleet average, treat it as a compatibility regression rather than a one-off support ticket.
2. **Low-Confidence Device Fallback**: For device classes with a known history of poor audio quality (e.g., cheap Bluetooth earbuds), proactively lower automatic-action thresholds and increase confirmation prompting rather than waiting for per-utterance failures to accumulate.
3. **New Device Class Detection**: Flag traffic from previously unseen device fingerprints so they can be manually profiled and validated before they scale to a meaningful share of traffic.

### Architecture Patterns
1. **Device-Aware Pipeline Configuration**: Route each session through a configuration resolver that selects noise-suppression, AEC, and confidence-threshold parameters based on detected device class, rather than hardcoding one pipeline for all input sources.
2. **Tiered Interaction Fallback by Device**: For device classes with historically poor recognition (e.g., car speakerphone, budget Bluetooth), automatically enable a more constrained interaction style (shorter prompts, explicit confirmations, DTMF fallback) instead of the full open-ended dialog used for high-quality devices.
3. **Continuous Device Regression Testing**: Maintain a test-audio corpus recorded/replayed through representative hardware (premium phone, budget phone, common Bluetooth models, in-car systems) and run it in CI against every ASR/pipeline change to catch device-specific regressions before deployment.

### Metrics
1. **task_success_rate_by_device_class**: Target: no device class more than 15pp below fleet average; Alert threshold: gap > 25pp
2. **wer_variance_across_devices**: Target: < 2x between best and worst device class; Alert threshold: > 3x
3. **unrecognized_device_fingerprint_rate_percent**: Target: < 5% of sessions; Alert threshold: > 15%
4. **device_specific_confirmation_rate_percent**: Target: matches configured profile (e.g., 30-40% for low-quality classes); Alert threshold: deviates > 20pp from profile target

### Alerts
1. **Device-Class Success Rate Collapse** (P1): Condition - a device class (e.g., a specific Bluetooth headset model) drops below 50% task success rate. Action: Pull sample audio for that class, verify pipeline configuration, consider temporary confirmation-mode override for affected class.
2. **Untuned New Device Surge** (P2): Condition - traffic share from an unrecognized/undefaulted device fingerprint exceeds 10% of daily volume. Action: Prioritize profiling and tuning for the new device class before it further dilutes aggregate metrics.
3. **Codec Negotiation Failures** (P2): Condition - codec negotiation fallback-to-lowest-common-denominator rate exceeds 20% of sessions. Action: Investigate client/server codec support mismatch, update supported codec list.

## References

- [BeConversive: Voice AI Challenges](https://www.beconversive.com/blog/voice-ai-challenges) - Device issues
- [AssistYou: Why AI Mishears Callers](https://www.assistyou.ai/blog/why-your-ai-voice-agent-mishears-callers) - Hardware issues
- [AppInventiv: Voice Agent Failures](https://appinventiv.com/blog/why-ai-voice-agents-fail/) - Compatibility
- [Bluejay: Production Failures](https://getbluejay.ai/resources/voice-agent-production-failures) - Real examples
