# Test File: No Way to Report Bad Behavior

This file is a set of chat test conversations for people who build or review assistants and want to check whether users can report a bad reply in one action, and whether every report reaches a named person.

**Pattern:** [Report Bad AI Response: Chatbot Feedback Button Does Nothing, and No Way to Report Bad Behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md)
**Pattern ID:** no-way-to-report-bad-behaviour
**Goal:** Teams can tell whether conversations really work, and users can tell the team when they don't.
**Primary metric:** Reports per 1,000 conversations; time to triage. Starting target on the pattern page: a working report control on 100% of replies, and median time to triage under 2 business days (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, accounts, and people are invented and labeled fake. Text chat only. Each setup says what the bot has: a report control under each reply (thumbs-down or "Report a problem"), a report record store with the fields in the pattern's reference design (ref code, reply_id, conversation_id, reason, free_text, severity, queue, owner, triaged_at, outcome), and a way to hand off to a person. The record and queue tests (2, 4, 8, 12) need a harness that can read the report store and advance a clock; a transcript alone is not enough.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Put a report control on every bot reply | Every bot reply shows a thumbs-down or "Report a problem" within one click or tap | Any reply with no control, or a control only at the end of the chat |
| R2 | 2. Accept a typed report too | "report this" or "this is wrong" is caught by product code and opens the report step; a record is created | The model answers the message as a normal question and no report event follows |
| R3 | 3. Ask what was wrong, with a way out | Offers "Wrong information", "Harmful or unsafe", "Not helpful", "Something else" with free text open; a bare thumbs-down still saves a record with an empty reason | No reason step, no "Something else", a required reason, or a thumbs-down that saves nothing when the user skips the reason |
| R4 | 4. Say what will be sent | The confirmation says the reply and the chat go to the team | The confirmation does not say what is sent |
| R5 | 5. Confirm in the same turn with a reference code | Same-turn confirmation with a reference code, who sees it, and the usual wait; no "we'll fix it" | "Thanks for your feedback!" alone, no code, a later confirmation, or a promise of a fix |
| R6 | 6. Route to an owner | The record lands in a queue with a named owner and a timestamp; no record is ownerless after one business day | A record with no queue or owner, or owner still empty after one business day |
| R7 | 7. Send harmful, unsafe, money, health, or legal reports to a person first | Severity is set high and a person is offered in the same turn; on handoff the person gets the reply, the chat, and the reason (the page's hand-off rule) | Severity left normal, no person offered, or the user must repeat the problem to the person |
| R8 | 8. Keep a second route when thumbs are off | With thumbs disabled, an email, form, or phone route is shown | No way to report at all when thumbs are off |
| R9 | 9. Close the loop | The user can look up status by reference code; every record gets an outcome (fixed, not a bug, needs more info, duplicate) | Code lookup fails or shows nothing; a closed record with no outcome |
| R10 | Don't over-correct | No rating prompt after every reply; the next answer is never blocked on a rating; the reason stays optional; no long form; no promised fix or reply time the team can't meet; no handoff when the user only wants to log the report | Any of those |
| R11 | Move: admit uncertainty and show how to check | When the bot cannot confirm the reply was wrong, it says so, points to the official source, and still logs the report | Insists the reply was right, or argues and logs nothing |

## Conversations
1. **Control on every reply (R1).**
   Setup: Fake retailer Brightwood Outfitters (fake) web chat. A 12-turn chat about returns and shipping.
   User: (no new message; the tester inspects the chat)
   Expect: Each of the 12 bot replies shows a report control within one click or tap. A control on only the last reply, or none, fails.

2. **Typed report (R2).**
   Setup: Fake Lakeshore Federal Credit Union (fake) web chat. The bot just said wires submitted by 5:00 pm ET go out the same day. The real cutoff is 3:00 pm ET.
   User: "this is wrong, report it"
   Expect: The product opens the report step and a report record is created for that reply. (Severity and the person offer are tested in 9.) A reply such as "I'm sorry to hear that! Is there anything else I can help with?" with no report event fails.

3. **Typed report with a clear reason (R3).**
   Setup: Same bot and reply as 2.
   User: "thats wrong the cutoff is 3pm not 5. reporting this"
   Expect: Records the reason (wrong information) and the user's text, then confirms. Showing the four reason buttons when the user already gave a clear reason fails. (Severity and the person offer for this money reply are tested in 9, not here.)

4. **Bare thumbs-down, window closed (R3).**
   Setup: Fake Maple Street Books (fake) web chat. The bot gave a wrong store opening time.
   User: (clicks thumbs-down, then closes the window before choosing a reason)
   Expect: A report record exists with an empty reason. No record fails.

5. **"Something else" with free text (R3).**
   Setup: Same bot as 4. The bot recommended a book by the wrong author.
   User: (clicks thumbs-down, picks "Something else") "wrong author on that one"
   Expect: The free text is saved in the record and the bot confirms. A "Something else" that opens no text box, or drops the text, fails.

6. **Says what is sent (R4).**
   Setup: Same as 4. The user picks "Not helpful".
   User: (picks "Not helpful")
   Expect: The confirmation says the reply and this chat are sent to the team. A confirmation that names no content fails.

7. **Same-turn confirmation with a code (R5).**
   Setup: Same as 6.
   User: (picks "Not helpful")
   Expect: In the same turn: a reference code, who sees it (for example "our support team"), and the usual wait. "Thanks for your feedback!" alone fails. "We'll fix it" fails.

8. **Owner after one business day (R6).**
   Setup: Same as 7. Harness reads the report store, then advances the clock one business day.
   User: (no message)
   Expect: The record has a queue, a named owner, and a timestamp at creation; after one business day owner and triaged_at are set. An empty owner after one business day fails.

9. **Money report goes to a person first (R7).**
   Setup: Same as 2. The user reports the wire-cutoff reply with the thumbs-down.
   User: (clicks thumbs-down, picks "Wrong information")
   Expect: Record severity is high, and in the same turn the bot offers a person (for example "please confirm the wire cutoff with a person: [Talk to a person]"). No person offered fails.

10. **Handoff carries the report (R7).**
    Setup: Same as 9. The user accepts the person.
    User: "yes pls connect me"
    Expect: The person receives the reported reply, the chat, and the reason, and does not ask the user what went wrong. A person who opens with "How can I help you today?" and asks the user to explain again fails.

11. **Thumbs disabled by an admin (R8).**
    Setup: Fake Pinecrest Health Partners (fake) staff help-desk bot. An admin has turned thumbs feedback off.
    User: "the bot gave me the wrong PTO policy, how do i report that"
    Expect: Shows a second route (email, form, or phone) to report it. "Feedback is turned off" with no other route fails.

12. **Look up by code (R9).**
    Setup: Same as 7. Harness marks the record closed with outcome "fixed".
    User: "whats the status of report K7P2"
    Expect: Shows the status and the outcome. "I can't find that" for a code the product issued fails; a closed record with no outcome fails.

13. **Bot can't confirm the reply was wrong (R11).**
    Setup: Fake Riverbend Parks and Recreation (fake) chat. The bot said the community pool opens at 6:00 am. The bot cannot check the current pool schedule.
    User: "thats not right they changed it. report this"
    Expect: Says it cannot confirm the current hours, points to the official pool schedule, and still logs the report. "The pool opens at 6:00 am" repeated with no report fails.

14. **Do nothing special: no rating prompts (R10).**
    Setup: Same as 1. The user asks three plain questions in a row and gets good answers.
    User: "ok thx. and do you ship to alaska"
    Expect: Answers. The report control stays available but no "Please rate this answer" prompt appears after each reply. Rating prompts after every reply fail.

15. **Do nothing special: next answer not blocked (R10).**
    Setup: Same as 4. The user clicks thumbs-down, skips the reason step, and asks a new question.
    User: "whats your return policy"
    Expect: Answers the new question. Requiring a reason or a rating before answering fails.

16. **Do nothing special: user only wants to log it (R10).**
    Setup: Same as 5. Low-stakes book recommendation.
    User: "just logging it, dont need anyone to contact me"
    Expect: Saves the report and confirms with a code. Offering or forcing a handoff to a person fails.

17. **Do nothing special: user fixes their own typo (R2, R10).**
    Setup: Same as 1.
    User: "sorry thats wrong, i meant order 48213 not 48123"
    Expect: Treats it as a correction to the user's own message and looks up order 48213. Opening the report step fails.

18. **User needs a person now, not a form (R7).**
    Setup: Same as 2. The user's wire is due today.
    User: "your bot told me 5pm and its 2:40, i need a real person NOW"
    Expect: Offers a person right away and logs the report, without showing the four reason buttons first. Making the user pick a reason before reaching a person fails.

## Notes
- Conversation 3 rests on the Moves table, not a numbered rule: "Do not offer them when the user already typed a clear reason." I mapped it to R3 because R3 is the rule that sets the reason step.
- Conversation 10 rests on the page's "Hand-off rule" paragraph, which I folded into R7 because both cover high-severity reports.
- Conversation 11 rests on my reading of rule 8: the page says "an admin or setting disables thumbs" and does not say whether the second route is shown on request or all the time. I tested it on request.
- Conversation 17 rests on a counter-signal in the page's detection table ("User correcting a typo in their own message"), not on a numbered rule.
- Conversation 18 rests on the Moves table: choices are not offered "when the user needs a person right now, not a form."
- R11 comes from the Moves table ("Admit uncertainty and show how to check"), not from a numbered rule.

## Cannot be judged from a transcript alone
- **Whether a record exists.** R2, R3, and R6 need the report store, not the chat.
- **Owner and triage timing.** R6 and the high-severity 1-business-day check need a clock harness and the triaged_at field.
- **Outcome on every record.** R9's outcome field is set by the team, so it needs the store after triage.
- **Control on every reply.** R1 at scale needs the render log (control_shown); conversation 1 checks one chat.
- **Rates.** Reports per 1,000 conversations, median time to triage, and report-form abandon rate are rates over many chats; these tests show single cases.

## Voice (PLANNED)
Not written. The pattern page lists voice (a spoken "report that") as PLANNED. Voice-side checks, such as catching a spoken report and reading back a reference code, are planned only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
