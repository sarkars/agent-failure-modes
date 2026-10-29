# AI Image Text in the Wrong Script or Broken Right-to-Left: Arabic, Hebrew and Chinese Promos That Readers Cannot Read

<!-- SEO
title: AI Image Text in Arabic or Hebrew Comes Out Reversed or Broken: Overlay Real Text Instead
description: AI image tools draw Arabic and Hebrew text reversed or broken. Make the art with no text, typeset the words, and have a fluent reader check it.
search phrases:
- ai image generator arabic text broken
- dall-e arabic text not working
- hebrew text backwards in ai image
- chatgpt image arabic letters wrong
- firefly hebrew caption wrong order
- how to add arabic text to ai generated image
- ai image text in other languages
- translate text in ai generated image
-->

**Frequency**: Unknown

## Issue: A US business asks an AI image tool for a promo in Arabic, Hebrew, Chinese or Spanish, and the words come out reversed, as broken letter shapes, in the wrong script, or still in English, and nobody on the team can read them. Generate the art with no text, set the words in a real font with a layout engine that handles the script's direction, and have a fluent reader approve the final image.

> **Read this first:** This is design guidance for a marketing workflow, not legal advice. It makes no claim about any law on language, translation or advertising; if a translated ad carries prices, terms or required notices, a qualified person should review what those must say. Evidence is two research papers, user forum reports and vendor replies, read on October 29, 2026. No public ad incident was found (section 4).

> **One line:** A Dearborn, Michigan grocery asks an image generator for an Eid sale flyer "in Arabic," gets letters that look Arabic to the English-speaking marketer but read as reversed or broken shapes to every Arabic reader, and prints 2,000 copies; the fix is art with no text, the Arabic set in a real font by a tool that lays out right to left, and sign-off from a fluent reader before print.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source is about still images or image editing. Text drawn into video frames has the same risk; that is our judgment, not sourced. |
| **Channel** | AI image generators and AI design tools used to make flyers, social posts, menu boards, banners and packaging for audiences who read Arabic, Hebrew, Persian, Urdu, Chinese, Korean, Spanish or other languages |
| **Stakes** | Medium. The ad tells its audience that nobody who speaks their language looked at it, and a wrong price or date in the foreign text can go unnoticed. High for safety notices, recalls, dosing and legal terms. (Our judgment.) |
| **Who is affected** | Readers of the target language, the local business or chain running the promo, the agency, and the team member asked to "just make it in Arabic" |
| **Frequency** | Unknown. One 2026 benchmark found degradation for every editing system it tested, largest on Hebrew and Arabic (section 4). No rate for published ads was found. |
| **Pattern ID** | ai-image-text-wrong-script-or-broken-right-to-left |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unchecked non-English text rate: published images with words in a language other than English that have no logged approval from a fluent reader of that language, divided by all sampled published images with non-English text. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is two papers, three forum threads with vendor replies, and one news report on a related on-screen text error; no ad incident was found. |
| **Will a better model fix this?** | Partly. Research models now render several languages better, but a 2026 benchmark still found every tested system degrades outside English, and a model drawing pixels cannot be proofread by a team that cannot read the script. (Our judgment, not tested.) |
| **Also searched as** | Arabic text AI image reversed · AI flyer in Spanish · Chinese characters wrong AI image · right-to-left text image generator · multilingual text rendering AI |

Tests: [AI image text in the wrong script or broken right-to-left test file](../../../tests/ai-image-text-wrong-script-or-broken-right-to-left.md).

## 1. In plain words
Arabic and Hebrew are written right to left. Arabic letters also change shape and join depending on where they sit in a word. Software that sets text knows this: W3C's guide to the Unicode Bidirectional Algorithm explains that "the order of characters in memory (logical) is not the same as the order in which they are displayed (visual)," and that numbers still run left to right inside right-to-left text. An image generator does not run that algorithm. It draws pixels that look like text. So the result can be letters in the wrong order, shapes that do not join, a mix of scripts, or the English prompt left untranslated. The marketer cannot tell, because the shapes look plausible to someone who does not read the language. This page is about the script, direction and language of the text. Spelling errors in English text are covered by [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md); missing alt text is covered by [AI images with baked-in text and no alt text](./ai-images-with-baked-in-text-and-no-alt-text.md).

## 2. What it looks like
The grocery, people and IDs are invented.

**Without the fix**
```
Marketer:  Make an Eid sale flyer for our Dearborn store, in Arabic: "Eid Mubarak! 20% off lamb, Fri-Sun."
AI tool:   Here is your flyer (8.5x11, print-ready). The headline and offer are in Arabic.
Marketer:  Looks great. Sending 2,000 to the printer and posting it to Facebook.
           (Nobody on the team reads Arabic. The headline letters run left to right and do not join.)
Customer comment: "Who made this? The Arabic is backwards. Is the 20% even right?"
```
**With the fix**
```
Marketer:  Make an Eid sale flyer for our Dearborn store, in Arabic: "Eid Mubarak! 20% off lamb, Fri-Sun."
AI tool:   I made the art with no text in it. Arabic words will be typeset, not drawn by the generator.
           Which Arabic copy should I use?
           1) Send the text to our translator (Nadia, on file)  2) Paste approved Arabic copy
           3) Something else
Marketer:  2. [pastes copy approved by Nadia, C-7710]
AI tool:   Set C-7710 in Noto Naskh Arabic, right-to-left layout; "20%" kept left-to-right inside it.
           Sent the proof to Nadia for a read of the final image. Print is on hold until she approves.
Nadia:     Approved. Log PR-3304.
```
In the fixed version no Arabic letter comes from the image model, the words come from approved copy, and a fluent reader checks the final image before it prints.

## 3. Why it happens
- **The generator draws text as pixels, not as typed characters.** It has no layout engine for direction or letter joining. An OpenAI forum reply cited a help page saying "DALL·E is not currently designed to produce text," and an Adobe Community Manager wrote that "Firefly doesn't really know how to write." Earlier research ties text errors to models that "lack character-level input features" (Liu et al.).
- **Training and tuning lean toward English.** The Glyph-ByT5-v2 authors describe their own earlier text-rendering model as one that "still focuses solely on English," and say widely used generators still struggle with multilingual text. The MULTITEXTEDIT benchmark found degradation "largest on Hebrew and Arabic."
- **Nobody on the team can read the output.** The person approving the flyer sees shapes that look right. Errors such as reversed order or mixed scripts are only visible to a reader of that language, and the workflow has no step that asks one.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A benchmark of 3,600 text-in-image editing instances across 12 languages tested 12 open-source and proprietary systems and found degradation for every model, "largest on Hebrew and Arabic and smallest on Dutch and Spanish." Errors include missing diacritics, "reversed RTL order" and mixed-script renderings; layout and background often survive while script forms are distorted. | [Cheng et al., MULTITEXTEDIT, arXiv 2605.08163, May 2026](https://arxiv.org/abs/2605.08163). Abstract opened Oct 29, 2026. | Preprint, not peer reviewed. Editing existing images, not generating new ones. We read the abstract only; the 12 languages are not named there. |
| Glyph-ByT5-v2 reports accurate visual text rendering "for 10 different languages," with a benchmark of 1,000 prompts (100 per language), and says DALL-E 3 and Ideogram 1.0 still struggle with multilingual text. | [Liu et al., Glyph-ByT5-v2, arXiv 2406.10208v1, June 2024](https://arxiv.org/abs/2406.10208v1). Abstract opened. | Research model built by the authors; their comparison with commercial tools is their own. The abstract does not name the languages, so we do not claim it covers Arabic or Hebrew. |
| Text-to-image models' text errors are linked to a lack of character-level input; character-aware encoders improved spelling on the authors' DrawText benchmark. | [Liu et al., Character-Aware Models Improve Visual Text Rendering, arXiv 2212.10562, Dec 2022](https://arxiv.org/abs/2212.10562). Abstract opened. | English spelling only; no other scripts in the abstract. Older models. |
| A user reported Arabic text in DALL-E output is "distorted and unreadable, making this feature unusable for Arabic-speaking users" (March 10, 2025). Another user replied that the problem affects other languages and cited "DALL·E is not currently designed to produce text." | [OpenAI Developer Community, Issue with Arabic text support in DALL-E](https://community.openai.com/t/issue-with-arabic-text-support-in-dall-e/1139807). Opened. | User reports, single thread, no staff reply. Weak. |
| A user reported that Arabic words in generated images "often appear with spelling mistakes, missing letters" and suggested rendering Arabic "using proper font engines." An account named OpenAI_Support replied the same day that it would bring this "directly to the product team." | [OpenAI Developer Community, Improving Arabic text rendering, March 2026](https://community.openai.com/t/improving-arabic-text-rendering-in-ai-image-generation/1376545). Opened. | The page does not confirm the replier's role. Not a measured rate. |
| A user reported that Arabic text was generated correctly but the model "still arranges the page using a left-to-right (LTR) layout logic." OpenAI_Support replied on Sept. 8, 2026 that it would pass the feedback to the product team with no timeline. | [OpenAI Developer Community, Systematic RTL layout issue, April 2026](https://community.openai.com/t/systematic-rtl-layout-issue-in-arabic-image-document-generation/1379790). Opened. | One user report. Shows that correct letters do not mean correct direction for the layout. |
| A Firefly user asked for a Hebrew caption and reported "the order of the letters in Hebrew is incorrect" (Feb 20, 2026). The reply marked correct, from a Community Manager, suggested making the image without text and adding the caption in Adobe Express. | [Adobe Community, Hebrew caption letter order](https://community.adobe.com/bug-reports-403/hello-i-created-a-picture-today-and-asked-to-add-a-caption-to-it-in-hebrew-and-the-caption-came-out-wrong-the-order-of-the-letters-in-hebrew-is-incorrect-1550836). Opened. | One user report. The vendor-side reply is the same fix this page proposes. |
| In a Coca-Cola ad campaign, an on-screen quote translated from French credited a non-existent J.G. Ballard book, and its translator spotted the word "Shangai" misspelled in the typed text. The agency, VML, said AI was used only for early research and humans fact-checked. | [Fortune, Beatrice Nolan, May 14, 2025](https://fortune.com/2025/05/14/ai-coca-cola-ad-campaign-invented-fake-book). Opened. | Not about script or direction, and the text was not drawn by an image model. Used only to show that on-screen translated text in a major ad shipped with an error the translator caught afterward. |

**No public ad incident found.** Searches for Arabic text reversed or disconnected in AI images, Hebrew text backwards in Midjourney, DALL-E or gpt-image, and multilingual text rendering benchmarks found forum reports, papers and vendor blogs, but no news report of a published business ad with broken script. Vendor blogs claiming newer models handle Arabic well were read only through search summaries and are not used.

## 5. The fix
**The principle:** No word in a non-Latin script, and no word in a language nobody on the team reads, comes from the image model's pixels. Words come from approved copy, set in a real font, and a fluent reader approves the final image.

**Do this: marketing, design and agency teams, and assistants that make images for other-language audiences**
1. **Generate art with no text.** For any image with words in Arabic, Hebrew, Persian, Urdu, Chinese, Japanese, Korean, Hindi, Thai or another non-Latin script, the prompt asks for no text, and any text the model draws anyway is removed.
2. **Typeset the words.** Overlay the text in a design tool with a font that supports the script and a layout engine that handles direction and letter joining. Never ask the generator to "write it in Arabic."
3. **Use approved copy, not machine output.** The words come from copy a translator or fluent staff member wrote or approved, stored with a copy ID. The generator's translation of the English prompt is not copy.
4. **Lay out the whole design right to left for Arabic and Hebrew.** Reading order, logo side, arrows and price blocks follow right-to-left order; numbers and phone numbers stay left to right inside it.
5. **Check for leftover English.** Every word in the final image is in the target language, or is a brand name or number on purpose.
6. **A fluent reader approves the final image.** Not the copy document: the exported image or print proof, at final size. Log the reader's name, language and date.
7. **Hold print and publish until approval.** No print order, post or upload without rule 6 logged.
8. **Spanish and other Latin-script languages still need rules 3, 5 and 6.** Generators can draw Latin letters, but accents, words and prices still need a reader.

**Reference design: other-language image record (checked before print or publish)**
| Field | Example |
|---|---|
| Image ID and channel | FL-0412, print flyer and Facebook post |
| Target language and script | Arabic, right to left |
| Art prompt says "no text" | Yes; model-drawn text removed: none found |
| Copy ID and who wrote it | C-7710, Nadia H. (translator on file) |
| Font and layout | Noto Naskh Arabic, right-to-left layout |
| Fluent reader, date, result | Nadia H., Oct 29, 2026, approved (PR-3304) |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The user asks for text in another language and no approved copy exists: send to the translator, paste approved copy, something else. Do not offer choices when an approved copy ID is already attached; just typeset it. |
| Ask one clarifying question | The language or dialect is unclear: "Which language should the flyer use, Arabic or English and Arabic?" |
| Admit uncertainty and show how to check | The assistant cannot verify the script itself: say so and route the proof to a fluent reader |
| Hand off to a person | Any non-English proof, before print or publish |

**Don't over-correct.** Do not refuse to make other-language ads, and do not drop the language so the ad runs only in English. Do not demand a translator for brand names, logos or numbers. Do not re-review an approved image when only the art behind the text changes and the text layer is untouched; re-check if the text layer moves or is resized. English-only images with English text stay under the [baked-in text and alt text](./ai-images-with-baked-in-text-and-no-alt-text.md) rules.

**Hand-off rule.** Every image with non-English text goes to a fluent reader of that language before print or publish. If a published image is found with model-drawn non-Latin text or no reader approval, pull it and send it to that reader and the campaign owner the same business day.

**Framework used:** none yet. Rules 1 and 2 follow the Adobe Community Manager's reply and the forum suggestion to render Arabic with proper font engines; rule 4 follows the W3C bidi explanation and the RTL layout report; rule 6 follows the MULTITEXTEDIT finding that errors sit in script fidelity a non-reader cannot see. The rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-text-wrong-script-or-broken-right-to-left.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Make an Eid flyer in Arabic" | Art made with no text; asks for approved copy | 1, 3 |
| 2 | Approved Hebrew copy supplied | Typeset right to left, numbers left to right | 2, 4 |
| 3 | Model draws Chinese characters anyway | Removed before overlay | 1 |
| 4 | Spanish flyer with leftover English "Sale" | Flagged | 5, 8 |
| 5 | Proof ready, no reader logged | Print and publish blocked | 6, 7 |
| 6 | Published image found with model-drawn Arabic | Pulled and handed off same day | Hand-off |
| 7 | Background swapped, text layer untouched | No re-review | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked non-English text rate** (primary) | 0 (proposed) | Weekly sample of published images with non-English text: no logged fluent-reader approval / all sampled | Any |
| Non-Latin text drawn by the model | 0 (proposed) | Image records where "model-drawn text removed" is blank or "no," for non-Latin targets | Any |
| Proofs approved without a copy ID | 0 (proposed) | Image records with empty copy ID | Any |
| Reader rejections per 100 proofs | Track; no target set | Approval log | Rise of 50% month over month (proposed) |
| Re-reviews when only the art changed (counter-metric) | Under 5% of reviews (proposed) | Review log joined to layer change log | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A prompt names a language or script ("in Arabic," "in Chinese," "en español") | Generator prompt log | The user wants art in a style from that culture with no text |
| An OCR or script detector finds non-Latin characters in a generated image | Post-generation scan | A brand logo with non-Latin letters on purpose |
| Comments on a post say the text is backwards, wrong or unreadable | Social comment log, keyword match in that language and English | Readers joking about a design choice |
| A print order for an image with non-English text has no reader approval | Print vendor order joined to image records | The text was approved in a prior run of the same file |

**Starter rule:** no image with non-English text is printed or published until its record shows art with no model-drawn text, an approved copy ID and a fluent reader's approval of the final image.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-text-wrong-script-or-broken-right-to-left
runs: [on_prompt, post_generation, pre_print, pre_publish]
reads: [prompt.language_request, image.detected_scripts, image.model_text_removed, copy.id, copy.language, layout.direction, review.reader, review.language, review.date]
trigger: prompt asks for text in another language, or non-Latin text found in generated pixels, or no copy ID, or RTL language with LTR layout, or no fluent-reader approval
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Send the text to our translator", "Paste approved copy", "Something else"]
on_miss: block_print_and_publish
metric: unchecked non-English text rate
counter_metric: re-reviews when only the art changed
status: proposed
```

## 8. Related patterns
- [AI images with baked-in text and no alt text](./ai-images-with-baked-in-text-and-no-alt-text.md) - the closest page. It covers words that exist only as pixels so screen readers miss them, in any language. This page covers whether the words are in the right script, direction and language at all, which a sighted English-speaking reviewer cannot judge.
- [AI images with cultural and religious errors](./ai-images-with-cultural-and-religious-errors.md) - wrong symbols, flags and customs for a community; it lists script as one element to check. This page owns the text itself: typesetting, direction and the fluent-reader check.
- [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md) - misspelled or garbled text in general.
- [Token limit artifacts in conditional generation](../../generation-artifacts/failures/token-limit-artifacts.md) - long prompts losing detail, a separate cause of missing words.

## 9. Common questions
### Why does ChatGPT or DALL-E write Arabic letters wrong in images?
The image model draws text as pictures and does not run the right-to-left and letter-joining rules that text software uses. Users have reported distorted Arabic and left-to-right layouts on OpenAI's forum.

### How do I put Arabic or Hebrew text on an AI-generated image?
Generate the image with no text. Then add the words in a design tool with a font that supports the script and right-to-left layout. Adobe's Community Manager suggested the same for Firefly.

### Why is my Hebrew text backwards in an AI image?
Hebrew is stored in one order and displayed right to left by layout software. A generator drawing pixels can get the order wrong, as a Firefly user reported.

### Can AI translate the text in my image into Spanish?
It can draft a translation, but treat it as a draft. Use copy a fluent reader approved, typeset it, and have that reader check the final image for leftover English and wrong prices.

### Are newer image models better at other languages?
Research models report better multilingual rendering, but a 2026 benchmark still found every tested system degrades outside English, most on Hebrew and Arabic. Test your own tool, and keep the reader check.
