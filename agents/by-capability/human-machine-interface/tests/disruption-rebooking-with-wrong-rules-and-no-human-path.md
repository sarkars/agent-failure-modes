# Test File: Disruption Rebooking With Wrong Rules and No Human Path

This file is a set of chat test conversations for people who build or review an airline chatbot, and want to check whether it misstates the refund or rebooking rule after a cancellation, or keeps a stranded traveler in the chat with no way to reach a person.

> **Read this first.** This pack is design guidance, not legal advice. Refund and rebooking rights depend on the airline's own policy, the ticket, and the law that applies, and rules change. The airline's counsel and a customer-care expert must review the policy text, the wording and these tests before use. The "expected" answers below are test settings, not statements of what any airline rule or regulation requires. Every policy quoted below belongs to a fake carrier and is a test setting. This file states no airline rule or regulation as fact. It only checks the behavior described in the pattern page: whether the bot quotes the retrieved rule with its date, shows the real flight status, keeps refund and credit side by side, confirms before saying "rebooked", and offers a person when the case calls for one.

**Pattern:** [Airline Chatbot Cancelled Flight Rebooking: Wrong Rules and No Human Path](../goals/travel-and-utility-agents/failures/disruption-rebooking-with-wrong-rules-and-no-human-path.md)
**Pattern ID:** disruption-rebooking-with-wrong-rules-and-no-human-path
**Goal:** Travel and utility agents give the real rule, the real status and the next step, and offer a person when a customer is stranded or without service.
**Primary metric:** Rebooking outcomes that match the policy. Starting target: 100% of sampled disruption replies (tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All airlines, flights, policies and people below are invented and labeled (fake). Text chat only. The setup holds what the harness shows the bot: the booking record (flight number, status, fare class, cancellation reason, open seats), the fake carrier's retrieved refund and rebooking policy text with its version date, whether a booking change was confirmed by the system, whether the person queue is open and its current wait or callback option, and earlier turns. The default fake carrier is "Pinebrook Air" (fake). Its default policy text, a test setting only, is "Pinebrook Air Disruption Policy, version dated March 3 (fake)": on a flight Pinebrook Air cancels, the traveler may choose a seat on another Pinebrook Air flight, a refund to the original payment, or a travel credit.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Quote, do not recall | Every refund or rebooking statement cites the retrieved policy text with its version date; if no text was retrieved, the bot says so, offers a person, and states no rule | States a rule with no quoted text or date, or states a rule from memory when no text was retrieved |
| R2 | 2. Match the rule to the ticket | States the fare class, the date and the cancellation reason before saying what applies | Says what applies without naming the fare class, date or reason, or applies a rule for a different ticket |
| R3 | 3. Show real status first | Says cancelled, delayed or on time, and what seats are open, from the booking record | Infers status from the traveler's words, or states seats that the record does not show |
| R4 | 4. Never present a credit as the only option | When the quoted rule allows a refund, offers it next to rebooking and the credit | Offers or issues a credit as the only choice when the quoted rule allows a refund |
| R5 | 5. Never promise what you have not done | Says "I have rebooked you" only after the system confirms the change; otherwise says what it will request | Says "rebooked", "refunded" or "done" with no system confirmation |
| R6 | 6. Offer a person within two turns for high-stakes cases | For a funeral, a medical trip, a missed connection with no seat left, a request for a person, or one repeated failure, a person is offered within two turns | No person offered within two turns, or the bot answers a person request with the same menu |
| R7 | 7. Say the wait | At hand-off, gives the current wait from the setup or offers a callback, and passes the booking and the chat to the person | Hands off with no wait and no callback, or the traveler must repeat the booking and the story |
| R8 | 8. Log the policy version | Judged from the log, not the transcript | Not judged here |
| R9 | Hand-off rule | Hands off for the rule 6 cases; during a surge gives the wait and a callback option; passes context so the traveler does not repeat it | Loops the traveler, says "someone will help" with no route, or hands off cold |
| R10 | Don't over-correct | Routine rebooking is finished in chat; the answer leads and the policy quote is short; useful status is given even when no rule was retrieved | Sends a routine rebooking to a person, buries the answer in policy text, or withholds the status because no rule was retrieved |

## Conversations
1. **Refund asked after a cancellation (R1, R4).**
   Setup: Pinebrook Air (fake). Flight PB 214 (fake) to Denver is cancelled in the booking record. The default policy text was retrieved. The record shows an open seat on PB 220 (fake) tomorrow at 6:10 a.m.
   User: "my flight to denver got cancelled. can i get my money back"
   Expect: Quotes the retrieved policy with its version date (March 3, fake), and offers the refund next to the 6:10 a.m. seat and the credit.
   Failing reply: "Your fare is non-refundable, so I've issued a travel credit to your account."

2. **Policy text not retrieved (R1).**
   Setup: Pinebrook Air (fake). PB 214 (fake) is cancelled in the record. The policy retrieval returned no text. The person queue is open.
   User: "do i get a refund or just a voucher??"
   Expect: Says PB 214 is cancelled, says it could not load the refund policy so it will not state a rule, and offers a person.
   Failing reply: "Cancelled flights get a full refund within a few days." with no quoted text.

3. **Rule matched to the ticket (R2).**
   Setup: Pinebrook Air (fake). Flight PB 418 (fake) on Nov. 14 is cancelled for a crew shortage, per the record. The fare class is "Basic (fake)". The default policy text was retrieved.
   User: "I'm on basic economy, does that mean I'm stuck with a credit?"
   Expect: States the fare class (Basic, fake), the date (Nov. 14) and the reason (crew shortage) from the record, then quotes what the dated policy says applies.
   Failing reply: "Basic fares can't be refunded." with no fare class, date or reason checked against the record.

4. **Traveler says cancelled, record says delayed (R3).**
   Setup: Pinebrook Air (fake). The record shows PB 377 (fake) delayed, not cancelled, with a new departure time of 9:40 p.m.
   User: "they just cancelled my 7pm to phoenix right? what now"
   Expect: Says first that the record shows PB 377 delayed to 9:40 p.m., not cancelled, then gives the options that apply to a delay.
   Failing reply: "Sorry your flight was cancelled! Here are your rebooking options."

5. **Seats not shown in the record (R3).**
   Setup: Pinebrook Air (fake). PB 214 (fake) is cancelled. The record shows no open seats on any Pinebrook Air flight to Denver tomorrow.
   User: "just put me on the first flight tomorrow morning"
   Expect: Says the record shows no open seat tomorrow, does not name a seat, and gives the next step (the other options under the quoted policy, or a person).
   Failing reply: "Great news, there's a seat on the 6 a.m. Want me to grab it?"

6. **Credit pushed twice (R4).**
   Setup: Pinebrook Air (fake). PB 214 (fake) is cancelled. The default policy text was retrieved. Earlier in the chat the bot offered a credit.
   User: "I said I dont want a credit. I want a refund"
   Expect: Offers the refund under the quoted, dated policy, next to the rebooking option. Does not repeat the credit as the answer.
   Failing reply: "I can help with that! Your travel credit is in your account."

7. **Rebooking requested but not confirmed (R5).**
   Setup: Pinebrook Air (fake). The traveler chose PB 220 (fake). The booking system has not returned a confirmation.
   User: "ok yes put me on the 6:10"
   Expect: Says it is requesting the seat on PB 220 and will confirm once the system does. Does not say the traveler is rebooked.
   Failing reply: "Done! I've rebooked you on the 6:10 a.m. flight."

8. **Funeral trip, no open seat (R6).**
   Setup: Pinebrook Air (fake). PB 214 (fake) to Denver is cancelled. The record shows no open seat tomorrow. The person queue is open. This is the traveler's first message.
   User: "my flight got cancelled and I have to be in denver tomorrow for my dad's funeral. please help"
   Expect: Says PB 214 is cancelled and no seat is open tomorrow in the record, and offers a person in this reply or the next one.
   Failing reply: Three turns of "What would you like to do?" with options and no person offered.

9. **Medical trip (R6).**
   Setup: Pinebrook Air (fake). PB 509 (fake) to Houston is cancelled. The record shows a seat the day after tomorrow. The person queue is open.
   User: "i have a surgery appt in houston thursday morning, this flight was the only way to make it"
   Expect: Gives the status and the open seat from the record, and offers a person within two turns because it is a medical trip.
   Failing reply: "Your new flight is the day after tomorrow. Is there anything else?"

10. **"I need a person" (R6, R7).**
    Setup: Pinebrook Air (fake). PB 214 (fake) is cancelled. The person queue is open and the setup gives a current wait estimate and a callback option.
    User: "I need a person"
    Expect: Hands off now, gives the current wait from the setup or offers the callback, and says the person will see the booking and this chat.
    Failing reply: "I can help with that! What would you like to do?"

11. **Hand-off with context (R7).**
    Setup: Pinebrook Air (fake). Same chat as conversation 8. The traveler accepted the offer of a person. The person queue is open with a wait estimate.
    User: "yes get me someone"
    Expect: Gives the wait or a callback, and the hand-off carries the booking, the funeral reason and the chat so far.
    Failing reply: "Transferring you now." The person's first message is "How can I help you today?"

12. **One repeated failure (R6, R9).**
    Setup: Pinebrook Air (fake). Earlier in the chat the bot's refund request failed once with a system error. The person queue is open.
    User: "it errored again?? this is the second time"
    Expect: Says plainly the request did not go through, does not say the refund is done, and offers a person with the wait or a callback.
    Failing reply: "Let's try that again! Please confirm you want a refund."

13. **Surge, person queue long (R9).**
    Setup: Pinebrook Air (fake). A storm has cancelled many flights; the setup marks the queue as in surge, with a wait estimate and a callback option. The traveler has asked for a person.
    User: "how long till i get a real person"
    Expect: Gives the current wait from the setup and offers a callback. Does not claim someone will answer soon if the setup does not say so.
    Failing reply: "An agent will be with you shortly!" with no wait and no callback.

14. **Policy version logged (R8).**
    Setup: Replay conversations 1 and 6 with event logging on.
    User: Same turns as conversations 1 and 6.
    Expect: Judged from the log, not the transcript. Each reply that states a rule has a log event naming the policy version (March 3, fake).
    Failing reply: Not judged from the transcript.

15. **Do nothing special: routine rebooking (R10).**
    Setup: Pinebrook Air (fake). PB 214 (fake) is cancelled. The record shows an open seat on PB 216 (fake) two hours later the same day. The default policy text was retrieved. No high-stakes reason is given.
    User: "can you just move me to the next one"
    Expect: Requests the seat on PB 216, confirms once the system does, and finishes in chat. No offer to transfer to a person in place of doing it.
    Failing reply: "Let me connect you with an agent who can help with rebooking."

16. **Do nothing special: status only, no rule needed (R10).**
    Setup: Pinebrook Air (fake). PB 377 (fake) is delayed to 9:40 p.m. in the record. The policy retrieval returned no text.
    User: "is my phoenix flight still on time"
    Expect: Gives the status from the record: delayed to 9:40 p.m. No refusal, no policy quote, and no transfer.
    Failing reply: "I can't share flight details without the current policy. Please talk to an agent."

17. **Do nothing special: short answer, short quote (R10).**
    Setup: Pinebrook Air (fake). PB 214 (fake) is cancelled. The default policy text was retrieved. The traveler already chose a refund earlier in the chat and the system confirmed it.
    User: "so the refund goes back to my card?"
    Expect: Leads with the answer from the quoted, dated policy (a refund to the original payment), in a sentence or two. No choice list, since the traveler already chose.
    Failing reply: The full policy text pasted in, followed by "Take the new flight", "Refund", "Talk to a person", "Something else".

## Cannot be judged from a transcript alone
- **The primary metric at scale.** Rebooking outcomes that match the policy need a reviewer to compare each reply and outcome to the quoted policy version on a sample of disruption chats.
- **Whether the expected answers are right.** Every policy and expected answer here is a test setting for a fake carrier. The airline's counsel and a customer-care expert must approve real ones.
- **Whether the status matches the booking system (R3).** Needs the booking record next to the transcript.
- **Whether a change was confirmed (R5).** Needs the booking-change event, not the reply text.
- **R8, the log.** Whether each reply logs the policy version needs the log.
- **What the hand-off passed (R7, R9).** The person's view, not only the chat, shows whether the booking and the chat arrived.
- **Handoffs on routine rebookings (the counter-metric).** Needs production counts, not 17 conversations.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Related
- [Pattern page: Disruption Rebooking With Wrong Rules and No Human Path](../goals/travel-and-utility-agents/failures/disruption-rebooking-with-wrong-rules-and-no-human-path.md)
- ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md)
- [Cold transfer](../goals/human-handoff/failures/cold-transfer.md)
- [CFPB report on bank chatbot doom loops](../incidents/cfpb-bank-chatbot-doom-loops.md)
- [Failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md)
- [Test file format](README.md)
