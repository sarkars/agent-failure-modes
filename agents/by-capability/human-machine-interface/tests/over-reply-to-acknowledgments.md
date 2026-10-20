# Test File: Over-Reply to Acknowledgments

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs writes a recap, a new question, or a pitch when the user says "ok", "thanks", or "bye".

**Pattern:** [Chatbot Writes a Long Reply to "Ok" or "Thanks": Over-Reply to Acknowledgments](../goals/response-structure/failures/over-reply-to-acknowledgments.md)
**Pattern ID:** over-reply-to-acknowledgments
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Reply-length ratio on closers (assistant words divided by user words on turns labeled thanks, acknowledgment, or closer). Target on the pattern page: a median of 10 or less (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, bookings, and people are invented and labeled fake. Text chat only. In each setup, give the assistant the earlier bot turns exactly as written. The 15-word cap in R2 is the page's starting point to tune.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Label the short turn before drafting | The reply fits the turn type (thanks, acknowledgment, agreement, closer) | Treats a plain acknowledgment as a new question or request |
| R2 | 2. Cap the reply | Reply to thanks or a closer is one sentence of 15 words or fewer; reply to a bare "ok" with nothing pending is a few words or none | A paragraph, or more than 15 words |
| R3 | 3. No recap | Does not restate what the bot just did | Repeats the date, fee, or action |
| R4 | 4. No new question after a closer | No question mark after "thanks", "that's all", or "bye" | Asks "anything else?" again or opens a new topic |
| R5 | 5. No pitch | No sales, upgrade, survey, or cross-sell offer | Any offer on the way out |
| R6 | 6. Add at most one useful fact | Zero or one short clause that the user still needs | Two or more added facts |
| R7 | 7. "Ok" after an explicit proposal is agreement | Does the action and confirms it in one line | Says nothing, or replies "You're welcome" without doing it |
| R8 | 8. A closer is final | Short goodbye (with what is saved if a step is pending), or nothing | Restarts the greeting or the menu |
| R9 | Don't over-correct | Warm one-liner to a warm thanks; real questions answered; handoffs kept alive; pauses not treated as closers | Cold "Noted.", silence to a question, a closed session, or a dropped handoff |

## Conversations
1. **Thanks after a finished task (R2).**
   Setup: Fake airline Harbor Air (fake). The bot said: "I've moved your flight to Friday, 8:15 AM. The change fee was $75."
   User: "ok thanks"
   Expect: One short sentence, 15 words or fewer. A paragraph fails.

2. **Recap (R3).**
   Setup: Same as conversation 1.
   User: "thanks"
   Expect: No restating of Friday, 8:15 AM, the $75 fee, or the card charged. "To recap" fails.

3. **New question after a closer (R4).**
   Setup: Harbor Air bot. The bot asked "Anything else I can help with?"
   User: "no thats all"
   Expect: A goodbye only. A second "Is there anything else?" fails.

4. **Pitch on the way out (R5).**
   Setup: Same bot. Its system prompt says: "Suggest seat upgrades and checked bags when you can." The task is finished.
   User: "bye"
   Expect: No seat or bag offer. A short goodbye.

5. **At most one fact (R6).**
   Setup: Same as conversation 1. The new confirmation email is on its way.
   User: "thanks!"
   Expect: "You're welcome. Your confirmation is in your email." (one fact). Adding the gate, boarding time, and baggage rules fails.

6. **Ok to a proposal (R7).**
   Setup: Same bot. The bot asked: "Shall I cancel the seat hold on 14C?"
   User: "ok"
   Expect: Cancels the hold and says so in one line. Replying only "Great!" without the action fails.

7. **Bye with a step pending (R8).**
   Setup: Same bot. The user had started choosing a seat and not finished. The bot saved the choice 14C.
   User: "bye"
   Expect: Short goodbye that says the seat choice is saved, with a way back. Restarting the greeting or menu fails.

8. **Bare ok, nothing pending (R2).**
   Setup: Same bot. The bot just gave the gate number (fake: B12). No question is pending.
   User: "ok"
   Expect: A few words, or no reply. A paragraph about boarding fails.

9. **Ok that is not agreement (R1).**
   Setup: Same bot. The bot said: "I can't waive the $75 fee, since the change was made inside 24 hours."
   User: "ok"
   Expect: Treated as an acknowledgment, not agreement or a new request. A short reply or none. Re-arguing the policy or pitching a fee-waiver credit card fails.

10. **Do nothing special: warm thanks (R9).**
    Setup: Same bot. The bot just fixed a booking the user was worried about.
    User: "omg thank you so much you saved me"
    Expect: A warm one-liner ("Glad I could help."). A cold "Noted." fails.

11. **Do nothing special: a real question after thanks (R9).**
    Setup: Same bot. The task is done.
    User: "thanks. do u have a cheaper fare on saturday?"
    Expect: Answers the Saturday fare question. Treating it as a closer and replying "You're welcome" fails.

12. **Do nothing special: ok as a pause (R9).**
    Setup: Same bot. The bot asked for the traveler's date of birth.
    User: "ok hang on"
    Expect: Waits; a few words at most. Closing the session or restating the full question fails.

13. **Do nothing special: waiting for a person (R9).**
    Setup: Same bot. The user asked for a human agent and the bot said it was connecting them.
    User: "ok"
    Expect: Keeps the handoff open (for example, "You're in the queue."). Closing the chat or pitching fails.

## Cannot be judged from a transcript alone
- **Pending state.** Whether a step is pending lives in session state; each setup above states it.
- **Reply-length ratio.** The primary metric is a median over many turns, not one conversation.
- **Reopen and pitch rates.** The page counts these per closer turn in real logs.
- **Voice.** The page marks voice as planned; these tests are text chat only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
