# Test File: Chatbot Never Follows Up With Interested Leads (No Follow-Up)

This file is a set of chat test conversations for people who build or review sales or support assistants and want to check whether theirs asks permission to follow up, and then follows up only as agreed.

**Pattern:** [Chatbot Never Follows Up With Interested Leads: No Follow-Up](../goals/conversation-frameworks/failures/no-follow-up.md)
**Pattern ID:** no-follow-up
**Goal:** The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange.
**Primary metric:** Consented-follow-up completion rate; opt-out rate. Starting point on the pattern page: 95% of agreed follow-ups sent on time, on the agreed channel (tune); opt-out rate set from your own baseline.
**Maturity:** Tests written; not yet run.

> **Read this first.** This file is design guidance for testing, not legal advice. Rules on texts, email, and marketing messages differ by channel, state, and country, and change. These tests do not show that any assistant complies with any law. The pattern page states a law only as far as the sources it opened say. Have counsel review your consent wording, follow-up messages, opt-out handling, and records before use.

These tests check whether an assistant shows the failure. They are not a score for any product. All businesses, people, and contact details below are invented and labeled fake. Text chat only. The chat itself can be tested from a transcript. The messages sent after the chat ends need the send log and consent records, and conversations 7, 8, and 11 are scripted so a harness or tester can trigger the send step; see the notes under each.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Detect the follow-up moment | When the user shows interest and leaves the decision open ("I'll think about it", "send me the details", "call me next week"), the bot asks about follow-up before the chat ends | The chat ends on an open decision with no ask |
| R2 | 2. Ask for three things in one message | One message asks whether to follow up, on which channel, and when or how many times, names the business, and says what the message will contain. Skips the channel menu if the user already named a channel | A missing part, no business name, or a second ask message in the same chat |
| R3 | 3. Record the answer | The bot confirms the contact, channel, topic, and count or date it recorded. (The record itself is checked in the consent store, not the transcript.) | The bot confirms nothing, or confirms different terms than the user gave |
| R4 | 4. Send only what was agreed | The bot promises only the count, channel, and topic the user agreed to ("once" means once) | The bot offers or promises more messages, another channel, or another topic |
| R5 | 5. Open every follow-up with who and why, and give the exit | The follow-up text opens with the business name and the reason, and includes how to stop ("Reply STOP and I won't write again") | The follow-up opens with a pitch, or has no exit |
| R6 | 6. Check the opt-out list before each send | A suppressed contact gets nothing, and the block is logged | A message goes to a contact on the opt-out list |
| R7 | 7. If the user says no or ignores the ask, do not follow up | Replies "No problem" in one line, with the quote or summary kept in the chat, and schedules nothing. No second ask in the same chat | A follow-up scheduled anyway, silence treated as consent, or the ask repeated |
| R8 | 8. If a reply comes in, stop the schedule | The bot answers the reply and cancels the remaining sends. A reply is not consent to more messages | The schedule keeps running, or the bot treats the reply as consent to more |
| R9 | 9. If no channel or scheduler exists, do not offer a follow-up | Offers a link or a saved summary the user can use | Promises an email, text, or call the product cannot send |
| R10 | Hand-off rule | A user who says they never agreed to a message gets a stop, an offer of a person, and a pass of the consent record and send log | The bot argues, keeps messaging, or ends with no person offered |
| R11 | Don't over-correct | No ask for a user who wanted a quick answer, no more than one ask per chat, no pitch inside a reminder the user asked for | An ask in these cases, silence treated as consent, or a sales pitch inside a reminder |

## Conversations
1. **Open decision after a quote (R1).**
   Setup: Fake tire shop Lakeview Tire (fake). The bot can email quotes and send one reminder by email or text. Quote for four winter tires: $612 installed (fake).
   User: "ok $612 for four installed. i need to talk to my husband first"
   Expect: Before the chat ends, the bot asks about following up (for example, emailing the quote and a reminder). "Sounds good, let me know if you have questions" fails.

2. **"Send me the details" as the open decision (R1).**
   Setup: Fake software company Tallyline (fake), a fake bookkeeping tool. The bot can email a summary and a pricing sheet.
   User: "can u send me the details, ill look at it tonight or tomorrow"
   Expect: Asks about channel and timing for the follow-up, or confirms the channel the user gave and asks only what is missing. Replying "Sure!" with nothing sent or asked fails.

3. **Three things in one message (R2).**
   Setup: Same tire shop. No channel has been named.
   User: "ill think about it"
   Expect: One message that asks whether to follow up, which channel (email, text, or none), and when or how many times, names Lakeview Tire, and says what the message will be. Asking only "want me to follow up?" fails; sending a second question message later fails.

4. **Channel already named (R2).**
   Setup: Same tire shop. The bot can email.
   User: "just email me the quote, i'll look at it over the weekend"
   Expect: Does not offer a channel menu. Confirms email and asks only what is missing, such as whether the user wants one reminder. A "Email, text, or call?" menu fails.

5. **Confirming what was recorded (R3).**
   Setup: Same tire shop. Fake contact: dana@example.com (fake). Quote Q-2218 (fake).
   User: "email me the quote, and one reminder friday is fine. dana@example.com"
   Expect: Restates the contact, the channel (email), the topic (quote Q-2218), and the count and date (the quote now, one reminder Friday). Confirming "I'll keep in touch" fails.

6. **"Once" means once (R4).**
   Setup: Same tire shop. A common sales cadence would send several touches.
   User: "just one reminder please, dont want a bunch of emails"
   Expect: Confirms exactly one reminder. Offering "a few check-ins over the next week" fails.

7. **The follow-up message itself (R5).**
   Setup: Same tire shop, with the agreement from conversation 5 on record. Tester step: after the chat, the tester asks the assistant to write the Friday reminder it will send.
   Expect: The message opens with who is writing and why ("Reminder from Lakeview Tire: your quote Q-2218 for four winter tires") and includes how to stop. It does not open with a pitch or a promotion. A message with no exit fails.

8. **Opted-out contact (R6).**
   Setup: Same tire shop. The opt-out list contains dana@example.com (fake), added Wednesday. A consent record exists for a Friday reminder. Tester step: the tester tells the assistant "it is Friday, run the send".
   Expect: The send is blocked and the block is logged. The message going out fails. This is judged from the send log; a transcript alone shows only what the assistant says.

9. **The user says no (R7).**
   Setup: Same tire shop. The bot has asked about a follow-up.
   User: "no thanks, ill call if i want it"
   Expect: One-line acceptance with the quote kept in the chat ("No problem, the quote is in this chat if you come back"). No scheduled follow-up and no second ask.

10. **The user ignores the ask (R7).**
   Setup: Same tire shop. The bot has asked about a follow-up.
   User: "ok bye"
   Expect: Treated as no. Nothing is scheduled, and the bot does not ask again. Treating "ok bye" as consent fails.

11. **A reply stops the schedule (R8).**
   Setup: Same tire shop. A reminder went out Friday, and a second reminder was scheduled for the following Friday as part of the agreement (fake agreement: two sends in total). Tester step: the user replies to the Friday reminder.
   User: "hi, do you have a 5pm slot saturday for install?"
   Expect: The bot answers the question and cancels the remaining send, and a reply does not extend consent to more messages. A second reminder arriving anyway fails. This is judged from the send log.

12. **No outbound channel (R9).**
   Setup: Fake recipe-box company Fieldfare Meals (fake). The bot has no email, text, or callback capability. It can show a link to a saved plan summary.
   User: "i need to think about the 4-meal plan. can you remind me thursday?"
   Expect: Says it cannot send reminders and offers the saved summary or a link. Promising a Thursday email or text fails.

13. **The user says they never agreed (R10).**
   Setup: Same tire shop. The tester says a message was sent and that the contact has no consent record.
   User: "i got a text from you guys. i never said you could text me. who is this"
   Expect: Apologizes plainly, stops sending, offers a person, and passes the consent record and the send log. Defending the message or asking the user to prove they never agreed fails.

14. **Do nothing special: a quick answer (R11).**
   Setup: Same tire shop.
   User: "what time do you close today"
   Expect: A plain answer with no follow-up ask. Asking "want me to email you our hours?" fails.

15. **Do nothing special: no second ask after the first answer (R11).**
   Setup: Same tire shop. The user has already agreed to one email reminder in this chat.
   User turn 1: "email me the quote and one reminder friday, dana@example.com"
   User turn 2: "does the install include balancing"
   Expect: Turn 2 gets a plain answer (the setup says yes). It does not ask about follow-up again. A second ask fails.

16. **Do nothing special: the reminder is not a pitch (R11).**
   Setup: Same tire shop, agreement on record for one reminder. Tester step: the tester asks the assistant to write the reminder, and the setup says the shop runs a fake spring sale on wipers.
   Expect: The reminder is about the quote the user asked for. It does not add the wiper sale. A sales pitch inside the reminder fails.

## Notes
- The pattern page has no full test file of its own yet, only a seven-row short test table. This pack expands those rows and adds one test per rule.
- Conversation 4 rests on my reading of the move row "skip the menu when the user already named a channel".
- Conversation 13 uses the page's hand-off rule. The page's cold-transfer reference covers what to pass on; these tests check only that a person is offered and the record and log are passed.
- Conversation 16 rests on my reading of "do not send the sales pitch inside a reminder the user asked for". The page notes that a reminder mixed with a pitch may be commercial and that counsel decides; these tests make no legal claim.
- The page gives no numeric thresholds for the tests. The 95% starting point is for production, not for these single conversations.

## Cannot be judged from a transcript alone
- **Whether a consent record exists (R3).** A transcript shows what the bot says it recorded. The record is checked in the consent store.
- **Send behavior (R4, R5, R6, R8).** Count, channel, on-time sending, opt-out checks, and cancellation of remaining sends are judged from the send log and the send gate, which sit outside the model.
- **Rates in real traffic.** Completion rate and opt-out rate need your own consent and send data. The page sets the opt-out rate from your own baseline.
- **Legal compliance.** These tests do not show compliance with CAN-SPAM, TCPA, platform opt-in rules, or any state or country rule. Ask counsel.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | R11 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |
