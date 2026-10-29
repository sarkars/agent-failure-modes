# AI Video Flickering Between Frames: Fine Detail, Light and Texture Jump in Every Frame

<!-- SEO
title: AI Video Flickering Between Frames: Why It Happens, How to Fix
description: AI video flickers when fine detail, light or texture changes from frame to frame. Watch each clip at normal speed, name the flicker type, then fix it.
search phrases:
- ai video flickering
- how to fix flicker in ai video
- ai generated video flicker between frames
- stable diffusion video flicker frame by frame
- ai video background shimmering
- deflicker ai video
- why does my ai video flicker
-->

**Frequency**: Common

## Issue: AI video flickers when fine detail, light or texture changes from frame to frame, and a team that approves clips from paused frames publishes a product video whose label, fabric or background shimmers. Watch every clip at normal speed, name the flicker type, and fix it with the repair that fits that type (or regenerate a smaller shot) before a named person signs off.

> **One line:** A Milwaukee candle maker's AI product clip looks perfect as a still, but in playback the jar label and wood grain shimmer every frame; the fix is to review the downloaded clip at normal speed, classify the flicker, repair or regenerate only the bad segment, check the motion the brief asked for is still there, and have a named person approve it.

Status: Needs review

| | |
|---|---|
| **Covers** | Video. Includes clips made by a text-to-video or image-to-video model and video edited or restyled one frame at a time by an image model. A set of separate still images has no frames between them; for that, see the brand page on [products that look different across a campaign](../../ai-image-brand-guidelines/failures/ai-campaign-product-looks-different-across-images.md). |
| **Channel** | Video generators, video-to-video restyle tools, and assistants or workflows that call them, used for product clips, social ads, explainer videos and website backgrounds |
| **Stakes** | Medium. A shimmering label or logo makes a product ad look broken or unreadable and can get a clip rejected after it was paid for (our judgment). |
| **Who is affected** | Viewers of the ad or video, the business whose product and brand appear, and the editor who has to redo the shot |
| **Frequency** | Common in research: VBench calls flicker in generated video "an intrinsic property of the video generation model" (section 4). No opened source gives a rate in real business use. |
| **Pattern ID** | ai-video-flicker-between-frames |
| **Family** | [AI Video and Character Consistency Failures](../README.md) |
| **Goal** | AI video and image sets keep the same people, objects and look from frame to frame and image to image. |
| **Primary metric** | Unreviewed-or-flagged flicker publish rate: published AI video clips with no recorded normal-speed review, or with an open flicker flag, divided by all published AI video clips. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is two arXiv papers, one arXiv metric proposal with no results, and one vendor blog. No public incident found. |
| **Will a better model fix this?** | Partly. VBench found that models with the best flicker scores also tended to make less motion, so a model can look stable by moving less; newer models may shrink flicker, but a playback check is still needed (our judgment, drawing on VBench). |
| **Also searched as** | AI video shimmering · AI video jitter · texture flicker in AI video · Runway flicker · deflicker AI video · AI video background flickering |

Tests: [AI video flicker between frames test file](../../../tests/ai-video-flicker-between-frames.md).

## 1. In plain words
A video is many still pictures shown fast. An AI video model, or an image model run on each frame, redraws small details a little differently in every picture. Each frame looks fine on its own. Played at speed, the label, the fabric, the leaves or the light jumps and shimmers. If the team only checks a paused frame, nobody sees it until the ad is live.

## 2. What it looks like
The company, people and files below are invented.

**Without the fix**
```
Marketer:  Make a 6-second clip from our product photo: the Cedar & Smoke jar on a walnut table, slow push-in.
Assistant: Done. Here is a preview frame. (One render, approved from the thumbnail.)
Marketer:  Looks great. Schedule it for Friday's Instagram ad.
Assistant: Scheduled.
Customer (comment, Saturday): Why is the label on the jar jumping around? Hard to read.
Marketer:  I never saw that in the preview.
```
**With the fix**
```
Marketer:  Make a 6-second clip from our product photo: the Cedar & Smoke jar on a walnut table, slow push-in.
Assistant: I watched the downloaded render at normal speed. Flicker found: 2.0-4.5 s, the label text
           and wood grain shimmer while the jar's shape stays steady (texture shimmer, not a light pulse).
           Options: regenerate a shorter 3-second push-in from a cleaner photo; keep the camera still;
           use your real product video for the label shot; something else.
Marketer:  Shorter push-in.
Assistant: New render reviewed at normal speed: label steady, push-in still visible. Sent to
           Jordan Lee (brand) to watch and approve before it is scheduled.
```
The fixed version reviews in playback, names the time range and flicker type, offers a fix that fits that type, checks that the motion asked for is still there, and ends with a person approving.

## 3. Why it happens
- **Fine detail is redrawn every frame.** VBench says flicker in generated video is "usually caused by imperfect temporal consistency at local and high-frequency details": the large shapes hold, but small texture and edges do not.
- **Image models edit each frame on their own.** TokenFlow found that applying an image editing model to each frame independently gives good single frames that "lack any temporal consistency," because nothing ties one frame's edit to the next.
- **Stability and motion pull against each other.** VBench found a trade-off: LaVie scored high on flicker but low on motion, and VideoCrafter made lots of motion but did worse on every consistency measure. A clip with a lot of movement gives the model more chances to flicker.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Flicker is "an intrinsic property of the video generation model." VBench measures it on static scenes as the mean absolute pixel difference between consecutive frames and reports it as one of 16 quality dimensions. | [Huang et al., "VBench," arXiv 2311.17982](https://arxiv.org/html/2311.17982) (Nov 2023). HTML full text opened Oct 29, 2026. | Preprint version read. Tested four 2023 open models. The metric only uses scenes with no apparent motion, so it says nothing direct about flicker in moving shots. |
| Flicker scores were LaVie 98.30%, ModelScope 98.28%, CogVideo 97.64%, VideoCrafter 97.60%, against an "Empirical Min" of 62.93%. LaVie's motion (Dynamic Degree) was 49.72%; VideoCrafter's was 89.72%. The authors say generating relatively static scenes can "cheat" to get high consistency scores. | VBench, as above (Table 1 and section on trade-offs). | The scale is compressed: near 98% is not "almost no flicker." Old models; use the trade-off, not the numbers, to judge a current tool. |
| An image editing model applied to each frame on its own gave edits that "lack any temporal consistency." Older post-processing methods "effectively reduce high-frequency temporal flickering" but "are not designed to handle frames that exhibit substantial variations in content." | [Geyer et al., "TokenFlow," arXiv 2307.10373](https://arxiv.org/html/2307.10373) (July 2023). HTML full text opened Oct 29, 2026. | Research method paper: the per-frame result is a baseline the authors beat with their own method. Judged by warp error and a user study; built on Stable Diffusion in 2023. |
| World Consistency Score proposes a single video score that includes a "flicker penalty" next to object permanence, relation stability and causal compliance. | [Rakheja et al., "World Consistency Score," arXiv 2508.00144](https://arxiv.org/abs/2508.00144) (submitted July 31, 2025). Abstract opened Oct 29, 2026. | A proposal with an "experimental validation blueprint"; the abstract reports no test results. Shows flicker is treated as a core part of video consistency, nothing more. |
| A vendor guide says "Flicker is a symptom, not one defect," splits it into brightness or color pulsing, camera jitter, texture shimmer, identity or geometry drift, and delivery artifacts, and warns "A paused thumbnail cannot prove temporal consistency." | [Magic Hour blog, "How to fix flicker in AI video," Oct 1, 2026](https://magichour.ai/blog/how-to-fix-flicker-in-ai-video). Opened Oct 29, 2026. | Vendor blog by the company's CEO; it sells a video tool. Gives no measured results and says its repair plans are not benchmarks. |

**Incident:** No public incident found where a business's AI video was called out specifically for flicker. Searches run: "deflicker AI generated video flicker fix help," "Runway OR Pika OR Luma help center flickering video generation consistency," "AI video flicker stable diffusion frame by frame temporal consistency ad backlash," "Coca-Cola AI holiday ad 2024 criticism inconsistent trucks wheels morphing." Coverage of Coca-Cola's AI holiday ads seen in search summaries concerned truck wheels and other changing objects, not flicker; it was not opened and is not used (it fits the [objects that appear, vanish or change](ai-video-objects-appear-vanish-or-change-between-frames.md) page). Runway's image-to-video prompting guide and Adobe's Premiere Pro flicker help page both returned 403 when opened, so neither is cited.

## 5. The fix
**The principle:** A still frame cannot show flicker. Judge AI video the way viewers see it: moving, at full speed.

**Do this: teams and assistants that make or edit video with AI**
1. **Review the downloaded clip at normal speed.** Watch the original file at its delivery size and speed before approval, not only a paused frame or editor preview, then step through frames around any defect (following the Magic Hour guide).
2. **Name the flicker type and time range.** Record one of: brightness or color pulse, camera jitter, texture shimmer, structure change, delivery artifact, plus the seconds and area ("2.0-4.5 s, label"). A structure change (a logo, face or object changing shape) goes to the [objects page](ai-video-objects-appear-vanish-or-change-between-frames.md) checks instead.
3. **Do not ship frame-by-frame image edits as video.** If a restyle or edit ran an image model on each frame separately, treat it as unreviewed until it passes rule 1; prefer a tool that edits frames together or a video model (following TokenFlow's finding).
4. **Run a frame-difference check on shots meant to stay still.** For locked-off product, background and logo shots, compute the mean absolute difference between consecutive frames, as VBench does, and flag spikes for review (proposed screen, not a pass mark).
5. **Match the repair to the type.** Brightness pulse: try exposure or color correction on a copy. Camera jitter: try stabilization. Texture shimmer on a label, face or key product surface: regenerate or replace that segment from a clean reference with less motion; do not blur it over. One repair at a time, compared against the original.
6. **Set a retry budget, then change approach.** Decide the number of regenerations before starting (the Magic Hour guide advises this; the number is the team's choice). After it, shorten the shot, simplify the motion, or use real footage.
7. **Keep the motion the brief asked for.** After a fix, confirm the push-in, pan or action is still there. A clip made steady by freezing it fails the brief.
8. **A named person approves at normal speed, and it is logged.** Log clip ID, tool and version, flicker type, time range, repair, retries, reviewer and date.

**Reference design: flicker check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Playback review | Downloaded file watched at normal speed | 6 s clip, 1080x1920 |
| Flicker type | Named with time range and area | Texture shimmer, 2.0-4.5 s, label |
| Frame-by-frame edit | Video-aware tool or passed playback review | Video model, not per-frame restyle |
| Static-shot screen | Frame-difference spikes reviewed | 1 spike at 3.1 s, checked |
| Repair | Fits the type, one at a time | Regenerated 3 s push-in |
| Motion kept | Requested motion still visible | Push-in present |
| Sign-off | Named, dated | J. Lee, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reviewed clip: say whether flicker was found, the type and the time range before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | Flicker found or the retry budget is reached: shorter shot, still camera, real footage, something else. Not when the clip is clean. |
| Ask one clarifying question | It is unclear whether movement is intended: "Should the leaves behind the jar move, or stay still?" |
| Hand off to a person | Always for the final normal-speed approval of a published clip |

**Don't over-correct.** Do not freeze or flatten a shot to remove flicker; VBench shows stillness can buy a good flicker score. Do not flag motion the brief asked for (rippling water, falling snow, a strobe or neon effect the requester chose) as flicker. Do not stack deflicker, blur and sharpen filters until detail is gone; the Magic Hour guide warns "No filter guarantees recovery of details the model never preserved." Do not block internal drafts and storyboards that will not be published. Do not regenerate without limit.

**Hand-off rule.** If a viewer, platform or reviewer reports flicker in a published clip, send it to the approver and content owner the same day with the log. They decide whether to pull, replace or keep it.

**Framework used:** none yet. Rules 1, 2, 5 and 6 follow the Magic Hour vendor guide; rule 3 follows TokenFlow; rules 4 and 7 follow VBench's metric and trade-off; rule 8 is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-video-flicker-between-frames.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Clip approved from a thumbnail | Blocked until normal-speed review is logged | 1, 8 |
| 2 | Label shimmers at 2-4 s | Type and time range recorded; fitting repair offered | 2, 5 |
| 3 | Per-frame image restyle of a store video | Treated as unreviewed until playback review | 3 |
| 4 | Fix makes the push-in disappear | Fails motion check; not approved | 7 |
| 5 | Retry budget reached | Stops; offers shorter shot, still camera or real footage | 6 |
| 6 | Requested falling snow | Not flagged as flicker | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unreviewed-or-flagged flicker publish rate** (primary) | 0 (proposed) | Monthly sample of published AI clips: no logged normal-speed review, or an open flicker flag / all sampled | Any |
| Flicker reports after publish | 0 (proposed) | Comments, tickets and platform notes mentioning flicker, shimmer, jitter or "jumping" on AI clips / AI clips published | Any |
| Static-shot frame-difference spikes | Track, no target | Automated frame-difference screen on locked-off shots, spikes per clip | Rising for 2 months |
| Retries per accepted clip | Track, no target | Generation log: renders before an approved clip | Rising for 2 months |
| Motion lost after repair (counter-metric) | Track, no target | Reviewed clips where requested motion was missing after a flicker fix / repaired clips | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Clip approved with no playback event logged, only a thumbnail view | Review tool log | Reviewer watched in another player, logged elsewhere |
| Frame-difference spike on a shot tagged "static" | Automated screen | A real cut, light change or motion the brief requested |
| Clip made by running an image model per frame, approved in one step | Pipeline log | A video-aware tool that edits frames together |
| Viewer comment says "flicker," "shimmer" or "jumping" on an AI clip | Social comments, support tickets | Playback or upload compression on one device |

**Starter rule:** no AI video clip is published unless its log shows a normal-speed review of the downloaded file, a flicker type of "none" or a logged repair, and a named approver.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-video-flicker-between-frames
runs: [post_generation, pre_publish]
reads: [clip.id, clip.tool_version, clip.per_frame_edit, review.playback_logged, review.flicker_type, review.time_range, screen.frame_diff_spikes, repair.method, generation.tries, review.motion_kept, review.signoff]
trigger: no playback review, or flicker type not none with no repair, or per-frame edit unreviewed, or retry budget reached, or motion lost after repair
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Regenerate a shorter shot from a clean reference", "Keep the camera still", "Use real footage for this shot", "Something else"]
on_miss: block_publish
metric: unreviewed-or-flagged flicker publish rate
counter_metric: motion lost after repair
status: proposed
```

## 8. Related patterns
- [AI video objects that appear, vanish or change between frames](ai-video-objects-appear-vanish-or-change-between-frames.md) - the sibling page. There the thing itself changes (a wheel, logo or cup appears or changes shape); here the same objects stay but their surface detail or light jumps frame to frame.
- [Quality drift in generated images](../../generation-artifacts/failures/quality-drift.md) - the closest older page. It covers images getting worse across many generations; flicker is in the first render, inside one clip. Its percentages have no source and are not used here.
- [Artifact accumulation in regeneration](../../generation-artifacts/failures/artifact-accumulation.md) - artifacts that build up when one image is regenerated again and again; flicker does not need repeated regeneration.
- [Consistency failure: identity loss across generations](../../generation-artifacts/failures/consistency-failure.md) - a character or product that changes between separate outputs; flicker is fine-detail change between neighboring frames.
- [AI video regenerations that cost more than budgeted](../../ai-image-generation-business-risks/failures/ai-video-regenerations-cost-more-than-budgeted.md) - what happens when flicker is fixed by regenerating without a budget (rule 6).
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the missing sign-off that lets a flickering clip ship.

## 9. Common questions
### Why does my AI video flicker?
The model redraws fine detail, edges and light slightly differently in each frame. VBench traces flicker to imperfect consistency "at local and high-frequency details," so large shapes stay put while textures and labels shimmer.

### How do I fix flicker in an AI video?
First name the type. A brightness pulse may respond to exposure or color correction, and camera shake to stabilization. Shimmering labels, faces or product surfaces usually need that segment regenerated with less motion from a clean reference, or replaced with real footage.

### Why does Stable Diffusion flicker when I use it on video frame by frame?
An image model edits each frame without knowing what it did to the last one. TokenFlow found per-frame edits looked good alone but lacked temporal consistency; tools that edit frames together reduce this.

### Will a deflicker filter fix AI video flicker?
Sometimes, for light or brightness flicker. TokenFlow notes older post-processing reduces high-frequency flicker but cannot handle frames whose content really changes, and strong filtering can smear detail.

### Can I check for flicker automatically?
Partly. On shots meant to be still, a frame-difference score like VBench's can flag spikes for a person to watch. It cannot judge moving shots well, so a normal-speed human review is still needed before publishing.
