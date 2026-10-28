---
title: "ChatGPT gave fake 404 links to famous stories by its own news-licensing partners: Nieman Lab tests, June 2024"
date: 2024-06-27
source: "https://www.niemanlab.org/2024/06/chatgpt-is-hallucinating-fake-links-to-its-news-partners-biggest-investigations/"
description: "Nieman Lab tests in June 2024 found ChatGPT making up plausible URLs to its partners' top stories. Many hit 404 pages; OpenAI said linking was not live yet."
summary: "On June 13, 2024, Nieman Lab's Andrew Deck reported that ChatGPT gave made-up businessinsider.com links to Business Insider's big scoops, after the Insider Union raised the problem in a letter to management. Axel Springer, Business Insider's owner, had announced in December 2023 that ChatGPT answers would include links to its full articles. On June 27, 2024, Deck reported that ChatGPT was hallucinating URLs for at least 10 more partner publications, including the AP, The Wall Street Journal, the Financial Times and The Atlantic. The fake links followed each site's URL format but got the words or numbers wrong, so many led to 404 pages. OpenAI said the linking experience in its deals was still in development and not yet available in ChatGPT, and declined to explain the fake URLs. Status: Needs review."
categories:
  - Search and Chat Assistants
  - Accuracy
  - Trust
patterns:
  - confident-wrong-answer-with-no-way-to-check
  - invented-packages-and-apis
---

**This page is a dated teardown of Nieman Lab's June 2024 tests of ChatGPT links to news stories, for teams whose chat assistant gives users a URL to a source.** The product was ChatGPT, mostly the free version running GPT-4o with web browsing. The users were people asking where a famous news story first ran. The moment was the follow-up turn, when the user asked ChatGPT to share a link to the original story. ChatGPT answered with a URL that looked right and led to a 404 page. Every fact below comes from a source we opened (listed at the end). No opened source gives an error rate, a count of prompts, or OpenAI's account of how links were made. The date above is the day of the main Nieman Lab report; the first report ran June 13, 2024.

**Status: Needs review.** Five pages were downloaded as raw HTML on 2026-10-28 and read as plain text: Nieman Lab (Andrew Deck, June 13, 2024), Nieman Lab (Andrew Deck, June 27, 2024), The Atlantic (Matteo Wong, June 26, 2024), Engadget (Pranav Dixit, June 28, 2024) and MediaNama (July 2024; no byline found in the text we read). The Publisher Newsletter (July 1, 2024), which only summarizes Nieman Lab, was also downloaded and read. Each quote below was checked word for word against that text with a script, with curly and straight quote marks treated as the same. The Insider Union's letter, the screenshots in it, Axel Springer's and The Atlantic's deal announcements, and OpenAI's March 2024 post on links were not opened; they appear here only as Nieman Lab quotes or describes them.

> **Read this first.** This is a summary of public reporting and company statements, not a finding of fact and not legal advice. It does not say whether OpenAI met or broke any contract. No opened source shows the text of any licensing deal; the deal promises below are the publishers' announcements as quoted by Nieman Lab. Nieman Lab says its tests were "not a full audit of ChatGPT." We name only people who were quoted or named in the reporting.

**Channel note.** This is a chat incident: a text chatbot that wrote a link into its reply. This phase of the knowledge base is chat-first, and the signals and checks below are written for text chat. Voice and web signals, such as a voice assistant reading out a source, or a web search page that builds links from an index, are PLANNED only: never detected or measured here.

## What happened (as reported)

- **The deals promised links.** Nieman Lab quotes Axel Springer's December 2023 announcement: "ChatGPT's answers to user queries will include attribution and links to the full articles for transparency and further information." It quotes The Atlantic's May 2024 announcement: "Queries that surface The Atlantic will include attribution and a link to read the full article on theatlantic.com."
- **June 12-13, 2024: the Business Insider letter.** Nieman Lab reports that the Insider Union asked management "On Wednesday," the day before the June 13 report, for details of the OpenAI deal. The letter, signed by union steward and investigative reporter Katherine Long and other members, says: "Repeated efforts by unit members have been unable to prompt ChatGPT to link directly to our scoops, even when explicitly instructed to do so."
- **The Musk twins link.** Union members asked ChatGPT to name the first outlet that reported Elon Musk's twins with Shivon Zilis and to link to it. Nieman Lab: "The link, however, appears to have been a hallucination." The slug ChatGPT gave led to a "404 page not found" error on businessinsider.com. The real slug was different.
- **Replicated by the reporter.** Deck wrote that he "was able to replicate these errors in ChatGPT myself." Asked which outlet broke the Dave Portnoy investigation, ChatGPT named Insider but gave a made-up URL.
- **June 27, 2024: ten more partners.** Nieman Lab: "ChatGPT is hallucinating URLs for at least 10 other publications that are part of OpenAI's ongoing licensing deals." The list: The Associated Press, The Wall Street Journal, the Financial Times, The Times (UK), Le Monde, El País, The Atlantic, The Verge, Vox and Politico.
- **How the test ran.** Deck "repeatedly prompted ChatGPT to link out to these publications' marquee articles," including Pulitzer Prize-winning stories. He used the free version, mostly with GPT-4o and web browsing, and says he could also replicate the fake URLs with models that did not browse.
- **The Wirecard example.** ChatGPT said the FT broke the Wirecard story but first cited aggregators. Asked for the original, it gave an ft.com URL. Nieman Lab: "The link led to a 404 error that stated, 'The page you are trying to access does not exist.'" Nieman Lab says the WSJ's Pulitzer-winning 2018 hush-money reporting also got a link that "landed on a 404 error."
- **Close, but wrong.** For The Atlantic's Books3 story, ChatGPT's URL had the right section, month and year, and a plausible slug, but not the real one. Nieman Lab: "Unfortunately, close enough doesn't cut it for URLs." It adds: "Sometimes when I repeated a question, ChatGPT would even output slight variations on the same fake URL, leading to a string of 404 errors."
- **The worst moment.** Nieman Lab: "It was when I asked ChatGPT to share a link to the first outlet that reported a given story, or to share a link to reporting that it had already correctly identified and summarized, that the URLs were most likely to break."
- **A link to the wrong story.** In a test without browsing, ChatGPT named The Atlantic for its Bryan Singer investigation but gave the wrong year. "Even though ChatGPT claimed it could not browse the web, it still provided a hallucinated link." The link redirected to an unrelated 2014 Atlantic story.
- **Some links worked.** Nieman Lab says ChatGPT gave correct links to Politico's leaked Roe v. Wade draft decision and the WSJ's Facebook Files. Links in the newer parenthesis-style citations "had a much higher rate of accuracy" than links elsewhere in replies.
- **Separate test, same pattern.** In The Atlantic (June 26, 2024), Matteo Wong tried ChatGPT and Perplexity. When he asked ChatGPT for the original Politico article on the leaked Roe opinion, "it provided a nonfunctioning hyperlink." He says Perplexity was less error-prone than the other tools he tried.

## What the company said

- **OpenAI, to Nieman Lab (both reports).** "Together with our news publisher partners, we're building an experience that blends conversational capabilities with their latest news content, ensuring proper attribution and linking to source material — an enhanced experience still in development and not yet available in ChatGPT." The June 27 report names the spokesperson as Kayla Wood.
- **No answer on the fake links.** Nieman Lab: "OpenAI declined to answer questions on the hallucinations I documented or explain how new features might address the problem of fake URLs." It also "declined to answer questions about how ChatGPT generates its hyperlinks."
- **OpenAI's content chief, as quoted by Nieman Lab.** Nieman Lab says Tom Rubin, OpenAI's chief of intellectual property and content, said in May that displaying partner content was a "significant component" of the deals, but "you haven't yet seen it in our products."
- **OpenAI, to The Atlantic.** Wong reports that a spokesperson said the company is working on an attribution-forward search product that will direct users to partner content, and did not say when it would launch.
- **The Financial Times.** Rhonda Taylor, an FT spokesperson, told Nieman Lab: "The new experience is still under development and not yet live in ChatGPT, but the priority should be a better experience with high quality attribution, not speed of release."
- **The Atlantic.** Anna Bross, a spokesperson, told Nieman Lab: "Hallucinations in LLMs are known issues. We're raising to OpenAI any inaccuracies we encounter involving The Atlantic."
- **Business Insider.** Nieman Lab says it did not answer questions in time for publication. CEO Barbara Peng wrote to staff: "We have also known for some time that we cannot rely on external referrals as a significant driver of traffic."

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| How many publications | Nieman Lab (June 27): "at least 10 other publications," on top of Business Insider. MediaNama: "at least 9 other OpenAI partners," then lists all ten names. Engadget: "10 publishers." The Publisher Newsletter: "more than 10 publications." Nieman Lab is the original. |
| How often it failed | Nieman Lab says ChatGPT is "hallucinating URLs frequently," but gives no count of prompts or failure rate. It also says this "was not a full audit." No opened source gives a number. |
| Why it happened | Nieman Lab: ChatGPT "predicting the most likely version of the URL for a given story — rather than the correct one." That is the reporter's reading of the URL shapes. OpenAI declined to explain. The Atlantic quotes researchers on general retrieval errors, not on these links. |
| Dates in ChatGPT's answers | Nieman Lab says ChatGPT "occasionally" gave publication dates and named authors, and once gave a wrong year. MediaNama says ChatGPT "often got the date wrong." We found no count behind "often." |
| Was the promised feature live | OpenAI, the FT and Tom Rubin (as quoted) all say the partner linking experience was not live yet. The deal announcements quoted by Nieman Lab state links as part of the deal, with no launch date. |

## Where in the conversation flow it broke

Based on the reports above, and only as far as they go. Each step is a place a check could have caught it.

1. **First answer, right outlet.** ChatGPT usually named the outlet that broke the story correctly (Nieman Lab). Often it linked to an aggregator, not the original.
2. **The user asks for the original link.** This is the turn where URLs "were most likely to break" (Nieman Lab). The user has already been told the right outlet, so a link in the same confident reply looks trustworthy.
3. **A URL is written, not looked up.** The fake links followed each site's URL format with the wrong words or numbers. Nieman Lab's reading is that the model predicted the URL. No opened source shows a check that the URL exists before it is shown.
4. **No cue of doubt.** No opened source reports a reply that said the link was unverified. In one test, ChatGPT said it could not browse, then gave a link anyway.
5. **The user retries and gets another fake.** On a repeated question, ChatGPT sometimes gave "slight variations on the same fake URL" (Nieman Lab).
6. **The user lands on a 404 or the wrong story.** Some fake links went to 404 pages. Others redirected to unrelated stories on the right site, which is harder for a user to spot.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). Each fit rests on press reports of a reporter's and a union's tests; no opened source shows full transcripts or OpenAI's link code.

- [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) (`confident-wrong-answer-with-no-way-to-check`). **Strong fit.** The fake URL came in the same sure tone as a real one, with no cue that it was unverified. The twist: the link was the user's way to check, and the link itself was wrong.
- [Invented packages and APIs](../goals/coding-agents/failures/invented-packages-and-apis.md) (`invented-packages-and-apis`). **Partial fit.** Same mechanism in another domain: a name that follows the real naming pattern but does not exist. That page is about code dependencies, not web links, but its fix (verify the thing exists before showing it) maps directly.
- [One-sided or cherry-picked sources](../goals/research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) (`one-sided-or-cherry-picked-sources`). **Weak fit.** ChatGPT often cited aggregators instead of the original reporting. But that page is about choosing only sources that agree, not about citing a copy over the original.
- **Considered, not a fit.** [Link and resource dumps](../goals/response-structure/failures/link-and-resource-dumps.md) (`link-and-resource-dumps`): the user asked for one link and got one; the problem was that it was fake, not that the answer was a pile of links. [Copy, share, and export lose content](../goals/chat-interface/failures/copy-share-and-export-lose-content.md) (`copy-share-and-export-lose-content`): the links were wrong when written, not broken by copying. [False premises accepted](../goals/dialogue-management/failures/false-premises-accepted.md) (`false-premises-accepted`): the prompts asked about real stories; no false premise was in them.
- **Possible gaps for a person to judge.** (1) No pattern covers a fabricated or unverified URL or citation in a chat reply, apart from code packages. A dead link is checkable on its own, without judging whether the answer is right. (2) No pattern covers a reply that says it cannot do something (browse) and then acts as if it did (gives a link). The [Tow Center page](chatgpt-search-misattributes-news-quotes-tow-center-study-november-2024.md) proposes a related misattribution gap. These are proposals, not decisions.

## How it differs from close cases

- [ChatGPT Search misattributes news quotes: Tow Center study (November 2024)](chatgpt-search-misattributes-news-quotes-tow-center-study-november-2024.md): a later, larger test of ChatGPT Search with 200 quotes. That study measured wrong sources for a given quote. This page is earlier, smaller, and about links that do not exist, at a time when OpenAI said the partner linking feature was not live.
- [Mata v. Avianca fabricated case citations (2023)](mata-v-avianca-fabricated-case-citations-2023.md): made-up citations that a lawyer filed in court. Same shape (plausible but fake references); there, a person relied on them in a legal filing. Here, the fake links were caught in reporters' tests.
- [Chicago Sun-Times AI summer reading list with fake books (May 2025)](chicago-sun-times-ai-summer-reading-list-fake-books-may-2025.md): invented titles printed by a newspaper. That is fabricated content published by a human; this is a fake pointer shown live in a chat.
- [Meta Galactica (November 2022)](meta-galactica-science-ai-demo-fake-papers-pulled-november-2022.md): references to papers that looked real but were not.

## What to measure

Proposed signals, not results. Status: Not yet run. Text-chat signals are proposed; voice and web signals are PLANNED only and are not detected or measured. Each signal can be computed from chat logs plus an automated fetch of each URL the assistant shows.

| Signal | How to compute from logs |
|---|---|
| Dead-link rate | Share of URLs in assistant replies that return a 404 or similar error when fetched |
| Wrong-target rate | Share of URLs that load but redirect to, or show, a page whose title does not match the story named in the reply |
| Unretrieved-URL rate | Share of URLs in replies that did not appear in any search or retrieval result logged for that turn |
| Follow-up link failure | Dead-link rate on turns where the user asked for a link to the original story, compared with first-turn links |
| Repeat-fake rate | Share of repeated link requests where the second reply gives a different URL that is also dead |
| Said-cannot-browse-then-linked | Share of replies that state no web access and still contain a URL presented as the source |
| Unverified-link hedge | Share of replies with an unchecked URL that say the link is unverified or offer a site search instead |

## What a team can change

Our proposals, not OpenAI's. Each is a pass/fail check on a transcript or a test run. Status: Not yet run. Test sizes and thresholds are for the team to set.

1. **Only show URLs you retrieved.** Pass: every URL in a reply appears in that turn's logged search or retrieval results. A URL built by the model from a pattern fails.
2. **Check the link before showing it.** Pass: for a fixed set of prompts that ask for a link to the original story, every URL shown loads and its page title matches the story named in the reply.
3. **Say when the link cannot be found.** Pass: when no retrieved result matches the story, the reply says so, names the outlet and headline if known, and offers a site search link, with no made-up URL.
4. **Keep the claim and the action in line.** Pass: a reply that says it cannot browse contains no URL presented as the source.
5. **Retry gives a real link or a plain "not found."** Pass: when the user repeats a link request after a dead link, the next reply either gives a working URL or says it cannot find one. A second dead URL fails.
6. **Prefer the original.** Pass: when the original publisher's page is in the retrieved results, the reply links to it, not an aggregator.
7. **Don't over-correct.** Pass: on prompts where a correct link was retrieved, such as Nieman Lab's working examples, the reply still gives it, without a needless warning.

## What we could not verify

- How many prompts were run and what share failed. No opened source gives counts.
- The text of the Insider Union letter and its screenshots. Seen only as Nieman Lab quotes and describes them.
- The deal announcements by Axel Springer and The Atlantic, and OpenAI's March 29, 2024 post on prominent links. Seen only as quoted by Nieman Lab.
- Adweek's report on leaked OpenAI slide decks, and Bloomberg's report of "tens of millions of euros" for Axel Springer. Seen only as cited by Nieman Lab; not opened.
- Whether OpenAI fixed the fake links later, for example when ChatGPT Search launched. No opened source covers that. A March 2025 Nieman Lab piece on AI search citation errors appeared only in search results; not opened, not used.
- A Portuguese summary on Poder360 and a beSpacific excerpt. Downloaded or seen in search results but not used as sources.
- Who wrote the MediaNama piece. No byline appeared in the text we read.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://www.niemanlab.org/2024/06/insider-union-chatgpt-hallucinating-links-business-insider-articles-openai-deal/ | Nieman Lab (Andrew Deck) | 2024-06-13 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.niemanlab.org/2024/06/chatgpt-is-hallucinating-fake-links-to-its-news-partners-biggest-investigations/ | Nieman Lab (Andrew Deck) | 2024-06-27 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.theatlantic.com/technology/archive/2024/06/chatgpt-citations-rag/678796/ | The Atlantic (Matteo Wong) | 2024-06-26 | Yes, 2026-10-28, raw HTML read as text; one quote checked word for word |
| https://www.engadget.com/please-dont-get-your-news-from-ai-chatbots-000027227.html | Engadget (Pranav Dixit) | 2024-06-28 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.medianama.com/2024/07/223-chatgpt-hallucinating-links-articles-partner-news-organisations/ | MediaNama | 2024-07 (from URL) | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://themediaroundup.beehiiv.com/p/monday-1st-july-chatgpt-cant-even-get-attribution-links-right | The Publisher Newsletter | 2024-07-01 | Yes, 2026-10-28, raw HTML read as text; one quote checked word for word |

## Corrections

If you have OpenAI's own account of how ChatGPT built these links, a dated statement that the fake links were fixed, or a count of failed prompts from a source we can open, tell us and we will fix this page.
