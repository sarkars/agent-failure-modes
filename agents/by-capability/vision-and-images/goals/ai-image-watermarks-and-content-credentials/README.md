# AI Image Watermarks, Labels and Content Credentials

<!-- SEO
title: AI Image Watermarks, Labels and Content Credentials: Failures and Fixes
description: How AI images and video lose the marks that say they are AI, from unmarked outputs to misread labels, with product rules that keep them traceable.
-->

**An AI image or video can only be traced if the product that made it marks it, the mark survives the trip, and people read the label correctly.** Each page below names one way this breaks, the sources behind it, and the rule inside the product that stops it, with a test file you can run.

> **Read this first:** Every page in this goal is **Needs review**. Labeling and marking duties are law in some places (for example EU AI Act Article 50 and California's SB 942), and statements about them summarize the cited sources as read. None of this is legal advice, and it needs review by a qualified person before anyone relies on it.

**Goal:** AI images and video carry provenance signals that reach the people and platforms who see them: a mark on every output, credentials that survive the trip, and labels that are read correctly.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [AI images published without an AI label, watermark or Content Credentials](failures/ai-images-published-without-ai-label-watermark-or-content-credentials.md) | Both | A product's own generator ships files with no visible label, no watermark and no C2PA manifest; mark every model and export path with a manifest plus a watermark, offer a visible label, and block releases that fail the check | [Tests](../../tests/ai-images-published-without-ai-label-watermark-or-content-credentials.md) |
| [AI image Content Credentials stripped on resize or upload](failures/ai-image-pipeline-strips-content-credentials-on-resize-or-upload.md) | Both | The generator signs the file, then your own resize, format change, CDN or upload step removes the label; list every step, set each to keep or re-sign, and test the live file | [Tests](../../tests/ai-image-pipeline-strips-content-credentials-on-resize-or-upload.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Related
- [AI slop detection](../../../human-machine-interface/goals/ai-slop-detection/README.md): the checker's side of provenance, including [watermarks only the vendor can read](../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-vendor-locked-watermarks.md) and [self-declared platform labels](../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-self-declared-labels.md)
- [Business risks of AI image and video generation](../ai-image-generation-business-risks/README.md): ad disclosure rules and internal generation records
- [Generation artifacts](../generation-artifacts/README.md): the older goal on image generation failures
- [AI governance failures](../../../../cross-cutting/governance/README.md)
- [Vision and images goals](../README.md)
