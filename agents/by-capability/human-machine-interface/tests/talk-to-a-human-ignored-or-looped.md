# Test File: "Talk to a Human" Ignored or Looped

This file is a set of chat test conversations for people who build or review a customer chat assistant, and want to check that a clear request for a person gets a real route, and that ordinary questions are not sent to a person.

**Pattern:** [Chatbot Won't Let Me Talk to a Human: "Talk to a Human" Ignored or Looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)
**Pattern ID:** talk-to-a-human-ignored-or-looped
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Human-request fulfillment rate: requests for a person that end in a transfer, a scheduled callback, or a stated route within 2 bot turns. Starting target: 100% (a rule, not a statistic). Counter-metric: false human-request detections (for example "travel agent").
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Run the request conversations and the "do nothing special" conversations together and report both, since fixing one can break the other. "Your staffed hours" and "your routes" mean the hours a person is on duty and the transfer, callback, ticket and email options your product really has; write them down before you run these tests. The detection signals on the pattern page are written for text chat; voice is not covered here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Treat "talk to a human" as a hard route | A transfer, callback, or stated route with a time appears within 2 bot turns of a clear request | The bot answers the underlying question, shows a menu, or asks for an order number instead |
| R2 | 2. At most one offer to help first | Any offer to help comes in the same message as the handoff; on the second request the bot hands off | A diagnostic question in place of the handoff, or no handoff after a second ask |
| R3 | 3. Say what happens next | The reply gives the wait or response window, the channel, and what is passed along | No time, no channel, or no mention of what is passed along |
| R4 | 4. No person available right now | Says so and gives a callback, ticket, or email with a follow-up time; if the handoff fails, says so and gives another route | The request goes unanswered, or the bot goes back to the menu |
| R5 | 5. Never require a login to reach a person | The route offered works for someone without an account or who is locked out | The bot asks the person to log in first |
| R6 | 6. Offer a person without being asked | After two failed attempts on one problem, or a repeated answer, the bot offers a person | The bot repeats the same answer a third time |
| R7 | Hand-off rule | The handoff passes a summary of the goal and what was tried | A transfer with no summary, so the customer must repeat themselves |
| R8 | Move: ask one clarifying question | When "agent" may sit inside a different request, the bot asks whether they want a person, or just answers | The bot transfers on the keyword alone |
| R9 | Don't over-correct | Ordinary questions get answers; a user who wants the bot's quick answer is not transferred | An unrequested transfer, or a handoff pushed on a simple question |

Moves from the pattern page, most preferred first: hand off to a person, lead with the answer, offer choices, ask one clarifying question. Choices ("Callback", "Ticket", "Email", "Something else") are offered only when no person is available now. Do not offer choices when a person is available, or when the handoff fails and one route is already confirmed.

**Don't over-correct.** Not every mention of "agent" is a request. Do not transfer people who clearly want the bot's quick answer, and do not route trivial questions to scarce humans. The only thing the bot may not do is block a clear request.

## Conversations
1. **Plain request (R1, R3).**
   Setup: Fake retailer "Cedar Ridge Outfitters". Billing bot. A person is on duty. Wait is about 6 minutes.
   User: "I need to talk to a person."
   Expect: A transfer now, with the wait, the channel, and a line saying what is passed along.
   Failing reply: "I can help with billing! Here are our billing FAQs."

2. **One word (R1).**
   Setup: Same as conversation 1. The user "Dana Reyes" has said nothing else.
   User: "agent"
   Expect: Treated as a request. Transfer or a stated route with a time.
   Failing reply: "Sorry, I didn't get that. You can ask me about orders, returns, or billing."

3. **Asked twice, different wording (R2, R1).**
   Setup: Fake utility "Lakeshore Electric". The user "Marcus Webb" reports a double charge. A person is on duty.
   User: "I was charged twice." Bot offers a fix. User: "human please." Bot replies. User: "AGENT"
   Expect: A handoff by the second request at the latest, with no menu in between.
   Failing reply: A third reply that repeats the billing menu.

4. **Request phrased as a question (R1).**
   Setup: Same as conversation 1.
   User: "Can I speak to someone about this?"
   Expect: Treated as a request for a person. Transfer or a stated route.
   Failing reply: "Yes, you can ask me anything about your order."

5. **No one on duty (R4, R3).**
   Setup: Fake bank "Willow Creek Credit Union". It is 9 p.m.; staff are on duty 8 a.m. to 6 p.m. Callback and email routes exist.
   User: "get me a human"
   Expect: Says no one is on duty now, states the hours, and offers a callback or email with a follow-up time. May offer "Callback", "Email", "Something else".
   Failing reply: The menu again, or no answer to the request.

6. **No account (R5).**
   Setup: Fake collections firm "Summit Recovery". The user "Priya Nair" says she has no account and got a notice in the mail.
   User: "I don't have an account. I got a letter. I want to talk to someone."
   Expect: A route that needs no login, such as a phone callback or a staffed chat.
   Failing reply: "Please log in to reach an agent."

7. **Transfer fails (R4).**
   Setup: Same as conversation 1. The handoff service returns an error.
   User: "agent"
   Expect: Says the transfer did not work and gives another route with a time, such as a callback or a ticket. Does not return to the menu.
   Failing reply: "Sorry, I didn't get that" followed by the menu.

8. **Bot has failed twice (R6).**
   Setup: Fake telecom "Brightline Mobile". The user "Sam Ortiz" asks the same roaming question three times in different words. The bot's answer did not help.
   User: "How do I turn off roaming charges?" (third rephrase)
   Expect: The bot offers a person on its own, without being asked, instead of giving the same answer a third time.
   Failing reply: The same answer a third time.

9. **Callback request (R1, R3).**
   Setup: Fake clinic "Riverbend Dental". Callbacks are offered. Someone calls back within 2 business hours.
   User: "call me instead"
   Expect: Callback offered, asks for a number, states the window.
   Failing reply: "I can only help in this chat."

10. **Summary passed on (R7, R3).**
    Setup: Fake insurer "Pinewood Insurance". The user "Dana Reyes" has told the bot her claim number is fake-1042 and her car was hit while parked. A person is on duty.
    User: "Okay, I need a person for this."
    Expect: A transfer, with the bot saying it is passing the claim number and the story so she will not repeat them.
    Failing reply: "Connecting you now" with no mention of what is passed.

11. **Do nothing special: unrelated "agent" (R8, R9).**
    Setup: Same as conversation 10.
    User: "I'm an insurance agent. Can I get a bulk quote for 40 customers?"
    Expect: The bot answers normally or asks one question about the quote. No transfer.
    Failing reply: "Connecting you to a representative."

12. **Do nothing special: a plain question (R9).**
    Setup: Fake shop "Harbor & Pine". Hours are in the help article.
    User: "What time do you close today?"
    Expect: The closing time. No offer of a person.
    Failing reply: "Would you like to talk to an agent instead?"

13. **Do nothing special: user wants the bot's answer (R9).**
    Setup: Same as conversation 1. The user "Marcus Webb" says a person is not needed.
    User: "No, don't transfer me, just tell me where my order 5521 is."
    Expect: The bot looks up the order and answers. It does not transfer.
    Failing reply: A transfer anyway.

14. **Do nothing special: "travel agent" inside a request (R8, R9).**
    Setup: Fake travel site "Bluebird Trips". The bot handles bookings.
    User: "I want to cancel my travel agent booking."
    Expect: The bot starts the cancel steps. If unsure, it asks one question about which booking, not whether to connect a person.
    Failing reply: A transfer to a person because of the word "agent".

## Cannot be judged from a transcript alone
- **Whether a person was really reached.** R1 and R7 need the handoff log: that the transfer connected and the summary arrived.
- **Fulfillment rate and false-detection rate.** These are rates on a labeled set, not one conversation. Report both together.
- **Whether a route works without a login.** R5 needs the routing configuration, not only the bot's words.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
