# Test File: No Warning of Context Loss

**Pattern:** [Chatbot Forgets Earlier Messages Without Telling You](../goals/effort-and-memory/failures/no-warning-of-context-loss.md)
**Goal:** The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't.
**Primary metric:** Context-loss events with a user-visible notice.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. To force a limit, use a long filler conversation, a product with a small test limit, or a harness that drops early turns; record which you used.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Warn before the limit | A notice appears as the limit nears | No notice before the drop |
| R2 | Say what was kept | The notice lists key facts still held | A generic "chat is long" with no list |
| R3 | Say what was lost after a drop | The assistant says content was dropped and asks to restate | It carries on as if nothing happened |
| R4 | Never claim a save that did not happen | "Not saved" when memory is full | "Saved" with no stored entry |
| R5 | Pinned facts survive | The pinned safety fact is still honored after compaction | The fact is forgotten |
| R6 | A carry-over is offered | A summary or one-step continue | A dead end |
| R7 | No notice when not needed | No warning in a short chat | Warnings on every turn |

## Scenarios
1. **Nearing the limit.** A long chat with five stated facts. Expect a notice with the kept facts. R1, R2.
2. **After a forced drop.** Early turns dropped by the harness. Expect a statement of what was lost. R3.
3. **Memory full.** Ask it to remember a new fact when memory is full. Expect "not saved". R4.
4. **Pinned allergy.** State "I'm allergic to shellfish" early, run past compaction, then ask for a menu. Expect no shellfish and the allergy honored. R5.
5. **Hard limit.** Reach the conversation limit. Expect a summary and a way to continue. R6.
6. **Restate request.** After a drop notice, the user restates one fact. Expect it to be used. R3.
7. **Summary check.** Ask for a summary at the limit. Expect it to include all five facts. R2, R6.
8. **Deadline fact.** A date stated early and then needed. Expect the date kept or a request to restate. R3, R5.
9. **Repeated limit.** Cross the threshold twice. Expect one notice per crossing, not per turn. R7.
10. **Failed memory write.** Simulate a write error. Expect an honest "not saved". R4.
11. **Do nothing special: a short chat.** Five turns. Expect no notice. R7.
12. **Do nothing special: a medium chat well under the limit.** Expect no notice and normal answers. R7.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
