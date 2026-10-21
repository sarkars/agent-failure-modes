# Test File: Impatient Idle Nudges

This file is a set of chat test conversations for people who build or review chat assistants and want to check whether theirs asks "are you still there?" too soon, or closes a chat while the user is still working.

**Pattern:** ["Are You Still There?" Chatbot Nudges That Come Too Soon: Impatient Idle Nudges](../goals/response-time/failures/impatient-idle-nudges.md)
**Pattern ID:** impatient-idle-nudges
**Goal:** Nudges respect how long a person reasonably needs to reply.
**Primary metric:** Nudge-then-abandon rate (lower is better). Starting target on the pattern page: set from your own baseline.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, claims, accounts, and people below are invented and labeled fake. Text chat only. Each setup states the clock facts (minutes of silence, typing events, tool calls), because the pattern lives in the timer and the platform settings. Most items need the session event log or a person watching the widget; those are marked "Needs a person". Times given are the pattern page's starting points (3 minutes, 10 minutes, 20 seconds, ten extensions). If you use other settings, record the product's own setting.

The fake product used throughout: "Harbor Health Plan (fake)" claims chat. Tasks the bot finishes: look up a claim by claim number, send an explanation of benefits (EOB). Fake claim number: 5521-884-07.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. No nudge while the user is typing or the bot owes the next turn | No nudge while typing, uploading, or a tool call runs; each resets the clock. Needs a person | A nudge or close during typing, an upload, or bot work |
| R2 | 2. Start the clock only when the ball is in the user's court | The idle timer starts after the bot's last message is fully shown | The timer runs during bot work or streaming |
| R3 | 3. Say how long you will wait for an effort request | The bot states a wait (starting point 10 minutes) when it asks the user to find something | No stated wait on a request to find a document or number |
| R4 | 4. Long first-nudge delay | No nudge before 3 minutes on a simple prompt, and none before the stated wait after an effort request (starting points to tune) | A nudge earlier than either |
| R5 | 5. One nudge, not a chain | One nudge that gives time left and choices, then the close | A second nudge, or a nudge chain |
| R6 | 6. One reply extends it | "More time", any message, or a button resets the clock; works at least ten times; at least 20 seconds to answer the warning | Needs a second reply, stops after fewer than ten, or gives under 20 seconds to answer |
| R7 | 7. Close softly | On close, says progress is saved (only if true) and how to resume; the session can be reopened | Deletes the session, or says nothing about saved progress or resuming |
| R8 | 8. Neutral nudge text | States time left and options (More time, Save and come back later, Something else) | "Hello?", "I haven't heard from you", or no options |
| R9 | Don't over-correct: keep a cap, close softly | A cap tuned to stakes still exists, and the chat still closes softly | Sessions never time out, or the cap is turned off for sensitive data |
| R10 | Hand-off rule | A silent user mid-task with a deadline or money at stake is offered a callback, or the case is saved for a person | Ends the chat with no callback or saved case |

## Conversations
1. **Typing starts at 2 minutes (R1).**
   Setup: The bot asked "What is the claim number?" and 2 minutes have passed. The client reports typing events from minute 2 on, for 4 more minutes. Needs a person.
   User: (types slowly, no send yet)
   Expect: No nudge while typing continues. A nudge at minute 3 fails.
2. **Tool call runs 90 seconds (R1, R2).**
   Setup: The user sent "5521-884-07". The claim lookup takes 90 seconds.
   User: (silent)
   Expect: No idle timer during the work and no nudge. A nudge while the bot works fails.
3. **Upload in progress (R1).**
   Setup: The user is uploading a photo of the denial letter (fake); the upload takes 4 minutes on a slow connection. Needs a person.
   User: (silent while uploading)
   Expect: No nudge or close. A close at 3 minutes fails.
4. **Clock starts after the last message is shown (R2).**
   Setup: The bot's long answer streams for 40 seconds, then asks "Does that answer it?"
   User: (silent)
   Expect: Silence is counted from the end of the streamed answer. Counting from the first word fails.
5. **Effort request states the wait (R3).**
   Setup: The bot needs the claim number from a paper letter.
   User: "ok let me find it"
   Expect: The bot's request said how long it will wait (for example "Go find it. I'll keep this chat open for 10 minutes."). No stated wait fails.
6. **No nudge before the stated wait (R4, R3).**
   Setup: The bot said it would wait 10 minutes. Silence is 5 minutes.
   User: (silent)
   Expect: No nudge at minute 5. A nudge at minute 3 fails.
7. **Simple prompt, silence past 3 minutes (R4, R5).**
   Setup: The bot asked "Do you want the EOB sent to the email on file?" Silence is 3 minutes 10 seconds (starting point, tune).
   User: (silent)
   Expect: One nudge with choices. A nudge before 3 minutes fails.
8. **One nudge only (R5).**
   Setup: A nudge went out at minute 10 after an effort request. The user is still silent 2 minutes later, within the nudge window.
   User: (silent)
   Expect: No second nudge; the chat waits out the window and then closes softly. A second nudge fails.
9. **"More time" ten times (R6).**
   Setup: The user taps [More time] on ten nudges in a row, over a long afternoon (fake). Needs the event log.
   User: "more time" (x10)
   Expect: Each one resets the clock, with no new nudge until the same wait has passed. A refusal on the 6th fails.
10. **Warning gives time to answer (R6).**
    Setup: A nudge is shown. Needs a person.
    User: (replies 25 seconds after the nudge)
    Expect: The reply still counts. A close before 20 seconds, or a reply ignored, fails.
11. **Soft close and resume (R7).**
    Setup: No reply after the nudge window. Progress (claim lookup started) is saved. Needs a person.
    User: (returns 20 minutes later) "found it, 5521-884-07"
    Expect: At close the bot said what is saved and how to resume, and the reopened session picks up. A fresh start fails.
12. **Close does not claim a save that did not happen (R7).**
    Setup: The platform does not store progress for this flow.
    User: (silent until close)
    Expect: The close says how to start again and does not claim saved progress. "Your progress is saved" with nothing saved fails.
13. **Nudge wording (R8).**
    Setup: A nudge fires.
    User: (reads it)
    Expect: Time left plus [More time] [Save and come back later] [Something else]. "Hello?" or "I haven't heard from you, so I'm closing this chat." fails.
14. **Do nothing special: quick back-and-forth (R4, R9).**
    Setup: The user replies within 20 seconds to each of six turns.
    User: "claim 5521-884-07" / "yes email" / "thx"
    Expect: No nudge, no wait statement, no "take your time" line. Any nudge fails.
15. **Do nothing special: user ends the chat (R9).**
    Setup: The bot asked "Anything else?" The user wrote "no thanks, bye".
    User: (nothing more)
    Expect: A short close line. A nudge afterward fails.
16. **Do nothing special: user says wait (R1, R4).**
    Setup: The user wrote "one sec, my wife has the letter" then went silent for 6 minutes. The bot had stated a 10-minute wait.
    User: (silent)
    Expect: No nudge at minute 3 or 6; at 10 minutes, one nudge. An early nudge fails.
17. **Deadline claim, user goes silent (R10).**
    Setup: The user is reporting a fraud charge of $480 (fake) and went silent after the nudge; the fake card team has a callback line.
    User: (silent past the nudge window)
    Expect: A callback is offered or the case is saved for a person with a note. A plain close fails.
18. **Sensitive chat still has a cap (R9).**
    Setup: A signed-in session shows a fake member's claim history. The user walked away for 3 hours. Needs a person.
    User: (silent)
    Expect: The session closes softly at the product's own cap. A session open for 3 hours with claims on screen fails.

## Cannot be judged from a transcript alone
- **Timing and events (R1-R6).** Need the session event log: bot message time, typing and upload events, tool-call state, nudge count.
- **Resume behavior (R7).** Needs the session store.
- **Thresholds.** Only the pattern page's starting points are used (3 minutes, 10 minutes, 20 seconds, ten extensions). They are not researched values. Otherwise record the product's own setting.
- **Production rates.** These tests do not measure nudge-then-abandon rate. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
