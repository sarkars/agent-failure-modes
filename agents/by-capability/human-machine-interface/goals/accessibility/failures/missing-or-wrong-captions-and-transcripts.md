# Chatbot Voice Messages Without Captions or Transcripts: Missing or Wrong Captions and Transcripts

<!-- SEO
title: Chatbot Voice Messages Without Captions or Transcripts: Fix
description: A chatbot sends audio or video with no text version, or shows a wrong transcript of a voice message. How to caption, transcribe, and let people correct it.
search phrases:
- chatbot voice message transcript wrong
- chatbot audio reply no text deaf users
- ai assistant captions accessibility
- voice message transcription errors hard of hearing
- chatbot video attachment no captions
- how to caption audio replies in a chat widget
- speech to text transcript accuracy chatbot
-->

**Frequency**: Occasional

## Issue: A chatbot sends audio or video with no captions or transcript, or shows a transcript of a voice message that is wrong and can't be fixed, so deaf and hard of hearing users miss content or get a wrong result; the fix is an accurate text version of every audio and video item, shown to the user and correctable.

> **One line:** The bot talks, or hears the user, in audio, but the text version is missing, hidden, or wrong, and the user has no way to see what the bot understood or to fix it.

| | |
|---|---|
| **Channel** | Written for **chat**: voice messages, audio replies, and audio or video attachments in a chat widget. Live voice calls and live video are **PLANNED (voice phase)**, not measured. |
| **Stakes** | Medium to high. A wrong transcript can change a booking, a pickup, or a payment, and a missing one hides the whole reply. |
| **Who is affected** | People who are deaf or hard of hearing, and anyone who can't play audio (a quiet room, a muted phone, a noisy street). Speakers whose voices the speech recognizer handles poorly get more wrong transcripts. |
| **Frequency** | Occasional. I found no count of how often chat products ship audio or video without a text version. |
| **Pattern ID** | missing-or-wrong-captions-and-transcripts |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Audio and video items with a text version (captions or transcript). Target: 100% (tune). Accuracy on a reviewed sample is reported next to it. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Better speech recognition lowers errors, but the product still has to show the text, flag doubt, and let the user correct it. (Our judgment, not tested.) |
| **Also searched as** | chatbot voice message transcript · no captions on chatbot audio · wrong speech to text in chat · chatbot video no captions · transcript of audio reply · deaf users AI assistant audio |

## 1. In plain words
A chat product often handles sound: the user sends a voice message, the bot answers with an audio clip, or either side attaches a recording or video. If the text version is missing, a deaf or hard of hearing person gets nothing. If it is wrong and the user never sees it, the bot acts on words nobody said. Every audio or video item needs an accurate text version that the user can see and correct.

## 2. What it looks like
**Without the fix** (a pharmacy's chat widget; the user is hard of hearing and sends voice because typing a long reply on a phone is slow)
```
User: [voice message, 0:07] "Move my Lisinopril pickup to Thursday at 4 p.m."
Bot:  [audio reply, 0:11, no text]
User: I'm hard of hearing. Can you type that?
Bot:  Your pickup is confirmed for Tuesday at 4 p.m.
User: I said Thursday.
Bot:  Sorry, I didn't catch that. Please try again.
```
**With the fix** (same widget, after the rules in section 5)
```
User: [voice message, 0:07]
Bot:  Here is what I heard: "Move my Lisinopril pickup to [unclear] at 4 p.m." [Fix the text]
      I couldn't make out the day. Which day: Wednesday, Thursday, Friday, or Something else?
User: Thursday
Bot:  Pickup moved to Thursday at 4 p.m. at the Elm Street pharmacy. I'll reply in text unless you ask for audio.
```
What changed: the user saw the transcript, the bot flagged the part it was unsure of instead of guessing "Tuesday", and the reply came as text.

## 3. Why it happens
- **Audio is treated as an add-on.** The text reply is the real answer and the audio is generated later, so the audio message ships without the text attached.
- **The transcript stays inside the pipeline.** The product converts speech to text for the model but never shows it, so a recognition error is invisible until the bot acts on it.
- **Speech recognizers fail unevenly.** Error rates differ by speaker, and some systems invent words in pauses, so the people who most need the transcript get the worst one.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 1.2.2 requires "Captions are provided for all prerecorded audio content in synchronized media" (with one exception for media that is a labeled alternative to text). Its intent is to "enable people who are deaf or hard of hearing to watch synchronized media presentations." The failure F8 is captions "omitting some dialogue or important sound effects." Opened. | [W3C, Understanding SC 1.2.2](https://www.w3.org/WAI/WCAG22/Understanding/captions-prerecorded.html) | Covers prerecorded video with sound, not chat voice messages as such, and not live content. Used as design reasoning. This page does not say what the law requires of any company. |
| For prerecorded audio-only content, WCAG 1.2.1 requires that "An alternative for time-based media is provided that presents equivalent information for prerecorded audio-only content"; the page lists people who are deaf or hard of hearing among those who benefit. Opened. | [W3C, Understanding SC 1.2.1](https://www.w3.org/WAI/WCAG22/Understanding/audio-only-and-video-only-prerecorded.html) | Prerecorded audio only. A bot's audio reply is closest to this case, but the criterion was not written for chat. |
| W3C's captions guide says "You will need to edit automatic captions for accuracy," and that automatic captions can be used as a starting point. It adds that captions and transcripts "include the same text, so one can be used to develop the other." Opened. | [W3C WAI, Captions](https://www.w3.org/WAI/media/av/captions/) | Guidance for media producers. It describes no measured error rates. |
| W3C's transcripts guide says a transcript is required at Level A for prerecorded audio, and for live audio only at Level AAA, where "usually this needs to be a live text stream." Opened. | [W3C WAI, Transcripts](https://www.w3.org/WAI/media/av/transcripts/) | Live audio is PLANNED (voice phase) here; I use this only to mark the boundary. |
| Five commercial speech recognizers (Amazon, Apple, Google, IBM, Microsoft) had an average word error rate of 0.35 for Black speakers and 0.19 for white speakers (2,141 matched snippets per group, 19.8 hours; data mostly from 2014 to 2017). The authors blame "insufficient audio data from black speakers when training the models." Opened. | [Koenecke et al., PNAS, 2020](https://pmc.ncbi.nlm.nih.gov/articles/PMC7149386) | Interview audio, systems as they were in 2019 and earlier, not chat voice messages. It shows recognition errors are uneven, not how current systems score. |
| In a study of OpenAI's Whisper, roughly 1% of transcriptions contained entire hallucinated phrases or sentences not in the audio, and 38% of those hallucinations included explicit harms. The effect was disproportionate for speakers with longer non-vocal stretches, as in aphasia. Opened (abstract). | [Koenecke et al., arXiv 2402.08021](https://arxiv.org/abs/2402.08021v2) | I read the abstract only. Press coverage I saw only in a search summary says the rate has since dropped, which I did not verify. One system, tested in 2023. |
| The ADA.gov effective-communication guidance lists open, closed, and real-time captioning among aids for people who are deaf or hard of hearing. It says state and local governments must give "primary consideration" to the aid the person requests. Opened. | [ADA.gov, Effective Communication](https://www.ada.gov/resources/effective-communication/) | The page says it has "no legally binding effect." Written for covered entities and says nothing about AI agents. |

I did not use a "99% accurate" caption figure: it appeared in a search summary only, and the same summary said a law-firm analysis found no numeric threshold in the FCC's 2014 order. I found no study of caption or transcript errors in chat widgets.

**Public incident.** No public incident found for missing or wrong captions in an AI chatbot product. The nearest item I opened is the Whisper hallucination study, which is research, not an incident.

## 5. The fix
**The principle:** Every audio or video item in the chat has an accurate text version, the user sees what the bot heard, and the user can correct it.

**Do this**
1. **Send text with every bot audio reply.** The text reply is in the same message as the audio clip. Pass if no bot audio message lacks a text body.
2. **Show the transcript of every voice message the user sends,** next to the bot's reply, with a "Fix the text" action. Pass if each user voice message has a visible transcript.
3. **Mark doubt, don't guess.** Mark low-confidence words as `[unclear]` and ask about them before acting. Pass if no action runs on a day, time, amount, or name the recognizer flagged.
4. **Echo back the facts that matter.** Before an action, repeat numbers, dates, names, and medications from a voice message in text. Pass if the confirmation shows each one.
5. **Apply corrections everywhere.** The user's edited text replaces the transcript for the rest of the chat, and the bot re-answers from it. Pass if the next bot turn uses the corrected text.
6. **Label automatic text.** Say "automatic transcript, may have errors" until a person has checked it, and never call it "captioned" or "verified." Pass if every unreviewed transcript carries the label.
7. **Give a text version of media the bot sends,** such as a clip, recording, or video: captions on the video, or a transcript under the audio, with speakers and meaningful non-speech sounds named ("[phone rings]"). If none exists, say so and offer a written summary. Pass if each media message has one of these.
8. **Say what you could and couldn't hear in a user's attachment.** If the audio of an uploaded video or recording can't be read (no speech found, unsupported language, too noisy), the bot says so and doesn't summarize from the file name. Pass if a failed transcript never yields a summary.

**Reference design**
| Step | What the user sees |
|---|---|
| User sends voice | A transcript bubble under the clip, labeled "automatic", with `[unclear]` marks and [Fix the text] |
| Bot replies | Text first; audio is optional and carries the same words |
| Bot sends a clip or video | Captions or a transcript attached; if none, a note and a summary offer |
| Action with facts from voice | A text echo of dates, numbers, and names, then the action |

```
For every voice message, show the user the transcript, mark words you are unsure of, and ask before acting on them.
Send text with every audio reply. Attach captions or a transcript to every clip you send, label automatic text as automatic, and use the user's corrections for the rest of the chat.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The recognizer is unsure: show the transcript, mark `[unclear]`, and say which part to check. |
| Offer choices: 2-4 options plus "Something else", free text open | The unclear word has a few likely values (a day of the week): list them plus "Something else", and keep typing open. |
| Hand off to a person | The transcript is corrected twice and still wrong, or the user asks for a person: pass the corrected text. |

**Don't over-correct.** Don't ask the user to confirm every word of every voice message, and don't block a reply until they approve the transcript. Mark only low-confidence words and facts that drive an action. Don't remove audio for people who like it: text is added, not swapped in. Don't stamp "verified" on text nobody checked.

**Hand-off rule.** After two corrections of the same message, or if the user asks, hand off to a person who can read text and reply in text. Pass the corrected transcript with the handoff ([no channel switch or context lost](../../channel-selection/failures/no-channel-switch-or-context-lost.md)).

**Framework used:** [Conversation moves](../../../solutions-library/conversation-moves.md)

## 6. How to test it (short version)
All tests: **Not yet run.**

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Trigger every bot audio reply type | Each has a text body in the same message | 1 |
| 2 | Send a voice message in the widget | A transcript appears with a fix action | 2 |
| 3 | Send a voice message with a mumbled day of the week | `[unclear]` appears and the bot asks, no action runs | 3 |
| 4 | Send a voice message with a date, amount, and name | The text confirmation repeats all three | 4 |
| 5 | Correct a transcript, then ask a follow-up | The bot's next answer uses the corrected text | 5 |
| 6 | View an unreviewed transcript | It is labeled automatic | 6 |
| 7 | Have the bot send a recording and a video | Each has captions or a transcript, or a stated gap plus summary offer | 7 |
| 8 | Upload a silent video, then a noisy recording | Bot reports it couldn't read the audio and gives no invented summary | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. None is sourced.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Audio and video items with a text version (primary) | 100% | Log each audio or video message with a `text_equivalent` field; count the share that has one | Below 99% |
| Transcript word error rate on a reviewed sample | Set from baseline | A person compares a sample of transcripts to the audio each month, split by speaker group where users consent to share it | Rising for two months, or a group over 1.5 times the average |
| Voice messages with a visible transcript | 100% | Log `transcript_shown` per user voice message | Below 99% |
| Actions run on a flagged low-confidence fact | 0 | Join `asr_low_confidence_fields` to action events | Any |
| Transcript corrections per 100 voice messages | Track; set from baseline | Count `transcript_corrected` events | A step change after a model or vendor change |
| Voice users who stop using voice after a correction (counter-metric) | Track; set from baseline | Users with no voice message in 14 days after a correction | Rising |

### Detection signals (proposed, not yet calibrated)
Written for chat events. Live call captions are PLANNED (voice phase) and not measured here.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot sends an audio or video message with no text version | Message event with `media_type` set and `text_equivalent` empty | A decorative sound or background music marked decorative |
| User asks "what did it say?", "can you type that?", or "no captions" within 2 turns of a media message | User turn text matching a phrase list after a media event | The user's phone was muted by choice and they asked for a recap |
| User restates a voice message in text ("I said Thursday") | User turn after a voice message that repeats it with different words | A change of mind |
| Bot acts on a transcript with low-confidence words and no echo-back | `asr_low_confidence_fields` not empty, `echo_sent` false, action event follows | Low confidence on filler words that don't change the action |
| Bot summarizes an attachment whose transcript failed | `transcript_status` is failed or empty, and the bot reply describes the content | The summary came from the user's text message, not the audio |

**Starter rule:** every audio or video item in the chat has an accurate text version, the user sees what the bot heard, and the user can correct it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: missing-or-wrong-captions-and-transcripts
runs: pre_send
reads: [message.media_type, message.text_equivalent, transcript_shown, asr_low_confidence_fields, echo_sent, transcript_status]
trigger: a bot message with audio or video is about to be sent, or a voice message transcript is about to drive an action
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Wednesday", "Thursday", "Friday", "Something else"]
on_miss: rewrite
metric: audio and video items with a text version
counter_metric: voice users who stop using voice after a correction
status: proposed
```

## 8. Related patterns
- [Voice-only flows with no text alternative](voice-only-flows-with-no-text-alternative.md) - that page covers a voice journey with no text route at all. This page assumes a text route exists and covers the captions and transcripts inside it: missing, unlabeled, or wrong. Its common questions note that captioning the bot's speech is not enough alone.
- [Repair failure (voice)](../../voice/failures/repair-failure.md) - spoken corrections and "say that again." This page covers fixing the text of what the recognizer heard.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md) - uneven quality by speaker. This page covers the transcript and the correction path for it.
- [Streaming text read out token by token](streaming-text-read-out-token-by-token.md) - the screen-reader side of text replies. Text added here should be announced once, not piece by piece.

## 9. Common questions
### Do chatbot voice messages need a transcript?
Show one. The W3C pages I opened say a text alternative serves people who are deaf or hard of hearing, and require one for prerecorded audio at Level A. Whether your product must comply is for a qualified person to say, not this page.

### Are automatic captions good enough?
As a starting point, not a finished product. W3C says you will need to edit automatic captions for accuracy, and the PNAS study found word error rates of 0.35 and 0.19 for two speaker groups. Label them as automatic and let users fix them (rules 3, 5, 6).

### What about live calls and live video captions?
PLANNED (voice phase). The chat rules above cover recorded messages and attachments only, and nothing here is measured for live audio.

### Does a transcript replace the audio?
No. Add text and keep audio for people who want it. Rule 1 puts both in one message.

### How do I measure caption accuracy?
Sample transcripts each month, have a person compare them to the audio, and report word error rate, as in the metrics table. The target is set from your own baseline.

---
## Technical section (optional: include when the fix needs engineering)

### T1. Solution architecture
```
user audio -> speech-to-text (words + confidence) -> transcript store (editable)
           -> UI bubble ([unclear] marks, Fix the text) -> model reads the stored transcript
bot reply  -> text reply (source) -> optional audio generated from the same text
bot media  -> caption/transcript lookup -> attach, or stated gap + summary offer
```
The model reads the stored transcript, so a user's edit changes every later turn.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| 1: text body on every audio reply | Message builder rejects audio with no text | Test 1 and the `text_equivalent` log field |
| 3: no action on a flagged fact | Action gate reads `asr_low_confidence_fields` | Test 3 |
| 8: no summary after a failed transcript | Reply check on `transcript_status` | Test 8 |

### T3. Evals
- **Dataset:** 100 recorded voice messages with known text, including accented, noisy, and pause-heavy speech and short numbers and dates. Starting size, to tune.
- **Judge rubric:** Is the transcript shown? Are doubtful words marked? Does the bot ask before acting on them?
- **Metrics and starting thresholds:** Transcript shown 100%; actions on flagged facts 0. Word error rate is reported by group, with no target until a baseline exists.
- **Release gate:** A new audio message type without a text body, or a speech vendor swap without a rerun of the dataset, blocks the release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Items with a text version | Below 99% | Below 95% | Find the message type missing text |
| Actions on flagged facts | Any | Any in a day | Check the action gate |

### T5. Trade-offs
- Marking `[unclear]` adds a turn when the recognizer is wrong. Mark only what drives an action.
- Showing transcripts exposes the user's spoken words in the thread. Keep them under the same retention rules as chat text.

---
### Deep dive (optional)
- Modality notes: live voice and video captioning is PLANNED (voice phase). Nothing here comes from voice or video logs.
- Research log: five searches were run: "WCAG 1.2.2 captions prerecorded understanding success criterion", "automatic captions accuracy 99% FCC closed captioning quality rules", "voice message transcription accuracy deaf hard of hearing users WhatsApp iMessage", "Koenecke racial disparities automated speech recognition PNAS 2020 word error rate", and "Careless Whisper speech-to-text hallucination harms aphasia".
- Sources opened: the W3C pages, the PMC copy of the PNAS paper, the arXiv abstract, and ADA.gov. Search summaries only, not used: FCC caption quality coverage, vendor posts on WhatsApp transcripts.
