# Test File: AI Video Objects Appear, Vanish or Change Between Frames

**Pattern:** [AI Video Objects Appear, Vanish or Change Between Frames: Extra Cups, Missing Props, Shifting Wheels](../goals/ai-video-consistency/failures/ai-video-objects-appear-vanish-or-change-between-frames.md)
**Pattern ID:** ai-video-objects-appear-vanish-or-change-between-frames
**Goal:** AI video and image sets keep the same people, objects and look from frame to frame and image to image.
**Primary metric:** Unchecked-or-escaped continuity rate: published AI video shots with no recorded frame-by-frame continuity check, or with an object that appears, vanishes or changes found after publish, divided by all published AI video shots (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's video workflow (the generator, the assistant that writes prompts and checks takes, any object tracker, and the publish gate) shows the failure. They are not a consistency score for any vendor. Run them in a test workspace and publish only to a test page. Several cases need a seeded or hand-picked take that contains the named defect; build those fixtures first. All companies, people and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Write a continuity list | List of people, products and props with counts and key features written and confirmed before generating | No list, or not confirmed |
| R2 | 2. Keep crowded shots short or split | A shot with many similar people or animals is shortened, split or composited | Generated as one long crowded shot with no extra check |
| R3 | 3. Check every shot frame by frame | Per-item record for each take; unlisted arrivals recorded with timecodes | Take played once at speed, or no record |
| R4 | 4. Check items that leave view | Covered or off-frame items confirmed to return unchanged | Not checked |
| R5 | 5. Check that changes stick | Changed objects confirmed to stay changed | Reverting change missed |
| R6 | 6. Fix, or drop, then stop | Defective take trimmed, regenerated within the limit or composited; never offered as is | Defective take offered or posted, or retries without limit |
| R7 | 7. Tracker as pre-screen only | Named person's frame-by-frame sign-off required before publish | Published on tracker result alone |
| R8 | 8. Log it | Log has list, takes checked, defects with timecodes, fix, reviewer, date | Any field missing |
| O | Don't over-correct | DNS cases run with no flag, retry or block | Flagged, retried or blocked |

## Test cases
1. **Continuity list first (R1).**
   Setup: Test workspace for "Copper Kettle Coffee" (fake), a Phoenix coffee shop.
   Action: Ask: "8-second clip: our barista slides two iced lattes across the counter to a customer."
   Pass: Before generating, the assistant lists 2 lattes, barista, customer, tip jar and cup logo, and asks the requester to confirm.
   Fail: Generates with no list.
2. **Object appears (R3, R6).**
   Setup: Seed a take where a third cup appears at 0:05.
   Action: Run the check.
   Pass: Defect recorded as "third cup appears, 0:05"; take not offered.
   Fail: Take offered, or defect not recorded.
3. **Object vanishes behind an arm (R4).**
   Setup: Seed a take where the tip jar is gone after the barista's arm passes it at 0:03.
   Action: Run the check.
   Pass: Recorded as an item that did not return after being covered.
   Fail: Missed.
4. **Shape or count changes mid-clip (R3).**
   Setup: "Lone Star Moving" (fake), a Dallas mover, asks for a box truck driving past; seed a take where a rear wheel set doubles at 0:04.
   Action: Run the check.
   Pass: Wheel count change recorded with timecode.
   Fail: Missed.
5. **Change does not stick (R5).**
   Setup: Seed a take where the customer takes the lid off a cup at 0:04 and the lid is back at 0:06.
   Action: Run the check.
   Pass: Recorded as a state change that reverted.
   Fail: Missed.
6. **Crowded shot (R2).**
   Setup: A Chicago dog daycare (fake) asks for "twelve puppies running across the yard" in one 10-second shot.
   Action: Run the workflow.
   Pass: Assistant proposes fewer puppies per shot, a shorter shot or compositing groups, and the take is still checked frame by frame.
   Fail: One long crowded shot generated and offered with no extra step.
7. **Retry limit (R6).**
   Setup: Retry limit 3; seed three takes that each have a defect.
   Action: Run the workflow.
   Pass: Stops after three; names each defect with timecode; offers trim, composite, live footage or something else.
   Fail: A fourth take runs automatically, or a defective take is offered.
8. **Tracker only (R7).**
   Setup: Tracker reports no flags; no person has checked the clip.
   Action: Try to publish to the test page.
   Pass: Blocked until a named person signs off.
   Fail: Published.
9. **"Nobody will notice" (R6).**
   Setup: Take with a known defect at 0:07; requester says "it's only on screen for a second, post it."
   Action: Send the request.
   Pass: Assistant declines to post that take and offers to trim before 0:07 or fix it.
   Fail: Posted.
10. **Log fields (R8).**
    Setup: Any approved shot.
    Action: Read its log.
    Pass: All listed fields present.
    Fail: Any field missing.
11. **DNS: object leaves frame on purpose (O).**
    Setup: Take where the customer picks up a cup and walks out of frame at 0:06.
    Action: Run the check.
    Pass: Not flagged.
    Fail: Flagged as a vanishing object.
12. **DNS: action changes the object (O).**
    Setup: Take where the barista pours milk and the cup goes from black to tan.
    Action: Run the check.
    Pass: Not flagged.
    Fail: Flagged as a changed object.
13. **DNS: abstract clip (O).**
    Setup: Ask for "a 6-second looping background of slow-moving amber light" for a website header.
    Action: Run the workflow.
    Pass: No continuity list required; no block.
    Fail: Blocked for a missing list.
14. **DNS: person enters from the edge (O).**
    Setup: Take where a second customer walks in from the right edge at 0:03, as the prompt asked.
    Action: Run the check.
    Pass: Not flagged.
    Fail: Flagged as an unlisted arrival.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Case 6 follows OpenAI's February 2024 statement that people or animals "can spontaneously appear, especially in scenes containing many entities" (Sora page, Wayback snapshot of Feb 17, 2024); what counts as "many" is the team's choice. Case 3 follows MemoBench (arXiv 2606.27537), which tests objects that leave view and return. Case 5 follows OpenAI's cookie-without-a-bite-mark example. Case 4 follows the wheel changes viewers reported in Coca-Cola's November 2025 ad (Campaign US). Case 8 follows the page's rule that a tracker, the method World Consistency Score (arXiv 2508.00144) describes, is a pre-screen only. The retry limit is the team's choice. Cases 1, 2, 7 and 9 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
