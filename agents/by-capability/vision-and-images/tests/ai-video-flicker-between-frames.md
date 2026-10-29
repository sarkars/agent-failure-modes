# Test File: AI Video Flickering Between Frames

**Pattern:** [AI Video Flickering Between Frames: Fine Detail, Light and Texture Jump in Every Frame](../goals/ai-video-consistency/failures/ai-video-flicker-between-frames.md)
**Pattern ID:** ai-video-flicker-between-frames
**Goal:** AI video and image sets keep the same people, objects and look from frame to frame and image to image.
**Primary metric:** Unreviewed-or-flagged flicker publish rate: published AI video clips with no recorded normal-speed review, or with an open flicker flag, divided by all published AI video clips (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's video workflow (the generator or restyle tool, the assistant that runs it, the reviewer and the publish gate) shows the failure. They are not a flicker score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people, products and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting. Fixture clips must not contain rapid full-screen flashing; use label, texture or small-area shimmer only.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Review at normal speed | Downloaded clip watched at normal speed and delivery size before approval; logged | Approved from a thumbnail, paused frame or editor preview only |
| R2 | 2. Name type and time range | Flicker type (or "none"), seconds and area recorded | Flicker noticed but not classified, or no time range |
| R3 | 3. No unreviewed per-frame edits | Per-frame image-model edit treated as unreviewed until R1 passes, or a video-aware tool used | Per-frame edit approved in one step |
| R4 | 4. Static-shot screen | Frame-difference screen run on shots tagged static; spikes sent to a person | Screen skipped, or spikes used as an automatic pass or fail |
| R5 | 5. Repair fits the type | Pulse: exposure or color fix; jitter: stabilization; shimmer on label, face or product: regenerate or replace segment; one repair at a time | Blur or stacked filters over shimmering text, or a mismatched repair |
| R6 | 6. Retry budget | Budget set before starting; at the limit, offers shorter shot, still camera or real footage | Regenerates without limit |
| R7 | 7. Keep requested motion | Requested motion confirmed present after a fix | Fix freezes or removes requested motion and clip is approved |
| R8 | 8. Named approval and log | Named approver at normal speed; log has clip ID, tool and version, type, time range, repair, retries, reviewer, date | Any field missing, or no named approver |
| O | Don't over-correct | DNS cases run with no flicker flag, repair or block | Flagged, repaired or blocked |

## Test cases
1. **Thumbnail approval (R1, R8).**
   Setup: Test workspace for "Lakeshore Candle Co." (fake), Milwaukee. A 6-second image-to-video clip of a candle jar, slow push-in.
   Action: Approve from the preview thumbnail and try to schedule it.
   Pass: Blocked until a normal-speed review of the downloaded file is logged.
   Fail: Scheduled.
2. **Label shimmer (R2, R5).**
   Setup: Fixture clip where the jar label text shimmers from 2.0 to 4.5 s while the jar shape is steady.
   Action: Run review.
   Pass: Logged as texture shimmer, 2.0-4.5 s, label; offers regeneration or replacement of that segment.
   Fail: No type or time range, or a blur filter applied to the label.
3. **Brightness pulse (R2, R5).**
   Setup: Fixture clip of a Phoenix coffee shop counter where overall exposure rises and falls; objects stay recognizable.
   Action: Run review.
   Pass: Logged as brightness pulse; exposure or color correction tried on a copy first.
   Fail: Logged as texture shimmer, or full regeneration as the only option offered.
4. **Per-frame restyle (R3).**
   Setup: A store walkthrough video restyled "as a watercolor" by running an image model on each frame.
   Action: Submit for approval.
   Pass: Marked unreviewed until playback review passes, or rerun with a video-aware tool.
   Fail: Approved in one step.
5. **Static-shot spike (R4).**
   Setup: A locked-off logo shot tagged static; the screen shows one frame-difference spike at 3.1 s.
   Action: Run the screen.
   Pass: Spike sent to a person, who checks 3.1 s and records the result.
   Fail: Screen skipped, or the clip auto-rejected or auto-passed on the score alone.
6. **Stacked filters (R5).**
   Setup: Shimmering product label; editor proposes deflicker plus blur plus sharpen at once.
   Action: Ask the assistant to "just clean it up."
   Pass: One repair at a time, compared against the original; label shimmer routed to regeneration or replacement.
   Fail: All filters stacked and the result approved.
7. **Retry budget reached (R6).**
   Setup: Budget set to 3; three renders all show label shimmer.
   Action: Run the workflow.
   Pass: Stops after three; offers a shorter shot, still camera, real footage or something else.
   Fail: A fourth render runs automatically.
8. **Motion lost (R7).**
   Setup: Brief asks for a slow push-in; the repaired clip is steady but the push-in is gone.
   Action: Submit for approval.
   Pass: Fails the motion check; not approved.
   Fail: Approved.
9. **Log fields (R8).**
   Setup: Any approved AI clip.
   Action: Read its log.
   Pass: All listed fields present.
   Fail: Any field missing.
10. **Structure change routed (R2).**
    Setup: Fixture clip where the logo changes shape mid-shot (not shimmer).
    Action: Run review.
    Pass: Logged as structure change and sent to the objects-change checks.
    Fail: Treated as flicker and filtered.
11. **Delivery artifact (R2).**
    Setup: Original download is clean; only the uploaded test-page version shows blocky shimmer.
    Action: Run review.
    Pass: Logged as delivery artifact; no regeneration started.
    Fail: Clip regenerated.
12. **DNS: requested motion (O).**
    Setup: Brief asks for "falling snow outside a Denver storefront window."
    Action: Generate and review.
    Pass: Snow not flagged as flicker.
    Fail: Flagged or filtered.
13. **DNS: internal draft (O).**
    Setup: Storyboard draft clip marked "internal, not for publishing."
    Action: Save to the drafts folder.
    Pass: No publish gate or approval required.
    Fail: Blocked.
14. **DNS: clean clip (O).**
    Setup: Clip reviewed at normal speed with no flicker found.
    Action: Approve.
    Pass: Logged as type "none"; no repair or retry offered.
    Fail: Repair or regeneration pushed anyway.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Cases 1, 2, 3, 6, 7, 10 and 11 follow the Magic Hour vendor guide (magichour.ai, Oct 1, 2026), which splits flicker into pulse, jitter, shimmer, structure drift and delivery artifact, says a paused thumbnail cannot prove temporal consistency, and advises a retry budget. Case 4 follows TokenFlow (arXiv 2307.10373), where per-frame image edits lacked temporal consistency. Case 5 follows VBench (arXiv 2311.17982), which measures flicker as frame-to-frame pixel difference on static scenes; using it as a screen, not a pass mark, is the page's proposal. Case 8 follows VBench's finding that stability and motion trade off. The retry budget and sample rate are the team's choices. Cases 9 and 12 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
