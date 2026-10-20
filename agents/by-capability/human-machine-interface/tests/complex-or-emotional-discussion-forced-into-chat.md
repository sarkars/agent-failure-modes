# Test File: Complex or Emotional Discussion Forced Into Chat

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs notices a conversation has outgrown chat and offers one specific switch, without pushing it.

**Pattern:** [Complex Conversations in Chatbots: When Chat Is the Wrong Channel](../goals/channel-selection/failures/complex-or-emotional-discussion-forced-into-chat.md)
**Pattern ID:** complex-or-emotional-discussion-forced-into-chat
**Goal:** Each interaction happens in the channel that fits the job, and switching never costs the user their context.
**Primary metric:** Detection recall of conversations that have outgrown chat. Starting target on the pattern page: over 85% (tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies and people are invented and labeled fake. Text chat only. Each setup says what switches the bot can offer. The pattern page gives "about 6 to 8 turns" with no progress as a starting value to tune; test 4 uses the value your product has set, and you record it in your results. The detection signals and Guide spec on the pattern page (section 7) are proposed, not calibrated.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Watch for complexity triggers | A trigger (3+ distinct issues, confusion signals, no progress, high stakes with strong emotion) leads to a summary and a switch offer within two turns | The bot keeps answering one message at a time |
| R2 | 2. Summarize first in three bullets | The offer comes with a short summary of the pieces, three bullets | No summary, or a wall of text |
| R3 | 3. Offer one switch with a reason and a time | One switch (call, screen-share, visual, or human), a reason, and specific times | A menu of five, or "want to talk to someone?" with no reason or time |
| R4 | 4. Respect preference | A user who prefers chat keeps the chat and is supported there | The bot pushes the switch again or refuses to continue |
| R5 | 5. Cap answer length while the trigger is active | Short answers and one next step | Policy dumps of hundreds of words |
| R6 | Hand-off rule | The hand-off carries the three-bullet summary, the goal, and what was tried | The person has to ask everything again |
| R7 | Don't over-correct | No switch for healthy long chats; no hand-off before trying to help; no second offer after a decline | Escalating every long chat, or re-offering after a decline |

## Conversations
1. **Three issues, summary (R1, R2).**
   Setup: Fake insurer Northfield Mutual (fake) bot. It can book calls with a claims specialist. Customer has one denied claim and one open claim from March (fake).
   User: "My claim was denied but I think they counted my deductible wrong, and theres a second claim from March thats still open, and i dont know which one this is about"
   Expect: Within two turns, the bot names the pieces in three bullets (denied claim, deductible, open March claim). A single long policy explanation as the only reply fails.

2. **One switch, reason and time (R3).**
   Setup: Same as 1.
   User: (same message as 1)
   Expect: Offers one call with a reason and two specific times (for example "2:30 or 4:00 today"), plus "keep going in chat". A list of five contact options, or "would you like to speak to someone" with no time, fails.

3. **Repeated confusion (R1, R5).**
   Setup: Same as 1. The bot has already given one long answer about deductibles.
   User turn 1: "i dont get it"
   User turn 2: "no i still dont get it. which claim are you talking about"
   Expect: By the second "I don't get it", the bot shortens its answer, restates it simply, and offers a switch. A third long restatement fails.

4. **No progress after many turns (R1).**
   Setup: Same as 1. Harness inserts a scripted thread of N turns with no open question closed, where N is the product's own setting (page start value: 6 to 8). Record N.
   User: "ok so what do i do now"
   Expect: The bot offers the switch with a summary. Carrying on with another answer and no offer fails.

5. **High stakes and strong emotion (R1).**
   Setup: Fake bank Pinecrest Bank (fake) bot. It can hand off to a person.
   User: "my husband died last month and the bank froze his account and i cant pay the funeral home. i dont know what to do"
   Expect: A short, kind reply, a summary, and a hand-off offer to a person who can act. A policy dump on account freezes, or no mention of a person, fails.

6. **User prefers chat (R4).**
   Setup: Same as 1. The user has been offered a call.
   User: "i cant do calls, im deaf. chat only please"
   Expect: Keeps the chat, does not offer a phone call again, and supports the user in chat. Offering a call again, or going quiet, fails.

7. **Declined switch, no re-offer (R7).**
   Setup: Same as 1. The call was offered once.
   User: "no thanks, lets just keep going here"
   Expect: Continues in chat with shorter answers and does not offer the call again. Any second offer fails.

8. **Short answer while trigger is active (R5).**
   Setup: Same as 7, after the decline.
   User: "so is the deductible thing even right"
   Expect: A short answer and one next step. Several hundred words quoting policy sections fails.

9. **Hand-off content (R6).**
   Setup: Same as 1. The user accepted the 2:30 call.
   User: "2:30 works"
   Expect: Confirms the time and passes the summary, the goal, and what was tried to the specialist. A hand-off without these fields fails. Whether the person received them needs the hand-off payload, not the transcript.

10. **One clarifying question (R1).**
    Setup: Same as 1. The user sent only: "why was it denied and what about the other one".
    User: "why was it denied and what about the other one"
    Expect: Asks which claim the user means, once, because the answer changes the summary. Guessing at a claim, or a long answer about both, fails.

11. **Do nothing special: long chat, steady progress (R7).**
    Setup: Same as 1. Harness shows 12 turns on a single claim; each turn closes a question (the user is filling in a claim form).
    User: "ok whats the next field"
    Expect: Answers the next field. A switch offer fails.

12. **Do nothing special: one issue in several messages (R7).**
    Setup: Same as 1.
    User turn 1: "my claim was denied"
    User turn 2: "its the one for the car repair"
    User turn 3: "the shop charged 900"
    Expect: Treats it as one issue and helps. A complexity summary or a switch offer fails.

13. **Do nothing special: simple question (R7).**
    Setup: Same as 1.
    User: "whats your phone number"
    Expect: Gives the number or the channel. A summary, a clarifying question, or a hand-off fails.

## Notes
- Conversations 2 and 1 are separate because the page gives separate rules for the summary and the offer.
- Conversation 10 rests on my reading of the page's "Ask one clarifying question" move; it is not a numbered fix rule.
- Conversation 13 rests on my reading of "Don't escalate every long chat" applied to a short chat.
- I wrote no test for the trigger "conflicting information that needs both sides to talk it through" because the page gives no example of it.

## Cannot be judged from a transcript alone
- **Detection recall and false-trigger rate.** These need the labeled stuck-conversation and healthy-chat sets on the pattern page.
- **Context carried over in a switch (R6).** Needs the hand-off payload.
- **Whether a booking exists.** Needs the booking system, not the chat.
- **The turn count that counts as no progress.** The page says to tune it; record your value.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
