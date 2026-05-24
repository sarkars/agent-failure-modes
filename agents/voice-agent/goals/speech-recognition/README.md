# Goal: Speech Recognition

Accurately transcribe spoken input across diverse speakers, accents, and conditions. ASR errors are the #1 cause of voice agent failures.

## Business Context

- Misheard words lead to wrong actions
- Accent bias excludes user segments
- Domain vocabulary often missing from ASR
- Confidence scores unreliable in noisy conditions
- Errors compound through the pipeline

## Failure Patterns

| Failure Pattern | Frequency | Impact |
|-----------------|-----------|--------|
| [Accent and Dialect Bias](failures/accent-dialect-bias.md) | Very Common | High |
| [Homophones Confusion](failures/homophones-confusion.md) | Very Common | High |
| [Domain Vocabulary Gaps](failures/domain-vocabulary-gaps.md) | Common | High |
| [Filler Word Mishandling](failures/filler-word-mishandling.md) | Common | Medium |
| [Number and Date Errors](failures/number-date-errors.md) | Very Common | Critical |
| [Name Recognition Failures](failures/name-recognition-failures.md) | Very Common | High |
| [Low Confidence Mishandling](failures/low-confidence-mishandling.md) | Common | High |
| [Streaming ASR Instability](failures/streaming-asr-instability.md) | Common | Medium |

## Key Statistics

| Finding | Source |
|---------|--------|
| ASR accuracy drops 16 points on accented speech | Voice AI Research |
| 40% of voice agent failures from ASR errors | BeConversive 2026 |
| Word Error Rate (WER) for names: 20-40% | ASR Benchmarks |
| Number transcription errors: 5-15% | Voice Commerce Studies |
| Non-native speakers: 2x higher WER | Accent Bias Research |

## Key Metrics

- Word Error Rate (WER) overall and by segment
- Name/number accuracy rate
- Confidence score calibration
- Accent coverage metrics
- Domain vocabulary hit rate
