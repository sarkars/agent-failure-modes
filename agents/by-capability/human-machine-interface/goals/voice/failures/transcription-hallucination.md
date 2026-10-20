# Speech to Text Making Up Words: Transcription Hallucination

<!-- SEO
title: Speech to Text Makes Up Words: Fix Transcription Hallucination
description: Speech-to-text can turn silence or noise into invented phrases. See what one study found, and a design that checks for speech before it trusts a transcript.
search phrases:
- whisper hallucination silence
- speech to text makes up words
- whisper transcribes thank you on silent audio
- ai transcription invents sentences
- voice note transcript has words nobody said
- how to stop whisper hallucinating
- speech recognition hallucination non-speech audio
(Phrases come from result titles and wording seen during research and from the source papers, not from volume data.)
-->

**Frequency**: Occasional

## Issue: Speech-to-text can turn silence, noise, or long pauses into phrases nobody said; the fix is to check that speech is present, flag suspect transcripts, and confirm before acting.

> **One line:** A voice note with nothing audible comes back as a confident sentence, and the bot acts on words the user never said.

| | |
|---|---|
| **Channel** | Written for **chat**: a bot that transcribes uploaded audio or voice messages and replies from the transcript. Audio-level signals for live voice (silence length, no-speech probability) are **PLANNED**. |
| **Stakes** | Low to high. An invented phrase in a call note, a cancellation, or a clinical summary can be acted on. |
| **Who is affected** | Anyone whose audio has silence, noise, or long pauses; the study below found more hallucination for speakers with aphasia, who pause more |
| **Frequency** | Occasional (our judgment). One 2023 study of one system found about 1% of transcriptions with invented phrases. I found no rate for current production bots. |
| **Pattern ID** | transcription-hallucination |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | Hallucinated-phrase rate on silence and non-speech test audio. Target: near 0 (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. Newer versions hallucinated less in the study's own re-test, but "always output text" is a property of the recognizer, so a check outside it is still needed. (Our judgment, not tested.) |
| **Also searched as** | whisper hallucination · speech to text invents words · transcript says thank you on silence · ai voice note transcript wrong · asr hallucination non-speech |
| **Flag** | V (voice) |

## 1. In plain words
A speech-to-text model is built to turn audio into words, so given silence or noise it can still return words. The invented text reads like a normal transcript, so nothing looks wrong. The fix is to treat "no speech heard" as a valid result, flag transcripts that do not fit the audio, and let the user confirm before the bot acts.

## 2. What it looks like
The transcripts below are made up for this page.

**Without the fix**
```
User: [sends a 40-second voice note recorded with the phone in a pocket; no one speaks]
Bot:  Transcript: "Thank you. Please cancel my appointment."
Bot:  Done. Your Thursday 2:30 cleaning at Oak Street Dental is canceled.
User: Wait, I didn't ask to cancel anything.
Bot:  I'm sorry, you said "Please cancel my appointment." Your slot has been released.
User: (calls the front desk to rebook)
```

**With the fix**
```
User: [sends the same 40-second voice note]
Bot:  I couldn't hear any speech in that voice note, so I haven't changed anything.
      Your Thursday 2:30 cleaning is still booked. What would you like to do?
      [Record again] [Type it instead] [Talk to the front desk] [Something else]
User: Type it instead
Bot:  Go ahead. I'll read back what I understand before I change anything.
```
The fixed bot does not treat the empty note as words, keeps the booking, and offers a way forward.

## 3. Why it happens
These are our reading of the pattern; the study supports the first two in part.
- **The recognizer must output something.** No-speech is not an answer the model is built to give. In a news report the lead author suggested the model may be "seeding silence as some sort of word".
- **Pauses raise the risk.** In the study, a higher share of non-speech time in a clip was associated with hallucination, and speakers with aphasia had far more non-speech time.
- **Nothing checks the transcript against the audio.** The bot treats the transcript as what the user said, and the original audio is not compared or not kept.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "Roughly 1%" of transcriptions contained entire hallucinated phrases or sentences (abstract); 1.4% in the results. 187 audio segments were involved. | [Koenecke et al., *Careless Whisper*, FAccT 2024 (arXiv v2)](https://arxiv.org/html/2402.08021v2). Opened and read. | One system (OpenAI Whisper API, April and May 2023 runs, default settings), English clips from AphasiaBank (13,140 segments). Not pure silence tests. The authors say 1.4% is likely an undercount. |
| 38% of hallucinated transcriptions contained at least one harm type: 19% perpetuate violence, 13% inaccurate associations (made-up names, relationships, health statuses), 8% false authority (for example website links). | Same paper. Opened and read. | The percentage is of hallucinated transcriptions, not of all transcriptions. "Harm" is the authors' coding. |
| Hallucinations in 1.7% of aphasia segments vs 1.2% of control (p=0.019). Non-vocal share 41% vs 15%. Non-vocal share was positively associated with hallucination in a regression. | Same paper. Opened and read. | Correlation in one dataset. The authors hypothesize that pauses and silence are a cause. |
| By December 2023, 12 of the 187 segments still hallucinated, which the authors attribute likely to late-November 2023 updates to Whisper. They conclude it "is improving at hallucination reduction" but still hallucinates. | Same paper. Opened and read. | The authors re-tested their own segments; this is not an independent measurement of current performance. |
| The authors found "exactly 0 comparable hallucination concerns" in Google, Amazon, Microsoft, AssemblyAI, and RevAI services. | Same paper. Opened and read. | 2023 test on one dataset; vendors change. Do not assume your service is safe. |
| Whisper returned "Thank you" for a silent audio file. About 1% figure repeated; lead author said OpenAI had improved the model since. | [Cornell Chronicle, June 11, 2024](https://www.news.cornell.edu/stories/2024/06/ai-speech-text-can-hallucinate-violent-language). Opened and read. | News article. The silent-file example is one anecdote, not a measured rate. |
| Fine-tuning 3 of 20 decoder heads of Whisper-large-v3 gave over 80% reduction in non-speech hallucination, with under 0.1% WER degradation on LibriSpeech. | [Calm-Whisper, arXiv 2505.12969](https://arxiv.org/abs/2505.12969). **Abstract opened only**; PDF text could not be read. | Research result on specific test sets. Not used in the fix. |
| Feeding Whisper non-speech audio produced a recurring set of hallucinations; a "bag of hallucinations" post-filter lowered word error rate. | [Investigation of Whisper ASR Hallucinations Induced by Non-Speech Audio, arXiv 2501.11378](https://arxiv.org/abs/2501.11378). **Abstract opened only**; no numbers in it. | Used only as support for checking known phantom phrases, not for any figure. |

**Not used.** A 2024 Associated Press report on hospital transcription (counts from several researchers and a company's audio-deletion practice) and a vendor blog's silence figures were seen **only in search summaries**; I could not open the originals, so no number from them is on this page. I found no independent measurement of the current hallucination rate.

## 5. The fix
**The principle:** Make "no speech heard" a valid result, and never let an unchecked transcript trigger an action.

**Do this**
1. **Check for speech first.** If speech is not detected in the audio, the reply says so and shows no transcript.
2. **Flag fit problems.** A transcript that is only a stock closing phrase ("Thank you.") on a file longer than 10 seconds, or the same phrase repeated 3 or more times in a row, is marked "unverified" (both numbers are starting points to tune).
3. **Confirm before acting.** For any action (cancel, pay, send, save to a record), read back what the bot understood and wait for a yes. Never act on an unverified transcript.
4. **Say what was and was not heard.** Show transcripts as "what I heard", and mark unclear or flagged parts instead of smoothing them over.
5. **Keep the audio for checking.** The original file stays available to the user and to review for as long as the transcript is used.
6. **Do not drop real speech.** Quiet, slow, or halting speakers get a recheck choice, not a "no speech" refusal on the first pass.
7. **Test on non-speech.** Before release, run silence, room noise, music, and long-pause clips; any non-empty transcript on pure silence blocks the release.

**Reference design: transcript check**
| Check | Result | Bot does |
|---|---|---|
| Speech detected, transcript fits the audio | Pass | Reads back and acts after a yes |
| No speech detected | Empty | "I couldn't hear any speech", offers choices |
| Speech detected but transcript is flagged | Unverified | Shows it as unverified, asks the user to confirm or retype |

```
When you receive audio, never present a transcript if no speech was detected: say you heard no speech.
If a transcript is only a stock closing phrase or a repeated phrase, call it unverified.
Before any action based on a transcript, read it back and wait for a yes.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The transcript is empty or flagged: say what was heard, and give the audio or a retype path. Do not use it when the transcript fits the audio and is confident. |
| Offer choices: 2-4 options plus "Something else", free text open | After "no speech heard": "Record again", "Type it instead", "Talk to the front desk", "Something else". Do not offer them when the user already confirmed the transcript. |
| Hand off to a person | The same note fails twice, or the action is high stakes and still unconfirmed. Do not hand off if the user asked to keep typing with the bot. |

**Don't over-correct.** Rejecting audio too eagerly fails the people who pause most, such as speakers with aphasia or a speech impairment. Do not refuse low-volume or halting speech on the first pass, and do not make users confirm every harmless line. Keep confirmation for actions and flagged transcripts, and track the rate of real speech rejected.

**Hand-off rule.** After two failed notes, or any unconfirmed high-stakes action, pass a person the audio, the transcript with its flag, and what was tried ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | A 40-second silent voice note | No transcript is shown; the reply says no speech was heard (1) |
| 2 | Speech with a long pause in the middle | The real words are kept; nothing is added during the pause (6, 7) |
| 3 | A transcript that is only "Thank you." on a 40-second file | Marked unverified (2) |
| 4 | A voice note asking to cancel, with clear speech | Read back, and the action waits for a yes (3) |
| 5 | A flagged transcript and a request to cancel | No action until the user confirms or retypes (3, 4) |
| 6 | A quiet, slow speaker | A recheck choice, not a refusal (6) |
| 7 | A pure-silence test clip returns text in the release suite | The release is blocked (7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Hallucinated-phrase rate on silence and non-speech test audio** (primary) | Near 0 | Run a fixed set of silence, noise, music, and long-pause clips each release; count non-empty transcripts | Any non-empty transcript on pure silence; over 1% on the whole set |
| Actions taken from a transcript the user did not confirm | 0 | Log each action with its confirmation flag | Any |
| Flagged transcripts shown as unverified | 100% | Sampled review of flagged cases | Below 95% |
| Real speech rejected as "no speech" (counter-metric) | Track; lower is better | Human-labeled sample of rejected notes | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published. File duration is upload metadata, so signals 1 to 4 can be logged without analyzing audio.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Written for text: the whole transcript is a stock closing phrase ("Thank you.") on a file longer than 10 seconds | Transcript text plus upload duration | A short thank-you the user really said, with silence around it |
| Written for text: transcript words per second of audio is far below the speaker's usual rate | Word count divided by file duration | A slow or pausing speaker |
| Written for text: the same phrase appears 3 or more times in a row | Transcript text | The user repeated it on purpose, such as counting |
| Written for text: the user's next message says "I didn't say that" or "that's not what I said" | Next user turn after a transcript | A real misrecognition, or the user misremembering |
| PLANNED for voice: text emitted for a segment with long silence or a high no-speech probability | Needs audio-level values from the recognizer; none are recorded here | Whispered or very quiet speech |

**Starter rule:** never present or act on a transcript when no speech was detected, and read back before any action.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds beyond the starting points above)
```yaml
pattern_id: transcription-hallucination
runs: pre_send
reads: [upload.duration_seconds, transcript.text, transcript.flag, action.pending, action.confirmed]
trigger: a transcript from user audio is about to be shown or used for an action
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Record again", "Type it instead", "Talk to a person", "Something else"]
on_miss: rewrite
metric: hallucinated-phrase rate on silence and non-speech test audio
counter_metric: real speech rejected as no speech
status: proposed
```

## 8. Related patterns
- [Repair failure](repair-failure.md): the agent hears a real correction wrongly. Here the recognizer hears words that were never spoken.
- [Background noise failures](../../../../speech-and-audio/goals/audio-handling/failures/background-noise-failures.md): noise lowers accuracy. This page covers noise or silence becoming fluent invented text.
- [Low confidence mishandling](../../../../speech-and-audio/goals/speech-recognition/failures/low-confidence-mishandling.md): confidence scores are not used. Invented text can arrive with no warning at all.
- [Silence misinterpretation](../../../../speech-and-audio/goals/conversation-flow/failures/silence-misinterpretation.md): the agent misreads a pause during a live call, not the transcript.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the same missing way to check, in chat answers.

## 9. Common questions
### Why does speech to text write "thank you" when nobody is talking?
In one news report, the lead author of the study below said Whisper produced "Thank you" for a silent file, and suggested silence may be treated as a word. It is a single example, not a measured rate. See [section 4](#4-why-it-matters).

### Is transcription hallucination only a Whisper problem?
In the 2023 study, the authors found no comparable cases at five other services, so they called it an OpenAI-specific concern then. That was one dataset and one year, so test your own service on silence.

### Does it still happen after newer versions?
The authors' own re-test in December 2023 found 12 of 187 segments still hallucinated, down from the earlier runs. I found no independent measurement of current versions, so run the test in [section 6](#6-how-to-test-it-short-version).

### What should a bot do with a voice note that is silent?
Say no speech was heard, change nothing, and offer to record again or type it. See [section 5](#5-the-fix).

---
## Technical section

### T1. Solution architecture
```
audio upload -> speech check (voice activity / no-speech flag) -> recognizer
             -> transcript check (stock phrase, repeats, length vs duration)
             -> reply (heard / no speech / unverified) -> readback -> action after yes
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No transcript shown when no speech is detected | Before the reply | Test 1 |
| No action without a confirmation | Action layer | Test 4, 5 |
| Silence suite blocks release | CI | Test 7 |

### T3. Evals
- **Dataset:** a silence, noise, music, and long-pause set, plus a matched set of real speech with pauses (include slow and quiet speakers). Start with 100 clips of each kind (starting point).
- **Judge rubric:** is any text emitted for a clip with no speech? Is every word in the transcript in the audio?
- **Metrics and starting thresholds:** non-speech hallucination near 0; real speech rejected tracked. Starting points to tune.
- **Release gate:** block a deploy if a pure-silence clip returns text or real-speech rejection rises.

### T5. Trade-offs
- A speech check can cut off quiet speech; keep the recheck choice and the original audio.
- Reading back adds a turn; keep it for actions and flagged transcripts.

---
### Deep dive
- **Open question.** The main study used speech clips with pauses, not pure silence. I found no opened test of how a voice-activity check changes the rate, so test it on your own set.
- **Modality notes.** Live voice (PLANNED): silence length and no-speech probability could gate the transcript before the agent speaks.
- **References.** [Koenecke et al. 2024](https://arxiv.org/html/2402.08021v2) (opened); [Cornell Chronicle](https://www.news.cornell.edu/stories/2024/06/ai-speech-text-can-hallucinate-violent-language) (opened); [Calm-Whisper](https://arxiv.org/abs/2505.12969) and [non-speech hallucination study](https://arxiv.org/abs/2501.11378) (abstracts opened).
