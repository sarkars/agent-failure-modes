# Ad Platforms That Reject or Label AI-Generated Ads: Meeting Google, Meta and TikTok AI Rules Before Launch

<!-- SEO
title: Ad Platforms That Reject or Label AI-Generated Ads: Google, Meta and TikTok AI Disclosure Rules
description: An AI-made ad goes live without the AI disclosure an ad platform asks for, or is rejected for it, because nobody checked each platform's own rule before launch. How a per-platform pre-launch check, the right disclosure setting and a rejection path prevent it.
search phrases:
- tiktok ads ai generated content toggle
- does tiktok require ai disclosure for ads
- meta political ads ai disclosure
- google ads altered or synthetic content checkbox
- ad rejected for ai generated content
- meta ai info label on ads
- do i have to label ai ads on facebook
- tiktok advertiser labeled as ai-generated
-->

**Frequency**: Occasional

## Issue: An AI-made or AI-edited ad goes live without the AI disclosure an ad platform asks for, or gets rejected or labeled by the platform, because the team checked the image but not each platform's own AI-creative rule. Before launch, run a per-platform check: match the creative's AI tags against each platform's current rule, set that platform's disclosure toggle or checkbox, re-check after every duplicate, and route any rejection to a named owner.

> **Read this first:** This page describes ad platform policies as the opened platform pages state them, read on October 29, 2026. Platform rules change often, and some pages below are news reports or archived copies, not the live policy. This is not legal advice, and a platform rule is not a law. Government disclosure laws are on the sibling page [AI-generated ad disclosure rules not met](./ai-generated-ad-disclosure-rules-not-met.md). Whether a given ad falls under a platform rule needs review by a qualified person before anyone relies on it.

> **One line:** A brand duplicates last quarter's TikTok campaign for a new AI-made video, and the duplicate quietly resets the "This ad contains AI-generated content" toggle, while the team assumes Meta and Google need the same label everywhere or none anywhere; the fix is a per-platform check before launch that reads each platform's current rule, sets the exact disclosure each one asks for, re-checks after every duplicate or creative swap, and sends any rejection to a named owner with the platform's stated reason.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Google's rule covers image, video and audio in election ads; Meta's covers photorealistic image, video and realistic audio in political and social issue ads; TikTok's covers image, video or audio that is completely AI-generated or significantly modified by AI (section 4). |
| **Channel** | Paid ads set up in Google Ads, Meta Ads Manager and TikTok Ads Manager, and the launch, duplicate and creative-swap steps inside them |
| **Stakes** | Medium to high. Per the opened sources, Meta rejects political or social issue ads that fail to disclose and may penalize repeat offenders; Google can suspend accounts after a warning; a missing label is also the story a reporter writes (section 4). |
| **Who is affected** | Viewers who cannot tell what is synthetic, the advertiser and its agency, and the campaign that is rejected or pulled mid-flight |
| **Frequency** | Occasional, by our reading. The Verge found Samsung TikTok ads with no AI disclosure in March 2026. No opened source gives a rejection rate. |
| **Pattern ID** | ad-platforms-reject-or-label-ai-generated-ads |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unchecked platform launch rate: live ads with AI-made or AI-edited creative and no logged per-platform check (rule version read, disclosure setting chosen, who decided) for that exact ad, divided by all live AI-creative ads sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Which platform asks for which disclosure, and whether a duplicate reset the toggle, are facts about platform settings and policy dates, not about the image. (Our judgment, not tested.) |
| **Also searched as** | TikTok AIGC label ads · Meta AI disclosure political ads · Google synthetic content election ads · AI info label Facebook ad · ad disapproved AI content |

Tests: [Ad platforms that reject or label AI-generated ads test file](../../../tests/ad-platforms-reject-or-label-ai-generated-ads.md).

## 1. In plain words
Each ad platform has its own AI rule, and they do not match. Google asks election advertisers to tick a box. Meta asks political and social issue advertisers to disclose realistic AI people and events, and puts its own "AI info" label on ads made with its tools. TikTok asks every regular ad with completely AI-generated or significantly AI-modified content to switch on a toggle. A team that treats "AI label" as one decision misses the platform that needed it, or labels where nothing was asked. And the setting can vanish: TikTok says duplicating a campaign resets the toggle.

## 2. What it looks like
The brand, people and IDs below are invented. The platform settings are the ones the opened pages describe (section 4).

**Without the fix**
```
Media buyer: Launch the fall latte spot on TikTok, Instagram and YouTube. Duplicate the August campaigns.
Ad tool:     Duplicated 3 campaigns. New video LC-207 attached. Ready to publish.
Media buyer: Publish all.
             (The video's barista is AI-generated. The August TikTok ad had the AI toggle on;
              the duplicate did not.)
Reporter:    "Lakeshore Coffee's TikTok ad shows no AI disclosure. Its YouTube version says AI was used."
Brand team:  "We labeled it." (Nobody checked the TikTok duplicate.)
```
**With the fix**
```
Media buyer: Launch the fall latte spot on TikTok, Instagram and YouTube. Duplicate the August campaigns.
Ad tool:     LC-207 is tagged "AI-generated: realistic person." Platform check, rules read Oct 29:
             TikTok: regular ad, fully AI-generated. The duplicate reset the AI toggle. Turn it on?
             Meta: commercial ad, not social issue. No self-disclosure field applies; an AI info label may appear.
             Google: not an election ad. The synthetic content checkbox does not apply.
             1) Turn TikTok toggle on and publish  2) Hold for review  3) Something else
Media buyer: 1.
Ad tool:     TikTok toggle on. Check logged for all 3 ads, owner R. Patel. Published.
```
In the fixed version the tool reads each platform's rule for this creative, catches the reset toggle, does not invent a label where none is asked, and logs who decided.

## 3. Why it happens
- **Three platforms, three different triggers.** Google's rule turns on election ads, Meta's self-disclosure on political and social issue ads with realistic people or events, and TikTok's on any regular ad with completely AI-generated or significantly AI-modified content. A single "do we label AI?" answer cannot fit all three.
- **The disclosure is a setting that copying does not keep.** TikTok's page says campaign duplication resets the AI toggle, "even if you reuse an ad that you previously used this toggle for." Teams that duplicate last quarter's campaign assume its settings came along.
- **Platform labels and advertiser disclosures get confused.** Meta labels ads made with its own generative AI tools and says it is starting to detect third-party AI, so a team may wait for the platform to label. But Meta's political ad rule, Google's checkbox and TikTok's toggle are the advertiser's job.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google: "Advertisers must disclose all election ads that contain synthetic or digitally altered content by selecting the checkbox in the 'Altered or synthetic content' section in their campaign settings." For mobile Feeds and Shorts and in-stream, Google generates the in-ad disclosure; for other formats the advertiser provides "a prominent disclosure." Resizing, cropping, color or brightening corrections and similar edits are out of scope. "A warning will be issued at least 7 days prior to any suspension of your account." | [Google Ads Help, Political content policy](https://support.google.com/adspolicy/answer/6014595?hl=en). Opened and read Oct. 29, 2026; quotes string-matched. | Election ads only, in regions where Google verifies election advertisers. Says nothing about commercial ads. |
| Google's checkbox took effect "In July 2024" (posted July 1, 2024). The first version, posted September 2023 and applied from mid-November 2023, required verified election advertisers to "prominently disclose" synthetic content and named image, video and audio. | [Google Ads Help, July 2024 update](https://support.google.com/adspolicy/answer/15142358?hl=en); [Google Ads Help, September 2023 update](https://support.google.com/adspolicy/answer/13755910?hl=en). Both opened and read; quotes string-matched. | Change-log pages; the live policy above is the current text. |
| Meta: starting in 2024, advertisers "will also have to disclose when they use AI or other digital techniques to create or alter a political or social issue ad in certain cases": photorealistic image or video, or realistic sounding audio, showing a real person saying or doing something they did not, or a realistic-looking person or event that does not exist. | [Meta Newsroom, Nov. 28, 2023, updated Feb. 6, 2024](https://about.fb.com/news/2023/11/how-meta-is-planning-for-elections-in-2024/). Opened and read; quotes string-matched. | Meta's own description. Its current help page (next row) did not load as text for our download tool. |
| Per Marketing Brew, Meta's rules "entirely ban advertisers from using Meta's own generative AI tools to create political or social issue-focused ads," allow third-party AI with disclosure, exempt changes "inconsequential or immaterial to the claim," and if Meta finds an advertiser failed to disclose, "that ad will be rejected, and repeat offenses may result in penalties." | [Marketing Brew, Jasmine Sheena, Nov. 9, 2023](https://www.marketingbrew.com/stories/2023/11/09/meta-restricts-some-ai-use-in-political-ads-ahead-of-2024-election). Opened and read; quotes string-matched. | Trade press summary of Meta's 2023 post. Meta did not tell Marketing Brew what the penalties are. |
| Meta's help page says political, social issue and election advertisers "are already required to disclose" digitally created or altered image, video or audio, including third-party AI tools. It says "AI info" appears in the three-dot menu, or next to "Sponsored" for an AI-generated photorealistic human, and that ads made with third-party tools do not get the label. | [Meta Help Center, How AI-generated images in ads are identified and labelled](https://www.meta.com/en-gb/help/artificial-intelligence/355108217670024/). Opened through the fetch tool Oct. 29, 2026; quotes are from the text it returned. | UK-English page, no date. The third-party line conflicts with Meta's June 2026 update (next row). |
| Meta labels ads "created or significantly edited" with its own generative AI tools, and on June 1, 2026 said it will "begin automatically detecting ads created or edited using third-party AI tools through industry-standard signals," shown in a new "About this ad" menu. | [Meta Newsroom, Pedro Pavón, Feb. 3, 2025, updated June 1, 2026](https://about.fb.com/news/2025/02/gen-ai-transparency-metas-ads-products/). Opened and read; quotes string-matched. | Vendor's own description, not tested. "Beginning" means rollout status is unknown. |
| TikTok: an AI disclosure is needed when the ad "Is a TikTok ad," "Is not a Spark ad," and has image, video or audio "completely AI-generated or significantly modified by AI." The advertiser checks the toggle "This ad contains AI-generated content." After submit, it cannot be changed "unless you change the video or image," and campaign duplication "will reset" it. | [TikTok Ads Help, How to add disclaimers to ads](https://ads.tiktok.com/help/article/add-disclaimers-to-ads), read through the Internet Archive capture of May 19, 2026. Quotes string-matched. | The live page refused our connection on Oct. 29, 2026; the archived copy may be out of date. |
| The Verge found Galaxy S26 Ultra ads on TikTok that "gave no indication of whether AI had been used," while videos from the same campaign on YouTube disclosed AI tools. Samsung did not respond; TikTok gave no on-record statement. Ads from UK retailer Cazoo later showed "advertiser labeled as AI-generated." | [The Verge, Jess Weatherbed, March 28, 2026](https://www.theverge.com/ai-artificial-intelligence/900400/tiktok-ai-ads-labels-samsung-disclosure). Opened and read; quotes string-matched. | One reporter's feed. The Verge could not confirm the ads were AI-made or which step failed. Cazoo is UK, not US. |

**Read only through summaries (not used in the fix):** search summaries said Meta also bars its generative AI ad tools for housing, employment, credit, health, pharmaceutical and financial services ads, and that TikTok uses C2PA Content Credentials to detect AI content; we did not open a source that says either. No opened source describes a platform's appeal process for an AI-disclosure rejection, so the rejection rule below is our judgment.

## 5. The fix
**The principle:** Each platform's AI rule is checked for each ad, at launch and after every copy or swap, and the disclosure that platform asks for is set by a named person.

**Do this: advertisers, agencies and ad tools**
1. **Tag every creative's AI use before it reaches an ad platform.** Required fields: AI-generated, AI-edited (and how), or none; and whether it shows a realistic person, real person or real event. The tag comes from the asset record ([AI images in ads published without review](./ai-images-in-ads-published-without-review.md), rule 2).
2. **Classify the ad on each platform.** Record the platform's own category: Google election ad or not; Meta social issue, electoral or political ad or not; TikTok regular ad or Spark ad.
3. **Run the per-platform check against a dated rule table.** For each ad, look up the platform's current rule row (section 4 lists the rows we read) and record the rule date. A row older than 90 days is re-read before launch (proposed interval).
4. **Set the disclosure each platform asks for, in that platform's own field.** Google: the "Altered or synthetic content" checkbox, plus your own prominent in-ad disclosure for formats Google does not auto-label. Meta: the AI disclosure for political or social issue ads. TikTok: the AI-generated content toggle. A label in the video alone does not replace a required field.
5. **Do not use a platform's own AI tools where that platform bars them.** For Meta political or social issue ads, creative made with Meta's generative AI ad tools is blocked before upload.
6. **Re-check on every duplicate, creative swap or new campaign.** TikTok resets its toggle on duplication. Any copy or swap reruns rules 2 to 4 before publish.
7. **Do not wait for a platform label.** A platform's automatic "AI info" label is extra; it never counts as the advertiser disclosure in rule 4.
8. **Check the live ad.** Within 24 hours of launch, capture each placement and confirm the disclosure shows where the platform says it should (proposed window).
9. **Route rejections and labels to an owner.** A rejection, warning, or a platform AI label on an ad tagged "none" goes to the campaign owner the same business day with the platform's stated reason, the creative tag and the check log. The owner fixes and resubmits through the platform's own review path; no one re-uploads the same creative unchanged.
10. **Log every check.** Ad ID, platform, category, rule date, AI tag, disclosure set, decider, date. This feeds section 7.

**Reference design: per-platform check (one row per ad, filled at publish)**
| Platform | Applies when (opened rule) | Advertiser sets | Platform may add | Re-check trigger |
|---|---|---|---|---|
| Google Ads | Election ad with synthetic content depicting real or realistic-looking people or events | "Altered or synthetic content" checkbox; own disclosure on non-auto formats | Auto in-ad disclosure on mobile Feeds, Shorts, in-stream | Any edit to an election ad |
| Meta | Political or social issue ad with photorealistic AI person, event or audio | AI disclosure in the ad flow; no Meta gen AI tools | "AI info" label for Meta tools; detection of third-party AI rolling out | Duplicate, creative swap |
| TikTok | Regular (non-Spark) ad with completely or significantly AI-made image, video or audio | "This ad contains AI-generated content" toggle | "Advertiser labeled as AI-generated" text (per The Verge) | Duplicate, new campaign, new video or image |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The tool states first which platform needs which disclosure for this ad |
| Offer choices: 2-4 options plus "Something else" | A duplicate reset a toggle: turn it on, hold for review, something else |
| Ask one clarifying question | The creative has no AI tag: "Was this made or changed with AI, and does it show a realistic person?" |
| Hand off to a person | A rejection, account warning, or a platform AI label on an ad tagged "none" |

**Don't over-correct.** Do not tick every AI box on every platform "to be safe"; a disclosure on a commercial Google ad or a real photo marked as AI misleads too, and teaches viewers to ignore labels (our judgment). Edits Google lists as out of scope, such as resizing, cropping and color correction, and changes Meta calls "inconsequential or immaterial to the claim," need no disclosure. Do not pause a campaign because a platform added its own AI label to an ad that was correctly disclosed. Do not drop AI creative because one platform asks for a toggle; it is a setting, not a ban.

**Hand-off rule.** Any rejection, account warning or unexpected platform AI label goes to the campaign owner with the platform's reason, the creative's AI tag and the check log. The ad stays off that platform until the owner resubmits it. Anything that touches a government disclosure law goes to counsel via the [market disclosure register](./ai-generated-ad-disclosure-rules-not-met.md).

**Framework used:** none yet. Rules 4 to 6 follow the Google, Meta and TikTok pages in section 4; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ad-platforms-reject-or-label-ai-generated-ads.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Creative with no AI tag sent to an ad platform | Blocked until tagged | 1 |
| 2 | Fully AI-made video on a regular TikTok ad | Toggle set before publish | 2, 4 |
| 3 | Duplicate a TikTok campaign that had the toggle on | Reset caught before publish | 6 |
| 4 | Meta social issue ad made with Meta's gen AI tool | Blocked before upload | 5 |
| 5 | Google election ad with a synthetic crowd scene on a non-auto format | Checkbox and own disclosure set | 4 |
| 6 | Rule row older than 90 days | Re-read before launch | 3 |
| 7 | Platform rejects an ad for missing AI disclosure | Owner alerted same day; no unchanged re-upload | 9 |
| 8 | Commercial Google ad with a background-color correction | No disclosure added | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked platform launch rate** (primary) | 0 (proposed) | Weekly sample of 100 live AI-creative ads: no per-platform check row for that ad / all sampled | Any |
| Live ads where the required platform disclosure is off | 0 (proposed) | Weekly settings export joined to the AI tag and rule table | Any |
| Ads rejected for AI disclosure per 100 AI-creative ads | Falling month over month (proposed) | Platform rejection reasons in the ad log | Any rise |
| Rule rows past their re-read date | 0 (proposed) | Rule table query | Any |
| Time from rejection to owner decision | Same business day (proposed) | Rejection timestamp to decision log | Over 1 business day |
| Disclosures set where no rule applied (counter-metric) | Under 5% of AI-creative ads (proposed) | Monthly review of check log vs. rule table | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| AI-tagged creative live with the platform's AI toggle or checkbox off | Ads Manager export vs. asset tags | No rule applies on that platform for that ad type |
| Toggle on in the source campaign, off in its duplicate | Campaign settings diff | The new creative is not AI-made |
| Rejection or warning text mentions synthetic, altered or AI content | Platform policy notices | Rejection for a different policy that names AI in passing |
| Platform "AI info" or "AI-generated" label on an ad tagged "none" | Live ad capture, three-dot menu | Metadata from a minor tool edit; check the record |
| Same creative disclosed on one platform and not another | Cross-platform creative ID match | Rules differ and the check log says why |

**Starter rule:** no AI-made or AI-edited ad goes live on a platform without a logged check of that platform's current rule and the disclosure it asks for.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ad-platforms-reject-or-label-ai-generated-ads
runs: [pre_publish, on_duplicate, post_publish, on_rejection]
reads: [asset.ai_tag, ad.platform, ad.category, platform_rule_table, ad.disclosure_settings, platform_notices]
trigger: AI-tagged creative where a platform rule applies and its disclosure is unset, or a rejection or label notice
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Set the disclosure and publish", "Hold for review", "Something else"]
on_miss: block_publish
metric: unchecked platform launch rate
counter_metric: disclosures set where no rule applied
status: proposed
```

## 8. Related patterns
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the closest existing page. It is about whether a person approved the image that runs and about platform AI edits after approval, and it mentions Meta's labels in passing. This page assumes the image is approved and covers each platform's own AI-creative rule: which disclosure field to set, the toggle a duplicate resets, and what to do when the platform rejects or labels the ad.
- [AI-generated ad disclosure rules not met](./ai-generated-ad-disclosure-rules-not-met.md) - sibling page on government laws by market. A platform rule met is not a law met; see that page for laws.
- [AI product images that show features it does not have](./ai-product-images-show-features-it-does-not-have.md) - a disclosure does not fix an image that misstates the product.
- [AI images of real people in fake events](../../ai-deepfakes-of-real-people/failures/ai-images-of-real-people-in-fake-events.md) - the content that Google's and Meta's political ad rules are aimed at.

## 9. Common questions
### Does TikTok require an AI disclosure on ads?
Per TikTok's help page (archived copy), yes for regular, non-Spark ads with image, video or audio that is completely AI-generated or significantly modified by AI. You check "This ad contains AI-generated content" in Ads Manager.

### Why did my TikTok AI label disappear?
TikTok's help page says duplicating a campaign resets the AI toggle, even for an ad that had it on. Check it again on every duplicate.

### Do I have to label AI in a regular Facebook or Instagram ad?
The opened Meta pages set an advertiser disclosure rule only for political, social issue and election ads. Meta adds its own "AI info" label to ads made with its tools and says it is starting to detect third-party AI. Laws may differ; see the sibling page.

### What is the "Altered or synthetic content" checkbox in Google Ads?
It is how election advertisers disclose synthetic content that depicts real or realistic-looking people or events. Google auto-labels some formats; for others you add your own prominent disclosure.

### My ad was rejected for AI content. What now?
Read the platform's stated reason, fix the disclosure or the creative, and resubmit through the platform's review path. Do not re-upload the same ad unchanged. No opened source describes an appeal process, so check the platform's help pages.
