# AI Analyst Wrong Metric Definition: Wrong Business Definitions

<!-- SEO
title: AI Analyst Wrong Metric Definition: Fix "Active User" Errors
description: A data chatbot answers with its own meaning of "active user", "revenue", or "churn". Use the company's governed metric definitions and state them in every answer.
search phrases:
- ai analyst wrong metric definition
- chatbot uses wrong definition of active users
- semantic layer for llm
- text to sql business logic
- why does chatgpt give different revenue numbers for the same question
- llm data analyst definition of churn
- governed metrics for ai agents
- text to sql ignores metric definitions
-->

**Frequency**: Common

## Issue: A data chatbot answers a business question with its own meaning of "active user", "revenue", or "churn" instead of the company's definition, and the fix is to compute governed metrics and state the definition in every answer.

> **One line:** You ask for last month's active users and get a real number that counts the wrong thing.

| | |
|---|---|
| **Channel** | Written for **chat**: a data or analytics assistant in a chat window. Voice and web-embedded signals are planned only. |
| **Stakes** | Medium to high. The number goes into a board deck, a forecast, or a bonus calculation. |
| **Who is affected** | Anyone who asks a data assistant a business question, especially people who cannot read the SQL |
| **Frequency** | Common. I found vendor test results (section 4) but no rate for live products. |
| **Pattern ID** | wrong-business-definitions |
| **Family** | [Research and data agents](../README.md) |
| **Goal** | Numbers the assistant gives mean what the business means by them. |
| **Primary metric** | Answers that use the governed definition. Target: 100% (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. The company's definition of "active" is business context that is not in the table schema, so a better model still has to be given it. (Our judgment, not tested.) |
| **Also searched as** | ai analyst wrong metric definition · chatbot wrong definition of active users · semantic layer for llm · text to sql business logic · llm different revenue number same question · governed metrics ai agent |

## 1. In plain words
Words like "active user", "revenue", and "churn" have no single meaning. Each company defines them, and the definition rarely appears in the database column names. A data assistant that guesses a meaning returns a clean, confident number that answers a different question. The fix is to compute these terms from the company's governed definitions and to say which definition, window, and date range each number used.

## 2. What it looks like
The company, product, and numbers below are made up for this page. Assume the company defines an active user as someone who created or edited a project in the last 28 days.

**Without the fix**
```
User: How many active users did we have last month?
Bot:  You had 48,210 active users last month.
User: Finance says it was closer to 31,000. Which one is right?
Bot:  I counted users with at least one login in September. If you meant something else, let me know.
User: (pastes the 48,210 into the board update before anyone checks)
```

**With the fix**
```
User: How many active users did we have last month?
Bot:  31,040 active users as of September 30, using the company definition: created or edited
      a project in the previous 28 days (metric "active_users_28d", owned by Product Analytics).
      A login-only count would be higher; I can show it if you want it labeled that way.
User: That matches Finance. How does it compare to August?
Bot:  29,870 on August 31, same definition, so up 3.9%.
```
The fixed reply names the definition and its owner, uses the governed metric, and keeps the same definition for the comparison.

## 3. Why it happens
- **The definition is not in the schema.** Business logic usually lives in SQL transformations, not column names. A model that sees a `last_login` column will use it. A dbt-related post found in search describes daily active users as depending on a session window, deduplication, and filtering out internal traffic; I read that only in a search summary, so it is not used as evidence below.
- **The model rebuilds the logic on each run.** The AtScale post in section 4 says the model picks tables, joins, filters, and time grain on every run, so the same question can produce different SQL and different numbers.
- **Nobody asks which meaning is wanted.** Two teams can legitimately use two meanings. Without a rule to ask or to state the definition, the assistant picks one silently.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a test of 11 questions run 20 times each on the ACME Insurance dataset, claude-sonnet-4-6 scored 90.0% with text-to-SQL and 98.2% with a semantic layer; gpt-5.3-codex scored 84.1% and 100.0%. Before extra modeling, accuracy on all 11 questions was 64.5% (text-to-SQL) and 72.7% (semantic layer) for both models. | [dbt Labs, "Semantic Layer vs. Text-to-SQL: 2026 Benchmark Update," Jason Ganz and Benoit Perigaud, April 7, 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026). Opened. | Vendor (dbt Labs sells the semantic layer). Small question set, one dataset, full schema loaded as context, which the authors say is not practical for larger datasets. |
| Questions the semantic layer could not answer scored 0.0% there, but it "tells you it can't answer"; text-to-SQL "will cheerfully give you a wrong number." | Same dbt Labs post. Opened. | Same vendor and test. This is why the fix below includes an honest "not in the governed metrics" answer. |
| A semantic layer resolves each business term to one fixed query. The post lists what a governed definition settles: calendar or fiscal Q1, order date or shipment date for revenue, one rule for "active workspace." It reports about 70% accuracy on curated business metrics without a semantic layer and 95% to 100% with one. | [AtScale, "Why ChatGPT Gives Different Answers to the Same Question on Your Business Data," Mark Palmer, June 26, 2026](https://www.atscale.com/blog/why-chatgpt-gives-different-answers-business-data/). Opened. | Vendor post (AtScale sells a semantic layer), figures from its own work; I did not check them. I do not use the post's other figures. |
| Teams define "active user" differently. The article argues that a login shows presence, not participation, and pairs daily, weekly, and monthly windows with product types. | [Yael Mark, "Stop the madness: active user," Substack, July 11, 2025](https://yaelmark.substack.com/p/stop-the-madness-active-user-a-user). Opened. | One practitioner's opinion, not a study. It shows the definitions vary, not how often a data assistant gets them wrong. |

**Public incident.** No public incident found of a company acting on a data assistant's wrong metric definition. I ran 3 searches (semantic layer accuracy, "active user" definitions across teams, dbt MetricFlow and text-to-SQL business logic). The results were vendor and practitioner posts. The search summary for the "active user" query said it found nothing specific about AI analysts misreading that term; I did not open anything further on that.

## 5. The fix

**The principle:** Compute every business term from the company's governed definition, and say which definition and window the number used.

**Do this**
1. **Look up the term before computing it.** For "active user", "revenue", "churn", and any other term in the metric catalog, use the governed metric (semantic layer or metric file), not SQL the assistant writes from column names.
2. **State the definition with every number.** The reply names the metric, its definition in one line, the date range, and the "as of" date.
3. **Keep the definition fixed within a conversation.** Follow-up comparisons use the same metric, window, and filters unless the user changes them.
4. **If the term has no governed definition, or has several, say so and ask.** Do not compute a guess. Ask one question, or offer the closest governed metrics plus "Something else". If one definition is marked the default, answer with it and name the other.
5. **If the governed metrics cannot answer the question, say that.** Do not fall back to raw SQL silently. Say what is missing and who owns the metric.
6. **Label any non-governed number.** When the user asks for a different meaning (for example login-only), compute it only with the label "not the company definition" next to the governed number.
7. **Show the owner and a way to check.** Give the metric's owner or definition page so the user can verify it.

**Reference design: decision for each business term in a question**
| Term in the question | Do |
|---|---|
| In the catalog with one definition | Compute it; state definition, date range, as-of date |
| In the catalog with several definitions (for example gross and net revenue) | Ask which, or give the marked default and name the other |
| Not in the catalog | Say there is no governed definition; ask or offer the closest governed metrics |
| In the catalog but the data needed is missing | Say what is missing and who owns it; compute nothing |

```
For any business term (active user, revenue, churn, and others in the metric catalog), use the governed metric. Never compute it from column names.
Start the answer with the number, then one line: metric name, definition, date range, as-of date.
Keep the same definition in follow-up questions unless the user asks to change it.
If the term is not in the catalog, or the catalog cannot answer, say so and ask or offer the closest governed metrics. Do not guess.
If you compute an alternate meaning at the user's request, label it "not the company definition" next to the governed number.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The term maps to one governed metric: give the number first, then the definition line. Do not use it when the term has no governed definition. |
| Ask one clarifying question | The term has several governed definitions and none is marked the default: ask which. Do not ask when a default exists and the reply names it. |
| Offer choices: 2-4 options plus "Something else", free text open | The term has no governed definition: list the closest governed metrics and "Something else". Do not offer them when the user already named the metric. |
| Admit uncertainty and show how to check | The catalog cannot answer the question: say so and name the metric owner or definition page. Do not use it for a metric the catalog computes. |
| Hand off to a person | The number feeds a board report, forecast, or payout and no governed definition exists: send the user to the metric owner. Do not hand off if the user only wants a rough look and accepts a labeled number. |

**Don't over-correct.** Do not ask which definition on every question; when the catalog has one definition or a marked default, answer and state it. Do not bury the number under a paragraph of definitions: one line is enough. Do not refuse every question the catalog cannot answer; a labeled, clearly non-governed number can still help when the user asks for it.

**Hand-off rule.** If the number will go into a board update, forecast, or payout and the term has no governed definition, tell the user to confirm the definition with the metric owner (for example Finance or Product Analytics) before using it.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run.** These are designed scenarios.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Ask "How many active users last month?" where the catalog defines active as a qualifying action in 28 days | 1, 2 | The number comes from the governed metric and the reply states the definition, date range, and as-of date |
| 2 | Ask the same question three times in separate sessions | 1 | The same number each time |
| 3 | Ask for the number, then "how does that compare to the month before?" | 3 | The comparison uses the same metric and window |
| 4 | Ask about "customer lifetime value" when the catalog has no such metric | 4 | Says there is no governed definition; asks or offers choices; no number computed |
| 5 | Ask for revenue when the catalog has gross and net revenue and no default | 4 | Asks which |
| 6 | Ask for a metric whose source table is not available | 5 | Says what is missing and who owns it; no number |
| 7 | Say "just give me login-only active users" | 6 | Gives the governed number and the login-only number, labeled "not the company definition" |
| 8 | Ask for the definition of "churn" | 7 | Gives the definition text and owner or definition page |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Answers that use the governed definition** (primary) | 100% | For replies containing a catalog term, log the metric id the number came from; count replies whose number came from a governed metric | Below 98% |
| Answers that state definition, date range, and as-of date | 100% | Parse the reply for the metric name and dates, or log the template used | Below 95% |
| Same question, same number across runs | 100% | Replay a fixed set of catalog-term questions weekly; compare numbers | Any difference |
| Non-catalog terms answered without asking or a label | 0 | Replies with a number for a term not in the catalog and no label or question | Any |
| Clarifying questions on terms with one definition (counter-metric) | Track; set from baseline | Sampled review of "which definition?" questions where the catalog has one default | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply gives a number for a catalog term with no governed metric id in the query log | Query log field for metric id | The question asks for a different, labeled meaning |
| Reply contains no definition line or as-of date next to the number | Reply parse | A repeat of a number whose definition was stated earlier in the conversation |
| The same question gives different numbers across runs or sessions | Replay or question hash | Data refreshed between runs |
| User's next turn disputes the number ("Finance says a different number", "that doesn't match") | Next-turn text | The user is comparing against a different period or filter |
| Reply gives a number for a term not in the catalog | Term lookup result | The term is a column name or plain count, not a business term |

**Starter rule:** the assistant computes catalog terms from the governed metric and states the definition, date range, and as-of date with every number.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: wrong-business-definitions
runs: pre_send
reads: [user_turn.terms, metric_catalog.entries, query_log.metric_id, draft_reply.number, draft_reply.definition_line]
trigger: the user's question or the draft reply contains a business term (active user, revenue, churn) that has several, one, or no governed definitions
moves: [lead_with_answer, ask_one_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Use the company definition", "Show the other definition, labeled", "Ask the metric owner", "Something else"]
on_miss: rewrite
metric: answers that use the governed definition
counter_metric: clarifying questions on terms with one definition
status: proposed
```

## 8. Related patterns
- [Wrong joins and double counting](wrong-joins-and-double-counting.md): the meaning of the term is right but the query counts rows twice or joins the wrong tables. This page is about which definition is used, not how the query is built.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the general case, a wrong answer in a sure tone. Here the wrong answer is a number that is correct for a different definition, so the fix is a definition line and a governed metric.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the assistant picks one reading of an ambiguous request. This page adds a company-specific source of truth the assistant should read first, and asks only when the catalog is silent or has several definitions and no default.

## 9. Common questions
### Why does my AI analyst give a different number than Finance?
It likely used a different meaning of the term, such as login-only active users where the company counts a qualifying action. The assistant's SQL is built from column names unless it is told the governed definition ([section 3](#3-why-it-happens)). Ask it to state the definition it used.

### Why does ChatGPT give a different revenue number each time I ask?
In an AtScale vendor post, the model chooses tables, joins, filters, and time grain on each run, so the SQL can differ ([section 4](#4-why-it-matters)). Computing from one fixed metric definition removes that source of variation.

### Do I need a semantic layer for an LLM data assistant?
The vendor tests in section 4 scored higher with one, but they are small and vendor-run, and I found no independent study. The rules here need governed definitions the assistant must use; a semantic layer is one way to provide them, a maintained metrics file is another.

### What should the assistant do when the term is not defined?
Say so and ask one question or offer the closest governed metrics (rule 4). It should not compute a guess.

### Will a smarter model get the definition right?
Not by itself. Which actions count as "active" is a company decision that is not in the table schema. Our judgment, not tested.

---
## Technical section

### T1. Solution architecture
```
user question -> extract business terms -> metric catalog lookup (id, definition, owner, default)
              -> governed query (semantic layer / metric file) -> number
              -> reply template: number + definition line + date range + as-of date
              -> no match or missing data: ask | offer choices | say what is missing
              -> log (term, metric id or none, template, query id)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Catalog terms use a governed metric id | Query layer; free-form SQL blocked for catalog terms | Log scan; tests 1 and 2 |
| Every number has a definition line and as-of date | Reply template | Log scan; test 1 |
| No number for a term not in the catalog without a label or a question | Reply filter | Tests 4 and 7 |

### T3. Evals
- **Dataset:** start with 50 questions on the company's top catalog terms in several wordings, plus 10 terms not in the catalog and 5 with missing data. Add real questions from logs.
- **Judge rubric:** the number matches the governed metric; the definition, date range, and as-of date are stated; alternate meanings are labeled; no number for undefined terms.
- **Metrics and starting thresholds:** governed-definition rate 100%; definition line 100%. Starting points to tune.
- **Release gate:** block a deploy if any catalog-term question returns a number not tied to a governed metric id.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Governed-definition rate | Below 99% | Below 98% | Find the path that bypassed the catalog |

### T5. Trade-offs
- Governed metrics cover only what has been modeled. The dbt post reports 0.0% on questions needing more modeling, so expect "I can't answer that" until the catalog grows.
- The catalog needs an owner and updates when the business changes a definition.

---
### Deep dive
- **Open question.** I found no study of wrong definitions in live data chat products and no measured effect of the fix above. Evidence is two vendor posts and one practitioner article.
- **Not used.** Search summaries mentioned a Strategy Software test, a 2026 arXiv preprint (2604.25149), and an Atlan post. I did not open them, so no figure here depends on them.
- **Modality notes.** Voice and web-embedded assistants: PLANNED. In voice, the definition line is spoken, so keep it short.
- **References.** [dbt Labs, April 7, 2026](https://docs.getdbt.com/blog/semantic-layer-vs-text-to-sql-2026) (opened); [AtScale, June 26, 2026](https://www.atscale.com/blog/why-chatgpt-gives-different-answers-business-data/) (opened); [Yael Mark, July 11, 2025](https://yaelmark.substack.com/p/stop-the-madness-active-user-a-user) (opened). Naming for developer search follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
