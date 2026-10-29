# AI Image Generator Misspells Text: Garbled Words on Signs, Posters and Menus

<!-- SEO
title: AI Image Generator Misspells Text: Why Words Come Out Garbled
description: AI image tools misspell words on signs, posters and menus or fill them with gibberish. Set real text in a design tool and proof every word before publishing.
search phrases:
- ai image generator misspells text
- why does ai mess up text in images
- ai generated image gibberish text
- dall-e misspelled words
- chatgpt image text spelled wrong
- firefly text garbled
- how to get correct text in ai image
- ai poster text wrong
-->

**Frequency**: Common

## Issue: Ask an AI image tool for a sign, poster, menu or slide with words on it, and it often draws letters missing, added or swapped ("Tcao" for "Taco"), invents gibberish filler text, or garbles a price, and a team that reads only the picture publishes it. Treat every word in an image as copy: set information text (names, prices, dates, menu items) in a design tool over generated art, proof every readable word against the approved copy, and fix by editing text, not by regenerating again and again.

> **One line:** An Austin food truck asks an image tool for a menu board reading "Brisket Taco $4.50" and gets "Brisket Tcao $4.5O," which goes to the printer; the fix is to generate the board art with a blank panel, set the exact menu text in a template, and have a named person proof every word at full size before print.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source measures or reports still images. Words in AI video carry the same risk and would need checks on sampled frames; no opened source measures text in AI video (our judgment). |
| **Channel** | Text-to-image tools, chat assistants that make images, and design tools with built-in generators, used for signs, posters, flyers, menus, event art, slides, social posts and ads |
| **Stakes** | Medium. A misspelled word on a poster or menu makes the business look careless and can become the story (section 4). Higher when the garbled text is a price, date, address or phone number a customer acts on (our judgment). |
| **Who is affected** | Customers who read the sign or menu, the business and its staff, and the designer or marketer who published it |
| **Frequency** | Common. OpenAI's own paper calls DALL-E 3's text "unreliable," and Adobe calls text "a known limitation" (section 4). No opened source gives a rate in real business use. |
| **Pattern ID** | ai-image-generator-misspells-text-in-images |
| **Family** | [AI Images That Ignore the Prompt](../README.md) |
| **Goal** | AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text. |
| **Primary metric** | Unproofed-or-misspelled text publish rate: published AI images with readable words where no word-by-word proof against approved copy was recorded, or any word differs from it, divided by all published AI images with readable words. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is two arXiv papers, one vendor research paper, two vendor help pages, one vendor forum reply, one user forum thread and two news reports. |
| **Will a better model fix this?** | Partly. OpenAI says text is "significantly improved" but can still struggle with "clarity," and in STRICT (2025) GPT-4o held up to about 800 characters while most other models declined past about 200. Short headlines are getting better; letter-perfect prices and menus still need a proof (our judgment, drawing on the cited tests). |
| **Also searched as** | AI misspelled my sign · AI poster gibberish letters · ChatGPT image typo · AI menu text wrong · AI image weird writing |

Tests: [AI image generator misspells text test file](../../../tests/ai-image-generator-misspells-text-in-images.md).

## 1. In plain words
A taco truck owner asks an image tool for a menu board with three items and three prices. The picture looks like a real chalkboard, so it goes to the printer. Up close, "Taco" reads "Tcao" and "$4.50" has a letter O in it. The tool drew shapes that look like letters. It never typed the words. Nobody read them one by one before print.

## 2. What it looks like
The business, people and prices below are invented.

**Without the fix**
```
Owner:     Make a chalkboard menu for Lone Star Tacos: Brisket Taco $4.50,
           Al Pastor Taco $3.75, Horchata $3.00.
Assistant: Here is your menu board. (One generation; it reads "Brisket Tcao $4.5O,"
           "Al Pastor Taco $3.75," "Horchta $3.00," plus a line of made-up words at the bottom.)
Owner:     Looks great, sending it to the print shop.
Customer (Saturday): Your sign says Horchta. And is the brisket $4.50 or $4.5-something?
```
**With the fix**
```
Owner:     Make a chalkboard menu for Lone Star Tacos: Brisket Taco $4.50,
           Al Pastor Taco $3.75, Horchata $3.00.
Assistant: A menu has item names and prices, so I made the chalkboard art with a blank
           panel and set your exact text in the menu template.
           Proof: 3 items, 3 prices, every word matches your list. No other text in the image.
           Sent to Maria Lopez to proof at full print size before it goes to the print shop.
Maria:     Proofed, approved.
```
The fixed version keeps prices and names out of the generator, reads back every word against the owner's list, removes stray text and ends with a named person proofing at print size.

## 3. Why it happens
- **The model reads words as tokens, not letters.** OpenAI's DALL-E 3 paper says its text encoder "actually sees tokens that represent whole words and must map those to letters in an image." Google researchers found that in T5, 87% of the most common English words are a single token, which hides their spelling; T5-XXL spelled common English words right only 66% of the time (Liu et al.).
- **The image is drawn as pixels, with no spell check.** CapCut's help page says garbled text comes from the model trying "to simulate text-like shapes without understanding real language." Nothing in generation compares the drawn letters with the prompt.
- **Longer text breaks down faster.** In STRICT, most diffusion models declined sharply past about 200 characters, which the authors tie to the 77-token limit of the CLIP text encoder many models use. A menu or flyer can pass that length quickly.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "DALL-E 3 can generate text when prompted," but "this capability is unreliable" because words have "missing or extra characters." | [Betker et al. (OpenAI), "Improving Image Generation with Better Captions" (DALL-E 3 paper)](https://cdn.openai.com/papers/dall-e-3.pdf). PDF opened Oct 29, 2026. | Vendor paper about its own model. The PDF is undated; it compares against outputs from Sept 20, 2023. Gives no error rate. |
| OpenAI's current image guide lists text rendering as a limitation: "Although significantly improved, the model can still struggle with precise text placement and clarity." | [OpenAI API docs, Image generation](https://developers.openai.com/docs/guides/image-generation). Opened Oct 29, 2026. | Vendor doc; no numbers. |
| Character-aware image models beat character-blind ones on DrawText spelling by 15+ points over Imagen-AR on frequent words and 30+ points on rare words (2,000 images per model, scored by OCR on the full string). OCR over-reported errors: when it flagged one, the image was actually right 34% of the time for ByT5-XXL and 9% for T5-XXL (128 samples checked by hand). | [Liu et al. (Google Research), "Character-Aware Models Improve Visual Text Rendering," arXiv 2212.10562](https://arxiv.org/abs/2212.10562) (v1 Dec 20, 2022; v2 May 3, 2023). Full PDF opened Oct 29, 2026. | Research models from 2022-2023, single words. Shows a cause and that OCR alone misjudges spelling, not a rate in today's products. |
| STRICT tested 10 models, including GPT-4o (gpt-image-1), Imagen 3, Gemini 2.0, FLUX 1.1 pro and Stable Diffusion 3.5. GPT-4o and Gemini held "strong performance up to approximately 800 characters" in English; most diffusion models declined past about 200. GPT-4o's normalized edit distance (lower is better) was 0.07 at 50 characters and 0.65 at 5,000. | [Zhang et al., "STRICT: Stress Test of Rendering Images Containing Text," arXiv 2505.18985](https://arxiv.org/html/2505.18985v1) (v1 May 25, 2025; EMNLP 2025 per search result, not opened). HTML opened Oct 29, 2026. | Preprint version read. Measures long blocks of text, not short signs. |
| An Adobe Community Manager answered a Firefly user's garbled-text complaint: "Text generation within AI models is a known limitation, and Firefly is no exception." She advised generating without text and adding it in Adobe Express, or using "Edit text in image." | [Adobe Community, June 29, 2026](https://community.adobe.com/questions-404/firefly-returns-a-slop-image-text-is-garbled-was-simplest-text-in-the-world-gives-an-awkward-unusable-image-poor-ratio-perspective-failure-to-feature-the-subject-1629777). Opened Oct 29, 2026. | Vendor staff reply in a forum. A later reply says each generation costs credits "regardless of whether the text comes out perfectly." |
| CapCut tells users to avoid prompting for exact words, use AI for "backgrounds, textures, scenes, objects," and add real text with its text editor. | [CapCut Help Center, Jan 12, 2026](https://www.capcut.com/help/garbled-text-on-ai-design). Opened Oct 29, 2026. | Vendor help page; no numbers. |
| A user reported that when ChatGPT makes an image with text labels, "the text is often misspelled or garbled," and proposed blank labels plus a separate proofread text step. | [OpenAI Developer Community, March 4, 2025](https://community.openai.com/t/misspellings-or-grabled-text-in-generated-illustrations/1135230). Opened Oct 29, 2026. | One user. The one reply is from another user, not OpenAI staff. |

**Incident:** "Willy's Chocolate Experience" in Glasgow, Scotland, was sold with AI-made images that NBC News said bore "strange and nonsensical lettering"; tickets cost £35 ($44.40), the event was canceled, police were called, and the organizer promised full refunds ([NBC News, Feb 27, 2024](https://www.nbcnews.com/tech/willy-wonka-inspired-chocolate-experience-outrage-rcna140726)). Hyperallergic listed the images' words, including "catgacating" and "exarserdray lollipops" ([Hyperallergic, Feb 28, 2024](https://hyperallergic.com/children-in-tears-at-disastrous-willy-wonka-factory-experience)). The garbled words were a sign of the AI images, not the main harm; the main harm was a misleading event (see [AI image mistakes in ads go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md)).

## 5. The fix
**The principle:** A word in an image is copy. Proof it like copy, and keep the words a customer acts on out of the generator.

**Do this: teams and assistants that make images with words in them**
1. **Flag text-bearing requests.** Before generating, mark any request that quotes words or asks for a sign, poster, menu, flyer, label, slide, banner or caption inside the image as "text matters."
2. **Set information text, don't generate it.** Prices, dates, times, addresses, phone numbers, URLs, names, menu items and any text longer than a short headline are set in a design tool over generated art with a blank area. Only a short display headline may be generated (we propose a limit of 5 words; STRICT's 200-character decline is far above that, so the cutoff is our judgment).
3. **Take the words from approved copy.** The exact copy comes from the requester's text or the approved brief, quoted once in the prompt or the template, never retyped from the image.
4. **Proof every readable word.** Compare each word in the final image with the approved copy and record the result. OCR may pre-screen, but a person makes the final read, since Liu et al. found OCR flagged correct words as errors.
5. **Remove stray text.** Any readable word the request did not ask for, such as gibberish on a background sign or a fake caption line, is blanked, removed or replaced with approved copy.
6. **Fix by editing, then stop.** If a generated headline is wrong, correct it with a text-edit tool or set it in the design tool. Regenerate at most a limit the team sets (2 tries is our proposed start), then switch to setting the text.
7. **A named person proofs at full size before publish.** Signs, menus, ads, flyers and slides get a recorded proof at the size they will print or display.
8. **Log it.** Approved copy, method (generated or set), proof result per word, stray text removed, reviewer and date.

**Reference design: text proof before sign-off**
| Check | Pass | Example |
|---|---|---|
| Request type | Text-bearing request flagged | "chalkboard menu" flagged |
| Method | Information text set, not generated | Prices set in template |
| Words vs copy | Every readable word matches approved copy | 9 of 9 words match |
| Stray text | None, or removed | Bottom gibberish line removed |
| Retry limit | Stopped and switched to setting text | 2 tries, then set |
| Proof | Named, dated, full size | M. Lopez, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every text-bearing result: say how the words were made (generated or set) and the proof result before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | A generated headline is still wrong at the retry limit: set it in the design tool, fix it with a text-edit tool, drop the words from the image and put them in the post text, something else |
| Ask one clarifying question | It is unclear whether the words must be exact: "Should the sign read exactly 'Grand Opening Saturday,' or is any shop sign fine?" |
| Hand off to a person | Always for the final proof of signs, menus, ads, flyers and slides |

**Don't over-correct.** Do not flag images with no requested words where background text is unreadable at publish size (a blurred Chicago street at night). Do not flag requests for invented or alien lettering on purpose (a fantasy map's runes). Do not ban generated headlines that pass the proof. Do not block internal drafts marked "not for publishing." Do not regenerate without limit; each try costs time and, on some tools, credits.

**Hand-off rule.** If a customer or reviewer reports a misspelled or garbled word in a published image, send it to the content owner and the approver the same day with the log, and replace every copy, including printed ones still in use.

**Scope.** This page is the general case for words in any language written in Latin letters. Packaging and labels in product shots go to [garbled packaging and label text](../../ai-image-brand-guidelines/failures/ai-product-shots-with-garbled-packaging-and-label-text.md); Arabic, Hebrew, Chinese and other scripts go to [wrong script or broken right-to-left](../../ai-image-generation-business-risks/failures/ai-image-text-wrong-script-or-broken-right-to-left.md).

**Framework used:** none yet. Rule 2 follows the Adobe and CapCut guidance and STRICT's length finding; rule 4 follows Liu et al.'s OCR check; rule 6 follows the Adobe "Edit text in image" advice; rules 1, 3, 5, 7 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-misspells-text-in-images.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Chalkboard menu with three prices | Flagged; prices set in template, not generated | 1, 2 |
| 2 | Generated headline reads "Grand Opennig" | Caught in proof; fixed by edit or setting | 4, 6 |
| 3 | Background sign shows gibberish | Removed or blanked before publish | 5 |
| 4 | OCR passes, no person proofed | Publish blocked | 7 |
| 5 | "A blurred city street at night" | Not flagged | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unproofed-or-misspelled text publish rate** (primary) | 0 (proposed) | Monthly sample of published AI images with readable words: no recorded proof, or any word differs from approved copy / all sampled | Any |
| Generated information text | 0 (proposed) | Generation log: prices, dates, names or menu items drawn by the generator rather than set | Any |
| Stray text left in | 0 (proposed) | Sampled review: readable words in published images not in the approved copy | Any |
| Tries per text-bearing image | Track, no target | Generation log: tries before a passing proof or the switch to setting text | Rising for 2 months |
| False text flags (counter-metric) | Track, no target | Sample of flagged requests with no words needed, or invented lettering on purpose | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt quotes words or names a sign, menu or poster; image published with no proof record | Generation log plus publish log | The words were set afterward in a design tool and proofed there, logged elsewhere |
| Prompt contains a price, date or phone number and the method is "generated" | Generation log | The number is decoration (a "1950s diner" sign), not information |
| Several regenerations of the same text prompt in a row | Generation log | The user is changing the scene, not fixing the words |
| Customer comment or ticket mentions "typo," "spelled wrong" or "says" plus a misread word, about an AI-made image | Social comments, support tickets | A typo in the approved copy itself |

**Starter rule:** no AI image with readable words is published unless its log shows a word-by-word proof against approved copy by a named person, and no price, date or contact detail in it was drawn by the generator.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-misspells-text-in-images
runs: [pre_generation, post_generation, pre_publish]
reads: [request.text, request.approved_copy, prompt.as_sent, image.method, image.ocr_words, review.word_proof, review.stray_text, generation.tries, review.signoff]
trigger: text-bearing request with information text generated, or any word differs from approved copy, or stray readable text, or retry limit reached, or no proof at publish
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Set the words in the design tool", "Fix the words with a text-edit tool", "Drop the words from the image and put them in the post text", "Something else"]
on_miss: block_publish
metric: unproofed-or-misspelled text publish rate
counter_metric: false text flags
status: proposed
```

## 8. Related patterns
- [Token limit artifacts](../../generation-artifacts/failures/token-limit-artifacts.md) - the closest older page. It covers details lost when a long prompt is cut at the encoder's limit; here a single short word can come out misspelled well inside the limit, though STRICT links long-text failures to that same 77-token limit.
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - meaning that drifts over repeated edits; here the first image already has wrong letters.
- [Garbled packaging and label text in AI product shots](../../ai-image-brand-guidelines/failures/ai-product-shots-with-garbled-packaging-and-label-text.md) - the product-shot case, where the fix is to place the real label art; this page covers signs, posters, menus and slides with no product label.
- [AI image text in the wrong script or broken right-to-left](../../ai-image-generation-business-risks/failures/ai-image-text-wrong-script-or-broken-right-to-left.md) - non-Latin scripts and translation; it needs a fluent reader, which this page does not cover.
- [AI images with baked-in text and no alt text](../../ai-image-generation-business-risks/failures/ai-images-with-baked-in-text-and-no-alt-text.md) - correctly spelled words that screen readers still cannot read.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the missing sign-off that lets a typo ship.

## 9. Common questions
### Why does AI mess up text in images?
Most image models read your prompt as word tokens, not letters, and then draw letter shapes as pixels. OpenAI's DALL-E 3 paper says the model "must map those to letters in an image," and nothing checks the spelling afterward.

### How do I get correct text in an AI image?
Generate the picture with a blank space, then add the words in a design tool. Adobe and CapCut both give this advice. Keep any generated words short, and read each one before you publish.

### Is ChatGPT better at text in images now?
Better, not perfect. OpenAI says text is "significantly improved" but can still lack clarity, and one 2025 test found GPT-4o strong up to about 800 characters. Prices and names still need a proof.

### Can I fix a misspelled word without regenerating the whole image?
Often, yes. Adobe points Firefly users to "Edit text in image," and any design tool can cover the word and set the correct one.

### Can OCR check the spelling for me?
As a first screen. In Liu et al., OCR flagged some correctly spelled words as errors, so a person should make the final read.
