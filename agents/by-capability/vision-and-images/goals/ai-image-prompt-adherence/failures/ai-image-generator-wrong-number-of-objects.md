# AI Image Generator Wrong Number of Objects: Ask for Four Chairs, Get Five

<!-- SEO
title: AI Image Generator Wrong Number of Objects: Why Counts Fail
description: Ask an AI image tool for four chairs or three apples and it often draws a different number. Count every image that states a number before you publish it.
search phrases:
- ai image generator wrong number of objects
- dall-e wrong number of items
- how to get exact number of objects in ai image
- ai generated image extra chair
- stable diffusion counting objects
- midjourney exact count prompt
- ai image generator can't count
-->

**Frequency**: Common

## Issue: Ask an AI image tool for "four counter stools," "a box of six donuts" or "three apples" and it often draws a different number, and a team that does not count the result publishes a listing, menu or lesson image that contradicts its own text. Flag every prompt where the number matters, count the objects in each image before it goes out, and build exact counts by layout or compositing when generation keeps missing.

> **One line:** A Denver furniture store asks for "a set of four counter stools at a kitchen island" and the listing image shows five; the fix is to treat any number in an image request as a claim, have someone count the objects in the final image and record the number, and switch to compositing one generated stool four times when regeneration keeps missing.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. All opened studies measure still images. A video that shows a stated number of items has the same risk, but no opened source measures counting in AI video. |
| **Channel** | Text-to-image tools, design tools with built-in generators and assistants that call them, used for product listings, menus, ads, worksheets and how-to images |
| **Stakes** | Medium. A wrong count in a product listing or menu shows the customer something different from what they get; a wrong count in a math worksheet teaches the wrong answer (our judgment). |
| **Who is affected** | Shoppers and diners who order from the image, students and teachers using the worksheet, and the team that published it |
| **Frequency** | Common in tests: no model in a 15-model 2025 benchmark averaged above 50% on exact counts (section 4). No opened source gives a rate in real business use. |
| **Pattern ID** | ai-image-generator-wrong-number-of-objects |
| **Family** | [AI Images That Ignore the Prompt](../README.md) |
| **Goal** | AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text. |
| **Primary metric** | Uncounted-or-wrong-count publish rate: published AI images made from a prompt that states a number that matters, where no count was recorded or the recorded count differs from the request, divided by all such published images. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is five arXiv papers (preprints or conference versions not checked), one vendor model report and one forum thread. |
| **Will a better model fix this?** | Partly. In one 2025 test GPT-4o drew 1, 2 or 3 objects right every time but 10 objects right only 12.5% of the time, so small counts are improving and larger ones are not (our judgment, drawing on the cited tests). |
| **Also searched as** | AI image extra object · AI can't draw exact number · DALL-E counting problem · AI image extra item · AI menu photo wrong portion |

Tests: [AI image generator wrong number of objects test file](../../../tests/ai-image-generator-wrong-number-of-objects.md).

## 1. In plain words
A furniture store sells counter stools in sets of four. The marketer asks an image tool for "a set of four counter stools at a kitchen island." The picture looks great, so it goes on the listing. It shows five stools. Customers order a set, get four, and ask where the fifth one is. The text said four; the picture said five. Nobody counted.

## 2. What it looks like
The store, people and SKU below are invented.

**Without the fix**
```
Marketer:  Listing image for SKU 4410: a set of four oak counter stools at a white kitchen island.
Assistant: Here is your image. (One generation; it shows five stools.)
Marketer:  Looks great, publishing.
Customer (two weeks later): I ordered the set in the photo and only four came.
           Where is the fifth stool?
```
**With the fix**
```
Marketer:  Listing image for SKU 4410: a set of four oak counter stools at a white kitchen island.
Assistant: Your request states a count (4 stools), so I counted each result before showing it.
           Three tries drew 5, 3 and 5 stools. None matched.
           Options: I composite one generated stool four times on the island; use your
           product photo of the set; show one stool close up with "Set of 4" in the
           listing text; something else.
Marketer:  Composite it.
Assistant: Done. Counted: 4 stools. Sent to Dana Ruiz (merchandising) to recount and approve.
```
The fixed version counts every image, says the counts it got, stops regenerating after a few misses, offers a way to build the exact count and ends with a person recounting.

## 3. Why it happens
- **The noise, not the prompt, sets how many shapes appear.** Zhao et al. found "diffusion models tend to rely heavily on the noise initialization": the random starting pattern decides the layout, and the number in the prompt only weakly steers it.
- **Each object has to be tracked as a separate thing.** Binyamin et al. write that "controlling the number of depicted objects using text is surprisingly hard," because the model must keep look-alike, overlapping objects apart and keep a running total while it draws.
- **Bigger numbers fail more, and wording tricks do not help.** In T2ICountBench, accuracy for 6 to 10 objects fell to roughly 10% to 30%, and rewriting the prompt as "3 times 4" or a grid made results worse than the plain prompt.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| T2ICountBench tested 15 tools, including DALL-E 3, Firefly 3, FLUX 1.1, Gemini 2.0 Flash and Imagen-3. "No model achieves an average accuracy above 50%"; the best, Imagen-3, averaged 43%, DALL-E 3 30%, Firefly 3 34%. Accuracy was roughly 60% to 80% for 1 to 5 objects and 10% to 30% for 6 to 10. | [Guo et al., "Text-to-Image Diffusion Models Cannot Count, and Prompt Refinement Cannot Help," arXiv 2503.06884](https://arxiv.org/abs/2503.06884) (v1 March 10, 2025; v2 Jan 23, 2026). Abstract and HTML full text opened Oct 29, 2026. | Preprint. Graded by five graduate students (Fleiss' kappa 0.58). A prompt passed if any one of four images was right, so a single image may do worse. Range figures are read from the paper's text, not exact per-model numbers. |
| Same paper: four prompt rewrites (multiply, add, grid, left-and-right groups) averaged 0.20 to 0.34 accuracy against 0.42 for the plain prompt; "all four types of prompt refinement lead to worse performance." | Guo et al., as above. | Home scene and plain style only, averaged over 15 models. |
| GenEval asks for 2, 3 or 4 objects and checks with an object detector at a 0.9 confidence threshold. Counting scores: Stable Diffusion 1.5 0.35, SD 2.1 0.44, SDXL 0.39, IF-XL 0.66. The detector agreed with human raters on 82.3% of counting checks. | [Ghosh et al., "GenEval," arXiv 2310.11513](https://arxiv.org/abs/2310.11513) (Oct 17, 2023). Abstract and HTML full text opened Oct 29, 2026. | 2022-2023 open models. Detector trained on 80 COCO object types, so it cannot count most products. |
| GPT-4o drew 1, 2 and 3 objects right 100% of the time but 10 objects 12.5%, averaging 71.13% on counts 1 to 10; FLUX.1 pro averaged 57.13%, Ideogram V2 31.38%. | [Zhao et al., "Demystifying Numerosity in Diffusion Models," arXiv 2510.11117](https://arxiv.org/abs/2510.11117) (Oct 13, 2025). HTML full text opened Oct 29, 2026. | Preprint. Manually annotated, per the authors. Simple "N objects" prompts only. |
| Imagen 3 scored 58.6% on exact counts of 1 to 10 objects, "outperforming the second one, DALL·E 3, by 12 percentage points"; numerical reasoning is "challenging for all models." | [Imagen-Team-Google, "Imagen 3," arXiv 2408.07009](https://arxiv.org/abs/2408.07009) (v3 Dec 21, 2024). HTML opened Oct 29, 2026. | Google's own test of its own model; not independent. |
| A user building math visuals asked DALL-E for "2 apples on the table; 3 apples on the floor" and got the wrong numbers; the only reply said "No solution for now." | [OpenAI Developer Community, Jan 4, 2025](https://community.openai.com/t/how-to-prompt-to-get-number-of-object-accurate/1079735). Opened Oct 29, 2026. | One user's report. The reply is from another user, not OpenAI staff. |
| Google's DOCCI dataset lists "counting" among the details its images were built to test and shows "the limitations of current text-to-image models in capturing long descriptions and fine details." | [Onoe et al., "DOCCI," arXiv 2404.19753](https://arxiv.org/abs/2404.19753) (April 30, 2024). Abstract opened Oct 29, 2026. | Abstract only; gives no counting rate. |

**Incident:** No public incident found where a business published an AI image with the wrong count and was called out for it. Searches run: "AI image generator wrong number of objects counting benchmark 2025," "gpt-image-1 counting objects accuracy exact number prompt OpenAI image generation limitations," "'how many' text-to-image counting layout-guided generation exact count 2026." Other 2025 papers seen only in search summaries (CountCluster, CountLoop, Testolin et al.) were not opened and are not used.

## 5. The fix
**The principle:** A number in an image request is a claim the image makes. Count it like you would proofread a price.

**Do this: teams and assistants that make images with a stated number**
1. **Flag count-bearing prompts.** Before generating, mark any request with a number or number word next to a countable object ("four stools," "a dozen eggs," "3 apples") as "count matters," unless the requester says the number is only mood.
2. **Write the count once, plainly.** Use a digit or number word next to the object and one count per object type. Do not count on "exactly," grids or math phrasing to fix it; Guo et al. found those rewrites did worse.
3. **Count every image before showing it as final.** Record the number of each counted object in the image. A person does the final count for anything published. A detector count may pre-screen (proposed, following GenEval's method), but not as the only check, since it disagreed with human raters on about one in six counting checks and knows few product types.
4. **Regenerate, then stop.** If the count is wrong, regenerate and count again, up to a limit the team sets (3 tries is our proposed starting point). Tell the requester the counts each try produced.
5. **Build exact counts another way after the limit.** Composite one generated object into a layout the right number of times, use a real product photo, or choose an image that does not depend on the count (one item close up with the count in text). For counts above 5, start here instead of regenerating (our proposed cutoff, from the drop T2ICountBench found above 5).
6. **Never change the text to match a wrong image.** If the set has four stools, the image must show four; do not edit the listing to "set of 5."
7. **A named person recounts before publish.** Listings, menus, ads and teaching images with a stated count need a recorded recount and approval.
8. **Log it.** Requested count, counted number per try, method (generated or composited), counter, approver and date.

**Reference design: count check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Prompt type | Count-bearing prompt flagged | "four oak counter stools" flagged |
| Count per try | Recorded for each image | 5, 3, 5 |
| Retry limit | Stopped at the team's limit | 3 tries |
| Method | Composited or real photo after limit | One stool placed 4 times |
| Text vs image | Listing text and image agree | "Set of 4," 4 stools |
| Recount | Named, dated | D. Ruiz, Oct 29, 2026: 4 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every count-bearing result: say the requested count and the counted number before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | The retry limit is reached: composite the object, use a product photo, show one item with the count in text, something else. Do not offer them when the count already matches. |
| Ask one clarifying question | It is unclear whether the number matters: "Does the image need to show exactly 12 cupcakes, or just a full tray?" |
| Hand off to a person | Always for the final recount on published listings, menus, ads and teaching images |

**Don't over-correct.** Do not flag plurals with no number ("a bowl of apples," "a busy café"). Do not count numbers that are not object counts ("a 1950s diner," "Route 66 sign," "a 3D render"). Do not count background clutter the request never numbered. Do not block mood images where the requester said the number is approximate. Do not regenerate without limit; each try costs time and money and, per the studies above, larger counts rarely come right by chance.

**Hand-off rule.** If a customer, teacher or reviewer reports a wrong count in a published image, send it to the approver and content owner the same day with the log. They decide whether to replace it.

**Framework used:** none yet. Rules 2 and 5 follow Guo et al.; rule 3 follows GenEval's detector method and its measured agreement; rules 1, 4 and 6-8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-wrong-number-of-objects.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "A set of four counter stools" | Flagged; count recorded per image | 1, 3 |
| 2 | Three tries all miss | Stops; counts told; options offered | 4, 5 |
| 3 | "Twelve cupcakes on a tray" for a menu | Built by compositing or photo from the start | 5 |
| 4 | Asked to change listing to "set of 5" | Refused; image fixed instead | 6 |
| 5 | Image scheduled with no recount | Publish blocked | 7 |
| 6 | "A bowl of apples" | Not flagged | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Uncounted-or-wrong-count publish rate** (primary) | 0 (proposed) | Monthly sample of published images from flagged prompts: log has no recorded recount, or recount differs from requested count / all sampled | Any |
| Text-image count mismatch | 0 (proposed) | Sampled review: number in listing or caption text vs objects counted in the image | Any |
| Tries per count-bearing image | Track, no target | Generation log: tries before a matching count or the switch to compositing | Rising for 2 months |
| False count flags (counter-metric) | Track, no target | Sample of flagged prompts where the number was not an object count or was marked approximate | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt with a number next to an object, one generation, image published, no count field | Generation log plus publish log | The number was marked approximate by the requester |
| Recorded count differs from requested count and the image is still approved | Count log plus approval log | The requester changed the brief to that count, logged elsewhere |
| Listing or caption text edited to a new number after the image was generated | CMS edit history | The product itself changed |
| Customer message or return reason mentions "missing," "only got" or a number, for an item with an AI listing image | Support tickets | A real shipping shortage |

**Starter rule:** no AI image made from a prompt that states an object count is published unless its log shows a recorded count that matches the request and a named person's recount.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-wrong-number-of-objects
runs: [pre_generation, post_generation, pre_publish]
reads: [request.text, prompt.as_sent, request.count_marked_approximate, image.counted_number, generation.tries, image.method, listing.text_count, review.recount, review.signoff]
trigger: count-bearing prompt with no recorded count, or counted number differs from requested, or retry limit reached, or no recount at publish
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Composite one object the right number of times", "Use our product photo", "Show one item with the count in the text", "Something else"]
on_miss: block_publish
metric: uncounted-or-wrong-count publish rate
counter_metric: false count flags
status: proposed
```

## 8. Related patterns
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - the closest older page. It covers outputs that drift away from a prompt over repeated edits; here the very first image already has the wrong count from a short, clear prompt.
- [Token limit artifacts](../../generation-artifacts/failures/token-limit-artifacts.md) - details dropped because a long prompt was cut off; a count fails even in a five-word prompt well inside the limit.
- [AI product images that show features it does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - the business and legal side of a listing image that promises something the product does not include; this page is the counting check that prevents one cause of it.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the missing sign-off that lets a wrong count ship.

## 9. Common questions
### Why can't AI image generators count?
The random starting pattern largely decides how many shapes appear, and the model has to keep similar objects apart while drawing. Zhao et al. trace the problem to that starting noise, and Binyamin et al. call count control "surprisingly hard."

### How do I get an exact number of objects in an AI image?
Write the count plainly, then count the result yourself. If a few tries miss, or the count is above about five, generate one object and place copies in a layout tool, or use a real photo.

### Does writing "exactly" or using a grid in the prompt help?
In T2ICountBench, grid and math-style rewrites did worse on average than the plain prompt. Keep the prompt simple and check the image.

### Are newer models better at counting?
For small numbers, yes in some tests: GPT-4o got 1 to 3 objects right every time in one 2025 study. At 10 objects it was right 12.5% of the time, so counting larger sets still needs a check.

### Can I use an AI vision model to count instead of a person?
As a first screen, possibly. GenEval's detector agreed with people on about 82% of counting checks for common objects, so a person should still recount anything you publish.
