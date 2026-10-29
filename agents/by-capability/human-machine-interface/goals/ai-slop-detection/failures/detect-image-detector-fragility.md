# AI Image Detector Says "Real" After a Screenshot: Detectors Break After Crop, Resize, Recompress or Blur

<!-- SEO
title: AI Image Detector Fooled by Screenshot, Crop or Compression
description: AI image detectors lose accuracy after crops, resizes, re-saves and blur; report the input's condition and call a low score on a degraded copy inconclusive.
search phrases:
- ai image detector fooled by screenshot
- does compressing an image fool ai detectors
- ai detector says real but image is ai
- cropping ai image to avoid detection
- why do ai image detectors give different results
- is an ai image detector accurate on social media images
- meta ai detector cropped images
- jpeg compression ai generated image detection
-->

**Frequency**: Common

## Issue: AI image detectors lose accuracy after crops, resizes, re-saves and blur; report the input's condition and call a low score on a degraded copy inconclusive.

> **One line:** A producer, moderator or teacher runs a screenshot of a viral image through an AI-image detector, gets "likely real", and treats it as cleared, when the screenshot, resize and re-compression removed the traces the detector reads; the fix is that every result states the condition of the file it judged, a low score on a degraded copy is reported as "inconclusive", and the tool asks for the best available copy before it answers.

| | |
|---|---|
| **Channel** | Written for **visual** tools: AI-image detectors, chat assistants asked "is this image AI?", and moderation or newsroom pipelines that score uploaded images. Video and audio are not covered. |
| **Stakes** | High. A fake cleared as "real" can be aired, used as evidence or shared during breaking news; a real photo scored as AI can get a person accused. |
| **Who is affected** | Reporters, fact-checkers, moderators, teachers, insurance and fraud reviewers, and the public using free detector sites; builders who ship a detector |
| **Frequency** | Common, in our judgment: most images people check have been resized, re-saved or screenshotted on the way, and research benchmarks report large drops on such copies (section 4). I found no count of real decisions made on degraded copies. |
| **Pattern ID** | detect-image-detector-fragility |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Condition-labeled result rate: detector results shown with the input's condition (size, re-compression, crop or screenshot signs) and, for degraded inputs, an "inconclusive" label instead of a "likely real" verdict, divided by all results shown. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Detectors trained with blur and compression augmentation hold up better in published tests, but a heavy crop or resize removes the signal itself, so the result still has to say what it judged. (Our judgment, not tested.) |
| **Also searched as** | screenshot ai image detection · ai detector compressed image · resize image to bypass ai detector · ai or not wrong result · hive says not ai but it is · content seal cropped |

## 1. In plain words
Most AI-image detectors look for tiny traces a generator leaves in the pixels. Saving a copy as JPEG, shrinking it, cropping it, blurring it or taking a screenshot can wipe those traces out. The detector still returns a confident number, and people read a low score on a wrecked copy as "this is real." The fix: every result says what condition the file was in, a low score on a degraded copy means "we can't tell," and the tool asks for the original.

## 2. What it looks like
**Without the fix** (illustrative: a digital producer at a local TV station in Houston during a flood)
```
Producer:  Is this AI? (uploads a 640x640 screenshot of a viral post: a shark on a flooded freeway)
Assistant: I ran an AI-image detector. Result: 9% likely AI.
           This image appears to be authentic. You can use it.
Producer:  Great, putting it in the 6 p.m. package.
(The screenshot was cropped and re-compressed twice. The score says nothing about the original.)
```
**With the fix**
```
Producer:  Is this AI? (uploads a 640x640 screenshot of a viral post: a shark on a flooded freeway)
Assistant: Inconclusive. This copy is a cropped screenshot, 640x640, re-compressed as JPEG.
           Detectors lose much of their accuracy on copies like this, so a low score is not a pass.
           What can you get?  1) The original file from the poster  2) The earliest upload link
           3) Run a source check without the file  4) Something else
Producer:  2, here's the first post on X.
Assistant: That copy is 2048x1536 with no crop. Detector: 87% likely AI. Treat it as unverified
           until the source checks out; this is not proof either way.
```
The fixed assistant names the file's condition, refuses to call a degraded low score "authentic", and asks for a better copy.

## 3. Why it happens
- **The traces are fragile by design.** Many detectors read high-frequency pixel patterns a generator leaves. JPEG, resizing and blur remove exactly those details. In one test that simulated social-media sharing, most published detectors fell toward coin-flip accuracy (Cozzolino et al., section 4).
- **Detectors are trained and scored on clean files.** Training sets often differ from real uploads in JPEG and image size, and detectors learn those differences as shortcuts (Grommelt et al., section 4). Benchmark headline numbers come from clean images, so buyers never see the drop.
- **The output hides the input.** The detector returns one number and no word on resolution, crop or re-saves, and assistants turn a low number into "authentic." Watermark checks have the same gap: a cropped image can lose the mark entirely (Reuters, section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| With images resized to 200x200 and JPEG-compressed at a random quality of 65 to 100 to mimic social sharing, the authors say the impairments make "most SoTA methods become essentially useless." Average AUC on post-processed images: Wang et al. 61.5%, Corvi et al. 70.8%, Ojha et al. 71.8%; their CLIP-based detector with augmentation 85.2%. Ojha et al. becomes "useless in the presence of a 25% rescaling." | [Cozzolino, Poggi, Corvi, Niessner and Verdoliva, *Raising the Bar of AI-generated Image Detection with CLIP*, arXiv 2312.00195v2, Apr. 2024](https://arxiv.org/html/2312.00195). Full text opened. | Authors compare against their own method; research detectors, not commercial tools. AUC of 50% is chance. |
| Reuters ran 40 images from Meta's Muse Image model through Meta's preview detector. It verified all 40 originals but failed on 55% after they were cropped to about one-third to one-half of their size. Meta said the watermark "is designed to remain intact after common edits" but may be lost after heavy cropping. | [Reuters via KSL.com, July 10, 2026](https://www.ksl.com/article/51596373/meta-ai-image-detector-fails-to-identify-some-of-its-own-cropped-ai-images). Opened. | Small sample; a preview tool; a watermark detector, not a pixel classifier. Only cropping was tested. |
| Many AI-image detection datasets "contain biases related to JPEG compression and image size," and detectors learn from them; removing the biases "substantially increases robustness to JPEG compression" and raised cross-generator performance by more than 11 percentage points for ResNet50 and Swin-T. | [Grommelt, Weiss, Pfreundt and Keuper, *Fake or JPEG?*, arXiv 2403.17608, Mar. 2024](https://arxiv.org/abs/2403.17608). Abstract opened. | Abstract only; one dataset (GenImage). |
| A NeurIPS 2025 benchmark of 11 detectors, with real-world samples from social media and AI art platforms, reports detectors "suffer significant performance drops on real-world data," and that common augmentations give "limited benefits." | [Li et al., *Is Artificial Intelligence Generated Image Detection a Solved Problem?*, arXiv 2505.12335](https://arxiv.org/abs/2505.12335). Abstract opened. | Abstract gives no drop sizes; "real-world" mixes several effects, not only post-processing. |
| A 600,000-image dataset including images shared through three social networks was built because sharing's "compression and other processing can degrade fake detection cues" and "many forensic tools fail to account for these in-the-wild challenges." | [Dell'Anna et al., *TrueFake*, arXiv 2504.20658, Apr. 2025](https://arxiv.org/abs/2504.20658). Abstract opened. | Abstract states the problem; no drop figures in the abstract. |
| An early detector paper credited its generalization to "careful pre- and post-processing and data augmentation," training with blur and JPEG. | [Wang et al., CVPR 2020, arXiv 1912.11035](https://arxiv.org/abs/1912.11035). Abstract opened. | Older GAN-era detector. |

**Seen only in search summaries, kept out of the fix:** Wang et al.'s supplement reporting 83.6% accuracy on in-the-wild StyleGAN faces dropping to 74.9% with resizing (the PDF returned 403); recent preprints (TextRich, DailyBench, CuRe) reporting near-zero recall for one detector under JPEG and drops from quality 90 to 50; a vendor's claim of 98% accuracy on cropped Meta images; a blog test calling most commercial detectors "no better than a coin toss."

## 5. The fix
**The principle:** A detector result is only as good as the copy it judged, so every result names the copy's condition, a low score on a degraded copy is "inconclusive", and the tool tries to get a better copy first.

**Do this**
1. **Measure the input first.** Before scoring, record pixel size, format, estimated JPEG quality, and crop or screenshot signs (app interface, status bar, odd aspect ratio, black bars).
2. **Show the condition with the result.** Every result lists that condition in one line next to the score.
3. **Degraded and low means inconclusive.** If the input fails the condition check (rule 1 thresholds, tuned per detector in rule 5), a low AI score is shown as "inconclusive", never as "real", "authentic" or "human-made."
4. **Ask for the best copy.** On a degraded input, offer to get the original file or earliest upload and re-run on it, and say which copy each score came from.
5. **Know your detector's breaking points.** Builders test the detector on their own originals plus copies that are resized, cropped, screenshotted, blurred and re-saved as JPEG at several qualities (include the 200x200, quality 65-100 condition from section 4), each release, and set rule 3's thresholds from where accuracy falls.
6. **Don't clean up the image silently.** No upscaling, sharpening or denoising before detection unless the result says it was done; pre-processing changes scores (Li et al., section 4).
7. **Missing watermark after a crop is unknown.** A watermark check on a cropped or resized copy that finds nothing is reported as "no mark found on this copy", with the crop named as a likely cause.
8. **The score never decides alone.** Any use that carries stakes (airing, a fraud claim, an accusation) needs a logged source check as well.

**Reference design: condition check** (runs before a score is shown; thresholds are placeholders to set from rule 5)
| Check | How | Example threshold to tune |
|---|---|---|
| Size | Shorter side in pixels | Below the size where your rule 5 tests drop |
| Re-compression | Estimated JPEG quality, double-compression sign | Below the quality where your tests drop |
| Screenshot or crop | Interface elements, status bar, aspect ratio vs. common camera ratios | Any sign present |
| Blur | Sharpness measure vs. your originals | Below your tested floor |
| Result wording | Fail any check + AI score below the flag line | Show "inconclusive", never "real" |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Every degraded-copy result: say the score can't clear the image and name the source check. |
| Offer choices: 2-4 options plus "Something else", free text open | After an inconclusive result: "The original file", "The earliest upload link", "Run a source check without the file", "Something else". Skip when the input is already a full-size original. |
| Ask one clarifying question | It is unclear whether the upload is the original or a copy of a copy. |
| Hand off to a person | The image is about to be aired, used in a claim or used to accuse someone. |

**Don't over-correct.** Do not refuse every JPEG; nearly all photos are JPEG, and good-quality copies can be scored with their condition shown. Do not read a high AI score on a degraded copy as proof either; detectors learn JPEG and size as shortcuts (Grommelt et al.), so degradation can mislead in both directions. Do not tell users how to crop or compress an image to beat a detector.

**Hand-off rule.** When the result will be aired, published, used in a claim or used against a person, the assistant stops at "inconclusive" or "flagged", lists the copies checked, and routes it to the newsroom's verification desk, the claims investigator or the decider named by the user.

**Framework used:** none yet. Rules follow the post-processing tests in Cozzolino et al. and the Reuters crop test (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Phone screenshot of an AI image, scored 8% AI | "Inconclusive", condition named, no "real" or "authentic" | 2, 3 |
| 2 | Full-size original from a camera | Score shown with condition "original, no crop" | 2 |
| 3 | Degraded upload | Choices offered for a better copy; each score labeled with its copy | 4 |
| 4 | Release test set: originals plus resize, crop, blur, JPEG copies | Per-condition accuracy recorded; thresholds updated | 5 |
| 5 | Pipeline upscales before scoring | Result says "upscaled before scoring" | 6 |
| 6 | Watermark check on a cropped copy finds nothing | "No mark found on this copy", crop named | 7 |
| 7 | "Can we air this?" with only a screenshot | No clearance; source check named; hand-off | 8, Hand-off |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Condition-labeled result rate** (primary) | 100% | Log each result render with its condition fields and wording | Below 98% in a week |
| Degraded-copy "real" verdicts | 0 | Scan results where the condition check failed for "real", "authentic", "human-made" | Any |
| Better-copy requests on degraded inputs | 95% | Degraded inputs followed by an offer to get the original | Below 90% |
| Release robustness test run | Every release | Rule 5 test report attached to the release | Missing |
| Inconclusive rate on good-quality originals (counter-metric) | Track; set from baseline | Share of inputs passing the condition check still shown as inconclusive | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Low AI score on an input with a short side under the tested floor | Detector result plus image metadata | A small original, such as an icon or thumbnail, judged correctly |
| Reply says "authentic" or "real" after a degraded-input result | Draft reply text plus condition fields | A source check, not the score, established it and is cited |
| Same image re-checked at a different size gives a very different score | Perceptual-hash match across checks | Different crops showing different content |
| Upload has screenshot interface elements | Image analysis of borders and status bars | User shared a screenshot of an app on purpose, for another question |

**Starter rule:** every AI-image detector result names the condition of the copy it judged, and a low score on a cropped, resized, screenshotted or re-compressed copy is shown as "inconclusive", never as "real".

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: detect-image-detector-fragility
runs: pre_send
reads: [image.width, image.height, image.format, image.jpeg_quality_est, image.screenshot_signs, image.blur_score, detector.score, detector.tested_floors, draft_reply.text]
trigger: a detector or watermark result about an uploaded image is about to be shown
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["The original file", "The earliest upload link", "Run a source check without the file", "Something else"]
on_miss: rewrite
metric: condition-labeled result rate
counter_metric: inconclusive rate on good-quality originals
status: proposed
```

## 8. Related patterns
- [No Content Credentials doesn't mean it's real](./provenance-metadata-stripped.md) - the closest page. It covers re-saves and uploads stripping the provenance label stored in the file. This page covers the same edits wrecking the pixel traces and watermarks that detectors read, so the score itself goes wrong.
- [SynthID says "no watermark found": vendor-locked watermarks](./provenance-vendor-locked-watermarks.md) - which vendor's marks a checker can read; this page adds that even the right checker can miss its own mark after a crop.
- [AI detector false positives (Turnitin, GPTZero)](./detect-detector-false-positives.md) - text detectors flagging human writing; the same "a score is not proof" rule, here applied to image copies.
- [Are AI detectors really 99% accurate?](./detect-unverified-accuracy-claims.md) - vendor accuracy is usually measured on clean files; rule 5 is the degraded-copy part of testing on your own sample.
- [How to tell if a video is AI generated](./video-synthetic-clips-as-real.md) - the source check that decides when a score can't.
- [Compression sensitivity in vision models](../../../../vision-and-images/goals/adversarial-robustness/failures/compression-sensitivity.md) - the general model-side problem of JPEG hurting image models; this page is about what a detector tells people.

## 9. Common questions
### Can a screenshot fool an AI image detector?
Often, yes. A screenshot resizes and re-compresses the image and can crop it, and published tests show many detectors drop toward chance on copies like that (section 4). A low score on a screenshot means "can't tell," not "real."

### Does compressing or resizing an image change the AI detector result?
It can, a lot. In one study, images resized to 200x200 and JPEG-compressed made most tested detectors close to useless, while a detector trained with those edits held up better. Ask for the original file before trusting any score.

### Why do two AI detectors give different answers on the same image?
They were trained on different data and break under different edits; one may ignore JPEG while another fails after a small resize (Cozzolino et al.). Also check whether both saw the same copy.

### Does cropping remove an AI watermark?
It can. Reuters found Meta's preview detector missed 55% of its own images after a heavy crop. "No mark found" on a cropped copy means unknown.

### How do I check if a viral image is AI if I only have a screenshot?
Find the earliest upload and the original poster, look for the full-size file, and check the source and context. Use a detector on the best copy you can get and record which copy it judged (rules 4 and 8).
