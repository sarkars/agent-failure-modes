# Test File: Auto-Scroll Fights the Reader

This file is a set of chat test conversations for people who build or review chat windows that stream replies and want to check whether theirs lets the reader scroll away from the newest text.

**Pattern:** [Chat Auto-Scroll Jumps to the Bottom While Streaming: Auto-Scroll Fights the Reader](../goals/chat-interface/failures/auto-scroll-fights-the-reader.md)
**Pattern ID:** auto-scroll-fights-the-reader
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Reports of scroll jumping; scroll-up events during streaming that were overridden. Starting target on the pattern page: 0 overridden scroll-ups in release tests (a starting point, to tune).
**Maturity:** Tests written; not yet run.

These tests check whether a chat window shows the failure. They are not a score for any product. The failure is in the window's scroll code, not in the model's words, so each conversation is judged from the client event log (the events named on the pattern page: `reply.stream_start`, `reply.chunk`, `scroll.user`, `scroll.programmatic`, `jump_to_latest.shown`, `jump_to_latest.click`, `message.send`) and the rendered transcript. Use a reply at least three screens long. All stores, people, and products are invented. Checks that need a real browser at set widths, keyboard focus, or pixel measurement are marked PLANNED. Web and voice are out of scope for this file except where marked PLANNED; voice has no scroll position.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep one `following` flag, on when a reply starts at the bottom | While the reader is at the bottom, `scroll.programmatic reason=chunk` follows the stream to the end with no user input | The view stops following a reader who never scrolled |
| R2 | 2. Turn following off on the first user scroll up | After a `scroll.user` up that leaves the view past the threshold, following is off | Following stays on after the reader scrolled up |
| R3 | 3. While following is off, chunks never change the scroll position | No `scroll.programmatic reason=chunk` between the scroll up and the reader's next scroll down, jump click, or send | Any chunk-driven scroll in that window (an overridden scroll-up) |
| R4 | 4. Show "Jump to latest" when following is off and content is below | `jump_to_latest.shown` after following turns off and a later chunk arrives; click scrolls to the end and turns following on | No button, or a click that does not return to the newest text |
| R5 | 5. Turn following back on only by the reader's action | Following resumes only after scroll back to the bottom, a jump click, or a send | Following resumes on its own while the reader is still reading above |
| R6 | 6. On send, show the reader's own message | `scroll.programmatic reason=send` shows the new message; this is not counted as an override | No scroll to the sent message, or a send scroll counted as an override |
| R7 | 7. Tag your own scrolls; only real input changes `following` | An image or code block expanding while at the bottom does not turn following off | Following turns off with no preceding `scroll.user` (lost follow) |
| R8 | 8. Keep browser scroll anchoring on for the list | Older history loading above leaves the visible message in place. PLANNED: needs a real browser | The visible message moves when history loads above |
| R9 | 9. Optional: anchor a long reply at its start | Only when the product has enabled it: the reply's first line stays at the top once the reply is taller than the view | Enabled, but the first line scrolls out of view |
| R10 | Don't over-correct: a reader who stays at the bottom keeps following | Following stays on with no scroll input; "Jump to latest" is not shown; the reply still streams | Following turned off for everyone, the button shown to a bottom reader, or streaming removed |

## Conversations
1. **Reader stays at the bottom (R1, R10).**
   Setup: Fake home-improvement store chat, Hearthline Hardware. Reply is a 40-line garbage disposal replacement guide, about three screens long. The reader makes no scroll input.
   User: "How do I replace a 1/2 hp garbage disposal myself?"
   Expect: `reply.stream_start`, then `scroll.programmatic reason=chunk` follows the stream to the end. No `scroll.user`. `jump_to_latest.shown` does not appear.

2. **Scroll up by mouse wheel mid-stream (R2, R3).**
   Setup: Same reply as conversation 1. At the point the reply passes the bottom of the screen, the harness sends one wheel scroll up to reread line 1 ("turn off the breaker first").
   User: "How do I replace a 1/2 hp garbage disposal myself?"
   Expect: One `scroll.user` up. After it, no `scroll.programmatic reason=chunk` for the rest of the stream. Any chunk-driven scroll fails, and that counts as one overridden scroll-up.

3. **Same, by touch swipe, Page Up, and scrollbar drag (R2).**
   Setup: Run conversation 2 three times, once per input: touch swipe, Page Up key, scrollbar drag. PLANNED: needs a real browser or device harness.
   User: "How do I replace a 1/2 hp garbage disposal myself?"
   Expect: Each input logs `scroll.user` with the matching `input` value and turns following off. An input type that is missed fails for that run.

4. **Scroll up, then click "Jump to latest" (R4).**
   Setup: Same as conversation 2, then the harness clicks "Jump to latest" while chunks still arrive.
   Expect: `jump_to_latest.shown` appears after following turned off and a later chunk arrived. After `jump_to_latest.click`, one `scroll.programmatic reason=jump` goes to the end, and chunks follow again.

5. **Scroll up, then scroll back to the bottom by hand (R5).**
   Setup: Same as conversation 2, then the harness scrolls back within the bottom threshold.
   Expect: Following resumes and the button hides. No resume happens before that scroll.

6. **Scroll up, then send a new message (R5, R6).**
   Setup: Same as conversation 2. While the first reply streams, the reader sends a follow-up.
   User: "wait, what was the first step?"
   Expect: `message.send`, then `scroll.programmatic reason=send` shows the new message and following is on. This send-scroll is not counted as an overridden scroll-up.

7. **A code block expands while at the bottom (R7).**
   Setup: Reply includes a collapsed 12-line code block that expands when it finishes rendering, and an image that loads late. The reader makes no scroll input.
   User: "show me the wiring diagram and the steps"
   Expect: Following stays on. The layout-driven scroll events are not logged as `scroll.user`. A following-off state with no preceding `scroll.user` fails (lost follow).

8. **Older history loads above while reading mid-thread (R8).**
   Setup: Thread with 60 earlier messages. The reader is viewing message 45. PLANNED: needs a real browser.
   User: (scrolls to the top edge, which loads older history)
   Expect: Message 45 stays where it was on screen after history loads. A visible jump fails.

9. **Reach the button by keyboard (R4).**
   Setup: Following is off, button visible. PLANNED: needs a real browser to check focus.
   User: (presses Tab until the button is focused, then Enter)
   Expect: The button is reachable by keyboard and is a real button. Focus did not move to it before the reader pressed Tab. Enter scrolls to the end.

10. **Optional anchor for a long reply (R9).**
    Setup: Run only if the product has enabled the optional start-anchor setting. Reply taller than the view.
    User: "give me the full return policy"
    Expect: Following stops once the reply's first line reaches the top of the view, and "Jump to latest" is shown. If the product has not enabled it, mark this conversation not applicable.

11. **Do nothing special: a short reply (R10).**
    Setup: Reply fits in one screen.
    User: "what time do you close today"
    Expect: No `scroll.user`, no button, and no overridden scroll-up. The reply is visible when it ends.

12. **Do nothing special: the reader at the bottom the whole time on a phone (R10).**
    Setup: Phone-width window, long reply, the reader taps nothing. PLANNED: needs a phone-width harness.
    User: "How do I replace a 1/2 hp garbage disposal myself?"
    Expect: Following stays on to the end, and no "Jump to latest" appears. Turning following off here is over-correcting.

13. **Complaint typed in chat (hand-off rule).**
    Setup: The window has the bug, so the reader types a complaint mid-stream.
    User: "this keeps jumping and I cant scroll up"
    Expect: The reply says scrolling up pauses following and that the button returns to the latest text, and the session's client scroll events are filed to the chat-window bug queue. Needs a person to check the queue. A reply that blames the reader fails.

## Cannot be judged from a transcript alone
- **Scroll position and pixel distance.** Needs the client event log or a browser harness; the rendered transcript text does not show where the view was.
- **Real input types, widths, and keyboard focus (PLANNED).** Conversations 3, 8, 9, and 12 need a real browser or device.
- **Whether a reader actually lost their place.** These tests check the events, not reading loss.
- **Production rates.** These tests do not measure how often the window overrides a scroll-up. Use the metrics on the pattern page. This file sets no thresholds beyond the starting targets stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Product and client version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
