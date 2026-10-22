# Test File: Accessibility Gaps in the Chat Visual Layer

This file is a set of chat test conversations for people who build or review a chat assistant with cards, buttons, charts and images, and want to check whether its critical flows meet the contrast, text-alternative, focus and announcement rules in the fix.

**Pattern:** [Chatbot Accessibility Problems: Poor Contrast, Missing Alt Text, Accessibility Gaps](../goals/visual/failures/accessibility-gaps.md)
**Pattern ID:** accessibility-gaps
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes. Here: critical flows meet WCAG 2.2 AA.
**Primary metric:** Automated plus manual WCAG 2.2 AA pass rate on critical flows. Starting target: 100% (a starting point; tune it).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Where a scenario has a card, chart or button, the setup describes it in words; the harness shows the agent the card spec and the render event. Voice and web-analytics versions are planned, never measured.

**Read this first.** This is design guidance for testing your own product. It is not legal or professional advice, and no accessibility specialist or lawyer has reviewed it. A transcript cannot show a real contrast ratio or a real screen-reader output. Those checks need the render event or a person with the tool. A passing run here is not WCAG conformance.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. List the critical flows and check each state | 3 to 5 named flows, each tested closed, open, card, button, error and done | Only the empty widget is checked, or states are skipped |
| R2 | 2. Text meets contrast | Bubble, card, hint and timestamp text is 4.5:1 or better (3:1 large), in light and dark | A text and background pair under 4.5:1 is sent or called fine |
| R3 | 3. Controls and states meet 3:1 | Button, chip, input and focus-ring colors are 3:1 or better, unrounded | A control pair under 3:1, or 2.999:1 called a pass |
| R4 | 4. No meaning by color alone | Status such as "Ready" or "Failed" also appears as words | Status shown only as a color or an icon |
| R5 | 5. Every image, chart and generated visual has a text alternative | Short alt that states the point, plus data or "Show as table"; decoration marked | Empty alt on informative visuals, or an image shown that the model cannot describe |
| R6 | 6. Every control is real, labeled, focusable, with a visible ring | Native control, a label that says the result, ring never removed | A look-alike element, no label, or the ring removed |
| R7 | 7. New replies and results are announced without moving focus | A live region or role announces the reply and the action result | The result appears silently, or focus jumps to announce it |
| R8 | 8. Gate the release | Under 100% blocks the release or ships with a named owner and date | Ships with a lower pass rate and no owner |
| R9 | Hand-off rule | After a user cannot read or operate a card, or two attempts fail, sends the answer as plain text and offers a person | Resends the same card, or gives no route to a person |
| R10 | Don't over-correct | Visuals stay, with text added. Alt is short. Only needed updates are announced | Cards and charts stripped to pass a scan, long alt on decoration, every small update announced |

## Conversations
1. **Test plan for one flow (R1).**
   Setup: Fake pharmacy "Northfield Pharmacy". A developer asks the assistant to help plan an accessibility check for the refill flow.
   User: "we're about to launch refill in the chat widget. how should we test it for accessibility?"
   Expect: Names the refill flow and its states (widget closed, open, a card, a button, an error, done) and says to scan and check by hand.
   Failing reply: "Run a scan on the chat window and you're done."

2. **Gray hint text on a card (R2).**
   Setup: Fake pharmacy "Northfield Pharmacy". The refill card spec sets hint text to #9AA0A6 on a white bubble. The harness reports that pair is under 4.5:1.
   User: "Refill my lisinopril."
   Expect: Sends the card with hint text changed to a pair at 4.5:1 or better, or flags the token pair before sending.
   Failing reply: Sends the card with the under-4.5:1 pair and says "Looks good."

3. **Focus ring too faint (R3).**
   Setup: Fake bank "Harbor Credit Union". The [Pay bill] button's focus ring is a light blue the harness reports at 2.999:1 against the card.
   User: "Is the Pay bill button okay for keyboard users?"
   Expect: Says 2.999:1 fails the 3:1 rule, because values are not rounded, and asks for a darker ring.
   Failing reply: "That's basically 3:1, so it passes."

4. **Status by color only (R4).**
   Setup: Fake pharmacy "Northfield Pharmacy". The refill card shows a green dot for ready and no word.
   User: "Is my refill ready?"
   Expect: The answer says "Ready for pickup Friday" in words, and the card includes the word "Ready".
   Failing reply: "See the green dot on the card."

5. **Chart with no alt (R5).**
   Setup: Fake pharmacy "Northfield Pharmacy". The harness has a "pickups this year" chart image with no alt field. The data shows 2 to 4 pickups each month.
   User: "How many pickups did I do this year?"
   Expect: States the point in text (2 to 4 each month), gives the chart a short alt, and offers [Show as table].
   Failing reply: Shows the chart with empty alt and "Here's your chart."

6. **Generated image it cannot describe (R5).**
   Setup: Fake insurer "Cedar Health". The assistant made an image of a claim timeline. It has no reliable description. This is a claim flow.
   User: "Where is my claim?"
   Expect: Does not show the image. Gives the status as text and offers the data.
   Failing reply: Shows the image with alt "image".

7. **A decorative icon (R5, R10).**
   Setup: Fake pharmacy "Northfield Pharmacy". The card has a small leaf icon next to the store name. It carries no information.
   User: "What time does the pharmacy close today?"
   Expect: The icon is marked decorative so a screen reader skips it. No long alt. Nothing special is needed.
   Failing reply: Alt text of three sentences describing the leaf.

8. **Look-alike button (R6).**
   Setup: Fake bank "Harbor Credit Union". The [Confirm pickup] control is a styled span with no role and no label. The harness shows its role and name as empty.
   User: "Can I confirm with the keyboard?"
   Expect: Says Tab cannot reach it, and the control must be a native button named "Confirm pickup".
   Failing reply: "Yes, press Tab and then Enter."

9. **Result announced silently (R7).**
   Setup: Fake pharmacy "Northfield Pharmacy". A screen-reader user presses [Confirm pickup]. The result text "Confirmed: pickup Friday" appears with no live region.
   User: (presses Enter on Confirm pickup)
   Expect: The result is announced without moving focus.
   Failing reply: The text appears in silence, or focus jumps to the message.

10. **Ship at 96% (R8).**
    Setup: Fake bank "Harbor Credit Union". A product manager reports 24 of 25 flow states pass and asks to ship today.
    User: "24 of 25 pass. ship it?"
    Expect: Says under 100% blocks the release unless a named owner and date are recorded for the failing state.
    Failing reply: "96% is great, ship it."

11. **Cannot read the card (R9).**
    Setup: Fake pharmacy "Northfield Pharmacy". The user already said once that the card is unreadable. A phone line exists.
    User: "i still can't read this card"
    Expect: Gives the refill answer as plain text and offers a person, with a one-line summary.
    Failing reply: Resends the same card.

12. **Strip it all (R10).**
    Setup: Fake insurer "Cedar Health". A developer wants the scan to pass.
    User: "can we just remove the charts and colors so the scan passes?"
    Expect: Says to keep the visuals and add text alternatives and words. Stripping is not the fix.
    Failing reply: "Yes, delete the charts and use plain gray."

13. **Plain question, nothing special (R10).**
    Setup: Fake pharmacy "Northfield Pharmacy". No card, chart or button is needed.
    User: "do you take Medicare?"
    Expect: A short text answer. No added visual, no accessibility lecture.
    Failing reply: A card, a chart and a note about screen readers.

14. **Already accessible, nothing special (R10).**
    Setup: Fake pharmacy "Northfield Pharmacy". The user says they use a screen reader. The card already has 4.5:1 text, a word status, a native button and a live region.
    User: "I use a screen reader. Refill my lisinopril."
    Expect: Sends the refill card as is and the answer in text first. No extra announcements.
    Failing reply: Strips the card or announces every small update.

## Cannot be judged from a transcript alone
- **Contrast ratios and focus-ring ratios.** They need the rendered theme token pairs, in light and dark.
- **Screen-reader output and Tab order.** They need a person using the tool on the real widget.
- **Live-region behavior and focus.** They need the render and accessibility-tree events.
- **Pass rate on critical flows.** It needs a scan plus a manual checklist per flow state, each release.
- **Visual-related complaints (counter-metric).** They need production events. Watch it; do not chase it.
- **Voice and web-analytics versions.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
