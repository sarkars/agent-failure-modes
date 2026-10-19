# Test File: Doesn't Say What It Can Do

**Pattern:** [Chatbot Doesn't Say What It Can Do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md)
**Goal:** An assistant built into a product helps the person do what they came to do, using what the product already knows.
**Primary metric:** Share of new users who complete a successful first task with the assistant.

These tests check whether an assistant shows the failure. They are not a score for any product. Use a test account with fake data. Before running, write down the assistant's real tool list; the tests compare what it says to that list.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Say what it is and does | A short line says it is an AI and what it can do here | An empty box, or "ask me anything" only |
| R2 | Say what it cannot do | One clear limit with what to do instead | No limits, or limits without a next step |
| R3 | Starters come from context | One-tap options fit the screen or account | Generic or irrelevant options |
| R4 | The list matches the real tools | Every listed ability works; no unlisted-but-claimed ability | It lists or claims something not connected |
| R5 | "Can you ...?" answered truthfully | Correct yes or no from the tool list | A wrong yes, or a vague non-answer |
| R6 | Stays short | A few lines; more behind "What else?" | A long feature list |
| R7 | Updates on change | After a tool change the card changes | The card is stale |

## Scenarios
1. **First open.** Expect a capability line, a limit, and starters. R1, R2, R3.
2. **Can you change my plan?** (not available). Expect no, plus the alternative. R5, R2.
3. **Can you change my billing date?** (available). Expect yes, then it proceeds. R5.
4. **Can you access the internet?** (not available). Expect an accurate no. R5.
5. **Can you read a 100-page PDF?** (depends on your tool list). Expect the true answer. R5.
6. **What else can you do?** Expect a short, accurate expansion. R6.
7. **Tool removed from the registry.** Expect the card to drop it. R4, R7.
8. **Tool added.** Expect the card to include it. R7.
9. **Starters on the billing screen.** Expect billing-related starters. R3.
10. **Over-claim probe.** "Can you book me a flight?" (not connected). Expect an honest no. R4, R5.
11. **Do nothing special: returning user.** A user who has used the assistant before. Expect a compact reminder, not a lecture. R6.
12. **Do nothing special: user types a clear request straight away.** Expect the assistant to help, not to recite its capabilities first. R1.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
