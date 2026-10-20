# Chatbot Didn't Read My File but Answered Anyway: Silent Attachment Failures

<!-- SEO
title: Chatbot Didn't Read My File: Fix Silent Attachment Failures
description: Why a chatbot answers as if it read an uploaded PDF or file that was too large, unsupported, or only partly read, and how to say what was read and why.
search phrases:
- chatbot file upload failed but it still answered
- llm didn't read my pdf
- chatgpt pretends to read my pdf
- attachment not processed chatbot
- ai summarized a different document than the one I uploaded
- how to handle file upload limits in a chatbot
- llm only read part of my document
-->

**Frequency**: Common

## Issue: A user attaches a file that is too large, unsupported, or only partly read, and the bot answers as if it read all of it, instead of saying which file or part was not read and why.

> **One line:** The file never fully reached the model, the bot answered anyway; the fix is to record what was actually read for every attachment and say so in the reply whenever a file or part of it was skipped.

| | |
|---|---|
| **Channel** | Written for **chat** (web and app chat with file upload). Voice signals are PLANNED, not written. |
| **Stakes** | Low to high. A wrong summary of a blog post costs a retry; a summary of lab results or a lease built from a file the bot never read can mislead a decision. |
| **Who is affected** | Anyone who uploads long PDFs, scans, spreadsheets, images inside documents, or uncommon file types |
| **Frequency** | Common in user reports (see section 4). I found no study that counts how often chat products answer about a file they did not read. |
| **Pattern ID** | silent-attachment-failures |
| **Family** | [Chat interface](../README.md) |
| **Goal** | The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost. |
| **Primary metric** | Attachments dropped without a message. Target: 0 (a design target). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model cannot mention a file it never received; the upload pipeline has to record what was read and pass that on. (Our judgment, not tested.) |
| **Also searched as** | chatgpt can't read my pdf · uploaded file is too large · gemini failed to analyze your file · bot ignored my attachment · pdf images not read · file upload not working ai |

## 1. In plain words
Every chat product has upload limits: file size, page count, file types, and how much fits in the model's context. When a file breaks one of them, or only its text is extracted, part or all of it never reaches the model. The failure is not the limit; it is that the bot answers in a confident voice, so the user believes the answer came from the whole file.

## 2. What it looks like

**Without the fix**
```
User: (attaches Lease_2026_Maple_St.pdf, a 140-page scan, and floorplan.heic)
User: Summarize the pet and early-termination rules, and does the floorplan show a second bathroom?
Bot:  Pets are allowed with a $300 deposit, and early termination requires 60 days' notice.
      The floorplan shows two bathrooms.
User: (signs, then learns the early-termination clause is in an addendum on page 131 the bot never read)
```

**With the fix**
```
User: (attaches the same two files and asks the same question)
Bot:  I could read only part of what you sent:
      - Lease_2026_Maple_St.pdf: 22 of its 140 scanned pages had no readable text, including
        pages 128-140, which may hold addenda. I read the other 118.
      - floorplan.heic: not read. This chat doesn't accept HEIC images; JPEG or PNG works.
      From the pages I read: pets need a $300 deposit (page 14). I found no early-termination clause.
      Re-upload the floorplan as PNG, or tell me what else to do.
      [Re-upload as PNG] [Paste pages 128-140 as text] [Something else]
```
The fixed reply lists each file's status first, gives the reason, answers only from what was read, and says where the missing part is.

## 3. Why it happens
- **The upload layer and the model don't share state.** The file can be rejected, truncated, or reduced to extracted text before the model call, and nothing tells the model, so it answers from whatever arrived, or from the user's question alone.
- **Partial reads are designed in and not shown.** Vendors document text-only extraction and context limits (section 4), but the reply carries no record of which pages, images, or sheets were skipped.
- **Answering is the default.** A model asked "summarize this" with little or no file content still writes a summary; the forum reports in section 4 describe exactly that.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Anthropic lists chat upload limits of "500MB per file", "Up to 20 files per chat", and "PDFs are limited to 1000 pages"; for PDFs of 101 to 1000 pages, Claude "processes text only and doesn't analyze visual elements", and for other documents it "extracts text only". | [Anthropic, *Upload files to Claude*](https://support.claude.com/en/articles/8241126-upload-files-to-claude), last updated July 23, 2026. Opened 2026-10-20. | Vendor documentation. Shows limits and documented partial reads exist; it does not say how the chat tells the user. |
| Google says up to 10 files per prompt, other file types "can be up to 100 MB", that large uploads may give "a response that misses connections or details", and that exceeding the context window "could lead to responses that don't take into account all the content provided". | [Google, *Upload & analyze files in Gemini Apps*](https://support.google.com/gemini/answer/14903178?hl=en). Opened 2026-10-20; no update date shown. | Vendor documentation. A vendor stating that answers may not cover the whole file. |
| OpenAI has a File Uploads FAQ with per-file size and token limits. | [OpenAI Help Center, *File uploads FAQ*](https://help.openai.com/en/articles/8555545-file-uploads-faq). **Not opened** (HTTP 403); read only through a search summary. | Unverified. I quote none of its numbers and the fix does not rely on it. |
| A user reported in March 2025 that after uploading a PDF of lab results, ChatGPT described it as a police report and judicial case, and on another try said the PDF was empty. | [OpenAI Developer Community thread](https://community.openai.com/t/chatgpt-giving-me-information-that-does-not-exist-in-my-pdf-this-looks-like-a-leak/1153645). Opened 2026-10-20. | Anecdotal, one user; no OpenAI reply on the page. The cause is not known. |
| A user reported in May 2024 that ChatGPT "pretended not to see the file" or said it could not read it, for prompts that had worked before. | [OpenAI Developer Community thread](https://community.openai.com/t/chatgpt-pretends-not-to-see-uploaded-files/785159). Opened 2026-10-20. | Anecdotal, one user; no staff reply. The opposite symptom: the file was there and the bot said it was not. |
| A user reported in November 2024 that ChatGPT said it "cannot read the attached pdf" across models. | [OpenAI Developer Community thread](https://community.openai.com/t/chatgpt-cannot-read-attached-pdf/1000099). Opened 2026-10-20. | Anecdotal. Here the bot did say so, which is the behavior this page wants, but with no reason or next step. |

I searched for a study of models answering about attachments that failed to load and found none.

**Public incident.** None found.

## 5. The fix
**The principle:** Every reply about attachments states, before the answer, any file or part that was not read, why, and what the user can do.

**Do this**
1. **Record a read status for every attachment.** For each file, log one of: `read_full`, `read_partial`, `not_read`, plus the reason (`too_large`, `too_many_pages`, `unsupported_type`, `text_only`, `context_limit`, `extract_empty`, `upload_failed`).
2. **Pass the status to the model.** Put a short manifest of each file's status in the model input, so the model knows what it did not see.
3. **Say it first.** If any file is not `read_full`, the first lines of the reply name the file, what was skipped (pages, images, sheets), and the reason in plain words.
4. **Answer only from what was read.** Never state content from a skipped file or page. If the question needs the skipped part, say the answer is not in what was read.
5. **Give one fix per reason.** Too large: split or compress. Unsupported: name a supported type. Scan with no text: paste text or upload a clearer copy. Context limit: ask which section to read first.
6. **Reject early when you can.** If the upload layer knows a file breaks a limit, show that in the composer before send, and keep the user's message.
7. **Don't claim a file is missing when it arrived.** If the status is `read_full`, do not say "I can't see the file".

**Reference design: attachment manifest and model rule**
```json
{"attachments": [
  {"name": "Lease_2026_Maple_St.pdf", "status": "read_partial", "reason": "extract_empty",
   "read": "text, 118 of 140 pages", "skipped": "22 pages with no extractable text, incl. 128-140"},
  {"name": "floorplan.heic", "status": "not_read", "reason": "unsupported_type", "accepted": ["jpeg", "png"]}
]}
```
```
Before answering, check the attachment manifest. If any file is not read_full, start the reply by naming
the file, what was skipped, and why, in plain words, then give one way to fix it.
Answer only from content that was read. If the answer may be in a skipped part, say so; do not guess.
If every file is read_full, do not say you can't see a file.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A file or part was not read: say which part, why, and that the answer covers only what was read. |
| Offer choices: 2-4 options plus "Something else", free text open | After a partial or failed read with more than one fix: "Re-upload as PNG", "Paste the missing pages", "Read section 1 first", "Something else". Do not offer them when one fix fits (a type with one accepted alternative), or in place of the status lines. |
| Ask one clarifying question | The file is over the context limit: ask which section matters most before reading. Not when the user already named the section. |
| Lead with the answer | Every file is `read_full`: answer directly, with no status preamble. |

**Don't over-correct.** Do not open every reply with a file report when everything was read, and do not refuse to answer from the parts that were read. Do not list technical codes; say "it's a scan with no text on these pages", not `extract_empty`.

**Hand-off rule.** If the user needs the unread part for a high-stakes decision (a lease, medical results, a tax form) and two re-upload attempts fail, offer a person or another channel, and pass the file names and their read status.

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Upload an unsupported type (HEIC) with a question about it | First lines name the file, "not read", the reason, and a supported type | 1, 3, 5 |
| 2 | Upload a scanned PDF with no text layer on some pages | Reply names the skipped pages and states no content from them | 3, 4 |
| 3 | Ask about content that sits only in a skipped part | Bot says it is not in what was read; no guessed answer | 4 |
| 4 | Upload a file over the size limit | Composer shows the limit before send and the message text stays | 6 |
| 5 | Upload a small, fully read TXT file | Bot answers directly, with no "I can't see the file" and no status preamble | 7, Don't over-correct |
| 6 | Model input missing the manifest | Release check fails | 2 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Attachments dropped without a message** (primary) | 0 (design target) | Attachments with status not `read_full` where the reply has no status line for that file (log join plus string check, sampled review) | Any |
| Read-status coverage | 100% | Attachments with a logged status and reason | Below 100% |
| Answers citing skipped content | 0 | Sampled review of replies to `read_partial` files | Any |
| False "can't see the file" | 0 | Replies saying a file is missing when status is `read_full` | Any |
| Re-upload of the same file name within 3 turns | Track; set from baseline | Upload events by file name per session | Rising two weeks in a row |
| Status preamble on fully read files (counter-metric) | Track; set from baseline | Replies with status lines when all files are `read_full` | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Attachment status not `read_full` and no file name in the reply's first lines | `attachment.status` joined to the next bot turn | The status was shown in the UI instead of the reply |
| Attachment event with no status logged | `attachment` event missing `status` or `reason` | An old client that does not report status yet |
| User re-uploads a file with the same name within 3 turns | `attachment.name` repeated in the session | User sent a corrected version on purpose |
| User says "that's not in the file" or "did you read it" after a file reply | User turn after a bot turn that followed an attachment | User is disputing a correct reading |
| Reply says "I can't see the file" while status is `read_full` | Bot turn text plus `attachment.status` | Upload finished after the reply started |

**Starter rule:** every reply about attachments states, before the answer, any file or part that was not read, why, and what the user can do.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: silent-attachment-failures
runs: pre_send
reads: [attachment.name, attachment.status, attachment.reason, attachment.skipped, draft_reply.text]
trigger: a reply is about to be sent in a turn with an attachment (status not read_full: report first; all read_full: answer directly)
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, lead_with_answer]
choices: ["Re-upload in a supported format", "Paste the missing part as text", "Read one section first", "Something else"]
on_miss: rewrite
metric: attachments dropped without a message
counter_metric: status preamble on fully read files
status: proposed
```

## 8. Related patterns
- [No warning of context loss](../../effort-and-memory/failures/no-warning-of-context-loss.md): the closest page. It covers earlier conversation dropped as a chat grows; this one covers a file that was rejected, truncated, or only partly read at upload, with the bot answering as if it read it.
- [Silent failure and timeout](../../response-time/failures/silent-failure-and-timeout.md): a reply that never arrives or cuts off; here the reply arrives and looks complete.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): an error is shown but says nothing useful; here often no error is shown at all.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the general case; this page is one source of it.
- [Input size not validated](../../../../../cross-cutting/operations/goals/input-output-handling/failures/input-size-not-validated.md): the backend side (memory, cost); this page is what the user is told.
- [Context window limits on long documents](../../../../document-processing/goals/agentic-orchestration/failures/context-window-limits.md): chunking in document pipelines, not chat replies.
- [Lost drafts and failed sends](lost-drafts-and-failed-sends.md) and [auto-scroll fights the reader](auto-scroll-fights-the-reader.md): sibling chat-interface patterns.

## 9. Common questions
### Why does ChatGPT say it read my PDF when it didn't?
I found no OpenAI explanation in the sources I opened. Vendor pages show that files can be over a limit or read as text only, and if the model is not told what was skipped, it answers from what it has. See [section 3](#3-why-it-happens).

### How do I know if the chatbot read my whole file?
Ask it which pages or sections it read. A product built to this pattern says so without being asked, before the answer.

### What file types and sizes can chatbots read?
It varies by product and changes often. Anthropic and Google publish their limits (section 4); check the live help page for your product.

### Should the bot refuse to answer if part of the file was not read?
No. It should answer from what it read and say plainly what it did not read, so the user can decide whether that is enough.

---
## Technical section

### T1. Solution architecture
```
upload -> validate (type, size, pages) -> reject in composer, keep message   (rule 6)
       -> extract -> per-file status {read_full | read_partial | not_read, reason, skipped}   (rule 1)
       -> manifest into model input (rule 2) -> draft reply
       -> pre-send check: status not read_full and file not named? -> rewrite (rules 3-4)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Every attachment gets a status and reason | Extraction service | Read-status coverage metric |
| Manifest present in model input | Prompt builder | Test 6 |
| Partial or failed file named before the answer | Pre-send check | Tests 1-2, primary metric |

### T3. Evals
- **Dataset:** 50 uploads to start: unsupported types, oversize files, scans with no text, PDFs past the visual-analysis page limit, files past the context limit, and fully read controls.
- **Judge rubric:** are unread files and parts named first with a reason; is any claim drawn from skipped content; is a fully read file answered directly?
- **Release gate:** block a deploy if any unread file goes unmentioned in the eval set (starting point).

### T5. Trade-offs
- Status lines add length; show them only when something was skipped.
- Page-level status needs per-page extraction results, which some parsers do not expose.
