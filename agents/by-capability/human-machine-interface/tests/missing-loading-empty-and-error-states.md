# Test File: Card Shows a Blank Box or Endless Spinner (Missing Loading, Empty, and Error States)

This file is a set of chat test conversations for people who build or review a chat assistant with cards or widgets that load data, and want to check whether each one says if it is loading, empty, or failed.

**Pattern:** [Chatbot Card or Widget Shows a Blank Screen or Endless Spinner: Missing Loading, Empty, and Error States](../goals/visual/failures/missing-loading-empty-and-error-states.md)
**Pattern ID:** missing-loading-empty-and-error-states
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes.
**Primary metric:** States defined on 100% of async views; blank-screen rate 0. Starting targets to tune.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Where a scenario has a card or widget, the setup describes it in words; the harness shows the agent the view spec, the fetch event and the render log. Voice and web-page versions are planned, never measured.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Define all three states before building the success view | Every async view on the spec has a loading, an empty and an error design | A view has only the success design, or one state is left to a browser default |
| R2 | 2. Loading at once, with a time limit | Loading text shows when the fetch starts, a slow message follows, and the error state shows at the timeout | A blank body, or a spinner that runs past the limit with no change |
| R3 | 3. Separate empty from error | "Empty" is shown only after a fetch that succeeded with zero items; a failed or timed-out fetch shows the error state | A failed fetch shown as "nothing here" |
| R4 | 4. Empty says why and what next | Says the fetch worked and found nothing, a likely reason, and one action | "No results" alone, or a paragraph |
| R5 | 5. Error says what failed, what is unchanged, and what to do | Cause in plain words, whether anything changed (only if true), one next step | "Something went wrong", or a claim that nothing changed when the log does not show it |
| R6 | 6. Announce state changes in text | State text sits in a status region, `aria-busy` is set while loading and cleared on every exit, error included | Color or motion only, or `aria-busy` left true after an error |
| R7 | 7. Fall back to chat text | If the widget cannot render, the reply states the same condition in words | The user is left with only a missing or empty card |
| R8 | 8. No spinner as the only signal for a long wait | For a wait the system knows is long, the view shows progress or what is happening | A bare spinner for a known long job |
| R9 | Don't over-correct | No loading text on a view that returns in a fraction of a second; no announcement of every update; no paragraph in an empty state | A flash of loading text on a fast load, a status message per row, or a long essay |

## Conversations
1. **Spec has only the success view (R1).**
   Setup: Fake retailer "Cobblestone Books". A new "Open orders" card is about to ship. The spec describes only the card with orders in it.
   User: "show my open orders"
   Expect: Before the card renders, the spec is fixed with loading, empty and error designs. The user gets a state, not a blank body.
   Failing reply: The card renders with an empty body and no state tag.

2. **Fetch never returns (R2).**
   Setup: Fake bank "Harbor Credit". The data call for the "Recent transactions" card never returns. The log shows 40 seconds elapsed.
   User: "hello? did that work?"
   Expect: Says the card is still not loaded, that it timed out, and offers Try again, Contact support, Something else.
   Failing reply: "Your transactions are loading." Card unchanged.

3. **Loading starts at once (R2).**
   Setup: Fake clinic "Lakeview Dental Group". The "Open appointments" card fetch takes 5 seconds.
   User: "what appointments do I have?"
   Expect: "Loading your appointments" shows the moment the fetch starts, and the card never has a blank body.
   Failing reply: A blank card for 5 seconds, then the list.

4. **Empty list that did load (R3, R4).**
   Setup: Fake retailer "Pinecrest Home". The fetch succeeded and returned zero open orders.
   User: "show my open orders"
   Expect: "You have no open orders. Orders you place will appear here." plus one action, such as [Browse items].
   Failing reply: "No results."

5. **HTTP error shown as empty (R3).**
   Setup: Fake utility "Bluewater Power". The fetch event has error code 503. The old logic shows "No bills found."
   User: "what bills do I owe?"
   Expect: The error state: the bills could not be loaded, nothing was changed, and a next step. It does not say "no bills".
   Failing reply: "You have no bills due."

6. **Malformed payload (R3, R5).**
   Setup: Fake insurer "Brightwell Insurance". The claims fetch returns a payload the card cannot read. The log shows a parse error and no write.
   User: "where's my claim?"
   Expect: Says it could not read the claim data, says nothing was changed because the log shows no write, and offers Try again or Contact support.
   Failing reply: "No claims on file."

7. **Generic error text (R5).**
   Setup: Fake airline "Skyline Air". The "Upcoming flights" fetch fails with a timeout. The card reads "Something went wrong."
   User: "show my flights"
   Expect: Names the cause in plain words (the flight system did not respond), says nothing was changed, and gives one next step.
   Failing reply: "Something went wrong. Please try again later."

8. **Screen reader user waits (R6).**
   Setup: Fake clinic "Lakeview Dental Group". A screen reader is in use. The card shows loading text in a plain div with no status role.
   User: "I pressed the button and my screen reader said nothing"
   Expect: Says what state the card is in, in the message. The spec is fixed so the text sits in a status region and `aria-busy` is cleared at the end.
   Failing reply: "It's loading on the card."

9. **Busy flag after an error (R6).**
   Setup: Fake bank "Harbor Credit". The fetch errored. The render log shows `aria-busy` still true on the card.
   User: "is the card still loading?"
   Expect: Says it failed, not that it is loading. The spec is fixed so `aria-busy` clears on error.
   Failing reply: "Yes, still loading."

10. **Widget will not mount (R7).**
    Setup: Fake retailer "Cobblestone Books". The chart widget failed to mount. The log shows the mount error.
    User: "show my spending by month"
    Expect: The reply says the chart could not be shown and why, in text, and offers Try again or the figures as a list.
    Failing reply: "Here is your spending:" with nothing under it.

11. **Known long job, spinner only (R8).**
    Setup: Fake insurer "Tallgrass Insurance". The "Year-end statement" card builds in about 40 seconds. The harness knows this.
    User: "make my year-end statement"
    Expect: Says it is building the statement, what step it is on, and offers Cancel. Not a bare spinner.
    Failing reply: A spinner alone for 40 seconds.

12. **Fast load, nothing special (R9).**
    Setup: Fake streaming service "Streamly". The "Current plan" card returns in 150 ms.
    User: "what plan am I on?"
    Expect: The card appears with the plan. No loading text flashes.
    Failing reply: "Loading your plan" flashes for a blink.

13. **Empty state, nothing special (R9).**
    Setup: Fake pharmacy "Maple Rx". The fetch worked and returned zero refills due. There is no sensible action.
    User: "any refills due?"
    Expect: One short line: no refills are due now. No action button is forced, and no paragraph.
    Failing reply: Three paragraphs on refills, plus a button to nowhere.

14. **Same view fails twice (R5).**
    Setup: Fake bank "Harbor Credit". The "Recent transactions" view has failed twice in a row. A support queue exists.
    User: "it's broken again"
    Expect: Offers a person and passes the view name, the error reference and what the user tried. Does not loop back to Try again alone.
    Failing reply: "Please try again."

## Cannot be judged from a transcript alone
- **States defined on every async view.** It needs the view inventory checked against the spec list.
- **Blank renders.** It needs the render log scanned for an empty body with no state tag.
- **Status-region and `aria-busy` behavior.** It needs an accessibility-tree check or a screen reader walkthrough.
- **Failed fetch rendered as empty.** It needs the fetch event and the render event for the same view.
- **Loading messages on fast loads (counter-metric).** It needs production render times.
- **Voice and web-page versions.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
