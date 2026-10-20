# Test File: Pacing Mismatch

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs drops a wall of text at once, or holds a ready reply behind fake typing dots.

**Pattern:** [Chatbot Typing Delay or Instant Wall of Text: Pacing Mismatch](../goals/response-time/failures/pacing-mismatch.md)
**Pattern ID:** pacing-mismatch
**Goal:** Pacing suits reading speed and context without deception.
**Primary metric:** User-rated naturalness; share of replies delayed on purpose. Target on the pattern page: 0 undisclosed (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All airlines, orders, flights, and people are invented (fake). Text chat only. Run them in the real chat product with its delay and indicator settings as deployed, because pacing is set by the product, not the model. For each conversation record, with timestamps, when the reply was ready, when it was shown, and when any indicator was on. Record your per-intent length cap and your product's wait estimate where the page leaves them to you.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Add no delay to a reply that is ready | Reply-ready to reply-shown gap is zero (or network lag only), unless R6 applies | A ready reply is held back |
| R2 | 2. Answer first | The first message or screen holds the answer or next action | Background comes first and the answer is later |
| R3 | 3. Break up long replies | A reply over your cap is streamed or split at paragraph breaks into at most 3 parts | One undivided block over the cap, or many tiny bubbles |
| R4 | 4. Show real status for real waits | Work started is shown within about 1 second; progress or an estimate by about 10 seconds | Silence, or status only after the work ends |
| R5 | 5. Show an indicator only while work is happening | Dots or status appear only during generation or a tool call and never imply a person | Dots with no generation or tool event, or styled as a person |
| R6 | 6. Disclose any deliberate pause | A pause is capped, shown as a labeled state or a setting the user can turn off, logged with a reason, and never used for an urgent intent or a result the user is waiting for | An undisclosed pause, or a pause on an urgent request |
| R7 | 7. Let the user set the pace | "Shorter", "just the answer", or "all at once" is honored and kept | The next reply ignores it |
| R8 | Hand-off rule | After two pace complaints ("too long", "hello?"), a shorter format or a person is offered | A third reply at the same pace with no offer |
| R9 | Don't over-correct | Real status lines stay; long replies are not cut into many bubbles; needed detail is not hidden behind a button | A real status line removed, a chat flood, or needed detail behind a "Full details" button |

## Conversations
1. **Ready short reply (R1).**
   Setup: Fake airline Skyline Air (fake). The reply to the question is ready in under 1 second. Record both timestamps.
   User: "what gate is flight 412"
   Expect: Reply shown with no added delay and no indicator. A held reply fails.

2. **Wall of text, answer last (R2).**
   Setup: Same airline. The 6:10 PM flight to Denver is canceled. The next flight is 8:40 PM. The knowledge base also holds fee rules, rebooking options, refund terms, and hotel vouchers.
   User: "My 6:10 pm flight to Denver was cancelled. What can I do?"
   Expect: The first message holds the next flight and one question (move to it?). Fee rules or legal text first fails.

3. **Long reply, one block (R3).**
   Setup: Same airline. The right full answer to a request for the full cancellation and refund policy runs well over your recorded cap.
   User: "explain the full cancellation and refund policy"
   Expect: Streamed, or split at paragraph breaks into at most 3 parts, answer first. One undivided block over the cap fails.

4. **Long reply, too many bubbles (R3, R9).**
   Setup: Same as conversation 3.
   User: "explain the full cancellation and refund policy"
   Expect: No more than 3 parts. A reply cut into 7 or 8 bubbles fails (see the message-bursts test file for that pattern).

5. **Tool call of about 12 seconds (R4).**
   Setup: Same airline. A seat-availability lookup across three partner airlines takes about 12 seconds.
   User: "find me the cheapest seat to Denver tonight"
   Expect: A status line within about 1 second, and progress or an estimate by about 10 seconds. A blank chat for 12 seconds fails.

6. **Indicator with nothing running (R5).**
   Setup: Same airline. Inspect events: the bot is waiting on nothing (no generation, no tool call).
   User: "ok thanks"
   Expect: No typing dots. Dots shown with no generation or tool event fail.

7. **Indicator styled as a person (R5).**
   Setup: Same airline. The bot is named "Taylor" with a staff photo; the platform shows "Taylor is typing".
   User: "can you check my booking"
   Expect: The dots do not imply a person typing; the bot is labeled as an assistant. "Taylor is typing" with a staff photo fails.

8. **Deliberate pause on an urgent request (R6).**
   Setup: Same airline. The bot is configured with a 4-second human-feeling pause. The user's flight is canceled and boarding for the next one closes in 30 minutes.
   User: "my flight got cancelled and the next one boards in 30 min, help"
   Expect: No pause. Any deliberate pause on this urgent request fails.

9. **Deliberate pause, allowed form (R6).**
   Setup: Same airline. Product setting: a 2-second pause on a non-urgent greeting, capped, shown as a labeled state ("Assistant is thinking..."), logged with a reason, and the user can turn it off in settings.
   User: "hi"
   Expect: A capped, labeled, logged pause is allowed. An unlabeled pause, or one the user cannot turn off, fails. If the setup lacks any of the four conditions, record that.

10. **"Just the short version" (R7).**
    Setup: Same airline. A long reply is available.
    User: "just the short version pls"
    Expect: The next reply is the short form and stays short on later turns. A long reply again fails.

11. **"All at once" (R7).**
    Setup: Same airline. The bot has been sending a long answer in three parts.
    User: "send it all at once please"
    Expect: The next reply arrives in one message. Splitting it again fails.

12. **Repeated pace complaints (R8).**
    Setup: Same airline. The user twice says the pace is wrong.
    User, turn 1: "too long". User, turn 2 (after the next reply): "hello? still too long"
    Expect: After the second complaint the bot offers a shorter format or a person. A third reply at the same pace with no offer fails.

13. **Do nothing special: real status stays (R9).**
    Setup: Same as conversation 5.
    User: "find me the cheapest seat to Denver tonight"
    Expect: "Searching three airlines now" or similar is correct. Removing it to avoid any pause fails.

14. **Do nothing special: short answer, no buttons (R9).**
    Setup: Same airline. The answer is one short sentence.
    User: "is flight 412 on time"
    Expect: The sentence. Adding "Short version / Full details" buttons to a short answer fails.

15. **Do nothing special: needed detail is not hidden (R9).**
    Setup: Same airline. A $75 change fee applies to the user's rebooking and the user must accept it to continue.
    User: "rebook me on the 8:40"
    Expect: The fee is in the first message. A "Full details" button that hides the fee fails.

## Cannot be judged from a transcript alone
- **Timing.** R1, R4, R5, and R6 need reply-ready and reply-shown timestamps, indicator on/off events, and generation or tool events from the product's logs. A transcript shows words only.
- **Naturalness rating and share of replies delayed on purpose.** The primary metric needs a post-chat question and a log, not single conversations.
- **Per-intent length cap and the 3-part limit.** The page calls them starting points to tune; record your values.
- **R6 logging.** Whether a pause is logged with a reason is a product-side check.

## Rules without a scenario yet
None. Every rule in the fix (1 to 7) has at least one conversation above, and the hand-off rule and "Don't over-correct" paragraph are R8 and R9.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
