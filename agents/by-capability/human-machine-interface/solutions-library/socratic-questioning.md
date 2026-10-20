# Tutor Bot Just Gives the Answer? Guide Learners With Socratic Questions

## The problem
A student types the homework question, and the tutor bot replies with the answer. The homework gets done, but nothing has been learned.

**This page is for you if** a tutor or learning bot should help people think, not hand over answers.

> Status: **framework.** No rule check yet; guiding versus telling needs an AI judge.

## The framework that fixes it
Socratic questioning is a teaching method of disciplined questions that help a learner examine ideas. Richard Paul, a critical-thinking scholar, grouped Socratic questions into six types: questions for clarification, about assumptions, about reasons and evidence, about viewpoints and perspectives, about implications and consequences, and about the question itself. For a tutor bot, the method is a guard against the easiest failure: solving the homework. A good Socratic turn asks one question that moves the learner one step closer.

## The question types
| Type | Purpose | Tutor example (algebra) |
|---|---|---|
| Clarification | What exactly do you mean? | "What does x stand for here?" |
| Assumptions | What are you taking for granted? | "Why did you assume both sides stay equal?" |
| Reasons and evidence | How do you know? | "How can you check that x = 4?" |
| Viewpoints | How else could this be seen? | "Is there another way to isolate x?" |
| Implications | What follows? | "If x = 4, what's 2x + 3?" |
| The question | Why does this question matter? | "Why do we want x alone?" |

## How to use it in a bot
1. Ask one question per turn, pitched at the step the learner is stuck on.
2. After two failed attempts, give a hint, then a worked step; don't let the learner stall.
3. Don't use it on users who need a fast fact; offer: "Want a hint or the answer?"
4. For children, keep questions concrete and short.

## Worked example
```
Student: solve 2x + 3 = 11
Bot (answer):   x = 4.
Bot (Socratic): What could you do to both sides to get rid of the + 3?
```

## What the checker flags
No rule check yet. Whether a tutor guided instead of giving the answer away needs an AI judge.

## Limits
- Endless questioning frustrates; pair with clear hints.

## Source
- Saint Mary's University Studio, [Socratic questions](https://studio.smu.ca/socratic-questions), citing Paul, R. (1990), *Critical Thinking* (secondary). That page shows the clarification, assumptions and evidence types in full; the other three types in the table are as commonly listed from Paul's work and were not confirmed on a page opened for this one.

## Related
- [Teach-back](teach-back.md)
- [GROW coaching](grow-coaching.md)
- [All frameworks](README.md)
