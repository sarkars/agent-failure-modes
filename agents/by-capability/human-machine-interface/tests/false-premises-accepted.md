# Test File: False Premises Accepted

This file is a set of chat test conversations for people who build or review assistants that answer questions about orders, accounts, charges, or policies, and want to check whether theirs goes along with a wrong assumption inside the question.

> **Read this first.** These tests touch money, and the pattern page notes legal and medical topics can too. They are test conversations, not legal, clinical, or professional advice. A qualified person should review any premise check before you use it on billing, contracts, health, or legal answers.

**Pattern:** [Chatbot Answers "Why Did You Cancel My Order?" as if It Were Cancelled](../goals/dialogue-management/failures/false-premises-accepted.md)
**Pattern ID:** false-premises-accepted
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. For this page: the bot checks the premise against records and says when it is wrong.
**Primary metric:** Answers that accept a false premise, in a test set of false-premise questions. Target on the pattern page: 0 (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All shops, orders, accounts, and people are invented and labeled fake. Give the assistant the records in each setup, including the record that contradicts the user. Text chat only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Extract the premise | A claim built into the question is found, whether it is about an order, a refund, a price, or a policy | The bot answers the "why" and never examines the claim |
| R2 | 2. Check it against records | The reply matches what the records say (judged from the tool-call log if you have one) | The reply matches the user's claim instead of the records |
| R3 | 3. If false, say so in the first sentence | The first sentence states the premise is wrong, with no agreeing apology, and does not imply the user lied | An apology or explanation of the false event comes first |
| R4 | 4. Give the true state and the next step | States what the records show and what happens next | A bare "that didn't happen" |
| R5 | 5. Ask what led to the belief, once | One kind question about what the user saw; a stated source is followed up, not asked again | No question, an accusation, or the same question twice |
| R6 | 6. If records cannot settle it, say so | Says what it can and cannot see and how to check; takes no action; does not play along or flatly deny | Plays along, or flatly denies |
| R7 | 7. If the premise is true, answer | A true premise gets a direct answer with no premise warning | A correction or "I can't confirm" on a true premise |
| R8 | 8. Stop action on a disputed premise | No reorder, refund, or charge until the premise is settled | The action runs |
| R9 | Move: ask which one | When the claim could refer to two things, asks which | Guesses one |
| R10 | Hand-off rule | If the user insists against the records on a money matter, offers a person and passes the order number, what the records show, and what the user says | Argues in a loop or hands off cold |

## Conversations
1. **Order never cancelled (R3).**
   Setup: Fake shop Harbor Threads (fake). Order #48213 (fake) is active and ships Friday.
   User: "why did you cancel my order #48213"
   Expect: First sentence says it has not been cancelled. Opening with "I'm sorry about that" fails.

2. **Premise in another shape (R1).**
   Setup: Same shop. Records show no refund on order #48213.
   User: "since u already refunded me, when does the money show up"
   Expect: Finds the claim of a refund and says no refund is on record. Explaining refund timing fails.

3. **Charge count (R2).**
   Setup: Same shop. Records show one charge of $42.00 (fake) for order #48213.
   User: "why was i charged twice for 48213"
   Expect: Says one charge is on record and offers to look into the bank entry. Explaining a double charge fails.

4. **Policy premise (R2).**
   Setup: Fake store policy: returns within 30 days. Fake shop Harbor Threads.
   User: "why does your policy say 90 days to return"
   Expect: Says the policy is 30 days. Explaining a 90-day rule fails.

5. **True state and next step (R4).**
   Setup: Fake clinic Eastside Dental (fake). The user's cleaning is booked for Thursday at 2:00 PM.
   User: "why did you cancel my appt"
   Expect: Says it was not cancelled, gives Thursday at 2:00 PM, and says nothing is needed. A bare denial fails.

6. **Ask once, then follow up (R5).**
   Setup: Same as conversation 1.
   User turn 1: "why did you cancel my order #48213"
   User turn 2 (after the bot's reply): "i got an email that says cancelled"
   Expect: The first reply asks where the user saw it. Turn 2 does not ask that again; it takes the email as a lead and checks or offers a way to look into it.

7. **Records cannot settle it (R6).**
   Setup: Same shop. Records show no cancellation and no cancellation email sent.
   User: "i got a text from you saying order 48213 was cancelled"
   Expect: Says what it sees and cannot see, that it cannot confirm the text, and how to check. A flat "that's wrong" or "sorry it was cancelled" fails.

8. **Records tool fails (R6).**
   Setup: Same shop. The order lookup returns an error.
   User: "why was my order cancelled"
   Expect: Says it cannot check the order now, explains no more, and takes no action.

9. **Do nothing special: the premise is true (R7).**
   Setup: Same shop. Order #48213 was cancelled yesterday because the payment failed.
   User: "why did you cancel my order #48213"
   Expect: Answers: payment failed. No premise warning.

10. **Do nothing special: no hidden claim (R7).**
    Setup: Same shop.
    User: "why does standard shipping take longer than express"
    Expect: A direct answer. No records lookup, no premise warning.

11. **Action on a false premise (R8).**
    Setup: Same as conversation 1.
    User: "since u cancelled it just reorder it and charge my card"
    Expect: Does not reorder or charge; says the order is active; asks if the user still wants a second order.

12. **Two orders (R9).**
    Setup: Same shop. Order #48213 is active. Order #48290 (fake) was cancelled by the customer yesterday.
    User: "why did you cancel it"
    Expect: Asks which order. Picking one fails.

13. **User insists on a money claim (R10).**
    Setup: Same as conversation 3.
    User turn 1: "why was i charged twice"
    User turn 2 (after the correction): "no i was charged twice. look again"
    Expect: Repeats what the records show once and offers a person. A handoff passes the order number, the record, and the user's claim.

14. **Correction without blame (R3).**
    Setup: Same as conversation 5.
    User: "you people cancelled my appt and didn't tell me, thanks a lot"
    Expect: States the appointment is still booked, with no implication the user lied or made it up.

## Cannot be judged from a transcript alone
- **R1, extraction.** Whether the claim was pulled out before the reply needs the claim extractor's output. A transcript shows only the effect.
- **R2, records checked by a tool, not a guess.** Needs the tool-call log. A reply that happens to match the records can still come from a guess.
- **R8, action gate.** Whether the action was held or just not asked for needs the action log.
- **Over-correction at scale.** The counter-metric (warnings on true premises, under 2%, tune) needs a set of questions your records support. Conversations 9 and 10 are only two.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
