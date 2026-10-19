# Test File: Missing the Obvious Intent

**Pattern:** [Chatbot Misses the Obvious](../goals/embedded-copilots/failures/missing-the-obvious-intent.md)
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows.
**Primary metric:** Top-intent accuracy on a test set of simple, common requests.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. For each scenario, write down the expected first answer before you run it.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Answer the likeliest reading first | The first reply addresses the labeled likeliest reading | A neighboring answer, a lecture, or a question comes first |
| R2 | Offer the runner-up in one line | One line covers the next likeliest reading | No alternative, or a long list |
| R3 | Ask only when no reading leads | One short question with choices on a truly ambiguous message | No question, or a question on a plain request |
| R4 | Do not over-read | The reply stays on what was asked | The reply adds assumed motives or unrequested content |
| R5 | Risky requests: ask first | A costly wrong guess triggers a question | The assistant acts on a guess |
| R6 | Context breaks ties | Page or account state is used and mentioned | Context is available but ignored |

## Scenarios
1. **Reset password.** "how do i reset my password". Expect reset steps first, change-password in one line. R1, R2.
2. **Cancel.** "cancel" with one active subscription. Expect the cancel path. R1.
3. **Receipt.** "I need a receipt for my order". Expect how to get it. R1.
4. **Plain hours question.** "when do you open". Expect hours, nothing else. R1, R4.
5. **Truly ambiguous.** "it's not working". Expect one short question with choices. R3.
6. **Two close readings.** "change my plan" when upgrade and downgrade are both open. Expect a short choice question. R3.
7. **Risky.** "delete it" with several items. Expect a question first. R5.
8. **Context ties.** "why is this higher" on the billing page. Expect the billing page used. R6.
9. **Runner-up is real.** "reset my password" from a signed-in user who wants to change it. Expect the one-line alternative to be present and correct. R2.
10. **Over-reading check.** "what is your return window". Expect the window, not advice about returning gifts. R4.
11. **Do nothing special: plain request, one reading.** "track my order" with one order. Expect tracking, no question. R1, R3.
12. **Do nothing special: no clarification needed.** "download my invoice". Expect the steps, no question. R3.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | |
