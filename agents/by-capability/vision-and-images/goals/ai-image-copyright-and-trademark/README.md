# AI Image Copyright and Trademark Risks

<!-- SEO
title: AI Image Copyright and Trademark Risks: Failures and Fixes
description: How AI image and video tools end up copying protected characters, artworks and brands, and the product rules that keep their output clear of them.
-->

**AI image and video tools copy protected characters, artworks, logos and training images, and the businesses using them assume they own what comes out.** Each page below names one way this happens, the reports behind it, and the rule inside the product that stops it, with a test file you can run.

> **Read this first:** Every page in this goal is **Needs review**. Statements about copyright, trademark and lawsuits summarize the cited news reports, filings and papers. Lawsuits are described only as filed allegations. None of this is legal advice, and it needs review by a qualified person before anyone relies on it.

**Goal:** AI image and video tools do not reproduce protected characters, artworks, trademarks or training images, and the business using them knows what it can and cannot claim to own.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [Copyrighted characters reproduced by AI image generators](failures/ai-image-generator-reproduces-copyrighted-characters.md) | Both | A generator draws a studio's character when asked by name, or from a few generic words | [Tests](../../tests/ai-image-generator-reproduces-copyrighted-characters.md) |
| [Near-copies of training images and stock-photo watermarks](failures/ai-images-copy-training-images-and-watermarks.md) | Image | Output that closely copies a training image, or shows a stock site's watermark | [Tests](../../tests/ai-images-copy-training-images-and-watermarks.md) |
| [AI art in the style of living artists](failures/ai-art-in-the-style-of-living-artists.md) | Image | A generator copies a working artist's look when asked by name, and the art carries their name | [Tests](../../tests/ai-art-in-the-style-of-living-artists.md) |
| [Brand logos and trademarks in AI images](failures/ai-image-generator-puts-brand-logos-in-images.md) | Image | A generator puts a real brand's logo or mark into an image, and the business posts it unapproved | [Tests](../../tests/ai-image-generator-puts-brand-logos-in-images.md) |
| [Training on images without permission](failures/ai-image-training-without-permission-lawsuits.md) | Image | A team adopts or fine-tunes an image generator without checking where its training images came from | [Tests](../../tests/ai-image-training-without-permission-lawsuits.md) |
| [Who owns AI-generated images](failures/who-owns-ai-generated-images-copyright.md) | Both | A tool tells a business it owns a generated logo or cover; it registers or promises rights it may lack | [Tests](../../tests/who-owns-ai-generated-images-copyright.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Planned (not yet written)
- Vendor terms or indemnity that do not cover how the business uses the output

## Related
- [Generation artifacts](../generation-artifacts/README.md): the older goal on image generation failures, including [safety filter bypass](../generation-artifacts/failures/safety-filter-bypass.md)
- [AI deepfakes of real people](../ai-deepfakes-of-real-people/README.md): real people's faces and voices; this goal covers characters, works and brands owned by someone
- [Governance](../../../../cross-cutting/governance/goals/governance/README.md)
- [Vision and images goals](../README.md)
