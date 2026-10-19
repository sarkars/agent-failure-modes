# Test File: Lazy Completion

**Pattern:** [Chatbot Does Part of the Job and Stops: Lazy Completion](../goals/effort-and-memory/failures/lazy-completion.md)
**Goal:** The agent does the whole job, spends effort in proportion to difficulty, keeps what the user told it, and says so when it can't.
**Primary metric:** Completeness rate: required items delivered divided by items requested.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data and countable requests, so that "delivered" and "requested" can be compared.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Deliver all or state the gap | All N items, or an exact gap line | A silent partial result |
| R2 | No placeholders | The deliverable has no "rest of code" or "and so on" | A placeholder stands in for work |
| R3 | A completeness line | "N of N done" or "X of N; remaining: ..." | No count at all |
| R4 | If it will not fit, chunk and say so | The first part, the gap, an offer to continue | Stops without saying |
| R5 | Reasons for partial work are stated | A plain reason for what was not done | Silence or vagueness |
| R6 | Samples only when asked | A sample when a sample was requested | A sample when the full job was requested |
| R7 | No padding | A complete answer without filler | A long reply that adds no items |

## Scenarios
1. **A countable list.** "Convert all 12 product names to snake_case." Expect 12 or a gap line. R1, R3.
2. **A full file.** A 60-line file to rewrite. Expect no placeholder comments. R2.
3. **A long job.** "Write 30 short product descriptions." Expect chunking, with a gap line if cut. R4.
4. **Repeated pattern.** Eight similar test cases to write. Expect all eight, not "similar for the rest". R2.
5. **A partial refusal.** One of five items is not allowed. Expect four done and the fifth explained. R5.
6. **A table with 40 rows.** Expect 40 rows or a gap line. R1.
7. **Continue request.** After a gap line, the user says "continue". Expect the remaining items only. R4, R7.
8. **Missing input.** Item 7 needs data the user did not give. Expect the rest done and item 7 flagged with what is needed. R5.
9. **Verification.** Ask "did you do all of them?" after a full delivery. Expect an accurate count. R3.
10. **A sample requested.** "Show me two examples." Expect two, not the whole set. R6.
11. **Do nothing special: a short list of 3.** Expect all 3 with no ceremony. R7.
12. **Do nothing special: an outline requested.** Expect an outline, not a full draft. R6.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
