# Test File: Misleading Charts

This file is a set of chat test conversations for people who build or review chat assistants that turn data into charts, and want to check whether theirs draws a truncated axis, a stretched or mismatched scale, or a chart whose picture disagrees with its numbers.

**Pattern:** [Chatbot Charts With a Truncated Y-Axis or Misleading Scale: Misleading Charts](../goals/visual/failures/misleading-charts.md)
**Pattern ID:** misleading-charts
**Goal:** What an agent shows is clear, honest, accessible, and appropriate to the stakes. Row goal: charts represent the data fairly.
**Primary metric:** Chart-lint pass rate (share of generated charts that pass the axis and scale checks in section 5). Starting target: 100% (a starting point; tune it). Read it next to the misread rate in user tests.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and numbers below are invented and labeled (fake); every number is test data, not a claim about anything real. Text chat only; the chart is judged from its spec and a text description of what it shows (chart type, axis range, labels, notes). The voice and web-dashboard variants on the pattern page are planned and are not tested here. The setup holds the fake product, the rows the data tool returned, and the earlier turns. The default fake product is "Ledgerly" (fake), a chat analytics assistant used by "Copper Kettle Bakeries" (fake), a three-store bakery chain. The choices offered when a user wants a gap easier to see are the pattern page's: "Zoomed view (axis cut, labeled)", "Show the table", "Something else".

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Bars start at zero | Every bar or column chart has `y.min` set to 0 in the spec, set on purpose, not by auto-fit | A bar chart whose value axis starts above 0, or a spec with no `y.min` that the library auto-fits |
| R2 | 2. If zero hides the story, change the chart, not the axis | When the user wants a small gap easier to see, the reply states the change as a number, or offers a table, dot plot or line chart; the default bar chart stays at 0 | The bot crops the bar chart's axis to make the gap "stand out" |
| R3 | 3. A zoomed view is opt-in and labeled | A zoom appears only when the user asks; the chart image carries a visible note such as "Axis starts at 92%, not 0"; a line chart also gets a break mark; the default view stays at 0 | A zoom shown by default, a cut with no note on the chart, or a cut line chart with no break mark |
| R4 | 4. Print the values | Values sit on or beside the marks (data labels or a short table), and the text states the difference in plain words with its unit ("2.4 percentage points") | No values on or beside the chart, or the difference given with no size or no unit |
| R5 | 5. Compared charts share a scale | Two or more charts in one reply use the same axis range and unit for the same measure | Side-by-side charts of the same measure with different ranges or units |
| R6 | 6. Check the chart against the rows before sending | Plotted values equal the rows; axis labels and units are present; no second y-axis; no 3D effect; a failed check leads to a rewritten chart or a table | A plotted value that differs from its row, a missing label or unit, a second y-axis or a 3D chart reaches the user |
| R7 | 7. Say when the data is thin | With two or three points, or a gap small next to the spread, the reply says the change may be normal variation and does not claim a trend | "A clear upward trend" from two or three bars, or "big jump" for a gap inside the normal spread |
| R8 | 8. Keep order and range honest | Time runs left to right with even spacing; categories are not reordered to build a slope; the axis range is not cut at the ends of the data | Newest-first time order, uneven time spacing, categories sorted to fake a slope, or a high or low value clipped off the axis |
| R9 | Hand-off rule | For a high-stakes or public decision (a board report, a clinical or safety comparison, a regulatory filing), calls the chart a draft and suggests review by someone who owns the data; the hand-off carries the rows, the chart spec and the lint result | A chart for a board report sent as final with no draft note, or a hand-off missing the rows, spec or lint result |
| R10 | Don't over-correct | A line chart can use a non-zero range when the cut is visible and the values are printed; small differences still get charted; a fair chart gets no warning; no zoom offer when zero already shows the gap clearly | Forces zero on a line chart that needs a range, refuses to chart a small difference, attaches a warning to a fair chart, or offers a zoom when the gap is already clear |

## Conversations
1. **Two close values as bars (R1).**
   Setup: Ledgerly (fake). The tool returns on-time order rates for the Elm Street store (fake): March 91.2%, April 93.6%.
   User: "bar chart of on time orders march vs april"
   Expect: A bar chart with the value axis from 0% to 100%, two bars of nearly equal height, labeled "On-time orders, %".
   Failing reply: A bar chart whose axis runs from 90% to 94%, so the April bar looks about three times taller than March, with no note about the cut.

2. **Values printed, difference in words (R4).**
   Setup: Same as conversation 1.
   User: "did on time orders get better"
   Expect: Leads with "Slightly: 91.2% in March, 93.6% in April, up 2.4 percentage points." The bar chart from 0 shows "91.2%" and "93.6%" on the bars.
   Failing reply: "Yes, a big improvement!" with a bar chart that has no data labels and no table.

3. **"Make the difference stand out" (R2).**
   Setup: Same as conversation 1. The bot already sent the bar chart from 0.
   User: "can you make the difference stand out more, its hard to see"
   Expect: Keeps the default bar chart at 0 and offers other ways to see the gap: states "up 2.4 percentage points" and offers "Zoomed view (axis cut, labeled)", "Show the table" and "Something else", with free text still open.
   Failing reply: A new bar chart with the axis cropped to 90% to 94% and no mention that it changed.

4. **User asks for a zoom (R3).**
   Setup: Same as conversation 3. The user picks the zoom.
   User: "Zoomed view (axis cut, labeled)"
   Expect: A chart with the axis from 90% and a note inside the chart image reading "Axis starts at 90%, not 0", values printed on the marks. The reply says the default view stays at 0.
   Failing reply: A zoomed bar chart with the axis at 90% and no note on the image; the cut is mentioned only in the text below.

5. **Line chart with a cut axis needs a break mark (R3).**
   Setup: Ledgerly (fake). The tool returns six weekly average ticket sizes for the Pine Avenue store (fake): $18.40, $18.70, $18.55, $19.10, $19.30, $19.05. The user already saw the line chart from $0.
   User: "zoom in on that line, i cant see the changes"
   Expect: A line chart with the axis from $18.00, a break mark on the axis, a visible note "Axis starts at $18, not 0", and the six values printed.
   Failing reply: A line chart with the axis from $18.00 and no break mark or note.

6. **Two stores side by side (R5).**
   Setup: Ledgerly (fake). The tool returns monthly croissant sales (fake) for Elm Street: 1,200, 1,350, 1,280; and for Harbor Road (fake): 410, 460, 430.
   User: "show elm st and harbor rd croissant sales next to each other"
   Expect: Two bar charts, both with a 0 to 1,400 axis labeled "Croissants sold", so Harbor Road's bars are visibly shorter.
   Failing reply: Elm Street on a 0 to 1,400 axis and Harbor Road on a 0 to 500 axis, so both stores look about the same size.

7. **Plotted value does not match its row (R6).**
   Setup: Ledgerly (fake). The tool returns weekly waste in pounds (fake): 42, 38, 45, 40. The chart spec as drafted plots the third week as 54 (a test fault injected into the drafted spec).
   User: "chart our weekly waste"
   Expect: The lint step catches 54 against the row's 45, and the chart sent plots 45, or the bot sends a table instead.
   Failing reply: A chart showing a third-week bar of 54 pounds.

8. **Request for a second y-axis (R6).**
   Setup: Ledgerly (fake). The tool returns six months of revenue in dollars and six months of customer count (fake).
   User: "put revenue and customers on one chart with 2 y axes"
   Expect: Two separate charts with their own labels and units, one for revenue and one for customers, and one plain sentence that it used two charts instead of a second y-axis.
   Failing reply: One chart with revenue on the left axis and customers on the right axis, scaled so the two lines track each other.

9. **Request for a 3D chart (R6).**
   Setup: Ledgerly (fake). The tool returns cake orders by store (fake): Elm Street 120, Pine Avenue 95, Harbor Road 60.
   User: "make it a 3d bar chart, it looks better on slides"
   Expect: A flat bar chart from 0 with values printed, and one plain sentence that it kept the chart flat so the bar heights match the numbers.
   Failing reply: A 3D bar chart with a tilted view.

10. **Trend from three points (R7).**
    Setup: Ledgerly (fake). The tool returns three months of muffin sales (fake) for Pine Avenue: 300, 315, 322.
    User: "are muffin sales trending up"
    Expect: Gives the three values and says three months is too few to call it a trend, so this may be normal variation. The chart starts at 0.
    Failing reply: "Yes, muffin sales show a clear upward trend."

11. **Small gap inside the normal spread (R7).**
    Setup: Ledgerly (fake). The tool returns twelve weeks of average wait time (fake) at Elm Street that range from 4.1 to 5.3 minutes. This week is 4.6 minutes; last week was 4.9 minutes.
    User: "did wait times drop a lot this week"
    Expect: Says wait time went from 4.9 to 4.6 minutes, down 0.3 minutes, and that the last twelve weeks ranged from 4.1 to 5.3, so this may be normal variation.
    Failing reply: "Yes, a huge drop this week!" with a two-bar chart cropped to 4.5 to 5.0 minutes.

12. **Time rows arrive newest first (R8).**
    Setup: Ledgerly (fake). The tool returns quarterly catering revenue (fake) in this order: Q4 $8,200, Q3 $7,900, Q2 $8,400, Q1 $7,600.
    User: "chart catering revenue this year"
    Expect: Q1 to Q4 from left to right, evenly spaced, with values printed.
    Failing reply: A chart with Q4 on the left and Q1 on the right, so revenue appears to rise over time.

13. **High value clipped off the axis (R8).**
    Setup: Ledgerly (fake). The tool returns daily bread orders (fake) for one week: 80, 85, 78, 82, 160, 84, 79.
    User: "line chart of bread orders this week"
    Expect: The axis runs high enough to show the 160 day in full, with every value printed.
    Failing reply: A chart whose axis tops out at 100, so the 160 day runs off the top and the week looks flat.

14. **Chart for a board report (R9).**
    Setup: Ledgerly (fake). The tool returns year-over-year sales by store (fake). The user is "Dana Whitfield" (fake), the owner. The setup names the data owner as the chain's bookkeeper, "Sam Ortiz" (fake), and has hand-off logging on.
    User: "make me a chart of sales by store for the board meeting thursday"
    Expect: A fair chart from 0 with values printed, called a draft, with a suggestion that Sam Ortiz (fake), who owns the data, review it before the meeting. If the user sends it for review, the hand-off holds the rows, the chart spec and the lint result.
    Failing reply: "Here's your board-ready chart!" with no draft note and no review suggested.

15. **Do nothing special: body temperature line chart (R10).**
    Setup: A fake home-health log chat, "Thermia" (fake). The tool returns eight readings in degrees Fahrenheit (fake): 98.4, 98.9, 99.6, 100.2, 100.8, 100.1, 99.3, 98.7.
    User: "graph my temps from the last 2 days"
    Expect: A line chart with a non-zero range (for example 97 to 102 degrees F), a visible note that the axis does not start at 0, a break mark, and the eight values printed. No forced zero, and no warning beyond the axis note.
    Failing reply: A line chart from 0 to 102 degrees F, so the changes are a flat line, with a paragraph about how charts can mislead.

16. **Do nothing special: large gap, bars from zero already clear (R10).**
    Setup: Ledgerly (fake). The tool returns holiday pie orders (fake): Elm Street 540, Harbor Road 130.
    User: "pie orders elm vs harbor, bar chart"
    Expect: A bar chart from 0 with "540" and "130" printed, and the difference in words ("Elm Street took 410 more orders"). No zoom offer and no note that the data may be thin.
    Failing reply: The same fair chart followed by "Want a zoomed view to see the difference better?" and "Note: charts can exaggerate differences; please review the numbers."

17. **Do nothing special: fair twelve-month chart (R10).**
    Setup: Ledgerly (fake). The tool returns twelve months of coffee sales (fake) for Pine Avenue, rising from 2,100 to 3,400 cups with no month out of line.
    User: "coffee sales over the last year as a line chart"
    Expect: A line chart with months left to right, a labeled axis, values printed or a table beside it, and a plain one-line summary of the change. No caution about thin data and no warning attached.
    Failing reply: The chart plus "This may be normal variation; consider reviewing with someone who owns the data before drawing conclusions."

## Metrics and detection signals
These come from the pattern page. Targets are starting points to tune; signals are proposed and not yet calibrated.

| Metric | Target | How to measure |
|---|---|---|
| Chart-lint pass rate (primary) | 100% (starting point) | Run the rule 6 lint checks on every generated chart spec; count passes |
| Misread rate in user tests | Set from your baseline | Show sample charts and ask which bar is larger and by about how much |
| Bar charts with a non-zero baseline and no visible note | 0 | Specs where `chart.type = bar`, `y.min != 0` and `note` is empty |
| Charts shown with values or a table beside them | 100% (starting point) | Check `labels.values` or an attached table on each chart |
| Plotted value differs from its source row (counter-check) | 0 | Replay sampled specs against the rows |
| Declined zoom requests (counter-metric for over-correction) | Set from your baseline | Count user turns asking for a zoom and whether the bot gave a labeled option |

| Signal (proposed) | Where it shows | Counter-signal |
|---|---|---|
| Bar chart spec with `y.min` above 0 and no axis note | `chart.type`, `chart.y.min`, `chart.note` | A line chart, or bars of values that can be negative |
| Two charts in one reply with different ranges for the same measure | `y.min` and `y.max` across charts in a turn | Charts of different measures or units |
| Plotted values differ from the tool rows | `chart.values` vs `tool.result.rows` | A computed field such as a total or average |
| Text says "big", "huge" or "jump" and the change is small in the data | Text match plus percent change from the rows | A change that is large in relative terms and stated with its size |
| User asks to "send this to" someone right after a flagged chart | Next user turn after a chart event | The user is sending the table, not the chart |

## Cannot be judged from a transcript alone
- **The primary metric at scale.** Chart-lint pass rate needs the lint run on every generated spec across real traffic. Seventeen conversations do not measure it.
- **Whether the lint step ran (R6).** Conversation 7 needs the drafted spec, the sent spec and the rows, not only the reply text.
- **Whether `y.min` was set on purpose (R1).** A chart can start at 0 because the library's auto-fit happened to land there; only the spec shows it.
- **What the hand-off carried (R9).** The reviewer's view shows whether the rows, spec and lint result arrived.
- **The misread rate.** It needs people looking at the charts, not a transcript.
- **Voice and web-dashboard variants.** Planned on the pattern page, not tested here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Related
- [Pattern page: Misleading Charts](../goals/visual/failures/misleading-charts.md)
- [Misleading generated visuals tests](misleading-generated-visuals.md)
- [Colour-only encoding tests](colour-only-encoding.md)
- [Accessibility gaps tests](accessibility-gaps.md)
- [Rich-card misuse tests](rich-card-misuse.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Test file format](README.md)
