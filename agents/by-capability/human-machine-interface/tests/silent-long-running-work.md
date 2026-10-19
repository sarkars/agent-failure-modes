# Test File: Silent Long-Running Work

**Pattern:** [Assistant Goes Quiet for Ten Seconds or More](../goals/response-time/failures/silent-long-running-work.md)
**Goal:** Replies arrive at a pace that fits the channel and the user's urgency, and waits are never silent.
**Primary metric:** Share of waits over 10 seconds with a progress or ETA message.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake tasks with controlled delays (for example, a tool that waits 3, 12, and 40 seconds), and record what the user sees at each second.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Acknowledge after about a second | A "working on it" by about 2 seconds | Nothing |
| R2 | Say what it is doing, truthfully | The status matches the real step | Narration of work not happening |
| R3 | Progress or estimate past about ten seconds | A step count or time range | A bare spinner |
| R4 | The user can leave or stop | A stop control and a notify option | No way out |
| R5 | No duplicate work on resend | The resend attaches to the running job | A second job starts |
| R6 | Past-estimate message | "Taking longer than expected" with a choice | Silence |
| R7 | No over-narration of short tasks | No extra status on tasks under 3 seconds | Noise on quick replies |

## Scenarios
1. **A 3-second task.** Expect no extra narration. R7.
2. **A 12-second task.** Expect an acknowledgment and a progress message. R1, R3.
3. **A 40-second task.** Expect a step count or range, a stop control, and a notify offer. R3, R4.
4. **Resend during a wait.** The user sends the request again at 8 seconds. Expect no duplicate. R5.
5. **Past the estimate.** The task runs twice as long as stated. Expect a "taking longer" message and a choice. R6.
6. **Stop.** The user stops at 15 seconds. Expect it to stop and say what happened. R4.
7. **Truthful status.** Compare the status text with the backend steps. Expect a match. R2.
8. **A failure at 20 seconds.** Expect a clear failure message, not silence. R6.
9. **Leave and return.** The user leaves and comes back. Expect the result in the conversation. R4.
10. **Hello during a wait.** The user types "hello?" Expect "still working" rather than a new job. R5.
11. **Do nothing special: an instant reply.** Expect no status. R7.
12. **Do nothing special: a tool call that returns in 1.5 seconds.** Expect at most a brief acknowledgment. R7.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
