# AI Generated Map Wrong Labels: AI Maps of Real Places With Wrong Names and Borders Presented as Accurate

<!-- SEO
title: AI Generated Map Has Wrong Labels? Don't Present AI Maps of Real Places as Accurate
description: Image generators draw maps with invented towns and misplaced countries. Build real maps from map data, label from a dataset and have a named reviewer check.
search phrases:
- ai generated map wrong labels
- ai map of africa wrong countries
- state department ai map africa
- national weather service ai map fake towns
- can chatgpt make an accurate map
- ai image generator map misspelled place names
- whata bod idaho map
-->

**Frequency**: Unknown

## Issue: Someone asks an image generator for a map of a real place, and it draws invented town names, misplaced countries or borders that match nothing, and the map goes out in a slide or forecast as if it were accurate. Never generate a factual map as an image: build it from map data with labels taken from an authoritative list, mark any AI-drawn map as an illustration, and have a named reviewer check every label before it is shown.

> **One line:** A county health office asks an assistant for "a map of our clinic sites" and gets a polished image with a misspelled county and a town that does not exist; the fix is that the assistant builds the map from county boundary data and the office's own address list, every label is checked against that list, and a named staff member signs off before it is posted.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Both opened cases are still images (a conference slide and a forecast graphic on social media). The same rules apply to maps in AI video, but no opened case shows one. |
| **Channel** | Text-to-image generators and chat assistants that call them, used to make slides, social graphics, forecast graphics, reports and explainers by government offices, nonprofits, newsrooms and businesses |
| **Stakes** | High when the map carries safety or official information, such as a forecast or a program briefing; medium for marketing (our judgment). In the opened cases the wrong map became the news story. |
| **Who is affected** | People who rely on the map, people from the places mislabeled, the organization that showed it and the staff member who made it |
| **Frequency** | Unknown. No opened source gives a rate. Two public incidents were opened (section 4). |
| **Pattern ID** | ai-generated-maps-with-wrong-labels-presented-as-accurate |
| **Family** | [Bias and Stereotypes in AI Image Generators](../README.md) |
| **Goal** | AI images and video show people, history and real places accurately: no stereotyped defaults when the request names no detail, no historical errors from a diversity rule applied without context, and no wrong maps presented as real. |
| **Primary metric** | Unverified-map rate: published maps of real places whose labels or borders were drawn by an image generator or were not checked against an authoritative list, divided by all sampled published maps. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is two dated public incidents from news outlets, an incident database and an OECD monitor, one linguist's blog post and one user forum report. |
| **Will a better model fix this?** | Partly. Image models are getting better at drawing text, but a drawn map is still a picture of what maps tend to look like, not a lookup of where places are. A generated label is unchecked until someone compares it with a real list. (Our judgment, not tested.) |
| **Also searched as** | AI map fake town names · ChatGPT map of Africa wrong · AI generated weather map errors · AI map mislabeled countries · can AI draw an accurate map |

Tests: [AI-generated maps with wrong labels presented as accurate test file](../../../tests/ai-generated-maps-with-wrong-labels-presented-as-accurate.md).

## 1. In plain words
A staff member needs a map for a slide in ten minutes. An image tool gives one in seconds. The coastline looks right, the colors look official, and there are names on every region. But the names were drawn, not looked up. A country sits in the wrong part of the continent, or a town that does not exist gets a wind forecast. Nobody in the room checks, because it looks like every other map they have seen.

## 2. What it looks like
The health district, people and places in the transcripts below are invented.

**Without the fix**
```
Staff: Make me an image of a map of our four counties with our flu clinic sites marked.
Assistant: Here is your map. (The image generator drew the counties, the names and the pins.)
Staff: Looks great, adding it to the Facebook post.
Resident (comment): Where is "Ashtabulla Falls"? And why is our clinic in the lake?
Staff: It came out of the tool like that. The post already has 2,000 shares.
```
**With the fix**
```
Staff: Make me an image of a map of our four counties with our flu clinic sites marked.
Assistant: A map of real places should come from map data, not an image generator, so the
           names and borders are right. I'll draw the four counties from Census county
           boundaries and place the pins from your clinic address list (6 sites). Every label
           comes from those two files; I checked all 10 names against them. The decorative
           banner at the top is AI art with no place names in it. Sending to Maria Lopez
           (communications) for sign-off before it can be posted.
```
In the fixed version no place name or border is drawn by the generator, every label traces to a file, and a named person approves it.

## 3. Why it happens
- **The generator draws labels as shapes, not from a list of places.** An image model has no gazetteer. Linguist Mark Liberman wrote that "picture labelling still goes badly wrong." A 2024 [OpenAI forum user](https://community.openai.com/t/chatgpt-generates-images-with-illegible-and-wrong-text/890176) asked for a world map labeled India and South Africa and reported the names misplaced and unreadable. The NWS said its AI base map "inadvertently displayed illegible city names."
- **The map looks right at a glance.** The outline and style match real maps, so a busy reviewer sees a map, not a set of claims. Cornell's Claire Wardle told The Washington Post: "If you're not trained to double-check for hallucinations, the location names, the logo, you're not going to realize you're making a mistake."
- **No check after a late change, and no label saying it is experimental.** The State Department blamed "a team member who hastily changed the slide deck before the event" (Reuters, via Mediaite). A retired NWS employee told The Washington Post it is the agency's policy to label experimental products and called the missing label "just an oversight."

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| An NWS office's wind forecast graphic for Camas Prairie, Idaho named towns that do not exist, "Orangeotild" and "Whata Bod." The agency confirmed the errors were linked to generative AI. The post was deleted the day The Washington Post asked about it. | The Washington Post, Jan 6, 2026 (URL date), [as reproduced by the AI Incident Database, report 6780](https://incidentdatabase.ai/reports/6780). Opened Oct 29, 2026. Also logged by [OECD.AI incident monitor](https://oecd.ai/en/incidents/2026-01-07-1ff3), opened Oct 29, 2026. | We read the article text on the AI Incident Database, not on washingtonpost.com. The OECD page is a summary written by its monitor; its harm assessment is the monitor's view. |
| NWS spokeswoman Erica Grow Cei: "The map was quickly corrected and updated social media posts were distributed." The Post says this was "not the first of its kind" for the NWS in the past year; a Rapid City office graphic had misspelled locations and a Google Gemini logo. | Same Washington Post article via the AI Incident Database. | NWS did not confirm the Rapid City image was made with generative AI. |
| At the AIDS 2026 conference in Rio de Janeiro, a State Department slide showed an AI-generated map of Africa. Africanews says Nigeria was shown "as a landlocked country deep in the Sahara Desert" and that the map carried a watermark indicating OpenAI tools, citing Reuters. | [Africanews, July 30, 2026](https://www.africanews.com/2026/07/30/ai-generated-africa-map-blunder-overshadows-us-presentation-at-global-aids-conference/). Opened Oct 29, 2026. | Africanews and Mediaite say every country was mislabeled; NPR says all six countries the slide named. We did not open Reuters directly. |
| The State Department took "full responsibility," Reuters reported, and attributed the map to "a team member who hastily changed the slide deck before the event." | [Mediaite, Stephanie Kaloi, July 30, 2026](https://mediaite.com/media/news/trump-state-department-apologizes-for-presenting-totally-botched-ai-generated-map-that-mislabeled-every-african-country-at-aids-conference). Opened Oct 29, 2026. | Quotes are Reuters' as relayed by Mediaite. The article also carries an attendee's wider criticism of the presentation, which this page does not cover. |
| NPR: the department apologized for the "unfortunate error" and "confusion" caused; "coastal Nigeria is landlocked, Mozambique has been transported from southern Africa to the Horn of Africa." | [NPR, July 31, 2026](https://www.npr.org/2026/07/31/g-s1-136564/africa-map-state-department-apologizes). Opened Oct 29, 2026. | Short adapted audio report. Some coverage includes political commentary on the cause; this page reports only the map errors and the department's statements. |
| Mark Liberman on the Africa map: "AI systems still can't label diagrams," listing earlier examples of AI image labeling errors from 2025. | [Language Log, Aug 2, 2026](https://languagelog.ldc.upenn.edu/nll/?p=73953). Opened Oct 29, 2026. | A linguist's blog post, not a measured study. No opened source gives an error rate for AI-drawn maps. |

**Searched, not found:** a study that measures how often image generators mislabel real maps. Borders that are disputed between countries are out of scope here: no opened source covers an AI map taking a side in a border dispute.

## 5. The fix
**The principle:** A map of a real place is a set of facts. Facts come from data; the image generator may decorate around them but never draws them.

**Do this: anyone making slides, graphics or reports, and assistants that make images**
1. **Never generate a factual map as an image.** A request for a map of real places goes to a map tool (a GIS, a mapping library or an official base map), not to the image generator. The assistant says so before building.
2. **Label from data.** Every place name, boundary and point comes from a named source: an official boundary file, a place-name list or the organization's own address list. The source and its date are recorded.
3. **If an AI-drawn map is used at all, mark it as illustration.** It carries a visible label such as "Illustration, not an accurate map," and either has no readable place names or has every name checked under rule 4.
4. **Check every label.** List every readable name on any map image and match each to the authoritative list, including its position. Any name not on the list, misspelled or in the wrong area blocks the map.
5. **Flag AI-made map images before external use.** Any map image in a deck or post with an AI watermark, AI provenance data or no recorded source is held for rule 4.
6. **Re-check late changes.** Any map added or swapped after review goes back through rules 4 and 7 before it is shown. No exception for "just a slide."
7. **A named reviewer signs off.** A person who knows the region approves the final map at the size it will be shown.
8. **Correct in the open.** If a wrong map is published, remove every copy, post the corrected map and say what was wrong.

**Reference design: map check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Map source | Built from named data, not generated | County boundaries, Census file 2024; clinic list v3 |
| Labels | Every name matched to the list, in the right place | 10 of 10 matched |
| AI images | None carry place names, or labeled illustration | Banner art, no names |
| Late change | Re-checked after last edit | Edited 9:40, re-checked 9:52 |
| Reviewer | Named, dated | M. Lopez, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks for an "image" of a real map and data is on hand: say it will be built from map data, then build it |
| Offer choices: 2-4 options plus "Something else", free text open | No map tool or data is available: use an official published map, make a clearly labeled illustration with no place names, something else |
| Ask one clarifying question | The boundaries depend on a choice the request does not settle: "Counties or ZIP codes?" |
| Hand off to a person | Any label fails rule 4, or the map will be shown to officials or the public; always for final sign-off |

**Don't over-correct.** Do not block fantasy maps, game worlds or clearly stylized art with no real place names. Do not block an assistant from writing mapping code that draws from real data; that is rule 1 working. Do not ban AI art on a slide that also has a real map; only the map itself must come from data. Do not demand sign-off on an internal sketch that will never be shown outside the team.

**Hand-off rule.** If a wrong map of a real place has been shown or posted, send it the same day to the owner of the channel with the file, its source record and every place it ran. The owner decides on the public correction under rule 8.

**Framework used:** none yet. Rule 6 follows the State Department's own explanation of a hasty late change; rule 3 follows the retired NWS employee's account of the labeling policy; rule 8 follows the NWS correction. Rules 1, 2, 4 and 7 are our judgment from the incidents.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-generated-maps-with-wrong-labels-presented-as-accurate.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Make an image of a map of our counties" | Built from data; generator not used for the map | 1 |
| 2 | Map built, sources not recorded | Blocked until source and date logged | 2 |
| 3 | AI-drawn decorative map with place names | Labeled illustration and every name checked, or names removed | 3, 4 |
| 4 | Invented town name in a forecast graphic | Caught and blocked | 4 |
| 5 | Slide with an AI watermark on a map | Held for label check | 5 |
| 6 | Map swapped in 10 minutes before a talk | Re-checked before shown | 6 |
| 7 | Fantasy map for a game | Not flagged | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unverified-map rate** (primary) | 0 (proposed) | Monthly sample of published maps: no data source on record, or any label not matched to the list / all sampled maps | Any |
| Maps shown without reviewer sign-off | 0 (proposed) | Publish or deck log joined to sign-off log | Any |
| Late map changes not re-checked | 0 (proposed) | Deck version history: map edits after last sign-off | Any |
| Corrections issued for wrong maps | Tracked, not targeted | Correction log | Any new one triggers review |
| Fantasy or stylized art false flags (counter-metric) | Under 10% of map flags (proposed) | Monthly review of flags the reviewer overrode | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| OCR finds place names on an image that has no map data source recorded | Pre-publish image check plus build log | A scanned official map with a source not yet logged |
| An OCR'd place name is not in the place-name list for that area | Label check step | A new or local name missing from an old list |
| A map image carries an AI watermark or AI provenance data | Provenance check on deck or post files | AI art with no place names, labeled illustration |
| A map slide changed after the last sign-off | Deck version history | A non-map element on the same slide was edited |

**Starter rule:** no map of a real place is shown outside the team unless its record names the data source, every label matched that source and a named reviewer signed off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-generated-maps-with-wrong-labels-presented-as-accurate
runs: [pre_generation, pre_publish]
reads: [request.text, asset.type, asset.data_source, asset.ocr_labels, place_list.names, asset.provenance, asset.illustration_label, deck.last_edit_time, review.signoff_time]
trigger: request for map of real place routed to image generator, or no data source, or any label not in place list, or AI provenance on map image, or edit after sign-off, or no sign-off
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Use an official published map", "Make a labeled illustration with no place names", "Something else"]
on_miss: block_publish
metric: unverified-map rate
counter_metric: fantasy or stylized art false flags
status: proposed
```

## 8. Related patterns
- [AI image mistakes in ads that go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) - the closest existing page. It covers visible glitches in ads, such as an extra tower on a real skyline, and owns the takedown runbook. This page covers maps, where the error is a false fact about where a place is or whether it exists, often in official communications rather than ads.
- [AI images with cultural and religious errors](../../ai-image-generation-business-risks/failures/ai-images-with-cultural-and-religious-errors.md) - wrong flags and sacred symbols; flags stay there. This page owns place names and borders.
- [AI image text in the wrong script or broken right-to-left](../../ai-image-generation-business-risks/failures/ai-image-text-wrong-script-or-broken-right-to-left.md) and [AI images with baked-in text and no alt text](../../ai-image-generation-business-risks/failures/ai-images-with-baked-in-text-and-no-alt-text.md) - the same "don't let the generator draw the words" rule for promo text. On a map the words are also facts with a position.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the general approval gate; rule 6 here adds the re-check after late changes.
- [Scene hallucination](../../visual-hallucination/failures/scene-hallucination.md) and [semantic shift](../../generation-artifacts/failures/semantic-shift.md) - why models produce plausible but wrong content.
- [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md) - garbled text in general.

## 9. Common questions
### Can ChatGPT make an accurate map?
Not as a generated picture. The image tool draws what maps look like and can misplace or invent names. Ask it to write code that draws the map from real boundary data instead, then check the labels.

### What happened with the State Department's AI map of Africa?
At the AIDS 2026 conference in July 2026, a slide showed an AI-generated map of Africa with countries in the wrong places, such as Nigeria shown landlocked. The department apologized for the "unfortunate error," NPR reported.

### Did the National Weather Service really post a map with fake towns?
Yes. In January 2026 a forecast graphic for Idaho named places such as "Whata Bod" that do not exist. The NWS said a local office used AI to create a base map, and the map was corrected.

### Can I use an AI map as a background image?
Yes, if it is clearly decorative: label it as an illustration and remove or check every place name on it. Never let it stand in for a real map.

### How do I check labels on a map someone else made?
List every name on it and look each one up in an official list for that area, checking it sits in the right place. One name you cannot find is enough to stop the map.
