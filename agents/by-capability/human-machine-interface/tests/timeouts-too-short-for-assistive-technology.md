# Test File: Timeouts Too Short for Assistive Technology

**Pattern:** [Chatbot Timed Out Before I Could Finish Typing: Timeouts Too Short for Assistive Technology](../goals/accessibility/failures/timeouts-too-short-for-assistive-technology.md)
**Pattern ID:** timeouts-too-short-for-assistive-technology
**Goal:** People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. (Family goal, from the pattern page.)
**Primary metric:** Timeouts hit by assistive-technology users, compared with others: the timeout rate for sessions with a declared extended-time need divided by the rate for all other sessions. Starting target: 1.0 or lower (tune).
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

> **Read this first.** These are design checks for your own product. They are not legal, clinical, or professional advice and make no conformance claim.

These tests check whether a chat shows the failure. They are not a score for any product. Run them in a text-chat widget with a real screen reader and a real switch or voice-control setup where you can, and set the harness clock so the idle limit is 5 minutes (the page's example). The 2-minute warning is the page's starting point (tune). Voice-call timeouts are PLANNED and not covered. All pharmacies, customers, and prescription numbers are invented (Lakeview Pharmacy).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. State the rule early | In the first reply that waits on the user, the bot says the chat stays open while they type and that a warning comes before it closes | The statement appears after the first idle period can end, or never |
| R2 | 2. Count input in progress as activity | A draft changing every few minutes, a focused input, or a switch or dictation step resets the idle clock | A session with a changing draft expires |
| R3 | 3. Warn in text, with time left | A transcript message with at least 2 minutes left, announced to screen readers, with buttons a keyboard user can reach | A warning with under 2 minutes, one that a screen reader doesn't read, or buttons a keyboard can't reach |
| R4 | 4. One action extends, with no cap | "Keep chat open" works with one Enter, tap, or switch selection, and the tenth extension works like the first | A second step, or an extension that stops working |
| R5 | 5. Offer to turn the limit off | The warning and first reply offer "Give me more time from now on", and choosing it stops idle closing and idle nudges | No such option, or a nudge or close after choosing it |
| R6 | 6. Don't let buttons or steps expire | Quick-reply buttons, forms, and a pending question stay valid past the idle limit. A step that must expire (a one-time code) says its limit and offers to resend | An unexplained "expired" message |
| R7 | 7. Keep the user's place on any close | The draft and transcript are kept, and the returning user sees them | A returning user sees an empty chat |
| R8 | Hand-off rule | After the chat closed twice in a time-sensitive task, the bot offers a person and passes the saved draft and facts | The bot sends the user back to the start, or hands off with nothing saved |

## Conversations
1. **Rule stated early (R1).**
   Setup: Lakeview Pharmacy refill chat. Idle limit 5 minutes.
   User: "I need to refill"
   Expect: The reply asks for the prescription number and says the chat stays open while they type and that they will be warned before it closes. A statement that comes only after a close fails.

2. **Draft counts as activity (R2).**
   Setup: The bot asks for a 10-digit prescription number. The user types 7 digits slowly over 6 minutes, changing the draft every 1-2 minutes, and sends nothing.
   Steps: Wait with the draft changing.
   Expect: The chat does not close and no warning appears while the draft changes. Closing at the 5-minute mark fails.

3. **Switch scanning counts (R2).**
   Setup: Switch-access user. The scanning highlight steps through letters, one selection every 40 seconds.
   Steps: Select 4 letters over 3 minutes.
   Expect: Each scan step and selection resets the idle clock. Any warning or close during the entry fails.

4. **Warning with time left (R3).**
   Setup: The user goes quiet. No draft.
   Steps: Wait until the warning.
   Expect: A message appears in the transcript with at least 2 minutes left, such as "This chat will close in 2 minutes because it has been quiet." with [Keep chat open], [Give me more time from now on], and [Something else]. A warning under 2 minutes fails.

5. **Warning announced to a screen reader (R3).**
   Setup: Screen reader running.
   Steps: Wait for the warning without moving.
   Expect: The warning is read aloud (live region or moved focus), and the buttons are reachable by Tab. A silent warning fails.

6. **Warning keeps the draft (R3).**
   Setup: The warning shows. The saved draft is "8821".
   User: (reads the warning)
   Expect: The warning says "Your draft and this conversation are kept." only if that is true. A claim of "kept" when the draft is lost fails.

7. **Extension works ten times (R4).**
   Setup: The user presses "Keep chat open" ten times in a row across ten warnings.
   Expect: Each press works the same with one action. A cap, a second confirmation, or a refusal on the tenth fails.

8. **More time from now on (R5).**
   Setup: Same widget.
   User: (selects "Give me more time from now on")
   Expect: The bot confirms ("Done. I won't close this chat on a timer.") and no idle close or idle nudge follows, however long the user is quiet. A later "Are you still there?" fails.

9. **Buttons survive the idle limit (R6).**
   Setup: The bot showed [Refill] [Transfer] [Hours] [Something else]. The user leaves for 8 minutes with extended time on.
   Steps: Return and press [Transfer].
   Expect: The button still works. An "expired" message with no reason fails.

10. **One-time code says its limit (R6).**
    Setup: The bot sent a 6-digit one-time code that expires in 10 minutes.
    User: (enters the code after 12 minutes)
    Expect: The bot says the code expired, states the 10-minute limit, and offers to resend. A bare "invalid code" fails.

11. **Draft kept on a close (R7).**
    Setup: The chat closed with 7 digits typed, and the user returns 20 minutes later.
    Steps: Reopen the chat.
    Expect: The transcript and the typed 7 digits are shown. An empty chat that asks for the number again fails.

12. **Chat closed twice, time-sensitive task (R8).**
    Setup: The refill chat closed twice. A refill must be done by tomorrow's pickup.
    User: "it closed again. i cant type that fast"
    Expect: The bot offers a person and passes the saved draft and facts (prescription digits so far, pickup tomorrow). Asking for the number again from the start fails.

13. **Do nothing special: fast typist finishes (R3).**
    Setup: A user types a full prescription number and sends within 2 minutes.
    User: "5530172904"
    Expect: No warning, no extension prompt, no "more time" offer. The bot continues the refill. Showing a warning to a user who is actively engaged is over-correcting.

14. **Do nothing special: active typing gets no extension prompt (R2, R5).**
    Setup: A user already chose "more time from now on", then asks a question and gets an answer.
    User: "what are your hours on sunday"
    Expect: The bot answers. It does not re-offer "more time" or repeat the early statement. Repeating the offer to a user who already chose it fails.

## Cannot be judged from a transcript alone
- **Timing.** Conversations 2, 4, 7, 9, and 11 depend on the clock. Set the idle limit and the warning lead time in your harness.
- **Announcements and focus** in conversation 5 need a real screen reader, and switch behavior in conversation 3 needs a real switch or a faithful simulation.
- **Primary metric.** The ratio of timeout rates for declared-need sessions versus others needs production logs, not a single conversation.

## Notes (rests on my reading, not the page's text)
- Conversations 1, 2, 4 and 5, 7, 8, 9, 11, and 13 follow the page's section 6 tests 1, 2, 3, 4, 5, 6, 7, and 8 respectively.
- Conversations 3, 6, 10, 12, and 14 are additions: 3 (switch input in rule 2), 6 (the "kept" claim in the reference design), 10 (rule 6, expiring step), 12 (Hand-off rule), and 14 (Don't over-correct).
- The 5-minute idle limit and the 2-minute warning follow the page's example and starting point. Lakeview Pharmacy and all numbers are invented.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
