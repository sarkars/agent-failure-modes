# AI Made-Up Numbers in Reports and Dashboards: Round-Number, Too-Clean Data and Fake Metrics

<!-- SEO
title: AI Made-Up Numbers in Reports: Spot Fake Metrics
description: AI tools fill reports, dashboards and case studies with invented round numbers and totals that don't add up; trace every number to a query or source.
search phrases:
- chatgpt made up numbers in report
- ai invented statistics in case study
- ai generated dashboard fake data
- how to tell if data is fabricated round numbers
- llm hallucinated numbers in summary
- percentages don't add up to 100 ai report
- check ai report numbers against source data
-->

**Frequency**: Common

## Issue: AI tools fill reports, dashboards and case studies with invented round numbers and totals that don't add up; trace every number to a query or source.

> **One line:** You ask ChatGPT, Claude, Copilot or a BI assistant for a Q3 case study or a dashboard and get "conversions up 40%", a channel split that sums to 105% and a retention rate nobody measured; the fix is that every number carries a link to the query or source it came from, totals are computed by code, sample data is labeled, and a pre-publish check flags round-number clusters, totals that don't sum and numbers absent from the source.

| | |
|---|---|
| **Channel** | Written for **visual and written** output: dashboards, charts, slide decks, reports and case studies drafted by AI tools. Chat answers about data are covered by the research-and-data patterns linked in section 8. |
| **Stakes** | Medium to high. A wrong number in a board deck, investor update or public case study is repeated by people who never see the source. |
| **Who is affected** | Analysts, marketers and founders who publish AI-drafted numbers; executives, customers and investors who read them |
| **Frequency** | Common, in our judgment. One study (section 4) found 3.97% to 6.48% of numbers in LLM summaries of financial reports were unsupported or wrong; I found no count for dashboards or case studies. |
| **Pattern ID** | data-too-clean |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Traced-number rate: published numbers whose provenance tag resolves to a query result or an opened source, divided by all published numbers. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Better models copy numbers from sources more faithfully, but no model can know a figure that was never in its input, so the tracing check is still needed. (Our judgment, not tested.) |
| **Also searched as** | ai fake statistics · chatgpt invented percentage · dashboard mock data shipped · numbers don't match source ai summary · too perfect data fabricated · ai case study made up results |

## 1. In plain words
When an AI tool is asked for a report or chart and the real numbers are missing or hard to reach, it writes numbers that look right: round percentages, smooth upward lines, neat splits. Nothing marks them as guesses. The reader sees a precise-looking figure and has no way to tell it came from nowhere. What is missing is a trail from each number back to the data.

## 2. What it looks like
**Without the fix** (illustrative: an online pet-supply store in Columbus, Ohio)
```
Marketer: Here's our Q3 orders CSV. Write a one-page case study on the email relaunch.
AI tool:  Q3 Results: Conversions increased by 40% after the relaunch.
          Revenue grew $250K quarter over quarter. Customer retention hit 92%.
          Channel mix: Email 45% · Paid search 35% · Organic 25%
          [chart: six-month line rising in equal steps, no dips]
Marketer: Perfect, sending to the VP.
(The CSV has no revenue or retention columns. The channel split sums to 105%.)
```
**With the fix**
```
Marketer: Here's our Q3 orders CSV. Write a one-page case study on the email relaunch.
AI tool:  Conversions rose 37.2%, from 1,812 in Q2 to 2,486 in Q3 [q1: count by quarter].
          Channel mix in Q3: Email 41.5% · Paid search 36.3% · Organic 22.2% [q2; sums to 100.0%].
          Not in the file, so left blank: revenue change, retention rate.
          NO DATA: revenue. Send the revenue export or say "drop revenue".
Marketer: Drop revenue and retention.
AI tool:  Removed both. 5 numbers on the page, 5 traced to q1 or q2, 0 untraced.
```
The fixed tool computes from the file, tags every number, leaves gaps visible, and reports a trace count before anyone forwards it.

## 3. Why it happens
- **The request asks for a finished-looking artifact, not for the data.** "Write a case study" or "build a dashboard" has slots for metrics. With no number in the input, the model fills the slot with a typical value, and its typical values lean round: one study found peaks at multiples of 10 and 5 (section 4).
- **Numbers are written as text, not computed.** Totals, percentages and deltas come out of the same text generation as the prose, so they can be off by a rounding step, an addition or a label. CNET's $10,300 interest figure is the arithmetic kind (section 4).
- **Nothing records where a number came from.** A generated "92%" and a queried "92%" are the same string in a slide or chart JSON, so reviewers have nothing to check against.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Manual annotation of summaries of 20 financial reports found numeric hallucination rates of 6.48% (Claude 2.0), 3.97% (Claude 2.1) and 5.74% (GPT-4). The taxonomy has four types: fabricated number, rounding error, arithmetic error and context mismatch; context mismatch was the most common. | [Cao, Raman, Dervovic and Tan, *Characterizing Multimodal Long-form Summarization: A Case Study on Financial Reports*, arXiv 2404.06162, 2024](https://arxiv.org/abs/2404.06162). Opened and read (full PDF). | Single study; one annotator; small sample; older models. The source data was in the prompt, so this is a lower bound for tasks where it is not. |
| The same study reports GPT-4 produced zero fabricated numbers and zero arithmetic errors, which the authors tie to it copying numbers directly from the report. | Same paper, section 4.2. Opened and read. | Supports rule 2: copied or computed numbers are safer than written ones. Single study. |
| Asked to grade 1,000 student essays from 1 to 100, models favored multiples of 5, with 65 the most common score "across varying datasets and metrics". On percentage prompts, multiples of 10 were local peaks. | [Shaikh et al., *CBEval: A framework for evaluating and interpreting cognitive biases in LLMs*, arXiv 2412.03605, Dec. 2024](https://arxiv.org/abs/2412.03605). Opened and read (full PDF). | Preprint; round-number results shown for GPT-4o-mini; a grading task, not report writing. Evidence that round values are a model default, not a rate for reports. |
| Data-forensics work describes the Mosimann technique: the rightmost digits of genuine count data are often uniformly distributed, while numbers people invent "are generally not uniform". The authors warn to confirm that uniformity applies before using the test. | [Pitt and Hill, *Statistical Detection of Potentially Fabricated Data*, arXiv 1311.5517, 2013](https://arxiv.org/abs/1311.5517). Opened and read (full PDF). | About human fabrication of lab counts, not AI. Business metrics such as percentages may not have uniform last digits, so use it as a flag, never proof. |
| A CNET explainer written with an AI tool said $10,000 at 3% interest compounded annually "would accrue $10,300 in interest after a year"; the real interest is $300. The fix came after Futurism alerted CNET. | [Gizmodo, Lauren Leffer, Jan. 17, 2023](https://gizmodo.com/cnet-ai-chatgpt-news-robot-1849996151). Opened and read. | Secondhand report of Futurism's finding; I did not open Futurism or CNET's correction. |
| CNET issued corrections on 41 of the 77 stories it published that were written using an AI tool. | [Talking Biz News, Jan. 25, 2023](https://talkingbiznews.com/media-news/cnet-found-errors-in-more-than-half-of-its-ai-stories/). Opened and read. | Secondhand: it cites The Verge, which I did not open. Not all corrections were numeric. |

**Seen only in a summary, kept out of the fix:** a search summary said Bloomberg corrected at least three dozen AI-generated article summaries in 2025, some with incorrect figures. The page I opened confirmed the "three dozen" count but not the figures, so I do not rely on it.

## 5. The fix
**The principle:** No number reaches a reader unless it traces to a query result or a cited source; gaps stay visible, and code, not the model, does the arithmetic.

**Do this**
1. **Tag every number.** Each figure in a report, chart, slide or case study carries a provenance tag: a query ID, a file and cell range, or an opened source URL. Untagged numbers block publish.
2. **Compute, don't write, derived numbers.** Totals, percentages, growth rates and averages are produced by code from tagged inputs. The check recomputes each one and it must match at the stated rounding.
3. **Parts must sum.** Any split shown as parts of a whole (channels, segments, pie slices) sums to its total, or to 100% within rounding of the last shown digit.
4. **No number absent from the source.** Every number in narrative text appears in the source data or is computed from it under rule 2.
5. **Leave gaps visible.** A missing metric renders as `NO DATA: <metric>` with what is needed, never as an estimate.
6. **Label sample data.** Generated or mock data is marked `is_sample: true` in the data file and shows a visible "Sample data" label on the chart. A production dashboard or published report with sample data fails the check.
7. **Flag, don't block, on shape.** Round-number clusters and too-smooth series send the report to a human reviewer with the flagged values listed. They are not proof of fabrication.

**Reference design: pre-publish number check**
| Check | What it looks at | Action on hit |
|---|---|---|
| Untraced number | Any numeral in text, labels or chart data with no provenance tag | Block |
| Number absent from source | Tagged value not found in the query result or source text (allow 1M = 1,000,000 style formats) | Block |
| Recompute mismatch | Total, percent or delta that differs from recomputation at its shown rounding | Block |
| Parts don't sum | Shares of one whole that miss 100% (or the total) by more than last-digit rounding | Block |
| Sample data in production | `is_sample: true` rows or "Sample data" labels in a production build | Block |
| Round-number cluster | Share of reported values ending in 0 or 5 well above the 20% that uniform last digits would give (proposed flag: over 50% with at least 10 values) | Human review |
| Too-smooth series | Time series with equal steps or no reversals over 6 or more points | Human review |
| Unit or label mismatch | Same value attached to a different label or unit than in the source ("profit" vs. "debt", thousands vs. millions) | Human review |

**Prompt block for the AI tool**
```
Use only numbers from the files or query results I give you. After each number, cite its source as [q#] or [file:cell].
Compute totals, percentages and changes with code, not in your head, and show the formula.
If a number I asked for is not in the data, write NO DATA: <metric> and say what data would fill it.
Never round a measured value to a nicer number. Never fill a chart with sample data unless I say "sample", and label it.
End with: numbers on the page, numbers traced, numbers untraced.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the analyst prompting the AI tool, or the checker reporting to the analyst)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | A requested metric (revenue, retention) is not in the data: the tool asks for the export once, listing every missing metric in one message. |
| Admit uncertainty and show how to check | The checker flags a round-number cluster or smooth series it cannot prove wrong: it lists the values and their tags so a person can open the source. |
| Offer choices: 2-4 options plus "Something else", free text open | A blocking hit: "Add the source", "Recompute from data", "Remove the number", "Something else". |

**Don't over-correct.** Round numbers are not fake by themselves: prices, targets, budgets and survey scales are often round on purpose, and a real 40% exists. Do not block on shape checks; send them to review. Do not strip every number from a draft to pass the check; a case study with no results is useless. Do not apply terminal-digit tests to small sets or to values with built-in rounding; Pitt and Hill warn the uniformity assumption must be confirmed first.

**Hand-off rule.** When a number cannot be traced and the analyst cannot supply a source, it goes to the data owner (the person who owns the warehouse table or the finance export) before publishing, and the report ships with that number removed if the owner does not answer.

**Framework used:** none yet. The checks draw on the Cao et al. annotation protocol and taxonomy and the Mosimann terminal-digit idea as described by Pitt and Hill (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Prompt asks for revenue growth; data has no revenue column | Output shows `NO DATA: revenue`, no revenue figure | 4, 5 |
| 2 | Report says "conversions up 40%"; data gives 37.2% | Check blocks: recompute mismatch | 2, 4 |
| 3 | Channel split 45% + 35% + 25% | Check blocks: parts sum to 105% | 3 |
| 4 | Retention "92%" with no tag | Check blocks: untraced number | 1 |
| 5 | Dashboard built with mock rows, deployed to production | Check blocks: sample data in production | 6 |
| 6 | 12 KPIs, 9 ending in 0 or 5, all traced and correct | Flagged for review, not blocked | 7 |
| 7 | Price list where every price ends in 9 or 0 by design | Reviewer can clear the flag with one note; no block | 7 |
| 8 | Summary calls a $75 million profit "debt" | Flagged as label mismatch | 4 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Traced-number rate** (primary) | 100% | Pre-publish check log: numbers with a resolving provenance tag / all numbers in the artifact | Below 100% on any published artifact |
| Recompute match rate | 100% | Derived numbers that match recomputation at shown rounding / all derived numbers | Any mismatch published |
| Parts-of-whole sum failures | 0 | Count of splits failing the sum check in published artifacts | Any |
| Sample data in production | 0 | `is_sample` rows or labels found in production builds and sent reports | Any |
| `NO DATA` markers left at publish | 0 | Count markers in the final artifact | Any |
| Shape-check false-positive rate (counter-metric) | Under 20% | Monthly review of 30 round-number and smooth-series flags, labeled real problem or not | Over 40% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A numeral in generated text with no matching value in the tool's query results or input files for that session | AI tool session log: output numbers vs. tool-call results | The analyst typed the number in chat or uploaded a file the check did not read |
| A percentage split that does not sum to 100 within last-digit rounding | Rendered chart data or report text | Multi-select survey answers, where shares can exceed 100% by design |
| Most reported values in one artifact end in 0 or 5 | Number extraction over the artifact | Targets, budgets, prices or survey scales that are round on purpose |
| A time series of 6 or more points with equal steps or no reversal | Chart data JSON | A cumulative count, which only rises, or a planned linear forecast |
| A chart whose data source is a hard-coded array instead of a query | Dashboard code or chart config | A labeled design mock that never ships |

**Starter rule:** block publishing when any number in a report, chart or dashboard has no provenance tag that resolves to a query result or an opened source.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: data-too-clean
runs: pre_send
reads: [artifact.numbers, artifact.provenance_tags, session.tool_results, source_files, chart.data, build.environment]
trigger: an AI tool is about to report a report, chart or dashboard as done, or an artifact is about to publish
moves: [ask_clarifying_question, admit_uncertainty, offer_choices]
choices: ["Add the source", "Recompute from data", "Remove the number", "Something else"]
on_miss: ask
metric: traced-number rate
counter_metric: shape-check false-positive rate
status: proposed
```

## 8. Related patterns
- [Placeholder data left in](./ui-placeholder-data-left-in.md) - the closest pattern. There the stand-ins look like stand-ins (Lorem ipsum, 555 numbers, "$XX") on a web page. Here the invented numbers sit in a report or analysis and look exactly like measured ones, so a word-list scan cannot find them; a trace to the data can.
- [Fabricated social proof](./ui-fabricated-social-proof.md) - invented testimonials, logos and "10,000+ customers" stats on a marketing page. This page covers invented metrics in analysis and reporting, where the reader is a decision-maker, not a site visitor.
- [AI made-up citations and fake quotes](./text-invented-citations.md) - invented sources and quotations; this page covers invented figures, which often have no citation at all.
- [Wrong joins and double counting](../../research-and-data-agents/failures/wrong-joins-and-double-counting.md) - a real query that returns wrong numbers. Here no query ran. Both need the SQL or source shown.
- [Inventing reconciling items](../../finance-agents/failures/inventing-reconciling-items.md) - an accounting case of the same move: a made-up figure that makes the numbers balance.
- [Fabricated content in document extraction](../../../../document-processing/goals/multimodal-reliability/failures/fabricated-content.md) - extracted fields with values not in the document; rule 4 is the same check applied to reports.

## 9. Common questions
### How can I tell if ChatGPT made up the numbers in my report?
Ask for the source of each number and check it against your data. Any figure that does not appear in your file or in a query result, or that you cannot recompute, is suspect. The check table in section 5 lists what to run.

### Are round numbers a sign of fake data?
Sometimes, but not on their own. One study found models favor multiples of 5 and 10, and data-forensics work treats odd last-digit patterns as a flag. Real data can be round too, so send clusters to a person, not to the trash.

### Why don't the percentages in my AI-generated chart add up to 100?
The model likely wrote each share as text instead of computing it from one total. Compute splits with code from the counts and check that they sum (rule 3).

### Is it OK to use sample data in an AI-built dashboard?
Yes, while you design it, if every chart says "Sample data" and the data file marks it. It must not reach a production dashboard or a sent report (rule 6).

### Will a better model stop inventing statistics?
Partly. In one study the model that copied numbers from the report invented none, but it still mislabeled some. A model cannot know a number that was never in its input, so keep the trace check.
