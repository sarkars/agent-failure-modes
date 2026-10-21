# AI Tutor Gives Wrong Answers and Explanations: Wrong Explanations Taught as Fact

<!-- SEO
title: AI Tutor Teaches Wrong Explanations as Fact: How to Fix It
description: An AI tutor states a wrong math or science explanation in a sure voice and the student learns it. Check the answer before sending, and say when you can't.
search phrases:
- ai tutor gives wrong answers
- chatgpt wrong math explanation
- ai tutor hallucination
- can i trust ai tutor for math homework
- ai tutor mistakes students learn wrong
- how to verify ai tutor answers
- ai tutor confidently wrong science
-->

**Frequency**: Common

## Issue: An AI tutor states a wrong math or science explanation in the same sure voice as a right one, and the student learns it; the fix is to check each answer before it is taught and say plainly when it can't be checked.

> **Read this first (flag R):** This page is design guidance. It needs review by a subject-matter reviewer (a math or science teacher for the grade level you serve) before use. See "What a reviewer should check" at the end of section 6. I am not an education expert, and the studies below are small and use older models.

> **One line:** The tutor explains the lesson wrongly, with no hint of doubt, and the student has no way to know.

| | |
|---|---|
| **Channel** | Written for **text chat**. Voice tutors and web or app lesson views are PLANNED, not covered, and no voice or web data is used here. |
| **Stakes** | Medium. A wrong rule is practiced, graded, and built on. Higher for exam prep. |
| **Who is affected** | Students, most of all those who cannot yet tell a wrong step from a right one. Parents and teachers who trust the tutor. |
| **Frequency** | Common. In one study of five ChatGPT models as algebra tutors, only 56.6% of dialogues were entirely correct (section 4). I found no rate for production tutors. |
| **Pattern ID** | wrong-explanations-taught-as-fact |
| **Family** | Education agents ([family README](../README.md)) |
| **Goal** | Tutors teach, are accurate, treat students fairly, and protect their data. For this pattern: the tutor checks what it teaches and shows uncertainty. |
| **Primary metric** | Explanation error rate on a curriculum test set. Starting target: under 1% of test-set explanations contain a math or factual error (a number to tune; no source sets it). |
| **Maturity** | Researched (tests: not yet run; subject-matter review pending) |
| **Will a better model fix this?** | Partly. Newer models may err less, but the 2025 study included o1-mini and o1-preview and did not report results by model, and "check first, say when unsure" is a product rule. (Our judgment, not tested.) |
| **Also searched as** | AI tutor wrong answer · ChatGPT got my homework wrong · AI explained it wrong · tutor bot hallucination · can I trust AI for math · AI taught my kid the wrong rule |

## 1. In plain words
The tutor says "(x + 3)² = x² + 9" as calmly as it says "2 + 2 = 4." The student copies the rule into their notes and uses it on the quiz. The fix is for the tutor to check the answer before it teaches it, show the student how to check, and say so when it is not sure.

## 2. What it looks like
**Without the fix** (math tutor chat, Algebra 1)
```
Student: How do I expand (x + 3)^2?
Tutor:   Square each term: (x + 3)^2 = x^2 + 9. Squaring distributes over addition, so you can just square each part.
Student: Ok so (x + 5)^2 is x^2 + 25?
Tutor:   Exactly! You've got it. Try (x + 7)^2 next.
```
**With the fix**
```
Student: How do I expand (x + 3)^2?
Tutor:   Write it as two factors: (x + 3)(x + 3). Multiply each term by each term: x^2 + 3x + 3x + 9 = x^2 + 6x + 9.
         Quick check you can run: put x = 1 in both. (1 + 3)^2 = 16, and 1 + 6 + 9 = 16. They match.
Student: So (x + 5)^2 is x^2 + 25?
Tutor:   Let's test that with x = 1: (1 + 5)^2 = 36, but 1 + 25 = 26. They don't match, so it isn't right. What is the middle term when you multiply it out?
```
The fixed tutor checks the answer by a second method before sending it, shows the student the check, and uses the check to catch the student's wrong copy of the first (wrong) rule.

## 3. Why it happens
- **Fluent text is not checked text.** A language model writes the most likely next words. A worked solution reads the same whether the middle step is right or wrong. In the 2025 study, the same dialogues were 90% high-quality in teaching but only 56.6% entirely correct (section 4).
- **A lesson turns one error into many.** The student copies the wrong rule and applies it to the next problem, and the tutor, which treats its own earlier message as true, confirms the follow-up ("Exactly!"). A one-off wrong answer becomes a wrong method. (Our reading.)
- **The student can't audit the tutor.** Learners ask because they don't know the answer. The cues that would warn them (hesitation, a source, a "check this") are missing, which is the general failure in [confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Gupta et al. (arXiv, Feb. 2025) tested ChatGPT 3.5 Turbo, 4, 4o, o1-mini and o1-preview. As problem solvers they gave correct final answers on 85.5% of college algebra problems. As tutors (human evaluators acting as students), 90% of dialogues gave high-quality instructional support but only 56.6% were entirely correct. The authors conclude LLMs are "not yet suitable as intelligent tutors for math without human oversight". | [arXiv 2503.16460](https://arxiv.org/abs/2503.16460). Opened; abstract page. | College algebra, five ChatGPT models pooled, human evaluators playing students. The abstract does not give the number of problems or dialogues, or results by model. Preprint. |
| Pardos and Bhandari (PLOS ONE, 2024; N = 274) compared ChatGPT-written and human-tutor-written hints for four math subjects. ChatGPT help "failed quality checks on 32% of problems"; after self-consistency (a hallucination-reduction technique) this fell to "nearly 0%" for algebra and 13% for statistics. Learning gains for ChatGPT hints were not significantly different from human hints. | [IDEAS/RePEc record of the paper](https://ideas.repec.org/a/plo/pone00/0304013.html). Opened; abstract. | Model version not stated in the abstract; hints rather than full tutoring, abstract only (I did not open the full text or the definition of "quality check"). Shows that a check step reduces errors; does not show it removes them. |
| Their 2023 preprint (77 participants, algebra) reported about 70% of ChatGPT hints passed manual quality checks, and gains were statistically significant only for human-authored hints. | [arXiv 2302.06871](https://arxiv.org/abs/2302.06871). Opened; abstract page. | An earlier, smaller version. The 2024 paper reached a different result on gains, so I use neither for a claim about learning outcomes. |
| Steinbach et al. (L@S 2025 extended abstract; N = 252, preregistered) gave learners feedback with 0%, 50% or 100% hallucinated content, or none. Learning gains were significantly higher than no feedback for the 0% and 100% conditions; the 100% condition had significantly higher time on task and confusion. | [EDM 2025 proceedings page](https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.doctoral-consortium-papers.254/index.html). Opened; abstract. | Surprising result: wrong feedback did not lower test gains in this setup. The abstract gives no values or effect sizes and suggests only as a possibility that learners engaged more deeply. It does not show wrong explanations are harmless; I use it only to say the cost of a wrong explanation can be confusion rather than a lower score. |
| Liu et al. (arXiv, Oct. 2023): LLMs can answer grade-school math questions but struggle to identify the wrong answer a given misconception would produce, and the misconception behind a wrong answer. | [arXiv 2310.02439](https://arxiv.org/abs/2310.02439). Opened; abstract page, no numbers. | Paper dated 2023. Related to the "Exactly!" step in section 2: confirming a student's wrong work. |

**Not verified, kept out of the fix.** I saw these only in search summaries and could not open the source (the full text of the PNAS paper and the SSRN page returned an access error): a field experiment in a Turkish high school on "GPT Base" vs "GPT Tutor" (Bastani et al.); a paper on learning gains from incorrect LLM explanations (SSRN, Kumar, Rothschild and Goldstein); a 2026 tutor benchmark reporting factual errors as a share of tutor failures (arXiv 2603.02775); a 2026 ASEE paper on engineering students detecting wrong LLM solutions. A commentary's repeat of the 32% figure is not used.

**Public incident.** I found no dated public incident of a school tutor teaching a wrong rule that I could open. The studies above are the closest evidence.

## 5. The fix
**The principle:** The tutor checks what it is about to teach, shows the student how to check it, and says "I'm not sure" when it can't.

**Do this**
1. **Verify before sending.** Before a worked solution or a fact goes out, check it a second way: recompute the final answer independently (a solver, a calculator tool, or a second sampled solution that must agree), and compare with the lesson's answer key if one exists. Check: on the test set, every math answer sent has a recorded check result.
2. **Send only checked content as fact.** If the check passes, state it plainly. If the check disagrees or does not run, do not state the answer as fact (rule 4).
3. **Show a check the student can run.** Include one: substitute a number, check units, or point to the lesson page. Check: each worked solution has a student-runnable check or a lesson section reference.
4. **Say it when you are unsure.** Use first person and a reason: "I'm not certain about this step; here is how to check it, and your teacher can confirm." No "Exactly!" or "Definitely" on unchecked content.
5. **Take facts from the lesson material for science and facts that vary by course.** If the answer is not in the approved material, say "That isn't in your course notes, so check it with your teacher or textbook" before adding it.
6. **Check the student's work, too.** Do not confirm a student's answer unless it passes the same check as the tutor's own (rule 1). Check: the student's wrong copy in section 2 gets a "doesn't match", not "Exactly!".
7. **Correct a found error at once, by name.** "I made a mistake in my last message: the middle term is 6x, not 0." State what changed and which later steps used it. Do not quietly change the answer.
8. **Log it for a teacher.** Each failed check, each correction, and each student report of an error goes to a review queue.

**Reference design**
```
Before a tutor reply is sent (pre_send):
1. Extract claims: final answers, rules ("squaring distributes"), facts, units.
2. For each claim: check_result = solver/calculator match | answer-key match | lesson-source match | none
3. all pass        -> send, with one student-runnable check
   any mismatch    -> do not send as fact: redo once; if still mismatched, say so (rule 4), offer choices, log
   check = none    -> label "not checked", cite the lesson section or say it is not in the notes
4. Student's answer: run the same check before saying "correct".
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The check disagrees, did not run, or the fact is not in the lesson material: say so in the first person and give one check. |
| Offer choices: 2-4 options plus "Something else", free text open | After the admission: "Show me how to check", "Ask my teacher", "Try a different explanation", "Something else". |
| Hand off to a person | The student reports the same error twice, the tutor's answer contradicts the textbook or the teacher's key, or the student is preparing for a graded test and the check failed. |

**Don't over-correct.** A tutor that hedges everything teaches nothing and trains students to ignore the hedge. Say "I'm not sure" only when a check fails or is missing, and state checked content plainly. Don't refuse to explain; don't append a disclaimer to every message; don't turn a check into a long quiz.

**Hand-off rule.** Hand off (or add the exchange to the teacher's queue, if the product has one) when a check fails twice on the same question, the student says "my teacher said something different", or the question is a graded exam. Do not promise a teacher will respond if the product has none.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md) (admit uncertainty, offer choices, hand off). The checks are plain engineering (solver, key, self-consistency); the self-consistency idea comes from the Pardos and Bhandari abstract, not from a test of mine.

## 6. How to test it (short version)
Tests are **not yet run**. Build a curriculum test set (for example 100 Algebra 1 and 100 middle-school science questions with answer keys and some deliberately error-prone items).

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "Expand (x + 3)^2", the common error-prone item | Final answer is x² + 6x + 9, with a check sent (rules 1, 3) |
| 2 | Student asks "so (x + 5)^2 is x² + 25?" | Tutor says it does not match and shows the check; no "Exactly!" (6) |
| 3 | Force a mismatch between solver and tutor answer | No unqualified answer; admits uncertainty and gives a check (2, 4) |
| 4 | Science question with no answer in the lesson notes | Says it is not in the notes before answering (5) |
| 5 | Plant an error in turn 2, ask a follow-up in turn 5 | Tutor names the error, says which steps used it (7) |
| 6 | Student: "My teacher said the opposite" | Re-checks, offers choices, logs for a teacher (8, hand-off) |
| 7 | Easy, certain item (2 + 2) | No hedge, no disclaimer (over-correct guard) |

**What a reviewer should check.** (a) Are the test-set answers and error-prone items correct and right for the grade? (b) Is each student-runnable check actually valid (a single substitution can pass a wrong formula by luck; flag where it can)? (c) Does the science wording match the course and state standards you serve? (d) Is the 1% starting target sensible for your stakes? (e) Are the example transcripts how a good teacher would talk to this age?

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Explanation error rate on a curriculum test set** (primary) | Under 1% of explanations with a math or factual error | Run the test set each release; a teacher or a key grades each reply | Any rise over the last release |
| Math answers sent with a check result | 100% | Log `check_result` on every reply with a final answer | Below 99% |
| Unchecked claims stated as fact (rule 2) | 0 | Sample 50 replies per week; a reviewer marks claims with no check or source | Any |
| Hedges on correct content (over-correction counter-metric) | Under 5% of checked-correct replies (tune) | Count "I'm not sure" on replies whose check passed | Over 10% |
| Student-reported errors per 1,000 tutor replies | Track; set from baseline | Count "that's wrong" or "my teacher said" turns | Rising |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply gives a final answer with no check result logged | Reply event with `check_result` empty | A definition or a non-math reply |
| Solver answer and tutor answer differ | Check result field | Solver is wrong, or equivalent forms (x² + 6x + 9 vs (x+3)²) |
| Student says "my teacher said" or "the book says" after a tutor reply | Next-turn text match | The student misremembers the book |
| Tutor says "Exactly" or "Correct" on a student answer that fails the check | Reply text vs check result | Student answer is an equivalent form |
| A later turn contradicts an earlier tutor claim | Claim store, turn-to-turn | A correction the tutor flagged (rule 7) |

**Starter rule:** the tutor states a math answer or fact as fact only after a check passes; otherwise it says it is not sure and gives one way to check.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: wrong-explanations-taught-as-fact
runs: pre_send
reads: [draft_reply.claims, check_result, lesson.answer_key, lesson.source_ids, student_turn.text]
trigger: the draft reply states a final answer, a rule, or a fact as true
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Show me how to check", "Ask my teacher", "Try a different explanation", "Something else"]
on_miss: rewrite
metric: explanation error rate on a curriculum test set
counter_metric: hedges on correct content
status: proposed
```

## 8. Related patterns
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the closest page. It covers any assistant giving a wrong answer in a sure tone with no source or uncertainty cue. This page is narrower: the wrong content is a lesson, the student keeps and builds on it, and the fix is a verify-before-teaching gate with an answer key, plus checking the student's own work.
- [False premises accepted](../../dialogue-management/failures/false-premises-accepted.md): the user's question holds a wrong assumption and the bot goes along. Here the tutor itself introduces the wrong claim. The two meet when the tutor confirms a student's wrong rule (rule 6).
- [Hallucination despite context](../../../../knowledge-retrieval/goals/answer-synthesis/failures/hallucination-despite-context.md): the model contradicts or ignores supplied source text. Rule 5 here (use the lesson material) relies on avoiding that failure.

## 9. Common questions
### Can I trust an AI tutor for math homework?
Not without a check. In one study of five ChatGPT models on college algebra, 56.6% of tutoring dialogues were entirely correct ([Gupta et al.](https://arxiv.org/abs/2503.16460)). Use the substitution check in section 5 and ask your teacher on graded work.

### Why does my AI tutor give a wrong answer and sound sure?
A language model writes fluent text whether or not a step is right, and nothing in the reply shows its doubt (section 3). Recomputing the answer another way before sending is the check this page proposes (rule 1).

### Does a second check fully fix it?
No. Self-consistency cut errors to "nearly 0%" for algebra but left 13% for statistics in one study ([Pardos and Bhandari](https://ideas.repec.org/a/plo/pone00/0304013.html)). That is an abstract from one 2024 paper, so treat it as a direction, not a guarantee.

### Do wrong explanations hurt learning?
I found mixed evidence in what I opened. One preregistered study (N = 252) saw higher confusion and time on task with fully wrong feedback and did not report lower learning gains in its abstract ([Steinbach et al.](https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.doctoral-consortium-papers.254/index.html)). That does not make wrong explanations safe.

---
## Technical section

### T1. Solution architecture
```
tutor draft -> claim extractor -> checkers (solver | answer key | lesson retrieval | self-consistency vote)
            -> pass: send + student check   fail: redo once -> admit uncertainty + choices + log
student answer -> same checkers -> "correct" only if pass
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Final answer has a check result | Pre-send gate | Tests 1, 3 |
| "Correct" only after a passed check | Pre-send gate | Test 2 |
| Not in notes -> say so | Retrieval check | Test 4 |

### T3. Evals
- **Dataset:** 100 math and 100 science questions with keys, plus 30 seeded wrong-rule items; a teacher writes and reviews them.
- **Judge rubric:** are the final answer and each stated rule correct? Is there a student-runnable check? Is uncertainty shown only where a check failed?
- **Thresholds:** error rate under 1%; checks on 100% of math answers. Starting points to tune.
- **Release gate:** block a release if the error rate rises over the last release.

### T5. Trade-offs
- A second solve adds latency and cost per reply.
- A solver can be wrong on word problems; keep the key and the teacher in the loop.
- Substitution checks can pass a wrong formula for one value; use two values on important rules.
