---
title: "ChatGPT Search Misattributes News Quotes: Tow Center Study"
date: 2024-11-27
source: "https://www.cjr.org/tow_center/how-chatgpt-misrepresents-publisher-content.php"
description: "A Tow Center test of 200 news quotes found ChatGPT Search gave wrong or partly wrong sources 153 times and admitted it could not answer only seven times."
summary: "On November 27, 2024, the Tow Center for Digital Journalism published, in the Columbia Journalism Review, a test of ChatGPT Search. Researchers Klaudia Jaźwińska and Aisvarya Chandrasekar gave it 200 block quotes from 20 publishers and asked for the source of each. It returned partially or entirely incorrect responses 153 times and acknowledged it could not answer accurately only seven times. It cited a plagiarized copy of a New York Times story and a syndicated copy of an MIT Technology Review story. OpenAI called it an atypical test. A March 2025 follow-up found similar problems across eight AI search tools. Status: Needs review."
categories:
  - Search and Chat Assistants
  - Accuracy
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - one-sided-or-cherry-picked-sources
  - tone-changes-shipped-with-no-regression-test
---

**This page is a dated teardown of one public study, the Tow Center's November 2024 test of ChatGPT Search, for teams that build a chatbot that answers with web sources and links.** ChatGPT Search is the web search feature inside OpenAI's ChatGPT. The study was a structured test by researchers, not a report of harm to one user. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** Five sources were downloaded as raw HTML on 2026-10-25 and read as text: the Columbia Journalism Review (CJR) report, its March 2025 follow-up, TechCrunch, Search Engine Journal and MediaPost. Each quote below was checked word for word against that text with a script. We did not open the study's data on GitHub.

> **Read this first.** This is a summary of public reporting and of one study, not legal advice and not a finding of fact about OpenAI. The study's own authors say more rigorous testing is needed to know the true error rate. OpenAI disputes the method. Do not read the counts below as a general accuracy rate for ChatGPT.

## What happened (as reported)

- **The report, November 27, 2024.** CJR published "How ChatGPT Search (Mis)represents Publisher Content" by Klaudia Jaźwińska and Aisvarya Chandrasekar of the Tow Center for Digital Journalism at Columbia's Graduate School of Journalism.
- **The pitch it tested.** The report says OpenAI emphasized "timely answers with links to relevant web sources" but made "no explicit commitment to ensuring the accuracy of those citations." Search Engine Journal (November 30, 2024) says ChatGPT Search launched the month before.
- **The method.** The Tow Center randomly picked 20 publishers. They included publishers with OpenAI deals, publishers suing OpenAI, and unaffiliated publishers that allowed or blocked its search crawler. It took block quotes from 10 articles per publisher, 200 in all. Each quote, pasted into Google or Bing, returned the source article in the top three results. ChatGPT was asked to identify the source.
- **How it was scored.** A citation was judged on the publisher name, URL and article date. Results were graded correct, partially correct or incorrect.
- **The headline count.** "In total, ChatGPT returned partially or entirely incorrect responses on a hundred and fifty-three occasions, though it only acknowledged an inability to accurately respond to a query seven times." Search Engine Journal reported it as: "Of 200 queries, 153 responses were incorrect."
- **Hedges were rare.** Only those seven outputs used words like "appears," "it’s possible," or "might," or said "I couldn’t locate the exact article."
- **Blocked content.** Forty of the 200 quotes came from publishers that blocked its search crawler. The report says ChatGPT "rarely gave any indication of its inability to produce an answer."
- **Wrong publisher.** ChatGPT credited a letter to the editor from the Orlando Sentinel (November 19) to a Time article from November 9. The report says more than a third of responses included incorrect citations like this.
- **A plagiarized copy.** The New York Times blocks all OpenAI crawlers. For a quote from a Times piece on an endangered whale species, ChatGPT cited a site called DMS Retail, which had copied the whole article without credit.
- **A syndicated copy.** MIT Technology Review allows the crawler. For one of its quotes, ChatGPT cited Government Technology, which had syndicated the piece, instead of the original.
- **Different answers to the same query.** Asked the same query several times, it "typically returned a different answer each time." For a Washington Post article from October 8, 2024, the first try gave the wrong date and credited the New York Times with no source. The second try was fully correct with a working link. The authors suspect the default "temperature" setting of GPT-4o.
- **Deals and crawler access did not predict accuracy.** The New York Post and The Atlantic have licensing deals and allow all OpenAI crawlers, yet their content was often cited wrongly. Mother Jones and the Washington Post allow crawling, yet were rarely identified. ChatGPT still attributed quotes to the New York Times that were not from its articles.
- **An editor's view.** Mat Honan, editor in chief of MIT Technology Review, said: "I don’t think the small disclaimers you see in these chatbots—or when searching on other platforms—are enough."
- **OpenAI's response.** A spokesperson said: "Misattribution is hard to address without the data and methodology that the Tow Center withheld, and the study represents an atypical test of our product." The statement added: "We’ve collaborated with partners to improve in-line citation accuracy and respect publisher preferences". The Tow Center says it described its method and observations to OpenAI but did not share its data before publishing.
- **Coverage.** TechCrunch (Natasha Lomas, November 29, 2024), Search Engine Journal (Matt G. Southern, November 30, 2024) and MediaPost (Ray Schultz, December 1, 2024) reported the same core counts.

## Later: the March 2025 follow-up

- On March 6, 2025, the same authors published "AI Search Has a Citation Problem" in CJR. They tested eight tools in February 2025: ChatGPT Search, Perplexity, Perplexity Pro, DeepSeek Search, Copilot, Grok-2, Grok-3 and Gemini.
- They ran 1,600 queries. The tools "provided incorrect answers to more than 60 percent of queries." Perplexity was wrong on 37 percent; Grok 3 on 94 percent.
- ChatGPT "incorrectly identified 134 articles, but signaled a lack of confidence just fifteen times out of its two hundred responses, and never declined to provide an answer."
- The authors say the results were consistent with the first study and are "not just a ChatGPT problem."

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| How often it hedged | CJR lists "appears," "it’s possible" and "might." Search Engine Journal says phrases like "possibly" were used in only seven responses. We follow CJR. |
| OpenAI's user count | CJR quotes "250M weekly ChatGPT users." TechCrunch quotes "250 million." Same figure, different form. |
| MediaPost date | The byline reads December 1, 2024; the page title shows 12/02/2024. |
| Per-publisher results | CJR shows them in a table image and on GitHub. We did not open either, so we give no per-publisher counts. |
| What OpenAI changed | No opened source says what OpenAI changed in ChatGPT Search after the study. |

## Where in the flow it broke

Based on the reports, in order:

1. **The question.** The user pastes an exact quote and asks where it came from. A search engine either bolds the match or says there are no results (CJR).
2. **The lookup.** For 40 quotes the original was off limits, because the publisher blocked the crawler. Nothing stopped the bot from answering anyway.
3. **The source pick.** When the original was blocked or missed, it reached for a copy: a plagiarized page or a syndicated reprint.
4. **The answer.** It named a publisher, date and link in the same sure tone whether right or wrong. Only seven answers in the whole test of 200 carried any hedge.
5. **The repeat.** The same query could give a right answer once and a wrong one the next time.
6. **The disclaimer.** A small general warning was the only cue, which Honan said is not enough.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit. 153 wrong or partly wrong answers with seven hedges is that page's issue in numbers. The twist is that a source was given, but it was the wrong one, so the user's way to check pointed the wrong way.
- **[One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md)** (`one-sided-or-cherry-picked-sources`). Weak fit. That page is about source choice and showing how strong each source is. Here the bot chose a plagiarized or syndicated copy over the original. The bias was toward reachable copies, not toward agreeing views.
- **[Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md)** (`tone-changes-shipped-with-no-regression-test`). Weak fit. The shared idea is a fixed set of queries run again and again. The study did that and found answers changed from run to run. That page covers tone, not facts, and no source says a change was shipped.
- **Considered and rejected.** [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md) (`excess-disclaimers-and-warnings`): the complaint was too little warning, not too much. [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`): the bot gave one confident answer, not a pile of links. [Guessing instead of asking](../goals/dialogue-management/failures/guessing-instead-of-asking.md) (`guessing-instead-of-asking`): the request was not ambiguous; the bot needed to say "not found," not ask a question. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`): the prompts held no false premise.
- **Possible gaps for a person to judge.** (1) No pattern covers misattribution: a citation that names the wrong publisher or links a copy instead of the original. That is checkable apart from a wrong answer. (2) No pattern covers a missing "not found" reply when the source is blocked or unreachable. (3) No pattern covers the same factual query giving different answers on repeat runs. These are proposals, not decisions.

## Related incidents

- [Apple Intelligence notification summaries (December 2024)](apple-intelligence-notification-summaries-misreport-news-headlines-december-2024.md): an AI feature that misreported news under a publisher's name, weeks later.
- [Google AI Overviews odd and unsafe answers (May 2024)](google-ai-overviews-odd-and-unsafe-answers-may-2024.md): another AI search answer stated with confidence and wrong.
- [Meta Galactica (November 2022)](meta-galactica-science-ai-demo-fake-papers-pulled-november-2022.md): references that looked real but were not.
- [Mata v. Avianca fabricated case citations (2023)](mata-v-avianca-fabricated-case-citations-2023.md): wrong citations a professional relied on.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Source match rate | Share of "where is this quote from" answers whose publisher, URL and date all match the original |
| Wrong-publisher rate | Share of answers that name a publisher other than the one that ran the quote |
| Copy-instead-of-original rate | Share of cited links that point to a reprint or copy when the original is known |
| Unreachable-source honesty | Share of queries on blocked or unreachable sources where the reply says it could not find or open the source |
| Hedge-when-wrong rate | Share of wrong answers that carry a stated doubt or "not found" |
| Repeat stability | Share of queries that give the same source on five runs |

## What a team can change

Our proposals, not OpenAI's. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Say "not found."** Run 40 quotes from sites the crawler may not open. Pass: every reply says it could not find or open the source, or gives the right source.
2. **Name the right publisher.** Run 200 exact quotes with known sources. Pass: no reply names a publisher that did not run the quote.
3. **Prefer the original.** For quotes whose original is reachable, pass: the link points to the original publisher's page, not a reprint.
4. **No credit to copies of blocked work.** For a quote from a blocked site, pass: the reply never cites a copy as the source.
5. **Same query, same source.** Run each of 50 quotes five times. Pass: all five replies name the same source, or all say "not found."
6. **Doubt shows when evidence is thin.** Pass: every reply whose link does not contain the quoted text says so.
7. **Link proves the claim.** Pass: the quoted text appears on every cited page.

## What we could not verify

- The study's per-publisher table and GitHub data. Not opened; no per-publisher counts appear here.
- The full prompt wording used in November 2024; the CJR text we read does not print it.
- OpenAI's launch press release that CJR quotes. Not opened; its words appear only as CJR quotes them.
- Search-summary claims from IndieHackers, the OECD AI incident page and The Decoder, including other error counts. Not opened; not used.
- Nieman Lab, Computing and The Daily Star coverage of the March 2025 follow-up. Seen only in search results; not used.
- Whether OpenAI changed ChatGPT Search after the study. No opened source says.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.cjr.org/tow_center/how-chatgpt-misrepresents-publisher-content.php | Columbia Journalism Review, Tow Center (Klaudia Jaźwińska and Aisvarya Chandrasekar) | 2024-11-27 | Yes, 2026-10-25, live raw HTML read as text; quotes checked word for word |
| https://techcrunch.com/2024/11/29/study-of-chatgpt-citations-makes-dismal-reading-for-publishers/ | TechCrunch (Natasha Lomas) | 2024-11-29 | Yes, 2026-10-25, live raw HTML read as text |
| https://www.searchenginejournal.com/chatgpt-search-shows-76-5-error-rate-in-attribution-study/533978/ | Search Engine Journal (Matt G. Southern) | 2024-11-30 | Yes, 2026-10-25, live raw HTML read as text |
| https://www.mediapost.com/publications/article/401521/chatgpt-misattributes-article-sources-study-finds.html | MediaPost (Ray Schultz) | 2024-12-01 | Yes, 2026-10-25, live raw HTML read as text |
| https://www.cjr.org/tow_center/we-compared-eight-ai-search-engines-theyre-all-bad-at-citing-news.php | Columbia Journalism Review, Tow Center (Klaudia Jaźwińska and Aisvarya Chandrasekar) | 2025-03-06 | Yes, 2026-10-25, live raw HTML read as text; quotes checked word for word |

## Corrections

If you have the study's full prompts, OpenAI's own account of what changed in ChatGPT Search afterward, or newer test results, tell us and we will fix this page.
