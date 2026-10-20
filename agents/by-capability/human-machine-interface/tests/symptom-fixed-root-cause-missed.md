# Test File: Chatbot Fixes the Same Problem Again and Again (Symptom Fixed, Root Cause Missed)

This file is a set of chat test conversations for people who build or review support bots and want to check whether theirs looks at the cause when the same problem comes back, instead of repeating the same fix.

**Pattern:** [Chatbot Fixes the Same Problem Again and Again: Symptom Fixed, Root Cause Missed](../goals/conversation-frameworks/failures/symptom-fixed-root-cause-missed.md)
**Pattern ID:** symptom-fixed-root-cause-missed
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Repeat-contact rate for the same root cause. The pattern page sets no target; track a baseline, then aim to lower it.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses and people below are invented and labeled fake. Text chat only. The pattern page found no controlled study of chatbots and repeat contacts, so these tests check behavior against the page's rules. Each setup says what the fake bot can see and change, because rules 1, 4, and 6 depend on it. In every setup the bot can take a one-time payment, see the card on file and its expiry, and change the autopay card after the user agrees, unless the setup says otherwise. Its history lookup covers this user's contacts and bot actions for the last 30 days, the page's starting point.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Look for a prior match before applying a fix | The reply shows the history was used: it names the earlier failures or says the problem has come back | The reply treats the request as a first-time problem despite a match |
| R2 | 2. On a match, say it is a repeat, then still give what was asked | One sentence naming the repeat, and the requested fix is still done in the same reply | No repeat sentence, or the fix is held back behind questions |
| R3 | 3. One question about the cause, not the symptom | Exactly one question, naming a fact from the account (such as the card's last four digits and expiry) | Several questions, or a question about the symptom ("what happened?") |
| R4 | 4. Fix the cause, or say who can | Changes the account only after the user says yes, offering choices with "Something else" | Changes autopay with no yes |
| R5 | 5. No third identical workaround | After two identical workarounds, the next reply asks the cause question or hands off | A third bare workaround |
| R6 | 6. Record the result | The session record holds a cause tag (such as an expired card) and whether the cause was fixed | No tag, or the workaround logged as the fix |
| R7 | 7. Say what to expect | After a cause fix, states what happens next and does not promise it will never recur | "This won't happen again" |
| R8 | Hand-off rule | Cause outside what the bot can see or change, or the problem returns after a cause fix: hands off with the user's goal, contact dates, workarounds applied, and cause tag | Another workaround, or a hand-off with no summary |
| R9 | Don't over-correct | No match means no cause question and no "recurring" claim. "Just take the payment" is done first. The cause check is offered once | A cause question on a first contact, a weak-match "again" claim, or repeated asking |

## Conversations
1. **History used (R1).**
   Setup: Fake utility Prairie Light & Water (fake), billing chat. The history shows two earlier autopay failures. The card on file ends in 6031 and its expiry has passed.
   User: "autopay failed again. can u take the payment now"
   Expect: The reply shows the bot used the history, for example by naming the earlier failures. A reply that reads as a first-time failure fails.

2. **Repeat sentence, fix still done (R2).**
   Setup: Same as conversation 1.
   User: "need this paid before the due date. autopay failed again"
   Expect: One sentence saying this is a repeat, and the payment is taken in the same reply. Holding the payment until the user answers fails.

3. **One cause question (R3).**
   Setup: Same as conversation 1.
   User: "autopay failed again, just take it"
   Expect: Exactly one cause question citing the card ending 6031 and its expiry, such as whether that card is still active. "What happened?" or two questions fails.

4. **Change only after a yes (R4).**
   Setup: Same as conversation 1. The bot asked whether the card is still active.
   User: "no, the bank sent me a new card"
   Expect: Offers choices such as new card on autopay, bank account, keep paying by hand, or something else, and does not change autopay until the user agrees. Adding the new card in this reply fails.

5. **Third workaround (R5).**
   Setup: Same as conversation 1. The history shows two one-time payments already applied for autopay failures. The cause has not been asked about.
   User: "autopay failed, take the payment again"
   Expect: The reply asks the cause question or hands off. Taking the payment alone, as a third identical workaround, fails.

6. **What to expect after the fix (R7).**
   Setup: Same as conversation 1. The new card was added to autopay after the user agreed.
   User: "great. so this wont happen again right?"
   Expect: States what happens next, such as that next month's bill charges the new card, and does not promise it will never recur. "Never again" fails.

7. **Record the result (R6).**
   Setup: Same as conversation 6. The test harness shows the saved session record after the chat.
   User: "ok thanks, bye"
   Expect: The record holds a cause tag for the expired card and a flag that the cause was fixed. A record with no tag, or one that logs only the payment, fails.

8. **Cause the bot cannot see (R8).**
   Setup: Same utility. The card on file is valid and not expired. The history shows two earlier failures, each handled with a one-time payment. The bot cannot see the billing system's autopay log.
   User: "autopay failed again. card is fine, i checked"
   Expect: Says it cannot see why, and hands off with the user's goal, the contact dates, the two payments applied, and a cause tag. Another bare payment fails.

9. **Failure after a cause fix (R8).**
   Setup: Same utility. The history shows the card was updated on autopay earlier, recorded as a cause fix. Autopay failed again.
   User: "autopay failed AGAIN even with the new card"
   Expect: Hands off with a summary, including the cause fix already made. Asking the same card question again fails.

10. **Control: first-time failure (R9).**
    Setup: Same utility. No earlier contact on this problem type.
    User: "my autopay failed this month. can you take the payment"
    Expect: Takes the payment. No cause question and no "this keeps happening" line. A cause question fails.

11. **Control: weak match (R9).**
    Setup: Same utility. The only earlier contact, three weeks ago, was a question about paperless billing, a different problem type.
    User: "autopay failed, can you take the payment now"
    Expect: Takes the payment with no claim that the problem is recurring. "This is the second time" fails.

12. **Control: "just take the payment" (R9).**
    Setup: Same as conversation 1.
    User: "i'm in a hurry. just take the payment"
    Expect: Takes the payment first and offers the cause check once, in a sentence. Withholding the payment until the cause is discussed fails.

13. **Control: user declines the check (R9).**
    Setup: Same as conversation 1. The bot has offered the cause check.
    User: "no thanks, just the payment"
    Expect: One-line acceptance and no second ask about the cause in this chat. Asking again fails.

14. **Control: no blame (R9).**
    Setup: Same as conversation 1.
    User: "autopay failed again. this is the third time"
    Expect: Neutral wording that gives the account fact and asks. "You must have changed your card" or any line implying the user caused it fails.

## Notes
- Conversation 7 rests on rule 6, which concerns saved state. I tagged it R6 and it needs the harness record, not the transcript.
- Conversation 5 reads rule 5 as: the reply must contain a cause question or hand-off, and the payment may still be taken with it, as rule 2 allows.
- Conversation 14 rests on the page's sentence not to assume a repeat means the user did something wrong. It is the most subjective test here.

## Cannot be judged from a transcript alone
- **Whether the lookup ran (R1).** A transcript shows the reply, not the lookup. The page says the bot can only check history if the product gives it access.
- **The saved record (R6).** Cause tag and cause-fixed flag live in state, not the chat.
- **Repeat-contact rate.** It needs tagged contacts over a window you choose. These tests do not measure it.
- **Whether a cause fix holds.** That needs later contacts, not a single chat.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
