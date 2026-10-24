---
title: "Canada Revenue Agency: the Charlie tax chatbot answered 2 of 6 audit questions correctly, October 2025"
date: 2025-10-21
source: "https://www.canada.ca/content/dam/oag-bvg/audit-reports/documents/parl_oag_202510_01_e.pdf"
description: "Canada's Auditor General tested the CRA's Charlie chatbot with six tax questions. It got two right, while public AI tools got five right."
summary: "In its October 2025 audit of Canada Revenue Agency (CRA) contact centres, the Office of the Auditor General of Canada tested the CRA's website chatbot, Charlie, with 6 tax questions. Charlie answered 2 accurately; other public AI tools answered 5. The auditors said Charlie's answers were brief, with limited context. The audit made no recommendation about Charlie itself. Later reporting, not the audit, says the CRA moved Charlie to a generative AI version."
categories:
  - Government
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - reviewing-only-failures
  - doesn-t-say-what-it-can-do
---

**This page is a dated teardown of one public audit finding about Charlie, the Canada Revenue Agency's tax chatbot, for teams that run a government or service chatbot that answers rules questions for the public.** Every fact below comes from a source we opened (listed at the end). The audit tested Charlie with only 6 questions, and it did not publish the questions or Charlie's answers.

**Status: Needs review.** The Auditor General's report (PDF, through an Internet Archive copy of the canada.ca file), the OAG's committee statement page and the CRA's response statement (both through Internet Archive copies), The Canadian Press via BNN Bloomberg, iPhone in Canada, the Western Standard and the AI Incident Database were downloaded as raw files and read as text on 2026-10-24. Each quote below was checked word for word against that text (line breaks in the PDF ignored). The live canada.ca pages timed out, and the oag-bvg.gc.ca report page now returns a 404 (see "What we could not verify").

> **Read this first.** This is a summary of public reporting, not a finding of fact and not legal or tax advice. We did not use Charlie, and we did not see the six test questions or Charlie's answers. The audit's main subject was the CRA's call centers; Charlie takes up two paragraphs of it.

## What happened (as reported)

- **The audit.** The Auditor General's 2025 report "Canada Revenue Agency Contact Centres" covered April 1, 2019, to June 30, 2025. The CRA's response statement is dated October 21, 2025.
- **What Charlie is.** Per the report, "Charlie is the Canada Revenue Agency's virtual chatbot, available on its website to provide automated assistance with frequently asked questions about taxes and benefits." It "is limited to general information and cannot address account-specific enquiries."
- **The test.** Auditors asked Charlie and "other publicly available artificial intelligence tools" 6 tax-related questions, 2 from each area of enquiry (individual taxes, benefits, business taxes).
- **The result.** "We found that Charlie provided accurate answers in only 2 out of the 6 questions we asked it, while the other public web-based conversational artificial intelligence tools answered 5 out of 6 questions accurately."
- **The style of the answers.** "Charlie's responses tended to be brief, offering limited context and minimal additional information."
- **The human baseline.** In the same audit, auditors placed 167 calls to agents between February and May 2025. Agent "responses to general individual-tax questions were accurate only 17% of the time."
- **In committee.** On October 28, 2025, The Canadian Press quoted Auditor General Karen Hogan: "Charlie got it right 33 per cent of the time, so that’s a little more accurate than reaching an agent and asking them a question about your personal taxes." She added: "I think it just highlights that there’s a lot of room for improvement."
- **The question from Parliament.** iPhone in Canada, citing the National Post, reports Liberal MP Anthony Housefather asked: "how is it that the government’s tool specialized for the CRA is worse than the average tool that anyone else can access anywhere?"
- **Cost and use, per later reports.** iPhone in Canada says parliamentary documents show "more than $18 million" spent on Charlie since 2018–2019. The Western Standard gives $18.06 million. iPhone in Canada says the CRA counts "more than 7 million conversations and over 18 million questions" since launch.
- **User feedback, per later reports.** The Western Standard, citing Blacklock's Reporter and Access to Information records, says an "Oct. 29 report" (year not given) found 36.4% of users who gave feedback were satisfied, and that users often asked to speak with a live agent. It quotes a CRA memo: "It falls short of meeting users’ expectations."

## What the agency did

- **No Charlie recommendation.** The report names Charlie only in paragraphs 35 and 36. Its recommendation for that section (paragraph 43) is about agents' evaluations and quality reviews, not the chatbot.
- **Promised more topics.** In its response in the report, the CRA said "as of November 2025 the GenAI chatbot beta on Canada.ca will be able to answer more questions, as the number of topics is increased."
- **Moved to generative AI, per later reports.** iPhone in Canada says that in November the CRA upgraded Charlie to a generative AI version. It says the CRA claims pre-release testing showed accuracy of "approximately 90%," but "acknowledged it cannot confirm real-world accuracy without reviewing every interaction."
- **An earlier bar.** The same story says internal testing once showed Charlie met "a 70 per cent accuracy threshold." The Western Standard says the newer benchmark was 90%, and quotes a memo: "No generative artificial intelligence system can achieve 100% accuracy."
- **The CRA's public statement.** The CRA's October 21, 2025, statement on the audit does not mention Charlie. It talks about call capacity and a 100-day service plan.

## Where in the conversation flow it broke

Based on the reports, and only as far as they go:

1. **The user.** A taxpayer opens a CRA web page and types a general tax or benefits question to Charlie.
2. **The scope.** Charlie can only give general information. Account questions are out of scope, per the audit.
3. **The answer.** In 4 of the auditors' 6 tries, the answer was not accurate. Answers were short, with "limited context."
4. **What the user can check.** No opened source says whether Charlie showed a source link, a date, or a warning with its answers.
5. **The next step.** Per the Western Standard, users often asked for a live agent after chatting. The same audit found agents accurate 17% of the time on general individual-tax questions.
6. **The team's view.** Per iPhone in Canada, the CRA said it cannot confirm real-world accuracy without reviewing every interaction. No opened source describes any sampled accuracy check on live chats.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Confident wrong answer with no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). Partial fit. The core is there: a public tax bot gave inaccurate answers on most test questions, and the answers were brief, with little context. But no opened source shows Charlie's tone or whether it cited sources.
- [Reviewing only failures](../goals/measurement-and-feedback/failures/reviewing-only-failures.md) (`reviewing-only-failures`). Weak fit. That page's fix is to read "a random sample of all conversations." The CRA reportedly said it could not confirm live accuracy without reading every chat. A sample would answer that. We do not know what the CRA reviews today.
- [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`). Weak fit. Charlie cannot handle account questions, and per the Western Standard, many users expected it to resolve problems, not point to information. We did not see what Charlie tells users about its limits.
- **Considered, not a fit.** [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`): users asked for agents, but no source says the bot blocked them. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`): it is about tidy test input; no source says how the CRA's tests were built. [Survey bias](../goals/measurement-and-feedback/failures/survey-bias.md) (`survey-bias`): the 36.4% figure is secondhand, and no source says how feedback was collected. [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) (`eligibility-answers-sound-like-decisions`): no opened source shows an eligibility answer.
- **Possible gaps for a person to judge.** The taxonomy has no pattern for a specialist bot that is less accurate than general-purpose tools on its own subject, or for a bot that ships with no ongoing accuracy measure on live questions. These are proposals, not decisions.

## Related incidents

- [NYC MyCity business chatbot (2024)](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): another government bot gave wrong answers about the rules it was built to explain.
- [TurboTax and H&R Block AI tax assistants (2024)](turbotax-and-hr-block-ai-tax-assistants-wrong-or-irrelevant-answers-march-2024.md): a test of tax chatbots by a newspaper, not an auditor.
- [WHO S.A.R.A.H. health chatbot (2024)](who-sarah-health-chatbot-wrong-and-outdated-answers-april-2024.md): a public-agency bot with outdated and uneven answers.

## What to measure

Proposed signals, not results. Status: Not yet run.

- Share of a fixed set of real taxpayer questions the bot answers accurately, scored each month by a reviewer.
- The same set run through one general-purpose AI tool, so the gap can be tracked.
- Share of answers that include a link to the official page they rest on.
- Share of chats where the user asks for a person, and share where the user returns with the same question within 7 days.
- Share of out-of-scope (account) questions where the bot says plainly it cannot help and names the right channel.

## What a team can change

Our proposals, not the CRA's. Each is a pass/fail check on a transcript or a review log. Status: Not yet run.

1. **Measure live accuracy by sample.** Pass: each month, a random sample of real chats is scored for accuracy, and the result is written down.
2. **Publish the bar.** Pass: the accuracy target and the test method are written down before launch and checked after it.
3. **Show the source.** Pass: every rules answer links to the official page it is based on.
4. **Say the limits.** Pass: when asked an account question, the bot says it cannot see accounts and names the right channel.
5. **Give enough context.** Pass: an answer to a rules question names the condition or exception that changes the answer, or says there is none.
6. **Don't over-correct.** Pass: a simple, well-covered question (for example a filing deadline) still gets a direct answer, not only a link or "contact us."

## What we could not verify

- The six questions and Charlie's six answers. The audit did not publish them.
- When the six questions were asked. The report gives the 167 agent calls as February to May 2025, but no date for the Charlie test.
- When Charlie launched. iPhone in Canada says February 2020; the AI Incident Database says March 2020; the Western Standard says "launched in 2025," which may mean the generative AI version.
- The cost figures, the 7 million conversations, the 70% and 90% figures, and the 36.4% satisfaction figure. These come from news reports of parliamentary and internal records; we did not open those records.
- The National Post story and Blacklock's Reporter story, cited by our sources. Not opened.
- A 44 per cent accuracy figure (attributed to Juno News) and a "66%" wrong-answer figure, seen only in search summaries. Not used.
- The OAG media release on canada.ca and the live report pages (timed out or 404). The archived PDF was used instead.
- The OpenParliament transcript of the committee meeting (blocked, 403). The Housefather question is taken from iPhone in Canada only.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.canada.ca/content/dam/oag-bvg/audit-reports/documents/parl_oag_202510_01_e.pdf | Office of the Auditor General of Canada | 2025-10 (CRA response dated 2025-10-21) | Yes, 2026-10-24, Internet Archive copy (2026-04-20) of the PDF, converted to text; quotes checked word for word |
| https://www.oag-bvg.gc.ca/internet/English/osh_20251023_e_44763.html | Office of the Auditor General of Canada (Karen Hogan) | 2025-10-23 | Yes, 2026-10-24, Internet Archive copy, raw HTML read as text; context only |
| https://www.canada.ca/en/revenue-agency/news/2025/10/the-minister-of-finance-and-national-revenue-and-the-secretary-of-state-canada-revenue-agency-and-financial-institutions-respond-to-the-auditor-gen.html | Canada Revenue Agency | 2025-10-21 | Yes, 2026-10-24, Internet Archive copy, raw HTML read as text |
| https://www.bnnbloomberg.ca/business/company-news/2025/10/28/cra-looking-at-ai-training-to-help-call-centre-staff-provide-accurate-answers/ | The Canadian Press via BNN Bloomberg (Catherine Morrison) | 2025-10-28 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.iphoneincanada.ca/2025/12/12/auditor-general-slams-ottawas-18-million-cra-chatbot-charlie/ | iPhone in Canada (Austin Blake), citing the National Post | 2025-12-12 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.westernstandard.news/news/cra-chatbot-gave-wrong-answers-10-of-the-time-despite-18-million-price-tag/74419 | Western Standard News Services, citing Blacklock's Reporter | 2026-06-27 (page metadata) | Yes, 2026-10-24, live raw HTML (article text in page data) read as text; quotes checked word for word |
| https://incidentdatabase.ai/cite/1310 | AI Incident Database | not dated on page | Yes, 2026-10-24, live raw HTML read as text; used only for the launch-date conflict |

## Corrections

If you have the six audit questions, Charlie's answers, the CRA's own accuracy data, or the date Charlie launched, tell us and we will fix this page.
