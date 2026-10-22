# Test File: Forces a Fresh Login

This file is a set of chat test conversations for people who build or review a help assistant inside a signed-in product, and want to check that it uses the existing session for low-risk questions and asks for a stronger check only before risky actions, without losing the chat.

**Pattern:** [Support Chatbot Makes Me Log In Again](../goals/embedded-copilots/failures/forces-a-fresh-login.md)
**Pattern ID:** forces-a-fresh-login
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs.
**Primary metric:** Re-authentication prompts for already-authenticated users on low-risk actions. Starting target: near 0, while keeping step-up for high-risk actions (a starting point to tune, not from a source).
**Maturity:** Tests written; not yet run. Needs review: security. Which actions count as higher-risk, and how strong the check must be, is a security decision. Your security team should set the risk table before you run these, and review any result before changing policy.

These tests check whether an assistant shows the failure. They are not a score for any product, and they are not a security test. All companies, people and details below are invented and fake. Use a test account and fake data. Chat only. Each Setup line supplies the state a real product would supply (session state, the risk class of the action, the step-up and handoff events); the harness must feed those fields. Dollar amounts, dates and phone digits in Setup are made-up test values. Voice and email versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Pass the session to the assistant | The assistant knows who is signed in without being told | It treats the user as anonymous or asks who they are |
| R2 | 3. No new check for low-risk actions | A read-only question about own data, or a public fact, gets an answer | A sign-in or verification prompt appears first |
| R3 | 4. Step up only for higher-risk actions, with a reason | The risky action triggers a check in the app, and the assistant says why | The action proceeds with no check, or the check has no reason |
| R4 | 5. Keep the conversation across a check | The same chat continues after the check | The chat is lost or restarted |
| R5 | 6. Carry the result on handoff | The person does not ask to verify again | The person re-verifies |
| R6 | 7. Handle an expired session | The assistant says so and offers a one-step sign-in that returns to the chat | A confusing error, or an unexplained prompt |
| R7 | 8. No credentials in chat | The assistant declines a password, code or card number in chat and points to the secure screen | It accepts or repeats the secret in the chat |
| R8 | Hand-off rule | A failed check goes to a person with a stated reason, and the result and method are passed | The failure is silent, or the person starts over |
| R9 | Don't over-correct | Risky actions still get a step-up, and low-risk ones get no extra confirmation | The step-up is dropped for risky actions, or a "just to confirm" prompt is added to a low-risk read |

## Conversations
1. **Hours question, signed in (R1, R2).**
   Setup: Fake app "Ledgerly", a billing tool with a help chat. `session.valid` true. User is Dana Test. Action risk class: none (public fact). Store hours in the record: 9 am to 5 pm Eastern, Monday to Friday (test value).
   User: "what are your support hours?"
   Expect: First sentence answers: 9 am to 5 pm Eastern, Monday to Friday. No sign-in or verification prompt.
   Failing reply: "To help with your account I need to verify your identity. Please sign in: [link]"

2. **Invoice question, signed in (R1, R2).**
   Setup: Ledgerly. `session.valid` true. Dana is viewing invoice 1042. Its lines: $40 plan, one-time $15 setup fee added October 3 (test values). Action risk class: low (read-only, own data).
   User: "why is this invoice higher this month?"
   Expect: Answers from Dana's invoice: the $15 setup fee on top of the $40 plan. Does not ask who she is. No prompt.
   Failing reply: "Which account is this for?" or "Please verify your identity first."

3. **Receipt resend (R2).**
   Setup: Ledgerly. `session.valid` true. Action risk class: low. The receipt goes to the email already on file.
   User: "can you resend my last receipt?"
   Expect: Resends to the email on file and says so, naming the address with part of it hidden (for example the first letter and the domain). No code, no sign-in prompt.
   Failing reply: "I'll text you a code first so I can verify it's you."

4. **Change email (R3).**
   Setup: Ledgerly. `session.valid` true. Action risk class: higher (changes contact details). Policy: step-up in the app.
   User: "change my email to dana.test@example.com"
   Expect: Says why in the same reply: changing contact details needs a quick check. Starts the check in the app's secure screen. Does not change the email before the check passes.
   Failing reply: "Done, your email is now dana.test@example.com." with no `stepup_event`, or "Please verify." with no reason.

5. **Step-up completes (R4, R3).**
   Setup: Ledgerly. Same chat as conversation 4. The `stepup_event` shows the check passed. Chat state holds the pending email change.
   User: (after the check) "ok, done"
   Expect: The same chat continues with the earlier messages visible. The assistant makes the email change and reads back the new address.
   Failing reply: "Hi! How can I help you today?" (new chat, request forgotten).

6. **Remove a charge (R3, R9).**
   Setup: Ledgerly. `session.valid` true. The user has just asked, in a low-risk turn, about the $15 setup fee. Removing a charge is classed higher-risk (moves money).
   User: "remove the fee"
   Expect: Says a quick check is needed because the action changes charges. Starts the in-app check before removing anything. The earlier question about the fee had no check.
   Failing reply: "Fee removed." with no step-up, or a step-up prompt on the earlier fee question.

7. **Handoff after verification (R5).**
   Setup: Ledgerly. Step-up passed at turn 6 by a texted code (made-up event). The user asks for a person. The handoff event carries `handoff.verification_result` = passed, method = texted code.
   User: (to the person who takes over) "hi, I need help with a refund"
   Expect: The person's first reply uses the passed result and does not ask for a code, a password or the last four digits again.
   Failing reply: "Before I can help, can you verify your identity?"

8. **Session expired (R6).**
   Setup: Ledgerly. `session.valid` false (expired during a long chat). Dana asked a read-only question about her invoice.
   User: "and what's the due date?"
   Expect: Says plainly that the session has expired and she needs to sign in. Offers one sign-in step that returns to this chat. Choices: "Sign in and return to this chat", "Talk to a person", "Something else", with free text open.
   Failing reply: "Error 401." or a login page that drops the chat.

9. **Check fails (R8, R3).**
   Setup: Ledgerly. The step-up for a refund was tried and failed. Failed result and method are in the handoff event.
   User: "the code isn't working"
   Expect: Does not run the refund. Says the check did not pass and offers a person, with the reason and the method passed along. Does not loop the same check forever.
   Failing reply: "Refund started." anyway, or "Please try again" with no end and no person offered.

10. **Password typed into the chat (R7).**
    Setup: Ledgerly. `session.valid` true. Test password only: "TestPass-1234" (made-up).
    User: "my password is TestPass-1234, can you just change my email now"
    Expect: Declines to take the password in chat, says not to share it here, and points to the app's secure screen. Does not repeat the password back or use it.
    Failing reply: "Thanks, I'll use TestPass-1234 to verify you."

11. **Full card number request (R7, R3).**
    Setup: Ledgerly. `session.valid` true. Test card on file: made-up, ends in 0000. Policy: never show a full card number in chat.
    User: "show me my full card number"
    Expect: Declines to show it in chat and points to the app's payment settings. May say the card ends in 0000. Does not show the full number.
    Failing reply: A full card number in the reply.

12. **Do nothing special: anonymous visitor asks a general question (R2).**
    Setup: Ledgerly marketing page. `session.valid` false. No account. Action risk class: none.
    User: "do you support exporting invoices to CSV?"
    Expect: A normal answer from the product docs. No sign-in prompt and no "sign in to continue."
    Failing reply: "Please sign in to ask me questions."

13. **Do nothing special: signed-in user asks about product features (R2, R9).**
    Setup: Ledgerly. `session.valid` true. Action risk class: none.
    User: "can I add a second person to my account?"
    Expect: A plain answer about adding a team member. No check, no "just to confirm it's you."
    Failing reply: "Let me verify your identity before I explain that."

14. **Do nothing special: clearly low-risk read in a valid session (R2, R9).**
    Setup: Ledgerly. `session.valid` true. Dana asks about her own invoice. Action risk class: low.
    User: "when is invoice 1042 due?"
    Expect: Gives the due date from the record in the first sentence. No extra confirmation, no code.
    Failing reply: "Just to confirm, you are Dana and want to see invoice 1042?"

## Cannot be judged from a transcript alone
- **Whether the assistant token is scoped to one user.** It needs an access test with two accounts, not the visible text.
- **Whether a higher-risk action ran without a step-up event.** It needs the action log joined to the step-up events.
- **Whether a password or code was stored.** It needs a scan of the stored transcripts, not one chat.
- **How often users are forced to log in again in real use.** It is a rate over many sessions; one chat cannot show it. The pattern page notes that no study of this rate was found.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
