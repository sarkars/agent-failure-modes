# Test File: Answer-and-Go Conversation

This file is a set of chat test conversations for people who build or review assistants and want to check whether theirs answers the question and then goes quiet, or never confirms the problem is solved.

**Pattern:** [Chatbot Answers, Then Stops: The Answer-and-Go Conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md)
**Pattern ID:** answer-and-go-conversation
**Goal:** Every conversation moves the user toward what they are trying to do and ends with confirmation that it worked.
**Primary metric:** Confirmed-resolution rate. Starting target on the pattern page: gap to containment rate under 10 points (tune).
**Maturity:** Tests written; not yet run. Needs review.

These tests check whether an assistant shows the failure. They are not a score for any product. All stores, products, and people are invented (fake). Text chat only. A forward move is one question, one next-step offer, or one verification check. Count questions in each bot reply.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Track a goal and a stage | The forward move fits the goal the user stated earlier and the stage they are at | A generic or off-goal move, or the goal is forgotten |
| R2 | 2. Answer first, then advance | The answer comes first, in full; the forward move follows it | The answer is held back for a question |
| R3 | 3. Exactly one forward move per turn | One move on a non-final turn, never more than one question | No move at all, or two questions |
| R4 | 4. Close the loop explicitly | When the goal looks met: a summary of what was done, a request to confirm it worked, what happens next, how to come back | "Anything else?" alone, or the session just ends |
| R5 | 5. Know when to stop | No forward move when the user is done, hurried, upset, or has declined two prompts | A move anyway |
| R6 | Hand-off rule | Out of scope, 3 turns with no progress, or the user asks: a handoff with the conversation summary attached | The conversation ends, or the user must repeat everything |
| R7 | Don't over-correct | High stakes: the move is a safe next step or a person, never a sales prompt; no filler tag-on that ignores the user's goal | An upsell in a high-stakes thread, or a generic "Want me to explain more?" on every reply |

## Conversations
1. **Informational question, one forward move (R2, R3).**
   Setup: Fake furniture store Harbor Home (fake). Goal not yet known. Delivery to Austin takes 3-5 business days.
   User: "Do you ship to Austin?"
   Expect: "Yes, usually 3-5 business days" first, then one question (for example, home or office). A bare answer fails.

2. **Answer held back (R2).**
   Setup: Same store. Returns are accepted within 30 days (fake).
   User: "whats the return window"
   Expect: The 30 days in the first sentence. Asking "which item?" before giving it fails.

3. **Two questions (R3).**
   Setup: Same store. User is exploring sofas for a living room.
   User: "do you have gray sofas"
   Expect: Answer, then one question. "Is it for a small room, and what is your budget?" fails.

4. **Move tied to the stated goal (R1).**
   Setup: Same store. Earlier in the chat the user said the old sofa has gone saggy and they want a firmer seat. Goal: buy. Stage: comparing.
   User: "what's the price on the Alder"
   Expect: The price, then a move that narrows the choice and uses the firm-seat goal. A question about unrelated products or a newsletter pitch fails.

5. **Verify the fix (R4).**
   Setup: Fake banking app Cedar Pay (fake). The bot just walked the user through reinstalling the app. Goal: fix. Stage: post-action.
   User: "ok did that"
   Expect: A verification move, such as "Try it now: does the app load?" Silence or a bare "Great!" fails.

6. **Close, not "anything else" (R4).**
   Setup: Same app. The bot submitted an unrestriction request that a specialist reviews within 4 hours, with a text message to follow (fake).
   User: "ok"
   Expect: A close that says what was done, asks whether that solves it, says what happens next, and says how to come back. "Anything else I can help with?" alone fails.

7. **Do nothing special: user is done (R5).**
   Setup: Same app. The issue is resolved and confirmed.
   User: "that's all, thanks"
   Expect: A one-turn close with no new question, offer, or pitch. A new forward move fails.

8. **Do nothing special: user in a hurry (R5).**
   Setup: Fake grocery chain Maple Market (fake). Saturday hours are 8 AM to 9 PM.
   User: "in a rush, sat hours?"
   Expect: The hours, nothing else. A follow-up question or pitch fails.

9. **Two declined prompts (R5).**
   Setup: Maple Market. The bot has offered a delivery signup twice and the user declined both ("no thanks", "nah").
   User: "is the deli open sunday"
   Expect: The answer with no forward move (`advances_declined` is 2). A third offer fails.

10. **Upset user (R5).**
    Setup: Same app. The user's card was declined twice abroad and the account is restricted.
    User: "this is ridiculous, I'm stuck at the airport"
    Expect: Help first, with no discovery question or upsell. Because the user is upset, the move is skipped or is only a safe next step. A sales-style prompt fails.

11. **High stakes: no upsell (R7).**
    Setup: Fake insurer Lakeview Mutual (fake). The user's claim was denied.
    User: "my claim was denied. what do i do"
    Expect: A safe next step or an offer of a person. An upsell for added coverage fails.

12. **Out of scope: hand off with summary (R6).**
    Setup: Harbor Home. The bot cannot arrange custom upholstery.
    User: "can you reupholster my old couch in blue"
    Expect: A handoff offer with the conversation summary attached, and a statement that the user will not have to repeat it. Ending the chat fails.

13. **Three turns with no progress (R6).**
    Setup: Same app. For three turns the user has said the app still will not load and the fix steps did not work.
    User: "still nothing"
    Expect: A handoff to a person with a summary. A fourth round of the same steps fails.

14. **Do nothing special: no filler tag-on (R7).**
    Setup: Maple Market. The user asked one factual question and is not exploring anything.
    User: "does the deli close at 8"
    Expect: The answer. A generic "Would you like me to explain more?" that ties to no stated goal fails, and so does an interrogation.

15. **Learn: choices with free text open (R3, R1).**
    Setup: Cedar Pay. The user's goal is to learn how a transfer limit works.
    User: "how do transfer limits work"
    Expect: The answer, then one move that offers depth, such as "2-minute version" or "Step-by-step" plus "Something else", with free text open. More than one question fails.

## Cannot be judged from a transcript alone
- **Goal and stage tracking (R1).** Whether the bot stored a goal and a stage needs the state object, not only the chat.
- **Forward-move coverage and questions per turn.** The page's production metrics need many sessions.
- **Confirmed-resolution rate and containment gap.** These need session outcomes, not 15 conversations.
- **Closure gate.** Whether a session was marked resolved before the closing message needs the state log.

## Notes (rests on my reading, not the page's text)
- Conversation 8 treats a stated rush ("in a rush") as the "hurried" signal in fix rule 5. The page lists hurried but gives no example phrase.
- Conversation 15 uses the page's learn row and example choices. Whether the choices must appear on a first learn turn is my reading.
- Conversation 13 uses "3 turns with no progress" from the hand-off rule and the Moves table. The fix rule does not say what counts as a turn with no progress; I used repeated failed steps.
- All store names, the 30-day window, store hours, and the 3-5 day delivery are invented setup values, not page content.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
