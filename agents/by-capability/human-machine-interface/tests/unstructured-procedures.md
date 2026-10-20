# Test File: Unstructured Procedures

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs answers a how-to question in running prose instead of numbered steps.

**Pattern:** [Unstructured Procedures: How-To Answers That Are Hard to Follow](../goals/response-structure/failures/unstructured-procedures.md)
**Pattern ID:** unstructured-procedures
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Procedure replies using numbered steps. Target on the pattern page: 100% (tune), paired with the user step-error rate.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, apps, accounts, and people are invented (fake). Text chat only. The 5-7 step limit in R8 is the page's practical starting point to tune, not a sourced figure.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Detect a procedure | A request with more than one action gets a list; a single-action answer is one sentence | A multi-action how-to answered in prose, or a one-action answer turned into a list |
| R2 | 2. Number the steps | 1, 2, 3 on separate lines; a, b, c only under a step with real sub-steps | Steps in a paragraph, or bullets with no numbers |
| R3 | 3. One action per step | Each step has one action (exception: actions that cannot be separated, such as holding a key while clicking) | A step with two actions joined by "and" or "then" |
| R4 | 4. Start each step with the verb | "Tap Download" | "You should then tap Download" |
| R5 | 5. Conditions before the action they govern | "If you use the web version, ..." comes before the step it affects | The condition trails the step |
| R6 | 6. Prerequisites before step 1 | What to have or turn on sits above the list | The prerequisite appears inside or after the steps |
| R7 | 7. Name what the user will see when it helps | A check line such as "A banner says Download started" where useful | No way for the user to tell the step worked, where one would help |
| R8 | 8. Keep the list short | For a long task, the first 5-7 steps, the total step count, and an offer of the rest | A very long list sent whole, or the total is missing |
| R9 | 9. End with one way to continue | One line such as "Tell me which step you're on" | No continuation, or a second question added |
| R10 | Move: ask when the steps differ and the session does not say which | One question or a few choices ("Windows", "Mac", "Phone", "Something else") before the steps | A guess at the platform, or both platforms' steps merged |
| R11 | Don't over-correct | No numbering on an explanation, a comparison, or a single action; no single action split into five steps; numbering kept when a task has more than two actions even if short | A list where none is called for, or prose for a short three-action task |

## Conversations
1. **Basic multi-action how-to (R1, R2).**
   Setup: Fake payroll app Paywise (fake). Resetting a password: open Sign in, tap Forgot password, enter the email, tap the emailed link, set a new password.
   User: "how do i reset my password"
   Expect: A numbered list, one action per line. A paragraph fails.

2. **Prerequisite above the list (R6).**
   Setup: Same app. Downloading a W-2 needs paperless delivery turned on in Settings first. Steps: sign in, open Documents, tap Tax Forms, select the year, tap Download.
   User: "How do I download my W-2?"
   Expect: The paperless prerequisite appears above step 1. A prerequisite stated last, or inside a step, fails.

3. **Single action is one sentence (R1, R11).**
   Setup: Same app. The Settings menu is the gear icon at top right.
   User: "where is the settings menu"
   Expect: One sentence. A one-item numbered list fails.

4. **Platform unknown (R10).**
   Setup: Same app. Steps differ on Windows and Mac. The session has no platform recorded.
   User: "how do i install the desktop app"
   Expect: One question or a choice set (Windows, Mac, Something else) before any steps. Steps for both merged into one list fail.

5. **Long task (R8).**
   Setup: Same app. Migrating records to a new account takes 14 steps.
   User: "how do i move everything to my new account"
   Expect: The first 5-7 steps, the total (14) stated, and an offer of the rest. All 14 sent whole fails.

6. **Two actions in one step (R3).**
   Setup: Same app. Updating a mailing address: open Profile, tap Edit, change the address, tap Save.
   User: "how do i change my mailing address"
   Expect: "Change the address" and "Tap Save" on separate lines. A step reading "Change the address and tap Save" fails.

7. **Verb first (R4).**
   Setup: Same app. Muting a chat: open the chat, tap its name, turn on Mute.
   User: "how can i mute a chat"
   Expect: Each step begins with a verb ("Open", "Tap", "Turn on"). "You should then tap the name" fails.

8. **Condition before the step (R5).**
   Setup: Same app. If a banner says "Verify email", it must be tapped before the Documents tab opens. The session says the user is on the web version.
   User: "how do i open my pay stubs"
   Expect: The condition ("If a banner says Verify email, tap it first") comes before the step it governs. The condition placed after the step fails.

9. **Say what the user will see (R7).**
   Setup: Same app. Tapping Download shows a banner "Download started" and the file appears in Downloads.
   User: "how do i download my pay stub"
   Expect: The steps include a check ("A banner says Download started"). Steps with no way to tell it worked fail.

10. **One way to continue (R9).**
    Setup: Same app. Any multi-step task.
    User: "how do i add my bank account"
    Expect: Ends with one line such as "Tell me which step you're on." Ending with two or more questions fails.

11. **Do nothing special: an explanation (R11).**
    Setup: Same app. Pay is higher this month because of a one-time bonus (fake).
    User: "why is my paycheck higher this month"
    Expect: A short explanation in sentences. A numbered list fails.

12. **Do nothing special: a comparison (R11).**
    Setup: Same app. Two fake plans, Basic and Plus.
    User: "whats the difference between basic and plus"
    Expect: A comparison in short paragraphs or a table. Numbered steps fail.

13. **Do nothing special: platform already known (R10, R11).**
    Setup: Same app. The session records that the user is on a Mac.
    User: "how do i install the desktop app"
    Expect: The Mac steps, numbered, right away. Asking "Windows or Mac?" fails.

14. **Do nothing special: unsplittable actions (R3, R11).**
    Setup: Same app. Force-restarting the desktop app: hold Shift and click Restart.
    User: "how do i force restart the app"
    Expect: "Hold Shift and click Restart" may stay as one step. Splitting it into two separate steps fails, because the key must stay held while clicking.

15. **Do nothing special: short three-action task (R1, R11).**
    Setup: Same app. Turning on alerts: open Settings, tap Alerts, turn on Pay alerts.
    User: "turn on pay alerts how"
    Expect: Still a numbered list of three. Squeezing it into prose to save space fails.

16. **Do nothing special: sub-steps only when real (R2, R11).**
    Setup: Same app. Step 3 of turning on two-step sign-in has a real choice: (a) an authenticator app or (b) text messages, each with its own actions.
    User: "how do i turn on two step sign in"
    Expect: Sub-steps a, b appear only under the step that has them. Lettering every step fails.

## Cannot be judged from a transcript alone
- **Step-error rate.** The paired metric needs a person to label, in real logs, whether the user's next message reports a wrong or skipped step.
- **Correct order.** A reviewer must know the true step order for each setup.
- **"Real sub-steps" and "cannot be separated."** A reviewer decides, per setup.
- **The 5-7 step limit.** The page calls it a starting point to tune; record yours.

## Rules without a scenario yet
None. Rules 1 to 9 of the fix each have at least one conversation. R10 comes from the page's Moves table and test 4; R11 is the page's "Don't over-correct" paragraph.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
