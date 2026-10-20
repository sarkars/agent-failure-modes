# Test File: Chatbot Gives Steps and Never Checks They Were Understood (Instructions Without Comprehension Checks)

This file is a set of chat test conversations for people who build or review assistants that walk users through multi-step tasks and want to check whether theirs sends a few steps at a time and asks for the plan in the user's own words when a step can cost money, data, or a deadline.

**Pattern:** [Chatbot Gives Multi-Step Instructions and Never Checks They Were Understood: Instructions Without Comprehension Checks](../goals/conversation-frameworks/failures/instructions-without-comprehension-checks.md)
**Pattern ID:** instructions-without-comprehension-checks
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Comprehension-check rate: replies that give a multi-step instruction with a costly step and are followed by an open comprehension check. Starting point on the pattern page: over 80% (tune on your own data).
**Maturity:** Tests written; not yet run.

**Read this first.** The pattern page is flagged for care because teach-back comes from human health communication, and it found no study of teach-back on chatbots. This file is design guidance for testing a hypothesis, not clinical or medical advice, and every task below is an everyday account, phone, or device task. The tests check behavior against the page's rules. They say nothing about whether teach-back improves understanding or cuts errors for a chatbot.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, accounts, and people below are invented and labeled fake. Text chat only. Each setup tells the assistant which steps are costly and why. This needs a test harness (or a prompt) that supplies a per-task list of costly steps, as the page's guardrails assume ("a task config or a judge"). R8 also needs a harness that stores the check log. Without those, the assistant cannot pass R2 or R8 by design, which is the page's own cause, not a model flaw.

**Rule applied in every setup** (from the page's reference design): for a task with 3 or more steps where any step can cost money, lose data, or miss a deadline, send at most 3 steps, put the costly step first, and end with one open question asking for the plan in the user's words.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Chunk: at most 3 steps per reply, with the costly step in the first chunk | The reply has 3 or fewer steps, and the costly step is in it. The limit of 3 is the page's starting point, not a sourced number | A reply with 4 or more steps, or a first chunk that leaves the costly step for later |
| R2 | 2. Name the costly step and what goes wrong if it is missed or done out of order | The reply marks the costly step and states the consequence in plain words ("leaving both on can charge you twice"). Which step is costly comes from the setup, so this needs a harness. Judgment call on what counts as plain | The step is listed like any other, or the warning is generic ("be careful") |
| R3 | 3. Ask open, not closed | The reply ends with one question that needs the user's own words ("In your own words, what will you do first?"). Judgment call on borderline questions such as "Which step comes first?", which the page uses only as the lighter follow-up | The reply ends with "Does that make sense?", "Any questions?", "Got it?", or nothing |
| R4 | 4. Do not count "ok" as understood when the chunk has a costly step | After a bare acknowledgment, the bot asks one lighter check and sends no new steps yet | The bot sends the next chunk, or closes the task, on an "ok" |
| R5 | 5. Compare the reply with the steps: check order and the costly detail, not wording | The bot confirms a restatement that has the right order and the costly detail, even in casual words, and flags one that has either wrong. Judgment call on partial restatements | Grades wording, confirms a wrong order or a missing costly detail, or flags a correct plan as wrong |
| R6 | 6. On a gap, own it, re-explain differently, and ask once more | Says the miss was in the explanation, uses different words or offers a checklist, and asks once more. Judgment call on "different" | Repeats the same text, blames the user, or moves on without correcting |
| R7 | 7. For hands-on steps, ask for what the screen shows | Asks the user to say what the screen or status shows after the step before sending more | Assumes the step worked and sends the next chunk |
| R8 | 8. Log the check: chunk, costly step, restatement, pass or gap | The harness record holds those four items for the check. Needs a harness; a transcript cannot show it | No record, or a record missing the restatement or the result |
| R9 | Hand-off rule: after two misses on the same costly step, or when the user asks for a person, hand off with the log | Offers or makes the hand-off and passes the task, the chunks sent, and each restatement | Asks a third time, refuses the person, or hands off with no summary |
| R10 | Don't over-correct | No check on a low-stakes tip, none when the user already stated the plan correctly, and none after "I've done this before" | A quiz on a trivial tip, a second check after a correct plan, or a check after the user has said they know the task |

## Conversations
Every conversation is tagged **Pattern ID: instructions-without-comprehension-checks**. Fake businesses: Pinewood Credit Union (fake), Brightline Mobile (fake), Cedar Cloud Photos (fake), Wavelength Internet (fake).

1. **Four-step task, three steps sent (R1).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Pinewood Credit Union (fake) app. The full task has 4 steps: add the new card, turn on autopay with the new card, turn off autopay on the old card, confirm the first payment shows "Scheduled". Costly step: turning off the old autopay before the new one is scheduled can cause a missed payment or a double one before the 15th.
   User: "got a new debit card. how do i move my car loan autopay to it"
   Expect: The first reply has at most 3 steps and includes the costly step. Sending all 4 steps in one reply fails.

2. **Costly step comes first, not last (R1).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Cedar Cloud Photos (fake). Task: close an account in 5 steps. Step 4 (delete the account) permanently removes the photos, and step 2 (download the export) is what protects them. The costly point is deleting before the export finishes.
   User: "want to close my cedar cloud account whats the steps"
   Expect: The first chunk contains the export step and the warning that deleting first loses the photos. Sending steps 1 to 3 as filler and holding the warning for the second reply fails.

3. **Name the cost in plain words (R2).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Brightline Mobile (fake). Task: move a phone number to a new carrier, 4 steps. Costly step: cancelling the old plan before the transfer finishes can lose the number.
   User: "switching carriers and keeping my number. how"
   Expect: The reply flags the cancel step and says what goes wrong (the number can be lost if the old plan is cancelled first). A neutral line such as "then cancel your old plan" fails. "Be careful with this step" with no consequence fails.

4. **Open question, not "Does that make sense?" (R3).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Same as conversation 1.
   User: "ok so what do i do"
   Expect: The reply ends with one question asking for the plan in the user's words, such as "In your own words, what will you do first?". Ending with "Does that make sense?" or "Let me know if you have questions!" fails.

5. **"ok got it" is not understanding (R4).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Same as conversation 1. The bot sent steps 1 and 2 with the warning and the open question. The user has not restated anything.
   User: "ok got it"
   Expect: Asks one lighter check, such as "Quick check: which step comes first?", and holds the next steps. Replying "Great! Here is step 3" fails.

6. **Wrong order in the restatement (R5, R6).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Same as conversation 1. The bot asked for the plan in the user's words.
   User: "add the card then turn off the old one i guess"
   Expect: Flags that the order is off, says the explanation was unclear, and re-explains in different words (the old autopay goes off only after the new one shows "Scheduled"). Confirming the plan fails.

7. **Right order, missing costly detail (R5).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Brightline Mobile (fake), conversation 3 task. The bot asked for the plan in the user's words.
   User: "ill get the transfer code, give it to the new carrier, and cancel the old plan"
   Expect: Catches that the plan never says to wait for the transfer to finish before cancelling, and asks about that one detail. Passing the plan because the three steps are in order fails.

8. **Correct plan in casual words (R5).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Same as conversation 1. The bot asked for the plan in the user's words.
   User: "add the card first then set up autopay on it. old one stays on till it says scheduled"
   Expect: Confirms in a line and sends the next chunk, with no second check on the same costly step. Asking for the plan again, or saying it must use the exact words, fails.

9. **Re-explain, do not repeat (R6).**
   Pattern ID: instructions-without-comprehension-checks.
   Setup: Same as conversation 1. The user's first restatement was wrong (old autopay turned off first). The bot has told the user the explanation was unclear.
   User: "wait so which one do i turn off first"
   Expect: Answers in different words or as a short checklist, owns that its first explanation was unclear, and asks once more for the plan. Pasting the original list again fails. "As I said above" fails.

10. **Hands-on step: ask what the screen shows (R7).**
    Pattern ID: instructions-without-comprehension-checks.
    Setup: Pinewood Credit Union (fake) app, same task. The bot sent steps 1 and 2. The user says both are done. Step 2 should leave the new autopay showing "Scheduled", and the old one must stay on until then.
    User: "did the card and the autopay thing"
    Expect: Asks what the status shows after step 2 ("Tell me what the new autopay says now") before telling the user to turn off the old one. Replying "Great, now turn off the old autopay" fails.

11. **The check is logged (R8).**
    Pattern ID: instructions-without-comprehension-checks.
    Setup: Wavelength Internet (fake). Task: replace a router, 4 steps. Costly step: factory-resetting the old router before copying the saved settings loses the home network setup. The harness keeps a per-chat record. The bot asked for the plan and the user gave a wrong order.
    User: "reset the old one then copy the settings"
    Expect: In the harness record, one entry holds the chunk, the costly step (reset before copying), the user's restatement as typed, and the result "gap". Needs a harness. A transcript alone cannot show this, so a run without a record is not a pass.

12. **Two misses, offer a person (R9).**
    Pattern ID: instructions-without-comprehension-checks.
    Setup: Wavelength Internet (fake), conversation 11 task. The user got the order wrong once and the bot re-explained in different words. The harness shows misses: 1.
    User: "reset the old one first then copy the settings i think"
    Expect: Sees the second miss on the same costly step, offers a person, and passes the task, the chunks sent, and both restatements. A third re-explanation with no offer of a person fails. A hand-off with no summary fails.

13. **User asks for a person (R9).**
    Pattern ID: instructions-without-comprehension-checks.
    Setup: Brightline Mobile (fake), conversation 3 task. The bot sent the first chunk and asked for the plan.
    User: "this is confusing can i just talk to someone"
    Expect: Hands off with the task, the chunk sent, and where the user is, with no further check question first. Asking the user to restate the plan before handing off fails.

14. **Control: low-stakes tip, no check (R10).**
    Pattern ID: instructions-without-comprehension-checks.
    Setup: Cedar Cloud Photos (fake) app. No costly step. Task: turn on dark mode.
    User: "how do i turn on dark mode"
    Expect: Gives the steps ("Tap Settings, then Appearance, then Dark") and stops. No request to say the plan back. "In your own words, what will you do first?" fails.

15. **Control: user already stated the plan (R10).**
    Pattern ID: instructions-without-comprehension-checks.
    Setup: Pinewood Credit Union (fake) app, conversation 1 task, costly step flagged. The user opens with the plan.
    User: "i'm gonna add the new card, set up autopay on it, and only turn off the old one after it says scheduled. what's the first screen"
    Expect: Answers the screen question and moves on. The user has already stated the order and the costly detail, so no check is asked. Asking "In your own words, what will you do?" fails.

16. **Control: "I've done this before" ends the check (R10).**
    Pattern ID: instructions-without-comprehension-checks.
    Setup: Brightline Mobile (fake), conversation 3 task, costly step flagged. The bot sent the first chunk with the warning and the open question.
    User: "i've done this before, ive switched carriers like 3 times. just give me the rest"
    Expect: Sends the remaining steps without a further check. The costly warning stays in the first chunk. Asking again, or refusing to continue until the user restates, fails.

## Notes
- R1: the limit of 3 steps is the page's starting point, "not a sourced limit". A product that tunes it to 4 should change conversation 1 and R1 to match.
- R2: which step is costly comes from the setup. A bot with no per-task list cannot be expected to find it every time, which is why this line needs a harness.
- R3: what counts as an "open" question is a judgment call at the edge. The page uses "Which step comes first?" only as the lighter follow-up after an "ok", so conversation 5 allows it and conversation 4 does not.
- R5: judging a free-text restatement is a judgment call. The page lists this as a trade-off, since the check will sometimes pass a wrong plan or fail a right one. Conversations 6 to 8 cover a wrong order, a missing costly detail, and a correct plan in casual words, and the grading is on order and the costly detail only.
- R6: "different words" is a judgment call. A reordered copy of the same sentences should not count.
- R7: the "tell me what the status says" wording is the page's text version of show-me. No real status screens are tested.
- R10: the page also says to ask at most one check per costly step. Conversations 8 and 16 cover the two exits the page names (correct plan, "I've done this before"). Conversation 5 asks for a lighter check after "ok", which the page requires, so it is not counted as a second check.
- The page's rule on "after two misses, offer a person" is tested in conversation 12. The state example in the page (`misses: 1`) is what the harness supplies.
- I did not write a test for voice, since the page marks voice as planned.
- The metric on the page is a rate. This file does not measure it.

## Cannot be judged from a transcript alone
- **Which steps are costly.** The task config sits outside the transcript.
- **Whether the check log was stored.** R8 needs the harness record, and conversation 11 has no transcript-only pass.
- **Whether users understood.** A passing restatement shows the user could say the plan, not that they will do it correctly. Error rate at each step needs real traffic.
- **Whether teach-back helps for chatbots.** The page found no chatbot study. The only outcome data it opened are from a small human pilot, so these tests check behavior only.
- **Rate in real traffic.** The comprehension-check rate and the friction metric need real chats and a sampled review.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
