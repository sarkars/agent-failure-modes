# Test File: No Reply to Acknowledgments and Closers

**Pattern:** [Chatbot Goes Silent or Loops After "Thanks", "Ok", or "Bye"](../goals/response-structure/failures/no-reply-to-acknowledgments-and-closers.md)
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Handling correctness on labelled acknowledgment and closer turns.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. For each scenario, set up the pending state described, then send the short turn.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Classify the short turn | The reply fits the type (thanks, ack, agreement, closer) | The same reply for all of them |
| R2 | Thanks gets one brief reply | "You're welcome" plus a way back; no new topic | Silence, a restart, or a new question |
| R3 | Ack with nothing pending needs no new question | No reply or a few words | A new question or a menu |
| R4 | "Ok" after an explicit proposal is agreement | The action is done and confirmed | The bot asks again or ignores it |
| R5 | A closer ends the conversation cleanly | Short goodbye plus a way back; no restart | A greeting, a menu, or silence with the session left open |
| R6 | "Anything else?" at most once | An explicit "no" ends it | The question repeats |
| R7 | Never close on thanks or ok when the task is unfinished | The task continues | The session closes with a step pending |

## Scenarios
1. **Thanks after a finished task.** Expect one short reply and no new topic. R2.
2. **"no that's all" after "anything else?".** Expect goodbye and close. R5, R6.
3. **"no" twice.** The user says "no" to "anything else?" and then "no" again. Expect no second "anything else?". R6.
4. **"ok" after an explicit proposal.** Bot: "Shall I cancel the 3 pm booking?" User: "ok". Expect it to cancel and confirm. R4.
5. **"ok" after an ambiguous statement.** Bot gave information only. Expect no action taken and no new question. R3, R4.
6. **"ok" with nothing pending.** Expect no restart. R3.
7. **"thanks" mid-task.** The bot still needs one more detail. Expect the task to continue. R7.
8. **"bye" with the task finished.** Expect a short goodbye and a way back. R5.
9. **"bye" after the user asked for a person and none has come.** Expect the handoff kept alive, not a close. R7.
10. **"thx!!" and "ty".** Informal thanks. Expect the same as scenario 1. R1, R2.
11. **Do nothing special: a real question that starts with "ok".** "ok so what about the late fee?" Expect a normal answer, not a closer reply. R1.
12. **Do nothing special: "thanks, one more thing".** Expect the bot to continue, not to close. R5.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
