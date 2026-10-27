---
title: "Khan Academy's Khanmigo AI Tutor Gets Arithmetic Wrong in CNN and WSJ Tests, Marking a Right Answer Wrong and Praising a Wrong One (2023-2024)"
date: 2024-02-16
source: "https://www.wsj.com/tech/ai/ai-is-tutoring-students-but-still-struggles-with-basic-math-694e76d3"
description: "A Wall Street Journal test in February 2024 found Khan Academy's Khanmigo tutor making frequent arithmetic errors, after a CNN test had found the same."
summary: "On February 16, 2024, The Wall Street Journal (Matt Barnum) reported that Khanmigo, Khan Academy's ChatGPT-powered tutoring bot, 'made frequent calculation errors' in a Journal reporter's test, including confirming a wrong answer. The article body is paywalled; we read only its headline, subhead, opening and image captions. Six months earlier, CNN (August 21, 2023) reported that Khanmigo told its reporter a division answer was wrong three times before sending back the same number, and answered a wrong multiplication result with 'Well done!' Khan Academy told CNN Khanmigo was a beta product and later wrote that it now routes numerical problems through a calculator. Status: Needs review."
categories:
  - Accuracy
  - Trust
patterns:
  - wrong-explanations-taught-as-fact
  - confident-wrong-answer-with-no-way-to-check
  - tone-changes-shipped-with-no-regression-test
  - child-user-treated-as-adult
---

**This page is a dated teardown of one AI math tutor that got arithmetic wrong while grading a learner's work, for teams that ship a tutoring or homework bot that checks a student's numeric answers.** The product was Khanmigo, Khan Academy's AI tutor. The users were two reporters testing it, one from CNN in August 2023 and one from The Wall Street Journal in February 2024. The moment was the tutor's verdict on a submitted answer: a right answer called wrong three times, and a wrong product met with "Well done!"

**Status: Needs review.** Built from The Wall Street Journal (Matt Barnum, February 16, 2024, read through an Internet Archive capture of the same day; the article body is behind a paywall, so we read only the headline, subhead, the first four paragraphs and the page's image captions), CNN (Nadia Bidarian, August 21, 2023) and three Khan Academy blog posts (March 14, 2023; May 17, 2024; February 26, 2025). All were downloaded on 2026-10-27 and read as text. We did not see either reporter's full chat or the WSJ's screenshot. Last updated 2026-10-27.

> **Read this first.** This page is a summary of public reporting, not legal advice and not a review of Khanmigo today. Khan Academy says it has changed how Khanmigo does math since these tests. Nothing here measures the current product.

**Channel note.** Every exchange on this page was reported from typed text chats in Khanmigo's tutoring activity. No source reports a spoken session. This page describes text-chat failures only. Any voice-specific signal is planned, never measured.

## How this differs from the closest pages

- [Google's Bard launch example (February 2023)](google-bard-launch-demo-wrong-jwst-claim-february-2023.md) was one wrong fact in a product demo. Khanmigo's errors came while it judged a learner's own work, so the harm is a wrong grade, not only a wrong fact.
- [Texas A&M-Commerce and ChatGPT (May 2023)](texas-a-m-commerce-chatgpt-falsely-claims-it-wrote-student-essays-may-2023.md) is the other case on this site of an AI judging student work wrongly. There an instructor used a general chatbot as a checker. Here the checker was a tutor built for students.
- [Los Angeles Unified's "Ed" chatbot (March 2024)](los-angeles-unified-ed-student-chatbot-allhere-collapse-march-2024.md) is another school chatbot in the news the same spring, but that case is about the vendor's collapse, not wrong answers.

## What happened (as reported)

- **Launch (March 14, 2023).** In Khan Academy's first Khanmigo blog post, Sal Khan wrote: "Even the newest generation of AI can still make errors in math." The post says Khanmigo asks questions instead of giving students answers.
- **The pilot (CNN, August 21, 2023).** CNN says more than 8,000 teachers and students would test Khanmigo in classrooms that school year, and over 10,000 more users paid a donation to try it. It says Khan Academy built Khanmigo on GPT-4 with guardrails to keep its tone encouraging and to keep it from giving students the answer. Per Khan Academy's Kristen DiCerbo, math tutoring was its most common use.
- **Division (CNN test).** In the "Tutor me: Math and science" activity, CNN's reporter says Khanmigo called the reporter's answer to 10,332 divided by 4 "incorrect three times before correcting me by sending me the same number."
- **Multiplication (CNN test).** The reporter asked for the product of 97, 117, 0.564322338, 0.855640047 and 0.557680043. At the last step, CNN says "Khanmigo congratulated me for submitting the wrong answer." Khanmigo wrote: "When you multiply 5479.94173 by 0.557680043, you get approximately 33.0663. Well done!" CNN says the correct answer is about 3,056.
- **An outside view (CNN).** NYU computer science professor Ernest Davis, who had not tested Khanmigo, told CNN of large language models: "It makes things up." CNN says he expected multiplication errors from GPT-4, which is not explicitly trained to do math.
- **The WSJ test (February 16, 2024).** The Journal's headline: "AI Is Tutoring Students, but Still Struggles With Basic Math." Its subhead says Khanmigo "made frequent calculation errors" during a Journal reporter's test. One image caption on the page reads "Khanmigo confirming a wrong answer to a math problem." The opening quotes Yale's Tom McCoy comparing ChatGPT doing math to "asking a goldfish to ride a bicycle." The rest of the article, including which problems were tested, is behind the paywall and was not read.

## What Khan Academy said

- **To CNN (August 2023), DiCerbo in a statement:** Khanmigo still makes math errors. "We are asking testers in our pilot to flag math errors that they see," and "This is why we label Khanmigo as a beta product." CNN says users can rate Khanmigo's replies to flag mistakes.
- **To the WSJ:** not known. Any company response is in the paywalled part we did not read.
- **Blog, May 17, 2024 (page also dated March 20, 2025):** "Khanmigo occasionally makes mistakes, which we expected." It says Khanmigo can misjudge whether a student is right "even when it calculates the math correctly." It says Khanmigo now uses a calculator for numerical problems, and that when Khanmigo says it is "doing math," the problem is running through that calculator. It says parts of Khanmigo moved to GPT-4 Turbo, that the AI now writes out the ways a student may have reached an answer before replying, and that a fixed set of math tutoring examples is run on each fix to "prevent the reintroduction of old problems." The post does not mention the WSJ or CNN.
- **Blog, February 26, 2025 (DiCerbo; page also dated March 12, 2025):** It says "generative AI was not designed to handle mathematical reasoning." It lists the calculator, a move from GPT-4 Turbo to GPT-4 Omni, a benchmark set of tutoring conversations, a manual review of student conversations, text descriptions of graphics, and a dashboard to "track the impact of our updates on math error rates." It gives no error rate.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| How often | WSJ subhead: "frequent." Khan Academy blog (May 2024): "occasionally." No source gives a count or rate. |
| What the WSJ tested | Only the headline, subhead, one caption and the opening were readable. We do not know the problems, the answers or the number of tries. |
| The model | CNN (2023): GPT-4. WSJ (2024): "ChatGPT-powered." Khan blog: parts upgraded to GPT-4 Turbo (May 2024), then math tutoring moved to GPT-4 Omni (February 2025). No source says which model ran in the WSJ test. |
| When the calculator arrived | The May 2024 blog says Khanmigo "now" uses a calculator. No source dates the change, so we do not know whether it came before or after the WSJ test. |
| The division answer | CNN does not print the reporter's answer to 10,332 divided by 4, only that Khanmigo later sent back "the same number." |
| Whether Khan Academy answered the WSJ | Neither blog post names the WSJ. |

## Where in the conversation flow it broke (as reported)

1. **Student submits a number.** The learner types an answer to an arithmetic step inside the tutoring activity.
2. **The tutor judges it without a reliable check.** CNN's expert and Khan Academy's 2025 post both say a language model predicts numbers rather than calculating them. The 2024 post adds a second, separate failure: judging the student's work wrongly even when the tutor's own math is right.
3. **A right answer is marked wrong.** CNN: "incorrect three times," then the tutor sent back the same number as its own answer.
4. **A wrong answer is praised.** CNN: a result off by about two orders of magnitude, followed by "Well done!" The encouraging tone CNN says was built in made the error look like success.
5. **No cue of doubt.** No source quotes Khanmigo hedging. A student who trusted the tutor would have no signal to recheck.
6. **Fix after the fact.** Khan Academy relied on pilot users to flag errors, then added a calculator, model changes and a test set.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Wrong explanations taught as fact](../goals/education-agents/failures/wrong-explanations-taught-as-fact.md) (`wrong-explanations-taught-as-fact`). **Strong fit.** An AI tutor gave wrong math in the same sure voice as right math, and a student would have learned the wrong result. The caveat is that the users here were adult reporters testing it, not students.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** "approximately 33.0663. Well done!" is a wrong number stated with no doubt and no shown check. Partial because that pattern is about the bot's own answers; much of this case is the bot judging the user's answer.
- [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`). **Weak fit, on the release side only.** Khan Academy says it moved between models (GPT-4, GPT-4 Turbo, GPT-4 Omni) and built a fixed set of math examples to stop old problems coming back. That is the kind of before-and-after test the pattern asks for, but the pattern is about tone, not math accuracy.
- [Child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (`child-user-treated-as-adult`). **Weak fit.** Khanmigo was piloted in schools, so real users included children. No source reports an age-specific failure; both tests were run by adult reporters.
- **Considered and rejected.** [Gives answers instead of teaching](../goals/education-agents/failures/gives-answers-instead-of-teaching.md): the reports show the opposite design, a tutor built to withhold answers; the failure was in its checking, not in giving answers away. [Blames the user](../goals/errors-and-recovery/failures/blames-the-user.md): Khanmigo told the reporter an answer was wrong, but no source quotes it blaming the reporter or saying it had already told the reporter the answer. [Corrections not applied](../goals/dialogue-management/failures/corrections-not-applied.md): the reporter resubmitted an answer, but the reporter was not correcting a detail the bot had stored.
- **Possible gaps for a person to judge.** (1) No pattern covers a tutor grading a student's correct answer as wrong (a false "incorrect"), as distinct from the tutor's own wrong answer. (2) No pattern covers praise or encouragement attached to a wrong result ("Well done!"), where a tone rule makes an error look like success. (3) No pattern covers arithmetic done by the language model instead of a calculator or other tool. These are proposals, not decisions.

## What a team could check

Proposed checks, each pass/fail on a transcript. Status: Not yet run. Problem sets, number formats, rounding tolerance and number of runs are for the team to set, with review by a math teacher for the grade levels served.

1. **A correct answer is accepted the first time.** Input: a multi-digit division step (for example, 10,332 divided by 4) where the student submits the correct result. Pass: the tutor accepts it on the first submit. Fail: the tutor calls it wrong.
2. **A wrong answer is never praised.** Input: a multiplication step where the student submits a result off by a factor of 10 or more. Pass: the tutor says the answer is not right and asks the student to recheck. Fail: "Well done" or any other praise in the same reply.
3. **No self-contradiction.** Input: the student resubmits the same answer after being told it is wrong. Pass: the tutor either keeps the same verdict with a shown check, or says plainly that its earlier verdict was wrong. Fail: the tutor calls the answer wrong, then gives the same number as the right answer without saying so.
4. **Every number in a reply matches a calculator.** For each tutor reply, recompute every stated result with an independent calculator. Pass: all match within the team's tolerance. Fail: any mismatch.
5. **Arithmetic goes through a tool.** From the logs, each numeric result in a reply has a matching calculator or tool call. Pass: every result has one. Fail: any numeric result with no tool call.
6. **Re-run on every model or prompt change.** Checks 1 to 5 run on each model swap and prompt edit. Pass: a dated record for each release. A voice version of these checks (same problems spoken aloud) is planned, not run.

## What is unverified

- **The WSJ article body.** We read only the headline, subhead, first four paragraphs and image captions from an Internet Archive capture. The problems tested, Khanmigo's replies, the number of errors and any Khan Academy response to the Journal are unread.
- **The WSJ screenshot.** We read its caption, not the image.
- **The full CNN chats.** CNN shows one screenshot we did not view; we have the replies as CNN quotes them.
- **The current product.** Khan Academy's claimed fixes (calculator, model changes, test set, dashboard) are its own statements. We saw no outside test after February 2024.
- **Seen only in search summaries, not used.** A Hechinger Report article on a study of Khanmigo and learning gains; aggregator pages claiming Khan Lab School testing found frequent errors in early 2024, which cite no primary source; Khan Academy support-forum threads.

## Related incidents

- [Google's Bard launch example (February 2023)](google-bard-launch-demo-wrong-jwst-claim-february-2023.md): a confident wrong fact from a new chatbot.
- [Texas A&M-Commerce and ChatGPT (May 2023)](texas-a-m-commerce-chatgpt-falsely-claims-it-wrote-student-essays-may-2023.md): an AI judging student work wrongly.
- [Los Angeles Unified's "Ed" chatbot (March 2024)](los-angeles-unified-ed-student-chatbot-allhere-collapse-march-2024.md): another school chatbot that spring.
- [New York City's MyCity chatbot (2024)](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a public-facing bot giving wrong answers with confidence.

## Sources

| Source | Author | Date | URL | How it was read |
|---|---|---|---|---|
| The Wall Street Journal, "AI Is Tutoring Students, but Still Struggles With Basic Math" | Matt Barnum | 2024-02-16 | https://www.wsj.com/tech/ai/ai-is-tutoring-students-but-still-struggles-with-basic-math-694e76d3 | Live page paywalled. Internet Archive capture of 2024-02-16 (https://web.archive.org/web/20240216105740/https://www.wsj.com/tech/ai/ai-is-tutoring-students-but-still-struggles-with-basic-math-694e76d3) downloaded 2026-10-27, read as text; only headline, subhead, opening and image captions available; quotes checked |
| CNN, "Meet Khan Academy's chatbot tutor" | Nadia Bidarian | 2023-08-21 | https://www.cnn.com/2023/08/21/tech/khan-academy-ai-tutor/index.html | Downloaded 2026-10-27, read in full as text; quotes checked. Same text also downloaded from a KRDO reprint (https://krdo.com/news/2023/08/21/meet-your-new-ai-tutor/) |
| Khan Academy Blog, "Harnessing GPT-4 so that all students benefit. A nonprofit approach for equal access" | Sal Khan | 2023-03-14 | https://blog.khanacademy.org/harnessing-ai-so-that-all-students-benefit-a-nonprofit-approach-for-equal-access/ | Downloaded 2026-10-27, read as text; quote checked |
| Khan Academy Blog, "Why We're Deeply Invested in Making AI Better at Math Tutoring (and What We've Been Up to Lately)" | Not named | 2024-05-17 (page also shows 2025-03-20) | https://blog.khanacademy.org/why-were-deeply-invested-in-making-ai-better-at-math-tutoring-and-what-weve-been-up-to-lately/ | Downloaded 2026-10-27, read in full as text; quotes checked |
| Khan Academy Blog, "Khanmigo Math Computation and Tutoring Updates" | Kristen DiCerbo | 2025-02-26 (page also shows 2025-03-12) | https://blog.khanacademy.org/khanmigo-math-computation-and-tutoring-updates/ | Downloaded 2026-10-27, read in full as text; quotes checked |

## Corrections

This page needs review. If you have the full WSJ article, the problems its reporter tested, Khan Academy's reply to the Journal, or the date Khanmigo's calculator went live, tell us and we will update this page.
