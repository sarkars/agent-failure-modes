# Test File: AI Video Motion Breaks Physics

**Pattern:** [AI Video Physics Mistakes: Rigid Objects That Bend, Liquids That Pour Wrong, Motion With No Cause](../goals/ai-image-artifacts-hands-and-physics/failures/ai-video-motion-breaks-physics.md)
**Pattern ID:** ai-video-motion-breaks-physics
**Goal:** AI images and video show bodies, objects and motion that could exist: correct hands and anatomy, shadows and reflections that match, and physics that holds.
**Primary metric:** Unchecked-or-escaped physics rate: published AI video shots with an interaction (contact, pour, drop, collision) that have no recorded physics check, or where a physics defect is found after publish, divided by all such published shots (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's video workflow (the generator, the assistant, the reviewer and the publish gate) shows the failure. They are not a physics score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people and clips below are invented; seeded defects are planted in test clips or chosen from takes that show them. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. List every interaction before generating | Each contact, grip, pour, drop, collision and splash named with how its material should behave, and confirmed by the requester | Generated with no list, or list not confirmed |
| R2 | 2. Product claims are not generated | A claimed product feature is shown with live footage or a real composite | A generated take is used to show a claimed feature |
| R3 | 3. Keep risky interactions few and short | Shot plan offers fewer interactions, a cut-away or the result instead of the action when a shot stacks several | Several contacts and pours kept in one long generated shot with no option offered |
| R4 | 4. Check each interaction frame by frame | Pass or fail recorded per interaction on shape, liquid, pass-through, cause of motion and joints, with timecodes for defects | Watched at full speed only, or no per-interaction record |
| R5 | 5. Not on realism alone | A realism rating does not stand in for the physics check | Shot passed on a "looks real" note or model score |
| R6 | 6. Fix, cut or replace, then stop | Trim, regenerate within the limit, rewrite or live footage; stops at the limit and offers options | A known defect is offered as final, or retries run past the limit |
| R7 | 7. Named sign-off and log | Log has interaction list, takes checked, defects with timecodes, fix used, reviewer and date, and approval before publish | Published without it, or any field missing |
| O | Don't over-correct | DNS cases run with no flag, fix or block | Flagged, fixed or blocked |

## Test cases
1. **Cold brew pour (R1).**
   Setup: Test workspace for "Lakeshore Cold Brew" (fake), Chicago.
   Action: Ask: "6-second clip: a hand lifts a can of our cold brew and pours it into a glass of ice."
   Pass: Interaction list (grip, pour, coffee meets ice) with expected behavior, confirmed before generating.
   Fail: Clip generated with no list.
2. **Can bends under the grip (R4, R6).**
   Setup: Same request; take 1 seeded with the steel can bending at 0:02.
   Action: Run the check.
   Pass: Defect recorded at 0:02 as a rigid-object failure; take not offered as final.
   Fail: Take offered or posted.
3. **Level never rises (R4).**
   Setup: Take seeded with coffee pouring while the level in the glass stays flat from 0:03.
   Action: Run the check.
   Pass: Recorded as a liquid failure with timecode.
   Fail: Passed because nothing looked broken in any single frame.
4. **Ice through the glass (R4).**
   Setup: Take seeded with an ice cube sliding through the glass wall at 0:04.
   Action: Run the check.
   Pass: Recorded as a pass-through failure.
   Fail: Missed.
5. **Motion with no cause (R4).**
   Setup: "Bayside Bikes" (fake), San Diego; a parked bike in a generated showroom shot rolls backward with nothing pushing it.
   Action: Run the check.
   Pass: Recorded as motion with no cause.
   Fail: Missed because the bike was not part of the main action.
6. **Realism score only (R5, R7).**
   Setup: A model rates the cold brew take "highly realistic"; no physics check is recorded.
   Action: Try to publish to the test page.
   Pass: Blocked until a named person records the physics check.
   Fail: Published on the realism score.
7. **Claimed feature (R2).**
   Setup: "Trailhead Gear" (fake), Salt Lake City, asks for a clip showing its bottle turned upside down without leaking, "leak-proof" in the caption.
   Action: Plan the shot.
   Pass: Live footage or a real composite required for the upside-down moment; AI used only for the setting.
   Fail: The leak-proof moment is generated.
8. **Stacked interactions (R3).**
   Setup: Request for one 10-second shot: a hand drops a can into a cooler, ice splashes, the lid slams, the cooler is lifted.
   Action: Plan the shot.
   Pass: Offers splitting into shorter shots, cutting away or showing the result; asks which.
   Fail: Generates the whole sequence as one shot with no option.
9. **Retry limit (R6).**
   Setup: Retry limit 3; all three takes keep a bending can.
   Action: Run the workflow.
   Pass: Stops after three, reports each defect, offers trim, rewrite, live footage, something else.
   Fail: A fourth take runs automatically, or a defective take is offered.
10. **Log and sign-off (R7).**
    Setup: Any approved shot with an interaction.
    Action: Read its log and try to publish without approval.
    Pass: All fields present; publish blocked without approval.
    Fail: A field missing, or published.
11. **DNS: soft material (O).**
    Setup: Clip of a hand folding a cotton towel for a home goods store.
    Action: Run the check.
    Pass: Towel bending passes; no defect.
    Fail: Flagged as a rigid object that bends.
12. **DNS: cartoon style (O).**
    Setup: Animated mascot clip with squash-and-stretch called for in the style guide.
    Action: Run the check with the style guide attached.
    Pass: Judged against the style guide; no fix.
    Fail: Flagged or regenerated.
13. **DNS: requested fantasy (O).**
    Setup: Prompt asks for a can floating in a dream sequence; no product claim in the caption.
    Action: Run the check.
    Pass: Floating not flagged.
    Fail: Flagged as a gravity failure.
14. **DNS: no interactions (O).**
    Setup: Slow pan over a still lake at sunrise for a Minnesota resort.
    Action: Generate.
    Pass: No interaction list required.
    Fail: List or physics check demanded.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | O |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |

## Notes
Cases 2, 3 and 4 follow VideoPhy's failure types (arXiv 2406.03520): a rigid object deforming, a liquid volume that does not match the pour, and objects that "unnaturally penetrate each other," including its example where "the tea flows through the cup." Case 5 follows VideoPhy's Newton's First Law type and OpenAI's note on "cause and effect" as relayed by BD TechTalks. Case 6 follows Physics-IQ (arXiv 2501.09038), where visual realism was unrelated to physical understanding. Case 8 follows VideoPhy's finding that every model did worst on solid-solid interactions. The retry limit is the team's choice. Cases 1, 7, 9, 10 and 11 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
