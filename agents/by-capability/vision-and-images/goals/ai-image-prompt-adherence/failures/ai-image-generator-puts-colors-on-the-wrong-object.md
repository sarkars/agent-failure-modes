# AI Image Generator Mixes Up Colors: Attributes Attached to the Wrong Object

<!-- SEO
title: AI Image Generator Mixes Up Colors Between Objects: How to Catch It
description: Ask an AI image tool for a blue sofa and a yellow chair and it may swap the colors. Check each object against the prompt before anyone uses the image.
search phrases:
- ai image generator wrong colors on objects
- ai image swapped colors between two objects
- midjourney color bleeding between objects
- stable diffusion attribute binding color leak
- ai image red car blue truck wrong color
- how to get ai to color each object correctly
-->

**Frequency**: Unknown

## Issue: Ask an AI image tool for two objects with different colors or materials, such as "a navy sofa and a mustard armchair," and it can swap them, put both colors on one object or spill a color onto the background, and the image ships because it looks right at a glance. List every object-attribute pair in the prompt, check each object in the output against its own pair, fix or regenerate any miss, and tell the requester what did not match before the image is used.

> **Read this first:** This page summarizes research papers as we read them on October 29, 2026. No public product incident was found. It makes no claim about advertising or consumer law; a product image in the wrong color raises questions a qualified person must answer, and nothing here is legal advice. The rules below are workflow choices.

> **One line:** A Denver furniture store asks for "a navy blue sofa and a mustard yellow armchair" for a product page and gets a mustard sofa and a navy armchair; the fix is to list each object with its color or material before generating, check each object in the result against that list, correct or regenerate any swap, and say plainly what did not match.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source tests still images. The same check would apply to objects in AI video, but no opened source measures video. |
| **Channel** | Text-to-image tools, design tools with built-in generators and chat assistants that call them, used by ecommerce, marketing and content teams |
| **Stakes** | Medium. A swapped color in a mood board costs a retry; in a product listing it shows a variant the store does not sell (our judgment). |
| **Who is affected** | Shoppers who buy from the picture, the team that publishes it and anyone who relies on the image matching the words |
| **Frequency** | Unknown. No opened source gives a rate in real business use. Benchmarks find it in controlled tests (section 4). |
| **Pattern ID** | ai-image-generator-puts-colors-on-the-wrong-object |
| **Family** | [AI Images That Ignore the Prompt](../README.md) |
| **Goal** | AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text. |
| **Primary metric** | Unchecked-binding rate: published images from prompts that give two or more objects their own color, material or texture, where no per-object check is logged, divided by all such published images. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is seven research papers and preprints; no product incident. |
| **Will a better model fix this?** | Partly. In a 2025 test GPT-4o scored 0.92 on single-color prompts but 0.61 on two-object color prompts, and a 2025 paper shows GPT-4o, Gemini 2.5 and Grok 3 still missing colors in its examples. Newer models do better, but none of the opened sources shows the problem gone. (Our judgment, drawing on the cited tests.) |
| **Also searched as** | AI color bleeding · AI image colors swapped · attribute leakage · wrong color on wrong object · AI ignores which object is which color |

Tests: [AI image generator puts colors on the wrong object test file](../../../tests/ai-image-generator-puts-colors-on-the-wrong-object.md).

## 1. In plain words
A store needs a room photo for a new sofa. The prompt says "a navy blue sofa and a mustard yellow armchair." The tool makes a nice room with both colors in it. But the sofa is mustard and the chair is navy. Both colors are there, so a quick look says "done." The product page now shows a sofa color the store does not carry.

## 2. What it looks like
The store, people and SKUs below are invented.

**Without the fix**
```
Merchandiser: Room scene for SKU 4410: a navy blue sofa and a mustard yellow armchair,
              light oak floor, morning light.
Assistant:    Here is your room scene. (One image; no check.)
Merchandiser: Looks good, adding it to the product page.
Customer service (Tuesday): Two customers ordered the "mustard sofa" from the photo.
              We don't make that sofa in mustard.
```
**With the fix**
```
Merchandiser: Room scene for SKU 4410: a navy blue sofa and a mustard yellow armchair,
              light oak floor, morning light.
Assistant:    I checked each item against your request. Sofa: mustard (asked navy). Armchair:
              navy (asked mustard). Floor: light oak, as asked. The colors came out swapped,
              so I won't mark this one ready. I regenerated 4 more; 1 matches on every item.
              Here it is, with the check. It goes to Jordan Lee for approval before it's listed.
```
The fixed version checks each object against its own color, says what was wrong and does not pass a swapped image as matching.

## 3. Why it happens
- **The model links the attribute to the wrong word.** Chefer et al. found Stable Diffusion "binds attributes to the wrong subjects or fails to bind them entirely"; for "A yellow bow and a brown bench," the yellow went to the bench.
- **Common pairings pull the attribute.** Trusca et al. write that models "often bind objects with their most common attributes": "a golden car and a red watch" can give "a golden watch and a red car." They also describe "attribute leakage," where "a golden ingot and fish" gives a goldfish.
- **One color is easy, two are hard, and a glance hides it.** Color Bind found models do far worse with multiple colors than with one. Both colors still appear in the image, so a reviewer who checks "is there navy and mustard?" misses the swap.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Stable Diffusion has "incorrect 'attribute binding', where the model binds attributes to the wrong subjects or fails to bind them entirely." Example: "A yellow bow and a brown bench," with yellow on the bench. | [Chefer et al., "Attend-and-Excite," SIGGRAPH 2023, arXiv 2301.13826](https://arxiv.org/abs/2301.13826). Full text opened Oct 29, 2026. | One model (Stable Diffusion, 2022-2023). Examples, not a rate. |
| Models "often bind objects with their most common attributes": "a golden car and a red watch" may give "a golden watch and a red car"; "a golden ingot and fish" gives "a goldfish and golden ingot." | [Trusca et al., "Object-Attribute Binding in Text-to-Image Generation," arXiv 2404.13766](https://arxiv.org/abs/2404.13766) (April 2024). Full text opened Oct 29, 2026. | Illustrative examples; the ingot example is credited to earlier work (Rassin et al., 2022). |
| On "a photo of a [COLOR A] [OBJECT A] and a [COLOR B] [OBJECT B]," "all the tested models perform poorly," the best getting 35% of attribute-binding images right. | [Ghosh et al., GenEval, arXiv 2310.11513](https://arxiv.org/abs/2310.11513) (Oct 2023). Full text opened Oct 29, 2026. | Models tested in 2023, up to SD-XL and IF-XL. Scored by an object detector and color classifier, not people. |
| T2I-CompBench++ builds 3,000 attribute-binding prompts in color, shape and texture. It finds "models tend to confuse the association between attributes and objects"; "A room with blue curtains and a yellow chair" may give "yellow curtains and a blue chair." | [Huang et al., T2I-CompBench++, arXiv 2307.06350](https://arxiv.org/abs/2307.06350) (v3, March 2025). Full text opened Oct 29, 2026. | The example is the authors' description of the failure, not a counted result. |
| GPT-4o scored 0.92 on GenEval's single-color task and 0.61 on attribute binding. | [Yan et al., GPT-ImgEval, arXiv 2504.02782](https://arxiv.org/abs/2504.02782) (v3, May 2025). Full text opened Oct 29, 2026. | Authors' own run. GenEval 2 (below) says GenEval scores drift from human judgment "as much as 17.7%" for current models, so treat the gap, not the exact numbers, as the finding. |
| Models "struggle to generate images that faithfully reflect multiple color attributes—far more so than with single-color prompts," and "neither inference-time techniques nor existing editing methods reliably resolve" it. Examples from "OpenAI 4O, Gemini 2.5, and Grok 3" "fail to generate the correct colors." | [Shomer-Chai et al., "Color Bind," arXiv 2508.19791](https://arxiv.org/abs/2508.19791) (v3, Dec 2025). Full text opened Oct 29, 2026. | Proprietary models shown as qualitative examples only; the measured results are on open diffusion models. The authors propose their own editing fix. |
| GenEval 2 adds 18 attributes (colors, materials, patterns) because GenEval "has been saturated for some time." | [Kamath et al., GenEval 2, arXiv 2512.16853](https://arxiv.org/abs/2512.16853) (Dec 2025). Full text opened Oct 29, 2026. | About the benchmark, not a failure rate; used here to qualify the scores above. |

Google's [Imagen paper and DrawBench](https://arxiv.org/abs/2205.11487) include two-color prompts such as "A brown bird and a blue bear," and the [Imagen 3 report](https://arxiv.org/abs/2408.07009) scores a color category; both were opened and show that vendors test for this, but neither reports a binding failure rate we use here.

**Not covered here, no opened source:** a public product incident where a swapped color reached customers, and clothing or accessories moving between two people (such as a red hat ending up on the wrong person); no opened source shows that case. Searches run: "attribute binding text-to-image benchmark 2025 color leakage wrong object," "image generation API docs prompting tips assign colors to each object attribute binding gpt-image Imagen Firefly," "GenEval 2 OR T2I-CoReBench OR OneIG-Bench attribute binding results 2025 2026 GPT-Image FLUX." No vendor doc about attribute binding was opened. A 2026 benchmark (WeGenBench) and T2I-CoReBench scores were read only in search summaries and are not used.

## 5. The fix
**The principle:** "Both colors are in the picture" is not a match. Every object is checked against its own attribute, and a miss is named, not hidden.

**Do this: teams and assistants that make images from multi-object prompts**
1. **List the pairs.** Before generating, write out every object that has its own color, material, texture or shape in the prompt as a pair: "sofa: navy blue," "armchair: mustard yellow." Flag any prompt with two or more pairs.
2. **Write each pair plainly.** Keep each attribute right next to its object, and put each object in its own clause ("A navy blue sofa. Beside it, a mustard yellow armchair."). Show the user the prompt as sent if it differs from what they typed. This is our judgment, not a proven fix.
3. **Check each object, not the image.** For a flagged prompt, check every pair on its own: "What color is the sofa?" A swap, a missing attribute, or one object taking both colors is a miss. A color spilling onto an object the prompt did not color (leakage) is a miss.
4. **Generate more than one for flagged prompts.** Make a small set and keep only images where every pair passes. Set size is the team's choice.
5. **Fix the region, then re-check.** If the best image misses one object, recolor that object with a masked edit, or generate the objects separately and composite. Check the whole image again after any edit; edits can change other areas.
6. **Say what did not match.** Never hand over an image as matching when a pair failed. Name the object, what was asked and what came out.
7. **Product images get a person.** Any image that shows a real product variant (color, finish, material) is checked by a named reviewer against the SKU before it is listed.
8. **Log it.** Prompt as written and as sent, the pair list, the per-pair result, any edit, reviewer and date.

**Reference design: per-object check before delivery**
| Pair from prompt | Asked | Found | Result |
|---|---|---|---|
| sofa | navy blue | mustard yellow | Miss (swapped) |
| armchair | mustard yellow | navy blue | Miss (swapped) |
| floor | light oak | light oak | Pass |
| Image status | | | Not ready: regenerate or fix sofa and armchair |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Delivering any image from a flagged prompt: give the per-object result first, then the image |
| Offer choices: 2-4 options plus "Something else", free text open | No image in the set passes every pair: recolor the wrong object in the best image, generate the items separately and combine them, keep it as a draft mood board only, something else. Do not offer choices when an image passes; deliver it with the check. |
| Ask one clarifying question | The prompt does not say which object an attribute belongs to ("a red and white kitchen with a table and chairs"): "Which items should be red?" |
| Hand off to a person | Always for product-variant images before listing; and when a customer reports the photo shows the wrong color |

**Don't over-correct.** Do not run the per-object check on prompts with one colored object or none; that is a different check. Do not count colors the prompt never assigned (a plant, a sky) as misses unless the prompt's color clearly spread onto them. Do not keep regenerating without limit; after the team's set number of tries, offer choices. Do not change the user's words silently; show any rewrite. Do not apply product-level review to internal sketches that will never be published.

**Hand-off rule.** If a published image is reported to show an object in the wrong color or material, send it to the reviewer and the content owner the same day with the log. They decide whether to pull it.

**Framework used:** none yet. Rules 1 and 3 follow the per-object scoring in GenEval and T2I-CompBench++; rule 5 follows Color Bind's finding that editing after generation can correct colors, and the planned A6 page on edits changing other areas; rules 2, 4, 6, 7 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-puts-colors-on-the-wrong-object.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "a navy blue sofa and a mustard yellow armchair" | Two pairs listed; prompt flagged | 1 |
| 2 | Output has colors swapped | Both objects marked as misses; not delivered as matching | 3, 6 |
| 3 | "a wooden table and a metal chair" gives a metal table | Material miss caught | 3 |
| 4 | Blue from the sofa spills onto the lamp | Leakage caught | 3 |
| 5 | Recolor edit changes the floor | Re-check catches it | 5 |
| 6 | Product variant image, no reviewer | Listing blocked | 7 |
| 7 | "a red apple on a table" | No per-object check forced | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked-binding rate** (primary) | 0 (proposed) | Monthly sample of published images from flagged prompts: log has no per-pair result / all sampled flagged images | Any |
| Delivered-with-miss rate | 0 (proposed) | Delivered images whose logged per-pair check shows a miss and no note to the user | Any |
| First-try pass rate | Track, no target | Share of flagged prompts where the first image passes every pair | Falling for 2 months |
| Over-check rate (counter-metric) | Track, no target | Sample of one-object or no-color prompts that still got a per-pair check or regeneration | Rising |
| Wrong-color reports after publish | 0 (proposed) | Customer service tickets or reviews tagged "photo color wrong" joined to image log | Any |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt with two or more object-attribute pairs and one generation delivered with no per-pair result | Generation log plus delivery log | A person checked it in a review step logged elsewhere |
| User's next message names an object and a color ("the sofa should be navy") right after delivery | Next user turn | The user changed their mind about the color |
| Per-pair check shows a miss and the image is still delivered or published | Check log plus publish log | The user chose "keep as draft" from the offered options |
| Customer ticket says the product photo color does not match the item | Support ticket tags | Screen or lighting differences, not a generated swap |

**Starter rule:** no image from a prompt that gives two or more objects their own color, material or texture is delivered as matching unless each object has a logged pass against its own attribute.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-puts-colors-on-the-wrong-object
runs: [pre_generation, post_generation, pre_publish]
reads: [prompt.as_written, prompt.as_sent, prompt.object_attribute_pairs, output.per_pair_result, edit.regions, review.signoff, image.is_product_variant]
trigger: two or more object-attribute pairs with no per-pair result, or a per-pair miss delivered as matching, or a product-variant image with no sign-off
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Recolor the wrong object in the best image", "Generate the items separately and combine them", "Keep it as a draft mood board only", "Something else"]
on_miss: block_delivery
metric: unchecked-binding rate
counter_metric: over-check rate
status: proposed
```

## 8. Related patterns
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - the closest existing page. It covers an image drifting from the prompt over repeated generations; this page covers the first image putting the right attributes on the wrong objects. Its percentages have no opened source and are not used here.
- [AI images that break brand logo, color and font rules](../../ai-image-brand-guidelines/failures/ai-images-break-brand-logo-color-and-font-rules.md) - about whether a brand color matches its exact hex value; this page is about which object gets which color.
- [AI product images that show features the product does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - what a swapped product color becomes once it is published.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the missing gate that lets a swap ship.

Planned pages in this goal, not yet written: wrong count of objects, wrong placement, and edits that change parts the user did not ask to change.

## 9. Common questions
### Why does AI put the colors on the wrong objects?
The model does not always tie each color word to the right object word. Research shows it leans toward common pairings, so "a golden car and a red watch" can come out as a golden watch and a red car.

### Does writing the prompt differently fix it?
It can help to keep each color right next to its object, but no opened source shows that wording alone fixes it. Check each object in the result.

### Do newer models still do this?
Less often in tests, but yes. A 2025 test found GPT-4o much better at one color than at two objects with two colors, and a 2025 paper shows recent commercial models still missing colors.

### Is it only colors?
No. Benchmarks also test materials, textures and shapes, such as wooden, plastic or rubber objects. Colors are the most studied.
