# Test File: Visuals That Don't Localise

This file is a set of chat test conversations for people who build or review chat assistants that show cards, carousels, charts, icons or generated images to users in more than one locale, and want to check whether those visuals mirror, label and lay out correctly outside US English.

> **Read this first.** Every expected label, icon decision and layout below is a test setting, not a statement of what any locale's users understand. A native reader of each test locale must review the visuals and these tests before use, as the pattern page requires. User turns typed in another language are shown here in English, marked "(typed in Arabic)" or similar. If you add the original non-English text to a run, a qualified translator must check it before use. Whether a gesture or color is a problem in a locale is a reviewer's decision; this pack never settles it.

**Pattern:** [Chatbot Icons, Colors and Arrows Confuse in Other Locales: Visuals That Don't Localise](../goals/visual/failures/visuals-that-don-t-localise.md)
**Pattern ID:** visuals-that-don-t-localise
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes. (Row goal: visuals work in each supported locale.)
**Primary metric:** RTL render pass; icon comprehension in test locales. Target: 100% of RTL render cases pass; comprehension target set from your first test round (starting point to tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies and people below are invented and labeled (fake). Text chat with cards; each expected answer describes the rendered card in words. Voice is planned on the pattern page and is not tested here. How text, numbers and punctuation are drawn inside a line (date order, decimal marks, mixed scripts) belongs to the [right-to-left and mixed-script rendering tests](right-to-left-and-mixed-script-rendering.md) and is not tested here. The setup holds the fake product, the user's locale and reading direction, the widget's mirror table (each icon marked mirror, keep, or locale variant), the locale's string table, the native-review log (which icons and locales a reviewer approved or changed), whether a person is available for hand-off, and the earlier turns. The default fake product is "Lakeshore Rx" (fake), a prescription refill chat run by "Lakeshore Pharmacy Inc." (fake). Its default test user lives in Dearborn, Michigan, and has the app set to Arabic, a right-to-left locale with a completed native review. The choices offered after a confusion report are the pattern page's: "Show text buttons", "Show a simple list", "Talk to a person", "Something else".

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a mirror table for every icon | Every icon on the rendered card has a mirror, keep, or locale-variant mark in the table; an unmarked icon stops the release check | A card renders with an icon that has no mark, and nothing flags it |
| R2 | 2. Mirror icons that carry direction | In RTL, back, next, forward, send and collapse-toward-a-side icons are flipped; "next" points in the reading direction | A direction icon is drawn the same as in English, so "next" points toward the first card |
| R3 | 2. Keep icons that do not carry direction | In RTL, charts, graphs, numbers, clocks, checkmarks, camera-type icons, media controls and logos are drawn the same as in English | A chart's time axis is reversed, digits are reordered, or a play button or progress bar is flipped |
| R4 | 3. A visible word next to every action icon | Each icon that triggers an action has a visible label from the locale's string table and an accessible name | An icon-only action button in any locale, or a label that only appears for screen readers |
| R5 | 4. Layout from reading direction | Card order, carousel order, button order and the primary action's side follow the locale; in RTL the first card is at the right edge and the primary action is on the reading-start side | The English left-to-right order is kept in RTL, or order is set by "left" and "right" instead of reading direction |
| R6 | 5. No text inside images or generated visuals | Every string on a card is selectable text that is translated, resizes and mirrors with the card | Any word baked into an image, banner or generated visual |
| R7 | 6. Color or a gesture symbol is never the only carrier of meaning | Status colors come with a word and a shape; thumbs, flags, hand symbols and colors with a possible local meaning come with a word and appear only as the review log allows for that locale | A color-only status, a language flag with no reviewer approval, or a symbol shown against the review log's decision |
| R8 | 7. Test each supported locale; fallback for an unreviewed locale | A locale with no reviewed visuals gets the English-reviewed set with labels from its string table, and the release notes say so | Unreviewed locale variants are shown, or the locale's visuals are dropped |
| R9 | Moves: admit uncertainty, then offer choices | When the user says a control is unclear or wrong-way, the bot restates the action in words and does not claim to see the screen; after a "this is confusing" report it offers the four choices | The bot insists the control is right, claims to see the display, or ignores the report; or it offers the choices when the card already has labeled buttons and the user only wants the answer |
| R10 | Hand-off rule | On a second confusion report, the card ID and locale are logged and the user is handed to a person with the card text attached; no fix date is promised | No hand-off after a second report, the person gets no card text, or the bot promises a fix by a date |
| R11 | Don't over-correct | English layouts stay unchanged and left-to-right; only direction icons mirror; icons are not replaced with text-only cards; a locale's visuals are not dropped over one icon; no color or gesture is called offensive without a reviewer's decision | Every icon is mirrored, an English card is mirrored, a reviewed icon is removed, or the bot calls a symbol offensive on its own |

## Conversations
1. **Carousel "next" chevron in Arabic (R2).**
   Setup: Lakeshore Rx (fake). Arabic locale, RTL. The user, "Samir Haddad" (fake), has a refill ready at three pickup stores. The mirror table marks the next and previous chevrons as mirror.
   User (typed in Arabic): "where can i pick it up"
   Expect: A carousel card, "Store 1 of 3", with the chevrons flipped: the "next" chevron points in the reading direction, toward store 2.
   Failing reply: The same carousel drawn as in English: the right chevron still points right and takes the user back toward store 1.

2. **Carousel order in Arabic (R5).**
   Setup: Same as conversation 1.
   User (typed in Arabic): "show me all 3 stores"
   Expect: Store 1 is the card at the right edge, store 3 at the left edge, and the primary "Choose this store" button sits on the reading-start (right) side of each card.
   Failing reply: Store 1 at the left edge and the primary button on the left, as in the English layout.

3. **Spending chart in Hebrew (R3).**
   Setup: "Fernwood Credit Union" (fake) chat. Hebrew locale, RTL. The user, "Noa Levin" (fake), has six months of card spending on file. The mirror table marks charts as keep.
   User (typed in Hebrew): "can u show my spending by month as a chart"
   Expect: A line chart drawn the same as the English one: the oldest month on the left, the newest on the right. The chart title, axis labels and legend are Hebrew text from the string table.
   Failing reply: The chart flipped to match the layout, with the newest month on the left and the line running the other way.

4. **Numbers on chart labels in Arabic (R3).**
   Setup: Lakeshore Rx (fake). Arabic locale, RTL. The user's refill cost history is on file; one month's total is $1,250.
   User (typed in Arabic): "chart of what i paid for refills this year"
   Expect: A bar chart drawn the same as in English, with each value label reading in normal digit order, for example "$1,250".
   Failing reply: The value label reversed by the mirroring step, so the digits read "052,1$".

5. **How-to video card in Hebrew (R3).**
   Setup: Fernwood Credit Union (fake). Hebrew locale, RTL. The mirror table marks media play and the progress bar as keep.
   User (typed in Hebrew): "is there a video on how to deposit a check with the app"
   Expect: A video card whose play triangle points the same way as in English and whose progress bar fills in the same direction as in English. The card's text and buttons follow the RTL layout.
   Failing reply: The play triangle flipped to point left and the progress bar filling from the right.

6. **Feedback icons with no words (R4).**
   Setup: Lakeshore Rx (fake). Arabic locale. The bot has just answered a question about store hours. The widget shows a feedback row after each answer.
   User (typed in Arabic): "thanks"
   Expect: The feedback row shows the thumbs-up with the visible word "Helpful" and the thumbs-down with "Not helpful", both from the Arabic string table, and each has an accessible name.
   Failing reply: A thumbs-up and a thumbs-down with no visible words.

7. **Icon-only toolbar on an order card (R4).**
   Setup: Lakeshore Rx (fake). Spanish (United States) locale, left-to-right. The order card has three actions: edit, cancel order, and share.
   User (typed in Spanish): "show me my order"
   Expect: Each action has a visible word next to its icon from the Spanish string table, so "Cancel order" is readable without guessing what the icon means.
   Failing reply: A pencil, a trash can and a share icon in a row with no words, so the cancel action can only be guessed from the trash can.

8. **Order status shown by color (R7).**
   Setup: Lakeshore Rx (fake). Arabic locale. The order is ready for pickup. The card template uses a status chip.
   User (typed in Arabic): "is my refill ready"
   Expect: A status chip with a word ("Ready") and a shape (a checkmark) as well as its color.
   Failing reply: A plain green dot with no word and no shape.

9. **Text baked into a card banner (R6).**
   Setup: Lakeshore Rx (fake). Arabic locale. The pickup card template has a banner image.
   User (typed in Arabic): "send me the pickup details"
   Expect: Every string on the card ("Ready for pickup", the store name, the pickup hours) is selectable Arabic text. The banner image holds no words.
   Failing reply: A banner image with "READY FOR PICKUP" in English drawn into the picture, above Arabic text.

10. **Larger text setting (R6).**
    Setup: Fernwood Credit Union (fake). English (United States) locale. The user has set the app's text size to the largest setting. The account card has a header graphic.
    User: "whats my balance"
    Expect: All card text, including the header's words, grows with the text setting, because it is text and not part of an image.
    Failing reply: The body text grows but the header's "Account summary" stays small because it is drawn into the header graphic.

11. **Language picker with a flag (R7).**
    Setup: Lakeshore Rx (fake). Spanish (United States) locale. The review log has no approval for language flags in any locale.
    User (typed in Spanish): "can i switch this to english"
    Expect: A language choice shown as words ("English", "Español"), with no national flags.
    Failing reply: A row of national flags as the only way to pick a language.

12. **Locale with no reviewed visuals (R8).**
    Setup: Lakeshore Rx (fake). Vietnamese locale, left-to-right. The setup says no native review of visuals has been done for Vietnamese yet; a draft Vietnamese icon variant set exists but is unreviewed. The string table for Vietnamese is complete.
    User (typed in Vietnamese): "where do i pick up my refill"
    Expect: The card uses the English-reviewed icon set with visible labels from the Vietnamese string table. Judged together with the release notes, which say Vietnamese is using the English-reviewed set.
    Failing reply: The card uses the unreviewed Vietnamese variant icons, or shows a text-only reply because the locale has no reviewed visuals.

13. **"Which arrow is next?" (R9).**
    Setup: Lakeshore Rx (fake). Arabic locale. The bot has shown the three-store carousel from conversation 1.
    User (typed in Arabic): "which arrow goes to the next store, this is confusing"
    Expect: Restates the action in words without claiming to see the screen, for example: "The next store is the one after this one, store 2 of 3." Then offers "Show text buttons", "Show a simple list", "Talk to a person" and "Something else", with free text still open.
    Failing reply: "The arrow on the right is clearly the next button." (the bot claims to know what the user sees and does not offer choices)

14. **Second confusion report (R10).**
    Setup: Lakeshore Rx (fake). Arabic locale. The user reported the carousel arrows as confusing once and chose "Something else". A pharmacy staff member is available for hand-off.
    User (typed in Arabic): "the arrows still go the wrong way, i cant find store 2"
    Expect: Hands off to the staff member with the card text attached (the three stores and their hours), so the user does not repeat anything. The card ID and locale are logged. No promise of when the display will be fixed.
    Failing reply: "Sorry about that! Our team will fix the arrows by next week. Try tapping the other arrow."

15. **New icon missing from the mirror table (R1).**
    Setup: Lakeshore Rx (fake). The harness adds a "collapse panel" icon to the refill card template without adding it to the mirror table, then runs the release render check in Arabic and Hebrew.
    User (typed in Arabic): "show my refill history"
    Expect: Judged from the release check: the unmarked icon fails the check, and the card template is not released until the icon is marked.
    Failing reply: The card ships with the new icon drawn the English way and no check failure recorded.

16. **Do nothing special: English carousel (R11).**
    Setup: Lakeshore Rx (fake). English (United States) locale, left-to-right. The user, "Karen Mitchell" (fake), has a refill ready at three stores.
    User: "where can i pick it up"
    Expect: The same carousel as before the fix: store 1 at the left edge, the "next" chevron pointing right, labeled buttons. Nothing is mirrored.
    Failing reply: An English carousel drawn right to left, with store 1 at the right edge.

17. **Do nothing special: labeled card, user only wants the answer (R9, R11).**
    Setup: Lakeshore Rx (fake). Arabic locale. The pickup card already has labeled "Next" and "Previous" buttons. The user has made no confusion report.
    User (typed in Arabic): "what time does store 2 close"
    Expect: Gives store 2's closing time. No offer of "Show text buttons" or the other choices, and no swap to a text-only card.
    Failing reply: "Here are the hours. Would you like to: Show text buttons, Show a simple list, Talk to a person, or Something else?"

18. **Do nothing special: reviewer-approved thumbs-up (R11).**
    Setup: Lakeshore Rx (fake). Arabic locale. The review log shows a native reviewer approved the thumbs-up and thumbs-down icons with the words "Helpful" and "Not helpful" for Arabic.
    User (typed in Arabic): "ok got it"
    Expect: The feedback row shows the thumbs icons with their words, as approved. No warning about the gesture and no removal of the icons.
    Failing reply: The feedback row removed for Arabic, or a note such as "We've hidden the thumbs-up because it may be offensive in your region."

## Cannot be judged from a transcript alone
- **The primary metric.** RTL render pass needs the render cases run on each release and widget change; icon comprehension needs 5 or more people from each test locale to name each icon without its label, against a target set from the first round. Eighteen conversations do not measure either.
- **R1, the mirror table.** Whether every icon is marked needs the icon table and the release check log, not only the card.
- **R4, accessible names.** Needs the rendered card's accessibility tree or a screen reader, not only the visible text.
- **R6, selectable text.** Needs the rendered card, not a text description of it.
- **R7 and R8, the review log and release notes.** Whether a reviewer approved a symbol for a locale, and whether the release notes name the fallback, needs those records.
- **What the hand-off passed (R10).** The receiving person's view, and the log entry with card ID and locale, show whether the card text arrived.
- **Whether the expected labels and layouts are right.** Every expected answer here is a test setting. A native reader of each test locale must review it.
- **Voice and a site-wide web check.** Planned on the pattern page, not tested here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |

## Related
- [Pattern page: Visuals That Don't Localise](../goals/visual/failures/visuals-that-don-t-localise.md)
- [Right-to-left and mixed-script rendering tests](right-to-left-and-mixed-script-rendering.md)
- [Colour-only encoding tests](colour-only-encoding.md)
- [Rich-card misuse tests](rich-card-misuse.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Test file format](README.md)
