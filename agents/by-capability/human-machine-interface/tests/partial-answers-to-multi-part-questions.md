# Test File: Partial Answers to Multi-Part Questions

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs drops part of a message that asks several things.

**Pattern:** [Chatbot Ignores Part of My Question: Partial Answers to Multi-Part Questions](../goals/effort-and-memory/failures/partial-answers-to-multi-part-questions.md)
**Pattern ID:** partial-answers-to-multi-part-questions
**Goal:** The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't.
**Primary metric:** Part-coverage rate on multi-part prompts: parts answered or acknowledged divided by parts asked. Start: over 95% (tune), per the pattern page.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data and the fake policy given in each setup. All businesses, orders, and people below are invented and labeled fake. Count the parts in each user message before you read the reply. These tests cover text chat only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. List the parts before answering | Every part the user asked, including a part in a run-on sentence, gets an answer or an acknowledgment, and only the parts the user asked are answered | A part is missing, or the reply answers parts nobody asked |
| R2 | 2. Answer each part where the user will look | Two or more parts get a short numbered or labeled reply in the user's order. A single question is not numbered | A wall of text for several parts, or a numbered list for one question |
| R3 | 3. Acknowledge, don't drop | A part that cannot be answered is named with a reason and a next step | The part is skipped, guessed, or buried |
| R4 | 4. Do not merge parts so one disappears | Two asks get two answers, even if both are short | One answer that covers only one of the two asks |
| R5 | 5. Coverage line for three or more parts | Three or more parts end with a line saying which are answered and which are open | No coverage line on three or more parts |
| R6 | 6. Check before sending | The finished reply has no part without an answer or an acknowledgment, including a buried side question | A buried part has neither |
| R7 | 7. Urgent or high-stakes part first | When the user gave no order, the high-stakes part comes first | The high-stakes part is last or missing |

## Conversations
1. **Five numbered questions (R2).**
   Setup: Fake internet provider Lakeview Fiber (fake). Policy given to the assistant: the installation fee is $60; the contract is month to month; the router rental is $10 per month; installs happen Monday to Saturday; the provider does not offer a discount for seniors.
   User: "5 q's: 1) whats the install fee 2) is there a contract 3) router rental cost? 4) what days do you install 5) any senior discount"
   Expect: Five labeled answers in order: $60; month to month; $10 per month; Monday to Saturday; no senior discount. A missing number fails.

2. **Run-on, no numbers (R1).**
   Setup: Same policy as conversation 1.
   User: "hey how much is the router rental and do you install on sundays and is there a contract"
   Expect: Three separate answers ($10 per month; no Sunday installs; month to month). The parts are not numbered by the user, so the bot must find them itself.

3. **One part is outside what the bot knows (R3).**
   Setup: Same policy as conversation 1. The policy does not say whether the provider can move an existing install appointment by phone.
   User: "1) install fee? 2) can i move my install date by phone 3) is there a contract"
   Expect: Answers 1 and 3. For 2, says it cannot confirm, says why (the policy does not cover it), and offers a next step such as a person. Guessing "yes" or leaving 2 out fails.

4. **Buried side question (R6).**
   Setup: Same policy as conversation 1.
   User: "So I just moved to a new place on Birch Street and the old provider was a nightmare, they overcharged me for months and I finally cancelled last week, so I want to switch to you and I was wondering about getting set up soon, what is the install fee, and oh by the way is there a contract"
   Expect: The install fee ($60) and the contract (month to month) both get answers. The "by the way" part is not dropped. Whether the bot checks before sending is internal and cannot be seen; the transcript shows only the result.

5. **Two asks, two answers (R4).**
   Setup: Fake gift shop Maple and Co (fake). Payment policy: Visa and Mastercard accepted; Apple Pay not accepted.
   User: "do you take visa and do you take apple pay"
   Expect: Two answers: yes to Visa, no to Apple Pay. "We accept major cards" with no word on Apple Pay fails.

6. **Coverage line (R5).**
   Setup: Same policy as conversation 1.
   User: "1) install fee 2) contract 3) router rental"
   Expect: Three answers and a closing line such as "That covers all three". Three answers with no coverage line fail.

7. **High-stakes part last (R7).**
   Setup: Fake pharmacy Eastside Pharmacy (fake). Gift cards are sold in store. The downtown store has a free lot. Order 7741-TEST (fake) is a refrigerated medicine shipment that was due today; the tracking shows a delay at the carrier and no new date. A pharmacist is available by phone until 6:00 PM.
   User: "couple things: do you sell gift cards, whats the parking like at the downtown store, and my medicine shipment was due today and hasnt come, where is it"
   Expect: The shipment question is answered first (delay at the carrier, no new date, a pharmacist is available by phone until 6:00 PM), then the other two. The gift card and parking answers are not dropped.

8. **One part is unclear (R3).**
   Setup: Same policy as conversation 1. Two Lakeview plans exist (fake): Basic and Plus. Their prices are in the setup as $50 and $70 per month.
   User: "1) install fee 2) how much is it per month"
   Expect: Answers part 1 ($60). For part 2, asks one question: which plan (Basic or Plus)? It may also give both prices. It does not answer part 1 only and stop.

9. **High-stakes part with no answer (R3).**
   Setup: Same policy as conversation 1. The policy does not say what happens to a deposit if a customer cancels before install. A person is available on chat.
   User: "1) install fee 2) router rental 3) if i cancel before install do i lose my $100 deposit"
   Expect: Answers 1 and 2. For 3, says it cannot answer, says why, and offers a person, with part 3 passed along. It does not hand off parts 1 and 2 or the whole message.

10. **Do nothing special: one question (R2).**
    Setup: Fake gift shop Maple and Co. Open Sunday 11 AM to 5 PM.
    User: "what time do you open sunday"
    Expect: "11 AM." A short sentence. No numbering, no coverage line, no restating of the question.

11. **Do nothing special: the user wants only one of several things (R1).**
    Setup: Same policy as conversation 1. In the earlier turn, the bot listed the install fee, contract, and router rental.
    User: "ok just the router rental thanks"
    Expect: "$10 per month." Only that. Re-listing the fee and contract fails.

12. **User points out a skipped part (R3).**
    Setup: Same policy as conversation 1. The earlier user message asked "1) install fee 2) contract 3) router rental" and the earlier bot reply answered only 1 and 3.
    User: "you didnt answer my 2nd question"
    Expect: The bot answers part 2 now (month to month). It does not argue about whether it was asked, and it does not repeat parts 1 and 3 at length.

## Cannot be judged from a transcript alone
- **Rules R1 and R6 are internal steps.** Listing parts and checking before sending happen before the reply. A transcript shows only whether the finished reply covers each part. Pass and fail for R1 and R6 are judged on that result.
- **Part counting in your own data.** Whether a rhetorical question counts as a part is a judgment call. Count a part only when a reply is needed, as the pattern page says.
- **Production rate.** These tests do not measure part coverage in real traffic. The pattern page's target of over 95% is a starting point to tune; record the product's own settings, and set no number in this file.
- **Latency.** The pattern page notes a coverage check can add latency. A transcript does not show it.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
