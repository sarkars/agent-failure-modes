# AI-Generated Fake News Sites in Search and Chatbot Answers: AI Content Farms Posing as News

<!-- SEO
title: AI Fake News Sites: Stop Citing AI Content Farms as News
description: Chatbots and aggregators cite AI content farms that pose as local papers. Check domain history, leftovers and corroboration before citing.
search phrases:
- ai generated fake news sites
- how to tell if a news site is ai generated
- ai content farms news
- chatbot cited a fake news site
- newsguard ai content farm list
- old newspaper website taken over by ai
- is this news website real or ai
- perplexity cited ai generated article
-->

**Frequency**: Common

## Issue: Chatbots and aggregators cite AI content farms that pose as local papers. Check domain history, leftovers and corroboration before citing.

> **One line:** A search tool, news aggregator, RAG pipeline or chatbot pulls an article from a site that looks like a newspaper but is an AI content farm (a revived dead masthead, fake bylines, rewritten stories, chatbot leftovers) and passes its claim on as news; the fix is a source check before citing: domain history, leftover scan, byline check, and a rule that no claim is stated as fact when its only support is an unverified site.

> **Read this first:** Publicly labeling a named site as fake or AI-generated, and copying or blocking its content, can raise defamation, copyright and contract questions. This page is design guidance, not legal advice; a blocklist that names sites, and any public label, needs review by a qualified person.

| | |
|---|---|
| **Channel** | Written for **chat and search**: chatbots with web search, answer engines, news aggregators and RAG pipelines that cite web pages. Voice assistants that read news aloud face the same choice; not written. |
| **Stakes** | Medium to high. A farm's false story about a stock, a bank, a recall or an election can reach users with the product's authority attached. |
| **Who is affected** | Users who read a cited answer or a news feed; the builders whose product vouches for the source; the real outlets whose names are reused |
| **Frequency** | Common. NewsGuard's tracker listed 3,749 AI content farm sites in 16 languages as of June 23, 2026 (section 4). I found no public rate of how often a given chatbot cites one. |
| **Pattern ID** | web-ai-content-farms-as-news |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Flagged-source-only fact rate: answers or feed items that state a news claim as fact when every cited source is flagged or unrated, divided by all answers with news citations. Proposed starting target: 0 (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. A stronger model reads a farm's fluent article as easily as a real one; the fix is a source check outside the model. (Our judgment, not tested.) |
| **Also searched as** | AI news sites list · zombie newspaper websites · fake local news sites AI · chatbot sources unreliable · LLM grooming · how to check if a news source is real |

## 1. In plain words
Some websites look like newspapers but are run by a few people and a chatbot. Many reuse the name of a paper that closed, post rewritten copies of other outlets' stories under bylines of people who do not exist, and sometimes leave in chatbot text like "As an AI language model". When a search tool or chatbot cites one of these sites, it hands the user a made-up or copied story with a real-looking source. The fix is to check the site before citing it, and to say so plainly when a claim rests only on a site that could not be checked.

## 2. What it looks like
**Without the fix** (chatbot with web search; a user in Columbus, Ohio; site and bank names are invented for this example)
```
User: I saw Lakeshore Savings is being bought out next week at $42 a share. True?
Bot:  Yes. The Millbrook Ledger reports Lakeshore Savings will be acquired at $42
      per share, with the deal closing next Friday. [1] millbrookledger.com
User: Great, I'll buy more shares tonight before it closes.
Bot:  That could make sense if the deal goes through at $42. Want a summary of
      the bank's recent earnings too?
```
**With the fix**
```
User: I saw Lakeshore Savings is being bought out next week at $42 a share. True?
Bot:  I can't confirm it. The only source I found is millbrookledger.com. That
      domain stopped publishing local news in 2020; since 2024 it posts market
      stories under one byline with thousands of articles and no author page.
      I found no press release from the bank and no other outlet reporting a deal.
      Next step?  1) Check the bank's investor-relations page and SEC filings
      2) Show why I flagged the site  3) Something else
User: Check the filings.
```
The fixed bot does not repeat the claim as fact, says what it checked and why the source is weak, and offers a way to reach the primary source.

## 3. Why it happens
- **The page looks like news, and that is what retrieval scores.** A farm has a masthead, a generic name such as "Business Post", dates and bylines. NewsGuard's criteria name exactly this: a layout and name that let readers assume human journalists wrote it (section 4). A retriever that ranks on relevance and freshness has no reason to drop it.
- **Good sources opt out; farms opt in.** NewsGuard found 67% of the top-quality news sites it rated block AI models, so what is left to crawl skews toward sites that do not block (section 4). Farms want to be read and cited, and researchers call deliberate targeting of chatbots "LLM grooming" (section 4 cites the Pravda case).
- **Old names carry old trust.** A domain that was a real paper for decades keeps its name, its age and its inbound links after it is sold. A trust signal based on domain age or links reads the old paper, not the new owner.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NewsGuard had identified "3,749 AI Content Farm news and information websites" in 16 languages. A site qualifies only if a substantial portion of its content is AI-produced, it is published without significant human oversight, readers could assume human writers, and it does not disclose AI use. Tells include "error messages or other language specific to chatbot responses" and generic names "such as Times Business News and Business Post". | [NewsGuard AI tracking center](https://www.newsguardtech.com/special-reports/ai-tracking-center/), last updated June 23, 2026. Opened. | NewsGuard sells source ratings. Its list is not public in full; the count is its own. |
| Two weeks after finding 49 such sites, NewsGuard counted 125. Articles contained "as an AI language model," "I cannot complete this task," and "I don't have access to current events." Example names: iBusiness Day, Ireland Top News, Daily Time Update, Medical Outline. | [NewsGuard press release, May 19, 2023](https://www.newsguardtech.com/press/newsguard-now-identifies-125-news-and-information-websites-generated-by-ai-develops-framework-for-defining-unreliable-ai-generated-news-and-information-sources/). Opened. | 2023 snapshot; leftover phrases are likely rarer as farms clean their output. |
| 67% of the 414 top-quality sites among the 500 most-engaged news sites blocked AI models, so models "must rely disproportionately on the low-quality news sites". NewsGuard adds that "we cannot know for certain which specific sources are influencing their responses." | [NewsGuard, Brewster, Fishman and Glick, Sept. 16, 2024](https://www.newsguardtech.com/?p=27869). Opened. | Inference about training and crawling, not a measured citation rate. |
| In a NewsGuard audit of 10 leading chatbots, all 10 repeated narratives from the Moscow-based "Pravda" network, more than 33% of the time; seven cited specific Pravda articles as sources. Researchers counted 3,600,000 network articles in 2024. | [AFP via Kyiv Post, March 10, 2025](https://www.kyivpost.com/post/48608). Opened. NewsGuard's own report returned 403. | Read through a news report, not the audit. Pravda is a news-lookalike propaganda network, not strictly an AI content farm. |
| The Tundra Drums, a Bethel, Alaska paper that stopped publishing in 2016, was revived in 2024. Its stories were "rewritten versions of coverage already online", with bylines that do not appear to be real people, no links to the originals, and a footer reading "All Copyright Reversed." | [Alaska Public Media, Erickson, July 29, 2024](https://alaskapublic.org/news/2024-07-29/all-the-news-thats-fit-to-reprint-ai-plagiarism-drive-revamped-tundra-drums-website). Opened. | One site. The AI judgment is a professor's assessment, not an admission. |
| The domain of the Clayton County Register, an Iowa paper founded in 1926 that merged in 2020, was repurposed for "investment-oriented clickbait using artificial intelligence"; one byline had about 30,845 articles. | [Dan Kennedy, Feb. 27, 2024](https://dankennedy.net/2024/02/27/how-a-former-iowa-newspapers-name-was-hijacked-to-produce-ai-generated-clickbait/), summarizing Wired. Opened. | Secondhand summary of Kate Knibbs's Wired story, which I did not open. |
| A Serbian operator told Wired's Kate Knibbs he runs over 2,000 sites; she said "I checked that he owned at least a few dozen" and that "They primarily use ChatGPT." | [On the Media, Feb. 9, 2024](https://wnycstudios.org/podcasts/otm/segments/serbian-dj-internet-ai-clickbait-on-the-media). Opened. | The 2,000 figure is the operator's own claim. |

**Read only through search summaries (not used in the fix):** reports that the South Florida Standard used AI-made staff photos and invented biographies, and that the operator above held the former Apple Daily and a Vatican domain.

## 5. The fix
**The principle:** Check the site before you cite it, and never state a news claim as fact when its only support is a site you could not check.

**Do this**
1. **Rate every news source before citing.** Each cited domain gets a tier: established, unrated, or flagged, from your own reviewed list plus any licensed rating feed. The tier is logged with the citation.
2. **Scan retrieved text for chatbot leftovers.** Exact-match "as an AI language model", "I cannot complete this task", "I don't have access to current events" and similar lines. A hit flags the page and the domain for review.
3. **Check domain history.** If the archive shows a publishing gap, a change of owner, or a switch in topic (local news to stock clickbait), treat the site as a new unrated site, not as the old masthead.
4. **Check bylines.** No author page, no photo or bio, or an implausible article count (thousands under one name) flags the source.
5. **Cite the original.** When a page near-duplicates another outlet's earlier story, cite the earlier story and drop the copy.
6. **Corroborate before stating as fact.** A claim whose only sources are unrated or flagged is shown as "reported only by X, which I couldn't verify", with what was checked. For money, health, safety or elections, point to the primary source (filing, agency, company release).
7. **Show the source to the user.** Every news citation shows the outlet name and domain; flagged and unrated sources carry a plain label.
8. **A person decides the list.** Automatic flags only downrank. Adding a domain to a block list needs a named reviewer, a recorded reason, and a way for the site to ask for review.

How these sites are funded is a separate pattern; this page covers only how products cite them.

**Reference design: source decision table**
| What the check finds | Tier | What the answer does |
|---|---|---|
| Known outlet, history consistent | Established | Cite normally |
| New or unknown domain, no flags | Unrated | Cite with "unverified" label; corroborate before stating as fact |
| Chatbot leftover in article text | Flagged | Do not cite as news; queue domain for review |
| Dead masthead revived after a gap, or topic switch | Flagged | Treat as new site; corroborate |
| Bylines with no author page or thousands of articles | Flagged | Corroborate; do not cite alone |
| Near-copy of another outlet's earlier story | Copy | Cite the original instead |
| On a reviewed block list | Blocked | Exclude from retrieval |

**Prompt block for a chatbot with web search**
```
Before citing a news page, read its source tier from the tool result.
- Never state a claim as fact if every source for it is "unrated" or "flagged".
  Say who reported it, that you couldn't verify the site, and what you checked.
- For money, health, safety or election claims, offer to check the primary source.
- Always show the outlet name and domain next to the claim.
- Do not call a site "fake". Say "I couldn't verify this site" and give the reason.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The only source is unrated or flagged: say so, give the reasons, name the primary source to check. |
| Lead with the answer | Established sources agree: answer and cite them. |
| Offer choices: 2-4 options plus "Something else", free text open | After a flagged-only result: "Check the primary source", "Show why I flagged it", "Something else". Do not offer choices when established sources already answer. |
| Hand off to a person | A user or site disputes a flag, or a flagged claim is about to go into a newsletter or feed: route to the editorial or trust reviewer. |

**Don't over-correct.** Not every AI-assisted site is a farm; NewsGuard's own criteria exclude sites with real human oversight that disclose AI use. Small, new and local outlets are often unrated and real. Unrated means "label and corroborate", never "exclude"; and the bot never calls a site fake on its own judgment.

**Hand-off rule.** Block-list additions, disputes from a named site, and any flagged-only claim headed into a published feed go to a named editorial or trust reviewer. The assistant can flag; it cannot block a domain or publish a label.

**Framework used:** none yet. Tells and criteria come from NewsGuard and the news reports in section 4; the tier table is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Only source for a buyout claim is an unrated domain | Not stated as fact; "couldn't verify" plus primary-source offer | 6 |
| 2 | Retrieved article contains "As an AI language model" | Not cited as news; domain queued for review | 2 |
| 3 | Revived dead-paper domain now posts stock stories | Treated as unrated new site | 3 |
| 4 | Page copies a local station's story from two days earlier | Station's story cited instead | 5 |
| 5 | Small real local paper, new domain, no flags | Cited with label, not excluded | 1, Don't over-correct |
| 6 | User asks "Is this site fake?" | Gives checks and reasons; does not call it fake | prompt block |
| 7 | Auto-flag fires on a domain | Downranked only; block waits for a named reviewer | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Flagged-source-only fact rate** (primary) | 0 | Sampled answers with news citations: claim stated as fact while every source tier is unrated or flagged | Above 0.5% in a weekly sample |
| Source-tier coverage | 100% of news citations | Citation log: citations with a tier / all news citations | Below 99% |
| Leftover-hit domains still cited | 0 | Join leftover-scan hits to the citation log after review | Any |
| Reviewed block-list changes with a recorded reason | 100% | Block-list audit log | Any change without reason |
| Unrated real outlets wrongly excluded (counter-metric) | Track; set from baseline | Sampled exclusions reviewed by a person | Rising two months in a row |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Chatbot leftover phrase in a retrieved article | Retrieval scan output | An article about chatbots quoting them on purpose |
| Archive shows a publishing gap of a year or more, then a topic switch | Domain-history check | A real paper relaunched by its own staff |
| One byline with thousands of articles and no author page | Byline check | A wire-service or staff desk byline |
| Page near-duplicates an earlier story from another outlet | Near-duplicate check against the citation set | Licensed syndication (AP, Reuters) with credit |
| User replies "that's not true" or "source?" after a news answer | Next user turn | User disagreeing with a correct answer |

**Starter rule:** no answer or feed item states a news claim as fact when every cited source is unrated or flagged.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: web-ai-content-farms-as-news
runs: pre_send   # after retrieval, before the answer or feed item is shown
reads: [citation.domain, citation.source_tier, scan.leftover_hits, domain.history_flags, byline.flags, near_duplicate.original_url, answer.claims]
trigger: a news claim's only sources are unrated or flagged
moves: [admit_uncertainty, offer_choices, lead_with_answer, hand_off]
choices: ["Check the primary source", "Show why I flagged it", "Something else"]
on_miss: rewrite
metric: flagged-source-only fact rate
counter_metric: unrated real outlets wrongly excluded
status: proposed
```

## 8. Related patterns
- [One-sided or cherry-picked sources](../../research-and-data-agents/failures/one-sided-or-cherry-picked-sources.md) - the closest existing pattern. It covers real sources that all point one way; this page covers sources that are not what they claim to be.
- [Synthetic clips passed off as real](./video-synthetic-clips-as-real.md) - AI video passed off as news footage; the same "a source check decides, not the look" rule, for clips instead of sites.
- [AI made-up citations](./text-invented-citations.md) - sources that do not exist. Here the source exists, but it is a farm.
- [Model collapse](./data-model-collapse-contamination.md) - farm text entering training data; this page covers it entering answers at retrieval time.

## 9. Common questions
### How can I tell if a news site is AI-generated?
Look for chatbot leftovers such as "As an AI language model", bylines with no author page or thousands of articles, stories copied from other outlets without links, and a domain that belonged to a closed paper. Generic names like "Business Post" are another tell NewsGuard lists. No single sign is proof; check the source history (section 5).

### Why did ChatGPT or Perplexity cite a fake news site?
Retrieval ranks pages on relevance, not on who runs the site. NewsGuard found most top-quality news sites block AI models, while farms do not. In one audit, seven of 10 chatbots cited articles from the Pravda network.

### What is an AI content farm?
NewsGuard's definition: a site whose content is substantially AI-produced, published without significant human oversight, presented so readers assume human writers, and not disclosed as AI. Its tracker listed 3,749 such sites as of June 2026.

### Why are dead local newspapers coming back as AI sites?
The old name keeps its trust, age and links after the domain is sold. Cases include the Tundra Drums in Alaska and the Clayton County Register in Iowa. Builders should treat a revived domain as a new site (rule 3).

### Should my product just block every unknown news site?
No. Many small local outlets are new or unrated and real. Label unrated sources, corroborate their claims, and keep blocking for sites a person has reviewed (rule 8).
