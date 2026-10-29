# AI Image Edit Changes the Whole Image: Ask to Change One Thing, Get Other Changes Too

<!-- SEO
title: AI Image Edit Changes the Whole Image? Stop Unrequested Changes
description: Ask an AI tool to remove one object and the face, door or sky changes too. Compare each AI edit with the original outside the edited area before use.
search phrases:
- ai image edit changes the whole image
- chatgpt changes entire image when editing
- chatgpt image edit keep everything else the same
- how to edit only part of an image with ai
- ai changed my face when editing photo
- gpt-image-1 edit changes unmasked area
- ai photo edit changed the background
-->

**Frequency**: Common

## Issue: Ask an AI image tool to make one change, such as "remove the trash bin" or "change her dress to blue," and the result also changes things nobody asked about: a face, a door color, the lighting, the size of a cup, and the team uses it because the reply said "Done" and nobody compared it with the original. Before editing, write what may change and what must stay; after editing, compare the result with the original outside the edited area, name every other change, and paste the original pixels back where an exact match matters.

> **Read this first:** One case below involves an edited image of a real person's body. Whether changing a real person's face or body in an image needs that person's consent is a legal question this page does not answer; it needs review by a qualified person. The rules below are workflow checks, not legal conclusions.

> **One line:** A Chicago real estate team asks an assistant to remove a trash bin from a listing photo and the edited photo also turns the red front door black; the fix is a written change list and keep list, a comparison against the original outside the edited area, a reply that names every unrequested change, and original pixels restored outside the edit before a named person signs off.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source tests or reports still-image edits. Editing one object in a video clip may show the same failure, but no opened source measures it. |
| **Channel** | Edit features in AI image tools and chat assistants (text-only edit requests, selection or mask edits, reference-image edits), and workflows that call image edit APIs |
| **Stakes** | Medium to high. A listing, product or ad image that shows something different from the real house, product or person; a real person's face or body changed without being asked (section 4 incident) |
| **Who is affected** | Customers who rely on the edited image, people shown in the photo, and the team that published it |
| **Frequency** | Common in one benchmark: Apple researchers found GPT-Image-1 "frequently introduces unintended changes in areas unrelated to the instruction" (section 4). No opened source gives a rate in real business use. |
| **Pattern ID** | ai-image-edit-changes-parts-you-did-not-ask-to-change |
| **Family** | [AI Images That Ignore the Prompt](../README.md) |
| **Goal** | AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text. |
| **Primary metric** | Unrequested-change publish rate: sampled published AI-edited images in which an item on the keep list differs from the original and the change was not reported and approved, divided by all sampled published AI-edited images. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is one arXiv benchmark (preprint), two OpenAI vendor documents, one dated hands-on review, two user forum threads and one dated public incident whose cause is disputed. |
| **Will a better model fix this?** | Partly. OpenAI now processes every image input to gpt-image-2 at high fidelity, but its docs still call the mask guidance that the model "may not follow" exactly. In GIE-Bench the best instruction follower was among the worst at leaving other pixels alone. Pasting original pixels back outside the edit does not depend on the model (our judgment). |
| **Also searched as** | ChatGPT redraws the whole picture · AI edit changed my face · inpainting changed the background · AI photo edit changed colors · edit only the selected area AI |

Tests: [AI image edit changes parts you did not ask to change test file](../../../tests/ai-image-edit-changes-parts-you-did-not-ask-to-change.md).

## 1. In plain words
A real estate agent asks an AI tool to take a trash bin out of a listing photo. The bin is gone and the photo looks fine, so it goes on the listing. But the tool also repainted the front door and dropped the shutters off an upstairs window. Buyers arrive and the house does not match the photo. The agent asked for one change and got three, and nothing told her about the other two.

## 2. What it looks like
The company, people and address below are invented.

**Without the fix**
```
Agent:     Remove the green trash bin by the garage in "412 Elm St front.jpg".
Assistant: Done! Here is your photo without the trash bin.
Agent:     Perfect, uploading it to the listing.
Buyer (at the showing): The photos show a black front door and shutters on the
           upstairs window. The door here is red and there are no shutters.
Agent:     I only asked it to remove the bin.
```
**With the fix**
```
Agent:     Remove the green trash bin by the garage in "412 Elm St front.jpg".
Assistant: Change: remove the trash bin. Keep: house, door, windows, roof, yard, sky.
           I edited only the bin area and compared the result with your original.
           The bin is gone. Outside that area, the front door turned from red to black.
           I pasted your original pixels back everywhere except the bin area, so only
           that area now differs. Side-by-side attached; your original is kept as version 1.
Agent:     Looks right.
Assistant: Sent to Maria Chen (listing coordinator) to check against the original before upload.
```
The fixed version states what may change and what must stay, compares with the original, names the unrequested change, restores the original outside the edit, keeps the original and ends with a person's check.

## 3. Why it happens
- **The "edit" can be a new drawing guided by the old one.** OpenAI's docs say masking with GPT Image "is entirely prompt-based": the model "uses the mask as guidance, but may not follow its exact shape with complete precision." Users in OpenAI's forum report that a small change request returns "a completely new image" (user reports, not confirmed by OpenAI).
- **Following the instruction and leaving the rest alone pull against each other.** GIE-Bench calls this "a key trade-off": GPT-Image-1 led on doing the asked edit but changed areas outside the edit more than most models tested, "altering background textures, shifting lighting, or distorting peripheral objects." OpenAI's Cookbook ties preserving unrelated areas and faces to a high input fidelity setting, which implies standard settings preserve less.
- **The result is judged alone, not against the original.** A black door or a slightly different smile looks plausible by itself. In TechRadar's test the changes were small: hair, expression, the size of a cup, a van that moved (our judgment that this is why such changes ship).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| GIE-Bench: 1,080 image-instruction pairs from 856 images, 9 edit types, 20 categories. GPT-Image-1 led on doing the asked edit (85.00% by a GPT-4o judge; OmniGen 60.74%, MagicBrush 48.33%) but "often over-modifies irrelevant image regions." | [Qian et al. (Apple), "GIE-Bench," arXiv 2505.11493](https://arxiv.org/abs/2505.11493) (v1 May 16, 2025; v3 July 25, 2025). Abstract and HTML full text opened Oct 29, 2026. | Preprint by Apple researchers testing a competitor's model. Correctness was judged by an AI model, not people; GPT-Image-1 was left out of the 100-example human study because its API was not yet released. |
| Same paper, scored only outside the edited object's mask: SSIM 0.5704 for GPT-Image-1 against 0.8703 for MagicBrush and 0.9585 for OneDiffusion; PSNR 13.36 against 20.48 and 26.24. GPT-Image-1 "frequently introduces unintended changes in areas unrelated to the instruction." | Qian et al., Table 3 and section 4.2, as above. | Pixel scores also punish harmless shifts. On masked CLIP (meaning, not pixels) GPT-Image-1 scored 0.9485, close to MagicBrush's 0.9489, so the objects stayed similar in kind while pixels changed. |
| "Masking with GPT Image is entirely prompt-based. The model uses the mask as guidance, but may not follow its exact shape with complete precision." For gpt-image-2 the API "processes every image input at high fidelity automatically." | [OpenAI API docs, image generation guide](https://developers.openai.com/docs/guides/image-generation). Opened Oct 29, 2026. | Vendor documentation. Gives no rate of changes outside the mask. |
| High input fidelity "allows you to make subtle edits to an image without altering unrelated areas," and with it "faces are preserved far more accurately than in standard mode." | [OpenAI Cookbook, "Generate images with high input fidelity"](https://developers.openai.com/cookbook/examples/generate_images_with_high_input_fidelity) (July 17, 2025). Opened Oct 29, 2026. | Vendor example, now marked archived; shows examples, not measurements. |
| A reviewer made three edits to one ChatGPT image. Changing the outfit also brought "small adjustments" to her expression and hairstyle and resized the cup, plate and table; adding a dog moved a van. Gemini stayed closer but in another edit removed a building and changed her dress and hair. | [Eric Hal Schwartz, TechRadar, May 9, 2025](https://www.techradar.com/computing/artificial-intelligence/i-compared-google-geminis-new-image-editing-feature-to-chatgpts-and-its-much-better-at-sticking-to-the-original); body read through the [Yahoo Tech syndicated copy](https://tech.yahoo.com/ai/articles/compared-google-geminis-image-editing-010000326.html). Opened Oct 29, 2026. | One informal test of one image; the TechRadar page itself did not load in full, so the text was read on Yahoo Tech. |
| A user says that asking ChatGPT for one minor change, such as removing text, makes it "generate a completely new image." | [OpenAI Developer Community, June 12, 2025](https://community.openai.com/t/when-you-ask-to-regenerate-an-image-with-1-minor-change-you-get-completely-new-image/1286219). Opened Oct 29, 2026. | One user's report. The only reply is from another user, not OpenAI staff. |
| A user reports that ChatGPT's edit feature changed "the entire image" at the pixel level, including areas outside the selected region, across repeated tests. OpenAI Support replied on Sept 17, 2026 that the findings were sent to the team for review. | [OpenAI Developer Community, May 10, 2026](https://community.openai.com/t/observed-mismatch-between-chatgpt-image-editing-ui-and-full-frame-regeneration-behavior/1380598). Opened Oct 29, 2026. | The "full-frame regeneration" claim is this user's own analysis. OpenAI's reply neither confirms nor denies it. |

**Incident:** On Jan 31, 2024, AAP reported that Australia's Nine network aired an image of Victorian MP Georgie Purcell altered to show "enlarged breasts and her dress turned into a crop top." Nine "blamed the imagery on an automation function in Adobe's Photoshop program during the resizing of a photo." Adobe said changes "would have required human intervention and approval," and Purcell said "I'm not sure I buy the AI excuse." ([The Nightly, AAP, Jan 31, 2024](https://thenightly.com.au/politics/australia/channel-nines-sexist-ai-image-of-mp-georgie-purcell-labelled-a-wake-up-call-c-13415939), opened Oct 29, 2026.) The cause is disputed; the case shows what happens when an image whose asked-for change was only a resize is aired without comparison to the original. Searches run: "AI image edit changed the whole image not just the part I asked ChatGPT," "image editing benchmark preservation unedited regions over-editing 2025 arXiv," "Gemini nano banana image edit changes face unwanted changes background news 2025," "Nine News Georgie Purcell edited photo Photoshop generative AI automation apology." Results seen only in search summaries (TIEdit and RS-RIE-Bench benchmarks, Digit.in and freshvanroot reviews of Nano Banana) were not opened and are not used. A Tom's Guide article on ChatGPT editing did not load and is not used.

## 5. The fix
**The principle:** An edit request is permission to change one thing. Everything else is a promise to leave it alone, and you check the promise against the original.

**Do this: teams and assistants that edit images with AI**
1. **Write the change list and the keep list before editing.** The keep list always includes real people's faces and bodies, products, property features, text and logos, plus anything the requester names. If the scope is unclear ("make it brighter"), ask one question first.
2. **Edit as locally as the tool allows.** Use a selection or mask and the highest input fidelity setting offered. Treat the mask as a request, not a guarantee; OpenAI says the model may not follow its exact shape.
3. **Compare with the original outside the edit area before showing the result as final.** Use a side-by-side view or a difference overlay, and record which keep-list items changed (following GIE-Bench, which scores only the area outside the edit).
4. **Name every unrequested change in the reply.** Never answer "Done" when anything on the keep list changed. Say what changed and where.
5. **Restore original pixels where an exact match matters.** Composite the edited area back onto the original file, so nothing outside the edit area differs. Use this by default for listings, product images and photos of real people.
6. **Stop after the retry limit and hand off.** If the edit keeps changing keep-list items, stop at the team's limit (3 tries is our proposed starting point) and send it to a person with an image editor.
7. **A named person checks against the original before publish.** Faces and bodies of real people, products, property features and text, side by side with the original.
8. **Keep the original and log every version.** Never overwrite the original. Log the change list, keep list, method, comparison result, changes reported, versions, approver and date.

**Reference design: edit check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Change list and keep list | Written before editing | Change: remove bin. Keep: door, windows, roof, sky |
| Method | Mask or selection; fidelity setting recorded | Mask on bin, high fidelity |
| Comparison | Done outside the edit area; changes listed | Door red to black |
| Reply | Every unrequested change named | "The front door turned from red to black" |
| Restore | Original pixels outside the edit area | Only the bin area differs |
| Sign-off | Named, dated, against the original | M. Chen, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every edit: say whether the asked change was made and whether anything else changed, before anything else |
| Ask one clarifying question | The scope is unclear: "Should the sky change too, or only the trash bin?" |
| Offer choices: 2-4 options plus "Something else", free text open | Something on the keep list changed: paste the original back outside the edit area, retry with a tighter selection, send it to a retoucher, something else. Not offered when nothing else changed. |
| Hand off to a person | The retry limit is reached, and always for the final check on published listings, products and photos of real people |

**Don't over-correct.** Do not flag changes the request asked for across the whole image: "make it look like evening," "turn this into a watercolor," "relight the room," "upscale it." Do not treat compression noise or tiny color shifts the reviewer cannot see side by side as unrequested changes. Do not force the full check on throwaway drafts or mood boards the requester says will not be published. Do not refuse to edit because masks are imperfect; edit, then check.

**Hand-off rule.** If a customer, a person shown in the image or a reviewer reports that a published edited image differs from reality or from the original, send it to the approver and content owner the same day with the original and the log. They decide whether to pull or replace it. Reports about a real person's face or body go to them first.

**Framework used:** none yet. Rules 2 and 3 follow the OpenAI docs, the OpenAI Cookbook and GIE-Bench's outside-the-mask scoring; rules 1 and 4-8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-edit-changes-parts-you-did-not-ask-to-change.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Remove the trash bin" on a listing photo | Change list and keep list written first | 1 |
| 2 | Edit also turns the door black | Reply names the door change; no plain "Done" | 3, 4 |
| 3 | Same edit, listing use | Original pixels restored outside the bin area | 5 |
| 4 | Headshot edit changes the person's smile | Named person checks against the original before publish | 7 |
| 5 | Three tries all change the face | Stops; hands to a retoucher | 6 |
| 6 | "Turn the photo into a watercolor" | Not flagged as unrequested change | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unrequested-change publish rate** (primary) | 0 (proposed) | Monthly sample of published AI-edited images: reviewer compares with the original; keep-list item differs and the log shows no report and approval / all sampled | Any |
| Edits shown with a comparison to the original | 100% (proposed) | Edit log: edits with a recorded side-by-side or difference check / all edits | Below 95% |
| Unreported change rate | 0 (proposed) | Sampled edits where a reviewer finds a keep-list change the reply did not name / all sampled | Any |
| Tries per edit | Track, no target | Edit log: tries before an accepted result or hand-off | Rising for 2 months |
| False change flags (counter-metric) | Track, no target | Sampled flags on edits that asked for a whole-image change | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Next user turn repeats the edit with "keep everything else," "only change" or "don't touch" | Chat log | The user is refining the asked change itself |
| User restores an earlier version or re-uploads the original right after an edit | Version history | The user is branching on purpose to try a different idea |
| Pixel difference outside the edit area above the team's threshold, and the image is still approved | Comparison job plus approval log | The request asked for a whole-image change, such as relighting |
| Customer message says the item, house or person "doesn't look like the photo," for an AI-edited published image | Support tickets, reviews | The real item changed after the photo was taken |

**Starter rule:** no AI-edited image is published unless its log shows a change list, a comparison with the original outside the edit area, every unrequested change reported, and a named person's check of faces, products, property features and text.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-edit-changes-parts-you-did-not-ask-to-change
runs: [pre_edit, post_edit, pre_publish]
reads: [request.text, edit.change_list, edit.keep_list, edit.method, edit.input_fidelity, edit.comparison_result, reply.changes_reported, edit.tries, image.original_kept, review.signoff]
trigger: no change list or keep list, or no comparison with the original, or keep-list item changed and not reported, or retry limit reached, or no sign-off at publish
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Paste the original back outside the edited area", "Retry with a tighter selection", "Send it to a retoucher", "Something else"]
on_miss: block_publish
metric: unrequested-change publish rate
counter_metric: false change flags
status: proposed
```

## 8. Related patterns
- [AI image tools that alter the product reference image you supplied](../../ai-image-brand-guidelines/failures/ai-image-generator-alters-supplied-product-reference-images.md) - the closest page. It covers a brand's own product photo used as a reference for a new scene or ad, where the product comes back changed. This page covers any edit request on any image, where the parts outside the asked change come back changed.
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - the older page on outputs that drift from the prompt over many iterations; here one single edit already changes unrequested areas.
- [Consistency failure: identity loss across generations](../../generation-artifacts/failures/consistency-failure.md) - the same subject looking different across separate generations; here the change happens inside one edit of one image.
- [AI product images that show features it does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - the business side when an edited listing image shows something the product does not have.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the missing sign-off that lets an unrequested change ship.
- [No record of the prompt, model and approver](../../ai-image-generation-business-risks/failures/no-record-of-prompt-model-and-approver-for-ai-images.md) - why rule 8 keeps the original and the log.

## 9. Common questions
### Why does ChatGPT change the whole image when I ask for one small edit?
OpenAI's docs say its mask is guidance the model may not follow exactly, and users report the edit can come back as a new drawing. An Apple benchmark found GPT-Image-1 often changed areas outside the requested edit.

### How do I edit only part of an image with AI?
Select or mask the area, use the highest fidelity setting your tool offers, then compare the result with the original. If anything else changed, paste the edited area onto your original file in an image editor.

### Does saying "keep everything else the same" work?
It may help, but it is not a guarantee. Check the result against the original either way, and name what must not change, such as the face or the product.

### Why did the AI change my face when I only asked to change my outfit?
In TechRadar's 2025 test an outfit edit also brought small changes to the person's expression and hair. OpenAI says its high input fidelity setting preserves faces "far more accurately than in standard mode."

### Are newer models better at leaving the rest alone?
Partly. OpenAI says gpt-image-2 always reads input images at high fidelity, but no opened source measures how often newer models still change unrequested areas. Compare every edit you plan to use.
