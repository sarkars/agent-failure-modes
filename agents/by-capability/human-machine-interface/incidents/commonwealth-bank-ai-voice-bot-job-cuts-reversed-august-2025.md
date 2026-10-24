---
title: "Commonwealth Bank: 45 call center jobs cut for an AI voice bot, then reinstated as an 'error' after a union dispute, August 2025"
date: 2025-08-21
source: "https://www.fsunion.org.au/cba-backflips-on-ai-cuts-but-the-threat-remains/"
description: "How Commonwealth Bank cut 45 call center jobs for an AI voice bot, then called it an error and reversed the cuts after a union dispute in August 2025."
summary: "In July 2025, Commonwealth Bank of Australia (CBA) said 45 roles in its Customer Service Direct business were no longer needed after it added a voice bot to its inbound customer enquiries line. The Finance Sector Union said call volumes were rising, not falling, and took a dispute to the Fair Work Commission. On August 21, 2025, CBA said its assessment was an error, that the roles were not redundant, and that it had apologized to the staff. The bank's own call data was not published in any source we opened."
categories:
  - Customer Service
patterns:
  - survey-bias
  - channel-chosen-for-organisational-convenience
  - escalates-too-early-or-too-late
---

**This page is a dated teardown of one public incident at Commonwealth Bank of Australia, for teams that plan to cut or move support staff because a voice bot or chatbot is said to be taking calls off their queue.** Every fact below comes from a source we opened (listed at the end). The bank's own call figures were not in any source we opened; the claims about them come from the union and news reports.

**Status: Needs review.** The Finance Sector Union media release, two Canberra Times (ACM) stories, Information Age (ACS), HCA Magazine, Cyber Daily and a Staffing Industry Analysts republication of a Bloomberg News story were downloaded as raw HTML and read as text on 2026-10-24. Each quote below was checked word for word against that text. Bloomberg's own page and the union's earlier dispute page blocked our download (see "What we could not verify").

> **Read this first.** This is a summary of public reporting, not a finding of fact and not legal or employment advice. We did not see or call the voice bot, and we did not see CBA's call data. We take no side in the labor dispute; we describe what the bank and the union each said.

## What happened (as reported)

- **The cut.** On August 1, 2025, The Canberra Times reported "A total of 90 jobs were axed at the Commonwealth Bank, including 45 roles in direct banking," linked to "a new voice bot system on the bank's inbound customer enquiries line." The 90 figure appears only in that story; every other source uses 45.
- **The bank's reason.** A CBA spokesperson told ACM: "By automating simple queries, our teams can focus on more complex customer queries that need empathy and experience." The spokesperson said the priority was to "explore opportunities for redeployment" for affected staff.
- **The claim at issue.** The union says CBA announced the cut in July and that the bot was one "which it claimed was reducing call volumes." Bloomberg News, as republished by Staffing Industry Analysts, says the bank had said the bot "reduced call volumes by 2,000 a week." We saw no CBA document with that number.
- **The union's account.** The FSU says "call volumes were rising, with management scrambling to offer overtime and even pulling team leaders onto the phones." Information Age and HCA Magazine report the same, attributed to the union.
- **The early reaction.** In July, FSU national secretary Julia Angrisano said workers "expect to be part of the change, not replaced by it" (per The Canberra Times).
- **The tribunal.** Per the Bloomberg story, the union took CBA to the workplace tribunal "earlier this month" (August), saying the bank was not open about call volumes. It also said CBA did not explain how roles were picked and was hiring similar roles with messaging duties in India. The FSU release refers to "a dispute before the Fair Work Commission."
- **Earlier context.** Information Age says CBA began testing a generative AI chatbot named Hey CommBank in late 2024, "leading to fears it would replace many of its 2,400 contact centre staff."

## What the company did

- **Called it an error.** On August 21, 2025, a CBA spokesperson said: "CBA’s initial assessment that the 45 roles in our Customer Service Direct business were not required did not adequately consider all relevant business considerations and this error meant the roles were not redundant" (Information Age; also HCA Magazine and Bloomberg).
- **Apologized.** "We have apologised to the employees concerned and acknowledge we should have been more thorough in our assessment of the roles required" (The Canberra Times, Information Age, HCA Magazine).
- **Gave staff a choice.** Per CBA, via The Canberra Times: stay in their current roles, seek redeployment within CBA, or leave. The FSU describes the choice as staying or "taking a voluntary exit payment."
- **Said it would review its process.** "We are also reviewing our internal processes to improve our approach going forward" (HCA Magazine).
- **The union's response.** Angrisano called it "a massive win for workers" and said "CBA has been caught out trying to dress up job cuts as innovation." The FSU said "Another hearing before the Fair Work Commission is scheduled for 25 August."
- **No published numbers.** No opened source gives CBA's own count of calls before or after the bot, or how the bot's effect was measured.

## Where in the conversation flow it broke

The reports describe a staffing decision, not a single call. Based on the reports, and only as far as they go:

1. **The caller.** A customer phones CBA's inbound customer enquiries line and reaches the new voice bot first.
2. **The bot's job.** Per CBA, it was meant to handle "simple queries" so staff could take complex ones.
3. **The count.** The bank reportedly counted the bot as taking about 2,000 calls a week off staff. No opened source says how a call was counted as handled.
4. **The decision.** That count was used to declare 45 roles not needed. CBA later said the assessment did not consider "all relevant business considerations."
5. **The front line.** Staff, per the union, saw more calls, not fewer: overtime offers and team leaders on the phones.
6. **What we cannot say.** No opened source says whether callers left the bot unresolved and called back, asked for a person, or simply called more for other reasons. The gap between the bank's number and the floor is reported; its cause is not.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Survey bias](../goals/measurement-and-feedback/failures/survey-bias.md) (`survey-bias`). Partial fit. That page's stakes line says "Teams ship, cut staff, or stop fixing things based on the score," and it warns that a loose containment count can include "frustrated abandonments." Here a bot metric was reportedly used to cut staff. But no survey was involved, and no source says how the number was built.
- [Channel chosen for organizational convenience](../goals/channel-selection/failures/channel-chosen-for-organisational-convenience.md) (`channel-chosen-for-organisational-convenience`). Partial fit. That page says "Cost targets drive the routing" and "Containment and cost per contact are on the dashboard." CBA framed the bot as easier for customers; the union framed it as cost-cutting. No opened source shows callers blocked from a person.
- [Escalates too early or too late](../goals/human-handoff/failures/escalates-too-early-or-too-late.md) (`escalates-too-early-or-too-late`). Weak fit. That page says a high containment rate is "Not by itself" good and should be paired with confirmed resolution. Staffing the humans behind a bot depends on how many calls still need them. No opened report describes when the bot handed off.
- **Considered, not a fit.** [Talk to a human ignored or looped](../goals/human-handoff/failures/talk-to-a-human-ignored-or-looped.md) (`talk-to-a-human-ignored-or-looped`): no opened report says callers could not reach a person. [IVR-style menu maze](../goals/voice/failures/ivr-style-menu-maze.md) (`ivr-style-menu-maze`): no source describes the bot's prompts or menus. [Clean-lab testing](../goals/measurement-and-feedback/failures/clean-lab-testing.md) (`clean-lab-testing`) and [Word-error-rate-only evaluation](../goals/voice/failures/word-error-rate-only-evaluation.md) (`word-error-rate-only-evaluation`): no opened source says how the bot was tested.
- **Possible gaps for a person to judge.** The taxonomy has no pattern for a staffing cut based on an unchecked deflection or containment claim. The survey-bias page itself notes no page named "containment counted as success" exists yet. A pattern such as "headcount cut on an unverified bot deflection number" could cover this case and [Klarna](klarna-ai-assistant-customer-service-reversal-2025.md). These are proposals, not decisions.

## Related incidents

- [Klarna AI assistant customer-service reversal (2025)](klarna-ai-assistant-customer-service-reversal-2025.md): a company said its AI did the work of many agents, then hired people again.
- [CFPB bank chatbot doom loops (2023)](cfpb-bank-chatbot-doom-loops.md): a US regulator documented bank customers stuck with bots and no route to a person.
- [Taco Bell drive-thru AI order failures (2025)](taco-bell-drive-thru-ai-order-failures-2025.md): a voice AI on a live customer line was rethought after public problems.

## What to measure

Proposed signals, not results. Status: Not yet run.

- Total inbound calls per week to the line, before and after the bot, including calls the bot took.
- Share of bot-handled calls where the same caller calls again on the same issue within 7 days.
- Share of bot calls where the caller asks for a person, and share that then reach one.
- Weekly overtime hours and team-leader time on the phones, next to the bot's handled-call count.
- Wait time to reach a person, before and after the bot.

## What a team can change

Our proposals, not CBA's. Each is a pass/fail check on call logs or a staffing review. Status: Not yet run.

1. **Define "handled."** Pass: a call counts as handled by the bot only if the caller does not call back on the same issue within a set window.
2. **Count total demand.** Pass: the staffing case shows total calls to the line, not only calls the bot took.
3. **Check the floor before the cut.** Pass: overtime, wait time and team-leader phone time are flat or down for a set period before any role is cut.
4. **Show the work.** Pass: the claimed weekly reduction, its method and its date range are written down and shared with the people reviewing the decision.
5. **Keep the route to a person.** Pass: on a sample of bot calls, every caller who asks for a person reaches one or gets a callback time.
6. **Don't over-correct.** Pass: a simple query the bot fully resolves (no callback, no handoff) still stays with the bot; the fix is the measure, not removing the bot.

## What we could not verify

- CBA's call figures. The 2,000-a-week number is the union's account of the bank's claim, via Bloomberg; no opened source shows CBA's data.
- When the bot went live. Search snippets (Kalkine, HackerNoon) say June 2025; no opened source gives a date.
- The 90 total. Only the August 1 Canberra Times story uses it; the FSU and others use 45.
- The outcome of the Fair Work Commission dispute, and of the hearing set for August 25, 2025.
- Bloomberg's own page (blocked as a robot check) and the FSU dispute page at fsunion.org.au/were-disputing-cbas-anti-jobs-agenda-in-fair-work/ (403). Seen only in search results; its claims are not used.
- A CBA newsroom statement. We found none; CBA's words here come from news reports.
- Coverage by Kalkine, getcoai, babl.ai, heise, HackerNoon and switzer.com.au. Seen only in search results; not used.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.fsunion.org.au/cba-backflips-on-ai-cuts-but-the-threat-remains/ | Finance Sector Union | 2025-08-21 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.canberratimes.com.au/story/9029592/ | The Canberra Times / ACM (Carla Mascarenhas) | 2025-08-01 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.canberratimes.com.au/story/9046323/commonwealth-bank-reverses-ai-chatbot-job-cuts-admits-error/ | The Canberra Times / ACM (Carla Mascarenhas) | 2025-08-21 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://ia.acs.org.au/article/2025/cba-reverses-ai-driven-job-cuts--admits--error-.html | Information Age, ACS (Denham Sadler) | 2025-08-21 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.hcamag.com/au/specialisation/hr-technology/cba-reverses-ai-triggered-employee-layoffs/546887 | HCA Magazine (Dexter Tilo) | 2025-08-21 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.cyberdaily.au/digital-transformation/12531-cba-rolls-back-ai-related-job-cuts-following-union-and-worker-backlash | Cyber Daily (Daniel Croft) | 2025-08-21 | Yes, 2026-10-24, live raw HTML read as text (partly behind a login wall); used for context only |
| https://www.staffingindustry.com/news/global-daily-news/australias-biggest-bank-reverses-plan-to-replace-jobs-with-ai | Staffing Industry Analysts, republishing Bloomberg News | 2025-08-26 (page metadata; Bloomberg URL dated 2025-08-21) | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |

## Corrections

If you have CBA's call data for the line, the date the voice bot went live, or the outcome of the Fair Work Commission dispute, tell us and we will fix this page.
