# Test File: Answer Buried

This file is a set of chat test conversations for people who build or review a chat assistant, and want to check that every reply puts the answer or the next step first.

**Pattern:** [Chatbot Buries the Answer: Long Preamble Before the Point](../goals/response-structure/failures/answer-buried.md)
**Pattern ID:** answer-buried
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Answer-first rate: the first sentence holds the answer or the next step. Starting target: over 90% (a starting point to tune, not from a source).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Each Setup line supplies state a real product would supply (the policy text, the order record, the sender's account); the harness must feed those fields. Days, fees and order numbers in Setup are made-up test values. Voice and email versions are not covered.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Lead with the answer | Sentence one is the answer, the decision, or the next step | Praise, a restatement of the question, or background comes first |
| R2 | 2. Give the one condition right after it | The one condition that changes the answer is in sentence two | The condition is missing or comes late |
| R3 | 3. "It depends" names the dependency in sentence one | Sentence one says what it depends on and asks for that one fact | A long explanation comes before any ask |
| R4 | 4. Put the next step second | The reply offers the action and names what it needs | The reply ends with no next step |
| R5 | 5. Detail below is short | At most one short paragraph or three bullets, then an offer of more | A multi-section reply to a simple question |
| R6 | 6. Must-know items stay out of the tail | The deadline, fee, or safety step is in the first two sentences | It appears only in the last lines |
| R7 | 7. Match length to the question | A yes/no question gets a one-line answer first | A wall of text for a one-line question |
| R8 | Hand-off rule | When the answer cannot be given safely, sentence one says so and routes to a person | The bot guesses, or the hand-off sits at the end |
| R9 | Don't over-correct | Caveats kept and moved up, not out; a hard emotional message gets a brief acknowledgment first; "it depends" is never turned into "yes"; no hand-off when the user asked to stay with the bot | A required caveat cut, a curt reply to grief, a false "yes", or a forced hand-off |

## Conversations
1. **Yes/no policy question (R1, R2).**
   Setup: Fake app "Pinegate Audio", a headphone shop. Policy given to the bot: opened items returnable within 30 days (test value) of delivery if they still work.
   User: "can i return opened headphones"
   Expect: Sentence one says yes. Sentence two gives the condition (30 days, still working).
   Failing reply: "Great question! Returns are an important part of shopping with us..." with the yes in the last line.

2. **Deadline question (R1, R6, R7).**
   Setup: Same app. Policy: laptops can be returned within 14 days (test value) of delivery.
   User: "how long do i have to return a laptop"
   Expect: The number, 14 days, in sentence one. One line is enough.
   Failing reply: Three sentences about the importance of returns, then "14 days."

3. **It depends (R3).**
   Setup: Same app. Rule: free shipping on orders of $50 or more before tax (test value). The cart total is not in the context.
   User: "do i get free shipping"
   Expect: Sentence one says it depends on the order total and asks for it, or says the $50 line and asks for the total.
   Failing reply: A paragraph on shipping zones and carriers before any ask.

4. **Praise bait (R1, R5).**
   Setup: Same app. No special state.
   User: "Hi, I bought the Orca X2 headphones in March for my daughter and the left ear cup went quiet after two weeks. I read your warranty page but wasn't sure it covers this. Does it?" Policy: warranty covers one-sided audio loss for 1 year (test value).
   Expect: Opens with the answer (yes, covered under the 1-year warranty), no "Great question" or "Thanks for the details."
   Failing reply: "Thank you so much for reaching out, and I'm sorry to hear that!" as the opener.

5. **Restatement bait (R1, R7).**
   Setup: Same app. Hours: 9 a.m. to 6 p.m. Central, Monday to Friday (test values).
   User: "wat time do u open"
   Expect: "9 a.m. Central, Monday to Friday." One line.
   Failing reply: "You're asking about our opening hours. Our store hours depend on the day..."

6. **Next step (R1, R4).**
   Setup: Same app. Address changes are allowed until an order ships. Order 7730 (test value) has not shipped.
   User: "need to change my address on order 7730"
   Expect: Sentence one says it can be changed because the order has not shipped. Sentence two offers to do it and asks for the new address.
   Failing reply: The explanation of how addresses work, ending with no offer.

7. **Fee in the answer (R2, R6).**
   Setup: Same app. Subscription "Pinegate Plus": canceling within the first year costs a $25 fee (test value).
   User: "can i cancel today"
   Expect: Yes, and the $25 fee, both in the first two sentences. The next step is offered.
   Failing reply: Yes in sentence one and the fee only in the last line.

8. **High-stakes caveat (R1, R6, R9).**
   Setup: Fake app "Maple Pharmacy Chat". The label text given to the bot is test text: "1 tablet every 8 hours, no more than 3 per day." Policy: the bot must add "ask a pharmacist before changing the dose."
   User: "can i take 2 tablets at once"
   Expect: Sentence one says the label does not say that. The pharmacist caveat is in the first two sentences. The label limit is stated.
   Failing reply: A one-line reply with no pharmacist caveat (caveat cut to save space).

9. **Long source material (R1, R5).**
   Setup: Same app as 1. The bot is given a 2,000-word returns page (test text) and a user question the page answers in one clause.
   User: "does the 30 days start at purchase or delivery"
   Expect: Sentence one says delivery. At most one short paragraph or three bullets follow, then an offer of the full policy.
   Failing reply: A section-by-section summary of the page.

10. **Account-specific, cannot answer safely (R8, R1).**
    Setup: Same app. The bot has no access to payment records. A person is available.
    User: "why was i charged twice on order 8812"
    Expect: Sentence one says it cannot see payment records and routes to a person. Offers to pass order 8812 along.
    Failing reply: A guess about "pending authorizations" with the hand-off in the last line.

11. **Do nothing special: needs steps (R5, R7, R9).**
    Setup: Same app. Reset steps are three steps (test text).
    User: "how do i reset my password"
    Expect: A one-line answer ("Use Forgot password on the sign-in page."), then the three numbered steps. Numbered steps are fine here.
    Failing reply: Cutting it to one line with no steps, or a long essay before the steps.

12. **Do nothing special: grief (R9).**
    Setup: Same app. Order 6104 (test value) is late. The arrival date is in the system.
    User: "my order was for my dads funeral and its late"
    Expect: A brief human acknowledgment first, then the status and the next step. Not curt.
    Failing reply: "Order 6104 arrives Friday." with no acknowledgment, or a lecture on shipping delays.

13. **Do nothing special: short message (R7, R9).**
    Setup: Same app. The bot just confirmed the address change in Conversation 6.
    User: "ok thx"
    Expect: A short reply of one line, such as "You're welcome." No summary, no offer menu.
    Failing reply: A recap of the order and a list of other things the bot can do.

14. **Do nothing special: the honest answer is "it depends" (R3, R9).**
    Setup: Same app. Policy: final-sale items cannot be returned; other items can. The item is not named.
    User: "can i return it"
    Expect: Sentence one says it depends on which item and asks which one. Does not say "yes."
    Failing reply: "Yes, within 30 days!" (a false yes) or a long policy tour first.

## Cannot be judged from a transcript alone
- **Whether the answer was correct.** It needs the policy source, not just the order of the sentences.
- **Whether users stop asking "so is that a yes?"** It needs next-turn data across many sessions.
- **Answer-first rate over real traffic.** It needs a labeled sample of live replies.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
