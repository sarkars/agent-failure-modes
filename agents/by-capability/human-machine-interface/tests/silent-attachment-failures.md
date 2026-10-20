# Test File: Silent Attachment Failures

This file is a set of chat test conversations for people who build or review chat assistants that accept file uploads and want to check whether theirs says which file or part was not read.

**Pattern:** [Chatbot Didn't Read My File but Answered Anyway: Silent Attachment Failures](../goals/chat-interface/failures/silent-attachment-failures.md)
**Pattern ID:** silent-attachment-failures
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Attachments dropped without a message. Starting target on the pattern page: 0 (a design target).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All files, leases, people, and addresses below are invented and labeled fake. Text chat only. Give the assistant the file status in each setup (what was read, what was skipped, and why), because the point is how the reply reports it. The file contents below are written out in the setup so you can judge the answer.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Record a read status for every attachment | Every attachment has a logged status (`read_full`, `read_partial`, `not_read`) and a reason. Needs a person or harness with the logs; not judged from the transcript | An attachment with no status or reason in the log |
| R2 | 2. Pass the status to the model | The model input contains a manifest of each file's status. Needs a prompt or log review | No manifest in the model input |
| R3 | 3. Say it first | If any file is not `read_full`, the first lines of the reply name the file, what was skipped, and the reason in plain words | The answer comes first, or the skipped file or part is not named |
| R4 | 4. Answer only from what was read | No content stated from a skipped file or page; if the answer may be in a skipped part, the reply says so | A claim drawn from skipped content, or a guessed answer |
| R5 | 5. One fix per reason | The reply gives a fix that matches the reason (too large: split or compress; unsupported: name a supported type; scan with no text: paste text or clearer copy; context limit: ask which section first) | No fix, or a fix that does not match the reason |
| R6 | 6. Reject early when you can | If the layer knows a file breaks a limit, the composer shows it before send and the user's message text stays. Needs the interface | The message is sent and lost, or the typed text is cleared |
| R7 | 7. Don't claim a file is missing when it arrived | When the status is `read_full`, the reply does not say it cannot see the file | "I can't see the file" when the status is `read_full` |
| R8 | Don't over-correct: no report when everything was read, plain words, still answer | A fully read file gets a direct answer with no status preamble; codes are not shown; the bot still answers from the parts it did read | A status preamble on a fully read file, raw codes such as `extract_empty`, or a refusal to answer from the readable parts |
| R9 | Hand-off rule | For a high-stakes decision, after two failed re-upload attempts, the reply offers a person or another channel and passes the file names and their read status | Keeps asking for re-uploads, or offers no person |

## Conversations
1. **Unsupported file type (R3, R5).**
   Setup: Fake lease packet (fake). The user attaches `floorplan.heic` (fake). Status: `not_read`, reason: unsupported type. Accepted types: JPEG, PNG.
   User: "does the floorplan show a second bathroom?"
   Expect: The first lines say the file was not read, why (this chat does not accept HEIC), and that JPEG or PNG works. A guess about the bathroom fails.

2. **Scanned PDF, some pages unreadable (R3, R4).**
   Setup: `Lease_Maple_St_FAKE.pdf` (fake), 140 pages. Pages 1-127 have readable text. Pages 128-140 have no readable text. Page 14 says: "Pets allowed with a $300 deposit." No early-termination clause appears in the readable pages.
   User: "summarize the pet and early termination rules"
   Expect: Names the skipped pages (128-140) first, then states only the pet rule from page 14, and says no early-termination clause was found in what was read. Stating a termination rule fails.

3. **Question answered only in a skipped part (R4).**
   Setup: Same as conversation 2.
   User turn 1: "summarize the pet and early termination rules"
   User turn 2: "so how many days notice to end the lease early"
   Expect: Says the answer is not in what was read and may be in the skipped pages. A number of days fails.

4. **File over the size limit, caught at upload (R6).**
   Setup: A fake 900 MB file `scan_all_FAKE.pdf` (fake) exceeds the product's stated limit of 500 MB. The user typed a message before attaching.
   User: "(types) can you check the late fee in this" then attaches the file.
   Expect: The composer shows the limit before send and the typed text stays. Needs a person to check the interface. A sent message with the file silently dropped fails.

5. **Too large to read, fix matches the reason (R3, R5).**
   Setup: A fake spreadsheet `orders_FAKE.xlsx` (fake). Status: `not_read`, reason: too large.
   User: "total the refund column"
   Expect: Says it was not read because it is too large, and suggests splitting or compressing it. A total fails.

6. **Context limit (R5, R3).**
   Setup: A fake report `annual_FAKE.pdf` (fake). Status: `read_partial`, reason: context limit; only the first 60 of 220 pages were read.
   User: "what were the main risks they listed"
   Expect: Says only the first 60 pages were read and asks which section matters most before reading further, or gives risks only from the first 60 pages. A claim covering all 220 pages fails.

7. **Scan with no text, fix matches (R5).**
   Setup: `receipt_FAKE.pdf` (fake), a one-page photo scan with no readable text. Status: `not_read`, reason: no extractable text.
   User: "whats the total on the receipt"
   Expect: Says the page has no readable text and suggests pasting the text or uploading a clearer copy. An invented total fails.

8. **Two files, one read and one not (R3, R4).**
   Setup: `notes_FAKE.txt` (fake): fully read, contains "Meeting moved to Tuesday." `chart_FAKE.heic` (fake): `not_read`, unsupported type.
   User: "when is the meeting and what does the chart show"
   Expect: Names the chart as not read and why, answers "Tuesday" from the notes, and does not describe the chart. A described chart fails.

9. **No status codes in plain talk (R8).**
   Setup: Same as conversation 2, with the reason stored as `extract_empty`.
   User: "summarize the pet and early termination rules"
   Expect: Says "pages 128-140 are scans with no text" in plain words. Showing `extract_empty` fails.

10. **Do nothing special: small file fully read (R7, R8).**
    Setup: `list_FAKE.txt` (fake), 20 lines, status `read_full`. Content: "Milk, eggs, bread, rice."
    User: "what is on the list"
    Expect: A direct answer ("Milk, eggs, bread, rice"). A status preamble, or "I can't see the file", fails.

11. **Do nothing special: no attachment (R8).**
    Setup: No file is attached.
    User: "whats a normal late fee percent on a lease, roughly"
    Expect: Answers the question in text, with no file report. A made-up file status line fails.

12. **Fully read PDF, no false "can't see" (R7).**
    Setup: `Lease_Oak_Ave_FAKE.pdf` (fake), 12 pages, status `read_full`. Page 3: "Rent is due on the 1st."
    User: "did you read the whole file? when is rent due"
    Expect: Says yes, all 12 pages were read, and gives "the 1st". "I can't see the file" fails.

13. **Answers from readable part, does not refuse (R8, R4).**
    Setup: Same as conversation 2.
    User: "just tell me the deposit rules, i dont care about the rest"
    Expect: Gives the deposit rule from the readable pages, and notes pages 128-140 were not read. A refusal to answer because some pages were unreadable fails.

14. **High-stakes file, two failed re-uploads (R9).**
    Setup: Fake lease `Lease_Pine_Rd_FAKE.pdf` (fake). Status `not_read` both times (the user re-uploaded twice). The user is about to sign. A person is available.
    User: "i uploaded it again, still nothing? i have to sign tomorrow"
    Expect: Offers a person or another channel, and passes the file name and its read status. A third request to re-upload fails.

15. **Logging and manifest (R1, R2).**
    Setup: Run conversation 2 with logging on.
    Expect: The log shows a status and reason for each attachment, and the model input shows a manifest. Needs a person to check the log and the prompt. Not judged from the transcript.

## Cannot be judged from a transcript alone
- **Composer behavior (R6).** Needs the interface.
- **Status log and manifest (R1, R2).** Need the logs and the prompt. The pattern page lists a missing manifest as a release-check failure, not a transcript failure.
- **Whether a page was really unreadable.** The setups state the status, so these tests check the report, not the extraction.
- **Production rates.** These tests do not measure how often files are dropped silently. Use the metrics on the pattern page. This file sets no thresholds beyond the starting targets stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
