# AI Images That Break Brand Guidelines

<!-- SEO
title: AI Images That Break Brand Guidelines: Failures and Fixes
description: How AI images and video go off brand, from a redrawn logo, off-palette colors and made-up fonts to a brand next to unsafe content, and rules that stop it.
-->

**AI-made images and video redraw a brand's logo, drift off its colors and fonts, or put its name next to content it would never approve.** Each page below names one way this happens, the reports behind it, and the rule inside the workflow that stops it, with a test file you can run.

> **Read this first:** Every page in this goal is **Needs review**. Statements about trademarks, brand safety and platform rules summarize the cited news reports, vendor pages and brand pages. None of this is legal advice, and it needs review by a qualified person before anyone relies on it.

**Goal:** AI images and video a brand publishes follow its brand guidelines: the right logo, colors, fonts, tone and product, nothing from another brand, and nothing unsafe next to its name.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [AI images break brand logo, color and font rules](failures/ai-images-break-brand-logo-color-and-font-rules.md) | Both | The generator redraws the brand's own logo, drifts off the palette and invents a font; generate only the scene, place the official logo file and brand-font text afterward, measure colors against the hex values and get a brand reviewer's sign-off | [Tests](../../tests/ai-images-break-brand-logo-color-and-font-rules.md) |
| [AI images put a brand next to unsafe content](failures/ai-images-shown-next-to-unsafe-content.md) | Image | Generators put a brand's logo, mascot or characters into sexual, violent or political scenes; block those prompts and check the scene before and after brand assets are added | [Tests](../../tests/ai-images-shown-next-to-unsafe-content.md) |

Another company's logo or character appearing in output is covered by [brand logos in AI images](../ai-image-copyright-and-trademark/failures/ai-image-generator-puts-brand-logos-in-images.md) in the copyright and trademark goal; this goal links to it instead of repeating it.

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Planned (not yet written)

## Related
- [Generation artifacts](../generation-artifacts/README.md): the older goal on image generation failures, including [consistency failure](../generation-artifacts/failures/consistency-failure.md)
- [Business risks of AI image and video generation](../ai-image-generation-business-risks/README.md): what the published image claims and how it is approved, including [model updates that change an approved style](../ai-image-generation-business-risks/failures/ai-image-model-update-changes-approved-style.md)
- [AI image copyright and trademark risks](../ai-image-copyright-and-trademark/README.md): who owns the output and whose marks are in it
- [Brand consistency in content marketing](../../../../by-use-case/content-marketing/goals/brand-consistency/README.md): brand voice in written content
- [Vision and images goals](../README.md)
