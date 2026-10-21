# Test File: Chat Widget Hard to Find or Intrusive

This file is a set of test scenarios for people who build or review website chat widgets and want to check whether theirs can be found (a labeled launcher, an entry point where people get stuck) without getting in the visitor's way (no auto-open, no repeat pop-ups, nothing covering the page).

**Pattern:** [Chat Widget Placement and Chatbot Pop-ups: Chat Widget Hard to Find, or Intrusive](../goals/onboarding-and-discoverability/failures/chat-widget-hard-to-find-or-intrusive.md)
**Pattern ID:** chat-widget-hard-to-find-or-intrusive
**Goal:** People know what the assistant can do and how to start, without needing to guess or to engineer prompts.
**Primary metric:** Widget open rate (user-initiated opens per session shown the launcher) and dismissals within a few seconds (proactive opens closed within 5 seconds with no message). Starting targets on the pattern page: open rate set from your baseline and rising; quick dismissals under 20% (both starting points to tune, not measured benchmarks).
**Maturity:** Tests written; not yet run.

These tests check whether a widget shows the failure. They are not a score for any product. All stores, orders, accounts, and people below are invented and labeled fake. Most of this pattern is about the page and the widget, not the words of the model, so most items cannot be judged from a transcript. Items marked "Needs a person" are checked by someone loading the page on a desktop and a phone and watching it. Items marked "Needs the widget event log" are checked from `widget.shown`, `widget.opened` and `widget.dismissed` events with `trigger`, `by`, and `ms_since_shown`. Only the items marked "Transcript" can be judged from the chat text.

The fake product used throughout: "Lakeview Fiber (fake)", a regional internet provider's website. Fake pages: Home, Plans (flagged complex), Install and fees (flagged complex), Checkout, Payment, Contact. Fake plans: Basic, Plus, and Max (invented names and speeds; no real prices are needed for these tests). Fake visitor: "Dana (fake)" in Columbus, Ohio.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Label the launcher with its job | The launcher shows visible text that names what the assistant helps with (for example "Ask about plans"). Needs a person | An icon alone, or a label that only says "Chat" |
| R2 | 2. Keep one launcher in one place | One launcher per page, the same position across page templates, not hidden by a sticky bar, and no second chat button. Needs a person | Two chat buttons, a launcher that moves between templates, or one covered by a sticky bar |
| R3 | 3. Put an entry point where the hard question comes up | Each page the team flags as complex has an inline entry with a page-specific prompt, and tapping it starts the chat on that task. Needs a person, and the transcript for the start | A flagged page with no inline entry, a generic prompt, or an entry that opens on a generic greeting |
| R4 | 4. Never auto-open the panel on page load | The full panel opens only when the visitor taps the launcher or an entry point. Needs the widget event log | Any `widget.opened` event with `by = auto` |
| R5 | 5. A proactive nudge is a small teaser, only on a clear sign of need | Every teaser has a logged sign (page flagged complex, or an unresolved earlier chat); none on checkout, payment, or form pages; at most one per session. Needs the widget event log | A teaser with no logged sign, a teaser on a blocked page type, or a second teaser in one session |
| R6 | 6. One dismissal means no for the session | After the visitor closes a teaser or the panel, no teaser shows again in that session. Needs the widget event log | A teaser after a dismissal in the same session |
| R7 | 7. Never cover what the visitor is using | With a teaser showing, no focused control is fully hidden, and Esc closes the teaser or panel and returns focus to where it was. Needs a person | A focused control entirely hidden, Esc that does nothing, or focus lost after closing |
| R8 | 8. Teaser text names a task | The teaser copy says what the assistant can do on this page. Needs a person | "How can I help you?" or "Chat with us" |
| R9 | 9. Log every show, open, and dismiss with its trigger | Each widget event carries `trigger`, `by`, and `ms_since_shown`. Needs the widget event log | An event missing any of the three fields |
| R10 | Don't over-correct: do not hide the widget to cut dismissals; no pulsing, bouncing, or looping sound; no second chat button; no menu of choices when the visitor already asked | The launcher stays visible and still; a visitor who typed a question gets an answer, not a choice menu | Launcher removed or tucked away, an animation or sound on a loop, or a choice menu shown after a typed question |
| R11 | Hand-off rule | The widget is not the only way to reach support (the contact page lists a phone number or form), and a visitor who asks for a person is routed to one | The contact page has no route other than the widget, or a request for a person is ignored or looped |

## Conversations
1. **Launcher has a label on every template (R1).**
   Setup: Load Home, Plans, Install and fees, Checkout, and Contact on a desktop browser and on a phone. Needs a person.
   User: (no chat turn; a person looks at the page)
   Expect: The person checks each page for a launcher with visible text that names its job (for example "Ask about plans"). An icon alone, or a label that says only "Chat", fails. Record the label seen on each page.

2. **Same place on every template (R2).**
   Setup: Same five pages, desktop and phone. Needs a person.
   User: (no chat turn)
   Expect: The person checks one launcher per page, in the same position on all five. A launcher in a different spot on any page, or two launchers on one page, fails.

3. **Not hidden by a sticky bar, no competing button (R2).**
   Setup: Plans page on a phone, scrolled so the page's sticky "Check my address" bar is showing. A second vendor "Contact us" chat button is installed on the same page for this test. Needs a person.
   User: (no chat turn)
   Expect: The launcher is fully visible above or beside the sticky bar. A launcher covered by the bar fails. A second chat button on the page fails.

4. **Inline entry on a flagged page (R3).**
   Setup: The Plans page is flagged complex. Needs a person.
   User: (no chat turn)
   Expect: A page-specific inline link sits under the plan table (for example "Not sure which plan fits? Compare with the assistant"). A flagged page with no inline entry, or one that says only "Chat with us", fails.

5. **Tapping the entry starts on the task (R3, Transcript).**
   Setup: Dana (fake) taps the "Compare with the assistant" link on the Plans page. No message typed yet.
   User: (opens from the link) "ok"
   Expect: The first bot message already starts on the plan comparison (it names the plans, or asks which matters most), not "Hi! How can I help you today?". A generic greeting fails.

6. **Generic launcher on a flagged page offers starting points (R3, Transcript).**
   Setup: Dana (fake) opens the chat from the bottom-right launcher on the Install and fees page and has typed nothing. The text box must stay usable.
   User: (taps the launcher, then waits)
   Expect: The panel shows 2-4 page-specific starting points (for example "Install fees", "Self-install", "Schedule an install") plus "Something else", with the text box open. A blank panel, or choices unrelated to the page, fails. (This test follows the pattern's "Offer choices" move; the closest rule is R3.)

7. **No auto-open on any page (R4).**
   Setup: Load Home, Plans, and Checkout in turn and wait 2 minutes on each, without touching anything. Needs the widget event log.
   User: (no chat turn)
   Expect: Zero `widget.opened` events with `by = auto`. Any auto-open of the full panel fails.

8. **Teaser on a flagged page has a logged sign, once (R5).**
   Setup: Open Plans (flagged complex), then Install and fees (also flagged) in one session. No earlier dismissals. Needs the widget event log.
   User: (no chat turn)
   Expect: At most one teaser in the session. Each teaser's `trigger` shows the sign (page flagged complex). A second teaser on the second flagged page, or a teaser with no logged sign, fails.

9. **No teaser on checkout, payment, or forms (R5).**
   Setup: Move through Checkout and Payment, and open the address form, in one fresh session. Needs the widget event log.
   User: (no chat turn)
   Expect: No `widget.shown` event with `trigger = teaser` on these pages. The labeled launcher remains. Any teaser fails.

10. **Returning visitor with an unresolved chat (R5).**
    Setup: Dana (fake) opened chat last week about install fees and left without a resolution; the session record shows this. She loads the Install and fees page. Needs the widget event log.
    User: (no chat turn)
    Expect: One teaser only, with a sign logged (unresolved earlier chat) and copy that picks up the topic (for example "Pick up your question about install fees?"). No auto-open. Two teasers, or a teaser with no logged sign, fails.

11. **Do nothing special: ordinary page, no sign of need (R5, R10).**
    Setup: Fresh session on the Home page (not flagged). No earlier chat. Needs the widget event log.
    User: (no chat turn)
    Expect: Only the labeled launcher shows. No teaser, no panel, no animation. A teaser here, with no sign of need, fails.

12. **A dismissed teaser stays dismissed (R6).**
    Setup: On the Plans page, a teaser appears and Dana (fake) closes it. She then opens Install and fees and one more flagged page in the same session. Needs the widget event log.
    User: (closes the teaser)
    Expect: No `widget.shown` with `trigger = teaser` after the `widget.dismissed` event in that session. A teaser on either later page fails.

13. **A closed panel means no proactive show (R6).**
    Setup: Dana (fake) opens the panel from the launcher, sends no message, and closes it. She then moves to another flagged page in the same session. Needs the widget event log.
    User: (opens, then closes the panel)
    Expect: No teaser on the next page in this session. The labeled launcher stays. A teaser fails.

14. **A teaser covers nothing in focus (R7).**
    Setup: A teaser is showing on the Plans page. Tab through every control on the page on a desktop, then at 200% zoom and again at phone width. Needs a person.
    User: (no chat turn)
    Expect: At no point is the focused control entirely hidden by the teaser or panel. A focused link or button fully behind the teaser fails.

15. **Esc closes and focus returns (R7).**
    Setup: A teaser is showing and focus was on the "Check my address" button. Press Esc. Needs a person.
    User: (no chat turn)
    Expect: The teaser closes and focus is back on the "Check my address" button. Esc that does nothing, or focus that jumps to the top of the page, fails.

16. **Teaser copy names a task (R8).**
    Setup: Collect the teaser text shown on the Plans page and on the Install and fees page. Needs a person.
    User: (no chat turn)
    Expect: Each teaser names something the assistant can do on that page (for example "Compare plans for your household"). "Hi there! How can I help?" or "Chat with us" fails.

17. **Events are complete (R9).**
    Setup: Run tests 7 to 13, then export all widget events. Needs the widget event log.
    User: (no chat turn)
    Expect: Every `widget.shown`, `widget.opened`, and `widget.dismissed` event has `trigger`, `by`, and `ms_since_shown`. A missing field in any event fails.

18. **Do nothing special: the launcher stays still and visible (R10).**
    Setup: Watch the launcher on the Plans page for 30 seconds on a desktop and a phone. Needs a person.
    User: (no chat turn)
    Expect: The launcher stays in place, visible, with no pulsing, bouncing, or looping sound. A moving launcher, a sound, or a launcher that fades out to avoid dismissals, fails.

19. **Do nothing special: typed question gets an answer, not a menu (R10, Transcript).**
    Setup: Dana (fake) opens the panel from the launcher and types a question straight away.
    User: "do u install on saturdays"
    Expect: The bot answers the question (or says what it knows and what it does not). It does not first show a menu of "Compare plans / Install and fees / Something else". A choice menu after a typed question fails.

20. **A request for a person is routed (R11, Transcript).**
    Setup: Dana (fake) is in an open chat on the Install and fees page. The Contact page lists a phone number and a form (fake; invented numbers are not needed in the test). Needs a person for the Contact page check.
    User: "can i just talk to someone"
    Expect: The bot shows the route to a person in the panel (phone or form) and does not loop back to a menu. A person must also confirm the Contact page lists a route other than the widget. A loop, a refusal, or a Contact page whose only route is the widget, fails.

## Cannot be judged from a transcript alone
- **Layout and labels (R1, R2, R3, R8).** Need a person looking at the page on a desktop and on a phone. Record what the label says, where it sits, and what the teaser says.
- **Auto-open, teasers, and dismissals (R4, R5, R6, R9).** Need the widget event log with `trigger`, `by`, and `ms_since_shown` for each show, open, and dismiss.
- **Keyboard and focus (R7).** Needs a person tabbing through the page, at 200% zoom and at phone width, and pressing Esc.
- **Visual noise (R10).** Needs a person watching the launcher for movement or sound.
- **Production rates.** These tests do not measure the open rate or the share of quick dismissals. Use the metrics on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
