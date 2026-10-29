# AI Image Generator Puts Objects in the Wrong Position: Left and Right, On and Under, In Front and Behind

<!-- SEO
title: Why AI Image Generators Ignore "Left Of," "Under" and "Behind" in Your Prompt
description: Ask an AI image tool for a lamp left of a chair and it may put it on the right. Check each placement in the image before you publish or write copy about it.
search phrases:
- ai image generator ignores left and right
- ai image wrong object placement
- dall-e to the left of not working
- ai image put object behind instead of in front
- midjourney object on top of instead of under
- how to control object position in ai images
- text to image spatial relationships fail
-->

**Frequency**: Unknown

## Issue: Ask an AI image tool for "a floor lamp to the left of a green armchair" or "a rug under the coffee table," and it often draws both objects but puts them in the wrong place: swapped left and right, on instead of under, behind instead of in front. List every placement the prompt asks for, check each one in the generated image, fix or flag any that fail, and check copy that names a position ("lamp on the left") against the final image before anything ships.

> **One line:** A Denver furniture store's marketer asks for "a brass floor lamp to the left of a green armchair, a jute rug under the coffee table" and gets the lamp on the right and the rug on the wall behind; the caption "the lamp on the left is $89" goes out next to it. The fix is to check each requested placement in the image, say which ones failed, offer a fix (flip, edit, rebuild in a layout tool or change the copy), and re-check before sign-off.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. All opened sources test still images. The same per-placement check would apply to frames of AI video, but no opened source measures video. |
| **Channel** | Text-to-image tools, design tools with built-in generators and chat assistants that call them, used by e-commerce, marketing and training teams for product scenes, room layouts, how-to diagrams and ads |
| **Stakes** | Medium. One wrong placement is easy to miss; it matters when copy, a price tag, an instruction or a callout refers to a position that the image does not show (our judgment). |
| **Who is affected** | Shoppers and readers who rely on "on the left" or "behind," and the team that published the mismatch |
| **Frequency** | Unknown. No opened source gives a rate in real business use. Every opened benchmark finds placement errors in controlled tests (section 4). |
| **Pattern ID** | ai-image-generator-puts-objects-in-the-wrong-position |
| **Family** | [AI Images That Ignore the Prompt](../README.md) |
| **Goal** | AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text. |
| **Primary metric** | Unchecked-placement rate: published AI images whose prompt or copy states a placement, with no recorded check of each placement in the final image, divided by all such published images. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is one vendor technical report, one vendor doc page and six research papers (one accepted at ICLR 2026, the rest read as arXiv preprints). No public incident found. |
| **Will a better model fix this?** | Not on its own, so far. OpenAI's DALL-E 3 report says it "still struggles with object placement," OpenAI's current image docs list placement as a limitation, GenEval found no gain on the position task as one model family grew, and 2025-2026 benchmarks still report the problem (section 4). (Our judgment, drawing on the cited sources.) |
| **Also searched as** | AI image left right wrong · object behind instead of in front · AI ignores spatial prompt · DALL-E positioning · AI room layout wrong |

Tests: [AI image generator puts objects in the wrong position test file](../../../tests/ai-image-generator-puts-objects-in-the-wrong-position.md).

## 1. In plain words
The prompt says where things go. The tool draws the things but not always where you said. A lamp asked for on the left lands on the right. A rug asked for under a table hangs on the wall. A dog asked for in front of the sofa sits behind it. The image looks fine, so nobody notices, until the caption, the price tag or the assembly step says "on the left" and the picture shows the opposite.

## 2. What it looks like
The store, people and products below are invented.

**Without the fix**
```
Marketer:  Living room scene for the fall sale: a brass floor lamp to the left of a green armchair,
           a jute rug under the coffee table. Caption: "The lamp on the left is $89."
Assistant: Here's your scene. (One image, presented as matching the prompt.)
Marketer:  Looks great, scheduling the email.
Customer service (two days later): Three customers asked why the "$89 lamp on the left" is a
           side table. The lamp is on the right, and the rug is on the wall behind the chair.
```
**With the fix**
```
Marketer:  Living room scene for the fall sale: a brass floor lamp to the left of a green armchair,
           a jute rug under the coffee table. Caption: "The lamp on the left is $89."
Assistant: Your prompt has 2 placements. I made 4 images and checked each one:
           lamp left of chair: 1 of 4 correct. Rug under table: 2 of 4 correct. Image 3 has both right.
           Use image 3? Other options: flip image 1 (no text or logos in it), edit the rug area,
           change the caption to "the lamp by the armchair," or something else.
Marketer:  Image 3.
Assistant: Image 3 re-checked with your caption: lamp is left of the chair, rug is under the table.
           Sent to Dana Ruiz (merchandising) to approve before the email goes out.
```
The fixed version names each placement, checks each one in each image, says what failed, offers options and ends with a check of the copy and a sign-off.

## 3. Why it happens
- **The training captions rarely said where things were.** OpenAI's DALL-E 3 report says its synthetic captioner "is unreliable at stating object placement, and this is reflected in our downstream models." A model that learned from captions without positions does not reliably follow positions.
- **The first object named pulls ahead.** VISOR found "a bias towards generating the first object mentioned"; GenEval found one model placed the first-named object on the left more often than on the right, "even when the prompts are evenly distributed among all four directions." Word order in the prompt can change the layout.
- **Equivalent wording gives different layouts.** VISOR reports "spatially inconsistent outputs for equivalent relationships": "A left of B" and "B right of A" do not reliably produce the same scene.
- **A bigger model alone did not help.** GenEval saw scores rise with model size on other tasks but "we do not see such an improvement on the position task."
- **Nobody checks the placement.** The objects are present and the image is attractive, so a quick look passes it. The error only shows when someone compares the image to the words.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "While DALL-E 3 is a significant step forward for prompt following, it still struggles with object placement and spatial awareness. For example, using the words 'to the left of', 'underneath', 'behind', etc are quite unreliable." | [Betker et al., OpenAI, "Improving Image Generation with Better Captions" (DALL-E 3 report), section 5.1](https://cdn.openai.com/papers/dall-e-3.pdf). Full PDF opened Oct 29, 2026. | Vendor's own statement about DALL-E 3; no rate given. Undated PDF, released with DALL-E 3 in 2023. |
| OpenAI's current image generation guide lists "Composition Control" as a limitation: the model "may have difficulty placing elements precisely in structured or layout-sensitive compositions." Masked edits "may not follow its exact shape with complete precision." | [OpenAI API docs, Image generation guide](https://developers.openai.com/docs/guides/image-generation). Opened Oct 29, 2026. | Applies to "GPT Image models" as the page states; no rate given. Vendor docs change without notice. |
| On 2D prompts such as "a person below an umbrella," "even the best model in our benchmark generates correct spatial relationships on less than 40% of test cases"; the best model (DALL-E 2) had all four images correct for a prompt in 7.49% of cases. | [Gokhale et al., "Benchmarking Spatial Relationships in Text-to-Image Generation" (VISOR), arXiv 2212.10015](https://arxiv.org/abs/2212.10015) (v3, Oct 27, 2023). Full PDF opened Oct 29, 2026. | Models from 2022-2023 (GLIDE, DALL-E mini, CogView2, DALL-E 2, Stable Diffusion 1.x and 2.1). Do not read these numbers as current. |
| Position task ("above," "below," "to the left of," "to the right of"), scored 0 to 1 with an object detector: from 0.02 (minDALL-E) to 0.15 (SD-XL); IF-XL 0.13. "Position and attribute binding tasks remain difficult overall." | [Ghosh et al., "GenEval," arXiv 2310.11513](https://arxiv.org/abs/2310.11513) (v1, Oct 17, 2023). Full PDF opened Oct 29, 2026. | Open-source models of 2022-2023 only; no commercial tools. Detector-based scoring, checked against human ratings on a subset. |
| Image generators "struggle with specific 3D details like object placement, relationships, and measurements." | [Wang et al., "GenSpace," arXiv 2505.24870](https://arxiv.org/abs/2505.24870) (May 30, 2025). Abstract opened Oct 29, 2026. | Preprint. Abstract only; per-model results not read. |
| After testing 21 models, text-to-image models "often fail in handling complex spatial relationships"; "higher-order spatial reasoning remains a primary bottleneck." | [Wang et al., "Everything in Its Place," arXiv 2601.20354](https://arxiv.org/abs/2601.20354) (Jan 2026, accepted at ICLR 2026). Abstract opened Oct 29, 2026. | Abstract only; the 21 models are not named on the abstract page. |
| Text-to-image models "often struggle to effectively compose complex scenes with multiple objects, displaying various attributes and relationships"; 3D spatial relationships are one of eight test categories. | [Huang et al., "T2I-CompBench++," arXiv 2307.06350](https://arxiv.org/abs/2307.06350) (v3, Mar 8, 2025). Abstract opened Oct 29, 2026. | Abstract only; per-category scores not read. |

Also opened: [DOCCI, arXiv 2404.19753](https://arxiv.org/abs/2404.19753) (Google, Apr 30, 2024), which built its image set to capture challenges "such as spatial relations, counting, text rendering"; its abstract does not report spatial results for image generators, so it supports only that placement is a recognized test area.

**Incident:** No public incident found. Searches run: "text-to-image spatial relationships left right benchmark 2025 FLUX GPT-4o image generation fails," "AI image generator ignores 'to the left of' 'behind' prompt placement wrong," "arXiv 2025 spatial relationship text-to-image evaluation benchmark 'spatial' generation state-of-the-art models still struggle." A tech blog comparison and several other 2025-2026 benchmarks (SpatialBench-UC, SANEval, SpatialReward) appeared only in search summaries and are not used.

## 5. The fix
**The principle:** A placement in the prompt is a requirement, not a hint. Check each one in the image, and never let copy describe a position the image does not show.

**Do this: teams and assistants that make images with placements**
1. **List the placements.** Before generating, pull out every placement in the prompt as "object A, relation, object B": left of, right of, above, below, on, under, in front of, behind, inside.
2. **Generate a set.** For a prompt with placements, generate more than one image (4 is our proposed starting point) so there is a correct one to choose.
3. **Check each placement in each image.** A person marks each listed placement correct or wrong. A vision model may pre-screen, but a person confirms, because vision models also confuse left and right (see [relative position confusion](../../spatial-reasoning/failures/relative-position-confusion.md)).
4. **Say what failed.** Never present an image as matching the prompt when a listed placement is wrong. Name the placement and the image.
5. **Offer a fix the person picks.** Pick a correct image from the set; mirror-flip for a left-right swap only if the image has no text, logos or handed objects; edit the area and re-check; build the scene from separate images in a layout tool; or change the copy to drop the position.
6. **Try word order once, then stop.** If no image is right, rewrite once with the anchor object named first and one placement per sentence, shown to the person before it runs. This follows the first-object bias in VISOR and GenEval; it is not a proven fix (our judgment).
7. **Check the copy against the final image.** Any caption, price tag, callout or instruction that names a position ("on the left," "behind the door") is checked against the final image after any flip or edit.
8. **A named reviewer signs off.** No image whose prompt or copy states a placement is published without a recorded check and approval.
9. **Log it.** Prompt, listed placements, set size, per-placement result, fix used, copy checked, reviewer and date.

**Reference design: placement check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Placements listed | Every relation in the prompt listed | lamp LEFT OF chair; rug UNDER table |
| Set checked | Each placement marked in each image | 4 images, 8 marks |
| Failure named | Wrong placements reported to requester | "Lamp is right of chair in images 1, 2, 4" |
| Fix | Chosen by requester and re-checked | Image 3 chosen |
| Flip safety | No text, logos or handed objects in a flipped image | n/a |
| Copy match | Position words in copy true in final image | "lamp on the left" true |
| Reviewer | Named, dated | D. Ruiz, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Always after the check: say how many placements were checked and which images pass |
| Offer choices: 2-4 options plus "Something else", free text open | No image passes every placement, or the requester must pick among fixes: pick image, flip, edit, change copy, something else. Do not offer choices when one image passes and the requester asked for exactly that. |
| Ask one clarifying question | A placement is ambiguous: "Left as the viewer sees it, or the chair's left?" |
| Hand off to a person | Always for publish sign-off; and when a published image is reported as not matching its copy |

**Don't over-correct.** Do not check or block images for placements the prompt never stated; free composition is fine when nobody asked for a layout. Do not flip an image with text, logos, clocks, steering wheels or a person's handed gesture. Do not rewrite the prompt more than once silently or at all without showing it. Do not trust a vision model's "left" or "right" without a person.

**Hand-off rule.** If a published image is reported as showing a position its copy contradicts, send it the same day to the reviewer who signed off and the content owner, with the log. They decide whether to replace the image or the copy.

**Framework used:** none yet. Rules 1-3 follow the per-relation scoring in VISOR and GenEval; rule 5's edit re-check follows OpenAI's note on imprecise masks; rule 6 follows the first-object bias in VISOR and GenEval; rules 4 and 7-9 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-puts-objects-in-the-wrong-position.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Lamp left of chair, rug under table" | Both placements listed | 1 |
| 2 | Set of 4, lamp wrong in 3 | Each image marked per placement; failure named | 2-4 |
| 3 | Requester picks flip; image has a store logo | Flip refused, other options shown | 5 |
| 4 | Caption says "on the left," image flipped | Copy re-checked on final image | 7 |
| 5 | Image scheduled with no check | Publish blocked | 8 |
| 6 | "A cozy reading nook," no placements | No placement check runs | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked-placement rate** (primary) | 0 (proposed) | Monthly sample of published images whose prompt or copy states a placement: no per-placement check in log / all sampled | Any |
| Copy-image position mismatch | 0 (proposed) | Sample of published images with position words in copy, checked by a second person | Any |
| Placement failure rate in sets | Track, no target | Wrong placements / all checked placements, by tool and relation type | Rising for 2 months |
| Unsafe flip rate (counter-metric) | 0 (proposed) | Flipped images that contain text, logos or handed objects | Any |
| Over-checking rate (counter-metric) | Track, no target | Placement checks run on prompts with no stated placement | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Requester re-prompts with the same placement in new words ("no, the lamp on the LEFT") | Next user turn | The requester changed their mind about the layout |
| Requester asks to flip, move or swap an object right after an image is shown | Next user turn or edit log | A style change unrelated to the prompt's placements |
| Copy with position words is published with an image that has no placement check | Publish log joined to check log | The image came from a photo shoot, not a generator |
| Same placement prompt regenerated many times in one session | Generation log | Requester exploring styles, not fixing placement |

**Starter rule:** no AI image whose prompt or copy states a placement is published unless its log shows each placement checked by a person in the final image and a named sign-off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-puts-objects-in-the-wrong-position
runs: [pre_generation, post_generation, pre_publish]
reads: [prompt.as_written, prompt.as_sent, placements.listed, set.size, check.per_placement, fix.used, image.has_text_or_logos, copy.position_words, review.signoff]
trigger: prompt or copy states a placement and no per-placement check on the final image, or image presented as matching with a failed placement, or flip on an image with text or logos, or no sign-off
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Use an image where every placement is right", "Flip or edit this image", "Change the copy to drop the position", "Something else"]
on_miss: block_publish
metric: unchecked-placement rate
counter_metric: unsafe flip rate
status: proposed
```

## 8. Related patterns
- [Semantic shift](../../generation-artifacts/failures/semantic-shift.md) - the closest existing page. It covers images drifting from the prompt over repeated generations (a blue car turning purple); this page covers a placement that is wrong on the first try, even when every object is right.
- [Spatial reasoning goal](../../spatial-reasoning/README.md) and [relative position confusion](../../spatial-reasoning/failures/relative-position-confusion.md) - the same left-right and on-under errors when a model reads an image. This page is about a model drawing one; the reading failure matters here because a vision model used as a checker can make it.
- [AI product images that show features it does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - wrong content in a product image; this page is wrong arrangement.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the missing sign-off that lets a wrong placement ship.
- [AI image generator mixes up colors](ai-image-generator-puts-colors-on-the-wrong-object.md) - the same scenes, but colors or materials land on the wrong object instead of objects landing in the wrong place.

## 9. Common questions
### Why does AI ignore "left of" in my prompt?
OpenAI says DALL-E 3's training captions rarely stated where objects were, so words like "to the left of" are "quite unreliable." Benchmarks from 2022 to 2026 find the same weakness across many models.

### Does the order of objects in my prompt matter?
It can. VISOR and GenEval found models favor the first object named, and one placed it on the left more often. Try reordering once, then check the result.

### Can I just flip the image?
For a left-right swap, often yes, if the image has no text, logos or handed objects such as a clock or a steering wheel. Re-check every placement and the copy after flipping.

### Can an AI vision model check the placement for me?
It can pre-screen, but a person should confirm. Vision models have their own left-right and on-under errors.

### Will newer models fix this?
Not reliably so far. OpenAI's current docs still list precise placement as a limitation, and 2025-2026 benchmarks still report it.
