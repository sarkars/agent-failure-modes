---
title: "A UK cancer doctor publicly tests Babylon Health's symptom checker chatbot for unsafe chest pain triage, and Babylon calls him a troll, February 2020"
date: 2020-02-25
source: "https://techcrunch.com/2020/02/25/first-do-no-harm/"
description: "How a UK consultant's public tests of Babylon Health's symptom checker raised chest pain triage concerns, and how the company and regulator responded."
summary: "For about three years, consultant oncologist David Watkins posted tests of Babylon Health's triage chatbot under the name Dr Murphy, focused on chest pain cases. One example: a fictitious 67-year-old smoker with central chest pain was offered gastritis or a sickle cell crisis. In February 2020 he named himself at a Royal Society of Medicine debate and appeared on BBC Newsnight. Babylon put out a press release calling him a troll, said he ran 2,400 tests and found only 20 genuine errors, and used his app usage data to say so. Watkins said he ran 800 to 900 full triages and still found issues in about one in three. In a letter dated December 4, 2020, the UK medical device regulator, the MHRA, told him his concerns were valid and ones it shared. Babylon said the letter was about regulation in general."
categories:
  - Health and Wellbeing Chatbots
  - Accuracy
  - Governance
patterns:
  - triage-wording-understates-or-overstates-urgency
  - confident-wrong-answer-with-no-way-to-check
  - no-user-facing-record-of-what-the-bot-said
---

**This page is a dated teardown of the public dispute over Babylon Health's symptom checker chatbot in February 2020, for teams that build or buy a chatbot that tells people how urgently to seek care.** The product was Babylon Health's symptom triage chatbot, offered in the UK in the GP at Hand app. The "user" was a tester: David Watkins, a consultant oncologist, who typed made-up patient cases into the bot and posted the results. The moment was the week of February 24, 2020 (the Monday, by the article dates), when he spoke publicly under his own name and Babylon answered with a press release that called him a troll. The page also covers the regulator's letter to him dated December 4, 2020, because that is how the dispute was later judged in public. Every fact below comes from a source we opened (listed at the end). Where we have only a second-hand account, we say so.

**Status: Needs review.** TechCrunch (two articles), MedCity News and AI News were downloaded as raw HTML on 2026-10-28 and read as plain text. The OECD AI incident page was also opened, but it only lists coverage; we use it for nothing else. Each quote below was checked word for word against that text. We did not open Babylon's press release, Watkins's tweets, the BBC Newsnight segment, the HSJ reports or the MHRA letter itself (see "What we could not verify").

> **Read this first.** This is a summary of public reporting, not a finding of fact. It is not medical advice. Nothing here says whether any answer the bot gave was right or wrong for a real patient; the cases were made up by a tester, and the clinical judgments are his or the reporters'. If you have chest pain or other warning signs, contact emergency services or a clinician, not a chatbot or this page. The dispute was between named people and a company; we report what each side said and do not decide it. Babylon Health's later history is out of scope.

**Channel note.** Chat. Per TechCrunch (2020), users of chatbots like this answer questions about their symptoms and get a possible cause at the end. Per AI News, Babylon's bot aimed to decide whether someone could treat themselves at home, should book a GP appointment, or should go straight to a hospital. Per TechCrunch, Watkins posted videos of these chats. This phase of the knowledge base is chat-first: voice signals and voice checks are planned and not covered here.

## What happened (as reported)

- **The product.** AI News (Ryan Daws, February 26, 2020) says the chatbot was in Babylon's GP at Hand app, which UK health secretary Matt Hancock championed. It says the bot aimed to cut the load on GPs and emergency departments by automating triage. MedCity News (Elise Reuter, February 27, 2020) says the chatbot was a Class 1 medical device, the class for low-risk devices, so it could give advice but not a diagnosis.
- **The tester.** Per TechCrunch (Natasha Lomas, February 25, 2020), Watkins, a consultant oncologist at The Royal Marsden NHS Foundation Trust, had posted chatbot triages on Twitter as "Dr Murphy" (@DrMurphy11) for several years. MedCity says he had "zeroed in" on the bot's cardiac chest pain results for three years. TechCrunch (Lomas, March 5, 2021) says he began raising concerns with UK regulators as early as February 2017.
- **The cases.** These are tester cases, not real patients, as reported:
  - MedCity: for a fictitious 67-year-old smoker with central chest pain, the app suggested gastritis or a sickle cell crisis.
  - AI News: for an obese 48-year-old heavy smoker with chest pain, the bot suggested a consultation "in the next few hours". AI News quotes his tweet: "I say call 999, the Babylon App says see your GP". AI News says this case was later fixed.
  - TechCrunch (2020) embeds a tweet showing a triage for a female patient that, per TechCrunch, failed to pick up a potential heart attack. The tweet carries the hashtag #GenderBias.
  - TechCrunch (2021) says that in May 2018 the MHRA told Babylon of two safety incidents with the chatbot, one with missed heart attack symptoms and one with missed DVT symptoms. This comes from a document Watkins sent the regulator, as TechCrunch describes it.
- **Going public.** Per TechCrunch (2020), Watkins named himself on Monday at a Royal Society of Medicine debate on AI and digital health, where he called for less hype and more independent testing. His line there, per TechCrunch: "validation is more important than valuation". MedCity says he appeared on BBC Newsnight on Tuesday, where Babylon's clinical innovation director, Keith Grimes, defended the bot.
- **The press release.** Per TechCrunch (2020), Babylon released a statement late Monday that called Watkins a "troll". Per TechCrunch and AI News, it said he had run 2,400 tests, raised "fewer than 100 test results which he considered concerning," and that a panel of clinicians found "genuine errors in our AI" in only 20. TechCrunch says that implied an error rate of 0.8%. The release also said he had posted "over 6,000 misleading attacks," per TechCrunch.
- **Watkins's answer.** He told TechCrunch the claims were "absolute nonsense" and that "There are certainly not 2,400 completed triage assessments." He estimated 800 to 900 full triages, many of them repeats to check whether an issue had been fixed. He said he found issues in about one in three runs, down from "one in one" for an earlier version in 2018. He said his testing focused on common and red flag cases, so it was not a measure of the bot's overall accuracy.
- **The data question.** TechCrunch (2020) says Babylon pulled his app usage data to write the release. Another doctor, Sam Gallivan, asked on Twitter whether other frequent users could expect their medical queries in a press release. Watkins told TechCrunch he could no longer open his query history in the app and did not know why. The UK data watchdog, the ICO, gave TechCrunch only a general statement.
- **The disclaimer.** TechCrunch (2020) says Babylon's materials state its AI tools "do not provide a medical diagnosis, nor are they a substitute for a doctor". Watkins said the bot still showed a suggested diagnosis and an action, so the disclaimer "doesn't make sense" to a patient.
- **The regulator, later.** TechCrunch (2021) reviewed a letter from the MHRA to Watkins dated December 4, 2020. It quotes the letter: "Your concerns are all valid and ones that we share." The letter also said several issues "fall outside of our existing remit," and that confidentiality stopped the MHRA from saying more on any investigation. TechCrunch says the HSJ reported the letter first.

## What the company said

- **In the February 2020 release, as quoted by TechCrunch.** Babylon said its AI had been used millions of times and "not one single patient has reported any harm." It said its technology met regulatory standards in five countries and had been validated as safe by the NHS on ten occasions. It cited patient ratings and a Care Quality Commission rating of "Outstanding" for leadership.
- **To TechCrunch about the data.** A spokesperson said the volume of his use showed it was a test, not a real health concern, and that Babylon shared only "non-personal statistical data" and met its data protection duties.
- **On BBC, as quoted by MedCity.** Grimes said the bot is "not giving out fake or false information," and that it gives safe information so patients seek help at the right time.
- **On the MHRA letter, March 2021, per TechCrunch.** Babylon said the letter's concerns were broad statements about the regulatory framework, which it agreed with. It said it had received no notice of any regulatory action. It said symptom checkers were "a very small part of Babylon's activities," and that it was moving its symptom checker from a Class 1 device to a Class IIa device under EU rules.
- **Fixes.** MedCity says Babylon did not confirm which of the 20 errors it fixed. Watkins told TechCrunch (2021) that Babylon fixed each case he posted one by one, and that a broad fix was for anyone with chest pain "it would immediately say go to A&E". He said that wastes care resources.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Number of tests | Babylon release (via TechCrunch, AI News): 2,400. Watkins: 800 to 900 full triages; he thinks Babylon counted chats that were opened but not finished. |
| Error rate | Babylon: 20 genuine errors, about 0.8%. Watkins: issues in about one in three runs, by focused testing of red flag cases. Neither figure is from an independent test. |
| How many cases he flagged | TechCrunch quotes "fewer than 100." MedCity says "the 100 tests" he raised. |
| "6,000 misleading attacks" | Babylon release (via TechCrunch). Watkins: he had not tweeted 6,000 times in total. AI News: his account showed 3,925 tweets when it wrote. |
| NHS validation | Babylon: validated as safe by the NHS ten times. Watkins, to the MHRA (via TechCrunch 2021): as far as he knew, the chatbot had not been validated. No opened source names the validation process. |
| What the MHRA letter means | Watkins: the regulator shares his safety and governance concerns. Babylon: the letter is about the regulatory framework, not Babylon. The MHRA declined to comment on individual cases. |
| Exam claim, June 2018 | AI News quotes a Babylon director saying the bot scored 82 percent at a 2018 event. A search summary gave 81%; we did not open a source for that figure. |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **Red flags went in, a low urgency came out.** In the reported cases, the tester entered chest pain plus risk factors such as age and smoking. The bot answered with a GP visit in hours, or with non-cardiac causes. The urgency tier was the part that mattered, and per the tester it was too low.
2. **The answer looked like a diagnosis.** Per Watkins, the bot showed a suggested diagnosis and an action, while a disclaimer said it was information only. A user had no clear way to know which part to trust.
3. **Fixes were case by case.** Per Watkins, each posted case was patched for that age and those exact answers, so similar cases broke again. The blunt fix, sending everyone with chest pain to A&E, swaps an understated tier for an overstated one.
4. **No outcome came back.** Per TechCrunch (2021), Watkins told the regulator the bot did not routinely ask how the patient did after triage. Without that, harm is hard to see, and Babylon's point that no patient reported harm says little.
5. **The tester's chat log was used against him, and he lost his own copy.** Babylon used his usage data in a press release, and he said he could no longer view his own history.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Triage wording understates or overstates urgency](../goals/health-scheduling-agents/failures/triage-wording-understates-or-overstates-urgency.md) (`triage-wording-understates-or-overstates-urgency`). **Core fit.** The reported cases are chest pain with risk factors routed to a GP or to non-urgent causes. The reported later fix, A&E for any chest pain, is the overstated side of the same pattern. **Where it does not match:** that page is written for scheduling and intake bots; Babylon's bot was a full symptom checker. The cases were tests, not real patients.
- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** The bot gave a suggested cause and an action with no sign of doubt, per Watkins. A user typing their own symptoms cannot check a triage answer. **Where it does not match:** the bot did carry a general disclaimer; the problem Watkins named was that it contradicted the answer, not that it was missing.
- [No user-facing record of what the bot said](../goals/privacy-and-governance/failures/no-user-facing-record-of-what-the-bot-said.md) (`no-user-facing-record-of-what-the-bot-said`). **Weak fit, one detail only.** Watkins said he could no longer open his own chat history, while the company could use it. No source says why, so treat this as a lead, not a finding.
- **Considered, not a fit.** `no-way-to-report-bad-behaviour`: Watkins did report issues, to the company, the public and the regulator; the gap was the response, and the missing outcome follow-up, which this pattern does not cover. `escalates-too-early-or-too-late`: about handing off to a person, not about urgency advice. `excess-disclaimers-and-warnings`: the issue was a conflicting disclaimer, not too many. `gender-and-pronoun-errors`: about addressing users, not about different triage by sex; one tweet's #GenderBias tag is the only sign of that, and we did not open the tweet.
- **Possible gaps for a person to judge.** No pattern in this taxonomy names (a) a company using a user's own chat logs in public to answer that user's complaint, or (b) a bot whose triage changes by sex for the same symptoms. Both are proposals, not decisions.

## How it differs from close cases

- [Nabla GPT-3 medical chatbot test, October 2020](nabla-gpt-3-medical-chatbot-test-tells-simulated-patient-to-kill-themselves-october-2020.md): also a test with a made-up patient, but by the builder, of a model it had not shipped. Here an outside clinician tested a live product used by patients, and the company disputed his results.
- [WHO S.A.R.A.H. health chatbot, April 2024](who-sarah-health-chatbot-wrong-and-outdated-answers-april-2024.md): a health chatbot with outdated facts and a public warning that answers may be wrong. Here the worry was the urgency advice, not facts.
- [NEDA Tessa chatbot, 2023](neda-tessa-chatbot-weight-loss-advice-2023.md): a health chatbot pulled after people posted harmful replies. Here the bot stayed in service, and the dispute moved to the regulator.

## What to measure

Proposed text-chat signals, not results. Status: Not yet run. Voice signals are planned only.

- Share of red flag test cases (from a clinician-owned list) where the bot's urgency tier matches the tier the clinicians set.
- Share of pairs of test cases that differ only in sex or age where the bot gives a different urgency tier, each reviewed by a clinician.
- Share of reported cases that, once fixed, also pass on near variants (a different age, a different order of answers).
- Share of triage chats that end with a follow-up question about what the user did and how it went.
- Days from an outside safety report to a written reply to the reporter.

## What a team can change

Our proposals, not Babylon's. Each is a pass/fail check on a transcript, a test run or a review sheet. Status: Not yet run. Which symptoms belong in which tier must come from clinicians, not from this page.

1. **Test red flags before launch and after every change.** Pass: every case on the clinician-owned red flag list gets the tier the clinicians set, in two runs on the release build.
2. **Fix the class, not the case.** Pass: a fix for one reported case also passes at least three near variants written by a clinician.
3. **Check sex and age pairs.** Pass: paired cases with the same symptoms get the same tier unless a clinician has written down why not.
4. **Lead with the action, not a guessed diagnosis.** Pass: the reply states the urgency tier and what to do first; any possible cause comes after it and is labeled as possible.
5. **Make the disclaimer match the answer.** Pass: the disclaimer text does not contradict the action the bot just gave.
6. **Ask how it went.** Pass: the bot or a follow-up message asks what the user did and whether they got care, and the answer is logged for safety review.
7. **Let users keep their own record.** Pass: a user can open and export each of their past triage chats.
8. **Answer critics on the record, not with their data.** Pass: no public statement includes a named user's usage data, and every outside safety report gets a written reply.
9. **Don't over-correct.** Pass: minor cases on the clinician list are not all sent to emergency care; the share sent to A&E for those cases stays at or below the target the clinicians set.

## What we could not verify

- Babylon's February 2020 press release. We read only the lines TechCrunch, AI News and MedCity quote.
- Watkins's tweets and videos. We saw only fragments embedded in the articles, so the exact bot wording, ages and outcomes come from the reporters.
- The BBC Newsnight segment and the Royal Society of Medicine debate. Not watched or read.
- The MHRA letter dated December 4, 2020. We read only TechCrunch's description and quotes; the HSJ report it cites was not opened.
- The May 2018 MHRA notices about missed heart attack and DVT symptoms. Seen only through TechCrunch's account of Watkins's document.
- Babylon's NHS validation claim and its exam score claims. No opened source shows the underlying test.
- Whether the bot changed its triage by sex. One tweet hashtag only.
- Seen only in search summaries / unverified: a 2019 test of identical cardiac symptoms in a man and a woman with different outcomes; an 81% exam score and a 72% average; HSJ, Pulse, Telecare Aware, PSL Hub, IT Pro, Vietnamnet and Nation.co.ke items. None is used for facts here. We did not open any BBC, Guardian, Forbes, Sifted, BMJ or Lancet piece for this page.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://techcrunch.com/2020/02/25/first-do-no-harm/ | TechCrunch (Natasha Lomas) | 2020-02-25 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://medcitynews.com/2020/02/babylon-physician-tussle-over-triage-chatbots-safety/ | MedCity News (Elise Reuter) | 2020-02-27 (page timestamp, UTC) | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.artificialintelligence-news.com/news/babylon-health-doctor-ai-chatbot-safety-concerns/ | AI News (Ryan Daws) | 2020-02-26 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://techcrunch.com/2021/03/05/uks-mhra-says-it-has-concerns-about-babylon-health-and-flags-legal-gap-around-triage-chatbots/ | TechCrunch (Natasha Lomas) | 2021-03-05 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://oecd.ai/en/incidents/2020-02-26-bc4b | OECD.AI incident monitor | 2020-02-26 (incident ID) | Yes, 2026-10-28; coverage list only, not used for facts |

## Corrections

If you have Babylon's press release, the MHRA letter, the Newsnight segment or Watkins's original tweets, tell us and we will fix this page.
