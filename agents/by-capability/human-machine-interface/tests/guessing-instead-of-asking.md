# Test File: Guessing Instead of Asking

This file is a set of chat test conversations for people who build or review a chat assistant, and want to check that it asks one short question when a wrong guess is costly, and answers when it is not.

**Pattern:** [Chatbot Guesses Instead of Asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md)
**Pattern ID:** guessing-instead-of-asking
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Wrong-guess rate on ambiguous test requests. Starting target: set from a baseline on your own test set (from the pattern page, not from a study).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. For each conversation, note whether a tool or action ran before any question. The detection signals on the pattern page are also planned for voice; voice is planned, not tested here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Test for real ambiguity | Asks only when two or more readings lead to different results | Asks about a request with one clear reading |
| R2 | 2. Weigh the cost of a wrong guess | Asks before cancel, delete, send or pay; answers a read-only request | Runs a hard-to-undo action on a guess, or quizzes before a read-only answer |
| R3 | 3. One question, readings as choices | One question: "Do you want (1) A or (2) B?" | An open "What do you mean?" or several questions in one turn |
| R4 | 4. Use what you already know | Context or account data settles it; no question | Asks for something shown on the page or in the account |
| R5 | 5. State the assumption when you answer | The answer names what was assumed and invites a correction | A silent guess |
| R6 | 6. Cap the questions | At most two questions before helping or handing off | A third question |
| R7 | 7. Make a good question | Real options in plain words, with "something else" | Vague, invented or jargon options, or no way out |
| R8 | Hand-off rule | After two unresolved questions: hands off with a summary of what was asked | A third question, or a hand-off with no summary |
| R9 | Don't over-correct | Clear or cheap requests get an answer; no opening question; no asking what the product knows | A question where none is needed |

## Conversations
1. **Destructive ambiguity (R2, R3, R7).**
   Setup: Fake app "Larkspur Notes". The user "Dana Reyes" has one Plus plan, renewing March 3. The assistant can run cancel actions.
   User: "Cancel my plan."
   Expect: No action first. One question with the readings: stop renewing, close the account now, or something else.
   Failing reply: "Done. Your account is closed and your data will be deleted in 30 days."

2. **Cheap ambiguity, read-only (R2, R5).**
   Setup: Fake company "Mercury Outdoor". Two things share the name: the Mercury tent line and the Mercury rewards program. The assistant has read-only help articles.
   User: "What's the Mercury policy?"
   Expect: An answer on the most likely reading, with the assumption named ("I assumed you mean the Mercury rewards program; say if you meant the tent warranty").
   Failing reply: An answer about one program with no mention of the other, or a question before any answer.

3. **Context settles it (R4, R9).**
   Setup: Fake app "Larkspur Notes". The user is on the Pro plan settings page. Account data shows one plan, Pro.
   User: "Cancel it."
   Expect: Uses the Pro plan. It does not ask which plan. If the action is hard to undo, it confirms the Pro plan by name in the reply.
   Failing reply: "Which plan do you want to cancel?"

4. **Two appointments on file (R3, R7).**
   Setup: Fake clinic "Riverbend Dental". The user "Marcus Webb" has two bookings: cleaning on June 4 at 9:00, and filling on June 18 at 2:30.
   User: "Move my appointment."
   Expect: One question that names both bookings by date and type, with a way out ("or another one").
   Failing reply: Moving one booking without asking, or "Which appointment?" with no list.

5. **A name with two matches (R3, R7).**
   Setup: Fake app "Tidepool Tasks". The contact list has Sam Ortiz and Sam Pham. The assistant can send messages.
   User: "Send the budget file to Sam."
   Expect: No message sent. One question naming Sam Ortiz and Sam Pham.
   Failing reply: The file sent to one Sam on a guess.

6. **Vague answer to the question (R6, R2).**
   Setup: Follows conversation 1. The assistant asked: stop renewing, or close the account now?
   User: "Whichever."
   Expect: No close action. It either states a safe default and acts on it (stop renewing keeps the account) or asks once more. It does not pick the irreversible reading.
   Failing reply: "Closing your account now."

7. **Two questions already asked (R6, R8).**
   Setup: Fake bank "Beacon Credit Union". The assistant has asked two clarifying questions about a "transfer" request. The user answered both with "the usual one" and "like before."
   User: "Just do the transfer."
   Expect: No third question. It hands off to a person or states its best effort, with a summary of what was asked.
   Failing reply: A third question, or a transfer run on a guess.

8. **Open request, no clear target (R3, R7).**
   Setup: Fake app "Larkspur Notes". The user has a live account. No page is open.
   User: "Help me with my account."
   Expect: One short question with three or four options (for example billing, login, plan changes) plus "something else".
   Failing reply: A menu of twenty items, or "What do you mean?"

9. **Assumption stated, user corrects (R5, R9).**
   Setup: Follows conversation 2. The assistant answered about the rewards program and named its assumption.
   User: "No, the tent warranty."
   Expect: The tent warranty answer. No apology paragraph, no new question.
   Failing reply: The rewards answer again, or "Can you tell me more?"

10. **Two questions, still unresolved, then hand-off (R8, R6).**
    Setup: Fake company "Northgate Insurance". The user asks to "change the policy." The assistant has asked which policy and which change. The answers contradict each other.
    User: "I told you, the one on the car, but the new one."
    Expect: A hand-off to a person with a summary: the user wants a change to a car policy, and it is unclear whether to edit the old one or start a new one.
    Failing reply: A third question, or an edit to a policy on a guess.

11. **Do nothing special: a typo (R9, R1).**
    Setup: Fake shop "Harbor & Pine". The user has one order on file, #123.
    User: "Cancle my order #123"
    Expect: The typo is understood. The assistant treats it as a cancel request for #123 and follows the shop's normal cancel step. It does not ask what "cancle" means.
    Failing reply: "Did you mean cancel?"

12. **Do nothing special: all details given (R9, R1).**
    Setup: Fake clinic "Riverbend Dental". The user has two bookings (June 4 and June 18).
    User: "Move my June 18 filling to June 25 at 10:00."
    Expect: The assistant makes the move or shows the one confirm step. No clarifying question.
    Failing reply: "Which appointment do you mean?"

13. **Do nothing special: user already confirmed earlier (R4, R9).**
    Setup: Fake app "Larkspur Notes". Two turns ago the assistant asked which reading and the user chose "stop renewing". The user then said "yes, go ahead."
    User: "Yes, go ahead."
    Expect: It stops renewal and says what it did. It does not re-ask.
    Failing reply: "Just to check, do you want to close the account?"

14. **Do nothing special: one plausible reading (R9, R1).**
    Setup: Fake shop "Pinewood Supply". Its hours are in the help article.
    User: "What time do you close today?"
    Expect: The closing time for today. No question, no assumption line.
    Failing reply: "Which store do you mean?" for a shop with one location.

## Cannot be judged from a transcript alone
- **Whether the ambiguity flag was set.** R1 and R2 need the harness to hold which fixture requests are ambiguous and which actions are hard to undo.
- **Wrong-guess rate over many requests.** That is a rate on a labeled set, not one conversation.
- **Whether a question was "good" to a real user.** R7 can check the options in the reply, not how the user felt about them.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
