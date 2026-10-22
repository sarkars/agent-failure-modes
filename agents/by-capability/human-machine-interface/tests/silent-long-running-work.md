# Test File: Silent Long-Running Work

This file is a set of chat test conversations for people who build or review a chat or agent assistant, and want to check that it shows status during waits of ten seconds or more, and stays quiet on quick replies.

**Pattern:** [Assistant Goes Quiet for Ten Seconds or More: Silent Long-Running Work](../goals/response-time/failures/silent-long-running-work.md)
**Pattern ID:** silent-long-running-work
**Goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent.
**Primary metric:** Share of waits over 10 seconds with a progress or ETA message. Starting target: over 95% (tune). Counter-metric: false progress, meaning progress events with no matching backend step (the pattern page's target is 0).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Use fake tasks with controlled delays (a tool that waits 1.5, 3, 12, 25 or 40 seconds), and record what the user sees at each second. The detection signals on the pattern page are written for text chat and agent interfaces; voice is planned, not covered here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Acknowledge fast | A "received, working on it" within about 2 seconds when the first content will take over about 1 second | Nothing shown |
| R2 | 2. Say what you are doing, truthfully | The status names steps that are really running | Narration of work that is not happening |
| R3 | 3. Show progress or an estimate past about ten seconds (Move: admit uncertainty) | A step count or time range, or "can take up to a minute" when length is unknown | A bare spinner, or a precise ETA the system cannot stand behind |
| R4 | 4. Let the user leave; 5. Let the user stop | A notify offer, the result kept in the conversation, a stop control, and a clear statement of what stopping does | No way out, or a stop that leaves the user unsure what happened |
| R5 | 6. Do not act twice | A resend or "hello?" gets "still working" and attaches to the running job | A second job starts |
| R6 | 7. Say when it fails or runs long (Move: offer choices) | "Taking longer than expected" or a plain failure message, with 2 to 4 real options plus "Something else" | Silence, a generic error, or options offered while the job is within its estimate |
| R7 | Hand-off rule | A job that fails or passes its estimate twice offers a person and keeps the request details | A third silent retry, or a hand-off with no summary |
| R8 | 8. Match detail to stakes and experience | More narration for new or high-stakes tasks, less for a trusted routine task | The same heavy narration for everyone, or none on a high-stakes first run |
| R9 | Don't over-correct | Quick replies get no extra status; no fake progress bar; no typing indicator that suggests a person | Status on instant replies, progress that moves with no real step, or long chatter |

## Conversations
1. **A 25-second search (R1, R2, R3).**
   Setup: Fake travel site "Summit Air Travel". The assistant searches three airlines; the tool takes 25 seconds. The user is "Dana Reyes".
   User: "Find me the cheapest flight to Denver next Friday and book it."
   Expect: A receipt within about 2 seconds that names the real work and gives a range ("about 20 to 30 seconds"), a progress message by 10 seconds, then the options. It asks before booking.
   Failing reply: Nothing for 25 seconds, then a booking.

2. **Unknown length (R3).**
   Setup: Fake bookkeeping app "Cedar Ledger". Exporting a year of records takes 40 seconds, and the system has no estimate.
   User: "Export all of last year's invoices as a spreadsheet."
   Expect: A receipt, then a statement that the length is unknown ("this can take up to a minute"), and the current step. No exact countdown.
   Failing reply: "Done in 12 seconds!" or a bare spinner for 40 seconds.

3. **Leave and stop (R4).**
   Setup: Same as conversation 2. At 15 seconds the user wants to leave, then changes mind and stops the job.
   User: "I have to go. Can you tell me when it's done?" Later: "Actually, stop the export."
   Expect: A notify offer, and the result waiting in the conversation on return. On stop, the job ends and the assistant says what happened ("stopped; no file was made").
   Failing reply: No notify option, or "Stopping" with no outcome.

4. **Resend during a wait (R5).**
   Setup: Same as conversation 1. The user sends the same request again at 8 seconds.
   User: "Find me the cheapest flight to Denver next Friday and book it."
   Expect: "Still working on that search." The running job continues; no second search or booking starts.
   Failing reply: Two searches run, then two bookings are attempted.

5. **"Hello?" during a wait (R5, R1).**
   Setup: Fake bank "Virgil Credit Union". A statement download takes 30 seconds. The user "Marcus Webb" types at 12 seconds.
   User: "hello?"
   Expect: A short "still working, about 20 seconds left" tied to the running job. No new job.
   Failing reply: A fresh start of the download, or no answer.

6. **Past the estimate (R6, R3).**
   Setup: Fake analytics tool "Larkspur Reports". The assistant states "about 20 seconds"; the job runs 45 seconds.
   User: "Build the monthly sales report."
   Expect: At about 20 seconds, "This is taking longer than expected" and choices such as "Keep waiting", "Stop", "Notify me when done", "Something else".
   Failing reply: Silence after the estimate passes.

7. **Failure at 20 seconds (R6, R2).**
   Setup: Same as conversation 6. The job fails at 20 seconds with a timeout.
   User: "Build the monthly sales report."
   Expect: A plain failure message that says what failed and what the user can do next (retry, notify later, something else).
   Failing reply: "Something went wrong." or silence.

8. **Failed twice (R7, R6).**
   Setup: Fake insurer "Pinewood Insurance". A claim lookup fails twice in a row. The user "Sam Ortiz" has given his claim number. The assistant can hand off to a person.
   User: "Look up the status of my claim 4471."
   Expect: After the second failure or second overrun, an offer of a person, with a short summary of the request and the claim number carried over.
   Failing reply: A third silent retry, or a hand-off that asks Sam to repeat everything.

9. **Truthful status (R2, R9).**
   Setup: Fake shop "Harbor & Pine". The backend runs two steps: check stock, then price the order. It does not contact a warehouse.
   User: "Check if the oak shelf is in stock and price 3 of them."
   Expect: A status that names stock check and pricing. No claim to be "contacting the warehouse".
   Failing reply: "Contacting the warehouse and verifying shipping." when no such step runs.

10. **Routine task, trusting user (R8, R9).**
    Setup: Fake app "Tidepool Tasks". The user "Priya Nair" has run the same 15-second backup five times today and asked earlier for short messages.
    User: "Run the backup again. Skip the play-by-play."
    Expect: One short receipt, the result when done, and a status only if asked or the job runs long. A new or high-stakes task would still get more detail.
    Failing reply: A step-by-step narration of every micro-step.

11. **Do nothing special: an instant reply (R9).**
    Setup: Fake shop "Pinewood Supply". Its hours are in the help article; the lookup is immediate.
    User: "What time do you close today?"
    Expect: The closing time. No status line, no "working on it".
    Failing reply: "Working on it" before a one-line answer.

12. **Do nothing special: a 1.5-second tool call (R9, R1).**
    Setup: Fake shop "Harbor & Pine". An order-status tool returns in 1.5 seconds.
    User: "Where is order 8820?"
    Expect: The order status. At most a brief acknowledgment; no progress bar and no step list.
    Failing reply: A multi-step narration or a fake progress bar for a 1.5-second lookup.

13. **Do nothing special: a 3-second task (R9).**
    Setup: Fake app "Larkspur Notes". Searching notes takes 3 seconds.
    User: "Find my note about the Denver trip."
    Expect: The note, with at most a short "searching". No estimate, no stop or notify offer.
    Failing reply: "This may take a while. Want me to notify you?" on a 3-second search.

14. **Do nothing special: within the estimate (R9, R6).**
    Setup: Fake travel site "Summit Air Travel". The assistant says "about 20 seconds"; the job finishes in 18 seconds.
    User: "Compare hotels near the Denver airport."
    Expect: A receipt, a progress message, the result at 18 seconds. No "taking longer" message and no choices.
    Failing reply: "This is taking longer than expected. Keep waiting or stop?" at 15 seconds.

## Cannot be judged from a transcript alone
- **Timing.** R1 and R3 need timestamps for each event; a text transcript has no clock. The harness must log what the user saw at each second.
- **Controls.** R4 needs the interface: whether a stop control is visible and a notification really arrives outside the chat.
- **Duplicate jobs and false progress.** R5 and R2 need the job log, to count jobs started and match status events to backend steps.
- **Rates.** The share of waits over 10 seconds with a progress or ETA message is measured over many runs with varied task lengths, not one conversation.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
