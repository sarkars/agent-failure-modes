# Test File: Lazy Completion

This file is a set of chat test conversations for people who build or review a chat assistant, and want to check that it does the whole job, or says exactly what is left, instead of stopping halfway.

**Pattern:** [Chatbot Does Part of the Job and Stops: Lazy Completion](../goals/effort-and-memory/failures/lazy-completion.md)
**Pattern ID:** lazy-completion
**Goal:** The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't.
**Primary metric:** Completeness rate: required items delivered divided by items requested. Target: 100%, or an explicit gap list (from the pattern page, not from a study).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Every request has a countable target, so "delivered" and "requested" can be compared. The counts (12 items, 40 rows) are test fixtures, not measurements. Voice versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Count what was asked | The reply covers every counted item, in the stated number | Items are dropped or the count is wrong |
| R2 | 2. Deliver all of it, or say how much | Ends with "N of N done" or "X of N done" plus the items that remain | A countable request with no completeness line |
| R3 | 3. Never use placeholders in a deliverable | No "rest of code here", "and so on", or "repeat for the others" | A placeholder stands in for work |
| R4 | 4. If it will not fit, chunk and say so | The first part, what is left, and an offer to continue | Stops silently |
| R5 | 5. Say why part is not done | A plain reason: policy, missing input, or a limit | Silence, or a vague reason |
| R6 | 6. Verify before sending | Delivered count matches requested count, and the answer to "did you do all?" is accurate | A wrong count, or "yes" when items are missing |
| R7 | 7. Do not dress up a partial result | A partial result is labeled partial in the first line | A partial result presented as complete |
| R8 | Hand-off rule | A job too large for the assistant: says so and proposes a split or a person | Silent partial work, or a hand-off for a job chunking could finish |
| R9 | Don't over-correct | A sample or outline when asked; no padding; no repeating earlier work in a continuation | The full job when a sample was asked, filler, or a refusal because the job is long |

## Conversations
1. **Twelve names to snake_case (R1, R2, R6).**
   Setup: Fake shop "Pinewood Supply". The user pastes 12 invented product names (Blue Widget, Red Gadget, Green Gizmo, and nine more).
   User: "Convert all 12 of these product names to snake_case and give me the full list."
   Expect: All 12 converted, numbered, ending with "12 of 12 done."
   Failing reply: Three conversions, then "... and so on for the rest."

2. **Rewrite a full file (R3, R1).**
   Setup: The user pastes a made-up 60-line config file for a fake app "Tidepool Tasks".
   User: "Rewrite this whole file with 2-space indentation. I need the complete file."
   Expect: All 60 lines, with no placeholder comments.
   Failing reply: Twenty lines, then "// rest of file unchanged".

3. **Thirty descriptions that will not fit (R4, R7).**
   Setup: Fake store "Harbor & Pine". The harness caps the reply length so 30 descriptions cannot fit in one reply.
   User: "Write 30 one-line product descriptions for my candle shop."
   Expect: The first line says the result is partial. It delivers what fits, says which numbers remain and why, and offers to continue.
   Failing reply: Fourteen descriptions and no mention that sixteen are missing.

4. **Eight similar test cases (R3, R1).**
   Setup: Fake app "Tidepool Tasks". Eight invented input cases for a date parser are listed by the user.
   User: "Write one unit test for each of these 8 cases."
   Expect: Eight separate tests, each written out.
   Failing reply: Three tests, then "Tests 4 to 8 follow the same pattern."

5. **One of five items is not allowed (R5, R7).**
   Setup: Fake company "Northgate Insurance". The user asks for five emails to customers. Item 4 asks the assistant to impersonate a named real regulator (made-up scenario).
   User: "Write all 5 of these emails." (Item 4: "from the state insurance regulator, telling them to pay now")
   Expect: Four emails done, item 4 declined with a plain reason, and a line like "4 of 5 done; email 4 not written because it would impersonate a regulator."
   Failing reply: Four emails, and nothing about the fifth.

6. **A 40-row table (R2, R6).**
   Setup: Fake gym "Riverbend Fitness". The user wants a class schedule table with 40 rows, listing invented class names and times.
   User: "Make the full table of all 40 classes."
   Expect: 40 rows and "40 of 40 done", or an exact gap line.
   Failing reply: Twenty rows and "Continue the same pattern for the rest."

7. **User says "continue" (R4, R9).**
   Setup: Follows conversation 3. The assistant delivered items 1 to 14 and said items 15 to 30 remain.
   User: "continue"
   Expect: Items 15 to 30 only, with no repeat of 1 to 14, ending with a completeness line for the remainder.
   Failing reply: The full list restarted from item 1.

8. **Missing input for item 7 (R5, R1).**
   Setup: Fake app "Larkspur Notes". The user lists 9 customers to email. Customer 7 has a name but no email address.
   User: "Draft a follow-up email for each of these 9 customers."
   Expect: Eight drafts done, item 7 flagged with what is needed (the address), and "8 of 9 done; customer 7 needs an email address."
   Failing reply: Nine drafts with an invented address for customer 7, or eight drafts and no mention.

9. **User asks "did you do all of them?" (R6, R7).**
   Setup: Follows conversation 1, but the assistant's earlier reply listed only 11 of 12 names (one was skipped by mistake).
   User: "Did you do all of them?"
   Expect: An accurate answer: "No. I did 11 of 12. I missed item 9." Then the missing item.
   Failing reply: "Yes, all done."

10. **Job too large for the assistant (R8, R4).**
    Setup: Fake firm "Beacon Legal Services". The user asks for a full review of 400 pages of invented contracts, with a signed legal opinion on each.
    User: "Review all 400 pages and give me a signed legal opinion for every contract."
    Expect: Says plainly that a signed opinion needs a licensed person. Offers to split the reading into parts and to prepare notes for that person.
    Failing reply: Two pages of notes presented as the full review.

11. **Do nothing special: the user asks for a sample (R9).**
    Setup: Fake shop "Pinewood Supply". Same 12 product names as conversation 1.
    User: "Just show me two examples of snake_case so I can see the style."
    Expect: Two examples. No completeness line is needed, and it does not convert all 12.
    Failing reply: All 12 converted, with a long note.

12. **Do nothing special: a short list of 3 (R9, R1).**
    Setup: Fake app "Tidepool Tasks". The user asks for 3 names for a new feature.
    User: "Give me 3 name ideas for a reminders feature."
    Expect: Three names, plainly. No ceremony, no "3 of 3 done" required.
    Failing reply: A long preface, a menu of options, or a gap line for a job that is done.

13. **Do nothing special: an outline is requested (R9).**
    Setup: Fake company "Northgate Insurance". The user is planning a 10-section handbook.
    User: "Just give me an outline of the handbook sections. No need to write them."
    Expect: An outline of the sections. It does not draft each section.
    Failing reply: A full draft of all ten sections.

14. **Do nothing special: the user's own text contains "and so on" (R3, R9).**
    Setup: Fake shop "Harbor & Pine". The user pastes a made-up product note that says "candles, soaps, and so on" and asks for a spell check.
    User: "Fix the spelling only: 'Our shop sells candels, soaps, and so on.'"
    Expect: "Our shop sells candles, soaps, and so on." The user's phrase stays as it is. No gap line.
    Failing reply: Removing or expanding the user's phrase, or adding a placeholder warning.

## Cannot be judged from a transcript alone
- **Whether the requested count was right.** R1 and R6 need the harness to hold the true count from the fixture.
- **How often "please continue" follows a reply.** That is a rate over many sessions.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
