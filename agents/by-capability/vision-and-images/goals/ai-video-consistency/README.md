# AI Video and Character Consistency Failures

<!-- SEO
title: AI Video and Character Consistency Failures and Fixes
description: How AI video drops, adds or changes people and objects between frames, and the frame-by-frame checks inside the workflow that catch it before publish.
-->

**AI video tools often make clips where every frame looks real but the frames disagree: an object pops in, a prop vanishes, a truck gains wheels between shots.** Each page below names one way this happens, the evidence behind it, and the check inside the workflow that stops it, with a test file you can run.

**Goal:** AI video and image sets keep the same people, objects and look from frame to frame and image to image.

Faces, clothes and characters changing between frames or across a set of images are covered by the older page [Consistency Failure](../generation-artifacts/failures/consistency-failure.md) (a merge proposal for a person is pending).

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [AI video objects appear, vanish or change between frames](failures/ai-video-objects-appear-vanish-or-change-between-frames.md) | Video | A third cup appears mid-clip or a prop is gone after an arm passes it; write a continuity list before generating, check every shot frame by frame against it, and have a named person sign off | [Tests](../../tests/ai-video-objects-appear-vanish-or-change-between-frames.md) |
| [AI video flickering between frames](failures/ai-video-flicker-between-frames.md) | Video | A product clip looks perfect as a still but the label and wood grain shimmer in playback; review the clip at normal speed, name the flicker type, never ship per-frame image edits as video, and repair within a set retry budget | [Tests](../../tests/ai-video-flicker-between-frames.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Related
- [Generation artifacts](../generation-artifacts/README.md): the older goal on generation failures, including [artifact accumulation](../generation-artifacts/failures/artifact-accumulation.md) and [quality drift](../generation-artifacts/failures/quality-drift.md)
- [AI brand guidelines](../ai-image-brand-guidelines/README.md): the brand's own product changing across a campaign's images and shots
- [Business risks of AI image and video generation](../ai-image-generation-business-risks/README.md): what happens when a flawed AI video is published
- [Vision and images goals](../README.md)
