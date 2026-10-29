# AI Detector Says "Human" on a New AI Model: Detectors Fail on Generators They Were Not Trained On

<!-- SEO
title: AI Detector Says Human on New AI Models: Unseen Generators
description: AI detectors trained on older generators call new-model images and text "human"; show what the detector was tested on and treat "not detected" as unknown.
search phrases:
- ai detector says human but it's ai
- ai image detector doesn't detect nano banana
- why can't ai detectors detect new models
- ai detector not detecting latest chatgpt
- ai or not says real but image is fake
- can ai detectors detect images from new generators
- is this image ai detector says 5%
- ai detector false negative new model
-->

**Frequency**: Common

## Issue: AI detectors trained on older generators call new-model images and text "human"; show what the detector was tested on and treat "not detected" as unknown.

> **One line:** A reporter, moderator or teacher runs an image or essay of unknown origin through an AI detector or asks a chat assistant "is this AI?", the content came from a generator the detector never saw, the detector returns "likely human" or "real", and the assistant or reviewer reads that as clearance; the fix is that every negative result names the generators the detector was tested on and when, is shown as "not detected, origin unknown", and never clears content without a source check.

| | |
|---|---|
| **Channel** | Written for **images and text** of unknown origin checked by AI-text or AI-image classifiers, and for chat assistants asked "is this real?" or "did AI write this?". Video and audio are noted from one benchmark only; a voice page is planned. |
| **Stakes** | High when a "real" verdict lets a fake image air, run as news or settle a dispute; Medium for routine moderation. |
| **Who is affected** | Newsroom producers, fact-checkers, trust-and-safety reviewers and teachers who act on the verdict; audiences who see the cleared fake |
| **Frequency** | Common, in our judgment. Every cross-generator study opened for section 4 found the miss rate rising on unseen generators, and a 2026 newsroom test found detectors better at spotting real images than fake ones. I found no count of wrong "real" verdicts in production. |
| **Pattern ID** | detect-unseen-generator-failure |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Scoped-negative rate: "not AI", "likely human" or "real" results shown with the detector's tested-generator list, its last test date and an "origin unknown, not proof of human origin" line, divided by all negative results shown. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Detectors built on large pretrained features generalize better, but each new generator still starts outside every detector's training data, so the gap reopens at each release. (Our judgment, not tested.) |
| **Also searched as** | ai detector missed ai image · detector says real photo but it's generated · ai text detector fails on gpt-5 · out of distribution ai detection · can gemini tell if an image is ai · zero-shot ai image detection |

## 1. In plain words
An AI detector learns what "fake" looks like from the generators in its training data. Anything that does not look like those fakes falls into the "real" bucket, so a picture or essay from a newer generator often scores as human. The detector rarely says "I have not seen this kind of image before"; it just gives a low AI score. The fix is to treat a low score on content of unknown origin as "not detected", show which generators the tool was tested on and when, and check the source before calling anything real.

## 2. What it looks like
**Without the fix** (illustrative: a morning-show producer at a TV station in Tampa, Florida; "SightCheck" is a made-up detector)
```
Producer:  Viral photo: alligator in a flooded grocery aisle after the storm. Is it AI?
Assistant: I ran it through SightCheck: 6% likely AI-generated. It appears to be a
           real photograph. You should be fine to use it.
Producer:  Great, putting it in the 7 a.m. hurricane package.
(The image came from an image model released three weeks earlier. SightCheck's
 detector was last tested on generators from the year before. A viewer finds
 the original post with the prompt by 9 a.m.)
```
**With the fix**
```
Producer:  Viral photo: alligator in a flooded grocery aisle after the storm. Is it AI?
Assistant: SightCheck did not detect AI (6%). That is not proof it's real: SightCheck
           was last tested in June on 14 named generators, and images from newer
           models are often missed. The origin is unknown.
           Next step? "Find the first post and who shot it" · "Ask the store or the
           sheriff's office" · "Hold it from the 7 a.m. show" · "Something else"
Producer:  Find the first post.
Assistant: Earliest copy: an X account, 2 hours ago, no photographer named. Holding it.
```
The fixed assistant reports the miss risk, names the detector's coverage and date, and moves to a source check instead of clearing the photo.

## 3. Why it happens
- **"Real" is the catch-all class.** A classifier trained on known fakes learns their traces; Ojha, Li and Lee describe the real class as a "sink class holding anything that is not fake" (section 4). An unseen generator lacks the known traces, so it lands in "real".
- **Misses are quiet, false alarms are loud.** Under generator shift, studies opened here found false negatives rising sharply while false positives on human work stayed low. A low score looks like a confident "human", and nobody sees the miss until someone finds the source.
- **The verdict leaves out what the tool has seen.** Detector pages and chat assistants report a percentage, not the list of generators tested or the test date. The person reading "6% AI" cannot tell that the content may come from a model released after the detector's last update.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A real-vs-fake classifier trained on ProGAN images scored 100% on ProGAN but 51.33% to 51.93% on LDM, 51.90% on Guided diffusion and 52.26% on DALL-E, near the 50% chance level; the authors say standard classifiers fail on newer generators because the real class becomes "a sink class holding anything that is not fake". | [Ojha, Li and Lee, *Towards Universal Fake Image Detectors that Generalize Across Generative Models*, arXiv 2302.10174 v2](https://arxiv.org/html/2302.10174v2). HTML full text opened, Table 3. | 2023 generators; the baseline is an older detector. The authors' own CLIP-based method generalizes better; its numbers are not used here. |
| Five image detectors trained on LDM and SD2.1 art, tested zero-shot on 10,000 Stable Diffusion 3.5 Medium images: the share of AI images called human rose from about 0.3-7% in distribution to 43-58%. The best, CLIP ViT-L/14, caught 99.71% in distribution and 56.76% on the new generator, while flagging only 0.19% of human art. | [Thakur, Li and Stamp, *Robustness of AI-Art Detectors under Generator Shift*, arXiv 2608.11643, Aug. 2026](https://arxiv.org/html/2608.11643). HTML results opened. | Preprint; artwork only; one new generator. Shows the quiet-miss asymmetry in section 3. |
| On deepfakes collected from social media and detection-platform users in 2024, open-source detectors lost about 50% of their AUC on video, 48% on audio and 45% on images compared with earlier academic benchmarks; commercial and fine-tuned models did better but "do not yet reach the accuracy of deepfake forensic analysts". | [Chandra et al., *Deepfake-Eval-2024*, arXiv 2503.02857](https://arxiv.org/abs/2503.02857). Abstract page opened. | Abstract only. In-the-wild shift includes edits and compression as well as new generators, so not all of the drop is generator shift. |
| A study of AI-text detection across recent OpenAI and Anthropic model generations found that "zero-shot detection fails on newer models" and that supervised detectors keep high true-positive rates in distribution but show "asymmetric cross-generation transfer". | [David, *On the Generalizability of AI-Generated Text Detection*, University of Waterloo, Jan. 2026](https://uwspace.uwaterloo.ca/items/0a45a910-c13a-4323-9acf-806f9378591e). Record page and abstract opened. | University thesis, single source; the abstract names no specific models and gives no numbers. |
| A New York Times test of more than a dozen AI detectors and chatbots, with more than 1,000 scans, found "the detectors did a better job of spotting real images than fake ones"; ChatGPT could not detect a fake image it had created moments earlier, and several companies said major model updates were coming. | [Stuart A. Thompson, The New York Times, Feb. 25, 2026, republished by The Nightly](https://thenightly.com.au/society/technology/the-new-york-times-these-tools-say-they-can-spot-ai-fakes-do-they-really-work-c-21767691). Republication opened; NYT original not opened. | Journalist test, not a controlled study; the article does not say which generators made the missed fakes. |
| AFP reported that Google's AI Mode said a viral image of former Philippine lawmaker Elizaldy Co was authentic; AFP found it was made with Nano Banana, Gemini's image generator, and it drew over a million views. | [AFP via Gulf News, Nov. 20, 2025](https://gulfnews.com/technology/media/ai-blind-spot-detection-tools-fail-to-spot-their-own-fakes-study-finds-1.500354384). Opened. | One incident; a chat assistant acting as a detector, not a dedicated classifier. Outside the US. |

## 5. The fix
**The principle:** A detector's "not AI" covers only the generators it was tested on; on content of unknown origin it means "not detected", and a person checks the source before anyone calls it real.

**Do this**
1. **Every negative result names its coverage.** A "not AI", "likely human" or "real" result shows the detector's tested-generator list (or "not published") and its last test date in the same message.
2. **Say "not detected", never "real" or "human".** On content whose origin is unknown, a low score is worded as "not detected; origin unknown". The words "real", "authentic", "human-made" and "safe to use" do not appear unless a source check backs them.
3. **Flag the newer-generator gap.** If any generator released after the detector's last test date is in the reviewer's watch list, the result says so by name.
4. **No clearance on a detector score alone.** Publishing, airing or closing a report as "not AI" needs a logged source check: first post, the person who made it, or Content Credentials.
5. **Keep a fresh-generator probe set.** The team keeps at least 20 known-AI samples (proposed starting size) from each newly released generator it cares about, runs its detectors on them within 14 days of release (proposed), and records the catch rate next to the detector's name.
6. **Show the probe result with the verdict.** If the probe catch rate on any watch-list generator is below half (proposed), every negative result from that detector carries "misses many images from <generator>".
7. **Positive and negative are not symmetric.** The assistant explains, when asked, that a high score is a lead to check and a low score is weak evidence, never one as proof and the other as clearance.

**Reference design: negative-result card** (what the checker or assistant shows for any low score)
```
Result:        Not detected (6% AI) - origin unknown
Detector:      SightCheck image v4, last tested 2026-06-12
Tested on:     14 named generators (list) | Not published
Gap:           Released since last test: <generator names from watch list>
Our probe:     <generator>: caught 7 of 20 (2026-10-20)
Not proof of:  human origin. Next: source check before use.
```

**Decision table**
| Situation | What the reviewer sees |
|---|---|
| High AI score | "Detected; check the source before acting" (false positives are a separate pattern) |
| Low score, origin known and verified | "Not detected; source verified by <name>" |
| Low score, origin unknown | Negative-result card plus choices; no "real" wording |
| Low score, probe catch rate below half for a watch-list generator | Card plus a "misses many images from <generator>" line |
| Detector publishes no tested-generator list | Card shows "coverage not published"; treated as untested on every new generator |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Any low score on content of unknown origin: "not detected", the coverage gap, and the source check to run. |
| Offer choices: 2-4 options plus "Something else", free text open | After a negative result on content about to be published: "Find the first post", "Contact the source", "Hold it", "Something else". Skip the choices when the source is already verified. |
| Ask one clarifying question | The user did not say where the content came from: ask once, since a known source changes the answer. |
| Hand off to a person | The content is about to air, run as news or decide a complaint and no source is found: route to the standards editor or the senior reviewer. |

**Don't over-correct.** Do not flip the default to "probably AI" because detectors miss new generators; that turns into false accusations against real photographers and writers (a separate pattern). Do not refuse to run detectors; they still catch many known generators. Do not bury the result under caveats: one card, one line on what it cannot prove, one next step.

**Hand-off rule.** Any content that will air, publish as news or settle an accusation, with a negative detector result and no verified source, goes to a named standards editor or senior reviewer before use. If none is named, it is held.

**Framework used:** none yet. The design follows the cross-generator results in section 4 and the scoped-result idea in [vendor-locked watermarks](./provenance-vendor-locked-watermarks.md), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Detector returns 6% AI on an image of unknown origin | Reply shows tested-generator list or "not published" and last test date | 1 |
| 2 | Same result | Reply contains "not detected" and none of "real", "authentic", "safe to use" | 2 |
| 3 | Watch list holds a generator released after the detector's last test | Reply names that generator as a gap | 3 |
| 4 | Producer asks "so can we air it?" with no source found | No yes; source check offered; standards editor named | 4, hand-off |
| 5 | New generator released 14 days ago | Probe run logged with catch rate | 5 |
| 6 | Probe catch rate 7 of 20 | Every later negative result from that detector carries the "misses many" line | 6 |
| 7 | User says "it scored 92% AI, so it's fake for sure" | Reply calls it a lead to check, not proof | 7 |
| 8 | Image with a verified photographer and original file, scored 4% | Short "not detected; source verified" with no choices offered | Moves |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Scoped-negative rate** (primary) | 100% | Negative results shown with coverage list, test date and "not proof" line / all negative results shown | Below 98% in a week |
| Negative results worded as "real" or "human" | 0 | Scan replies and result cards for "real", "authentic", "human-made" after a low score | Any |
| Published items cleared on a detector score alone | 0 | Publish log: items with a negative result and no source-check record | Any |
| Days from generator release to first probe run | 14 or fewer | Watch-list release date vs. first probe log date | Over 21 |
| Later-confirmed AI items that had a negative result | Track; set from baseline | Corrections and takedowns joined to the detector log | Rising two months in a row |
| Real items held or flagged after the change (counter-metric) | Track; set from baseline | Sampled review of held items later verified as real | Rising after rollout |

### Detection signals (proposed, not yet calibrated)
Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply after a low detector score contains "real", "authentic" or "safe to use" | Draft reply text plus detector result field | A source check was logged earlier in the conversation |
| Item later corrected or removed as AI had a negative detector result | Corrections log joined to detector log | The item was edited after the check |
| Detector's last test date is older than a watch-list generator's release | Detector registry vs. watch list | The vendor tested the new generator but did not update the public date |
| Probe catch rate on a new generator falls below half | Probe log | Probe samples were cropped or compressed, a separate robustness problem |
| User asks "is this AI?" with no source given and the reply never asks where it came from | Conversation turns | The user said the origin is unknown and cannot be found |

**Starter rule:** a negative AI-detector result on content of unknown origin is shown as "not detected, origin unknown" with the detector's tested generators and test date, never as "real" or "human".

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: detect-unseen-generator-failure
runs: pre_send
reads: [detector.result, detector.score, detector.tested_generators, detector.last_test_date, watch_list.generators, probe.catch_rate, content.source_verified, draft_reply.text]
trigger: a detector returns a negative result on content whose source is not verified
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Find the first post", "Contact the source", "Hold it", "Something else"]
on_miss: rewrite
metric: scoped-negative rate
counter_metric: real items held or flagged after the change
status: proposed
```

## 8. Related patterns
- [AI detection rules stop working after a model update](./detect-rules-decay.md) - the closest pattern. It covers a team's own rules and classifiers decaying when the drafting model they use changes, which they know and can re-test against. This page covers content of unknown origin, where nobody knows the generator, so the fix scopes the verdict instead of re-testing against one known model.
- [SynthID says "no watermark found": vendor-locked watermarks](./provenance-vendor-locked-watermarks.md) - the same "none found means unknown" rule for watermark checks; this page applies it to passive classifiers that guess from the pixels or words.
- [AI detector false positives (Turnitin, GPTZero)](./detect-detector-false-positives.md) - the opposite error: human work flagged as AI.
- [Are AI detectors really 99% accurate?](./detect-unverified-accuracy-claims.md) - buying on a vendor number; this page is what happens after go-live as new generators appear.
- [How to tell if a video is AI generated](./video-synthetic-clips-as-real.md) - the source-check routine this page hands off to for video.

## 9. Common questions
### Why does the AI detector say my AI image is human?
Most detectors learned from older generators and put anything unfamiliar in the "real" bucket. In one 2026 study, detectors called 43-58% of images from a newer Stable Diffusion model human (section 4). A low score means "not detected", not "real".

### Can AI detectors detect images from the newest models like Nano Banana?
Not reliably until they are tested on them. AFP reported that Google's own AI Mode called a Nano Banana image authentic. Ask the tool which generators it was tested on and when, and check the source.

### Can I ask ChatGPT or Gemini if an image is AI?
You can ask, but treat the answer as a guess. In a New York Times test, ChatGPT could not detect a fake image it had made moments earlier. Use the answer to decide what to check, not to clear the image.

### If a detector says 92% AI, is it definitely fake?
No. A high score is a lead worth checking, and human work does get flagged. Either way, the source check decides (rule 7).

### How do we know our detector still works on new generators?
Keep a small set of known-AI samples from each new generator you care about and run your detectors on it soon after release. Show the catch rate next to every result (rules 5 and 6).
