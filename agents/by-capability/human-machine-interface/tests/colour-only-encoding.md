# Test File: Color-Only Encoding

This file is a set of chat test conversations for people who build or review assistants that show cards, status chips, tables, or charts, and want to check whether theirs shows status, risk, or priority by color alone.

> **Read this first.** These are test conversations only. They are design guidance, not legal or accessibility-compliance advice. An accessibility expert should review the pack before you rely on it, and your own users with color vision deficiency and screen readers should test the real widget. Expected behavior below names what the pattern page requires, not exact words.

**Pattern:** [Chatbot Status Colors: Color-Only Encoding in Cards, Chips, Charts and Tables](../goals/visual/failures/colour-only-encoding.md)
**Pattern ID:** colour-only-encoding
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes.
**Primary metric:** Share of status, risk, and priority items (chips, card badges, chart series, table cells) that carry a non-color cue: visible text or a distinct shape. Starting target on the pattern page: 100% (tune it).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, invoices, and people below are invented and labeled fake. Setting: a text chat widget with rich cards, chips, generated tables, and chart images. Rendered states are described in words, because a transcript cannot show color. For each scenario, check the render payload (text, icon, accessible label) and, where possible, view the card in grayscale and with a screen reader.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Every status, risk, or priority item has visible text | Each item carries a word such as "In stock", "Late", "High risk", "Due Friday" | A dot, bar, or chip with no word |
| R2 | 2. Add a second non-color cue | Each state has its own icon shape, position, or pattern | Two states share a shape and differ only in hue |
| R3 | 3. A standalone chip or icon has an accessible name | The accessible label matches the state, such as "Out of stock" | A chip with no text next to it and no label |
| R4 | 4. Put the answer in the message text | The sentence says which option is in stock or which invoice is overdue | The result lives only in the card |
| R5 | 5. In tables, write the state in the cell | Each row's cell (or an adjacent cell in the same row) says the state | A red or green fill with no state word |
| R6 | 6. In charts, label directly or add a pattern | Series are named on lines or slices, or have different marker shapes or line styles, plus a one-sentence text summary; graphic parts keep the 3:1 contrast floor | Series told apart by hue only, no summary |
| R7 | 7. Keep a legend only as a backup | A legend may appear, but the direct labels or shapes carry the meaning | A color legend is the only key |
| R8 | 8. Check text contrast on every tone | Chip text meets the target your reviewer sets (starting point 4.5:1) | Low-contrast text on any tone |
| R9 | Hand-off rule | A user who says they cannot read the status gets a text version, which is kept for the session, then a person or another channel if it still fails | The bot repeats the colored card, or asks again every turn |
| R10 | Don't over-correct | One word plus one icon per item; color kept as reinforcement; one clear primary action | All color stripped, or a card cluttered with icons, badges, and bold |

## Conversations
1. **Stock card (colour-only-encoding; R1, R2).**
   Setup: Fake store Northfield Outfitters (fake). The Ridgeline 40L pack: Denver 12 in stock, Boulder 2, Fort Collins 0.
   User: "is the ridgeline 40l in stock near me"
   Expect: A card where each store row has a word and count ("In stock (12)", "Low stock (2)", "Out of stock") and a different icon per state, such as a check mark, a warning triangle, and a cross.
   Failing reply: A card with three rows and a green, yellow, and red dot, no words.

2. **Answer in the message text (colour-only-encoding; R4).**
   Setup: Same store and data.
   User: "which store has it"
   Expect: The sentence says "Yes, at Denver" before or beside the card, so a user who skips the card still gets the answer.
   Failing reply: "Here's what I found:" followed only by the card.

3. **Same shape, different hue (colour-only-encoding; R2).**
   Setup: Same store. The card uses a filled circle for every state: green for in stock, orange for low, red for out.
   User: (sees the card)
   Expect: Fail on R2 even if each row has a word. The shapes must differ per state.
   Failing reply: Three identical circles that differ only in fill.

4. **Standalone chip (colour-only-encoding; R3).**
   Setup: Fake bank app HarborPay (fake). A transaction row shows a chip with an icon and no adjacent text. The chip says the payment is pending.
   User: "what's the status of my $84.20 payment" (fake)
   Expect: The chip carries an accessible label "Pending", and the reply text says the payment is pending.
   Failing reply: An unlabeled orange dot, with the reply "See below."

5. **Table with fills (colour-only-encoding; R5).**
   Setup: Fake business tool InvoiceBay (fake). Three invoices: #1041 paid, #1042 overdue by 9 days, #1043 due Friday (all fake).
   User: "show my invoices, overdue ones in red"
   Expect: A table with a Status column that reads "Paid", "Overdue (9 days)", and "Due Friday". Red on the overdue row is allowed as a bonus.
   Failing reply: A table with a red row and a green row and no Status column.

6. **Chart with three series (colour-only-encoding; R6, R7).**
   Setup: Fake gym app Stridely (fake). Weekly minutes for Cardio, Strength, and Yoga across 4 weeks.
   User: "chart my workouts by type"
   Expect: A line chart where each line is named at its right end and has a distinct marker shape, followed by a sentence such as "Cardio is highest every week." A legend may appear but is not the only key.
   Failing reply: Three lines in blue, green, and orange with only a color legend and no summary.

7. **Chart text summary (colour-only-encoding; R6).**
   Setup: Same app. A single-series line chart of weight over 8 weeks.
   User: "graph my weight"
   Expect: One line, labeled axes, and a one-sentence summary of the trend. Color carries no meaning here, so a single hue is fine.
   Failing reply: A chart with no axis labels or text summary.

8. **Chip contrast (colour-only-encoding; R8).**
   Setup: Same store. The "Low stock" chip uses light yellow text on a white background.
   User: (sees the chip)
   Expect: Fail on R8: the text is hard to read against its tone. Measure against the reviewer's target (starting point 4.5:1).
   Failing reply: Pale text on a pale fill that fails the measured ratio.

9. **User says they cannot tell the dots apart (colour-only-encoding; R9).**
   Setup: Same store. The earlier card was color-only.
   User: "which one is the green one? I can't tell them apart"
   Expect: The next reply is a text list ("Denver: in stock, 12. Boulder: low stock, 2. Fort Collins: out of stock"), and later replies in the session stay text-first without asking again.
   Failing reply: "The green dot is the first one." followed by the same colored card on the next turn.

10. **User still cannot read it after the text version (colour-only-encoding; R9).**
    Setup: Same store. The text list was sent; the user is on a screen reader and says the widget reads nothing useful.
    User: "the list still reads wrong, I can't use this"
    Expect: The bot offers a person or another channel with the same facts in a summary.
    Failing reply: Sending the card a third time.

11. **Do nothing special: word plus icon plus color (colour-only-encoding; R10).**
    Setup: Same store. The card already has a word, a distinct icon, and a green tint on in-stock rows.
    User: "is the ridgeline 40l in stock near me"
    Expect: Pass as is. The tint is fine because it only reinforces the word and icon. Nothing is added or removed.
    Failing reply: Stripping all color, or adding extra badges and bold to every row.

12. **Do nothing special: decorative dot beside a word (colour-only-encoding; R1, R10).**
    Setup: Same store. A row reads "Boulder, CO - Low stock (2)" with a small yellow dot before it, and the dot is marked decorative.
    User: (sees the row)
    Expect: Pass. The state is in text and the dot adds nothing the word does not.
    Failing reply: Treating the dot as a failure and rebuilding the row.

13. **Do nothing special: single-series chart (colour-only-encoding; R6, R10).**
    Setup: Same fitness app. A single-series chart in one color with a title and summary.
    User: "graph my weight"
    Expect: Pass. Color carries no meaning, so no pattern or extra marker is needed.
    Failing reply: Adding five marker shapes and a legend to a one-line chart.

14. **Priority chips in a ticket list (colour-only-encoding; R1, R2).**
    Setup: Fake help desk DeskWell (fake). Tickets: #301 high, #302 medium, #303 low.
    User: "list my open tickets"
    Expect: Each ticket shows "High", "Medium", or "Low" plus a different icon per level, and the message text names the high-priority ticket first.
    Failing reply: A red, orange, and gray bar beside each ticket, no words.

## Cannot be judged from a transcript alone
- **R2, R3, R8.** Shapes, accessible labels, and contrast need the render payload or the real widget, not the chat text.
- **Screen-reader output.** What a screen reader says needs the real screen reader and widget. The page's claim about it is our judgment, so test it on the readers your users use.
- **Grayscale check.** It needs the rendered card.
- **Compliance.** Whether WCAG 1.4.1 applies to your product, and at which level, is for your accessibility reviewer.
- **Production rate.** The share of items with a non-color cue needs the payload lint described on the pattern page.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests, and have an accessibility reviewer judge the renders.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
