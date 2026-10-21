# Test File: Mobile Keyboard or Screen Hides the Reply

This file is a set of chat test conversations for people who build or review web chat widgets and want to check whether the newest reply stays readable on a phone with the keyboard open, in landscape, or with larger text.

**Pattern:** [Chatbot Answer Hidden by the Phone Keyboard: Mobile Keyboard or Screen Hides the Reply](../goals/chat-interface/failures/mobile-keyboard-or-screen-hides-the-reply.md)
**Pattern ID:** mobile-keyboard-or-screen-hides-the-reply
**Goal:** The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost.
**Primary metric:** Layout defects per device in release testing. Starting target on the pattern page: 0 open defects on every device and viewport in the test matrix (a starting point, to tune).
**Maturity:** Tests written; not yet run.

These tests check whether a chat window shows the failure. They are not a score for any product. The failure is in the page layout, not the model's words, so most checks need a real phone, an emulator, or screenshots. Those checks are marked PLANNED, because this repo's chat-first scope does not measure layout. What a transcript and the client event log can show is marked as such (`reply.visible_ratio`, `ui.show_full_reply_tap`, `client.keyboard_open`, and the user's own words). The pattern page says native-app behavior and voice are PLANNED, not written. Use fake data. All airlines, stores, and people are invented.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Size the chat window to the visible area | With the keyboard open, the message list shrinks above the keyboard. PLANNED: needs a real device | The list keeps full height and runs under the keyboard |
| R2 | 2. Never overlap the reply with the input bar | The message list ends where the input bar begins. PLANNED: screenshot review | The input bar sits on top of any part of the newest reply |
| R3 | 3. Scroll to the newest reply after the keyboard opens, only if the reader was at the bottom | `reply.visible_ratio` is 1 for the newest reply when the reader was at the bottom; no jump when the reader had scrolled up | The newest reply is partly outside the visible area for a bottom reader, or the view jumps for a reader who had scrolled up |
| R4 | 4. Reflow, don't clip | At 320 CSS pixel width and 200 percent text, no text, button, or quick-reply chip is cut off and nothing needs horizontal scrolling. PLANNED: screenshot or automated check | Clipped text or buttons, or a horizontal scroll event in the chat window |
| R5 | 5. Test the matrix before release | A test run log row exists for each device and state in the matrix | A device or state missing from the log |
| R6 | 6. Make the failure recoverable | If the newest reply is not fully visible, "Jump to latest" or "Show full reply" is offered | A hidden reply with no way to see it |
| R7 | Lead with the answer | The key fact is in the first line of the reply, so the visible part holds it | The fact sits in the last line, which is the part most likely to be covered |
| R8 | Don't over-correct: normal desktop layout is unchanged | No "Show full reply" prompt when the reply is fully visible; the page still scrolls and zooms | An extra prompt on desktop, or the page locked so it cannot scroll or zoom |

## Conversations
1. **Small phone, portrait, keyboard open, long reply (R1, R2, R3).**
   Setup: Fake airline chat widget, Skyharbor Air, on a small iPhone-class screen (real device or emulator). PLANNED for the layout check. Booking: Denver flight, fare type Main Cabin (fake). Reply is the change-fee policy, about 8 lines, ending with a $75 fee line.
   User: "Can I change my Denver flight for free?"
   Expect: With the keyboard open, the newest reply and the input bar are both fully visible, with no overlap. In the event log, `reply.visible_ratio` is 1 and `client.keyboard_open` is true. A ratio below 1 fails.

2. **Same, landscape (R1, R2).**
   Setup: Same as conversation 1, rotated to landscape. PLANNED.
   User: "Can I change my Denver flight for free?"
   Expect: The newest reply can be read by scrolling the list, and the input bar is visible. An input bar that covers the reply fails.

3. **Text at 200 percent, 320 CSS pixel width (R4).**
   Setup: Same reply and a row of three quick-reply chips: "Change flight", "Cancel flight", "Talk to a person". PLANNED: screenshot or automated reflow check.
   User: "Can I change my Denver flight for free?"
   Expect: No clipped text or chips, and no horizontal scroll. A client scroll event with a nonzero horizontal offset fails.

4. **Reader scrolled up, keyboard opens (R3, R6).**
   Setup: A long thread. The reader has scrolled up to reread an earlier price ($89 seat fee, fake). Then taps the input box so the keyboard opens. PLANNED for the view check.
   User: (taps the input box)
   Expect: The view does not jump to the bottom. "Jump to latest" is offered. A forced scroll to the bottom fails.

5. **Quick-reply buttons at narrow width with the keyboard open (R4, R5).**
   Setup: Same chips as conversation 3, narrow phone, keyboard open. PLANNED.
   User: (taps "Talk to a person")
   Expect: All three chips are reachable and tappable, and the tap sends. A chip behind the keyboard fails.

6. **Send with the keyboard open (R1).**
   Setup: Keyboard open on a phone. PLANNED.
   User: "ok, change it to Friday"
   Expect: The send works and the bot's reply arrives with `reply.visible_ratio` of 1. A client event with keyboard state and a send error fails, unless a network error explains it.

7. **Key fact in the first line (R7).**
   Setup: Fake reply with the answer last: three lines of fare background, then "Your change fee is $75." Compare with a reply that opens with "Your change fee is $75."
   User: "how much to change my flight"
   Expect: The fee is in the first line. A fee only in the last line fails, because that line is the one most likely to be covered.

8. **Reader says they cannot see it (R6, hand-off rule).**
   Setup: A mobile client with `client.device_class` mobile. "Show full reply" has been offered and tapped, and the reply is still cut off.
   User: "I cant see the answer, its cut off on my phone"
   Expect: The bot offers a person or another channel (an email or a web link), and passes the conversation id and the device and browser details. Another repeat of the same reply fails. Needs a person to check the hand-off payload.

9. **Matrix coverage (R5).**
   Setup: Release test run log for the matrix on the pattern page: small iPhone, mid-size Android phone, tablet; portrait and landscape; keyboard closed and open; text 100 and 200 percent.
   Expect: One log row per device and state, with the defect count. A missing row fails. This is a release check, not a transcript check.

10. **Do nothing special: desktop window (R8).**
    Setup: Desktop browser, normal window, the same reply as conversation 1.
    User: "Can I change my Denver flight for free?"
    Expect: The layout is unchanged and no "Show full reply" prompt appears. An extra prompt while the reply is fully visible fails.

11. **Do nothing special: short reply on a phone (R8).**
    Setup: Phone, keyboard open, reply of one line.
    User: "what time do you open"
    Expect: The reply is shown in full with no extra prompt. A "Show full reply" button on a one-line reply fails.

12. **Do nothing special: the page still zooms (R8).**
    Setup: Phone. PLANNED.
    User: (pinch to zoom, then scroll the page)
    Expect: Zoom and page scroll still work. A page locked against zoom or scroll to hide the defect fails.

## Cannot be judged from a transcript alone
- **Layout, overlap, and clipping (PLANNED).** Need a real phone, an emulator, or screenshots. The chat transcript text does not show what was covered.
- **Browser keyboard behavior.** It differs by browser and version (section 4 of the pattern page). Rerun the matrix after browser releases.
- **Native-app and voice (PLANNED).** The pattern page does not cover them yet.
- **Production rates.** These tests do not measure how often replies are hidden. Use the metrics on the pattern page. This file sets no thresholds beyond the starting targets stated there.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Device, browser, and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
