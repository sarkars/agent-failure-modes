# Why AI Images Look Fake (Waxy Skin, Glossy Light, Wrong Shadows): The Over-Smooth Stock-Photo Look

<!-- SEO
title: Why AI Images Look Fake: Waxy Skin and Wrong Shadows
description: AI images on sites and ads read as fake from waxy skin, glossy stock lighting and wrong shadows. Art-direct them and run a pre-publish light check.
search phrases:
- why do ai images look fake
- ai generated images plastic skin
- ai photos too smooth
- how to make ai images look less ai
- ai stock photo look on website
- ai image wrong shadows
- ai image reflections wrong
- should i use ai images on my website
-->

**Frequency**: Common

## Issue: AI images on sites and ads read as fake from waxy skin, glossy stock lighting and wrong shadows. Art-direct them and run a pre-publish light check.

> **One line:** A team publishes an AI-made hero image, ad or article photo straight from the generator, and visitors see waxy, poreless skin, glossy light from everywhere and shadows or reflections that cannot be right, and read the brand as careless; what is missing is art direction and a review before publishing: brand photo references in the brief, real photography where trust matters, and a skin, light and reflection checklist every image must pass.

| | |
|---|---|
| **Channel** | **Visual**: still images published on websites, ads, emails and articles, made with Midjourney, DALL-E, Imagen, Firefly or similar. Video is PLANNED, not written. |
| **Stakes** | Low to high. A blog header costs a little attention. A "real customer", team or product photo that looks generated costs trust in the claim next to it. |
| **Who is affected** | Marketing and content teams, small businesses using AI for site images, and their visitors |
| **Frequency** | Common, by our judgment. I found no count of how often published AI images carry this look (section 4). |
| **Pattern ID** | image-stock-look |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Reviewed-before-publish rate: AI-generated images published with a recorded checklist result, divided by all AI-generated images published. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Newer models may render skin texture and simple light better, but the polished default comes from the brief, and whether a trust-critical slot should hold a generated image is not a model question. (Our judgment, not tested.) |
| **Also searched as** | AI plastic skin · AI images too perfect · AI stock photo look · uncanny AI ad · AI photo lighting wrong · make AI images look real |

## 1. In plain words
Ask an image generator for "a happy family in a modern kitchen" and it returns the most polished average of that idea: smooth skin with no pores, bright even light with a glow on every edge, and glossy surfaces. Look closer and the shadows fall in two directions or the window reflection shows a different room. Visitors may not name the fault, but many read the picture as "AI, no one checked", and that doubt spreads to the page. The builder can catch it with a brief that says what the light and the people should look like, and a short check before the image goes live.

## 2. What it looks like
**Without the fix** (a dental office site in Phoenix, no review step)
```
Manager:  Make a hero image for Desert Bloom Dental: a happy family at a checkup. Stunning, ultra-detailed, 8k.
Tool:     [Image: four people with flawless, poreless skin and identical bright smiles, lit evenly
          from every side, a glowing rim of light on each head, a chrome lamp reflecting a different room.]
Manager:  Perfect. Publish it above "Real smiles from real Phoenix families."
          (A week later a review on the clinic's listing reads: "Are any of these people real?
          The website looks like AI.")
```
**With the fix** (brief with references, checklist before publishing)
```
Manager:  Hero image for the services page (not the testimonials, those use our own photos).
          Match refs/office-01.jpg and refs/office-02.jpg: late-morning window light from the left,
          35mm look, natural skin with visible texture, muted tan and teal palette. No "8k", no "flawless".
Tool:     [Image: a hygienist and patient by a window, light from the left, soft shadow to the right.]
Reviewer: Skin at 100%: texture visible, pass. Light: one direction, shadows agree, pass.
          Reflections: chair's chrome arm shows the window, pass. Matches refs: pass. Checklist v3 logged.
```
The brief named the light and the look instead of "stunning", the trust slot kept real photos, and a person checked skin, light and reflections before it went live.

## 3. Why it happens
- **The brief asks for polish, not a look.** "Stunning, ultra-detailed, 8k" with no reference photo pulls the output toward a glossy, evenly lit average. PhyBench found that spelling out the physical outcome in the prompt raised DALL-E 3's physics score from 1.09 to 2.46 (section 4), so vague briefs leave more to chance. The link from "quality words" to waxy skin is our judgment.
- **The generator has no model of the scene's geometry.** Farid notes that text-to-image tools are not built on explicit geometric modeling, so shadows and reflections can look right locally and still disagree with each other.
- **No one checks before publishing.** At thumbnail size the image looks fine. Farid argues that people are poor at certain geometric judgments, so wrong shadows often pass a glance.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Farid generated 25 DALL-E 2 images per prompt. For three cubes on a sunny sidewalk, the cast shadows in every image were inconsistent with a single light source, yet he called them perceptually convincing. For a toy dinosaur in a vanity mirror, all but three reflections were obviously disconnected from the scene. | [Farid, *Perspective (In)consistency of Paint by Text*, arXiv 2206.14617, June 27, 2022](https://arxiv.org/abs/2206.14617); full text read on [ar5iv](https://ar5iv.labs.arxiv.org/html/2206.14617). | One author, one 2022 model, three prompts. Newer models are not tested. |
| Farid's checking method: a point on an object, its shadow and the light lie on one line, so lines drawn from shadow to object should meet at one point in a real photo; the same test works for reflections. He says AI images "seem to struggle" with perspective-correct shadows and reflections. | [Farid, *Photo forensics from lighting, shadows and reflections*, Content Authenticity Initiative, Sept. 14, 2023](https://contentauthenticity.org/blog/photo-forensics-from-lighting-shadows-and-reflections). Opened. | Expert blog, not a new study. He warns that points must be matched carefully and lens distortion removed first. |
| PhyBench tested 6 text-to-image models on 700 prompts across 31 physical scenarios. Models "frequently err" except in optics, where all did well; explicit prompts raised DALL-E 3 from 1.09 to 2.46. | [Meng et al., *PhyBench*, arXiv 2406.11802 v3, Sept. 2024](https://arxiv.org/html/2406.11802v3). Opened. | Scored by a GPT-4o judge the authors built. Optics doing well means wrong light is not guaranteed; check, do not assume. |
| In Miller et al., 124 participants labeled about 2 of 3 AI-generated White faces as human, the least accurate were the most confident, and the effect did not hold for Asian and Black faces. | [Dawel et al., The Conversation, Nov. 13, 2023](https://theconversation.com/can-you-spot-the-ai-impostors-we-found-ai-faces-can-look-more-real-than-actual-humans-215160). Opened. | Authors' own summary of a *Psychological Science* paper I did not open. Isolated faces, not ads. |
| A University of Southampton project page reports that Miller et al. found people treated smooth skin as a sign of AI when it did not predict AI at all. | [Southampton, DISCERN-AI project](https://www.southampton.ac.uk/research/projects/discern-ai-developing-an-intervention-to-support-critical-evaluation-of-real-non). Opened. | Secondhand description. It means smooth skin draws the "AI" suspicion, whether or not it is AI: the cost to a brand is real either way. |
| A CNN report said social media users found Coca-Cola's 2024 AI holiday ads went too far into the "uncanny valley"; Coca-Cola defended them as the "intersection of human creativity and technology". | [CNN Newsource via FOX5 Las Vegas, Nov. 22, 2024](https://www.fox5vegas.com/2024/11/22/coca-cola-faces-backlash-ai-holiday-ads). Opened. Campaign Asia's [headline and standfirst](https://www.campaignasia.com/video/coca-cola-faces-backlash-for-ugly-ai-generated-christmas-spot/499379) quote users calling it "deeply uncanny" and "soulless" (rest paywalled). | Video, not a still. Social media reaction, not a measured survey. |
| Deseret News relays the Better Business Bureau saying AI images often have "a very airbrushed look", and BBC advice to check shadows, lighting and eye reflections. | [Bott Rivera, Deseret News, Mar. 21, 2024](https://www.deseret.com/u-s-world/2024/03/21/how-to-spot-ai-images/). Opened. | Secondhand: I did not open the BBB or BBC originals. Consumer tips, not research. |

**Seen only in a summary, not used as evidence.** Reports that readers criticized a Guess ad with AI models in the August 2025 US *Vogue* as unrealistically perfect (the FashionNetwork page returned 403), and that J.Crew, Shein and Skechers drew criticism for AI ads (eMarketer returned 403). A 2026 preprint ([arXiv 2608.30210](https://arxiv.org/abs/2608.30210)) was summarized as ranking oversmoothness and skin texture among the cues people and models use; I could open only its abstract, which does not list cues. I found no study that measures trust or sales loss from the stock look itself.

## 5. The fix
**The principle:** No AI image is published until someone has chosen its look against brand references and checked its skin, light and reflections; where the picture is a claim about real people or products, use a real photo.

**Do this**
1. **Record a review for every AI image.** Each published AI image has a log entry: reviewer, checklist version, result per check, and the page slot.
2. **Trust slots get real photos.** Team, customer, testimonial, before-and-after, product-as-sold and news images are photographs. An AI image in one of these slots fails review.
3. **Brief with references, not adjectives.** The prompt or tool settings include at least two approved brand photos (or a style reference) and name the light: direction, time of day and hardness. Words such as "8k", "ultra-detailed", "flawless" and "perfect skin" are removed.
4. **Skin passes at 100% zoom.** Faces show texture variation (pores, fine lines, uneven tone). Uniform waxy sheen fails: regenerate, retouch in texture, or replace with a photo.
5. **One light story.** All shadows fall the same way, objects resting on a surface have contact shadows, and lines from shadow points to object points meet at one point (the CAI test). Any disagreement fails.
6. **Reflections match or are cropped.** Mirrors, windows, glasses, chrome and eyes show the scene that is in front of them. A reflection the reviewer cannot verify is cropped out or the image is replaced.
7. **Side by side with the brand set.** The image is viewed next to the reference photos at the size it will publish. Flag glow on every edge, oversaturation and even light from all sides that the references do not have.

**Reference design: slot decision table**
| Slot | AI image allowed? | Requirement |
|---|---|---|
| Team, customers, testimonials, "real results" | No | Own or commissioned photos only |
| Product as the buyer will receive it | No | Real product photo; a render must be labeled (see [misleading generated visuals](../../visual/failures/misleading-generated-visuals.md)) |
| Blog header, mood or concept image | Yes | Rules 1, 3-7 |
| Ad creative with people | Yes, with care | Rules 1, 3-7 plus a second reviewer outside the team |

**Reference design: pre-publish checklist** (each row pass/fail; log the version)
| Check | How | Fails if |
|---|---|---|
| Slot | Look up the slot in the table above | AI image in a "No" slot |
| Skin | View faces at 100% | No texture; plastic sheen |
| Light | Draw 2-3 shadow-to-object lines | Lines do not meet; shadows disagree; no contact shadows |
| Reflections | Inspect every reflective surface | Reflection shows a different scene or is missing |
| Brand match | Side by side with references at publish size | Glow, oversaturation or flat all-around light the references lack |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the builder prompting the tool, or the reviewer reporting to the builder; the fit is our judgment)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The brief has no reference photo or light direction: the tool or reviewer asks for one before generating. |
| Offer choices: 2-4 options plus "Something else", free text open | An image fails a check: "Regenerate with the reference", "Retouch the flagged area", "Use a real photo", "Something else". |
| Admit uncertainty and show how to check | The reviewer cannot tell whether a shadow is right (diffuse light, no clear source): it says so and names the line test. |
| Hand off to a person | The image is for a trust slot or a paid ad with people (see hand-off rule). |

**Don't over-correct.** Do not add film grain or "imperfection" filters to make an image pass; grain over wrong shadows is still wrong. Do not treat smooth skin as proof that an image is AI: retouched photos are smooth too, and Miller et al. found people misread smooth skin as an AI sign (section 4). Do not ban AI images everywhere; a concept image that passes the checklist is fine. Do not call out a photographer's work as AI on looks alone.

**Hand-off rule.** Any image for a trust slot, or a paid ad showing people, goes to a named human owner (brand lead or photographer). An image that fails the checklist twice is replaced with a licensed or commissioned photo, not regenerated a third time.

**Framework used:** none yet. The light and reflection checks follow Farid (section 4); the slot table and the rest are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | AI image published with no review entry | Publish step blocks it | 1 |
| 2 | AI-generated "happy customers" photo on a testimonials block | Fails the slot check | 2 |
| 3 | Prompt says "stunning, 8k, flawless skin", no references | Reviewer or tool asks for references and the light; words removed | 3 |
| 4 | Portrait with poreless, glossy skin at 100% | Fails skin check | 4 |
| 5 | Two objects with shadows falling opposite ways | Fails light check | 5 |
| 6 | Mirror shows a different room | Cropped or replaced before publishing | 6 |
| 7 | Retouched real photo with smooth skin uploaded by the team | Not flagged as AI (over-correction check) | Don't over-correct |
| 8 | Image fails twice | Routed to a real photo, no third generation | Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Reviewed-before-publish rate** (primary) | 100% | CMS log: AI images published with a checklist entry / all AI images published | Below 95% in a week |
| AI images in trust slots | 0 | Asset provenance (generator metadata or Content Credentials) joined to slot type | Any |
| First-pass checklist failure rate | Track; set from baseline | Checklist log, by check (skin, light, reflections, brand) | Rising two months in a row |
| Visitor comments calling an image AI or fake | Track; set from baseline | Phrase match ("AI", "fake", "not real") in comments, reviews and ad replies near the image | Any rise after a new image goes live |
| Real photos wrongly flagged as AI (counter-metric) | Under 5% | Monthly sample of 20 flags, labeled by provenance | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Image with AI provenance published with no review entry | CMS publish event joined to checklist log | Review done outside the system and not logged |
| Prompt log contains "8k", "flawless", "perfect skin" or "ultra-detailed" and no reference image | Generator prompt log | A deliberate stylized illustration, not a photo look |
| Image published within minutes of generation, no edit events | Generator and CMS timestamps | A reviewed template image reused on purpose |
| Comment or ad reply on the image mentions "AI" or "fake" | Comment and reply text | A visitor talking about AI in general |

**Starter rule:** block publishing any AI-generated image that has no recorded pass on the slot, skin, light and reflection checks.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: image-stock-look
runs: pre_send   # before the image is published
reads: [asset.provenance, asset.slot_type, prompt_log.text, prompt_log.reference_images, checklist.version, checklist.results]
trigger: an AI-generated image is about to be published
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Regenerate with the reference", "Retouch the flagged area", "Use a real photo", "Something else"]
on_miss: ask
metric: reviewed-before-publish rate
counter_metric: real photos wrongly flagged as AI
status: proposed
```

## 8. Related patterns
- [Extra fingers and garbled text in AI images](./image-visual-artifacts.md) - the closest pattern in this family: visible errors in one part of the image (hands, lettering). This page covers the overall polished look and light physics, and does not cover hands or text.
- [Generation artifacts goal](../../../../vision-and-images/goals/generation-artifacts/README.md) and [quality drift](../../../../vision-and-images/goals/generation-artifacts/failures/quality-drift.md) - the model maker's side: images that get worse over repeated generation. This page is the publisher's side: one image that looks fine to the team but reads as AI to visitors, fixed by art direction and review, not by changing the model.
- [Misleading generated visuals](../../visual/failures/misleading-generated-visuals.md) - a chatbot shows a render as if it were the real product; this page's slot table sends those cases there.
- [Default gradient look](./ui-default-gradient-look.md) - the same "nobody chose it" default in web UI color.
- [Fabricated social proof](./ui-fabricated-social-proof.md) - an AI face on a testimonial is both a stock-look problem and invented proof.

## 9. Common questions
### Why do AI images look fake?
Often the skin is too smooth, the light is bright from every side, and shadows or reflections disagree with each other. Farid's tests on DALL-E 2 found shadows that fit no single light and reflections that did not match the scene (section 4). Newer models vary, so check each image.

### How do I make AI images look less like AI?
Give the tool two or more of your own photos as references and name the light, drop words like "8k" and "flawless", and check skin, shadows and reflections before publishing (section 5).

### Should I use AI images on my website?
For concept and blog images, yes, if they pass a review. For your team, customers, results and products, use real photos; a generated face there turns a style problem into a trust problem.

### How can I check if the shadows in an image are right?
Pick a point on a shadow and the matching point on the object, draw a line through them, and repeat. In a real photo lit by one source, the lines meet at one point ([Farid, CAI](https://contentauthenticity.org/blog/photo-forensics-from-lighting-shadows-and-reflections)).

### Is smooth skin proof that a photo is AI?
No. Retouched photos are smooth too, and Miller et al. found people wrongly used smooth skin as a sign of AI. Treat it as a reason to look closer, not a verdict.
