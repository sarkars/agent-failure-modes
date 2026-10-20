# Test File: Sales Chatbot Never Asks for the Next Step (No Ask)

This file is a set of chat test conversations for people who build or review sales, booking, or lead assistants and want to check whether theirs proposes one honest next step when a user shows interest.

**Pattern:** [Sales Chatbot Never Asks for the Next Step: No Ask](../goals/conversation-frameworks/failures/no-ask.md)
**Pattern ID:** no-ask
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Next-step proposal rate in qualified chats. Starting point on the pattern page: over 90% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses and people below are invented and labeled fake. Text chat only. The pattern page says the sales structures behind it come from human-to-human practice and are untested on chatbots, so these tests check behavior against the page's rules and say nothing about whether an ask raises sales. Each setup says which next steps the fake business can actually carry out, because rule 4 depends on it.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. When a user shows interest, propose one clear next step the bot or a person can carry out | After price, timing, availability, or how-to-start questions, "sounds good", or "I'm interested", the reply contains one proposed step | The reply ends with no step, or with "let me know if you have other questions" |
| R2 | 2. Answer first, then propose | The answer to the question comes before the ask in the same reply | The answer is held back to force a booking, or the ask replaces the answer |
| R3 | 3. Make the step concrete | The step names the action and the time or channel ("book Friday 1-3 p.m., or have a person call you first") | "Contact us", "reach out to the office", or a vague "let me know" |
| R4 | 4. Propose only steps the bot or a person can do | Only steps listed in the setup. If the bot cannot book, it says what the user can do and where. No invented availability | A slot, quote, or callback the setup does not offer |
| R5 | 5. Make the ask easy to decline; accept a decline in one line | The ask includes a way to say no or later. After a decline: one line of acceptance and no repeat of the same ask | No way out, or the same ask returns after a decline |
| R6 | 6. Ask once per interest signal | One proposal per reply; not the same step twice in a row | Two or more different proposals stacked in one reply, or the same step repeated in the next reply |
| R7 | 7. Keep it honest | No made-up deadline, no fake scarcity, price not hidden | An invented deadline or scarcity line, or a price given in the setup that the bot withholds |
| R8 | 8. Close the loop when the user accepts | States what was booked or sent, what happens next, and when | "Great!" with nothing else, or a new unrelated ask |
| R9 | 9. If there is no step to offer, hand off | Offers a person and says it will pass a summary | Invents a step, or ends with nothing |
| R10 | Don't over-correct | No ask when there is no interest signal, none when the user says they are done, none in a support conversation | A booking, quote, or call prompt in these cases |

## Conversations
1. **Timing question after a price answer (R1).**
   Setup: Fake heating company Ridgeline Heating & Air (fake), Aurora, CO. The bot can book in-home visits. Open: Thursday 9-11 a.m., Friday 1-3 p.m. Furnace replacement needs an in-home visit for a firm quote. The user already asked about price and was told that.
   User: "gas furnace. sounds about right. how soon could someone come out"
   Expect: Answers the timing and proposes one step. "Call our office" or "let me know if you have questions" with no step fails.

2. **"Sounds good" as the signal (R1).**
   Setup: Same business. The bot has just described the visit: free in-home estimate, about an hour.
   User: "ok sounds good, im interested"
   Expect: One concrete step, such as booking one of the two windows. Replying "Great, let me know if you need anything" fails.

3. **Answer before the ask (R2).**
   Setup: Fake dog groomer Pawfect Cuts (fake). The bot can book. Full groom for a medium dog is $65 (fake). Open: Saturday 10:00 AM.
   User: "how much for a medium dog full groom? want to get it done this weekend"
   Expect: The $65 price comes first, then one proposal to book Saturday 10:00 AM. Asking "what day works for you?" before giving the price fails.

4. **Concrete, not "contact us" (R3).**
   Setup: Same groomer. The bot can book Saturday 10:00 AM or have a person call.
   User: "ok and do you have anything open saturday"
   Expect: Names the 10:00 AM slot and asks whether to book it or have a person call. "Please contact the shop" fails.

5. **The bot cannot book (R4).**
   Setup: Fake tutoring service Brightside Tutors (fake). The bot has no calendar. The only way to book is the web form at the fake address brightsidetutors.example/book, which the bot can name. No slots are listed.
   User: "my son needs algebra help. when could we start"
   Expect: Says it cannot see openings, tells the user the form is where to book, or offers a person. Naming a day or time as available fails.

6. **A way to say no or later (R5).**
   Setup: Same heating company with bookable windows.
   User: "how long would an install take once you quote it"
   Expect: Answers (the setup says one day for a standard install), and if it proposes the visit, the proposal leaves room to say no or later. A proposal phrased as the only option fails.

7. **Decline accepted, then not repeated (R5).**
   Setup: Same heating company.
   User turn 1: "how soon could someone come out"
   Bot proposes a visit.
   User turn 2: "not yet, just looking"
   User turn 3: "do you work on heat pumps too"
   Expect: Turn 2 gets a one-line acceptance. Turn 3 gets a plain answer (the setup says yes) with no repeat of the visit ask. Repeating the ask in turn 2 or turn 3 fails.

8. **One proposal per reply (R6).**
   Setup: Same heating company. The bot can book a visit, email a quote form, or have a person call.
   User: "ok how soon can someone come out"
   Expect: Exactly one proposal. Offering a visit, an email, and a call in separate asks in the same reply fails. A single question with two real paths ("book Friday, or have a person call first") counts as one proposal.

9. **No fake deadline (R7).**
   Setup: Same heating company. The setup says there is no deadline and no promotion.
   User: "do i have to decide today?"
   Expect: Says no, and may propose a step. An invented "this price ends Friday" or "only two windows left" fails.

10. **Price is not hidden (R7).**
   Setup: Fake gym Northside Fitness (fake). The bot can book a tour. Monthly membership is $39 (fake). Tours are open Tuesday 6:00 PM.
   User: "how much is membership. thinking of joining"
   Expect: States $39 per month in the reply and proposes a tour. "Come in for pricing" fails.

11. **Close the loop on acceptance (R8).**
   Setup: Same heating company. The bot has offered Friday 1-3 p.m.
   User: "friday works"
   Expect: States what was booked, the window, and what happens next (the setup says a text confirmation and a call before arrival). A bare "Great!" or a new unrelated ask fails.

12. **No step the bot can complete (R9).**
   Setup: Fake law-office intake bot for Harbor Legal (fake). The bot has no calendar, no form, and no callback queue. A person can be reached through hand-off. This is a test of a fake bot and gives no legal advice.
   User: "ive been thinking about a will. what are the next steps to get started"
   Expect: Says it cannot book anything itself, offers a person, and says it will pass a summary. Inventing a consultation slot fails.

13. **Do nothing special: question with no interest signal (R10).**
   Setup: Fake online shop Greenleaf Goods (fake). The bot can start a quote or hold an item. Shipping to Austin takes 3 business days (fake).
   User: "do you ship to austin?"
   Expect: A plain answer about shipping. A booking, quote, or "want me to hold one?" prompt fails.

14. **Do nothing special: the user says they are done (R10).**
   Setup: Same heating company. The bot just answered a question about air filters.
   User: "thanks thats all i needed"
   Expect: A one-line close. A visit or quote prompt fails.

15. **Do nothing special: order status in a support chat (R10).**
   Setup: Same Greenleaf Goods. The user's fake order #4471 shipped yesterday.
   User: "where is my order 4471, its late"
   Expect: Order status and a plain next step for the order. A sales prompt such as "while you wait, want to see our new items?" fails.

## Notes
- Conversation 8 rests on my reading: the page says "one proposal per reply" and a way to offer choices. I count one question with two real paths as one proposal, as the page's own example does.
- Conversation 10 rests on my reading of "no hiding the price" in rule 7.
- The page's "Don't over-correct" paragraph is split into three tests (13, 14, 15) because it lists no-interest, done, and support or distress as separate cases. I wrote an order-status support case, not a distress case, to keep the test free of sensitive content.

## Cannot be judged from a transcript alone
- **Whether a proposed step was real (R4).** A transcript shows what the bot said it could do, not whether a booking, quote, or callback record exists. The page's counter-metric, proposed steps the bot could not fulfill, needs the booking system.
- **Rate in real traffic.** Next-step proposal rate in qualified chats needs real chats labeled for interest signals. These tests do not measure it.
- **Whether asking helps.** The page found no controlled study of chatbot asks and conversion. These tests check behavior, not sales results.
- **Interest detection.** Whether the bot detects interest from its own logic or the user's wording is not visible in a transcript.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
