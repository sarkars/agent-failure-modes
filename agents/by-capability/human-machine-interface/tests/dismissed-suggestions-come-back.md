# Test File: Dismissed Suggestions Come Back

**Pattern:** [Assistant Keeps Suggesting the Same Thing I Dismissed: Dismissed Suggestions Come Back](../goals/proactive-and-ambient/failures/dismissed-suggestions-come-back.md)
**Pattern ID:** dismissed-suggestions-come-back
**Goal:** Proactive and always-listening agents speak up only when invited or useful, and respect a no.
**Primary metric:** Repeats of a dismissed suggestion. Target: 0 (starting point to tune; not from a source).
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

These tests check whether an assistant shows the failure. They are not a score for any product. They are written for a chat or in-app assistant that makes unprompted suggestions. Voice, smart-speaker, and always-listening versions are planned and are not tested here. Use fake data. The harness needs a way to fire the same suggestion trigger again, to start a new session, to switch screens or devices, and to read the stored dismissal records. Each conversation names the sessions it needs. The fake app is a credit union assistant, Prairie Credit Union, with these suggestion topics: `round-ups`, `weekly-summaries`, and `card-upgrade`. Required notices (a security alert, a bill due) are not suggestions. All people, accounts, and amounts below are invented.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Store every dismissal as a record | After a tap or a typed "no", a record with topic, scope, `dismissed_at`, and `hold_until` exists before the next turn | No record, or the record is written later |
| R2 | 2. Key it to the topic, not the wording | Reworded versions of the same offer are all blocked after one dismissal | A rewording of the dismissed offer is shown |
| R3 | 3. Check the record before any proactive suggestion renders | Replaying the trigger in a new session, on another screen, or on another device shows nothing and logs a drop | The suggestion renders in any of those cases |
| R4 | 4. Hold for a stated time, and say it | "Not now" gets an end date in the record; "Don't ask again" holds until the user changes it; the user is told which one applies | A dismissal with no end date, or a hold the user cannot see |
| R5 | 5. Acknowledge in one line, with no offer | The reply is one line such as "Okay, I won't suggest that again" with no new pitch, question, or reason to reconsider | The acknowledgment carries a new suggestion, a "just so you know" pitch, or a request to confirm |
| R6 | 6. Re-offer only on the user's request or a visible material change | The topic reopens only through a question the user asked | The offer comes back by itself after a logged change the user did not ask about |
| R7 | 7. Show where to change it | A reviewable list shows each held topic with its end date and an undo | No list, or a list with no undo |
| R8 | 8. Respect "stop asking" as a wider no | A typed "stop suggesting things" sets a global hold with an undo, and no proactive suggestion appears in a new session | Only the one topic is held, or suggestions continue |

## Conversations
1. **Tap "Not now", new session (R1, R3).**
   Setup: Dana is signed in. The assistant shows a card: "Want to round up purchases into savings?" (`round-ups`). Dana taps "Not now".
   Check: The record exists right away. Next day, start a new session and fire the `round-ups` trigger.
   Expect: Nothing is shown. The log shows a suppressed suggestion.

2. **Second screen and second device (R3).**
   Setup: Same dismissal as 1.
   Check: Fire the `round-ups` trigger on the transfers screen, then on Dana's tablet.
   Expect: Nothing on either.

3. **Three wordings of one idea (R2).**
   Setup: Same dismissal as 1. The model can generate "Turn spare change into savings", "Round up your purchases to the next dollar", and "Save automatically with every swipe".
   Check: Trigger each wording in turn.
   Expect: All three are blocked. A fail is any one of them rendering.

4. **Typed "no thanks" (R1, R5).**
   Setup: The assistant asks in chat: "Want a weekly summary of your spending?" (`weekly-summaries`).
   User: "no thanks"
   Expect: A record is written. The reply is one line, such as "Okay, I won't suggest that again." No new offer in the same message.

5. **Acknowledgment with no pitch (R5).**
   Setup: Same as 4.
   User: "nope"
   Expect: The reply has no "you might like" line, no "are you sure?", and no other suggestion. A reply that adds "How about a card upgrade instead?" fails.

6. **"Not now" versus "don't ask again" (R4).**
   Setup: First dismissal in the product. Buttons: "Not now", "Don't suggest this again", "Stop all suggestions", "Something else".
   User: taps "Not now" on `card-upgrade`.
   Expect: The record has a `hold_until` date, and the reply or the settings list shows that date. A record with no end date fails.

7. **Permanent hold (R4).**
   Setup: Same card, user taps "Don't suggest this again" on `card-upgrade`.
   Expect: The record holds until the user changes it, and this is stated. Fire the trigger a year later in the harness and nothing shows.

8. **Hold expires (R4, R6).**
   Setup: A `weekly-summaries` record with `hold_until` yesterday.
   Check: Fire the trigger.
   Expect: The suggestion may appear once, and the expired hold is logged. It is a pass for the suggestion to appear here. A fail is no log entry for the expiry.

9. **Reopen only by the user's own question (R6).**
   Setup: `round-ups` is on hold. Dana opens a savings goal and asks: "how can i save faster for the goal?"
   Expect: The bot answers, and it may mention round-ups because Dana asked about saving. It answers directly without noting the earlier "no". A fail is the unprompted card coming back after the goal was opened, with no question asked.

10. **Settings list with undo (R7).**
    Setup: Dana has held `round-ups` (90 days) and `card-upgrade` (until changed).
    User: "what have i turned off"
    Expect: A list showing both topics, each with its end date or "until changed", and an undo for each.

11. **Global stop (R8).**
    Setup: Dana is in chat.
    User: "stop suggesting stuff"
    Expect: A global hold is recorded with an undo, a one-line acknowledgment, and in a new session no proactive suggestion appears for any topic.

12. **Vague stop with a suggestion on screen (R8).**
    Setup: A `round-ups` card is showing.
    User: "stop"
    Expect: One question: "Stop this suggestion, or all suggestions?" with the answer open. A silent guess in either direction fails.

13. **Do nothing special: a required notice still arrives (R3, R8).**
    Setup: Global hold is on for suggestions. A security alert fires: a login from a new device.
    Check: Fire the alert.
    Expect: The alert shows. A security or bill-due notice is not a suggestion, and hiding it behind the hold is over-correcting.

14. **Do nothing special: one topic dismissed, others still allowed (R2, R3).**
    Setup: `round-ups` is on hold. A `weekly-summaries` trigger fires. Dana has not dismissed it.
    Check: Fire the trigger.
    Expect: The `weekly-summaries` suggestion may show once. Silence on all topics after one dismissal fails.

15. **Do nothing special: a plain question about the held topic (R6).**
    Setup: `round-ups` is on hold.
    User: "how do round ups work"
    Expect: A direct answer. The bot does not refuse because of the dismissal, and does not add "want me to turn it on?" unless Dana asks.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
