# What Are the Most Common Audio-Handling Failures in Voice AI Agents?

**Voice agents fail under degraded audio conditions because the audio pipeline — network transport, device hardware, acoustic environment, and call session state — sits upstream of ASR and silently feeds it corrupted input, so the recognizer is doing its best on data that is already lossy before a single phoneme is decoded.** Packet loss, codec compression, background noise, echo, competing speakers, and disconnections all degrade the same signal in different ways, and each failure mode compounds directly into word error rate rather than surfacing as a distinct, catchable error.

## Key Takeaways

- 6 patterns cover audio handling, splitting into signal-path degradation (network/device), acoustic interference (noise/echo/multi-speaker), and session lifecycle (disconnection) — three distinct failure surfaces upstream of ASR.
- Packet loss above 3-5% pushes WER increases of 25% or more, and noise levels below 5-10dB SNR push WER to 30-90%, meaning ASR accuracy is directly gated by audio quality, not just recognition-model quality.
- Device class alone drives a 2-3x WER variance — the same utterance succeeds on a premium phone and fails on cheap Bluetooth earbuds or a car speakerphone, because microphone quality and audio path vary that much.
- Mid-call disconnections occur in 5-15% of calls, but only 34% are properly classified and only 23% trigger a callback, meaning most disconnections lose partially-captured data with no recovery path.

## Scope

- **Signal-Path Degradation** — [audio-quality-degradation](failures/audio-quality-degradation.md), [device-compatibility-issues](failures/device-compatibility-issues.md). Both originate outside the acoustic environment — network transport (packet loss, jitter, codec) and device hardware (microphone quality, Bluetooth compression) — and degrade the signal before any sound-source competition enters the picture.
- **Acoustic Interference** — [background-noise-failures](failures/background-noise-failures.md), [echo-feedback-issues](failures/echo-feedback-issues.md), [multi-speaker-confusion](failures/multi-speaker-confusion.md). Grouped because all three involve a competing sound source — ambient noise, the agent's own echoed voice, or another human speaker — occupying the same channel as the target speech.
- **Session Lifecycle** — [call-disconnection-handling](failures/call-disconnection-handling.md). Distinct from the other two clusters because the failure is not signal quality but session-state management: detecting, classifying, and recovering from a call ending mid-conversation.

## When Audio Handling Matters

- The deployment spans real-world capture conditions — mobile networks, car speakerphones, Bluetooth headsets, smart speakers at distance — rather than a controlled, single-device test environment
- Voice interactions happen in physically noisy or acoustically complex settings — drive-throughs, streets, homes with TV or family members present, open-plan offices
- A pipeline owner needs to decide where audio pre-processing (AEC, noise suppression, jitter buffering) ends and where downstream confidence-gating or confirmation dialog needs to begin

## Cross-Pattern Insight

Every audio-handling pattern shares the same two-layer mitigation shape: a pre-processing stage that reduces the failure rate at the signal level (adaptive codecs and FEC for network loss, neural noise suppression and beamforming for ambient noise, acoustic echo cancellation with a TTS reference signal for echo, speaker diarization for multi-speaker scenes, real-time connection monitoring for disconnection), paired with a detection-and-response layer that treats degraded conditions as a first-class signal rather than an invisible input problem — lowering confidence thresholds, triggering confirmation prompts, or switching to a more constrained interaction mode (DTMF fallback, half-duplex muting) when quality drops below a threshold. None of the 6 patterns are solved by the ASR model alone; all require the audio front-end and the application logic to cooperate.

## Frequently Asked Questions

### What's the difference between audio-handling failures and speech-recognition failures?
Audio-handling patterns describe problems with the acoustic signal itself — noise, echo, packet loss, device variance, disconnection — before ASR ever runs. Speech-recognition patterns describe the recognizer misreading a clean(er) signal — accent bias, homophone confusion, domain vocabulary gaps. A noisy recording and a mistranscribed clean recording are different bugs with different fixes. See [Speech Recognition](../speech-recognition/).

### Can better ASR models compensate for poor audio quality?
Only partially. The patterns show WER increasing proportionally with packet loss, noise level, and device quality regardless of model capability — a noise-robust model trained on augmented data reduces but does not eliminate the gap, and severe degradation (packet loss >5%, SNR <5dB) routes to unusable transcription even with strong models. The reliable mitigation is architectural: pre-processing plus quality-aware confidence gating.

### What causes the same voice agent to perform differently across devices?
Because microphone quality, audio codec, and acoustic path differ by device class — the [device-compatibility-issues](failures/device-compatibility-issues.md) pattern documents a 2-3x WER variance across premium phones, budget phones, Bluetooth earbuds, car systems, and smart speakers, driven by hardware differences a single global pipeline configuration doesn't account for.

### How should a voice agent handle a mid-call disconnection?
[Call-disconnection-handling](failures/call-disconnection-handling.md) recommends classifying the disconnect type (clean end, network drop, accidental, frustrated) within 3 seconds, saving all partial conversation state immediately, and triggering a differentiated callback — a network drop or accidental hang-up merits a prompt callback that resumes from the saved step, while a frustrated hang-up after an objection should not be called back immediately.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Audio Quality Degradation](failures/audio-quality-degradation.md) | Packet loss, jitter, and codec compression degrade audio before ASR, increasing WER proportionally to signal loss |
| [Background Noise Failures](failures/background-noise-failures.md) | Ambient noise (traffic, crowds, machinery) drives WER from 5% at high SNR to 50-90% at low SNR |
| [Call Disconnection Handling](failures/call-disconnection-handling.md) | Mid-call drops go undetected or unclassified, losing partial data and skipping callback recovery |
| [Device Compatibility Issues](failures/device-compatibility-issues.md) | Microphone quality and audio path vary 2-3x in WER impact across phone, Bluetooth, car, and speaker device classes |
| [Echo Feedback Issues](failures/echo-feedback-issues.md) | Agent's own TTS output leaks into the mic, causing false triggers, self-interruption, or feedback squeal |
| [Multi Speaker Confusion](failures/multi-speaker-confusion.md) | Overlapping voices (TV, family, coworkers) blend into one transcript without speaker diarization |

**Total: 6 patterns**

## Related Goals

- [Speech Recognition](../speech-recognition/) — recognition-layer errors (accents, homophones, vocabulary gaps) that occur even on a clean signal
- [Voice Synthesis](../voice-synthesis/) — TTS output-side quality problems, the mirror concern to audio-handling's input-side focus
- [Conversation Flow](../conversation-flow/) — dialog-management failures that occur once audio has been successfully captured and transcribed
