# AI Images That Ignore the Prompt

<!-- SEO
title: AI Images That Ignore the Prompt: Failures and Fixes
description: How AI images miss what the prompt asked for, from the wrong number of objects to wrong placement, with checks inside the workflow that catch it.
-->

**AI image tools often return a picture that looks right but does not match the request: the wrong number of items, things in the wrong place, colors on the wrong object or misspelled text.** Each page below names one way this happens, the research behind it, and the check inside the workflow that stops it, with a test file you can run.

**Goal:** AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [AI image generator wrong number of objects](failures/ai-image-generator-wrong-number-of-objects.md) | Image | Ask for four stools or three apples and get a different number; flag prompts where the count matters, count every image before publish, and composite exact counts when regeneration keeps missing | [Tests](../../tests/ai-image-generator-wrong-number-of-objects.md) |
| [AI image generator puts objects in the wrong position](failures/ai-image-generator-puts-objects-in-the-wrong-position.md) | Image | Ask for a lamp left of a chair or a rug under a table and get it elsewhere; check each requested placement, name the ones that failed, and fix by flip, edit or layout-first rebuild | [Tests](../../tests/ai-image-generator-puts-objects-in-the-wrong-position.md) |
| [AI image generator mixes up colors](failures/ai-image-generator-puts-colors-on-the-wrong-object.md) | Image | Ask for a navy sofa and a mustard chair and get the colors swapped; list each object with its color before generating, check each object after, and fix or say what did not match | [Tests](../../tests/ai-image-generator-puts-colors-on-the-wrong-object.md) |
| [AI image generator misspells text](failures/ai-image-generator-misspells-text-in-images.md) | Image | A menu board reading "Brisket Taco $4.50" comes out as "Brisket Tcao"; set prices, dates and names in a template instead of generating them, proof every readable word against approved copy, and have a named person check at full size | [Tests](../../tests/ai-image-generator-misspells-text-in-images.md) |
| [AI image generator ignores negative prompts](failures/ai-image-generator-ignores-negative-prompts.md) | Image | Ask for "a man without glasses" and get glasses; describe what should be there instead, put the item in the tool's exclusion field, and check every image for every excluded item before calling it done | [Tests](../../tests/ai-image-generator-ignores-negative-prompts.md) |
| [AI image edit changes parts you did not ask to change](failures/ai-image-edit-changes-parts-you-did-not-ask-to-change.md) | Image | Ask to remove one trash bin and the front door turns black too; write a keep list, compare with the original outside the edit area, name every unrequested change, and restore original pixels | [Tests](../../tests/ai-image-edit-changes-parts-you-did-not-ask-to-change.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Related
- [Generation artifacts](../generation-artifacts/README.md): the older goal on image generation failures, including [semantic drift](../generation-artifacts/failures/semantic-shift.md) and [token limit artifacts](../generation-artifacts/failures/token-limit-artifacts.md)
- [Business risks of AI image and video generation](../ai-image-generation-business-risks/README.md): what the published image claims and how it is approved
- [Vision and images goals](../README.md)
