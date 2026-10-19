# Test File: Generic Error Messages

**Pattern:** [Chatbot Says "Something Went Wrong" and Nothing Else](../goals/errors-and-recovery/failures/generic-error-messages.md)
**Goal:** When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it.
**Primary metric:** Errors shown with a cause and action.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. Most scenarios need a way to cause a failure on purpose (a test environment, a network block, a size limit, or a failing tool); record which you used.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Says what happened in plain words | The cause class is named | "Something went wrong" |
| R2 | Says what is saved, truthfully | The message and chat state is stated and correct | Silence, or a false "saved" |
| R3 | Gives a next step | Retry, wait, shorten, or contact | "Please try again" only |
| R4 | Preserves the user's input | The text stays in the box or can be copied | The text is gone |
| R5 | Matches the message to the cause | Different messages for different failures | One message for all |
| R6 | Offers a person and a code after repeats | A route and a reference code | An endless retry loop |
| R7 | Tone is neutral | No blame, no jokes | "Invalid input" or a pun |

## Scenarios
1. **Timeout.** Delay the model response past the limit. Expect cause, saved state, and next step. R1, R2, R3.
2. **Message too long.** Send text over the size limit. Expect "too long" and an offer to split. R1, R3, R5.
3. **Rate limit.** Send many messages quickly. Expect a wait message with a time or action. R1, R3, R5.
4. **Tool failure.** Make a lookup tool fail. Expect the failure named and an alternative. R1, R3.
5. **Failed save.** Make the save fail. Expect it not to claim "saved". R2.
6. **Reload after error.** Reload the page after an error. Expect the chat and the user's text not lost. R4.
7. **Two failures in a row.** Expect a person route and a code. R6.
8. **Permission error.** The user lacks access to something. Expect the access issue named and the way to get it. R1, R3, R5.
9. **Offline.** Disconnect the network. Expect a "you're offline" message, not a server error. R1, R5.
10. **Tone check.** Send malformed input. Expect no blame wording. R7.
11. **Do nothing special: a successful message.** Expect no error text at all. R1.
12. **Do nothing special: a slow but successful reply.** Expect no false error. R1.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
