# Test File: Silent Failure and Timeout

This file is a set of chat test conversations for people who build or review an assistant, and want to check that a timed-out request or a cut-off answer always ends in a visible state with a next step.

**Pattern:** [Chatbot Stops Mid-Answer or Never Replies: Silent Failure and Timeout](../goals/response-time/failures/silent-failure-and-timeout.md)
**Pattern ID:** silent-failure-and-timeout
**Goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent.
**Primary metric:** Silent-failure rate: requests that end with no reply, no error, and no marker that the answer is incomplete. Target: 0 (a starting point to tune, from the pattern page, not from a study).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Timeouts, silence, early stream closes and tool failures are simulated in the Setup line; the harness must supply them on demand (for example, a tool call that returns nothing after the harness's deadline). Dates, amounts and order numbers are made-up test values. Voice versions are planned for voice, not tested here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Put a deadline on every wait | A failure state replaces the wait at the deadline | A spinner or silence that never ends |
| R2 | 2. Complete only on a positive signal | A stream that closed without a finish signal is treated as incomplete | Partial text shown as a finished answer |
| R3 | 3. Show an incomplete state | "This answer was cut off" (or similar), and the partial text stays visible | Partial text removed, or shown with no label |
| R4 | 4. Name what happened, what is saved, what to do | Cause in plain words, whether the question is saved, one next step | A catch-all message, a code alone, or nothing |
| R5 | 5. Offer to continue | A cut-off answer gets "Continue" and "Start over" | Only a generic retry |
| R6 | 6. Do not act twice | A retry attaches to the original job; the action runs once | The action runs a second time |
| R7 | 7. Log every failure with its cause | Not judged from a transcript; see the list below | Not judged here |
| R8 | Hand-off rule | After two failures in a row, a person is offered and the saved question goes with it | No route to a person, or the user must retell the question |
| R9 | Don't over-correct | Normal replies get no marker, no error, no automatic retry loop | A false "cut off" label, an error on a slow reply that finishes, or a hand-off the user declined |

## Conversations
1. **The backend never answers (R1, R4).**
   Setup: Fake app "Tallow Books", an online bookstore with a help assistant. The model call returns no response and no error until after the harness's deadline.
   User: "Where is my order 3318?" (made-up)
   Expect: At the deadline the wait ends. The reply says the request took too long, that the question is saved, and gives one next step such as try again or be notified.
   Failing reply: Nothing. The spinner keeps going.

2. **The stream stops mid-sentence, then closes normally (R2, R3).**
   Setup: Tallow Books. The stream sends "Your return window is 30 days, and refunds go back to the original pay" (fixture text), then closes with the normal end marker but no finish reason.
   User: "What is the return policy?"
   Expect: The partial text stays on screen with a label that the answer was cut off.
   Failing reply: The partial text is shown with no label, as if it were the whole answer.

3. **The stream stops and the connection drops (R2, R3, R4).**
   Setup: Fake app "Fernwick Cloud", file storage. The stream sends half an answer, then the connection drops with no close event.
   User: "Explain how to share a folder with my team."
   Expect: Partial text kept and labeled as cut off. Says the question is saved and offers a next step.
   Failing reply: The text freezes and nothing else appears.

4. **A tool call fails (R4).**
   Setup: Fernwick Cloud. The "look up storage usage" tool returns an error code (test value E-5021) instead of data.
   User: "How much storage am I using?"
   Expect: Says in plain words that the lookup failed, that the question is saved, and offers one next step. A short reference code may appear after the message.
   Failing reply: "Something went wrong." Or the assistant states a usage figure it never got.

5. **The user resends after a timeout (R6).**
   Setup: Tallow Books. The user's earlier request "Cancel order 3318" started a cancel job. The reply timed out, but the job ran. The harness counts cancel actions.
   User: "hello? did that work? cancel order 3318"
   Expect: The assistant attaches to the original job, reports its status, and does not start a second cancel. The harness count stays at one.
   Failing reply: A second cancel runs, or the assistant says "Done" without checking the job.

6. **Continue after a cut-off answer (R5).**
   Setup: Fernwick Cloud. A numbered answer to "How do I restore a deleted file?" was cut off after step 2 and labeled. The user taps Continue.
   User: (taps) "Continue the answer"
   Expect: The answer resumes from step 3 using the earlier context. It does not restart or repeat steps 1 and 2.
   Failing reply: The whole answer is generated again from step 1, or the assistant says it has nothing to continue.

7. **Start over after a cut-off answer (R5).**
   Setup: Same as conversation 6. The user taps Start over.
   User: (taps) "Start over"
   Expect: The original question is run again cleanly, with no leftover partial text mixed in.
   Failing reply: The old partial text is glued to the front of the new answer, or the user must retype the question.

8. **Two failures in a row (R8, R4).**
   Setup: Tallow Books. The harness fails two requests of the same kind in a row (backend silence both times). The user's question is saved.
   User: "Why was I charged twice on order 3318?" (made-up), then, after the second failure, "ugh"
   Expect: After the second failure the assistant offers a person and passes the saved question along, so the user does not retell it.
   Failing reply: A third generic "Try again" with no route to a person.

9. **The user reloads after a failure (R3, R4).**
   Setup: Fernwick Cloud. A request failed with the question saved and partial text shown. The user reloads the page.
   User: (reloads, then types) "Is my question still there?"
   Expect: The saved question and any partial text are back on screen, and the assistant confirms what is saved.
   Failing reply: A blank chat, or "I don't have any earlier message."

10. **A failure outside staffed hours (R4, R8).**
    Setup: Tallow Books. A request fails twice. The support team is closed (a flag the harness sets), so no person is available.
    User: "I need this fixed today."
    Expect: Failure state, saved question, and a next step that does not need a person now, such as leaving a message or being notified. It does not promise a person who is not there.
    Failing reply: "Connecting you to an agent now," with no agent available.

11. **Do nothing special: a very short complete answer (R9).**
    Setup: Tallow Books. The stream sends "Yes." and then a proper finish reason.
    User: "Do you ship to Canada?"
    Expect: The short answer is shown as is. No cut-off label, no error.
    Failing reply: "This answer was cut off. Continue / Start over" on the one-word reply.

12. **Do nothing special: a slow reply that finishes before the deadline (R1, R9).**
    Setup: Fernwick Cloud. The harness delays the reply but finishes before the deadline, with a finish reason.
    User: "List my five largest folders."
    Expect: The answer arrives and is shown normally. No timeout message, no retry offer.
    Failing reply: "This is taking longer than we can wait," shown on a reply that then finishes.

13. **Do nothing special: a normal long answer with a finish signal (R2, R9).**
    Setup: Fernwick Cloud. The stream sends a long step-by-step answer ending in a full sentence, then a finish reason.
    User: "Walk me through setting up two-step sign-in."
    Expect: The full answer is shown with no marker. The assistant does not ask whether it was complete.
    Failing reply: A cut-off label on a complete answer, or an automatic retry that repeats the answer.

14. **Do nothing special: the user asks to stay with the bot after two failures (R8, R9).**
    Setup: Tallow Books. Two failures in a row, as in conversation 8.
    User: "Please don't send me to a person. Just try again."
    Expect: The assistant tries again once and respects the choice. It may mention a person is available later, without pushing.
    Failing reply: A forced hand-off, or a refusal to try again.

## Cannot be judged from a transcript alone
- **Whether the deadline fired on time.** R1 needs the harness clock and the request log, not only the chat text.
- **Whether a failure was logged with its cause (R7).** This needs the log of end reason, last event, and cause code for each request.
- **Whether a stream closed with a finish signal.** R2 needs the stream events, since the chat text can look the same either way.
- **How often silent failures happen in real use.** The rate is over many requests; one chat cannot show it.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
