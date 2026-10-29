# AI Images With Baked-In Text and No Alt Text: Prices and Dates Screen Readers Cannot Read

<!-- SEO
title: AI Images With Baked-In Text and No Alt Text: Accessibility Risk
description: AI-made promo images put the price, date or offer in pixels with no alt text, so screen readers miss it. Keep key text live; write alt text from the copy.
search phrases:
- ai generated image alt text
- text in image accessibility wcag
- do images with text need alt text
- alt text for promo banner with price
- is text in images bad for accessibility
- ai social media graphic screen reader
- ada lawsuit missing alt text website
- how to write alt text for a flyer image
-->

**Frequency**: Unknown

## Issue: A business posts an AI-made image whose price, date, hours or offer exist only as pixels, with no alt text or with alt text that skips the words, so screen-reader users and people who enlarge text never get the information. Keep information text as live text where the channel allows it, and where it must be in the image, publish alt text that carries the same words from the approved copy.

> **Read this first:** This page is design guidance for a publishing workflow. It is not legal advice. The rules cited (W3C's WCAG 2.2 and US Justice Department guidance) are general accessibility rules, not specific to AI images; applying them to AI-made images is our reading. Lawsuit counts are one law firm's tally of all website accessibility cases, not of AI images or alt text. Whether the ADA or any other law applies to a given business, site or post is for a qualified lawyer to decide. Sources read on October 29, 2026.

> **One line:** A grocery chain asks an image generator for "BOGO chicken thighs, $2.99/lb, Sat-Sun only," posts the result as its home page banner and Instagram post with no alt text, and a blind shopper's screen reader says only "image" or a file name; the fix is to keep the offer in live text beside the art, and where text must sit in the image, write alt text from the approved copy and block publishing without it.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Mainly still images (web banners, email heroes, social graphics, flyers posted online). For video, text shown only on screen (a price, a date, a phone number) and never spoken is the same gap; video rules here are our judgment. |
| **Channel** | AI design and marketing tools that generate images with text, then a CMS, email builder or social scheduler that publishes them |
| **Stakes** | Medium. The shopper misses the offer, hours or terms; the business risks complaints and, in the US, website accessibility claims (section 4). High when the text is a recall, a safety notice, a deadline or a price someone pays. |
| **Who is affected** | Blind and low-vision people using screen readers or zoom, people with dyslexia using text-to-speech, and the business and agency that published the post |
| **Frequency** | Unknown for AI images. Missing alt text is common on the web in general: 53.1% of the top million home pages in February 2026 (section 4). No count found for AI-made images. |
| **Pattern ID** | ai-images-with-baked-in-text-and-no-alt-text |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unreadable-text rate: published images with information text in the pixels whose alt text is missing, empty, a file name, or not carrying that text, divided by all published images with information text sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Newer generators draw text more cleanly, which makes baking the offer into the image more tempting, and alt text is a field the publishing tool fills or leaves blank, not a model output. (Our judgment, not tested.) |
| **Also searched as** | AI banner no alt text · text in AI image screen reader · alt text for sale flyer · WCAG images of text AI · AI Instagram post accessibility |

Tests: [AI images with baked-in text and no alt text test file](../../../tests/ai-images-with-baked-in-text-and-no-alt-text.md).

## 1. In plain words
A screen reader cannot read words that are drawn into a picture. It reads the image's alt text. If the alt text is missing, it may say "image" or read the file name. If the alt text says "grocery banner," the listener still does not learn the price or the dates. People who enlarge text also lose: text inside an image cannot be set to the font size or colors they need, which is what WCAG 1.4.5 protects. AI image tools make this easy to get wrong, because the fastest path is "put the offer in the prompt and post what comes out." This page is about information text: prices, dates, hours, terms, calls to action. Garbled text is covered by [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md); required legal fine print is covered by [AI image ads missing or unreadable disclaimers](./ai-image-ads-missing-or-unreadable-disclaimers.md).

## 2. What it looks like
The grocery chain, people and IDs are invented.

**Without the fix**
```
Marketer:  Weekend promo banner: "BOGO chicken thighs, $2.99/lb, Sat-Sun only, Oak Lawn and Joliet stores."
AI tool:   Here is your banner (1600x500) and a 1080x1080 Instagram version. Both have the text in the image.
Marketer:  Publishing to the home page and scheduling the post.
           (CMS alt field left blank. Scheduler posts with no alt text.)
Shopper's screen reader on the home page: "Link, image, promo underscore gen underscore 8812 dot png."
           (The price, dates and stores never reach her. The image is also the link to the weekly ad.)
```
**With the fix**
```
Marketer:  Weekend promo banner: "BOGO chicken thighs, $2.99/lb, Sat-Sun only, Oak Lawn and Joliet stores."
AI tool:   Making the art with no text. On the home page the offer goes in live text beside the art.
           Copy C-2291 (approved 10/27) supplies the words.
           For Instagram the text must be in the image, so I overlaid it from C-2291 and drafted alt text:
           "Buy one, get one free chicken thighs, $2.99 a pound, Saturday and Sunday only, Oak Lawn and Joliet."
           Banner link text: "See this week's ad." Both alt fields filled; publish check passed. Log PL-5520.
Marketer:  Publish.
```
In the fixed version the words a shopper needs exist as text on every channel, and nothing publishes with an empty alt field.

## 3. Why it happens
- **Text in the prompt is the fastest path.** As generators draw short text more cleanly (our observation, not a measured claim), the offer goes into the picture instead of into the page. The words then exist only as pixels, which WCAG calls an "image of text."
- **Alt text lives in a different tool from the generator.** The image is made in one tool and published from a CMS, email builder or scheduler whose alt field is optional. Nobody owns filling it, and publishing does not stop when it is blank.
- **Automatic alt text describes the picture, not the offer.** Auto-captions say "chicken on a plate with text" and miss or misread the price; reading the words back from AI pixels can copy their spelling errors. The approved copy, not the pixels, is the reliable source.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 2.2 Success Criterion 1.1.1: "All non-text content that is presented to the user has a text alternative that serves the equivalent purpose," with listed exceptions, including pure decoration. | [W3C, WCAG 2.2](https://www.w3.org/TR/WCAG22/). Opened. | A technical standard, not a law by itself. Not about AI. |
| WCAG 2.2 SC 1.4.5 Images of Text (Level AA): "text is used to convey information rather than images of text," with exceptions when the image can be customized or the presentation is "essential." "Logotypes (text that is part of a logo or brand name) are considered essential." An image of text is "text that has been rendered in a non-text form (e.g., an image) in order to achieve a particular visual effect." | [W3C, WCAG 2.2](https://www.w3.org/TR/WCAG22/) and [Understanding SC 1.4.5](https://www.w3.org/WAI/WCAG22/Understanding/images-of-text). Opened. | Applies only when the technology can achieve the same visual presentation with real text. A social post that only accepts an image is a harder case; our rule 2 handles it. |
| For an image of text, "the text alternative must contain the same text presented in the image." | [W3C WAI images tutorial, Images of Text](https://www.w3.org/WAI/tutorials/images/textual/), updated April 12, 2017. Opened. | Tutorial guidance, not the standard itself. |
| February 2026 scan of the top 1,000,000 home pages: 95.9% had detected WCAG 2 failures; "Missing alternative text for images" on 53.1% of pages; 16.2% of all home page images (10.8 per page) lacked alt text. The report suggests rising errors "likely reflect" trends including "automated or AI-assisted coding practices." | [WebAIM Million, 2026](https://webaim.org/projects/million/). Opened. | Automated detection; home pages only. The AI remark is WebAIM's interpretation, not a measurement, and is about code, not AI images. |
| February 2025 scan: 18.5% of home page images lacked alt text; 44% of those were linked images, producing links "that were not descriptive." | [WebAIM Million, 2025](https://webaim.org/projects/million/2025). Opened. | Same method caveat. Shows why a banner that is also a link is the worst case. |
| US Justice Department guidance (March 18, 2022): Title III's requirements "apply to all the goods, services, privileges, or activities offered by public accommodations," including on the web; "Text alternatives convey the purpose of an image, including pictures, illustrations, charts, etc." It states the guidance has "no legally binding effect" and that businesses "can currently choose how they will ensure" access. | [ADA.gov, Guidance on Web Accessibility and the ADA](https://www.ada.gov/resources/web-guidance/). Opened. | Non-binding guidance. The page notes it does not reflect the newer rule for state and local governments. Does not mention images of text. Legal reading needs review. |
| Seyfarth Shaw counted 3,117 website accessibility lawsuits in US federal court in 2025, up from 2,452 in 2024 (Launey and Vu, March 25, 2026). | [Seyfarth, ADA Title III blog](https://www.adatitleiii.com/2026/03/federal-court-website-accessibility-lawsuit-filings-bounce-back-in-2025/). Opened. | All website accessibility suits, not alt text or AI images. Keyword search of court data; state courts excluded; may miss cases. |

**Searches for an incident (none found).** "AI generated image text no alt text accessibility screen reader social media marketing"; "ADA website lawsuit images of text alt text retailer 2025 number of lawsuits"; "Chain Store Age retailers face risks if websites aren't accessible." No public incident or lawsuit about an AI-made image with baked-in text was found. Results were about missing alt text in general and AI tools that write alt text.

**Not used.** The planned [Chain Store Age article](https://chainstoreage.com/retailers-face-risks-if-websites-arent-accessible) and a related Chain Store Age commentary returned HTTP 403 and were not read. A Perkins School for the Blind piece on AI-written alt text, a Sprout Social model card for AI alt text, and OpenAI's image generation announcement also returned 403. Search summaries said that a mid-2025 tracker counted about 2,014 federal website suits in the first half of 2025 with missing alt text among commonly cited barriers, that a court once ruled against Winn-Dixie over its website, and that the Justice Department moved the state and local government web rule deadlines to 2027 and 2028. We did not open sources for these, so they are not stated as fact here.

## 5. The fix
**The principle:** Every word a customer needs from an AI-made image reaches them as text: live text on the page where possible, and otherwise alt text with the same words from the approved copy.

**Do this: marketers, agencies and AI design tools**
1. **Keep information text out of the image when the channel allows live text.** On web pages and HTML email, prices, dates, hours, terms and calls to action go in live text next to or over the art. The generator makes art with no text (WCAG 1.4.5).
2. **When text must be in the image, overlay it from the approved copy.** Social posts and image-only placements get the text overlaid from the copy sheet, not drawn by the generator, so the words are known and match (see [garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md)).
3. **Write alt text from the copy, with the same words.** Alt text for an image of text carries every information word in the image, taken from the copy sheet, plus a short note on the picture if it adds meaning. Never build it only from OCR of AI pixels or from an auto-caption.
4. **Classify every image before publishing.** Informative (alt from rule 3), linked (alt names the destination or action), logo (the brand name), or decorative (empty alt, allowed only when the image has no text and no information). Missing alt, a file name, or "image" fails.
5. **Block publishing on a failed check.** The CMS, email builder and scheduler run the check on every image and every size. A failed image does not publish; others in the batch proceed.
6. **Check the live version.** After publishing, read the alt text back from the live page or post. Some tools drop alt text on resize, crop or cross-posting.
7. **For video, say what the screen shows.** A price, date, phone number or URL shown only on screen is also spoken in the voiceover or given in the caption or description text (our judgment; see [missing or wrong captions](../../../../human-machine-interface/goals/accessibility/failures/missing-or-wrong-captions-and-transcripts.md)).
8. **Log every check.** Image ID, channel, class, copy ID, alt text, live read-back result, who approved, date.

**Reference design: copy sheet entry and publish log**
```yaml
copy_sheet:
  id: C-2291
  approved: {by: brand lead, name: T. Alvarez, on: 2026-10-27}
  info_text: "Buy one, get one free chicken thighs, $2.99 a pound, Saturday and Sunday only, Oak Lawn and Joliet."
  link_text: "See this week's ad"
publish_log:
  id: PL-5520
  image: promo-weekend-1080
  channel: instagram
  class: informative
  text_in_pixels: overlaid_from_copy      # never generator-drawn
  alt_text_source: copy_sheet C-2291
  alt_contains_info_text: true
  live_readback: pass
  date: 2026-10-28
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The tool states what it did: art without text, live text on the page, alt text drafted from the copy |
| Ask one clarifying question | An image has text and no copy sheet: "Is this text information customers need, or decoration?" |
| Offer choices: 2-4 options plus "Something else", free text open | An image-only channel and no alt field: post the text in the caption, use a different placement, something else. Not when the alt field exists; then just fill it. |
| Hand off to a person | No approved copy, or the image text and the copy disagree |

**Don't over-correct.** Do not ban text from every image; logos, brand names and image-only social posts are fine when the alt text carries the words. Do not give decorative images long alt text; empty alt is right for pure decoration, and filling it adds noise to screen readers. Do not start alt text with "Image of," stuff it with keywords, or paste a whole flyer's legal page into it; required fine print is handled on the [disclaimers page](./ai-image-ads-missing-or-unreadable-disclaimers.md).

**Hand-off rule.** An image with information text and no copy sheet, image text that differs from the copy, or a channel that cannot carry alt text goes to the content owner named on the copy sheet, with the image, channel and failed check. That image stays held; the rest of the batch proceeds.

**Framework used:** WCAG 2.2 SC 1.1.1 and 1.4.5 and the W3C images tutorial (section 4). Writing alt text from the copy sheet rather than the pixels is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-images-with-baked-in-text-and-no-alt-text.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Web banner prompt with price and dates | Art has no text; offer is live text on the page | 1 |
| 2 | Instagram post that needs the text in the image | Text overlaid from copy; alt carries the same words | 2, 3 |
| 3 | Alt field left blank at publish | Blocked | 4, 5 |
| 4 | Alt text is "promo_gen_8812.png" or "image" | Blocked | 4 |
| 5 | Alt text omits the price | Blocked | 3 |
| 6 | Linked banner | Alt names the destination | 4 |
| 7 | Scheduler drops alt on cross-post | Live read-back fails and flags it | 6 |
| 8 | Video shows a phone number never spoken | Flagged | 7 |
| 9 | Decorative texture with no text | Empty alt passes | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unreadable-text rate** (primary) | 0 (proposed) | Weekly sample of published images with information text: alt read back from live page or post, compared with the copy sheet / all sampled | Any |
| Images published with empty, file-name or "image" alt | 0 (proposed) | CMS, email and scheduler publish logs | Any |
| Generator prompts containing prices, dates or hours for web placements | Trending down (proposed) | Prompt log scan | Rising two weeks running |
| Alt text dropped between publish and live | 0 (proposed) | Live read-back vs publish log | Any |
| Decorative images given long alt text (counter-metric) | Under 5% of decorative images (proposed) | Publish log sample | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| OCR finds a price, date or time in an image whose alt is empty | Pre-publish image scan | A product photo where the price tag is not the offer |
| Alt text is a file name, "image," or under three words on an image with text | Publish log | A logo whose alt is the brand name |
| Alt text shares no numbers with the image's copy sheet | Publish check | Copy sheet has no numbers |
| A linked image with no alt or link text | Live page scan | Link text sits in a visible caption next to the image |
| Image text and copy sheet differ | OCR vs copy sheet | OCR misread of correct overlay; check the layer |

**Starter rule:** no image with information text publishes until its alt text carries the same words from the approved copy, or the words are live text beside it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-images-with-baked-in-text-and-no-alt-text
runs: [on_prompt, pre_publish, post_publish]
reads: [prompt.text, copy_sheet, image.ocr, image.class, alt_text, link_target, live_page.alt_text, video.voiceover, video.captions]
trigger: info text in pixels with empty, file-name or mismatched alt; linked image without alt; alt dropped after publish
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Put the text in the caption", "Use a different placement", "Something else"]
on_miss: block_that_image
metric: unreadable-text rate
counter_metric: decorative images given long alt text
status: proposed
```

## 8. Related patterns
- [Chatbot accessibility problems: contrast, alt text, focus](../../../../human-machine-interface/goals/visual/failures/accessibility-gaps.md) - the closest existing page. It checks a chat widget's own cards and visuals against WCAG. This page is about images a business makes with AI and publishes on its site, email and social channels.
- [AI image ads missing or unreadable disclaimers](./ai-image-ads-missing-or-unreadable-disclaimers.md) - the sibling page; same overlay rule, applied to required legal text and its size and duration.
- [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md) - when the drawn words are wrong; this page is when they are right but unreadable to assistive technology.
- [Missing or wrong captions and transcripts](../../../../human-machine-interface/goals/accessibility/failures/missing-or-wrong-captions-and-transcripts.md) - the video side: speech and on-screen text without a text track.
- [Token limit artifacts in conditional generation](../../generation-artifacts/failures/token-limit-artifacts.md) - older page on long prompts losing their end, one way baked-in text comes out incomplete.

## 9. Common questions
### Do images with text in them need alt text?
Yes, if the text carries information. W3C's tutorial says the alt text must contain the same text shown in the image.

### Is it bad to put text in AI-generated images?
On web pages and email, put prices, dates and offers in live text instead (WCAG 1.4.5). Logos and image-only social posts are fine if the alt text carries the words.

### Can I let AI write my alt text?
Use it as a draft at most. Build the alt text from your approved copy, because a captioner may skip the price or copy a misspelling from the image.

### Can a business be sued over missing alt text?
Website accessibility suits are filed in the thousands each year in US federal court (section 4), but whether a law applies to your site or post is a question for a lawyer.

### What alt text should a decorative AI background get?
Empty alt, if it has no text and carries no information, so screen readers skip it.
