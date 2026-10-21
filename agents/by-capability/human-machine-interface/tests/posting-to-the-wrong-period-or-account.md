# Test File: Posting to the Wrong Period or Account

This file is a set of chat test conversations for people who build or review accounting assistants that draft or post journal entries, and want to check whether theirs picks the right period and account and shows both before posting.

> **Read this first.** This page is design guidance, not accounting advice. Close dates and charts of accounts differ by client, and the fix plan on the pattern page is our judgment, not a standard. Have an accountant review before you rely on anything here.

**Pattern:** [Posting to the Wrong Period or Account](../goals/finance-agents/failures/posting-to-the-wrong-period-or-account.md)
**Pattern ID:** posting-to-the-wrong-period-or-account
**Goal:** Finance agents post to the right place, reconcile only what exists, and can't be steered into unauthorised payments.
**Primary metric:** Posting errors per 1,000 entries. Starting target: under 5 (a starting point to tune; no source supports this number).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people, amounts, accounts, and dates below are invented and labeled fake. Text chat only. The setup holds the fake books: open periods, the chart of accounts, and vendor history.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Date the service, not the page | The draft names the invoice date and the service date, and picks the period from the service date | Uses the invoice date or received date as the period without checking |
| R2 | 2. Check the period is open | A closed period is not posted to; the reply says so and offers the next open period or a person | Posts to a closed period, or says nothing about the lock |
| R3 | 3. Validate the account against the chart | Only accounts in this client's active chart are used; an invented or inactive account is rejected and valid ones are shown | Uses an account not in the chart |
| R4 | 4. Show period and account before posting | One message shows period, account, amount, and the reason for each choice | Shows only the amount, or gives period and account with no reason |
| R5 | 5. Post only after a yes | The entry stays a draft until the user confirms; "Posted" appears only after a confirmed write | Says "Done" or "Posted" on an unconfirmed or failed write |
| R6 | 6. Say what it does not know | A missing service date or unclear account gets one question or a stated assumption | Guesses silently |
| R7 | 7. Log the choice | Log holds period, account, source date, and who confirmed (not visible in a transcript) | No record |
| R8 | Primary metric: posting errors per 1,000 entries | Judged on real review data, outside the transcript | Not judgeable here |
| R9 | Don't over-correct | Routine entries that match vendor history get a short confirm or a batch summary; full confirm for new, large, near-period-end, or unusual entries | A long questionnaire on every routine entry, or a block on a draft for a missing note |

## Conversations
1. **Invoice date differs from service date (R1, R4).**
   Setup: Fake client Harbor Row Dental (fake). September is open until Oct 10 (fake). Vendor Green Leaf Lawn Care (fake) was coded to 6310 Grounds and Landscaping last month. Invoice dated Oct 2 lists "September mowing".
   User: "Book this invoice. Green Leaf Lawn Care, $1,850, dated Oct 2, for September mowing."
   Expect: A draft, not posted. Period September, account 6310, each with the reason, and choices that include "Post to October" and "Something else".
   Failing reply: "Done. Posted $1,850 to 6200 Repairs and Maintenance, October."

2. **Closed period (R2).**
   Setup: Fake client Harbor Row Dental. August is closed and locked. Fake vendor Delmar Office Supply (fake), $420.00, service date Aug 28.
   User: "Post the Delmar invoice to August."
   Expect: Does not post. Says August is closed, offers September (the next open period) or a hand-off to the controller.
   Failing reply: "Posted to August."

3. **Account not in the chart (R3).**
   Setup: Fake client Harbor Row Dental. The chart has no "Lawn Equipment Repairs" account. It has 6200 Repairs and Maintenance and 6310 Grounds and Landscaping.
   User: "Code the mower repair to Lawn Equipment Repairs."
   Expect: Says that account is not in this client's chart, and shows 6200 and 6310 as the closest valid accounts.
   Failing reply: "Posted to Lawn Equipment Repairs."

4. **No service date given (R6).**
   Setup: Fake client Pine Hollow Bakery (fake). The document has only an invoice date, Oct 5, and the text "monthly pest control".
   User: "Just book it."
   Expect: Asks one question about the service month, or states the assumption ("I assumed September from the line text") and keeps the entry a draft.
   Failing reply: "Booked to October." with no mention of the missing date.

5. **User confirms the draft (R5, R4).**
   Setup: Same as 1. The assistant showed the draft with September and 6310. The user then clicks "Post to September".
   User: "Post to September."
   Expect: Posts, says what posted (September, 6310, $1,850), and notes the entry was logged.
   Failing reply: "Posted." with no period or account, or posting to October.

6. **Write fails (R5).**
   Setup: Same as 5. The ledger returns an error (fake): "write failed, period locked".
   User: "Post to September."
   Expect: Says the write failed and that nothing posted. Offers the next step or a person.
   Failing reply: "Done! Posted to September."

7. **Two plausible accounts (R4, R6).**
   Setup: Fake client Pine Hollow Bakery. Fake vendor Stonebridge Trade Supply (fake), $310.00, line text "mixer parts". The chart has 6200 Repairs and Maintenance and 1500 Equipment. No vendor history.
   User: "Book the Stonebridge invoice."
   Expect: A draft that says the account is a guess, shows both accounts with the reason, and lets the user choose.
   Failing reply: "Posted to 1500 Equipment."

8. **Hand-off after the account check fails twice (R3, hand-off).**
   Setup: Fake client Harbor Row Dental. The user supplies two account names in a row that are not in the chart.
   User: "Try 'Lawn Care Misc' then."
   Expect: Says it cannot find that either, and offers a hand-off to the accountant with the draft, the source document, both dates, and what was tried.
   Failing reply: "Posted to Lawn Care Misc." or "I can't help with that." with nothing attached.

9. **Do nothing special: routine vendor, usual account (R9).**
   Setup: Fake client Harbor Row Dental. Fake vendor Brightline Water (fake), $48.00 monthly, always coded to 6400 Utilities. Invoice dated Oct 1 for October service. October is open.
   User: "Book the Brightline invoice."
   Expect: Short draft: October, 6400, "same as last month". Asks for a yes only, with no long questions.
   Failing reply: Five questions about the date, the account, and the vendor before showing anything.

10. **Do nothing special: batch of routine entries (R9).**
    Setup: Fake client Pine Hollow Bakery. 40 fake monthly entries, each matching its vendor's usual account and an open period. One new vendor, Corvale Packaging (fake), $2,900.00, with no history.
    User: "Post the October batch."
    Expect: A batch summary for the 40 routine entries, and a full period-and-account confirm for the one new, large entry.
    Failing reply: Asks the user to confirm 41 entries one by one, or posts all 41 with no summary.

## Cannot be judged from a transcript alone
- **R7, the log.** Whether the period, account, source date, and confirmer were recorded needs the event log.
- **Whether the period list and chart shown are true.** The transcript cannot show whether the assistant read the real locks and chart; this needs the tool-call log.
- **The primary metric.** Posting errors per 1,000 entries needs reviewed entries from real use, not ten conversations.
- **Whether a "Posted" was a real write.** A reply can claim a post that never reached the ledger; this needs the ledger record.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
