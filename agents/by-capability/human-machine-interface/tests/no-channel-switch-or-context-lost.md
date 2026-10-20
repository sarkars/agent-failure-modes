# Test File: No Channel Switch, or Context Lost in It

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs always offers a way to another channel or a person, and passes a short summary so the user never repeats themselves.

**Pattern:** [Chatbot Handoff Loses Context: Customers Repeat Themselves After a Switch](../goals/channel-selection/failures/no-channel-switch-or-context-lost.md)
**Pattern ID:** no-channel-switch-or-context-lost
**Goal:** Each interaction happens in the channel that fits the job, and switching never costs the user their context.
**Primary metric:** Re-ask rate after handoff: questions from the next agent or bot that the handoff packet already answered. Starting target on the pattern page: under 5% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, accounts, and people are invented and labeled fake. Phone numbers use the 555 range. Text chat only: where a test involves a phone call, it checks the chat side of the switch (the offer, the consent, the summary, the packet). Voice-side checks are PLANNED only (see the end of this file). Each setup says what the bot can hand off to and whether the harness can read the handoff record (packet, consent flag, delivery acknowledgement). Tests that judge the packet or the next agent's first message need that record; a chat transcript alone is not enough.

The packet fields come from the pattern page's reference design: `user`, `goal`, `established`, `tried`, `sentiment`, `next_action`, `channel_preference`, `transcript_ref`.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Always provide a path to another channel or a person, and say when it will happen | The bot offers a way to a person or another channel and states when it will happen | "I can't help with that" with no path, a bare phone number with no context, or a path with no time |
| R2 | 2. Send a handoff packet every time | The packet holds user, goal, what's established, what's been tried, emotional state, and next action, with a transcript link | No packet, or a packet missing a required field |
| R3 | 3. Say what's happening in plain words | The reply says why it is switching, who is next, and how long it will take | A switch with no reason, no named next person or team, or no time |
| R4 | 4. Ban re-asking | The next agent or bot asks only for what the packet is missing | The next agent asks for the goal, name, or what was tried when the packet has it |
| R5 | 5. Confirm before you leave | The bot shows the summary, asks "Is this right?", and a correction lands in the packet before the transfer | No chance to check the summary, or the packet still carries the old fact |
| R6 | Don't over-correct | Short summary with the transcript linked; no switch without consent; no handoff for things the bot can safely solve; no channel choices when the user said to stay in chat | The whole transcript pasted as the summary, a switch the user did not agree to, or a handoff for a request the bot could finish |
| R7 | Hand-off rule: if the packet can't be delivered | The bot says the handoff did not go through and gives a reference to quote | A silent failure, or "you're all set" when no acknowledgement came back |

## Conversations
1. **Packet on escalation (R2).**
   Setup: Fake bank Pinecrest Federal Credit Union (fake) bot. It can hand off to a billing team in chat. The bot verified the user, Marcus (fake), and confirmed a duplicate $42.10 charge from Oct 14 on his statement. It cannot reverse charges. Harness reads the handoff record.
   User: "ok so u cant reverse it. what now"
   Expect: The packet carries user, goal ("reverse duplicate $42.10 charge from Oct 14"), established (duplicate on statement, user verified), tried (bot could not reverse), sentiment, next action, and a transcript link. A handoff with only a case ID fails.

2. **Say why, who, and how long (R3).**
   Setup: Same as 1. The billing team's posted wait in chat is about 10 minutes.
   User: "ok so u cant reverse it. what now"
   Expect: The reply says why ("reversing a charge needs a billing specialist"), who is next (the billing team), and when (about 10 minutes, here in chat). "Transferring you now." with nothing else fails. (Separate from 1: this checks the words the user sees, not the packet.)

3. **No dead end (R1).**
   Setup: Fake internet provider Harborline Broadband (fake) bot. It cannot change the billing address on a business account. Business support takes chat handoffs and callbacks.
   User: "need to change billing address on my business acct"
   Expect: Says it can't do this itself, offers a way to business support, and says when that happens. "I'm not able to help with that. Please call 1-800-555-0142." with no time and no summary fails.

4. **Say when, outside hours (R1).**
   Setup: Same as 3. It is 9:40 PM ET. Business support chat is staffed 8 AM to 8 PM ET. The bot can queue a chat handoff for the morning.
   User: "is anyone there who can do this"
   Expect: Says no one is available now, says when someone will be (after 8 AM ET), and offers to queue it with the summary. "An agent will be with you shortly" fails.

5. **Show the summary and ask (R5).**
   Setup: Same as 1, just before the transfer.
   User: "yes please get me someone"
   Expect: The bot shows a short summary of what it will pass and asks "Is this right?" (or similar) before transferring. A transfer with no summary shown fails.

6. **User corrects the summary (R5).**
   Setup: Same as 5. The bot's summary said the charge was on Oct 14.
   User: "no it was the 12th not the 14th"
   Expect: The bot accepts the fix in one reply, and the packet shows Oct 12 before the transfer. A packet that still says Oct 14 fails. Harness reads the handoff record.

7. **Next agent starts from the packet (R4).**
   Setup: Same as 1, after the handoff. A test agent or bot on the billing team receives the packet. Harness reads the receiving side's first message.
   User: (no message yet)
   Expect: The first message names the charge and the date and moves to the next action. "Hi, can I get your name and what the issue is?" fails.

8. **Ask only what is missing (R4).**
   Setup: Same as 7, but the packet has no field for whether Marcus wants the money back to his checking or savings account.
   User: "hi"
   Expect: The receiving agent asks only which account the refund should go to. Re-asking the charge amount or what the bot tried fails. A check-back such as "I see a duplicate $42.10 charge from Oct 12. Is this right?" is not a re-ask.

9. **User asks for a call (R1, R3).**
   Setup: Fake insurer Cedar Mutual (fake) bot, mid-chat about a denied windshield claim. It can book a callback and pass the summary. Callback slots exist today at 2:00 PM and 3:30 PM ET.
   User: "can someone just call me about this"
   Expect: Offers a callback time, says the caller will already have the summary, and says who will call. "Please call our claims line" with no time and no summary fails. (Chat side only; what the caller says is PLANNED.)

10. **Packet fails to deliver (R7).**
    Setup: Same as 1. The harness makes the handoff service return no delivery acknowledgement.
    User: "ok send me to billing"
    Expect: Says the transfer did not go through and gives a reference the user can quote (for example the conversation ID). "You're all set, someone will be right with you" fails.

11. **Long chat, short summary (R6).**
    Setup: Fake software company Lumen Ledger (fake) bot. A 50-turn chat about a sync error. It hands off to tier-2 support.
    User: "fine escalate it"
    Expect: A short packet with the full transcript linked through `transcript_ref`. The whole transcript pasted into the summary field fails.

12. **Ask before switching channels (R6).**
    Setup: Same as 9. The bot decides a call would fit better. The user has not asked for one.
    User: "the denial letter says glass isnt covered but my policy says it is"
    Expect: Offers the switch and waits for a yes before booking a call, and the packet carries the consent flag. "A claims rep will call you in 15 minutes" with no question fails.

13. **Offer choices when a switch is needed (R1).**
    Setup: Same as 3. Chat handoff and callback are both available.
    User: "ok how do i get this done"
    Expect: Offers 2 to 4 options plus "Something else" (for example "Message me here", "Call me", "Keep going in chat", "Something else") and leaves free text open. Picking a channel for the user fails.

14. **Do nothing special: the bot can solve it (R6).**
    Setup: Fake retailer Brightwood Outfitters (fake) bot. It can look up tracking. Order 51907 (fake) shipped yesterday and has a tracking number.
    User: "wheres my order 51907"
    Expect: Gives the tracking status and stops. Offering a person or a call, or starting a handoff, fails.

15. **Do nothing special: user wants to stay in chat (R6).**
    Setup: Same as 3. The bot can walk the user through the address change form on the website.
    User: "i dont want to call anyone, just tell me the steps here"
    Expect: Gives the steps in chat. Offering "Call me" or handing off fails.

16. **Mood travels in the packet (R2).**
    Setup: Same as 1. Earlier, Marcus wrote "this is the second time this month, im really annoyed".
    User: "just get me a person"
    Expect: The packet's `sentiment` field reflects that he is frustrated. A packet with no sentiment, or "neutral", fails.

## Notes
- Conversation 4 rests on my reading of rule 1 ("say when it will happen"). The page does not mention staffed hours; I wrote the after-hours case from that rule.
- Conversation 8 rests on my reading of rule 4 and the first detection signal's counter-signal. The page allows asking for what the packet is missing and treats "Is this right?" as a confirmation, not a re-ask; the checking-or-savings field is my example.
- Conversation 13 rests on the Moves table and the Guide spec `choices`, not on a numbered rule. I mapped it to R1 because the move applies when the bot needs to offer a path.
- Conversation 15 rests on the Moves table ("when the user has said they want to stay in chat") and the Don't over-correct line on consent, which I combined into R6.
- Conversations 1 and 2 are split because rule 2 (the packet) and rule 3 (the words to the user) can fail separately. The same goes for 5 and 6 (showing the summary versus applying a correction).

## Cannot be judged from a transcript alone
- **Packet contents and completeness.** R2, conversation 6, and conversation 16 need the handoff record, not the chat.
- **Delivery and consent.** R7 needs the delivery acknowledgement; conversation 12 needs the consent flag in the packet.
- **The receiving side.** R4 needs the next agent's or bot's first message, which may live in a separate system.
- **Re-ask rate.** A rate over many handoffs; these tests show single cases.

## PLANNED (voice and web, not written as tests)
- **Voice:** after a chat-to-call switch or a warm transfer, check that the next agent's spoken summary matches the packet, and that they do not ask on the call for anything the packet holds.
- **Web:** check packets that drive a shared-screen or co-browse session.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
