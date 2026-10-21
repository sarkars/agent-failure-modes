# Chatbot File Too Large, No Warning: No Warning About Input Limits

<!-- SEO
title: Chatbot File Too Large With No Warning: Fix Input Limits
description: Why a chatbot lets people upload files, pages or minutes past its limits without saying so, and a fix: state limits before upload and give a clear over-limit message.
search phrases:
- chatbot file too large error
- chatgpt file upload limit
- gemini audio upload limit 10 minutes
- claude uploaded file is too large
- how to show file size limit before upload
- file upload error message too large ux
- whatsapp chatbot media file too big
- chatbot upload failed no reason
(Phrases come from result titles and wording seen during research, not from volume data.)
-->

**Frequency**: Common

## Issue: The chat accepts a file, a long PDF, or a long recording with no word about its size, page, or length limits, and the person learns about the limit only after a failed or cut upload; the fix is to state the limits before upload and, when a file is over, say which limit, by how much, and what to do.

> **One line:** The person uploads a 22-minute video or a 300-page PDF, waits, and gets "Upload failed" or a vague answer, because nobody told them the chat takes 10 minutes or 100 pages.

| | |
|---|---|
| **Channel** | Written for **chat** (web and app chat with an attach button, and messaging channels such as WhatsApp and Messenger). Voice-call signals are PLANNED, not written. |
| **Stakes** | Low to high. A wasted upload costs minutes; an insurance claim, tax document, or medical record that cannot be sent before a deadline costs more. |
| **Who is affected** | People sending long PDFs, scans, phone videos, call recordings, or many files at once; people on slow mobile data, where a failed upload costs the most time |
| **Frequency** | Common as a design gap (our judgment). Every vendor page we opened publishes limits (section 4); none says the limit is shown in the chat before upload. No study counts this. |
| **Pattern ID** | no-warning-about-input-limits |
| **Family** | [Multimodal input](../README.md) |
| **Goal** | Whatever the person attaches, the assistant says what it received and works from what is really there. |
| **Primary metric** | Over-limit uploads with a clear message. Target: 100% (starting point; tune on your own data). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Limits are set by the product, the plan, and the channel, and the model often never sees an over-limit file; the interface has to state the limit and catch the file. (Our judgment, not tested.) |
| **Also searched as** | uploaded file is too large · chatbot won't take my pdf · how long can an audio file be in gemini · max file size chatgpt · whatsapp media too big for bot |

## 1. In plain words
Every chat product has limits: megabytes per file, pages per PDF, minutes of audio or video, files per message, and uploads per day. The failure is that the person finds out the hard way: after a long upload, through a bare "Upload failed", a raw server error, or a reply that quietly covers only part of the file. A good chat says the limits next to the attach button and, when a file is over, names the limit, the file's own size, and a next step.

## 2. What it looks like
Illustrative transcripts (invented for this page, not from a real product). "Saguaro Mutual" is an invented Phoenix home insurer with a claims chat. Its limits here (10 minutes of video, 100 MB, 100 pages) are invented for the example.

**Without the fix**
```
User: (attaches kitchen_leak.mp4, a 22-minute phone video, 410 MB; no limits shown anywhere)
      (the upload bar runs for 4 minutes on mobile data)
Bot:  Upload failed. Please try again.
User: (tries again; waits 4 more minutes)
Bot:  Upload failed. Please try again.
User: Why?? My claim is due Friday.
Bot:  I'm sorry for the trouble. Is there anything else I can help with?
```

**With the fix**
```
(Under the attach button: "Video up to 10 min and 100 MB · PDF up to 100 pages · up to 5 files")
User: (attaches kitchen_leak.mp4, 22 minutes, 410 MB)
Bot:  This video is 22 minutes and 410 MB. This chat takes videos up to 10 minutes and 100 MB,
      so I didn't upload it. Your message is saved.
      You can send the 2-3 minutes that show the damage, split it into three clips,
      or send photos instead.
      [Send a shorter clip] [Send photos] [Something else]
```
The fixed chat states the limits before the person picks a file, checks the file before the long upload starts, names both numbers, keeps the message, and gives ways forward.

## 3. Why it happens
- **Limits live in help articles, not in the composer.** Vendors publish limits on support pages (section 4), and those limits differ by file type, plan, and channel. The attach button rarely repeats them, so the person cannot check before sending.
- **The check runs late and speaks in server terms.** If size or length is checked only after upload, the person waits for a failure, and the error is written for engineers: one public report shows a raw byte value as the message (section 4).
- **The chat layer does not know which limit was hit.** Upload, channel, and model limits sit in different services. When only "failed" reaches the chat, the bot cannot say "too long" versus "too big", so it falls back to a generic apology.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google's Gemini Apps page says up to 10 files per prompt, "Each video can be up to 2 GB", other file types "can be up to 100 MB", total video length up to 5 minutes and total audio up to 10 minutes (longer on paid plans), and that there are rolling upload limits over time. | [Google, *Upload & analyze files in Gemini Apps*](https://support.google.com/gemini/answer/14903178?hl=en). Opened 2026-10-21 (fetch tool summary); no update date shown. | Vendor documentation. Shows that limits cover size, minutes, file count, plan, and time window at once, which is a lot for a person to know before upload. It does not say what the chat shows when one is hit. |
| Anthropic lists "500MB per file", "Up to 20 files per chat", "PDFs are limited to 1000 pages", says PDFs of 101 to 1000 pages are read as text only, and that a PDF over 1000 pages shows an "Uploaded file is too large" error. | [Anthropic, *Upload files to Claude*](https://support.claude.com/en/articles/8241126-upload-files-to-claude), dated July 23, 2026 on the page. Opened 2026-10-21 (fetch tool summary). | Vendor documentation. The summary named one error text; the article did not describe messages for other limits. |
| Meta's WhatsApp Cloud API lists 16 MB for audio and video, 100 MB for documents, 5 MB for images, and 100 MB for incoming media; an oversize incoming file triggers error code 131052, and the page tells the business to "Send customers a warning message" when it happens. | [Meta, WhatsApp Business Platform, Media](https://developers.facebook.com/documentation/business-messaging/whatsapp/business-phone-numbers/media). Opened 2026-10-21 (fetch tool summary). | Vendor documentation. The platform hands the warning to the business; if the bot builder skips it, the customer hears nothing. |
| Meta's Messenger Platform says assets can be saved "up to 25 MB", with "8 MB for images", and a fetch timeout of 75 seconds for videos and 10 seconds for other files. | [Meta, Messenger Platform, Saving Assets](https://developers.facebook.com/documentation/business-messaging/messenger-platform/send-messages/saving-assets). Opened 2026-10-21 (fetch tool summary). | Vendor documentation for what a business can send and save, not for what a user can upload. Shows the limits a Messenger bot works within. |
| OpenAI has a ChatGPT file uploads help article with per-file size, token, image, and daily upload limits. | [OpenAI Help Center, *File uploads FAQ*](https://help.openai.com/en/articles/8555545-file-uploads-faq). **Not opened** (HTTP 403 on 2026-10-21); read only through a search summary. | Unverified. We quote none of its numbers, and the fix does not rely on it. |
| A Document360 feature request (June 30, 2026) reports no upfront sign of a 150 MB limit, no progress indicator, and an error reading "Request body too large. The max request body size is 157286400 bytes." It asks for a client-side check, the limit shown near the attach control, and sizes in MB. | [Document360 feedback board](https://feedback.document360.com/feature-request/p/file-upload-fails-silently-until-server-timeout-with-no-upfront-size-guidance). Opened 2026-10-21 (fetch tool summary). | One user, one product, and a document editor rather than a chatbot. It shows the exact failure shape; status "under review", 1 vote. |
| The GOV.UK Design System says a too-big error should read "The selected file must be smaller than [largest file size]", and gives set wording for wrong type and too many files. The NSW Government design system says to "highlight any input restrictions to the users upfront, for example format or size" and that users should not need to re-upload files. | [GOV.UK Design System, File upload](https://design-system.service.gov.uk/components/file-upload/); [NSW Design System, File upload](https://designsystem.nsw.gov.au/components/file-upload/index.html). Both opened 2026-10-21 (fetch tool summaries). | Government form guidance from the UK and Australia, not US and not chat. We use it for wording only. |

**Public incident.** None found. Searches covered vendor upload limits and upload error-message guidance; results were documentation and one feature request, not a dated incident.

## 5. The fix
**The principle:** State the limits before the person uploads, check the file before the long upload, and when a file is over a limit, say which limit, the file's own value, and what to do next.

**Do this**
1. **Show the limits at the attach control.** Size, pages, minutes, file count, and accepted types, in plain units, for the person's plan and channel. One line; a "more" link for the rest.
2. **Check before the long upload.** Read size, page count, duration, and type on the device or at the first byte, and stop an over-limit file before the person waits for it.
3. **Name the limit and both numbers.** "This video is 22 minutes; this chat takes up to 10." Never a bare "Upload failed" and never a raw byte count.
4. **Give a next step that fits the limit.** Too long: send a shorter clip or split it. Too many pages: send the pages that matter or split the file. Too big: compress or send photos. Wrong type: name one accepted type. Daily cap: say when it resets.
5. **Keep everything else.** The typed message and any files under the limit stay; the person never re-types or re-attaches them.
6. **When a limit can only be hit after upload, say so in the reply.** A context or text-only limit gets its own line ("I read the text of this 300-page PDF but not its charts"). The full read-status rules are in [silent attachment failures](../../chat-interface/failures/silent-attachment-failures.md).
7. **On messaging channels, answer the platform's oversize event.** When the platform reports a file too large (such as WhatsApp error 131052), send the person a message with the limit and a next step; never leave the turn silent.
8. **Log every over-limit upload with its limit.** One of `too_large`, `too_many_pages`, `too_long`, `too_many_files`, `unsupported_type`, `rate_limited`, plus the file's value and the limit, and whether a message was shown.

**Reference design: limit record and reply rule**
```json
{"upload_check": {"file": "kitchen_leak.mp4", "result": "over_limit", "limit": "too_long",
  "file_value": "22 min", "limit_value": "10 min", "also_over": [{"limit": "too_large", "file_value": "410 MB", "limit_value": "100 MB"}],
  "message_kept": true, "message_shown": true}}
```
```
Before an upload: show the accepted types and the size, page, length, and file-count limits for this
user's plan and channel. When a file is over a limit: do not start the full upload. Name each limit it
breaks, the file's own value and the limit in plain units, keep the user's message, and give one next
step per limit. Never reply "Upload failed" alone.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A file is over a limit: the first line says which limit and both numbers, before any apology. |
| Offer choices: 2-4 options plus "Something else", free text open | More than one way forward fits ("Send a shorter clip", "Send photos", "Something else"). Not when one fix is the only one (a wrong type with one accepted alternative); then just say it. |
| Ask one clarifying question | The file is over a page or length limit and only part is needed: "Which pages matter most?" Not when the person already said. |
| Hand off to a person | No way under the limit works for a high-stakes, time-bound upload (a claim or filing due soon), or two tries fail. Not if the person asked to stay with the bot. |

**Don't over-correct.** Do not open every chat with a wall of limits or repeat them in every reply; one line at the attach button is enough until a file is near or over. Do not block files that are under the limit "to be safe", and do not show the full limit table to someone sending one small photo. The counter-metric in section 7 watches for limit text where nothing was over.

**Hand-off rule.** If the person cannot get the file under the limit after two tries and the upload is high stakes or due soon, offer a person or another channel (an upload link, email, or mail-in address), and pass the file name, which limit it broke, and the person's message so they do not start over ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | Open the chat on a free plan and on a paid plan | The attach control shows that plan's size, page, length, file-count limits and types (rule 1) |
| 2 | Attach a video twice the length limit on slow data | Rejected before the full upload; message names minutes and the limit (rules 2, 3) |
| 3 | Attach a PDF over the page limit with a typed question | Message names page count and limit; the typed question is still there (rules 3, 5) |
| 4 | Attach a file over two limits at once | Both limits named with both numbers; one next step each (rules 3, 4) |
| 5 | Hit the daily upload cap | Message says it is a daily cap and when it resets (rule 4) |
| 6 | Send an oversize file on WhatsApp | The person gets a message with the limit and a next step; no silent turn (rule 7) |
| 7 | Attach a small photo well under every limit | No limit text in the reply (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Over-limit uploads with a clear message** (primary) | 100% | Over-limit upload events where the shown message names the limit, the file's value, and a next step (template check plus sampled review) | Below 95% |
| Over-limit files caught before full upload | Track; set from baseline | Over-limit events with `stage = pre_upload` divided by all over-limit events | Falling |
| Bare "Upload failed" or raw error shown | 0 | Message text matched against generic and byte-count templates | Any |
| Message kept after an over-limit upload | 100% | `message_kept` on over-limit events | Below 100% |
| Limit text shown when nothing was over (counter-metric) | Track; set from baseline | Bot turns with limit wording and no over-limit event in the turn | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for chat; voice-call signals are PLANNED. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Over-limit upload event and the message does not name the limit | `upload_check.limit` joined to the shown message text | The UI showed the limit outside the message body |
| The same file is attached two or more times after a failure | `upload_check.file` repeated within the session | The first failure was a network drop, not a limit |
| Over-limit event with `stage = post_upload` and a long upload time | `upload_check.stage` and upload duration | A limit that can only be known after upload, such as a context limit |
| User asks "why did it fail" or "what's the limit" after an upload | User turn after an upload event | The user is asking ahead of uploading |
| Platform oversize event with no bot turn after it | Channel webhook error (for example WhatsApp 131052) with no outbound message | The person sent a new message first and got an answer there |

**Starter rule:** when a file is over a limit, name which limit, the file's own value and the limit, and give a next step; never "Upload failed" alone.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-warning-about-input-limits
runs: pre_send
reads: [upload_check.result, upload_check.limit, upload_check.file_value, upload_check.limit_value, upload_check.stage, upload_check.message_kept, draft_reply.text]
trigger: an upload check returns over_limit, or the channel reports an oversize file
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Send a shorter or smaller file", "Send only the part that matters", "Send photos instead", "Something else"]
on_miss: rewrite
metric: over-limit uploads with a clear message
counter_metric: limit text shown when nothing was over
status: proposed
```

## 8. Related patterns
- [Silent attachment failures](../../chat-interface/failures/silent-attachment-failures.md): the closest page. It covers the reply after a file was rejected or only partly read, with the bot answering as if it read it. This page is the step before: telling people the limits before they upload, and the quality of the over-limit message itself (which limit, both numbers, a fitting next step).
- [Context window overflow, silent truncation](../../../../../cross-cutting/operations/goals/memory-safety/failures/context-window-overflow-silent-truncation.md): its "Long upload silently cut" example is a limit that bites after upload with no notice. This page aims to catch limits before upload and name them when they cannot be.
- [Voice notes and audio attachments ignored](voice-notes-and-audio-attachments-ignored.md): the sibling page for audio, including transcription size and format limits.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): "Upload failed. Please try again." is one; this page gives the upload-specific wording.
- [Lost drafts and failed sends](../../chat-interface/failures/lost-drafts-and-failed-sends.md): what goes wrong when the typed message is lost along with the file.
- [Input size not validated](../../../../../cross-cutting/operations/goals/input-output-handling/failures/input-size-not-validated.md): the backend side (cost, memory, abuse); this page is what the person is told.

## 9. Common questions
### Why does my chatbot say "upload failed" with no reason?
Often the file broke a size, page, or length limit, and only a generic failure reached the chat. The vendor pages in [section 4](#4-why-it-matters) publish many such limits, but they are on help pages, not next to the attach button.

### What is the file size limit for ChatGPT, Claude, or Gemini?
It varies by product, file type, and plan, and it changes. On 2026-10-21 Anthropic's page listed 500 MB per file and 1000 PDF pages, and Google's listed 100 MB for most files and 10 minutes of audio on the free plan. We could not open OpenAI's page, so we give no number for it; check the live pages.

### Where should a chat show its upload limits?
At the attach button, in one line, for the person's own plan and channel. Repeat them in the reply only when a file is near or over a limit. See rule 1 in [section 5](#5-the-fix).

### What should a "file too large" message say?
Which limit, the file's own value, the limit, and what to do: "This video is 22 minutes; this chat takes up to 10. Send a shorter clip or photos." Keep the person's typed message.

### Is this the same as the bot silently reading only part of my file?
No. That is [silent attachment failures](../../chat-interface/failures/silent-attachment-failures.md). This page is about warning before upload and the message when a file is over a limit; the two fixes work together.

---
### Deep dive (optional)
- **Sources read through a fetch tool summary.** The Google, Anthropic, Meta (WhatsApp and Messenger), Document360, GOV.UK and NSW pages were opened with a fetch tool that returned summaries, not raw page text. Quoted phrases and numbers are those the tool reported; recheck them on the live pages before quoting them in your own docs.
- **Read only in search summaries (unverified, not used in the fix):** OpenAI ChatGPT upload limits (per-file size, token cap, image size, daily upload caps for free users), and third-party pages restating Gemini limits.
- **Modality notes.** On a voice call, limits are about call length and recording length, said aloud before the person starts. Those signals are PLANNED and not written here.
