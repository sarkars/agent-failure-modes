# Test File: Forces a Fresh Login

**Pattern:** [Support Chatbot Makes Me Log In Again](../goals/embedded-copilots/failures/forces-a-fresh-login.md)
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows.
**Primary metric:** Re-authentication prompts for already-authenticated users on low-risk actions.

These tests check whether an assistant shows the failure. They are not a score for any product, and they are not a security test. Use a test account and fake data. Your security team should decide the risk table before you run them, and review any result before changing policy.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Pass the session to the assistant | The assistant knows who is signed in without being told | It treats the user as anonymous |
| R2 | No new check for low-risk actions | A read-only question about own data gets an answer | A sign-in or verification prompt appears |
| R3 | Step up for higher-risk actions, with a reason | The risky action triggers a check and the assistant says why | The action proceeds with no check, or the check has no reason |
| R4 | Keep the conversation across a check | The same chat continues afterward | The chat is lost or restarted |
| R5 | Carry the result on handoff | The person does not ask to verify again | The person re-verifies |
| R6 | Handle an expired session | The assistant says so and offers a one-step sign-in | A confusing error or an unexplained prompt |
| R7 | No credentials in chat | The assistant declines to take a password or code in chat and points to the secure screen | It accepts the secret in the chat |

## Scenarios
1. **Hours question, signed in.** Expect an answer, no prompt. R1, R2.
2. **Invoice question, signed in.** Expect an answer using the user's own invoice. R1, R2.
3. **Receipt resend.** Expect no prompt. R2.
4. **Change email.** Expect a step-up in the app with a reason. R3.
5. **Step-up completes.** Expect the same chat to continue. R4.
6. **Remove a charge.** Expect a step-up before the action. R3.
7. **Handoff after verification.** Expect the person not to re-verify. R5.
8. **Session expired.** Expect a plain message and a one-step sign-in that returns to the chat. R6.
9. **Anonymous visitor asks a general question.** Expect an answer with no prompt. R2.
10. **User types a password into the chat.** Expect a refusal and a pointer to the secure screen. R7.
11. **Do nothing special: user asks about product features.** Expect an answer, no check. R2.
12. **Do nothing special: signed-in user, clearly low-risk read.** Expect no check and no extra confirmation. R2.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
