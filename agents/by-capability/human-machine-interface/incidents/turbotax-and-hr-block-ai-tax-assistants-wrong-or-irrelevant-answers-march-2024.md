---
title: "TurboTax and H&R Block AI tax assistants: a Washington Post test found wrong or irrelevant answers to tax questions"
date: 2024-03-04
source: "https://nysscpa.org/news/1046937-tech-columnist-turbotax-and-hr-block-chatbots-are-unhelpful-or-wrong-much-of-the-time-2024-03-07"
summary: "In March 2024 a Washington Post test found the TurboTax and H&R Block AI tax chatbots gave wrong or irrelevant answers up to half the time. Both firms called the tools works in progress and pointed to their guarantees. No opened source reports a filed return that went wrong because of the bots."
categories:
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - link-and-resource-dumps
  - guessing-instead-of-asking
---

**This page is a dated teardown of one public test of two AI tax assistants built into tax-filing software, for teams that ship an assistant answering questions where a wrong answer has legal or money consequences.** Every fact below comes from a source we opened (listed at the end). We could not open the Washington Post column itself, so its findings are told here through the outlets and the government office that reported on it.

**Status: Needs review.** Every source was read through a fetch-tool summary, not as a full page. Each quote below was checked in a second fetch of the same page, except the Taxpayer Advocate quotes, which were checked against the raw page text. Details we saw only in search summaries are listed under "What we could not verify" and kept out of the claims.

**Read this first.** This is design analysis, not tax or legal advice. The tax answers quoted below are what the sources report the reviewers judged correct; check any tax question of your own with a qualified tax professional or the IRS.

## What happened (as reported)

- **The products.** TurboTax, from Intuit, offered an assistant called Intuit Assist. H&R Block offered one called AI Tax Assist. Both sat inside the companies' online filing software (NYSSCPA, March 7, 2024; iTechPost, March 5, 2024).
- **The test.** Geoffrey A. Fowler, a technology columnist at The Washington Post, tested both chatbots. The National Taxpayer Advocate's June 11, 2024 tax tip calls it "A recent informal review by the Washington Post." It says the chatbots "provided inaccurate or irrelevant responses up to 50 percent of the time when initially asked 16 complex tax questions." iTechPost (Kyle Marcelino, March 5, 2024) also reports 16 questions. Thomson Reuters Checkpoint (Tim Shaw, June 17, 2024) says human tax professionals reviewed the answers. NYSSCPA names Beverly Goodman, a tax manager at EP Wealth, as one who helped Fowler analyze the advice.
- **The college question.** Per Thomson Reuters, the test used a hypothetical California family whose daughter attends college in Arizona, and asked where she should file. H&R Block's bot said she had to file in both states. NYSSCPA reports that the correct answer is that she files in the other state only if she earned income there. TurboTax's bot, per Thomson Reuters, instead gave general resources on state renters credits, filing for an extension, and who counts as a full-time student.
- **The air conditioner question.** Kit Eaton's Inc. piece, syndicated by CPA Practice Advisor (March 12, 2024), says that for "a question about tax credits after installing a new air conditioner," TurboTax gave a long response that the Post and its tax experts judged irrelevant.
- **Other wrong answers.** iTechPost says the chatbots "reportedly offer incorrect filing status and information about the Internal Revenue System's guidelines on cryptocurrency." (The agency is the Internal Revenue Service; the error is iTechPost's.) It gives no example answers.
- **A second round for TurboTax.** NYSSCPA reports that after Intuit updated its system, Fowler's second round produced "many more correct, straightforward answers." Yet "the chatbot still responded with answers and links to irrelevant information a quarter of the time."
- **H&R Block after testing.** NYSSCPA reports: "Though its answers were more on-topic, he found, the bot was also more likely to make up answers that were just wrong."
- **The labels in the product.** NYSSCPA reports that "Both companies included caveats in their products, describing them as works in progress." It quotes Intuit Assist as saying it "is still developing and will improve with your help," and H&R Block's bot as saying it "is still learning, so please review all responses." The Inc. piece calls these "fine print disclaimers."
- **Fowler's advice.** NYSSCPA reports Fowler concluded that users can ignore the chatbots and still do their taxes.
- **The Taxpayer Advocate's response.** Citing the Post review, the National Taxpayer Advocate's June 11, 2024 tip said: "As a result, taxpayers should not solely rely on AI-generated tax advice." Thomson Reuters attributes the tip to National Taxpayer Advocate Erin Collins.

## What Intuit and H&R Block said

- **Intuit, on the fix.** NYSSCPA reports that spokeswoman Karen Nolan told Fowler that Intuit changed its system so Intuit Assist pulls self-help answers first from a more advanced search capability, replacing the older technology that had been the first source.
- **Intuit, on users.** NYSSCPA reports Nolan told Accounting Today that Intuit had not found a significant number of users with problems. She said TurboTax gives every filer "a tax return lifetime guarantee, including 100% accurate calculations, audit support and a maximum refund."
- **Intuit, in June.** Thomson Reuters reports an Intuit spokesperson said back-end improvements had been made since the Post's testing. An Intuit statement said the assistant "is designed to intuitively show, guide, and help our TurboTax customers, and do more of the hard work for them."
- **H&R Block, on accuracy.** NYSSCPA reports spokeswoman Teri Daley said accuracy is not perfect and may never be, given how complex the tax system is. Heather Watts, senior vice president of consumer tax products, told Accounting Today that more detailed user input produces more accurate answers, and that H&R Block "is backed by guarantees including audit support, maximum refunds and 100 percent accuracy."
- **H&R Block, in June.** Thomson Reuters reports H&R Block's senior vice president of consumer tax products said staff monitor questions and feedback daily, and that its evaluation "does not suggest a significant number of incorrect or irrelevant answers."
- **On audits.** The Inc. piece says both firms told the Post "they would provide assistance if users were audited after listening to an AI's bad advice."
- **What no opened source says.** Which of the 16 questions each bot got wrong. What the guarantees cover when the error came from the chatbot's advice rather than the software's math. Whether anyone retested H&R Block's bot.

## Where in the flow it broke

Based on the reports above, and only as far as they go:

1. **The question.** A filer typed a plain tax question inside the software they were using to file, such as where a college student should file.
2. **The missing fact.** The right answer to the college question depends on one fact the question did not give: whether the daughter earned income in Arizona. No opened source says either bot asked for it. Reading the reports, we infer it did not; that is our reading, not a reported fact.
3. **The answer.** H&R Block's bot stated a rule (file in both states) as if it applied. TurboTax's bot answered a nearby topic (renters credits, extensions, student status) instead of the question.
4. **The links.** After its update, TurboTax's bot still sent answers and links to irrelevant information about a quarter of the time, per NYSSCPA.
5. **The caveat.** The only warning was a standing label that the tool was still learning or developing. The reports do not describe any per-answer cue that a given answer was uncertain or needed a professional.
6. **The stakes.** The filer was in the middle of a legal filing. A wrong answer here can mean a missed or extra state return.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). Strong fit. H&R Block's bot gave a wrong filing rule, and NYSSCPA reports it was "more likely to make up answers that were just wrong." The only caveat was a general "still learning" label, not a cue on the wrong answer or a source the filer could check. The opened sources do not describe the bots' tone, so "confident" rests on the absence of any per-answer warning.
- [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`). Partial fit. TurboTax answered the college question with general resources on other topics, and still sent "answers and links to irrelevant information" after its update. That pattern is about links in place of an answer; here the links were also off topic, which is worse than that page describes.
- [Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md) (`guessing-instead-of-asking`). Partial fit. The college answer turns on whether the daughter earned income in Arizona, and H&R Block's own Heather Watts said detailed input gives better answers. No source says the bot asked; we infer it did not, so treat this fit as our reading.
- **Considered, weak.** [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md): that page is about too many caveats. Here there was one standing caveat, which the Inc. piece calls fine print, and no warning on the answers that mattered. The overlap is only that page's point that the one warning that matters should stand out.
- **Considered, not a fit.** [Eligibility answers sound like decisions](../goals/government-service-agents/failures/eligibility-answers-sound-like-decisions.md): it is about public-service chats, not private tax software. [Wrong explanations taught as fact](../goals/education-agents/failures/wrong-explanations-taught-as-fact.md): it is about tutoring. [Answer buried](../goals/response-structure/failures/answer-buried.md): TurboTax's long air conditioner reply was judged irrelevant, not a right answer hidden in text.
- **Gap for a person to judge.** No pattern in the taxonomy covers an assistant that answers a nearby topic instead of the question asked, as TurboTax did with renters credits and extensions. "Answers a nearby question" may be warranted as its own pattern; that is a proposal, not a decision.

## Related incidents

- [NYC MyCity chatbot gives businesses illegal advice (2024)](nyc-mycity-chatbot-gives-businesses-illegal-advice-2024.md): a government chatbot stated rules that the reporting says were wrong under the law.
- [Microsoft Copilot wrong election answers (December 2023)](microsoft-copilot-wrong-election-answers-december-2023.md): a tested assistant gave wrong answers to questions about official rules and dates.

## What to measure

Our proposals, not the Post's, Intuit's or H&R Block's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Reviewed accuracy rate | Answers a tax professional marks correct, divided by answers reviewed (on a labeled sample of real questions) |
| Off-topic answer rate | Answers a reviewer marks as about a different topic than the question, divided by answers reviewed |
| Off-topic link rate | Answers with at least one link a reviewer marks irrelevant to the question, divided by answers with any link |
| Missing-fact ask rate | Questions whose correct answer depends on a fact the user did not give, where the assistant asks for that fact before answering, divided by those questions |
| Conditional answer rate | Answers to those same questions that state the condition (for example "only if she earned income there") instead of a flat rule, divided by those questions |
| Per-answer caution rate | Answers a reviewer marks wrong or uncertain that carried an answer-level cue to check with a professional, divided by answers marked wrong or uncertain |

## What a team can change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run.

1. **Answer the question asked.** Pass: on the college test question, the reply addresses where the student must file, not renters credits or extensions.
2. **Ask for the deciding fact, or state the condition.** Pass: when the answer turns on a fact the user did not give, the reply asks for it in one short question, or states the rule with its condition ("only if she earned income in Arizona").
3. **No flat rule where the law is conditional.** Pass: the reply never says "you must file in both states" when filing in the second state depends on income there.
4. **Links must match the question.** Pass: every link in the reply is about the topic the user asked about.
5. **Put the caution on the answer, not only on the box.** Pass: on a question a reviewer marks complex, the reply itself says to confirm with a tax professional or the IRS, beyond the standing "still learning" label.
6. **Don't over-correct.** Pass: a simple question with a settled answer, such as how to find a field in the software, gets a direct answer with no extra warning.

## What we could not verify

- The Washington Post column itself. The page returned HTTP 403. Its date of March 4, 2024 comes from the URL NYSSCPA links to, not from the page.
- That two tax professionals reviewed the answers. Seen only in a search summary; opened sources say "human tax professionals" and name one, Beverly Goodman.
- That TurboTax's first version failed more than half the questions and H&R Block's failed more than 30 percent. Seen only in search summaries; kept out of the claims. The opened figure is the Taxpayer Advocate's "up to 50 percent."
- That H&R Block recommended single filing status and ruled out head of household. Seen only in a search summary. iTechPost, which we opened, says only "incorrect filing status."
- Accounting Today's original article with the Nolan, Daley and Watts statements. We read those statements only as NYSSCPA reports them; the Accounting Today page was not opened.
- Inc.'s original article. The Inc. page returned HTTP 403; we read the same piece as syndicated by CPA Practice Advisor, which credits "Kit Eaton, Inc. (TNS)."
- Coverage from Gusto, Vibe Graveyard, WNYC's On the Media, AARP and Insightful Accountant. Seen only in search results; not opened.
- Marketplace (April 15, 2024) describes a separate Temple University test, not the Post's, so we use it for no claim here.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://nysscpa.org/news/1046937-tech-columnist-turbotax-and-hr-block-chatbots-are-unhelpful-or-wrong-much-of-the-time-2024-03-07 | NYSSCPA, The Trusted Professional (no byline) | 2024-03-07 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked in a second fetch |
| https://taxpayeradvocate.irs.gov/news/tax-tips/is-ai-generated-tax-advice-making-the-grade/2024/06 | Taxpayer Advocate Service (no byline; page last updated 2026-01-07) | 2024-06-11 | Yes, 2026-10-23, fetch-tool summary; quotes taken from a fetch that asked for exact sentences |
| https://tax.thomsonreuters.com/news/do-not-solely-rely-on-ai-tax-advice-says-taxpayer-advocate-industry-responds/ | Thomson Reuters Checkpoint (Tim Shaw) | 2024-06-17 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked in a second fetch |
| https://www.cpapracticeadvisor.com/2024/03/12/why-your-business-shouldnt-rely-on-ai-powered-tax-prep-advice/102491/ | CPA Practice Advisor (Kit Eaton, Inc., via Tribune Content Agency) | 2024-03-12 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked in a second fetch |
| https://www.itechpost.com/articles/121348/20240305/ai-chatbots-tax-filing-giving-bad-advices-reports.htm | iTechPost (Kyle Marcelino) | 2024-03-05 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked in a second fetch |
| https://www.marketplace.org/story/2024/04/15/tax-ai-assistants-intuit-hr-block | Marketplace (Meghan McCarty Carino) | 2024-04-15 | Yes, 2026-10-23, fetch-tool summary; describes a different test, so not used for claims |
| https://www.washingtonpost.com/technology/2024/03/04/ai-taxes-turbotax-hrblock-chatbot/ | The Washington Post (Geoffrey A. Fowler) | 2024-03-04 (from URL) | No. HTTP 403 |
| https://www.inc.com/kit-eaton/your-business-should-not-rely-on-ai-powered-advice-from-turbo-tax.html | Inc. (Kit Eaton) | 2024-03 | No. HTTP 403 |

## Corrections

If you can share the Washington Post's full list of 16 questions and how each bot scored, or a later retest of either assistant, tell us and we will fix this page.
