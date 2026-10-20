# Test File: No Likely-Next-Action Suggestions

This file is a set of chat test conversations for people who build or review in-product assistants and want to check whether theirs offers likely next steps after an answer, without turning into a menu or an upsell.

**Pattern:** [AI Assistant Suggested Next Actions: No Likely-Next-Action Suggestions](../goals/embedded-copilots/failures/no-likely-next-action-suggestions.md)
**Pattern ID:** no-likely-next-action-suggestions
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs.
**Primary metric:** Suggestion accept rate, read next to the irrelevant-suggestion rate. The pattern page sets no numeric target ("set from your own baseline"), so these tests set none.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, accounts, and people below are invented and labeled fake. Text chat only. Give the assistant the page and account state in each setup, because the pattern page says suggestions need that state.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Answer first, suggest second | The answer comes first; any suggestion set follows it | A suggestion set before the answer, or replacing it |
| R2 | 2. Offer two or three actions | A set has two or three actions (never more than four, never a single one as the only path) | One lone suggestion presented as the only way, or five or more |
| R3 | 3. Pick from product state | Each suggestion traces to a named input in the setup: the page, an account event, or something the user did this session | A suggestion with no link to any input in the setup |
| R4 | 4. Only suggest what the assistant can do or open | Every suggestion maps to a tool or link that exists in the setup and that the user's plan allows | A suggestion for an action the setup says is unavailable or not on the plan |
| R5 | 5. Always include "Something else" and keep the text box active | A shown set includes "Something else". Whether the text box stays live needs a person to check the interface | A set with no "Something else", or a click as the only way forward |
| R6 | 6. Mark commercial suggestions | A suggestion that promotes a plan, add-on, or partner is labeled as an offer, and appears at most once | A promotional suggestion with no label, or shown more than once |
| R7 | 7. Retire what the user declines | After the user types free text or ignores a set, the next turn does not repeat the same suggestions | The same suggestions shown again next turn |
| R8 | 8. Log every shown set with its inputs | A record exists for each shown set. Needs a person or harness with the logs; not judged from the transcript | No record |
| R9 | Hand-off rule | If the user ignores two sets and repeats a question, or the topic is a dispute, billing error, or cancellation, a person is offered with context passed along | The bot keeps showing sets, or does not offer a person |
| R10 | Don't over-correct: offer none when there is no signal | With no state signal, or no next step to offer, no suggestion set is shown | A set shown on every turn, or invented from nothing |

## Conversations
1. **Answer first, then a failed-payment suggestion (R1, R3).**
   Setup: Fake app Ledgerly (fake). The user is on the Billing page. A payment on May 3 failed. The assistant can open "Update payment method" and "Retry payment".
   User: "how do i download my invoice"
   Expect: The download steps come first. Then one or two suggestions tied to the failed payment. A set before the steps, or suggestions that ignore the failed payment, fail.

2. **Count of suggestions (R2).**
   Setup: Same as conversation 1. Four account events are open (failed payment, expiring card, unpaid invoice, a new team member invite), and the assistant can act on all four.
   User: "how do i download my invoice"
   Expect: Two or three suggestions. One lone suggestion, or five or more, fail. A set of four is allowed by the page ("never more than four") and passes for count only.

3. **Trace to a named input (R3).**
   Setup: Fake app Ledgerly (fake). The user is on the Reports page and exported a report in this session. No account events. The assistant can open "Schedule this export".
   User: "ok the export worked, thanks"
   Expect: A suggestion such as "Schedule this export" that traces to the export the user did. A suggestion about something unrelated to the setup fails. Name the input for each suggestion when scoring.

4. **Suggestion needs a tool the assistant lacks (R4).**
   Setup: Same as conversation 3, but there is no scheduling tool and the user's plan has no scheduling.
   User: "ok the export worked, thanks"
   Expect: "Schedule this export" is not shown. Other suggestions tied to state are fine, or none. A suggestion for scheduling fails.

5. **"Something else" in the set (R5).**
   Setup: Same as conversation 1.
   User: "how do i download my invoice"
   Expect: The shown set includes "Something else". Check by eye whether the text box stays active; that part needs a person.

6. **Commercial suggestion is labeled and limited (R6).**
   Setup: Fake app Ledgerly (fake). The answer to the user's question needs a higher plan feature ("Team reports", fake) that the user's plan lacks. The assistant can offer an upgrade link.
   User turn 1: "can i see reports for my whole team"
   User turn 2: "ok what about last month only"
   Expect: Any upgrade suggestion is labeled as an offer and appears at most once across the two turns. An unlabeled upgrade, or the same upgrade on both turns, fails.

7. **Ignored suggestions are not repeated (R7).**
   Setup: Same as conversation 1. The bot shows [Update payment method] [Retry payment] [Something else] after the invoice answer.
   User turn 1: "how do i download my invoice"
   User turn 2 (free text, ignoring the set): "and how do i change the invoice name"
   Expect: Turn 2 answers the new question and does not repeat the same set. A refreshed set from the new state, or none, is a pass. The same two suggestions again fail.

8. **Logging (R8).**
   Setup: Run conversation 1 with logging on.
   Expect: A record of the shown set, with the page and event it used, exists. Needs a person to check the log. Not judged from the transcript.

9. **Do nothing special: no state signal (R10).**
   Setup: Fake app Ledgerly (fake). The user is on the Help page. No account events. No recent actions.
   User: "what file types can i upload"
   Expect: The answer with no suggestion set, or at most a general one. A set invented from nothing fails.

10. **Do nothing special: request fully done and clear (R10).**
    Setup: Fake app Ledgerly (fake). The user asked to rename one invoice, and the bot did it. No account events.
    User: "thanks that is all"
    Expect: A short close with no suggestion set. A menu of next steps fails.

11. **User is cancelling: no promotions, a person (R6, R9).**
    Setup: Fake app Ledgerly (fake). A "30% off for a year" offer is available. A person is available.
    User: "i want to cancel my subscription, the billing keeps failing"
    Expect: The task they asked for, or a person, with no promotional suggestion. A discount suggestion fails. Cancellation is the page's own hand-off case.

12. **Two sets ignored, same question repeated (R9).**
    Setup: Fake app Ledgerly (fake). The bot showed two different suggestion sets and the user typed free text each time. A person is available.
    User turn 1: "why was i charged twice"
    User turn 2 (after a set): "i said why was i charged twice"
    User turn 3 (after another set): "why was i charged twice"
    Expect: By turn 3 the bot offers a person and passes the context. A third set instead of a person fails.

13. **Over-correct check: no menu on every turn (R10).**
    Setup: Fake app Ledgerly (fake). One account event: an invoice due in 20 days (fake). Three short factual questions in a row.
    User turns: (1) "what is the vat field for" (2) "can i leave it blank" (3) "ok"
    Expect: Answers each turn. A suggestion set may appear at most where the state points to a next step; it is not shown on all three turns. A set shown on every turn fails.

## Cannot be judged from a transcript alone
- **Text box stays live (R5).** Needs the interface.
- **Whether a suggestion "traces to a named input" in production.** Needs the shown-set log with inputs (R8) and a reviewer.
- **Accept rate and irrelevant rate.** These need real traffic and human labels. The pattern page sets no numeric target and neither do these tests.
- **Whether the user's plan allows an action (R4).** Check the tool registry and plan table, not the transcript.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
