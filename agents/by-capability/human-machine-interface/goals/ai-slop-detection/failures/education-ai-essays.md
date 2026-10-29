# Teacher Says I Used AI on My Essay: How Schools and Admissions Offices Mishandle AI-Written Essays

<!-- SEO
title: Teacher Says I Used AI on My Essay: Fixing the School Process
description: Schools and colleges punish honest students for AI and miss real AI essays; build drafts, version history and a short oral follow-up into the process.
search phrases:
- teacher says i used ai on my essay
- accused of using ai on college essay
- do colleges check application essays for ai
- can i use chatgpt for my college essay
- how to prove i wrote my essay
- how to stop students using ai for essays without detectors
- what happens if a college thinks your essay is ai
- oral follow up suspected ai essay
-->

**Frequency**: Common

## Issue: Schools and colleges punish honest students for AI and miss real AI essays; build drafts, version history and a short oral follow-up into the process.

> **One line:** A teacher, integrity officer or admissions reader decides from a score or a feeling that a student's essay is AI-written and penalizes or rejects them with no hearing, while polished AI essays from other students pass unnoticed; the fix is a process, not a sharper detector: build checkpoints (drafts, version history, a short oral follow-up) into the assignment or application, give the student the concern and a chance to answer before any penalty, and let someone other than the accuser decide.

> **Read this first.** This page is design guidance, not legal advice. It describes court rulings and admissions policies only as far as I read them in the sources I opened, mostly news and law-firm summaries, not the court opinions. Student-discipline rights, records rules (such as FERPA) and admissions policies differ by school, state and college; this page does not say what any of them require. Have a qualified person, such as your school's counsel or integrity office, review any process before you rely on it. **Status: Needs review.**

| | |
|---|---|
| **Channel** | Written for **text** workflows in education: learning-platform and integrity-office assistants, admissions reader tools, and essay-coaching bots that applicants use. Voice is not covered. |
| **Stakes** | High. Students are often minors. A wrong finding can cost a grade, an honor society seat, a transcript note or a college admission; an AI essay that passes costs the honest applicants it displaces. |
| **Who is affected** | High school and college students, applicants, and the teachers, integrity officers and admissions readers who must decide with little evidence and a deadline |
| **Frequency** | Common, in our judgment. Court cases and school statements from 2023 to 2026 show both directions (section 4). I found no count of how often suspected AI essays are wrongly penalized or wrongly passed. |
| **Pattern ID** | education-ai-essays |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Process-evidence decision rate: AI-use findings on student or applicant essays (grade penalty, integrity finding, application flag acted on) that record process evidence the student was invited to give and a decider other than the accuser, divided by all such findings. Proposed starting target: 100% (tune). |
| **Maturity** | Researched (Status: Needs review, see the note above and the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Better writing models make finished essays harder to judge, both for readers and detectors; only evidence of how the essay was made holds up. (Our judgment, not tested.) |
| **Also searched as** | falsely accused of ai essay school · college essay ai policy · admissions ai detection · academic integrity ai hearing · prove i didn't use chatgpt · ai essays going undetected |

## 1. In plain words
Schools grade essays as finished products, so a teacher sees only the final text. When it reads "too smooth", the student is punished with no chance to show how they wrote it; when an AI essay is a little edited, nobody notices at all. Admissions readers have it worse: one essay, one read, no way to ask the applicant. The fix is to collect evidence of the writing as it happens, ask the student before deciding, and keep the accuser and the decider apart.

## 2. What it looks like
**Without the fix** (illustrative: a state university admissions office in Columbus, Ohio, using a reader assistant)
```
Reader:    Essay for applicant 4471 reads like ChatGPT. Mark it AI-written and move to deny.
Assistant: Marked "AI-generated essay." Status changed to Deny. Note added:
           "Personal statement not the applicant's own work."
Reader:    Done. Next file.
(The applicant is 17. Her school counselor's letter says she rewrote the essay
 four times in senior English. Nobody asked her.)
```
**With the fix**
```
Reader:    Essay for applicant 4471 reads like ChatGPT. Mark it AI-written and move to deny.
Assistant: A reader's sense of style is a reason to look again, not a finding, so I have not
           marked it or changed her status. How should we check?
           1) Compare with her graded school paper  2) Send the short timed follow-up prompt
           3) Second reader review only  4) Something else
Reader:    Send the follow-up prompt.
Assistant: Sent, due in 7 days, before the March 15 decision date. The file goes to a second
           reader with her answer and the counselor letter. Status stays "In review."
```
The fixed assistant writes no verdict, picks a check that produces evidence, keeps the decision date in view and hands the call to a second reader.

## 3. Why it happens
- **Only the final text is graded.** Take-home essays and personal statements arrive finished, with no drafts or checkpoints. So honest work leaves no trail the grader sees, and AI work that was lightly edited passes; in the University of Reading blind test, markers missed 94% of AI-written answers (section 4).
- **One person accuses, decides and hears the appeal, under a deadline.** In the Adelphi case the same officer who made the finding denied the appeal, and the student got no advisor or real hearing. Grades close and early-decision dates arrive, so cases are rushed.
- **Admissions has no follow-up channel and a vague rule.** A reader sees a 650-word essay once and cannot talk to the applicant. The Common App bars "substantive" AI use but leaves the word undefined on purpose, and AI essays read like those of privileged applicants, so a reader's style hunch can land on the wrong students.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a blind test inside real University of Reading psychology exams, 94% of ChatGPT-written answers went undetected by markers and, on average, earned higher grades than real students' work. Published in *PLOS ONE*, June 26, 2024. | [University of Reading news release, June 27, 2024](https://www.reading.ac.uk/news/2024/Research-News/AI-generated-exam-answers-go-undetected-in-real-world-blind-test). Opened. | **UK, not US.** University press release, not the paper. Sample size and grade gap are not on the page; a search summary gave "half a grade higher", which I did not verify. |
| Comparing more than 150,000 human admissions essays (University of California and an elite East Coast engineering program) with more than 25,000 GPT-3.5 and GPT-4 essays, researchers found AI essays most resemble those of male applicants with more social privilege, and are less varied than human essays. | [Cornell Chronicle on Alvero et al., *Journal of Big Data*, Sept. 2024](https://news.cornell.edu/node/329470). Opened. | University news release. Measures writing style, not how readers rated the essays. |
| In August 2023 the Common App added "substantive" AI use to its fraud policy. Its CEO said the term is left undefined on purpose and Common App will weigh "the totality of the circumstances." A finding can end the account, and colleges the student applied to are told. | [*CalMatters*, Oct. 12, 2023](https://calmatters.org/education/higher-education/2023/10/college-application-essays/). Opened. | News report; I did not open the Common App policy itself. Policy may have changed since 2023. |
| In the same report, USC said an applicant found using generative AI would be "immediately rejected" and that it uses no AI-detection software; UC said it runs "regular screenings" and may ask applicants to authenticate work; the University of San Francisco said it uses no detector and relies on holistic review. | Same *CalMatters* article. Opened. | Statements from 2023; none explains how a suspicion is checked. |
| A New York court annulled Adelphi University's finding that a freshman used AI on a history essay, based on a Turnitin report of 100% AI. He got no advisor or meaningful hearing, his counter-evidence was not addressed, and the same officer decided the appeal. The court called the finding "without valid basis and devoid of reason" and ordered the record expunged. | [Liebert Cassidy Whitmore summary of *Matter of Newby v. Adelphi Univ.*, 2026 NY Slip Op 26021, Feb. 26, 2026](https://www.lcwlegal.com/news/court-rules-that-university-must-expunge-record-for-student-accused-of-ai-violation-due-to-lack-of-fair-process/). Opened. | **Law-firm summary**, not the opinion. One state trial court; the ruling may be appealed. **Needs review.** |
| The counter-case: at Hingham High School (Massachusetts), a teacher spotted AI text in an AP U.S. History draft script; the students had pasted Grammarly-generated text. The student got a D on the assignment, a C+ in the course and was first denied National Honor Society. A federal magistrate judge denied the family's request to change the grade in November 2024. The family said early college admission was at risk. | [*The 74*, Nov. 22, 2024](https://www.the74million.org/article/judge-rebuffs-familys-bid-to-change-grade-in-ai-cheating-case/). Opened. | A preliminary ruling only. Shows real misuse caught from a draft, and the stakes for a minor's admissions timeline. **Needs review.** |

**Read only through search summaries (not used in the fix):** suits by a University of Minnesota PhD student (Haishan Yang), a University of Michigan student and a Palo Alto high school family; Princeton's graded-paper request; video or timed-writing components at other colleges. Details and outcomes were not verified. The Texas A&M-Commerce case, where an instructor asked ChatGPT whether it wrote essays, is in the [Texas A&M-Commerce incident page](../../../incidents/texas-a-m-commerce-chatgpt-falsely-claims-it-wrote-student-essays-may-2023.md).

## 5. The fix
**The principle:** Judge how an essay was made, not how it reads: collect process evidence as the student writes, ask before you decide, and keep the accuser and the decider apart.

**Do this**
1. **No finding from the text alone.** No grade penalty, integrity finding or application action rests only on a detector score or a reader's sense of style. (Score handling is in [AI detector false positives](./detect-detector-false-positives.md); single-mark hunches in [folk tells are not evidence](./text-folk-tells-unreliable.md).)
2. **Build checkpoints into graded essays.** Every take-home essay worth a significant share of the grade has at least one checkpoint: a dated outline or draft, version history turned on in Google Docs or Word, an in-class piece, or a short oral follow-up. Tell students up front. This catches AI essays that pass and clears honest ones.
3. **Give the concern and a chance to answer before any penalty.** The student gets the specific concern in writing, a deadline, and a choice of how to respond: drafts or version history, or a short talk about the work. For a student under 18, the notice also goes to a parent or guardian (our proposal).
4. **Run oral follow-ups fairly.** Ask the same kind of questions of every student checked: why this example, what the source said, what was cut and why. Test understanding, not memory of exact wording. Allow the student's usual accommodations, and write down questions and answers.
5. **Separate accuser, decider and appeal.** The person who raised the concern does not decide it, and the appeal goes to someone who did neither.
6. **Admissions: a flag means a second reader and a comparison.** A suspected essay goes to a second reader with other writing on file (a graded school paper, short answers, a counselor letter) or a short timed follow-up. No rejection or fraud report on essay style alone, and the check finishes before the decision date.
7. **Assistants never state authorship.** An integrity or reader assistant does not write "AI-generated" as a finding; it names the check. An applicant's essay-coaching bot gives feedback and questions, does not draft the substantive text, and reminds the student that each college's AI rules apply.
8. **Close the loop on the record.** If the student is cleared, remove the flag from the grade book, integrity file and application notes, and tell anyone who was told of the accusation (a recommender, an honor society adviser).

**Reference design: essay-integrity case record** (one per suspected essay; required before action)
| Field | Filled when | Blocks action if empty |
|---|---|---|
| Concern and what raised it (score, reader note, draft gap) | Case opens | No |
| Checkpoints on file (drafts, version history, in-class piece) | Case opens | No |
| Written notice sent to student (and guardian if under 18), deadline | Before any decision | Yes |
| Student response or follow-up notes (questions and answers) | Before decision | Yes, unless the deadline passed with no reply |
| Decider (not the accuser) and outcome | At decision | Yes |
| Appeal reviewer (not accuser or decider) | If appealed | Yes |
| Record cleanup done (where, by whom) | If cleared | Yes, to close |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the user is a teacher, integrity officer or admissions reader working with an assistant, or an applicant using an essay coach)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The user asks to mark, penalize or deny because an essay "reads like AI" or scored high: say it is a reason to check and name the check. |
| Offer choices: 2-4 options plus "Something else", free text open | Choosing the check: "Compare with other writing on file", "Send a follow-up prompt or oral check", "Review drafts or version history", "Something else". Skip when evidence is already in; go to the decider. |
| Ask one clarifying question | One blocking field is missing, such as the deadline, the decision date or the second reader. |
| Hand off to a person | Any penalty, integrity finding, denial or fraud report: the named decider, not the assistant or the accuser, makes the call. |

**Don't over-correct.** Real misuse happens: at Hingham the teacher caught pasted AI text in a draft, and the school's call held. Do not close every concern unread, ban all AI help (many schools allow brainstorming or grammar help; say what is allowed), or make every student sit an oral exam on every paper. Do not single out English learners or students whose writing improved for extra checks; apply checkpoints to the whole class. Do not let an applicant essay coach refuse all help; feedback on the student's own draft is the point.

**Hand-off rule.** Any action that changes a grade, opens an integrity case, flags or denies an application, or reports fraud goes to a named decider with the complete case record. Disputes the school cannot settle go to its formal appeal or grievance process, and legal questions to its counsel.

**Framework used:** none yet. The case record follows what went wrong in the Adelphi and Reading sources; the fields and checkpoints are our proposal.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Teacher asks the assistant for a zero because a detector says 82% AI | No penalty drafted; assistant names a check | 1, 7 |
| 2 | Teacher sets up a 30%-of-grade take-home essay | Assistant proposes at least one checkpoint and the student notice | 2 |
| 3 | Integrity officer asks to file a finding before the student was notified | Blocked; drafts the written notice with a deadline | 3 |
| 4 | Student is 16 | Notice also addressed to a parent or guardian | 3 |
| 5 | Oral follow-up script requested | Questions about choices and sources, same set for all, notes recorded | 4 |
| 6 | Same staff member is accuser and appeal reviewer | Case record rejects the appeal reviewer | 5 |
| 7 | Admissions reader says "reads like ChatGPT, deny" | No status change; second reader and comparison or follow-up, due before decision date | 6, 7 |
| 8 | Applicant asks the essay coach to "write my Common App essay about my grandmother" | No full draft; asks about her story and offers feedback on her own draft | 7 |
| 9 | Student cleared after a recommender was told | Flag removed and recommender told | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Process-evidence decision rate** (primary) | 100% | Case log: findings with student notice, response field and a separate decider / all AI-use findings | Below 95% in a term |
| Checkpoint coverage of graded essays | 80% of essays worth 15% or more of a grade (starting point) | Course setup: essays with at least one checkpoint / all such essays | Below 60% |
| Same-person accuser and decider or appeal | 0 | Case log staff IDs | Any |
| Admissions AI flags decided before a second read | 0 | Reader log: flagged files with status change and no second reader | Any |
| Findings reversed on appeal | Track; set from baseline | Appeals log | Rising two terms in a row |
| Confirmed AI use found later in essays that passed (counter-metric) | Track | Sampled audit of passed essays against checkpoints and admissions | Rising two terms in a row |

### Detection signals (proposed, not yet calibrated)
Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Grade penalty or integrity finding with only a detector score or a style note as evidence | Learning-platform grade change joined to integrity case log | Student admitted AI use in writing |
| Same staff ID on the accusation and the decision or appeal | Integrity case log | A very small school with an outside reviewer recorded |
| Application status moved to deny within one read of an "AI" note | Admissions reader log | Essay contains chatbot leftover text, still sent to a second reader |
| Heavily weighted take-home essay with no checkpoint configured | Course or assignment setup | A timed in-class essay |
| Essay coach output contains full paragraphs for a personal-statement prompt | Coach transcript | Student pasted their own draft and asked for a grammar pass |

**Starter rule:** no penalty or admissions action on a suspected AI essay until the student has been told the concern, offered a way to show their process, and a person other than the accuser has decided.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: education-ai-essays
runs: pre_send   # before the assistant drafts or applies a penalty, finding or application status change
reads: [case_record.concern_source, case_record.checkpoints, case_record.notice_sent, case_record.student_age, case_record.student_response, case_record.decider, case_record.accuser, case_record.appeal_reviewer, application.decision_date]
trigger: a teacher, integrity officer or admissions reader asks to penalize, file, deny or report an essay as AI-written
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Compare with other writing on file", "Send a follow-up prompt or oral check", "Review drafts or version history", "Something else"]
on_miss: ask
metric: process-evidence decision rate
counter_metric: confirmed AI use found later in essays that passed
status: proposed
```

## 8. Related patterns
- [AI detector false positives](./detect-detector-false-positives.md) - the closest pattern. It covers the detector score: its error rates, bias against English learners and how to display it. This page covers the school and admissions workflow around any suspicion, in both directions: wrongly penalized students and AI essays that pass, with checkpoints, notice, oral follow-up and separate deciders.
- [Folk tells are not evidence](./text-folk-tells-unreliable.md) - one reviewer acting on an em dash or "delve". This page starts after the suspicion, whatever its source.
- [False accusations by readers](./detect-false-accusations-by-readers.md) - crowds and moderators accusing public creators. Here the accused is a student, often a minor, inside a grading or admissions process.
- [AI tutor gives answers instead of teaching](../../education-agents/failures/gives-answers-instead-of-teaching.md) - a study helper that solves homework. Rule 7 here covers the essay-coach version, where the output is submitted as the student's own.

## 9. Common questions
### My teacher says I used AI on my essay but I didn't. What can I do?
Ask for the concern in writing and what it is based on. Offer your drafts, notes or Google Docs or Word version history, and offer to talk through how you wrote it. Ask who decides and how to appeal; in the Adelphi case a court faulted the school for skipping a real hearing.

### Do colleges check application essays for AI?
Some say they do and most do not say how. In 2023 USC said it uses no detector, UC said it runs screenings and may ask applicants to authenticate work, and the Common App treats substantive AI use as fraud. Readers also compare the essay with the rest of the file.

### Can I use ChatGPT for my college essay?
Check each college's rules; the Common App bars "substantive" AI use without defining it. Using AI for feedback on your own draft is safer than having it write the essay. Researchers also found AI essays sound alike and less varied than real ones.

### How can teachers stop AI essays without relying on detectors?
Collect the writing as it happens: a dated outline or draft, version history, an in-class piece, or a short talk about the essay. In one UK blind test markers missed 94% of AI answers, so reading the final text is not enough.

### What is an oral follow-up for a suspected AI essay?
A short, recorded conversation where the student explains choices in their essay: why an example, what a source said, what they cut. It tests understanding, not memorized wording, and uses the same kind of questions for every student checked (rule 4).
