---
title: "Dukaan: CEO says an AI chatbot let the e-commerce platform lay off 90% of its support team, and posts speed figures that draw backlash, July 2023"
date: 2023-07-10
source: "https://edition.cnn.com/2023/07/12/business/dukaan-ceo-layoffs-ai-chatbot/index.html"
description: "How Dukaan's CEO said an AI chatbot let the company lay off 90% of its support team in July 2023, the speed figures he posted, and the public backlash."
summary: "On July 10, 2023, Suumit Shah, CEO of the Bengaluru e-commerce platform Dukaan, posted on Twitter that the company had laid off 90% of its support team because of an AI chatbot. He said time to first response went from 1m 44s to instant, resolution time from 2h 13m to 3m 12s, and support costs fell about 85%. He said the bot, Lina, marked 1,400 tickets resolved in one night. CNN (July 12, 2023) reported that Shah said the 23 layoffs were made in September. Many users called the post insensitive. No opened source checks the figures or reports a reversal."
categories:
  - Customer Service
patterns:
  - answer-and-go-conversation
  - escalates-too-early-or-too-late
  - talk-to-a-human-ignored-or-looped
---

**This page is a dated teardown of public posts and reporting on Dukaan replacing most of its customer support team with an AI chatbot, for teams that plan to cut support staff because a chatbot's own dashboard says it answers faster.** The product was Dukaan, a Bengaluru-based platform for online stores, and its support chatbot, Lina. The users were the merchants who wrote to Dukaan support. The moment was a Twitter thread in which the CEO announced the cut and posted speed figures. Every fact below comes from a source we opened (listed at the end). No opened source has Dukaan's support logs or an outside test of the bot.

**Status: Needs review.** Three of Suumit Shah's July 10, 2023 tweets (through Twitter's public embed service), CNN, MediaNama, Business Today, Storyboard18, People Matters, Interesting Engineering, The Decoder, HRD (HCA Magazine) and the OECD.AI incident entry were downloaded as raw HTML or JSON on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. Business Insider, The Washington Post, The Economic Times and VCCircle were not opened.

> **Read this first.** This is a summary of public posts and reporting, not a finding of fact, and not legal or employment advice. It does not say whether Dukaan broke any law or treated any worker unfairly. The speed and cost figures are the CEO's own claims; no opened source checked them. We name no laid-off worker and no customer.

**Channel note.** Text chat. Per Shah's thread and the reporting, the bot handled live chats and support tickets in text. This phase of the knowledge base is chat-first: the text-chat signals and checks below are proposed; voice is planned and not covered here.

## What happened (as reported)

- **The post.** On July 10, 2023, Shah tweeted: "We had to layoff 90% of our support team because of this AI chatbot." The same tweet said "Tough? Yes. Necessary? Absolutely." It listed three results: "Time to first response went from 1m 44s to INSTANT!", "Resolution time went from 2h 13m to 3m 12s" and "Customer support costs reduced by ~85%".
- **The reason he gave.** A second tweet that day said: "Given the state of economy, startups are prioritizing "profitability" over striving to become "unicorns," and so are we." It added: "Customer Support had been a struggle for us since long & fixing it felt like an opportunity to me."
- **How the bot was built.** CNN (Anna Cooban, July 12, 2023) reports Shah said the bot was "built by one of the firm's data scientists in two days." People Matters (Samriddhi Srivastava, July 12, 2023) names him as lead data scientist Ojasvi Yadav. Per People Matters, the first demo answered general questions but had trouble with account-specific ones, such as delayed payouts. It quotes Shah: "A day later, he came up with another demo and this time bot answered both generic as well as account-specific questions, instantly."
- **The "resolved" count.** MediaNama (Kamya Pandey, July 12, 2023) reports the bot was tested with Dukaan's VIP community, and that within one night "1400 support tickets have been marked as 'resolved' by Lina," per Shah. HRD (Dexter Tilo, October 4, 2023) says Lina marked as resolved 200 live chats and 1,400 support tickets.
- **The product launch.** MediaNama and Storyboard18 (July 11, 2023) report Shah used the same thread to launch Bot9, a service for other companies to build support chatbots. Storyboard18 says its API uses ChatGPT and costs $69 per month.
- **The timing.** CNN: "Shah told CNN Wednesday that the 23 layoffs were made in September." CNN also says he told VCCircle at the time that a shift from smaller businesses to consumer-facing brands reduced the need for live chat or calls.
- **The backlash.** Business Today (Tarun Mishra, July 11, 2023) ran the headline "'Heartless decision,' say netizens." A user asked what help the laid-off staff got. Shah replied in Hindi that he would cover it in a LinkedIn post; Interesting Engineering translates part of the reply as people on Twitter preferring "profitability" over "sympathy." Storyboard18 quotes one user: "The support team was laid off here because the business is failing and funding is dry, not because of AI."
- **One customer's report.** MediaNama embeds a July 10, 2023 reply from a user who says the bot "wasn't answering as I needed it to." The user says they reworded questions several times and did not renew a premium plan. This is one public post, not a measured failure rate.

## What the company said

- **To CNN.** Shah said he believed "in a future where AI and humans work together, each doing what they do best." CNN says Dukaan was still hiring for engineering, marketing and sales roles.
- **To The Washington Post, per HRD.** HRD quotes Shah calling it a "no-brainer" to replace the team with a bot that is "like 100 times smarter." We did not open the Post's article.
- **What we did not find.** No opened source has a Dukaan statement on how "resolution time" or "resolved" was measured, how a merchant reaches a person now, or what support the laid-off staff received.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| When the layoffs happened | CNN: Shah said they were "made in September," with no year given. Interesting Engineering says September 2022, "10 months ago," citing CNN. HRD says they "took place early this year." The July 10 tweet gives no date. |
| How many people | The tweet says 90%. CNN says 23 layoffs. No opened source gives the team's full size. |
| Account-specific questions | Interesting Engineering says the bot "fell short" on account questions. People Matters says that was the first demo and a second demo a day later handled them. The Decoder (Matthias Bastian, July 15, 2023) says it answered both kinds. |
| The bot's name | Every opened source says Lina, except one Storyboard18 line that calls it "Lisa." |
| The model | The Decoder says "presumably GPT-4-based." Storyboard18 says Bot9's API uses ChatGPT. No Dukaan source names the model behind Lina. |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The ask.** A merchant wrote in with a question. Shah's own example of a hard one was about a payout pending for days (per Interesting Engineering and People Matters).
2. **The first reply.** The bot replied at once. This is the "1m 44s to INSTANT" claim; it measures speed, not whether the answer fit.
3. **The answer.** For general questions, Shah says the bot was accurate. For account questions, the sources disagree on whether it worked. One user says it did not answer theirs.
4. **The close.** The bot "marked" tickets "resolved." No opened source says whether merchants agreed, came back, or asked again.
5. **The person.** With 90% of the team gone, no opened source says how or when a merchant reaches a human. One user joked, per Interesting Engineering, that the best part of a chatbot is when it says it is connecting you to a human.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). No opened source shows a full failed conversation, so no fit is core.

- [Answer-and-go conversation](../goals/conversation-leadership/failures/answer-and-go-conversation.md) (`answer-and-go-conversation`). **Partial fit.** Shah's headline count is tickets "marked as 'resolved'" by the bot overnight. That page's lesson is that a closed chat is not a solved problem. One user's post says the bot replied but did not solve the issue.
- [Escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) (`escalates-too-early-or-too-late`). **Partial fit.** Cutting most of the team decides, in effect, how much a person can take over. No opened source says when Lina hands off, or reports a late handoff.
- ["Talk to a human" ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`). **Weak fit.** It is the risk to test after a cut like this. No opened source shows a merchant asking for a person and being refused.
- **Considered, not a fit.** [Survey bias](../goals/measurement-and-feedback/failures/survey-bias.md) (`survey-bias`): no satisfaction survey was cited; the claims were speed and cost. [Handoff outside staffed hours with no alternative](../goals/human-handoff/failures/handoff-outside-staffed-hours-with-no-alternative.md) (`handoff-outside-staffed-hours-with-no-alternative`): no source gives staffed hours. [Reviewing only failures](../goals/measurement-and-feedback/failures/reviewing-only-failures.md) (`reviewing-only-failures`): no source says how Dukaan reviewed chats. `cold-transfer` and `undisclosed-bot-identity`: no source reports a transfer, and Shah announced the bot publicly.
- **Possible gap for a person to judge.** No taxonomy entry covers sizing a support team from the bot's own speed and "resolved" figures, before anyone checks repeat contacts or churn. This is a proposal, not a decision.

## How it differs from close cases

- [Klarna AI assistant (2024 to 2025)](klarna-ai-assistant-customer-service-reversal-2025.md): Klarna published a share of chats and said customers could still choose a live agent; in 2025 its CEO said it was recruiting humans again. Dukaan announced the cut itself, with speed figures, and no opened source reports a reversal.
- [Commonwealth Bank voice bot (August 2025)](commonwealth-bank-ai-voice-bot-job-cuts-reversed-august-2025.md): a voice bot, a union dispute and a reversal the bank called an error. Dukaan was text chat, the reaction came from social media, and the cut stood in every source we opened.
- [CFPB on bank chatbot doom loops](cfpb-bank-chatbot-doom-loops.md): a regulator describing customers stuck in loops with no person. Here no loop is reported; the open question is whether a person was reachable at all.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice signals are planned only. Each is computable from chat and ticket logs.

- Share of bot-"resolved" tickets where the same merchant writes again on the same topic within a set window.
- Share of chats where the user rewords the same question two or more times before the chat ends.
- Share of chats where the user asks for a person, and median time from that request to a person's first message.
- Share of account-specific chats (payout, order, billing) the bot closes without a person, against the same share for general questions.
- Median time from first message to the user confirming the fix, kept apart from time to first reply.
- Plan renewal rate for merchants whose last contact was bot-only, against those who reached a person.

## What a team can change

Our proposals, not Dukaan's. Each is a pass/fail check on a transcript, a test run or a log query. Status: Not yet run. Windows and thresholds are for the team to set.

1. **"Resolved" means the user agreed.** Pass: a log query finds no ticket marked resolved by the bot without a user confirmation or a set quiet period with no reply.
2. **Measure repeats before cutting staff.** Pass: the staffing plan shows the repeat-contact rate for bot-closed tickets next to the speed figures.
3. **A person is one ask away.** Pass: a test user who types "talk to a human" gets a person, a ticket number or a stated wait time in the next reply.
4. **Account questions get a path.** Pass: a test question about a pending payout either shows the real status from the account or offers a person; it never gives a generic answer and closes.
5. **Don't count speed as success.** Pass: the support dashboard shows time to fix next to time to first reply.
6. **Don't over-correct.** Pass: a test user with a general how-to question gets the answer from the bot, without being pushed to a queue.

## What we could not verify

- Whether the speed and cost figures are accurate, and how "resolution time" was measured. No opened source checked them.
- When the layoffs happened and how many people were on the team. CNN, Interesting Engineering and HRD differ (see the table).
- That the cut was 23 of 26 staff. Seen only in a search summary attributed to Business Insider; not opened, not used.
- Shah's remarks to The Economic Times and VCCircle, and The Washington Post interview. Seen only as quoted by others or in summaries.
- Shah's promised LinkedIn post about help for laid-off staff. Not found or opened.
- Any later outcome: whether Dukaan rehired, kept the bot, or saw churn. A StartupItalia one-year follow-up appeared only in a search summary; not opened.
- Seen only in search summaries, not used: IT World Canada, Outlook Business, ChannelNews, Supercar Blondie, Gigazine, Futurezone, Tweaktown, Inquirer, Indian Defence Review, Tabla, HR Katha, The Sun (Malaysia) and ET CIO. India Retailing was downloaded but its article text did not load, so it is not used.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://twitter.com/suumitshah/status/1678460567000850450 | Suumit Shah (X/Twitter) | 2023-07-10 | Yes, 2026-10-28, via Twitter's public oEmbed JSON; quotes checked word for word |
| https://twitter.com/suumitshah/status/1678460569844588547 | Suumit Shah (X/Twitter) | 2023-07-10 | Yes, 2026-10-28, via oEmbed JSON; quotes checked word for word |
| https://twitter.com/suumitshah/status/1678503672206983171 | Suumit Shah (X/Twitter) | 2023-07-10 | Yes, 2026-10-28, via oEmbed JSON |
| https://edition.cnn.com/2023/07/12/business/dukaan-ceo-layoffs-ai-chatbot/index.html | CNN (Anna Cooban) | 2023-07-12 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.medianama.com/2023/07/223-ecommerce-platform-dukaan-replace-customer-support-team-ai-chatbot/ | MediaNama (Kamya Pandey) | 2023-07-12 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.businesstoday.in/amp/latest/trends/story/heartless-decision-say-netizens-after-dukaan-replaces-90-staff-with-ai-chatbot-for-customer-support-389276-2023-07-11 | Business Today (Tarun Mishra) | 2023-07-11 | Yes, 2026-10-28, raw HTML read as text |
| https://www.storyboard18.com/how-it-works/dukaan-ceo-called-out-for-being-insensitive-after-posting-about-replacing-support-staff-with-ai-chatbot-10074.htm | Storyboard18 (staff) | 2023-07-11 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://www.peoplematters.in/news/strategic-hr/after-firing-90-staff-for-ai-bot-dukaan-ceo-says-log-profitability-dekhte-hai-sympathy-nahi-38413 | People Matters (Samriddhi Srivastava) | 2023-07-12 | Yes, 2026-10-28, raw HTML read as text; quote checked word for word |
| https://interestingengineering.com/innovation/indian-startup-fired-staff-replaced-ai-chatbot | Interesting Engineering (Sejal Sharma) | 2023-07-14 | Yes, 2026-10-28, raw HTML read as text |
| https://the-decoder.com/startup-claims-to-have-replaced-90-percent-of-its-support-staff-with-a-chatbot/ | The Decoder (Matthias Bastian) | 2023-07-15 | Yes, 2026-10-28, raw HTML read as text |
| https://www.hcamag.com/us/specialization/recruitment/absolutely-necessary-firm-replaces-support-staff-with-ai-chatbot/461986 | HRD / HCA Magazine (Dexter Tilo) | 2023-10-04 | Yes, 2026-10-28, raw HTML read as text |
| https://oecd.ai/en/incidents/2023-07-11-a665 | OECD.AI incidents monitor | 2023-07-11 (entry) | Yes, 2026-10-28, raw HTML read as text; not relied on for any fact |

## Corrections

If you have Dukaan's own definition of "resolved," the date and size of the layoffs from a primary source, or a later report on how the bot performed, tell us and we will fix this page.
