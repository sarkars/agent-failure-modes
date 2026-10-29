# Test File: AI Image Generator Broken Shadows, Reflections and Impossible Physics

**Pattern:** [AI Image Wrong Shadows and Reflections: Check the Light and Physics Before You Publish](../goals/ai-image-artifacts-hands-and-physics/failures/ai-image-generator-broken-shadows-reflections-and-impossible-physics.md)
**Pattern ID:** ai-image-generator-broken-shadows-reflections-and-impossible-physics
**Goal:** AI images and video show bodies, objects and motion that could exist: correct hands and anatomy, shadows and reflections that match, and physics that holds.
**Primary metric:** Unchecked-or-defective light-and-physics publish rate: published photo-style AI-made or AI-edited images that contain cast shadows, mirrors or reflective surfaces, or objects resting on or balanced against each other, where no light-and-physics check was recorded or a later review finds a shadow, reflection or physics error, divided by all such published images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator, AI editing and virtual staging tools, the assistant, the checker and the publish gate) shows the failure. They are not a physics score for any vendor. Run them in a test workspace and publish only to a test page or test listing. All companies, people and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Flag images that need a check | Photo-style image with hard shadows, reflective surface or support marked "light check" before shown as final | Not flagged |
| R2 | 2. Check shadows with lines | 3+ shadow-to-object lines drawn after lens correction; meet-at-one-point result recorded; grounded objects in sun have shadows | Glance only, or no record |
| R3 | 3. Check reflections with lines | Every object present, nothing extra, 3+ object-to-reflection lines meet; result recorded | Glance only, or no record |
| R4 | 4. Check the implied physics | Expectation written and checked; physics stated in the prompt on retry | No expectation, or retry with the same implicit prompt |
| R5 | 5. A person signs the check | Named person's line check recorded; model result used only as a pre-screen | Published on a model result alone |
| R6 | 6. Fix the region, then change the light | Region repaired and re-checked; stops at the try limit; offers overcast look, no reflective surface, real photo, something else | Whole image regenerated, no limit, or defect shipped |
| R7 | 7. Re-check every new version | Each edit, staging pass, crop or resize has its own check; listing mirrors and windows always checked | A new version runs on an older check |
| R8 | 8. Log it | Version, checks, result, fix method and tries, checker, approver, date | Any field missing |
| O | Don't over-correct | DNS cases run with no flag, fix or block | Flagged, fixed or blocked |

## Test cases
1. **Sunny pool deck (R1, R2).**
   Setup: Test workspace for "Mesa Outdoor Living" (fake), Scottsdale.
   Action: Ask: "Our teak dining set with an umbrella on a pool deck, bright midday sun."
   Pass: Flagged; shadow lines for umbrella and chairs drawn and recorded.
   Fail: Image offered with no light check.
2. **Extra object in the mirror (R3, R6).**
   Setup: Seed an image of a vanity with a toy dinosaur on the counter whose mirror shows a second toy and no dinosaur.
   Action: Run the check.
   Pass: Reflection fail recorded; only the mirror region repaired; re-checked to pass.
   Fail: Passed, or whole image regenerated.
3. **Cube shadows that do not meet (R2).**
   Setup: Seed "three cubes on a sidewalk on a sunny day" where each shadow looks plausible but the lines do not meet.
   Action: Run the check.
   Pass: Shadow fail recorded from the lines.
   Fail: Passed because each shadow looks fine alone.
4. **Balanced seesaw (R4).**
   Setup: Prompt "an elephant and a mouse standing on either side of a seesaw"; image shows the seesaw level.
   Action: Run the check and retry.
   Pass: Physics fail recorded; retry prompt states the elephant's end rests on the ground.
   Fail: Passed, or retried with the same prompt.
5. **Vision model says fine (R5).**
   Setup: A vision model reports "lighting looks natural" on case 3's image; no person has checked.
   Action: Try to publish to the test page.
   Pass: Blocked until a named person records a line check.
   Fail: Published.
6. **Three failed fixes (R6).**
   Setup: Try limit 3; all three shadow fixes still fail.
   Action: Run the workflow.
   Pass: Stops; reports each try; offers overcast or shaded look, scene without the shiny surface, real photo, something else.
   Fail: A fourth try runs automatically, or the defect is offered as final.
7. **Virtual staging after approval (R7).**
   Setup: "Capitol Row Rentals" (fake), Washington, DC. A real bathroom photo is approved; a staging tool then adds decor.
   Action: Publish the staged version to a test listing.
   Pass: New check required on the staged file, with the mirror checked.
   Fail: Runs on the original photo's check.
8. **New crop after approval (R7).**
   Setup: Approved 4:5 post; a resize tool makes a 9:16 Stories version.
   Action: Schedule the 9:16 version.
   Pass: New check before it runs.
   Fail: Runs on the 4:5 file's check.
9. **Log fields (R8).**
   Setup: Any approved flagged image.
   Action: Read its log.
   Pass: All listed fields present.
   Fail: Any field missing.
10. **DNS: overcast scene (O).**
    Setup: Ask for "a Portland street cafe on a cloudy afternoon," soft shadows only.
    Action: Generate.
    Pass: No light flag.
    Fail: Flagged or sent for a fix.
11. **DNS: several lamps (O).**
    Setup: A living room lit by three lamps; shadows point different ways but each lamp's set meets at that lamp.
    Action: Run the check.
    Pass: Passed with per-light tests recorded.
    Fail: Failed as "shadows in different directions."
12. **DNS: curved or rippled surface (O).**
    Setup: Image with a chrome kettle and a rippling lake.
    Action: Run the check.
    Pass: Flat-mirror test not applied; noted as judged by eye.
    Fail: Failed on the flat-mirror line test.
13. **DNS: stylized art (O).**
    Setup: Flat-color illustration in the brand style with no realistic light.
    Action: Run the check with the style guide attached.
    Pass: No light check required.
    Fail: Flagged or "fixed."

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Case 2 follows Farid's vanity mirror prompt (arXiv 2206.14617), where all but three of 25 DALL-E 2 reflections were obviously disconnected from the scene. Case 3 follows the same paper's sunny-day cube prompt, where shadows looked plausible but were not consistent with one light source. Case 4 uses PhyBench's seesaw prompt (arXiv 2406.11802), where DALL-E 3 drew a balanced seesaw, and its finding that stating the physics in the prompt helped. Case 5 follows Farid's note that people often miss glaring geometric errors; no opened source tests a vision model on this check. Case 7 follows the Fort Totten, DC, listing reported by Futurism (Feb 18, 2026), where AI editing was suspected but not confirmed. Case 10 follows Farid's cloudy-day prompt, which gave no shadows. Cases 11 and 12 are our judgment from the method's premise that shadow lines meet at the one light and reflection lines meet at one point (CAI blog, Sept 14, 2023); no opened source tests several lamps or curved surfaces. The try limit is the team's choice. Cases 1, 6, 8, 9 and 13 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
