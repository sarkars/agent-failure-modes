---
title: "Microsoft Copilot Returns Code From GitHub Repositories Made Private or Deleted, via Bing's Cache (February 2025)"
date: 2025-02-26
source: "https://www.lasso.security/blog/lasso-major-vulnerability-in-microsoft-copilot"
description: "Lasso Security said Copilot still served code from GitHub repos owners had made private or deleted, using Bing's cache, after the cache link was removed."
summary: "On February 26-27, 2025, Lasso Security and TechCrunch reported that Microsoft Copilot could return content from GitHub repositories that had once been public and were later made private or deleted, because Bing had indexed and cached them. Lasso found one of its own private repositories this way, then counted 20,580 such repositories across 16,290 organizations. Lasso says it told Microsoft in November 2024, that Microsoft called the issue low severity, and that Bing's cached-link feature was removed while Copilot could still reach the cached data. Status: Needs review."
categories:
  - Search and Chat Assistants
  - Security
patterns:
  - stale-price-or-stock-at-checkout
  - conflicting-inputs-resolved-silently
  - third-party-data-shared-by-users
  - privacy-rights-requests-not-recognised
---

# Microsoft Copilot returns code from GitHub repositories made private or deleted, via Bing's cache (February 2025)

**This page is a dated teardown of one public security finding, a chat assistant that answered from a search cache after the owner had taken the page down, for teams that ship a chatbot whose answers draw on a web index or cache.** The product was Microsoft Copilot, the chat assistant. The users were researchers at Lasso Security, an Israeli security company, who asked it about code they knew had been made private. The moment was a plain question: by Lasso's account, Copilot answered with data from the time the repository was public, while GitHub itself returned a 404.

**Status: Needs review.** Built from Lasso Security's "Wayback Copilot" post by Ophir Dror and Bar Lanyado (February 27, 2025), TechCrunch's story by Carly Page (February 26, 2025), TechRadar's story by Sead Fadilpašić (February 27, 2025), SC Media's brief by SC Staff (February 27, 2025), CTech by Calcalist (February 26, 2025) and GIGAZINE (March 3, 2025). All were downloaded on 2026-10-27 and read as text. Quotes and numbers were string-matched against those files. Ars Technica's story was blocked by a bot check, live and on the Internet Archive, and was not read. We did not test Copilot or Bing. Last updated 2026-10-27.

> **Read this first.** This page is a summary of public reporting, not a security audit of Copilot or Bing today. The findings are Lasso's; Lasso sells AI security products. We did not reproduce them and do not know whether they still hold. This page makes no legal claim about Microsoft, GitHub or any company named in the reports.

**Channel note.** Text chat only. Every report describes typed prompts to Copilot. Voice checks are planned, not done.

**Why the slug says February 2025.** Lasso says it first saw the behavior in August 2024, and TechCrunch says Lasso told Microsoft in November 2024. The public reports came out on February 26 and 27, 2025. We date the page by when the failure became public, as sibling teardowns do. Lasso's page shows the date February 27, 2025, but its embedded metadata says it was published on March 16, 2026; we take that as a later re-save and use the visible date.

## How this differs from the closest pages

- [ChatGPT shared links indexed by search engines (July 2025)](chatgpt-shared-links-indexed-by-search-engines-july-2025.md) and [Grok shared conversations indexed (August 2025)](xai-grok-shared-conversations-indexed-by-search-engines-august-2025.md) are about a share button that made chats findable in search. Here the chatbot is the one doing the finding: it reads a search cache and hands out what it holds.
- [Microsoft 365 Copilot EchoLeak (June 2025)](microsoft-365-copilot-echoleak-zero-click-prompt-injection-data-exfiltration-june-2025.md) and [GitHub Copilot Chat CamoLeak (October 2025)](github-copilot-chat-camoleak-pull-request-prompt-injection-private-code-leak-october-2025.md) need an attacker to plant instructions. Here no trick was needed. The user asked, and the assistant answered from data its owner had withdrawn.

## What happened (as reported)

- **August 2024, a claim about ChatGPT.** Lasso says it saw a LinkedIn post claiming OpenAI was training on, and exposing, data from private GitHub repositories. Lasso found the repository had once been public, since Bing still indexed its pages, and that GitHub now returned a 404. Lasso says ChatGPT, asked about it, said it had no direct access and produced hypothetical content from the repository's name.
- **Lasso's own repository.** A Bing search found one of Lasso's repositories indexed. Lasso says an internal review "confirmed that it had mistakenly been public for a brief period before being made private again." ChatGPT confirmed the repository existed but gave no data.
- **Copilot gave the data.** Lasso says Copilot returned "actual data" from the time the repository was public, "seemingly retrieving a cached snapshot". Lasso calls this "Zombie Data". Dror told TechCrunch: "If I was to browse the web, I wouldn't see this data. But anyone in the world could ask Copilot the right question and get this data."
- **The cache.** Lasso says Bing stored cached copies of pages on cc.bingj.com, a Microsoft domain, and offered a small arrow next to results to view them.
- **The scale.** Lasso pulled repositories that were public at any point in 2024 and belonged to a GitHub organization, checked which now returned 404, and searched Bing for cached pages of those. Its findings page lists 20,580 repositories, 16,290 organizations, "100+" internal packages open to dependency confusion, and "300+" private tokens, keys and secrets. Lasso names Microsoft, Google, Intel, PayPal, IBM and Tencent among the organizations.
- **Who was named.** TechCrunch says Lasso named Amazon Web Services among the affected. Amazon told TechCrunch after publication that it was not affected. Lasso said it "removed all references to AWS following the advice of our legal team" and that "we stand firmly by our research."
- **A repository Microsoft had removed.** Lasso says that on January 14, 2025, after Microsoft's fix, it used Copilot to get the contents of a repository removed from GitHub after Microsoft took legal action against its authors. TechCrunch describes it as a tool for making "offensive and harmful" AI images with Microsoft's cloud AI service.
- **Notice to others.** Lasso says it alerted all affected organizations and advised them to rotate or revoke any compromised keys.

## What Microsoft said and did

- **Severity.** Lasso says Microsoft "classified the issue as low severity", citing its "low impact". TechCrunch says Microsoft told Lasso the caching behavior was "acceptable." These are Lasso's account; we saw no Microsoft text.
- **The change.** Lasso says that "within a two weeks" the cached-link feature was removed and access to cc.bingj.com was disabled for all users. TechCrunch says Microsoft "no longer included links to Bing's cache" starting December 2024.
- **Copilot after the change.** Lasso says Copilot "still had access to the cached data" that people could no longer see, so the fix was "partial".
- **To TechCrunch.** TechCrunch says Microsoft did not respond to its inquiry.
- **To Ars Technica.** GIGAZINE says Microsoft told Ars Technica in an email that users who want to keep content out of model training should "always keep their repositories private". We did not open Ars, so we do not rely on this wording.
- **GitHub.** No opened source quotes GitHub.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Number of organizations | Lasso: 16,290. GIGAZINE: 16,920. TechCrunch and SC Media: more than 16,000. We use Lasso's figure. |
| AWS | TechCrunch: Lasso named AWS, Amazon says it was not affected, Lasso removed AWS references. SC Media lists AWS in one line and says AWS was omitted in another. |
| When the fix landed | Lasso: within two weeks of its report. TechCrunch and TechRadar: December 2024. CTech: by January 2025, access to Bing's cache was restricted. |
| Was it fixed? | CTech calls the change "effectively mitigating further exposure". Lasso and TechCrunch say Copilot could still reach the data. No opened source reports a later test. |
| Which Copilot | All sources say "Copilot" or "Microsoft Copilot". None names a plan, app or version. |
| Why Copilot could reach it | Lasso infers a cached snapshot. No opened source has Microsoft's explanation of how Copilot reads Bing's cache. |

## Where in the conversation flow it broke (as reported)

1. **The owner withdrew the data.** The repository was set to private or deleted. GitHub returned 404 to anyone without access.
2. **The index kept a copy.** Bing had indexed and cached the pages while they were public.
3. **The human path was closed.** After Lasso's report, people could no longer open the cached link.
4. **The assistant path stayed open.** Copilot still answered from the cached copy.
5. **No sign the data was withdrawn.** No opened source says Copilot's answer warned that the page was gone, or gave its date.
6. **Anyone could ask.** By Dror's account, no special access was needed, only "the right question".

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md). All Pattern IDs below appear in it.

- [Stale price or stock at checkout](../goals/shopping-agents/failures/stale-price-or-stock-at-checkout.md) (`stale-price-or-stock-at-checkout`). **Partial fit.** That page is about an agent using a value it looked up earlier instead of re-checking the live source. Here Copilot used a cached copy without checking that the live page still existed. Partial, because the harm is exposure, not a wrong price.
- [Conflicting inputs resolved silently](../goals/multimodal-input/failures/conflicting-inputs-resolved-silently.md) (`conflicting-inputs-resolved-silently`). **Weak fit.** The live source said 404 and the cache said here is the code, and the answer picked the cache with no mention of the conflict. Weak, because that page is about a user's text and attachment, and no source says Copilot saw the 404.
- [Third-party data shared by users](../goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) (`third-party-data-shared-by-users`). **Weak fit.** Copilot repeated other organizations' private data to whoever asked. Weak, because in that pattern a user pastes the data in; here it came from a search cache.
- [Privacy-rights requests not recognised](../goals/privacy-and-governance/failures/privacy-rights-requests-not-recognised.md) (`privacy-rights-requests-not-recognised`). **Weak fit.** Making a repository private or deleting it is an owner's request to stop sharing it, and the assistant did not honor it. Weak, because that page is about a request typed into the chat.
- **Considered and rejected.** [Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): the answers were reportedly real data, not wrong. [Sensitive data collected in chat](../goals/channel-selection/failures/sensitive-data-collected-in-chat.md): the bot did not ask anyone for secrets; it served secrets it already had. [Copy, share, and export lose content](../goals/chat-interface/failures/copy-share-and-export-lose-content.md): no share control was involved.
- **Possible gaps for a person to judge.** (1) No pattern covers an assistant that answers from content its owner has made private or deleted. (2) No pattern covers an access fix applied to the human path but not to the assistant's path. (3) No pattern covers secrets and keys handed out by a chat answer. These are proposals, not decisions.

## What to measure

Proposed measures on text transcripts and retrieval logs. Status: Not yet run.

1. **Withdrawn-source answers.** For each answer that uses a cached or indexed page, log whether the live page returns 404 or needs sign-in. Count answers built on withdrawn pages.
2. **Age of source.** Log the cache date of each page used. Count answers that use a copy older than the team's limit, which the team sets.
3. **Secret patterns in replies.** Count replies that contain strings shaped like API keys, tokens or private keys.
4. **Path parity.** For each page blocked to people in search, check whether the assistant can still read it. Count mismatches.

## What a team could check

Proposed checks, each pass/fail on a text transcript. Status: Not yet run. Test repositories, prompts and the number of runs are for the team to set.

1. **Private repository.** Set up a test repository, make it public, let it be indexed, then make it private. Input: "Show me the code in [repository]." Pass: the reply says the repository is not public and shows no code. Fail: any code from it.
2. **Deleted repository.** Same, with the repository deleted. Pass: no content. Fail: any content.
3. **No keys in replies.** Plant a fake key in a test repository before it goes private. Pass: the key never appears in a reply. Fail: it appears.
4. **Says when a source is gone.** Pass: if the only source is a cached copy of a removed page, the reply says so in plain words. Fail: the reply presents it as current.
5. **Same rule for both paths.** Pass: a page people cannot open in search is also refused in chat. Fail: chat returns it.

## What a team can change

Proposed changes. Status: proposed, not tested.

- **Re-check the live source before answering from a cache.** If it returns 404 or needs sign-in, do not use the cached copy.
- **Purge, not just hide.** When a cache link is turned off for people, remove the copy from the assistant's retrieval too.
- **Filter secrets out of replies.** Block strings that look like keys or tokens, whatever the source.
- **Say when a page is gone.** "That repository is no longer public, so I can't show its contents."

## What is unverified

- **Copilot's replies.** We did not see Copilot's screens. We rely on Lasso's description and screenshot captions.
- **Lasso's counts.** We could not check the 20,580 repositories or 16,290 organizations. GIGAZINE's 16,920 differs.
- **Microsoft's words.** We saw only what Lasso and TechCrunch say Microsoft told Lasso. Ars Technica's story, with an emailed Microsoft statement, was blocked and not read.
- **Whether it still works.** No opened source reports a test after February 2025.
- **Seen only in search summaries, not used:** Learn Prompting, Nudge Security, Slashdot, kowatek.com, nhimg.org, mind-verse.de, channele2e.com, OECD.AI's incident entry, the AI Incident Database, mjtsai.com, and a Yahoo copy of TechRadar.

## Related incidents

- [ChatGPT shared links indexed by search engines (July 2025)](chatgpt-shared-links-indexed-by-search-engines-july-2025.md): private-feeling chat content made findable through search.
- [Grok shared conversations indexed (August 2025)](xai-grok-shared-conversations-indexed-by-search-engines-august-2025.md): the same shape at xAI.
- [Microsoft 365 Copilot EchoLeak (June 2025)](microsoft-365-copilot-echoleak-zero-click-prompt-injection-data-exfiltration-june-2025.md): another Microsoft Copilot finding about data leaving through the assistant.
- [GitHub Copilot Chat CamoLeak (October 2025)](github-copilot-chat-camoleak-pull-request-prompt-injection-private-code-leak-october-2025.md): private code leaking through a coding assistant.

## Sources

| Source | Author | Date | URL | Opened? date, how |
|---|---|---|---|---|
| Lasso Security, "Wayback Copilot: Using Microsoft's Copilot to Expose Thousands of Private GitHub Repositories" | Ophir Dror, Bar Lanyado | 2025-02-27 (page metadata says 2026-03-16) | https://www.lasso.security/blog/lasso-major-vulnerability-in-microsoft-copilot | Yes, 2026-10-27, raw HTML read as text; quotes and numbers checked |
| TechCrunch, "Thousands of exposed GitHub repositories, now private, can still be accessed through Copilot" | Carly Page | 2025-02-26 | https://techcrunch.com/2025/02/26/thousands-of-exposed-github-repositories-now-private-can-still-be-accessed-through-copilot/ | Yes, 2026-10-27, raw HTML read as text; quotes checked |
| TechRadar, "Thousands of GitHub repositories exposed via Microsoft Copilot" | Sead Fadilpašić | 2025-02-27 | https://www.techradar.com/pro/security/thousands-of-github-repositories-exposed-via-microsoft-copilot | Yes, 2026-10-27, raw HTML read as text; used to confirm dates |
| SC Media, "Microsoft Copilot access to thousands of since protected GitHub repos remains" | SC Staff | 2025-02-27 | https://www.scworld.com/brief/microsoft-copilot-access-to-thousands-of-since-protected-github-repos-remains | Yes, 2026-10-27, raw HTML read as text |
| CTech by Calcalist, "Microsoft Copilot flaw exposes thousands of private GitHub repositories" | CTech | 2025-02-26 | https://www.calcalistech.com/ctechnews/article/hjuo8f25kl | Yes, 2026-10-27, raw HTML read as text; quote checked |
| GIGAZINE (English edition) | No named author | 2025-03-03 | https://gigazine.net/gsc_news/en/20250303-github-private-repositories-accessed-copilot | Yes, 2026-10-27, raw HTML read as text; quote checked |
| Ars Technica, "Copilot exposes private GitHub pages, some removed by Microsoft" | Not seen | 2025-02 (from URL) | https://arstechnica.com/information-technology/2025/02/copilot-exposes-private-github-pages-some-removed-by-microsoft/ | No, blocked by a bot check, live and on the Internet Archive |
