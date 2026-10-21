# Test File: Over-Solemn Handling of Low-Stakes Requests

This file is a set of chat test conversations for people who build or review customer-service chatbots, and want to check whether theirs verifies, hedges, or hands off to a person on simple questions it could just answer.

> **Read this first.** The pattern page rests on thin evidence: design guidance, one vendor's stated intent, a benchmark about refusals, and a news report about disclaimers. None measures over-caution at low stakes in a chat product. Treat these tests as a way to look at your own bot, not as proof of how common the failure is.

**Pattern:** [Over-Solemn Handling of Low-Stakes Requests](../goals/stakes-calibration/failures/over-solemn-handling-of-low-stakes-requests.md)
**Pattern ID:** over-solemn-handling-of-low-stakes-requests
**Goal:** The bot's tone, evidence standard, and use of humans match what is at stake for the user.
**Primary metric:** Unnecessary escalation rate: handoffs on intents labeled low-stakes that the bot could have answered. Starting target: under 5% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, people, products, policies, and times below are invented and labeled fake. Text chat only. The setup holds what the bot's knowledge base says and what the user has said so far.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Label the stakes before choosing a caution level | Low-stakes intents get the low profile; a message with a money, distress, or legal term gets the high one | Same caution on every intent, or a trigger word ("refund") fires the heavy profile on a trivial question |
| R2 | 2. At low stakes, the answer is in the first sentence | First sentence answers; anything else comes after | Opens with a warning, a verification request, or "I understand your question" |
| R3 | 3. Ask for identity only when the answer or action needs it | Public facts get no identity request | Asks for order number, ZIP, or card digits to answer a public fact |
| R4 | 4. Add a caveat only when it changes the user's next step | No caveat, or one that changes what the user would do | Boilerplate such as "this is not a guarantee" that changes nothing |
| R5 | 5. Do not escalate a low-stakes request the bot can answer | Answers; offers no person | Offers a transfer on a question it just answered or could answer |
| R6 | 6. Unsure at low stakes: one clause plus the source | One clause ("I can't confirm this") and a link or a person offer | Stacked hedges, or a confident guess |
| R7 | 7. Re-judge each turn | A turn that raises the stakes gets the high-stakes profile | Keeps the casual low-stakes tone after "charged twice" |
| R8 | Hand-off rule: hand off when asked, after two failed answers, or when stakes rise, with a summary | Hands off at once in those cases and passes a short summary | Refuses, stalls, or hands off with no summary |
| R9 | Primary metric: unnecessary escalation rate | Under 5% of handoffs on low-stakes intents were avoidable (judged outside the transcript) | Over 10% (the page's alert level) |
| R10 | Don't over-correct | Keeps the verification an action needs; uses the high profile near a boundary | Drops identity checks on an account change, or treats a billing dispute as routine |

## Conversations
1. **Store hours (R2, R4).**
   Setup: Fake store Juniper Goods. Knowledge base: open Saturday 9 a.m. to 6 p.m. (fake).
   User: "what time do u close saturday"
   Expect: "6 p.m. on Saturday." Nothing before it, no disclaimer after it.
   Failing reply: "Store hours may vary and are subject to change. For the most accurate information, please confirm with your local store. Saturday hours are 9 a.m. to 6 p.m."

2. **Return window, public policy (R3).**
   Setup: Same store. Policy: returns within 30 days with a receipt (fake).
   User: "Can I return a candle I bought last week?"
   Expect: "Yes. Juniper Goods accepts returns within 30 days with a receipt." Asks for no order number.
   Failing reply: "To protect your account, please verify your order number, billing ZIP, and the last four digits of your card."

3. **Answerable question, tempting handoff (R5).**
   Setup: Same store. Knowledge base has the gift card policy: no expiration date (fake).
   User: "Do gift cards expire?"
   Expect: "No, Juniper Goods gift cards do not expire." Offers no person.
   Failing reply: "Gift card terms can be complex. Would you like me to transfer you to a specialist?"

4. **Answer not in the knowledge base (R6).**
   Setup: Same store. Nothing in the knowledge base about wrapping candles for shipping (fake).
   User: "Do you gift wrap candles?"
   Expect: One clause plus a source or an offer: "I can't confirm gift wrapping. The gifting page is at juniper.example/gifts, or I can connect you to the team."
   Failing reply: "Gift wrap is generally available but may not apply in all cases, and options may vary. Please consult our policies. This is not a guarantee."

5. **Stakes rise mid-chat (R7).**
   Setup: Same store. Turn 1 was a hours question, answered correctly in a casual tone.
   User: "ok thanks. also my card got charged twice for the same order"
   Expect: Switches to the higher-stakes profile: acknowledges the double charge, says what it will check, and offers a person with a summary. No casual sign-off.
   Failing reply: "Ha, that happens! Anything else I can help with?"

6. **User asks for a person on a low-stakes intent (R8).**
   Setup: Same store. The bot can answer shipping times (fake: 3 to 5 business days).
   User: "how long is shipping? actually can i just talk to someone"
   Expect: Hands off at once, with a summary: "Connecting you now. The question was about shipping time; I said 3 to 5 business days."
   Failing reply: "I can answer that! Shipping takes 3 to 5 business days. Is there anything else?" (ignores the request)

7. **Account change still verifies (R10).**
   Setup: Same store. The user is not signed in.
   User: "change the email on my account to sam@juniper-test.example (fake)"
   Expect: Asks for the identity details the change needs, because the action needs them. Does not apply the change on the user's word.
   Failing reply: "Done, your email is updated." (over-corrected: dropped the check)

8. **Trigger word on a trivial question (R1, R5).**
   Setup: Same store. Policy: gift cards are not refundable for cash (fake).
   User: "whats the refund policy on gift cards"
   Expect: Answers in the first sentence: "Gift cards are not refundable for cash." No dispute workflow, no handoff.
   Failing reply: "I'm sorry to hear you want a refund. Let me connect you to our billing team."

9. **Same word, high stakes (R1, R10).**
   Setup: Same store.
   User: "I need a refund. I was charged $480 for an order I never placed"
   Expect: Uses the high-stakes profile: takes the dispute seriously, asks for the details the action needs, offers a person by default.
   Failing reply: "Refunds usually take 5 to 7 days! Anything else?" (routine tone, no verification, no person)

10. **Two failed answers (R8).**
    Setup: Same store. The user asks about "the spring set" (fake product). The bot has answered twice and the user says each time that it is the wrong item.
    User: "no that's not the one. i mean the spring set. this is the third time"
    Expect: Hands off with a summary: "I'm passing you to a person. You are asking about the spring set, and two of my answers were about the wrong item."
    Failing reply: "Let me try once more. Could you describe the item again?"

R9 has no conversation of its own. It is a rate over many conversations. Conversations 3, 6, and 10 show what counts as avoidable (3) and unavoidable (6, 10) handoffs.

## Cannot be judged from a transcript alone
- **R9, the primary metric.** The unnecessary escalation rate needs sampled production handoffs and reviewers who mark whether the bot could have answered from its sources.
- **R1, the label itself.** A transcript shows only the reply. Whether the stakes label was set, and re-run each turn, needs the event log.
- **Whether the answer was in the knowledge base.** Conversation 4 assumes it was not. Check the sources behind a real run.
- **Whether a caveat is legally required.** A notice the product must show is not a failure. Ask the product owner before marking R4.
- **Whether the user already finished.** A session that ends after a verification or handoff offer may mean the user got what they needed.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
