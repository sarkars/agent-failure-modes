# AI Images With Cultural and Religious Errors: Wrong Deities, Broken Flags and Stereotyped People

<!-- SEO
title: AI Images With Cultural and Religious Errors: Checks Before Ads, Packaging and Banners Go Out
description: AI art for a holiday or faith gets a sacred symbol or flag wrong, so check each one with someone from that community before it is printed.
search phrases:
- ai generated image cultural mistake brand apology
- ai artwork wrong religious symbol recall
- mamee lord murugan ai trident
- ai generated flag wrong stars stripes
- singapore national day ai banner flag
- ai image stereotypes different countries
- how to check ai images for cultural sensitivity
- ai generated ad offends religious community
-->

**Frequency**: Occasional

## Issue: A brand or public body uses AI art for a holiday, faith or market and gets a sacred figure, flag or custom wrong, and the community it was made for spots it. List every culture-specific element, place flags from the official file, and have a reviewer from that community sign off before anything is printed or posted.

> **Read this first:** This page describes incidents and statements as the cited reports describe them. It mentions one flag law only as The Standard reports it, and makes no claim about what any law requires; that needs review by a qualified person. This is design guidance, not legal advice. Three of the four incidents are outside the US and are marked: Malaysia (two) and Singapore. The time limits in the fix are our proposals.

> **One line:** A team asks an image tool for "Lord Murugan at Batu Caves" or "a National Day banner," and the tool draws a trident where the sacred spear should be or a flag with no stars; nobody on the team knows the difference, so the people the image was meant to honor find it after it is printed; the fix is a list of every symbol, flag, script and custom in the image, an official reference for each, and a named reviewer from that community before launch.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. All four incidents are still images (a product bag, street banners, a website image, a billboard). The rules apply to video frames too, but no opened source covers a video case. |
| **Channel** | Packaging, printed banners, out-of-home ads, websites and social posts made with AI for a religious or national occasion, or for a market or community the team is not part of |
| **Stakes** | High. A religious community is offended, products are recalled from shelves (MAMEE), and a distorted national flag may break local law (Singapore, as reported; section 4). |
| **Who is affected** | The community whose faith, flag or customs are shown, the brand or public body, its agency or volunteers, and retailers holding recalled stock |
| **Frequency** | Occasional, by our judgment: section 4 lists four incidents from 2024 to 2026 in three countries. No opened source gives a rate. |
| **Pattern ID** | ai-images-with-cultural-and-religious-errors |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Escaped cultural error rate: published AI-made or AI-edited assets with a listed culture-specific element whose cultural, religious or national-symbol error was first reported after publish, divided by all such published assets. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A better model may draw a flag's stars more often, but it cannot know which attribute a local temple statue holds or which detail a community finds offensive, and Rest of World's test shows the defaults lean to stereotypes. (Our judgment, not tested.) |
| **Also searched as** | AI art offends Hindus · AI flag error · AI holiday banner mistake · AI image cultural insensitivity · brand recalls AI packaging |

Tests: [AI images with cultural and religious errors test file](../../../tests/ai-images-with-cultural-and-religious-errors.md).

## 1. In plain words
A snack company wants a bag that celebrates its home state. Someone asks an AI tool for the famous statue at the local temple. The tool draws a god holding the wrong weapon. Nobody on the team worships there, so nobody notices. The bags reach stores, worshippers see the mistake, and the company has to apologize to religious leaders and pull every bag. A flag, a holy figure or a holiday custom is not decoration to the people it belongs to. The tool only knows what such things usually look like.

## 2. What it looks like
The grocery chain and people below are invented. The defect follows Rest of World's finding that Midjourney showed Chinese dishes with chopsticks "in threes rather than pairs," which a source called "extremely inauspicious" (section 4).

**Without the fix**
```
Designer:  Lunar New Year flyer for the Grant Avenue store in San Francisco is done. AI made the dumpling plate.
Manager:   Looks festive. Print 5,000 and post it on Instagram.
           (Two days later, a customer comment under the post)
Customer:  "Three chopsticks on the plate? That's bad luck. Did anyone Chinese look at this?"
Manager:   Deletes the comment. The flyers stay in the bags at checkout.
Customer:  Posts a photo of the flyer; local community pages share it.
```
**With the fix**
```
Designer:  Lunar New Year flyer for the Grant Avenue store: dumpling plate, red lanterns, greeting in Chinese.
Check tool: Market tag: Lunar New Year, Chinese American shoppers. Culture-specific elements: 2 found (lanterns are decoration).
            1) Chopsticks: image shows 3. Reference: a pair. FAILED.
            2) Chinese greeting: matches the approved text from the reviewer. Passed.
            Reviewer needed. 1) Fix chopsticks, resend  2) Use a licensed dish photo  3) Something else
Designer:  2.
Reviewer:  L. Wong, store team, reads Chinese, celebrates the holiday: approved for print and Instagram.
```
In the fixed version every culture-specific element is listed and checked, a real photo replaces the failed element, and a named person from the community signs off before print.

## 3. Why it happens
- **The model draws the common version, not the sacred one.** It learned what spears, flags and dinner tables usually look like, so it swaps a vel for a trident or drops a flag's stars. Rest of World's test of 3,000 images found that national prompts collapse into a few props, such as a sombrero for "a Mexican person" (section 4). How meaning slips during generation is covered in [semantic drift](../../generation-artifacts/failures/semantic-shift.md).
- **The team is not from the community it is portraying.** A general art review asks "does it look good?" Only someone who knows the faith or flag asks "is that what he holds?" MAMEE said its team should have been "more alert to the sensitivities of this country" (section 4).
- **Small or volunteer jobs skip review.** Singapore's banners were made by "residents who volunteered their time," and a resident asked why they "were not checked before printing." A government site's flag image went up with 11 stripes (section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| MAMEE "apologised for an AI-generated illustration of the sacred Lord Murugan on its Selangor-themed bag." The artwork showed the Batu Caves statue "with a three-pointed trident rather than the vel," a divine spear. MAMEE said the team should have been "more alert to the sensitivities of this country," that it "had started recalling the bags through its retail network and distribution channels," and Malaysia Hindu Sangam said on Sept. 20 that MAMEE's leaders had visited it. | [Marketing-Interactive, Claudia Khaw, Sept. 21, 2026](https://www.marketing-interactive.com/mamee-recalls-bags-after-ai-artwork-of-lord-murugan-sparks-backlash). Opened and read. | Malaysia, not US. Single outlet opened. The article gives no recall start date. |
| AI-generated National Day banners at a Singapore housing estate "showed the flag without its crescent moon and five stars"; a third showed them "smeared into indistinct blobs." The community club said the banners were made by "residents who volunteered their time," and that AI output "should always be carefully checked before it is used." "The banners were removed by July 22." | [The Standard, July 24, 2026](https://www.thestandard.com.hk/world/article/338091/Singapore-removes-AI-generated-National-Day-banners-after-flag-error). Opened and read. | Singapore, not US. No author named. The Standard cites The Independent Singapore, which we did not open. |
| The same article says: "Under the National Symbols Act 2022, producing or displaying a distorted flag is prohibited." | Same source. | A news report's summary of a non-US law. Not checked against the law; needs review by a qualified person. |
| The DOGE.gov landing image showed a US flag that "featured 11 stripes and a deformed mush of about 37 stars," and "the site has been stripped of the image." | [Futurism, Joe Wilkins, Jan. 22, 2025](https://futurism.com/doge-website-ai-american-flag). Opened and read. | US. A federal website, not an ad. The article calls it AI-generated; we did not see the agency confirm it. |
| Rest of World "analyzed 3,000 AI images" from Midjourney across five countries and the US. "99 out of the 100 images for 'a Mexican person'... featured a sombrero or similar hat." For "an Indian person," "Ninety-two of the subjects wore a traditional pagri." "All 100 images" for "an American person" featured a flag. Chopsticks "were often shown in threes rather than pairs." | [Rest of World, Victoria Turk, Oct. 10, 2023](https://restofworld.org/2023/ai-image-stereotypes/). Opened and read. | One tool (Midjourney), English prompts, one run per prompt, 2023. A test of defaults, not a business incident. |
| An agency's AI billboard showed the Petronas Twin Towers "with three towers instead of two." | [Malay Mail, Aug. 9, 2024](https://www.malaymail.com/news/malaysia/2024/08/09/a-case-of-one-too-many-ad-agency-says-sorry-over-ai-gaff-showing-petronas-twin-towers-with-extra-tower-in-merdeka-billboard/146474). Opened and read. | Malaysia. Told in full on [AI image mistakes in ads that go viral](./ai-image-mistakes-in-ads-go-viral.md); here only as a national landmark on a national-day ad. |

**Searched and not used:** a deleted DHS post about a Sikh truck driver ([Local News Matters, Sept. 13, 2026](https://localnewsmatters.org/2026/09/13/deleted-dhs-post-featuring-stockton-truck-driver-draws-backlash-from-sikh-community/), opened) was called "seemingly AI-generated," but it was a deliberate message, not an error, so it belongs to a bias page. Search summaries mentioned a Chinese AI ad that stigmatized menstruation and a Ramadan campaign criticized on LinkedIn; we did not open them.

**What no source shows.** No opened source measures how often AI art carries cultural errors in real campaigns, or whether a community reviewer prevents them. The review rules below are our judgment, drawn from what each incident lacked.

## 5. The fix
**The principle:** Any symbol, figure, flag or custom that belongs to a faith, nation or community is checked against an official reference and signed off by someone from that community before it is printed or posted.

**Do this**
1. **Tag the market and occasion.** Every AI-made or AI-edited asset made for a religious or national occasion, or for a community or market the team is not part of, gets a tag naming it (for example "Diwali, Indian American shoppers in Edison, NJ").
2. **List every culture-specific element.** For tagged assets, list each sacred figure and what it holds or wears, flags and emblems, landmarks, script and text, dress, food customs, and numbers or colors with meaning. Each gets a reference.
3. **Never generate flags and emblems.** Place national and state flags, seals and emblems from the official file. Sacred figures and famous religious sites come from a licensed or approved photo, or a depiction the reviewer approves.
4. **Check each element against its reference.** Count stars, stripes and points; check what each figure holds; check text letter for letter in the right script. Any mismatch fails the asset.
5. **Name a community reviewer.** A tagged asset needs sign-off from a named person who belongs to or works closely with that community. For a sacred figure, the reviewer practices the faith, or the brand asks a recognized religious body or paid consultant. The reviewer is not the designer.
6. **Check people for stereotypes.** When a prompt names a nationality, ethnicity or faith, the reviewer checks the people for default props (one hat, one flag, one age group) and asks: would people from here see themselves?
7. **Small, volunteer and internal jobs too.** Banners, flyers and posts made by volunteers, local stores or staff follow rules 2 to 5 before printing.
8. **If an error is reported, confirm it with the reviewer, then pull everything.** Use the placement map and timings in [AI image mistakes in ads that go viral](./ai-image-mistakes-in-ads-go-viral.md), rules 7 to 10, and add printed stock: recall through retail and distribution channels, as MAMEE did.
9. **Apologize to the community by name.** The apology says what was wrong in the community's own terms ("a trident instead of the vel"), says AI made it if it did, and states what was pulled. For a religious error, the brand offers to meet the community's leaders.
10. **Feed the review back.** Within one week (proposed), the element is added to that market's reference list.

**Reference design: culture element checklist (one row per element)**
| Element | Type | Reference | Check | Reviewer sign-off |
|---|---|---|---|---|
| Lord Murugan statue | Sacred figure | Licensed temple photo | Holds the vel, not a trident | Required, practicing reviewer or religious body |
| Singapore flag | National flag | Official flag file | Crescent and five stars present | Required; flag placed from file, not generated |
| US flag | National flag | Official flag file | 13 stripes, 50 stars | Placed from file |
| Chopsticks on a plate | Food custom | Approved photo | A pair, not an odd count | Required |
| Greeting text | Script | Reviewer-approved text | Letter for letter | Required |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The check tool reports the failed element first: "Flag: reference has 5 stars, image shows 0" |
| Offer choices: 2-4 options plus "Something else", free text open | An element fails: place the official file or licensed photo, fix and resend to the reviewer, something else |
| Admit uncertainty and show how to check | The tool cannot tell whether an object is sacred or decorative: it shows the crop and asks the reviewer |
| Hand off to a person | Any tagged asset, any sacred figure, any reported cultural error |

**Don't over-correct.** Do not drop a community's holidays or people from campaigns to avoid risk; that is a different harm. Generic decoration with no listed meaning (lanterns, string lights) needs no reviewer. Do not ask one employee to speak for a whole faith or country without their agreement; pay a consultant if no one fits. A joke comment with no named error is not a report; confirm with the reviewer first.

**Hand-off rule.** A sacred figure, a national symbol, or a reported cultural error goes to the community reviewer and the campaign owner with the asset, the element list and the references. A question about whether a flag or symbol law applies goes to counsel. The asset does not print or post until the reviewer signs off.

**Framework used:** none yet. Rules 3 and 4 answer the flag and trident cases; rules 5 and 6 are our judgment from MAMEE's statement and Rest of World's findings.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-images-with-cultural-and-religious-errors.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Diwali flyer with no market tag | Tag required before review | 1 |
| 2 | Temple statue holding the wrong object | Element listed; fails against the photo | 2, 4 |
| 3 | National Day banner with a generated flag | Blocked; official file placed | 3 |
| 4 | Asset tagged, designer self-approves | Held for a named community reviewer | 5 |
| 5 | "A Mexican family" ad, everyone in sombreros | Reviewer flags the stereotype | 6 |
| 6 | Volunteer banner sent straight to the printer | Held for rules 2 to 5 | 7 |
| 7 | Confirmed error on printed packaging | Recall through retail and distribution | 8 |
| 8 | Draft apology says "an error" only | Blocked; names the element and AI use | 9 |
| 9 | Lanterns-only Lunar New Year banner | No reviewer demanded | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Escaped cultural error rate** (primary) | 0 (proposed) | Incident log: tagged assets with a confirmed cultural error first reported after publish / all published tagged assets, monthly | Any |
| Tagged assets with community sign-off | 100% (proposed) | Asset log: tagged assets with a named reviewer record / all tagged assets | Under 100% |
| Flags and emblems placed from the official file | 100% (proposed) | Element checklist: flag rows with source "official file" / all flag rows | Any generated flag |
| Untagged occasion assets | 0 (proposed) | Sampled review of AI assets whose text names a holiday or nation but have no tag | Any |
| Assets held with no listed element (counter-metric) | Under 10% of holds (proposed) | Asset log, monthly | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt or copy names a holiday, faith, deity, nation or flag, and the asset has no market tag | Prompt log vs. asset log | A passing mention in body copy, not in the image |
| Comments name a symbol or custom ("wrong weapon," "no stars," "bad luck") | Post comments, community pages | A joke about a correct image; check with the reviewer |
| A religious body, temple or community group contacts the brand | Press and customer inbox | A sponsorship request |
| A flag row in the checklist has source "generated" | Element checklist | A stylized flag the reviewer approved as art |

**Starter rule:** no AI-made asset for a religious or national occasion or another community prints or posts until every culture-specific element matches an official reference and a named reviewer from that community signs off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-images-with-cultural-and-religious-errors
runs: [pre_publish, post_publish]
reads: [asset.market_tag, asset.culture_elements, asset.references, reviewer.signoff, prompt_log, comments, incident_log]
trigger: asset names a holiday, faith, nation or community, an element fails its reference, or a report names a cultural error
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Place the official file or licensed photo", "Fix and resend to the reviewer", "Something else"]
on_miss: block_publish_or_open_incident
metric: escaped cultural error rate
counter_metric: assets held with no listed element
status: proposed
```

## 8. Related patterns
- [AI image mistakes in ads that go viral](./ai-image-mistakes-in-ads-go-viral.md) - the closest page; it tells the Petronas billboard case and owns the takedown runbook. That page checks counts and shapes any careful reviewer can verify. This page covers errors only a person from the community recognizes, such as which weapon a deity holds, and adds the community reviewer, official flag files and the community apology.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - who approved the version that ran.
- [AI-generated ad disclosure rules not met](./ai-generated-ad-disclosure-rules-not-met.md) - the other multi-market page: labeling laws per market, not cultural content.
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - why the model swaps one object for a similar one.
- [Chatbot assumes a regional or community style](../../../../human-machine-interface/goals/cultural-adaptation/failures/regional-and-community-styles.md) - the same risk in chat text.

## 9. Common questions
### Why did the AI draw the wrong weapon on Lord Murugan?
The tool draws what similar statues usually hold, not what this one holds. MAMEE's bag showed a trident instead of the vel, and the bags were recalled. Use a licensed photo and a reviewer who knows the faith.

### Can I use AI to make a flag for a holiday banner?
Place the flag from the official file instead. AI banners in Singapore dropped the flag's crescent and stars, and a US government site showed a flag with 11 stripes.

### How do I check AI images for cultural sensitivity?
List every symbol, figure, flag, script and custom in the image, check each against a real reference, and have someone from that community sign off before printing.

### Why do AI images of people from other countries look stereotyped?
Rest of World found Midjourney put a sombrero on 99 of 100 images of "a Mexican person." Name specific details in the prompt and have a reviewer check the people.

### What should a brand do after an AI image offends a religious community?
Confirm the error with someone from the community, pull every copy including printed stock, and apologize in the community's own terms, as MAMEE did with Malaysia Hindu Sangam.
