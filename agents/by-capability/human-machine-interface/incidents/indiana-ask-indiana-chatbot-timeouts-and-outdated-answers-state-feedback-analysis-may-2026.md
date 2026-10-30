---
title: "Indiana's 'Ask Indiana' state chatbot left users waiting with no answer and gave out-of-date season and event information, per the state's own feedback analysis, May 2026"
date: 2026-05-28
source: "https://www.in.gov/digital-state-survey/files/ask-indiana-feedback-analysis.pdf"
description: "A state analysis of 94 feedback responses on Indiana's IN.gov chatbot found 46% negative, citing timeouts, stale answers and broken links."
summary: "Indiana's 'Ask Indiana' chatbot went to public beta on IN.gov in June 2024 and became the homepage default in 2025. A state feedback analysis, marked 'Analysis generated May 28, 2026', covers 94 responses from June 21, 2024 to May 30, 2026. It reports sentiment of about 41% positive, 13% neutral and 46% negative, and says the bot 'struggles with outdated data, broken links, response timeouts, and edge-case queries.' Users quoted in it wrote 'I waited for over five minutes and never received an answer' and 'It pulled incorrect out of date information for 2024 seasons, not 2025 season.' The state's 2025 NASCIO award entry called the bot robust and reliable. Status: Needs review."
categories:
  - Government
  - Customer Service
  - Trust
patterns:
  - silent-failure-and-timeout
  - channel-chosen-for-organisational-convenience
  - over-refusal-of-ordinary-requests
---

**This page is a dated teardown of a state government's own feedback analysis of its website chatbot, for teams that put a generative AI assistant on a public agency's front page in place of search.** The product was "Ask Indiana," the chatbot on IN.gov, built on Tyler Technologies' platform with Azure OpenAI and Bing search over IN.gov content. The users were Indiana residents and state staff who filled in its feedback form. The moments were plain ones: a question typed three times with no reply, and a state park question answered with last year's season. Every fact below comes from a source we opened (listed at the end). The date above is the date the analysis says it was generated.

**Status: Needs review.** On 2026-10-30 the state's PDF could not be reached directly (connection refused from our network), so we read it as text through the r.jina.ai reader, which reported the file's server date as June 9, 2026. The Indiana Capital Chronicle launch story (Madelyn Hanes, May 15, 2025) and Indiana's NASCIO award entry (PDF, project dates through April 2025) were read the same way. Each English quote below was checked word for word against the saved text with a script, with curly and straight quote marks treated as the same.

> **Read this first.** This is a summary of a state document, a news story and a state award entry, not a finding of fact about Indiana's systems and not legal advice. The feedback is self-selected: 94 responses, about 86 of them legitimate, against roughly 60,000 questions the state says the bot had answered by its award entry. The percentages describe people who chose to leave feedback, not all users. No opened source makes a legal or regulatory claim about the bot, and this page makes none. Design guidance here needs review by a person. We name only state officials and reporters who appear in the sources.

**Channel note.** This is a chat incident: a text chat window on a state website. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat. The analysis lists "Speech input issues reported" in its late period; voice signals, such as speech input that fails silently, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The launch.** NASCIO entry: "Ask Indiana was deployed to Beta starting in June 2024," under the search bar. On April 22, 2025 the state made it "the default customer engagement option" on the homepage. It says the bot pulls from nearly 100,000 IN.gov pages.
- **The goal.** NASCIO entry: "The primary goal is to get people off IN.gov as quickly as possible." It counts a 10% drop in homepage time and monthly searches falling to "less than half" of the 954,779 average as success.
- **The state's own view in 2025.** "The chatbot has proven its robustness and reliability as a valuable resource for residents seeking access to state services."
- **A reporter's test, May 2025.** The Capital Chronicle asked "Can my employer ask if I am pregnant?" and got: "I'm sorry, but I cannot provide information on this topic." Asked about Medicaid spending, the bot opened with "As of May 2024" figures.
- **The feedback, 2024 to 2026.** The analysis: about 41% positive, 13% neutral and 46% negative; 45% would use it again and 41% would not. It says the bot "performs well for straightforward government information lookups but struggles with outdated data, broken links, response timeouts, and edge-case queries."
- **No reply, no signal.** Under "No Response / Timeouts (Critical Issue)": "I waited for over five minutes and never received an answer." "Typed in my question 3 times with no results." "No indication that it was in the middle of thinking of a response."
- **Stale answers.** "It pulled incorrect out of date information for 2024 seasons, not 2025 season." "Kept giving me government meetings that had already happened." "The 4H fair happened in July and the Woods on Wheels does not happen in Hancock county this weekend."
- **Vague links.** "It just says to try online, without a link or source." Two broken IN.gov addresses are listed.
- **Users who wanted search back.** "Just take me to the webpage, or at least give me the option to."
- **What worked.** "It provides a detailed answer, and even better it links to the citations used so I can go and double check myself." Testers from other states were positive.
- **The trend.** Late 2025 to May 2026: "Higher proportion of negative public feedback" and "Continued timeout/no-response problems."

## Timeline

| When | What | Source |
|---|---|---|
| June 2024 | Public beta on IN.gov, under the search bar; feedback period starts June 21, 2024 | NASCIO entry; feedback analysis |
| October 2024 | State signs a four-year, $22 million web portal contract with Tyler Indiana | Capital Chronicle |
| 2025-04-22 | Full production; chatbot becomes the homepage default | NASCIO entry |
| 2025-05-15 | Capital Chronicle tests the bot; one question refused | Capital Chronicle |
| Oct 2024 to mid-2025 | Recurring stale seasonal and event answers | Feedback analysis |
| Late 2025 to May 2026 | More negative public feedback; timeouts continue | Feedback analysis |
| 2026-05-28 | Analysis generated | Feedback analysis |

## What the state said

- **To the Capital Chronicle (May 2025).** Graig Lubsen of the Indiana Office of Technology said the bot was created to modernize how residents reach state services. The paper says the terms tell users the assistant "may not always be correct or up to date."
- **In the NASCIO entry.** Plans include "Automated transcript reviews to identify potential issues" and "Quick guardrail adjustments to correct inaccurate information." A handoff to people is "(Early stages) Allows transfer to human agents for complex queries."
- **On the 2026 analysis.** No opened source quotes the state on its findings or on fixes.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Is it reliable | NASCIO entry (2025): "robustness and reliability." Feedback analysis (2026): 46% negative, timeouts a "Critical Issue." |
| When it launched | NASCIO: beta June 2024, production April 22, 2025. Capital Chronicle (May 15, 2025): a "new" chatbot on a redesign launched "last week." |
| Project dates | NASCIO PDF title: "April 2024-April 2025." Its body: "October 2023 – April 2025." |
| Local events | NASCIO: 226 local government sites were "purposefully excluded." Feedback: "Events / Local Info" marked "Negative (inaccurate)," with a Hancock County complaint. |
| Analysis dates | Covers feedback to May 30, 2026, but says it was generated May 28, 2026. Its rating table is garbled in the text we read; we use only its stated totals. |

## Where in the conversation flow it broke

Based on the feedback quotes and the two state documents, and only as far as they go. Each step is a place a check could have caught it.

1. **The bot replaced the front door.** Search moved behind the chat in April 2025. Users who wanted a page and not an answer had to ask for one.
2. **The wait had no end and no cue.** Users report minutes of silence and no sign the bot was working. A user who retypes three times is a timeout the logs can count.
3. **Date-sensitive answers ignored the date.** Season prices, deer season, county fairs and meetings were answered from past pages, with no check that the date had passed.
4. **Out-of-scope questions got in-scope answers.** Local content was excluded by design, yet local event questions were answered, and wrongly.
5. **A fair question met a wall.** The pregnancy question got a refusal with only a pointer to "Indiana's official website."
6. **The success metric pointed the wrong way.** Less time on IN.gov counts as a win whether a user found the answer or gave up.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on self-selected feedback quotes and one reporter's test; no opened source shows the bot's logs.

- [Silent failure and timeout](../goals/response-time/failures/silent-failure-and-timeout.md) (`silent-failure-and-timeout`). **Good fit.** Users waited over five minutes, saw no error and retyped the question. Not strong only because the analysis does not say how often it happened.
- [Channel chosen for organisational convenience](../goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md) (`channel-chosen-for-organisational-convenience`). **Partial fit.** The bot became the default to get people off the site fast, and users asked for search back. But search stayed available, and no source says cost drove the choice.
- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Partial fit.** A common workplace question was refused. One reporter test only; no source says how often it happens.
- **Considered, not a fit.** [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): answers carry citations, which users praised. [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`): the complaint was too few specific links, not too many. [No accessible working or done signal](../goals/accessibility/failures/no-accessible-working-or-done-signal.md) (`no-accessible-working-or-done-signal`): no source says the users were blind. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`): the 50-question test set was weak on dates, not on typos.
- **Possible gap for a person to judge.** No ID covers a bot that answers a date-bound question (a season, an event, a meeting) from a page whose date has passed. This is a proposal, not a decision.

## How it differs from close cases

- [Hall County, Georgia chatbot gave wrong tag, title and tax answers, April 2026](hall-county-georgia-ask-hall-county-chatbot-wrong-tag-title-and-property-tax-answers-april-2026.md): a county warned residents about wrong answers. Here the state's own feedback shows the problem; no public warning is reported.
- [Denver's Sunny 311 chatbot, October 2026](denver-sunny-311-chatbot-outdated-links-misread-questions-council-rejects-contract-october-2026.md): outdated links and misread questions, then a council vote. Here no opened source reports a contract decision.
- [Ask CAL FIRE chatbot, July 2025](cal-fire-ask-cal-fire-chatbot-cannot-answer-evacuation-orders-stale-containment-july-2025.md): stale data found by reporters. Here users found it, in the state's own form.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are PLANNED only and are not detected or measured. Each can be computed from chat logs and the feedback form.

| Signal | How to compute from logs |
|---|---|
| No-reply rate | Share of user messages with no bot reply within a set time |
| Retype rate | Share of sessions where the user sends the same or a near-same question two or more times in a row |
| Stale-date answers | Share of replies on seasons, events or meetings that cite a page whose date is past |
| Out-of-scope local answers | Share of county or city questions answered with content instead of a referral |
| Refusal dead ends | Share of refusals that give no specific page, office or phone number |
| Search-back requests | Share of feedback or chats asking for search or for a link to the page instead of an answer |

## What a team can change

Our proposals, not Indiana's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Thresholds are for the team to set.

1. **Never leave the user waiting blind.** Pass: in a test with a forced backend delay, the user sees a working cue at once and a plain error with a retry and a search link before a set time.
2. **Check the date on date-bound answers.** Pass: asked "how much is camping this season," the bot cites the current season's page or says it has no current figure.
3. **Hold the scope you set.** Pass: a county event question gets a referral to the county, not an answer from state pages.
4. **Make every refusal a next step.** Pass: a refused question names a specific page or office, not only "Indiana's official website."
5. **Keep search one click away.** Pass: from the chat, a user reaches classic search results for the same words in one click.
6. **Measure success by answers, not exits.** Pass: the team's dashboard reports retype and no-reply rates next to time on site.

## What we could not verify

- How many sessions hit timeouts, or whether timeouts were fixed after May 2026.
- Who wrote the analysis or how it was generated; it names no author.
- Whether the pregnancy refusal still happens; we did not test the bot.
- The 2026 NASCIO entry for Indiana and a search summary saying the launch disclaimer called the tool a beta that could make mistakes. Seen only in search results; not used.
- An earlier IN.gov site feedback analysis (ingov-feedback-analysis.pdf), seen in search results only.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.in.gov/digital-state-survey/files/ask-indiana-feedback-analysis.pdf | State of Indiana (no author named) | Generated 2026-05-28; server date 2026-06-09 | Yes, 2026-10-30, through r.jina.ai as text; direct connection refused. Quotes checked word for word. |
| https://indianacapitalchronicle.com/2025/05/15/meet-ask-indiana-state-governments-new-ai-resident-assistant-chatbot/ | Indiana Capital Chronicle (Madelyn Hanes) | 2025-05-15 | Yes, 2026-10-30, through r.jina.ai as text. Quotes checked word for word. |
| https://www.nascio.org/wp-content/uploads/2025/09/IN-_Artificial-Intelligence.pdf | Indiana Office of Technology, NASCIO award entry | Project through April 2025; posted 2025-09 per URL | Yes, 2026-10-30, through r.jina.ai as text. Quotes checked word for word. |

## Corrections

If you have Indiana's response to the 2026 analysis, timeout or accuracy data from the bot's logs, or a newer test of Ask Indiana from a source we can open, tell us and we will fix this page.
