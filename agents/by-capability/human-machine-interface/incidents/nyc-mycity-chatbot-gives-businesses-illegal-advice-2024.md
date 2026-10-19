---
title: "NYC's MyCity Business Chatbot Tells Owners Things the Reporting Says Break the Law"
date: 2024-03-29
source: "https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law"
summary: "In March 2024 The Markup, with Documented and THE CITY, reported that New York City's MyCity chatbot gave business owners answers on tips, cash, housing and more that the article says conflict with city or state rules. The city called it a pilot; a later administration took it down in early 2026."
categories:
  - Government
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - eligibility-answers-sound-like-decisions
---

**This page is a dated teardown of one public chatbot incident, for teams that put an AI assistant in front of people asking what rules apply to them.** Every fact below comes from a source we opened (listed at the end). Claims are marked as reported or unknown. Spot an error? See "Corrections" at the end.

> **Read this first.** This is design analysis, not legal advice. We do not say what any law requires. Where a rule is described below, it is what the cited article says the rule is, and we did not check it against the statutes. Have counsel review any bot that answers legal-obligation questions.

## What happened (as reported)

- **October 2023.** NYC announced the MyCity chatbot for business owners. The Markup says it runs on Microsoft Azure AI services (The Markup, March 29, 2024).
- **March 29, 2024.** The Markup (reporter Colin Lecher), copublished with Documented and THE CITY, reported the bot giving wrong or incomplete answers. As reported: it said buildings need not accept Section 8 or rental-assistance tenants; that a landlord could lock a tenant out; that there are no limits on residential rent; that a restaurant could refuse cash; that an employer could take a cut of workers' tips; that there are no rules on notifying staff of schedule changes; and it suggested hiding funeral prices. The article lists contrary rules for most of these, including a 2020 City Council cash law and a Federal Trade Commission funeral rule. We did not verify those rules ourselves.
- **Same question, different answers.** The article says one reporter was told landlords must accept vouchers, while ten staffers asking the same question were told no. A Legal Services NYC housing director, Rosalind Black, tested it and found more housing errors. Errors also showed up in other languages.
- **Around April 2, 2024.** A Tuesday response from Mayor Eric Adams, per an April 5 Yahoo-syndicated article, said the bot is wrong in some areas and has to be fixed. He also said new technology must go into the real environment to iron out kinks. That article says the site then called it a beta product whose answers may be inaccurate or incomplete.
- **January 30, 2026.** The Markup reported that Mayor Zohran Mamdani's administration plans to take the bot down, citing budget savings. The Markup's later update, dated February 4, 2026, says the city took the bot down and stated the beta test had ended.

## What the city and others said

- **City Office of Technology and Innovation (March 2024).** Per The Markup, a spokesperson said the bot is a pilot that will improve and has already given thousands of people timely, accurate answers. We have not seen that figure's basis.
- **Same office (April 2024).** Per the Yahoo article, it expected to "significantly mitigate inaccurate answers" within a week. Microsoft told Reuters it was fixing the bot; we did not read that report.
- **Andrew Rigie, NYC Hospitality Alliance.** Per The Markup, wrong legal information is a massive liability for small businesses.
- **Mamdani (January 2026).** Per The Markup and StateScoop, he called the bot functionally unusable and said it cost around half a million dollars.

## Where the sources disagree or are thin

- **Pilot or not.** The Markup quotes the city calling it a pilot. The Yahoo article says Adams's remarks imply real-world testing but does not use "pilot."
- **Cost.** Mamdani said about half a million dollars. The sources add that building it reportedly cost nearly $600,000 (attributed to ABC7 NY, which we did not open). Maintenance cost is unclear.
- **Takedown timing.** StateScoop (January 30) says no date was set. The Markup's February 4 update says it was already down. These are consistent over time, but we have no exact takedown date.
- **Whether it got better.** The Markup says the city improved some answers and seemed to limit what the bot would answer. We found no test data on how accurate it became.
- **Not found.** Any lawsuit, fine, or business that acted on a wrong answer. No opened source reports one.

## Pattern match

- [Chatbot is confidently wrong and you can't check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) is the core fit. The Markup says the bot often gave no links to verify, and that the same question got different answers. A disclaimer on the page sat beside answers stated as fact.
- [Government chatbot eligibility answers that sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md) is a partial fit only. This bot answered "what rules apply to my business," not "do I qualify for a benefit." What carries over is an official-looking voice with no line between general information and what the agency decides.

## Where in the flow it broke

The break was at the answer step of an open-ended chat on a city site. A business owner asked a rules question, and the bot answered in the city's voice.

1. **No grounding the user could check.** The Markup says verification links were often missing. Without a source, the reader cannot tell a right answer from a wrong one.
2. **Unstable answers.** The same question gave opposite answers across staffers. A reader who asks once cannot know which one they got.
3. **Warnings did not match the voice.** The page said answers may be wrong, yet the answers were stated plainly. We have no data on whether anyone read the warning.

## What to measure

Proposed metrics; none come from NYC. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Rule claims with no cited official page | Replies that state an obligation or permission, divided by those that link a current source |
| Answer consistency | Same legal question asked 10 times, share of runs that agree |
| High-stakes topics answered without a person path | Replies on pay, housing, safety, or fees that offer no contact or official page |
| Expert-spotted errors | Wrong answers found in sampled review by staff who know the rules |
| Feedback-form reports | Inaccuracy reports per 1,000 conversations |

## What a team can change

Proposed rules, each a pass/fail check on a transcript. Status: Not yet run.

1. **State a rule only with its source.** Any reply about what a business must or may do links the official page it relies on. Check: every such reply has a working link.
2. **Refuse to guess on topics you have not verified.** If no vetted text covers the question, say so and point to the official office. Check: scripted out-of-scope questions get a refusal.
3. **Test for consistency.** Run each high-stakes question many times and fail the release if answers conflict. Check: agreement rate meets a bar you set.
4. **Put the limit in the answer, not only on the page.** For legal topics, add a line in the reply saying it is general information and to confirm with the agency or a lawyer. Check: string match in the reply.
5. **Don't over-correct.** Refusing everything makes the bot useless. Limit hard blocks to legal-obligation topics, and keep answering plain how-to and where-to questions from vetted pages.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://themarkup.org/news/2024/03/29/nycs-ai-chatbot-tells-businesses-to-break-the-law | The Markup | 2024-03-29 | Yes, 2026-10-20 |
| https://sg.news.yahoo.com/nyc-mayor-defends-ai-system-183527596.html | Yahoo (syndicated) | 2024-04-05 | Yes, 2026-10-20 |
| https://themarkup.org/artificial-intelligence/2026/01/30/mamdani-to-kill-the-nyc-ai-chatbot-we-caught-telling-businesses-to-break-the-law | The Markup | 2026-01-30 (update 2026-02-04) | Yes, 2026-10-20 |
| https://statescoop.com/mamdani-kill-nyc-ai-chatbot/ | StateScoop | 2026-01-30 | Yes, 2026-10-20 |

Not opened: Daily Maverick's April 2024 article (blocked, 403), THE CITY's own coverage, any NYC.gov statement or the live MyCity page, the Reuters report, ABC7 NY, and the statutes the article cites. Anything from those is not stated above except where marked as attributed.

## Corrections

If you have the original city statement, a better takedown date, or the chatbot's own text, tell us and we will fix this page.
