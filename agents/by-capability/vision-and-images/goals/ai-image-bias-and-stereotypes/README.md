# Bias and Stereotypes in AI Image Generators

<!-- SEO
title: Bias and Stereotypes in AI Image Generators: Failures and Fixes
description: How AI images show people, history and places wrongly, from stereotyped defaults for jobs to over-corrected history, with workflow rules that stop it.
-->

**AI image tools fill gaps in a prompt with their most common picture, so a request for "a nurse" or "a CEO" can return the same stereotyped person every time.** Each page below names one way this happens, the research behind it, and the rule inside the workflow that stops it, with a test file you can run.

> **Read this first:** Every page in this goal is **Needs review**. Statements about discrimination law and fairness summarize the cited papers and reports. None of this is legal advice, and it needs review by a qualified person before anyone relies on it.

**Goal:** AI images and video show people, history and real places accurately: no stereotyped defaults when the request names no detail, no historical errors from a diversity rule applied without context, and no wrong maps presented as real.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [AI image generator stereotyped defaults for jobs and people](failures/ai-image-generator-stereotyped-defaults-for-jobs-and-people.md) | Image | A prompt that names a role but no person returns one gender, age and look, often more lopsided than the real workforce; generate a set, review who appears, write any choice into the prompt openly and get sign-off | [Tests](../../tests/ai-image-generator-stereotyped-defaults-for-jobs-and-people.md) |
| [Historically wrong images from a context-blind diversity rule](failures/ai-image-generator-historically-inaccurate-diverse-images.md) | Both | A range-of-people rule fires on prompts that name a time, place or real group (Gemini, Feb 2024); keep the stated context, show the rewrite, test with history prompts | [Tests](../../tests/ai-image-generator-historically-inaccurate-diverse-images.md) |
| [AI maps with wrong labels presented as accurate](failures/ai-generated-maps-with-wrong-labels-presented-as-accurate.md) | Image | AI-drawn maps of real places with invented towns or misplaced countries shown as real; build maps from data, check every label, named reviewer | [Tests](../../tests/ai-generated-maps-with-wrong-labels-presented-as-accurate.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Related
- [Generation artifacts](../generation-artifacts/README.md): the older goal on image generation failures
- [Business risks of AI image and video generation](../ai-image-generation-business-risks/README.md): what the published image claims and how it is approved, including [AI images with cultural and religious errors](../ai-image-generation-business-risks/failures/ai-images-with-cultural-and-religious-errors.md)
- [Vision and images goals](../README.md)
