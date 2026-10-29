# Approved AI Image Cannot Be Made Again: Same Prompt, Different Output

<!-- SEO
title: Approved AI Image Can't Be Recreated: Same Prompt, Different Output
description: A team reruns the prompt behind an approved AI image and gets a different one. Keep the approved file as the master and edit from it, never regenerate it.
search phrases:
- same prompt different image every time
- how to recreate the same ai image
- midjourney same seed different image
- dall-e 3 seed parameter
- regenerate exact same ai image
- client approved ai image need higher resolution
- stable diffusion same seed different result gpu
- ai image not reproducible
-->

**Frequency**: Common

## Issue: A team gets sign-off on an AI-made image, later reruns the same prompt to get a new size, a fix or a higher resolution, and the generator returns a different image that nobody approved. Keep the approved output as the master file with its full generation record, make every variant by editing that file, and treat any regeneration as a new image that needs new approval.

> **One line:** A brand approves an AI catalog image, the designer reruns the saved prompt for a print size and gets a different room; the fix is to store the original output as the master, make every variant from it, and treat any regeneration as a new image.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. The sources opened are image generator docs and forums. Video generators were not researched for this page. |
| **Channel** | Ad, catalog, packaging, web and social images made with an image generator (Midjourney, DALL-E 3 and its successors, Stable Diffusion-family models through Diffusers or ComfyUI) |
| **Stakes** | Medium. The usual cost is rework and a second approval round. It turns into a publishing risk when the regenerated image goes out under the old approval (our judgment). |
| **Who is affected** | The designer or agency, the brand owner who approved the image, legal or compliance reviewers whose sign-off covered the old image, and print or media vendors waiting on files |
| **Frequency** | Common, by our reading. The vendor docs say a new random seed is used on every run unless one is fixed, and some tools offer no seed at all (section 4). No opened source gives a rate. |
| **Pattern ID** | approved-ai-image-cannot-be-reproduced |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unmastered approval rate: approved AI images with no stored master file (original output at full resolution plus its generation record) linked to the approval, divided by all approved AI images sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Different outputs from the same prompt are how these tools are built, and vendors retire and update models. Only keeping the file fixes it. (Our judgment, not tested.) |
| **Also searched as** | recreate AI image exactly · same seed not working Midjourney · DALL-E 3 no seed · AI image regenerate for print · lost original AI image |

Tests: [Approved AI image cannot be reproduced test file](../../../tests/approved-ai-image-cannot-be-reproduced.md).

## 1. In plain words
An image generator starts each image from random noise. If you do not fix the starting noise (the "seed"), you get a new picture every run. Some tools let you fix it; DALL-E 3 did not, according to Microsoft's forum answers. Even with a fixed seed, a new model version, a changed setting or different hardware can change the result. So the prompt is not a recipe for the approved image. The approved file is the only copy. Teams lose it when they save a screenshot or a compressed preview, approve a thumbnail, or plan to "just rerun it" for print later.

## 2. What it looks like
The brand, people and IDs below are invented.

**Without the fix**
```
Brand lead: Approved. The living room with the green sofa is our fall catalog cover.
Designer:   Great, I'll save the prompt.
            [Two weeks later] Printer needs 300 dpi and a 9:16 version for Instagram.
Designer:   [Reruns the saved prompt in the generator.]
Generator:  [New image: a gray sofa, a different window, a lamp where the plant was.]
Designer:   Close enough. Sending to the printer and the ad team.
Brand lead: This isn't the room I approved. The sofa isn't even our Harlow model.
```
**With the fix**
```
Designer:   Approved. Saving the master: original PNG at full size, prompt, model and
            version, seed, settings, tool and date, linked to approval A-2291.
            [Two weeks later] Printer needs 300 dpi and a 9:16 version.
Asset tool: A-2291 has a master. Variants come from it. Pick one:
            1) Upscale the master  2) Extend the canvas to 9:16 from the master
            3) Regenerate (makes a new image that needs new approval)  4) Something else
Designer:   2, then 1.
Asset tool: Variant A-2291-v2 made from the master. Changed area marked for the brand lead.
```
In the fixed version nobody reruns the prompt to get the approved image back. The variant is built from the saved file, and the one changed area goes back for review.

## 3. Why it happens
- **Every run starts from new noise unless a seed is fixed, and some tools give no seed.** Midjourney says that without a chosen seed it "will use a new random one every time." Microsoft's moderators said a seed "is not available in Dalle-3 model." A team that saved only the prompt saved nothing that brings the image back.
- **A fixed seed is not a fixed result.** Midjourney warns seeds "shouldn't be relied on for the same results over different prompting sessions" and that the prompt, model version and settings changes can all change the output. Diffusers and PyTorch say results can differ between CPU and GPU and across releases even with the same seed.
- **The model itself goes away.** OpenAI's forum notice says DALL-E 2 and DALL-E 3 were deprecated on May 12, 2026. An image approved on a retired model cannot be regenerated on it at all.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "If you don't choose a seed, Midjourney will use a new random one every time." Seeds "shouldn't be relied on for the same results over different prompting sessions. Assume that if you take a break and come back later, your seed may no longer work as expected." "Factors like your prompt, model version, and even slight parameter or settings changes can lead to unexpected results." In Turbo mode "seed locking is not reliable." The page also says seeds are "99% identical in V8.X." | [Midjourney Docs, Seeds](https://docs.midjourney.com/docs/seeds). The fetch tool got HTTP 403; the page was opened with a direct download (redirects to the help center article) and read Oct. 29, 2026. Quotes copied from the saved text. | Vendor documentation, current version only. "99% identical" is Midjourney's own claim with no method given. |
| Diffusers: "Diffusion is a random process that generates a different output every time." A GPU generator "can diverge from CPU results." Limiting randomness is possible "but it is not *guaranteed* even with an identical seed." Passing the same Generator object twice gives different results because "its state has changed." | [Hugging Face Diffusers docs, Reproducibility](https://huggingface.co/docs/diffusers/en/using-diffusers/reusing_seeds). Opened Oct. 29, 2026. | Applies to open models run with the Diffusers library, not to hosted tools. |
| PyTorch: "Completely reproducible results are not guaranteed across PyTorch releases, individual commits, or different platforms." Results "may not be reproducible between CPU and GPU executions, even when using identical seeds." | [PyTorch notes, Reproducibility (2.15)](https://docs.pytorch.org/docs/2.15/notes/randomness.html). Opened Oct. 29, 2026. | Framework documentation, not about images specifically. |
| A user asked how to use seeds in DALL-E 3 "to get the consistency of generating images." A Microsoft moderator answered on June 17, 2024: "AFAK, Seed is not available in Dalle-3 model." | [Microsoft Q&A, Seeds in Dalle3](https://learn.microsoft.com/en-us/answers/questions/1696166/seeds-in-dalle3). Opened Oct. 29, 2026. | Forum answer, hedged ("AFAK"), Azure OpenAI, 2024. |
| A second Microsoft Q&A answer, Feb. 14, 2024, from a user named Charlie Wei: "reproducible output is not supported on DALL-E." The asker was trying to keep images consistent for a comic-book story. | [Microsoft Q&A, deterministic output in dalle3](https://learn.microsoft.com/en-us/answers/questions/1531341/generate-images-with-deterministic-output-using-se). Opened Oct. 29, 2026. | Community answer, not official docs. |
| A forum notice says "Dall-e-2" and "Dall-e-3" are deprecated "on May 12, 2026," and points users to "gpt-image-1.5 or gpt-image-1- mini." Posted April 9, 2026. | [OpenAI Developer Community](https://community.openai.com/t/deprecation-reminder-dall-e-will-be-shut-down-on-may-12-2026/1378754). Opened Oct. 29, 2026. | Community post by a forum user, not OpenAI's own deprecations page. |
| A user asked how to "generate the exact same image twice from the same prompt" after trying ChatGPT, Adobe Firefly and ComfyUI (Nov. 26, 2024). The only concrete reply was to fix the seed. | [Hugging Face Forums](https://discuss.huggingface.co/t/how-can-i-generate-the-exact-same-image-twice-using-ai-image-generation-tools/127913). Opened Oct. 29, 2026. | One user's question. Shows the need, not a business loss. |

**No public incident found** of a business that lost an approved AI image this way. Searches run: "Midjourney seed parameter same seed same prompt identical image docs"; "OpenAI gpt-image-1 seed parameter not supported reproduce same image API"; "cannot recreate AI generated image client approved regenerate different result"; and a search for brands or agencies reproducing approved assets from the same prompt. **Read only through summaries (not used in the fix):** vendor blog posts (neurohive, Fast.io, Morphic, a Pollo AI article) on brand consistency through reference images and audit trails, and whether gpt-image models accept a seed. We did not open those or the current OpenAI image API reference.

## 5. The fix
**The principle:** The approved file is the asset. A prompt and a seed are notes about how it was made, not a way to make it again.

**Do this: designers, agencies and asset tools**
1. **Save the master at approval.** Approval is recorded only against a stored master: the original output file at full resolution, not a screenshot, preview or chat download that was resized or compressed.
2. **Save the generation record with it.** Prompt, negative prompt, reference images, tool, model name and version, seed (or "no seed offered"), settings, mode, and date. For self-hosted models also the library versions and CPU or GPU.
3. **Approve the master, not a preview.** The approver sees the stored master or a view of it with its ID. An approval that points at no master ID is not an approval.
4. **Make every variant from the master.** Resizes, crops, upscales, canvas extensions and small fixes start from the master file. The variant gets a child ID and the changed areas are marked.
5. **Treat regeneration as a new image.** Rerunning a prompt, even with the same seed, makes a new asset ID with no approval. It never inherits the old one.
6. **Get the needed sizes before sign-off when you can.** List print, web and social sizes in the brief and produce them from the master while the project is open.
7. **Re-approve changed areas.** A variant that adds or changes content (an extended canvas, a replaced object) goes back to the approver with the change marked. A pure resize or crop does not.
8. **Check before the model is retired.** When a vendor announces a model retirement, list live campaigns whose masters were made on it and confirm each master is stored.

**Reference design: master record (one per approved image)**
| Field | Example | Pass if |
|---|---|---|
| Master file | A-2291.png, 2048 x 2048, original output | Stored, not a screenshot or preview |
| Generation record | Prompt, model and version, seed 41877, settings, tool, Oct. 3 | All fields present, or "not offered" stated |
| Approval | Brand lead, Oct. 3, approval of A-2291 | Points at the master ID |
| Variants | A-2291-v2 (9:16 extend), A-2291-v3 (upscale) | Each made from the master; changed areas marked |
| Regenerations | A-2310 (new prompt run) | New ID, no approval inherited |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The tool says up front whether the approved image has a master and that variants come from it |
| Offer choices: 2-4 options plus "Something else" | A size or fix is needed: upscale, extend, regenerate as new, something else. Do not offer them when the request is a plain resize; just do it from the master. |
| Admit uncertainty and show how to check | Someone asks if the same seed will bring the image back: say it may not, and point to the stored master |
| Hand off to a person | The master is lost and a live campaign depends on it: the brand owner decides between a new approval and pulling the asset |

**Don't over-correct.** Do not ban regeneration; new images for new work are the point of the tool. Do not demand pixel-identical reruns before approving a tool, since the vendors say they cannot promise them. Do not send every crop or resize back for approval; only variants that add or change content need it. Seeds are still useful for testing prompt changes, which is what Midjourney says they are for.

**Hand-off rule.** If an approved image has no stored master and a live or scheduled campaign needs a new version, the asset tool stops and sends it to the brand owner with what is known (preview, prompt, record). Nothing ships as "the approved image" until they approve a new master.

**Framework used:** none yet. Rules 2 and 5 follow the Midjourney, Diffusers and PyTorch statements in section 4; rule 8 follows the DALL-E retirement notice; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/approved-ai-image-cannot-be-reproduced.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Approval recorded against a screenshot | Blocked until a master is stored | 1, 3 |
| 2 | Master saved with no model version | Record flagged incomplete | 2 |
| 3 | Print needs 300 dpi of an approved image | Upscaled from the master | 4 |
| 4 | Designer reruns the prompt with the same seed | New ID, no approval inherited | 5 |
| 5 | 9:16 extension adds new content | Sent back with the change marked | 7 |
| 6 | Model retirement announced | Live masters listed and checked | 8 |
| 7 | Master lost, campaign live | Handed to the brand owner | Hand-off |
| 8 | Plain crop of the master | Ships with no new approval | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unmastered approval rate** (primary) | 0 (proposed) | Monthly sample of approved AI images: no master ID linked / all sampled | Any |
| Masters with an incomplete generation record | Under 5% (proposed) | Record field check | Over 10% |
| Published images with no path back to an approved master | 0 (proposed) | Published asset hashes joined to master and variant IDs | Any |
| Regenerations shipped under an old approval ID | 0 (proposed) | Asset log: new generation job linked to an existing approval | Any |
| Live masters on a retiring model not confirmed stored | 0 by the retirement date (proposed) | Model field joined to vendor retirement list | Any after notice |
| Resizes and crops sent for re-approval (counter-metric) | Under 10% of variants (proposed) | Variant log by change type | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Generation job run with a prompt copied from an approved asset's record | Generator or asset log | A deliberate new concept based on the old prompt |
| Approved file is a low-resolution PNG or JPEG with no generation record | Asset store | An image that was not AI-made, such as a photo |
| Published image hash matches no master or variant | Ad, web or print export vs. asset store | A vendor or platform recompressed the file |
| Approver comment "this isn't what I approved" after a resize request | Review tool comments | Approver changed their mind about the original |

**Starter rule:** no AI image is marked approved unless its original output file and generation record are stored and the approval points at that file's ID.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: approved-ai-image-cannot-be-reproduced
runs: [on_approval, on_variant_request, on_generate, on_model_retirement]
reads: [approval.asset_id, asset.master_file, asset.generation_record, job.prompt, vendor.retirement_list]
trigger: approval with no stored master, a variant made by regeneration, or a regeneration linked to an existing approval
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Upscale the master", "Extend the canvas from the master", "Regenerate as a new image needing approval", "Something else"]
on_miss: block_approval
metric: unmastered approval rate
counter_metric: resizes and crops sent for re-approval
status: proposed
```

## 8. Related patterns
- [Consistency failure](../../generation-artifacts/failures/consistency-failure.md) - the closest existing page and an overlap. It covers the same subject drifting across many generations (frames of a character, a product series) and suggests seed reuse as a fix. This page covers getting one already-approved image back later; it says a seed is not enough and the stored file is the fix. A merge or cross-link is proposed for a person to decide.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the sign-off step. This page adds that sign-off must point at a stored master, so a regenerated image cannot ride on it.
- [Quality drift](../../generation-artifacts/failures/quality-drift.md) - output quality changing over time; a model update is one reason an old seed stops working.
- [AI image mistakes in ads that go viral](./ai-image-mistakes-in-ads-go-viral.md) - what happens when an unchecked regeneration ships with an error.

## 9. Common questions
### Why does the same prompt give a different image every time?
The generator starts from random noise. Midjourney says that without a chosen seed it uses a new random one every time.

### If I save the seed, can I get the exact same image back?
Not reliably. Midjourney says seeds should not be relied on across sessions, and the Diffusers docs say reproducibility "is not *guaranteed* even with an identical seed." Save the image file itself.

### Does DALL-E 3 have a seed?
Microsoft forum answers from 2024 say no. A notice in OpenAI's developer forum says DALL-E 2 and DALL-E 3 were set to shut down on May 12, 2026.

### The client approved a small image. How do I get a print version?
Upscale or extend the original output file. Do not rerun the prompt; that makes a different image that needs new approval.

### Is a regenerated image that looks almost the same still approved?
No. Treat it as a new image. Small differences, like a different sofa or a new lamp, are exactly what the approver did not see.
