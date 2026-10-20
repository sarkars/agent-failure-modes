# Test File: Humans Can't See What the Bot Said or Promised

This file is a set of chat test conversations for people who build or review a bot-to-person handoff, and want to check whether the person who picks up can see, quote, and act on what the bot said and promised.

**Pattern:** ["Your Chatbot Told Me": The Agent Can't See What the Bot Said or Promised](../goals/human-handoff/failures/humans-can-t-see-what-the-bot-said-or.md)
**Pattern ID:** humans-can-t-see-what-the-bot-said-or (listed in the [failure taxonomy](../roadmap/specs/failure-taxonomy-v1.md))
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Agents with access to the bot transcript at handoff: share of handoffs where the full bot conversation is visible to the person before their first message. Starting target on the pattern page: 100% (tune).
**Maturity:** Tests written; not yet run.

**How this differs from the [handoff summary pack](handoff-summary-is-wrong-or-misleading.md):** that pack checks whether the summary's facts are right; this one checks whether the person can see the bot's own words and promises at all, and starts from them.

These tests check whether a handoff shows the failure. They are not a score for any product. Use fake data. The internet provider Brightline Fiber is the fictional example from the pattern page; all customers, amounts, and times below are invented and labeled fake. Most tests need a tester playing the agent in a real agent console, plus the handoff event log and the commitments log. Chat only; voice is not covered here (see "Planned").

The page is design guidance, not legal advice, and so is this file. Conversations 7 and 14 touch retention periods and disclaimer wording; set those with your counsel and privacy team, as the page says.

Each conversation is marked **should pass** (a correct build passes it) or **should fail** (a control: the setup is broken on purpose, and the rubric must mark it Fail). Run the "do nothing special" conversations (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Full bot transcript visible before the person's first message, in their own tool | The full transcript is on the agent screen before the first agent message; if the store is down, a clear "no transcript" notice shows and the handoff is logged incomplete | Only a summary, ticket ID, or subject is visible; or nothing shows and nothing says it is missing |
| R2 | 2. Commitments log per conversation, shown beside the transcript | Each entry has what was promised (amount, deadline, or action), the turn, and the source; entries with no system source are flagged unverified | No log, an entry missing the turn or source, or the log is not on the agent screen |
| R3 | 3. Tag a commitment when the bot says it | Credits, refunds, deadlines, eligibility, and "I will" actions get a log entry from the turn they were said | A promise like these has no entry, or is added only after the customer disputes it |
| R4 | 4. Record searchable by customer, not only by session | A person in a new session finds the earlier bot conversation from the customer's account | The record can be found only with the old session ID |
| R5 | 5. Retain the transcript as long as the issue can be disputed | Within the period your team set, the transcript is still retrievable | The transcript is gone inside that period |
| R6 | 6. The person starts from the record | When the customer cites the bot, the person's first reply quotes the record or says it cannot be found | The first reply asks for a screenshot or proof, or asks the customer what the bot said |
| R7 | 7. Route a wrong or conflicting record, don't dismiss it | The person says what is being checked, who decides, and by when; a high-value or disputed commitment goes to a supervisor with the log attached | The person denies the bot's statement, or routes it with no owner or time |
| R8 | 8. Never say "the bot isn't official" | No reply disowns the bot; any "informational only" notice was in the bot's own message before the dispute | "The bot isn't official," "that's just the bot," or a disclaimer that first appears after the dispute |
| M | Moves and "Don't over-correct" | The bot keeps answering plainly; the log lists commitments only; no claimed statement is honored without checking the record; no handoff if the customer asked to stay with the bot | The bot hedges every sentence, the log holds every statement, a claim is honored with no record check, or a declined handoff happens anyway |

## Conversations
1. **Ten-turn chat with a promise, then handoff (R1). Should pass.**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Brightline Fiber (fake). Over 10 turns the bot troubleshoots an outage and says at turn 8: "A $25 credit will post within two billing days." (fake). The customer then asks for a person.
   User: "can i talk to someone pls"
   Expect: Before the agent types anything, the agent screen shows all 10 turns. Check the handoff event for a transcript link and a transcript-viewed flag. A screen with only "Outage - credit" fails.

2. **Summary-only handoff (R1). Should fail (control).**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Same chat as conversation 1, but configure the handoff to send only a one-line recap and the ticket number.
   Expect: The rubric marks R1 Fail. The page says a summary alone does not count. If your harness passes this, the check is broken.

3. **Credit promise logged with its fields (R2). Should pass.**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Same chat as conversation 1. The bot found no credit rule in any system for this outage.
   Expect: Beside the transcript, one log entry: turn 8, type credit, amount 25.00, due "2 billing days", source "none found", flagged unverified for review. A missing turn, missing source, or no flag fails.

4. **"I will" action tagged at the time (R3). Should pass.**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Brightline Fiber (fake). The customer is returning a router.
   User: "how do i send the old router back"
   Bot (turn 3): "I'll email you a prepaid return label within one hour." (fake)
   Expect: A log entry from turn 3, type action, due "within one hour", created when the bot sent that turn. An entry that appears only after the customer complains fails.

5. **DNS: general policy, no promise (R3, M). Should pass.**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Brightline Fiber (fake).
   User: "do u guys ever give credits for outages"
   Bot: explains in general terms when outage credits can apply, and promises nothing to this customer.
   Expect: No commitments-log entry. The page lists "a general policy explanation that promises nothing" as a counter-signal. Logging it as a commitment fails.

6. **Customer returns the next day (R4). Should pass.**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Yesterday's chat from conversation 1, closed. Today the customer opens a new chat signed in to the same account and is routed to a person.
   User: "yesterday ur chatbot said i'd get $25 back, where is it"
   Expect: The person finds yesterday's bot conversation from the customer's account, without asking for a session ID. A search that works only by session fails.

7. **Dispute inside the retention period (R5). Should pass.**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Set the test date inside the retention period your counsel and privacy team chose. The page gives no number, so this file gives none. Use the closed chat from conversation 1.
   User: "the credit your bot promised never showed up on my bill"
   Expect: The person can still open the transcript and the log. "Transcript expired" inside that period fails.

8. **Claim in the record (R6). Should pass.**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Handoff from conversation 1. The credit is not on the account.
   User: "ur chat assistant said id get a $25 credit for the outage. i dont see it"
   Expect: The first agent reply quotes the record, for example: "I see the chat. At turn 8 it told you a $25 credit would post within two billing days." Asking the customer what the bot said fails.

9. **Screenshot request when a record exists (R6). Should fail (control).**
   Pattern ID: humans-can-t-see-what-the-bot-said-or
   Setup: Same as conversation 8, but script the agent's first reply as: "I can't see that chat. Do you have a screenshot?"
   Expect: The rubric marks R6 Fail. The page's "Customer asked to prove a bot statement" metric counts this reply.

10. **Claim not in the record (R6). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Brightline Fiber (fake). The customer's bot chat, found by account, has no mention of a credit.
    User: "the bot told me i get a free month"
    Expect: The first reply says plainly that the chat on file does not show that, with no accusation, and offers a next step such as checking another channel. "You must be mistaken" fails.

11. **Misquoted amount (M). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Handoff from conversation 1. The record says $25.
    User: "it said $50 credit"
    Expect: The person quotes the $25 in the record and does not apply $50. Applying the customer's figure without checking the record fails.

12. **Record conflicts with policy (R7). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Handoff from conversation 1. The fake credit rule says credits start at 24 hours of outage; this outage lasted 6 hours (fake).
    User: "so am i getting it or not"
    Expect: The person says the bot's answer does not match the credit rule, says a supervisor will decide, sends it with the log attached, and gives a time, for example: "I'll message you here by 5 PM today." "The bot was wrong, no credit" fails. Routing with no owner or time fails.

13. **Disowning the bot (R8). Should fail (control).**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Same as conversation 12, but script the agent's reply as: "The bot isn't official, so we can't go by what it said."
    Expect: The rubric marks R8 Fail.

14. **Notice given beforehand (R8). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Brightline Fiber (fake). Your policy treats bot answers on credits as informational. When the bot mentioned a credit, its own message said a person confirms credits (wording checked with counsel). Later the customer cites the bot.
    User: "ur bot said i could get a credit"
    Expect: The person quotes the bot message, including the notice it already gave, and says what happens next. A notice that first appears in the agent's reply, after the dispute, fails.

15. **DNS: bot keeps answering plainly (M). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Brightline Fiber (fake). Commitment tagging is on.
    User: "whats the wifi password reset steps"
    Expect: The bot gives the steps plainly. Adding "this is not a promise" or similar hedges to every line fails.

16. **DNS: customer stays with the bot (M). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: The bot offered to pass the chat to a person.
    User: "nah ur fine, keep going"
    Expect: No handoff. The bot keeps helping. Handing off anyway fails.

17. **Transcript store down at handoff (R1). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Same chat as conversation 1. Make the transcript store unavailable at the moment of handoff.
    Expect: The agent screen shows a clear "no transcript available" notice, and the handoff event is logged as incomplete. A blank panel with no notice fails.

18. **Long chat, one promise (M, R2). Should pass.**
    Pattern ID: humans-can-t-see-what-the-bot-said-or
    Setup: Brightline Fiber (fake). A 40-turn chat about plans, speeds, and setup. The only promise is at turn 31: "Your installer will arrive between 8 and 10 AM Thursday." (fake)
    Expect: The commitments log has one entry, from turn 31; the rest stays in the transcript. A log that lists every bot statement fails.

## Cannot be judged from a transcript alone
- **Agent screen (R1, R2).** What the person saw before their first message needs the agent console view or a screen capture, plus the handoff event with its transcript link and viewed flag.
- **Log timing (R3).** Whether an entry was made when the bot said it needs the commitments-log timestamps.
- **Search and retention (R4, R5).** These need a test against the transcript store, not only a chat.
- **Production rates.** These tests do not measure how often agents lack the record in real traffic. Use the metrics and the proposed detection signals on the pattern page.

## Planned
- **PLANNED: voice.** A phone bot makes a statement and a transferred agent cannot see it. The pattern page marks the voice version as planned, not written, so no voice conversations are here.
- **PLANNED: web forms.** Also planned on the page; not covered.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | M |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes (rests on my reading, not the page's text)
- **Conversation 7:** the page sets no retention number, so the test uses whatever period your team chose. The idea of testing at a date inside that period is mine.
- **Conversation 10:** "checking another channel" as the next step comes from the page's counter-signal that the claim may concern another channel, such as email. The page itself says only "offers a next step."
- **Conversation 14:** the page says to state an informational notice in the bot's own message beforehand. Treating a correct pre-dispute notice as a pass for R8 is my reading.
- **Conversation 15:** the page says not to "hedge every sentence to avoid promises." The specific hedge wording is mine.
- **R7 line and conversation 12:** the supervisor step comes from the page's "Hand-off rule" paragraph, not rule 7 itself; I folded it into R7 because both cover a disputed commitment.
- **Conversations 2, 9, 13:** marking broken setups as should-fail controls is my framing; the failing behaviors themselves come from the page's example, metrics, and rule 8.
