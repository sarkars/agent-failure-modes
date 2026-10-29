# Getty Images v. Stability AI: Training-Data and Watermark Lawsuits in the US and UK, Filed 2023

<!-- SEO
title: Getty Images v. Stability AI, 2023-2025: Lawsuits, Watermarks, UK Ruling
description: Getty sued Stability AI in the UK and US in 2023 over training on its photos and Getty watermarks in Stable Diffusion output. Sourced dates, claims and rulings.
search phrases:
- getty images v stability ai
- getty images lawsuit stable diffusion
- stable diffusion getty watermark lawsuit
- getty stability ai uk high court judgment 2025
- getty stability ai delaware complaint 12 million
-->

**This page is a dated teardown of one public dispute over an image model's training data and output, for builders of image generators and for teams that pick an image vendor.** The rights holder was Getty Images, a stock photo company. The product was Stable Diffusion, made by Stability AI, and its paid interface DreamStudio. The moment was output that showed a warped Getty Images or iStock watermark on an image Getty never made. **US and UK cases.**

**Status: Needs review.** Built from sources opened on 2026-10-29. Read in full as text: Getty's original US complaint (D. Del., filed Feb. 3, 2023) and the UK High Court judgment ([2025] EWHC 2863 (Ch), Nov. 4, 2025). Read through a fetch tool's extract: Getty's newsroom statement (Jan. 17, 2023), SiliconANGLE (Feb. 6, 2023), Bloomberg Law (Aug. 15, 2025) and Reuters via Yahoo (Nov. 4, 2025). We did not open the amended US complaints, the new California complaint, any US court order, or any Stability AI statement. Every statement below about law, claims or rulings is **Needs review** by a qualified person and is not legal advice.

The file name says 2023 because both suits were filed that year. The UK judgment came in November 2025; the US case moved to California in August 2025.

## What happened (as reported)

**The UK case.**
- **Filing.** Getty's newsroom statement of Jan. 17, 2023 says it began proceedings in the High Court of Justice in London. It says Stability "unlawfully copied and processed millions of images protected by copyright."
- **The judgment.** Mrs Justice Joanna Smith handed down judgment on Nov. 4, 2025, after hearings in June 2025 (case IL-2023-000007). The claimants were six Getty and iStock entities; the defendant was Stability AI Limited.
- **Claims dropped before judgment.** The judgment (para. 9) says Getty accepted there was "no evidence" that training took place in the UK, so the training claim was abandoned. The prompts behind its examples of copied output had been blocked by Stability, so the outputs claim was abandoned too. The database right claim fell with them. **Needs review (law).**
- **Watermark examples the court used.** The "Spaceships Image" came from model v1.2 with a "vector art" prompt in Getty's own experiments. The "Dreaming Image" came from a real user whose prompt included "vector art"; the model is not known. The "First Japanese Temple Garden Image" came from a real user of v2.1 with the prompt "japanese temple garden with blooming sakura and kami."
- **Trade marks.** Getty won under sections 10(1) and 10(2) for iStock watermarks from v1.x accessed through DreamStudio or the Developer Platform, based on the Dreaming and Spaceships images. It won under section 10(2) for a Getty Images watermark from v2.x, based on the Temple Garden image. It lost the Getty Images mark under 10(1) and the whole 10(3) claim. The court found no evidence of a single UK user generating either watermark with SD XL or v1.6. **Needs review (law).**
- **Scope of the win.** The judge called her trade mark findings "both historic and extremely limited in scope." She said it is "impossible to know how many (or even on what scale)" such watermarks were made in real life.
- **Copyright.** The secondary infringement claim was dismissed. The judgment says a model that "does not store or reproduce any Copyright Works (and has never done so)" is not an "infringing copy." **Needs review (law).**
- **Other points.** The judge declined to address passing off. She made no finding on how many Getty works were used in training. She found additional damages not justified. Other matters go to a later hearing.

**The US case.**
- **Filing.** The complaint against Stability AI, Inc. was filed in the US District Court for the District of Delaware on Feb. 3, 2023 (Case 1:23-cv-00135). SiliconANGLE reported it on Feb. 6, 2023.
- **The training allegation.** The complaint alleges Stability copied "more than 12 million photographs" with captions and metadata, without permission or payment. It says Getty found over 12 million links to its images in the LAION datasets used for training.
- **The watermark allegation.** Paragraph 11: output "often" contains "a modified version of a Getty Images watermark," which it says falsely implies a link to Getty. It says some output ranges "from the bizarre to the grotesque." Paragraph 52 shows a watermarked Getty original next to a Stable Diffusion output with a modified watermark. Paragraph 60 says Stability "has not modified its model to prevent that from happening."
- **Eight claims.** Copyright infringement; false copyright management information; removal or alteration of copyright management information; Lanham Act trademark infringement, unfair competition and dilution; Delaware deceptive trade practices; and Delaware trademark dilution. **Needs review (law).**
- **Relief asked.** Among other things, an injunction, damages and profits, statutory damages, and "the destruction of all versions of Stable Diffusion trained using Getty Images' content without permission." The complaint names no dollar total.
- **Move to California.** Bloomberg Law (Aug. 15, 2025) reports Getty voluntarily dismissed the Delaware case and the same day filed a new suit in the Northern District of California. It says Getty cited Stability's own Delaware arguments for a transfer there.

## What each party said

- **Getty, after the UK ruling.** Reuters quotes Getty: the ruling shows "Stable Diffusion's inclusion of Getty Images' trademarks in AI-generated outputs infringed those trademarks." Getty said it would use the ruling in its "parallel lawsuit against Stability AI in the U.S."
- **Stability AI.** No source we opened carries a Stability AI statement. A search summary attributes a comment to its general counsel; we did not open that source.

## Timeline

| Date | Event | Source |
|---|---|---|
| Jan. 17, 2023 | Getty announces UK proceedings in the High Court in London. | Getty newsroom statement |
| Feb. 3, 2023 | Getty files the US complaint in Delaware. | Complaint header and signature block |
| Feb. 6, 2023 | SiliconANGLE reports the Delaware suit. | SiliconANGLE |
| June 2025 | UK trial: hearings on 9-12, 17-20, 25-27 and 30 June. | UK judgment |
| Thurs., Aug. 14, 2025 | Getty dismisses in Delaware and refiles in N.D. Cal. Bloomberg Law says "Thursday"; the date is our reading of its Aug. 15 (UTC) dateline. | Bloomberg Law |
| Nov. 4, 2025 | UK judgment handed down. Reuters reports it the same day. | UK judgment; Reuters via Yahoo |

## Where the sources disagree or are silent

| Topic | What the sources say |
|---|---|
| Date of the UK judgment | The judgment says Nov. 4, 2025. A search summary said one outlet gives Nov. 5; we did not open it. |
| How often watermarks appeared | The US complaint says "often" and "frequently." The UK judge said scale is "impossible to know" and found no UK evidence for SD XL or v1.6. |
| Number of works used in training | The US complaint alleges more than 12 million. The UK judge made no finding on the number. |
| US case outcome | No source we opened reports any ruling in the US case. Status after August 2025 is unknown to us. |

## Pattern IDs

Pattern IDs below are the ones in the linked pages' header tables.

- [AI images that copy training images and show stock-photo watermarks](../goals/ai-image-copyright-and-trademark/failures/ai-images-copy-training-images-and-watermarks.md) (`ai-images-copy-training-images-and-watermarks`). **Good fit; this case is one of that page's sources.** Real user prompts with no brand in them returned images with a Getty or iStock watermark.
- [AI image training without permission lawsuits](../goals/ai-image-copyright-and-trademark/failures/ai-image-training-without-permission-lawsuits.md) (`ai-image-training-without-permission-lawsuits`). **Good fit for the US case.** The complaint is about scraping millions of photos without a license. In the UK the training claim was abandoned for lack of a UK link, so the UK case does not test it.
- [AI image generator puts brand logos in images](../goals/ai-image-copyright-and-trademark/failures/ai-image-generator-puts-brand-logos-in-images.md) (`ai-image-generator-puts-brand-logos-in-images`). **Partial fit.** A watermark is a trademark appearing in output nobody asked for; the UK trade mark findings rest on that. Partial because that page covers logos in general, not stock watermarks.
- **Considered, not a fit.** [AI image vendor indemnity gaps](../goals/ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md) (`ai-image-vendor-indemnity-gaps`): no opened source mentions a Stability customer facing a claim or seeking indemnity.

## Where in the flow it broke

Based on the opened sources, and only as far as they go. Each step is a place a check could have caught it.

1. **Watermarked stock photos went into training data.** The complaint alleges over 12 million Getty links in the LAION datasets. No opened source says any filter removed watermarked images.
2. **The model learned the watermark.** Plain prompts such as a Japanese temple garden returned a Getty Images watermark (UK judgment).
3. **No output check caught it.** The images reached users through DreamStudio and the Developer Platform; no source mentions a watermark detector on output.
4. **The fix came after the lawsuit.** The UK judgment says Stability blocked the prompts behind Getty's copied-output examples. No opened source says when or how.

## What a builder should take from it

Our proposals, drawn from the linked pattern pages. Status: Not yet run. These are product checks, not legal advice.

1. **Scan output for stock watermarks before delivery.** Pass: an image showing a Getty Images or iStock style banner is held, and the user gets a new image. Fail: it is delivered.
2. **Test plain prompts, not just brand prompts.** Pass: a release test set includes prompts with no brand words, such as "vector art," and logs any watermark rate per model version. Fail: only prompts naming a brand are tested.
3. **Track data provenance per model version.** Pass: the vendor can say which datasets trained v1.x, v2.x and SD XL, and whether watermarked images were removed. Fail: no record exists.
4. **Block a reported prompt and its near variants.** Pass: when a rights holder reports a prompt that returns its image, the block covers rewordings. Fail: only the exact string is blocked.
5. **Don't over-correct.** A user's own photo with their own watermark, or a prompt asking for a blank stock-style layout, should go through.

## What we could not verify

- The images themselves in the complaint and the judgment; our PDF text extraction dropped them. Descriptions here come from the text around each image.
- The amended Delaware complaints, any Delaware ruling, the Northern District of California complaint, its case number, and its status after August 2025.
- Any Stability AI statement on either case.
- From search summaries only, kept out of the facts: a $1.8 trillion damages estimate (PetaPixel returned HTTP 403), a Stability general counsel quote, a Nov. 5 date for the UK judgment, an earlier UK summary judgment ruling, and a researcher's Getty sample count.
- **Needs review:** what the UK findings mean under UK trade mark and copyright law, whether they bind or guide any US court, and how any appeal stands. No opened source reports an appeal.

## Sources

| URL | Author / publisher | Date | Opened |
|---|---|---|---|
| https://storage.courtlistener.com/recap/gov.uscourts.ded.81407/gov.uscourts.ded.81407.1.0.pdf | Getty Images complaint, D. Del. 1:23-cv-00135 | 2023-02-03 | Yes, downloaded 2026-10-29, read as text, quotes string-matched |
| https://www.judiciary.uk/wp-content/uploads/2025/11/Getty-Images-v-Stability-AI.pdf | Mrs Justice Joanna Smith, High Court, [2025] EWHC 2863 (Ch) | 2025-11-04 | Yes, downloaded 2026-10-29, read as text, quotes string-matched |
| https://newsroom.gettyimages.com/en/getty-images/getty-images-statement | Getty Images | 2023-01-17 | Yes, 2026-10-29, read through fetch tool extract |
| https://siliconangle.com/2023/02/06/getty-images-sues-stability-ai-copyright-trademark-infringement/ | Maria Deutscher, SiliconANGLE | 2023-02-06 | Yes, 2026-10-29, read through fetch tool extract |
| https://news.bloomberglaw.com/ip-law/getty-drops-stability-ai-copyright-suit-refiles-in-california | Annelise Levy, Bloomberg Law | 2025-08-15 | Yes, 2026-10-29, read through fetch tool extract; may be a paywalled excerpt |
| https://www.yahoo.com/news/articles/getty-images-largely-loses-landmark-112010375.html | Sam Tobin, Reuters (via Yahoo) | 2025-11-04 | Yes, 2026-10-29, read through fetch tool extract |
| PetaPixel, The Verge, Bird & Bird, SCL, Cleary Gottlieb, Squire Patton Boggs, CMS and others | Various | 2023-2025 | Summary only (search results); not used for any fact. The Verge and PetaPixel could not be fetched. |

## Corrections

If you have a US court order, the California case number, a Stability AI statement or news of an appeal, from a source we can open, tell us and we will fix this page.
