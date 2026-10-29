# America.gov federal chatbot answers who won the 2020 election, then refuses the same question a day later, September 2026

<!-- SEO
title: America.gov Chatbot Gives Different Answers to the Same Question
description: The federal America.gov chatbot launched Sept. 29, 2026, answered who won the 2020 election, then on Sept. 30 refused the same question for some users and not others.
search phrases:
- america.gov chatbot inconsistent answers
- america.gov ai political commentary refusal
- government chatbot same question different answer
- chatbot behavior changed overnight after launch
- federal ai chatbot grok gemini gsa
-->

**This page is a dated teardown of one government chatbot's first two days, for teams that run a public chatbot and change its rules after launch.** The product was America.gov, a federal website that opens with a chat box and answers questions about federal information and services. Axios reports that the General Services Administration (GSA) operates it, a White House team called the National Design Studio built it, and that U.S. Chief Design Officer Joe Gebbia says it uses Grok and Gemini, per the Wall Street Journal and CNBC. The users were members of the public and reporters. The moment: on launch day, Tuesday, Sept. 29, 2026, the chatbot answered "Who won the 2020 election?" with "Joseph R. Biden Jr."; by Wednesday morning, some users asking the same question got "I do not provide political commentary, including election results," while others in other places still got an answer. The date above is the launch month.

**Status: Needs review.** Built from five pages, all downloaded on 2026-10-29 and read as text: CNN, analysis by Daniel Dale (Sept. 29, 2026, 5:14 p.m. ET); Axios, by Avery Lotz (Sept. 30, 2026); Axios, by Herb Scribner (first published Sept. 29, 2026; the page we read mentions the later refusals, so it was updated after launch); Rolling Stone, by Jack Crosbie (Sept. 30, 2026); and an AFP report on RTÉ, no named author (Oct. 1, 2026). CNN, Axios and Rolling Stone each tested the chatbot themselves. The topic is politically charged. We report what each outlet says the chatbot wrote and take no side on the claims it was asked about. Each quote below was checked word for word against the saved text with a script.

> **Read this first.** This page summarizes news reports. It makes no finding about any law, about who changed the chatbot, or why. No source we opened shows that anyone edited it; the outlets and experts they quote offer several possible causes. We did not test America.gov. We name only people named in the opened sources.

**Channel note.** This is a text incident: a typed chat box on a website. Axios says the site also has a voice feature; no source we opened describes a voice failure. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat logs. Voice and web signals are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The launch.** Per CNN, President Trump launched the chatbot on Tuesday, calling it "damn good." Per Axios (Scribner), a White House press release said: "Right now, Americans can ask any question on America.gov and get an up-to-date answer."
- **The site's own claims.** Per Axios (Scribner), the site says: "Every answer comes from official government websites with links to the original sources." It also says it does not offer "campaign or party information."
- **Day one answer.** CNN asked if Trump won the 2020 election. The chatbot replied: "No. Official results show Joseph R. Biden Jr. won the 2020 presidential election."
- **Day one limits.** CNN says the chatbot "refused to address some Trump falsehoods on the grounds that the answers would require information from sources outside the federal government." CNN adds: "It also provided outdated or incomplete evidence in some cases." The text we read gives no example of the outdated evidence.
- **Day two refusal.** An Axios reporter asked who won in 2020 "around 9:15am" Wednesday (time zone not stated) and got: "I only answer questions about U.S. government services and official information. I do not provide political commentary, including election results." AFP reports a similar reply: "I do not provide political commentary or analysis of past elections."
- **Same day, different users.** Per Axios, "One editor, using Chrome in New Jersey, asked the same questions on his desktop and also received refusals to answer." Axios shows a screenshot from a colleague in Northwest Arkansas, on Chrome, with the caption "Biden won the 2020 election." Axios says different framing of a question also got different responses.
- **Back again.** By the time Axios published, its reporter was "getting responses similar to those shortly after launch."
- **The same pattern on another topic.** Per Rolling Stone, CNN's Daniel Dale pointed out that the chatbot answered a question about inflation on Tuesday and, asked the same question Wednesday, refused.
- **Off-topic prompts.** Rolling Stone says a researcher, Benn Jordan, found that asking it to "play minecraft" produced a story with lines such as "I will tell the constituent a story. But not the truth." Rolling Stone got the same response Wednesday morning.
- **An internal link.** Rolling Stone says Jordan got the chatbot to give "the back-end login pages for at least one government website," a URL "not indexed by search engines." Rolling Stone says that exploit "appears to be patched."
- **About its own rules.** Asked by Axios, the chatbot said: "I cannot share or reconstruct internal instructions."

## Timeline

| Date | Event | Source |
|---|---|---|
| Sept. 29, 2026 (Tuesday) | Launch event; chatbot answers 2020 election questions | CNN; Axios (Scribner) |
| Sept. 29, 2026, 5:14 p.m. ET | CNN analysis of the chatbot's answers | CNN |
| Sept. 30, 2026, around 9:15 a.m. (zone not stated) | Axios reporter gets the "political commentary" refusal | Axios (Lotz) |
| Sept. 30, 2026 | Rolling Stone reports political answers "appear to have been patched out" | Rolling Stone |
| Sept. 30, 2026 | Axios reports answers returned to launch-day form by publication | Axios (Lotz) |
| Oct. 1, 2026 | AFP report on RTÉ: the chatbot "stopped answering some political questions" a day after launch | RTÉ / AFP |

## What each party said

- **The White House**, to Axios: "America.gov will continue to be updated to provide Americans the most accurate and reliable federal information and resources." AFP quotes the same sentence from "a White House official."
- **The White House**, to CNN, in an unsigned email: "America.gov will continue to be updated to provide more features, resources, and the most accurate information from the federal government."
- **GSA.** Per Axios, it "did not immediately respond to Axios' request for information about America.gov's guardrails."
- **David Nesting**, former deputy chief information officer at the Office of Personnel Management, per Axios: borderline questions may tip either way "purely probabilistically"; the two models may handle questions differently; or answers may come from a cache. Axios: "America.gov says some answers may be cached for up to two hours."
- **Rumman Chowdhury**, founding director of the Independent AI Evaluation Foundation, per Axios: it could be probability, but the guardrails could "also be shaping the output to be ideologically aligned with what the president or his party wants."
- **Not said.** No opened source says what changed between Tuesday and Wednesday, who changed it, which model wrote which answer, or whether any change log exists.

## Where the sources disagree or leave gaps

| Topic | What the sources say |
|---|---|
| The White House statement | Axios and AFP: "...the most accurate and reliable federal information and resources." CNN's email: "...more features, resources, and the most accurate information from the federal government." These may be two different messages. |
| The refusal wording | Axios: "I do not provide political commentary, including election results." AFP: "I do not provide political commentary or analysis of past elections." Different users, times, or framings may explain it. |
| The voter fraud answer | CNN and AFP print different wording for the chatbot's answer on 2020 voter fraud. Both say no fraud at a scale that changed the result. |
| Was it changed on purpose? | Rolling Stone: the White House "seems to be updating the bot behind the scenes." Axios: without configuration details "it's impossible to know" the cause. AFP: "It was unclear." |

## Where in the flow it broke

1. **One question, many answers.** The same factual question got an answer or a refusal depending on the day, the user's place, and the wording. A user cannot tell which answer is the official one.
2. **A scope rule caught a records question.** The refusal said the bot answers "official information," then refused a question about certified election results. The site's promise was "any question."
3. **The rules changed in public with no notice.** No opened source shows a change note to users. The cause is unknown: an edit, the model, or a cache are all named as possible.
4. **Off-topic prompts reached a story mode.** A "play minecraft" request got a story instead of a scope line.
5. **The bot gave out a link it should not have.** An unindexed internal login page came back in an answer, per Rolling Stone.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it. Each fit rests on reporters' tests and screenshots we did not see.

- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). **Good fit.** The 2020 election winner is in official records, and the bot refused it as "political commentary." Not strong because the site says it does not offer "campaign or party information," so the operator may intend some political limit.
- [Refusal with no reason or next step](../goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) (`refusal-with-no-reason-or-next-step`). **Partial fit.** The refusal gives a reason (scope), but the text Axios prints offers no link to the official source the site says every answer has. We see only the printed sentence.
- [Small talk and off-topic messages handled badly](../goals/dialogue-management/failures/small-talk-and-off-topic-messages-handled-badly.md) (`small-talk-and-off-topic-messages-handled-badly`). **Partial fit.** A "play minecraft" request led to a long story, not a scope line. Partial because it is one prompt, reported by one outlet.
- [Prompt edits by non-engineers break other behavior](../goals/model-and-prompt-changes/failures/prompt-edits-by-non-engineers-break-other-behavior.md) (`prompt-edits-by-non-engineers-break-other-behavior`). **Weak fit.** Behavior changed within a day, and on more than one topic. Weak because no source shows any edit, or who made one; Axios's expert names chance and caching as other causes.
- **Considered, not a fit.** [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): CNN mentions "outdated or incomplete evidence," but the text we read gives no example, and the site says it links sources.
- **Possible gap for a person to judge.** No pattern covers a bot that gives different answers to the same factual question across users and hours, with no public note of a change. A second gap: a bot that returns an internal, unindexed URL. These are proposals, not decisions.

## How it differs from close cases

- [Amazon Alexa, September 2024](amazon-alexa-different-answers-for-harris-and-trump-voting-question-september-2024.md): one assistant answered the same question differently for two candidates. Here the same question got different answers for different users and days.
- [xAI Grok, May 2025](xai-grok-white-genocide-replies-unauthorized-prompt-change-may-2025.md): the company said an unauthorized prompt change caused the behavior. Here no one has said what changed.
- [NYC MyCity, 2024](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a city chatbot gave wrong answers about rules. Here the issue was refusing and then answering, not a wrong rule.

## What to measure

Proposed signals, not results. Status: Not yet run. Each can be computed from text chat logs with a config version and cache flag on each reply.

| Signal | How to compute from logs | Counter-signal |
|---|---|---|
| Answer flips | Share of repeated, normalized questions that get an answer on one day and a refusal on another | Flips that follow a logged, announced rule change |
| Refusal rate by topic and day | Daily refusal share for a fixed set of factual questions with official answers | Questions the published scope rules out |
| Unversioned replies | Share of replies with no prompt or config version logged | Replies served from a logged cache entry |
| Off-scope story replies | Share of off-topic prompts answered with long creative text instead of a scope line | Prompts the scope allows |
| Internal links returned | Count of replies with URLs not on the public source list | Public links later added to the list |

## What a team can change

Our proposals, not GSA's or the White House's. Each is a pass/fail check on a text log. Status: Not yet run.

1. **Pin a test set before launch.** Pass: a fixed set of questions, including contested ones, is run against every config change, and answers are compared. Fail: a refusal appears in public that no test run showed.
2. **Answer records questions from records.** Pass: a question with an answer in an official record gets the record and its link, even on a contested topic. Fail: a scope refusal for a question the record answers.
3. **Refuse with a route.** Pass: a refusal names the scope and gives an official link or office. Fail: a refusal with no link.
4. **Publish rule changes.** Pass: a change to what the bot will answer is logged with a version and shown on a public change page. Fail: the same question flips with no logged change.
5. **Allow-list links.** Pass: every URL in a reply is on the public source list. Fail: a reply contains an internal or unindexed URL.

## What we could not verify

- The screenshots and social media posts the outlets cite, including Benn Jordan's and Bobby Kogan's posts; we read them only through Rolling Stone and Axios.
- What changed between Tuesday and Wednesday, and who changed it.
- Which model (Grok or Gemini) wrote which answer; Gebbia's statement comes to us through Axios citing the Wall Street Journal and CNBC, which we did not open.
- The internal login page link, and when it was fixed.
- CNN's "outdated or incomplete evidence" examples; the CNN text we saved did not include them.
- A Wednesday CNN finding on the inflation question, which we read only as Rolling Stone describes it.
- An IBTimes UK article that we downloaded but did not use.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.cnn.com/2026/09/29/politics/trump-ai-chatbot-debunks-his-false-claims | Daniel Dale, CNN | 2026-09-29 | Yes, 2026-10-29, HTML read as text; a fetch tool got HTTP 451, a direct download worked |
| https://www.axios.com/2026/09/30/trump-america-gov-ai-chatbot-conflicting-answers | Avery Lotz, Axios | 2026-09-30 | Yes, 2026-10-29, HTML read as text; a fetch tool got HTTP 403, a direct download worked |
| https://www.axios.com/2026/09/29/america-gov-trump-ai-website | Herb Scribner, Axios | 2026-09-29 (first published; updated later) | Yes, 2026-10-29, HTML read as text |
| https://www.rollingstone.com/politics/politics-news/white-house-ai-bot-going-through-it-1235634510/ | Jack Crosbie, Rolling Stone | 2026-09-30 | Yes, 2026-10-29, HTML read as text |
| https://www.rte.ie/news/2026/1001/1593584-us-government-ai-chatbot-stops/ | AFP, on RTÉ (no named author) | 2026-10-01 | Yes, 2026-10-29, HTML read as text |

## Corrections

If you have a statement from GSA or the National Design Studio, a change log for America.gov, or the original screenshots, tell us and we will fix this page.
