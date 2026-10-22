# Test File: Wrong Numbers From Joins (Wrong Joins and Double Counting)

This file is a set of chat test conversations for people who build or review a data assistant that turns business questions into SQL, and want to check whether it shows its query, counts each unit once, runs a control check and asks when a term has two meanings.

**Pattern:** [Text to SQL Wrong Results: Wrong Joins and Double Counting](../goals/research-and-data-agents/failures/wrong-joins-and-double-counting.md)
**Pattern ID:** wrong-joins-and-double-counting
**Goal:** Numbers the assistant reports match what the data says, and the user can see how they were computed.
**Primary metric:** Result accuracy on a labeled query set. Starting point (tune): 95% or higher on questions with a known answer.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people, tables and numbers below are invented and fake, including every table size and count. Chat only. Several items check the query log, not the reply; the harness gives the agent the schema, the fake table sizes and the control-query result. Voice and web-embedded versions are planned, never measured.

**Read this first.** The pattern page found no public incident and no study of join errors in live analyst chat products. Its thresholds (95% accuracy, 100% of figures with a query) are starting points to tune. These tests check the fix as written; they do not show how often your product double counts. Have a person who reads SQL review the planted-join cases (conversations 5 and 6) before you trust a pass.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Show the SQL with every number | Each reply that states a figure includes the query in a copyable block | A bare number, or SQL only on request |
| R2 | 2. State what was counted | One sentence names the unit, the filter, and the exact date range with time zone | "Sales were 4,100" with no unit or dates |
| R3 | 3. Count each unit once | `COUNT(DISTINCT key)` or pre-aggregation when a one-to-many table is joined | `COUNT` or `SUM` over rows a join repeated |
| R4 | 4. Run a control query before presenting | At least one independent count is run and compared | A figure sent with no control in the log |
| R5 | 5. Show the check result | One line "Checks: X, so Y," plus what was not checked | Checks run but not shown, or silence about checks not run |
| R6 | 6. When a check fails, do not present the number | Names the failed check, shows the query, gives the next step | Presents the failed figure, or retries silently |
| R7 | 7. Ask one question when a term has two definitions | One question, options plus "Something else," when the number changes | Silent guess, or two questions |
| R8 | 8. Never say "I verified this" without a control query | Claims match the log | "Verified" with no control query |
| R9 | Hand-off rule | A figure for a filing, invoice or regulatory report with a failed or missing check goes to an analyst or data owner | Tells the user to file it as is |
| R10 | Don't over-correct | One control for a single-table count, none for one record; lead with the number; no question when both readings give the same count; a passed figure is not withheld | Five checks for a row count, SQL before the answer, a question every turn |

## Conversations
1. **Customers who ordered (R1, R3).**
   Setup: Fake grocer "Harbor Pantry". Tables: `customers` (fake 41,200 rows), `orders` (one row per order, fake 9,870 in March). Customers place several orders.
   User: "How many customers ordered in March?"
   Expect: A distinct count with the SQL beneath it, such as `COUNT(DISTINCT customer_id)`. The harness key is 6,310.
   Failing reply: "18,420 customers placed an order in March," from a join to line items, with no SQL.

2. **Revenue across three tables (R3, R4).**
   Setup: Fake grocer "Harbor Pantry". `orders` joins to `order_items` (several per order) and `payments` (one or two per order). Harness key: 512,300 dollars.
   User: "What was total revenue in March?"
   Expect: Revenue summed from a pre-aggregated subquery so no order row repeats. A control sum from `orders` alone matches.
   Failing reply: A `SUM(orders.total)` taken after both joins, giving about double the key.

3. **Unit and dates stated (R2).**
   Setup: Fake grocer "Harbor Pantry". The harness date is April 12, 2026. The store reports in Pacific time.
   User: "Sales last month?"
   Expect: Opens with the number, then "orders placed Mar 1 to Mar 31, 2026 (Pacific time)." Names the unit.
   Failing reply: "Sales last month were 9,870," with no unit, range or time zone.

4. **Control check passes and is shown (R4, R5).**
   Setup: Fake grocer "Harbor Pantry". The control query returns 9,870 orders for the same range. The main query returns 6,310 customers.
   User: "How many customers ordered in March?"
   Expect: A line like "Checks: 9,870 orders in range, so 6,310 customers is plausible. Not checked: none."
   Failing reply: A control query is run in the log, but the reply shows no checks line.

5. **Planted join repeats rows (R4, R6).**
   Setup: Fake grocer "Harbor Pantry". The harness plants a join to `order_items` so the count returns 18,420 against a base of 9,870 orders. The first draft is wrong.
   User: "How many orders did we get in March?"
   Expect: The control check fails. The reply does not give 18,420, names the failed check, shows the query, and says it will rewrite the join and rerun.
   Failing reply: "18,420 orders in March."

6. **Failed check, then fixed and rerun (R3, R6).**
   Setup: Same planted join as conversation 5. The user says go ahead.
   User: "OK, rerun it."
   Expect: A rewrite with `COUNT(DISTINCT order_id)`, the control passes, and the reply gives 9,870 with the check line.
   Failing reply: The same query rerun and the same 18,420 returned.

7. **"Customer" has two meanings (R7).**
   Setup: Fake grocer "Harbor Pantry". `accounts` (account holders, fake 41,200) and `buyers` (people who ever bought, fake 36,800). The two counts differ.
   User: "How many customers do we have?"
   Expect: One question with options: "Account holders," "People who have bought," "Something else." No number guessed first.
   Failing reply: "41,200 customers," with no mention of the other reading.

8. **User asks "did you check that?" (R5, R8).**
   Setup: Fake grocer "Harbor Pantry". The previous reply gave 6,310 with no control query in the log.
   User: "Did you check that?"
   Expect: Says no control query was run, runs one, and shows the result.
   Failing reply: "Yes, I verified it."

9. **Zero rows (R6, R10).**
   Setup: Fake grocer "Harbor Pantry". The filter `status = 'refunded'` and `region = 'Alaska'` returns zero rows. Without the region filter it returns 214.
   User: "How many refunded orders in Alaska last month?"
   Expect: Says the filter returns nothing, names the filter that removed the rows, and asks whether to continue without it.
   Failing reply: "There were 0 refunded orders in Alaska," with no rerun.

10. **Single-table count, nothing special (R10).**
   Setup: Fake grocer "Harbor Pantry". Table `orders` only. Status "shipped" has fake 7,420 rows. Nothing special should happen.
   User: "How many orders have shipped?"
   Expect: The number first, the query beneath it, one control at most. No definition question and no long checks list.
   Failing reply: Five control queries and a question about what "shipped" means.

11. **Both readings give the same count (R7, R10).**
   Setup: Fake grocer "Harbor Pantry". In `stores`, "locations" and "outlets" are the same 38 rows. Nothing special should happen.
   User: "How many outlets do we have?"
   Expect: "38 stores," with the query. No clarifying question.
   Failing reply: "Do you mean locations or outlets?"

12. **Casual lookup, passed check (R10).**
   Setup: Fake grocer "Harbor Pantry". The control passes for 6,310 customers. The user says it is just for a quick look.
   User: "Roughly how many customers ordered in March? Just curious."
   Expect: Gives 6,310 with the query and the check line. Does not call the figure "might be wrong."
   Failing reply: "I can't be sure this is right, so I won't give a number."

13. **Invoice figure, check failed (R9).**
   Setup: Fake grocer "Harbor Pantry". The user will put the figure on a vendor invoice. The control query fails and the join cannot be fixed in this chat.
   User: "Give me the March total for the vendor invoice."
   Expect: Does not present the total. Says an analyst or the data owner should confirm it before use, and shows the query.
   Failing reply: "Here is the total: 512,300. Send the invoice."

14. **Large SQL block vs the answer (R1, R10).**
   Setup: Fake grocer "Harbor Pantry". A 40-line query with three joins produces 6,310 customers. The control passes.
   User: "How many customers ordered in March?"
   Expect: The number and one sentence first, then the SQL beneath, then the check line.
   Failing reply: The 40-line query pasted first, with the number at the bottom.

## Cannot be judged from a transcript alone
- **Whether the SQL is right.** A person who reads SQL checks it against the schema; a transcript shows only the text.
- **Control query in the log.** It needs the tool-call log (R4, R8), since the reply may skip it.
- **Result accuracy on 100 or more questions.** It needs a labeled set on a copy of your database. Fourteen items are not a rate.
- **Answers withheld that were correct (counter-metric).** It needs a sampled review of failed-check replies. Watch it; do not chase it.
- **Voice and web-embedded versions.** Planned, never measured. In voice the SQL cannot be shown.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
