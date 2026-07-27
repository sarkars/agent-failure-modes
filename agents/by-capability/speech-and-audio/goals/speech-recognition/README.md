# What Are the Most Common Speech-Recognition Failures in AI Voice Agents?

**Speech recognition fails in AI voice agents when the transcription layer either mishears open-vocabulary or ambiguous speech, or correctly produces uncertain output that the application then treats as certain.** Names, numbers, accents, and domain jargon are all open- or low-frequency vocabulary that general-purpose ASR models under-cover; homophones and streaming interim results are inherently ambiguous until enough context arrives; and confidence scores meant to flag that uncertainty are frequently ignored or miscalibrated, so a 45%-confidence guess gets executed with the same downstream trust as a 98%-confidence one.

## Key Takeaways

- 8 patterns span three failure classes: systematic accuracy gaps (accents, names, domain vocabulary), fundamentally ambiguous input (homophones, numbers/dates, fillers), and failure to act on ASR's own uncertainty signals (confidence mishandling, streaming instability).
- Accent and dialect bias produces a 10-20 point WER gap for non-standard accents, and name recognition error rates run 20-40% versus 5-10% for common words — both driven by training-data underrepresentation rather than a fixable acoustic quirk.
- 70% of voice agents reportedly ignore ASR confidence scores entirely, and proper thresholding is shown to reduce errors by 30-50%, meaning most of the accuracy loss in speech recognition is an application-layer gap, not a model-layer one.
- Domain-adapted ASR raises medical-term accuracy from roughly 72% to 94%, demonstrating that custom vocabulary injection — not a better general model — is what closes domain-specific gaps.

## Scope

- **Systematic Accuracy Gaps** — [accent-dialect-bias](failures/accent-dialect-bias.md), [name-recognition-failures](failures/name-recognition-failures.md), [domain-vocabulary-gaps](failures/domain-vocabulary-gaps.md). Grouped because all three stem from training-data underrepresentation of a vocabulary or acoustic class (non-standard accents, ethnic names, industry jargon) that a general-purpose model was never optimized for.
- **Fundamentally Ambiguous Input** — [homophones-confusion](failures/homophones-confusion.md), [number-date-errors](failures/number-date-errors.md), [filler-word-mishandling](failures/filler-word-mishandling.md). Grouped because the acoustic signal is genuinely underdetermined (to/two/too, 15/50, um/uh) and disambiguation requires context or grammar constraints the decoder doesn't always apply.
- **Uncertainty-Handling Failures** — [low-confidence-mishandling](failures/low-confidence-mishandling.md), [streaming-asr-instability](failures/streaming-asr-instability.md). Grouped because both concern how the application treats ASR's own signals of incompleteness or uncertainty — confidence scores and interim streaming hypotheses — rather than an inherent recognition error.

## When Speech Recognition Matters

- Users span diverse accents, dialects, or ethnic-name populations, and a pipeline owner needs to verify recognition accuracy isn't systematically worse for any demographic group
- The application acts on transcribed values without independent verification — order quantities, phone numbers, credit card digits, account names — where a single misheard digit or homophone breaks the transaction
- The agent uses streaming/real-time ASR and triggers actions before the final transcript is available, risking premature or reversed actions when interim results change

## Cross-Pattern Insight

Every speech-recognition pattern converges on the same architectural fix: constrain or boost the decoder with context (custom lexicons, format grammars, conversation-state priors, domain language models) to reduce ambiguity before decoding, then gate any residual uncertainty through calibrated confidence thresholds and confirmation dialog rather than trusting a single-pass transcript. The patterns repeatedly show that a stronger general ASR model narrows but does not close the accuracy gap — vocabulary injection, N-best hypothesis scoring, and threshold calibration are what actually move the accuracy numbers, and none of the three are a training-time-only fix.

## Frequently Asked Questions

### What makes voice agents perform worse for some accents or names than others?
Because ASR acoustic and language models are trained predominantly on standard accents and common Western names — [accent-dialect-bias](failures/accent-dialect-bias.md) documents a 10-20 point WER gap for non-standard accents, and [name-recognition-failures](failures/name-recognition-failures.md) documents 20-40% name WER (2-4x higher for ethnic names) versus 5-10% for common words, both traceable to training-data underrepresentation.

### Should a voice agent act on a low-confidence ASR transcript?
No. [Low-confidence-mishandling](failures/low-confidence-mishandling.md) shows accuracy at confidence <0.6 running 50-70% versus 97% at confidence >0.9, yet many systems apply no threshold at all — the fix is a tiered confidence ladder that routes low-confidence results to confirmation or repeat-request rather than auto-execution.

### Is it safe to act on streaming ASR interim results before the final transcript arrives?
Not for consequential actions. [Streaming-asr-instability](failures/streaming-asr-instability.md) documents 20-30% of utterances having significant interim-to-final changes, including negation flips ("cancel" without "don't" appearing until later) — critical actions should wait for the final result or a stability-gated interim.

### How much does domain-specific vocabulary customization actually help?
Substantially — [domain-vocabulary-gaps](failures/domain-vocabulary-gaps.md) reports general ASR at 70-80% accuracy on medical terminology versus 92-97% for domain-adapted ASR, a gap large enough to be a patient-safety issue for drug names and dosages specifically.

## Patterns

| Pattern | Mechanism |
|---|---|
| [Accent Dialect Bias](failures/accent-dialect-bias.md) | Non-standard accents see 10-20 point WER increases from training-data underrepresentation |
| [Domain Vocabulary Gaps](failures/domain-vocabulary-gaps.md) | Medical/legal/financial jargon substituted with phonetically similar common words |
| [Filler Word Mishandling](failures/filler-word-mishandling.md) | "Um," "like," and other disfluencies transcribed literally and misread as semantic content |
| [Homophones Confusion](failures/homophones-confusion.md) | Sound-alike words (to/two/too, there/their) resolved wrong without sufficient context |
| [Low Confidence Mishandling](failures/low-confidence-mishandling.md) | Confidence scores available but unused, so uncertain transcripts are acted on as if certain |
| [Name Recognition Failures](failures/name-recognition-failures.md) | Open-vocabulary personal/business names misheard, breaking identity and account lookups |
| [Number Date Errors](failures/number-date-errors.md) | Similar-sounding digits and ambiguous date/time formats corrupt quantities, phone numbers, and cards |
| [Streaming Asr Instability](failures/streaming-asr-instability.md) | Real-time transcription changes mid-utterance, risking action on a not-yet-final hypothesis |

**Total: 8 patterns**

## Related Goals

- [Audio Handling](../audio-handling/) — signal-quality problems (noise, packet loss, device variance) that precede and compound recognition errors
- [Voice Synthesis](../voice-synthesis/) — the output-side mirror of recognition: TTS mispronunciation and prosody rather than ASR mishearing
- [Conversation Flow](../conversation-flow/) — dialog-management failures downstream of a (correctly or incorrectly) recognized utterance
