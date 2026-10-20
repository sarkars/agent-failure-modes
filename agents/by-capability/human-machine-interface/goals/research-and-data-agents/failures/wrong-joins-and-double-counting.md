# Text to SQL Wrong Results: Wrong Joins and Double Counting

<!-- SEO
title: Text to SQL Wrong Results: Fix Join Double Counting
description: An AI analyst runs a query that joins tables wrong and reports inflated numbers with confidence. Show the SQL, check the grain, and run sanity checks.
search phrases:
- text to sql wrong results
- ai analyst double counting
- llm sql join duplicates rows
- chatgpt sql wrong count one to many join
- fan trap text to sql
- ai data analyst gives wrong numbers
- how to validate llm generated sql
- text to sql hallucinated join
-->

**Frequency**: Common

## Issue: An AI analyst runs a query that joins tables the wrong way and reports inflated numbers with confidence; the fix is to show the SQL, state what is counted, and run sanity checks before answering.

> **One line:** You ask "how many customers ordered in March" and the bot answers with a precise number that counts order lines, not customers.

| | |
|---|---|
| **Channel** | Written for **chat**: a data assistant in a chat window that answers business questions with numbers from SQL. Voice and web-embedded signals are planned only. |
| **Stakes** | Medium to high. A wrong count in a chat answer ends up in a slide, a forecast, or a board report. |
| **Who is affected** | Non-technical users who cannot read SQL, and analysts who trust a quick answer |
| **Frequency** | Common (our judgment). The sources in section 4 call these errors a known failure of generated SQL. I found no rate for live analyst bots. |
| **Pattern ID** | wrong-joins-and-double-counting |
| **Family** | [Research and data agents](../README.md) |
| **Goal** | Numbers the assistant reports match what the data says, and the user can see how they were computed. |
| **Primary metric** | Result accuracy on a labeled query set. Target: 95% or higher on questions with a known answer (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. Better models write better SQL, but a query that runs cleanly and returns the wrong count raises no error, so a check outside the model is still needed. (Our judgment, not tested.) |
| **Also searched as** | text to sql wrong results · ai analyst double counting · llm sql join duplicates · ai data analyst wrong numbers · fan trap sql llm · validate llm generated sql |
| **Flag** | R (reliability) |

## 1. In plain words
A data assistant turns your question into SQL, runs it, and tells you the number. If it joins a table that has many rows per customer and then counts, each customer is counted once per row. The query does not fail, so the answer looks fine. The fix is to show the SQL with every number, say exactly what was counted, and check the result against a second count before presenting it.

## 2. What it looks like
The numbers below are made up for this page.

**Without the fix**
```
User: How many customers ordered in March?
Bot:  18,420 customers placed an order in March 2026.
User: That's more than our whole customer list for the month. Orders alone were about 9,900.
Bot:  You're right to question it. Let me recheck.
Bot:  I reran it: 18,420 customers placed an order in March 2026.
User: (stops using the bot for finance questions)
```

**With the fix**
```
User: How many customers ordered in March?
Bot:  6,310 customers placed at least one order from Mar 1 to Mar 31, 2026 (Pacific time).
      Query: SELECT COUNT(DISTINCT customer_id) FROM orders
             WHERE order_date >= '2026-03-01' AND order_date < '2026-04-01'
      Checks: 9,870 orders in the same range, so 1.56 orders per customer; 6,310 is below the 9,870 orders and below the 41,200 total customers.
      "Ordered" here includes orders later cancelled. Do you want cancelled orders excluded, or the count of orders instead? Something else is fine too.
User: Exclude cancelled.
```
The fixed bot shows the query, names what a "customer" and "March" mean, runs a check against the order count, and asks about the one open definition.

## 3. Why it happens
- **A join that runs is not a join that is right.** One customer has many orders, and one order has many items. Joining the tables and then counting or summing repeats each row, and the database raises no error.
- **The model does not know the grain.** Without a declared "one row per order" or "one row per line item," the model cannot tell which column is safe to sum or count.
- **Nothing between the SQL and the chat checks the result.** The number goes straight from the query to the reply in a confident tone.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Snowflake's Cortex Analyst team describes double counting as a measure that is "summed multiple times," names fan traps and chasm traps as the two common forms, and says it flags a query when an additive aggregate such as `SUM` or `COUNT` is applied above the lowest-granularity table. | [Yahia Bsat, Snowflake Engineering Blog, Feb 20, 2025](https://www.snowflake.com/en/engineering-blog/snowflake-cortex-analyst-introducting-joins-complex-schemas). Opened. | Vendor blog describing its own product. It gives no error rate and uses the TPC-H sample schema. |
| A practitioner lists the fan-out join as a failure where the query "looks correct" and wrong numbers reach dashboards with no error. It also lists NULL handling and date-range mistakes, and recommends sanity checks such as flagging zero rows or negative revenue. | [Tian Pan, "Text-to-SQL in Production," Apr 10, 2026](https://tianpan.co/blog/2026-04-10-text-to-sql-failure-modes-production). Opened. | Single practitioner blog. Its "5x too high" example is illustrative, not measured, and its sample SQL would not actually inflate the sum. Its accuracy ranges cite sources I did not open, so I do not use them. |
| On Spider 2.0, 632 enterprise text-to-SQL workflow problems, a code agent built on o1-preview solves "only 21.3% of the tasks," against 91.2% on Spider 1.0 and 73.0% on BIRD. | [Lei et al., arXiv 2411.07763, ICLR 2025](https://arxiv.org/abs/2411.07763). Opened (through the fetch tool, which summarized the abstract). | A 2024 model on a research benchmark, not live chat traffic. It measures whether SQL is right, not how often a wrong answer reaches a user. Earlier versions of the paper gave a lower figure; I use the latest one. |

**Public incident.** No public incident found of an analyst bot reporting a wrong join-based number that harmed a named organization. I ran 3 searches (text-to-SQL fan-out double counting, BIRD benchmark accuracy, Spider 2.0 results). Search summaries also mentioned an open-source pre-execution checker and Hacker News threads; I did not open them and do not use their claims.

## 5. The fix

**The principle:** No number reaches the user without its query, a plain statement of what was counted, and a check that the number is plausible.

**Do this**
1. **Show the SQL with every number.** Each answer that states a figure includes the query that produced it, in a block the user can copy.
2. **State what was counted.** Name the unit (customers, orders, line items), the filter, and the exact date range with its time zone, in one sentence next to the number.
3. **Count each unit once.** When a query joins a table with many rows per unit, count with `COUNT(DISTINCT key)` or aggregate the many-side table in its own subquery before joining. Never `SUM` or `COUNT` over rows that a join has repeated.
4. **Run at least one control query before presenting a figure.** Compare against an independent count, such as the base table's row count for the same filter. If the answer is larger than the base table allows, do not present it.
5. **Show the check result in the answer.** One line: "Checks: X, so Y." Say which checks were not run.
6. **When a check fails, say so and do not present the number.** Name the failed check, show the query, and give the next step (fix the join and rerun, or ask).
7. **Ask one question when the metric has two definitions.** If "customer," "revenue," or "active" could mean two things in this schema, ask once. Do not guess silently.
8. **Never write "I verified this" without a control query in the log.**

**Reference design: answer template and check table**
```
<number> <unit> <filter>, <start date> to <end date> (<time zone>).
Query: <SQL>
Checks: <control result>, so <conclusion>. Not checked: <list or "none">.
<one definition question, only if a term is ambiguous>
```
| Query pattern | Check before presenting | If it fails |
|---|---|---|
| Count or sum after joining a one-to-many table | Same figure from the base table alone, or `COUNT(DISTINCT key)` equals the count | Rewrite with DISTINCT or pre-aggregation; rerun |
| Count of units for a period | Result is not larger than the base-table count for that period | Do not present; report the failed check |
| Sum of a value stored once per order | Join does not repeat order rows | Aggregate before the join |
| Zero rows or negative total | Rerun without the newest filter to find which filter removed the rows | Say the filter returns nothing and ask |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A check failed, or none could run: say the number is unconfirmed, show the query, and name the check the user can run. Do not use it for a figure whose control query passed. |
| Ask one clarifying question | A term such as "customer" or "revenue" has two definitions in the schema and the number changes: ask which. Do not ask when both definitions give the same count. |
| Offer choices: 2-4 options plus "Something else", free text open | The question could mean customers, orders, or paying customers: list them with "Something else". Do not offer them when the schema allows only one reading. |
| Hand off to a person | The figure feeds a financial filing, a billing change, or a decision the user says is final, and a check failed or could not run. Do not hand off a casual lookup. |

**Don't over-correct.** Do not run five checks for a single-table row count; one control is enough, and none for a lookup of one record. Do not paste long SQL before a short answer; lead with the number and put the query beneath it. Do not ask a definition question on every turn; ask only when the number changes. Do not withhold a figure that passed its check because it "might be wrong."

**Hand-off rule.** If a figure is for a financial filing, an invoice, or a legal or regulatory report, and a check failed or could not run, tell the user to have an analyst or the data owner confirm it before use.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run.** These are designed scenarios on a small test database with known answers.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "How many customers ordered in March?" on a schema where customers have several orders | The count equals the known distinct count; SQL shown | 1, 3 |
| 2 | Ask for total revenue where orders join to line items and to payments | The figure equals the known total; no row repeated by the join | 3, 4 |
| 3 | Plant a join that repeats rows | The control check fails, the bot does not present the number and says why | 4, 6 |
| 4 | "Customers" means account holders in one table and buyers in another | The bot asks one question with "Something else" | 7 |
| 5 | "Sales last month" with no date given to the bot | The reply states the exact start and end dates and the time zone | 2 |
| 6 | The user asks "did you check that?" after a bare number | The bot shows a control query result, or says none was run | 5, 8 |
| 7 | A single-table row count for one status | One query, number, and query shown; no extra checks or questions | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Result accuracy on a labeled query set** (primary) | 95% or higher | Run 100 or more questions with known answers on a copy of your database; compare the reported figure to the key | Below 90%, or any drop of 3 points from the last release |
| Share of answers that show the query | 100% | Replies with a number that contain a SQL block, over all replies with a number | Below 98% |
| Answers with a stated unit and date range | 100% | Sampled review of 50 replies a week against the template | Below 95% |
| Answers with a control query logged | 95% or higher | Share of figures with a control-query event in the same turn | Below 90% |
| Answers withheld that were correct (counter-metric) | Track; set from baseline | Sampled review of replies that reported a failed check; count those where the original figure was right | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply states a number and has no SQL block | Reply text parse | The user turned off query display in settings |
| Generated SQL aggregates after joining a one-to-many table with no DISTINCT or pre-aggregation | SQL parse plus schema keys | The schema marks the join as one-to-one |
| Reported count is larger than the base-table count for the same filter | Query result vs control event | The base table is a snapshot taken at a different time |
| No control-query event in the turn that produced a figure | Tool-call log | A lookup of one known record |
| User's next turn disputes the number ("that seems high," "that doesn't match the dashboard") | User turn text | The dashboard uses a different definition |

**Starter rule:** every number the assistant states comes with its SQL, what was counted, and the result of at least one control query, or it says no check was run.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: wrong-joins-and-double-counting
runs: pre_send
reads: [draft_reply.figures, query.sql, query.result, control_query.result, schema.join_cardinality]
trigger: a draft reply states a figure computed from a query that joins a table with many rows per unit
moves: [admit_uncertainty, ask_one_question, offer_choices, hand_off]
choices: ["Count customers", "Count orders", "Count paying customers", "Something else"]
on_miss: rewrite
metric: result accuracy on a labeled query set
counter_metric: answers withheld that were correct
status: proposed
```

## 8. Related patterns
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the general case, a wrong answer in a sure tone. This page is narrower: the wrong answer is a number from a query that ran, so the check is a control query and the query shown, not general hedging.
- [Invented packages and APIs](../../coding-agents/failures/invented-packages-and-apis.md): a coding assistant names something that does not exist. Here nothing is invented; real tables are joined in a way that repeats rows.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the assistant picks one reading of an ambiguous request. It is one cause here (rule 7), but the double count also happens when the question is clear.

## 9. Common questions
### Why does my AI analyst give wrong counts?
Often the query joins a table with many rows per customer and then counts, so each customer is counted once per row. The query runs without error, so nothing signals the mistake. See [section 3](#3-why-it-happens).

### What is a fan-out or fan trap in SQL?
It is a join that multiplies rows, and an aggregate over those rows then counts or sums the same value several times. Snowflake's team uses "fan trap" and "chasm trap" for the two forms ([section 4](#4-why-it-matters)).

### How do I check SQL an LLM wrote?
Read what is counted and the date range, then compare the figure with a count from the base table alone. If the join result is larger than the base allows, the join is repeating rows. The assistant should show this check, not leave it to you ([section 5](#5-the-fix)).

### Will a better model stop this?
It will help, but I found no study that measures it. The Spider 2.0 result in section 4 shows models still miss many enterprise tasks. Our judgment is that a check outside the model is still needed.

### Should the bot show SQL to non-technical users?
Yes, beneath the number, so a colleague who reads SQL can check it. Lead with the plain-language answer and what was counted.

---
## Technical section

### T1. Solution architecture
```
question -> resolve terms and dates -> draft SQL -> parse (joins, aggregates, schema keys)
         -> rewrite if a one-to-many join feeds an aggregate -> run
         -> control query (base-table count, DISTINCT count) -> compare
         -> pass: reply with number, SQL, units, checks
         -> fail: reply with failed check, SQL, next step; log
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Every figure has a SQL block | Reply filter before send | Log scan; test 1 |
| No aggregate over a row-repeating join without DISTINCT or pre-aggregation | SQL parser before run | Tests 2, 3 |
| Control query result logged before a figure is sent | Agent runtime | Test 6; metric row 4 |
| Read-only database credentials | Database role | Permission audit |

### T3. Evals
- **Dataset:** start with 100 questions on a copy of your own schema with known answers. Include one-to-many joins, two fact tables on one dimension, NULL filters, and relative dates.
- **Judge rubric:** the figure matches the key; the SQL is shown; unit, filter, and date range are stated; a failed check is reported, not hidden.
- **Metrics and starting thresholds:** accuracy 95% or higher; query shown 100%. Starting points to tune.
- **Release gate:** block a deploy if accuracy drops 3 points against the last release or any planted-join case is presented.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Answers with a number and no SQL block | Below 98% | Below 90% | Find the path that skips the template |

### T5. Trade-offs
- A control query adds one database call and some latency. Cache base-table counts for a short time.
- A control check catches inflated counts, not a wrong filter or a wrong definition; those need the clarifying question.
- Showing SQL to every user adds length. Keep it beneath the number.

---
### Deep dive
- **Open question.** I found no study of join errors in live analyst chat products and no measured effect of this fix. The evidence is two vendor or practitioner write-ups and a research benchmark.
- **Not used.** Search summaries mentioned the BIRD benchmark gap, a metric-reliability paper, and an open-source pre-execution checker. I did not open those sources, so nothing here depends on them.
- **Modality notes.** Voice and web-embedded analyst assistants: PLANNED. In voice, the SQL cannot be shown, so the units and checks must be spoken and the query sent to a screen.
- **References.** [Snowflake Engineering Blog, Feb 20, 2025](https://www.snowflake.com/en/engineering-blog/snowflake-cortex-analyst-introducting-joins-complex-schemas) (opened); [Tian Pan, Apr 10, 2026](https://tianpan.co/blog/2026-04-10-text-to-sql-failure-modes-production) (opened); [Lei et al., arXiv 2411.07763](https://arxiv.org/abs/2411.07763) (opened). Naming follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
