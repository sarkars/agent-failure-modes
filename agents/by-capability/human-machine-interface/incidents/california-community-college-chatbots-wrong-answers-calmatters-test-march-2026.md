---
title: "California community college chatbots named a former president, gave wrong office hours and fumbled a Social Security question in CalMatters tests, March 2026"
date: 2026-03-06
source: "https://calmatters.org/education/higher-education/college-beat/2026/03/college-ai-chatbot/"
description: "CalMatters tested California community college chatbots. One named a former president, gave wrong office hours, and dodged a Social Security question."
summary: "On March 6, 2026, CalMatters reported that California community college districts spend millions on student-facing chatbots from vendors such as Gravyty and Gecko. In CalMatters testing, East Los Angeles College's bot named a president who had left the job and gave wrong financial aid hours and dates; asked in Spanish whether a Social Security number is needed to enroll, it sent users to the registrar to update one, and in English it pivoted to financial aid. Fresno City College's bot showed similar problems and returned accurate food pantry information only when the question had a typo. District officials said the problems come from configuration and source data. Status: Needs review."
categories:
  - Education
  - Government
  - Trust
  - Customer Service
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - missing-the-obvious-intent
  - plain-language-and-language-access-gaps
  - clean-lab-testing
---

**This page is a dated teardown of one news test of public college chatbots, for teams that run a student-facing or public-agency chatbot on top of an FAQ library or a scraped website.** The products were the chatbots on California community college websites, including East Los Angeles College's and Fresno City College's (both from the vendor Gravyty, formerly Ocelot) and Santa Monica College's (from Gecko). The users were prospective and current students asking about admissions, financial aid and campus services. The moment was a set of test questions CalMatters typed into the bots, published on March 6, 2026. The date above is that publication date.

**Status: Needs review.** Built from one original news report and two primary documents, all downloaded on 2026-10-29 and read as text: the CalMatters article by Martin Romero (dated March 6, 2026) and two Los Angeles Community College District (LACCD) news posts that confirm the leadership change behind one of the wrong answers. We also opened two copies of the CalMatters article republished by LAist (March 6, 2026) and inewsource (March 9, 2026); both say they are CalMatters republications under a Creative Commons license, so they are **not** independent sources and add no facts. CalMatters is the only original reporting on the bots' answers we could open. The LACCD posts are independent of CalMatters but confirm only the background fact (who led East Los Angeles College), not the bot's error itself. Each quote below was checked word for word against the saved text with a script, with curly and straight quote marks treated as the same.

> **Read this first.** This page summarizes a news report. It is not financial aid, enrollment or immigration advice and does not say whether a Social Security number is needed to enroll at any college. CalMatters gives the questions it typed, but it does not print the bots' full replies, so we do not quote any bot's words: no opened source does. Student names below are as printed in CalMatters, quoted on the record.

**Channel note.** This is a text chat incident: typed chatbots on college websites. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals, such as a campus phone line reading out office hours or a web page that disagrees with the chat, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The spending.** CalMatters reports that "Three community college districts that responded to a CalMatters survey reported annual costs ranging from about $151,000 to nearly half a million dollars." At LACCD, "contracts and amendments approved since 2021 total about $3.8 million through 2029, according to district board documents."
- **The headline test.** "East Los Angeles College's bot couldn't even correctly name its own president." Asked "Who is the current president of ELAC?" the bot "incorrectly named Alberto Román, who left the position last year to become the district's chancellor."
- **Office hours.** Asked "What is the financial aid office's current schedule?" the ELAC bot "provided incorrect hours and dates."
- **The Social Security question, two languages.** The ELAC bot "claims to support several languages, including English, Spanish, Chinese and Vietnamese." Asked in Spanish "Do I need a Social Security number to enroll?", "the system directed users to visit the registrar's office to update their Social Security number." In English, "the bot pivoted to discussing financial aid."
- **Fresno City College.** Its Gravyty bot "showed similar problems" on the Social Security question, and "often failed to direct students to the correct offices and, in some cases, listed incorrect locations and hours."
- **The typo.** A Fresno City College student "got accurate information on the availability of free food at her campus' Ram Pantry only when accidentally adding a typo to her query. Repeated CalMatters testing confirmed the same outcome."
- **Santa Monica College.** Its Gecko bot "was more successful in answering most questions," but at first, "when asked about mental health counseling, the bot did not mention the campus' Center for Wellness and Wellbeing. It does now."
- **Use.** LACCD colleges "average 5,000 to 7,000 interactions per month"; CalMatters reports 5,000 at the State Center Community College District and 4,000 at Santa Monica College.
- **The background fact, from LACCD.** An LACCD post dated November 7, 2024 says Monte E. Perez "was named Interim President of East Los Angeles College (ELAC)" on November 6, 2024, and quotes "Interim Chancellor Dr. Alberto J. Román." A post dated May 8, 2025 says the board "has officially appointed Dr. Alberto J. Román as the Chancellor." So by the CalMatters test, the name the bot gave had not been ELAC's president since November 2024.

## What each party said

- **Students.** Pablo Aguirre, an ELAC student, gave up on financial aid questions "after it kept asking him questions instead of giving him a clear answer," and said: "I just didn't find it as useful." Reanna Carlson, Fresno City College student government vice president: "I think the chatbot is outdated and can't navigate the services we provide on campus effectively." Bryan Hartanto, an international student at Santa Monica College, "worries that following inaccurate guidance could jeopardize his visa status."
- **Los Angeles Community College District.** Associate Vice Chancellor Betsy Regalado: "If you don't have that question in that library, then those poor people don't get an answer or they won't get an accurate answer." CalMatters reports staff review the FAQ library "at least once or twice a year for accuracy" and that the district plans "to transition to a new AI chatbot platform as early as late spring."
- **Santa Monica College.** Dean of enrollment services Esau Tovar said in an email the bot "was never designed to address all aspects of the student journey," and that the college aims for "good answers with fewer errors" rather than "great answers with potentially more errors."
- **District officials, as summarized by CalMatters.** The problems "stem from how the tools are configured and the information they draw from, rather than the technology itself."
- **Not said.** No opened source quotes Gravyty or Gecko, quotes a Fresno City College or State Center official on the specific wrong answers, or says whether the ELAC president answer or the office hours were fixed after publication.

## Where in the flow it broke

Based on the CalMatters report, and only as far as it goes. Each step is a place a check could have caught it.

1. **The source went stale.** The LACCD bot "relies on a manually maintained library" reviewed "once or twice a year." A leadership change in November 2024 was still wrong in the bot's answer more than a year later.
2. **The bot answered from the stale entry anyway.** It named a person and gave hours and dates as facts. The report does not say the bot showed a date, a source page or any doubt.
3. **The plain question got a neighboring answer.** "Do I need a Social Security number to enroll?" got a pointer to the registrar to update a number in Spanish and financial aid in English: two different wrong turns on one question.
4. **Exact wording decided the answer.** The food pantry answer came back right only with a typo, which suggests the match depended on the exact string, not the meaning. CalMatters does not explain why.
5. **Errors were found by outsiders.** A reporter's test, not a district review, surfaced these answers.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on one news report; no opened source shows a full chat.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Partial fit.** The bot named a former president and gave wrong office hours and dates. Partial because CalMatters does not print the replies, so we cannot see the tone or whether a source link was shown.
- [Missing the obvious intent](../goals/embedded-copilots/failures/missing-the-obvious-intent.md) (`missing-the-obvious-intent`). **Good fit.** A plain yes-or-no enrollment question got a reply about updating a number (Spanish) or about financial aid (English), which is the neighboring-question failure this pattern names.
- [Plain-language and language access gaps](../goals/government-service-agents/failures/plain-language-and-language-access-gaps.md) (`plain-language-and-language-access-gaps`). **Partial fit.** The bot advertises Spanish, and the Spanish answer to an enrollment question went somewhere different from, and no better than, the English one. Partial because the pattern is written for government program questions, and the English answer was also wrong, so this may be one intent failure seen twice rather than a language gap.
- [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`). **Weak fit.** The pattern says bots tested on clean input fail on messy input. Here the reverse showed up: the clean food pantry question failed and the typo version worked. That still points to a test set that never varied the wording. Weak because no source says how the colleges tested.
- **Considered, not a fit.** [Typos, shorthand, and noisy input](../goals/language-and-locale/failures/typos-shorthand-and-noisy-input.md) (`typos-shorthand-and-noisy-input`): about a bot that fails on typos; here the typo helped. [Mixed-language experience](../goals/language-and-locale/failures/mixed-language-experience.md) (`mixed-language-experience`): about one reply mixing languages; no source says the Spanish reply mixed in English. [Reviewing only failures](../goals/measurement-and-feedback/failures/reviewing-only-failures.md) (`reviewing-only-failures`): no source says what the districts review beyond the FAQ library check.
- **Possible gaps for a person to judge.** (1) No pattern covers a bot whose answers go stale on a fixed review cycle (here, people and hours that change more often than the library is checked). (2) No pattern covers a bot whose right answer depends on an exact string, so a reworded or corrected question gets a worse answer. These are proposals, not decisions.

## How it differs from close cases

- [NYC MyCity chatbot gives businesses illegal advice, 2024](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): reporters tested a public bot and found wrong legal answers. Here the wrong answers were facts that changed (a president, office hours), not rules of law.
- [Hall County, Georgia "Ask Hall County" chatbot, April 2026](hall-county-georgia-ask-hall-county-chatbot-wrong-tag-title-and-property-tax-answers-april-2026.md): the bot's index left out the office that owned the answers. Here the owner's own FAQ library was in the index but out of date.
- [Alaska Court System's AVA probate chatbot, January 2026](alaska-court-system-ava-probate-chatbot-wrong-answers-launch-delayed-january-2026.md): wrong answers were caught in testing before launch. Here the bots had been live for years and a reporter's test found the errors.

## What to measure

Proposed signals, not results. Status: Not yet run. Text signals are proposed; voice and web signals are PLANNED only and are not detected or measured here. Each can be computed from text chat logs joined to the bot's answer source; each has a counter-signal.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Answer age on changeable facts | For answers that state a person's title, office hours, dates or a location, days since the source entry was last edited | Facts that truly have not changed (verified by the office) |
| Owner check failures | Share of a weekly sample of such answers that the named office marks wrong | Errors traced to the office's own outdated web page |
| Same question, different language | For a fixed question set asked in each supported language, share of pairs where the answers point to different offices or topics | Pairs where one language answer is a correct, fuller version of the other |
| Wording sensitivity | For each test question, run five rewordings (including one typo); share of questions where at least one rewording gets a different office or a missing link | Rewordings that truly change the question |
| Repeat-and-leave | Share of chats where the user retypes the same question or the bot asks two or more questions back without answering, then the chat ends | Chats that end with a link click to the right office |

## What a team can change

Our proposals, not the colleges'. Each is a pass/fail check on a text chat log. Status: Not yet run. Review cycles, sample sizes and question sets are for each college to set, with the offices that own each topic.

1. **Date and source every changeable fact.** Pass: an answer naming a person, hours, dates or a location shows the source page and its last-updated date. Fail: the reply names a president with no source or date.
2. **Check people and hours on a short cycle.** Pass: every library entry with a name, schedule or date has an owner and was confirmed within the cycle the college sets; expired entries are hidden and the bot links to the office page instead. Fail: an entry for a president who left more than a year ago is still served.
3. **Answer the question asked, first.** Pass: on "Do I need a Social Security number to enroll?", the first sentence answers that question (or says the bot cannot, and names the office that can). Fail: the reply is about updating a number or about financial aid.
4. **Test every advertised language with the same questions.** Pass: before launch and after each content change, a fixed question set in each supported language returns the same office and topic as English. Fail: Spanish and English send the user to different places.
5. **Test rewordings, not one phrasing.** Pass: each test question passes in at least five wordings, including a typo and a short form. Fail: the right answer appears only for one exact string.

## What we could not verify

- The bots' actual reply text for any CalMatters question; the article describes the replies but does not print them.
- Any statement from Gravyty or Gecko, or from Fresno City College or State Center officials on the specific errors.
- Whether the ELAC president answer, the financial aid hours or the Social Security answers were corrected after March 6, 2026.
- The district board documents CalMatters cites for contract amounts; they are linked as a Google Drive folder, which we did not open, so contract figures are as reported by CalMatters.
- Whether LACCD moved to Gravyty's generative AI platform in spring 2026, and whether the State Center contract (through June 20, 2026) was renewed.
- How many students acted on a wrong answer.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://calmatters.org/education/higher-education/college-beat/2026/03/college-ai-chatbot/ | Martin Romero, CalMatters | 2026-03-06 | Yes, opened on 2026-10-29, HTML read as text; quotes checked word for word |
| https://laccd.edu/news/dr-monte-e-perez-named-interim-east-los-angeles-college-president | Los Angeles Community College District, news post | 2024-11-07 | Yes, opened on 2026-10-29; quotes checked word for word |
| https://www.laccd.edu/news/welcoming-dr-roman-our-new-chancellor | Los Angeles Community College District, news post | 2025-05-08 | Yes, opened on 2026-10-29; quotes checked word for word |
| https://laist.com/news/education/california-colleges-spend-millions-on-faulty-ai-systems-the-chatbot-is-outdated | LAist (republished CalMatters article) | 2026-03-06 | Yes, opened on 2026-10-29; a republication, not used as an independent source |
| https://inewsource.org/2026/03/09/california-colleges-ai-systems-chatbots/ | inewsource (republished CalMatters article) | 2026-03-09 | Yes, opened on 2026-10-29; a republication, not used as an independent source |
| https://oecd.ai/en/incidents/2026-03-06-d5de | OECD AI Incidents Monitor | 2026-03-06 (entry) | Yes, opened on 2026-10-29; used only to find the reports, not cited for facts |

## Corrections

If you have a transcript from one of these college chatbots, a statement from Gravyty, Gecko or a district about these answers, or news of a fix, from a source we can open, tell us and we will fix this page.
