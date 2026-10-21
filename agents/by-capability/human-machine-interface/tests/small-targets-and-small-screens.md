# Test File: Small Targets and Small Screens

This file is a set of chat test conversations for people who build or review chat widgets with chips, card buttons, links, and carousels, and want to check whether theirs is usable by thumb on a 320 CSS pixel wide phone.

> **Read this first.** These are test conversations and widget checks only. They are design guidance, not accessibility-compliance advice. An accessibility expert should review the pack before you rely on it. Pixel sizes below are the pattern page's starting points, to tune on your own devices. Expected behavior names what the pattern page requires, not exact words.

**Pattern:** [Chatbot Buttons Too Small to Tap on a Phone: Small Targets and Small Screens](../goals/visual/failures/small-targets-and-small-screens.md)
**Pattern ID:** small-targets-and-small-screens
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes.
**Primary metric:** Target-size pass rate: share of interactive elements that meet WCAG 2.5.8 (24 by 24 CSS pixels, or the spacing exception) in a render at 320 CSS pixels wide. Starting target on the pattern page: 100% (tune it).
**Maturity:** Tests written; not yet run.

These tests check whether a widget shows the failure. They are not a score for any product. All stores, dates, and people below are invented and labeled fake. Setting: a web chat widget on a phone. Where a scenario involves the look of the widget, the rendered state is described in words, and the check is a measurement (box size, gap, scroll width), not a screenshot.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Meet the floor on every control | Chips, card buttons, send, and close are at least 24 by 24 CSS px or pass the spacing exception; chips and primary buttons meet your 44-48 px starting target | A control under 24 px with no spacing exception |
| R2 | 2. Space targets apart | At least 8 px between adjacent tappable controls, both directions | Controls touching or closer than 8 px |
| R3 | 3. Rows wrap or stack; no forced sideways scroll | At 320 CSS px wide, chips wrap and card buttons go full width; nothing needed to answer is clipped | A row runs off the right edge, or the page scrolls sideways |
| R4 | 4. A carousel can be used without swiping | Next and previous buttons that meet R1, a peek of the next card, a "Show all as a list" option, and about 5 cards or fewer | Swipe is the only way, or the list alternative is missing |
| R5 | 5. Keep links from crowding | One link per line or button when a message has several; an in-sentence link is still styled distinctly | Two links in adjacent words |
| R6 | 6. Short, distinct labels that fit | Labels wrap to two lines or are shortened; no two chips look identical | Truncated labels that look the same |
| R7 | 7. Keep typing open and confirm risky taps | The user can type the answer; after a tap that books, pays, or deletes, the bot shows what was chosen and offers undo or "change" | Typing blocked, or a booking confirmed without showing the choice |
| R8 | 8. Test the real thing | Checked at 320 CSS px, with enlarged text, in portrait and landscape, on at least one small phone | Only tested on a desktop browser |
| R9 | Hand-off rule | After two mis-taps or "I can't tap", the bot stops buttons for that step, asks in words, and offers a person if it still fails | The bot shows the same chips again |
| R10 | Don't over-correct | 2-4 likeliest options plus "Something else", with "More" where more exist | One option per screen forcing six messages of scrolling, or needed options hidden |

## Conversations
1. **Chip size (small-targets-and-small-screens; R1).**
   Setup: Fake furniture store Harbor Furniture (fake). Widget at 320 CSS px wide. The delivery reply has six date chips, each 18 px tall.
   User: (sees the chips)
   Expect: Fail on R1 for the chips. A passing widget shows chips of 44-48 px height, and none under 24 by 24 px.
   Failing reply: Six chips, 18 px tall, labeled "Tue 3", "Wed 4", and so on.

2. **Gap between chips (small-targets-and-small-screens; R2).**
   Setup: Same widget. Three chips are 48 px tall with a 2 px gap.
   User: (sees the chips)
   Expect: Fail on R2: the gap is under 8 px. A passing widget leaves 8 px or more horizontally and vertically.
   Failing reply: Large chips set edge to edge.

3. **Wrap at 320 px (small-targets-and-small-screens; R3).**
   Setup: Same widget at 320 CSS px wide. The bot offers six delivery days.
   User: (opens the widget)
   Expect: The reply shows the likeliest few days as full-width buttons that stack, with "More days" and "Something else". Scroll width does not exceed client width.
   Failing reply: A single row of chips with a right arrow, partly clipped, needing a sideways swipe.

4. **Carousel without swiping (small-targets-and-small-screens; R4).**
   Setup: Fake shoe store Pace & Co (fake). The bot shows four running shoes in a carousel at 320 px wide.
   User: "show me trail shoes under $120"
   Expect: Previous and next buttons that meet R1, a peek of the next card, and a "Show all as a list" option.
   Failing reply: Cards that change only by swipe, no list option.

5. **Carousel size (small-targets-and-small-screens; R4, R10).**
   Setup: Same store. A search returns nine matching shoes.
   User: "trail shoes"
   Expect: About five cards or fewer, best match first, with "More" to see others.
   Failing reply: Nine cards in one carousel.

6. **Three links in one message (small-targets-and-small-screens; R5).**
   Setup: Same store. The bot answers a shipping question and points to three pages: the shipping policy, the returns policy, and the size guide.
   User: "how does shipping and returns work"
   Expect: A direct answer in text, then each link on its own line or in its own button, none touching another.
   Failing reply: "See shipping policy returns policy size guide" as three links in a row on one line.

7. **Distinct labels (small-targets-and-small-screens; R6).**
   Setup: Same store. Two delivery dates: Thu, Oct 5 and Thu, Oct 12 (fake dates).
   User: "when can you deliver"
   Expect: Labels such as "Thu, Oct 5" and "Thu, Oct 12" wrap or shorten, and the two stay distinct.
   Failing reply: Two chips that both read "Thu, Oc..." after truncation.

8. **Confirm after the tap (small-targets-and-small-screens; R7).**
   Setup: Same furniture store. The user taps the chip "Thursday, Oct 5".
   User: (taps the chip)
   Expect: "Delivery set for Thursday, Oct 5. Reply 'change' to pick another day." The user types "change" and picks another date without restarting.
   Failing reply: "Great, your delivery is booked." with no date and no way to change.

9. **Typing stays open (small-targets-and-small-screens; R7).**
   Setup: Same store. The bot shows three date buttons.
   User: "friday the 6th"
   Expect: The bot handles the typed date and confirms Friday, Oct 6.
   Failing reply: "Please choose one of the options above."

10. **Two mis-taps in a row (small-targets-and-small-screens; R9).**
    Setup: Same store. The user tapped a chip, said "no wrong one", and the bot showed the same chips again.
    User: "wrong again, I keep hitting the wrong one"
    Expect: The bot stops showing buttons for this step, asks "Which day do you want?" in words, and offers a person if typing also fails.
    Failing reply: A third identical row of small chips.

11. **Large text and landscape (small-targets-and-small-screens; R8).**
    Setup: Same widget on a small phone with text enlarged to 200%, in landscape.
    User: (opens the widget)
    Expect: No clipped options, targets still meet R1 and R2.
    Failing reply: Chips that overlap or fall off the screen once text is enlarged.

12. **Do nothing special: widget already passes (small-targets-and-small-screens; R10).**
    Setup: Same widget. Options are three full-width 48 px buttons, 8 px apart, plus "Something else", with typing open.
    User: "when can you deliver"
    Expect: Pass as is. No change, no extra confirmation, no added message.
    Failing reply: Reflowing to one option per screen "to be safe".

13. **Do nothing special: one in-sentence link (small-targets-and-small-screens; R5, R10).**
    Setup: Same store. The bot answers a question with one link inside a sentence, styled with an underline.
    User: "where's your size guide"
    Expect: Pass. A single inline link is exempt from the size rule and does not need its own button.
    Failing reply: Splitting the sentence to make a button for one link.

14. **Do nothing special: user prefers typing (small-targets-and-small-screens; R7, R10).**
    Setup: Same store. The bot offered three date buttons; the user types "next Wednesday".
    User: "next wednesday"
    Expect: The bot accepts the typed answer, confirms the date in words, and does not scold the user for not tapping.
    Failing reply: "Tap one of the buttons to continue."

## Cannot be judged from a transcript alone
- **R1, R2, R3.** Sizes, gaps, and overflow need a measurement of the rendered widget at 320 CSS px (for example box sizes and scroll width), not chat text.
- **R4, swipe behavior.** Needs the real widget on a touch screen.
- **R8, the physical phone.** At least one small physical phone is required.
- **Mis-tap rate.** Needs production tap logs, not fourteen scenarios.
- **Compliance.** Whether WCAG 2.5.8 is required for your product is for your accessibility reviewer.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests, and record the viewport and device.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
