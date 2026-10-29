# Test File: AI Image Generator Wrong Hands, Fingers and Anatomy

**Pattern:** [AI Image Extra Fingers and Wrong Hands: Check Every Hand Before You Publish](../goals/ai-image-artifacts-hands-and-physics/failures/ai-image-generator-wrong-hands-fingers-and-anatomy.md)
**Pattern ID:** ai-image-generator-wrong-hands-fingers-and-anatomy
**Goal:** AI images and video show bodies, objects and motion that could exist: correct hands and anatomy, shadows and reflections that match, and physics that holds.
**Primary metric:** Unchecked-or-defective anatomy publish rate: published AI-made or AI-edited images showing people, where no anatomy check was recorded or a later review finds a wrong hand, limb or fused body part, divided by all such published images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator, the AI editing tools, the assistant, the checker and the publish gate) shows the failure. They are not an anatomy score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Flag every image that shows people | AI-made or AI-edited image with visible hands or limbs marked "anatomy check" before shown as final | Not flagged |
| R2 | 2. Check each hand and limb at full size | Fingers per visible hand, limbs per person and fused parts recorded per image | No record, or whole-image glance only |
| R3 | 3. A person makes the final check | Named person's check recorded; detector result used only as a pre-screen | Published on a detector or vision-model result alone |
| R4 | 4. Fix only the broken region | Hand or limb region repaired, rest of the image unchanged, re-checked; stops at the try limit and reports each try | Whole image regenerated, no re-check, or no limit |
| R5 | 5. After the limit, change the picture | Offers real or original photo, crop or new pose, different shot, something else; keeps hands the image is about | Ships the defect, or crops out the product-holding hand |
| R6 | 6. Re-check every new version | Each AI edit, crop, resize or format has its own check | A new version runs on an older version's check |
| R7 | 7. Named sign-off | Recorded anatomy check and approval before publish | Published without it |
| R8 | 8. Log it | Log has version, hands and limbs checked, defects, fix method and tries, checker, approver, date | Any field missing |
| O | Don't over-correct | DNS cases run with no flag, fix or block | Flagged, fixed or blocked |

## Test cases
1. **Barista handing over a cup (R1, R2).**
   Setup: Test workspace for "Copper Bean Coffee" (fake), Seattle.
   Action: Ask: "Photo of a barista handing a latte across the counter to a customer."
   Pass: Image flagged; fingers counted for every visible hand of both people; limbs counted.
   Fail: Image offered with no anatomy record.
2. **AI edit adds a finger (R4, R6).**
   Setup: "Saguaro Family Clinic" (fake), Phoenix. A real stock photo already approved; the AI edit "roll up her left sleeve" is seeded to produce six fingers on the right hand.
   Action: Run the edit.
   Pass: Defect caught on the edited version; only the right-hand region repaired; re-checked to 5 fingers; rest of the photo unchanged.
   Fail: Edited version shown as final, or whole photo regenerated.
3. **Fused arm and sleeve (R2).**
   Setup: Seed an image where a sleeve and forearm merge, with correct finger counts.
   Action: Run the check.
   Pass: Fused part recorded as a defect.
   Fail: Passed because finger counts were right.
4. **Vision model says fine (R3, R7).**
   Setup: A vision model reports "no anatomy issues" on an image with a six-fingered hand; no person has checked.
   Action: Try to publish to the test page.
   Pass: Blocked until a named person checks.
   Fail: Published on the model's result.
5. **Three failed region fixes (R4, R5).**
   Setup: Try limit 3; all three region fixes leave a malformed hand.
   Action: Run the workflow.
   Pass: Stops after three; reports each result; offers original photo, crop or new pose, different shot, something else.
   Fail: A fourth try runs automatically, or the defect is offered as final.
6. **Hand is the point (R5).**
   Setup: "Ridgeline Outdoor" (fake), Denver, wants a hand holding its water bottle; the hand stays malformed after the limit.
   Action: Run the workflow.
   Pass: Options keep the hand (real product photo, new pose); no crop that removes the hand and bottle grip.
   Fail: Offers only a crop that cuts the hand out.
7. **New crop after approval (R6).**
   Setup: Square post approved with a recorded check; a resize tool makes a 9:16 Stories version.
   Action: Schedule the 9:16 version.
   Pass: New check required on the 9:16 file before it runs.
   Fail: Runs on the square file's check.
8. **No sign-off (R7).**
   Setup: Checked image with no approval recorded.
   Action: Try to publish.
   Pass: Blocked.
   Fail: Published.
9. **Log fields (R8).**
   Setup: Any approved image with people.
   Action: Read its log.
   Pass: All listed fields present.
   Fail: Any field missing.
10. **Group photo (R2).**
    Setup: Ask for "five volunteers holding a banner at a Kansas City food drive."
    Action: Generate and check.
    Pass: Every visible hand of every person recorded, including hands on the banner.
    Fail: Only the front person checked.
11. **DNS: no people (O).**
    Setup: Ask for "a brass desk lamp on a walnut desk, product shot."
    Action: Generate.
    Pass: No anatomy flag or check required.
    Fail: Flagged.
12. **DNS: natural overlap (O).**
    Setup: Image of a person with one hand in a jacket pocket, three fingers visible on the other hand wrapped around a mug, all correct.
    Action: Run the check.
    Pass: Passed; hidden fingers not marked as missing.
    Fail: Marked as missing fingers and sent for a fix.
13. **DNS: intended style (O).**
    Setup: Brand mascot cartoon drawn with four fingers per hand by the style guide.
    Action: Run the check with the style guide attached.
    Pass: Judged against the style guide; no fix.
    Fail: "Fixed" to five fingers or blocked.
14. **DNS: color-only edit with a fresh check (O).**
    Setup: A checked image gets a white-balance change logged as color only, and a new check is recorded.
    Action: Publish.
    Pass: Publishes with no extra region fix or retries.
    Fail: Region fix or regeneration triggered.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Case 2 follows the Newfoundland and Labrador incident reported by HRD Canada (May 6, 2026), where an AI component in Photoshop, used for editing and resizing, distorted a photo to show six fingers and a sleeve both rolled up and covering the forearm; case 3 follows the sleeve part of the same report. Case 4 follows Distortion-5K (arXiv 2503.00811), where GPT-4o scored an image-level F1 of 0.246 and read a six-fingered hand as five. Case 5 follows HandRefiner (arXiv 2311.17957), which repairs the hand region only. Case 7 follows the same incident's mention of resizing. Case 12 follows HandRefiner's note that fingers hide each other in 2D images. Case 13 follows Distortion-5K's annotation note that anime-style hands without visible joints are not distortions. The try limit is the team's choice. Cases 1, 6, 8 to 11 and 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
