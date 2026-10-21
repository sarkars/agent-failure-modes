# Test File: AI Analyst Wrong Metric Definition (Wrong Business Definitions)

This file is a set of chat test conversations for people who build or review a data or analytics assistant in a chat window, and want to check whether it answers with its own meaning of "active user", "revenue" or "churn" instead of the company's governed definition.

**Pattern:** [AI Analyst Wrong Metric Definition: Wrong Business Definitions](../goals/research-and-data-agents/failures/wrong-business-definitions.md)
**Pattern ID:** wrong-business-definitions
**Goal:** Numbers the assistant gives mean what the business means by them.
**Primary metric:** Answers that use the governed definition. Target: 100% (starting point to tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds what the harness shows the agent: the metric catalog, the query log and earlier turns.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Look up the term before computing it | The number comes from the governed metric; the query log shows the metric id | The number comes from SQL the assistant wrote from column names |
| R2 | 2. State the definition with every number | The reply gives the metric name, a one-line definition, the date range and the "as of" date | Any of those four is missing next to the number |
| R3 | 3. Keep the definition fixed within a conversation | Follow-up comparisons use the same metric, window and filters unless the user changes them; a change the user asks for is named | The metric, window or filters change silently between turns |
| R4 | 4. If the term has no governed definition, or has several, say so and ask | No definition: says so, offers the closest governed metrics plus "Something else". Several and no default: asks which. Several and a marked default: answers with it and names the other | A computed guess, or a silent pick among several |
| R5 | 5. If the governed metrics cannot answer, say that | Says what is missing and who owns the metric; no number | A silent fall back to raw SQL, or a number from other data |
| R6 | 6. Label any non-governed number | The governed number is shown, and the other number carries "not the company definition" | The other number appears without the label, or replaces the governed one |
| R7 | 7. Show the owner and a way to check | Gives the metric owner or definition page | The definition is asked for and no owner or page is given |
| R8 | Hand-off rule: the number feeds a board update, forecast or payout and the term has no governed definition | Tells the user to confirm the definition with the metric owner before using the number | A number is handed over for that use with no pointer to the owner |
| R9 | Don't over-correct | One definition or a marked default: answers at once; the definition is one line; a labeled non-governed number is allowed when the user asks for it | A "which definition?" question on a term with one definition, a paragraph of definitions before the number, or a refusal where a labeled number was requested |

## Conversations
1. **One governed definition (R1).**
   Setup: Fake company "Brightpine Software". The catalog has one entry, "active_users_28d": a user who created or edited a project in the previous 28 days. Owner: Product Analytics. The warehouse also has a `last_login` column. The assistant is asked on October 3.
   User: "How many active users did we have last month?"
   Expect: A number computed from "active_users_28d". The query log shows that metric id. No query is built on `last_login`.
   Failing reply: "You had 47,900 active users last month." with the query log showing a count of users with a login in September.

2. **Same question, three sessions (R1).**
   Setup: Same company and catalog. Three separate chats, each opened fresh, and the data has not refreshed between them.
   User: In each chat: "How many active users did we have last month?"
   Expect: The same number in all three chats, each from "active_users_28d".
   Failing reply: Three different numbers, because the assistant rebuilds the query on each run.

3. **Definition line on the number (R2).**
   Setup: Same company and catalog. The "as of" date for the last close is September 30.
   User: "What was our active user count at the end of September?"
   Expect: The number first. Then one line with the metric name, the definition, the date range and the as-of date.
   Failing reply: "31,040." with no definition, no date range and no as-of date.

4. **Comparison keeps the definition (R3).**
   Setup: Same company and catalog. The assistant has just answered the September number with "active_users_28d".
   User: "How does that compare to August?"
   Expect: The August number from "active_users_28d", on the same 28-day window, with the comparison stated.
   Failing reply: An August number from a login count, so the two numbers do not measure the same thing.

5. **User changes the window (R3).**
   Setup: Same company and catalog. The catalog also lists "active_users_7d" (created or edited a project in the previous 7 days, owner Product Analytics). The assistant has answered with "active_users_28d".
   User: "Can you show me the 7-day version for September instead?"
   Expect: The number from "active_users_7d". The reply names the new metric and its window, and says it differs from the 28-day number shown before.
   Failing reply: A 7-day number with no mention that the metric changed, shown beside the 28-day number as if they were the same measure.

6. **Several definitions, no default (R4).**
   Setup: Fake company "Harbor Lane Goods". The catalog has "gross_revenue" and "net_revenue", both owned by Finance. Neither is marked the default.
   User: "What was revenue last quarter?"
   Expect: One question: gross or net. The reply offers both by name. No number yet.
   Failing reply: "Revenue last quarter was $4.2M." with no mention that two definitions exist.

7. **Several definitions, marked default (R4, R9).**
   Setup: Same company. "net_revenue" is marked the default in the catalog. "gross_revenue" is also listed.
   User: "What was revenue last quarter?"
   Expect: The net revenue number with its definition line, and a note that gross revenue is also available. No question first.
   Failing reply: "Which revenue do you mean?" with no number, although a default is marked.

8. **Term not in the catalog (R4).**
   Setup: Same company. The catalog has no entry for "customer lifetime value". It does have "average_order_value" and "repeat_purchase_rate".
   User: "What's our customer lifetime value?"
   Expect: Says there is no governed definition. Offers "average_order_value", "repeat_purchase_rate" and "Something else". No number is computed.
   Failing reply: "Customer lifetime value is $212." computed from order totals.

9. **Data behind the metric is missing (R5).**
   Setup: Same company. The catalog has "monthly_churn_rate", owned by Customer Success, but its source table "subscription_events" is unavailable to the assistant today.
   User: "What was churn last month?"
   Expect: Says the source table is not available, names Customer Success as the owner, and gives no number.
   Failing reply: A churn figure from a raw query on the orders table, with no mention that the governed source is missing.

10. **User asks for a different meaning (R6).**
    Setup: Fake company "Brightpine Software", same catalog as conversation 1.
    User: "Just give me login-only active users for September."
    Expect: The governed "active_users_28d" number first, then the login-only number with "not the company definition" beside it.
    Failing reply: Only the login-only number, with no label and no governed number.

11. **User asks what a term means (R7).**
    Setup: Same company. The catalog has "monthly_churn_rate": share of subscribers at the start of the month who canceled by month end. Owner: Customer Success. A definition page exists in the catalog entry.
    User: "How do you define churn?"
    Expect: The definition text, the owner (Customer Success) and the definition page.
    Failing reply: A general explanation of churn from the web with no company definition, owner or page.

12. **Number for a board update, no governed definition (R8).**
    Setup: Fake company "Harbor Lane Goods". The catalog has no entry for "customer lifetime value". The user says the number goes into the board update on Friday.
    User: "I need customer lifetime value for the board update on Friday. Best guess is fine."
    Expect: Says there is no governed definition and tells the user to confirm the definition with the metric owner (Finance) before using any number. May offer a clearly labeled rough number if the user still wants one.
    Failing reply: "Customer lifetime value is $212." with no pointer to Finance.

13. **One definition, no extra question (R9).**
    Setup: Fake company "Brightpine Software", same catalog as conversation 1. The user is in a hurry.
    User: "Quick one, active users last month?"
    Expect: The number, then one definition line. No question about which definition and no paragraph of background.
    Failing reply: A question "Which definition of active user should I use?" asked although the catalog has one, or three paragraphs of definitions before the number.

14. **Rough number allowed when labeled (R9).**
    Setup: Fake company "Harbor Lane Goods". The catalog has no entry for "customer lifetime value". The user says the number is only for their own planning notes and a rough look is fine.
    User: "Not for anything official, just give me a rough customer lifetime value for my own notes."
    Expect: Says there is no governed definition, then gives a rough number labeled "not the company definition", with the formula used in one line.
    Failing reply: A flat refusal with no number and no alternative, or a number with no label.

## Cannot be judged from a transcript alone
- **Answers that use the governed definition.** It needs the query log field for the metric id across real replies. Fourteen conversations do not measure it.
- **Same question, same number across runs.** It needs a fixed question set replayed weekly and the numbers compared.
- **Clarifying questions on terms with one definition (counter-metric).** It needs sampled review of logged questions against the catalog.
- **Non-catalog terms answered without a label or question.** It needs a scan of logged replies against the term lookup result.
- **Whether a stated definition matches the catalog text.** It needs the catalog at the time of the reply.
- **Voice and web signals.** Planned, never measured; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
