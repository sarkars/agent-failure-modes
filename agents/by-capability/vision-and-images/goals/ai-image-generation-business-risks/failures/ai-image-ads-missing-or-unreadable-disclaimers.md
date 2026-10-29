# AI Image Ads With Missing or Garbled Disclaimers: When the Generator Draws the Fine Print

<!-- SEO
title: AI Image Ads With Missing or Garbled Disclaimers and Fine Print
description: AI-made ads drop required fine print or draw it as garbled text. Overlay approved disclaimers as real text after generation and check them at every size.
search phrases:
- ai image generator fine print garbled
- can ai add disclaimer text to ad image
- ai generated ad disclaimer misspelled
- how big does a disclaimer have to be in an ad
- ftc clear and conspicuous disclosure size
- small print not legible ad ruling
- add legal text to ai generated image
- ai video ad disclaimer on screen time
-->

**Frequency**: Unknown

## Issue: An AI-made ad image or video drops the fine print the ad needs, or draws it as misspelled, tiny or unreadable text, because the generator was asked to include it. Never let the generator draw required text: overlay the approved disclaimer as real text after generation and check its wording, size and on-screen time at every placement.

> **Read this first:** This page is design guidance for an ad production workflow. It is not legal advice. The rules cited are general advertising disclosure rules (FTC staff guidance in the US, the ASA and Clearcast in the UK). None of them is specific to AI images. Statements about them are what the cited source says, read on October 29, 2026. Which disclosures an ad needs, and what size and timing make them clear, is for a qualified lawyer or compliance reviewer to decide.

> **One line:** A marketer types the loan rate and its fine print into an AI image prompt, the generator draws "Anual Percntage Rae" at six pixels in the corner, and the banner runs at 320x50 where nobody can read it; the fix is to keep required text out of the generator, overlay it from a compliance-approved disclosure sheet as real text after generation, and check wording, size, contrast, placement and duration on every final size before launch.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Still ads (banners, social posts, print, out-of-home) and video ads (social, streaming, connected TV). For video, on-screen time is part of the check. |
| **Channel** | AI design and ad tools that make the art and, if asked, the text in it: text-to-image, image editing, text-to-video, and ad platforms' generated variants |
| **Stakes** | High. A disclosure that is missing or cannot be read can leave the ad misleading (section 4: an ASA ruling ordered an ad with illegible small print not to run again). |
| **Who is affected** | Viewers who miss the terms or risks, the advertiser, its agency, and the compliance reviewer who approved different text |
| **Frequency** | Unknown. No public incident found of an AI-made ad faulted for garbled or missing fine print (searches in section 4). The rules and rulings found are about ads in general. |
| **Pattern ID** | ai-image-ads-missing-or-unreadable-disclaimers |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Disclosure mismatch rate: live ad placements whose required disclosures are missing, generator-drawn, or not matching the approved disclosure sheet in wording, size or duration, divided by all live placements sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Research shows character-aware models spell better, so garbled text may shrink, but a model still does not know which disclosure a claim needs or what size and timing a market expects, and text drawn into pixels cannot be checked or edited as text. (Our judgment, not tested.) |
| **Also searched as** | AI fine print garbled · AI ad disclaimer misspelled · add disclaimer to AI image · legal text in AI generated ad · AI video legal super |

Tests: [AI image ads missing or unreadable disclaimers test file](../../../tests/ai-image-ads-missing-or-unreadable-disclaimers.md).

## 1. In plain words
Many ads need fine print: loan terms, "results not typical," safety warnings, offer end dates. When a team makes the ad with an AI tool, it is tempting to put that text in the prompt and let the tool draw it. Image generators draw letters as shapes, and long strings of small, unusual words are where they fail most. The fine print comes out misspelled, half there, or too small to read, and a quick look at a thumbnail does not catch it. This page is about the ad's own required disclosures. The separate duty to label the ad as AI-made is on [AI-generated ad disclosure rules not met](./ai-generated-ad-disclosure-rules-not-met.md); the same overlay rule below applies to that label too.

## 2. What it looks like
The credit union, people, rates and IDs are invented. The disclosure wording is a fixture, not legal advice.

**Without the fix**
```
Marketer:  Spring auto loan banner. Headline "Rates as low as 1.99% APR*". Fine print at the bottom:
           "*APR = Annual Percentage Rate. 36-month term, with approved credit. Rates subject to change."
AI tool:   Here is your banner (1200x628), plus 300x250 and 320x50 versions.
           (Bottom strip reads "*APR = Anual Percntage Rae. 36-mnth trm, with aprovd credt.")
Marketer:  Looks great. Sending all three to the Phoenix campaign.
           (At 320x50 the strip is a gray smear about 4 pixels tall. The last sentence is gone.)
```
**With the fix**
```
Marketer:  Spring auto loan banner. Headline "Rates as low as 1.99% APR*". Fine print at the bottom: ...
AI tool:   I won't draw the fine print into the image; required text is added as real text afterward.
           Generating the art with no text and the bottom 20% left clear. Disclosure sheet DS-0412
           (Desert Sun CU, approved by compliance 10/20): claim "1.99% APR" needs disclosure D1.
           D1 overlaid from the sheet. Wording matches. 1200x628 and 300x250 pass the sheet's size check.
           320x50: D1 renders below the sheet's minimum size. Blocked.
           1) Drop 320x50  2) Send to compliance for a small-unit version  3) Something else
Marketer:  1.
AI tool:   320x50 dropped. Two sizes ready. Check log CL-7781 saved.
```
In the fixed version the generator never draws legal text, the wording comes from an approved sheet, and the size that cannot carry the disclosure is held rather than shipped.

## 3. Why it happens
- **Generators draw letters as shapes.** Liu and colleagues found popular text-to-image models "lack character-level input features," and that character-aware models did far better on rare words. Fine print is the hard case: many words, small type, and terms like "APR" that are rare in captions. (Applying their finding to fine print is our inference.)
- **The disclosure becomes part of the art.** Once the fine print is pixels, nobody can copy-check it, resize it or fix one word. Each resize, crop or generated variant shrinks or cuts it, and reviewers approve at thumbnail size where garble and tiny type look like texture.
- **The tool does not know the rules the ad is judged by.** FTC staff and the ASA judge the final ad as a viewer sees it: size next to the claim, contrast, placement, time on screen. A generator asked for "fine print at the bottom" optimizes for a good-looking image and may drop a line from a long prompt (see [token limit artifacts](../../generation-artifacts/failures/token-limit-artifacts.md)).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Required disclosures "must be clear and conspicuous." Factors include placement and "proximity to the relevant claim," prominence, whether it is "unavoidable," distractions, and whether "visual disclosures appear for a sufficient duration." "Size Matters. Disclosures that are at least as large as the claim to which they relate are more likely to be effective." "The ultimate test is not the size of the font or the location of the disclosure ... the ultimate test is whether the information intended to be disclosed is actually conveyed to consumers." | [FTC, .com Disclosures, March 2013](https://www.ftc.gov/sites/default/files/attachments/press-releases/ftc-staff-revises-online-advertising-disclosure-guidelines/130312dotcomdisclosures.pdf). Opened; text extracted from the PDF and quotes string-matched. | FTC staff guidance, not a rule, and the document says it is not a safe harbor. From 2013; not about AI. |
| A disclosure "can only qualify or limit a claim to avoid a misleading impression. It cannot cure a false claim." If it contradicts a material claim, "the claim itself must be modified." | Same FTC document. Quotes string-matched. | Same as above. |
| ASA ruling on an Omnipod 5 video-on-demand ad (seen on ITVX, December 2024), upheld May 21, 2025: the small print was not clearly legible at a reasonable viewing distance and did not stay on screen long enough, especially given the amount of text. The ASA said "viewers should not be expected to pause the ad to read the qualifications." Rules cited: CAP Code 3.1 and 3.10. | [ASA ruling, Insulet International Ltd](https://www.asa.org.uk/rulings/insulet-international-limited-a24-1273006-insulet-international-limited.html). Opened through a fetch tool; quote from the text it returned. | Non-US (UK). Not an AI-made ad. Shows how a regulator judges legibility and duration. |
| ASA advice: qualifications "should not be presented in a text size, font, or colour which makes them difficult to read," and "must not mislead by contradicting the claims that they qualify." | [ASA, Claims that require qualification](https://www.asa.org.uk/advice-online/claims-that-require-qualification.html), dated July 31, 2025. Opened through a fetch tool. | Non-US guidance; not AI-specific. |
| UK TV legal supers (HD, 16:9): "Preferred minimum text height" 30 lines; 26 lines on an opaque single-colored block. Hold: "0.2 seconds per word" plus 2 seconds recognition up to 9 words, 3 seconds for 10 or more. BCAP superimposed text guidance took effect March 1, 2019. | [Clearcast help, Legal supers](https://help.clearcast.co.uk/en/article/legal-supers-our-helpful-tools). Opened through a fetch tool. | Non-US; UK broadcast only. The page calls its timings "approximate." An example of one market's numbers, not a US standard. |
| Popular text-to-image models "lack character-level input features"; character-aware models showed "30+ point accuracy gains over competitors on rare words" on a visual spelling benchmark. | [Liu et al., Character-Aware Models Improve Visual Text Rendering, arXiv 2212.10562](https://arxiv.org/abs/2212.10562). Abstract opened and read. | Research benchmark from 2022 (revised 2023); newer commercial models were not tested there. |

**Searches for an incident (none found).** "AI image generator garbled text small print disclaimer ad"; "AI-generated ad gibberish text fine print backlash brand 2024 2025"; "ASA ruling small print not legible video ad qualification 2025". Results showed AI ads criticized for garbled background text, and non-AI ads faulted for illegible small print, but no AI-made ad faulted for its disclosures.

**Not used.** The planned [UX Collective article on text in AI images](https://uxdesign.cc/lost-for-words-why-text-in-ai-images-still-goes-wrong-b5232c39bd11) and a UCL explainer refused our fetch (HTTP 403) and were not read. Search summaries said a 2024 Skechers magazine ad had garbled store-sign text, that Meta told advertisers reviewing AI outputs is their responsibility, and that newer models render short text well. We did not open sources for these, so they are not stated as fact here.

## 5. The fix
**The principle:** Every required disclosure in a live ad is real text from an approved sheet, never pixels drawn by the generator, and was checked at the size and duration where it runs.

**Do this: advertisers, agencies and AI ad tools**
1. **Keep a disclosure sheet per ad, owned by compliance.** Each claim that needs a disclosure, the exact approved wording, where it sits relative to the claim, and the minimum size, contrast and (for video) on-screen time counsel set for each market and format. No sheet, no launch.
2. **Never prompt the generator with required text.** The tool strips disclosure text from prompts (lines with "*", "fine print," "terms," "APR," "results not typical" and the like) and asks for clean space instead: "no text, leave the bottom 20% clear."
3. **Overlay disclosures as real text after generation.** Insert the wording from the sheet by reference, not retyped, as a live text layer or burned-in super from the layout tool.
4. **Remove generator-drawn text that looks like fine print.** OCR the generated art before overlay; any small text block in the disclosure zone is cleared or the art is regenerated with "no text."
5. **Check every final size and cut.** OCR the export: wording matches the sheet letter for letter; size, contrast and placement meet the sheet's minimums; for video, the disclosure holds for the sheet's duration and appears with the claim it qualifies.
6. **Re-check after any change.** A resize, crop, new cut, platform-generated variant or added placement re-runs check 5 for that version.
7. **If the disclosure cannot fit, change the ad, not the font.** Drop the placement, shorten the claim, or send to compliance. Never shrink below the sheet's minimum; never use the disclosure to rescue a claim that is false (FTC: it "cannot cure a false claim").
8. **Log every check.** Ad version, placement size, sheet ID and version, OCR text, size and duration measured, result, who approved, date.

**Reference design: disclosure sheet row and check log**
```yaml
disclosure_sheet:
  id: DS-0412
  approved: {by: compliance, name: R. Okafor, on: 2026-10-20}
  claims:
    - claim: "Rates as low as 1.99% APR"
      disclosure_id: D1
      text: "APR = Annual Percentage Rate. 36-month term, with approved credit. Rates subject to change."
      placement: same frame, directly below claim
      min_size: per compliance memo M-77 for each placement size   # counsel sets, not this page
      min_duration_video: per memo M-77
check_log:
  id: CL-7781
  ad: DSCU-SPRING-AUTO-v3
  placement: 300x250
  generator_text_found: none
  ocr_text_matches_sheet: true
  size_check: pass
  result: pass
  date: 2026-10-26
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A placement cannot carry the disclosure at minimum size: drop it, send to compliance, something else |
| Ask one clarifying question | A prompt holds fine print and no sheet exists: "Is this text a required disclosure from compliance, or decorative copy?" |
| Admit uncertainty and show how to check | The user asks whether the disclosure is legally enough: say the tool checks the sheet, not the law, and name the reviewer |
| Hand off to a person | No sheet, a stale sheet, or a claim that the disclosure contradicts |

**Don't over-correct.** Do not pile on disclaimers the sheet does not list, and do not fill the frame with a wall of legal text; the ASA faulted the Omnipod ad partly for the amount of text shown too briefly. Brand names, slogans and decorative words the creative team approved are not disclosures; garbled decorative text is handled on [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md). Do not block an ad because OCR misreads correct small type; check against the text layer before failing it.

**Hand-off rule.** No sheet, a sheet past its review date, a claim with no listed disclosure, or a placement that fails the size or duration check goes to the compliance reviewer named on the sheet, with the ad version, the claim and the failed check. That placement stays held; others proceed.

**Framework used:** none yet. Rules 1, 5 and 7 follow the FTC factors and the ASA ruling in section 4; keeping text out of the generator is our judgment, consistent with Liu et al.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-ads-missing-or-unreadable-disclaimers.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Prompt includes the fine print text | Text stripped from prompt; art made with clear space | 2 |
| 2 | No disclosure sheet for a claim with "*" | Held; one clarifying question; routed to compliance | 1 |
| 3 | Generated art contains small text in the disclosure zone | Cleared or regenerated before overlay | 4 |
| 4 | Overlay wording differs from sheet by one word | Blocked | 3, 5 |
| 5 | 320x50 size renders disclosure below minimum | That size held; others pass | 5, 7 |
| 6 | Video super shorter than the sheet's duration | Blocked | 5 |
| 7 | Platform makes a cropped variant after approval | Check re-runs; cut disclosure blocks it | 6 |
| 8 | Log export | Every check has all fields in rule 8 | 8 |
| 9 | Approved slogan text in the art | Not treated as a disclosure; passes | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Disclosure mismatch rate** (primary) | 0 (proposed) | Weekly sample of live placements: OCR and layer check against the sheet / all sampled | Any |
| Placements live with generator-drawn disclosure text | 0 (proposed) | Export check: disclosure text found in raster, not in a text layer or super | Any |
| Prompts sent to the generator containing disclosure text | 0 (proposed) | Prompt log scan after stripping | Any |
| Placements launched without a sheet ID | 0 (proposed) | Ad server placements joined to check log | Any |
| Video ads with disclosure hold below sheet duration | 0 (proposed) | Frame-level check of the super's on-screen time | Any |
| Holds where compliance found the ad fine (counter-metric) | Under 20% of holds (proposed) | Check log review, monthly | Over 40% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt contains "*", "fine print," "terms apply," "APR" or "results not typical" | Generation prompt log | A headline that names a rate the sheet says needs no footnote |
| OCR finds small text in the bottom band of generated art | Pre-overlay OCR | A store sign or packaging in the scene |
| OCR of the export does not match the sheet text | Export check | OCR misread of correct small type; compare with the text layer |
| A claim with "*" and no disclosure in the same frame or scene | Export check, frame sampling | Disclosure sits in a voiceover the sheet allows |
| A placement size added after the check log date | Ad server change history | A larger size of the same aspect ratio, checked automatically |

**Starter rule:** required disclosures are never drawn by the generator; they are overlaid as real text from the approved sheet and checked at every placement size before launch.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-ads-missing-or-unreadable-disclaimers
runs: [on_prompt, post_generation, pre_launch, on_change]
reads: [prompt.text, disclosure_sheet, generated_art.ocr, export.ocr, export.text_layers, placement.sizes, video.super_timing]
trigger: disclosure text in prompt, no sheet, generator text in disclosure zone, wording mismatch, size or duration below sheet minimum
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Drop this placement", "Send to compliance", "Something else"]
on_miss: block_that_placement
metric: disclosure mismatch rate
counter_metric: holds where compliance found the ad fine
status: proposed
```

## 8. Related patterns
- [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md) - the closest existing page. It catches garbled text of any kind and requires generator text to match approved copy. This page is about legally required disclosures, which must never be generator-drawn and must also pass size, placement and duration checks.
- [AI-generated ad disclosure rules not met](./ai-generated-ad-disclosure-rules-not-met.md) - the "made with AI" label each market requires. This page covers the ad's own disclosures (offer terms, risk information). An AI label, when required, should be overlaid by the same rule.
- [AI product images that show features it does not have](./ai-product-images-show-features-it-does-not-have.md) - when the picture itself is false, fine print cannot fix it.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - who approved the version that ran.
- [Token limit artifacts in conditional generation](../../generation-artifacts/failures/token-limit-artifacts.md) - older page on long prompts losing their end, one way fine print gets dropped.

## 9. Common questions
### Can I ask an AI image generator to add the fine print to my ad?
Don't. Generate the art with no text and clear space, then add the approved wording as real text in your layout or video tool, where you can check every word and resize it.

### Why does AI mess up small text in images?
Research by Liu and colleagues found popular image models lack character-level input, so they draw words as shapes; rare words did worst. Fine print is long, small and full of rare terms.

### How big does a disclaimer have to be in an ad?
No single US number was found. FTC staff list factors: proximity, prominence, size next to the claim, contrast and time on screen. UK TV has set figures (Clearcast, section 4). Your compliance team sets the minimum on the sheet.

### Can a disclaimer fix an AI image that shows something the product doesn't do?
No. FTC staff guidance says a disclosure cannot cure a false claim; change the image.

### Does this apply to AI video ads too?
Yes. In video the disclosure must also stay on screen long enough to read; the ASA faulted a video ad whose small print did not.
