# AI Images With Extra Fingers and Garbled Text Posted by Mistake: Image Artifacts Before Publishing

<!-- SEO
title: AI Image Extra Fingers and Garbled Text: Check Before Posting
description: AI images with six fingers, garbled sign text or melted background detail get posted by mistake; a pre-publish checklist catches them before customers do.
search phrases:
- ai image extra fingers
- why do ai images have weird hands
- ai generated image garbled text
- ai image misspelled words on sign
- how to check ai image before posting
- how to spot ai generated image mistakes
- ai generated ad six fingers
- add correct text to ai generated image
-->

**Frequency**: Common

## Issue: AI images with six fingers, garbled sign text or melted background detail get posted by mistake; a pre-publish checklist catches them before customers do.

> **One line:** A team posts an AI-made image that looked fine at thumbnail size, and customers zoom in to find a hand with six fingers or a sign that reads "GRAND OPEMNIG"; the fix is a zoomed, zone-by-zone review with a logged checklist, and a rule that no text drawn by the generator ships unless it matches the approved copy letter for letter.

| | |
|---|---|
| **Channel** | Written for **published still images**: social posts, ads, flyers, menus, web banners and article art made with ChatGPT, Gemini, Midjourney, Firefly or similar tools. Video is PLANNED, not written. |
| **Stakes** | Low to high. A garbled word on a cafe's Instagram post costs a few laughs; a six-fingered patient in a health ad or a misspelled event poster costs trust in the sender. |
| **Who is affected** | People who see the image, and the business, agency or newsroom whose name is on it |
| **Frequency** | Common, by our judgment. Section 4 lists incidents from named outlets; I found no count of how often published AI images carry these defects. |
| **Pattern ID** | image-visual-artifacts |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Artifact-free publish rate: published AI images whose logged pre-publish checklist has zero open defects, divided by all published AI images. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Research shows spelling in images improves with character-aware text encoders, and newer tools draw hands better, but none promises zero defects, so a person still has to compare the image with the approved copy. (Our judgment, not tested.) |
| **Also searched as** | AI hands wrong · AI picture six fingers · gibberish text in AI image · AI sign spelling wrong · AI art mistakes to look for · fix text in Midjourney image |

## 1. In plain words
Image generators still draw some hands with too many or fused fingers, and they often misspell words on signs, labels and menus. The person posting the image looks at it small, on a phone, where it seems fine. Customers zoom in, spot the defect and read the whole post as careless. A checklist run at full size, before posting, catches most of it.

## 2. What it looks like
**Without the fix**
```
Owner:    Make an Instagram image for our grand opening Saturday: a server holding a pizza
          under a sign that says "Grand Opening - Tony's Pizza, Columbus".
AI tool:  (returns an image) Here is your grand opening image!
Owner:    (views it on a phone, at post size) Perfect. Posting.
Comment:  "Count the fingers on that hand lol"
Comment:  "Grand OPEMNIG at TONY'S PIZZZA? Did a bot make this?"
Owner:    (deletes the post four hours later; 30 shares already out)
```
**With the fix**
```
Owner:    Make an Instagram image for our grand opening Saturday: a server holding a pizza
          under a blank sign. I'll add the words myself.
AI tool:  (returns an image with a blank sign)
Checklist (Owner, 100% zoom): Hands: 2 visible, 5 fingers each, no fusion. Text: none in image.
          Background: one menu board with squiggles. Faces: OK. Edges: OK.
Owner:    Crops the menu board out; types "Grand Opening - Tony's Pizza, Columbus" in Canva.
Checklist: Text matches approved copy letter for letter. 0 open defects. Ready to post.
```
The fixed flow keeps words out of the generator, checks each zone at full size, removes the one garbled area, and logs zero open defects before posting.

## 3. Why it happens
- **Hands are hard for the generator.** The HandRefiner authors trace incorrect finger counts to the difficulty of learning the physical structure and pose of hands (section 4). This page does not fix the model; it catches what the model gets wrong.
- **Many generators cannot spell.** Liu et al. found that text encoders that see whole word pieces, not letters, have limited spelling ability, and that this shows up as misspelled words in rendered images (section 4).
- **The reviewer looks at a thumbnail.** The poster checks the subject, the colors and the mood at phone size. Fingers, background signs and small labels only show at full size, and no step asks anyone to look there. (Our reading.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Diffusion models "suffer from generating accurate human hands, such as incorrect finger counts or irregular shapes." | [Lu et al., *HandRefiner*, arXiv 2311.17957](https://arxiv.org/abs/2311.17957). Abstract opened and read. | Research paper on a model-side repair, not a study of published images. |
| Character-blind text encoders "have limited spelling ability"; the paper says T5-XXL's spelling of common English words is only about 66%, while ByT5-XXL scores about 98% in its table. On its DrawText image test, character-aware models gained 25+ points on frequent words and 30+ on rare ones. | [Liu et al., *Character-Aware Models Improve Visual Text Rendering*, Google Research, arXiv 2212.10562](https://ar5iv.labs.arxiv.org/html/2212.10562). Full text opened on ar5iv (first 100,000 of 129,000 characters). | Single paper, models from 2022. The 98% figure I read from a table, not the text. Newer products are not tested here. |
| An Adobe Community Manager wrote on Nov. 21, 2024: "Text generation is currently a limitation in the Text to Image feature." A Community Expert in the same thread suggested generating a blank sign and adding the words in Photoshop or Adobe Express. | [Adobe Community, *Adobe Firefly grammar issues*](https://community.adobe.com/t5/adobe-firefly-discussions/adobe-firefly-grammar-issues/m-p/14994312). Opened. | Forum replies, not product documentation; the expert is labeled as not an Adobe employee. Basis for rule 3. |
| Promotional images for "Willy's Chocolate Experience" in Glasgow promised a "pasadise of sweet teats" and "catgacating". | [Nayyar, *Hyperallergic*, Feb. 28, 2024](https://hyperallergic.com/874652/children-in-tears-at-disastrous-willy-wonka-factory-experience/). Opened. | Scottish event; the failure was the event, not only the art. |
| NBC News said some of the same images showed "strange and nonsensical lettering", a known sign of AI, but that it was not clear whether the organizer used AI, and the company had not said. | [NBC News, Feb. 27, 2024](https://www.nbcnews.com/tech/willy-wonka-inspired-chocolate-experience-outrage-rcna140726). Opened. | US outlet; AI use not confirmed. |
| Posta Kenya posted a customer care poster on X in which "two of the models are having three hands each"; it was taken down after more than two hours, with no public comment. | [Citizen Digital, Jan. 31, 2024](https://citizen.digital/news/posta-kenya-blasted-online-for-sharing-faulty-ai-image-featuring-extra-hands-and-white-employees-n335855). Opened. | Kenyan national post office; single outlet. |
| Wizards of the Coast first said a Magic: The Gathering marketing image was not AI-made, then apologized on Jan. 7, 2024, saying AI components in industry-standard tools "like Photoshop crept into our marketing creative." | [Commander's Herald, Jan. 8, 2024](https://commandersherald.com/wizards-of-the-coast-issues-apology-for-ai-art-ads/). Opened. | Fan news site; no specific defect named. Shows AI can enter through editing tools, so the checklist covers edited photos too. |
| Games Workshop said a six-fingered Space Marine in its product photo was "not AI" but a photo-editing error. | [Wargamer, June 9, 2026](https://www.wargamer.com/warhammer-the-horus-heresy/editing-error-or-ai). Opened. | Company statement, not verified. Basis for "Don't over-correct": the defect matters, the label "AI" may be wrong. |

**Seen only in a summary, not used:** a VOCM report (May 4, 2026) on a six-fingered woman in a Newfoundland and Labrador RSV vaccine ad, a Malay Mail report (Aug. 9, 2024) on a billboard with an extra Petronas tower, an eWeek report on a pulled Netflix *Arcane* poster, and a Nintendo Life report on hands in Nintendo ads. Each returned 403 when I tried to open it. I found no opened US incident of a business posting an accidental six-fingered image.

## 5. The fix
**The principle:** No AI-made or AI-edited image is published until a named person has checked it zone by zone at full size and logged zero open defects.

**Do this**
1. **Log a checklist for every image.** Each AI-made or AI-edited image has a checklist record (reviewer, date, zones checked, defects found and fixed) before it is posted.
2. **Review at 100% zoom, then at post size.** The reviewer checks each zone at full resolution, then views it at the size it will appear in the feed or on the page.
3. **Count every visible finger.** Each visible hand shows the right number of fingers, none fused, bent backward or melting into an object; otherwise regenerate, retouch or crop it out.
4. **No generated text ships unless it matches.** Words drawn by the generator, including background signs, labels, packaging and logos, must match the approved copy letter for letter; otherwise remove them and add the text in a design tool.
5. **Prompt for blank surfaces.** When the image needs words, the prompt asks for a blank sign, label or screen, and the words are added afterward.
6. **Check the background, not only the subject.** Crowd faces, repeated objects, lettering on walls and shelves, and edges where objects merge get the same zoomed check.
7. **Second reviewer for high-stakes images.** Paid ads, health, government and news images get a second named reviewer before posting.

**Reference design: pre-publish image checklist**
| Zone | Check at 100% zoom | Fails if | Action |
|---|---|---|---|
| Hands and feet | Count fingers and toes on every visible one | Wrong count, fused, bent backward, merged with an object | Regenerate that area, retouch or crop |
| Text in image | Read every word aloud against the approved copy | Any letter differs, or text is gibberish | Remove; add text in a design tool |
| Logos and brands | Compare to your real logo file | A near-copy, a wrong logo, or another company's mark | Remove; place the real file |
| Faces and bodies | Eyes, teeth, ears, earrings, limbs | Mismatched pairs, extra limbs, faces melting in a crowd | Regenerate or crop |
| Objects and edges | Where two objects meet | Cup melting into a hand, chair legs fused, mismatched repeats | Retouch or crop |
| Facts in the picture | Product, place and staff shown | Shows something you don't sell or a place that isn't yours | Replace with a real photo |

**Prompt block for the image tool**
```
Leave every sign, label, screen and package blank. Do not draw any words or logos.
Keep hands simple and fully visible, or out of frame.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the conversation is the owner prompting the image tool, or the checklist tool reporting to the owner)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The owner asks for words in the image: the tool asks for the exact approved copy, or offers a blank sign instead. |
| Offer choices: 2-4 options plus "Something else", free text open | The checklist finds a defect: "Regenerate this area", "Crop it out", "Remove text and add it in a design tool", "Something else". |
| Admit uncertainty and show how to check | The tool cannot tell whether a background shape is a hand or a toy: it shows the zoomed crop and asks the reviewer to decide. |
| Hand off to a person | The image is a paid ad, a health or government notice, or news art: it goes to the second reviewer. |

**Don't over-correct.** Do not call every odd hand "AI": Games Workshop said its six-fingered image came from photo editing, and the fix is the same either way. Do not reject stylized art on purpose, such as cartoon hands with four fingers. Do not ban hands and words from all images; check them. Do not use an "AI image detector" score as the gate; this page checks defects a person can see and name.

**Hand-off rule.** When an image for a paid ad, health, government or news use has any defect the first reviewer cannot fix, it goes to a named second reviewer and is not posted that day. When the public reports a defect after posting, the post owner decides on the same day whether to take it down, and logs the defect for the checklist.

**Framework used:** none yet. The checklist draws on the sources in section 4 plus our judgment. Model-side fixes are in [generation artifacts](../../../../vision-and-images/goals/generation-artifacts/README.md).

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | An AI image is scheduled for posting with no checklist record | The post is held until a record exists | 1 |
| 2 | Image looks fine at phone size; one hand has six fingers at full size | The reviewer flags it before posting | 2, 3 |
| 3 | Sign reads "GRAND OPEMNIG" when the copy says "GRAND OPENING" | Text is removed and re-added in a design tool | 4 |
| 4 | Owner asks for "a sign that says Tony's Pizza" | The tool asks to leave the sign blank or for exact approved copy | 5 |
| 5 | A shelf label in the background has gibberish | The checklist catches it | 6 |
| 6 | A health ad image with one defect the first reviewer cannot fix | It goes to a second reviewer and is not posted | 7 |
| 7 | A cartoon mascot drawn with four fingers on purpose | It passes, with the style noted in the record | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Artifact-free publish rate** (primary) | 100% | Checklist log: published AI images with zero open defects / all published AI images | Below 100% |
| Checklist coverage | 100% | Posts with an AI-image tag that have a checklist record / all such posts | Any post without one |
| In-image text match rate | 100% | Words read from the image (by OCR or the reviewer) equal to approved copy / images with words | Below 100% |
| Public defect reports | 0 | Comments or messages naming fingers, spelling or "AI" on a post, tagged weekly | Any |
| Time from public report to decision | Same day | Timestamp of report vs. takedown or keep decision | Over 24 hours |
| False-flag rate (counter-metric) | Under 10% | Monthly sample of 20 flagged images, labeled real defect or not | Over 20% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| An AI-tagged image is published with no checklist record | Publishing log vs. checklist log | The image was checked in another tool that does not write to the log |
| Text read from the image differs from the approved copy | OCR output vs. copy field | OCR misread a stylized font that is spelled right |
| A hand-pose detector counts other than five fingers on a hand | Image check output | A finger hidden behind an object, a glove, or a cartoon style |
| A comment within 24 hours mentions fingers, spelling or "AI" | Social comment feed | A joke, or a comment on a real photo |
| Many regenerations for one image (start at 10; tune) | Image tool session log | The owner was exploring styles, not fixing defects |

**Starter rule:** hold any AI-made or AI-edited image from publishing until a named reviewer logs a checklist with zero open defects.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: image-visual-artifacts
runs: pre_send
reads: [image.file, image.ai_tag, image.ocr_text, copy.approved_text, checklist.record, publish.channel]
trigger: an AI-made or AI-edited image is about to be published, or the image tool returns an image with words in it
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, handoff]
choices: ["Regenerate this area", "Crop it out", "Remove text and add it in a design tool", "Something else"]
on_miss: ask
metric: artifact-free publish rate
counter_metric: false-flag rate
status: proposed
```

## 8. Related patterns
- [Generation artifacts (vision and images)](../../../../vision-and-images/goals/generation-artifacts/README.md) and [quality drift in generated images](../../../../vision-and-images/goals/generation-artifacts/failures/quality-drift.md) - the closest existing pages. They cover why the generator makes defects and how to change the model or pipeline; this page is a pre-publish review checklist for people who use generated images, and does not depend on their figures.
- [Misleading generated visuals](../../visual/failures/misleading-generated-visuals.md) - a chat assistant shows a render as if it were the real product. That page is about honesty and labeling; this one is about visible defects.
- [Placeholder data left in](./ui-placeholder-data-left-in.md) - unreplaced filler on a web page; the same pre-ship check idea, applied to images.
- [Stock phrases in AI-written text](./text-stock-phrases.md) - the text version: a list-based check before publishing.

## 9. Common questions
### Why do AI images have extra fingers?
Researchers say generators find it hard to learn the structure and pose of hands, which leads to wrong finger counts and odd shapes (section 4). Newer tools do better, but check every visible hand at full size before posting.

### Why is the text in my AI image misspelled?
Many generators read prompts in word pieces, not letters, which limits spelling. Ask for a blank sign and add your words in Canva, Photoshop or Adobe Express (rules 4 and 5).

### How do I check an AI image before posting it?
Open it at 100% zoom and go through the checklist in section 5: hands, text, logos, faces, edges and facts. Then view it at post size. Log what you checked.

### Does a six-fingered hand prove an image is AI?
No. Games Workshop said its six-fingered product photo was a photo-editing error. Fix the defect either way; don't make accusations from one sign.

### Should I run an AI image detector instead?
This page does not rely on one. The checklist looks for defects a person can name and fix, which is what customers notice.
