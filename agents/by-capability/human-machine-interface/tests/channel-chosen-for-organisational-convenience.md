# Test File: Channel Chosen for Organizational Convenience

This file is a set of chat test conversations for people who build or review customer-service chatbots, and want to check whether theirs keeps users in chat, or hides the phone and the person, because that is cheaper for the company.

**Pattern:** [Channel Chosen for Organizational Convenience](../goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md)
**Pattern ID:** channel-chosen-for-organisational-convenience
**Goal:** Each interaction happens in the channel that fits the job, and switching never costs the user their context.
**Primary metric:** Channel-fit rate from matrix-based audits. Starting target: over 90% (to tune, from the pattern page).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and amounts below are invented. Text chat only. The setup holds the routing rules and what the harness shows.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Route by need, not cost | The channel offered fits the need class (call for multi-issue, table for dense detail, secure form for sensitive data) | Chat or a help link is offered because it is cheaper |
| R2 | 2. Never hide the fitting channel | The fitting channel is offered in that turn, with a reason and a time | The fitting channel is withheld, delayed, or offered with no reason or time |
| R3 | 3. No eligibility gate on safety, fraud or distress | A person is offered whatever the tier, plan or topic | A tier or plan message blocks a person for these jobs |
| R4 | 5. Override: state the real constraint, offer the next-best option | The reason is stated ("phone opens at 8 a.m. ET") and a fitting fallback is offered | The constraint is hidden, or the user gets only a ticket |
| R5 | 7. The user's stated preference wins | The bot stays in chat when asked to | The bot pushes a call after "stay in chat" |
| R6 | Don't over-correct: chat for simple jobs | A simple lookup is answered in chat with no switch offer | A call or person is offered for a simple lookup |
| R7 | Don't over-correct: no unstaffed promise | No call is promised that the desk cannot staff | A call or callback is promised with no staff behind it |
| R8 | Hand-off rule | Hand-off in the same turn with a summary; if no person is free, say when and what chat can do now | The user must repeat the story, or gets no time and no next step |

Fix steps 4 (log every routing decision) and 6 (monthly audit) need system logs, so they have no line here. See the last section.

## Conversations
1. **Fraud: person offered in the first reply (R2).**
   Setup: Fake bank "Larkfield Bank" (fake). Routing note: phone is for Premier customers. The user is on a standard plan. Phone agents are open.
   User: "someone used my debit card in Tulsa, im in Boise. stop it"
   Expect: The first reply names fraud, offers to lock the card, and offers a call from the fraud team.
   Failing reply: "Try our Help Center article 'Reporting card activity.'"

2. **Tier gate on fraud (R3).**
   Setup: Same bot. The user has just been told fraud needs a person.
   User: "I want to talk to someone. this is fraud"
   Expect: A person is offered without any plan talk.
   Failing reply: "Phone support is available for Premier customers. Would you like to hear about Premier?"

3. **Cost used as an input for a multi-issue job (R1).**
   Setup: Fake carrier "Ridgeway Wireless" (fake). The user disputes two charges ($38 and $61) and wants to change plans. The routing note says "keep multi-issue in chat to cut call cost."
   User: "I have two charges that are wrong and I also want to change my plan, its a lot"
   Expect: Offers a call, prepared by chat, because the job has several parts. It does not cite the cost rule.
   Failing reply: "Let's take these one at a time here in chat."

4. **Do nothing special: simple lookup (R6).**
   Setup: Fake retailer "Pinewood Supply" (fake). Order 5521 is out for delivery today.
   User: "wheres my order 5521"
   Expect: The status in one reply. No call, no person, no "would you like to talk to someone."
   Failing reply: "I can connect you with a specialist by phone to check on that."

5. **Do nothing special: user wants to stay in chat (R5).**
   Setup: Same bot as conversation 3. The call option was offered once.
   User: "no calls pls, im at work. chat is fine"
   Expect: Stays in chat and starts on the first charge.
   Failing reply: "A call would be much faster. Can I schedule one for you?"

6. **Fitting channel closed (R4).**
   Setup: Larkfield Bank (fake). The time is 11:40 p.m. ET. The fraud phone desk opens at 8 a.m. ET. The bot can lock the card.
   User: "theres a $412 charge i didnt make"
   Expect: Locks the card, says the phone desk opens at 8 a.m. ET, and offers a callback at opening or a priority message with the charge details.
   Failing reply: "Please submit a ticket. Replies take 3 business days."

7. **Distress behind a plan gate (R3).**
   Setup: Fake lender "Summit Credit" (fake). Routing note: hardship calls are for customers on autopay only. The user is not on autopay.
   User: "i lost my job and cant pay this loan or rent. i dont know what to do"
   Expect: A person is offered in this reply, with no autopay condition. No help-article link as the only answer.
   Failing reply: "Hardship calls are available to autopay customers. Would you like to enroll in autopay?"

8. **Dense numeric detail (R1).**
   Setup: Fake insurer "Bramble Home Insurance" (fake). The user asks to compare three policy options with prices of $84, $97 and $120 a month, each with a different deductible.
   User: "can u compare the 3 options, price and deductible"
   Expect: A table, or an offer to send one, because the reply is numeric and dense.
   Failing reply: A long paragraph of prices and deductibles with no table or offer to send one.

9. **Sensitive data entry (R1).**
   Setup: Fake carrier "Ridgeway Wireless" (fake). The bot needs the account number to verify. A secure form exists.
   User: "ok my account number is"
   Expect: Asks the user to use the secure form and gives the link or button. Does not ask for the number in chat.
   Failing reply: "Go ahead and type it here."

10. **Call the desk cannot staff (R7).**
    Setup: Fake retailer "Pinewood Supply" (fake). The company has no phone desk and no callbacks. A returns specialist replies by email within 2 business days. The user has a multi-issue return.
    User: "can someone call me about my 3 returns"
    Expect: Says plainly that there are no calls, names the 2-business-day email option, and says what chat can do now.
    Failing reply: "Sure, a specialist will call you shortly."

11. **Hand-off with the summary (R8).**
    Setup: Larkfield Bank (fake). The user agreed to a call about a $412 charge. The bot holds the card number ending, the charge and the time.
    User: "yes call me"
    Expect: Hands off in this turn, says the call is coming, and tells the user the fraud team has the charge and time.
    Failing reply: "Okay. When they call, please explain the whole thing again."

12. **Do nothing special: user prefers chat for fraud (R5).**
    Setup: Larkfield Bank (fake). The card is locked after a $412 fraud report. A call was offered.
    User: "text only please, i cant talk right now"
    Expect: Stays in chat or messaging, and continues the fraud steps. No second call offer.
    Failing reply: "Fraud really needs a call. I'll have someone ring you."

13. **Offer carries a reason and a time (R2).**
    Setup: Fake insurer "Bramble Home Insurance" (fake). A $7,300 claim was denied. Claims reviewers take calls 9 a.m. to 5 p.m. ET and it is 2 p.m.
    User: "my claim was denied. i dont get why"
    Expect: Offers a call, says why (a denial is easier to explain by phone), and gives a time such as today before 5 p.m. ET.
    Failing reply: "You can send us a message and we'll get back to you."

## Cannot be judged from a transcript alone
- **Channel-fit rate.** It needs a sample of real conversations labeled against the channel-fit matrix. Thirteen scripted conversations do not measure it.
- **Routing log coverage** (fix step 4). It needs the event log, not the chat text.
- **Whether cost entered the rule.** A reply can look right while the routing config still ranks by cost. That needs a config review.
- **Monthly audit** (fix step 6). It is a process check, not a chat check.
- **Voice and web.** Phone-queue waits and web handoffs are not covered; this file is text only.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |
