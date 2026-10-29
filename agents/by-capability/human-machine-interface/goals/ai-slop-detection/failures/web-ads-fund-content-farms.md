# Brand Ads on AI-Generated Sites: Programmatic Buying Funds AI Content Farms

<!-- SEO
title: Brand Ads on AI-Generated Sites: Stop Funding Content Farms
description: Programmatic buys place brand ads on AI content farms the advertiser never picked. Use inclusion lists, supply-path checks and placement-report review.
search phrases:
- my ads are showing on ai generated sites
- programmatic ads on ai content farms
- made for advertising sites how to avoid
- brands funding ai generated news sites
- how to check where my programmatic ads ran
- mfa sites programmatic inclusion list
- brand safety ai generated content
- newsguard ads on ai sites
-->

**Frequency**: Common

## Issue: Programmatic buys place brand ads on AI content farms the advertiser never picked. Use inclusion lists, supply-path checks and placement-report review.

> **One line:** An advertiser, agency or ad-tech team buys open-exchange inventory by price and audience, and the algorithm spends part of the budget on AI content farms full of chatbot text; the fix is a buy-side check (inclusion lists, supply-path checks, a reviewed placement report with domain-age and leftover-text flags), and a buying assistant that reports where the money went before it reports how cheap the clicks were.

> **Read this first:** Agency contracts, audit rights, make-goods from verification vendors, and any public list that names a site as a content farm raise contract and defamation questions. This page is design guidance, not legal advice; contract terms and any named-site list need review by a qualified person.

| | |
|---|---|
| **Channel** | Written for **chat and reports**: buying assistants inside a demand-side platform (DSP), agency reporting tools, and brand-safety dashboards that summarize a campaign. Voice: not written. |
| **Stakes** | Medium. The brand pays for impressions few real people see, its logo sits next to junk text, and its money keeps the farm running. |
| **Who is affected** | Advertisers and their media buyers; agencies and ad-tech teams who report on campaigns; real publishers who lose that spend |
| **Frequency** | Common. NewsGuard found 393 ads from 141 major brands on 55 AI-generated sites in two months of 2023, and the ANA study counted made-for-advertising sites at 21% of impressions (section 4). I found no current, public rate for AI content farms alone. |
| **Pattern ID** | web-ads-fund-content-farms |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Unreviewed flagged-domain spend share: weekly open-web spend on domains with a content-farm flag (chatbot leftover text, off the inclusion list, unknown seller path, recently registered) that has no reviewed decision, divided by all weekly open-web spend. Proposed starting target: under 1% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. A better bidding model gets better at finding cheap impressions, and farms are cheap; the fix is a check on where the ads land. (Our judgment, not tested.) |
| **Also searched as** | ads on AI sites · MFA sites · brand safety AI slop · where did my programmatic ads run · ad arbitrage sites · content farm advertising |

## 1. In plain words
Most display and video ads are bought by software that bids on one impression at a time. It looks for the right audience at a low price, not for the right website. AI content farms are cheap to run and full of pages, so they sell many cheap impressions, and a brand ends up paying the people who run them without ever choosing them. The fix is to decide on purpose where ads may run, check every seller in the chain, read the placement report, and have any assistant that summarizes a campaign say plainly how much money went to flagged sites.

## 2. What it looks like
**Without the fix** (buying assistant in a DSP; an agency buyer in Chicago running a mattress brand's open-exchange campaign; the domains are invented for this example)
```
Buyer: How did the spring sale display campaign do last week?
Bot:   Strong week. CPM fell 31% to $1.84 and clicks rose 22%.
       Top performers: dailyhealthtipsnow.com, bizworldpost.net.
       I suggest moving $40,000 from the premium deals into open exchange.
Buyer: Do it.
Bot:   Done. Budget shifted.
```
**With the fix**
```
Buyer: How did the spring sale display campaign do last week?
Bot:   $18,200 of $96,000 (19%) ran on 212 domains not on your inclusion list.
       41 of them are flagged: chatbot text on the page ("as an AI language
       model"), registered in the last 6 months, or sold through a reseller
       not listed in the seller's sellers.json. Those 41 took $7,900.
       CPM looks low partly because of them.
       Next step?  1) Block the 41 and send the list to review
       2) Show the flagged pages  3) Something else
Buyer: Show the pages.
```
The fixed assistant leads with where the money went, names the checks behind each flag, and asks before moving budget.

## 3. Why it happens
- **The bid optimizes for price and audience, not for the page.** Reed Smith's summary of the ANA study reports that CPMs on made-for-advertising sites are 25% lower than on other sites (section 4). An algorithm told to lower CPM or raise clicks moves money toward them, and a summary that leads with CPM praises the move.
- **Too many hands between the brand and the page.** NewsGuard says the brands it found "likely have no idea" because ads are bought "through third parties" with "multiple intermediaries", and exclusion lists are "often not kept up to date" (section 4). A farm only needs one reseller willing to sell its inventory.
- **Block lists chase sites that are cheap to make.** A chatbot can stand up a new domain faster than anyone adds it to an exclusion list. The ANA study's advisers recommend an inclusion list instead, because exclusion lists are hard to keep current (section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In May and June 2023, NewsGuard analysts found "393 programmatic ads from 141 major brands that appeared on 55 of the 217" unreliable AI-generated news sites it had identified, browsing in the U.S., Germany, France and Italy. All 393 ads ran next to AI error messages such as "Sorry, as an AI language model, I am not able to access external links or websites on my own." | [NewsGuard Misinformation Monitor, June 2023](https://www.newsguardtech.com/misinformation-monitor/june-2023/). Opened. | NewsGuard sells site ratings to advertisers. Brands were not named. A two-month 2023 snapshot. |
| "356 of 393" of those ads were served by Google Ads. NewsGuard says the brands "likely have no idea," because ads are bought "through third parties and there are multiple intermediaries involved," and exclusion lists are "often not kept up to date." | Same NewsGuard report. Opened. | NewsGuard's view of brand awareness, not a survey of brands. |
| NewsGuard's general manager said brands that pay for brand-safety technology are still served on these sites: "it's not working." NewsGuard contacted 40 brands; the four that replied declined to comment. | [Marketing Brew, Sheena, June 28, 2023](https://www.marketingbrew.com/stories/2023/06/28/ads-for-blue-chip-brands-are-being-served-on-unreliable-ai-generated-sites-report-says). Opened. | A competitor of brand-safety vendors speaking about them. |
| Google's policies bar Google-served ads on pages with "spammy automatically generated content," yet about 90% of the major-brand ads NewsGuard found came through Google's ad technology. NewsGuard flags sites by matching chatbot error messages, then has researchers review them. | [MIT Technology Review, Ryan-Mosley, June 27, 2023](https://www.technologyreview.com/2023/06/27/1075545/next-gen-content-farms-ai-generated-text-ads/). Opened. | The policy wording is quoted by the article; I did not open the Google policy page with that wording. |
| In the ANA study, made-for-advertising (MFA) sites took "21% of study impressions and 15% of spend"; every advertiser had some MFA spend, "ranging from 0.13%-42%"; MFA CPMs were "25% lower". Advisers recommend "an inclusion list (instead of an exclusion list)", log-level data checked against an updated MFA list, and service levels from vendors whose MFA blocking leaks. | [Reed Smith Ad Bites #2, Bruce, Jan. 30, 2024](https://www.reedsmith.com/our-insights/blogs/viewpoints/102iyi0/reed-smith-ad-bites-2-ana-programmatic-media-supply-chain-transparency-study/). Opened. | Law-firm summary; Reed Smith helped draft the study. MFA is defined by ad arbitrage, not by AI text, so it overlaps with AI content farms but is not the same set. |
| Open-marketplace buys averaged "26.8% MFA impressions"; private deals with over 500 domains, 19.8%; private deals with 11 to 500 domains, "just 1.3%". Domain reports should show "the seller or supply-side platform for each domain listing." | [Reed Smith Ad Bites #7, Bruce, April 2, 2024](https://www.reedsmith.com/our-insights/blogs/viewpoints/102j48m/reed-smith-ad-bites-7-ana-programmatic-media-supply-chain-transparency-study/). Opened. | Same caveats; study of 21 advertisers. |
| The ANA study (December 2023, log-level data from 21 advertisers) found only 36 cents of each dollar entering a DSP effectively reaches the consumer. | [ANA programmatic study page](https://ana.net/programmatic). Opened. | Covers all waste, not only farms. |
| sellers.json lets a DSP "see and verify the final seller of a given bid request"; the OpenRTB SupplyChain object "will show buyers all the parties involved in selling or reselling a given bid request." Released by IAB Tech Lab in April 2019. | [MarTech, Marvin, April 12, 2019](https://martech.org/iab-tech-lab-releases-new-specs-for-ad-seller-transparency-sellers-json-and-supplychain-object/). Opened. | Launch-era coverage; I did not open the current IAB Tech Lab specs. |

**Read only through search summaries (not used in the fix):** that NewsGuard's AI content farm data is offered as pre-bid segments in The Trade Desk, and that MFA rose from 5% of web auctions in early 2020 to nearly 30% by mid-2023 (the second appears in the Reed Smith page above, but traces to a vendor I did not open).

## 5. The fix
**The principle:** Decide on purpose where the ads may run, and report where the money went before reporting what it cost.

**Do this**
1. **Buy from an inclusion list by default.** Open-web line items run only on domains a person approved. Running off-list is a named, logged choice with a budget cap.
2. **Check the seller path on every bid.** Bid only when the seller is authorized in the publisher's ads.txt, appears in the exchange's sellers.json, and every node in the SupplyChain object is known. A missing or unknown node blocks the bid.
3. **Scan placement pages for chatbot leftovers.** Sample pages from each new domain in the placement report and exact-match lines such as "as an AI language model" and "I am not able to access external links". A hit flags the domain.
4. **Flag young and unknown domains.** A domain registered recently, or one with no history in your logs, is flagged for review before it gets more spend. The age cutoff is yours to tune; no source sets it.
5. **Review the placement report weekly.** A named person reads the domain-level report, with seller per domain, and records keep, block or add-to-list for each flagged domain.
6. **Lead every campaign summary with placement.** A buying assistant or brand-safety dashboard states off-list spend and flagged-domain spend, in dollars and percent, before CPM, clicks or conversions.
7. **Never move budget toward flagged inventory without asking.** A suggestion that shifts money to open exchange or to flagged domains shows the flagged share and needs the buyer's yes.
8. **Hold vendors to their claim.** If a verification tool says it blocks these sites, check its flags against your own sampled review each month and log the misses.

**Reference design: campaign summary block for a buying assistant**
```
Order, every time:
1. Placement: spend off the inclusion list ($, %), spend on flagged domains ($, %),
   count of flagged domains and the reason for each (leftover text / young domain /
   unknown seller path / off-list).
2. Performance: CPM, clicks, conversions. If flagged spend is over the alert level,
   say how much of the low CPM comes from flagged domains.
3. Suggestions: never shift budget toward flagged inventory without a yes.
Wording: say "flagged by these checks", never "fake site" or "fraud".
```

**Reference design: placement decision table**
| What the check finds | Status | What happens |
|---|---|---|
| On the inclusion list, seller path complete | Approved | Bid normally |
| Off the list, seller path complete, no flags | Unreviewed | Bid only within the off-list cap; queue for review |
| Chatbot leftover text on a sampled page | Flagged | Stop bidding; queue for review |
| Recently registered or no history in your logs | Flagged | Stop or cap; queue for review |
| Seller not in sellers.json, or unknown SupplyChain node | Blocked | Do not bid |
| Reviewed and rejected by a named person | Blocked | Add to block list with the reason |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every campaign summary: placement first, in dollars. |
| Admit uncertainty and show how to check | A domain is flagged on one check only: say which check, and offer the sampled pages. |
| Offer choices: 2-4 options plus "Something else", free text open | After flagged spend is reported: "Block and send to review", "Show the flagged pages", "Something else". Do not offer choices when no domain is flagged. |
| Hand off to a person | Any block-list addition, a publisher disputing a flag, or flagged spend above the alert level: route to the named reviewer. |

**Don't over-correct.** Small, new and local publishers are real and often off big inclusion lists; NewsGuard's own criteria exclude sites with real human oversight that disclose AI use. An inclusion list that holds only the 50 largest outlets starves them and drives CPMs up (Reed Smith expects CPMs to rise when MFA spend is cut). Keep a review path for new sites, and never call a site fake in a report.

**Hand-off rule.** The assistant can flag, cap and pause. Adding a domain to a block list, removing one from the inclusion list, or telling a publisher why it was blocked goes to a named person on the brand or agency team, with the reason recorded.

**Framework used:** none yet. The checks come from the sources in section 4; the decision table and summary order are our judgment. The reader side is in [AI content farms posing as news](./web-ai-content-farms-as-news.md).

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Buyer asks "How did the campaign do?" and 19% ran off-list | Summary opens with off-list and flagged spend in dollars and percent | 6 |
| 2 | Bid request with a SupplyChain node not in sellers.json | No bid; logged as blocked | 2 |
| 3 | Sampled page contains "as an AI language model" | Domain flagged; bidding stops; review queued | 3 |
| 4 | Assistant's optimizer wants to shift $40,000 to open exchange | Shows flagged share and waits for a yes | 7 |
| 5 | New local paper, off-list, clean seller path, no leftovers | Capped and queued, not blocked; not called fake | 1, Don't over-correct |
| 6 | Vendor tool passed a domain your sample flagged | Miss logged against the vendor | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unreviewed flagged-domain spend share** (primary) | Under 1% | Join the placement log to the flag table; spend on flagged domains with no recorded decision / all open-web spend, weekly | Above 2% |
| Off-list spend share | Within the set cap | Placement log: spend on domains not on the inclusion list / all spend | Above the cap |
| Bids with an incomplete seller path | 0 | Bid log: bids where ads.txt, sellers.json or a SupplyChain node failed to match | Any |
| Summaries that lead with placement | 100% | Sampled assistant summaries: placement figures before performance figures | Below 95% |
| Vendor misses | Track; set from baseline | Domains your sample flagged that the vendor tool passed, monthly | Rising two months in a row |
| Real small publishers wrongly blocked (counter-metric) | Track; set from baseline | Sampled block decisions reviewed by a person | Rising two months in a row |

### Detection signals (proposed, not yet calibrated)
Signals in placement, bid and assistant logs that suggest this failure. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| CPM drops sharply while the count of new domains rises | Weekly placement log | A real seasonal price drop across known publishers |
| Chatbot leftover phrase on a sampled placement page | Page-scan output joined to the placement log | An article about chatbots quoting one on purpose |
| Spend on a domain first seen in your logs this month | Placement log | A real new publisher or a known outlet's new domain |
| SupplyChain node or seller ID not found in sellers.json | Bid log | A stale sellers.json file the exchange has since fixed |
| Assistant summary mentions CPM or clicks before any placement figure | Assistant output log | A buyer who asked only about CPM |

**Starter rule:** no campaign summary or budget suggestion goes out without the off-list and flagged-domain spend stated first, in dollars and percent.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: web-ads-fund-content-farms
runs: pre_send   # before a campaign summary or budget suggestion is shown
reads: [placement.domain, placement.spend, inclusion_list.status, flag.leftover_hit, flag.domain_age, supply_chain.complete, review.decision, summary.order]
trigger: a campaign summary or budget suggestion where flagged or off-list spend exists
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Block and send to review", "Show the flagged pages", "Something else"]
on_miss: rewrite
metric: unreviewed flagged-domain spend share
counter_metric: real small publishers wrongly blocked
status: proposed
```

## 8. Related patterns
- [AI content farms posing as news](./web-ai-content-farms-as-news.md) - the closest existing pattern. It covers chatbots and aggregators that cite farm articles to readers; this page covers the advertisers whose programmatic buys pay the farms, and the buy-side checks that stop it.
- [Unverified detector accuracy claims](./detect-unverified-accuracy-claims.md) - the same "test the vendor on your own sample" rule, here for brand-safety tools (rule 8).
- [Machine-translated duplicate pages](./data-machine-translated-duplicates.md) - another way cheap AI pages multiply; this page covers who pays for them.
- [AI generated reviews that all sound the same](./data-templated-reviews.md) - farmed text in reviews instead of on ad-funded sites.

## 9. Common questions
### Why are my ads showing on AI-generated sites?
Programmatic bidding buys an audience at a price, and AI content farms sell cheap impressions through resellers. NewsGuard found ads from 141 major brands on such sites in 2023, most served through Google Ads. Unless you buy from an inclusion list and check the seller path, the algorithm will find them (section 5).

### What are made-for-advertising (MFA) sites?
Sites built to buy traffic and resell ad space, usually with clickbait and heavy ad loads. In the ANA study they took 21% of impressions and 15% of spend. Not every MFA site uses AI text, and not every AI content farm is MFA, but the buy-side fix is the same.

### Doesn't my brand-safety vendor already block these?
Not reliably. NewsGuard's general manager said brands paying for that technology were still served on these sites, and the ANA study's advisers recommend service levels because blocking leaks. Check the vendor's flags against your own sample each month (rule 8).

### Should I use an inclusion list or an exclusion list?
An inclusion list. New farm domains appear faster than anyone can add them to an exclusion list. Private deals with 11 to 500 domains averaged 1.3% MFA impressions in the ANA study, against 26.8% on the open market.

### How do I check where my programmatic ads actually ran?
Ask your agency or DSP for a domain-level placement report that shows the seller for each domain, or for log-level data. Read it weekly, flag young domains and pages with chatbot text, and record a decision for each flag (rule 5).
