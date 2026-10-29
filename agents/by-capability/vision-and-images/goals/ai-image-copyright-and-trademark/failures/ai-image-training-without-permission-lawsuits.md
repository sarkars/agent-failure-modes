# Was This AI Image Generator Trained on Stolen Art? Picking or Fine-Tuning a Model Without Checking Training Data Permission

<!-- SEO
title: Was This AI Image Generator Trained on Stolen Art? Check Before You Use It
description: Businesses adopt or fine-tune image generators without asking where the training images came from. How to check provenance, avoid unlicensed fine-tuning and keep a record.
search phrases:
- was this ai image generator trained on stolen art
- is midjourney trained on copyrighted images
- which ai image generators use licensed training data
- commercially safe ai image generator
- can i fine tune stable diffusion on someone else's art
- getty images lawsuit stability ai training data
- artists lawsuit stable diffusion laion
-->

**Frequency**: Common

## Issue: Businesses adopt or fine-tune image generators without asking where the training images came from. How to check provenance, avoid unlicensed fine-tuning and keep a record.

> **Read this first:** Statements about copyright, terms of use and lawsuits on this page summarize the news reports and law-firm summaries cited here. Lawsuits are described only as filed allegations and early rulings as those sources report them; this page does not predict any outcome. It is not legal advice and needs review by a qualified person, such as a copyright lawyer, before anyone relies on it. The fix below is a product and procurement choice, not a legal conclusion.

> **One line:** A marketing team picks an image generator, or fine-tunes one on images pulled from the web, without asking where the training images came from, and later faces artist complaints, takedowns or a vendor named in a lawsuit; the fix is a training-data provenance check before any model is adopted, no fine-tuning on images the business lacks rights to, and a record of the model and data behind every published asset.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source is about still-image generators. A business choosing a video generator faces the same check, but no opened source describes a video training case. |
| **Channel** | Procurement and production: choosing a generator vendor, fine-tuning jobs, and the creative tools and asset libraries that publish the output |
| **Stakes** | High. A vendor the business relies on may be sued over its training data (section 4), and the business's own fine-tuned model may be built on work it has no right to use. |
| **Who is affected** | The artists and photographers whose work was used, the business publishing the assets, and its customers and partners who reuse them |
| **Frequency** | Common, by our reading: the opened lawsuits name widely used generators. No opened source gives a rate of businesses that skip the check. |
| **Pattern ID** | ai-image-training-without-permission-lawsuits |
| **Family** | [AI Image Copyright and Trademark Risks](../README.md) |
| **Goal** | AI image and video tools do not reproduce protected characters, artworks, trademarks or training images, and the business using them knows what it can and cannot claim to own. |
| **Primary metric** | Unverified-provenance asset rate: published generated assets whose record does not name a model with a completed training-data provenance check, divided by all published generated assets. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Where training images came from is a fact about data and permission, not model quality; a better model trained on the same data has the same gap. (Our judgment, not tested.) |
| **Also searched as** | AI trained on my art without permission · scraped training data lawsuit · licensed data image generator · fine-tune on artist images · AI training opt out |

Tests: [AI image training without permission test file](../../../tests/ai-image-training-without-permission-lawsuits.md).

## 1. In plain words
A retailer's marketing team needs 200 ad images by Friday. They pick the generator their designer likes, and to match a look, they fine-tune it on 300 images saved from an illustrator's portfolio. Nobody asks what the vendor trained on, or whether the team may use those 300 images. Months later the illustrator finds the ads and the vendor is named in a lawsuit. The team cannot say which ads came from which model.

## 2. What it looks like
The opened sources do not show a transcript. The product below is a generic in-house creative assistant; the retailer is invented.

**Without the fix**
```
User:  Fine-tune our image model on these 300 images from Dana Reyes's portfolio site
       so the fall campaign matches her look.
Tool:  Uploaded 300 images. Training started; your custom model will be ready in 2 hours.
User:  Great. Use it for all 200 Denver store ads.
Tool:  Done. 200 images saved to the campaign folder.
```
**With the fix**
```
User:  Fine-tune our image model on these 300 images from Dana Reyes's portfolio site
       so the fall campaign matches her look.
Tool:  I can't train on these: there is no license on file for them. I can:
       1) Train on images your team owns or has licensed  2) Ask Dana Reyes for a license
       3) Describe the look in words instead  4) Something else
User:  Option 2. Who handles that?
Tool:  I've sent the request to your licensing lead, Jordan Kim, with the image list.
       Until a license is on file, ads use the approved model, which has a provenance check on file.
```
In the fixed version the training job does not start, the reason is one line, the user gets working paths, and the hand-off goes to a named person.

## 3. Why it happens
- **The question is not on the buying checklist.** Teams compare image quality and price. Where the training images came from is not on the form, so no one asks. (Our reading.)
- **Scraped datasets hide their sources.** The artists' lawsuit alleges Stable Diffusion was trained on images "scraped from the internet" in the LAION-5B dataset (VICE). A business using a model built this way inherits a question it cannot answer from the tool itself.
- **Fine-tuning feels like a private step.** Uploading a folder of saved images takes minutes, and the tool does not ask about rights. The business becomes the party that chose the training data. (Our reading.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Getty Images sued Stability AI in the US District Court for the District of Delaware, alleging Stability copied at least 12 million of its images with captions and metadata "without permission" to train Stable Diffusion, without a license, even though Getty's terms of use ban "unauthorized reproduction" for commercial purposes. Getty had filed a similar suit in the UK in January 2023. | [AI Business, Ben Wodecki, Feb. 8, 2023](https://aibusiness.com/nlp/getty-sues-stable-diffusion-parent-in-the-u-s-). Opened via curl; text extracted and read. | Allegations as one outlet reports them. The [sibling page](ai-images-copy-training-images-and-watermarks.md) covers the case's later status. Needs review (law). |
| Artists Sarah Andersen, Kelly McKernan and Karla Ortiz filed a class action against Stability AI, DeviantArt and Midjourney. It claims the tools were trained on "billions of copyrighted images scraped from the internet" in LAION-5B, used "without compensation or consent from the artists." A Stability AI spokesperson said anyone who believes this isn't fair use "does not understand the technology and misunderstands the law." | [VICE, Chloe Xiang, Jan. 17, 2023](https://vice.com/en/article/artists-are-suing-over-stable-diffusion-stealing-their-work-for-ai-art). Opened and read; quotes string-matched. | Claims in a filing. The article gives no court or filing date. Needs review (law). |
| In Andersen v. Stability AI (N.D. Cal.), the court granted in part and denied in part motions to dismiss claims that the defendants infringed by including the artists' works "in data used to train" their AI product. Induced infringement claims against Stability and Runway survived; two DMCA claims against Stability were dismissed. | [Loeb & Loeb, Aug. 12, 2024](https://www.loeb.com/en/insights/publications/2024/08/andersen-v-stability). Opened and read; quotes string-matched. | A ruling on whether allegations are enough to proceed, not a finding of infringement. Needs review (law). |
| Disney, Universal and related companies sued Midjourney in the Central District of California. The complaint alleges Midjourney's service "uses the plaintiffs' copyrighted works to train its model without permission." It seeks damages, an injunction and an accounting of profits. | [Law Street Media, David Nayer, June 18, 2025](https://lawstreetmedia.com/insights/disney-and-universal-sue-midjourney-for-copyright-infringement/). Opened and read; quotes string-matched. | Allegations as one outlet reports them. The article does not mention video. Needs review (law). |
| Getty launched a generator "trained only on licensed content" from its creative collection, not editorial images; contributors are paid by a formula, and Getty indemnifies customers. Axios says Adobe "has pursued a similar approach with Firefly." | [Axios, Ina Fried, Sept. 25, 2023](https://www.axios.com/2023/09/25/getty-images-ai-creation-tool). Opened via curl; quotes string-matched. | The vendor's own claims as reported; not tested. |
| Adobe says "we trained our first Firefly model on licensed images from Adobe Stock and public domain content where copyright has expired," and that it does not train on Creative Cloud subscribers' personal content. | [Adobe Firefly FAQ](https://www.adobe.com/cc-shared/fragments/products/firefly/faq). Opened through a fetch tool that returned the quotes; no date shown. | Vendor's own statement, single source. It covers the first model; we did not read what later models used. |
| Spawning said Stability AI would honor artists' opt-out requests, registered at haveibeentrained.com, for Stable Diffusion 3. Spawning's Mat Dryhurst said "we have no false confidence it will be possible to enforce things in a completist way." | [VentureBeat, Sharon Goldman, Dec. 15, 2022](https://venturebeat.com/ai/stability-ai-to-honor-artist-opt-out-requests-for-stable-diffusion-3). Opened through a fetch tool; quotes not string-matched. | A 2022 announcement. A figure of about 80 million opt-outs by March 2023 was seen only in a search summary and is not used. |

**Law.** None of the opened sources says whether training on images without permission is lawful in the US. The cases above are allegations and early rulings. This page links them and does not argue them. **Needs review** by a qualified person.

## 5. The fix
**The principle:** No model is used for published work until someone has checked and recorded where its training images came from, and no fine-tune runs on images the business lacks rights to.

**Do this: businesses that buy or fine-tune generators**
1. **Run a provenance check before adoption.** Before a model is approved, record the vendor's written answer to: what was it trained on, does it use licensed or public domain data, does it honor artist opt-outs, and does it offer indemnity. A model with no answer stays in the sandbox.
2. **Record pending lawsuits, without judging them.** Note any filed lawsuit over the vendor's training data, with its date and a link. The record states what was filed, not who is right; legal counsel decides what it means for use.
3. **Prefer licensed-data models for published work.** When two models meet the creative need, choose the one whose vendor says it was trained on licensed or public domain data, as Getty and Adobe describe.
4. **Never fine-tune on images without rights on file.** A fine-tune job starts only when every training image is owned by the business, licensed with a license ID, or public domain, and the job logs that record.
5. **Block scraped folders.** Images saved from another person's website, social feed or portfolio are not training data unless a license is on file. Decline in one line and offer choices.
6. **Record the model and data behind every asset.** Each published asset stores the model name and version, the provenance check ID, and any fine-tune dataset ID.
7. **Re-check on change.** A new model version, a new lawsuit, or a vendor terms change reopens the check within 30 days (proposed).
8. **Route complaints to a person with the record.** An artist complaint or takedown notice goes to a named owner with the asset record, so the team can find every asset from that model or dataset.

**Reference design: asset record and gate**
| Field | Example | Gate |
|---|---|---|
| model_id, version | approved-gen v3 | Must match an approved model |
| provenance_check_id | PC-2026-014 (vendor answers, date, reviewer) | Missing = not publishable |
| known_lawsuits | Links and filing dates, no conclusions | Informational; counsel decides |
| finetune_dataset_id | DS-0091 | Optional; if present, must pass rule 4 |
| dataset_rights | owned / licensed (license ID) / public domain | Any image without one = job blocked |
| published_asset_ids | campaign folder IDs | Lets a complaint find every affected asset |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | Every blocked fine-tune or unapproved model request |
| Ask one clarifying question | It is unclear whether the business owns the uploaded images |
| Admit uncertainty and show how to check | A user asks whether a vendor's model is "safe"; say what the record shows and where to read it |
| Hand off to a person | License requests, artist complaints, takedown notices, a new lawsuit against a vendor |

**Don't over-correct.** Fine-tuning on the business's own product photos, its own staff's artwork, licensed stock with license IDs, or public domain images stays allowed. Testing a model in a sandbox before the check is done stays allowed; only publishing waits. A pending lawsuit is recorded, not treated as a ban; counsel decides. Do not block a user who asks a text question about how a model was trained. Do not refuse a whole folder because one image lacks a record: list that image and let the rest proceed.

**Hand-off rule.** License requests, artist complaints, takedown notices and any new lawsuit against a vendor go to a named owner (licensing or legal) with the asset record and provenance check; the person, not the tool, decides.

**Framework used:** none yet. Rule 3 follows the licensed-data approach Getty and Adobe describe (section 4); the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-training-without-permission-lawsuits.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Publish an asset from a model with no provenance check | Blocked; sandbox use only | 1, 6 |
| 2 | Fine-tune on images saved from an artist's site | Declined with reason and options | 4, 5 |
| 3 | Fine-tune on the business's own product photos | Proceeds; rights logged | 4, Don't over-correct |
| 4 | Published asset lookup by model | Every asset has model, version, check ID | 6 |
| 5 | Vendor ships a new model version | Check reopened | 7 |
| 6 | Artist complaint about an ad | Routed to owner with the asset record | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unverified-provenance asset rate** (primary) | 0 (proposed) | Asset records: published assets with no approved model and check ID / all published generated assets | Any |
| Fine-tune jobs with any image lacking a rights record | 0 (proposed) | Fine-tune job log, dataset_rights field | Any |
| Approved models with a check older than its latest version or terms change | 0 (proposed) | Model registry dates vs check dates | Any over 30 days |
| Complaints resolved with a full asset list | 100% (proposed) | Sampled review of complaint tickets | Under 95% |
| Wrongly blocked owned or licensed fine-tunes (counter-metric) | Under 2% (proposed) | Sampled review of 100 blocked jobs a month | Over 5% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Fine-tune upload whose image sources are URLs on domains the business does not own | Upload metadata, dataset log | Licensed stock with license IDs attached |
| Published asset with no model or version in its record | Asset library export | Asset made before logging began; backfill, not a breach |
| Model in production use with no provenance check ID | Model registry vs usage log | Model used only in the sandbox |
| Artist complaint or takedown notice naming a generated asset | Support or legal ticket queue | Complaint is about an output copy or style; see the related pages |

**Starter rule:** no generated asset is published unless its record names an approved model with a provenance check on file, and no fine-tune runs on an image without a rights record.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-training-without-permission-lawsuits
runs: pre_finetune_and_pre_publish
reads: [request.text, upload.sources, dataset_rights, model_registry.provenance_checks, asset_record]
trigger: fine-tune images lack a rights record, or a publish names a model with no provenance check
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Train on images you own or license", "Request a license", "Describe the look in words", "Something else"]
on_miss: block
metric: unverified-provenance asset rate
counter_metric: wrongly blocked owned or licensed fine-tunes
status: proposed
```

## 8. Related patterns
- [AI images that copy training images and show stock-photo watermarks](ai-images-copy-training-images-and-watermarks.md) - the closest existing page. It covers the output side: a delivered image that copies one training photo. This page covers the input side: whether the model or fine-tune had permission to use the images at all. Both cite the Getty case.
- [AI art in the style of living artists](ai-art-in-the-style-of-living-artists.md) - covers naming an artist in the prompt. Fine-tuning on an artist's images, covered here, is the route that page says a prompt rule does not reach.
- [No vendor risk control](../../../../../cross-cutting/governance/goals/governance/failures/no-vendor-risk-control.md) - the general vendor risk gap; rule 1 is that check applied to training data.
- [Model collapse in generation](../../generation-artifacts/failures/model-collapse.md) - a fine-tuning quality problem on narrow data, not a permission problem; linked only.
- [AI browser agent bypasses CAPTCHAs or site terms](../../../../human-machine-interface/goals/browser-agents/failures/bypasses-captchas-or-site-terms.md) - an agent ignoring a site's rules; relevant when an agent gathers fine-tune images.

## 9. Common questions
### Was this AI image generator trained on stolen art?
Ask the vendor in writing what it trained on. Lawsuits allege some popular generators were trained on images used without permission (section 4); these are allegations, not findings.

### Which AI image generators use licensed training data?
Getty says its generator was trained only on licensed content, and Adobe says its first Firefly model used Adobe Stock and public domain images. These are vendor statements we have not tested.

### Can I fine-tune Stable Diffusion on someone else's art?
Not under this page's rules unless you have a license on file. Whether it is legal is a question for a lawyer.

### If my vendor is sued, can I still use the images?
This page does not answer that. Record the lawsuit and ask counsel; the asset record shows which images came from that model.

### Should we ban every model with a lawsuit against it?
No. Record it and let counsel decide. Section 5 lists what stays allowed.
