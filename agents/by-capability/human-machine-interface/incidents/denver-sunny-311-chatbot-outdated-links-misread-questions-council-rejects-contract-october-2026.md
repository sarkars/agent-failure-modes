# Denver's "Sunny" 311 chatbot misread questions and served outdated links, then the City Council rejected its contract, October 2026

<!-- SEO
title: Denver Sunny 311 Chatbot: Old Links, Contract Rejected
description: Denver's Sunny 311 chatbot misread questions and linked to years-old pages in a 2024 test; in October 2026 the City Council voted down its contract.
search phrases:
- denver sunny chatbot council vote
- denver 311 ai chatbot citibot contract rejected
- city chatbot outdated links
- government chatbot misreads question keywords
- 311 hours cut chatbot instead of people
-->

**This page is a dated teardown of one US city's public 311 text chatbot, for teams that run a city or county service bot that answers from the government's own website and stands in for phone staff.** The product was "Sunny," Denver's AI assistant, run by the vendor Citibot, which answers on denvergov.org, by text message and on WhatsApp. The users were Denver residents with non-emergency questions and reports. Two moments matter. In a 2024 press test, Sunny misread a question about Denver's Broadway as one about New York and answered other questions with links to pages years out of date. In October 2026, the Denver City Council voted 9-3 against a five-year, $3.9 million contract extension, and councilmembers argued the program "often provides inaccurate information". The date in the title is the month of that vote coverage.

**Status: Needs review.** Built from five news sources, all opened and saved as text on 2026-10-29. (1) Westword, "Just How Bright Is Sunny, Denver’s New AI Chatbot?" (published June 1, 2024), which ran its own test of the bot. The direct page returned error 403, so we read the full article through a text-reader proxy (r.jina.ai). Our copy does not show the byline; its photos are credited to Catie Cheshire. (2) The Denver Post's story by Elliott Wenzler, as republished by GovTech (Tribune Content Agency) on October 14, 2026. (3) Denver7, by Ryan Fish (October 21, 2026). (4) Colorado Politics, by Deborah Grigsby (October 6, 2025). (5) CBS Colorado, by Jennifer McRae (October 7, 2025). We found no council record, vote tally from the city, or city audit we could open, so there is no primary document here. Every quote below was checked word for word against the saved text with a script.

> **Read this first.** This page is design guidance, not legal advice and not a view on city budgets, labor or AI policy. It reports what news outlets wrote about a city service and a council vote. It makes no finding about Denver, Citibot, or any council member. The 2024 test is one outlet's test from more than two years before the vote; we do not know whether the bot still behaves this way. We did not use Sunny ourselves.

**Channel note.** This is a text incident: a web chat box on denvergov.org, plus text message (Hey311, 439311) and WhatsApp, per Westword and Colorado Politics. Westword does not say which of these it used for its test. The rejected contract would have added a "voicebot" for 311 calls, per GovTech; that voice part never ran in any source we opened. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported)

- **What the bot is.** Per Westword, Sunny was introduced in February 2024, is "Powered by chatbot Citibot using AWS technology," and "only pulls from denvergov.org and the city’s 311 knowledge base rather than the entire internet." Westword reports the software cost $184,000 for the first year of a three-year contract. A city FAQ quoted by Westword says "it’s not likely it will generate responses using information outside of Denver’s 311 knowledge base".
- **What worked in the 2024 test.** Westword reported a pothole through Sunny and found the process "smooth." Its verdict: "On potholes, Sunny gets a 10/10."
- **A misread question.** Westword asked why the stretch of Broadway south of downtown was a mess. "At first, Sunny seemed to think the question applied to New York’s Broadway." The bot replied: "I’m sorry, but I can only provide information or answer questions related to Denver, Colorado." After Westword said it meant Broadway in Denver, Sunny answered. Westword's broader read: the bot gets confused, "seeming to pull from keywords rather than entire sentences."
- **A half answer, then a wrong page.** Asked "Is there lead in my water?", Sunny said "Denver Water’s Lead Reduction Program follows five main components to ensure the safety of the water supply." Westword says it did not list them or link to the program, and pointed to a page about water quality in streams and lakes. After Westword said it meant lead at home, Sunny said: "However, based on the knowledge we have, there is no specific information provided about lead water testing or mitigation in homes." Westword notes that the information lives on Denver Water's own site, not denvergov.org.
- **"We are not sure" plus old links.** Asked whether people can use psilocybin mushrooms, Sunny replied "We are not sure." It then offered links that included a marijuana symposium page for an event that, per Westword, "hasn’t occurred since 2019." Westword: "A lot of the links Sunny offers in support of its responses are outdated, especially for events." Asked about events, it suggested pages for the 2021 MLB All-Star game and an event open only to city employees.
- **The overall test verdict.** Westword: "on anything more complicated than the basics, the bot struggles, but it could be helpful for new residents."
- **More load on the bot.** On October 6, 2025, the city cut 311 phone hours to 7 a.m. to 5 p.m. weekdays, "to align with its budget and ensure the best possible service", per the city post quoted by Colorado Politics. The same post said: "Our chatbot, Sunny, can answer questions and connect you to services 24/7!" Colorado Politics reports the city "eliminated nine vacant and one filled 311 customer service agent positions."
- **The council vote.** GovTech (Denver Post): the council rejected the Citibot contract, and "Councilmembers argued that the program often provides inaccurate information and eliminates jobs that humans should have." Councilman Paul Kashmann: "I don’t know anyone who thinks the world of customer service has improved since humans have been replaced with bots." The opened sources give no specific wrong answer the council cited.
- **The city's case.** Per GovTech, a mayor's spokesman said the chatbot "has a 90% customer service satisfaction rating" (GovTech's wording). Denver7 quotes the mayor's office as saying the rating is "around 90 percent". Denver7 also reports the city's warning that if Sunny "were to become unavailable for a period of time while we iron out the details, we would expect to see a 40% increase in 311 calls, with a corresponding increase in caller wait times." The city says it plans to hire and train three new 311 agents.

## Timeline

| Date | Event | Source |
|---|---|---|
| February 2024 | Denver introduces Sunny | Westword |
| June 1, 2024 | Westword publishes its test of Sunny | Westword |
| October 6, 2025 | City cuts 311 phone hours and points residents to Sunny | Colorado Politics; CBS Colorado (October 7, 2025) |
| October 1, 2026 | Citibot contract "technically expired", per GovTech | GovTech (Denver Post) |
| A Tuesday shortly before October 14, 2026 | Council votes 9-3 against the five-year, $3.9 million extension | GovTech (Denver Post), posted October 14, 2026; Denver7 says "last week" on October 21, 2026 |
| October 21, 2026 | Denver7 reports the city is exploring "options" to keep Sunny | Denver7 |
| End of October 2026 | Contract paid through this point, per GovTech | GovTech (Denver Post) |

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| When does Sunny's money run out? | GovTech: "The contract for Sunny is paid for through the end of October." Denver7: the contract ends at the end of October, but there is "money budgeted for the chatbot through this year and into 2027." Neither says whether Sunny went offline. |
| What does "40%" measure? | GovTech: about 40% of the city's 311 customer service calls this year came "through Sunny and the city’s online reporting hub" (two channels together). Denver7: the city expects "a 40% increase in 311 calls" if Sunny goes away. These are different claims; neither isolates Sunny alone. |
| Is the bot inaccurate now? | The 2024 Westword test shows misreads and old links. The 2026 council claim of inaccuracy is reported as an argument, with no examples in the opened sources. The city's satisfaction rating is its own figure, with no method given. No opened source tested the bot in 2025 or 2026. |
| Exact vote date | GovTech says "Tuesday" in a story posted October 14, 2026; Denver7 on October 21 says "last week". We did not find the council record to confirm the date. |
| Who wrote the Westword test | Our copy shows no byline; the photos are credited to Catie Cheshire. |

## Where in the flow it broke

All steps come from Westword's 2024 test, except step 5.

1. **One word drove the reading.** The user wrote "Broadway" in a question about downtown construction. The bot matched the word to New York and gave its out-of-area refusal. It did not ask which Broadway. The user had to restate the question.
2. **The answer started but did not finish.** On lead in water, the bot named a program with "five main components" and stopped there, then linked a page about streams and lakes.
3. **The source set had a hole the bot did not name.** Lead-at-home information lives on Denver Water's site. The bot said it had no information, but did not point to the utility that does.
4. **Old pages came back as current help.** Event and restaurant questions returned 2021 and 2022 city pages, including a symposium "hasn’t occurred since 2019."
5. **Fewer people behind the bot.** In 2025 the city cut 311 phone hours and staff and pointed residents to Sunny 24/7. When the bot misreads or stalls after hours, the person route is closed until morning. No opened source reports a resident harmed by this; it is the setup, not a reported case.
6. **The feedback route sat outside the chat.** Per Westword, the city asks people to report bad replies through the city's online services hub by choosing "other." The opened sources do not say whether the chat itself has a report button.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on Westword's quoted replies and on news reports; we saw no chat logs.

- [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`). **Good fit.** For psilocybin, events and restaurants, Sunny answered with links that did not answer the question, many of them years out of date, such as the 2021 MLB All-Star game page.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Partial fit.** A safe, local question about Broadway got the out-of-area refusal because the word resembled an out-of-scope topic. The taxonomy entry is about risky-looking words; here the trigger was a scope rule, not a safety rule.
- [Channel chosen for organisational convenience](../goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md) (`channel-chosen-for-organisational-convenience`). **Partial fit.** The city cut 311 phone hours "to align with its budget" and pointed residents to the bot 24/7. No opened source shows a resident who needed a person and could not reach one.
- **Considered, not a fit.** [Dead-end "I don't understand" replies](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) (`dead-end-i-don-t-understand-replies`): when unsure, Sunny gave links rather than a bare could-not-understand line. [No way to report bad behaviour](../goals/measurement-and-feedback/failures/no-way-to-report-bad-behaviour.md) (`no-way-to-report-bad-behaviour`): a reporting route exists, though outside the chat; we found nothing saying reports go unread. [Partial answers to multi-part questions](../goals/effort-and-memory/failures/partial-answers-to-multi-part-questions.md) (`partial-answers-to-multi-part-questions`): the lead question was one question, not several. [Small talk and off-topic messages handled badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md) (`small-talk-and-off-topic-messages-handled-badly`): declining sports trivia is in scope for a 311 bot.

## How it differs from close cases

- [Hall County, Georgia Ask Hall County chatbot, April 2026](hall-county-georgia-ask-hall-county-chatbot-wrong-tag-title-and-property-tax-answers-april-2026.md): a county office warned within days that its bot gave wrong tax answers. In Denver the bot ran for more than two years, and the check that ended up mattering was a contract vote, not a public warning.
- [NYC MyCity chatbot gives businesses illegal advice, 2024](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a city bot stating wrong rules with confidence. Sunny's reported failures were softer: misread words, unfinished answers and old links.
- [IRS Automated Collection chatbot, TIGTA audit, June 2026](irs-automated-collection-chatbot-unrecognized-keywords-broken-links-tigta-audit-june-2026.md): a scripted bot that missed keywords and sent broken links. Sunny is an AI bot that answers from the city's own site; Westword reported no broken links, but many pointed to stale pages.

## What to measure

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Out-of-scope refusal on in-scope text | Share of out-of-area refusals where the user's next message restates the same topic with the city's name | Refusals on topics the bot is meant to decline, such as sports |
| Restate after an answer | Share of sessions where the user writes *I meant* or repeats the question with one added word | Users who ask a new, related question |
| Age of linked pages | Share of replies that link a page whose posted date is older than the team's set limit (the team picks the limit) | Old pages that are still the current rule, such as a law |
| Past-event links | Share of event replies that link an event whose date has passed | Archive questions where the user asked about a past event |
| Named-but-not-given content | Replies that say a program has components, steps or options and do not list them | Replies that list them or link a page that does |
| Unsure reply with no referral | Replies that say the bot is not sure and name no office, phone line or outside agency | Replies that say not sure and route to the right office |
| After-hours strand | Sessions outside staffed 311 hours that end with an unresolved question and no next step | Sessions that end with a service request filed |

## What a team can change

Our proposals, not Denver's or Citibot's. Each is a pass/fail check on a text log or a config. Status: Not yet run.

1. **Ask before refusing on a place name.** Pass: when a message names something that exists both in and out of the service area, the bot asks which one or assumes the local one and says so. Fail: it gives the out-of-area refusal.
2. **Finish what you start.** Pass: if a reply says a program has parts, it lists them or links the page that does. Fail: it names a count and stops.
3. **Name the right outside owner.** Pass: when the answer lives with another agency or utility, the bot names it and gives its contact. Fail: it says it has no information and stops.
4. **Keep old pages out of answers.** Pass: pages about past events, or past the team's set age, are excluded from links unless the user asked about the past. Fail: a 2021 event page is offered as current help.
5. **Say what happens after hours.** Pass: when the bot cannot help outside staffed hours, it says when 311 reopens and offers to file a request. Fail: the chat ends with no next step.
6. **Put the report button in the chat.** Pass: each reply has a way to flag it inside the chat, and flags reach a named team. Fail: the only route is a form elsewhere on the site.

## A cheap test

Status: Not yet run. Write 30 questions residents ask, including some that use a local name shared with a famous place (a street, park or neighborhood) and some whose answer lives with another agency. Ask each in every channel you offer. Record whether the bot asked which place, refused, finished its answer, named the right outside agency, and the posted date of each page it linked.

## What we could not verify

- Any council record, agenda item or video for the vote; we found none we could open, so the exact date rests on news reports.
- Which inaccurate answers, if any, councilmembers had in mind.
- Whether Sunny went offline after October 2026, or a new contract was signed.
- How the city measured its satisfaction rating, and over what period.
- The city audit Colorado Politics mentions (311 requests "misrouted to the wrong agency due to missing information"); we did not open it, and it may not concern Sunny.
- Whether the 2024 misreads and old links were fixed.
- The original Denver Post article; we read its text only as republished by GovTech.
- Westword's direct page returned error 403; we read it through the r.jina.ai text proxy.
- Seen only in search summaries, and kept out of the page text: a Governing quote page on the Kashmann remark, Citibot's own case study on Denver, a Johns Hopkins GovEx blog post, and a Colorado Politics story from August 2026 about a different contract.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.westword.com/news/denver-ai-chatbot-sunny-knows-basics-cant-help-on-hot-topics-20891202 | Westword (byline not in our copy; photos credited to Catie Cheshire) | 2024-06-01 | Yes, read 2026-10-29 as full text through r.jina.ai; direct request returned 403 |
| https://www.govtech.com/artificial-intelligence/denver-ai-chatbot-sunny-may-go-dark-after-contract-vote | Elliott Wenzler, The Denver Post, republished by GovTech via Tribune Content Agency | 2026-10-14 | Yes, HTML downloaded 2026-10-29, read as text |
| https://www.denver7.com/news/local-news/after-council-pushback-denvers-ai-chatbot-faces-uncertain-future | Ryan Fish, Denver7 | 2026-10-21 | Yes, HTML downloaded 2026-10-29, read as text |
| https://www.coloradopolitics.com/2025/10/06/denver-311-service-hours-reduced-sunny-chatbot-takes-on-more/ | Deborah Grigsby, Colorado Politics | 2025-10-06 | Yes, HTML downloaded 2026-10-29, read as text |
| https://www.cbsnews.com/colorado/news/denver-changes-311-service-hours-ai-chatbot-answer-questions | Jennifer McRae, CBS Colorado | 2025-10-07 | Yes, HTML downloaded 2026-10-29, read as text |
| https://web.archive.org/web/2026/https://www.westword.com/news/denver-ai-chatbot-sunny-knows-basics-cant-help-on-hot-topics-20891202 | Internet Archive | Not checked | Tried 2026-10-29; error 429. Not used. |

## Corrections

If you have the council record for the vote, the city's satisfaction survey method, Sunny's status after October 2026, or a newer test of the bot, tell us and we will fix this page.
