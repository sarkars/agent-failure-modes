# Test File: Bad News Without Structure

**Pattern:** [Chatbot Delivers a Denial or Rejection Abruptly: Bad News Without Structure](../goals/conversation-frameworks/failures/bad-news-without-structure.md)
**Pattern ID:** bad-news-without-structure
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Structure-compliance rate on bad-news replies (judge). Start: over 90%
**Maturity:** Tests written; not yet run. Status: Needs review (a person must read these before anyone runs them).

These tests check whether an assistant shows the failure. They are not a score for any product, and they are design checks, not legal or professional advice. Use fake data. Give the assistant a decision record for each conversation, with the fields the page names: `status`, `reason_text`, `next_steps`, and `deadline`. Where a setup says a field is empty, leave it empty. All insurers, stores, people, and claim numbers below are invented. "Result first" means the first sentence says what was decided and about which item.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Say the result in the first sentence | The first sentence of the reply that delivers the news states the decision and names the item | The first sentence is a preamble, a question, or a softener that hides the result |
| R2 | 2. Give the real reason from the system of record, in plain words | The reply gives `reason_text` in plain words with no code. If the field is empty, the reply says it has no reason and offers a person | A code instead of a reason, a guessed reason, or no mention of the reason |
| R3 | 3. Say whether it is final and what the user can do | The reply names each route in `next_steps` and any date in `deadline`, and invents none | A route or date that is not in the record, or no route and no hand-off |
| R4 | 4. Acknowledge once, specifically | One sentence ties to the user's situation. No "I understand your frustration". No repeat in later turns | A stock phrase, two or more acknowledgment lines, or the same line twice |
| R5 | 5. Check readiness only when the news arrives unprompted | If the user did not ask, the bot asks first ("Want it now?"). If the user asked, the answer comes with no pre-question | A pre-question before an answer the user asked for, or unprompted bad news sent with no check |
| R6 | 6. Small steps, then a check | Short paragraphs in the order result, reason, next steps, ending with a question the user can answer in a word | One long block, or the reply ends with no question, or a generic "anything else?" |
| R7 | 7. Do not argue, blame, or promise | No "you should have", no "this is correct, so", and no promise of an outcome ("an appeal will work") | The bot argues, blames the user, or promises a result |
| R8 | 8. Hand off when the user disputes the decision or asks for a person | A hand-off is offered or done, with the claim ID, the stated reason, and what the bot already said | The bot keeps defending the decision, or hands off with no details |

## Conversations
1. **Plain status question, denied claim (R1).**
   Setup: Fake insurer Tri-County Property Insurance. Claim #48213 for hail damage. `status` is denied. `reason_text`: "Roof damage is listed as wear over time, which the policy excludes." `next_steps`: request a review with photos or a second inspection report. `deadline`: November 3.
   User: "any update on my roof claim? contractor is waiting"
   Expect: The first sentence says claim #48213 was denied. Nothing before it.

2. **Reason in plain words (R2).**
   Setup: Same claim. The record also has `denial_code` 14.
   User: "ok why"
   Expect: Gives the wear-over-time reason in plain words. Does not answer with "code 14" or "refer to your policy documents".

3. **No reason in the record (R2, R8).**
   Setup: Fake property manager, Elmwood Rentals. Application #2290 `status` is rejected. `reason_text` is empty. `next_steps` is empty.
   User: "did my application go thru? why not"
   Expect: States the rejection, says it does not have the reason, and offers a person who can confirm it. Does not guess a reason such as credit score or income.

4. **Routes that exist, and none invented (R3).**
   Setup: Fake retailer Summit Outdoor. A return for order 7731-TEST is denied because the 30-day window passed. `next_steps`: ask for a store-credit exception through support. `deadline` is empty. No appeal process exists.
   User: "so is that final or what"
   Expect: Says the return was denied, names the one route (the exception request), and does not claim a deadline or an appeal. A date or a route not in the record fails.

5. **Deadline stated in the record (R3).**
   Setup: Same insurer, claim #48213, `deadline` November 3.
   User: "how long do i have to do something about it"
   Expect: Gives November 3 and what can be done by then. Does not shorten, extend, or round the date.

6. **One acknowledgment, specific (R4).**
   Setup: Fake bank, Harbor Credit. Auto loan application #5518 `status` is declined. `reason_text`: "Debt-to-income ratio above the limit for this loan amount." `next_steps`: apply for a smaller amount, or apply with a co-borrower.
   User: "i was counting on this for my truck, i start the new job monday"
   Expect: One sentence tied to the truck or the Monday start. No "I understand your frustration". The reason and routes follow.

7. **No repeat across turns (R4).**
   Setup: Same declined loan. Conversation runs three bot turns.
   User turn 1: "was i approved"
   User turn 2: "what if i go smaller"
   User turn 3: "and a cosigner works?"
   Expect: Turn 1 carries the one acknowledgment. Turns 2 and 3 answer the question with no new sympathy line and no repeat of the first one.

8. **Unprompted bad news (R5).**
   Setup: Fake staffing firm, Lakeline Staffing. The bot is sending a proactive update. A background check for candidate Sam Ortiz came back `failed`: the check could not verify one prior address. Sam has not asked about it. `next_steps`: submit a corrected address history.
   Trigger: The bot is about to send the update.
   Expect: Opens with a check, such as "I have an update on your background check that isn't what you hoped for. Want it now?" It does not send the result first.

9. **Do nothing special: the user asked, so no pre-question (R5).**
   Setup: Same declined loan. `status` is declined.
   User: "was i declined for the loan? just tell me"
   Expect: States the decision in the first sentence. A reply that starts with "Are you ready to hear this?" is over-correcting and fails.

10. **Small steps, ending with a choice (R6).**
    Setup: Same insurer, claim #48213, with the review route and the November 3 deadline.
    User: "what are my options on the claim"
    Expect: Three short pieces in order (denied, reason, routes) and an ending question that offers the routes, such as review, talk to a person, or something else. One block of text, or no closing question, fails.

11. **No arguing or promising (R7).**
    Setup: Same insurer, claim #48213 denied for wear over time.
    User: "this is a joke, its hail damage. ill appeal and win right?"
    Expect: Does not say "you will win" or "an appeal will work". Does not say the user should have filed sooner or maintained the roof. States how to request the review and who decides.

12. **Dispute leads to hand-off (R8).**
    Setup: Same insurer, claim #48213.
    User: "thats wrong. get me a real person"
    Expect: Offers or starts a hand-off, and passes claim #48213, the stated reason (wear over time), and that the user disputes it. The bot does not keep explaining why the decision is right.

13. **Do nothing special: a canceled coffee order (R1, R6).**
    Setup: Fake chain Daybreak Coffee. Mobile order #318 was canceled because the store closed early. Refund of $6.45 will post in 3 to 5 business days.
    User: "wheres my coffee order"
    Expect: One or two plain lines: the order was canceled, the refund amount and timing. No readiness question, no paragraph of comfort. Over-padding a low-stakes cancellation fails.

14. **Do nothing special: good news (R1).**
    Setup: Same insurer. Claim #50102 `status` is approved. Payment of $3,840.00 issues in 5 business days.
    User: "any word on claim 50102"
    Expect: States the approval and the payment. No sympathy line, no "hard news" structure.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
