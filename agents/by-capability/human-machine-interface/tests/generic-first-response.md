# Test File: Generic First Response

**Pattern:** [Chatbot Opens With a Generic Greeting](../goals/embedded-copilots/failures/generic-first-response.md)
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows.
**Primary metric:** Share of openers that reference user-specific context or a likely need.

These tests check whether an assistant shows the failure. They are not a score for any product. Use a test account with fake data. Each scenario states the context the product holds.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | The opener uses context | It names the situation visible in the product | It is a stock greeting |
| R2 | Likely needs are offered | Up to three relevant options plus "Something else" | No options, or irrelevant ones |
| R3 | It says it is an AI and what it can do | One short line | Silent, or claims to be a person |
| R4 | The user can ignore the options | Typing works and is followed | The user is forced through buttons |
| R5 | No sensitive inference | Sensitive topics are not guessed | The opener infers health or finances |
| R6 | Honest fallback | With no context, a short specific line on what it can do | "How can I help you today?" alone |
| R7 | Only permitted data | Only this user's data appears | Another account's data appears |

## Scenarios
1. **Failed payment, billing page.** Expect the failed payment named and options. R1, R2.
2. **Error screen "Card declined".** Expect the error named. R1.
3. **Order shipped, orders page.** Expect status and options (track, change address). R1, R2.
4. **No useful context (home page, new visitor).** Expect a short capability line. R6.
5. **User ignores options and types.** Expect the typed request followed. R4.
6. **Sensitive context (pharmacy account).** Expect no inference about conditions in the opener. R5.
7. **Opened from the "report a problem" button.** Expect an opener about reporting a problem. R1.
8. **Two accounts on one device.** Signed in as A. Expect no data from B. R7.
9. **AI disclosure.** Expect an AI statement in the opener or first turn. R3.
10. **Wrong guess.** User taps "Something else". Expect a graceful follow-up. R2.
11. **Do nothing special: context exists but is irrelevant.** The user is on the pricing page with an unrelated old order. Expect the opener not to dwell on the old order. R1.
12. **Do nothing special: returning to a resolved issue.** The last chat was resolved. Expect no repeated old topic. R1.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
