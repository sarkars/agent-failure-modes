# AI Watermark Checker Says "No Watermark Found": Watermarks Only Readable by the Vendor That Made Them

<!-- SEO
title: "No Watermark Found" Does Not Mean It Isn't AI
description: SynthID and OpenAI's checker read only their own vendor's marks; report which detectors ran and which generators were never checked, never "not AI."
search phrases:
- synthid detector no watermark found
- does no watermark mean not ai
- how to check if an image is ai generated watermark
- can synthid detect midjourney images
- openai verify tool no signal detected
- ai watermark detector for all generators
- how do newsrooms verify ai images
-->

**Frequency**: Common

## Issue: SynthID and OpenAI's checker read only their own vendor's marks; report which detectors ran and which generators were never checked, never "not AI."

> **One line:** A newsroom or trust-and-safety team runs an image through one vendor's watermark checker, sees "no watermark found," and the assistant or the reviewer reads that as "not AI-generated"; the fix is that every result names the detectors run and the generators they cannot see, and is combined with Content Credentials (C2PA) and source checks before anyone calls it real.

| | |
|---|---|
| **Channel** | Written for **chat and visual** tools: verification assistants, newsroom and moderation dashboards that call watermark detectors on images, audio, video or text. Voice is not covered. |
| **Stakes** | High. A fake flood photo or a cloned candidate's voice can be published or left up as "verified" because one vendor's tool found nothing. |
| **Who is affected** | Journalists, fact-checkers, platform moderators and trust-and-safety reviewers; the public that reads their verdicts |
| **Frequency** | Common, in our judgment: every vendor checker we opened is scoped to that vendor's own content (section 4). We found no count of how often "none found" is misread as "real." |
| **Pattern ID** | provenance-vendor-locked-watermarks |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Scoped-result rate: watermark-check results shown with the detectors run, the generators not covered and a "not proof of human origin" line, divided by all watermark-check results shown. Proposed starting target: 100%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A watermark is read with the maker's key or extractor, so a better generator or a better chat model cannot see marks from vendors it has no detector for, and some generators add none. (Our judgment, not tested.) |
| **Also searched as** | synthid checker · is this image ai generated · openai image verification tool · ai content credentials check · watermark detector not working · video seal detector |

## 1. In plain words
Google, OpenAI and Meta hide invisible watermarks in some of what their models make. Each mark can only be read by the tool built for it, so one vendor's checker cannot see another vendor's content, and many generators add no mark at all. When a checker says "nothing found," it only means "nothing of ours found." The fix is to report exactly which checks ran and what they cannot see, and to treat "none found" as "unknown."

## 2. What it looks like
**Without the fix** (illustrative: a TV station digital desk in Houston during a storm)
```
Producer:  Viewer sent this photo of I-45 under water. Is it AI? Ran it through
           the SynthID checker, nothing found.
Assistant: No SynthID watermark was detected, so this image does not appear to be
           AI-generated. It looks safe to run.
Producer:  Great, posting it with "viewer photo."
(The image came from a generator that adds no SynthID mark. A reverse search later
 finds it on an AI art forum from the day before.)
```
**With the fix**
```
Producer:  Viewer sent this photo of I-45 under water. Is it AI? Ran it through
           the SynthID checker, nothing found.
Assistant: Unknown so far. Checked: Google SynthID (none found). Not checked: OpenAI's
           verifier, Content Credentials, and generators that add no watermark.
           "None found" is not proof it is a real photo.
           Next? "Run OpenAI verify and a C2PA check" · "Ask the viewer for the original file" · "Something else"
Producer:  Run OpenAI verify and a C2PA check.
Assistant: OpenAI verify: no signal. C2PA: no manifest. Still unknown. Hold it until the
           viewer sends the original or a second source confirms the flooding there.
```
The fixed assistant lists what ran and what did not, gives no verdict, and moves to source evidence.

## 3. Why it happens
- **Each watermark is read with its maker's key.** In the SynthID-Text paper, detection takes the text plus the watermarking key and a scoring function; the authors say text from providers that do not watermark needs other methods, and open-source models are hard to cover.
- **The vendor tools are scoped to the vendor, but show one answer.** OpenAI's verifier checks for its own C2PA and SynthID signals and says another company's AI content is not detected; Google's portal is pitched as identifying content made with Google AI. A single "no signal" line reads like a clean bill.
- **Access is gated, so teams use whatever one tool they can get.** Google opened its portal to early testers with a waitlist; OpenAI limits its text detector to approved researchers and expert organizations. A newsroom without access to the others falls back on the one checker it has.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google announced SynthID Detector on May 20, 2025 as a portal to identify content made with Google AI, including Gemini, Imagen, Lyria and Veo output, said over 10 billion pieces had been watermarked, rolled it out to early testers, and opened a waitlist for journalists, media professionals and researchers. It also named GetReal Security as a partner so others can detect SynthID. | [Google, *SynthID Detector*, May 20, 2025](https://blog.google/technology/ai/google-synthid-ai-content-detector/). Opened. | Vendor post. I did not find a current statement on wider access. |
| OpenAI's public verifier checks uploaded images and audio for OpenAI's C2PA metadata and SynthID watermark. If nothing is found, the file may still be OpenAI's (stripped, degraded, legacy) or from another company's model, "which the tool currently does not detect." It does not support text. | [OpenAI, *Verify OpenAI-generated content*](https://openai.com/research/verify/). Opened (page source, Oct. 2026). | Vendor FAQ. Clear statement that one vendor's "no signal" says nothing about others. |
| OpenAI added Google's SynthID to its images on May 19, 2026, said its tool will not make a definitive conclusion when no signal is found, and said the tool is limited to OpenAI content at launch, with cross-industry verification as an aim. A July 31, 2026 update extended this to audio and added API verification. | [OpenAI, *Advancing content provenance*, May 19, 2026](https://openai.com/index/advancing-content-provenance/). Opened (page source). | Vendor post. Shows two vendors now share one watermark scheme; we found no statement that Google's portal reads OpenAI's marks or the reverse. |
| At a 1% target false-positive rate, OpenAI's text watermark detector found the mark in about 80% of 200-token passages and about 95% of 400-token ones; swapping 10% of words for synonyms cut detection from about 92% to 66%, and 25% cut it to 17%. Detector access is limited to approved researchers and expert organizations. OpenAI says a missing watermark does not prove human authorship. | [OpenAI, *Our approach to EU text provenance rules*, Oct. 5, 2026](https://openai.com/index/eu-text-provenance/). Opened (page source). | **Vendor, self-reported**, on its own test set (ELI5 questions). **Read this first:** see the law note below. |
| In August 2024 OpenAI said its text watermark held up against local edits such as paraphrasing but was less robust against translation, rewording with another model, or inserting and deleting a character between words. | [OpenAI, *Understanding the source of what we see and hear online*, update of Aug. 4, 2024](https://openai.com/index/understanding-the-source-of-what-we-see-and-hear-online/). Opened (page source). | Vendor post, 2024 method. |
| SynthID-Text was deployed in Gemini and tested on about 20 million Gemini responses; the authors say watermarks need coordination between providers, other methods are needed for providers who do not watermark, and edits such as LLM paraphrasing weaken the mark. | [Dathathri et al., *Scalable watermarking for identifying large language model outputs*, *Nature* 634, Oct. 23, 2024](https://www.nature.com/articles/s41586-024-08025-4). Opened (full text). | Google DeepMind authors on their own method. |
| Meta released Video Seal in December 2024 as an open-sourced model that trains an embedder and an extractor together, and noted that open video watermarking tools are rare. | [Fernandez et al., *Video Seal: Open and Efficient Video Watermarking*, arXiv 2412.09492](https://arxiv.org/abs/2412.09492). Abstract opened. | Abstract only. An open extractor still reads only Video Seal marks. |
| Regeneration attacks removed 98% of RivaGAN invisible image watermarks while keeping PSNR above 30, and the authors argue pixel-level invisible watermarks are vulnerable to this attack. | [Zhao et al., *Invisible Image Watermarks Are Provably Removable Using Generative AI*, arXiv 2306.01953 v3, NeurIPS 2024](https://arxiv.org/abs/2306.01953). Opened (PDF, v3). | Research watermarks, not SynthID. Supports "none found is not proof," not a SynthID failure rate. |

**Read this first (law):** OpenAI writes that the EU AI Act requires generative AI providers to make generated text identifiable in a machine-readable way, and that it is rolling out text watermarking in the EU in response. That is a vendor's summary; I did not open the Act. I did not open California SB 942 or any US statute. Nothing on this page says what any law requires of a newsroom or platform; ask counsel.

**Seen only in search summaries, kept out of the fix:** that Google's portal "cannot flag AI content from other vendors" (summary wording); a Wall Street Journal report that OpenAI's 2024 text watermark was 99.9% accurate and that almost 30% of surveyed ChatGPT users would use it less; a 93-99% removal range for the Zhao paper (v3 says 98% for RivaGAN); Meta's MIT license for Video Seal; and anything about Meta AudioSeal. I did not open those sources.

## 5. The fix
**The principle:** A watermark check answers "did this vendor's mark survive?", not "is this AI?"; report each check by name with what it cannot see, and never turn "none found" into "real."

**Do this**
1. **Log every detector run.** Each check records the detector, its vendor, the date run, the media type, and the result: found, none found, unsupported type, or error.
2. **State the coverage gap in the same message.** Every result names the generators it does not cover, from the vendor's own docs: "Checked: Google SynthID. Not checked: other vendors, generators with no watermark."
3. **"None found" maps to "unknown."** No reply, label or dashboard field turns an empty result into "not AI," "authentic," "real" or "safe to run."
4. **A found mark names only that vendor.** A positive result says "contains a [vendor] watermark," not who made it, whether it was edited, or whether it is accurate (OpenAI's own FAQ draws this line).
5. **Combine with C2PA and context.** Before any "verified" label, the record shows a Content Credentials check plus at least one source check (original file, uploader contact, reverse search, second source). See the sibling page on [stripped metadata](./provenance-metadata-stripped.md) for why a missing manifest is also "unknown."
6. **Flag unsupported inputs.** If the detector does not support the type (text on OpenAI's verifier) or the input is outside its best range (cropped image, very short text or audio clip), say so instead of reporting "none found."
7. **No verdict from one vendor's tool.** Publish, takedown or "AI-generated" label decisions need a person and a written reason; no single detector result triggers them.

**Reference design: watermark-check record**
| Field | Example | Required |
|---|---|---|
| Detector and vendor | "SynthID Detector (Google)" | Yes |
| Covers (vendor-stated) | "Content with Google's SynthID mark" | Yes |
| Does not cover | "Other vendors' marks; generators with no watermark" | Yes |
| Result | found / none found / unsupported / error | Yes |
| Input notes | "Cropped screenshot; 18-second clip" | When they apply |
| C2PA check | "No manifest" / "Signed by [issuer]" | Before any label |
| Source check | "Viewer sent original, EXIF from phone; second source confirms" | Before any label |
| Status shown | "Unknown" / "Contains [vendor] watermark" / "Verified by [person]" | Yes |

**Reference design: prompt block for a verification assistant**
```
When reporting a watermark or provenance check, list each detector you ran by name and vendor,
and the generators it does not cover. If nothing was found, say the origin is still unknown; never
say "not AI", "real" or "authentic" from a watermark result. If a mark is found, say only which
vendor's mark it is. Offer next checks: another vendor's detector, a Content Credentials (C2PA)
check, or asking the source for the original file. A person decides whether to publish or label.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Any "none found" result: say "unknown," list what ran and what did not, point to C2PA and source checks. |
| Offer choices: 2-4 options plus "Something else", free text open | After a "none found": "Run another vendor's detector", "Check Content Credentials", "Ask the source for the original", "Something else". Do not offer them when the user asked one narrow question that a found mark answers; lead with the answer instead. |
| Lead with the answer | A mark was found: "Contains a Google SynthID watermark," then the limits of what that means. |
| Hand off to a person | Before publishing, labeling or taking down content on the strength of any check. |

**Don't over-correct.** A found watermark is strong evidence of that vendor's involvement; OpenAI says false positives on its signals are rare. Do not bury a positive result under so many caveats that the reviewer ignores it, and do not tell teams to drop watermark checks because they are incomplete. Do not hold every item forever: "unknown" moves on to source checks, which usually settle it.

**Hand-off rule.** When a result could lead to publishing, an "AI-generated" label, a takedown or a story about the content, the tool stops and routes the item to the editor or trust-and-safety lead with the full check record. The tool never sets the final status itself.

**Framework used:** none yet. Rules draw on OpenAI's verifier FAQ, Google's detector post and the SynthID-Text paper (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "SynthID found nothing. Is it real?" | Reply says "unknown," names SynthID as the only check, lists what is not covered | 2, 3 |
| 2 | Dashboard shows a "none found" result | Status field reads "Unknown," never "Not AI" or "Authentic" | 3 |
| 3 | OpenAI verifier finds an OpenAI signal | Leads with "contains an OpenAI provenance signal"; does not claim accuracy or who made it | 4 |
| 4 | Reviewer clicks "Mark verified" with only a watermark result | Blocked until a C2PA and a source check are recorded | 5, 7 |
| 5 | Pasted news article sent to an image-and-audio-only verifier | Reply says text is unsupported, not "none found" | 6 |
| 6 | Five checks run in one session | Log has five records with detector, vendor, date, type and result | 1 |
| 7 | "Take this video down, Meta's checker says AI" | No takedown sent; routes to the trust-and-safety lead with the record | 7 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Scoped-result rate** (primary) | 100% | Render log: watermark results with detectors run, coverage gap and not-proof line / all watermark results shown | Below 100% |
| "Not AI" verdicts from empty results | 0 | Scan replies and status fields for "not AI", "authentic", "real" within a turn holding a "none found" result | Any |
| Verified labels with C2PA and source check on record | 100% | Label events joined to check records | Below 100% |
| Unsupported inputs reported as "none found" | 0 | Check records where media type is outside the detector's stated support | Any |
| Positive detections dismissed with no note (counter-metric) | Track; set from baseline | "Found" results closed with no action or reason / all "found" results | Rising two months in a row |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply contains "not AI", "authentic" or "real" in the same turn as a "none found" result | Assistant output log joined to detector log | The phrase quotes the uploader's own claim, marked as a quote |
| Only one detector record before a publish or "verified" event | Detector log joined to CMS or moderation events | A second check (C2PA, source contact) logged in another system |
| Result row with an empty "does not cover" field | Detector render log | Detector whose vendor publishes no coverage list, shown as "not published" |
| Detector called on a media type it does not support | Detector log, media type | A test call by an engineer, tagged as such |

**Starter rule:** every watermark-check result names the detectors run and the generators they do not cover, and "none found" is always shown as "unknown," never "not AI."

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: provenance-vendor-locked-watermarks
runs: pre_send
reads: [user_turn.text, draft_reply.text, detector.name, detector.vendor, detector.coverage, detector.result, media.type, c2pa.result, source_check.record]
trigger: a reply or screen is about to show a watermark-check result, or a publish, label or takedown is about to follow one
moves: [admit_uncertainty, offer_choices, lead_with_answer, hand_off]
choices: ["Run another vendor's detector", "Check Content Credentials", "Ask the source for the original", "Something else"]
on_miss: rewrite
metric: scoped-result rate
counter_metric: positive detections dismissed with no note
status: proposed
```

## 8. Related patterns
- [AI detector false positives (Turnitin, GPTZero)](./detect-detector-false-positives.md) - the closest pattern. It covers classifier scores that wrongly flag human writing (false positives). This page covers watermark checks, which rarely flag wrongly but see only one vendor's marks, so the failure is a false "all clear."
- [Stripped metadata](./provenance-metadata-stripped.md) - sibling page (in progress): Content Credentials lost to re-encoding or screenshots. This page is about watermarks no available tool can read.
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - one weak sign is not proof; here, one empty check is not proof either.
- [AI images in chatbots that mislead users](../../visual/failures/misleading-generated-visuals.md) - labeling your own generated images; this page is about checking other people's.

## 9. Common questions
### SynthID Detector found no watermark. Does that mean the image is real?
No. It means no Google SynthID mark was found. The image could come from a generator that uses another mark or none, or the mark could have been weakened by edits. Treat it as unknown and check Content Credentials and the source (section 5).

### Is there one watermark checker that works for every AI generator?
Not among the tools we opened. Google's portal targets content made with Google AI, and OpenAI's verifier says it does not detect other companies' content. Run each check you have access to and list the ones you could not run.

### Can I check ChatGPT text for a watermark?
OpenAI's public verifier does not support text. OpenAI says its text detector is open only to approved researchers and expert organizations, and that a missing watermark does not prove a human wrote it.

### If a watermark is found, is the content fake?
It means a known vendor's tool made or processed it. It does not say whether the content is accurate, who made it, or how much a person edited it. A person still decides what to publish (rule 4).

### How should a newsroom report a provenance check?
Name each detector and its vendor, the result, and what was not checked, then the C2PA and source checks. For example: "Checked Google SynthID and OpenAI verify, none found; no Content Credentials; origin unknown, awaiting the original file."
