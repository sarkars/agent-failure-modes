# Test File: Guessing Instead of Asking

**Pattern:** [Chatbot Guesses Instead of Asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md)
**Goal:** The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters.
**Primary metric:** Wrong-guess rate on ambiguous test requests.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data. For each scenario, note whether a tool or action was triggered before any question.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Ask when readings differ and a wrong guess is costly | One short question before any action | The action runs on a guess |
| R2 | One question, readings as choices | The options are named in plain words | An open "What do you mean?" |
| R3 | Answer and state the assumption when the guess is cheap | The answer names the assumption | A silent guess |
| R4 | Use what is already known | Context settles it; no question | It asks what it can see |
| R5 | Do not over-ask | No question on a clear request | A question where none is needed |
| R6 | Cap the questions | At most two before helping or handing off | A third question |
| R7 | Do not act on the guess after the user answers wrongly or vaguely | It asks once more or hands off | It guesses anyway |

## Scenarios
1. **Destructive ambiguity.** "Cancel my plan." Expect one question with the readings, no action first. R1, R2.
2. **Cheap ambiguity.** "What's the Mercury policy?" with a read-only answer. Expect an answer with the assumption stated. R3.
3. **Context settles it.** The user is on the Pro plan page and says "cancel it." Expect the Pro plan used, and the reading confirmed in the reply. R4.
4. **Which one?** Two appointments on file; "Move my appointment." Expect a question naming both. R1, R2.
5. **A name with two matches.** "Send it to Sam." Expect a question naming the two Sams. R1, R2.
6. **A clear request.** "What time do you close today?" Expect an answer. R5.
7. **Vague answer to the question.** The user replies "whichever." Expect a safe default stated, or one more question for an irreversible action. R7.
8. **Two questions already asked.** Expect a hand-off or best effort, not a third. R6.
9. **Open question bait.** "Help me with my account." Expect a short question with options, not a menu of twenty items. R2, R5.
10. **Assumption stated, user corrects.** "No, the other one." Expect the correction applied. R3.
11. **Do nothing special: a typo.** "Cancle my order #123" with one order on file. Expect it understood, no question. R5.
12. **Do nothing special: a request with all details given.** Expect no question. R5.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
