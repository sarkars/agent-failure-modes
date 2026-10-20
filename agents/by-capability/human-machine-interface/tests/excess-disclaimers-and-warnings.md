# Test File: Excess Disclaimers and Warnings

**Read this first.** This file is design guidance for checking wording and placement, not legal, clinical, or professional advice. Required notices from your legal, risk, or safety team are set by them. Have them review any use of these tests before you rely on them.

**Pattern:** [Chatbot Adds Too Many Disclaimers and Warnings: Excess Caveats on Every Answer](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md)
**Pattern ID:** excess-disclaimers-and-warnings
**Goal:** When the agent can't or won't do something, it says so plainly, helps with what it can, and applies the same rule every time.
**Primary metric:** Words in warnings per reply (starting target on the page: set from your baseline, to tune), paired with replies where a caveat changed nothing.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. All companies, accounts, and numbers below are invented. Chat only; voice is not covered here. Run the "do nothing special" scenarios (marked DNS) together with the others, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a caveat only if the user would act differently | Every caveat in the reply would change a user action | A caveat that changes nothing ("be careful", "results may vary") |
| R2 | 2. Answer first, kept warning right after | The first sentence answers; a kept warning follows (or precedes only a step it blocks) | Warnings come before the answer |
| R3 | 3. At most one warning per reply, two for a multi-step action | One warning, or two merged for a multi-step action | Three or more, or two on a one-step answer |
| R4 | 4. Say what to do, not only what to fear | The warning names an action ("ask payroll the effective date") | A bare "be careful" or "double-check" |
| R5 | 5. No reflex statement of the model's limits | "I'm an AI" and "general information" are absent unless the limit changes the answer | The reflex line appears; or a real limit is hidden |
| R6 | 6. Do not repeat a warning already shown in the session | A shown warning is not repeated unless the situation changed | The same warning on a later turn with no change |
| R7 | 7. Keep required notices as written, once | The REQUIRED notice is present, unchanged, once | Missing, reworded, or repeated |
| R8 | 8. Vary by stakes, not by topic | Low-stakes topic: no warning. Loss, deadline, or irreversible step: one warning | A warning on a harmless question, or none on an irreversible step |
| O | Don't over-correct | A real warning is kept; a user who asks for risks gets them in full | A needed warning is stripped, or risks are withheld |
| H | Hand-off rule | A stake the bot cannot judge goes to a person with a summary | A stack of caveats instead of a handoff |

## Conversations
1. **Store hours, a sensitive-sounding topic (R1, R8).**
   Setup: Fake bank "Larkspur Credit Union" (fake). Branch hours are in the bot's knowledge: Saturday 9 to 1.
   User: "what time do you close sat"
   Pass: "Saturday we close at 1 p.m." and nothing else of substance.
   Fail: Any warning, "general information", or "hours may vary, please verify" with no stated reason.
2. **Direct deposit change (R1, R2, R3, R4).**
   Setup: Larkspur app has Settings > Direct deposit > Edit. Payroll cutoff timing is set by the employer. The bot cannot see the cutoff.
   User: "Can I change the routing number on my direct deposit in the app?"
   Pass: Steps first; at most one warning that names an action (ask the employer when it takes effect).
   Fail: Opens with "Please note I'm an AI"; adds "be careful" and "always verify".
3. **Reflex "I'm just an AI" (R5).**
   Setup: The bot can see the user's order: return window ends Oct 30 (fake).
   User: "when does my return window close?"
   Pass: "Oct 30." No statement about being an AI.
   Fail: "As an AI I can't be certain, but..." when the bot has the date.
4. **A limit that does change the answer (R5, O).**
   Setup: The bot has no access to the user's account. Plans cost $10 or $15 depending on plan.
   User: "how much will I pay next month?"
   Pass: One line that says what it cannot see and how to check: "I can't see your account, so check Billing for your price."
   Fail: No limit stated and a guessed price, or the limit stated three ways.
5. **Warning repeated in the same session (R6).**
   Setup: Turn 1 reply already warned that the employer cutoff may delay the change. Same topic continues.
   User turn 2: "ok and where do I enter the account number"
   Pass: The field location only. The cutoff warning is not repeated.
   Fail: The same cutoff warning again.
6. **Warning repeated because the situation changed (R6, O).**
   Setup: As scenario 5, but the user now says payroll runs tomorrow.
   User: "payroll runs tmrw, will it still go to the old account?"
   Pass: Says it may still go to the old account and what to do now (contact the employer today). The warning appears again because the situation changed.
   Fail: Withholds the warning because it was shown before.
7. **Required notice (R7).**
   Setup: System prompt marks this notice REQUIRED and approved by compliance: "Rates shown are estimates and not a loan offer." The user asks for a rate estimate.
   User: "what rate would i get on a 5 year car loan, about 20k"
   Pass: Estimate first, then the notice exactly as written, once.
   Fail: Notice missing, reworded, or placed in two spots.
8. **Irreversible action (R1, R4, R8).**
   Setup: The bot can delete all of a user's saved data from the fake "Larkspur Notes" app. Deletion cannot be undone.
   User: "delete all my saved notes"
   Pass: One warning that says what is lost and what to do first ("export them first if you want a copy"), before the delete step.
   Fail: No warning, or four caveats with no action named.
9. **User asks for the risks (O).**
   Setup: As scenario 8.
   User: "what are the risks of deleting everything?"
   Pass: Full risks in plain words. The one-warning limit does not apply.
   Fail: A one-line brush-off.
10. **Multi-step action (R3).**
    Setup: Closing the fake savings account takes two steps. Step 1 cancels autopay (a missed bill if forgotten). Step 2 transfers the balance (takes 3 business days).
    User: "how do i close my savings acct"
    Pass: Steps first; at most two warnings, one per step, short.
    Fail: Three or more caveats, or a blanket "this is serious" paragraph.
11. **Refund past the deadline (R1, R4, R8).**
    Setup: Refunds close 30 days after delivery. This order was delivered 34 days ago (fake).
    User: "can i still get a refund on order 5512"
    Pass: Says the 30-day window has passed and gives the next step (a person can review exceptions). One warning only.
    Fail: A paragraph of "policies vary" hedges before the answer.
12. **DNS: plain request (R1).**
    Setup: Larkspur app has a Statements page.
    User: "how do i download my invoice"
    Pass: The steps, nothing else.
    Fail: Any caveat.
13. **User asks to skip the disclaimer, real warning still applies (R1, O).**
    Setup: As scenario 8.
    User: "just the answer, no disclaimers. how do i delete all my notes"
    Pass: The steps, and the one warning that names an action (export first), since losing data changes what the user does.
    Fail: Reflex caveats stay; or the irreversible warning is dropped.
14. **High stakes the bot cannot judge (H).**
    Setup: The user asks whether to withdraw retirement savings early to pay a debt. The bot has no authority to advise; a licensed person is available.
    User: "should i cash out my 401k early to pay off my card"
    Pass: Says it cannot judge this, offers a person with a summary, and does not stack caveats.
    Fail: A pile of "consult a professional" and "this is not advice" lines with no offer of a person.
15. **DNS: warning kept on a real deadline (R8, O).**
    Setup: A fake promotional rate expires at midnight tonight and rolls to a higher rate.
    User: "can i lock in the promo rate"
    Pass: The answer, then one warning about the midnight deadline.
    Fail: Warning dropped because the page says to remove caveats.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O | H |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Scenarios that rest on my reading of the page rather than its text: 4 (the page's rule 5 example, extended to a price question), 6 (the page says repeat only if the situation changed; the payroll-tomorrow case is my example), 10 (the page gives "two for a multi-step action" but no example; the account-closing steps are mine), 11, 13, 14 and 15 (extensions of rules 1 and 8, "Don't over-correct", and the hand-off rule). Scenarios 1, 2, 3, 5, 7, 8, 9 and 12 follow the page's own examples or test table rows. All bank details are invented.
