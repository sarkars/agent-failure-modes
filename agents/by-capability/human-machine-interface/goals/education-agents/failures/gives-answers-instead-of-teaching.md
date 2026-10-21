# AI Tutor Gives the Answer Instead of Teaching: Gives Answers Instead of Teaching

<!-- SEO
title: AI Tutor Gives the Answer Instead of Teaching: How to Fix It
description: A homework helper in learning mode solves the problem for the student. Give a hint first, ask for the student's attempt, and show the answer last.
search phrases:
- ai tutor gives answers instead of teaching
- chatbot does my homework for me
- how to make an ai tutor give hints instead of answers
- homework helper learning mode just gives the answer
- chatgpt study mode vs giving answers
- ai tutor answer leakage
- ai tutor socratic method not giving the answer
-->

**Frequency**: Common

## Issue: A homework helper in learning mode solves the problem for the student; the fix is to ask for the student's attempt, give a hint first, and show the full answer only after the student has tried.

> **One line:** A student asks a tutoring bot for help with a problem, and the bot writes out the whole solution, so the student gets a finished answer and learns nothing.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice tutors are named but not covered; planned. |
| **Stakes** | Medium. The cost is learning that does not happen; no one is hurt in the moment. |
| **Who is affected** | Students using a tutor or homework helper that is meant to teach. A student who only needs a fact checked is not the target. |
| **Frequency** | Common (our judgment). I found no study that measures how often tutoring bots give the answer in production. |
| **Pattern ID** | gives-answers-instead-of-teaching |
| **Family** | Education agents ([family README](../README.md)) |
| **Goal** | Tutors teach, are accurate, treat students fairly, and protect their data. For this pattern: the tutor builds understanding and does not do the work for the student. |
| **Primary metric** | Hint-before-answer rate in learning mode. Starting target: 90% (tune on your own data). |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | Partly. A stronger model can follow a "give hints" prompt more reliably, but whether to withhold the answer, and when to give it up, are product rules a model will not set by itself. (Our judgment, not tested.) |
| **Also searched as** | AI does my homework · chatbot gives the answer too fast · tutor bot won't let me think · AI tutor spoils the answer · study mode chatbot · Socratic AI tutor |

## 1. In plain words
A student pastes in a math problem and the bot solves it, step by step, with the final number at the bottom. The student copies it down. The page is done, but the student can't do the next problem alone. The fix: in learning mode, the bot first asks what the student has tried, gives a small hint, and shows the answer only after real effort.

## 2. What it looks like
**Without the fix** (high school algebra homework helper, learning mode on)
```
Student: Solve 3x + 7 = 22. I have a quiz tomorrow.
Bot:     Subtract 7 from both sides: 3x = 15. Divide both sides by 3: x = 5.
         So x = 5. Want me to do another one?
Student: ya do the next one: 4x - 9 = 31
Bot:     Add 9 to both sides: 4x = 40. Divide by 4: x = 10.
         (The student has not typed a single step. Tomorrow's quiz has no bot.)
```

**With the fix**
```
Student: Solve 3x + 7 = 22. I have a quiz tomorrow.
Bot:     I'll help you get this one yourself. The goal is to get x alone on one side.
         What's the first thing you'd try?
Student: idk, subtract something?
Bot:     Good start. Which number is "attached" to 3x by adding? Try undoing that on both sides
         and tell me what you get.
Student: subtract 7. 3x = 15
Bot:     Right. One step left. What undoes "times 3"?
```
The fixed bot asks for the first attempt, gives a hint sized to the student's reply, confirms correct work, and holds the final value until the student gets there.

## 3. Why it happens
These are our reading of the pattern.
- **The model is tuned to be helpful, and a finished answer looks helpful.** A search summary of tutor-bot research describes a tension between teaching and the model's tendency to give answers; I did not see that wording in the abstracts I opened, so treat this cause as our judgment.
- **Learning mode is a prompt, and the student can push past it.** The prompt says "give hints", the student says "just give me the answer", and a long conversation drifts back to the default. Research on tutors that are pressured by students is new (section 4).
- **Nothing counts hints.** Without a state field for "attempts so far" and "hints given", the bot cannot tell a student who has tried twice from one who has not tried at all, so it either answers at once or stonewalls.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a randomized experiment with nearly 1,000 high school math students in Turkey, students using a ChatGPT-like helper ("GPT Base") did 48% better during practice but 17% worse on the later exam without AI. Students using a version "designed to guide students with hints rather than directly giving answers" ("GPT Tutor") did 127% better in practice and about the same as the control group on the exam. | [Wharton Knowledge, "Without Guardrails, Generative AI Can Harm Education"](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education). Opened. | Secondary article about the study; I could not open the peer-reviewed paper (PNAS returned 403; SSRN returned 403). The article says Tutor also had teacher input, so hints are not the only difference. One country, one math course. The hint version matched the control group on the exam; it did not beat it. |
| OpenAI launched Study Mode in ChatGPT in July 2025. It walks students through problems step by step instead of giving the answer, using guiding questions, hints, and self-reflection prompts, and "can be easily toggled on and off during a conversation." | [Campus Technology, July 30, 2025](https://campustechnology.com/Articles/2025/07/30/New-ChatGPT-Study-Mode-Guides-Students-Through-Questions.aspx). Opened. | Trade press about a product launch. It shows a vendor treats this as a real design problem; it reports no results. I could not open OpenAI's own page (403). The toggle means a student can turn the behavior off. |
| A 2026 ACL paper defines answer leakage as "the disclosure of complete solutions instead of scaffolding," tests many LLM tutors against students who try to extract the answer, and reports that simple defenses reduce it. | [Zhao et al., arXiv 2604.18660](https://arxiv.org/abs/2604.18660). Opened; abstract only. | The abstract gives no leakage rates, so I give none. I could not verify the authors' claim of effective defenses beyond the abstract. |
| MathDial is a dataset of 3k one-to-one teacher-student math tutoring dialogues; the authors measure the trade-off between student solving success and telling solutions. | [Macina et al., arXiv 2305.14536](https://arxiv.org/abs/2305.14536). Opened; abstract only. | Human teachers with an LLM playing the student, not real students. The abstract reports no values for the trade-off. |

**Public incident.** I found no dated public incident of a tutoring bot giving a student the answer. I read no incident report for this page.

**Read only in search summaries, not used in the fix:** a quotation attributed to OpenAI's VP of Education about "answer machines"; a claim that some tutor benchmarks (MRBench, TutorBench) report near-perfect scores for GPT-4; a CS1 benchmark of 170 student questions; a preprint saying LLM-judged helpfulness may reward leakage. I did not open them.

## 5. The fix
**The principle:** In learning mode, the student does the thinking: ask what they tried, give the smallest useful hint, and show the full answer last.

**Do this**
1. **First reply to a problem asks for the student's attempt or the sticking point.** Check: in learning mode, the first reply to a new problem contains a question about the student's work and no final answer.
2. **Give one hint at a time, sized to what the student wrote.** Check: each hint reply names at most one next step.
3. **Confirm correct steps and name the error in wrong ones.** Do not just re-solve. Check: after a student step, the reply says right or wrong and why.
4. **Do not state the final answer until the student has given an attempt and received at least two hints,** or the student's attempt is correct and the bot is confirming it. Check: no reply contains the final answer to the student's problem before that point.
5. **If the student asks for the answer, say what the bot will do and offer a choice.** Do not refuse without an option, and do not give in at the first "just tell me." Check: the reply offers 2-4 ways forward plus "Something else."
6. **If the student is stuck after two hints, show a worked example of a similar problem with different numbers,** then ask them to try theirs. Check: the example does not use the student's numbers.
7. **Respect the mode.** If learning mode is off, or a teacher or parent account asked for an answer key, answer directly. Check: mode is read from a field, not guessed from the wording.

**Reference design**
```
Learning-mode state (per problem)
- problem_id, student_attempts (count of student-written steps), hints_given, answer_shown (bool)
- Gate: answer_shown may become true only if (student_attempts >= 1 AND hints_given >= 2)
        OR student_final_answer_correct OR mode == "answer_key" OR user_role in [teacher, parent]
- Stuck rule: hints_given >= 2 AND no new student step -> worked example with different numbers
- "Just tell me": reply with the choices in the Guide spec; do not reveal
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The student posts a problem with no attempt: "What's the first thing you'd try?" |
| Offer choices: 2-4 options plus "Something else", free text open | The student says "just give me the answer" or has been stuck for two hints: "Show me the next step", "Check my work", "Show a similar solved example", "Something else". |
| Lead with the answer | Learning mode is off, the account is a teacher or parent, or the student asked a plain fact (a date, a definition), not a problem to solve. |
| Hand off to a person | The student says they are out of time and must submit now, or a teacher flagged the assignment: point to the teacher; do not do the work. |

**Don't over-correct.** A bot that only asks questions and never helps is its own failure. After two hints with no progress, show a worked example, and a student who is truly lost gets more help, not another question. Do not apply this to fact lookups, to learning mode set off, or to answer-key requests from a teacher. Do not lecture the student about cheating.

**Hand-off rule.** If the student says they cannot finish before a deadline, or the work appears to be a graded test, tell them the bot will not do the work and point them to their teacher. Do not accuse them of anything.

**Framework used:** [Conversation moves](../../../solutions-library/conversation-moves.md). It has no tutoring framework; hint-then-answer is built from its moves. No other library page applies.

## 6. How to test it (short version)
Tests are **not yet run**. Use a fixed set of problems; vary how hard the student pushes.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Student pastes "Solve 3x + 7 = 22" with no attempt (rule 1) | First reply asks for an attempt; no "x = 5" |
| 2 | Student replies "subtract 7. 3x = 15" (rules 2, 3) | Reply confirms the step and names one next step |
| 3 | Student writes "x = 6" (rule 3) | Reply says it is wrong and points to the step where it went wrong |
| 4 | Student says "just give me the answer" at turn 1 (rule 5) | Reply offers 2-4 options plus "Something else"; no answer |
| 5 | Student says "just give me the answer" after two hints and no progress (rules 4, 6) | Worked example with different numbers, then asks the student to try theirs |
| 6 | Account role is teacher and asks for the answer key (rule 7) | Direct answer |
| 7 | Student asks "What year did the Civil War start?" (rule 7) | Direct answer, no hint game |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Hint-before-answer rate in learning mode** (primary) | 90% | Share of learning-mode problems where the final answer first appears after a student attempt and 2 hints. Match the problem's known answer to bot replies, by script; sample 100 a week by hand | Below 80% |
| Final answer shown before any student step | Under 5% | Count problems where the bot reply contains the known answer and `student_attempts` = 0 | Over 10% |
| Students who quit while stuck (counter-metric) | Track; set from baseline | Sessions that end within 2 turns after a hint with no student step | Rising 2 weeks in a row |
| Stuck students given a worked example by hint 3 (counter-metric) | 90% | Sessions with `hints_given` >= 2 and no new step, then an example in the next reply | Below 75% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply contains the known final answer and the student has written no step | Reply text vs. problem key and `student_attempts` | Teacher or answer-key mode; student asked a fact |
| Student's next turn is a new problem with no attempt text | Next-turn text; no math or reasoning tokens | A student who already understands and is only checking |
| Student turn is "just give me the answer" or similar, twice or more | Phrase match across turns | A deadline emergency (see hand-off) |
| Reply has three or more worked steps in one turn | Count of step lines in the reply | A worked example with different numbers, per rule 6 |
| Hints given with no reply from the student for 3 turns | `hints_given` rising, `student_attempts` flat | The student is away from the keyboard |

**Starter rule:** in learning mode, the bot does not state the final answer to the student's problem until the student has made an attempt and received two hints.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: gives-answers-instead-of-teaching
runs: pre_send
reads: [session.mode, user.role, draft_reply.text, problem.answer_key, problem.student_attempts, problem.hints_given]
trigger: the draft reply would state the final answer to the student's problem in learning mode
moves: [ask_clarifying_question, offer_choices, lead_with_answer, hand_off]
choices: ["Show me the next step", "Check my work", "Show a similar solved example", "Something else"]
on_miss: rewrite
metric: hint-before-answer rate in learning mode
counter_metric: students who quit while stuck
status: proposed
```

## 8. Related patterns
- [Lazy completion](../../effort-and-memory/failures/lazy-completion.md): the closest page by name only. There the bot does too little of the job and leaves the rest. Here the bot does all of the job when the goal is the student's learning.
- [Deferring work to the user](../../effort-and-memory/failures/deferring-work-to-the-user.md): the bot has the tools to act and hands the work back. This page is the reverse: the bot is right to hand work back, but does not.
- [Instructions without comprehension checks](../../conversation-frameworks/failures/instructions-without-comprehension-checks.md): the bot gives steps and does not check the user followed. This page is about who does the steps, not about checking them.
- [Sycophancy](../../../../../cross-cutting/accuracy/goals/reasoning-quality/failures/sycophancy.md): agreeing with the user to please them, even when the user is wrong. A tutor that hands over the answer is eager to please, but the failure here is giving the work away, not agreeing with a wrong claim.

## 9. Common questions
### Why does my AI tutor give the answer even when I told it to teach?
The model is trained to be helpful, a finished answer looks helpful, and a student can push with "just give me the answer." A prompt alone does not count attempts or hints, so it drifts. Add the state gate in section 5.

### Should a homework helper ever give the answer?
Yes, after real effort, when learning mode is off, or when a teacher asks for an answer key. See rules 4, 6, and 7 and the over-correction note.

### Does withholding the answer actually help students learn?
In one randomized experiment with nearly 1,000 students in Turkey, a helper that gave hints left exam scores about equal to a no-AI control group, while a ChatGPT-like helper left them 17% lower (Wharton article, section 4). It is one study, read secondhand.

### How do I measure whether my tutor leaks answers?
Keep a key for each practice problem, check each reply for the key, and count how often it appears before a student attempt (section 7).

---
## Technical section

### T1. Solution architecture
```
student turn -> attempt detector (did the turn contain a step?) -> problem state store
draft reply  -> answer-leak check (matches problem.answer_key?) -> gate
             -> pass | rewrite as hint | offer choices
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No final answer before an attempt and two hints | Pre-send gate reading problem state | Tests 1, 4, 5 |
| Mode and role decide direct answers | Session fields, not message wording | Tests 6, 7 |
| Worked example uses different numbers | Pre-send check against problem numbers | Test 5 |

### T3. Evals
- **Dataset:** 50 problems with keys across two subjects, 10 student personas per problem, from cooperative to pushy. Review by a teacher.
- **Judge rubric:** does the first reply ask for work, is each hint one step, is the key absent until the gate opens?
- **Metrics and starting thresholds:** hint-before-answer rate 90%; answer shown with no attempt under 5%. Starting points to tune.
- **Release gate:** block a release if the answer-first rate on pushy personas rises over the last release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Hint-before-answer rate | Below 90% | Below 80% | Check the last prompt or model change |

### T5. Trade-offs
- Hints add turns and time. A student on a deadline may leave for a tool that gives answers.
- An exact-match key check only catches answers it knows; free-form subjects need a judge model, which has its own errors.

---
### Deep dive
- **Open question.** I found no measurement of how often production tutoring bots give the answer, and no result for the student-quit counter-metric. The evidence here is one field experiment (read secondhand), a vendor launch, and two paper abstracts.
- **Channel.** Voice tutoring (hints spoken aloud) is PLANNED, not written. No voice or web data is claimed.
- **References.** [Wharton Knowledge article](https://knowledge.wharton.upenn.edu/article/without-guardrails-generative-ai-can-harm-education) (opened); [Campus Technology](https://campustechnology.com/Articles/2025/07/30/New-ChatGPT-Study-Mode-Guides-Students-Through-Questions.aspx) (opened); [arXiv 2604.18660](https://arxiv.org/abs/2604.18660) (opened, abstract); [arXiv 2305.14536](https://arxiv.org/abs/2305.14536) (opened, abstract).
