# Test File: Typos, Shorthand, and Noisy Input

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs understands typos, texting shorthand, and sloppy typing without bouncing the user, silently "fixing" an ID, or acting on a misread value.

> **Read this first.** These are test conversations only. They are not legal or professional advice. All businesses, codes, names, and amounts are invented (fake).

**Pattern:** [Chatbot Doesn't Understand My Typos or Texting Shorthand: Typos, Shorthand, and Noisy Input](../goals/language-and-locale/failures/typos-shorthand-and-noisy-input.md)
**Pattern ID:** typos-shorthand-and-noisy-input
**Goal:** Noisy input is understood nearly as well as clean input.
**Primary metric:** Intent accuracy on a noisy set vs. clean. Starting target on the pattern page: gap under 5 points (a starting point to tune, not from a source). Single conversations below cannot measure a gap; see "Cannot be judged from a transcript alone".
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Text chat only; voice-to-text errors and web forms are PLANNED, not written. Every conversation below carries the Pattern ID above; the R-lines say which rule it checks.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Answer, don't bounce | A message with one obvious reading gets an answer or a restatement of that reading | "I didn't understand, please rephrase" to a message a reviewer reads one way |
| R2 | 2. Never correct or comment on spelling | No mention of typos, spelling, "did you mean," or "complete sentences" | Any such remark |
| R3 | 3. Never silently repair identifiers | A code, amount, date, phone number, or name is used exactly as typed; if it matches no record, the bot says so and asks | An action or lookup on a value the user did not type, such as the nearest match |
| R4 | 4. Confirm before acting | Before a change, cancel, refund, or payment, the bot restates the action with key values in plain spelling and waits for a yes | A write action with no restatement turn |
| R5 | 5. Ask only when readings split | One question or 2-4 choices plus "Something else" when two readings lead to different actions | A guess between different actions |
| R6 | 6. Name what you did understand | A clarifying reply quotes words from the user's turn and asks about the rest | A question about the whole message, or a generic fallback |
| R7 | 7. Do not mirror the shorthand | The reply is in the product's normal register | "ur," "thx," "u," or other shorthand echoed back |
| R8 | 8. Two misses, offer a person | A person is offered by the second miss; no third "didn't understand" | A third fallback in a row |
| R9 | Hand-off rule | If an identifier on a money or booking action still matches nothing after one ask, the bot offers a person with what was understood | Another guess, or a dead end |
| R10 | Don't over-correct | No restatement or quote-back on read-only answers; no question when one reading is clear or when both readings give the same answer | Confirming every message, or turning every typo into a question |

## Conversations
1. **Order status with typos (R1, R2).**
   Setup: Chat for a fake store, Pinecrest Supply (fake), with a read-only order-status lookup. Order 55123 exists.
   User: "wheres my ordr, #55123"
   Expect: The status for order 55123 with no remark on spelling. A rephrase request or "did you mean order?" fails.

2. **Flight change in shorthand (R1, R5).**
   Setup: Fake airline, Skyline Air (fake). Confirmation 7XK2QP exists, with flights on Friday, Oct 23 and Friday, Oct 30 possible.
   User: "cn u chng my flite 2 fri? same cty. conf # 7XK2QP"
   Expect: The bot reads it as a change request and asks only which Friday (or offers the two dates), using 7XK2QP exactly as typed. "Which flight?" fails, because the code names it. "Please rephrase" fails.

3. **No spelling comment on a casual question (R2).**
   Setup: Fake pharmacy, Maple Pharmacy (fake). Store hours are in the bot's knowledge.
   User: "wat time do u clos tmrw"
   Expect: Tomorrow's closing time in plain spelling, with no remark on the typing. Any mention of spelling fails.

4. **Code with two characters swapped (R3).**
   Setup: Skyline Air. Confirmation 7XK2QP exists. 7XK2PQ does not.
   User: "cancel flight 7XK2PQ pls"
   Expect: The bot says it finds no booking with that code and asks the user to check it. Using 7XK2QP, the nearest real code, fails.

5. **Name typed oddly on a booking (R3).**
   Setup: Fake clinic, Clinica Norte (fake), booking an appointment under a name.
   User: "book it under Jhon Smyth"
   Expect: The bot uses "Jhon Smyth" exactly as typed and shows it back in the restatement. Changing it to "John Smith" without being asked fails.

6. **Subscription cancel (R4).**
   Setup: Fake streaming service, Brightline (fake), with a cancel-subscription action.
   User: "cancl my subscripton"
   Expect: The bot restates "cancel your subscription" (with the plan name and end date if it has them) and waits for a yes. Cancelling at once fails.

7. **Refund with a typed amount (R3, R4).**
   Setup: Pinecrest Supply, with a refund action. The last charge was $42.50.
   User: "pls refnd my last charge, 42.50"
   Expect: The bot restates the refund of $42.50 in plain spelling and waits for a yes. A refund with no restatement fails.

8. **Ambiguous abbreviation (R5).**
   Setup: Clinica Norte, with patient-lookup and payment intents both live.
   User: "pt balance"
   Expect: One question or choices such as "Patient" and "Payment" plus "Something else." Guessing one reading fails.

9. **Do nothing special: shorthand with one clear meaning (R10).**
   Setup: Maple Pharmacy.
   User: "wat r ur hrs"
   Expect: The store hours, with no question and no restatement. "Do you mean hours?" fails.

10. **Partly readable message (R6).**
    Setup: Pinecrest Supply.
    User: "asdf, my thng broke"
    Expect: The bot quotes "broke" and asks which item or order. A generic "I didn't understand, please rephrase" fails.

11. **Do not mirror the shorthand (R7).**
    Setup: Brightline support chat.
    User: "u r gr8, thx"
    Expect: A reply in the product's normal register, such as "You're welcome. Anything else I can help with?" Echoing "ur" or "thx" fails.

12. **Two unreadable messages in a row (R8).**
    Setup: Pinecrest Supply. The user's first message was unreadable and the bot has asked one question about it.
    User: "kjh wrtq bnn ??" (second unreadable message)
    Expect: The bot offers a person by this turn and passes along what it understood. A third "I didn't understand" fails.

13. **Identifier still matches nothing (R9).**
    Setup: Skyline Air. The bot has already told the user that 7XK2PQ matches no booking and asked them to check.
    User: "its 7XK2PQ i swear. cancel it"
    Expect: The bot does not use a near match and offers a person with the typed code and the request. Cancelling 7XK2QP fails.

14. **Do nothing special: clean message (R10).**
    Setup: Maple Pharmacy.
    User: "What time does the store open on Saturday?"
    Expect: The opening time, with no quote-back and no confirmation. "Just to confirm, you're asking about Saturday hours?" fails.

15. **Do nothing special: read-only lookup with an informal message (R10).**
    Setup: Pinecrest Supply, read-only lookup. Order 55123 exists.
    User: "check status of 55123"
    Expect: The status, with no restatement turn. A confirm-before-lookup turn fails, because confirmation is for write actions.

16. **Dictation-style errors on a write action (R4).**
    Setup: Clinica Norte, with a reschedule action. The patient has an appointment.
    User: "I need to reschedual my apointment for next tuesday morning"
    Expect: The bot handles the reschedule request with no spelling remark and restates the change (appointment, the Tuesday date, a morning slot) before acting. Rescheduling with no restatement fails.

## Cannot be judged from a transcript alone
- **Primary metric.** The page measures a gap in intent accuracy between a clean set and a noisy copy. That needs labeled data and many runs. These are single cases.
- **Rephrase requests on an obvious reading (rate).** Needs a sample of production turns and a reviewer.
- **Identifiers changed from user text (R3).** A transcript may look right while the tool call used another value. Check the tool-call log against the user's typed value.
- **Voice and dictation errors from speech recognition.** PLANNED, not covered.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives eight scenarios. Conversations 1, 2, 4, 6, 8, 10, 11, and 12 follow them.
- Conversations 3, 5, 7, 9, 13, 14, 15, and 16 are my additions from the rules: 3 (rule 2), 5 and 7 (rules 3 and 4), 9, 14, and 15 (Don't over-correct), 13 (hand-off rule), and 16 (rule 4).
- The airline, store, pharmacy, clinic, streaming service, names, and amounts are mine. "7XK2QP" and "55123" come from the page's examples.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
