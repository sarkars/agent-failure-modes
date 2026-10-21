# Chatbot Ignored My Voice Note: Voice Notes and Audio Attachments Ignored

<!-- SEO
title: Chatbot Ignored My Voice Note: Fix Audio Attachments Ignored
description: Why a chatbot drops a voice note or audio file, or transcribes it badly without saying so, and a fix: transcribe, show the transcript, say what was unclear.
search phrases:
- chatbot ignores voice message
- whatsapp bot only supports text messages
- chatbot can't read my voice note
- ai chatbot audio attachment not working
- how to handle voice notes in a whatsapp chatbot
- bot replies to voice message with wrong answer
- chatbot audio file too large unsupported format
- show transcript of voice note in chatbot
(Phrases come from result titles and wording seen during research, not from volume data.)
-->

**Frequency**: Common

## Issue: A user sends a voice note or audio file in a text chat and the assistant drops it, answers as if nothing was attached, or transcribes it badly without saying so; the fix is to transcribe it, show the transcript, say what could not be heard, and let the person correct it.

> **One line:** The person talks for 40 seconds, and the bot answers as if they had sent nothing, or answers a different question than the one they spoke.

| | |
|---|---|
| **Channel** | Written for **chat** (text chat where the user attaches an audio file or sends a voice note: WhatsApp, Telegram, web chat). Live voice-call signals are PLANNED, not written. |
| **Stakes** | Low to high. A dropped note costs a retype; a mis-transcribed account number, dose, or address in a billing, health, or delivery chat can cost money or time. |
| **Who is affected** | People who find talking easier than typing (driving, on a phone, low typing comfort, some disabilities), and anyone sending a long or detailed message |
| **Frequency** | Common as a design gap (our judgment). Public evidence is vendor documentation and forum anecdotes (section 4); no study counts how often chat products drop audio. |
| **Pattern ID** | voice-notes-and-audio-attachments-ignored |
| **Family** | [Multimodal input](../README.md) |
| **Goal** | Whatever the person attaches, the assistant says what it received and works from what is really there. |
| **Primary metric** | Audio attachments handled (acknowledged, transcribed and shown back). Starting target: 100% (tune on your own data). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Models transcribe better, but a dropped or unsupported attachment is a product-flow issue, and a better transcriber still needs a step that shows its result. (Our judgment, not tested.) |
| **Also searched as** | whatsapp bot doesn't understand voice messages · chatbot says it can only read text · ai ignored my audio file · voice note not transcribed · bot answered the wrong thing from my voice message |

## 1. In plain words
In many chat products a voice note arrives as a file, not as text. If nobody built a step to open that file and turn it into words, the bot sees a message with no text and either says nothing, repeats itself, or replies "Sorry, I can only read text". A second version is quieter: the audio is transcribed, but wrongly, and the bot answers the wrong words without showing the person what it heard.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "Pioneer Valley Power" is an invented utility with a WhatsApp support bot.

**Without the fix**
```
User: (sends a 40-second voice note: "Hi, I was charged $212 on the 3rd but my bill
      says $128. I paid by card ending 4471. Can someone fix that?")
Bot:  Sorry, I can only read text messages. How can I help you today?
User: (types) never mind
      (the person leaves; the billing problem is still open)
```

**With the fix**
```
User: (sends the same 40-second voice note)
Bot:  I got your voice note (0:40). Here is what I heard:
      "Hi, I was charged $212 on the 3rd but my bill says $128. I paid by card ending
      4471. Can someone fix that?"
      I couldn't make out one word near the end ("fix" or "check"?). Is this right?
      [Yes, that's right] [Fix the text] [Something else]
User: Yes, that's right.
Bot:  Thanks. You were charged $212 on the 3rd, and your bill shows $128. I'm opening
      a billing review for the card ending 4471 and will message you here within 2 business days.
```
The fixed bot says what it received, shows the transcript, names the part it was unsure about, and lets the person confirm or correct before it acts. (The "2 business days" is invented for the example.)

## 3. Why it happens
- **Audio arrives as a file, and text is what the bot reads.** On WhatsApp the incoming message is a media object, not a string. A flow that only handles the text field sees an empty message. Vendor docs show the audio is received but not always processed (section 4).
- **Support is a setting, not a given.** A transcription step has limits (file size, format, language) and often a switch that must be turned on. When it is off, or the file breaks a limit, nothing tells the user.
- **The transcript is treated as truth.** When transcription does run, its output goes straight to the model. Nobody shows it to the person, so a misheard name, amount, or negation becomes the question the bot answers.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WhatsApp Cloud API lists supported audio types (AAC, AMR, MP3, M4A, OGG) with a 16 MB limit; OGG must use the OPUS codec and only mono is accepted. Incoming media has a 100 MB limit, and a larger file triggers a webhook with error code 131052, and the page says to warn the customer. Media IDs from webhooks expire after 7 days. | [Meta, WhatsApp Business Platform, Media](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media). Opened 2026-10-21 (fetch tool summary of the page). | Vendor documentation, undated in what was returned. It shows limits exist and that the business must handle the oversize case; it does not show how often bots fail. |
| Telegram's Bot API says "For the moment, bots can download files of up to 20MB in size", and the download link is "guaranteed ... valid for at least 1 hour". It describes a Voice object as "a voice note". | [Telegram Bot API reference](https://core.telegram.org/bots/api). Opened 2026-10-21 (fetch tool summaries of three page sections). | Vendor documentation. The limit is stated as temporary ("for the moment"). |
| OpenAI's speech-to-text guide says files "can be up to 25 MB", lists input formats as mp3, mp4, mpeg, mpga, m4a, wav and webm, says Whisper "supports 98 languages, but accuracy varies by language", and says corrections should be checked against the original audio. | [OpenAI, Speech to text guide](https://developers.openai.com/api/docs/guides/speech-to-text). Opened 2026-10-21 (fetch tool summary). | Vendor documentation. The list shown has no ogg, so a WhatsApp or Telegram voice note (OGG/OPUS) may need converting first. That is an inference, not a tested result. |
| Anthropic's chat upload article lists document types (PDF, DOCX, CSV, TXT, HTML, ODT, RTF, EPUB, JSON, XLSX) and image types (JPEG, PNG, GIF, WebP) and does not mention audio. | [Anthropic, *Upload files to Claude*](https://support.claude.com/en/articles/8241126-upload-files-to-claude), dated July 23, 2026 on the page. Opened 2026-10-21. | Silence in one help article is not proof that a product cannot take audio. It shows a chat can list its accepted types without audio, so a user may not know. |
| Chatfuel's help page says its AI "uses speech recognition to transcribe audio messages and then processes them like any other text message", and that the bot may not respond to voice messages if automations are off, "Incoming messages" is not set, the channel is disconnected, or audio quality is poor. | [Chatfuel docs, why Chatfuel does not process audio messages](https://chatfuel.com/docs/ai-features/why-chatfuel-does-not-process-audio-messages). Opened 2026-10-21 (fetch tool summary). | Vendor documentation for one product. It shows that a missing setting makes audio go unanswered. |
| A Make Community user reported on July 7, 2026 that a test audio note to a WhatsApp chatbot got the normal bot reply plus "Sorry — only text messages are supported.", and that the message kept appearing after the scenario was disabled and the webhook deleted. | [Make Community thread](https://community.make.com/t/sorry-only-text-messages-are-supported-message-in-whatsapp-what-is-causing-this/111770). Opened 2026-10-21. | Anecdote, one user. The only reply asked the user to share the solution; the source of the message is not known. |
| A GoHighLevel feature request (August 16, 2025) says that when a lead sends audio or an image to a WhatsApp AI appointment bot, the bot "simply repeats the last message in a loop", and asks for a text-only fallback message. | [GoHighLevel ideas board](https://ideas.gohighlevel.com/ad-reporting-and-attribution/p/handling-non-text-messages-in-whatsapp-ai-appointment-booking-bot). Opened 2026-10-21. | Anecdote, one user. The page showed one vote and no status. |
| A paper tested a Dutch speech recognizer and compared word error rates across gender, age, regional accents and non-native accents. Another paper reported word error rate per English accent and found the model less accurate on accents less common in its training data. | [Feng et al., arXiv:2103.15122](https://arxiv.org/abs/2103.15122) (2021); [Cámbara et al., arXiv:2105.05041](https://arxiv.org/abs/2105.05041) (2021). Opened 2026-10-21; only the abstract pages were read, and neither page gave error-rate values. | Shows accuracy differs by speaker group in those systems. It does not give a rate for any current product, so no number is claimed here. |

**Public incident.** No public incident found. Searches run: WhatsApp business API audio limits; OpenAI speech-to-text limits; chatbot ignores voice message; Telegram getFile voice limit; WhatsApp chatbot not responding to voice notes. Results were vendor docs and the two forum anecdotes above, not a dated, sourced incident.

## 5. The fix
**The principle:** When an audio file or voice note arrives, say you received it, show the transcript, name any part you could not hear or open, and act only after the person confirms or corrects it.

**Do this**
1. **Acknowledge every audio attachment.** The first line of the reply says an audio message arrived and how long it is (or its file name). Never answer a voice-note turn as if it were empty.
2. **Transcribe, then show the transcript.** Put the transcript in the reply, labeled "Here is what I heard". Do not hide it in logs.
3. **Say what could not be heard.** Mark unclear words, names, numbers, and amounts, and ask about them. Never fill a gap with a guess.
4. **Let the person correct it.** Offer "Yes, that's right", "Fix the text", and "Something else"; accept a typed correction as the new text.
5. **Check the file before the model sees it.** Compare type, size, and length with your transcription limits (for example the 25 MB speech-to-text limit and the 16 MB, 20 MB and 100 MB figures in section 4; confirm them against live docs). Convert formats when you can, such as OGG/OPUS to a format your transcriber accepts.
6. **If you cannot transcribe it, say so and give a way forward.** "I can't open this audio (too long). Send a shorter note or type it." Never a bare "I can only read text" without a next step, and never silence.
7. **Confirm before acting on high-risk details.** Amounts, dates, doses, addresses, and account numbers in a transcript are read back and confirmed before any action (see [over-confirmation](../../dialogue-management/failures/over-confirmation.md) for the cost line).
8. **Keep the audio's status in the log.** One of `transcribed_confirmed`, `transcribed_unconfirmed`, `not_transcribed` plus a reason (`too_large`, `unsupported_format`, `too_long`, `transcription_off`, `transcription_failed`, `no_speech_detected`).

**Reference design: status and reply rule**
```json
{"attachments": [
  {"type": "audio", "duration_s": 40, "status": "transcribed_unconfirmed",
   "transcript": "Hi, I was charged $212 on the 3rd but my bill says $128 ...",
   "unclear": [{"near": "end of note", "options": ["fix", "check"]}]}
]}
```
```
When an audio attachment arrives: say it arrived, show the transcript, list anything unclear, and ask
the person to confirm or correct it. Do not take action on amounts, dates, doses, addresses, or account
numbers until they confirm. If the audio could not be transcribed, say so and why, and give one way forward.
Never reply as if no audio was sent.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The transcript has unclear words or the file could not be opened: show what was heard, mark the gaps, say what is known and what is not. |
| Offer choices: 2-4 options plus "Something else", free text open | After showing the transcript: "Yes, that's right", "Fix the text", "Something else". Skip them when the person already replied in words. |
| Ask one clarifying question | One unclear word changes the answer ("fix" or "check"?): ask that one question. Not when the answer is the same either way. |
| Lead with the answer | The transcript is clear and the request is low-stakes: show the transcript in one line, then answer. |
| Hand off to a person | The audio cannot be transcribed twice in a row, or it is high stakes (billing dispute, medical, safety) and the details stay unclear. Not if the person asked to stay with the bot. |

**Don't over-correct.** Do not make the person confirm a transcript that is clear and low-stakes, and do not paste a long transcript above a one-line answer. For a short, clear note, a one-line "I heard: ..." followed by the answer is enough. Do not offer a menu in place of the transcript. The cost of too much checking is the [over-confirmation](../../dialogue-management/failures/over-confirmation.md) failure.

**Hand-off rule.** If two attempts to get usable text fail, or the unclear part is a high-stakes detail, offer a person and pass along the audio's status, the transcript so far, and the unclear parts, so the person does not have to start over ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | Send a clear 40-second voice note with a billing question | Reply says an audio message arrived, shows the transcript, and asks to confirm (rules 1, 2, 4) |
| 2 | Send a note with a mumbled amount | The unclear amount is marked and asked about; no guessed number (rule 3) |
| 3 | Send an audio file over your size limit | Reply says it is too large and gives a way forward; not silence, not "text only" (rules 5, 6) |
| 4 | Send an OGG/OPUS voice note to a transcriber that does not list ogg | The flow converts it or says it cannot open it; never an empty answer (rule 5) |
| 5 | Send a silent or noise-only note | Reply says no speech was found; no invented transcript (rules 3, 6) |
| 6 | Send a short, clear, low-stakes note ("what are your hours?") | One-line "I heard" and the answer; no confirm step (Don't over-correct) |
| 7 | A note containing a dose, address, or account number | Details are read back and confirmed before any action (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Audio attachments handled (acknowledged, transcribed and shown back)** (primary) | 100% | Audio attachment events joined to the next bot turn; count turns that name the audio, show a transcript or a reason, with sampled review | Below 95% |
| Replies to an audio turn that treat it as empty | 0 | Bot turn after an audio event with no mention of the audio (string check plus sampled review) | Any |
| Transcripts corrected by the user | Track only; set from baseline | Corrections after a transcript turn; each one is a caught error | None; near 0 for months may mean users skim |
| Transcript shown on clear, low-stakes notes with a confirm step (counter-metric) | Track; set from baseline | Confirm steps on notes with no unclear marks and no high-risk details | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; live voice-call signals are PLANNED. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Audio attachment event, and the next bot turn does not mention audio | `attachment.type = audio` joined to the bot turn text | The UI showed the status outside the message body |
| Bot turn after an audio event is a generic "how can I help" or "I can only read text" with no next step | Bot turn text matched against a short template list | A deliberate text-only product that says so before the user sends audio |
| Same bot turn text sent twice after an audio event | Repeated bot text across two turns | A retry after a platform delivery error |
| User re-sends the same content as typed text right after a reply | Text turn after an audio turn with a matching intent | The user adding detail on purpose |
| User says "did you hear my message" or "I sent a voice note" | User turn after a bot turn that followed an audio event | The user is checking a correct reading |
| Audio event with no `status` logged | `attachment` event missing `status` or `reason` | An old client that does not report status yet |

**Starter rule:** when an audio attachment arrives, say you received it, show the transcript, name what could not be heard, and let the person correct it before you act.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: voice-notes-and-audio-attachments-ignored
runs: pre_send
reads: [attachment.type, attachment.status, attachment.reason, attachment.transcript, attachment.unclear, draft_reply.text]
trigger: a reply is about to be sent in a turn that contains an audio attachment
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, lead_with_answer, hand_off]
choices: ["Yes, that's right", "Fix the text", "Something else"]
on_miss: rewrite
metric: audio attachments handled (acknowledged, transcribed and shown back)
counter_metric: transcript shown on clear, low-stakes notes with a confirm step
status: proposed
```

## 8. Related patterns
- [Silent attachment failures](../../chat-interface/failures/silent-attachment-failures.md): the closest page. It covers documents and images that were too large, unsupported, or only partly read. This page is about audio: the file has to be turned into words first, the transcript can be wrong, and the fix shows the transcript back.
- [Transcription hallucination](../../voice/failures/transcription-hallucination.md): speech-to-text invents words from silence or noise. This page covers the earlier failure (audio not handled at all) and the show-and-confirm step that also catches invented text.
- [Missing or wrong captions and transcripts](../../accessibility/failures/missing-or-wrong-captions-and-transcripts.md): the accessibility view of a wrong or hidden transcript, including audio the bot sends.
- [Word-error-rate-only evaluation](../../voice/failures/word-error-rate-only-evaluation.md): why one error-rate number does not show whether a transcript is good enough for the task.
- [Atypical speech mishandled](../../voice/failures/atypical-speech-mishandled.md): speech that recognizers handle worse.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the general failure when an unclear word becomes a guess.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): the opposite failure to avoid when adding a confirm step.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): "Sorry, I can only read text" is a generic error with no next step.

## 9. Common questions
### Why does my WhatsApp chatbot ignore voice messages?
A voice note arrives as a media file, not as text. If your flow reads only the text field, or the transcription step is off or the file breaks a limit, the bot has nothing to answer. Vendor docs and the forum anecdotes in [section 4](#4-why-it-matters) show that missing settings and unsupported media are common causes.

### Should the bot transcribe the voice note or ask the person to type?
Transcribe it when you can, show the text, and let the person fix it. Ask them to type only when you cannot open the file, and say why. See the Do this list in [section 5](#5-the-fix).

### What are the size and format limits for audio?
They vary by product and change. Section 4 lists what the Meta, Telegram and OpenAI pages said when opened on 2026-10-21 (16 MB audio and 100 MB incoming media for WhatsApp, 20 MB downloads for Telegram bots, 25 MB for OpenAI transcription). Check the live pages before you rely on them.

### Can I trust the transcript of a voice note?
Not blindly. The OpenAI guide says accuracy varies by language and that corrections should be checked against the original audio, and the two papers in section 4 found accuracy differing by accent. That is why the fix shows the transcript and asks about unclear parts.

### Do I have to confirm every transcript?
No. Confirm when the note has unclear words or high-risk details such as amounts, doses, or addresses. For a short, clear, low-stakes note, a one-line "I heard: ..." and the answer is enough.

---
## Technical section

### T1. Solution architecture
```
inbound audio -> validate (type, size, duration) -> reject early with a reason and next step   (rules 5, 6)
              -> convert if needed (e.g. OGG/OPUS -> accepted format) -> transcribe
              -> speech check (no speech? say so)  -> mark low-confidence spans
              -> status {transcribed_confirmed | transcribed_unconfirmed | not_transcribed, reason}   (rule 8)
              -> reply: acknowledge + transcript + unclear parts + confirm choices   (rules 1-4)
              -> high-risk fields? hold the action until the person confirms   (rule 7)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Every audio attachment gets a status and reason | Media intake service | Status-coverage metric |
| Reply to an audio turn names the audio | Pre-send check | Tests 1, 3; primary metric |
| Transcript shown before any action on high-risk fields | Action gate | Test 7 |
| No transcript produced for silent or noise-only audio | Speech check before the model | Test 5 |

### T3. Evals
- **Dataset:** 40 audio items to start: clear notes, noisy notes, mumbled amounts, silent files, oversize files, an OGG/OPUS voice note, accented speech, and two short low-stakes controls.
- **Judge rubric:** does the reply acknowledge the audio; is the transcript shown; are unclear parts marked; is any guessed value stated as heard; is a clear low-stakes note answered without a confirm step?
- **Metrics and starting thresholds:** all are starting points to tune: 100% of audio turns acknowledged; 0 guessed values stated as heard; 0 invented transcripts on silent files.
- **Release gate:** block a deploy if any audio test in the eval set gets a reply that treats the note as empty (starting point).

### T5. Trade-offs
- Showing a transcript adds length; keep it to one line for short, clear notes.
- Transcription adds cost and latency per note; the acknowledgment can go out first ("Got your voice note, reading it now").

---
### Deep dive (optional)
- **Modality notes.** Live phone calls handle audio differently (streaming, barge-in, read-back by voice). Those signals are PLANNED and not written here; see [transcription hallucination](../../voice/failures/transcription-hallucination.md) for the voice-side check.
- **Sources read through a fetch tool summary.** The Meta, OpenAI, Chatfuel, Anthropic and Telegram pages and the arXiv abstract pages were opened with a fetch tool that returned summaries, not raw page text. Quoted phrases and numbers are the ones the tool reported; recheck them on the live pages before quoting them in your own docs.
- **Read only in search summaries (unverified, not used in the fix):** that third-party WhatsApp guides list five sendable audio types and the same 16 MB figure; that a May 2026 Claude Code feature request reports a rejected WAV attachment.
