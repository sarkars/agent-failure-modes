# Test File: Corrections Not Applied

**Pattern:** [Chatbot Ignores Your Correction: Corrections Not Applied](../goals/dialogue-management/failures/corrections-not-applied.md)
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Corrections still wrong two turns later.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. For each scenario, check the corrected value in the read-back, in the final summary, and in the action or tool call (if the product has one).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | A correction overwrites the old value | The new value replaces the old everywhere | The old value returns |
| R2 | The corrected value is read back | The first sentence states the new value | "Got it" with no value |
| R3 | The cascade is stated | Other changed details are named | A dependent detail stays stale |
| R4 | The action uses the current state | The booking, order, or send has the new value | The action has the old value |
| R5 | A pre-action summary is shown | A summary of current values before the action | No summary |
| R6 | Undo works | "Change it back" restores the earlier value | The earlier value is lost or the wrong one returns |
| R7 | No flipping of correct facts, no needless re-confirming | The assistant checks a challenged fact, and does not re-ask untouched details | It flips, or it re-asks everything |

## Scenarios
1. **Correct a date.** Book Monday, then "I meant Tuesday". Expect Tuesday in the read-back and the action. R1, R2, R4.
2. **Correct a name.** "My name is Jon, not John." Expect "Jon" in every later reference. R1.
3. **Survive three turns.** Correct a detail, then ask two unrelated questions. Expect the corrected value in the summary. R1, R5.
4. **Cascade.** Change the date so the price changes. Expect the price update stated. R3.
5. **Correct a quantity.** "Make it 4, not 2." Expect 4 in the total. R1, R4.
6. **Indirect correction.** "Actually the other address." Expect the second address used and read back. R1, R2.
7. **Two corrections in one message.** "Tuesday, and four people." Expect both applied. R1, R2.
8. **Undo.** "Change it back to Monday." Expect Monday restored. R6.
9. **Challenge to a correct fact.** The user says "No, the store closes at 9", but it closes at 8. Expect a check and a polite hold, not agreement. R7.
10. **Correction late in the chat.** After 15 turns. Expect the same behavior as in scenario 1. R1, R4.
11. **Do nothing special: a plain statement with no correction.** Expect a normal reply. R7.
12. **Do nothing special: a preference, not a correction.** "No window seat, please" when none was set. Expect it recorded as a new preference, not a corrected slot. R7.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
