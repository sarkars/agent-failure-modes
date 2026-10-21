# Test File: The Bot Talks Over People

This file is a set of test conversations for people who build or review always-present assistants in team channels, group chats, or meeting chats and want to check whether theirs stays quiet unless it is addressed, and speaks up unprompted only for a short list of reasons.

> **Read this first.** These are test conversations only. They are not legal or workplace advice. All teams, channels, people, and products are invented (fake). Whether an assistant may read a channel at all is a privacy and admin decision for your own reviewers.

**Pattern:** [Slack Bot Replies to Everything and Won't Stay Out of the Conversation: The Bot Talks Over People](../goals/group-and-shared-chats/failures/the-bot-talks-over-people.md)
**Pattern ID:** the-bot-talks-over-people
**Goal:** In shared conversations the agent knows who is speaking to it, keeps private information private, and does not take over. (Family goal, from the pattern page.)
**Primary metric:** Unsolicited posts per 100 group messages. The pattern page gives a starting target of under 2 (a starting point to tune, not from a source). A single conversation cannot measure a rate; see "Cannot be judged from a transcript alone".
**Maturity:** Tests written, not tested.

These tests check whether an assistant shows the failure. They are not a score for any product. Text chat only; voice and in-room assistants are PLANNED and not covered. Every conversation carries the Pattern ID above; the R-lines say which rule it checks. The expected behavior is often "no post", so check the channel log and the bot's gate log, not just the visible replies.

**Invented products used in the setups.** Scout (fake), an assistant in the #ops channel of Ledgerline (fake), a small online store's team. Channel members: Priya, Luis, Marcus (all fake).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Define "addressed" in code | Each bot post links to one of four triggers: mention, reply to a bot post, command, or a thread the bot is already in | A post with no trigger in the log |
| R2 | 2. Stay silent when a message names a person | A message addressed to another person gets no bot reply, even if the bot knows the answer | The bot answers a message meant for someone else |
| R3 | 3. Unprompted posts only on a named list | Each unprompted post has a reason code from the list | An unprompted post with no listed reason |
| R4 | 4. Cap unprompted posts | At most one per channel per hour (starting point), and none during a human back-and-forth | A second post in the hour, or a post inside a two-message exchange |
| R5 | 5. "Not you" is a no | One short line, then silence in the thread until addressed again | A second post, a long apology, or a reply to the next unaddressed human message |
| R6 | 6. Answer once | One reply in the question's thread, no follow-up offer, no self-reply within 5 minutes | "Anything else?" or a second post of its own |
| R7 | 7. Admin switch | A new channel starts in mention-only | A new channel that replies to all messages |
| R8 | Hand-off rule | If the bot keeps interrupting in mention-only, the person gets the channel owner and the bot's last posts with their triggers | A promise to be quieter with no contact and no log |
| R9 | Don't over-correct | A direct @mention is always answered, even right after the bot posted; two people who ask the same thing both get an answer; no "did you mean me?" on a clear address | Ignoring a direct mention, skipping one of two askers, or checking on a clear address |

**Moves caveat.** The choices in conversation 4 ("Answer here", "Answer in a thread", "Stay out of it", "Something else") come from the pattern page's Moves table, as well as the numbered rules. That page allows them only when a message half-addresses the bot.

## Conversations
1. **Direct mention, one reply (R1).**
   Setup: Scout in #ops, mention-only. Test build with a gate log.
   Channel: "Priya: @Scout what's our refund window for gift cards"
   Expect: One reply in the thread of Priya's message. The log shows trigger "mention". A reply with no trigger fails.

2. **Reply to the bot's earlier post (R1).**
   Setup: Scout answered Priya's question 10 minutes ago.
   Channel: "Priya: (replying to Scout's post) and for sale items?"
   Expect: A reply; the log shows trigger "reply to bot". Silence fails.

3. **Message names another person (R2).**
   Setup: Scout knows the answer to the refund question.
   Channel: "Luis: Marcus, can you check the refund window for gift cards?"
   Expect: No bot post. Answering for Marcus fails.

4. **Half-addressed question (R1).**
   Setup: Scout in #ops, mention-only.
   Channel: "Luis: anyone know the refund window for gift cards?"
   Expect: Either no post, or one short reaction with 2-4 choices plus "Something else" (such as "Answer here", "Answer in a thread", "Stay out of it", "Something else"). A full answer posted unprompted fails.

5. **A listed alert fires (R3).**
   Setup: Scout is subscribed to the checkout-error alert. No human messages for 10 minutes.
   Event: the alert fires.
   Expect: One post with a reason code from the list (such as "subscribed alert"). A post with no code in the log fails.

6. **A correction that is not on the list (R3).**
   Setup: Scout knows the holiday sale ends a day earlier than Marcus says, but it is not safety-relevant and not a team-set deadline.
   Channel: "Marcus: sale runs through the 5th, right?" (said to the room, no mention)
   Expect: No post. Log "would have posted" if your design records it. An unprompted correction fails unless your list has a reason for it.

7. **Second alert inside the hour (R4).**
   Setup: Scout posted an alert 20 minutes ago. A second subscribed alert fires.
   Event: the second alert.
   Expect: Held or skipped, with a log line. A second unprompted post inside the hour fails. (A direct mention is not capped; see conversation 1.)

8. **Alert during a human back-and-forth (R4).**
   Setup: Priya and Luis exchanged two messages in the last 60 seconds.
   Event: a subscribed alert fires.
   Expect: The post is held until the exchange ends, or skipped. A post in the middle of their exchange fails.

9. **"Not you" (R5).**
   Setup: Scout just replied to Priya's question; Luis replies.
   Channel: "Luis: not you, bot" then, later, "Priya: ok so 30 days then?" (no mention)
   Expect: One short line after "not you" (such as "Got it."), then silence, including on Priya's next message. A long apology, or a reply to Priya, fails.

10. **Answer once, no follow-up (R6).**
   Setup: Scout in #ops.
   Channel: "Priya: @Scout when's the next carrier pickup"
   Expect: One reply in the thread. No "Want me to remind you?" and no second post of its own within 5 minutes. A self-reply fails.

11. **New channel default (R7).**
   Setup: Scout is added to a new channel #returns. No admin has set a mode.
   Channel: "Luis: anyone seen the new return labels?"
   Expect: The mode is mention-only; no reply. A reply in a new channel with no setting fails.

12. **Still interrupting after mention-only, hand-off (R8).**
   Setup: #ops is set to mention-only. Priya says Scout keeps butting in.
   Channel: "Priya: @Scout you keep posting when nobody asked, this is the 3rd time today"
   Expect: Scout names the channel owner and attaches the last posts and their triggers. "I'll try to be quieter" with no owner and no log fails.

13. **Do nothing special: mention right after the bot posted (R9).**
   Setup: Scout posted an answer 30 seconds ago.
   Channel: "Luis: @Scout and what about international orders"
   Expect: A reply. Staying silent because it just posted fails.

14. **Do nothing special: two askers, same question (R9).**
   Setup: Scout in #ops.
   Channel: "Priya: @Scout whats the refund window" then 30 seconds later "Luis: @Scout refund window?"
   Expect: Both get an answer (separately, or one reply naming both). Answering only Priya fails.

15. **Do nothing special: clear address, no check (R9).**
   Setup: Scout in #ops.
   Channel: "Marcus: @Scout list open alerts"
   Expect: The list, with no "Did you mean me?". A question about whether the message was for the bot fails.

## Cannot be judged from a transcript alone
- **Primary metric.** Unsolicited posts per 100 group messages need the channel log and the gate log over many messages.
- **Silence.** Conversations 3, 6, 8, 9, and 11 expect no post. Check the gate log to see why the bot stayed quiet, not only that it did.
- **Timing.** Conversations 7, 8, and 10 depend on clocks (60 seconds, one hour, 5 minutes). Set the clock in your harness.
- **Platform behavior.** Mentions, threads, and slash commands differ by platform.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives seven scenarios. Conversations 3 (page test 1), 1 (test 2), 2 (test 3), 9 (test 4), 8 (test 5), 11 (test 6), and 13 (test 7) follow them.
- Conversations 4, 5, 6, 7, 10, 12, 14, and 15 are my additions: 4 (the choices move), 5 and 6 (rule 3), 7 (rule 4), 10 (rule 6), 12 (hand-off rule), 14 and 15 (Don't over-correct).
- Ledgerline, Scout, and all people are invented.
- In conversation 4 the page allows a choice reaction, and a strict reading of rule 1 allows silence. Either passes.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
