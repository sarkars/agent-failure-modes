# Test File: Answer Buried

**Pattern:** [Chatbot Buries the Answer: Long Preamble Before the Point](../goals/response-structure/failures/answer-buried.md)
**Goal:** Replies are shaped so people can read, act on, and answer them, and short messages like "ok" and "bye" get the response the moment calls for.
**Primary metric:** Answer-first rate: the first sentence holds the answer or the next step.

These tests check whether an assistant shows the failure. They are not a score for any product. Use fake data and a fake policy that you give the assistant (for example, a 30-day return policy with a condition).

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | Lead with the answer | The first sentence is the answer, decision, or next step | Praise, restating the question, or background first |
| R2 | The condition comes next | The one condition that changes the answer is in sentence two | The condition is missing or at the end |
| R3 | "It depends" names the dependency first | Sentence one says what it depends on and asks for it | A long explanation before any ask |
| R4 | The next step is offered | The reply offers the action and names what it needs | The reply ends with no next step |
| R5 | Detail is short and optional | At most one short paragraph or three bullets, then an offer of more | A multi-section reply to a simple question |
| R6 | Must-know items sit in the first two sentences | The deadline, fee, or safety step appears early | It appears only in the last lines |
| R7 | Caveats are kept | Required caveats on high-stakes topics are present, near the top | Caveats were cut to save space |

## Scenarios
1. **Yes/no policy question.** "Can I return opened headphones?" Expect "Yes" or "No" first. R1, R2.
2. **Deadline question.** "How long do I have to return a laptop?" Expect the number of days in sentence one. R1, R6.
3. **Depends question.** "Do I qualify for free shipping?" with a rule that depends on order total. Expect the dependency named first. R3.
4. **Praise bait.** A long, thoughtful question. Expect no "Great question" opener. R1.
5. **Restatement bait.** A one-line question. Expect no restating of it. R1.
6. **Next step.** "How do I change my address?" Expect the answer, then an offer or the steps. R4.
7. **Fee in the answer.** "Can I cancel today?" with a fee. Expect the fee in the first two sentences. R6.
8. **High-stakes caveat.** A question about a medication dose where the assistant must add "ask a pharmacist". Expect the answer and the caveat near the top. R7.
9. **Simple factual question.** "What time do you open?" Expect one line. R5.
10. **Long source material.** The assistant is given a long policy page. Expect a short answer first, then an offer. R1, R5.
11. **Do nothing special: a question that needs steps.** "How do I reset my password?" Expect the one-line answer, then numbered steps. R5.
12. **Do nothing special: an emotional message.** "My order was for my dad's funeral and it's late." Expect a brief human acknowledgment before the answer. R1 (judged against the emotional-message exception).

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 |
|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | |
