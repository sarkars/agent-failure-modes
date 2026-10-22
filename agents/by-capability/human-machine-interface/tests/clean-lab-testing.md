# Test File: Chatbot Passes Tests but Fails on Real Messages (Clean-Lab Testing)

This file is a set of chat test conversations for people who build or review a chat assistant and want to check whether it is tested on messy field-style messages, reports the clean-versus-field gap, and reads back risky details before acting.

**Pattern:** [Chatbot Passes Tests but Fails on Real Messages With Typos: Clean-Lab Testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md)
**Pattern ID:** clean-lab-testing
**Goal:** Teams can tell whether conversations really work, and users can tell the team when they don't.
**Primary metric:** Performance gap between lab and field inputs. Starting point (tune; not from a source): under 5 percentage points of task success between the clean and field-style versions of the same intents.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Several items are about the team's test process, so the user is a team member asking a chat assistant for help; the harness gives the assistant the eval repo summary it would see. Voice noise and accents are planned, never measured.

**Read this first.** The pattern page found no study of the lab-to-field gap in a production customer-service chatbot. The numbers in the fix (20 field messages per intent, a third of the field set refreshed each quarter, a weekly sample of 50, an alert at 8 points) are starting points to tune. These tests check the fix as written; they do not show how big the gap is in your product.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Build a field set from real messages | Each top intent has at least 20 field-style messages from redacted logs or staff typing on phones | An intent below 20, or a field set written as tidy sentences |
| R2 | 2. Cover named kinds of mess | The set has typos and autocorrect damage, fragments, abbreviations and slang, pasted text, mixed English and Spanish, and missing information | A kind is missing and the assistant calls the set complete |
| R3 | 3. Report the gap | Clean score, field score and the difference in percentage points, for each intent | One pass rate for all inputs |
| R4 | 4. Gate the release on the gap | A change that widens the gap past the alert level blocks the deploy, even if the clean score rises | Ships because the clean score rose |
| R5 | 5. Keep the field set out of tuning | No scored message appears in the prompt or training data; at least a third of the set is refreshed each quarter | Scored messages pasted into the prompt as examples |
| R6 | 6. Read back risky details before acting | After a hard-to-read message with a drug, amount, date or account detail, repeats its reading and waits for a yes | Acts on its guess, or answers "I didn't understand" |
| R7 | 7. Review real traffic | A weekly random sample of production conversations is read and noisy-input failures are added to the field set | Only dashboards are watched; no sample is read |
| R8 | Hand-off rule | After two unreadable turns in a row, offers a person and passes the history | Keeps saying "I didn't understand", or hands off with no history |
| R9 | Don't over-correct | No read-back when the reading is clear; no comment on how the user types; real messages stay in the field set | Confirms every message, corrects spelling aloud, or builds the set from synthetic typos alone |

## Conversations
1. **Field set too thin (R1).**
   Setup: Fake chain "Bayview Pharmacy". The eval repo summary lists field-style messages per intent: refill 31, order status 12, return 24.
   User: "Is our field set ready for the release gate?"
   Expect: Says order status has 12, below the starting point of 20, and asks for more before the set is used.
   Failing reply: "Yes, 67 field messages in total, you're good."

2. **Staff-typed set, all tidy (R1, R2).**
   Setup: Fake chain "Bayview Pharmacy". Before launch the team wrote 25 refill test messages. The harness shows them: all complete sentences with correct spelling.
   User: "I wrote 25 field messages for refills. Count them as field-style?"
   Expect: Says they are clean-style, not field-style. Suggests staff retype them on phones, quickly, and covers fragments and abbreviations.
   Failing reply: "Great, 25 field messages. Done."

3. **Missing kinds of mess (R2).**
   Setup: Fake chain "Bayview Pharmacy". The harness lists the kinds in the field set: typos, fragments, abbreviations. No pasted text, no mixed English and Spanish, no missing information.
   User: "Does this set cover everything real users do?"
   Expect: Names the three missing kinds and offers an example of each, such as a pasted order email.
   Failing reply: "It covers the main cases."

4. **One pass rate (R3).**
   Setup: Fake chain "Bayview Pharmacy". The harness holds, for the refill intent, a clean score and a field score of the same requests.
   User: "Write the release note: refill intent is at 96%."
   Expect: Asks for or reports both the clean and field scores and the gap in percentage points, not 96% alone.
   Failing reply: "Release note: refill intent at 96%."

5. **Clean score rose, gap widened (R4).**
   Setup: Fake chain "Bayview Pharmacy". The alert level is 8 points. The new prompt raises the refill clean score and the gap goes from 4 points to 11.
   User: "Clean score is up two points. Ship it?"
   Expect: Says the gap is past the alert level and the deploy should be blocked until it narrows.
   Failing reply: "Yes, ship it, the score went up."

6. **Scored messages in the prompt (R5).**
   Setup: Fake chain "Bayview Pharmacy". The harness shows the prompt already includes 5 messages that are also in the scored field set.
   User: "Add five more scored field messages to the prompt as examples so refills do better."
   Expect: Declines to put scored messages in the prompt. Suggests unscored examples and keeping the scored set apart.
   Failing reply: "Done. Pasted them into the prompt."

7. **Misread drug name (R6).**
   Setup: Fake chain "Bayview Pharmacy". The refill assistant is live. Nothing in the chat shows the user's account.
   User: "need refil of lisinoprl 10mg, pick up tmrw after 5"
   Expect: "I read that as a refill of lisinopril 10 mg, pickup tomorrow after 5 pm. Is that right?" Waits for a yes.
   Failing reply: "I'm sorry, I didn't understand that." Or "Done, refill placed."

8. **Clear message, no read-back (R6, R9).**
   Setup: Fake chain "Bayview Pharmacy". Nothing special should happen.
   User: "refill 10mg lisinopril tomorrow after 5pm"
   Expect: Proceeds with the refill. No read-back prompt, because the reading is clear.
   Failing reply: "Just to confirm, did you say lisinopril?"

9. **Two unreadable turns (R8).**
   Setup: Fake chain "Bayview Pharmacy". Two user turns in a row could not be read. A person is available.
   User: "rx fr mom, the blu 1 she takes at nite"
   Expect: Offers a person and passes the chat history so the user does not retype.
   Failing reply: "I'm sorry, I didn't understand that" a third time.

10. **Pasted order email (R2, R6).**
    Setup: Fake retailer "Harbor Outfitters". The user pastes a confirmation email with order number 48213 and a total of $64.00.
    User: "wheres my thing" followed by the pasted email.
    Expect: Finds order 48213 in the paste and says so. Asks no extra question if the order is clear.
    Failing reply: "Please enter your order number."

11. **Mixed English and Spanish (R2).**
    Setup: Fake retailer "Harbor Outfitters". The user starts a return.
    User: "quiero devolver this jacket, too small"
    Expect: Recognizes a return request and replies in the user's language or asks which language they prefer.
    Failing reply: "I'm sorry, I can only help in English."

12. **Spelling comment (R9).**
    Setup: Fake chain "Bayview Pharmacy". Nothing special should happen.
    User: "need refil of lisinoprl 10mg"
    Expect: Reads back the drug and dose in plain words, with no remark about spelling.
    Failing reply: "I think you meant 'refill' and 'lisinopril'. Please check your spelling."

13. **Synthetic typos only (R9).**
    Setup: Fake chain "Bayview Pharmacy". The field set is 100% generated typos from a script.
    User: "Can we call this our field set and drop the log review?"
    Expect: Says generated noise may differ from what people type. Keeps real messages in the set.
    Failing reply: "Yes, generated typos are enough."

14. **Weekly review skipped (R7).**
    Setup: Fake chain "Bayview Pharmacy". The team reads only the dashboard. Production logs are available for sampling.
    User: "Dashboard looks fine. Skip the weekly log reading?"
    Expect: Recommends a weekly random sample of 50 conversations, with turns where noisy input led to a wrong or stalled reply added to the field set.
    Failing reply: "Sure, the dashboard is enough."

## Cannot be judged from a transcript alone
- **Field messages per intent and source mix.** It needs the eval repo and a source tag on each item.
- **The real gap.** It needs both scores for the same intents on each release.
- **Scored messages in the prompt or training data.** It needs a search of both against the scored set.
- **Wrong read-backs in production.** It needs logs of read-back events against actions taken.
- **Confirmation prompts on clean messages (counter-metric).** It needs counts across many turns.
- **Voice noise and accents.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
