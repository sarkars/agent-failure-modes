# AI Image Extra Fingers and Wrong Hands: Check Every Hand Before You Publish

<!-- SEO
title: AI Image Extra Fingers and Wrong Hands: How to Catch Them
description: AI images often show six fingers, extra limbs or fused body parts. Check every visible hand before publishing, fix only that region and re-check each edit.
search phrases:
- ai image extra fingers
- why does ai draw hands wrong
- ai generated hands six fingers
- how to fix ai hands
- stable diffusion bad hands fix
- midjourney hands wrong
- ai image extra limbs
- ai photo edit added a finger
-->

**Frequency**: Common

## Issue: AI image tools, and AI edits of real photos, often give people six fingers, missing fingers, extra limbs or body parts fused together, and a team that looks only at the whole picture publishes it. Check every visible hand and limb at full size before anything goes out, fix only the broken region, and check again after every edit, crop or resize.

> **One line:** A Phoenix clinic uses an AI tool to roll up the sleeve in a stock photo for a flu shot post, and the woman ends up with six fingers; the fix is to treat every visible hand as something to count, fix the hand region alone when it is wrong, re-check after each AI edit and have a named person sign off with the check recorded.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. All opened studies and the incident are still images, including an AI-edited photo. The goal also covers video, but no opened source measures hands or limbs in AI video. |
| **Channel** | Text-to-image tools, AI editing features inside photo editors, and assistants that call them, used for social posts, ads, health and public notices, listings and stock-style photos |
| **Stakes** | Medium. A six-fingered hand tells viewers the image is AI and fake, which undercuts a health notice or a brand (our judgment, supported by the incident and the political ad in section 4). |
| **Who is affected** | People who see the post or ad, the organization whose name is on it, and the team that published it |
| **Frequency** | Common in tests: a 2025 benchmark found nearly 50% of human images from four current models had distortions (section 4). No opened source gives a rate in published business images. |
| **Pattern ID** | ai-image-generator-wrong-hands-fingers-and-anatomy |
| **Family** | [AI Image Artifacts: Hands, Anatomy and Physics](../README.md) |
| **Goal** | AI images and video show bodies, objects and motion that could exist: correct hands and anatomy, shadows and reflections that match, and physics that holds. |
| **Primary metric** | Unchecked-or-defective anatomy publish rate: published AI-made or AI-edited images showing people, where no anatomy check was recorded or a later review finds a wrong hand, limb or fused body part, divided by all such published images. Proposed starting target: 0. |
| **Maturity** | Researched; tests written, not yet run. Evidence is four papers (three arXiv preprints, one ECCV 2024 paper), one trade-press incident report, two explainer articles and one tertiary reference entry. |
| **Will a better model fix this?** | Partly. Newer tools are reported to be better at hands, but in a 2025 test only Stable Diffusion 3.5 of four current models produced undistorted humans more than half the time, so a check is still needed (our judgment, drawing on section 4). |
| **Also searched as** | AI six fingers · AI hands look weird · extra arm AI photo · AI generated image deformed hands · Photoshop AI added finger |

Tests: [AI image generator wrong hands, fingers and anatomy test file](../../../tests/ai-image-generator-wrong-hands-fingers-and-anatomy.md).

## 1. In plain words
A clinic wants a photo of an older woman with a bandage on her arm. The marketer asks an AI tool to roll up her sleeve. The picture looks fine on a phone screen, so it goes up. Commenters zoom in: she has six fingers on one hand. Now the post is about the clinic's sloppy AI, not the flu shot. Nobody counted the fingers, and nobody looked again after the edit.

## 2. What it looks like
The clinic, people and files below are invented.

**Without the fix**
```
Marketer:  Take stock photo 2207 and roll up her left sleeve so the bandage shows.
Assistant: Done. Here is the edited photo. (Her right hand now has six fingers.)
Marketer:  Perfect, scheduling it for the flu shot post at 9 a.m.
           (Next morning)
Commenter: Count her fingers. Did a robot make this? Why would I trust your shots?
Marketer:  Deleting it now. How did nobody see that?
```
**With the fix**
```
Marketer:  Take stock photo 2207 and roll up her left sleeve so the bandage shows.
Assistant: Done. The photo shows people, so I checked hands and limbs at full size.
           Left hand: 5 fingers. Right hand: 6 fingers, added by the edit.
           I fixed only the right-hand region and checked again: 5 fingers, 2 arms,
           sleeve and arm no longer merge.
           Options: use the fixed version; use the original photo with the sleeve down;
           crop to the shoulder and bandage; something else.
Marketer:  Use the fixed version.
Assistant: Sent to Maya Chen (communications) to recount hands and approve before 9 a.m.
```
The fixed version checks every visible hand after the edit, names the defect, repairs only that region, re-checks, offers other ways out and ends with a person signing off.

## 3. Why it happens
- **Hands are complicated and leave little room for error.** HandRefiner's authors note a hand model has "16 joints and 27 degrees of freedom," so a hand that is slightly off looks wrong at once.
- **A hand is a 3D object drawn in 2D.** Fingers hide each other, so training photos show "varying numbers of fingers and different shapes" by pose and angle (HandRefiner). UCL's Peter Bentley told BBC Science Focus that these tools have "absolutely no concept of the three-dimensional geometry" of a hand.
- **Hand training data is limited.** RHanDS points to "the limited style diversity in existing hand image datasets," and HandRefiner says its own fix struggles with intertwined fingers for the same reason.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Diffusion models "suffer from generating accurate human hands, such as incorrect finger counts or irregular shapes." The paper's examples come from Stable Diffusion, SDXL and Midjourney. Its fix repaints only the hand region and leaves "other parts of the image untouched." | [Lu et al., "HandRefiner," arXiv 2311.17957](https://arxiv.org/abs/2311.17957) (v1 Nov 29, 2023; v2 Aug 16, 2024). Abstract and HTML full text opened Oct 29, 2026. | Preprint. Authors note it may fail on intertwined fingers and very small hands. |
| "Typical malformations of generated hands include irregular hand shapes and incorrect numbers of fingers." | [Wang et al., "RHanDS," arXiv 2404.13984](https://arxiv.org/html/2404.13984v1) (April 22, 2024). HTML opened Oct 29, 2026. | Preprint; describes the problem, gives no rate. |
| Distortion-5K: 4,700 annotated images of normal and malformed people, with flaws such as "proliferated limbs, missing fingers, deformed extremities, or fused body parts." On a 500-prompt benchmark, "nearly 50%" of images from Stable Diffusion 3.5, Flux.1-dev, Recraft v3 and Hunyuan Image had distortions; only SD 3.5 had an undistorted rate above 0.5. | [Ma et al., "Evaluating and Predicting Distorted Human Body Parts for Generated Images," arXiv 2503.00811](https://arxiv.org/abs/2503.00811) (March 2, 2025). Abstract and HTML full text opened Oct 29, 2026. | Preprint. The rate is scored by the authors' own detector, not by people. Four models only. |
| Same paper: asked to tell distorted from normal human images, GPT-4o scored an image-level F1 of 0.246; the authors report it called a hand clearly showing six fingers a five-fingered hand. Their trained detector reached F1 0.899 on locating distortions. | Ma et al., as above. | One prompt design for GPT-4o; newer vision models not tested. The detector is the authors' own and not released at the time of the paper. |
| AbHuman: 56K generated human images with 147K labeled anomalies in 18 categories; models "usually struggle with accurately rendering images featuring humans, resulting in distorted limbs." Refining with HumanRefiner gave "a 2.9x improvement in limb quality" over SDXL and 1.4x over DALL-E 3 in human evaluations. | [Fang et al., "HumanRefiner," ECCV 2024](https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/4696_ECCV_2024_paper.php). Abstract opened Oct 29, 2026. | Abstract only. The authors' own method and evaluation. |
| A 2024 North Carolina political ad showed a candidate as an "AI monstrosity" with 14 fingers. | [Geoff Brumfiel, NPR, via Texas Public Radio, Sept 16, 2026](https://www.tpr.org/2026-09-16/as-campaign-season-gears-up-ai-generated-ads-are-everywhere). Opened Oct 29, 2026. | Deliberate, not an error. Used only to show that extra fingers are read as a sign of AI. |
| Midjourney V5 was reported as "creating hands with the correct amount of fingers," something earlier versions "struggled to create." | [Corbin Davenport, How-To Geek, March 16, 2023](https://www.howtogeek.com/879711/midjourney-v5-creates-better-images-fewer-nightmare-hands/). Opened Oct 29, 2026. | Anecdotal: based on demo images posted by one user, not a Midjourney statement or a test. |
| Stable Diffusion "experiences issues with hands and teeth," and the entry suggests prompting the subject to hide hands or not show teeth. | [EBSCO Research Starters, "Stable Diffusion"](https://www.ebsco.com/research-starters/computer-science/stable-diffusion). Opened Oct 29, 2026. | Tertiary reference entry, undated, and the only source for teeth. Weak: teeth are not part of the fix below. |

**Incident (Canada):** On May 6, 2026, HRD Canada reported that a vaccination post on the Government of Newfoundland and Labrador's Facebook page showed an older woman with six fingers on one hand and a sleeve both rolled up and covering her forearm. A government statement reported by CBC said the AI component in Photoshop, "used for editing and re-sizing photos," distorted the image and the error "was not captured in the reviewing process"; the post was taken down, and Premier Tony Wakeham said, "We have to tighten up how government deals with AI." Source: [Jim Wilson, HRD Canada, May 6, 2026](https://www.hcamag.com/ca/specialization/transformation/6-fingers-nl-premier-vows-crackdown-on-ai-use-after-faulty-vaccine-image/574237), crediting CBC; opened Oct 29, 2026. Phase-1 notes cite [VOCM, May 4, 2026](https://vocm.com/2026/05/04/ai-generated-image-with-six-fingers-a-mistake-says-minsiter/) describing it as an RSV vaccine ad; that page returned 403 in this run and is not used for details. No US accidental incident was opened: the search "company apologizes AI generated ad extra fingers hands 2025 2026 United States" returned non-US cases only.

## 5. The fix
**The principle:** A hand in a published image is something you count, the same way you proofread a phone number. And an AI edit is a new image, so it gets counted again.

**Do this: teams and assistants that make or edit images showing people**
1. **Flag every image that shows people.** Any AI-made image, or real photo changed by an AI tool, with a visible hand, arm, leg or foot is marked "anatomy check" before anyone shows it as final.
2. **Check each visible hand and limb at full size.** Count fingers per hand (five, one of them a thumb), count arms and legs per person, and look where bodies touch clothing, objects or other people for fused or merged parts. Record the result per image.
3. **A person makes the final check.** A detector may pre-screen (proposed), but not as the only check: in Distortion-5K, GPT-4o missed most distorted images and read a six-fingered hand as five.
4. **Fix only the broken region.** Repaint or refine the hand or limb area and leave the rest of the approved image alone, as HandRefiner does; then check again. Stop after a limit the team sets (3 tries is our proposed starting point) and say what each try produced.
5. **After the limit, change the picture, not the facts.** Offer a real photo, the original unedited photo, a crop or pose that keeps hands out of frame, or a different shot. Do not crop out a hand that the image is about (a hand holding the product).
6. **Re-check after every AI edit, crop, resize or new format.** Each new version gets its own anatomy check, including platform resizes and "small" fixes to a real photo.
7. **A named person signs off.** Ads, social posts, public and health notices, and listings with people need a recorded anatomy check and approval before publish.
8. **Log it.** Per image: version, hands and limbs checked, defects found, fix method and tries, checker, approver and date.

**Reference design: anatomy check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Image type | People visible, flagged | Edited stock photo 2207 flagged |
| Hands | Fingers counted per visible hand | L 5, R 6 then 5 after fix |
| Limbs and joins | Arms and legs counted; no fused parts | 2 arms; sleeve and arm separate |
| Fix method | Region only, within the try limit | Right hand repainted, 1 try |
| Version | Check done on the exact file that runs | 1080x1080 post file |
| Sign-off | Named, dated | M. Chen, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every image with people: give the anatomy result (fingers per hand, defects found) before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | A defect remains after the try limit: real photo, original photo, crop or new pose, something else. Do not offer them when the check passed. |
| Ask one clarifying question | It is unclear whether hands matter to the shot: "Does her hand need to show the bandage, or can we crop to the shoulder?" |
| Hand off to a person | Always for the final anatomy check and sign-off on anything published |

**Don't over-correct.** Do not flag images with no people or animals in them. Do not mark a hand as wrong because an object or another hand hides some fingers; natural overlap is not a defect, but count what is visible. Do not apply photo rules to a style that draws hands simply on purpose (a cartoon mascot with four fingers, anime hands without joints); judge it by the style guide. Do not crop every hand out of every image as a reflex, and do not regenerate a whole approved image to fix one finger.

**Hand-off rule.** If anyone reports a wrong hand, limb or body part in a published image, the content owner pulls every copy the same day and sends the log to the approver. The [viral ad mistakes page](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) covers the public correction.

**Framework used:** none yet. Rule 3 follows Distortion-5K's GPT-4o result; rule 4 follows HandRefiner and HumanRefiner, which repair the region rather than the whole image; rule 6 follows the Newfoundland and Labrador incident, where an AI edit to a photo added the finger; rules 1, 2, 5, 7 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-wrong-hands-fingers-and-anatomy.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Generated photo of a barista handing over a cup | Flagged; fingers counted per hand | 1, 2 |
| 2 | AI sleeve edit adds a sixth finger | Caught on the edited version; region fixed and re-checked | 4, 6 |
| 3 | Only a vision model checked the image | Publish blocked until a person checks | 3, 7 |
| 4 | Three region fixes all fail | Stops; options offered | 4, 5 |
| 5 | 9:16 crop made after approval | Re-checked before it runs | 6 |
| 6 | Product shot of a lamp, no people | Not flagged | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked-or-defective anatomy publish rate** (primary) | 0 (proposed) | Monthly sample of published AI-made or AI-edited images with people: no anatomy check in the log, or a reviewer finds a wrong hand, limb or fused part / all sampled | Any |
| Versions published without their own check | 0 (proposed) | Publish log: file version that ran vs version with a recorded check | Any |
| Region-fix tries per flagged image | Track, no target | Generation log: tries before a pass or the switch to another picture | Rising for 2 months |
| False anatomy flags (counter-metric) | Track, no target | Sample of flagged images marked "no defect" because of natural overlap or an intended style | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Image with people published with no anatomy check field | Generation log plus publish log | No people are visible; the person flag was wrong |
| AI edit applied to an approved photo and the new version published without a new check | Editor history plus publish log | The edit was color only, logged as such, and a check was still recorded |
| Comments or replies on a post mention "fingers," "six," "extra arm" or "AI" | Social comments, support inbox | A deliberate parody or styled image |
| Post deleted or ad paused within 48 hours of going live | Platform activity log | A scheduled end date or a wording fix |

**Starter rule:** no AI-made or AI-edited image showing people is published unless the log shows an anatomy check on that exact version and a named person's sign-off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-wrong-hands-fingers-and-anatomy
runs: [post_generation, post_edit, pre_publish]
reads: [image.people_visible, image.version, image.ai_edited, check.fingers_per_hand, check.limbs_per_person, check.fused_parts, fix.method, fix.tries, review.checker, review.signoff, style.intended_simplified]
trigger: people visible and no anatomy check on this version, or defect found, or try limit reached, or no sign-off at publish
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Use a real or original photo", "Crop or repose so hands are out of frame", "Try a different shot", "Something else"]
on_miss: block_publish
metric: unchecked-or-defective anatomy publish rate
counter_metric: false anatomy flags
status: proposed
```

## 8. Related patterns
- [AI ad mistakes that go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) - the closest existing page. It covers the business side once a defective ad is public (reference checks for landmarks and products, pulling and correcting the ad); this page is the anatomy defect itself and how to catch and fix it in the workflow before it runs.
- [AI images in ads published without review](../../ai-image-generation-business-risks/failures/ai-images-in-ads-published-without-review.md) - the missing sign-off and platform auto-edits that let a defect ship; this page says what the reviewer checks on bodies.
- [Quality drift in generated images](../../generation-artifacts/failures/quality-drift.md) - the older page on images getting worse over many steps; a wrong hand appears in the first image or after one edit.
- [AI image generator wrong number of objects](../../ai-image-prompt-adherence/failures/ai-image-generator-wrong-number-of-objects.md) - the same "count it before you publish" idea for objects the prompt numbered; fingers are counted even when the prompt never mentions them.

## 9. Common questions
### Why does AI give people six fingers?
A hand has many joints and fingers that hide each other in photos, so the tool sees different finger counts in its training images and has no 3D model of a hand. Researchers behind HandRefiner and RHanDS name hand structure and limited hand data as the main causes.

### How do I fix bad hands in an AI image?
Repaint only the hand area with your tool's inpainting or region edit, then count the fingers again. If a few tries fail, use a real photo or pick a crop or pose where hands are not the focus.

### Can AI-edited real photos get extra fingers too?
Yes. In the Newfoundland and Labrador case, the government said the AI component in Photoshop, used for editing and resizing, distorted a photo and the woman ended up with six fingers. Check every edited version, not just fully generated images.

### Can I use an AI model to check the hands for me?
Only as a first screen. In one 2025 test, GPT-4o missed most distorted human images and called a six-fingered hand five-fingered, so a person should check anything you publish.

### Are newer AI image generators fixing hands?
Some are better: How-To Geek reported Midjourney V5 drew correct finger counts more often. But a 2025 benchmark still found nearly half of human images from four current models distorted, so keep the check.
