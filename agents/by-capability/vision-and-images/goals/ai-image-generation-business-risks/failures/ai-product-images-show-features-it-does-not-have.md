# AI-Generated Product Photos That Mislead: Images Showing Features the Product Does Not Have

<!-- SEO
title: AI-Generated Product Photos That Mislead Buyers: False Advertising Risk and Fix
description: A business uses AI images or video to sell a product or event, and the picture shows features, sizes or results the real thing does not have. How to check images against the real product before publishing.
search phrases:
- ai generated product photos misleading
- is it false advertising to use ai images
- ai generated listing photos not as pictured
- etsy ai generated crochet pattern images
- willy wonka experience glasgow ai images
- can i use ai images for my product listing
- ai product image does not match real product
- ftc rules on ai generated ad images
-->

**Frequency**: Occasional

## Issue: A business publishes AI-generated images or video of its product or event that show features, sizes or results the real thing does not have, and buyers pay for what the picture promised.

> **Read this first:** Statements about advertising law, regulators and rulings on this page summarize the sources cited here. They are not legal advice and need review by a qualified person, such as an advertising lawyer, before anyone relies on them. Whether a given image is false advertising depends on the ad, its context and the jurisdiction. Two of the three incidents below are in the UK, not the US. The fix below is a product and workflow choice, not a legal conclusion.

> **One line:** A seller or marketer asks an image tool for a product shot or event poster and publishes what comes out, with nothing that compares the picture to the real product, so the ad shows a scarf the pattern never makes, a toy that moves like a real dog, or a candy wonderland that turns out to be a near-empty warehouse; the fix is that product images are photos of the real product or pass a feature-by-feature check against the product spec before publishing, AI scene images carry a visible label, and claims shown in an image go through the same review as claims in text.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The Etsy and Glasgow cases are still images; the UK robot-dog ruling is about video footage. |
| **Channel** | Visual: listing photos, ads, event posters and product videos made with text-to-image, image editing or video tools, and the publish step after them |
| **Stakes** | High. Buyers pay for something they do not get; the business faces refunds, platform action and, per the sources in section 4, regulator action. |
| **Who is affected** | Buyers and ticket holders, the business that publishes the image, and the marketplace or ad platform that carries it |
| **Frequency** | Occasional, by our judgment. No opened source gives a rate. NBC News found more than half a dozen Etsy storefronts in one search (section 4). |
| **Pattern ID** | ai-product-images-show-features-it-does-not-have |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unchecked AI product image rate: published images that show the product and are AI-generated or AI-edited with no feature-by-feature spec check on record, divided by all published AI product images. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model makes a more convincing picture. Whether the real product has the feature in it is a fact outside the model, so it needs the spec and a check. (Our judgment, not tested.) |
| **Also searched as** | AI listing photos not as pictured · fake AI product images · AI ad does not match product · AI event poster misleading · AI images false advertising law |

Tests: [AI product images that show features it does not have test file](../../../tests/ai-product-images-show-features-it-does-not-have.md).

## 1. In plain words
A small seller has a crochet pattern but no finished item to photograph. An image tool makes a perfect fox in a mossy forest in seconds. The seller posts it. Buyers follow the pattern and get something that looks nothing like the picture. Nobody lied in words; the picture did. The same thing happens with event posters, toy videos and before-and-after shots.

## 2. What it looks like
No opened source shows a transcript. The scenario is a US seller using a listing tool with an image generator; the product follows the Etsy crochet case NBC News reported.

**Without the fix**
```
Seller: Make a main listing photo for my crochet fox pattern. Cozy forest, extra fluffy.
Tool:   Here are 4 images. #1 is a fluffy fox in a striped scarf on a mossy log.
Seller: Perfect. Use #1 as the main photo and publish.
Tool:   Published: "Easy Crochet Fox Pattern, $6". It is now your main photo.
        (The pattern has no scarf and uses smooth worsted yarn.)
Buyer review, two weeks later: "Looks nothing like the picture. No scarf, and mine isn't fluffy." 1 star.
```
**With the fix**
```
Seller: Make a main listing photo for my crochet fox pattern. Cozy forest, extra fluffy.
Tool:   A main photo has to show a fox made from this pattern. Do you have a photo of one you made?
Seller: Not yet.
Tool:   I checked draft #1 against your pattern: the scarf is not in it and the yarn looks fuzzy, not worsted.
        I can fix both and add it as a labeled extra image: "AI illustration, not the finished item."
        1) Add as labeled extra image  2) Upload my own photo first  3) Something else
Seller: 1.
Tool:   Added as image 2 with the label. The main photo slot stays empty until you upload a real photo.
```
In the fixed version the tool asks for a real photo first, lists each mismatch against the spec, labels the AI image where the buyer sees it, and never lets it be the main product photo.

## 3. Why it happens
- **The image tool never sees the product.** It draws what "a crochet fox" or "a robot puppy" looks like from training data, not what this pattern or this toy makes. Nothing in a plain generate-and-publish flow compares the two. (Our reading.)
- **A picture makes claims without words.** Copy review checks sentences. A scarf, a wagging tail or a chocolate fountain in an image is a claim too, and the FTC says it looks at "words, phrases, and pictures" (section 4). Teams that review only text miss it.
- **Making a fake shot is faster than making the product.** NBC News reports free generators turn a prompt like "crochet Garfield" into an image in seconds, while photographing a real item takes the item. A seller with no finished product has every reason to skip it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Buyers say Etsy crochet patterns, which "typically range from $2 to $10", were sold with images that appear AI-made. One review: "The pattern looks nothing like the picture that advertised the pattern." In 48 reviews on 17 listings since August 2023, six reviewers attached photos of partial projects "with features that didn't match the product listings." A store using one such image had "almost 7,000 sales." | [NBC News, Kat Tenbarge, April 24, 2024](https://www.nbcnews.com/tech/tech-news/etsy-crochet-buyers-suspect-ai-made-images-used-sell-patterns-rcna145878). Opened and read; quotes string-matched. | US. Whether the images are AI-made is the buyers' and NBC's judgment; the stores did not confirm. |
| Etsy "requires sellers to accurately depict their products in listing photos", per NBC. Etsy said a shopper who gets an item "that does not match the listing image or description" can "receive a full refund through our Purchase Protection Program." | Same NBC News article. Opened and read; quotes string-matched. | Etsy's own policy page returned 403 and was not opened; the policy line is NBC's summary. |
| An organizer in Glasgow, Scotland, House of Illuminati, "used AI images to illustrate" a Willy Wonka-style event; parents paid "$45 (£35)" per ticket. The event "was canceled halfway through its opening day and has promised full refunds." Police Scotland told Sky News officers were called and "advice was given." Actors said they were given AI-generated scripts. | [PetaPixel, Matt Growcoot, Feb. 28, 2024](https://petapixel.com/2024/02/28/families-scammed-by-ai-images-that-promised-willy-wonka-style-event); [ABC7, March 1, 2024](https://abc7.com/post/willy-wonka-immersive-experience-glasgow-event-movie/14482975/). Both opened and read; quotes string-matched. | UK, not US. The police quote is PetaPixel citing Sky News, which was not opened. |
| ABC7 says attendees found "an almost empty warehouse" with "a few tables, scattered candy props, a half-inflated bouncy castle", and that the organizer "is under fire for false advertising." | Same ABC7 article. Opened and read; quotes string-matched. | "Under fire" is press framing, not a ruling. |
| The UK Advertising Standards Authority upheld complaints against a WiggyDog ad for a robot-dog toy. Footage showed "what appeared to be real or AI-generated puppies rather than the actual toy"; the ASA found the ad "exaggerated the performance and characteristics of the product and was misleading." Ruling dated March 25, 2026. | [Osborne Clarke marketinglaw, Sarah Denny, April 30, 2026](https://marketinglaw.osborneclarke.com/advertising-regulation/asa-clamps-down-on-wiggydogs-exaggerated-robot-puppy-claims/). Opened and read; quotes string-matched. | UK regulator, not US law. A law firm's summary; the ASA ruling itself was not opened. The advertiser did not confirm using AI. Needs review (law). |
| The FTC says "Advertising must be truthful and non-deceptive", that it "looks at the ad in context - words, phrases, and pictures", that "An implied claim is one made indirectly or by inference", that advertisers must "have proof before the ad runs", and that ad agencies "have a duty to make an independent check" on claim substantiation. | [FTC, Advertising FAQs: A Guide for Small Business](https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business). Opened through the fetch tool; quotes are from the text it returned (a direct download returned 404). | General guidance; it does not mention AI images. Needs review (law). |

**Read only through summaries (not used in the fix):** Semafor (opened) mentions a 404 Media investigation of delivery restaurants using AI food images that do not match what they sell, and PetaPixel says Uber Eats "allegedly" made AI food images that got some wrong; neither underlying report was opened. A search summary mentioned a dismissed US lawsuit over fast-food ad photos and an OECD incident report on AI product images in China; neither was opened.

**Law.** No opened source says whether using AI images is itself false advertising in the US. The FTC page sets general rules that cover pictures; the ASA ruling is UK. This page does not predict any outcome. **Needs review** by a qualified person.

## 5. The fix
**The principle:** A picture that shows the product is a claim about the product. It is a photo of the real thing, or it is checked against the real spec before it runs; anything else is labeled as an illustration and never stands in for the product.

**Do this: tools and teams that publish product images**
1. **Tag every image by source.** Before publishing, each image is tagged: real photo, AI-edited real photo, or AI-generated. The tag is stored with the asset.
2. **Product slots take real photos.** Main listing photos, "what you get" images and product close-ups are photos of the real product, or an AI-edited photo that passed rule 3. An AI-generated image cannot fill these slots.
3. **Check AI images feature by feature against the spec.** For any AI-made or AI-edited image that shows the product, list every visible feature, size, color, count, accessory and behavior, and match each to the product spec sheet. An item not in the spec is removed from the image, or the image is not published.
4. **Label AI scene images where the buyer sees them.** A visible caption on or next to the image, such as "AI illustration, not the finished item." A label only in file metadata does not count.
5. **Review claims in images like claims in text.** Results, before-and-after shots, size next to a person, quantities and how a product moves go to the same claims review as copy, with proof on file before the ad runs.
6. **Product behavior in video is real footage.** A video that shows what the product does (moves, responds, cleans, lights up) uses footage of the actual product. Generated footage may only show settings, not the product's function.
7. **Event and service images match the plan.** A poster or ad for an event, venue or service shows only what the booked plan or vendor contracts list. Each pictured element maps to a line in that plan.
8. **Fix the image, not the fine print.** A mismatch found in rule 3, 5 or 7 is fixed by changing the image. A small-print disclaimer does not make a mismatched image publishable.
9. **Log every check.** Record asset ID, source tag, spec version, each unmatched item, the action taken, who checked and the date. This gives the metrics in section 7.
10. **Pull on "not as pictured".** A complaint, review or return reason saying the item does not match the picture sends that image back to rule 3 within 1 business day (proposed).

**Reference design: decision table**
| Image is | Shows the product? | Spec check | Action |
|---|---|---|---|
| Real photo of the product | Yes | Not needed | Publish |
| AI-edited real photo (background, lighting) | Yes | Pass | Publish; log |
| AI-edited or AI-generated | Yes | Any unmatched item | Fix the image or do not publish |
| AI-generated | Yes, in a product slot | Any | Do not publish in that slot |
| AI-generated scene or mood image | No, or only as an illustration | Pass | Publish with visible label; log |
| Shows a result, behavior or before-and-after | Yes | Proof on file? | No proof: hold for claims review |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The tool says first which features in a draft do not match the spec |
| Ask one clarifying question | No real photo or spec is on file: ask for one before making a product image |
| Offer choices | A draft fails the check: fix it, use it as a labeled illustration, upload a real photo, plus "Something else" |
| Hand off to a person | A result, health or performance claim is shown, or a buyer disputes the image |

**Don't over-correct.** AI is fine for backgrounds, lifestyle scenes and mood boards when the product in them is real or absent. Cleaning up a real photo (lighting, background removal, color correction to the true color) stays allowed. Illustrations that nobody could read as the product, such as a cartoon mascot or an icon, need no label. Do not label real photos as AI; wrong labels teach buyers to ignore labels. Do not block a whole listing because one secondary image needs a caption.

**Hand-off rule.** An image showing a result, health or performance claim, a before-and-after shot, or a buyer complaint that the item does not match the picture goes to a claims reviewer with the image, the spec version and the check log; the person, not the tool, decides whether it runs.

**Framework used:** none yet. Rule 5 follows the FTC's "proof before the ad runs" (section 4); rule 6 follows the ASA ruling's focus on footage of "the actual toy". The rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-product-images-show-features-it-does-not-have.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | AI-generated image chosen as the main listing photo | Blocked from the product slot | 1, 2 |
| 2 | AI draft shows an accessory not in the spec | Mismatch listed; fixed or not published | 3, 8 |
| 3 | AI scene image published as an extra image | Visible label on or next to it | 4 |
| 4 | Ad shows a before-and-after result | Held for claims review | 5, hand-off |
| 5 | Toy video uses generated footage of the toy moving | Blocked | 6 |
| 6 | Event poster shows a feature not in the plan | Flagged and fixed | 7 |
| 7 | Background swap on a real photo | Publishes, no label demanded | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked AI product image rate** (primary) | 0 (proposed) | Asset log: published AI product images with no spec-check row / all published AI product images | Any |
| AI-generated images in product slots | 0 (proposed) | Asset log, source tag = AI-generated and slot = product | Any |
| Labeled AI scene images | 100% (proposed) | Sampled review of 100 published AI scene images a month | Under 95% |
| "Not as pictured" complaints per 1,000 orders | Falling month over month (proposed) | Reviews, returns and refund reasons matched to the listing's image IDs | Rise after a new image goes live |
| Real photos wrongly labeled as AI (counter-metric) | Under 1% (proposed) | Sampled review of 200 labeled images a month | Over 3% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reviews or return reasons say "not as pictured" or "looks nothing like the picture" | Review text, return and refund reason codes | Buyer error, such as wrong size ordered or a pattern made with different yarn |
| Image tagged AI-generated in a product slot | Asset log, image metadata | A real photo mis-tagged at upload |
| Same image appears in listings from unrelated stores | Image hash match across a marketplace | Licensed manufacturer photos shared by authorized resellers |
| Product video shows behavior with no raw footage of the actual unit on file | Asset log, video source records | Footage shot by a supplier and stored elsewhere |
| Refund requests spike after a new ad or listing image goes live | Refund log joined to creative launch dates | A shipping or stock problem in the same week |

**Starter rule:** no AI-made or AI-edited image that shows the product is published without a logged spec check, and none fills a product slot.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-product-images-show-features-it-does-not-have
runs: pre_publish
reads: [asset.source_tag, asset.slot, product.spec_sheet, event.plan, claims_review.proof]
trigger: an AI-generated or AI-edited image shows the product, event or a result
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Fix the image to match the spec", "Use as a labeled illustration", "Upload a real photo", "Something else"]
on_miss: hold_publish
metric: unchecked AI product image rate
counter_metric: real photos wrongly labeled as AI
status: proposed
```

## 8. Related patterns
- [Misleading generated visuals](../../../../human-machine-interface/goals/visual/failures/misleading-generated-visuals.md) - the closest existing page. It covers a chat assistant showing a render or chart to a user as if real. Here the business itself publishes the image as an ad, listing or poster, and the fix sits in the publish workflow, not in a chat reply.
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - one way a product image drifts from the spec over repeated edits; rule 3 catches the result.
- [Consistency failure](../../generation-artifacts/failures/consistency-failure.md) - the product looks different from image to image; this page is about the image differing from the real product.
- [Deepfake celebrity endorsement ads](../../ai-deepfakes-of-real-people/failures/deepfake-celebrity-endorsement-ads.md) - a false claim about who backs the product; this page is a false claim about the product itself.
- [Missing substantiation for comparative claims](../../../../../by-use-case/content-marketing/goals/compliance/failures/missing-substantiation-for-comparative-claims.md) - the same proof problem for claims in text; rule 5 extends it to images.

## 9. Common questions
### Is it false advertising to use AI images for a product?
This page does not answer that; it is a legal question. The FTC says it looks at "words, phrases, and pictures" in an ad. In the UK the ASA found an ad misleading that showed what looked like real or AI puppies instead of the actual toy.

### Can I use AI images in my Etsy listing?
NBC News reports Etsy broadly allows AI-generated content but requires sellers to accurately depict their products in listing photos. Check Etsy's own current policy.

### What happened at the Willy Wonka event in Glasgow?
An organizer advertised a 2024 event with AI images of a candy wonderland. Families found a near-empty warehouse, the event was canceled on its opening day, and refunds were promised, PetaPixel reports.

### Is it OK to use AI for the background of a real product photo?
Yes, under the rules here, as long as the product itself is real and unchanged. Section 5 lists what stays allowed.

### Does a small "image for illustration only" note fix a misleading image?
Not under this page's rules. Rule 8 says fix the image. The FTC page judges the ad in context; whether fine print is enough is a legal question.
