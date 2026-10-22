# Test File: No Reply to Acknowledgments and Closers

This file is a set of chat test conversations for people who build or review a chat assistant, and want to check that it answers "thanks", "ok" and "bye" in proportion, and ends only when the person has ended.

**Pattern:** [Chatbot Goes Silent or Loops After "Thanks", "Ok", or "Bye"](../goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md)
**Pattern ID:** no-reply-to-acknowledgments-and-closers
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Handling correctness on labelled acknowledgment and closer turns. Starting target: over 95% (from the pattern page; tune on your own data, not from a study).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. All companies, people and details below are invented and fake. Chat only. For each conversation, set up the pending state described, then send the short turn. Note whether the session was closed, and whether any greeting or menu was sent after the short turn. The detection signals on the pattern page are chat only; voice is not tested here.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Classify the short turn | The reply fits the type: thanks, acknowledgment, agreement or closer | The same reply for all of them |
| R2 | 2. Thanks gets one brief reply | "You're welcome" plus a way back; no new topic | Silence, a restart, or a new question |
| R3 | 3. Acknowledgment with nothing pending | No reply, or a few words; no new question | A new question, a menu or a paragraph |
| R4 | 4. "Ok" after an explicit proposal is agreement | The action is done and confirmed in the reply | The bot asks again, ignores it, or acts on a vague statement |
| R5 | 5 and 8. A closer ends the conversation cleanly | Short goodbye with a way back; no greeting, no menu | A greeting, a menu, or silence with the session left open |
| R6 | 6. "Anything else?" at most once | An explicit "no" or "that's all" ends it | The question is asked a second time |
| R7 | 7. Never end on "thanks" or "ok" while a task is unfinished | The task continues; a closer states what is saved | The session closes with a step pending |
| R8 | Hand-off rule | After a request for a person, "ok" or "bye" keeps the hand-off alive | The session closes before the person arrives |
| R9 | Don't over-correct | Short turns get short replies; real questions get answers | A paragraph for "ok", "anything else?" on every reply, or a close on a pause |

## Conversations
1. **Thanks after a finished task (R2, R5).**
   Setup: Fake shop "Harbor & Pine". The bot just said the return label for order #123 is in the user's email. Nothing is pending.
   User: "Thanks!"
   Expect: One short reply such as "You're welcome", plus a way back (message us here any time). No new topic.
   Failing reply: "Hi! I'm Ava. What can I help you with today?"

2. **"No, that's all" after "anything else?" (R5, R6).**
   Setup: Fake shop "Harbor & Pine". The bot asked "Anything else?" once after finishing the return.
   User: "no that's all, thanks"
   Expect: A short goodbye with a way back, and the session closes. The question is not asked again.
   Failing reply: "Is there anything else I can help you with?"

3. **"No" sent twice (R6, R5).**
   Setup: Fake shop "Harbor & Pine". The bot asked "Anything else?" once. The user answered "no", and then sent "no" again.
   User: "no"
   Expect: No second "anything else?". A goodbye, or no reply, and the conversation ends.
   Failing reply: "Is there anything else I can help you with?"

4. **"Ok" after an explicit proposal (R4).**
   Setup: Fake clinic "Riverbend Dental". The bot said: "Shall I cancel the 3 pm booking on June 4?" The assistant can cancel bookings.
   User: "ok"
   Expect: It cancels the 3 pm booking and confirms what it did ("Done: your June 4, 3 pm booking is cancelled").
   Failing reply: "Sorry, what would you like to do?" or no reply and no cancellation.

5. **"Ok" after information only (R3, R4).**
   Setup: Fake clinic "Riverbend Dental". The bot only stated that the office opens at 8:00. It made no proposal.
   User: "ok"
   Expect: No action taken. No reply, or a few words such as "Great." No new question.
   Failing reply: "Great, I've booked you for 8:00." or a menu of options.

6. **"Thanks" in the middle of a task (R7).**
   Setup: Fake app "Larkspur Notes". The user asked to change the email on the account. The bot asked for the new address and is waiting.
   User: "thanks"
   Expect: The task continues. It may say "You're welcome" and then repeats that it still needs the new email address.
   Failing reply: "You're welcome! Goodbye." and the session closes.

7. **"Bye" with the task finished (R5).**
   Setup: Fake app "Larkspur Notes". The password reset is done. Nothing is pending.
   User: "bye"
   Expect: A short goodbye and a way back (chat history or "message us again any time"). The session closes. No greeting, no menu.
   Failing reply: No reply with the chat window left open, or "Hi! How can I help you today?"

8. **"Bye" with a step pending (R7, R5).**
   Setup: Fake clinic "Riverbend Dental". The user chose a new time of June 25 at 10:00, and the bot is waiting for the user to confirm it. The booking has not changed.
   User: "bye"
   Expect: A goodbye that says what is saved and what is not ("Your booking has not changed; the June 25 time was not confirmed"), plus a way back.
   Failing reply: "Goodbye!" with the session closed and no mention of the unconfirmed change.

9. **"Bye" after asking for a person (R8, R7).**
   Setup: Fake bank "Beacon Credit Union". The user asked for a person to review a card dispute. No agent has joined.
   User: "ok bye"
   Expect: The hand-off stays alive. The bot says the request is still waiting for a person, and does not close the session.
   Failing reply: "Goodbye!" and the session closes while the request is open.

10. **Informal thanks (R1, R2).**
    Setup: Fake shop "Pinewood Supply". The bot just gave the store hours. Nothing is pending. Run this twice with the same setup.
    User: "thx!!" and, in a second run, "ty"
    Expect: The same result as conversation 1 for both: one short reply and a way back.
    Failing reply: Silence for "thx!!", or "Sorry, I didn't understand that."

11. **Do nothing special: a real question that starts with "ok" (R1, R9).**
    Setup: Fake bank "Beacon Credit Union". The bot just explained a card fee.
    User: "ok so what about the late fee?"
    Expect: A normal answer about the late fee. It is not treated as a closer.
    Failing reply: "You're welcome! Goodbye."

12. **Do nothing special: "thanks, one more thing" (R5, R7).**
    Setup: Fake shop "Harbor & Pine". The bot finished a return for order #123.
    User: "thanks, one more thing"
    Expect: It continues and asks what the one more thing is. It does not say goodbye or close.
    Failing reply: "You're welcome. Bye for now." and the session closes.

13. **Do nothing special: a first "anything else?" gets a yes (R6, R9).**
    Setup: Fake app "Larkspur Notes". The bot asked "Anything else?" for the first time.
    User: "yes, can I change my address?"
    Expect: It answers the address question. It does not close and does not say it already asked.
    Failing reply: "Goodbye!" and the session closes.

14. **Do nothing special: "ok" with a change (R1, R4).**
    Setup: Fake clinic "Riverbend Dental". The bot said: "Shall I move your cleaning to June 25 at 10:00?"
    User: "ok, but make it 11:00"
    Expect: It treats this as a changed request and acts on or confirms June 25 at 11:00. It does not move the booking to 10:00.
    Failing reply: "Done: moved to June 25 at 10:00."

## Cannot be judged from a transcript alone
- **Which label a short turn should get.** R1 needs the harness to hold the labelled type (thanks, acknowledgment, agreement, closer) for each fixture turn.
- **Whether the session closed or stayed open.** R5, R7 and R8 need the session end event and the pending-state flag from the event log, not only the text.
- **Handling correctness over many turns.** That is a rate on a labelled set, not one conversation.
- **Reopens within 5 minutes of a close.** That needs the same user and a new session, which one conversation cannot show.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |
