---
title: "Los Angeles Unified: 'Ed' student chatbot switched off after its builder AllHere collapsed, amid student-data claims, March-June 2024"
date: 2024-03-20
source: "https://www.the74million.org/article/whistleblower-l-a-schools-chatbot-misused-student-data-as-tech-co-crumbled/"
description: "How LAUSD launched a sun-shaped AI helper for students and parents, then shut it off within three months when its vendor collapsed amid privacy claims."
summary: "Los Angeles Unified School District launched 'Ed,' an AI chatbot and portal for students and parents built by the startup AllHere, on March 20, 2024. On June 14, 2024, AllHere furloughed most of its staff and the district says it turned the chatbot off. A former AllHere engineer told The 74 the bot put student records into every prompt and sent most requests to servers abroad; the district said it reviewed the platform for privacy compliance. AllHere's founder was later indicted on investor-fraud charges, and the chatbot has not been reported as restored in any source we opened."
categories:
  - Governance
  - Security
patterns:
  - avatar-overpromising
  - doesn-t-say-what-it-can-do
  - child-user-treated-as-adult
---

**This page is a dated teardown of one public incident at Los Angeles Unified School District (LAUSD), for teams that put an AI chatbot in front of students and parents and rely on an outside vendor to run it.** Every fact below comes from a source we opened (listed at the end). The privacy claims come from one former AllHere employee; the district disputes them, and no audit result was in any source we opened.

**Status: Needs review.** Six sources were downloaded as raw HTML and read as text on 2026-10-24: two stories from The 74, an LA School Report republication of a third 74 story, a Los Angeles Times story republished by GovTech, an EdSurge story and a TNND story on WJLA. Each quote below was checked word for word against that text. The Justice Department press release blocked our download (see "What we could not verify").

> **Read this first.** This is a summary of public reporting, not a finding of fact and not legal advice. We did not use Ed, see its code or read the contract ourselves. The whistleblower's claims are allegations. The founder's charges are allegations, not a conviction. No source we opened says the superintendent was charged with anything.

## What happened (as reported)

- **The launch.** LAUSD unveiled Ed on March 20, 2024, at Roybal Learning Center (Los Angeles Times via GovTech). It was a chatbot shaped like a sun, plus a portal meant to pull together "student records, assignments, grades, academic recommendations and mental health referrals."
- **The promise.** Superintendent Alberto Carvalho said at the ASU+GSV conference in April: "He’s going to talk to you in 100 different languages, he’s going to connect with you, he’s going to fall in love with you" (The 74). He called it the nation’s first "personal assistant" for students.
- **What it could actually do.** A district official, Tony Aguilar, said "The chatbot only answered questions it recognized." Other questions might get a reply such as "Ask your teacher" (LA Times via GovTech). AllHere also "had provided human moderators to oversee the system."
- **The collapse.** On June 14, 2024, AllHere furloughed most of its staff. The district said it dropped AllHere after "we were notified of their financial collapse", and that the chatbot was unplugged that day (LA Times via GovTech, July 3, 2024).
- **The money.** The contract was for up to $6 million over five years, and AllHere had been paid about half, per a district statement (LA Times via GovTech; EdSurge).
- **The whistleblower.** Chris Whiteley, a former AllHere senior director of software engineering laid off in April, told The 74 he warned the district, its inspector general and state officials, and that none responded. He said the bot put student personal data in all prompts, even when not needed, shared prompts with other third parties, and sent seven out of eight requests to servers abroad.
- **One reported reply.** Per The 74, which saw source code Whiteley shared: "When querying the simple prompt “Hello,” the chatbot provided the student’s grades, progress toward graduation and other personal information."
- **Household data.** Whiteley said the bot "processed the personal information for all students in a household" to answer even a question about one child (LA School Report, republishing The 74).
- **The design brief.** The bot was told to act as a "friendly, concise customer support agent" and reply "using simple language a third grader could understand" (The 74).
- **Later.** The 74 reports AllHere filed for Chapter 7 bankruptcy in August 2024, and its founder was indicted in November 2024 on charges of defrauding investors of "nearly $10 million". TNND reports the FBI searched Carvalho’s home and district headquarters on February 25, 2026, and that he resigned effective June 21, 2026. It says the investigation is partly about his dealings with AllHere, and that neither he nor a consultant whose home was also searched has been charged.

## What the district did

- **Defended its review.** "Throughout the development of the Ed platform, Los Angeles Unified has closely reviewed the platform to ensure compliance with applicable privacy laws and regulations" (district statement, via EdSurge).
- **Stated the rules.** "Pursuant to contract and applicable law, AllHere is not authorized to store student data outside the United States without prior written consent from the District" (The 74).
- **Promised follow-up.** The district "takes these concerns seriously and will continue to take any steps necessary to ensure that appropriate privacy and security protections are in place in the Ed platform" (The 74).
- **Kept the portal, paused the bot.** Officials said the information stayed on the Ed platform, reached by "drop boxes and clicking links" (LA Times via GovTech). The district said it would "temporarily disable the chatbot" and it would "only be restored when the human-in-the-loop aspect is re-established" (LA School Report).
- **Opened an inquiry.** The inspector general’s office interviewed Whiteley by video on July 2, 2024 (LA School Report). The 74 later said the district and the inspector general opened separate inquiries. No opened source gives a finding.
- **After the indictment.** A spokesperson called it, "if true, a disturbing and disappointing house of cards that deceived and victimized many across the country" (The 74, November 20, 2024).

## Where in the conversation flow it broke

The reports describe a product and a vendor, not one logged chat. Based on the reports, and only as far as they go:

1. **The front door.** A student or parent opens Ed, a smiling sun the superintendent said would "fall in love with you".
2. **The first message.** Per the code The 74 saw, a plain "Hello" got back the student’s grades and graduation progress. No source says the user asked for them or was asked to confirm who they were.
3. **The data behind each turn.** Per Whiteley, every prompt carried student records, including other children in the same household, and most went to servers abroad. The district says the contract barred storage abroad without consent. Storage and processing may differ; no opened source settles it.
4. **The edge of what it knew.** Questions it did not recognize could get "Ask your teacher". No source says whether users were told up front what Ed could answer.
5. **The people behind it.** Human moderators came from AllHere. When AllHere furloughed staff on June 14, the district turned the chatbot off and said it would stay off until that human-in-the-loop role was back.
6. **What we cannot say.** No opened source has a real user transcript, a count of users, or any audit of where data went.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Avatar overpromising](../goals/visual/failures/avatar-overpromising.md) (`avatar-overpromising`). Partial fit. That page covers an "emotive persona" that makes users "trust or tell it too much". Ed was a mascot sun pitched as a friend that would "fall in love with you," while staff said it only answered questions it recognized. No source measured what users expected.
- [Doesn't say what it can do](../goals/embedded-copilots/failures/doesn-t-say-what-it-can-do.md) (`doesn-t-say-what-it-can-do`). Partial fit. The gap between "personal assistant" and "Ask your teacher" is the gap that page describes. But no source shows Ed's welcome screen, so we cannot say whether it listed its limits.
- [Child user treated as adult](../goals/age-adaptation/failures/child-user-treated-as-adult.md) (`child-user-treated-as-adult`). Weak fit. That page says to "Collect no personal data beyond what's essential" for minors. Ed's users were known to be students, so the issue is not missed age signals. The claimed problem is the bot sending more student data than each answer needed.
- **Considered, not a fit.** [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`): here the system, not the user, supplied the data. [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`): no source says Ed asked users to type sensitive data. [Dead-end "I don't understand" replies](../goals/conversation-leadership/failures/dead-end-i-don-t-understand-replies.md) (`dead-end-i-don-t-understand-replies`): "Ask your teacher" names a next step, and no transcript shows a loop. [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`): no opened source reports a wrong answer.
- **Possible gaps for a person to judge.** (1) No pattern covers a bot that puts more personal records into each model call than the question needs, or volunteers them on a greeting. (2) No pattern covers a live bot whose human reviewers or vendor disappear, leaving no owner. These are proposals, not decisions.

## Related incidents

- [NYC MyCity chatbot gave businesses illegal advice (2024)](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): another public-sector chatbot launched with high claims.
- [WHO S.A.R.A.H. health chatbot (April 2024)](who-sarah-health-chatbot-wrong-and-outdated-answers-april-2024.md): a public body's persona bot with limits users could not see.
- [DeepSeek exposed database (January 2025)](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md): chat data exposed by the vendor's own systems.

## What to measure

Proposed signals, not results. Status: Not yet run.

- Personal fields sent to the model per request, compared with the fields the answer used.
- Share of greetings or off-topic turns whose reply contains a grade, attendance record or other student record.
- Share of requests processed outside the country the contract names, from the vendor's own logs.
- Share of turns ending in a deflection such as "Ask your teacher," by topic.
- Hours per week a named human reviewer is actually on duty, next to the chatbot's live hours.

## What a team can change

Our proposals, not LAUSD's. Each is a pass/fail check on a transcript, a request log or a contract review. Status: Not yet run.

1. **Send only what the question needs.** Pass: on a sample of logged requests, no student record goes to the model unless the question asks about that record.
2. **No records on a greeting.** Pass: a "Hello" turn returns no grade, attendance or other student record.
3. **One child at a time.** Pass: a question about one child sends no data about siblings.
4. **Say the limits first.** Pass: the first screen lists what Ed can answer, and an out-of-scope reply names a person or page to try.
5. **Match the mascot to the job.** Pass: launch copy and the welcome message claim no feeling or ability the bot lacks.
6. **Plan for the vendor leaving.** Pass: a written runbook names who turns the bot off, who keeps the portal up, and how data is returned or deleted, and it has been rehearsed once.
7. **Don't over-correct.** Pass: a parent asking "what grade does my child have in math?" after sign-in still gets the grade; the fix is scoping the data, not hiding it.

## What we could not verify

- Whiteley's technical claims. They come from him and from code The 74 says it saw; no audit or inspector general finding was in any opened source.
- Whether data was stored, not just processed, abroad. The district says storage abroad needed consent; no source settles it.
- Whether Ed was disabled on June 14. The 74 says it asked for proof and got no response.
- Whether the chatbot ever came back. No opened source says so.
- The Justice Department release at justice.gov (our download returned no article). Its content is used only as quoted in The 74.
- Search-result snippets saying the district spent about $300,000, and Fox News and other reports on the 2026 FBI probe. Not opened; not used.
- Wikipedia's "Ed (chatbot)" page. Downloaded but not used as a source of facts.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.the74million.org/article/whistleblower-l-a-schools-chatbot-misused-student-data-as-tech-co-crumbled/ | The 74 (Mark Keierleber) | 2024-07-01 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.govtech.com/education/k-12/lausd-shutters-new-ai-chatbot-when-developer-goes-out-of-business | GovTech, republishing the Los Angeles Times (TNS) | 2024-07-03 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.laschoolreport.com/l-a-schools-probe-charges-its-hyped-now-defunct-ai-chatbot-misused-student-data/ | LA School Report, republishing The 74 | 2024-07-15 (page date) | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.edsurge.com/news/2024-07-15-an-education-chatbot-company-collapsed-where-did-the-student-data-go | EdSurge (Jeffrey R. Young) | 2024-07-15 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://www.the74million.org/article/feds-charge-once-lauded-allhere-ai-founder-in-10m-scheme-to-defraud-investors/ | The 74 | 2024-11-20 | Yes, 2026-10-24, live raw HTML read as text; quotes checked word for word |
| https://wjla.com/news/nation-world/los-angeles-school-district-superintendent-resigns-amid-fbi-investigation-board-of-education-lausd-alberto-carvalho-raid-doj | WJLA, TNND (The National News Desk) | 2026-06-22 | Yes, 2026-10-24, live raw HTML read as text; used for the 2026 events only |

## Corrections

If you have the inspector general's findings, an audit of where Ed's data went, or a record of the chatbot being restored, tell us and we will fix this page.
