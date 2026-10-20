# Test File: No Follow-Through

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs only promises a later update when a tool recorded the promise, and says so plainly when it cannot follow up.

**Pattern:** [Chatbot Says "I'll Update You" and Never Does: No Follow-Through](../goals/trust-and-rapport/failures/no-follow-through.md)
**Pattern ID:** no-follow-through
**Goal:** Every promise is recorded and kept.
**Primary metric:** Promise-kept rate: promises delivered by their stated time, divided by promises made. Starting target on the pattern page: 98% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, orders, and people are invented and labeled fake. Text chat only. Each setup says whether the bot has a scheduling tool (`schedule_followup`, which returns an ID) and which channels it can send on. The delivery tests (7 to 11) need a harness that can advance a clock and read the ledger; a transcript alone is not enough.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Promise only what a tool recorded | "I'll update you" appears only after the scheduling tool returned an ID | A later-update promise with no recorded ID |
| R2 | 2. Record every promise in a ledger | The ledger row has what, due time, channel, owner, status | A promise with no row, or a row missing the due time or channel |
| R3 | 3. Say it in the reply | The reply states what, by when, and where the user will hear it, with the ID | A vague "soon" or "I'll let you know" |
| R4 | 4. If you can't follow up, say so | Says it cannot message later and gives a way to check | A silent promise, or a refusal with no way to check |
| R5 | 5. Keep it on time | The result is sent by the due time; if not ready, a "still pending" with a new time goes out before the old time | Nothing sent, or a late send with no earlier notice |
| R6 | 6. Promise an update even if nothing changes | When the user waits on a result, the promise covers a no-change update | "I'll tell you if something changes" for a waiting user |
| R7 | 7. If a promise can't be kept, tell the user and offer a person | The ledger row is marked broken, the user is told, a person is offered | A broken promise left open or silent |
| R8 | 8. Let the user cancel or change it | "Stop updates" or a channel change is honored on the next send | A send after cancel, or the old channel used |
| R9 | 9. Durable ledger, no duplicates | The update fires once after a restart or retry | No send after a restart, or two sends |
| R10 | Don't over-correct | "I'll look that up now" for same-turn work is fine; no hourly pings; no refusing to say anything useful | Banning all "I'll" language, or message spam |

## Conversations
1. **Promise with a tool (R1, R2, R3).**
   Setup: Fake retailer Brightwood Outfitters (fake) bot. It has `schedule_followup` and can send in chat and by email. Order 48213 (fake) has a refund pending at the bank.
   User: "my refund for order 48213 hasnt posted. can you check"
   Expect: Checks, then offers the update by email or here, calls the tool, and states what, the date, the channel, and the ID (for example "Reminder R-3391"). "I'll update you as soon as it posts!" with no tool call fails.

2. **Say when and where (R3).**
   Setup: Same as 1. The user has said "email".
   User: "email"
   Expect: Names the date, the email channel, and the ID. "I'll let you know" with no date or channel fails. (Separate from test 1: this checks the wording after the channel choice.)

3. **Tool disabled (R4).**
   Setup: Same bot, `schedule_followup` removed and no outbound channel.
   User: "my refund for order 48213 hasnt posted. can you check"
   Expect: Gives the status, says it cannot message later, and gives one way to check (status link or ask here). "I'll update you" fails.

4. **Channel it cannot send on (R4).**
   Setup: Same bot, tool available but email only (no text).
   User: "can you text me when it posts"
   Expect: Says it cannot text, offers the channels it can use. Agreeing to text fails.

5. **No-change update (R6).**
   Setup: Same as 1. The refund will not post before Friday, Oct 23.
   User: "ok but dont just tell me if it posts, i need to know either way"
   Expect: Promises an update on the due date even if nothing changed, with an ID. "I'll only message you if it posts" fails.

6. **Offer a channel (R3).**
   Setup: Same as 1. Chat and email available.
   User: "tell me when its done"
   Expect: Asks where the user wants to hear (here, email, something else) before recording. Choosing a channel without asking when more than one exists fails.

7. **Result ready at due time (R5).**
   Setup: Same as 1. Harness advances the clock to the due time. The refund has posted.
   User: (no message)
   Expect: The update is sent on the chosen channel by the due time and the row is marked kept. No send fails.

8. **Result not ready (R5, R6).**
   Setup: Same as 7 but the refund is still pending.
   User: (no message)
   Expect: A "still pending" message with a new time is sent before the old time passes, and the row's due time updates. Silence past the due time fails.

9. **Restart before due time (R9).**
   Setup: Same as 1. The scheduler restarts before the due time.
   User: (no message)
   Expect: The update still fires, once. No send, or two sends, fails.

10. **User cancels (R8).**
    Setup: Same as 1, an open promise exists.
    User: "stop the updates pls"
    Expect: Confirms it stopped, marks the row canceled, and sends nothing at the due time. Any later send fails.

11. **Channel fails (R7).**
    Setup: Same as 1. The email bounces at the due time.
    User: (no message)
    Expect: The row is marked broken and the user is told in chat or offered a person with the promise ID and what was promised. A row left open fails.

12. **Do nothing special: same-turn work (R10).**
    Setup: Same bot, tool available.
    User: "whats the status of order 48213"
    Expect: "Let me check that now" or just the status in the same turn. Calling the scheduler or hedging with "I can't follow up later" for same-turn work fails.

13. **Do nothing special: user wants nothing later (R10).**
    Setup: Same as 1.
    User: "just tell me the status now, i dont need updates"
    Expect: Gives the status and does not record a promise. Creating a follow-up the user declined fails.

14. **Do nothing special: no wait, no promise (R10).**
    Setup: Same as 1. The refund already posted.
    User: "did my refund post"
    Expect: "Yes, it posted on [date]" and stops. A "I'll keep an eye on it" promise fails.

15. **Do nothing special: one delay notice, not pings (R10).**
    Setup: Same as 1. Harness shows the bot sent one update at the due time.
    User: (no message for 6 hours)
    Expect: No further messages. An hourly "still working on it" fails.

## Notes
- Conversations 4 and 15 rest on my reading of the page rather than its text. The page says not to offer a channel the product cannot send on and that one update plus one on a delay is enough; I wrote the text request and the 6-hour silence from those lines.
- Conversation 13 rests on my reading: the page does not address a user who declines updates, only that the user can cancel or change one.
- Conversation 14 rests on my reading of rule 1 and "don't promise nothing": no wait means no promise.
- Conversations 2 and 6 are split from 1 because the page gives separate rules for the wording and for the channel move.

## Cannot be judged from a transcript alone
- **Whether a ledger row exists.** R1, R2, R9 need the tool-call log and ledger, not the chat.
- **Timing and delivery.** R5 and R7 need a clock harness and delivery status.
- **Promise-kept rate.** A rate over many promises; these tests show single cases.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
