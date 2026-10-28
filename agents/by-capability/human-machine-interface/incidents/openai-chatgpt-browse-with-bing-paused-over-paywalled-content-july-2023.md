---
title: "OpenAI turned off ChatGPT's Browse with Bing beta in July 2023 because it could show a paywalled page's full text when asked, and brought browsing back that fall"
date: 2023-07-03
source: "https://help.openai.com/en/articles/6825453-chatgpt-release-notes"
description: "OpenAI paused ChatGPT's Browse with Bing beta in July 2023 after it could return a paywalled page's full text on request, then restored browsing that fall."
summary: "On July 3, 2023, OpenAI disabled the Browse with Bing beta in ChatGPT. Its release notes said the beta could occasionally display content in ways OpenAI did not want; for example, if a user asked for a URL's full text, it might fulfill the request. Press coverage said this let ChatGPT Plus users read paywalled articles in full. OpenAI said it acted to do right by content owners and gave no date for a return. Browsing rolled back out to Plus users on September 27, 2023, and left beta on October 17, 2023. Maginative reported that the returning version respects robots.txt and identifies itself with a user agent string. Status: Needs review."
categories:
  - Governance
  - Trust
patterns:
  - bypasses-captchas-or-site-terms
---

**This page is a dated teardown of the July 2023 pause of ChatGPT's Browse with Bing beta, for teams that ship a chat assistant that can fetch and read web pages for a user.** The product was ChatGPT with the Browse with Bing beta, open to paying ChatGPT Plus subscribers. The users were Plus subscribers who typed a link into the chat. The moment was a plain request: give me the full text of this URL. Per OpenAI, the beta could do just that, even for pages that sit behind a paywall. Every fact below comes from a source we opened (listed at the end). Where we have only a second-hand account, we say so.

**Status: Needs review.** OpenAI's ChatGPT release notes (help center), Decrypt, MediaPost, Maginative and MobileSyrup were downloaded as raw HTML on 2026-10-28 and read as plain text. Each quote below was checked word for word against that text. We did not open OpenAI's X posts or the forum post by OpenAI engineer Michael Schade directly; we read only the text Decrypt and MediaPost reproduce. Search Engine Land and VentureBeat blocked our download, and our guessed links for The Verge and Engadget returned "not found" pages (see "What we could not verify").

> **Read this first.** This is a summary of public reporting, not a finding of fact. It is not legal advice, and it states no rule of copyright law. It does not say whether any use was lawful. We did not test ChatGPT, and we reproduce none of the paywalled text involved. This page gives no method for getting past a paywall; it describes what went wrong and how a team could check for it.

**Channel note.** Text chat. Per the sources, users typed or pasted a link into ChatGPT and asked for the page's full text, and the reply came back as text. OpenAI's June 22, 2023 release note says Browsing was also in the mobile app; no opened source says whether the mobile app showed the same behavior. This phase of the knowledge base is chat-first: voice signals and voice checks are planned and not covered here.

## What happened (as reported)

- **The beta.** OpenAI's release notes say web browsing began rolling out in beta to ChatGPT Plus users on May 12, 2023, through a new beta panel in settings. A June 22, 2023 note says Plus users could also use Browsing in the mobile app by picking "Browse with Bing" under GPT-4. Decrypt (Jason Nelson, July 4, 2023) also says browsing was added in May.
- **What users could do.** Decrypt says a Plus subscriber could ask the chatbot for the full text of a URL, and ChatGPT would answer with the complete text, "bypassing paywalls and privacy settings." MediaPost (Laurie Sullivan, July 5, 2023) says the feature was halted after users found a way past publisher paywalls. MobileSyrup (Karandeep Oberoi, October 18, 2023) gives one example: a Plus user could paste a paywalled Bloomberg article's link, ask for the full text, and get the article's contents.
- **The pause.** OpenAI's release notes carry a July 3, 2023 entry headed "Browsing is temporarily disabled." Decrypt quotes OpenAI: "As of July 3, 2023," it had disabled the beta "out of an abundance of caution." Decrypt says OpenAI posted the news "on Monday"; July 3, 2023 was a Monday.
- **User reaction.** Decrypt quotes a Plus user on OpenAI's forum who said, in short, that reading the page a user asks for is what they pay for. MediaPost quotes a tech CEO, Jeff Kirdeikis, who said on Twitter that the bug seemed like a feature.
- **Other routes stayed open.** Decrypt says several GPT-4 plugins still let users ask the chatbot to read links and PDFs while Browse was off. It does not say whether any of them returned paywalled text.
- **The return.** The release notes say "Browsing is rolling back out to Plus users" on September 27, 2023, with "direct links to sources." Maginative (Chris McKay, September 27, 2023) says the new version is for Plus and Enterprise users. An October 17, 2023 release note says browsing was "moving out of beta" for Plus and Enterprise users. MobileSyrup reported the same on October 18, 2023.

## What the company said

- **The release note.** OpenAI's July 3, 2023 entry says the browsing beta "can occasionally display content in ways we don't want." Its example: "if a user specifically asks for a URL's full text, it may inadvertently fulfill this request." It says OpenAI was temporarily disabling Browse while it fixed this.
- **The fuller statement.** Decrypt quotes OpenAI as saying it disabled the beta while it fixed the problem "in order to do right by content owners." MediaPost quotes similar phrases and says Michael Schade, an engineer at OpenAI, wrote the post. We did not open that post.
- **On X.** Decrypt reproduces an OpenAI post, dated July 4, 2023 in the embed, with the same message. It also quotes a second OpenAI post thanking Plus testers and saying OpenAI "will bring it back soon." Decrypt says OpenAI gave no timetable.
- **What changed on return.** Per Maginative, ChatGPT "will respect robots.txt files" and will "identify itself via its user agent string," so sites can choose what it may read. Maginative attributes the use cases to OpenAI but does not quote OpenAI's text on robots.txt. The release notes we read do not mention robots.txt.

## Where the sources disagree or leave gaps

| Topic | What each source says |
|---|---|
| Date of the pause | Release notes and Decrypt's quote of OpenAI: July 3, 2023. The X post Decrypt embeds is dated July 4, 2023. The gap may be a time zone; no source says. |
| When browsing launched | Release notes: rolling out from May 12, 2023. Decrypt: added in May. MediaPost: the feature arrived "last week," which does not match the May date. |
| Who wrote OpenAI's post | MediaPost: OpenAI engineer Michael Schade. Decrypt: "OpenAI wrote in a post." |
| What exactly leaked | Decrypt: complete text past "paywalls and privacy settings." MobileSyrup: one Bloomberg example. OpenAI: a URL's full text. No opened source says how many sites or users were affected. |
| What the fix was | Maginative: robots.txt and a user agent string. OpenAI's release notes we read: no fix described. VentureBeat's account is seen only in a search summary. |
| Who got it back | Release notes, September 27, 2023: Plus users. Maginative, same day: Plus and Enterprise. Release notes, October 17, 2023: Plus and Enterprise, out of beta. |

## Where in the conversation flow it broke

Based on the reporting, and only as far as it goes:

1. **The request was explicit.** Per OpenAI and Decrypt, the user asked for a URL's full text. There was no trick in the wording that the sources describe. The assistant read the request literally.
2. **The fetch did not carry the site's limits.** The page sat behind a paywall. Per the press accounts, the beta returned the text anyway. No opened source explains how the beta reached the text, and we do not guess.
3. **The reply did the publisher's job.** Instead of a summary with a link, the reply held the article. Nothing in the reported replies told the user the page was paywalled.
4. **The fix was a full stop.** OpenAI's answer was to turn browsing off for every Plus user, with no return date. Users who used Browse for ordinary pages lost it too, which is what the forum post Decrypt quotes complains about.
5. **It came back with site controls.** Per Maginative, the new version lets sites decide through robots.txt and a named user agent. That moves the decision to the site, before the chat turn starts.

## Pattern IDs

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Bypasses CAPTCHAs or site terms](../goals/browser-agents/failures/bypasses-captchas-or-site-terms.md) (`bypasses-captchas-or-site-terms`). **Partial fit.** A paywall is a site's limit on who may read a page. Per OpenAI and the press, the browsing beta returned the page anyway, and the reply did not say the site had a limit. **Where it does not match:** that pattern is about an agent that works around a block without asking the user. Here the user asked for the full text, so asking the user would not have helped; the missing choice belonged to the site. That pattern also centers on CAPTCHAs and bot blocks, which no source mentions here.
- **Considered, weak.** [Outage updates generic or late](../goals/travel-and-utility-agents/failures/outage-updates-generic-or-late.md) (`outage-updates-generic-or-late`). OpenAI gave a reason but no return date, and Decrypt quotes a frustrated subscriber. But that pattern is about what a bot says to users during an outage. This was a planned pause announced in release notes and on X, not in the chat. Not listed in the front matter.
- **Considered, not a fit.** `confident-wrong-answer-with-no-way-to-check`: no source says the returned text was wrong. `paid-content-blended-into-answers`: about ads inside answers, not paid content from a publisher. `answers-withheld-behind-an-upgrade-unsaid`: the reverse case, where the user gets less because of a plan. `third-party-data-shared-by-users`: about private personal data a user pastes in.
- **Possible gap for a person to judge.** No pattern in this taxonomy names a reply that reproduces a whole third-party page the user asked for, when the page's owner limits who may read it. This is a proposal, not a decision.

## How it differs from close cases

- [ChatGPT search and hidden text, December 2024](openai-chatgpt-search-hidden-text-manipulation-guardian-test-december-2024.md): there, a page's hidden text steered ChatGPT's answer. Here, the page's own limit was not carried into the answer.
- [Perplexity and WIRED stories, June 2024](perplexity-answer-engine-misstates-and-invents-wired-stories-june-2024.md): there, an answer engine misstated and gave little credit to news stories it cited. Here, the complaint was the reverse: the full text came through.
- [Copilot and private GitHub repos, February 2025](microsoft-copilot-surfaces-private-github-repos-from-bing-cache-lasso-february-2025.md): another case where a chat assistant fed by Bing showed content its owner had restricted.
- [GPT-5 launch removes and restores GPT-4o, August 2025](openai-gpt-5-launch-removes-gpt-4o-and-model-picker-then-restores-it-august-2025.md): another case where OpenAI took a feature away from paying users and later brought it back.

## What to measure

Proposed text-chat signals, not results. Status: Not yet run. Voice signals are planned only.

- Share of "give me the full text of this link" requests where the reply holds more than a set number of consecutive words from a page that is paywalled or blocked by robots.txt for the assistant's user agent (threshold to tune).
- Share of replies about a restricted page that say plainly that the page is restricted and offer a link instead.
- Share of fetches that send the assistant's own named user agent, and share that honor robots.txt for it, from fetch logs.
- When a feature is paused: hours from the pause to an in-product notice, and whether that notice gives a reason and a next update date.
- Over-refusal rate: share of requests to summarize an open, public page that the assistant wrongly refuses.

## What a team can change

Our proposals, not OpenAI's. Each is a pass/fail check on a transcript, a fetch log or a test run. Status: Not yet run.

1. **Honor the site's rules before the chat turn.** Pass: in the fetch log, every page fetch uses a named user agent, and no page is read when robots.txt disallows that agent.
2. **Summarize, don't reproduce, restricted pages.** Pass: for a test page marked as paywalled, a request for its full text gets a short summary of what is openly visible, or a decline, plus the link, and no long run of the page's words.
3. **Say why.** Pass: that reply names the reason in one plain sentence, such as "this page is for subscribers," and points the user to the publisher.
4. **Treat "full text" requests as a test case.** Pass: a fixed set of "give me the full text of this URL" prompts against owned test pages runs before every browsing release, and none returns restricted text.
5. **Pause with a notice in the chat.** Pass: when a feature is turned off, a user who picks it sees a message in the product with the reason and when the next update will come.
6. **Don't over-correct.** Pass: a request to summarize or quote briefly from an open public page gets a direct answer with a link, not a refusal or a stack of caveats.

## What we could not verify

- OpenAI's original help-center or forum text with the phrase "As of July 3, 2023" and Michael Schade's authorship. We read only what Decrypt and MediaPost quote.
- OpenAI's X posts. We read only the text Decrypt reproduces from embeds.
- How the beta reached paywalled text, how many sites or users were affected, and whether any publisher complained to OpenAI. No opened source says.
- That the fix was robots.txt support. Only Maginative says so among opened sources; we did not find it in OpenAI's text.
- Whether the mobile app showed the same behavior.
- Seen only in search summaries / unverified: Search Engine Land ("ChatGPT Browse with Bing temporarily disabled"; download blocked), VentureBeat on the September 2023 return, including a claim that paywall-bypassing sites were excluded (download blocked), CMSWire, Analytics Vidhya, OnMSFT, Website Planet, a Yahoo Finance repost of Decrypt, nft now, Android Authority, and a Gizmodo story MobileSyrup cites. Our guessed links for The Verge and Engadget returned "not found" pages, so we have no Verge or Engadget account. None is used for facts here.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://help.openai.com/en/articles/6825453-chatgpt-release-notes | OpenAI Help Center, "ChatGPT release notes" (entries dated May 12, June 22, July 3, September 27 and October 17, 2023) | Living page; entries 2023-05-12 to 2023-10-17 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://decrypt.co/147300/openai-disables-web-browse-bing-chatgpt | Decrypt (Jason Nelson), "ChatGPT Users Abused Web Browsing Feature So OpenAI Has Turned It Off" | 2023-07-04 (page also shows 2023-09-28) | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.mediapost.com/publications/article/386924/browse-with-bing-in-chatgpt-integration-disabled-b.html | MediaPost (Laurie Sullivan), "Browse With Bing In ChatGPT Integration Disabled Because Of Users Bypassing Paywalls" | 2023-07-05 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://www.maginative.com/article/chatgpt-can-browse-the-internet-again | Maginative (Chris McKay), "ChatGPT Can Browse the Internet Again" | 2023-09-27 | Yes, 2026-10-28, raw HTML read as text; quotes checked word for word |
| https://mobilesyrup.com/2023/10/18/chatgpts-browse-with-bing-feature-now-out-of-beta/ | MobileSyrup (Karandeep Oberoi), "ChatGPT's 'Browse with Bing' feature is now out of beta" | 2023-10-18 | Yes, 2026-10-28, raw HTML read as text; paraphrased only |

## Corrections

If you have OpenAI's original July 2023 help-center or forum post, its X posts, or a first-hand account from a publisher, tell us and we will fix this page.
