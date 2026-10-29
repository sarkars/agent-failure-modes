# AI Image Content Credentials Stripped on Resize or Upload: Your Own Pipeline Removes the AI Label

<!-- SEO
title: AI Image Label Stripped on Resize or Upload: Keep C2PA
description: Your resize step, CDN or social scheduler drops the C2PA and IPTC AI label your image tool added. Map each step, keep the label and check the served file.
search phrases:
- content credentials removed after resize
- cdn strips c2pa metadata
- cloudflare images preserve content credentials
- sharp resize removes metadata c2pa
- keep iptc digital source type on upload
- ai image label lost after webp conversion
- how to keep ai label on generated images website
-->

**Frequency**: Common

## Issue: Your resize step, CDN or social scheduler drops the C2PA and IPTC AI label your image tool added. Map each step, keep the label and check the served file.

> **Read this first:** This page describes vendor settings and standards documents as we read them on October 29, 2026. It makes no claim about what any AI labeling law, platform rule or advertising rule requires; any such question needs review by a qualified person, and nothing here is legal advice. Keeping Content Credentials in a file is a technical step, not proof that a business has met a labeling duty.

> **One line:** An Austin home-goods store generates room scenes with a tool that signs them as AI-made, then its own CMS resizes them, converts them to WebP and serves them through a CDN set to remove metadata, so the images on the live sale page carry no AI label at all; the fix is to list every step a file passes through, switch each one to keep and re-sign the label or mark it as one that strips, and check the file served from the live URL, not the original.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The opened vendor docs (Cloudflare, Fastly, Cloudinary, sharp) are about still images; the opened Fortune report is about social video encoders stripping credentials from uploaded videos. |
| **Channel** | The builder's own path from generator to viewer: editing tools, image libraries, CMS and DAM upload, image CDN, social schedulers and ad uploads |
| **Stakes** | Medium to high. Every image that leaves unlabeled looks the same as a camera photo to any checker downstream, and the business may believe its outputs are labeled when they are not (our judgment). |
| **Who is affected** | People who see the images and cannot tell they are AI-made; the team that relies on the generator's label for its own disclosure; platforms that read the label |
| **Frequency** | Common, our judgment. Two opened tools remove all metadata by default (Fastly Image Optimizer, the sharp library) and Cloudflare says credentials "would frequently be stripped" by a CDN. No opened source measures a rate for AI outputs. |
| **Pattern ID** | ai-image-pipeline-strips-content-credentials-on-resize-or-upload |
| **Family** | [AI Image Watermarks, Labels and Content Credentials](../README.md) |
| **Goal** | AI images and video carry provenance signals that reach the people and platforms who see them: a mark on every output, credentials that survive the trip, and labels that are read correctly. |
| **Primary metric** | Served-copy label survival rate: AI images whose live, served file still carries a valid C2PA manifest and the IPTC Digital Source Type, divided by all AI images published. Proposed starting target: 100%, or a logged exception with a visible label. |
| **Maturity** | Researched. Evidence is one standards explainer, one NIST report, one news report and vendor docs. |
| **Will a better model fix this?** | No. The label is lost in file handling after the model is done; a better generator signs the same file and the same pipeline strips it. (Our judgment, not tested.) |
| **Also searched as** | c2pa lost after cdn · content credentials not showing on my website · next.js image optimization metadata · webp conversion removes xmp · scheduler removes ai label |

Tests: [AI image pipeline strips content credentials test file](../../../tests/ai-image-pipeline-strips-content-credentials-on-resize-or-upload.md).

## 1. In plain words
Many image generators put two labels inside the file: a signed Content Credentials record (the C2PA standard) and an IPTC "digital source type" field that says the image was made by AI. Those labels live in the file's metadata. Most resize tools, format converters and image CDNs throw metadata away to save bytes unless someone turns a setting on. So the generator does its job, and the business's own website or scheduler removes the label before anyone sees the image.

This page is the builder's side. The reader's side, where someone runs a checker, finds no credentials and calls the image real, is covered on [provenance metadata stripped](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-metadata-stripped.md).

## 2. What it looks like
The store, people and settings below are invented examples.

**Without the fix**
```
Marketer:  Publish these 12 AI room scenes to the spring sale page and schedule them for Instagram.
Assistant: Done. All 12 are live at /spring-sale and scheduled for Friday 9 a.m.
           They were made in our image tool, which adds Content Credentials.
(The CMS made 3 sizes in WebP; the CDN zone is set to remove metadata.
 None of the 12 served files has a manifest or a Digital Source Type.)
```
**With the fix**
```
Marketer:  Publish these 12 AI room scenes to the spring sale page and schedule them for Instagram.
Assistant: The 12 originals carry Content Credentials, but the copies our CDN serves have none:
           the zone's metadata setting removes them. Choose one:
           "Hold until Dana turns on credential preservation and I re-check"
           · "Publish now with a visible 'AI-generated image' caption" · "Something else"
Marketer:  Hold until Dana fixes it.
Assistant: Held. I sent Dana Ruiz (web lead) the zone name and the failed check.
```
The fixed assistant checks the served file, says which step stripped the label, offers choices and hands the setting change to a person.

## 3. Why it happens
- **Delivery tools default to removing metadata.** Fastly's docs say "By default, the image optimizer will remove all metadata embedded in an image," and the sharp library's docs say "By default all metadata will be removed." A team that never touches the setting strips the label on every resize.
- **Preservation is a separate switch, often per zone or per URL.** Cloudflare keeps credentials only when a zone toggle is on, and its docs say "When this setting is disabled, any existing Content Credentials will always be discarded." Cloudinary's 2024 post ties preservation to an `fl_c2pa` flag for beta customers. A setting turned on for one zone, path or format is easy to miss on another.
- **Teams check the file they made, not the file users get.** The generator's output carries the label, so it looks done. The C2PA explainer notes that a crop in "a non-Content Credentials aware tool" can go unrecorded; the loss shows only in the served copy.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "Can the provenance metadata be removed? Yes it can." The answer is "durable Content Credentials": a hash binding plus a watermark or fingerprint, so the credential can "be discovered in cloud-hosted storage even if it is removed from the asset." | [C2PA Explainer, v2.3](https://spec.c2pa.org/specifications/specifications/2.3/explainer/Explainer.html). Opened Oct 29, 2026. | Standards guidance, not a measurement. |
| Metadata "can similarly be stripped altogether, as it often is when files are shared (e.g., via social media platforms)," for deception or "benign reasons such as privacy protection." Use depends on "users and platforms not stripping the metadata (or at least saving it in external metadata repositories, which do not yet exist on a wide scale)." | [NIST AI 100-4, *Reducing Risks Posed by Synthetic Content*, Nov 2024](https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-4.pdf). PDF opened Oct 29, 2026. | Overview report; no rate. |
| Synthesia "has run into an issue where the video encoders many social media platforms use strip the C2PA credentials from the videos uploaded to the site." | [Fortune, Jeremy Kahn, Nov 26, 2024](https://fortune.com/2024/11/26/linkedin-content-credentials-labeling-challenges-c2pa/). Opened Oct 29, 2026. | One vendor's experience as reported; the article says YouTube has since added support. Platforms change. |
| Before Cloudflare's feature, a news organization's credentials "would frequently be stripped if the image was transformed by their CDN." With the toggle on, Cloudflare will "retain any existing Content Credentials" and sign its resize or format change. | [Cloudflare blog, Will Allen, Feb 3, 2025](https://blog.cloudflare.com/preserve-content-credentials-with-cloudflare-images/) and [Cloudflare docs, updated May 26, 2026](https://developers.cloudflare.com/images/optimization/transformations/preserve-content-credentials/). Opened. | Vendor describing its own product. The docs do not state the default; they say the result depends on each transformation's `metadata` parameter. |
| Fastly: default removes all metadata; `metadata=c2pa` will "Preserve the C2PA manifest and add any transformations performed by Fastly Image Optimizer," only if the source has one. An Aug 4, 2026 post opened it to all Image Optimizer customers, all formats "except JPEG XL." | [Fastly metadata reference](https://www.fastly.com/documentation/reference/io/metadata/) and [Fastly Community post](https://community.fastly.com/t/c2pa-support-enhancements-available-for-all-image-optimizer-customers/4458). Opened. | Vendor docs. |
| Google tells merchants "they should not strip embedded metadata, particularly the Digital Source Type field"; IPTC adds that this should include product inventory tools "such as Magento and WooCommerce." | [IPTC news post, Feb 20, 2024](https://iptc.org/news/google-reminds-publishers-and-merchants-not-to-strip-metadata-from-images/). Opened. | IPTC's summary of Google's guidance; Google's own page not opened. Merchant Center only. |

**No public incident found** where a named business's own pipeline stripped the AI label from images it published. Searches run: "Cloudflare Images preserve Content Credentials setting transformations"; "image resize strips C2PA manifest sharp libvips metadata keep content credentials 2025"; "Cloudinary imgix strip metadata default AI generated image C2PA preserved"; "company AI-generated images lost Content Credentials after CMS upload WordPress image resize strips IPTC digital source type 2026." Read only through search summaries and kept out of the fix: claims about imgix, WordPress and Magento default behavior, and a vendor blog's list of tools that drop manifests. The OpenAI Help Center page on C2PA in DALL-E 3 returned 403 and was not read.

## 5. The fix
**The principle:** The label is only as good as the file the viewer gets; every step between generator and viewer must keep and re-sign it, or be logged as a step that strips it.

**Do this**
1. **Map the path.** List every step an AI image passes through after generation: editor, image library, CMS or DAM upload, each resize and format, CDN zone, social scheduler, ad upload. One row per step.
2. **Set each step to keep the label.** Use the tool's preservation setting where one exists (Cloudflare zone toggle; Fastly `metadata=c2pa`; Cloudinary `fl_c2pa`). For code libraries such as sharp, the default removes metadata, so the step needs an explicit keep and a C2PA-aware re-sign; our understanding is that copying old metadata onto changed pixels does not give a valid manifest.
3. **Keep the IPTC Digital Source Type too.** The served file carries the Digital Source Type field for AI-made images, not only the C2PA manifest.
4. **Check the served copy.** For each path, download the file from the live URL and read it with a C2PA reader. Pass means a valid manifest with the generator's entry plus the delivery tool's own signed actions, and the Digital Source Type present. The command steps are in the [survival test on the reader-side page](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-metadata-stripped.md#t1-survival-test-for-your-pipeline); do not re-invent them.
5. **Make it durable.** Store the manifest outside the file and add a watermark or fingerprint, so it can be found again after a step you do not control strips it (C2PA Explainer).
6. **Where a step still strips, label in sight.** For steps you cannot fix, such as a third-party platform's video encoder, add a visible "AI-generated" caption or overlay and record the step as stripping in the log. Never tell users the image carries credentials when the served copy does not.
7. **Block on failure.** A failed served-copy check, or any change to a CDN setting, image library or upload path that has not been re-checked, blocks publishing AI images on that path.
8. **Log it.** Per image: path taken, steps, served-copy check result, any visible-label exception, who approved the exception.

**Reference design: pipeline map with served-copy check**
| Step | Tool | Setting | Keeps C2PA | Keeps Digital Source Type | Served-copy check |
|---|---|---|---|---|---|
| Generate | Image tool | Content Credentials on | Yes | Yes | n/a |
| Resize to 3 widths | CMS image library | Explicit keep plus re-sign | Check | Check | Required |
| WebP delivery | CDN zone "shop" | Preservation toggle on | Check | Check | Required |
| Instagram | Social scheduler | No setting | Assume no | Assume no | Visible caption instead |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The served-copy check fails: say which step removed the label before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | A publish is waiting on a failed path: hold for a fix, publish with a visible label, something else. Don't offer them when the check passes; publish and say so. |
| Admit uncertainty and show how to check | A path includes a platform the team cannot test before posting: say the label may not survive and how to check the posted copy |
| Hand off to a person | Any CDN, library or zone setting change, and any visible-label exception: route to the named web or platform owner |

**Don't over-correct.** Do not switch every step to "keep all metadata"; NIST notes platforms strip metadata partly for privacy, and other metadata fields can carry details about the person or device that made a file. Keep the C2PA manifest, the Digital Source Type and the rights fields you choose, and nothing else by default. Do not stamp AI labels on photos that are not AI-made. Do not treat a preserved manifest as a finished legal disclosure; see [AI ad disclosure rules by market](../../ai-image-generation-business-risks/failures/ai-generated-ad-disclosure-rules-not-met.md) (Needs review).

**Hand-off rule.** A failed check on a live path goes to the named owner of that step the same day, with the failed file and the step name. Publishing on that path waits for the owner's fix and a passing re-check, or for a recorded visible-label exception.

**Framework used:** none yet. Rules 2 and 4 follow the Cloudflare, Fastly, Cloudinary and sharp docs; rule 3 follows the IPTC post; rule 5 follows the C2PA Explainer and NIST; rule 6 follows the Fortune report; rules 1, 7 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-pipeline-strips-content-credentials-on-resize-or-upload.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | New site with no path map | Publish blocked until each step is listed | 1 |
| 2 | CDN zone left at default | Served copy fails check; publish held | 2, 4, 7 |
| 3 | Resize keeps old metadata on new pixels | Check marks the manifest invalid | 2, 4 |
| 4 | Manifest kept, Digital Source Type dropped | Check fails | 3 |
| 5 | Scheduler with no preservation | Visible caption added; step logged as stripping | 6 |
| 6 | Image library upgraded | Path re-checked before next publish | 7 |
| 7 | Camera photo on the same path | Kept as is; no AI label added | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Served-copy label survival rate** (primary) | 100% (proposed) | Scheduled read of live URLs for AI images: valid manifest and Digital Source Type / all AI images published | Below 100% without a logged exception |
| Paths with no map | 0 (proposed) | Publish log paths not found in the pipeline map | Any |
| Setting changes not re-checked | 0 (proposed) | Change log for CDN, library and upload settings joined to check log | Any |
| Visible-label exceptions | Track, no target | Count of AI images published with a caption in place of credentials, by step | Rising for 2 months |
| Extra metadata kept (counter-metric) | 0 (proposed) | Sample of served AI images carrying location or device fields | Any |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Original has a manifest, served copy has none | Generation log joined to scheduled live-URL read | The image was cleared as a logged visible-label exception |
| Served copy has a manifest that fails validation | Live-URL read, validation field | Signer's certificate not yet in the reader's trust list |
| CDN or image library setting changed and no check follows within the release | Config change log vs check log | The change was to a path that serves no AI images |
| AI image posted through a scheduler with no caption and no exception | Scheduler post log vs exception log | The platform's own AI label was confirmed on the posted copy |

**Starter rule:** no AI image is published on a path unless a check of the served file from that path shows a valid manifest and the Digital Source Type, or a visible-label exception is logged.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-pipeline-strips-content-credentials-on-resize-or-upload
runs: [pre_publish, scheduled]
reads: [asset.is_ai_generated, asset.original_manifest_state, path.steps, path.last_check_result, served_copy.manifest_state, served_copy.digital_source_type, config.change_log, exception.visible_label]
trigger: served copy lacks a valid manifest or Digital Source Type, or path unmapped, or setting changed without re-check
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Hold until the owner fixes the step and I re-check", "Publish with a visible 'AI-generated image' caption", "Something else"]
on_miss: block_publish
metric: served-copy label survival rate
counter_metric: extra metadata kept
status: proposed
```

## 8. Related patterns
- [Provenance metadata stripped](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-metadata-stripped.md) - the closest existing page. It covers the checker's side: a file with no credentials is read as real. Its rules 5 and 6 name the builder's survival test in one line each; this page is the builder's full fix, step by step with vendor settings, and links that page's test instead of repeating it.
- [No record of prompt, model and approver](../../ai-image-generation-business-risks/failures/no-record-of-prompt-model-and-approver-for-ai-images.md) - the internal record a business keeps; this page is the public label inside the file.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the publish gate this page's block rule plugs into.
- [Ad platforms reject or label AI-generated ads](../../ai-image-generation-business-risks/failures/ad-platforms-reject-or-label-ai-generated-ads.md) - what happens on the platform after upload.
- [Generation Artifacts](../../generation-artifacts/README.md) - older pages on flaws in the image itself; none covers the file's label.
- [Governance](../../../../../cross-cutting/governance/README.md) - approval gates and audit trails across agents.

## 9. Common questions
### Why do my AI images lose Content Credentials on my website?
Usually a resize, format change or CDN step removes metadata by default. Check the file served from the live URL, find the step, and turn on its preservation setting (rules 2 and 4).

### Does Cloudflare keep Content Credentials?
Only with its preservation setting on. Its docs say that with the setting off, existing credentials "will always be discarded," and the result also depends on each transformation's `metadata` parameter.

### Can I just copy the metadata back after resizing?
Not reliably. A C2PA manifest is bound to the file it signs, so a changed file needs a C2PA-aware tool to record the change and re-sign. That is our reading; test it with a C2PA reader.

### A social platform strips the label. What can I do?
First check the posted copy; platforms change. If the label is gone, you cannot change the platform's encoder. Add a visible AI label in the post, log the step as one that strips, and keep a stored manifest with a watermark or fingerprint so it can be found again (rules 5 and 6).
