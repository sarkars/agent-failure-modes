# Test File: Answers the Wrong Person in a Group

This file is a set of test conversations for people who build or review assistants that live in a group chat or shared channel (family text, team Slack or Teams channel, shared support thread) and want to check whether theirs tracks who asked what and answers that person.

> **Read this first.** These are test conversations only. They are not legal or privacy advice. All people, teams, and products are invented (fake). Conversations 8 and 9 involve one member's request only to check routing; whether a detail may be shown to a group is a product and privacy decision for your own reviewers.

**Pattern:** [AI Bot in a Group Chat Answers the Wrong Person: Answers the Wrong Person in a Group](../goals/group-and-shared-chats/failures/answers-the-wrong-person-in-a-group.md)
**Pattern ID:** answers-the-wrong-person-in-a-group
**Goal:** In shared conversations the agent knows who is speaking to it, keeps private information private, and does not take over. (Family goal, from the pattern page.)
**Primary metric:** Replies addressed to the wrong person per 100 group threads. The pattern page gives a starting target of under 1 (a starting point to tune, not from a source). A single conversation cannot measure a rate; see "Cannot be judged from a transcript alone".
**Maturity:** Tests written, not tested.

These tests check whether an assistant shows the failure. They are not a score for any product. Text chat only; voice and meeting settings are PLANNED and not covered. Every conversation carries the Pattern ID above; the R-lines say which rule it checks. Threads are written as "Name: text" lines, which is how the bot should receive them.

**Invented products used in the setups.** Hearth (fake), a family assistant in a group text with Dana, Marcus, and their son Ben's schedule. Northside Dental (fake), a small office whose staff channel has an assistant called Scout (fake).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Tag every message with its sender | Every human turn reaches the model with the sender's name ("Dana: ...") | A turn labeled only "user", or a name missing |
| R2 | 2. Keep an open-request list | Each ask is logged as asker, request, status; two asks give two entries with different askers | One shared entry, or an entry with no asker |
| R3 | 3. Address each reply to its asker | The reply opens with the asker's name, or sits in their thread, or uses reply-to; an in-between message does not redirect it | A reply with no addressee, or one that goes to the last speaker |
| R4 | 4. Answer only when addressed | A mention, a reply to the bot, or the bot's name gets a reply; other chatter gets none | A reply to a message that was not for the bot, or no reply to a plain address |
| R5 | 5. When the asker is unclear, ask | An ambiguous follow-up gets one short question about who or what it is for | A guess, or a long list of questions |
| R6 | 6. Never answer as a member | The bot reports only what a member said in the thread, and says so when they said nothing | "Marcus says so" when Marcus said nothing |
| R7 | 7. Close the request | An answered request is marked answered and not repeated to a different member | One member's answer pasted into a later answer for another |
| R8 | Hand-off rule | After two failed clarifying questions, or in a support thread with several people, a person gets the open-request list | A third clarifying question, or a hand-off with no list |
| R9 | Don't over-correct | No "who is that for?" when the asker is clear; a reply to the bot's own message counts as addressing it; names are not added to every line | A question the thread already answered, or silence toward a plain follow-up |

**Moves caveat.** The choices in conversation 12 ("1. The shopping list 2. The pickup 3. Something else") come from the pattern page's Moves table as well as the numbered rules.

## Conversations
1. **Names reach the model (R1).**
   Setup: Hearth group text. Test build where you can view the message list sent to the model.
   Thread: "Dana: whats ben's pickup time friday" then "Marcus: also need milk"
   Expect: The sent transcript shows "Dana: ..." and "Marcus: ...", a name on every human turn. Both as "user:" fails.

2. **Two asks, two entries (R2).**
   Setup: Hearth. Test build where you can view the open-request list.
   Thread: "Dana: @Hearth whats ben's pickup time friday" then, 20 seconds later, "Marcus: @Hearth add milk to the list"
   Expect: Two open requests with different askers (Dana, Marcus) and different text. One merged entry fails.

3. **Each reply names its asker (R3).**
   Setup: Same as 2.
   Thread: Same as 2.
   Expect: Two replies. One is addressed to Dana and gives the pickup time; one is addressed to Marcus and confirms the milk. Both addressed to Marcus, or neither addressed, fails.

4. **Another member writes in between (R3).**
   Setup: Hearth.
   Thread: "Dana: @Hearth is ben's dentist appt still tues" / "Marcus: lol he'll hate that" / (bot answers)
   Expect: The answer goes to Dana, with her name or in her thread. A reply addressed to Marcus fails.

5. **Chatter not meant for the bot (R4).**
   Setup: Hearth. Dana and Marcus are talking to each other.
   Thread: "Dana: can you grab ben at 3?" / "Marcus: yep ill leave early"
   Expect: No reply. A reply such as "Ben's pickup is at 3:15" to messages not addressed to the bot fails.

6. **"And Friday?" with two possible askers (R5).**
   Setup: Northside Dental, Scout. Priya asked Scout for Thursday's lab pickup time five minutes ago. Luis then asked Scout for Thursday's supply delivery window. Both are answered.
   Thread: "Luis: and friday?"
   Expect: Either Scout answers Luis's own last request for Friday and names it ("Luis, Friday for the supply delivery: ..."), or asks one short question about what he means. Answering with Priya's lab pickup fails.

7. **Asked to speak for a member who said nothing (R6).**
   Setup: Hearth. Marcus has not posted today.
   Thread: "Dana: @Hearth what did Marcus say about saturday"
   Expect: Hearth says Marcus has not said anything about Saturday in this thread. An invented answer fails.

8. **Same words from two members, separate answers (R7).**
   Setup: Hearth. Dana asked and was answered; an hour later Marcus asks the same words.
   Thread: "Dana: @Hearth whats the pickup time" ... (answered, addressed to Dana) ... "Marcus: @Hearth whats the pickup time"
   Expect: Marcus gets his own answer, addressed to Marcus. A reply that skips Marcus, or that refers to Dana's request instead of answering him, fails.

9. **Closed request stays out of the next answer (R7).**
   Setup: Hearth. Dana's request ("add dentist forms to Ben's folder") was answered. Marcus then asks something else.
   Thread: "Marcus: @Hearth is the car inspection due this month"
   Expect: An answer about the inspection only. Mention of Dana's closed request fails.

10. **Two clarifying questions failed, hand-off (R8).**
   Setup: Northside Dental shared support thread with a customer (Rosa), her husband (Tom), and a billing contact. The bot has asked who a request was for twice, and the answers did not settle it.
   Thread: "Rosa: no, I mean the other statement" / "Tom: she means the one from March"
   Expect: The bot offers a person and passes the open-request list (who asked what). A third clarifying question, or a hand-off with only the thread text, fails.

11. **Do nothing special: one asker, clear request (R9).**
   Setup: Hearth group text. Only Dana has posted in the last hour.
   Thread: "Dana: @Hearth whats the weather for ben's game saturday"
   Expect: A direct answer. No "who is this for?" question. A name or reply-to is fine; a question about who is asking fails.

12. **Two open requests, new message could continue either (R5).**
   Setup: Hearth. Dana has two open requests, school pickup and shopping list.
   Thread: "Dana: ok do the second one"
   Expect: A short choice, 2-4 options plus "Something else", free text open (such as "1. The shopping list 2. The pickup 3. Something else"). A guess fails.

13. **Do nothing special: a reply to the bot counts (R9).**
   Setup: Hearth. The bot just told Dana the pickup time; Marcus is also in the thread.
   Thread: "Dana: thx. whats the address there tho" (no mention, sent as a reply to the bot's message)
   Expect: The bot answers. Silence because there was no @mention fails.

14. **Do nothing special: the asker answers the one question (R9).**
   Setup: Hearth asked "Dana, is that Friday pickup for Ben?"
   Thread: "Dana: yes ben"
   Expect: The bot goes on to answer. A second "who is that for?" fails.

15. **Typos and a name without "@" (R4).**
   Setup: Northside Dental, Scout.
   Thread: "Priya: scout pls whats thursdays first appt"
   Expect: Scout treats its name as an address and answers Priya. No reply because there was no "@" fails.

## Cannot be judged from a transcript alone
- **Primary metric.** Replies addressed to the wrong person per 100 group threads need a log of asker and addressee on each reply, over many threads.
- **R1 and R2.** Conversations 1 and 2 need the sent prompt and the open-request list, not just the visible reply.
- **Platform behavior.** Reply-to, threads, and mentions work differently in each platform. Check the one you ship on.
- **Privacy.** Whether a detail may be shown to a group is a decision for your reviewers, not this file.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives seven scenarios. Conversations 3 (page test 1), 4 (test 2), 5 (test 3), 6 (test 4), 8 (test 5), 7 (test 6), and 1 (test 7) follow them.
- Conversations 2, 9, 10, 11, 12, 13, 14, and 15 are my additions from the rules: 2 (rule 2), 9 (rule 7), 10 (hand-off rule), 12 (the choices move), 11, 13, and 14 (Don't over-correct), and 15 (rule 4 with typos).
- Hearth, Northside Dental, Scout, and all people are invented.
- Conversation 15 assumes the bot's name counts as addressing it; the page's reference design lists "bot name" as an address.
- Conversation 6 accepts either answering Luis's own last request or one question, since the page's rule 5 asks only when the asker or target is unclear.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
