---
title: "xAI's Grok Share Links Show Up in Google and Other Search Engines, August 2025"
date: 2025-08-20
source: "https://www.forbes.com.au/news/innovation/xai-published-hundreds-of-thousands-of-grok-chatbot-conversations/"
description: "Grok's share button made public links that Google, Bing and DuckDuckGo indexed. Forbes reported over 370,000 such chats; users said they had no warning."
summary: "On August 20, 2025, Forbes (Iain Martin) reported that each time a Grok user clicked share, the unique link was also open to search engines, and that a Google search showed more than 370,000 indexed Grok conversations. Two users told Forbes they did not know shared chats would be findable on Google. Unlike ChatGPT's July 2025 case, no opened source describes any opt-in step. xAI did not respond to Forbes or TechCrunch. xAI's current FAQ says a share link posted publicly may be indexed. Status: Needs review."
categories:
  - Governance
patterns:
  - copy-share-and-export-lose-content
---

# xAI's Grok Share Links Show Up in Google and Other Search Engines, August 2025

**This page is a dated teardown of one public case, a chatbot share button whose links search engines could find, for teams that let users share a chat by link.** The product was xAI's Grok. The user was anyone who clicked "share" to send a chat to someone. The moment was the click: by the reports, nothing on screen said the page would also be open to search engines. Every fact below comes from a source we opened (listed at the end). We do not quote or link any indexed chat, and we repeat what outlets say about the chats only in general terms.

**Status: Needs review.** Eight pages (Forbes Australia's copy of the Forbes article, TechCrunch, Tom's Guide, Business Standard, ForkLog, heise online, Malwarebytes, Vice) and xAI's Consumer FAQs were downloaded as raw HTML on 2026-10-26 and read as text. Quotes were string-matched against those files. The Forbes US page returned 403 and was not read.

> **Read this first.** This is a summary of public reporting. It is not legal or privacy advice. We did not test Grok, then or now, and we did not open any indexed chat. We make no finding about anyone's intent. We have no statement from xAI or Elon Musk beyond a Grok account post that two outlets relay. **Last updated: 2026-10-26.**

**Why the slug says August 2025.** Forbes published on August 20, 2025 (TechCrunch's article citing it is dated 14:04 UTC that day; Forbes Australia's copy is dated 23:45 UTC on August 20, shown as August 21 in its own page text). ForkLog and Forbes say users on X had pointed out indexed Grok chats since January 2025, so the behavior was older; we date the page by when the failure became widely public, as the sibling teardowns do.

## What happened (as reported)

- **The share button.** Forbes (Iain Martin) says clicking "share" on a Grok chat creates a unique URL to send by email, text or other means, and that the URL is "also made available to search engines, like Google, Bing and DuckDuckGo." Forbes says this happened "without warning or a disclaimer to the user." TechCrunch (Rebecca Bellan, August 20, 2025) and Business Standard (Aashish Kumar Shrivastava, August 21, 2025) repeat the mechanism, citing Forbes.
- **The count.** Forbes says that on the day it published, a Google search showed more than 370,000 indexed Grok conversations. Tom's Guide (Amanda Caswell, August 20, 2025) gives "more than 300,000 Grok conversations," also citing Forbes. No opened source made its own count.
- **What was in them, in general terms.** Forbes says the pages ranged from business tasks such as writing posts to questions about medicine and psychology, and that some showed a user's name, personal details and at least one password. It says uploaded images, spreadsheets and some documents could also be reached through the shared page. Forbes and TechCrunch also say some shared chats showed Grok giving instructions that break xAI's own rules, such as for drugs and bombs. We do not repeat details.
- **Users who did not know.** Forbes quotes two people whose chats were indexed. A British journalist told Forbes he did not know a shared prompt would be findable on Google. Nathan Lambert, of the Allen Institute for AI, said chats he shared with his team were indexed "despite no warnings of it."
- **Google's position.** Forbes quotes Google spokesperson Ned Adriance: "Publishers of these pages have full control over whether they are indexed."
- **xAI's response.** Forbes says xAI "did not respond to a detailed request for comment." TechCrunch says xAI did not immediately respond and that it asked when xAI began indexing. heise online (Eva-Maria Weiß, August 22, 2025) says xAI did not comment to Forbes.
- **The earlier Grok post.** After OpenAI dropped ChatGPT's searchable-share option, TechCrunch and ForkLog say Grok's X account posted that Grok had "no such sharing feature," and Musk quote-posted it with "Grok ftw." ForkLog embeds the post, dated August 1, 2025. We did not open it on X.
- **Third parties using it.** Forbes says marketers on LinkedIn and BlackHatWorld discussed making Grok chats on purpose to show up in Google results. It quotes an SEO agency head: "Every shared chat on Grok is fully indexable and searchable on Google."
- **xAI's FAQ today.** xAI's Consumer FAQs page (dated May 12, 2025 at the top, fetched 2026-10-26) says a share link posted publicly "may be subject to indexing by a search engine (e.g., Google)." It says users can remove links at grok.com/share-links. We cannot tell when this note was added or whether it was there in August 2025.

## What the user saw

The user wants to show one chat to a colleague or a friend. They click "share," get a link and send it. By Forbes's account, nothing on the screen says the page is public to the whole web or open to search engines. Later, a stranger searching Google for a topic can land on that chat. Both users Forbes names say they did not know; the researcher learned it from Forbes and said he was surprised, given the recent ChatGPT case.

## Where in the flow it broke

Based on the outlets' descriptions, in order:

1. **The intent.** Share one chat with a known person (Forbes; Lambert shared with his team).
2. **The control.** One "share" click makes a unique link (Forbes, TechCrunch). No opened source describes a second step, a setting or a choice of audience.
3. **The disclosure.** None at the click, per Forbes ("without warning or a disclaimer") and heise ("what Grok did not communicate directly"). xAI's FAQ note exists today, off the share screen; its August 2025 state is unknown.
4. **The page.** The shared page was reachable by search engine crawlers (Forbes). No opened source explains the technical reason, for example whether the page told crawlers not to index it.
5. **The exposure.** Hundreds of thousands of pages in Google results, including uploads (Forbes).
6. **The way back.** The FAQ today offers a "Remove" link per share. Tom's Guide says deleting chats "won't make them completely disappear from searches." No opened source reports a fix by xAI.

**Contrast with ChatGPT.** In [ChatGPT's July 2025 case](chatgpt-shared-links-indexed-by-search-engines-july-2025.md), the user had to create a link and then tick a separate "discoverable" option; Forbes also says ChatGPT users "had opted" in. For Grok, the opened sources describe only the share click. We cannot say there was no option anywhere, only that no opened source mentions one.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| How many chats | Forbes: more than 370,000 via a Google search. Tom's Guide: more than 300,000, citing Forbes. Vice and ForkLog: more than 370,000; heise: around 370,000; all citing Forbes. No opened source gives a count for Bing or DuckDuckGo. |
| When indexing began | Forbes: unclear when the share feature was added; X users warned "since January." ForkLog embeds a January 20, 2025 post. TechCrunch asked xAI and got no answer. |
| Whether users were warned | Forbes and heise: no warning at the share step. Malwarebytes (Pieter Arntz, August 22, 2025): "sometimes" without users' knowledge. xAI's FAQ today: a public share "may be" indexed. |
| Who controls indexing | Google, via Forbes: the publisher of the pages. xAI: no statement found. |
| Why the pages were indexable | No opened source says. Search summaries mention missing noindex tags; we did not verify that. |
| What xAI did after | No opened source reports a change, a takedown or a statement. |

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Copy, share and export lose content](../goals/chat-interface/failures/copy-share-and-export-lose-content.md)** (`copy-share-and-export-lose-content`). Partial fit. That page is about what a share or export does to a reply, and its stakes line names a shared link that shows more than the sender meant. Here the link reached a far wider audience than the sender chose. Partial, because the page is mainly about formatting lost on copy and export, not audience. The sibling ChatGPT and Meta AI teardowns use the same partial match.
- **Considered and rejected.** [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`): Forbes says some chats held a name, personal details and a password, but not whose, and the failure is in publishing, not in the bot repeating or storing them. [Manipulated consent UI](../goals/visual/failures/manipulated-consent-ui.md) (`manipulated-consent-ui`): that page needs a consent prompt with tilted choices; the reports describe no prompt at all. [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md) (`sensitive-data-collected-in-chat`): no source says Grok asked for the data. [Hidden commands and features](../goals/onboarding-and-discoverability/failures/hidden-commands-and-features.md) (`hidden-commands-and-features`): about features users cannot find, not effects they are not told about. [Always-listening surprises](../goals/in-car-and-home-assistants/failures/always-listening-surprises.md) (`always-listening-surprises`): a similar shape, where nobody was told, but written for voice assistants in the home.
- **Possible gaps for a person to judge.** (1) No pattern covers a share control whose real audience (anyone, including search engines) is wider than what the user picked (one person), with no notice at the click. (2) No pattern covers a vendor's public statement about its own product, here "no such sharing feature," that its product's behavior contradicts. (3) No pattern covers shared chat pages being made on purpose by third parties to game search results. These are proposals, not decisions.

## Related incidents

- [ChatGPT shared chats appear in search results (July 2025)](chatgpt-shared-links-indexed-by-search-engines-july-2025.md): the same outcome weeks earlier, but behind an opt-in "discoverable" option, which OpenAI then removed.
- [Meta AI Discover feed shows private chats (June 2025)](meta-ai-discover-feed-shows-private-chats-june-2025.md): a share flow users did not seem to understand, posting to a public feed; Meta later added a warning.
- [OpenAI ChatGPT bug exposes other users' chat titles (March 2023)](openai-chatgpt-bug-exposes-other-users-chat-titles-march-2023.md): chats seen by people they were not meant for, there through a bug.
- [DeepSeek exposed database leaks chat history (January 2025)](deepseek-exposed-database-leaks-chat-history-and-api-keys-january-2025.md): chat content open to the public web, there through an unsecured database.

## What to measure

Proposed signals, not results. Status: Not yet run.

| Signal | How to compute |
|---|---|
| Audience stated at the click | Whether the share screen names, in plain words, who can open the link and whether search engines can find it (yes/no per screen and per app) |
| Crawler exposure of share pages | Share of a sample of your share URLs that a search crawler is allowed to index, from the page's robots meta tag, response headers and robots.txt |
| Indexed share pages | Count of your share URLs found by a `site:` search on each major search engine, checked on a set schedule |
| Uploads exposed by share | Share of share pages that also expose files the user uploaded, and whether the share screen says so |
| Time to unreachable | Hours from a user removing a share link to the page returning an error, and to it leaving search results |
| Comprehension | In a user test, share of participants who say correctly who can see a chat after they click share. Run it on your own users |

## What a team can change

Our proposals, not xAI's. Each is a pass/fail check on a screen, a page or a transcript. Status: Not yet run.

1. **Name the audience at the click.** Pass: the share screen says who can open the link and whether search engines can find it. Fail: no audience text, or only text in an FAQ.
2. **Link-only by default.** Pass: a new share page tells crawlers not to index it unless the user picks a separate, clearly labeled public option. Fail: share pages are indexable by default.
3. **Say what goes with it.** Pass: the screen lists what the link exposes, including uploaded files. Fail: uploads are exposed without mention.
4. **Show the way back.** Pass: the confirmation after sharing links to the page that removes shares. Fail: removal is reachable only from an FAQ.
5. **Make removal reach search.** Pass: a removed share returns an error and the team asks search engines to drop it. Fail: the page stays reachable or listed.
6. **Keep public claims true.** Pass: any public statement about how sharing works matches a test of the live share page. Fail: they differ.

## What we could not verify

- The Forbes US article (403). We used Forbes Australia's copy with the same byline; we assume, but did not check, that the text matches.
- Any indexed Grok chat, the share screen as it looked in August 2025, and the count of 370,000. We did not test Grok.
- Grok's August 1, 2025 post and Musk's reply on X. Seen only as relayed by TechCrunch and ForkLog.
- Whether xAI changed sharing or removed pages from search after the reports. No opened source says.
- When xAI's FAQ note on indexing was added.
- Seen only in search summaries, not used in the text: that share pages lacked noindex tags; reports in eWeek, Storyboard18, Cyber Daily, Mashable, TechRadar, Silicon UK, SEO Sherpa, all-ai.de, TechEconomy and a PDF copy of Forbes; a BBC report (none found); and any Fortune or Search Engine Journal coverage (none found).

## Sources

| URL | Publisher (author) | Date | Opened |
|---|---|---|---|
| https://www.forbes.com.au/news/innovation/xai-published-hundreds-of-thousands-of-grok-chatbot-conversations/ | Forbes Australia, copy of Forbes (Iain Martin) | 2025-08-20 (page data, UTC); page text says 2025-08-21 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://techcrunch.com/2025/08/20/thousands-of-grok-chats-are-now-searchable-on-google/ | TechCrunch (Rebecca Bellan) | 2025-08-20 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://www.tomsguide.com/ai/hundreds-of-thousands-of-grok-chatbot-conversations-are-showing-up-in-google-search-heres-what-happened | Tom's Guide (Amanda Caswell) | 2025-08-20 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://www.business-standard.com/technology/tech-news/search-engines-reportedly-indexed-users-chats-with-grok-what-it-means-125082100440_1.html | Business Standard (Aashish Kumar Shrivastava) | 2025-08-21 | Yes, 2026-10-26, raw HTML read as text |
| https://forklog.com/en/xais-grok-chatbot-conversations-exposed-on-google/ | ForkLog (no byline found) | 2025-08-21 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://heise.de/-10589123 | heise online (Eva-Maria Weiß) | 2025-08-22 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://www.malwarebytes.com/blog/news/2025/08/grok-chats-show-up-in-google-searches | Malwarebytes (Pieter Arntz) | 2025-08-22 | Yes, 2026-10-26, raw HTML read as text |
| https://www.vice.com/en/article/grok-chats-showing-up-google-search/ | Vice (Matt Jancer) | 2025-08-24 | Yes, 2026-10-26, raw HTML read as text |
| https://x.ai/legal/faq | xAI, Consumer FAQs | Page shows 2025-05-12; fetched 2026-10-26 | Yes, 2026-10-26, raw HTML read as text; quotes checked |
| https://www.forbes.com/sites/iainmartin/2025/08/20/elon-musks-xai-published-hundreds-of-thousands-of-grok-chatbot-conversations/ | Forbes (Iain Martin) | 2025-08-20 (from URL) | No, blocked (403) |

## Corrections

If you have the Forbes US text, an xAI statement, a screenshot of Grok's share screen from 2025, or a record of when sharing changed, tell us and we will fix this page.
