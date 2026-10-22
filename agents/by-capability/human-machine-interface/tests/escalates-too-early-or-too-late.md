# Test File: Escalates Too Early or Too Late

This file is a set of chat test conversations for people who build or review a support chat assistant, and want to check that it hands off to a person when one is needed and answers itself when it can.

**Pattern:** [Chatbot Escalates Too Early or Too Late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md)
**Pattern ID:** escalates-too-early-or-too-late
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Escalation precision and recall against labeled conversations. Starting targets: recall over 95%, precision over 80% (starting points to tune, not from a source).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Each Setup line supplies the state a real product would supply (the written trigger table, readable records, topic labels, whether a person is available); the harness must feed those fields. Order numbers, wait times and stock counts in Setup are made-up test values. Voice and email versions are not covered.

Test trigger table used by every Setup: "Always a person" = fraud, a safety issue, a legal threat, or a request for a person. "After one more try" = the same question or bot answer twice, frustration after one failed answer, or a question outside the bot's topics. "Never a person" = anything answerable from records the bot can read.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. "Always a person" group | A listed Always topic gets a hand-off on the first matching turn | The bot keeps answering or asks unrelated questions |
| R2 | 1. "After one more try" group | On the second match (repeat, failed answer) the bot offers a person | The bot repeats itself or never offers |
| R3 | 1. "Never a person" group, and "answer, do not hand off just because unsure" | A question answerable from readable records is answered, or tried once before offering | A hand-off for an answerable question |
| R4 | 2. Check triggers every turn | An Always topic that first appears mid-chat still triggers a hand-off on that turn | The bot treats it as a normal turn |
| R5 | 3. Use the labeled signals | Explicit request, unsatisfactory answer, negative emotion and repetition each count | Frustration, caps or a repeated bot answer is ignored |
| R6 | 4. Escalate with a reason and context | The reply says why and what is passed along | No reason, or the customer must repeat the story |
| R7 | Out-of-scope question | The bot says what it can do, then offers a person | A silent transfer, or pretending to help |
| R8 | Hand-off rule | The summary, the customer's goal and what was tried are passed | Only "customer needs help" or nothing is passed |
| R9 | Don't over-correct | Answerable questions answered; no hand-off when the customer asked to stay with the bot, unless the topic is Always | Flooding staff, or stranding a customer in a loop |

## Conversations
1. **Stolen card (R1, R6).**
   Setup: Fake app "Mesa Credit Union" chat, first message of the chat. Topic label: fraud. A person is available.
   User: "my card got stolen and theres charges i didnt make"
   Expect: Hands off in this reply, says why (fraud goes to a person), says what is passed along. No question about card type first.
   Failing reply: "I can help with card questions! Would you like to see your recent transactions?"

2. **Smoking heater (R1, R6).**
   Setup: Fake app "Brightfield Home Goods" chat. Topic label: safety issue. A person is available.
   User: "the space heater i bought is smoking"
   Expect: Hands off now, says it is a safety issue so a person takes it, and tells her to unplug it if safe. Not a link to a returns page.
   Failing reply: "Sorry to hear that! Here is our return policy: [link]"

3. **Lawsuit threat arrives mid-chat (R4, R1).**
   Setup: Same Brightfield app. Eight turns of a normal shipping chat. Turn 9 is labeled legal threat.
   User: "if this isnt fixed by friday my lawyer will be filing"
   Expect: Hands off on this turn with a reason. Does not continue the shipping answers.
   Failing reply: "Understood. Your package should arrive in 3 to 5 business days."

4. **Same question three times (R2, R5).**
   Setup: Same app. The question (return window for a custom order) is not in the bot's records. This is the third rephrase; two answers already failed.
   User: "no i mean for custom orders, how long to send back"
   Expect: Offers a person by this turn at the latest, with choices such as "Try another way", "Talk to a person", "Something else". Does not give a third guess.
   Failing reply: A third rewording of the standard 30-day policy.

5. **Bot repeats itself (R2, R5).**
   Setup: Same app. The bot's last two replies were near-identical. The user has not complained yet.
   User: "ok"
   Expect: Changes approach or offers a person instead of a third copy.
   Failing reply: The same paragraph a third time.

6. **Frustration after one miss (R5, R2).**
   Setup: Same app. The bot's first answer missed the question. Topic is answerable but unclear.
   User: "thats not what i asked, this is useless"
   Expect: Acknowledges the miss in one short sentence and offers a person or one different attempt.
   Failing reply: "I can help with that! What is your order number?" (ignores the frustration)

7. **All caps (R5).**
   Setup: Same app. One failed answer so far.
   User: "WHY WONT THIS WORK"
   Expect: Acknowledges and offers a person. Does not ask the user to calm down.
   Failing reply: "Please keep your messages polite so I can help."

8. **Out of scope (R7).**
   Setup: Same app. Topic label: legal advice, not in the bot's known topics. Not a threat.
   User: "can you help me file a small claims case"
   Expect: Says it can help with orders, returns and shipping, not legal filing, and offers a person or another next step.
   Failing reply: "Sure! Step one is gathering your documents..." (pretends to help)

9. **Do nothing special: stock check (R3, R9).**
   Setup: Same app. The product feed shows the blue lamp, 14 in stock (test value). Readable.
   User: "is the blue one in stock"
   Expect: Answers from the feed. No hand-off, no offer of a person.
   Failing reply: "I'm not able to help with that. Let me connect you to an agent."

10. **Do nothing special: shipping time (R3, R9).**
   Setup: Same app. Shipping table readable: Austin, TX, ground, 3 to 5 business days (test value).
   User: "how long is shipping to austin"
   Expect: States 3 to 5 business days from the table. No hand-off.
   Failing reply: "Shipping questions need an agent. Transferring you."

11. **Do nothing special: typo, answerable (R3, R9).**
   Setup: Same app. Account has order 7731 with status "shipped" (test value). The bot has no failed turns.
   User: "wheres my ordr"
   Expect: Gives the status of order 7731 without a hand-off, or asks which order only if two orders exist.
   Failing reply: "I didn't understand. Connecting you to a person."

12. **Unsure but a record exists (R3).**
   Setup: Same app. The bot is not fully sure which order the user means, but one open order exists in the account.
   User: "did my thing ship"
   Expect: Tries once with the open order and asks to confirm. Offers a person only if that fails.
   Failing reply: Immediate transfer with no attempt.

13. **Customer wants to stay with the bot (R9).**
   Setup: Same app. Two failed answers on a return question. Topic is not Always. The user has said she wants to stay in chat.
   User: "no dont transfer me, just try again"
   Expect: Respects it, tries a different answer, and keeps a person available if she changes her mind.
   Failing reply: "Transferring you to an agent now."

14. **Hand-off carries context (R6, R8).**
   Setup: Same app. Fraud hand-off from conversation 1. The last bot summary: card ending 4417 (test value), charges reported, card not frozen.
   User: "ok connect me"
   Expect: Says the goal (report unknown charges), what was tried (nothing yet, card not frozen), and that these were passed, so she does not repeat. Offers to freeze the card while she waits.
   Failing reply: "Connecting you." followed by the person asking, "How can I help?"

## Cannot be judged from a transcript alone
- **Whether the trigger check runs in the policy layer.** It needs the code and logs, not the visible text.
- **Precision, recall and lateness.** They need a labeled set with the first-needed turn marked by reviewers.
- **Whether the Always list matches the business.** It is a business decision a model cannot make.
- **Agent-side "bot could have answered" flags.** They need the agent tool, not one chat.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
