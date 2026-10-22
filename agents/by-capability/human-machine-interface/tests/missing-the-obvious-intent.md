# Test File: Assistant Misses the Obvious (Missing the Obvious Intent)

This file is a set of chat test conversations for people who build or review an in-product assistant, and want to check that it answers the likeliest reading of a plain request first and asks only when it must.

**Pattern:** [Chatbot Misses the Obvious](../goals/embedded-copilots/failures/missing-the-obvious-intent.md)
**Pattern ID:** missing-the-obvious-intent
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows.
**Primary metric:** Top-intent accuracy on a test set of simple, common requests. Starting target: over 95% (a starting point to tune on your own set).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat and in-product text only. Each Setup line supplies the state a real product would supply (the page the user is on, the account state, the prior turns, the intent label); the harness must feed those fields. Order numbers, plan names and counts in Setup are made-up test values. Voice and email versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Rank readings using the words, the screen and the account state | The reply matches the reading the setup labels as likeliest | A neighboring answer, or a lecture on a related topic, comes first |
| R2 | 2. If one reading clearly leads, answer it directly | The first reply is the answer, with no question before it | A question, a menu or a tip comes before the answer |
| R3 | 2. Add one line for the next most likely reading | One line covers the runner-up and is correct | No alternative where one is labeled, or a long list |
| R4 | 3. If no reading leads, ask one short question with choices | One short question with the options as choices | A guess, or an open "How can I help?" with no options |
| R5 | 4. Do not over-read | The reply stays on what was asked | Assumed motives, advice nobody asked for, or extra content |
| R6 | 5. Confusion-list pairs have a fixed first answer | The first answer matches the listed one for the pair (reset vs change, cancel vs pause) | The other half of the pair comes first |
| R7 | Context breaks the tie, and the reply says so | Uses the page or account state and names it ("Since you're on the billing page...") | Context is supplied but ignored or unmentioned |
| R8 | Hand-off rule | After two misses in a row, a person is offered, and not offered after one miss | A third attempt with no offer, or an offer after the first miss |
| R9 | Don't over-correct | Risky requests (moving money, deleting data) get a question first; plain requests get no question; truly ambiguous ones are not answered by a guess | Acting on a risky guess, asking about a plain request, or answering an ambiguous one as if plain |

## Conversations
1. **Reset password, signed out (R1, R2, R3, R6).**
   Setup: Fake app "Fernhill Banking Help", a chat help desk inside a fake credit union app. The user is signed out. The confusion list says reset-vs-change: first answer is reset.
   User: "how do i reset my password"
   Expect: The reset steps first (use "Forgot password" on the sign-in screen, enter the email, open the emailed link), then one line: if signed in and just changing it, go to Settings > Security.
   Failing reply: "Strong passwords use at least 12 characters. Would you like tips?"

2. **Cancel with one subscription (R1, R2, R6).**
   Setup: Fake app "Plume Streaming". The account has one active plan, "Plume Basic" (test value). The confusion list says cancel-vs-pause: first answer is cancel.
   User: "cancel"
   Expect: The cancel path for Plume Basic first, then one line that a pause option exists if the user only wants a break.
   Failing reply: "Are you sure you want to cancel? Many members find our deals helpful. What is the reason?"

3. **Do nothing special: receipt (R2, R5, R9).**
   Setup: Fake app "Plume Streaming". The user has one paid month on file. One reading leads; no risk.
   User: "I need a receipt for my order"
   Expect: How to get the receipt (Account > Billing > Receipts), nothing more. No question.
   Failing reply: "Is this for taxes or for a refund? Tell me more about what you need it for."

4. **Do nothing special: plain hours question (R2, R5, R9).**
   Setup: Fake app "Larkspur Hardware Help". Store hours are on file: weekdays 8 a.m. to 6 p.m. (test values).
   User: "when do you open"
   Expect: The opening time, in one or two sentences. No tips, no extra offers.
   Failing reply: "Great question! Before I answer, are you asking about the store, the lumber yard or the online desk?"

5. **Truly ambiguous message (R4, R9).**
   Setup: Fake app "Plume Streaming". No page context; the intent label is ambiguous. Likely readings: playback problem, sign-in problem, payment problem; none leads.
   User: "its not working"
   Expect: One short question with choices: video won't play, can't sign in, payment problem, something else. No guess at a fix.
   Failing reply: "Try clearing your cache and restarting the app."

6. **Two close readings (R4).**
   Setup: Fake app "Plume Streaming". The account is on "Plume Plus" (test value) with both an upgrade to Premium and a downgrade to Basic open. The two readings are about equally likely.
   User: "change my plan"
   Expect: One short question with two choices, upgrade or downgrade, plus "Something else". Nothing else first.
   Failing reply: "Here are all our plan prices and features..." (a wall of text that avoids the question)

7. **Many readings, none close (R4, R5).**
   Setup: Fake app "Fernhill Banking Help". The user is on the home screen. The intent label is broad.
   User: "help with my account"
   Expect: Asks what the user is trying to do, with a few examples (check a balance, reset a password, dispute a charge). Does not pick one.
   Failing reply: "Sure, I will close your account now."

8. **Risky request with several items (R9).**
   Setup: Fake app "Pinecrest Photo Vault". The user has three albums, "Trip 2025", "Trip 2026" and "Receipts" (test values), and the message names none. Delete is permanent.
   User: "delete it"
   Expect: Asks which album, listing the three, before doing anything.
   Failing reply: "Done. Your most recent album was deleted."

9. **Context breaks the tie (R1, R7).**
   Setup: Fake app "Plume Streaming". The user is on the billing page. The latest charge is $2 higher than last month (test values) because of a plan change on the account.
   User: "why is this higher"
   Expect: Uses the billing page and the account, says so ("Since you're on the billing page..."), and explains the change in the charge.
   Failing reply: "What is higher? Please tell me what you mean."

10. **Runner-up is the real one (R3, R6).**
   Setup: Fake app "Fernhill Banking Help". The user is signed in and has just said they know their password. The confusion list says reset-vs-change: first answer is reset.
   User: "reset my password" then, after the reply, "thx i know it, just wanna change it"
   Expect: First reply gives reset steps plus the one-line change path (Settings > Security). Second reply gives the change steps in full, without apology or a restart.
   Failing reply: A first reply with no mention of the change path, so the second turn starts from zero.

11. **Over-reading check (R5).**
   Setup: Fake app "Larkspur Hardware Help". The return window on file is 30 days (test value).
   User: "what is your return window"
   Expect: The window, 30 days, and nothing about gifts, reasons or restocking fees.
   Failing reply: "30 days. Are you returning a gift? You may want to think about whether it is worth the hassle..."

12. **Do nothing special: one order to track (R2, R9).**
   Setup: Fake app "Larkspur Hardware Help". The account has one open order, 8841 (test value), shipped.
   User: "track my order"
   Expect: The tracking status for order 8841 straight away. No question about which order.
   Failing reply: "Which order do you mean? Please give me the order number."

13. **Two misses in a row (R8).**
   Setup: Fake app "Plume Streaming". The assistant has already answered "refund" with refund policy text twice; the user meant "stop the charge going out tomorrow". Both are logged as misses (the user reworded twice). A person is available.
   User: "no, i said stop it from charging me tomorrow"
   Expect: Answers the reworded request (steps to turn off auto-renew) and offers to bring in a person, since this is the second miss. After the first miss, no offer.
   Failing reply: A third attempt with refund policy text and no offer of a person.

14. **Do nothing special: invoice download (R2, R5, R9).**
   Setup: Fake app "Fernhill Banking Help". The user is on the statements page, signed in. One reading leads.
   User: "download my invoice"
   Expect: The steps to download the invoice from the statements page. No question, no extras.
   Failing reply: "Do you want a PDF, a CSV or a printed copy by mail? And for which month?"

## Cannot be judged from a transcript alone
- **Whether the golden set was re-run after a model or prompt change.** It needs the release log, not the visible text.
- **Rephrase-after-first-answer and over-clarification rates.** Both are rates over many sessions and need the intent labels in the event log.
- **Whether the labeled likeliest reading is right.** It needs two reviewers, not one chat.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
