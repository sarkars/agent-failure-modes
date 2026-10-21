# Test File: User-Context Channel Mismatch

This file is a set of chat test conversations for people who build or review text chat assistants and want to check whether theirs offers a fitting channel when the user says something about their situation, such as driving, being deaf, being in a loud place, or being in a meeting.

**Pattern:** [Chatbot Channel Selection by User Context: Offering Text, Voice, or a Callback That Fits](../goals/channel-selection/failures/user-context-channel-mismatch.md)
**Pattern ID:** user-context-channel-mismatch
**Goal:** Each interaction happens in the channel that fits the job, and switching never costs the user their context.
**Primary metric:** Context-aware channel-offer rate: of conversations where the user states a situation cue, the share whose next bot turn offers a fitting channel. Starting target on the pattern page: 90% (a starting point to tune, not a measured benchmark).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, orders, accounts, and people below are invented and labeled fake. Text chat only; voice and web versions are planned on the pattern page and are not tested here. Some items need the cue log or the channel-change log and are marked "Needs the message log" or "Needs a person". The tests do not say how drivers, or Deaf or hard-of-hearing people, behave or what they prefer. They only check whether the bot uses what the user said. This file is test design, not legal or accessibility advice.

The fake product used throughout: "Redline Delivery (fake)" support chat. Channels the product really has: stay in chat, a text message with a link or summary, a callback from a person, a person who messages in the chat, and a relay call (calls placed through a relay service are accepted). Fake customer: Maria Santos (fake), order RD-30581 (fake). Where a test says so, the setup removes channels. Expected options always come from this list.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Log a cue only from the user's own words or actions in this conversation | Every logged cue cites a user turn; nothing is logged from name, location, age, device, or a guess. Needs the message log | A cue logged with no user turn behind it, or a cue taken from the profile |
| R2 | 2. Offer fitting channels in the next bot turn after a cue | The next bot turn has 2-4 channels the product really has, plus "Something else", with free text open. If the cue is unclear, the bot asks one clarifying question first. If the user asks for another channel, that channel is offered with a one-line reason and what carries over | No offer after a clear cue, an offer without "Something else", more than 4 options, or a channel the product does not have |
| R3 | 3. Offer, don't decide | The current channel stays open and the bot changes channel only after the user picks. Needs the channel-change log for the no-switch test | A channel change with no user choice turn, or the chat closed off |
| R4 | 4. Never refer the user only to a channel their cue rules out | The offer has at least one channel that fits the cue | A phone-only referral after "can't hear", or a voice step after "too loud" |
| R5 | 5. Don't name a condition the user didn't name | No bot turn names or asks about a condition the user did not raise; the bot describes the situation ("if that's easier") | "Since you're deaf" when the user never said it, or a question about a disability or health |
| R6 | 6. Remember the choice | The choice holds for the rest of the session; the same offer is not repeated unless the user changes the situation | The same offer shown again with no change in the user's situation |
| R7 | 7. Say so when no channel fits | The bot says no fitting channel exists, says what happens next, and hands off; it never ends on a channel the cue rules out | The conversation ends on a ruled-out channel, or the bot is silent about the gap |
| R8 | Don't over-correct: no channel offers with no cue, no asking everyone about their situation, no removing chat, no lecture; "I've parked" ends the cue | A message with no cue gets a normal answer; no safety lecture; a user who says they are parked or home is not offered channels again | A channel offer with no cue, a question to everyone about their situation, a lecture, or the offer repeated after "I'm parked" |
| R9 | Hand-off rule | A person who accepts text or relay is offered when no fitting channel exists, after two declined offers that did not help, or when the user asks, with what has been said passed on. If no person is available, the bot says when one will be and offers a text callback | No person offered in those cases, or "no one is available" with no time and no text callback |

## Conversations
1. **Cue comes from the user's turn (R1).**
   Setup: Redline Delivery (fake) chat. The profile has only the name Maria Santos (fake) and a ZIP code. Needs the message log.
   User: "hi where is my order RD-30581" / "im driving right now. can u move it to sat"
   Expect: The cue log has one entry, "driving", citing the second user turn. A cue entry that cites the profile or no turn fails.

2. **Profile hints are not a cue (R1).**
   Setup: Same, but the profile shows an older phone model and age 78 (fake). Do nothing special applies. Needs the message log.
   User: "can i change my delivery address for RD-30581"
   Expect: No cue is logged, no channel offer is shown, and the bot helps with the address in chat. A logged cue, or an offer based on the profile, fails.

3. **Driving cue gets an offer (R2).**
   Setup: Same as 1.
   User: "im driving. can I move my delivery to saturday"
   Expect: The next bot turn offers 2-4 real options (for example short answers now, a text with a link for when parked, a callback) plus "Something else". An answer that asks the user to type the order number and date, with no offer, fails.

4. **"I'm deaf" gets an offer (R2).**
   Setup: Same.
   User: "im deaf. can someone help me with a missed delivery"
   Expect: The next bot turn offers options such as staying in chat, a person messaging here, a relay call, plus "Something else". A reply with only a phone number fails.

5. **"In a meeting" gets an offer (R2).**
   Setup: Same.
   User: "cant talk, in a meeting. need to reschedule RD-30581"
   Expect: Options that need no voice (stay in chat, a text summary, a callback later) plus "Something else". A voice-only offer fails.

6. **Unclear cue: one clarifying question (R2).**
   Setup: Same.
   User: "its a bit loud here"
   Expect: One clarifying question, such as "Would a text summary be easier?" A full menu of four channels on a vague line, or silence about it, fails.

7. **User asks for another channel (R2).**
   Setup: Same. The bot is mid-way through a rescheduling task.
   User: "can u just text me this instead"
   Expect: The bot offers the text route, says in one line what carries over (the order and the new date), and waits for the user's pick. An answer that ignores the request and continues in chat fails.

8. **Ordinary chat question after the offer (R3).**
   Setup: The bot has just offered options after "im driving". The user ignores the menu.
   User: "what time is the saturday window"
   Expect: The bot answers in chat. It does not switch the channel or hold back the answer until the user picks. Pushing the user to choose first fails.

9. **No channel change before a choice (R3).**
   Setup: The bot can send a text with a link. The user says "driving" and has not yet picked an option. Needs the channel-change log.
   User: "driving. move my delivery to sat"
   Expect: No text is sent and no channel change is logged until the user picks. A link sent before a choice fails.

10. **Too loud to hear: not only the phone line (R4).**
    Setup: The bot has a phone line and chat.
    User: "i cant hear u its too loud here, is there a number i can call"
    Expect: The offer includes chat or a text summary, not only the phone line. A reply with only the phone number fails.

11. **Can't hear and asks for the phone number (R4).**
    Setup: Same.
    User: "I cant hear on calls. whats the number for claims"
    Expect: The reply includes at least one option that fits (stay in chat, a person messages here, a relay call). Giving the phone number alone fails.

12. **Don't name a condition the user didn't name (R5).**
    Setup: Same. Scan all bot turns after the cue.
    User: "calls are hard for me, can we do this some other way"
    Expect: The bot offers options in plain terms and does not write "since you're deaf" or "do you have a hearing problem". Naming or asking about a condition fails.

13. **The choice is remembered (R6).**
    Setup: The user picked "text me a summary". Needs the message log.
    User: "ok text me" / "also will it come before noon" / "and do i need to be home"
    Expect: The two later questions are answered with no new channel offer. The offer is shown once per cue; a repeat fails.

14. **Do nothing special: "I've parked" ends the cue (R8).**
    Setup: Earlier in the chat the user said they were driving and chose a text summary. Do nothing special applies.
    User: "ok parked now, so can u just tell me the delivery window here"
    Expect: The bot answers in chat with no new channel offer. A repeated offer fails.

15. **No fitting channel exists (R7).**
    Setup: Special setup: this product has no text route, no relay, and no callback. Only a phone line.
    User: "I cant hear on the phone. can someone help with my claim"
    Expect: The bot says no fitting channel is available, says what happens next, and hands off to a person who accepts text. Ending on the phone number alone fails.

16. **Do nothing special: no cue, plain order question (R8).**
    Setup: Same as 1. Do nothing special applies.
    User: "wheres my package RD-30581"
    Expect: A normal answer with the order status. No channel options and no "Something else" menu. An offer fails.

17. **Do nothing special: a bare greeting (R8).**
    Setup: Same. Do nothing special applies.
    User: "hi"
    Expect: A normal greeting and "how can I help". No question about where the user is, whether they are driving, or how they would like to be contacted. Such a question fails.

18. **Do nothing special: no safety lecture (R8).**
    Setup: Same.
    User: "im driving, whats my delivery window"
    Expect: A short answer plus the channel offer from R2. No lecture such as "please pull over" or "never use your phone while driving". A lecture fails.

19. **Two offers declined, neither helped (R9).**
    Setup: The user said "too loud". The bot offered a text summary; the user declined. The bot offered a callback; the user declined.
    User: "no. none of that works" / "just get me a real person"
    Expect: A person who accepts text is offered, and what has been said so far is passed on. A third menu fails.

20. **User asks for a person; none available (R9).**
    Setup: The user cannot talk. No person is staffed right now. The product can send a text callback.
    User: "cant talk right now. get me a person pls"
    Expect: The bot says when a person will be available and offers a text callback. "No one is available" with no time and no text callback fails.

## Cannot be judged from a transcript alone
- **The cue log (R1, R6).** Needs the message log: each logged cue, the user turn behind it, and whether any offer was shown.
- **Channel changes (R3).** Need the channel-change log to confirm none happened before a user choice.
- **Channels the product really has (R2).** A person must check each offered option against the product's channel list.
- **Primary metric.** These tests do not measure the context-aware channel-offer rate. Use the metrics on the pattern page.
- **Law and standards.** These tests make no claim about what applies to any company. Have a qualified reviewer check any flow before relying on it.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
