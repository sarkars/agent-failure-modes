---
title: "AI Assistants Misrepresent News: EBU and BBC Study"
date: 2025-10-22
source: "https://www.ebu.ch/research/open/report/news-integrity-in-ai-assistants"
description: "An EBU and BBC study had journalists at 22 public broadcasters grade 2,709 answers from ChatGPT, Copilot, Gemini and Perplexity; 45% had at least one significant issue, most often sourcing."
summary: "On October 22, 2025, the European Broadcasting Union (EBU) and the BBC published News Integrity in AI Assistants. Twenty-two public service media organizations in 18 countries and 14 languages asked the free versions of ChatGPT, Copilot, Gemini and Perplexity 30 core news questions in late May and early June 2025. Journalists graded 2,709 core answers. 45% had at least one significant issue; sourcing (31%) was the biggest cause, then accuracy (20%) and missing context (14%). Gemini had significant issues in 76% of answers. The study builds on a February 2025 BBC study that found significant issues in 51%. The publishers ran and graded the study themselves. Status: Needs review."
categories:
  - Search and Chat Assistants
  - Accuracy
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - text-invented-citations
  - one-sided-or-cherry-picked-sources
---

**This page is a dated teardown of one public study, the EBU and BBC "News Integrity in AI Assistants" report of October 2025, for teams that build a chat assistant that answers news or current-events questions with web sources.** It was a structured test by broadcasters, not a report of harm to one user. Every fact below comes from a source we opened (listed at the end).

**Status: Needs review.** On 2026-10-30 we downloaded the full report PDF from the EBU and the BBC's February 2025 report PDF, extracted their text, and read the methods and findings sections. We also read the BBC press release as raw HTML and three news reports through a fetch tool. In review we re-read the report, the BBC release, Reuters and The Register as raw page text and matched every number and quote below against it; Al Jazeera blocked the raw fetch, so its one figure rests on a fetch summary. Numbers below come from the report unless another source is named.

> **Read this first.** This is a summary of one study, not a finding of fact about OpenAI, Microsoft, Google or Perplexity. The study was designed, run and graded by public broadcasters whose own content was being judged, and its foreword asks for more publisher control over how AI uses their content. They have an interest in the outcome. The answers came from free versions in May and June 2025; the report says several assistants have been updated since. Do not read the counts below as current error rates.

## What happened (as reported)

- **The report, October 21-22, 2025.** The EBU report page is dated October 21, 2025. The BBC press release is timed 12:01 am, October 22, 2025. It was launched at the EBU News Assembly in Naples. Reuters (Olivia Le Poidevin) ran on Yahoo News at 10:08 pm UTC, October 21.
- **Who took part.** 22 public service media organizations in 18 countries, working in 14 languages, including the BBC, ZDF, Radio France, Yle, SVT and NPR in the United States.
- **What testers asked.** 30 "core" questions, picked from real audience questions, were asked by every organization; some added "custom" local questions. Each question carried a prefix such as "Use DW sources where possible." Examples: "Who is the Pope?", "Is Viktor Orbán a dictator?", "Why were NASA astronauts stuck in space?"
- **Which assistants.** The free consumer versions of ChatGPT, Copilot, Gemini and Perplexity, on default settings. Answers were generated in late May and early June 2025. Organizations that block AI crawlers lifted the blocks during that window, then put them back.
- **How it was graded.** Journalists rated each answer for accuracy (including direct quotes), sourcing, opinion versus fact, editorialization and context. Each was rated no issues, some issues, significant issues or don't know.
- **How many answers.** From a possible 2,760 core answers, refusals and failed runs were dropped, leaving 2,709 graded core answers. Across all 3,113 core and custom questions, only 17 got a refusal (0.5%).
- **The headline count.** "Overall, 45% of all AI responses were found to have at least one 'significant' issue." Counting "some issues" too, 81% had an issue.
- **By type of error.** Sourcing 31% (claims not supported by the cited source, no source at all, or wrong or unverifiable source claims). Accuracy 20%, with every assistant between 18 and 22%. Context 14% (Copilot 23%, others near 10%). Opinion versus fact 6%. Of 1,053 answers with a direct quote, 12% had significant quote problems.
- **By assistant.** Significant issues: Gemini 76%, Copilot 37%, ChatGPT 36%, Perplexity 30%. Significant sourcing issues: Gemini 72%, ChatGPT 24%, Perplexity and Copilot 15% each. 42% of Gemini answers gave no direct link to a specific piece of content.
- **Outdated facts.** The report calls outdated information one of the most common issues. Asked "Who is the Pope?" in late May 2025, ChatGPT, Gemini and Copilot named Francis, who had died in April. Copilot did so while also giving his death date in the same answer.
- **Wrong on the law.** Perplexity said surrogacy is prohibited by law in Czechia; the report says it is not regulated either way. Gemini said disposable vapes would be illegal to buy, when the change covered sale and supply.
- **Sure and wrong.** Asked why NASA astronauts were stuck in space, Gemini said they were not, and suggested the user was thinking of a sci-fi movie. Two astronauts had spent just over nine months on the space station.
- **Sources that do not back the claim.** ChatGPT cited a Swiss broadcaster (SRF) for an EU claim when the SRF source said the opposite. Gemini credited a quote to the Belgian broadcaster VRT that a financial economist had said. Gemini often wrote "according to" a broadcaster with no link or a link to another outlet; evaluators saw this in 54% of Gemini answers and in no more than 4% for any other assistant.
- **Satire as fact.** Asked if Elon Musk did a Nazi salute, Gemini used a Radio France satire segment as a news source, added words to a quote from it, and linked a Telegraph video that did not contain the claims.
- **Long source lists.** Perplexity added 19 URLs to one answer but referred to only three in the text.
- **What the publishers asked for.** Developers should cut errors and publish results by language and market. The team released a News Integrity in AI Assistants Toolkit with a checklist and an error taxonomy.
- **Company responses.** Reuters says it contacted the companies for comment; Al Jazeera says none had immediately responded. No opened source carries a statement from any of the four companies about this study.

## Earlier: the BBC's February 2025 study

- The BBC's Responsible AI team asked the same four assistants 100 news questions on December 5-6, 2024, with the prefix "Use BBC News sources where possible." The BBC lifted its crawler blocks for the test.
- It found significant issues in 51% of answers. 19% of answers that cited BBC content added factual errors. 13% of quotes sourced to BBC articles were altered or not in the cited article.
- That round used paid or enterprise tiers in some cases (ChatGPT Enterprise, Copilot Pro, Perplexity Pro). The 2025 round used free versions, so the report says the two cannot be compared directly. On BBC-only data (362 answers then, 237 now), significant issues fell from 51% to 37%.

## How this differs from the Tow Center study

The [Tow Center study of ChatGPT Search (November 2024)](chatgpt-search-misattributes-news-quotes-tow-center-study-november-2024.md) pasted 200 exact quotes into one product and asked only "where is this from?". It scored one thing: the citation. This study asked open news questions, in 14 languages, to four assistants, and journalists graded the whole answer: facts, quotes, sources, opinion and context. Tow was run by an outside research center; this one was graded by the broadcasters whose content was cited. Both found the same core problem: few refusals and few hedges, even when the answer or the source was wrong.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| How many answers | The BBC release and The Register say "more than 3,000"; Reuters says 3,000. Al Jazeera (read only through a fetch summary) says "more than 2,700," as does the report's country section. The report says 2,709 core answers were graded, from 3,113 core and custom questions. The figures count different sets. |
| Gemini's rate | The BBC release and The Register's headline give 76% (any significant issue). Reuters and The Register's body give 72%, which the report gives for sourcing only. |
| Other assistants | The Register lists ChatGPT 24% and Perplexity and Copilot 15% as error rates. In the report those are sourcing rates; overall rates are 36%, 30% and 37%. We follow the report. |
| Pope error timing | Reuters says "several months" after his death; The Register says "weeks." The report says the ChatGPT answer came in May 2025; Francis died in April. |
| Audience trust | The Register says 42 percent of 2,000 UK adults trust AI to give accurate news summaries. The BBC release and the report say "just over a third." The report gives 42% as the share who would trust the original news source less after an AI error. We did not open the BBC audience study and use none of these as fact. |
| Grading consistency | The report describes quality checks but gives no agreement rate between graders. |

## Where in the flow it broke

1. **The question.** A user asks about a moving story ("Who is the Pope?", "Is Trump starting a trade war?"). The report says fast-changing stories drew the most significant issues.
2. **The lookup.** The assistant draws on an index or model memory that may be out of date, and does not check the date against the event.
3. **The source pick.** It cites a page that does not support the claim, an unrelated page, a satire segment, or names an outlet with no link.
4. **The answer.** It writes in a sure, news-like voice, rarely refuses, and seldom says what is not known. Opinions can appear as fact or as the outlet's own view.
5. **The display.** A long list of links makes the answer look checked even when the text uses only a few of them.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit. 0.5% refusals, a dead Pope named as current, and an answer telling the user they had the facts wrong are this page's issue. The report has a whole section on over-confidence.
- **[Invented citations and quotes](../goals/ai-slop-detection/failures/text-invented-citations.md)** (`text-invented-citations`). Partial fit. Altered quotes (12% of answers with quotes) and source claims the linked page does not support match the page's check. But that page covers a writer publishing AI drafts; here the assistant shows the citation straight to the reader.
- **[One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md)** (`one-sided-or-cherry-picked-sources`). Partial fit. The missing-context (14%) and opinion-versus-fact (6%) findings, and the satire answer the report calls one sided, touch that page's "show where sources disagree." Most sourcing errors here were wrong or missing sources, not biased choice.
- **Considered and rejected.** [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`): Perplexity's 19 links came with an answer, not instead of one. [Stale price or stock at checkout](../goals/shopping-agents/failures/stale-price-or-stock-at-checkout.md) (`stale-price-or-stock-at-checkout`): same idea of stale data, but it is about shopping totals, not facts. [Results delivered without context](../goals/health-scheduling-agents/failures/results-delivered-without-context.md) (`results-delivered-without-context`): about patient test results.
- **Possible gaps for a person to judge.** (1) Outdated facts in general answers: no pattern covers stating a past fact as current. (2) Misattribution: naming an outlet as the source of a claim or opinion it did not publish. (3) Opinion presented as fact or as the source's own view. (4) Cited-but-unused source lists that look like evidence. These are proposals, not decisions.

## Related incidents

- [ChatGPT Search misattributes news quotes: Tow Center study (November 2024)](chatgpt-search-misattributes-news-quotes-tow-center-study-november-2024.md): citation-only test of one product; see the comparison above.
- [Apple Intelligence notification summaries (December 2024)](apple-intelligence-notification-summaries-misreport-news-headlines-december-2024.md): an AI summary put a false claim under the BBC's name.
- [Perplexity misstates and invents WIRED stories (June 2024)](perplexity-answer-engine-misstates-and-invents-wired-stories-june-2024.md): an answer engine misreported a named outlet's articles.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute from logs |
|---|---|
| Claim support rate | Share of cited claims whose linked page contains the claim |
| Direct-link rate | Share of news answers with at least one link to a specific article, not a home page or Wikipedia page about the outlet |
| Unlinked attribution rate | Share of answers that say "according to [outlet]" with no link to that outlet's page |
| Quote match rate | Share of quoted strings found word for word on the cited page, credited to the right speaker |
| Currency check | Share of "who is the current X" answers that match a dated reference list on the run date |
| Cited-but-unused links | Links in the source list that no sentence in the answer refers to |
| Stated-unknown rate | Share of answers to unresolved stories that say what is not yet known |

## What a team can change

Our proposals, not the companies' or the publishers'. Each is a pass/fail check on a transcript. Status: Not yet run.

1. **Every claim has a page that says it.** Pass: for each linked claim, the cited page contains it.
2. **Name an outlet only with its link.** Pass: no answer says "according to [outlet]" without a link to that outlet's page.
3. **Quotes match exactly.** Pass: every quoted string appears word for word on the cited page and names the right speaker.
4. **Check "current" facts on the day.** Keep 20 office-holder questions with a dated answer key. Pass: every answer matches the key on the run date.
5. **Label opinion.** Pass: every evaluative sentence names who holds the view and never puts it in the cited outlet's mouth unless the outlet said it.
6. **No satire as news.** Pass: no answer to a factual question cites a page tagged as satire or comedy.
7. **Say what is not known.** For 10 questions on open stories, pass: each answer states one thing not yet confirmed.
8. **Trim the source list.** Pass: every listed link is referred to in the answer text.

## What we could not verify

- The BBC-Ipsos audience study and its trust figures. Not opened; not used as fact.
- The News Integrity in AI Assistants Toolkit. Not opened; its contents are described only as the report states them.
- NPR's October 21, 2025 post, Journalism.co.uk, Press Gazette and other coverage. Seen only in search results; not used.
- Any response from OpenAI, Microsoft, Google or Perplexity to this study. None found in opened sources.
- Whether results hold for paid tiers or for the updated models listed in the report's October 16, 2025 table.

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.ebu.ch/research/open/report/news-integrity-in-ai-assistants | EBU research page | 2025-10-21 | Yes, 2026-10-30, fetch tool |
| https://www.ebu.ch/files/live/sites/ebu/files/Publications/Intelligence/open/EBU-Intelligence-BBC_News_Integrity_in_AI_Assistants_Report_2025.pdf | EBU and BBC, full report | October 2025 | Yes, 2026-10-30, PDF downloaded, text extracted and read |
| https://www.bbc.co.uk/mediacentre/2025/new-ebu-research-ai-assistants-news-content | BBC Media Centre press release | 2025-10-22 | Yes, 2026-10-30, raw HTML read as text |
| https://www.ebu.ch/news/2025/10/ai-s-systemic-distortion-of-news-is-consistent-across-languages-and-territories-international-study-by-public-service-broadcaste | EBU press release | 2025-10-22 | Yes, 2026-10-30, fetch tool |
| https://www.bbc.co.uk/aboutthebbc/documents/bbc-research-into-ai-assistants.pdf | BBC (Oli Elliott), February 2025 study | February 2025 | Yes, 2026-10-30, PDF downloaded, text extracted and read |
| https://www.yahoo.com/news/articles/ai-assistants-widespread-errors-news-220841474.html | Reuters via Yahoo News (Olivia Le Poidevin) | 2025-10-21 | Yes, 2026-10-30, fetch tool |
| https://www.aljazeera.com/news/2025/10/22/ai-models-misrepresent-news-events-nearly-half-the-time-study-says | Al Jazeera (John Power) | 2025-10-22 | Yes, 2026-10-30, fetch tool |
| https://theregister.com/2025/10/24/bbc_probe_ai_news | The Register (Owen Hughes) | 2025-10-24 | Yes, 2026-10-30, fetch tool |

## Corrections

If you have the Toolkit, grader agreement data, company responses, or newer test results, tell us and we will fix this page.
