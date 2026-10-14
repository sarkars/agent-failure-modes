# Speech and Audio AI Agent Failures by Goal: 66 Patterns, Causes, and Fixes

**Speech and Audio AI agents fail in 4 distinct ways, grouped by the goal each failure breaks.** Find the goal that matches what you are seeing, open its list, and use the fix on each pattern page.

## Key Takeaways

- 66 documented patterns across 4 goals; the most documented is [Conversation Flow](conversation-flow/) with 44.
- Each pattern page gives the symptoms, an example, the root cause, and mitigations.

## Speech and Audio Goals

| Goal | When it fails | Patterns |
|---|---|---|
| [Audio Handling](audio-handling/) | Voice agents fail under degraded audio conditions because the audio pipeline — network transport, device hardware, acoustic environment, and call session state | 6 |
| [Conversation Flow](conversation-flow/) | Voice agents fail at conversation flow because dialog management in voice has to solve real-time turn-taking, persona consistency, structured data capture | 44 |
| [Speech Recognition](speech-recognition/) | When the transcription layer either mishears open-vocabulary or ambiguous speech, or correctly produces uncertain output that the application then treats as certain. | 8 |
| [Voice Synthesis](voice-synthesis/) | When the synthesis layer applies a default, one-size-fits-all rendering to text that actually needs domain-specific pronunciation, content-appropriate emotion, or a stable persona | 8 |

**Total: 66 patterns**

## Frequently Asked Questions

### What makes conversation flow have so many more patterns than other speech-and-audio goals?

Conversation flow sits at the intersection of real-time audio mechanics (turn-taking, latency, silence handling — problems that don't exist in text chatbots) and business-logic dialog management (step sequencing, data capture, compliance, scope boundaries — problems that exist in any structured conversation, voice or text). See [Conversation Flow](conversation-flow/).

### What makes voice agents perform worse for some accents or names than others?

Because ASR acoustic and language models are trained predominantly on standard accents and common Western names — [accent-dialect-bias](speech-recognition/failures/accent-dialect-bias.md) documents a 10-20 point WER gap for non-standard accents, and [name-recognition-failures](speech-recognition/failures/name-recognition-failures.md) documents 20-40% name WER (2-4x higher for ethnic names) versus 5-10% for common words, both traceable to training-data underrepresentation. See [Speech Recognition](speech-recognition/).

### What's the difference between brand-term mispronunciation and general pronunciation errors?

[Brand-term-mispronunciation](voice-synthesis/failures/brand-term-mispronunciation.md) focuses specifically on brand names, acronyms, and version/number formats unique to a product or company. See [Voice Synthesis](voice-synthesis/).

## Related

- [Speech and Audio overview](../)
- [All agent failure patterns](../../../)
