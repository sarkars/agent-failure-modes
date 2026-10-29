# AI Ad Mistakes That Go Viral: Extra Towers, Backward Feet and Two-Handled Bikes

<!-- SEO
title: AI Ad Mistakes That Go Viral: Pre-Flight Checks and What to Do When One Spreads
description: A brand runs an AI-made ad with a visible mistake, such as an extra tower on a famous skyline or a bike with two sets of handlebars, and the public finds it first. How to check landmarks, products and bodies against a reference before launch, and how to pull and correct the ad once it spreads.
search phrases:
- ai generated ad mistake goes viral
- ai billboard extra tower petronas
- ai ad extra fingers brand apology
- j crew ai ad backward foot
- what to do if your ai ad goes viral for the wrong reason
- how to apologize for an ai generated ad mistake
- how to check ai images before an ad campaign
- rei two handlebars ai ad
-->

**Frequency**: Common

## Issue: A brand runs an AI-made or AI-edited ad with a visible mistake, such as an extra tower on a real skyline, a foot facing backward or a product with parts it does not have, and the public spots and shares it before the brand does. Check every landmark, product and body in the ad against a real reference before launch, and when one spreads anyway, pull every copy the same day and post a plain correction that names the mistake.

> **Read this first:** This page describes incidents and company statements as the cited reports describe them. It makes no claim about what any law requires. Three of the six incidents are outside the US and are marked: Malaysia, Australia and Kenya. The timing targets in the fix are our proposals, not findings from any source.

> **One line:** An agency publishes an AI-made billboard or social ad that looked fine at a glance, and within hours people are counting the Petronas towers or the handlebars on a bike and sharing screenshots; the fix is a reference check before launch (count and shape of every landmark, product part and limb against a real photo or spec) and a response runbook after (confirm, pull every placement on one list, post a correction that names the defect and the new check).

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The Malaysia billboard, REI, J.Crew and Posta Kenya cases are still images; the Jeanswest case is two 20-second video spots plus a still image (section 4). |
| **Channel** | Paid social ads, digital billboards, brand social posts and campaign images or video made or changed with AI tools |
| **Stakes** | Medium. The ad becomes a public joke about the brand, staff time goes to takedown and statements, and in REI's case the ad showed a product "not something you will find in our assortment" (section 4). |
| **Who is affected** | The brand or public agency named on the ad, its agency, the people pictured, and everyone who sees and shares it |
| **Frequency** | Common, by our judgment: section 4 lists six incidents from 2024 to 2026 across four countries. No opened source gives a rate. |
| **Pattern ID** | ai-image-mistakes-in-ads-go-viral |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Escaped defect rate: published AI-made or AI-edited ad assets whose visible defect was first reported after publish, divided by all published AI-made or AI-edited ad assets. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Newer models draw fewer broken hands, but a model does not know that a skyline has two towers or that this bike has one set of handlebars unless it is checked against a reference, and no model takes down an ad or writes the correction. (Our judgment, not tested.) |
| **Also searched as** | AI ad fail · AI billboard mistake · brand mocked for AI image · AI campaign glitch · company pulls AI ad after backlash |

Tests: [AI image mistakes in ads go viral test file](../../../tests/ai-image-mistakes-in-ads-go-viral.md).

## 1. In plain words
A team makes a holiday billboard with an AI tool. It shows a famous building, and the AI draws one tower too many. Nobody counts. People driving past take photos, and the picture spreads online by lunch. Now the team has two jobs it never planned for: find every place the ad runs and pull it, and tell the public what went wrong without making it worse.

## 2. What it looks like
The dealership, agency and people below are invented. The defect follows the Malaysia billboard case (section 4).

**Without the fix**
```
Agency:     Fourth of July billboard is live on I-64, plus Facebook and Instagram. Arch skyline, fireworks.
            (Three hours later, a comment under the Facebook post)
Commenter:  "Since when does St. Louis have TWO Arches? Did a robot make this?"
Social lead: Deletes the Facebook post. No reply.
            (The billboard and the Instagram post keep running; screenshots of both are shared that night.)
Client:     "Why is a reporter asking me about our two-Arch ad?"
```
**With the fix**
```
Designer:   Final for the Fourth of July billboard: Arch skyline, fireworks, approved copy.
Check tool: Reference check failed. Landmark "Gateway Arch": reference count 1, image shows 2.
            Product: none. Hands and feet: none visible. Text matches approved copy letter for letter.
            1) Swap in the licensed skyline photo  2) Regenerate once and recheck  3) Something else
Designer:   1.
Check tool: Licensed photo placed. All reference checks pass. Sent to second reviewer (billboard rule).
Reviewer:   M. Chen: viewed at full size and at billboard scale. Approved for 1 billboard and 2 social posts.
```
In the fixed version the landmark is counted against a reference, the fix is a real photo instead of more tries, and a second person signs off because it is out-of-home. If a defect still gets out, rules 7 to 11 apply.

## 3. Why it happens
- **The generator does not know the real count.** It draws what towers, bikes and feet usually look like, not this skyline or this product, so an extra tower or a second set of handlebars looks plausible to it. Why the defects appear, and why repeated edits add more, is covered in [artifact accumulation](../../generation-artifacts/failures/artifact-accumulation.md) and [consistency failure](../../generation-artifacts/failures/consistency-failure.md).
- **Nobody checks the picture against the real thing.** Review asks "does it look good?", not "how many towers does this building have?" A J.Crew ankle pointing backward and a Posta Kenya poster where two models have three hands each went out unchecked (section 4).
- **There is no plan for after launch.** The ad runs on screens, in ad sets and in reposts nobody listed, and nobody owns the reply. REI's ad ran a week; Posta Kenya's post stayed up more than two hours and drew no comment; Jeanswest did not answer a trade reporter (section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| An AI-generated digital billboard in Desa Sri Hartamas, Kuala Lumpur, "mistakenly depicted the Petronas Twin Towers with three towers instead of two." It was commissioned by the Brickfields police headquarters for Merdeka month. "eagle-eyed Malaysians quickly spotted the error and shared it on social media." Agency Wow Media said: "We sincerely apologise for the confusion caused and will review all procedures to ensure such errors do not happen again." "The billboard was promptly removed." | [Malay Mail, Aug. 9, 2024](https://www.malaymail.com/news/malaysia/2024/08/09/a-case-of-one-too-many-ad-agency-says-sorry-over-ai-gaff-showing-petronas-twin-towers-with-extra-tower-in-merdeka-billboard/146474). Opened and read. | Malaysia, not US. The client is a police station, not a brand; Malay Mail cites Malaysiakini, which we did not open. |
| Wow Media said on Facebook it "had identified the error in the visual displayed on the screen and had immediately deleted it," and "will re-evaluate the procedure to avoid any similar problems in the future." | [Marketing-Interactive, A'bidah Zaid Shirbeeni, Aug. 12, 2024](https://www.marketing-interactive.com/advertising-agency-wow-media-ai-display-twin-towers). Opened and read. | Malaysia. The article gives no detail on what procedure changed. |
| REI's Instagram ad for a Van Rysel bike showed "dual front and rear handlebars," "too many chains" and "blurry lettering." It "had been up for a week before being taken down on June 22." The ad ended up on Reddit. REI said "Meta auto-enrolled us in an AI personalization tool," and that "While a two-handled bike might be interesting, it is not something you will find in our assortment." REI unenrolled and apologized. | [TechSpot, Rob Thubron, June 25, 2026](https://techspot.com/news/112895-rei-pulls-ai-generated-bike-ad-after-meta.html). Opened (by direct download) and read. | US. The same incident anchors [H2](./ai-images-in-ads-published-without-review.md), which covers the platform edit; here it is used only for the defect and the response. |
| J.Crew posted three Instagram images for a Vans collaboration. Blackbird Spyplane, after a tip, found a "model" who looks different between pictures, "an ankle that appears to point backwards" and a camera that does not look real. J.Crew updated the captions to read "Digital art by: @samfinn.studio." | [PetaPixel, Matt Growcoot, Sept. 2, 2025](https://petapixel.com/2025/09/02/j-crews-ai-generated-fashion-images-look-a-lot-like-real-photos/). Opened (by direct download) and read. | US. Blackbird Spyplane's own report was not opened. |
| Futurism lists "one man's foot facing backwards and another's hands melting into the handlebars of his bike," and says J.Crew "didn't actually cop to the use of AI in the caption," calling the images "digital art." J.Crew's statement to The Cut did not mention AI. | [Futurism, Maggie Harrison Dupré, Aug. 31, 2025](https://futurism.com/j-crew-ad-faked-ai). Opened (by direct download) and read. | US. Opinionated coverage; The Cut was not opened. |
| Jeanswest posted two 20-second Instagram spots (Dec. 30, 2025 and Jan. 6, 2026) with AI models described as having "blurry and unnatural movements." One commenter asked, "How did this epic AI monstrosity get post approval?" Jeanswest had not responded to B&T's request for comment before publication. | [B&T, Oliver Cerovic, Jan. 16, 2026](https://www.bandt.com.au/are-you-pranking-us-jeanswest-ridiculed-online-over-ai-monstrosity/). Opened and read. | Australia, not US. Much of the criticism is about taste ("lazy," "no soul"), which is closer to the planned backlash page listed in [this goal's README](../README.md); no removal reported. |
| Posta Kenya posted a customer care poster on X in which "two of the models are having three hands each." It stayed up "for more than two hours," and the agency had not "publicly commented on the errors." | [Citizen Digital, Kenneth Gachie, Jan. 31, 2024](https://citizen.digital/news/posta-kenya-blasted-online-for-sharing-faulty-ai-image-featuring-extra-hands-and-white-employees-n335855). Opened and read. | Kenya, not US. National post office, single outlet. |
| eMarketer says Skechers "was slammed for an AI-generated billboard showing a generic, poorly rendered figure," and that "obvious synthetic errors can make campaigns look careless." | [eMarketer, Jeremy Goldman, Sept. 4, 2025](https://www.emarketer.com/content/j-crew--shein--skechers-slammed-flawed-ai-ad-campaigns). Opened (by direct download) and read. | US. A short secondary summary; it names no defect for Skechers and gives no source for that claim. |

**Read only through summaries (not used in the fix):** a search summary said a Newfoundland and Labrador minister called a six-fingered woman in an RSV vaccine ad "a mistake" (VOCM, May 4, 2026); the page returned 403. A search summary said McDonald's Netherlands removed an AI holiday ad in December 2025; we did not open it, and the reported problem was tone, not a defect.

**What no source shows.** No opened source measures whether a fast correction reduces harm, or compares apology wordings. The response rules below are our judgment, shaped by the contrast between Wow Media's prompt removal and apology and the silent or vague replies in other cases.

## 5. The fix
**The principle:** Anything in an ad that exists in the real world gets checked against the real world before launch, and once a defect is public, the brand pulls every copy and says plainly what went wrong.

**Do this: before launch (pre-flight)**
1. **List the real things in the ad.** For each AI-made or AI-edited ad asset, list every landmark, the product being sold, logos, visible bodies and all text. Each item gets a reference: a licensed photo, the product spec photo, the logo file or the approved copy.
2. **Match count and shape to the reference.** Towers, spires and arches are counted; product parts (handlebars, wheels, chains, buttons, straps) are counted against the spec photo; text matches the approved copy letter for letter. Any mismatch fails the asset.
3. **Check bodies where they meet things.** At full size, check feet and ankles for direction, and every hand that touches an object (handlebars, cups, phones) for fingers merging into it. The general zone checklist is in [image visual artifacts](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md); use it too.
4. **Check every variant, placement and shot.** Each crop, size and platform variant is checked, not only the master file. For video, each shot is checked at reduced speed for bodies, faces and objects that change between frames.
5. **Swap in a real photo after a second failure.** If a landmark or the product fails the reference check twice, use a licensed or real photo for that element instead of regenerating again; repeated edits add artifacts (see [artifact accumulation](../../generation-artifacts/failures/artifact-accumulation.md)).
6. **Second reviewer for big or public placements.** Billboards and other out-of-home ads, ads for public agencies, and paid campaigns above a spend line the brand sets get a second named reviewer, who views the asset at full size and at display scale.

**Do this: once a defect is public (response)**
7. **Keep a placement map.** Every asset has a list of where it runs: screens, ad sets, organic posts, email, partner reposts. This list is what takedown works from.
8. **Confirm, then pull everything.** A report naming a defect ("two Arches," "two handlebars") is checked against the file within 1 hour (proposed). If confirmed, every placement on the map is paused or removed the same day, and each removal is logged with a time.
9. **Post a correction where the ad ran.** Within 24 hours (proposed), on the same channels, a statement that names the defect in plain words, says AI made or changed the image if it did, says what was removed, and names the check being added. No denial and no vague label, such as "digital art" for an AI-made image, before the record is checked ([H2](./ai-images-in-ads-published-without-review.md) rule 9).
10. **Do not delete in silence.** Removing a post without a word leaves the screenshots as the only story. Keep the original file and screenshots of each placement for the review.
11. **Feed the review back.** Within one week (proposed), the defect type is added to the reference list or checklist from rules 1 to 3, and the incident record names which rule would have caught it.

**Reference design: incident runbook (one row per step)**
| Step | Owner | Done when | Proposed time limit |
|---|---|---|---|
| Report logged with screenshot and placement | Social lead | Row in incident log | On receipt |
| Defect confirmed against the approved file | Campaign owner | "Confirmed" or "not a defect" recorded | 1 hour |
| Every placement on the map paused or removed | Media buyer, out-of-home vendor | Each row has a removal time | Same day |
| Correction posted where the ad ran | Comms lead, client sign-off | Link logged | 24 hours |
| Check added to pre-flight list | Creative lead | Checklist version updated | 1 week |

**Correction template** (fill from the incident log; do not post before step 2 is "Confirmed")
```
Our Fourth of July billboard showed two Gateway Arches. There is one. The image was made with an AI tool,
and we did not catch the error before it ran. We have taken it down from the billboard and our social
pages. From now on, every landmark and product in our ads is checked against a real photo before launch.
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The check tool reports the failed item first: "Landmark: reference count 1, image shows 2" |
| Offer choices: 2-4 options plus "Something else", free text open | A reference check fails: swap in a real photo, regenerate once, something else |
| Admit uncertainty and show how to check | The tool cannot tell a hand from a glove or a shadow: it shows the crop and asks the reviewer |
| Hand off to a person | A defect is reported after launch, or a second reviewer is required |

**Don't over-correct.** Stylized or fantasy art that nobody could read as the real building or product needs no reference check. A comment joking "AI made this" is not a defect report; confirm against the file before pulling anything. Do not post a correction for a defect that is not confirmed, and do not pull a whole campaign when one variant is wrong. Criticism of AI use itself, with no defect named, belongs to the backlash pattern, not this runbook.

**Hand-off rule.** A confirmed defect in a live ad goes to the campaign owner and the comms lead with the screenshot, the approved file and the placement map. For agency work, the client approves the correction before it is posted. The ad stays down until the owner signs off on a fixed version.

**Framework used:** none yet. Rules 2 and 5 answer the extra-tower and two-handlebar cases; rules 7 to 10 are our judgment from the response contrast in section 4.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-mistakes-in-ads-go-viral.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Skyline ad with an extra tower | Reference check fails before launch | 1, 2 |
| 2 | Bike ad with a second set of handlebars | Fails against the spec photo | 2 |
| 3 | Model's ankle points backward | Flagged at full size | 3 |
| 4 | Master file clean, Stories crop shows a sixth finger | Crop flagged | 4 |
| 5 | Landmark fails twice | Real photo swapped in | 5 |
| 6 | Billboard with one reviewer | Held for second reviewer | 6 |
| 7 | Confirmed defect report on one post | Every placement on the map removed same day | 7, 8 |
| 8 | Draft reply denies AI use before checking | Blocked; correction names the defect | 9, 10 |
| 9 | Comment "lol AI" with no defect, file matches | Ad keeps running | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Escaped defect rate** (primary) | 0 (proposed) | Incident log: AI ad assets with a confirmed defect first reported after publish / all published AI ad assets, monthly | Any |
| Reference-check coverage | 100% (proposed) | Asset log: AI ad assets with a reference-check record / all AI ad assets | Under 100% |
| Time from confirmed report to last placement removed | Same day (proposed) | Incident log: confirm time to latest removal time | Over 24 hours |
| Corrections posted within 24 hours of confirmation | 100% (proposed) | Incident log: correction link time | Any missed |
| Incidents with a checklist update within a week | 100% (proposed) | Checklist version history joined to incident log | Any missed |
| Ads pulled with no confirmed defect (counter-metric) | Under 10% of pulls (proposed) | Incident log, monthly | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Comments name a count or body part ("two Arches," "three hands," "foot is backwards") | Ad and post comment feeds | A joke about a real photo; check the file |
| Screenshots of the ad shared from accounts outside the brand | Social listening for brand name plus "AI" | Fans sharing the ad because they like it |
| An AI ad asset published with no reference-check record | Asset log vs. publish log | Checked in a tool that does not write to the log |
| A placement still live after the incident is marked "removed" | Placement map vs. live capture | Cached thumbnail, not a live ad |
| A trade or news outlet asks for comment about an ad | Press inbox | A request about an unrelated campaign |

**Starter rule:** no AI-made or AI-edited ad runs until every landmark, product and body in it has passed a reference check, and a confirmed public defect is removed everywhere the same day.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-mistakes-in-ads-go-viral
runs: [pre_publish, post_publish]
reads: [asset.real_items, asset.references, asset.variants, reference_check.record, placement_map, comments, incident_log]
trigger: reference check fails, an AI ad asset has no check record, or a defect report names a count or body part
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Swap in a real photo", "Regenerate once and recheck", "Something else"]
on_miss: block_publish_or_open_incident
metric: escaped defect rate
counter_metric: ads pulled with no confirmed defect
status: proposed
```

## 8. Related patterns
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the sibling page, which also uses the REI ad. It covers who approved which version, platform AI edits after approval, and disclosure. This page assumes an AI image was approved on purpose and covers whether its visible content matches reality, and what to do once a mistake is public.
- [AI images with extra fingers and garbled text posted by mistake](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md) - the closest existing page: a general zoomed checklist for hands, text and edges before any post. This page adds reference checks for real landmarks and products, variant and video checks for ad campaigns, and the takedown and correction runbook.
- [AI product images show features the product does not have](./ai-product-images-show-features-it-does-not-have.md) - a deliberate or unchecked feature claim; here the defect is an obvious glitch, not a believable false feature.
- [Artifact accumulation](../../generation-artifacts/failures/artifact-accumulation.md), [consistency failure](../../generation-artifacts/failures/consistency-failure.md) and [semantic shift](../../generation-artifacts/failures/semantic-shift.md) - why the defects occur in the model.

## 9. Common questions
### Why did the AI billboard show an extra Petronas tower?
The generator draws what skylines usually look like, not a count of this one. Malay Mail reports the agency apologized and removed the billboard. Count every landmark against a real photo before launch.

### What should a brand do when its AI ad goes viral for a mistake?
Confirm the defect against the file, pull every placement the same day, and post a short correction where the ad ran that names the mistake and the new check. Do not delete in silence.

### Should the apology say the image was made with AI?
Under this page's rules, yes, if it was. J.Crew's "digital art" caption drew criticism for not saying AI. Check the asset record before saying anything.

### How do I check an AI ad image before it runs?
List every real building, product, logo, body and line of text in it, and compare each with a real photo, spec or approved copy. Check every crop and, for video, every shot.

### Is it OK to blame the ad platform's AI tool?
Say what happened if the record shows it, as REI did, but own the fix: what was removed and what check is now in place.
