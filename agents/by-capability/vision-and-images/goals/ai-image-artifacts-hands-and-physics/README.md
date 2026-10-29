# AI Image Artifacts: Hands, Anatomy and Physics

<!-- SEO
title: AI Image Artifacts: Hands, Anatomy and Physics Failures
description: How AI images break bodies and physics, from six fingers and fused limbs onward, with checks inside the workflow that catch the defect before it is published.
-->

**AI image tools often return a picture that looks fine at a glance but shows something that could not exist: six fingers, an extra arm, a sleeve merged into a forearm, shadows that point to two different suns, or a can that bends like rubber in a video.** Each page below names one way this happens, the research behind it, and the check inside the workflow that stops it, with a test file you can run.

**Goal:** AI images and video show bodies, objects and motion that could exist: correct hands and anatomy, shadows and reflections that match, and physics that holds.

## Patterns

| Pattern | Covers | One line | Tests |
|---|---|---|---|
| [AI image generator wrong hands, fingers and anatomy](failures/ai-image-generator-wrong-hands-fingers-and-anatomy.md) | Image | AI images and AI photo edits give people six fingers, extra limbs or fused body parts; check every visible hand at full size, fix only the broken region and re-check every new version before a named person signs off | [Tests](../../tests/ai-image-generator-wrong-hands-fingers-and-anatomy.md) |
| [AI image generator broken shadows, reflections and impossible physics](failures/ai-image-generator-broken-shadows-reflections-and-impossible-physics.md) | Image | AI images draw shadows that point to different suns, mirrors that reflect the wrong thing and scenes that break simple physics; check photo-style images with hard light, reflections or balance using lines, not a glance, and re-check every version before a named person signs off | [Tests](../../tests/ai-image-generator-broken-shadows-reflections-and-impossible-physics.md) |
| [AI video motion breaks physics](failures/ai-video-motion-breaks-physics.md) | Video | AI video bends rigid objects, pours liquids wrong, passes objects through each other and moves things with no cause; list every interaction before generating, check each one frame by frame, use live footage for claimed product features, and have a named person sign off | [Tests](../../tests/ai-video-motion-breaks-physics.md) |

All tests are **Not yet run**. All detection signals and Guide specs are proposed.

## Related
- [Generation artifacts](../generation-artifacts/README.md): the older goal on image generation failures, including [quality drift](../generation-artifacts/failures/quality-drift.md)
- [AI images that ignore the prompt](../ai-image-prompt-adherence/README.md): images that look fine but do not match the request
- [Vision and images goals](../README.md)
