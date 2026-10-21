# Chatbot Charts With a Truncated Y-Axis or Misleading Scale: Misleading Charts

<!-- SEO
title: Chatbot Charts With a Truncated Y-Axis or Bad Scale
description: A chat assistant draws a bar chart whose axis starts above zero or whose scale is stretched, so a small gap looks huge. Rules to chart fairly.
search phrases:
- truncated y axis misleading chart
- bar chart axis doesn't start at zero
- AI generated chart misleading
- chatbot chart exaggerates difference
- should bar charts start at zero
- dual axis chart misleading
- chart lint rules for generated charts
- how to stop an LLM making misleading charts
-->

**Frequency**: Occasional

## Issue: A chat assistant draws a chart with a truncated axis or an uneven scale, so a small difference in the data looks large and the user decides on the picture, not the numbers.

> **One line:** The bot picks the chart's axis range to "show the story", so a 3% gap looks like a 300% gap; the fix is to make bar charts start at zero, keep scales honest and matched, label any exception, and print the real values next to the chart.

| | |
|---|---|
| **Channel** | Written for **chat** (charts in a chat widget, rich card or generative UI, plus the text beside them). Voice and web-dashboard variants are PLANNED, not written. |
| **Stakes** | Medium to high. A chart of sales, test results or prices drives a decision. |
| **Who is affected** | Anyone shown a chart the assistant built from real data, and anyone who forwards that chart |
| **Frequency** | Occasional. I found no study that counts how often chat products draw truncated or stretched charts; the rating is our judgment. |
| **Pattern ID** | misleading-charts |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. Row goal: charts represent the data fairly. |
| **Primary metric** | Chart-lint pass rate (share of generated charts that pass the axis and scale checks in section 5). Starting target: 100% (a starting point; tune it). Read it next to the misread rate in user tests. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can follow a "start bars at zero" rule, but the choice of axis range is made in the chart code or tool defaults, and a model asked to make a gap "stand out" will still truncate. (Our judgment, not tested.) |
| **Also searched as** | truncated axis · chart doesn't start at zero · AI chart exaggerates · misleading graph · dual y-axis · stretched scale |

## 1. In plain words
When a chat assistant turns numbers into a chart, something has to choose where the axis starts and how it is scaled. If the bot (or the charting library's auto-range) starts a bar chart at 90 instead of 0, two bars of 94 and 97 look like one is several times taller. The numbers are right and the picture is wrong, and people remember the picture.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Northwind Pharmacy" assistant)
```
User: Did on-time prescription fills improve after we added the second pharmacist?
Bot:  Yes, a big jump. [bar chart: "Before" bar short, "After" bar nearly 4x taller;
      y-axis runs 92% to 97%, no label on the cut]
User: Wow, send that to the owner.
      (the real values were 93.1% and 95.8%)
```
**With the fix**
```
User: Did on-time prescription fills improve after we added the second pharmacist?
Bot:  Slightly: 93.1% before, 95.8% after, up 2.7 points.
      [bar chart: both bars from 0%, values printed on the bars]
      Both months were about 94% to 96% on average, so this may be normal variation.
      [Zoomed view, axis starts at 92%]  [Show the table]  [Something else]
```
The fixed version starts the bars at zero, prints the values, says the size of the change in words, and offers a zoomed view only on request, with the cut labeled.

## 3. Why it happens
- **The range is chosen to make the data "readable".** Charting libraries auto-fit the axis to the data, and a model told to "make the difference clear" has an easy way to do it: crop the axis.
- **Nothing checks the picture against the numbers.** The chart code receives rows and draws them; no step compares bar heights to values or flags a non-zero baseline before the image is sent.
- **Models read charts the same way people do.** Tests of vision-language models show they are also fooled by truncated axes (see section 4), so asking the same model to "review its own chart" by looking at the image is weak.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The UK Government Analysis Function's chart checklist (2 May 2023) has the bar-chart rule "Do not break the numerical axis - it should always start at zero", says "if starting the axis from zero stops you from telling the story clearly, consider an alternative chart", and that even a signposted break still displays "the relative size of bars ... very strongly". For line charts it says to clearly label a broken y-axis, and that small-multiple charts need the same scale on every numerical axis. | [Government Analysis Function, Accessible charts: a checklist of the basics](https://analysisfunction.civilservice.gov.uk/policy-store/charts-a-checklist) (opened; quoted text is from the fetch result). | UK government guidance for public-sector publishing. It is a style rule, not a law, and it is about accessibility and clarity, not chat. |
| Correll, Bertini and Franconeri report that bar charts with y-axes that do not begin at zero "can visually exaggerate effect sizes", that crowd-sourced experiments found truncation changes perceived effect size across chart types, and that the effect persists for viewers who know the axis is truncated. They "advise against ironclad rules" about y-axes and say usefulness depends on the goal. | [Truncating the Y-Axis: Threat or Menace? (arXiv 1907.02035)](https://arxiv.org/abs/1907.02035v1) (abstract page opened; I did not read the full paper). | The authors do not say truncation is always wrong. This is why rule 3 allows a labeled, opt-in zoom instead of a ban. Lab experiments with crowd workers, not chat users. |
| Yang, Vargas Restrepo, Stanley and Marsh, in five studies, found that cutting off the bottom of a bar graph's axis made viewers judge differences as bigger; the effect held after participants were taught about it, and about 83.5% of participants showed it. | [Truncating Bar Graphs Persistently Misleads Viewers, J. Applied Research in Memory and Cognition 10(2), 2021](https://scholars.duke.edu/publication/1474486). **Read through a summary** (the Duke listing; the PDF would not load as text). Kept out of the fix rules. | Summary only; I did not check sample sizes or methods. |
| Tonglet et al. report that distorted charts, such as truncated or inverted axes, reduce multimodal LLMs' question-answering accuracy to "the level of the random baseline", and that extracting the underlying data table and answering from it with a text-only model improved results on misleading charts by 15.4 to 19.6 percentage points. | [Protecting multimodal large language models against misleading visualizations (arXiv 2502.20503, v2, Mar 2025)](https://arxiv.org/abs/2502.20503v2) (abstract page opened). | Tests models that read charts, not models that draw them. It supports checking charts against the data table (rule 6), not any claim about how often assistants draw bad charts. |
| Mahbub et al. analyzed over 16,000 responses from ten vision-language models across eight misleading chart designs and found most models were deceived; interpretations changed though the data stayed the same. | [The Perils of Chart Deception (arXiv 2508.09716, IEEE VIS 2025)](https://arxiv.org/abs/2508.09716) (abstract page opened). | Same limit: models reading charts. |

**How this differs from the closest pages.** [Misleading generated visuals](misleading-generated-visuals.md) covers an AI-made picture shown as real, and says a chart should be drawn from the returned rows. This page starts after that is done: the chart is built from true data and is still misleading because of the axis, scale or chart type. [Colour-only encoding](colour-only-encoding.md) covers meaning carried by color alone. [Accessibility gaps](accessibility-gaps.md) covers text alternatives and contrast. [Cognitive overload](cognitive-overload.md) covers too many charts or cards at once.

**Public incident.** I found no public incident of a chat assistant drawing a truncated chart, and did not search for one beyond the research queries. **Research gap (R):** no study I opened measures how often LLM-generated charts truncate axes, so every frequency claim here is our judgment.

## 5. The fix

**The principle:** A chart must show the size of a difference as the data does: bars start at zero, scales are shared where charts are compared, any exception is labeled on the chart, and the real values sit beside it.

**Do this**
1. **Bars start at zero.** Every bar or column chart has a value axis whose baseline is 0. The chart code sets it explicitly and does not use an auto-fit range.
2. **If zero hides the story, change the chart, not the axis.** Show the change as a number ("up 2.7 points"), or use a table, a dot plot or a line chart. The Government Analysis Function guidance in section 4 says to consider an alternative chart.
3. **A zoomed view is opt-in and labeled.** If the user asks for one, put a visible note in the chart image ("Axis starts at 92%, not 0") and, for line charts, a break mark on the axis. The default view stays at zero.
4. **Print the values.** Show the numbers on or beside the marks (data labels or a short table), and state the difference in the text in plain words with the unit ("2.7 percentage points").
5. **Compared charts share a scale.** When the reply shows two or more charts side by side, every numerical axis uses the same range and unit.
6. **Check the chart against the rows before sending.** A lint step compares the chart spec to the returned rows: baseline is 0 for bars, plotted values equal the rows, axis labels and units are present, no second y-axis, no 3D effect. A failed check rewrites the chart or sends a table instead.
7. **Say when the data is thin.** If there are two or three points, or the gap is small compared with the spread, say that the change may be normal variation. Do not claim a trend from two bars.
8. **Keep order and range honest.** Time runs left to right with even spacing, categories are not reordered to build a slope, and the axis range is not cut at the ends of the data to hide high or low values.

**Reference design: chart spec the bot must emit**
| Field | Rule |
|---|---|
| `chart.type` | bar for comparing amounts; line for change over time |
| `y.min` | 0 for bar; any value for line only with a visible axis note |
| `y.label` and `y.unit` | Required; same text as the user's term ("on-time fills, %") |
| `labels.values` | true |
| `source` | Where the rows came from and the as-of date, in the caption |
| `note` | Required when `y.min` is not 0 or the series is shorter than 6 points |

```
When you draw a chart, start every bar chart's value axis at 0 and print the values.
If a zoomed axis would help, offer it as an option and label the cut on the chart.
State the size of the difference in plain words with its unit.
Use the same scale on charts shown together. Do not use a second y-axis or 3D.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply says the size of the difference in words first ("up 2.7 points"), then shows the chart |
| Admit uncertainty and show how to check | The data is thin or the gap is small: say it may be normal variation and offer the table |
| Offer choices | The user wants the gap easier to see: "Zoomed view (axis cut, labeled)", "Show the table", plus "Something else", free text open. Do not offer when zero already shows the gap clearly. |

**Don't over-correct.** Do not force a zero baseline on every chart. A line chart of body temperature or a stock price can use a non-zero range, and Correll and colleagues advise against ironclad rules. The check is that the cut is visible and the values are printed. Also do not refuse to chart small differences, and do not attach a warning to every chart that is fair.

**Hand-off rule.** When the chart will be used for a high-stakes or public decision (a board report, a clinical or safety comparison, a regulatory filing), tell the user the chart is a draft and suggest review by someone who owns the data. Pass the rows, the chart spec and the lint result with the hand-off.

**Framework used:** none yet. Rules 1, 2 and 5 follow the Government Analysis Function checklist in section 4; rule 3 follows Correll and colleagues; rules 4 and 6 to 8 are our own design judgment.

## 6. How to test it (short version)
No test file yet. The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask for a bar chart of two values close together (93.1 and 95.8) | Both bars start at 0 and values are printed | 1, 4 |
| 2 | Say "make the difference easier to see" | The bot offers a labeled zoom or a different chart; the default stays at zero | 2, 3 |
| 3 | Ask for a line chart of a series with a non-zero range | The axis range is shown and any cut is noted on the chart | 3 |
| 4 | Ask for two charts of the same measure for two stores | Both use the same axis range and unit | 5 |
| 5 | Feed rows with a changed value and compare to the chart spec | The lint step catches a plotted value that differs from the row | 6 |
| 6 | Ask for a trend from three data points | The reply says the data is thin and does not claim a trend | 7 |
| 7 | Ask for a chart for a board report | The reply calls it a draft and suggests review; hand-off packet includes rows and spec | Hand-off |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Chart-lint pass rate** (primary) | 100% (starting point) | Run the lint checks in rule 6 on every generated chart spec; count passes | Below 99% |
| Misread rate in user tests | Set from your baseline | Show a sample of charts and ask which bar is larger and by about how much; count answers off by more than a set margin | Rising |
| Bar charts with a non-zero baseline and no visible note | 0 | Query chart specs where `chart.type = bar`, `y.min != 0` and `note` is empty | Any |
| Charts shown with values or a table beside them | 100% (starting point) | Check `labels.values` or an attached table on each chart | Below 95% |
| Charts where a plotted value differs from its source row (counter-check) | 0 | Replay sampled specs against the rows | Any |
| Zoom requests that were declined (counter-metric for over-correction) | Track; set from your baseline | Count user turns asking for a zoom or "bigger difference" and whether the bot gave a labeled option | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat** text and chart events only; none has been measured. Voice and dashboard signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A bar chart spec has `y.min` above 0 and no axis note (rule 1) | `chart.type`, `chart.y.min`, `chart.note` | A line chart, or a bar chart of values that can be negative |
| Two charts in one reply have different axis ranges for the same measure (rule 5) | Compare `y.min` and `y.max` across charts in a turn | Charts of different measures or units |
| A chart's plotted values differ from the tool rows (rule 6) | `chart.values` vs `tool.result.rows` | A computed field such as a total or average |
| The text says "big", "huge" or "jump" and the change is small in the data (rules 4, 7) | Text match plus the percent change from the rows | A change that is large in relative terms and stated with its size |
| User forwards or asks to "send this to" someone right after a chart with a flagged spec (hand-off rule) | Next user turn after a chart event | The user is sending the table, not the chart |

**Starter rule:** every bar chart the assistant draws starts at zero, prints its values, and any axis cut is labeled on the chart.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: misleading-charts
runs: pre_send
reads: [chart.type, chart.y.min, chart.y.max, chart.values, chart.note, tool.result.rows]
trigger: a reply is about to include a chart the assistant built from data
moves: [lead_with_answer, admit_uncertainty_show_how_to_check, offer_choices]
choices: ["Zoomed view (axis cut, labeled)", "Show the table", "Something else"]
on_miss: rewrite
metric: chart-lint pass rate
counter_metric: declined zoom requests
status: proposed
```

## 8. Related patterns
- [Misleading generated visuals](misleading-generated-visuals.md): an AI-made picture shown as real; this page is about true data drawn with a misleading axis or scale.
- [Colour-only encoding](colour-only-encoding.md): meaning carried by color alone, in charts and chips.
- [Accessibility gaps](accessibility-gaps.md): text alternatives, contrast and focus for charts and cards.
- [Cognitive overload](cognitive-overload.md): too many charts or cards at once.
- [Rich-card misuse](rich-card-misuse.md): a card or chart where a sentence would do.

## 9. Common questions
### Should a bar chart always start at zero?
For bars, yes by default. The UK Government Analysis Function checklist says the numerical axis should always start at zero, because bar length is what the eye compares. Line charts can use another range if the cut is clearly marked, and Correll and colleagues say usefulness depends on the goal (section 4).

### Is a truncated y-axis ever okay?
Sometimes, for line charts or a labeled zoom when small changes matter, such as a lab value. The cut must be visible on the chart, the values printed, and the zoom must not be the default (rule 3). Research I opened found the effect persists even for viewers who know the axis is cut.

### How do I stop an LLM from making a misleading chart?
Do not rely on the prompt alone. Set the axis explicitly in the chart code, lint the spec against the returned rows, and add the four-line prompt block from section 5. Tests of models that read charts (section 4) suggest they are also fooled by distortions, so check the spec, not a picture of it.

### What should the bot do when the difference is tiny?
Say so in words with the unit, show the bars from zero, and note that it may be normal variation (rule 7). Offer a labeled zoom or the table if the user wants a closer look. Do not stretch the axis to make the gap look meaningful.

### Are dual-axis charts misleading?
They can be, because the two scales can be set to make lines cross or track each other. I did not open a source that measures this, so rule 6 bans a second y-axis as our design judgment. Show two separate charts with their own labels instead.
