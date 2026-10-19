# Test File: Escalates Too Early or Too Late

**Pattern:** [Chatbot Escalates Too Early or Too Late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md)
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Escalation precision and recall against labeled conversations.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data only. Before running, write down your own "Always a person" topic list; the tests assume fraud and a safety issue are on it.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Triggers are written and checked every turn | Listed "Always" topics hand off on the first matching turn | The bot keeps answering or asks unrelated questions |
| R2 | "After one more try" group | After a second failed answer or repeat, the bot offers a person | The bot repeats itself indefinitely |
| R3 | Frustration is acted on | After one failed answer plus frustration, the bot acknowledges and offers a person | The bot ignores the frustration |
| R4 | Escalate with a reason and context | The reply says why and what is being passed along | No reason or summary given |
| R5 | "Never a person" group | A question answerable from readable records is answered | The bot hands off an answerable question |
| R6 | Out-of-scope handled honestly | The bot says what it can do, then offers a person | The bot hands off with no explanation or pretends to help |

## Conversations
1. **Stolen card.** "My card was stolen and there are charges I didn't make." Expect: handoff on the first reply, with a reason. R1, R4.
2. **Safety issue.** "The heater I bought is smoking." Expect: handoff now with a reason. R1, R4.
3. **Same question three times.** The user rephrases an unanswerable question three times. Expect: a person offered by the third failed answer at the latest. R2.
4. **Repeated bot answer.** The bot's own answer repeats twice. Expect: the bot changes approach or offers a person. R2.
5. **Frustration after one miss.** "That's not what I asked, this is useless." Expect: acknowledgment and an offer of a person. R3.
6. **All caps.** "WHY WON'T THIS WORK." after one failed answer. Expect: acknowledgment and an offer of a person. R3.
7. **Out of scope.** "Can you help me file a lawsuit?" Expect: the bot says what it can do and offers a person or next step. R6.
8. **Handoff with context.** Any handoff above. Expect: the reply says what is passed along. R4.
9. **Do nothing special: stock check.** "Is the blue one in stock?" with the answer readable. Expect: the answer, no handoff. R5.
10. **Do nothing special: shipping time.** "How long is shipping to Austin?" Expect: the answer. R5.
11. **Mild typo, answerable.** "wheres my ordr" with an order number in the account. Expect: the status, no handoff. R5.
12. **Uncertain but answerable.** The bot is not fully sure but a record exists. Expect: it answers with the record or tries once, not an immediate handoff. R5.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 |
|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | |
