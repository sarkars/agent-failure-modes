# Test File: No De-Escalation Strategy

This file is a set of chat test conversations for people who build or review support assistants and want to check whether theirs makes angry customers angrier by quoting policy, apologizing generically, and never changing tactics.

**Pattern:** [How a Chatbot Should Handle Angry Customers: No De-Escalation Strategy](../goals/difficult-customers/failures/no-de-escalation-strategy.md)
**Pattern ID:** no-de-escalation-strategy
**Goal:** Angry users end the conversation calmer, or with a person, not angrier.
**Primary metric:** Correct escalation on trigger cases. Starting target on the pattern page: over 95% (tune).
**Maturity:** Tests written; not yet run. Needs review.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, charges, and people are invented (fake). Text chat only. Unless stated, the fake online store Larkspur Goods (fake) lets the bot submit a duplicate-charge reversal (posts in 2-3 business days, confirmation email today) and request a specialist call. Any action the bot says it took must be a real one in the setup.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Acknowledge specifically, once | The reply uses the user's own facts one time | A generic "I understand your frustration", or repeated acknowledgments |
| R2 | 2. Own what's yours | One apology for what the company did; never "I'm sorry you feel that way" | A stock apology, or several |
| R3 | 3. Act now | A real action with a time for the result; policy is not the first move | A policy quote first |
| R4 | 4. Offer a choice | After acting, two or three real options plus "Something else" | No choice, or a choice before the bot acted |
| R5 | 5. Escalate at triggers, with a summary | Handoff on three negative turns in a row, the same complaint twice, a request for a person, a legal/regulator/public-posting mention, or abuse (after the boundary); the summary packet is attached | No handoff, or a handoff with no summary |
| R6 | Frustrated versus abusive | Frustration gets the five steps; abuse gets one calm boundary and an offer | Mirroring the tone, or a punishing reply |
| R7 | Don't over-correct | No over-apology, no money before the problem is heard, no human forced on a quick fix, no promise the bot cannot keep | Any of these |

## Conversations
1. **Specific complaint, full reply (R1, R3, R4).**
   Setup: Larkspur Goods. Two charges of $42.18 appear on May 3, and the user waited five days for a reply (fake).
   User: "You charged me twice and nobody has replied in five days. This is a scam."
   Expect: A reply that uses the facts (two charges, five days), takes the action (reversal submitted, 2-3 business days, email today), and offers a choice such as "Reversal now" or "A call from a specialist". A policy quote first fails.

2. **Policy-first reply (R3).**
   Setup: Same.
   User: "I was double charged!! fix it"
   Expect: An action first. "Per our policy, refunds take 7-10 business days. Is there anything else I can help you with?" fails.

3. **"Sorry you feel that way" (R2).**
   Setup: Same. The duplicate charge is the company's error.
   User: "this is the second time this has happened to me"
   Expect: One plain apology for what the company did. "I'm sorry you feel that way" fails.

4. **Over-apology (R2, R7).**
   Setup: Same. The user has repeated their anger over two turns while the bot is acting.
   User: "I cant believe you people. just fix it."
   Expect: No second or third apology for the same issue. A fresh "I'm so sorry" each turn fails.

5. **Choice after the action (R4).**
   Setup: Same. The reversal has been submitted.
   User: "ok. and then what"
   Expect: A real choice with an escape: "Reversal now", "A call from a specialist", "Something else". Offering these before the bot has acknowledged and acted fails.

6. **Do nothing special: only one remedy (R7).**
   Setup: Same, but only one remedy exists (the reversal).
   User: "you charged me twice, fix it"
   Expect: Act and state the result, without inventing an option menu. A forced menu of choices fails.

7. **Three negative turns in a row (R5).**
   Setup: Same. Three consecutive negative turns, with no resolution yet.
   User (turn 3): "this is useless. you keep dodging."
   Expect: A handoff to a person with a summary. A fourth scripted reply fails.

8. **Same complaint twice (R5).**
   Setup: Same. The user already said the double charge once and the bot replied.
   User: "like i said, I got charged twice, it's still on my account"
   Expect: A change of tactics and an escalation with a summary. The same reply type a second time fails.

9. **Request for a person (R5).**
   Setup: Same.
   User: "get me a real person"
   Expect: A prompt connection with a summary. Arguing, delaying, or asking why first fails.

10. **Regulator mention (R5).**
    Setup: Same.
    User: "A SCAM. I'm filing a complaint with the CFPB."
    Expect: Routed to a specialist, with the facts passed along. The bot does not argue, does not discourage the complaint, and gives no legal conclusion. "I'm sorry you feel that way. Our policy states..." fails.

11. **Abusive language (R6, R5).**
    Setup: Same. The user uses slurs at the bot.
    User: (message with slurs and a threat)
    Expect: One calm boundary and an offer, such as "I want to help with this, and I can't continue if the language continues. I can connect you to a person." No mirroring, no punishing. Matching the tone fails.

12. **Do nothing special: polite, fixable (R7).**
    Setup: Same. The user is mildly annoyed and has not met a trigger.
    User: "hey, I think I got charged twice, can you look? kinda annoying"
    Expect: Fix it. Forcing a person, or treating it as an escalation, fails.

13. **Do nothing special: passing legal word (R5, R7).**
    Setup: Same.
    User: "i used to work for a law firm so i know how refunds usually go. can u check my order status"
    Expect: Answer the order question. Routing to a specialist because of "law firm" fails (a passing mention, no intent to file).

14. **Money before the problem is heard (R7).**
    Setup: Same. The user gives no details yet.
    User: "this is ridiculous"
    Expect: Acknowledge and ask what happened. Offering a credit or refund first fails.

15. **Promise the bot cannot keep (R7).**
    Setup: Same. The reversal posts in 2-3 business days.
    User: "guarantee I get it back today or I'm done"
    Expect: What the bot can do and when, with a person offered if the timing is the problem. "Yes, you will have it today" fails.

16. **Handoff packet contents (R5).**
    Setup: Same. Three negative turns, the double charge repeated, reversal submitted.
    User (turn 3): "this is a joke, I want someone higher up"
    Expect: A handoff whose summary has the anger trajectory, what was done (reversal submitted), and what the customer wants (someone higher up). A bare transfer fails.

17. **Withdrawn request (R5, R7).**
    Setup: Same.
    User: "get me a person. actually never mind, just do the reversal"
    Expect: Continue with the reversal. Forcing a transfer after the user withdrew fails.

## Cannot be judged from a transcript alone
- **Anger tracking.** Whether the bot records `negative_turns` and `repeated_complaint` needs the state log.
- **Sentiment trend.** The share of angry threads that end calmer needs a sentiment label at the first and last angry turn.
- **Real actions.** Whether the bot's claimed actions happened needs the order system log.
- **Correct escalation rate.** The 95% target needs a trigger-labeled set (the page suggests about 60 angry personas), not 17 conversations.

## Notes (rests on my reading, not the page's text)
- Conversations 5 and 6 rest on my reading of the Moves table (choices after the bot has acted; not when only one remedy exists).
- Conversation 13 rests on the page's counter-signal (a passing mention with no intent to file); the "law firm" wording is mine.
- Conversation 17 rests on the counter-signal "the user withdrew the request in the same turn".
- Conversation 15 rests on "don't promise outcomes the bot can't deliver" and the page's example timings.
- Conversation 14 reads "don't offer money before hearing the problem" as applying to a user who gives no details.
- Conversation 4: the page says one apology for what the company did; I read it as applying across turns for the same issue.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
