# Test File: No Warning About Input Limits

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs states its upload limits before a file is sent, and, when a file is over a limit, says which limit, the file's own value, and what to do next.

> **Read this first.** These are test conversations only. All limits below belong to an invented insurer's chat and are invented for the test; they are not the limits of any real product. Real limits vary by file type, plan, and channel and change over time, so check your own product's current limits. Time-bound claims and filings are high stakes: a reviewer should confirm the hand-off path before you rely on it.

**Pattern:** [Chatbot File Too Large, No Warning: No Warning About Input Limits](../goals/multimodal-input/failures/no-warning-about-input-limits.md)
**Pattern ID:** no-warning-about-input-limits
**Goal:** Whatever the person attaches, the assistant says what it received and works from what is really there. (Family goal, from the pattern page.)
**Primary metric:** Over-limit uploads with a clear message. Starting target on the pattern page: 100% (a starting point to tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, files, and people are invented (fake). Text chat only; voice-call signals are PLANNED, not written. Most conversations need an upload control you can drive in a test harness, so the setup says what the file is. Every conversation below carries the Pattern ID above; the R-lines say which rule it checks.

**Invented limits used in every setup unless stated.** Saguaro Mutual (fake), a Phoenix home insurer with a claims chat, accepts video up to 10 minutes and 100 MB, PDFs up to 100 pages, up to 5 files per message, and types MP4, MOV, PDF, JPG, and PNG, plus 20 uploads per day. These numbers are the page's example limits, extended with the type list and daily cap for testing.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Show the limits at the attach control | One line next to the attach control with size, pages, minutes, file count, and types for this plan and channel | No limits shown before the person picks a file |
| R2 | 2. Check before the long upload | An over-limit file is stopped before the full upload (judged from the harness timing or log) | The person waits for the full upload, then gets the failure |
| R3 | 3. Name the limit and both numbers | The message gives the limit, the file's own value, and the limit value in plain units | "Upload failed" alone, or a raw byte count |
| R4 | 4. A next step that fits the limit | Too long: shorter clip or split. Too many pages: send the pages that matter or split. Too big: compress or photos. Wrong type: name one accepted type. Daily cap: when it resets | A generic "try again," or a step that does not fit the limit |
| R5 | 5. Keep everything else | The typed message and under-limit files stay | The person must re-type or re-attach |
| R6 | 6. Limits only known after upload get their own line | The reply says what part was read and what was not | An answer as if the whole file was read |
| R7 | 7. On messaging channels, answer the platform's oversize event | The person gets a message with the limit and a next step | A silent turn |
| R8 | 8. Log every over-limit upload with its limit | Not judged here (needs the event log) | Not judged here |
| R9 | Hand-off rule | After two failed tries on a high-stakes, time-bound upload, a person or another channel is offered, with the file name, the limit hit, and the message passed on | Another retry loop, or a cold transfer |
| R10 | Don't over-correct | No limit wall at the start, no limit text where nothing was over, under-limit files not blocked | Limit text on a small photo, or a blocked under-limit file |

## Conversations
1. **Limits shown at the attach control (R1).**
   Setup: Open the Saguaro Mutual claims chat on a desktop browser. Do not attach anything.
   User: (none; inspect the screen next to the attach button)
   Expect: One line near the attach control with video minutes and MB, PDF pages, file count, and types. Limits only on a help page, or no limits shown, fails.

2. **Free plan versus paid plan (R1).**
   Setup: A fake product, Cobalt Notes (fake), whose free plan allows smaller files than its paid plan (both invented). Open the chat once on each plan.
   User: (none; inspect the attach control)
   Expect: Each plan's control shows that plan's own limits. The same line for both plans fails.

3. **Long video, caught early (R2, R3, R4).**
   Setup: Saguaro Mutual. The user attaches kitchen_leak.mp4, 22 minutes and 410 MB, on mobile data.
   User: (attaches the file) "this is the leak, claim is due friday"
   Expect: The file is rejected before the full upload starts. The first line names both numbers ("This video is 22 minutes and 410 MB; this chat takes up to 10 minutes and 100 MB") and offers a clip, split, or photos. "Upload failed. Please try again." fails.

4. **Message kept after rejection (R5).**
   Setup: Same as 3.
   User: (the typed message is still in the thread after the file is rejected)
   Expect: The typed message is saved and answered or acknowledged. The user is not asked to re-type it. A lost message fails.

5. **PDF over the page limit, question typed (R3, R4, R5).**
   Setup: Saguaro Mutual. The user attaches a 240-page scanned policy, policy_scan.pdf.
   User: "what does page 12 say about water damage?"
   Expect: The reply names the page count and the limit ("240 pages; the limit is 100"), offers to take the pages that matter or a split file, and keeps the typed question. A bare failure fails.

6. **Over two limits at once (R3, R4).**
   Setup: Saguaro Mutual. The user attaches roof_walkthrough.mov, 14 minutes and 300 MB.
   User: (attaches the file)
   Expect: Both limits are named with both numbers (length and size) and one next step each. Naming only one limit fails.

7. **Wrong file type (R4).**
   Setup: Saguaro Mutual. The user attaches estimate.xlsx.
   User: "here is the contractor estimate"
   Expect: The reply names one accepted type that fits (for example, PDF) and how to get there. Listing every limit in the product instead of the one that applies fails.

8. **Too many files (R3, R4).**
   Setup: Saguaro Mutual. The user attaches 8 photos in one message.
   User: "damage photos, kitchen and hall"
   Expect: The reply says the chat takes up to 5 files per message and that 8 were attached, and tells the person what happened to them (the first 5 received, or none; the chat must say which). Silently keeping only some files fails.

9. **Daily cap (R4).**
   Setup: Saguaro Mutual. The user has made 20 uploads today. The next upload hits the daily cap.
   User: (attaches one more photo) "one last one"
   Expect: The reply says it is a daily cap and when it resets. "Upload failed" fails.

10. **A limit that bites after upload (R6).**
    Setup: Saguaro Mutual (invented behavior for the test): a 90-page PDF is under the page limit, but the chat reads only the text, not the images, of the file.
    User: "can you check the photos in this repair report?"
    Expect: The reply says it read the text of the file and not its images, and offers a next step (send the images as photos). Answering as if the images were read fails.

11. **WhatsApp oversize event (R7).**
    Setup: Saguaro Mutual's claims line on WhatsApp (fake). The user sends a video over the channel's limit and the platform reports an oversize file to the bot.
    User: (sends a 40 MB video)
    Expect: The person receives a message that names the limit and a next step. No outbound message after the platform's oversize event fails.

12. **High stakes, two failed tries (R9).**
    Setup: Saguaro Mutual. A claim is due Friday. The user has tried two times to upload a 22-minute video.
    User: "this is the third time, I'm out of time, what do I do"
    Expect: The bot offers a person or another channel (an upload link, email, or mail-in address), and passes along the file name, the limit hit, and the user's message so nobody starts over. Another retry loop fails.

13. **Do nothing special: small photo, well under every limit (R10).**
    Setup: Saguaro Mutual. The user attaches ceiling_stain.jpg, 2 MB.
    User: "here's the stain on the ceiling"
    Expect: A normal reply about the photo with no limit text. Limit text in the reply fails.

14. **Do nothing special: file under the limit but not tiny (R10).**
    Setup: Saguaro Mutual. The user attaches a 38-page PDF, adjuster_letter.pdf (limit is 100 pages).
    User: "can you summarize this letter?"
    Expect: The reply summarizes the letter. It does not block the file, ask the user to shorten it, or recite the limits. A blocked file fails.

15. **Do nothing special: user asks about the limits (R10).**
    Setup: Saguaro Mutual. The user has not attached anything.
    User: "how big can my videos be?"
    Expect: A one-line answer with the limits that apply to videos (10 minutes, 100 MB), not the full table of every limit. A full wall of every limit fails.

## Cannot be judged from a transcript alone
- **Primary metric.** The page measures the share of over-limit uploads with a clear message over production events, with template checks and sampled review. These are single cases.
- **R2, early check.** Whether the file was stopped before the full upload needs the harness timing or the event `stage` field.
- **R8, logging.** Needs the event log (the limit type, the file's value, the limit, and whether a message was shown).
- **Real limits.** The limits here are invented. For a real product, test against that product's own current limits.
- **Channel behavior.** The WhatsApp conversation (11) needs a channel where the platform's oversize event can be triggered; the pattern page describes one but I did not verify the event on that channel myself.
- **Voice.** PLANNED, not covered here.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives seven scenarios. Conversations 1, 3, 5, 6, 9, 11, and 13 follow them. The rest are my additions from the rules: 2 (plans), 4 (rule 5), 7 (wrong type), 8 (too many files), 10 (rule 6), 12 (hand-off rule), 14 and 15 (Don't over-correct).
- Saguaro Mutual's 10 minutes, 100 MB, and 100 pages are the page's example limits. The 5-file count comes from the page's example footer. The type list and the 20-upload daily cap are mine, for testing. Cobalt Notes is invented.
- In conversation 8, what happens to the extra files (first five kept, or none) is a product choice; the test only checks that the reply says which.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
