# AI Images That Copy Training Images and Show Stock-Photo Watermarks: Near-Copies and Getty-Style Marks in Generated Output

<!-- SEO
title: AI Images Copying Training Photos and Stock Watermarks
description: AI image generators can output near-copies of training photos, even with stock watermarks, and products can catch them before users ship them.
search phrases:
- ai image generator copies training images
- stable diffusion getty watermark
- ai image has watermark in it
- diffusion model memorization images
- ai generated image looks like stock photo
- getty images v stability ai watermark
- check ai image for copied training data
-->

**Frequency**: Occasional

## Issue: AI image generators can output near-copies of training photos, even with stock watermarks, and products can catch them before users ship them.

> **Read this first:** Statements about copyright and trademark on this page summarize the sources cited here, including filed claims and rulings as those sources report them. They are not legal advice and need review by a qualified person, such as a copyright or trademark lawyer, before anyone relies on them.

> **One line:** An image generator hands a user a picture that is almost a copy of one photo it was trained on, sometimes with a smeared "Getty Images" style watermark still on it, and the user posts it as original art; the fix is that the product checks every output against an index of known images and a watermark and logo detector before delivery, and the model vendor removes duplicate images from training data.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. All opened sources concern still images. Video is not covered: no opened source shows a video generator copying a training clip or watermark. |
| **Channel** | Visual: text-to-image generators, image APIs, and the apps and design tools built on them |
| **Stakes** | High. The user may publish a copy of someone's photo or a third party's trademark as their own; the vendor faces claims like those Getty filed (section 4). |
| **Who is affected** | Users who ship generated images (marketers, small businesses, designers), the photographers and stock agencies whose images are copied, and the generator vendor |
| **Frequency** | Occasional, by our reading: researchers extracted copies only with a dedicated search (section 4), and the UK judge said she could not find the watermark cases "widespread". No opened source gives a rate for everyday prompts. |
| **Pattern ID** | ai-images-copy-training-images-and-watermarks |
| **Family** | [AI image copyright and trademark risks](../README.md) |
| **Goal** | AI image and video tools do not reproduce protected characters, artworks, trademarks or training images, and the business using them knows what it can and cannot claim to own. |
| **Primary metric** | Near-copy delivery rate: delivered outputs that match an indexed image above the near-duplicate threshold or carry a detected third-party watermark, divided by all delivered outputs in a weekly sample. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Cleaner, deduplicated training data can reduce copies, but no opened source shows a model that never copies, so an output check is still needed. (Our judgment, not tested.) |
| **Also searched as** | AI image with Getty watermark · Stable Diffusion memorized photo · is my AI image copied · AI art looks like a stock photo · diffusion model regurgitation |

Tests: [AI images copy training images and watermarks test file](../../../tests/ai-images-copy-training-images-and-watermarks.md).

## 1. In plain words
A model learns from millions of photos. Most of the time it blends them. Sometimes it gives back one photo almost exactly, or it paints in the faint watermark a stock site stamped on its pictures, because that mark showed up on so many training images. The user cannot tell. They post the image on a product page, and it carries someone else's photo or someone else's brand.

## 2. What it looks like
The products below are generic. The Getty complaint shows real Stable Diffusion outputs with a modified Getty Images watermark; the dialogue is our illustration.

**Without the fix (image generator)**
```
User:  Photo of two soccer players going for a header, stadium lights, for our
       sporting goods store's Facebook banner.
Tool:  Here are 4 images (1024x1024).
       [Image 2 shows a gray, warped "gettyimages"-style banner across the middle]
User:  Image 2 is great. Download it.
Tool:  Downloaded. Want a matching Instagram size?
```
**With the fix (image generator)**
```
User:  Photo of two soccer players going for a header, stadium lights, for our
       sporting goods store's Facebook banner.
Tool:  Here are 3 images. A 4th was held back: it carried a stock-photo
       watermark, which can signal a copy of a real photo.
       1) Make another in its place  2) Vary image 2  3) Something else
```
**Without and with the fix (near-copy)**
```
Before: Prompt "portrait of [a named person], studio photo". Output matches a known
        photo of that person almost pixel for pixel. Delivered.
After:  Same output. Near-duplicate check: match above threshold to an indexed
        image. Status: held, regenerated with a new seed. Logged with match ID.
```
In the fixed versions the copy never reaches the user, the user still gets a usable image, and the hold is logged so the vendor can find the source.

## 3. Why it happens
- **The model memorizes some training images.** Carlini et al. report that diffusion models memorize individual training images and emit them at generation time (section 4). Our reading, not from an opened source: a photo or watermark repeated many times in training is the likeliest to come back.
- **The watermark is part of the picture the model learned.** Stock photos shown on public sites carry visible watermarks; the Getty complaint says each image on its sites displays one. A model trained on such copies can learn the mark as part of "a sports photo". (Our reading of the complaint.)
- **Nothing compares the output to anything.** Most products filter prompts and outputs for nudity or violence. A near-copy of a stadium photo is neither, so it passes. (Our reading.)
- **The user cannot check.** The user has no access to the training set, so they cannot tell a fresh image from a copy, and a warped watermark can look like noise.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Carlini and eight co-authors report that diffusion models including DALL-E 2, Imagen and Stable Diffusion "memorize individual images from their training data and emit them at generation time". Using a generate-and-filter method they extracted over a thousand training examples, including photos of individual people and trademarked company logos. | [Carlini et al., "Extracting Training Data from Diffusion Models", arXiv 2301.13188, Jan. 30, 2023](https://arxiv.org/abs/2301.13188). Abstract page opened and read; full PDF not read. | A research attack with many generations per prompt, not normal user prompts. The abstract gives no rate for everyday use. |
| Somepalli et al. built image retrieval tools to compare generated images with training samples and report that models, "including the popular Stable Diffusion model, blatantly copy from their training data". | [Somepalli et al., "Diffusion Art or Digital Forgery?", arXiv 2212.03860, Dec. 2022](https://arxiv.org/abs/2212.03860v3). Abstract page opened and read. | Abstract only; no rate read. A follow-up paper on caption duplication was seen only in a search summary and is not used. |
| Getty Images' amended complaint in the US District Court for the District of Delaware (C.A. No. 23-135, filed Mar. 29, 2023) alleges Stability AI copied more than 12 million photographs with captions and metadata, and that "Often, the output generated by Stable Diffusion has contained a modified version of a Getty Images watermark", which it says falsely implies an association with Getty. It shows side-by-side examples. | [Amended Complaint, Document 13, via the Internet Archive's copy of the docket](https://ia601604.us.archive.org/32/items/gov.uscourts.ded.81407/gov.uscourts.ded.81407.13.0.pdf). Opened; text extracted and read. | These are allegations in a filing, not findings. Paragraph 1 also alleges removed or altered copyright management information, false copyright management information, and trademark infringement. |
| SiliconANGLE reported the original Delaware filing and quoted it: "Stable Diffusion often adds the stock photo provider's watermark to the images it generates". | [SiliconANGLE, Maria Deutscher, Feb. 6, 2023](https://siliconangle.com/2023/02/06/getty-images-sues-stability-ai-copyright-trademark-infringement/). Opened and read. | Reports the complaint; the article includes no Stability AI statement. |
| BakerHostetler's tracker says the Delaware case was voluntarily dismissed without prejudice and that Getty intends to file in the Northern District of California. It lists trademark claims "arising from the accused technology's ability to replicate Getty Images' watermarks". | [BakerHostetler case tracker](https://www.bakerlaw.com/getty-images-v-stability-ai/). Opened and read; dates and docket sections are behind a paywall. | No dates shown. Status of any California filing not read. |
| In the UK case, the High Court (Justice Joanna Smith) found no copyright infringement and found Stable Diffusion "did not retain or reproduce copyrighted materials", but ruled that images with the Getty watermark infringed Getty's trademark. She wrote: "While I have found instances of trademark infringement, I have been unable to determine that these were widespread". | [Canadian Lawyer, Jacqueline So, Nov. 5, 2025](https://www.canadianlawyermag.com/news/international/stability-ai-getty-images-split-uk-high-court-win-in-copyright-and-trademark-challenge/393317). Opened and read. | A UK ruling as one outlet reports it, not US law. The article does not say which model versions. Reports on versions and an appeal were seen only in search summaries and are not used. |

**Law.** The opened sources report filed claims and one UK ruling; none says how US courts will treat a near-copy or a watermark in an output. This page does not argue or predict any case. **Needs review** by a qualified person.

## 5. The fix
**The principle:** No output reaches the user if it closely matches a known image or carries a third-party watermark or logo the user did not ask for and has no right to.

The fix sits with two builders.

**Do this: products that deliver generated images (app or API)**
1. **Near-duplicate check on every output.** Before delivery, compare each output with a perceptual or embedding hash against a reference index: the vendor's training set if available, plus licensed stock and known-image sets. A match above the threshold is held, not delivered.
2. **Watermark and logo detector on every output.** Run a detector for stock-photo watermarks and known logos. A hit the prompt did not ask for (and that the account has no rights record for) is held.
3. **Replace, don't just block.** A held image is regenerated with a new seed, or the user is offered choices; the user still gets a usable set.
4. **Log the match.** Keep the output hash, matched image ID, score and detector hit, so the vendor can trace which training images are being copied.
5. **Tell the user plainly.** Say one image was held because it looked like a copy of an existing photo or carried a watermark. Do not claim the remaining images are guaranteed safe.

**Do this: model vendors (training side)**
6. **Deduplicate training data.** Remove exact and near-duplicate images, and images that carry visible stock watermarks, before training. This is vendor-side; a team that only calls an API cannot do it, but should ask the vendor whether it is done.
7. **Feed holds back.** Matched training images found by rule 4 go into the next dedup pass.

**Reference design: decision table**
| Near-duplicate match? | Third-party watermark or logo? | Rights record or user asked for it? | Action |
|---|---|---|---|
| No | No | n/a | Deliver |
| No | Yes | Yes (own logo, licensed asset) | Deliver; log |
| No | Yes | No | Hold; regenerate or offer choices |
| Yes, above threshold | Any | User's own uploaded image (edit) | Deliver; it is their image |
| Yes, above threshold | Any | No | Hold; regenerate; log match ID |
| Borderline score | Any | No | Regenerate; sample for human review |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | An image is held: "Make another in its place", "Vary another image", "Something else" |
| Admit uncertainty and show how to check | The check is borderline: say the image may resemble an existing photo and offer a reverse image search before use |
| Hand off to a person | A rights holder reports a copied image: a reviewer gets the output hash and match log |

**Don't over-correct.** Do not hold a user's own uploaded photo when they edit it; a match to their own upload is expected. Do not hold the user's own logo or a brand asset they have rights to. Do not block generic subjects ("a red apple on a white table", "the Eiffel Tower at night") because many similar photos exist; hold only close matches to one specific image. Do not hold images with any text in them; hold only text that a detector matches to a known watermark or logo. Do not refuse prompts that mention "stock photo style"; check the output, not the words.

**Hand-off rule.** A report from a photographer or stock agency that an output copies their image goes to a human reviewer with the output hash, the match log and the prompt; the reviewer, not the model, decides.

**Framework used:** none yet. The output check follows the retrieval comparison in Somepalli et al. (section 4); training-data dedup is our judgment, not a finding from an opened source.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-images-copy-training-images-and-watermarks.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Soccer header, stadium lights, editorial sports photo" | No delivered image carries a stock watermark | 2, 3 |
| 2 | Output seeded to match an indexed image | Held and regenerated; match logged | 1, 4 |
| 3 | User asked for an image with a held output | User told plainly, offered choices | 3, 5 |
| 4 | User edits their own uploaded photo | Delivered | Don't over-correct |
| 5 | User's own logo on a mug mockup | Delivered | Don't over-correct |
| 6 | Rights holder reports a copy | Sent to a reviewer with the log | Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Near-copy delivery rate** (primary) | 0 (proposed) | Weekly sample of 1,000 delivered outputs re-checked offline with a stricter index / sample size | Any |
| Watermark in delivered output | 0 (proposed) | Detector run on the same sample, hits confirmed by a person | Any confirmed |
| Hold rate | Track; no target (proposed) | Held outputs / all outputs, from the delivery log | Doubles week over week |
| Repeat matches to one training image | 0 repeats after dedup (proposed) | Match log grouped by matched image ID | Same ID matched 3+ times in a week |
| Wrongly held outputs (counter-metric) | Under 2% of holds (proposed) | Sampled holds a reviewer judges not a copy / sampled holds | Over 5% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Output embedding very close to one indexed image | Near-duplicate check result | A famous landmark or product shot many people photograph the same way |
| Gray semi-transparent text band or logo across the middle | Watermark detector result | The user's own logo, or text they asked for |
| Same output hash across different users and seeds | Delivery log | A very short generic prompt with low variety |
| Prompt names a stock site, photographer or "editorial photo" of a known event | Prompt log | A style request with no copy in the output |
| A rights holder report that cites a specific source photo | Support queue | A similar but independent image |

**Starter rule:** no generated image is delivered if it closely matches one known image or carries a watermark or logo the user has no rights to.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-images-copy-training-images-and-watermarks
runs: pre_send
reads: [output.image, output.hash, near_dup.result, watermark_detector.result, request.text, request.uploads, account.rights_records]
trigger: an output matches an indexed image or carries a third-party watermark or logo with no rights record
moves: [offer_choices, admit_uncertainty, hand_off]
choices: ["Make another in its place", "Vary another image", "Something else"]
on_miss: regenerate
metric: near-copy delivery rate
counter_metric: wrongly held outputs
status: proposed
```

## 8. Related patterns
- [Training data leakage and memorization](../../visual-hallucination/failures/training-data-leakage.md) - the closest existing page. It covers vision models that see things learned from training data in new images; here a generator outputs a copy of a training image or its watermark.
- [AI image generator reproduces copyrighted characters](ai-image-generator-reproduces-copyrighted-characters.md) - a sibling page. There the output copies a character like a cartoon mascot, often on request; here it copies one specific photo or watermark, usually without being asked.

## 9. Common questions
### Why does my AI image have a Getty Images watermark?
The model likely learned the mark from watermarked stock photos in its training data. Getty's US complaint alleges Stable Diffusion outputs often contained a modified Getty watermark. Do not use the image; generate another.

### Can AI image generators copy real photos?
Researchers have shown it. Carlini et al. report extracting over a thousand training images from diffusion models, including photos of real people.

### What did the UK court decide in Getty v. Stability AI?
Canadian Lawyer reports the High Court found no copyright infringement but ruled that the watermarked images infringed Getty's trademark, while finding the instances not shown to be widespread. This is a UK ruling as one outlet reports it.

### How can I check whether an AI image is a copy?
Run a reverse image search before you publish it, and look for faint text or logos. A product can do this for you with a near-duplicate check (section 5).

### Is every AI image a copy?
No. The opened sources show copies happen in some cases, mostly found by targeted search; they do not say most outputs are copies.
