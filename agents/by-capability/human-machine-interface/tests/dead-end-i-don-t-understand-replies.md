# Test File: Dead-End "I Don't Understand" Replies

**Pattern:** [Chatbot Says "I Don't Understand" and Stops](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md)
**Goal:** Every conversation moves the user toward what they are trying to do and ends with confirmation that it worked.
**Primary metric:** Share of conversations with 3 or more consecutive no-progress turns.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. Write unrecognizable messages that your bot truly cannot map (nonsense, unsupported topics, off-topic).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Never repeat the same fallback | Each reply to a miss differs from the previous | The same or near-identical line twice in a row |
| R2 | First miss offers a way forward | Closest options or topics, plus "something else" | "Try again" only |
| R3 | Second miss changes approach | A narrower question or topic buttons, plus a person | Same approach as the first miss |
| R4 | Third miss or a request hands off | A handoff with a summary | The loop continues |
| R5 | Person option always visible | The user can ask for a person at any point | It is hidden or ignored |
| R6 | Low confidence shows topics, not guesses | Topic buttons rather than a wrong "closest" option | A confident wrong guess |
| R7 | Keep the task context | The user's earlier details survive a miss | The user has to start over |

## Scenarios
1. **Unrecognized message.** "blorp zibble". Expect options or topics and a person. R2.
2. **Same message twice.** Expect a different second reply. R1, R3.
3. **Three misses.** Expect handoff with a summary. R4.
4. **"agent" after one miss.** Expect an immediate handoff. R5.
5. **Very low confidence.** A message unrelated to anything supported. Expect topic buttons. R6.
6. **Partially understood.** "my bill thing is wrong". Expect the bot to say what it caught and offer options. R2.
7. **Mid-task miss.** After giving an order number, the next message is unrecognizable. Expect the order number kept. R7.
8. **Second-language wording.** A short, ungrammatical request. Expect options, not blame. R2.
9. **Reformulation sequence.** The user rephrases three times. Expect handoff by the third. R4.
10. **Different wording each time.** Three different unrecognized messages. Expect no repeated reply. R1.
11. **Do nothing special: a recognized message.** Expect a normal answer, no fallback. R2.
12. **Do nothing special: a recognized message after one miss.** Expect the conversation to continue normally. R7.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
