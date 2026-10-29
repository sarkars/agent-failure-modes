# AI Changed My Product Photo: AI Image Tools That Alter the Product Reference Image You Supplied

<!-- SEO
title: AI Changed My Product Photo? Stop AI Tools Altering Your Supplied Product Image
description: You give an AI image tool or ad platform your real product photo and get back a product with changed parts, colors or labels. Lock and check it.
search phrases:
- ai changed my product photo
- ai image generator changed my product
- keep product the same in ai image
- meta ai changed my product image
- ai product photo wrong label
- ai background generator changed product shape
- rei two handlebars bike ad meta ai
- reference image not followed ai
-->

**Frequency**: Unknown

## Issue: A brand hands an AI image tool or an ad platform its real product photo, packshot or brand image, and the output shows the product with changed parts, colors, labels or proportions, and it runs because nobody compared it with the file they supplied. Keep the real product pixels out of the generator's reach where you can, list what must not change, and check every output and every live ad against the original reference before it runs.

> **Read this first:** This page summarizes news reports and vendor documentation as we read them on October 29, 2026. Whether an ad that shows an altered product is misleading advertising, and whether altering a hired model's face in a brand image needs her consent, are legal questions this page does not answer; they need review by a qualified person, such as an advertising lawyer. The rules below are workflow choices, not legal conclusions.

> **One line:** A paddle-sports brand gives an image tool its studio packshot of a two-seat yellow kayak for a lakeside spring ad, and the tool returns a kayak with three seats, an orange hull and a smeared logo; the fix is that the generator only makes the scene around a masked or composited real product, a locked list of parts, colors and label text is checked against the supplied file, and any platform variant is checked the same way before it runs.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened case is a still image: the REI bike ad and the campaign photos in the Business Insider reporting. The same checks apply to sampled video frames (our judgment; no opened video case). |
| **Channel** | Image editing and reference-image generation in AI image tools, product-photo background generators, and ad-platform creative tools that edit supplied images, plus the assistants that call them |
| **Stakes** | Medium to high. The ad shows a product the store does not sell (REI: "not something you will find in our assortment"), and the brand answers for it in public (section 4). |
| **Who is affected** | Shoppers, the brand, the vendor whose photo was altered, and models whose faces appear in the original shoot |
| **Frequency** | Unknown. No opened source gives a rate. Business Insider interviewed eight advertisers and agency executives (MediaPost, TNW), which shows the complaint is not one-off but is not a rate. |
| **Pattern ID** | ai-image-generator-alters-supplied-product-reference-images |
| **Family** | [AI Images That Break Brand Guidelines](../README.md) |
| **Goal** | AI images and video a brand publishes follow its brand guidelines: the right logo, colors, fonts, tone and product, nothing from another brand, and nothing unsafe next to its name. |
| **Primary metric** | Altered-reference rate: sampled published assets built from a supplied product or brand reference image in which the product fails any item on its locked list (shape, part count, color variant, logo, label text), divided by all sampled assets built from a reference. Proposed starting target: 0. |
| **Maturity** | Researched. One dated public incident (REI, June 2026) from an opened report, a secondhand summary of Business Insider reporting, and three vendor documents. |
| **Will a better model fix this?** | Partly. Higher input fidelity reduces drift, but OpenAI and Dreamina both still say masks and references guide rather than guarantee the result, and a model cannot turn off an ad platform's auto edit. (Our judgment, not tested.) |
| **Also searched as** | AI altered my packshot · Advantage+ changed my product · AI product background changed the bottle · image to image product not accurate · Midjourney keep my product |

Tests: [AI image generator alters supplied product reference images test file](../../../tests/ai-image-generator-alters-supplied-product-reference-images.md).

## 1. In plain words
The team has the real thing: a photo from the shoot, a clean packshot, the vendor's approved image. They give it to an AI tool to put the product in a new scene, or they upload it to an ad platform that "enhances" it. The tool does not paste the product in. It makes new pixels that look like the product. A bike grows a second set of handlebars, a dress becomes a shirt and trousers, a label's words smear. Because the team started from a real photo, they assume the product is still real and nobody checks it against the file they handed over.

## 2. What it looks like
The company, people and files below are invented.

**Without the fix**
```
Marketer:  Here's our packshot (NW-Tandem-Yellow.png). Put the kayak on a Minnesota lake at sunrise.
Assistant: Here's your spring ad. (The generator redrew the whole image from the reference.)
Marketer:  Beautiful. Sending it to the ad platform with enhancements on.
Customer (comment): Which model has three seats? I only see a two-seat version on your site.
Marketer:  The packshot was right. The tool must have changed it.
```
**With the fix**
```
Marketer:  Here's our packshot (NW-Tandem-Yellow.png). Put the kayak on a Minnesota lake at sunrise.
Assistant: I'll generate only the lake and sky, with the kayak cut out from your packshot and placed
           in. Locked list from the product record: 2 seats, yellow hull, black trim, logo on bow.
           Check against NW-Tandem-Yellow.png: 2 seats, hull color matches, logo pixels unchanged.
           One flag: the water reflection under the hull is generated, so it shows no logo; that is
           allowed. Platform enhancements are off for this ad. This goes to Jordan Lee for sign-off.
```
In the fixed version the product pixels come from the supplied file, the locked list is checked item by item against that file, and a person approves before it runs.

## 3. Why it happens
- **The generator redraws the product; the reference guides but does not lock it.** OpenAI says its mask is guidance and the model "may not follow its exact shape with complete precision," and that the model may struggle with consistency for "brand elements across multiple generations." Dreamina's FAQ says output "can change a label, a seam, a cap or the product's proportions."
- **The ad platform edits the supplied image after hand-off.** REI said a Meta AI tool made an "inaccurate and inappropriate alteration of a vendor-provided image." Advertisers told Business Insider Meta's tools changed products in campaign photos they shot themselves (TNW).
- **The wrong reference or the wrong comparison.** Midjourney's style reference "doesn't copy objects or people," so it cannot carry a product. Dreamina warns that checking each image against the last generated one lets "a small change in one generation" become the next reference.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| REI's Instagram ad for a Van Rysel bike showed "dual front and rear handlebars," "too many chains, blurry lettering," and "had been up for a week before being taken down on June 22." REI said: "Meta auto-enrolled us in an AI personalization tool that produced an inaccurate and inappropriate alteration of a vendor-provided image in some of our ads." Van Rysel confirmed the original came from its own shoot. | [TechSpot, Rob Thubron, June 25, 2026](https://www.techspot.com/news/112895-rei-pulls-ai-generated-bike-ad-after-meta.html). Opened via direct download Oct 29, 2026; quotes string-matched. | One incident. REI's statement is as TechSpot reports it. Already used on two sibling pages (section 8); here it is the example of a supplied image being changed. |
| The model from the original shoot, Amity Rockwell, wrote: "To alter a product they're supposedly selling? And my face along with it?" | Same TechSpot article. Quote string-matched. | Her post as quoted by TechSpot; we did not open the post. |
| Business Insider, in interviews with eight advertisers and agency executives, reported a backlash against Meta's AI ad tools. A Meta spokesperson said its terms state "AI can make mistakes and that it is the advertiser's responsibility to review the AI outputs." | [MediaPost, Around the Net, July 13, 2026](https://www.mediapost.com/publications/article/416505/metas-ai-ad-tools-are-a-nightmare-some-brands-al.html). Opened via direct download; quotes string-matched. | A short summary of Business Insider, which we did not open. |
| Meta suggested turning a client's pajama dress into a shirt and trousers (consultant Jessica Gleim), and marketer Abigail Hogue watched Meta's AI "warp the products in a campaign she had shot herself." | [TNW, Ana Maria Constantin, July 14, 2026](https://thenextweb.com/news/meta-ai-ad-tools-brands-chaos). Opened; Hogue quote string-matched. | Secondhand from Business Insider. The pajama dress was a suggestion; TNW does not say it ran. |
| OpenAI: input_fidelity "controls how strongly a model preserves details from input images during edits and reference-image workflows"; masking is "entirely prompt-based"; consistency for "brand elements" may occasionally struggle. | [OpenAI image generation guide](https://developers.openai.com/docs/guides/image-generation). Opened Oct 29, 2026; quotes string-matched. | Vendor documentation for one model family; it states limits, not rates. |
| Midjourney's Style Reference "doesn't copy objects or people, just the overall style." | [Midjourney docs, Style Reference](https://docs.midjourney.com/docs/style-reference). Opened via direct download; quote string-matched. | Describes one feature. Not evidence that any brand misused it. |
| Dreamina's FAQ says output "can change a label, a seam, a cap or the product's proportions," advises "Review each output against the original, not only against the previous generated image," and says a preserve prompt "is an instruction to the model, not proof of identical output." | [Dreamina (CapCut), Sep 30, 2026](https://dreamina.capcut.com/ai-image/product-image-consistency-faq). Opened; quotes string-matched. | A vendor describing its own tool's limits. No test data. |
| An agency-tools blog says Advantage+ Creative enhancements are on by default and that agencies' top complaint is silent changes to submitted assets, including cropped logos. | [AdLibrary, Murat Bock, Sep 20, 2026](https://adlibrary.com/posts/advantage-plus-creative-changes). Opened. | Vendor blog; its complaint claim is secondhand ("Trade coverage citing Financial Times"), which we did not open. Meta's default settings are disputed between sources. |

**Read through a summary only, kept out of the fix:** a search summary said Meta told The Seattle Times that Advantage+ Creative is off by default, and that a brand called Kirruna saw ads that "misrepresented product materials." We did not open those reports.

## 5. The fix
**The principle:** The supplied file is the truth about the product. The tool may change the scene; anything it does to the product is checked against that file before it runs.

**Do this: brand, marketing and agency teams, and assistants that build images from product references**
1. **Write a locked list per reference.** Before generating, list from the product record what must not change: shape and proportions, part counts (seats, handlebars, buttons), color variant, logo, label wording, included accessories.
2. **Composite the product where you can.** Cut the product out of the supplied file and generate only the scene around it, or edit with the product masked. Because masks are guidance only, rule 4 still applies.
3. **Use the right reference type.** A style reference sets look and color only; never use it to carry the product. Use the tool's image or object reference, with high input fidelity where offered.
4. **Check every locked item against the supplied file.** Count parts, sample product colors, read label text against the packshot, and compare the logo pixels. Compare to the original, never to an earlier generated image.
5. **Fix in place, then fall back to the real photo.** If an item fails, fix that region once. If it still fails, use the authentic product image in a controlled layout. Do not keep re-rolling.
6. **Treat platform edits as new outputs.** Turn off ad-platform enhancements that edit product images. Any platform variant that is allowed goes through rule 4, and the live render is compared with the supplied file within 24 hours of launch.
7. **A named reviewer signs off** on the final file with the locked-list result attached.
8. **Log the build:** reference file and source (shoot, vendor), locked list, tool and version, method (composite, masked edit, reference), check results, reviewer and date.

**Reference design: locked-list check**
| Locked item | Supplied file | Output | Result |
|---|---|---|---|
| Seats | 2 | 2 | Pass |
| Hull color | Yellow, sampled | Within team tolerance | Pass |
| Logo on bow | Present, file pixels | Unchanged | Pass |
| Label text | "Northwater Tandem 13" | Same, readable | Pass |
| Accessories | 2 paddles | 2 paddles | Pass |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A reference image is supplied and the product record is on hand: say the scene will be generated around the real product and which items will be checked, then do it |
| Ask one clarifying question | The reference shows more than one variant, or no product record exists: "Which color variant is this ad for?" |
| Admit uncertainty and show how to check | The tool cannot composite and must regenerate the product: say the product may drift and show the locked-list result |
| Hand off to a person | Any locked item still fails after one fix, a live ad differs from the supplied file, or a customer reports a product that looks wrong; always for final sign-off |

**Don't over-correct.** Do not ban reference-based generation; scenes, lighting and props may change. Do not fail generated reflections, shadows or background props that are not the product. Do not fail allowed crops and resizes to fit a placement. Do not demand a locked list for internal mood boards that will not be published. Do not treat a new camera angle as a failure in itself; check it against a real photo of that view if one exists.

**Hand-off rule.** If a published asset shows an altered product, pause it, send the asset, the supplied file and the build log to the campaign owner the same day, and tell the vendor if the source was theirs. The owner decides on any public statement.

**Framework used:** none yet. Rules 1, 4 and 5 follow the Dreamina FAQ; rules 2 and 3 follow the OpenAI and Midjourney documentation; rule 6 answers the REI case and the Business Insider reporting; rules 7 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-alters-supplied-product-reference-images.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Packshot supplied with no product record | Locked list built or question asked before generating | 1 |
| 2 | "Put this product in a new scene" | Product composited or masked, scene generated | 2 |
| 3 | Product passed as a style reference | Refused for product use; image reference used | 3 |
| 4 | Output has an extra part | Caught by count against the supplied file | 4 |
| 5 | Second variation checked only against the first output | Fails; must compare to original | 4 |
| 6 | Label text fails twice | Real photo used in a layout | 5 |
| 7 | Platform enhancement edits the product after upload | Live render compared and ad paused | 6 |
| 8 | Generated shadow differs from studio shadow | Not flagged | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Altered-reference rate** (primary) | 0 (proposed) | Weekly sample of published assets built from a reference: locked-list check against the supplied file / all sampled | Any |
| Assets with no locked-list record | 0 (proposed) | Build log joined to publish log | Any |
| Live ads that differ from the supplied file | 0 (proposed) | Live-render capture compared with the approved file | Any |
| Re-roll count per asset | Under 3 (proposed) | Generation log | Over 5 |
| False flags on scene areas (counter-metric) | Under 10% of flags (proposed) | Monthly review of flags the reviewer overrode | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Object count in the product region differs from the locked list | Output check log | The scene adds a second product on purpose, recorded in the brief |
| Product-region similarity to the supplied file drops below the team's threshold | Image comparison in the build log | A new angle, checked against a real photo of that view |
| Live ad render differs from the uploaded file beyond allowed crops | Live-render capture | Placement crop or resize on the allowed list |
| OCR of label text differs from packshot text | Output check log | Label hidden by a prop, recorded as allowed |
| Customer comment names a product feature the catalog does not list | Ad comments routed to the campaign owner | Customer confusing two real models |

**Starter rule:** no asset built from a supplied product image is published unless its build log shows a locked list checked against that file and a named reviewer's sign-off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-alters-supplied-product-reference-images
runs: [pre_generation, pre_publish, post_launch]
reads: [request.reference_files, product_record.locked_list, generation.method, generation.reference_type, output.locked_check, platform.enhancements, live_render.diff, review.signoff]
trigger: reference supplied with no locked list, or reference passed as style only, or any locked item fails, or platform enhancement edits product, or live render differs from supplied file, or no sign-off
moves: [lead_with_answer, ask_clarifying_question, admit_uncertainty, hand_off]
on_miss: block_publish
metric: altered-reference rate
counter_metric: false flags on scene areas
status: proposed
```

## 8. Related patterns
- [AI images break brand logo, color and font rules](./ai-images-break-brand-logo-color-and-font-rules.md) - the closest page. There the generator draws the brand's logo from a prompt with no file; here the team supplied the real product image and the tool changed it.
- [AI images in ads published without review](../../ai-image-generation-business-risks/failures/ai-images-in-ads-published-without-review.md) - also uses the REI case, for who approved which version and platform settings; this page is the product-fidelity check itself.
- [AI product images show features it does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - checks an image against the product spec, often with no reference at all; this page checks against the supplied photo.
- [AI image mistakes in ads go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) - what happens after launch.
- [Consistency failure](../../generation-artifacts/failures/consistency-failure.md) and [semantic shift](../../generation-artifacts/failures/semantic-shift.md) - drift across generations or from the prompt's meaning; this page is drift from a fixed source file.

## 9. Common questions
### Why did the AI change my product when I gave it the real photo?
Most tools do not paste your photo in. They make a new image guided by it, so parts, labels and proportions can shift. Dreamina's own FAQ says this.

### How do I keep my product exactly the same in an AI image?
Cut the product out of your photo and generate only the background, then check the result against the original file.

### Can I use Midjourney style reference for my product?
No. Midjourney says style reference does not copy objects or people. It carries the look, not the product.

### Did Meta really change REI's bike ad?
REI said Meta auto-enrolled it in an AI tool that altered a vendor image; the ad showed two sets of handlebars and ran a week before it came down on June 22, 2026 (TechSpot).

### How do I stop Meta Advantage+ from changing my product image?
Turn off the enhancements that edit images in each ad, then compare the live ad with your uploaded file after launch.
