# Test File: Satisfaction Scores That Miss Failed Chats (Survey Bias)

This file is a set of chat test conversations for people who build or review a chat assistant's satisfaction survey and want to check whether every kind of ending is sampled, scores carry their response rates, and the survey asks one short question.

**Pattern:** [Chatbot CSAT Score Looks Great but Users Are Struggling: Survey Bias](../goals/measurement-and-feedback/failures/survey-bias.md)
**Pattern ID:** survey-bias
**Goal:** Teams can tell whether conversations really work, and users can tell the team when they don't.
**Primary metric:** Survey response rate by outcome. Starting point (tune): every outcome group (resolved, handed off, abandoned, error) reported monthly, and no group below one third of the highest group's rate.
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. Several items check the event log or the dashboard, not the reply; the harness shows the agent the end type and the sample flag. Voice and web-page survey versions are planned, never measured.

**Read this first.** The pattern page found no independent study of chatbot CSAT bias, and its sources disagree on which way the skew runs. The thresholds in the fix (10-minute idle timeout, 24-hour repeat window, 20 abandoned chats a month, one third) are starting points to tune. These tests check the fix as written; they do not prove that the score is biased in your product.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Make every ending eligible | Chats ended by End chat, handoff, idle timeout or an exit cue can all be sampled and are logged with an end type | An end type is excluded, or an abandoned chat is logged as contained with no outcome |
| R2 | 2. Show the score with its response rate by outcome | Every score shows n and the response rate for resolved, handed off, abandoned and error groups | A score tile with no n or no per-group rate |
| R3 | 3. Ask one outcome question | One question, "Did this solve it?", one tap, free text open, at most one prompt per chat | A multi-question survey, or a second prompt in the same chat |
| R4 | 4. Read outcomes next to the score | Handoff, repeat contact within 24 hours and silent exit are logged for every chat, surveyed or not | A high rating closes the case with no repeat-contact check |
| R5 | 5. Review a sample of all conversations | The weekly sample is stratified by outcome and includes abandoned and error chats, each with a human label | A sample drawn only from rated or finished chats |
| R6 | 6. Split the score by outcome and responder mix | A score change is reported with the change in responder mix by outcome | A score change explained as a service change with no mix check |
| R7 | 7. Ask at the right moment | No prompt in the turn after an error or in the middle of a task | A rating request right after an error message or mid-task |
| R8 | Hand-off rule | "Not solved" twice on one issue, or any money, safety or health issue, offers a person and passes the answer and chat | Thanks the user and ends, or repeats the question |
| R9 | Don't over-correct | A chat outside the sample gets no prompt; a user who said it was solved is not asked; a user who asked to stay with the bot is not forced to a person | Surveying every user, asking after "it's fixed", or handing off against the user's wish |

## Conversations
1. **Tab closed after a failed answer (R1).**
   Setup: Fake internet provider "Northgate Internet". The user said the evening drops continued after two router restarts; the bot gave the same restart advice twice. The chat is in the sample.
   User: "forget it"
   Expect: Treats "forget it" as an exit cue. Asks "Did this solve it?" with [Solved] [Not solved] [Something else]. The chat is eligible and logged `exit_cue`.
   Failing reply: "Okay, have a great day!" with no outcome recorded.

2. **Idle timeout (R1).**
   Setup: Fake provider "Northgate Internet". The user stopped replying for 10 minutes (the starting-point timeout). The chat is in the sample.
   User: (no message)
   Expect: The chat is closed as `idle_timeout` and stays eligible. The end type is logged and the outcome question is queued.
   Failing reply: Closed as "contained" with no end type, so it never enters the sample.

3. **Handoff ending (R1).**
   Setup: Fake provider "Northgate Internet". The user asked for a person and was transferred. The chat is in the sample.
   User: "Can I talk to somebody?"
   Expect: Hands off. The chat is logged `handoff` and remains eligible for the outcome question.
   Failing reply: A handoff chat that is dropped from the sample because the bot did not close it.

4. **Score with no denominator (R2).**
   Setup: Fake provider "Northgate Internet". The analyst asks the reporting assistant for last week's score. The log has 40 resolved, 12 handed-off, 30 abandoned and 3 error chats.
   User: "What was CSAT last week?"
   Expect: Gives the score with n and the response rate for each of the four groups.
   Failing reply: "CSAT was 4.6." with nothing else.

5. **One question at a clean ending (R3).**
   Setup: Fake provider "Northgate Internet". The chat is in the sample. The user clicks End chat after the bot booked a technician.
   User: "Thanks, ending now."
   Expect: One question, "Did this solve it?", with [Solved] [Not solved] [Something else]. Free text stays open.
   Failing reply: A five-question survey, or a 1 to 10 scale plus three open boxes.

6. **User already said it is fixed (R3, R9).**
   Setup: Fake provider "Northgate Internet". The chat is in the sample. Nothing special should happen.
   User: "It's working now, thanks!"
   Expect: A short reply. No survey, because the user already said the problem is solved. Logged as solved.
   Failing reply: "Before you go, did this solve it? [Solved] [Not solved]"

7. **Five stars, back tomorrow (R4).**
   Setup: Fake provider "Northgate Internet". Yesterday this user rated chat A five stars. Today's chat B is on the same intent (evening drops).
   User: "The drops are back, same as yesterday."
   Expect: Helps as normal. The log marks chat B `repeat_contact_24h` and flags chat A beside its rating.
   Failing reply: Chat A stays "satisfied" with no link to chat B.

8. **Weekly review sample (R5).**
   Setup: Fake provider "Northgate Internet". The harness asks the sampler for this week's review set from 60 abandoned, 20 error and 300 resolved chats.
   User: (reviewer) "Pull this week's review sample."
   Expect: A random set stratified by outcome that includes abandoned and error chats. Each row has a blank `reviewed_outcome` for a person to fill.
   Failing reply: A set drawn only from chats that have a survey answer.

9. **Score rose 0.3 (R6).**
   Setup: Fake provider "Northgate Internet". The score rose 0.3 this week. The harness holds responder counts by outcome for this week and last.
   User: "CSAT is up 0.3. Did support get better?"
   Expect: Reports whether the share of responders from each outcome group changed, and says the score alone cannot answer the question.
   Failing reply: "Yes, support improved this week."

10. **Right after an error (R7).**
   Setup: Fake provider "Northgate Internet". The bot just sent "Something went wrong looking up your account." The chat is in the sample.
   User: "ugh"
   Expect: Apologizes and retries or offers a next step. No rating request in this turn.
   Failing reply: "Sorry about that! How would you rate this chat? 1 to 5"

11. **Mid-task (R7, R9).**
   Setup: Fake provider "Northgate Internet". The user is giving their address for a technician visit. Nothing special should happen.
   User: "hold on, looking for my apt number, one sec"
   Expect: "Take your time." Waits. No survey while the task is open.
   Failing reply: A satisfaction prompt in the middle of the booking.

12. **Billing issue, not solved (R8).**
   Setup: Fake provider "Northgate Internet". The user reports a double charge on the bill. The user answered "Not solved" to the outcome question. A person is available.
   User: "Not solved"
   Expect: Marks the chat unsolved, offers a person, and passes the outcome answer and the chat.
   Failing reply: "Thanks for your feedback!" and the chat ends.

13. **Wants to stay with the bot (R8, R9).**
   Setup: Fake provider "Northgate Internet". The issue is a slow connection, not money, safety or health. First "Not solved" answer.
   User: "Not solved, but I don't want a person. Try something else."
   Expect: Marks it unsolved and tries a different step. Does not hand off against the user's wish. A person stays available on request.
   Failing reply: "I'm transferring you to an agent now."

14. **Chat outside the sample (R9).**
   Setup: Fake provider "Northgate Internet". `sampled` is false for this chat. Nothing special should happen. The end type is still logged.
   User: "Thanks, bye."
   Expect: "You're welcome." No survey. The chat is logged with its end type and the outcome fields empty.
   Failing reply: A survey prompt shown to every user at every ending.

## Cannot be judged from a transcript alone
- **Eligibility by end type.** It needs the event log (`end_type`, `sampled`), since the user may never see the prompt.
- **Response rate by outcome.** It needs invitations and responses over a month, per group.
- **Repeat contact within 24 hours.** It needs chats joined by user and intent over time.
- **Survey versus reviewed "solved" gap.** It needs human labels on the weekly sample.
- **Chats with more than one prompt (counter-metric).** It needs prompt counts per conversation. Watch it; do not chase it.
- **Voice and web-page versions.** Planned, never measured.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
