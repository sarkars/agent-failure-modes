# Test File: Controls Unreachable by Keyboard

**Pattern:** [Chatbot Widget Not Keyboard Accessible: Controls Unreachable by Keyboard](../goals/accessibility/failures/controls-unreachable-by-keyboard.md)
**Pattern ID:** controls-unreachable-by-keyboard
**Goal:** People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. (Family goal, from the pattern page.)
**Primary metric:** Keyboard-only task completion in testing. Target: 100% (starting point).
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

These tests check whether a chat widget shows the failure. They are not a score for any product, and they are design checks, not a WCAG conformance claim or legal advice. Run them on a text-chat web widget with the mouse unplugged, using Tab, Shift+Tab, Enter, Space, and Esc only, then repeat the announcement checks with a screen reader. Voice is PLANNED and not covered. The widget below is invented: "Lakeview Pharmacy" chat, with a launcher, a message box, Send, Stop, Copy, thumbs, Close, and quick-reply chips. No real people's data.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Use native controls | Launcher, chips, send, stop, copy, thumbs, and close are reached by Tab in a logical order and work with Enter and Space | A control Tab skips, or one that does nothing on Enter or Space |
| R2 | 2. Show focus on every control | Each control shows a visible focus mark at normal and 200% zoom, in light and dark themes | A control with no visible mark in any of those conditions |
| R3 | 3. Keep focus out of hiding | A focused control is never entirely behind the widget, a sticky bar, or a banner | A focused control fully hidden |
| R4 | 4. On open, move focus in; on close, move it back | Open puts focus in the message box (or panel heading). Close, by button or Esc, returns focus to the launcher | Focus stays on the page, or lands on the top of the page after close |
| R5 | 5. Closed means out of the tab order | A closed or hidden panel has zero focusable controls | Any focusable control inside a closed panel |
| R6 | 6. No traps, and say how to leave | An open modal panel holds focus, Esc closes it, and the hint is visible. An inline chat does not trap | Focus reaches the page behind a modal, Esc does nothing, or an inline chat traps Tab |
| R7 | 7. Never drop focus when a control changes | If a control disables, hides, or is replaced, focus moves to the next logical control, never the page top. Prefer a text confirmation over removing the control | Focus lands on `body` or the page top after a control is activated |
| R8 | 8. Don't steal focus for new messages | A new bot reply is announced, not focused. Exception: after a chip is activated, focus goes to the start of the reply it produced | Focus is pulled out of the message box by a reply the user did not trigger with a chip |
| R9 | 9. Chips never replace typing | 2-4 chips plus "Something else", and the message box stays open and reachable | 5 or more chips, no "Something else", or a message box hidden by the chips |
| R10 | Hand-off rule | A user who reports they can't reach a control gets a non-widget route (phone, email, or callback) in the same message, and the control id is logged | The bot keeps asking the user to press the control, or offers no other route |

## Conversations
1. **Launcher by keyboard (R1).**
   Setup: Lakeview Pharmacy site, chat closed.
   Steps: Tab from the top of the page until focus reaches "Chat with us". Press Enter.
   Expect: The launcher takes focus in the normal tab order and Enter opens the panel. A launcher that Tab skips fails.

2. **Chips respond to Enter and Space (R1).**
   Setup: Panel open. Bot shows "Hi! I can help with refills, transfers, or hours. [Refill] [Transfer] [Hours] [Something else]".
   Steps: Tab to [Refill], press Space. Reload the test, Tab to [Hours], press Enter.
   Expect: Both activate the chip. A chip that responds to only one key fails.

3. **Logical tab order (R1).**
   Setup: Panel open, one bot reply with chips, Copy, and two thumbs.
   Steps: Press Tab repeatedly from the message box.
   Expect: Focus moves through controls in reading order (reply, chips, Copy, thumbs, Send, Close, or the order the layout shows). Jumping backward or to the page behind fails.

4. **Visible focus at 200% zoom, dark theme (R2).**
   Setup: Browser zoom 200%, dark theme on.
   Steps: Tab through the launcher, each chip, Copy, thumbs, Stop, Send, and Close. Take a screenshot at each stop.
   Expect: Each focused control shows a visible mark. Any screenshot with no mark fails.

5. **Focus not hidden by a sticky bar (R3).**
   Setup: Host page has a sticky cookie banner pinned to the bottom, covering part of the panel at a narrow window width.
   Steps: Tab to Send and Close.
   Expect: Each focused control is at least partly visible, not entirely behind the banner. A control fully covered fails.

6. **Open moves focus in (R4).**
   Setup: Chat closed.
   Steps: Tab to the launcher, press Enter.
   Expect: Focus moves to the message box (or the panel heading), and a screen reader announces the name of the chat dialog or region. Focus left on the launcher with the panel open behind it fails.

7. **Esc returns focus to the launcher (R4).**
   Setup: Panel open, focus in the message box.
   Steps: Press Esc. Then reopen and activate the Close button.
   Expect: Both routes close the panel and return focus to "Chat with us". Focus on the top of the page fails.

8. **Closed panel has no tab stops (R5).**
   Setup: Panel opened once, then closed.
   Steps: From the launcher, press Tab 10 times.
   Expect: Focus moves on into the host page. It never stops on an invisible chip, Send, or thumb. Check by counting focusable elements inside the closed widget: expect 0.

9. **Modal panel holds focus, Esc exits (R6).**
   Setup: Widget is configured as a modal dialog. Hint "Press Esc to close" is shown.
   Steps: Open it, press Tab 30 times, then press Esc.
   Expect: Focus never reaches the page behind. Esc closes it. A panel with no Esc exit, or with no visible hint, fails.

10. **Do nothing special: inline chat does not trap (R6).**
    Setup: The same widget configured as an inline panel inside the "Contact" page, not a modal.
    Steps: Tab through the panel, past Close, and on.
    Expect: Focus leaves the panel and continues down the page. A trap on an inline chat fails. A modal-style trap here is the over-correction.

11. **Chip pressed, chip row disappears (R7).**
    Setup: Bot shows [Refill] [Transfer] [Hours] [Something else]. The chip row is replaced by the next reply after one is chosen.
    Steps: Tab to [Transfer], press Enter.
    Expect: Focus goes to the start of the reply the chip produced (see R8 exception), or the next logical control. It is never on `body` or the top of the page.

12. **Thumbs vote stays reachable (R7).**
    Setup: Bot reply with thumbs up and down.
    Steps: Tab to thumbs up, press Enter. Press Shift+Tab, then Tab.
    Expect: A text confirmation such as "Thanks for the feedback" and the thumb stays focusable, marked chosen. A thumb that leaves the tab order and drops focus to the page top fails.

13. **Reply arrives while typing (R8).**
    Setup: The user is typing "Can I get a 90-day supply" in the message box. A late bot reply from an earlier question arrives.
    Steps: Keep typing as the reply appears.
    Expect: Focus stays in the message box and the typed text is intact. The reply is announced to a screen reader. Focus pulled into the reply fails.

14. **Do nothing special: Stop and Copy keep focus where the table says (R7, R8).**
    Setup: A reply is streaming and a previous reply has Copy.
    Steps: Tab to Copy and press Enter. Later, press Stop during a stream.
    Expect: Focus stays on Copy with "Copied" announced. After Stop, focus goes to the message box with "Stopped" announced. Moving focus anywhere else fails.

15. **Chip set size and typing (R9).**
    Setup: Bot asks "What would you like to do?".
    Steps: Count chips. Tab to the message box and type "need to move my pickup".
    Expect: 2-4 chips plus "Something else", and typing works at any point. Seven chips with no "Something else", or a message box covered by the chip row, fails.

16. **Do nothing special: one obvious next step, no chips (R9).**
    Setup: The user types "yes" to "Do you want to confirm pickup for 4 p.m.?".
    Steps: Read the next bot turn and Tab through it.
    Expect: The bot confirms in text. No chip row is added for a single obvious step.

17. **User cannot reach a control (R10).**
    Setup: In a test build, the thumbs control is deliberately not in the tab order.
    User: "i use a keyboard and cant press the thumbs up button. it just skips it"
    Expect: The bot gives a phone number, email, or callback in the same message (for example "Call the pharmacy at 555-0123" in the fake setup), and the control id is in the log. Asking the user to "try clicking" fails.

## Cannot be judged from a transcript alone
- **Focus, tab stops, and focus rings** are not in a text log. These need a manual run (the pattern's section 6) or a client that records focus events.
- **Announcements** (conversations 6, 12, 13, 14) need a real screen reader; test each pairing you support.
- **Primary metric.** Keyboard-only task completion needs a scripted task per release, not a single conversation.

## Notes (rests on my reading, not the page's text)
- Conversations 1-3 map to page tests 1; 4 and 5 to page test 2; 6-8 to page test 3; 9 to page test 4; 11, 12, and 14 to page test 5; 13 to page test 6; 15 to page test 7.
- Conversations 10, 16, and 17 are additions: 10 and 16 check Don't over-correct, 17 checks the Hand-off rule.
- Lakeview Pharmacy, the phone number, and the widget are invented.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
