# AI-Generated Images in Chatbots Misleading Users: Misleading Generated Visuals

<!-- SEO
title: AI-Generated Images in Chatbots That Mislead Users
description: A chatbot shows an AI render, diagram or chart as if it were the real product or the real data. Rules to label it, keep it faithful, and show the real thing.
search phrases:
- chatbot shows AI generated product image as real
- AI generated product images misleading customers
- chatbot diagram wrong labels
- AI generated infographic wrong numbers
- how to label AI generated images in a chatbot
- AI generated image looks like real photo chatbot
- generative UI chart doesn't match data
- C2PA content credentials chatbot images
-->

**Frequency**: Occasional

## Issue: A chat assistant shows an AI-generated render, diagram or chart that looks like the real product, photo or data, and the user acts on it as if it were real.

> **One line:** The bot shows a picture or chart it generated, with no label and no check against the source, so the user believes it is the actual item or result; the fix is to label every generated visual, build charts and diagrams from the source data, and never use a render where the real photo or data is needed.

> **Read this first (flag L).** This page is design guidance, not legal advice. Review it with counsel before use. It states advertising or labeling rules only as far as a source I opened (see section 4); I opened no statute and no EU, state or country AI-labeling text. Whether a given picture is a misleading claim depends on its context and on your jurisdiction.

| | |
|---|---|
| **Channel** | Written for **chat** (images, charts and diagrams in a chat widget, rich card or generative UI). Voice and web-page variants are PLANNED, not written. |
| **Stakes** | Medium to high. A wrong product image drives a purchase; a wrong diagram or chart drives a decision. |
| **Who is affected** | Shoppers shown a render of a product, and anyone shown a chart, floor plan or how-to diagram the bot drew |
| **Frequency** | Occasional. I found no study that counts how often chat products show unlabeled generated visuals; the rating is our judgment. |
| **Pattern ID** | misleading-generated-visuals |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Share of generated visuals shown with a visible "AI-generated" label. Starting target: 100% (a starting point; tune it). Read it next to the chart-to-source mismatch count, target 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Newer image models may draw text and numbers better, but a model still cannot know which picture is the real product, and labeling is a product decision. (Our judgment, not tested.) |
| **Also searched as** | AI product image not real · chatbot made-up chart · AI diagram wrong labels · render shown as actual product · unlabeled AI image · generated infographic errors |

## 1. In plain words
Chat assistants can now draw: a product render, a "how it looks in your room" mockup, a diagram, a chart. The failure is when that picture is shown as if it were the real thing, with no label, or when its labels and numbers don't match the facts behind it. The user trusts it because it looks like a photo or a clean chart, and then buys, installs or decides on it.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Brightside Lamps" assistant)
```
User: What does the Aria floor lamp look like in brushed brass?
Bot:  Here it is in brushed brass.
      [image: photorealistic lamp, warm glow, a reading nook behind it]
User: Great, does that shade come in 18 inches?
Bot:  Yes! Order now for $129.   (the render shows a 24-inch shade; the real lamp has none in brass)
```
**With the fix**
```
User: What does the Aria floor lamp look like in brushed brass?
Bot:  Brass is not in our photo set yet. Here is the black version photographed in our studio:
      [catalog photo, labeled "Product photo: Aria, black"]
      I can also draw a preview in brass.   [Show an AI preview]  [Something else]
User: Show an AI preview.
Bot:  [image labeled "AI-generated preview, not a photo. Finish and size may differ."]
      Shade sizes come from the spec sheet: 14 or 16 inches. [See spec sheet]
```
The fixed version shows a real photo when one exists, offers a generated preview only on request, labels it where the eye lands, and takes sizes from the catalog, not from the picture.

## 3. Why it happens
- **The picture comes from a different system than the facts.** An image model draws what a lamp "looks like"; the catalog holds the real colors and sizes. Nothing checks one against the other before the picture is sent.
- **Generated images look finished.** A render, chart or diagram has no visible cue that it was made by a model, so the product has to add one. Teams often ship the image and skip the label.
- **Models imitate the look of data.** A model can draw something shaped like a chart or diagram without plotting values or labeling parts correctly (see the Risepoint row in section 4).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The FTC's small-business guide says the FTC "looks at the ad in context - words, phrases, and pictures", that an express claim "is literally made in the ad", an implied claim "is one made indirectly or by inference", and that advertisers must have "proof before the ad runs." | [FTC, Advertising FAQs: A Guide for Small Business](https://www.ftc.gov/business-guidance/resources/advertising-faqs-guide-small-business). Opened; quotes are from the page text returned by the fetch tool. | General advertising guidance. It does not mention AI images or chatbots. A chat answer is not automatically an "ad"; ask counsel. |
| Google's Merchant Center guidance, as quoted by IPTC (Feb 20, 2024): "Google requires that you preserve any metadata tags which indicate that the image was created using generative AI." "All AI-generated images must contain the IPTC DigitalSourceType trainedAlgorithmicMedia tag." | [IPTC, Google reminds publishers and merchants not to strip metadata from images](https://iptc.org/news/google-reminds-publishers-and-merchants-not-to-strip-metadata-from-images/). Opened. I could not open Google's own help page (a fetch returned 404). | Applies to Google Merchant Center product feeds, not to chat. It is a metadata tag, not a visible label. |
| The C2PA Technical Specification 2.2 (May 2025) describes "a model for storing and accessing cryptographically verifiable information", bundled in "a C2PA Manifest". It says provenance data should not make value judgments about whether it is "good" or "bad". Section 9.3.1 considers the case where a manifest "is removed from an asset". | [C2PA Specification 2.2](https://spec.c2pa.org/specifications/specifications/2.2/specs/C2PA_Specification.html). Opened first ~100,000 of ~579,000 characters only. | I read about one-sixth of the text. A manifest records origin; it does not prove an image is accurate. Removal and re-encoding behavior beyond section 9.3.1 not checked. |
| An education-sector guide says image generators are "far less consistent when asked to communicate precise information such as numbers, labels, or small text", can infer "what a chart looks like" but not "how to plot values accurately", and in labeled charts "AI names or categories are frequently wrong or repeated." | [Risepoint Faculty Center, Understanding AI's limits with text and data](https://faculty.risepoint.com/?p=1510) (Oct 1, 2025). Opened. | Single secondary source with no test data in the part read; models change fast, so retest your own model. |
| In Feb 2024 Google paused Gemini's image generation of people after users showed inaccurate historical images. Google's post says the tuning "failed to account for cases that should clearly _not_ show a range." | [Google, Gemini image generation got it wrong](https://blog.google/products/gemini/gemini-image-generation-issue/) (Feb 23, 2024); library page: [Google pauses Gemini image generation of people](../../../incidents/google-gemini-image-generation-paused-february-2024.md). Opened. | Google's own account of its cause. The case is about historical accuracy, not product renders or labeling, so it shows an image model drawing something that does not match reality, not this exact failure. |

I also saw, **read through a summary** only (not opened, kept out of the fix): OpenAI's help center page on C2PA metadata and SynthID in ChatGPT-generated images (a fetch returned 403), and a search summary saying OpenAI said in 2024 that C2PA metadata "can easily be removed" and that screenshots can drop it. Treat metadata as a helper, not a guarantee.

**How this differs from the closest pages.** [Dark patterns](dark-patterns.md) covers rigged choices and cancel flows; this page covers a picture that misstates what something looks like or says. [Cognitive overload](cognitive-overload.md) covers too much on the screen. [AI disclosure failures](../../../../speech-and-audio/goals/conversation-flow/failures/ai-disclosure-failures.md) covers how the agent answers "are you a bot?" in a conversation; this page covers whether a generated image is marked as generated. [Attribute hallucination](../../../../vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md) covers a model misdescribing an image it was shown; this page covers images the assistant produces and shows. A planned pattern for misleading charts built from real data is named in the roadmap and is not linked here.

**Public incident.** The Gemini case above is the nearest item in the library. I found no public incident of a chatbot showing an unlabeled AI render as a real product.

## 5. The fix

**The principle:** Never let a generated picture stand in for the real item or the real data: use the real photo or the source data when it exists, label anything generated where the user will see it, and build charts and diagrams from the source, not from the model's drawing.

**Do this**
1. **Real over generated.** When a catalog photo, screenshot or official diagram exists for the thing being asked about, show that. Generate only when none exists, and say so.
2. **Label every generated visual in the message.** A visible caption on or directly under the image, such as "AI-generated preview, not a photo", in the same message. A label only in file metadata does not count.
3. **Say what may differ.** The caption names the likely gap in plain words ("finish and size may differ"). A label alone is not enough where the picture could be read as the product.
4. **Facts come from the source, not the picture.** Sizes, colors, prices, specs and availability in the text come from the catalog or record. If the text and the image disagree, the source wins and the image is not sent.
5. **Charts are rendered from data.** A chart or table is drawn by code from the returned rows, with values and axis labels read from those rows, not drawn by an image model. Show the source and date next to it.
6. **Diagrams with labels get a label check.** For a generated or code-drawn diagram, every label must appear in the source material (manual, schema, spec). A label not found there is removed, or the diagram is not shown.
7. **Keep provenance metadata on, as a backup.** Write the IPTC `trainedAlgorithmicMedia` tag (and C2PA if your tool supports it) when you create or serve a generated image. Do not rely on it as the user-visible label.
8. **Never present a render as the actual item** ("Here is your order", "This is the one in stock"). Words like "your", "this unit" and "in stock" are reserved for real photos.

**Reference design: generated visual**
| Part | Content |
|---|---|
| Lead | Say what the image is: "Here is an AI preview" or "Product photo" |
| Image | Real asset if one exists; otherwise a generated one with a visible caption |
| Caption | "AI-generated, not a photo" plus the likely difference |
| Facts | Text from the catalog or source rows; link to the spec or data |
| Exit | "Something else"; real photos or a person if the user wants proof |

```
When showing an image the assistant generated, put a visible label in the same message: "AI-generated, not a photo", plus what may differ.
Use the real photo, screenshot or source data whenever one exists.
Take every size, color, price and number from the source, never from the image.
Do not call a generated image "your item", "this unit" or "in stock".
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply says first whether the image is a real photo or a generated preview, then shows it |
| Admit uncertainty and show how to check | The model cannot verify a detail in a generated image: say so and link the spec sheet or source |
| Offer choices | No real photo exists: "Show an AI preview", "Send me the spec sheet", plus "Something else", free text open |
| Hand off to a person | The user needs proof of the real item for a purchase or claim: offer a person who can send actual photos |

**Don't over-correct.** Do not bury every image under legal text or refuse all generated visuals. A caption of one short line is enough for a preview, and a decorative icon or an illustration of a concept needs no disclaimer if nobody could mistake it for the real item. Also do not label real photos as AI-generated; wrong labels teach users to ignore them.

**Hand-off rule.** When the user asks "is this real?", disputes a product against the image, or asks for proof of condition, stop generating and route to a person or to the real photos, with the caption text and product ID in the summary.

**Framework used:** none yet. Rules 2 and 7 follow the labeling and metadata points in section 4; rules 4 to 6 are our own design judgment on how to keep facts and pictures aligned.

## 6. How to test it (short version)
No test file yet. The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask for a product variant that has no photo | The bot shows the nearest real photo, or offers a generated preview and waits | 1 |
| 2 | Request a generated preview | A visible caption in the message says AI-generated and names what may differ | 2, 3 |
| 3 | Ask for a size or price after a preview | The answer matches the catalog row, not the image | 4 |
| 4 | Ask for a chart of last quarter's orders | The chart is drawn from the returned rows; every value matches them | 5 |
| 5 | Ask for a "how to wire this" diagram | Every label is found in the manual; a label not found is removed | 6 |
| 6 | Download or serve a generated image | The file carries the `trainedAlgorithmicMedia` tag | 7 |
| 7 | Ask "is this your real photo?" after a render | The bot says it is a generated preview and offers real photos or a person | 8, hand-off |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Generated visuals shown with a visible label** (primary) | 100% (starting point) | Log each image render with `image.source` (real, generated) and `caption` text; count generated images whose caption matches the label template | Below 99% |
| Chart-to-source mismatches | 0 | Replay sampled charts against the rows that produced them; compare every plotted value and label | Any |
| Generated images where text and image disagree on a fact | 0 in sampled review | Sample generated images with a product or spec in the same turn; a reviewer checks the facts against the record | Any |
| Generated images with provenance tag present | 100% | Inspect stored and served files for the IPTC tag after your compression step | Below 100% |
| "Is this real?" or return-reason "not as pictured" after a generated image (counter-metric) | Track; set from your baseline | Count user turns matching those intents, and returns coded "not as shown", per generated image | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat** text and image events only; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| An outgoing image has `source = generated` and no caption matching the label template (rule 2) | `message.image.source`, `message.image.caption` | A decorative icon flagged `decorative = true` |
| Bot text uses "your", "this unit" or "in stock" in the same message as a generated image (rule 8) | Text match next to `image.source = generated` | The real photo is attached too and the generated one is labeled |
| A number or label in a chart's spec has no matching row (rule 5) | Compare `chart.values` to `tool.result.rows` | A computed field (average, total) that is not a row |
| User asks "is this real?" or "what does it really look like?" within 2 turns of an image (rules 1, 3) | Intent match on the next user turns | The user asking about a different aspect, such as size |
| A product-fact sentence changes after the image is generated (rule 4) | Text and image generated in the same turn disagree on a spec field | A deliberate correction that cites the source |

**Starter rule:** every image the assistant generates carries a visible "AI-generated" caption in the same message, and facts in the reply come from the source, not from the picture.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: misleading-generated-visuals
runs: pre_send
reads: [message.image.source, message.image.caption, message.text, catalog.record, tool.result.rows, chart.values]
trigger: a reply is about to include an image, chart or diagram the assistant generated
moves: [lead_with_answer, admit_uncertainty_show_how_to_check, offer_choices, hand_off]
choices: ["Show an AI preview", "Send me the spec sheet", "Something else"]
on_miss: rewrite
metric: generated visuals shown with a visible label
counter_metric: "is this real" and not-as-pictured rate after a generated image
status: proposed
```

## 8. Related patterns
- [Dark patterns](dark-patterns.md): rigged choices and cancel flows; this page is about a picture that misstates the item or data.
- [Cognitive overload](cognitive-overload.md): too much on the screen; this page is about what is on it being untrue.
- [No clear primary action](no-clear-primary-action.md): unranked buttons beside the image.
- [AI disclosure failures](../../../../speech-and-audio/goals/conversation-flow/failures/ai-disclosure-failures.md): the agent's answer to "are you a bot?"; this page is about labeling generated images.
- [Attribute hallucination (vision)](../../../../vision-and-images/goals/visual-hallucination/failures/attribute-hallucination.md): a model misdescribes an image it received.
- [Google pauses Gemini image generation of people](../../../incidents/google-gemini-image-generation-paused-february-2024.md): an image model drawing what does not match reality.

## 9. Common questions
### Do I have to label AI-generated images in my chatbot?
I did not open a law that settles this for chat, so I can't say what applies to you; ask counsel. The sources I opened show two things: the FTC judges an ad by its words and pictures together, and Google requires an AI-origin metadata tag on images in Merchant Center feeds. Rule 2 asks for a visible label anyway, as a design choice.

### Is C2PA or a metadata tag enough as the label?
No. A metadata tag is invisible to most users, and the C2PA spec itself discusses manifests being removed from an asset. Use metadata as a backup (rule 7) and a caption as the label (rule 2).

### Can a chatbot show a generated chart or diagram?
Yes, if it is drawn from data or source material and checked. Rule 5 says to render charts from rows with code; rule 6 says every diagram label must be found in the source. A secondary source says image generators often get chart labels and numbers wrong, so retest on your own model.

### When is a generated image fine without a warning?
When no one could mistake it for the real item: a decorative header or a concept illustration. A product preview, a floor plan or a "what it looks like on you" image needs a label (rules 2 and 3). The test is whether the user would act on it as fact.

### What if my users want to see the real item?
Show real photos first (rule 1), and when none exist, say so and offer a person who can get them (hand-off rule). A preview offered as "AI preview, not a photo" is honest; a render offered as "here it is" is not.
