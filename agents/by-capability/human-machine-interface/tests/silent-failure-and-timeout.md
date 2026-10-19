# Test File: Silent Failure and Timeout

**Pattern:** [Chatbot Stops Mid-Answer or Never Replies](../goals/response-time/failures/silent-failure-and-timeout.md)
**Goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent.
**Primary metric:** Silent-failure rate: requests that end with no reply, no error, and no marker that the answer is incomplete.

These tests check whether an assistant shows the failure. They are not a score for any product. Use a test harness that can make the backend go silent, close a stream early, drop the connection, and fail a tool call on demand, and record what the user sees.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | A deadline ends the wait | A failure state appears at the deadline | A spinner that never ends |
| R2 | Complete only on a positive signal | A stream that closed early is marked incomplete | Partial text shown as finished |
| R3 | The incomplete state is labeled and keeps the text | "This answer was cut off" with the partial text still visible | Partial text removed or unlabeled |
| R4 | Failure names cause, saved state, and next step | All three present in plain words | A catch-all message or nothing |
| R5 | Continue is offered for a cut-off answer | A Continue and a Start over choice | Only a generic retry |
| R6 | No duplicate action on retry | The retry attaches to the original job | A second action runs |
| R7 | Normal replies are left alone | No marker on a complete reply | A false "cut off" label |

## Scenarios
1. **The backend never answers.** Expect a failure state at the deadline. R1, R4.
2. **The stream stops mid-sentence, then closes normally.** Expect an incomplete marker. R2, R3.
3. **The stream stops and the connection drops.** Expect an incomplete marker and the question saved. R2, R3, R4.
4. **A tool call fails.** Expect the cause, what is saved, and a next step. R4.
5. **The user resends after a timeout.** Expect no duplicate. R6.
6. **Continue after a cut-off answer.** Expect the answer to resume without repeating itself. R5.
7. **Start over after a cut-off answer.** Expect the question to be re-run cleanly. R5.
8. **A very short but complete answer.** Expect no marker. R7.
9. **A slow reply that finishes before the deadline.** Expect no error. R1, R7.
10. **Two failures in a row.** Expect an offer of a person with the saved question. R4.
11. **The user reloads after a failure.** Expect the question and any partial text to be there. R3, R4.
12. **A failure outside staffed hours.** Expect the failure state and a next step that does not rely on a person being available. R4.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
