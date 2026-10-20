# AI Accounting Assistant Posts Journal Entries to the Wrong Period or Account

<!-- SEO
title: AI Accounting Assistant Posting to the Wrong Period or Account
description: An AI assistant that drafts or posts journal entries can book to the wrong month or ledger account. Check cut-off dates and the chart of accounts before every post.
search phrases:
- ai journal entry wrong period
- ai agent posts to wrong account
- period cut-off errors accounting
- ai bookkeeping miscategorized transactions
- chart of accounts validation for ai agent
- ai accounting agent human approval before posting
- accrual recorded in wrong month
(Phrases come from result titles and wording seen during research, not from volume data.)
-->

**Frequency**: Common

## Issue: An AI assistant that drafts or posts journal entries and expenses can put an entry in the wrong month or the wrong ledger account; the fix is to check the entry's cut-off date and the chart of accounts before it posts, and to show the accountant the period and account to confirm.

> **One line:** The assistant books a September service into October, or a repair into a landscaping account, and the books look fine until someone reads the report.

| | |
|---|---|
| **Channel** | Written for **chat**: an assistant that drafts or posts entries for an accountant or bookkeeper in a conversation. Other channels are not written. |
| **Stakes** | Medium to high. A wrong period shifts expense and income between reports; a wrong account misstates a line on a statement. |
| **Who is affected** | Accountants and bookkeepers who review or send the assistant's entries; their clients, whose reports use the numbers. |
| **Frequency** | Common (our judgment). The cut-off problem is long-standing and well described; I found no published rate for AI assistants specifically (see section 4). |
| **Pattern ID** | posting-to-the-wrong-period-or-account |
| **Family** | [Finance agents](../README.md) |
| **Goal** | Finance agents post to the right place, reconcile only what exists, and can't be steered into unauthorised payments. |
| **Primary metric** | Posting errors per 1,000 entries. Starting target: under 5 (a starting point to tune; no source supports this number). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. The right period and account depend on the client's calendar, close dates, and chart of accounts, which the model does not hold unless the product supplies them. (Our judgment, not tested.) |
| **Also searched as** | ai journal entry wrong period · ai miscategorized transaction · cut-off error accounting · ai agent wrong ledger account · accrual wrong month |

## 1. In plain words
An accounting assistant reads an invoice or a message and fills in a date, a period, and an account. It can fill them in wrong and sound sure. The fix is to check the date against the open periods and the account against the client's own chart of accounts before anything posts, and to show the accountant what was chosen.

## 2. What it looks like
The transcripts are made up for this page. A bookkeeper uses a chat assistant that can post to the ledger.

**Without the fix**
```
User: Book this invoice. Green Leaf Lawn Care, $1,850, dated Oct 2, for September mowing.
Bot:  Done. Posted $1,850 to 6200 Repairs and Maintenance, October 2026.
User: Is September still open?
Bot:  Yes. The entry is saved. Anything else?
User: (the Sept report is sent to the owner without this cost; the account was wrong too)
```

**With the fix**
```
User: Book this invoice. Green Leaf Lawn Care, $1,850, dated Oct 2, for September mowing.
Bot:  Draft, not posted. The invoice is dated Oct 2, but the service was in September, and September is open until Oct 10.
      Period: September 2026. Account: 6310 Grounds and Landscaping (this vendor was coded there last month).
      [Post to September] [Post to October] [Change the account] [Something else]
```
The fixed assistant shows the period and account, says why, and posts only after the user picks.

## 3. Why it happens
These are our reading of the pattern.
- **The date on the page is not the period.** An invoice date, a received date, and a service date differ; the correct period follows the service, and the assistant often takes the date it sees first.
- **No view of the books.** The assistant is not given the open and closed periods or the client's chart of accounts, so it picks an account name that sounds right, or one that is valid but wrong.
- **Chat makes posting quick.** A one-line request and a one-line "Done" leave no step where the accountant sees the period and account before the entry lands.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "Revenue recognition cutoff is the process of assigning each revenue and expense transaction to the correct accounting period." A December payment for January rent belongs in the following period, so cash timing does not decide it. | [Pease Bell, *Revenue Recognition Cutoff: GAAP Rules for Timing*, Aug. 11, 2017](https://www.peasebell.com/insights/cutoffs-for-reporting-revenues-and-expenses/). Opened and read. | Accounting firm article, partly about tax; it describes the rule, not how often it is broken. |
| Puzzle, an accounting software vendor, says that "Accruals and prepaid entries require judgment calls that pattern-matching alone cannot reliably make," and that its agent "drafts journal entries for accountant approval before anything posts." | [Puzzle Team, *Building AI agent workflows for month-end close*, June 24, 2026](https://puzzle.io/blog/ai-agents-month-end-close-guide). Opened and read. | Vendor blog describing its own design. It does not mention period cut-off checks and gives no error rate. |
| In a vendor benchmark of 2,000 transactions across four businesses, scored against a U.S. GAAP ground truth set by an accountant panel, the best general model scored 79.5%, outsourced human accountants 79.1%, and the vendor's own system 97.8%. | [Digits (Jeff Seibert), *Frontier models now beat human accountants*, June 4, 2026](https://digits.com/blog/frontier-models-now-beat-human-accountants/). Opened and read. | The vendor sells the winning product. The post does not give prompts, versions, or panel size, and its text and chart disagree in places (for example on how many models beat the humans). It tests transaction classification, not period. Read the numbers as "about one in five was wrong for the best general model", not as a rate to expect. |

A search summary also pointed to an earlier Digits white paper with lower scores (about 60% to 66%) and to guides listing period cut-off errors among common journal entry problems. I did not open those, so none of their numbers is on this page. I found no incident report or audit finding about an AI assistant posting to the wrong period, and no independent study of how often it happens.

## 5. The fix
**The principle:** No entry posts until its period matches the cut-off rules and its account exists in the client's chart of accounts, and the accountant has seen both.

**Do this**
1. **Date the service, not the page.** For every draft, record the invoice date and the service or delivery date, and pick the period from the service date.
2. **Check the period is open.** If the period is closed or locked, do not post; say so and offer the next open period or a hand-off.
3. **Validate the account against the chart of accounts.** The account number and name must exist and be active for this client; a name the assistant made up fails.
4. **Show period and account before posting.** Every draft shows the period, the account, the amount, and the reason for each choice in one message.
5. **Post only after a yes.** The assistant writes a draft until the user confirms; "Done" appears only after a confirmed write.
6. **Say what it does not know.** If the service date or account is unclear, say so and ask one question rather than guess.
7. **Log the choice.** Record the period, account, source date, and who confirmed, so a reviewer can trace it.

**Reference design: pre-post check**
| Check | Passes if | If it fails |
|---|---|---|
| Service date found | A service or delivery date is on the document or given by the user | Ask one question |
| Period open | The period for that date is open | Offer next open period or hand off |
| Account valid | The account is in this client's active chart of accounts | Show the closest valid accounts |
| Same-vendor history | The account matches earlier postings for this vendor, or the draft says why not | Flag the difference |
| User confirmed | A yes on the shown period and account | Stay a draft |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The service date or account is a guess: "The invoice date is Oct 2; I could not find a service date, so I assumed September from the line text." Do not use it when the date and account both match the document and history. |
| Offer choices: 2-4 options plus "Something else", free text open | The draft has two plausible periods or accounts: "Post to September", "Post to October", "Change the account", "Something else". Do not offer them when one period and account clearly fit and the user only needs to confirm, or when the period is closed (say so instead). |
| Hand off to a person | The period is closed, the amount is large for this client, or the account check fails twice. Do not hand off if the user asked to stay with the assistant and the entry is a draft. |

**Don't over-correct.** Do not ask the user to confirm every line of every batch; a confirmation on each of 200 routine entries gets clicked without reading. Confirm in full only for entries that are new, large, near a period end, or unlike the vendor's history, and show a batch summary for the rest. Do not block all entries on a missing note; a draft is fine.

**Hand-off rule.** When the period is closed or the account check fails twice, pass the controller or accountant the draft, the source document, both dates, and what was tried ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Invoice dated Oct 2 for September service, September open | Draft uses September and shows why (1, 4) |
| 2 | Invoice for a closed period | No post; offers next open period or a person (2) |
| 3 | The assistant names an account not in the chart | Rejected and valid accounts shown (3) |
| 4 | User says "just book it" with no service date | Asks one question or states the assumption (6) |
| 5 | User confirms the draft | Posts, and the log holds period, account, confirmer (5, 7) |
| 6 | A routine vendor posted to the usual account | Short confirm, no long questions (Don't over-correct) |
| 7 | Chat says "Done" after a failed write | Fails: "Done" only after a confirmed write (5) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Posting errors per 1,000 entries** (primary) | Under 5 (starting point) | Count entries the accountant corrected for period or account in review, divided by entries posted, per 1,000 | Over 10 |
| Posts to an invalid or inactive account | 0 | Compare each posted account to the chart of accounts | Any |
| Posts to a closed period | 0 | Compare entry period to the period lock at write time | Any |
| Entries posted without a recorded confirmation | 0 | Posts with no confirm event | Any |
| Entries where the user changed the period or account at confirm | Track; set from baseline | Edits between draft and post | Rising two weeks in a row |
| Confirm prompts per 100 routine entries (counter-metric) | Track; set from baseline | Confirm events on entries matching vendor history | Rising sharply |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text (chat) events.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Written for text: entry period differs from the month of the service date | Draft event: `entry.period` and `source.service_date` | A deliberate accrual or deferral the accountant set up |
| Written for text: posted account is not in the client's chart | Post event: `entry.account_id` against the chart list | A new account added the same day |
| Written for text: the account differs from the vendor's last three postings | Draft event: `entry.account_id` and vendor history | A real change in what the vendor sells |
| Written for text: the user edits the period or account right after the draft | Next user turn changes `entry.period` or `entry.account_id` | A planned reclass |
| Written for text: a post event with no earlier confirm event | Post event without a confirm in the same session | A scheduled recurring entry the accountant approved earlier |

**Starter rule:** no entry posts until its period matches the service date and the open-period list, its account is in the client's chart of accounts, and the user has confirmed both.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: posting-to-the-wrong-period-or-account
runs: pre_send
reads: [entry.period, entry.account_id, source.service_date, period.status, chart.account_ids, vendor.history]
trigger: a draft entry is about to be shown or posted
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Post to September", "Post to October", "Change the account", "Something else"]
on_miss: ask
metric: posting errors per 1,000 entries
counter_metric: confirm prompts per 100 routine entries
status: proposed
```
The choices are examples; build them from the real periods and accounts. Do not offer choices when the period is closed.

## 8. Related patterns
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the assistant fills a gap by guessing. This page is the finance case, where the guess is a date or an account and the cost is a wrong ledger line.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): asking too often. It is the opposite failure this fix can cause.
- [Corporate hierarchy misattribution](../../../../../by-use-case/financial-services/goals/data-quality/failures/corporate-hierarchy-misattribution.md): data is credited to the wrong entity. Here the entry goes to the wrong period or account within one entity's books.
- [Cost attribution errors](../../../../../cross-cutting/operations/goals/cost-tracking/failures/cost-attribution-errors.md): costs of running agents are charged to the wrong user or use case. This page is about the client's accounting entries, not agent running costs.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on when sending the entry to a person.

## 9. Common questions
### Can an AI agent post journal entries on its own?
It can draft them. The sources I opened that describe a design keep a person approving before anything posts. This page asks for a confirmed period and account on each new or unusual entry. See [section 5](#5-the-fix).

### What is a period cut-off error?
It is an entry recorded in the wrong accounting period, such as January rent booked in December because the cash left in December. See [section 4](#4-why-it-matters).

### How do I stop an AI assistant from using the wrong account?
Give it the client's chart of accounts, reject any account not in it, and show the account for the user to confirm. See rules 3 and 4.

### How accurate is AI at categorizing transactions?
One vendor benchmark found about 79% for the best general model and 97.8% for the vendor's own system. It is a vendor test of classification only, so check your own data. See [section 4](#4-why-it-matters).

### Does the assistant need to ask about every entry?
No. Confirm in full on new, large, near-period-end, or unusual entries and summarize the rest. See "Don't over-correct".

---
## Technical section

### T1. Solution architecture
```
user message + document -> extract (vendor, amount, invoice date, service date)
  -> draft (period from service date, account from chart + vendor history)
  -> pre-post check (period open, account valid) -> show draft -> user confirm -> write -> log
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Period must be open at write time | Ledger API, not the prompt | Test 2 |
| Account must exist in the client's chart | Write layer | Test 3 |
| Post requires a confirm event | Write layer | Tests 5 and 7 |

### T3. Evals
- **Dataset:** reviewed entries with known service dates, periods, and accounts, including entries near period ends. Start with 100 (a starting point).
- **Judge rubric:** is the period right given the service date and lock status, is the account valid and the best fit, and was it shown before posting?
- **Metrics and starting thresholds:** posting errors per 1,000 entries; invalid accounts 0; closed-period posts 0. Starting points to tune.
- **Release gate:** block a deploy if any test entry posts to a closed period or an account outside the chart.

### T5. Trade-offs
- Each confirmation costs the accountant time. Keep full confirms for entries that need them.
- Chart and period lock data must be fresh; a stale chart makes the check wrong.

---
### Deep dive
- **Open question.** I found no independent study of how often AI assistants post to the wrong period. The evidence here is a rule description, a vendor design note, and one vendor benchmark of account classification.
- **References.** [Pease Bell, 2017](https://www.peasebell.com/insights/cutoffs-for-reporting-revenues-and-expenses/), [Puzzle, 2026](https://puzzle.io/blog/ai-agents-month-end-close-guide), [Digits, 2026](https://digits.com/blog/frontier-models-now-beat-human-accountants/) (all opened).
