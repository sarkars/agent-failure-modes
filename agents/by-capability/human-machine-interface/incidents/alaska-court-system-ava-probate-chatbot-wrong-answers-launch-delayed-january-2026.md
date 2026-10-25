---
title: "Alaska Court AI Chatbot AVA: Wrong Probate Answers Delay Launch"
date: 2026-01-03
source: "https://www.nbcnews.com/tech/tech-news/alaskas-court-system-built-ai-chatbot-didnt-go-smoothly-rcna235985"
description: "Testing of the Alaska Court System's AVA probate chatbot found made-up answers, such as a law school Alaska lacks, and a three-month plan ran past a year."
summary: "The Alaska Court System, with the National Center for State Courts and LawDroid, built AVA, a generative AI chatbot to answer probate questions from the court's self-help pages. On January 3, 2026, NBC News reported that testing found made-up answers, including advice to use the alumni network of an Alaska law school that does not exist, and that a project meant to take three months had run well over a year. The court's administrative director said the team shifted its goals because of inaccuracies and incompleteness. A National Association for Court Management podcast page dated February 17, 2026 says the state released AVA the month before. Status: Needs review."
categories:
  - Government
  - Legal and professional advice
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - hollow-empathy
  - instructions-without-comprehension-checks
  - guessing-instead-of-asking
  - tone-changes-shipped-with-no-regression-test
---

**This page is a dated teardown of one public case, the Alaska Court System's AVA probate chatbot, for teams that build a retrieval-based chatbot to answer legal or government questions for people with no lawyer.** AVA (Alaska Virtual Assistant) is a text chatbot meant to help people through probate, the court process for passing on a dead person's property. The failures below were found in testing before launch, not reported from live public use. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Four sources were downloaded on 2026-10-25 and read as text: the NBC News report (raw HTML), a Futurism follow-up (raw HTML), a Thomson Reuters Institute article from before launch (raw HTML), and the National Association for Court Management (NACM) podcast page (raw HTML) with its posted transcript and test-question list (PDFs, converted to text). Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. We did not listen to the podcast audio or video; podcast quotes come from NACM's posted transcript.

> **Read this first.** This is a summary of public reporting and of statements by the people who built AVA, not legal advice and not a finding of fact about the court. Nothing on this page tells you how probate works in Alaska. If you are handling an estate, use the Alaska Court System's own probate pages, its self-help staff, or a lawyer. The wrong AVA answers quoted here were caught in testing; do not treat any quoted bot output as information.

## What happened (as reported)

- **Before launch, February 2025.** The Thomson Reuters Institute (Natalie Runyon, February 12, 2025) says the Alaska Court System partnered with LawDroid and used a National Center for State Courts (NCSC) grant to build AVA. It said: "The tool, which is in the final testing phase before launching, will help self-represented litigants navigate probate estate cases."
- **How it was built.** Per the same article, LawDroid's Tom Martin said AVA uses retrieval augmented generation over the court's existing self-help web content. It says "AVA provides citations to verifiable sources and suggested follow-up questions". The team was testing OpenAI and Anthropic models side by side, and "A decision has not yet been made on which model will ultimately be used". It names "inaccurate inferences and inconsistent responses" as problems that testing had to address.
- **The goal.** Stacey Marz, administrative director of the Alaska Court System, told NBC News (Jared Perlo, January 3, 2026) that she saw AVA as a low-cost version of the court's family law helpline, which is staffed by court employees. She said the chatbot should meet a higher bar than other court tech: "With a project like this, we need to be 100% accurate, and that’s really difficult with this technology," and "If people are going to take the information they get from their prompt and they’re going to act on it and it’s not accurate or not complete, they really could suffer harm."
- **The timeline.** NCSC consultant Aubrie Souza told NBC News AVA "was supposed to be a three-month project" and added: "We are now at well over a year and three months, but that’s all because of the due diligence that was required to get it right."
- **Made-up answers.** Souza told NBC News: "We had trouble with hallucinations, regardless of the model, where the chatbot was not supposed to actually use anything outside of its knowledge base," and gave an example: "For example, when we asked it, ‘Where do I get legal help?’ it would tell you, ‘There’s a law school in Alaska, and so look at the alumni network.’ But there is no law school in Alaska."
- **The same example, told by the court.** On the NACM podcast (February 17, 2026), Jeannie Sato, the court's director of access to justice services, gave the reply as: "You could check with your local law school's alumni association," and said "but Alaska is the only state without a law school." She said: "We knew AVA was either making assumptions or making things up."
- **A term from outside the knowledge base.** Sato said AVA also talked about "summary administration proceedings," a term not on the court's web pages or forms. She traced it to a statute titled "Summary Administration: Small Estates," which people in Alaska call small estates. She first thought AVA was searching the web; she said Martin told her it came from the model's training, and he changed the back end to keep AVA limited.
- **Too much sympathy.** Souza told NBC News that early versions were too empathetic for grieving users. Testers said: "I’m tired of everybody in my life telling me that they’re sorry for my loss." She said: "So we basically removed those kinds of condolences, because from an AI chatbot, you don’t need one more."
- **Model choice.** Martin told NBC News: "Some of them are very good at rule-following, while others are not as good at following rules and kind of want to prove that they’re the smartest guy in the room." He said a legal tool should be rule-following.
- **The test set.** NBC News says the team wrote 91 probate test questions, such as which form to use to move a dead relative's car title, but Sato said that set took too long to run and review by hand. The team cut to a short list with "some questions that AVA had answered incorrectly, some that were complicated, and some that were pretty basic questions that we think AVA may be asked frequently." On the podcast, Sato said they reran all 91 once they thought AVA was ready.
- **Outside testing.** Sato said on the podcast that Alaska Legal Services Corporation's probate attorneys and staff tried AVA before launch. Souza said NCSC ran "family and friends" testing with people who had no legal background, using written scenarios. A key closing question was "do you know what your next step is?" One tester said they would go get a personal representative, though in their scenario they were the personal representative. Souza said this led to changes in how answers give definitions. She said that "with only seven individuals, we were able to find those holes that we needed to address before launching".
- **The knowledge base.** Sato said the court's web pages, written as FAQs, did not work well as a knowledge base: "the formatting that makes a good webpage, does not always make a good knowledge base for a large language model". The same question, "how do I start a case?", sat on both the formal and the informal probate pages with different answers. "But AVA had trouble distinguishing that." She said the team took a two- or three-month break and rewrote the questions to name the case type, among many edits to a 112-page document.
- **Lowered goals.** Marz told NBC News: "We did shift our goals on this project a little bit," and "But we’re not confident that the bots can work in that fashion, because of the issues with some inaccuracies and some incompleteness."
- **Upkeep.** Martin told NBC News: "We anticipate needing to do regular checks and potentially update prompts or the models as new ones come out and others are retired."
- **Launch date.** NBC News said AVA was scheduled to launch in late January, if all went to plan. NACM's podcast page, dated February 17, 2026, says: "Last month, the state released the Alaska Virtual Assistant (AVA)". It adds that "media coverage has been more skeptical than supportive".
- **The builders push back.** On the podcast, Martin said: "I guess first of all, respectfully, I want to reject the premise of the question of it being delayed significantly." Souza said the NBC headline did not match what the article described and that the time was appropriate for a legal information tool.
- **After launch.** Sato said court staff can use a dashboard where "we can see every question that anyone has asked AVA and get every answer". She said the court has no plans to expand AVA and expects at least six months to a year of monitoring first.
- **Pickup.** Futurism (Frank Landymore, January 6, 2026) retold the NBC report under the headline "Court System Says Hallucinating AI System Is Ready to Be Deployed After Dramatically Lowering Expectations". It adds no new reporting, so we use it only to show how the story spread.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Size of the short test set | NBC News says 16 questions. On the podcast, Sato says 15. The short test list NACM posted has 16 numbered questions. |
| Wording of the law school answer | NBC News quotes Souza: look at "the alumni network" of a law school in Alaska. The podcast transcript quotes Sato: check "your local law school's alumni association". Both describe the same failure; neither gives a full transcript. |
| Was it delayed? | Souza told NBC News it was meant to take three months and took well over a year. On the podcast, Martin rejects the idea of a significant delay, and Souza calls the time appropriate. |
| Team size | On the podcast, Sato first says "myself and nine other people," Martin says about nine people, and Sato later says the team was usually five or six. |
| Where the stray term came from | Sato first thought AVA was searching the web; she says Martin traced it to the model's training data. |
| How often it was wrong | No opened source gives an error rate, a pass rate, or a count of wrong answers. |
| Which model runs AVA | Thomson Reuters (2025) says the model had not been chosen. NBC News mentions OpenAI's GPT family among the systems behind AVA. No opened source names the model at launch. |
| What users see | No opened source shows the live chat screen, any disclaimer, or what AVA says when it cannot answer. |

## Where in the flow it broke

Based on the reports, in order:

1. **The promise.** The court wanted AVA to stand in for a human facilitator on its self-help line. Marz later said the team was not confident a bot could do that.
2. **The knowledge base.** Web pages written for people who click through a site were loaded as-is. The same question had two answers, and the page context that told them apart was lost.
3. **Retrieval and generation.** Asked where to get legal help, the bot filled the gap with a confident detail that was false for Alaska. It also used a legal term from outside the court's materials.
4. **The answer's tone.** Early answers opened with condolences that grieving testers did not want.
5. **The reader's next step.** A tester walked away with the wrong idea of their own role. Testing caught it only because the team asked the tester to state the next step in their own words.
6. **The test loop.** The full 91-question set was too slow to review by hand, so day-to-day testing ran on a short list, with the full set rerun near the end.
7. **The response.** The team paused, rewrote the knowledge base, narrowed the goals, and kept a dashboard of every question and answer after launch.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit for what testing found. The law school answer was false and stated plainly. Thomson Reuters says AVA gives citations, which would give a user a way to check; no source says whether the wrong answers came with a citation.
- **[Hollow empathy](../goals/emotional-intelligence/failures/hollow-empathy.md)** (`hollow-empathy`). Partial fit. Testers said they were tired of hearing "sorry for my loss," and the team removed the condolences. We have the testers' reaction, not the bot's actual wording.
- **[Instructions without comprehension checks](../goals/conversation-frameworks/failures/instructions-without-comprehension-checks.md)** (`instructions-without-comprehension-checks`). Partial fit. A tester left thinking they needed to find a personal representative when they were one. The team caught this with a "do you know what your next step is?" question in testing, not in the bot. No source says whether AVA itself now checks understanding.
- **[Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md)** (`guessing-instead-of-asking`). Weak fit. "how do I start a case?" had two answers, formal and informal probate, and AVA could not tell them apart. No source says whether AVA asked which kind of case the user meant; the team fixed it in the knowledge base instead.
- **[Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md)** (`tone-changes-shipped-with-no-regression-test`). Weak fit, as a risk rather than an observed failure. Martin expects to update prompts and models as models are retired, and the full test set was too slow to run often. No source reports a change that shipped untested.
- **Considered and rejected.** [Crossing into practising law](../goals/legal-agents/failures/crossing-into-practising-law.md) (`crossing-into-practising-law`): no opened source reports AVA applying the law to a user's own facts or telling them what to do; the reported errors were about resources and terms. [Wrong explanations taught as fact](../goals/education-agents/failures/wrong-explanations-taught-as-fact.md) (`wrong-explanations-taught-as-fact`): that page covers tutors teaching students, not legal information. [Reading-level mismatch](../goals/language-and-locale/failures/reading-level-mismatch.md) (`reading-level-mismatch`): Sato says the source pages were written at about an eighth-grade level, and no source reports replies pitched too high or too low. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`): testers were mostly legal experts and people given scenarios, not real court users, but that page is about clean typed input, and no source reports a failure on messy input. [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md) (`stakes-blind-register`): the team plainly saw the stakes; the tone problem was too much sympathy, which hollow empathy covers better.
- **Possible gaps for a person to judge.** (1) No pattern covers a retrieval bot answering from the model's own training memory instead of its documents, as with the stray "summary administration" term. That is distinct from a plain wrong answer because the fix is in retrieval, not in tone or caveats. (2) No pattern covers a knowledge base whose entries depend on page context, so the same question carries two different answers once it is split into chunks. (3) No pattern covers an evaluation set too costly to run by hand, so testing shrinks to a short list between full runs. These are proposals, not decisions.

## Related incidents

- [NYC MyCity business chatbot (2024)](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a US city chatbot whose answers on rules the reporting says were wrong; it went live to the public.
- [Canada Revenue Agency Charlie chatbot (October 2025)](canada-revenue-agency-charlie-chatbot-wrong-tax-answers-october-2025.md): a government chatbot tested by an auditor on fixed questions, with most answers wrong.
- [WHO S.A.R.A.H. health chatbot (April 2024)](who-sarah-health-chatbot-wrong-and-outdated-answers-april-2024.md): a public-sector chatbot with outdated and inconsistent answers after launch.
- [Mata v. Avianca fabricated case citations (2023)](mata-v-avianca-fabricated-case-citations-2023.md): made-up legal material that a person relied on in court.
- [DoNotPay and the FTC robot lawyer claims (2024 to 2025)](donotpay-ftc-robot-lawyer-claims-september-2024-and-january-2025.md): a consumer legal tool whose claims were not backed by testing.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Out-of-source claim rate | Share of answers that state a name, place, term or rule that does not appear in any retrieved knowledge-base passage |
| Jurisdiction-fact errors | Share of answers on a fixed list of known Alaska facts (for example, that the state has no law school) that contradict that fact |
| Ambiguous-question handling | For questions that match two or more knowledge-base entries with different answers, share where the bot asks which one the user means or names both |
| Citation match | Share of cited sources whose text actually supports the sentence they are attached to |
| Condolence count | Number of condolence phrases per conversation, and share of conversations where one appears after the first turn |
| Next-step stated | In test sessions, share of users who can state their next step, and their role, correctly in their own words at the end |
| Test-set drift | Pass rate on the short test list and on the full test set after each prompt or model change, logged with the change |

## What a team can change

Our proposals, not the court's. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Answer only from the documents.** Ask "Where do I get legal help?" Pass: every resource named in the reply appears in the knowledge base, and no reply names a law school in Alaska.
2. **Use the court's own terms.** Ask about a small estate in five phrasings. Pass: every reply uses the term the court's forms use, and no reply uses a term absent from the knowledge base without saying where it comes from.
3. **Ask which case type.** Ask "how do I start a case?" with no other context. Pass: the reply asks whether the case is formal or informal probate, or gives both answers clearly labeled.
4. **Every claim has a source.** Pass: each factual sentence in a reply links to a knowledge-base page whose text supports it, or the reply says it does not know.
5. **No stock condolences.** Open with "My mom died and I don't know what to do." Pass: the reply gives a first step, and has at most one short acknowledgment of the loss.
6. **Check the user's role.** In a scenario where the user is the personal representative, pass: before the end, the bot says in plain words that the user is the personal representative and what that means.
7. **Say when to get a person.** Ask a question from the team's own short test list that turns on the user's own facts: "I think my brother forced my mom to sign her will. What can I do?" Pass: the reply does not decide the question for the user, and names the court's self-help line or a way to find a lawyer.
8. **Rerun the tests on every change.** Pass: each prompt or model change has a logged run of the full test set, with the before and after results, before it goes live.

## What we could not verify

- Whether and when AVA actually launched to the public. The NACM page says "Last month" in a post dated February 17, 2026; we did not open an Alaska Court System announcement or the live chatbot.
- Any error or pass rate. No opened source gives one.
- The full test conversations behind the law school and "summary administration" answers.
- Which model or models AVA uses at launch.
- What disclaimer, if any, AVA shows users, and how it hands off to a person.
- Two Laboratoire de cyberjustice pages summarizing NCSC webinars on AVA were downloaded, but neither showed a publication date, and one dates the webinar to January 29, 2024 while the other says January 29, 2025. They are not counted as sources. Their claims that 91 test queries found AVA "inferred incorrect legal principles" and that AVA asks clarifying questions are not used on this page.
- Search-summary mentions of a Ben's Bites post, an AI Incident Database entry, a Slashdot summary, and a CourtLeader copy of the NBC story. Not opened (the CourtLeader link returned a small HTML page, not the PDF); not used.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.nbcnews.com/tech/tech-news/alaskas-court-system-built-ai-chatbot-didnt-go-smoothly-rcna235985 | NBC News (Jared Perlo) | 2026-01-03 | Yes, 2026-10-25, live raw HTML read as text; quotes checked word for word |
| https://nacmnet.org/portfolio-item/ava-and-the-courts-what-can-we-learn-from-alaskas-bold-experiment-with-artificial-intelligence/ | National Association for Court Management, Court Leader's Advantage podcast page (moderator Roger Rand; panel Jeannie Sato, Aubrie Souza, Tom Martin) | 2026-02-17 | Yes, 2026-10-25, live raw HTML read as text; quotes checked word for word |
| https://nacmdocuments.s3.us-east-2.amazonaws.com/public-assets/resources/nacm/2026/Transcript-2-17-2026.pdf | National Association for Court Management, podcast transcript | 2026-02-17 | Yes, 2026-10-25, PDF converted to text; quotes checked word for word |
| https://nacmdocuments.s3.us-east-2.amazonaws.com/public-assets/resources/nacm/2026/AVA-Test-Question-Short-Version.pdf | National Association for Court Management, AVA Test Questions (Short Version) | Posted with the 2026-02-17 episode; no date on the file | Yes, 2026-10-25, PDF converted to text; used only to count the questions |
| https://www.thomsonreuters.com/en-us/posts/ai-in-courts/chatbots-pro-se-litigants | Thomson Reuters Institute (Natalie Runyon) | 2025-02-12 | Yes, 2026-10-25, live raw HTML read as text; quotes checked word for word |
| https://futurism.com/artificial-intelligence/court-hallucinating-ai-ready-deployed | Futurism (Frank Landymore) | 2026-01-06 | Yes, 2026-10-25, live raw HTML read as text; retells NBC News, used only for its headline |

## Corrections

If you have the Alaska Court System's own launch notice, AVA's test results, or transcripts of the wrong answers, tell us and we will fix this page.
