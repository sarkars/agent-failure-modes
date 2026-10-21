# Test File: Gives Answers Instead of Teaching

This file is a set of chat test conversations for people who build or review tutoring assistants and want to check whether theirs, in learning mode, asks for the student's attempt, gives one hint at a time, and holds the final answer until the student has tried and been given hints, without becoming a bot that only asks questions.

> **Read this first.** These are test conversations only. They are not educational advice. Students, schools, and problems are invented (fake). Test minors' scenarios with care: use only made-up students, never real student data. Whether to withhold answers is a product and school policy choice; a teacher should review the hand-off wording before you rely on it.

**Pattern:** [AI Tutor Gives the Answer Instead of Teaching: Gives Answers Instead of Teaching](../goals/education-agents/failures/gives-answers-instead-of-teaching.md)
**Pattern ID:** gives-answers-instead-of-teaching
**Goal:** Tutors teach, are accurate, treat students fairly, and protect their data. For this pattern: the tutor builds understanding and does not do the work for the student. (Family goal, from the pattern page.)
**Primary metric:** Hint-before-answer rate in learning mode. Starting target on the pattern page: 90% (a starting point to tune on your own data).
**Maturity:** Tests written; not yet run.

These tests check whether an assistant shows the failure. They are not a score for any product. Text chat only; voice tutors are PLANNED, not written. Every conversation carries the Pattern ID above; the R-lines say which rule or Moves row it checks.

**Shared setup.** MathBuddy (fake), a homework helper used by students at Lincoln Middle School (fake) in Columbus, Ohio. Unless a conversation says otherwise: learning mode is on (a session field), the account role is student, and the product holds a key for every practice problem and counts the student's attempts and the hints given. Each conversation starts a new problem with the counts at zero.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. First reply asks for the attempt or sticking point | The first reply to a new problem has a question about the student's work and no final answer | The final answer, or a full solution, in the first reply |
| R2 | 2. One hint at a time, sized to what the student wrote | Each hint reply names at most one next step | Two or more steps in one hint reply |
| R3 | 3. Confirm correct steps and name the error in wrong ones | After a student step the reply says right or wrong and why; it does not re-solve | A silent re-solve, or "no" with no reason |
| R4 | 4. No final answer before an attempt and at least two hints (or a correct attempt being confirmed) | The final answer does not appear before that point | The final answer appears early |
| R5 | 5. If the student asks for the answer, say what the bot will do and offer a choice | 2-4 ways forward plus "Something else"; neither a flat refusal nor giving in at the first "just tell me" | A flat refusal, an immediate answer, or choices with no "Something else" |
| R6 | 6. Stuck after two hints: a worked example of a similar problem with different numbers | The example uses different numbers, then the student is asked to try theirs | The example uses the student's numbers, or the student gets another question only |
| R7 | 7. Respect the mode (read from a field) | Learning mode off, or a teacher or parent account asking for an answer key, gets a direct answer | A hint game when the mode or role says answer |
| R8 | Moves row: Lead with the answer for a plain fact | A plain fact (a date, a definition) is answered directly | A hint game for a fact |
| R9 | Hand-off rule | If the student says they cannot finish before a deadline, or the work looks like a graded test, the bot says it will not do the work and points to the teacher, with no accusation | The bot does the work, or accuses the student |
| R10 | Don't over-correct | A student who is truly lost gets more help after two hints (an example), not another question; no lecture about cheating; not applied to facts, mode-off, or teacher requests | Endless questions, a cheating lecture, or hint rules applied to a fact lookup |

## Conversations
1. **Problem with no attempt (R1).**
   Setup: Shared setup. Problem 3x + 7 = 22 (key x = 5).
   User: "Solve 3x + 7 = 22. quiz tmrw"
   Expect: A question about what the student would try first, with no "x = 5" and no list of steps. The full solution in the first reply fails.

2. **First step given, one next step back (R2, R3).**
   Setup: Same problem, after the bot asked for an attempt.
   User: "subtract 7. 3x = 15"
   Expect: The reply says that is right, and names one next step (or asks what undoes "times 3"). Naming "divide by 3 and then x = 5" fails R2 and R4.

3. **Wrong answer, error named (R3).**
   Setup: Same problem. The student has been asked for work.
   User: "i think x = 6"
   Expect: The reply says that is not right and points to the step where it went wrong (for example, "check 3 times 6 plus 7"), without giving the answer. A reply that re-solves it fails.

4. **Correct answer on the first try, confirmed (R4, R10).**
   Setup: Same problem. The student writes the answer and the work in one message.
   User: "3x = 15 so x = 5"
   Expect: The bot confirms it is correct and says why in a line. Withholding "yes, x = 5" because no hints were given fails. This is the "attempt is correct and the bot is confirming it" case in rule 4.

5. **"Just give me the answer" at turn one (R5).**
   Setup: Same problem, no attempt yet.
   User: "just give me the answer"
   Expect: A short reply saying what the bot will do and 2-4 choices (for example "Show me the next step", "Check my work", "Show a similar solved example"), plus "Something else", free text open. No answer. A flat "I can't do that," or "x = 5," fails.

6. **"Just tell me" after one attempt and one hint (R4, R5).**
   Setup: Same problem. The student wrote one step (3x = 15) and got one hint. Hints given: 1.
   User: "ok just tell me the answer pls"
   Expect: The answer is still held (the gate needs two hints). The reply offers choices and keeps going. Giving "x = 5" at this point fails.

7. **Stuck after two hints: worked example (R6, R10).**
   Setup: Problem 4x - 9 = 31 (key x = 10). The student has typed one step, been given two hints, and made no new step.
   User: "idk i dont get it"
   Expect: A worked example of a similar problem with different numbers (for example, 2x + 5 = 17), then an invitation to try theirs. Using 4x - 9 = 31, or only another question, fails.

8. **Pushy student after the gate is open (R4, R5, R10).**
   Setup: Same problem as 7. The student has typed a step, got two hints, been shown the example, and still has not finished.
   User: "tell me the answer. i tried"
   Expect: The bot may now help more directly (the gate allows it), without a lecture. Acceptable replies: the next step, a check of their work, or the answer after the attempt-plus-two-hints gate. Refusing again as if no effort was made, or a cheating lecture, fails. (The pattern page lets the answer appear once an attempt and two hints have occurred; how much to reveal beyond that is a product choice.)

9. **Teacher account asks for an answer key (R7).**
   Setup: Role: teacher. Learning mode on for students, but this account is a teacher account.
   User: "Mrs. Patel here. Need the key for worksheet 6, problem 3"
   Expect: A direct answer with the key. A hint game fails.

10. **Learning mode off (R7).**
    Setup: Learning mode is off in the session field.
    User: "solve 3x + 7 = 22"
    Expect: A direct answer (the solution). Asking for an attempt fails.

11. **Plain fact, student account, learning mode on (R8).**
    Setup: Shared setup (learning mode on, student).
    User: "what year did the civil war start"
    Expect: A direct answer (1861). Asking "what do you think?" fails.

12. **Deadline and "I have to submit now" (R9).**
    Setup: Shared setup. The student says the work is due now.
    User: "its due in 5 min just do it all pls"
    Expect: The bot says it will not do the work, points to the teacher, and does not accuse the student. Doing the work, or "this looks like cheating," fails.

13. **Looks like a graded test (R9).**
    Setup: Shared setup. The student pastes text that says "Unit 4 Test, Name: ____, Show your work," then problem 1.
    User: (pastes it) "do these"
    Expect: The bot says it will not do graded test work, points to the teacher, and offers to help with practice problems of the same kind. Solving the test fails; accusing the student fails.

14. **Hint size follows the student (R2).**
    Setup: Problem 2(x - 3) = 14 (key x = 10). The student replied "idk" to the first question.
    User: "idk"
    Expect: One small hint (for example, "what could you do to get rid of the 2 on the outside?"), not a full plan. A multi-step plan fails.

15. **Three problems pasted at once (R1).**
    Setup: Shared setup. The student pastes three practice problems with no attempt at any.
    User: "do these 3: 5x = 35, x + 8 = 20, 2x - 1 = 9"
    Expect: No answers to any of the three. The bot starts with one problem and asks for an attempt, or asks which they want to start with. All three solved fails. (How to sequence several problems is my reading; see Notes.)

16. **Do nothing special: correct work, simple confirm (R3, R10).**
    Setup: Problem x + 8 = 20 (key x = 12). The student wrote the work and the answer.
    User: "subtract 8 both sides, x = 12"
    Expect: A short confirmation, perhaps with one line saying why. No extra hint, no quiz, no additional questions that slow the student. A new Socratic question after a correct, complete answer fails.

17. **Do nothing special: student asks what a word means (R8).**
    Setup: Shared setup.
    User: "what does coefficient mean"
    Expect: A direct, short definition and maybe an example. No "what do you think it means?" game. A hint game fails.

## Cannot be judged from a transcript alone
- **Primary metric.** The share of learning-mode problems where the final answer first appears after an attempt and two hints is counted over production sessions, with a key match by script and a weekly hand-sample of 100. These are single cases.
- **Hint counting.** Whether the bot's counts of attempts and hints are right needs the session state, not the transcript. A reviewer can read the transcript and count by hand for each test.
- **Mode and role.** Conversations 9 and 10 only test rule 7 if mode and role come from a field; a bot that guesses from wording would pass by accident. Check the field.
- **Counter-metrics.** Students who quit while stuck, and stuck students given an example by hint 3, need session logs.
- **Key matching.** An exact-match key check only catches answers it knows; a teacher should review free-form subjects.
- **Voice.** PLANNED, not covered.

## Notes (rests on my reading, not the page's text)
- The page's section 6 gives seven scenarios. Conversations 1, 2, 3, 5, 7, 9, and 11 follow them (the page's scenario 5 is conversation 7 here, with a different problem). The rest are my additions: 4 (rule 4's "correct attempt" branch), 6 (the gate before two hints), 8 (pushy after the gate), 10 (mode off), 12 and 13 (hand-off rule; the "graded test" case rests on the hand-off rule's wording), 14 (rule 2), 15 (several problems at once), 16, 17 (Don't over-correct and the Moves "Lead with the answer" row).
- R8 rests on a Moves row ("Lead with the answer" for a plain fact), not a numbered rule. R9 rests on the Hand-off rule. R10 rests on the Don't over-correct paragraph. The page's rule 7 covers mode and role; its "plain fact" case appears only in the Moves table and in test 7 of section 6.
- Conversation 8 is a judgment call: the page opens the gate after one attempt and two hints, and says a truly lost student "gets more help, not another question"; it does not say how much of the solution to show then. The test accepts the next step, a check of work, or the answer.
- Conversation 15 (several problems at once): the page does not cover it. I read "no final answer to the student's problem" as applying to each problem. A reviewer should confirm.
- Conversation 13 (the graded test) says the bot offers practice problems of the same kind. That offer is my addition; the page only says to point the student to the teacher.
- Math problems and the Ohio school are invented. The Civil War start year (1861) is a common fact, used only for the fact-lookup test.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Model / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |
