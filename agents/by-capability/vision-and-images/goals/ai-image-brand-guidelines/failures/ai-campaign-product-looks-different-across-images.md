# AI Product Looks Different in Every Shot: Keeping a Brand's Product Consistent Across an AI Campaign

<!-- SEO
title: AI Product Looks Different in Every Image? Keep One Product Across an AI Campaign
description: In an AI campaign the product changes from image to image and shot to shot. Build every frame from one approved product reference and check the whole set.
search phrases:
- ai product looks different in every image
- keep product consistent across ai images
- coca cola ai ad trucks different wheels
- ai video product changes between shots
- consistent product in ai generated campaign
- reference image product consistency ai video
- ai ad product shape changes
- same product in every midjourney image
-->

**Frequency**: Unknown

## Issue: A brand makes a campaign's images or video shots with AI, and its own product changes from one image or shot to the next (a different wheel count, cap, label or shape), and the set ships because each piece was checked on its own. Build every image and shot from the same approved product reference, either composited from real product files or conditioned on one locked set of reference images, and approve the campaign only after every image and sampled frame is checked side by side against a written product spec.

> **Read this first:** This page summarizes news reports and vendor documentation as we read them on October 29, 2026. It makes no claim about advertising or consumer-protection law. Whether an AI image that shows the product inconsistently could mislead buyers is a legal question this page does not answer; it needs review by a qualified person. The rules below are workflow choices.

> **One line:** A Minneapolis water-bottle brand ships 12 AI social images and a 15-second AI video, and the bottle has a flip cap in some, a two-tab cap in others and a handle in half; the fix is a product spec card with countable features, every image built from the same approved product files or references, and one reviewer who signs off on a contact sheet of the whole set, not image by image.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The opened Coca-Cola and Toys "R" Us cases are video; the OpenAI limitation is about still images across generations, and Google's reference feature is for video. |
| **Channel** | Text-to-image and text-to-video generators, AI ad studios and agencies, and the assistants and design tools that produce multi-image or multi-shot campaigns |
| **Stakes** | Medium. The brand's own product is the one thing a campaign must get right; when it changes between shots, viewers notice and it becomes the story (our judgment, from the Coca-Cola coverage in section 4). |
| **Who is affected** | The brand owner, its customers, the agency or staff member who made the set, and the brand reviewer |
| **Frequency** | Unknown. No opened source gives a rate. Two public cases were opened (section 4). |
| **Pattern ID** | ai-campaign-product-looks-different-across-images |
| **Family** | [AI Images That Break Brand Guidelines](../README.md) |
| **Goal** | AI images and video a brand publishes follow its brand guidelines: the right logo, colors, fonts, tone and product, nothing from another brand, and nothing unsafe next to its name. |
| **Primary metric** | Product-mismatch rate: published campaign images and video shots whose product fails any check on the product spec card, divided by all sampled images and shots. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is three news reports on one ad, one news report on another, and two vendor documentation pages. |
| **Will a better model fix this?** | Partly. Reference-image inputs help, but each image or shot is still a new sample, and OpenAI's own guide says its model may still struggle with recurring brand elements. Someone still has to check the set. (Our judgment, not tested.) |
| **Also searched as** | AI truck has different wheels · product changes shape in AI video · Sora continuity · consistent packshot AI · same product every scene AI |

Tests: [AI campaign product looks different across images test file](../../../tests/ai-campaign-product-looks-different-across-images.md).

## 1. In plain words
A brand runs one campaign: a dozen social images, a few banner sizes and a short video. Each piece is generated on its own. Each one looks good on its own, so each one gets approved on its own. Put them side by side and the product is not the same product: a truck has four wheels in one shot and six in the next, a bottle's cap changes, the label moves. The customer sees the campaign as a set, even when the review did not.

## 2. What it looks like
The company, people, files and product below are invented.

**Without the fix**
```
Coordinator: Make 12 Instagram images of our Trailhead 32 oz bottle at lakes, campsites
             and trailheads, plus a 15-second video, same bottle in all of them.
Assistant:   Done: 12 images and a 6-shot video. (Each was generated from the text prompt.)
Reviewer:    Approved, one at a time, in the ad tool.
Customer (comment, week 2): Which one is the real bottle? Half have a handle and the cap keeps changing.
Brand lead:  Image 4 has a flip cap, image 9 a two-tab cap, and video shot 3 has no logo panel.
```
**With the fix**
```
Coordinator: Make 12 Instagram images of our Trailhead 32 oz bottle at lakes, campsites
             and trailheads, plus a 15-second video, same bottle in all of them.
Assistant:   I'll use product spec card TH32 v3: two-tab cap, no handle, logo panel front
             center, Pine Green. Close-ups use the real packshot composited in; wide shots are
             conditioned on the same three reference photos (TH32-front, -side, -cap).
             Check result: 11 images pass. Image 7 shows a handle, so I'll repaint that area
             from the packshot and re-check it. Video: 3 frames per shot checked, all pass.
             Contact sheet of all 12 images and 18 frames goes to Maya Chen (brand) for set sign-off.
```
In the fixed version the product comes from the same files every time, every image and shot is checked against the same written features, and a person approves the set as a set.

## 3. Why it happens
- **Every image and shot is a new sample.** Nothing in a normal generation carries the product from one output to the next. OpenAI's image guide lists, as a limitation, that its model "may occasionally struggle to maintain visual consistency for recurring characters or brand elements across multiple generations." Il Sole 24 Ore, citing the Daily Mail, put the Coca-Cola trucks down to video models losing continuity, which it called 'time drift'.
- **The product is described in words, not supplied as files.** Text leaves the product's details for the model to fill in again each time. Vendors offer a way to pass the real product in: OpenAI says "You can use one or more images as a reference to generate a new image," and Google's Veo page says "You provide up to three images of a single person, character, or product." When the reference set changes between shots, or is skipped, the product changes too.
- **Review is per asset, not per set.** Shots are picked one at a time from many tries: the Toys "R" Us team described "condensing hundreds of iterative shots down to a couple dozen." A reviewer who sees one image or shot at a time cannot see that shot 3 and shot 7 disagree (our judgment about the cause; the sources report the result, not the review process).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Viewers of Coca-Cola's 2025 AI remake of "Holidays Are Coming" (made with AI studio Silverside) pointed out "visual inconsistencies linked to the appearance of the trucks": in some shots "an extra row of wheels in the middle," in others three wheels clustered where two had appeared. "Coca-Cola declined to comment on the creative inconsistencies." Video. | [Campaign, Shannon Miller, Nov 5, 2025](https://campaignlive.com/article/coca-cola-reignites-ai-ad-debate-new-holiday-campaign/1938664). Opened Oct 29, 2026 (page fetched directly); quotes string-matched. | Describes viewer observations; Campaign did not count shots itself. Coca-Cola said the 2024 film "performed exceptionally well," so no harm to sales is shown. |
| The trucks "seem to change shape" and "move their wheels from one shot to the next"; the article says generative video models "fail to keep characters and objects consistent across multiple takes." | [Il Sole 24 Ore, Nov 6, 2025](https://en.ilsole24ore.com/art/coca-cola-christmas-ad-made-l-ai-and-error-hunt-started-AHP0vaaD). Opened Oct 29, 2026; quotes string-matched. | Italian outlet, English text "Translated by AI." It credits the ad to Secret Level, while Campaign credits the trucks spot to Silverside and a "Fantastical" version to Secret Level. Its cause is relayed from the Daily Mail, which we did not open. |
| TechRadar's review of the 2025 ad said "the mix of styles remains inconsistent," and recalled the 2024 version's "flickering wheels, awkward lighting and uncanny humans." It also said the 2025 wheels "genuinely rotate." Video. | [TechRadar, John-Anthony Disotto, Nov 4, 2025](https://www.techradar.com/ai-platforms-assistants/coca-cola-faces-backlash-again-for-missing-the-spirit-of-the-holidays-with-another-ai-slop-ad). Opened Oct 29, 2026; quotes string-matched. | Opinion review. It is about style, not the product's features, and it credits the wheel rendering as improved. |
| An AI videomaker said the Toys "R" Us Sora film had problems "keeping a character's appearance consistent from scene to scene." The team still needed "some corrective visual effects work." Video. | [Decrypt, Jose Antonio Lanz, June 25, 2024](https://decrypt.co/237017/ai-film-toys-r-us-sora-controversy). Opened Oct 29, 2026; quotes string-matched. | The character is the founder as a boy, not a product; we use it for a brand's own recurring subject. The consistency point is one person's post, paraphrased by Decrypt. |
| OpenAI lists consistency for "recurring characters or brand elements across multiple generations" as a limitation, and supports one or more reference images per generation. | [OpenAI, Image generation guide](https://developers.openai.com/docs/guides/image-generation). Opened Oct 29, 2026; quotes string-matched. | Vendor documentation for its own models; gives no rate. |
| Veo can take up to three reference images of "a single person, character, or product" and the page says it "preserves the subject's appearance in the output video." | [Google Cloud, Generate videos from references](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/video/generate-videos-from-references) (the Vertex AI URL now redirects here). Opened Oct 29, 2026; quote string-matched. | Vendor claim, not tested by us. A reference is a steer; the page gives no accuracy figure. |

**Read through a summary only:** a search summary said a Drum article by Dino Burbidge found only two of 11 truck scenes in the 2025 Coca-Cola ad showed the same wheel layout. The Drum page returned no text when fetched, so these counts are not used anywhere else on this page.

## 5. The fix
**The principle:** One product, one set of source files, one check across the whole set. The generator makes scenes; the product comes from the brand's approved files.

**Do this: brand, marketing and agency teams, and assistants that build multi-image or multi-shot campaigns**
1. **Write a product spec card before generating.** List the product's countable, checkable features (shape, parts and their counts, cap or lid type, label and logo position, colors, proportions) with a version number and the approved photos, packshots or 3D renders.
2. **Never generate the product from words alone.** Every image and shot either composites the real product from the approved files or is conditioned on the same locked reference set named on the spec card. The build log records which.
3. **Use the real product for close-ups.** Where the product is large or the hero of the frame, composite it from the packshot or 3D render rather than relying on a reference-conditioned redraw.
4. **Check every image and every shot against the card.** Count and compare each listed feature. For video, check at least the first, middle and last frame of every shot, since the product can change within a shot.
5. **Review the set side by side.** Approval is given on one contact sheet with all images and the sampled video frames in view, not on single assets.
6. **Fix by edit, not by rerolling the set.** Repair a failing image by repainting or compositing from the approved files. Any regenerated image or shot goes back through rule 4 and onto the contact sheet.
7. **Lock the card and references for the campaign.** New sizes, shots or later flights use the same card version and reference files, and are checked against the approved contact sheet.
8. **A named reviewer signs off and the build is logged.** Log the card version, reference files, generator and version, composite or reference method per asset, the per-asset check result, reviewer and date.

**Reference design: product check on the contact sheet**
| Check | Pass | Example |
|---|---|---|
| Spec card | Named and versioned | TH32 v3 |
| Product source per asset | Composite from packshot, or locked reference set | Image 1-6 composite; video shots reference set A |
| Feature counts | Every listed feature matches in every asset | Two-tab cap, no handle, logo panel front center |
| Video frames | First, middle, last of each shot checked | 6 shots x 3 frames, all pass |
| Fixes | Repaired from approved files and re-checked | Image 7 handle removed, re-checked |
| Set sign-off | Named reviewer on the contact sheet | M. Chen, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request asks for several images or shots of the product and the spec card and files are on hand: say which card and files will be used and how, then build |
| Offer choices: 2-4 options plus "Something else", free text open | No spec card or product files are available: upload product photos, write the card together now, make scenes without the product for now, something else |
| Ask one clarifying question | The card does not settle a variant the request implies: "The 32 oz with the two-tab cap, or the new straw lid?" |
| Hand off to a person | Any asset still fails a feature check after one fix; always for set sign-off |

**Don't over-correct.** Do not demand that scenes, backgrounds, animals, props or lighting match across the set; only features on the spec card are checked. Do not flag a variant the card lists as approved, such as a second color. Do not block an openly stylized version, such as a "fantastical" cut, where the brand has written down which product features may change. Do not gate internal mood boards; the check is at approval and publish.

**Hand-off rule.** If a published campaign shows the product inconsistently, send the affected assets and the build log to the brand owner the same day, and replace or pull every copy of the failing images and shots. The brand owner decides whether to say anything publicly.

**Framework used:** none yet. Rules 2 and 3 follow the OpenAI and Google reference-image documentation; rules 4 and 5 answer the Coca-Cola truck reports; rule 6 follows the Toys "R" Us account of shot selection and corrective effects; rules 1, 7 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-campaign-product-looks-different-across-images.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Request for 12 images with no spec card | Card written or requested before generation | 1 |
| 2 | Product described only in the text prompt | Composite or locked references used | 2 |
| 3 | Hero close-up of the product | Real packshot composited | 3 |
| 4 | One image shows an extra part | Caught by feature check | 4 |
| 5 | Product changes inside one video shot | Caught by first/middle/last frame check | 4 |
| 6 | Each asset approved alone in the ad tool | Blocked until contact-sheet sign-off | 5 |
| 7 | New banner size added in week 3 | Same card and references; checked against sheet | 7 |
| 8 | Backgrounds differ across the set | Not flagged | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Product-mismatch rate** (primary) | 0 (proposed) | Weekly sample of published campaign images and video shots checked against their spec card / all sampled | Any |
| Assets with no product source logged | 0 (proposed) | Build log field "composite or reference set" empty / all assets | Any |
| Campaigns approved without a contact sheet | 0 (proposed) | Sign-off log joined to campaign list | Any |
| Assets added after set approval and not re-checked | 0 (proposed) | Publish log dates vs. contact-sheet version | Any |
| Allowed-variation false flags (counter-metric) | Under 10% of flags (proposed) | Monthly review of flags the reviewer overrode | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A feature count (wheels, caps, handles) differs between assets in one campaign | Per-asset check results or reviewer tags | The card lists two approved variants |
| A product crop scores low similarity to the reference set compared with the rest of the set | Pre-approval image check | Extreme angle, motion blur or partial view |
| An asset's build log has no reference set or composite layer | Build log | The asset is a scene with no product in it |
| An asset is published with a card version older than the campaign's | Publish log | An approved earlier flight re-run on purpose |

**Starter rule:** no campaign asset showing the product is published unless its build log names the spec card, the product source and a passing feature check, and it appears on a signed contact sheet.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-campaign-product-looks-different-across-images
runs: [pre_generation, pre_approval, pre_publish]
reads: [request.text, campaign.spec_card.version, campaign.spec_card.features, campaign.reference_files, asset.product_source, asset.feature_check, asset.video_frames_checked, contact_sheet.signoff, publish.card_version]
trigger: multi-asset request with no spec card, or asset with no product source, or any feature check fails, or video shot missing frame checks, or no contact-sheet sign-off, or card version mismatch
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Upload product photos", "Write the spec card now", "Make scenes without the product for now", "Something else"]
on_miss: block_publish
metric: product-mismatch rate
counter_metric: allowed-variation false flags
status: proposed
```

## 8. Related patterns
- [Consistency failure](../../generation-artifacts/failures/consistency-failure.md) - the closest existing page: any subject losing its identity across generations, from the model's side. This page is narrower and operational: the brand's own product across one campaign's set of images and video shots, checked against a written spec and approved as a set. A merge of the two is proposed for a person to decide.
- [AI images break brand logo, color and font rules](ai-images-break-brand-logo-color-and-font-rules.md) - one asset breaking the brand guide; this page is the product disagreeing across assets.
- [AI image model update changes the approved style](../../ai-image-generation-business-risks/failures/ai-image-model-update-changes-approved-style.md) - the look shifting when the vendor's model changes; here the product shifts within one campaign, with or without an update.
- [Approved AI image cannot be reproduced](../../ai-image-generation-business-risks/failures/approved-ai-image-cannot-be-reproduced.md) - why rule 6 edits rather than regenerates.
- [AI product images show features it does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - the product shown wrong against reality; this page is the product shown differently against itself.
- [AI ad mistakes that go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) and [AI ads backlash for replacing artists](../../ai-image-generation-business-risks/failures/ai-ads-backlash-for-replacing-artists-with-ai.md) - what happens after a flawed AI ad airs; the second covers the Coca-Cola and Toys "R" Us backlash about artists.
- [Artifact accumulation](../../generation-artifacts/failures/artifact-accumulation.md) - errors building up over long generations. A planned AI video consistency goal will cover video shots more fully.

## 9. Common questions
### Why does my product look different in every AI image?
Each image is generated fresh, and a text prompt leaves the details to the model each time. Give the model the same product photos for every image, or place the real product in, and check the set side by side.

### How do I keep the same product across AI video shots?
Use reference images of the product on every shot, keep the same reference set for the whole campaign, and check the first, middle and last frame of each shot against a list of the product's features.

### What went wrong with the Coca-Cola AI trucks?
Viewers spotted the trucks' wheels changing between shots of the 2025 holiday ad, according to Campaign and Il Sole 24 Ore. Coca-Cola declined to comment on the inconsistencies to Campaign.

### Do reference images fix product consistency?
They help. Google says Veo keeps a product's appearance from up to three reference images, and OpenAI supports reference images, but OpenAI also lists consistency for brand elements as a limitation. Still check every asset.

### Is it OK if the backgrounds change between images?
Yes. Only the product's listed features need to match. Scenes, lighting and props can change.
