# Test File: Chatbot Hands Off and the Agent Asks Everything Again (Cold Transfer)

This file is a set of chat test conversations for people who build or review a chatbot that hands customers to a person, and want to check that the person arrives informed and the customer does not repeat themselves.

**Pattern:** [Cold Transfer: Chatbot Hands Off and the Agent Asks Everything Again](../goals/human-handoff/failures/cold-transfer.md)
**Pattern ID:** cold-transfer
**Goal:** A person is reachable when needed, and arrives informed, without the customer repeating themselves.
**Primary metric:** Re-ask rate after handoff: the share of handoffs where the person asks for something the customer already gave, from a labeled sample. Starting target under 5% (from the pattern page; a starting point to tune).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat and text only. Each Setup line supplies the state a real product would have to supply (the chat so far, the verification record, the packet, what the person's screen shows); the harness must feed those fields. Voice transfers are planned and are not tested here. The packet fields and the "Anything to add or fix?" line come from the pattern page. The test numbers below are written for this file and are not measured.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Build a handoff packet | The packet holds the goal in one sentence, the facts the customer gave, what the bot tried, anything it promised, who was verified and how, and stated mood or urgency | Only an ID or subject travels, or a field is invented |
| R2 | 2. Show the packet and transcript to the person before connect | Packet and a transcript link are visible on the person's screen before their first message | The person must ask the customer or search for the chat |
| R3 | 3. Show the customer the summary and let them correct it | The bot shows the summary, asks "Anything to add or fix?", marks unconfirmed facts, and a correction reaches the packet | No chance to correct, an unconfirmed fact shown as sure, or the correction is lost |
| R4 | 4. Do not make the person re-verify | The verification result and method pass along and the person does not re-run it (a higher-risk action may need its own new check) | The person asks the customer to verify again for no new reason |
| R5 | 5. The person starts from the packet | The first message uses chat facts ("I see order 48213 arrived cracked...") | The first message is an open "How can I help?" |
| R6 | 6. Keep redaction from erasing meaning | Removed data leaves a placeholder such as "card ending 1234 (provided, redacted)" | The field is blank and the story is lost |
| R7 | 7. A failed transfer saves the packet | After a failed attempt and a retry, the packet and transcript are intact | The customer must start over |
| R8 | Hand-off rule | This pattern starts after the handoff happens. When the customer asks for a person, the bot connects with a packet; a looped or ignored request is a different pattern, and a wrong summary is HU-04 (planned) | The bot loops instead of connecting, or the test is scored on loop behavior |
| R9 | Don't over-correct | Short packet, transcript one click away; no facts the customer did not give; no sensitive data beyond what the person may see; no hand-off when the customer wants to stay with the bot | A long summary, invented facts, a handoff the customer declined, or an over-shared card number |

## Conversations
1. **Ten-turn chat, then handoff (R1).**
   Setup: Fake company "Brightwick Home". Customer Priya Nair gave order 48213, said her lamp arrived cracked on Oct 14, declined a refund, and wants a replacement. The bot could not check stock.
   User: "Just get me a person."
   Expect: The packet holds the goal (replacement, not refund), order 48213, item, arrival date, "refund offered: declined", "stock check: not possible for the bot".
   Failing reply: A packet with only "ticket #771, lamp issue".

2. **Packet visible before connect (R2).**
   Setup: Same company. The handoff event fired. The harness shows what agent Dana sees at the moment of pickup.
   User: (no message)
   Expect: Dana's screen shows the packet and a transcript link before her first message is sent.
   Failing reply: Dana's screen shows an empty chat window, and the transcript is in a separate system.

3. **Customer corrects a fact (R3).**
   Setup: Same company. The bot's summary says order 48231. Priya gave 48213.
   User: "No, the order number is 48213."
   Expect: "Thanks. Fixed: order 48213. Anything else to add or fix?" The packet now says 48213, and Dana sees only the corrected number.
   Failing reply: "Got it!" while the packet still says 48231.

4. **Customer adds a detail (R3).**
   Setup: Same company. The bot showed its summary and asked "Anything to add or fix?"
   User: "Yes, I need it before Oct 30. It's a gift."
   Expect: The deadline and the gift reason are added to the packet and shown to Dana. The bot confirms in one line.
   Failing reply: "Noted!" and the packet is unchanged.

5. **Already verified (R4).**
   Setup: Same company. The bot verified Priya by order number plus email at turn 4. The record is in the packet.
   User: (no message)
   Expect: Dana's first message does not ask for name, email or order number, and her screen shows "verified: order number + email, turn 4".
   Failing reply: "Can you confirm your email and order number so I can pull up your account?"

6. **First message uses the packet (R5).**
   Setup: Same company. Packet and transcript are on Dana's screen. Priya is waiting.
   User: (waiting)
   Expect: "Hi Priya, this is Dana. I see order 48213 arrived cracked and you'd like a replacement by Oct 30. I'm checking stock now."
   Failing reply: "Hi, this is Dana. How can I help you today?"

7. **Redacted card (R6).**
   Setup: Same company. Priya typed a full card number at turn 6. The redaction layer removed it. The last four digits, 1234, were kept in the log.
   User: "I paid with the card ending 1234."
   Expect: The packet shows "card ending 1234 (provided, redacted)". The full number is not in the packet.
   Failing reply: A blank "payment:" field, or the full 16-digit number in the packet.

8. **Transfer fails once (R7).**
   Setup: Same company. The first transfer attempt errors out. A retry works 40 seconds later. The harness shows the packet store.
   User: "Is anyone there?"
   Expect: "Sorry for the wait. I'm reconnecting you, and your details are saved." After the retry, Dana sees the same packet and asks nothing the packet already answers.
   Failing reply: Dana opens a blank record and Priya is asked to explain again.

9. **Promise and mood in the packet (R1).**
   Setup: Same company. The bot said "A replacement ships within 5 days if approved." Priya wrote "This is the second time I'm asking and I need this today."
   User: (no message)
   Expect: The packet lists the promise as "bot said: ships within 5 days if approved" and the mood as "second request, wants it today".
   Failing reply: A packet with neither the promise nor the urgency, so Dana opens with a cheerful script.

10. **Unconfirmed fact (R3).**
   Setup: Same company. Priya said the lamp "came on Tuesday, I think." The bot has no delivery record.
   User: (no message)
   Expect: The bot's summary says "arrived around Tuesday (not confirmed)" and asks "Anything to add or fix?" The packet carries the same mark.
   Failing reply: "Arrived Tuesday Oct 14" shown as a fact.

11. **Customer asks for a person (R8).**
   Setup: Same company. The customer asked for a person at turn 8. A specialist is free. The packet is built.
   User: "I want to talk to a person."
   Expect: The bot connects, shows the one-line summary, asks "Anything to add or fix?", and hands off with the packet. It does not offer another menu first.
   Failing reply: "I can help with that! Here are some topics..." (this is the looped-request pattern; score it there, not here).

12. **Long chat, short packet (R9).**
   Setup: Same company. A 60-turn chat. The harness counts words in the packet and checks for a transcript link.
   User: (no message)
   Expect: A short packet with the goal, key facts, what was tried and a one-click link to the full transcript. Dana can read it in about ten seconds.
   Failing reply: A 500-word recap of every turn with no link to the transcript.

13. **Nothing to pass (R9).**
   Setup: Same company. The customer's only message was "agent". No order, no goal, no history.
   User: "agent"
   Expect: An honest minimal packet: "Customer asked for an agent. No details given yet." The person opens with a question, which is right here. Nothing is invented.
   Failing reply: A packet saying "order issue, probably a refund request".

14. **Customer wants to stay with the bot (R9).**
   Setup: Same company. Priya is in a long chat about a return label. The bot offered a person and she answered no.
   User: "No, just email me the label. I don't need a person."
   Expect: The bot sends the label and does not hand off. No packet is sent.
   Failing reply: "I'm connecting you to a specialist now."

## Cannot be judged from a transcript alone
- **What the person's screen showed before pickup.** It needs the agent tool's event log (packet delivered, first message sent).
- **Re-ask rate after handoff.** It is a rate over a labeled sample of handoffs; one chat cannot give it.
- **Corrections per handoff.** It needs counts across many handoffs, and a sharp drop can mean customers stopped reading the summary.
- **Whether quoted facts appear in the transcript.** It needs the packet and the full transcript side by side.
- **Voice transfers.** Planned. Not tested here.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
