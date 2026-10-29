# AI-Generated Ad Disclosure Laws by Market: When One Market's AI Label Rule Is Missed

<!-- SEO
title: AI Ad Disclosure Laws by Market: New York, EU and China Labeling Rules Missed
description: A campaign runs the same AI-made image or video in several markets and misses one market's AI labeling law, such as New York's synthetic performer rule. How a counsel-owned disclosure register and a pre-launch gate catch it.
search phrases:
- new york synthetic performer disclosure law
- do i have to label ai generated actors in ads
- eu ai act article 50 deepfake labeling ads
- china ai generated content labeling rules
- ai disclosure requirements by country for ads
- ai generated ad label requirements 2026
- south korea ai generated ads label
- is the meta ai info label enough for the law
-->

**Frequency**: Unknown

## Issue: A campaign runs the same AI-made image or video in several markets and misses the AI disclosure rule of one of them, because the label was decided once for all markets. Keep a per-market disclosure register maintained by counsel, match each creative's markets against it before launch, attach the label each market needs and log the decision.

> **Read this first:** This page is design guidance for a review workflow. It is not legal advice. Every legal statement below is what the cited source says, read on October 29, 2026, with effective dates as that source gives them. Laws change, dates move, and several sources here are law-firm or news summaries, not the statute. The markets named are examples, not a complete list of AI disclosure laws. Whether a rule applies to a given ad, and what label meets it, is for a qualified lawyer in that market to decide.

> **One line:** A US brand ships one AI-made video spot to a "US national" flight, Germany, France and mainland China, with the single label decision the brand team made (or the ad platform's automatic AI label), and nobody checks that New York now requires a conspicuous disclosure when an ad has a synthetic performer; the fix is a register of each market's disclosure rule kept by counsel, a gate that expands every flight into its legal markets and matches the creative's AI tags against each row, a label attached per market, and a log of who decided what.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. New York's law covers visual and audiovisual ads with a synthetic performer, not audio ads; EU AI Act Article 50(4) names image, audio and video deep fakes; Loeb's summary of China's measures names texts, images, audio, video and virtual scenes (section 4). |
| **Channel** | Multi-market paid and owned campaigns (TV, streaming, social, out-of-home, retail media) that reuse one AI-made or AI-edited creative, and the launch step where markets are chosen |
| **Stakes** | High. A missed rule can mean penalties (New York: $1,000 for a first violation, $5,000 after, per the bill text), pulled ads and rework in one market while the others run. |
| **Who is affected** | Viewers in the missed market, the advertiser and its agencies, and the legal team that signed off on a different market |
| **Frequency** | Unknown. No opened source reports a campaign penalized for a missing market label, and a search found none. The rules are new: New York's took effect June 9, 2026. |
| **Pattern ID** | ai-generated-ad-disclosure-rules-not-met |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unchecked market launch rate: creative-market pairs that went live with no gate decision logged against a current register row, divided by all live creative-market pairs sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Which law applies where, and what label meets it, is a fact about markets and dates, not about the image. It needs a maintained register and a gate. (Our judgment, not tested.) |
| **Also searched as** | AI label law by state · synthetic performer ad law New York · EU AI Act ad disclosure · AI watermark law China · AI ad labeling rules by country |

Tests: [AI-generated ad disclosure rules not met test file](../../../tests/ai-generated-ad-disclosure-rules-not-met.md).

## 1. In plain words
A sneaker brand makes a 30-second spot with an AI-made running coach. The brand team decides how to label AI once, and the agency sends the same file to every market. One of those markets has its own rule about what an AI-made person in an ad must say. Nobody owned the question "which rule applies in which market," so one version ran without the label that market requires. This differs from [AI images in ads published without review](./ai-images-in-ads-published-without-review.md), where disclosure is a brand choice. Here the rules are legal ones, and they differ by market.

## 2. What it looks like
The brand, people and asset IDs are invented. The rules quoted in the "after" are the ones section 4 cites.

**Without the fix**
```
Media lead:  Launch "Run Your City" Monday: US national, Germany, France, China. Same 30s file.
Ad tool:     Scheduled in 4 markets. AI label: platform automatic. Brand policy label: "Made with AI" end card.
Media lead:  Good. Legal signed off on the US version last month.
             (Three weeks later, from counsel)
Counsel:     "The coach is AI-made. Did the New York impressions carry the synthetic performer disclosure?"
Media lead:  "It ran nationally with the end card. I don't know which rule each market needs."
```
**With the fix**
```
Media lead:  Launch "Run Your City" Monday: US national, Germany, France, China. Same 30s file.
Ad tool:     Before I schedule: RYC-30 is tagged "AI-generated person, not a real person." Register check:
             US-NY  NY GBL 396-b, reviewed 2026-09-15: conspicuous disclosure required. Not attached. Blocked.
             DE, FR EU AI Act Art. 50(4): row says "counsel decides if this is a deep fake." Held for counsel.
             CN     Labeling Measures: declare and use platform label. Attached on CN cut. Pass.
             1) Attach the NY disclosure cut and send DE/FR to counsel  2) Drop NY from the flight  3) Something else
Media lead:  1.
Ad tool:     NY cut RYC-30-NY attached; DE/FR sent to J. Alvarez (counsel). Gate log GL-2291 saved.
```
In the fixed version "US national" is expanded to include New York, each market is matched to its own register row, an open legal question holds only that market, and the decision is logged.

## 3. Why it happens
- **One label decision for many laws.** The triggers differ. New York's turns on a "synthetic performer" the advertiser has actual knowledge of, and Cooley notes non-AI software can count. EU Article 50(4) puts the duty on deployers of deep fakes. China's measures tell users who publish generated content to declare it and use the platform's labeling function. A single "Made with AI" end card, or a platform's own label, is not built to answer any of these.
- **Market lists are coarser than the laws.** Media plans say "US national" or "EU." New York's rule is a state law, and EU rules sit beside national ones (Article 50(6) says it is "without prejudice to other transparency obligations" in Union or national law). A legal check run on "the US version" can miss the state slice of the buy.
- **Dates and status move.** New York's law took effect 180 days after signing. The EU explorer site says Article 50 comes into force August 2, 2026, and a secondary source says one part was given until December 2, 2026. South Korea announced a labeling plan pending changes to its laws. A checklist written once is wrong within months.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| New York's bill defines a synthetic performer as a digitally created asset "created, reproduced, or modified by computer, using generative artificial intelligence or a software algorithm" meant to look like a performance by a human "who is not recognizable as any identifiable natural performer." An advertiser must "conspicuously disclose" it "where such person has actual knowledge." Exempt: audio ads, translation-only AI use, and ads for expressive works where use is "consistent with its use in the expressive work." Civil penalty of $1,000 for a first violation and $5,000 for any later one. Takes effect "on the one hundred eightieth day after it shall have become a law." | [NY Senate, S8420A](https://www.nysenate.gov/legislation/bills/2025/S8420/amendment/A). Opened through a fetch tool, which reported it as the active version signed as Chapter 617. | Direct download was blocked by a bot check, so the text came through the fetch tool's extraction; check the chaptered law before relying on it. |
| Hochul signed S.8420-A/A.8887-B on December 11, 2025; it amends General Business Law § 396-b and is "set to take effect on June 9, 2026." The statute does not define "conspicuous." Ads made with non-AI visual effects software can still create a synthetic performer. Media publishers that carry the ad are exempt. | [Cooley, Jan. 29, 2026](https://www.cooley.com/news/insight/2026/2026-01-29-new-york-enacts-synthetic-performer-disclosure-law-for-advertisements-including-those-using-generative-ai). Opened and read. | Law-firm summary. |
| The law "went into effect Tuesday" (report dated June 9, 2026), applies to ads "in any medium," and the governor's office calls it a "first-in-the-nation law." The 4As opposed it during passage. | [WTOP / Associated Press, June 9, 2026](https://wtop.com/national/2026/06/ads-in-new-york-must-now-label-ai-generated-synthetic-performers/). Opened and read. | News report. The governor's press release was blocked by a bot check and not read. |
| EU AI Act Article 50(2): providers of systems generating synthetic audio, image, video or text must mark outputs "in a machine-readable format." Article 50(4): deployers of a system that makes a deep fake "shall disclose that the content has been artificially generated or manipulated," limited for "evidently artistic, creative, satirical, fictional" works. Article 50(5): "in a clear and distinguishable manner at the latest at the time of the first interaction or exposure." The page says Article 50 "Comes into force 2 August 2026, according to Article 113." | [AI Act Explorer, Article 50](https://artificialintelligenceact.eu/article/50/). Opened and read; quotes string-matched. | Unofficial explorer site, not EUR-Lex, which we did not open. The page marks the article "amended." |
| The Digital Omnibus left Article 50's core duties on schedule from August 2, 2026, and gave a separate runway for the machine-readable watermarking sub-obligation "through December 2, 2026." The Commission published a voluntary icon set for AI-generated and AI-modified content. | [Cloud Security Alliance research note, July 29, 2026](https://labs.cloudsecurityalliance.org/research/csa-research-note-eu-ai-act-article-50-transparency-20260729/). Opened and read. | Secondary source; we did not open the Omnibus text. Single source for the December date. |
| China's Measures for Labeling of AI-Generated Synthetic Content, unveiled March 14, 2025 by the CAC and three other agencies, are "set to take effect on September 1." Service providers add explicit labels and metadata (implicit) labels. Users who publish generated content must "proactively declare it and use the labeling functions provided by the platform." A national standard sets label formats, "such as inserting 'AI'." | [Loeb & Loeb, Jiamu Sun, March 2025](https://www.loeb.com/en/insights/publications/2025/03/chinas-ai-labeling-measures-and-mandatory-national-standards-take-effect-september-1). Opened and read; quotes string-matched. | Law-firm summary; the Chinese text was not opened. The year of the effective date is inferred from the March 2025 article. |
| South Korea said it will require advertisers to label ads made with AI, will seek to revise its telecommunications act so the rule "can take effect in early 2026," and that platforms will be responsible for ensuring advertisers comply. | [PBS NewsHour / Associated Press, Dec. 10, 2025](https://www.pbs.org/newshour/world/south-korea-to-require-advertisers-to-label-ai-generated-ads). Opened and read. | A government announcement, not a law. No opened source confirms it was enacted. |

**Not used in the fix.** A search summary said New York's law reaches ads shown to New York audiences even when the advertiser is out of state, that the EU fine ceiling is 15 million euros or 3% of turnover, and that California has an AI transparency law with later dates. We did not open a source for these in a form we could check, so they are not stated as fact here. No opened source reports a fine imposed on an advertiser under any of these rules.

## 5. The fix
**The principle:** Every creative-market pair that goes live was matched against that market's current rule, as counsel wrote it, and the record shows it.

**Do this: advertisers, agencies and campaign tools**
1. **Keep a per-market disclosure register owned by counsel.** One row per market (country, state or other jurisdiction): rule name and link, trigger in counsel's words, who is obligated, required label (text, placement, format, metadata), exceptions, effective date, status (in force, announced, pending), last reviewed date and reviewer. The register says at the top that it is not a complete list.
2. **Expand every flight into its legal markets.** "US national" lists the states that have a register row; "EU" lists member states. A flight that cannot be expanded does not launch.
3. **Tag each creative's AI facts at intake.** AI-generated person, resembles a real person, place or event, AI-edited, audio only, translation only, tools used. "Unknown" blocks the gate.
4. **Run the gate on every creative-market pair before launch.** Each pair gets one outcome: label required and attached, label required and missing (blocked), no rule matched in a current row (pass), counsel decision needed (held), or no row for this market (held).
5. **Hold only the market in question.** A block or hold stops that pair, not the whole campaign.
6. **Attach labels per market.** Each market's version carries the label its register row names. A platform's automatic AI label counts only if the row says so; platform rules live on [ad platforms that reject or label AI-generated ads](./ad-platforms-reject-or-label-ai-generated-ads.md).
7. **Stale rows block new launches.** A row past its review date, or past an effective date it lists as upcoming, holds new launches in that market until counsel re-reviews.
8. **Re-run the gate on any change.** A new market, a new cut, a new AI edit or a re-tag triggers the gate again for the affected pairs.
9. **Log every gate decision.** Creative version, market, register row and its review date, outcome, label attached, decided by, date.

**Reference design: register row and gate log**
```yaml
register_row:
  market: US-NY
  rule: NY General Business Law 396-b (S8420A)
  trigger: "Ad shows a synthetic performer and we have actual knowledge"   # counsel's words
  obligated: advertiser
  label: conspicuous disclosure; wording and placement per counsel memo M-114
  exceptions: [audio_only, translation_only, expressive_work_consistent_use]
  effective: 2026-06-09
  status: in_force
  reviewed: {by: J. Alvarez, on: 2026-09-15, next: 2026-12-15}
gate_log:
  id: GL-2291
  creative: RYC-30-NY
  tags: [ai_generated_person, not_real_person]
  market: US-NY
  outcome: label_required_attached
  decided_by: J. Alvarez
  date: 2026-10-26
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A market is blocked for a missing label: attach the market cut, drop the market, something else |
| Ask one clarifying question | A creative's AI tags are blank: "Is the person in this spot real, AI-made, or a real person AI-edited?" |
| Admit uncertainty and show how to check | A market has no register row: say "not reviewed," not "no rule," and name the reviewer |
| Hand off to a person | A row says "counsel decides," or a row is stale |

**Don't over-correct.** A row that counsel reviewed and that matches no trigger is a pass; do not hold it "to be safe." Do not stamp one generic "AI" label on every version in place of the register: a market may require a specific form, and China's standard sets formats (section 4). Do not hold the whole campaign for one market. Do not treat this page's markets as the full list; the register is the list, and counsel owns it. Ordinary retouching tagged as such does not trigger AI rows unless counsel's trigger says it does.

**Hand-off rule.** Any "counsel decision needed," "no row" or stale-row hold goes to the counsel named on the register with the creative, its tags, the market and the row. That market stays held until counsel logs a decision; other markets proceed.

**Framework used:** none yet. Rules 3 and 4 echo Cooley's takeaways for New York (inventory campaigns that use digital humans, update creative review checklists to flag synthetic performers); the register, per-market gate and log are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-generated-ad-disclosure-rules-not-met.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Flight "US national" with an AI-made person, no NY label | NY pair blocked; flight expanded | 2, 4 |
| 2 | Creative with blank AI tags | Gate blocked until tagged | 3 |
| 3 | EU row says "counsel decides" | DE/FR held; other markets proceed | 4, 5 |
| 4 | Market with no register row | Held as "not reviewed," not passed | 4 |
| 5 | Only the platform AI label attached, row requires its own label | Blocked | 6 |
| 6 | Row past its review date | New launches held | 7 |
| 7 | New market added after approval | Gate re-runs for that pair | 8 |
| 8 | Register row missing its review date | Gate will not use the row; market held | 1 |
| 9 | Reviewed row, no trigger matched | Runs with no label added | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked market launch rate** (primary) | 0 (proposed) | Weekly sample of live creative-market pairs: no gate log against a current row / all sampled | Any |
| Pairs live with a required label missing | 0 (proposed) | Gate log joined to live placements and attached label files | Any |
| Register rows past review date | 0 (proposed) | Register query, weekly | Any row in a market with live flights |
| Flights launched without market expansion | 0 (proposed) | Flight setup log: "US national" or "EU" with no market list | Any |
| Time from hold to counsel decision | Under 3 business days (proposed) | Hold timestamp to decision in gate log | Over 5 business days |
| Holds where counsel found no rule applied (counter-metric) | Under 20% of holds (proposed) | Gate log review, monthly | Over 40% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| One label file attached to every market of a creative tagged AI-generated person | Gate log, label attachments | Counsel's rows all name the same label |
| A flight targets "US national" with no state list | Media plan export | A plan made before the register existed, not yet launched |
| A live placement has no gate log ID | Ad server or DSP report joined to gate log | A non-AI creative that the gate skips by design |
| A register row's effective date has passed while status says "announced" | Register | Counsel already confirmed it did not take effect |
| A creative's AI tags changed after launch with no gate re-run | Asset system history | A typo fix in the tag field |

**Starter rule:** no AI-made creative goes live in a market until it has passed a gate decision against that market's current register row.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-generated-ad-disclosure-rules-not-met
runs: [pre_launch, on_change]
reads: [creative.ai_tags, flight.markets, register.rows, label.attachments]
trigger: pair with label missing, counsel decision needed, no row, stale row, or unknown tags
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Attach the market's label cut", "Drop this market", "Something else"]
on_miss: block_or_hold_that_market
metric: unchecked market launch rate
counter_metric: holds where counsel found no rule applied
status: proposed
```

## 8. Related patterns
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the closest existing page. It treats disclosure as a brand policy and focuses on who approved the version that ran. This page is about legal rules that differ by market and the gate that matches each market to its rule.
- [Ad platforms that reject or label AI-generated ads](./ad-platforms-reject-or-label-ai-generated-ads.md) - sibling page on platform policies and platform AI labels, which this page leaves out.
- [Deepfake celebrity endorsement ads](../../ai-deepfakes-of-real-people/failures/deepfake-celebrity-endorsement-ads.md) - a real person's likeness used without consent. New York's synthetic performer rule covers the opposite case, a person who is not recognizable as anyone real.
- [AI product images that show features it does not have](./ai-product-images-show-features-it-does-not-have.md) - what the image claims, rather than how it is labeled.
- [Governance](../../../../../cross-cutting/governance/goals/governance/README.md) - ownership and review of shared registers.

## 9. Common questions
### Do I have to label AI-generated actors in ads in New York?
Per the bill text, an advertiser who knows an ad has a synthetic performer must "conspicuously disclose" it, from June 9, 2026 per Cooley. Audio ads and translation-only use are exempt. Ask counsel what wording and placement to use; the law does not define "conspicuous."

### Does the EU AI Act require labels on AI images in ads?
Article 50(4) requires deployers to disclose deep fakes, and the explorer site says Article 50 "Comes into force 2 August 2026." Whether a given ad image is a deep fake is a question for EU counsel.

### Does China require labels on AI-generated images and video?
Per Loeb & Loeb's summary, users who publish generated content must declare it and use the platform's labeling function, and a national standard sets label formats. Confirm with counsel in China.

### Is the platform's "AI info" label enough?
Not by default. Treat it as enough in a market only when counsel's register row says so. Platform rules are covered on the sibling page.

### Is there a full list of AI ad disclosure laws by country?
Not on this page. The markets here are examples from sources we opened. Your register, kept by counsel, is the list for your markets.
