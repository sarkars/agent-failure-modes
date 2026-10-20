---
title: "Google Search AI Overviews Give Odd and Unsafe Answers, Google Responds"
date: 2024-05-30
source: "https://blog.google/products/search/ai-overviews-update-may-2024/"
summary: "In late May 2024, users and reporters shared AI Overviews in Google Search that told people to put glue on pizza and that cited a satire page on eating rocks. On May 30, 2024, Google's head of Search said some examples were real, some were fake, and listed changes. Google's accuracy and violation figures are its own and were not independently checked."
categories:
  - Search
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - one-sided-or-cherry-picked-sources
---

**This page is a dated teardown of one public answer-engine incident, for teams that let an AI write a short answer at the top of a search or help page.** Every fact below comes from a source we opened (listed at the end). Google's numbers and explanations are Google's own account; we found no independent test of them. We could not open The Verge or The Washington Post, so anything from them is second-hand.

## What happened (as reported)

- **Launch.** Google's post of May 30, 2024, written by Liz Reid, its head of Search, says Google had launched AI Overviews for everyone in the U.S. Engadget (May 30) also describes a "US rollout." We did not find the launch date in the sources we opened.
- **May 24, 2024.** 9to5Google (Ben Schoon) lists wrong answers people had shared: glue for pizza; "chicken only needs to be cooked to 102-degrees F"; "blinker fluid" treated as a real thing; adding more oil to put out an oil fire; and "not a country in Africa that starts with the letter K." We did not check each against Google's results. The same article quotes a Google spokesperson saying many examples "have been uncommon queries" and that "the vast majority of AI Overviews provide high quality information, with links to dig deeper on the web." The article's author wrote that the feature "literally cannot be turned off."
- **Glue on pizza.** TechCrunch (Sarah Perez, May 31) says the glue suggestion came from an 11-year-old Reddit comment. Engadget says it was based on forum content. Google's post names "using glue to get cheese to stick to pizza" as an example of forum advice, sometimes sarcastic or trolling, that the system used.
- **Eating rocks.** For "How many rocks should I eat?", TechCrunch says the overview cited satirical content from a geological software provider's website. Google's post says satire had been republished on that site, and that almost no one had searched that question before screenshots spread. Engadget says this answer was real.
- **Other claims.** Engadget, citing The Washington Post (not opened), says the feature also claimed Barack Obama was Muslim and that people should drink plenty of urine to pass kidney stones. We have not seen the original answers.
- **Fakes.** Google's post says many widely shared screenshots were faked, some obviously silly and some implying dangerous results on leaving dogs in cars, smoking while pregnant, and depression, and says those overviews never appeared. Engadget describes the dog claim as fake. We cannot verify this ourselves.
- **May 30, 2024.** Google published the post. It says "some odd, inaccurate or unhelpful AI Overviews certainly did show up" (quote via TechCrunch and Engadget).

## What Google said

From Google's post (our paraphrase, except where quoted):

- **Causes.** Nonsensical queries that seem designed to produce errors; "data voids" or information gaps on a topic; satire; user-generated content with bad advice; and, in a small number of cases, misreading the language on a page. TechCrunch reports Reid said the feature does not "hallucinate" like other language models but can err for other reasons, such as misinterpreting queries.
- **Testing.** Per TechCrunch, Google said it "tested the feature extensively before launch," including "robust red-teaming efforts," and that "there's nothing quite like having millions of people using the feature with many novel searches."
- **Numbers.** Google says its tests found AI Overviews accuracy "on par with featured snippets," and that it found a content policy violation on "less than one in every 7 million unique queries" where overviews appeared. The post as we read it does not describe the test or define "accuracy" or "violation," so we cannot judge these figures.
- **Changes.** Better detection of nonsensical queries that should not get an overview; limits on satire and humor content; limits on user-generated content where it could give misleading advice; triggering restrictions where overviews were not helpful; action on individual overviews that broke content policies; "more than a dozen" technical improvements in all. Google says it aims not to show overviews on hard news topics, and that it added refinements to strengthen protections on health queries. Engadget reports Google stopped showing AI answers for certain health topics; the post as we read it says "refinements," so we use that wording.

## What the sources do not say

- How many people saw a wrong overview, or how many answers were wrong. No source gives a count of real errors.
- Whether anyone was harmed by following one. No source reports a case.
- The model or retrieval setup, and how it picked the Reddit comment or the satire page.
- Whether the changes worked. We opened no after-the-fact measurement.
- How the "7 million" and "on par with featured snippets" figures were measured.
- Exactly which screenshots were fake. Google says many; we have no list.

## Pattern match

- [Chatbot is confidently wrong and you can't check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (Pattern ID `confident-wrong-answer-with-no-way-to-check`) is the core fit. The reported answers stated odd or unsafe advice as plain fact at the top of results. The sources do not show an uncertainty cue, and 9to5Google reports the feature could not be turned off. Links to sources did exist: Google's spokesperson says answers come "with links to dig deeper," and TechCrunch says the rocks answer cited the satire site. So the user could check in principle; the sources do not say whether the answer made the weak source obvious. The fit is strong on tone and stakes (food safety, a fire), partial on "no way to check."
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (Pattern ID `one-sided-or-cherry-picked-sources`) is a partial fit. That pattern is about a summary that leaves out sources that disagree. Here the reported problem was the opposite kind of source failure: a joke page and a forum comment treated as authority. Nothing we read says the system hid conflicting sources. We list it because the fix (show source strength) overlaps; we do not claim it is the same failure.

Not matched: [Stakes-blind register](../goals/stakes-calibration/failures/stakes-blind-register.md). It is about tone for grief, money and health. The sources describe wrong content, not an upbeat tone, so we do not force it.

## Where in the flow it broke

Based on the reports, the weak points were before and at the answer step:

1. **Trigger.** Odd queries, like the rocks question, got an overview at all. Google's own fix list includes better detection of queries that should not get one.
2. **Source choice.** A satire page and a sarcastic forum comment were used as the basis for an answer. Google's fixes name satire and user-generated content.
3. **Display.** The answer appeared as a confident summary. The sources do not describe any check on the claim before display, and Google's launch-time testing did not catch these before they went public.
4. **Correction.** Google's post lists system-level changes plus action on individual overviews that broke content policies. The sources do not say how fast any single bad answer was removed.

The reported cost is public ridicule and a policy response. No source reports a loss or an injury.

## What to measure

Proposed metrics; none come from Google. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Answers resting on a joke, satire or forum source | Sampled answers whose main source is tagged satire or user-generated, divided by all sampled answers |
| Answers to odd or nonsense queries | Answers shown for queries a classifier marks nonsensical or novel, divided by all answers |
| Unsafe advice rate | Reviewer-rated answers that give advice a safety reviewer calls harmful (food, fire, medicine), divided by answers in those topics |
| Share of answers with a visible source label | Answers whose first screen names the source type (forum, news, reference) |
| User reports per 1,000 answers | "Wrong or harmful" feedback clicks divided by answers shown |

## What a team can change

Proposed rules, each a pass/fail check on a test set. Status: Not yet run.

1. **No answer from satire or joke sources.** Tag source types; block tagged satire from the answer step. Check: a scripted set of known satire pages never becomes the basis of an answer.
2. **Sparse-evidence queries get no summary.** If few good sources exist, show plain results or say "I can't find reliable information." Check: a set of nonsense queries ("How many rocks should I eat?") returns no summary.
3. **Forum advice on safety topics needs a second source.** For cooking, fire, medicine and children, a single forum comment cannot carry an answer. Check: scripted safety queries show at least one reference or official source.
4. **Say where the answer comes from.** Show source type on the first screen, not only links below. Check: string match for a source label in every shown answer.
5. **Offer a way to turn it off or report it.** Check: a report control exists and logs the query and answer.
6. **Don't over-correct.** Blocking all forum content would remove useful first-hand advice that Google itself says forums provide. Test rule 3 on ordinary how-to queries to confirm helpful answers still appear.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://blog.google/products/search/ai-overviews-update-may-2024/ | Google (Liz Reid) | 2024-05-30 | Yes, 2026-10-20 |
| https://techcrunch.com/2024/05/31/google-admits-its-ai-overviews-need-work-but-were-all-helping-it-beta-test/ | TechCrunch (Sarah Perez) | 2024-05-31 | Yes, 2026-10-20 |
| https://9to5google.com/2024/05/24/google-ai-overview-mistakes-misinformation/ | 9to5Google (Ben Schoon) | 2024-05-24 | Yes, 2026-10-20 |
| https://www.engadget.com/google-is-putting-more-restrictions-on-ai-overviews-after-it-told-people-to-put-glue-on-pizza-011316780.html | Engadget (Mariella Moon) | 2024-05-30 | Yes, 2026-10-20 |

Not opened: The Verge's May 23, 2024 article (our fetch tool refused it); The Washington Post (cited second-hand by Engadget); and other results seen only in search summaries (Tom's Guide, iMore, Android Authority, Inquirer, NBC, Jakarta Post, Fortune). Nothing from those is used above except where marked second-hand.

## Corrections

If you have the original screenshots, Google's post archive, or a better date, tell us and we will fix this page.
