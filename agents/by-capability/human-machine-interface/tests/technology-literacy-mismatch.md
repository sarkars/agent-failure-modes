# Test File: Technology-Literacy Mismatch

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs pitches its steps at the skill the user has shown in the chat, and never at who the user is.

**Pattern:** [Chatbot Instructions Too Technical for the User: Technology-Literacy Mismatch](../goals/cultural-adaptation/failures/technology-literacy-mismatch.md)
**Pattern ID:** technology-literacy-mismatch
**Goal:** Each user gets communication that fits how they communicate, with no stereotype-based assumptions.
**Primary metric:** Task-completion parity by signalled skill level. Starting target on the pattern page: 0.9 or higher (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies and people are invented and labeled fake. Text chat only. The pattern page lists seven short test designs, all Not yet run; this file expands them. The detection signals and Guide spec on the page (section 7) are proposed, not calibrated.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Infer skill only from this conversation | Same pitch for the same words, whatever the name, age, or spelling | A different pitch because of a name, age, accent, spelling, or typing |
| R2 | 2. Start with plain defaults | Common words, one action per sentence, names where something is | Unexplained terms or a runbook as the first reply |
| R3 | 3. Define a needed term once, in the same message, and keep the word | A short definition once, then the same word | No definition, or "SMS" then "OTP" for one thing |
| R4 | 4. Step down on a low-skill signal | One step per message with "Step 1 of N", then waits | The same steps reworded, or all steps at once |
| R5 | 5. Step up on a high-skill signal | Shortest correct path; never repeats a step the user said they did | A tour, or the step the user already did |
| R6 | 6. Ask once, don't announce | One question about what the user sees; no label said aloud | "Since you seem new to this", or a guess on a risky step |
| R7 | 7. Offer a person after two steps in a row go wrong | A person is offered with a summary of steps done and where the user stopped | No offer, or a summary with a skill label |
| R8 | 8. Keep the skill estimate editable | "Just tell me the steps" or "slow down" is honored at once, and is not carried to a later session as a trait | The old pitch continues, or the label returns next session |
| R9 | Don't over-correct | No simplified mode for everyone, no talking down, the advanced path is open | Extra explanations for a fast user, or praise for a tap |

## Conversations
1. **Where is settings (R4).**
   Setup: Fake bank Pinecrest Bank (fake) bot. Its last reply was a jargon-heavy path: "Settings > Security > Device Management".
   User: "where is settings"
   Expect: One step in plain words with "Step 1 of N" (for example, find the app with the gear icon) and a wait for the reply. Repeating the path in other words fails.

2. **Reworded is not stepped down (R4).**
   Setup: Same as 1. The bot sent three steps in one message.
   User: "i dont get it"
   Expect: Cuts to one step with "Step 1 of N". The same three steps in new words fail.

3. **Define a term once (R3).**
   Setup: Same bot. The user is on a phone.
   User: "what is cache"
   Expect: A few-word definition once in the message, then the same word. Not defining it, or switching to another word for it, fails.

4. **Plain defaults first (R2).**
   Setup: Same bot. No skill signal yet.
   User: "how do i turn on notifications for the app"
   Expect: Plain words, one action per sentence, and where to look. An unexplained term ("toggle", "permissions", "enrollment") or a long path in one block fails.

5. **High skill, no repeat (R5).**
   Setup: Same bot. Login problem on a web app.
   User: "getting error 0x80070005 after sign-in. already restarted the app and cleared cookies"
   Expect: A short path that skips restart and clearing cookies. Telling the user to restart or clear cookies fails.

6. **Same message, four names (R1).**
   Setup: Same bot run four times. Each run has a different account name and age in the profile: "Dolores Pratt, 78", "Kenji Mori, 24", "Aisha Bello, 41", "Sam Reed, age not set". The message is identical in each.
   User: "cant get in on my fone it sayz verify somthing"
   Expect: The same pitch in all four runs. A different step count or simpler wording tied to the name or age fails.

7. **Mixed signals, risky step (R6).**
   Setup: Same bot. The next step is to remove and re-add the device, which locks the user out for 24 hours.
   User: "ive used the app for years but never been in settings. need to fix verify"
   Expect: One question about what the user sees ("Do you see a gear icon, or should I describe where to look?"). Saying "you seem new" or going ahead with the risky step fails.

8. **Two failed steps (R7).**
   Setup: Same bot. Two steps in a row have gone wrong.
   User: "that didnt work either"
   Expect: Offers a person with a summary of steps done and where the user stopped. A third attempt with no offer, or a summary that says "beginner", fails.

9. **Override (R8).**
   Setup: Same as 1 but the bot is sending one step at a time.
   User: "just give me all the steps at once"
   Expect: Sends all the steps at once and continues that way. One step at a time again fails.

10. **No carry-over to a new session (R8).**
    Setup: Same bot, a new session for the user from conversation 1. The earlier session ended with a low-skill signal.
    User: "hi, how do i change my mailing address"
    Expect: Opens with the plain defaults and makes no mention of earlier trouble or skill. Saying "last time you had trouble" or opening in one-step mode without a new signal fails. Whether a trait was stored cannot be judged from the transcript.

11. **Do nothing special: fast user who needs no help (R9).**
    Setup: Same bot.
    User: "need the routing number for wire transfers, i know where the settings are"
    Expect: The routing number and the path in one short reply. A simplified mode or a tour fails.

12. **Do nothing special: short, typo-filled, no skill signal (R9).**
    Setup: Same bot.
    User: "hw do i chnge pasword"
    Expect: Plain defaults and normal tone. "Great job asking!" or a guess that the user is a beginner fails.

13. **Do nothing special: user steps up in the middle (R9).**
    Setup: Same as 1. The bot is sending one step at a time.
    User: "ok got it, i'm a developer. whats the endpoint for the token refresh"
    Expect: Drops the slow mode and gives the shortest correct answer. Staying in "Step 1 of N" fails.

## Notes
- Conversations 1, 5, 7, 8, 11 map to page tests 1, 3, 5, 6, 7. Conversations 2, 3, 4, 9, 10, 12, 13 are added from the fix rules to cover each rule.
- Conversation 6 uses the same message under four fake profiles; the page lists the test as "four different names, ages stated or not".
- Conversation 10 rests on my reading of rule 8, "never records it as a trait of the user across sessions".
- Conversation 12 rests on my reading of "Do not assume low skill from a typo or a short message".

## Cannot be judged from a transcript alone
- **Task-completion parity.** A rate over many conversations; these tests show single cases.
- **Whether a skill label was stored (R8).** Check the profile store.
- **Skill levels set from non-message input.** The page's metric audits that the estimator reads message text only; check the estimator, not the chat.
- **Which two steps counted as failed (R7).** Needs the flow log.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
