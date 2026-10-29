# Test File: AI Campaign Where the Product Looks Different From Image to Image

**Pattern:** [AI Product Looks Different in Every Shot: Keeping a Brand's Product Consistent Across an AI Campaign](../goals/ai-image-brand-guidelines/failures/ai-campaign-product-looks-different-across-images.md)
**Pattern ID:** ai-campaign-product-looks-different-across-images
**Goal:** AI images and video a brand publishes follow its brand guidelines: the right logo, colors, fonts, tone and product, nothing from another brand, and nothing unsafe next to its name.
**Primary metric:** Product-mismatch rate: published campaign images and video shots whose product fails any check on the product spec card, divided by all sampled images and shots (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's campaign workflow (the generator, the assistant or design tool that composites, the product check, the contact-sheet review and the publish gate) shows the failure. They are not a score for any vendor. Run them with a test spec card, dummy product photos and a test ad account. All companies, products, files, people and IDs below are invented. Covers image and video; for video, check the first, middle and last frame of every shot. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Write a product spec card | Versioned card with countable features and approved files exists before generation | Generation starts with no card |
| R2 | 2. Never generate the product from words alone | Every asset logs a composite or the locked reference set | Any asset made from text only |
| R3 | 3. Real product for close-ups | Hero close-ups composite the packshot or 3D render | Close-up product redrawn by the generator |
| R4 | 4. Check every image and shot | Every listed feature checked per asset; first, middle, last frame per video shot | Any asset or shot unchecked, or a mismatch missed |
| R5 | 5. Review the set side by side | Approval given on one contact sheet of the whole set | Assets approved one at a time |
| R6 | 6. Fix by edit, not reroll | Failing asset repaired from approved files and re-checked | Rerolled and published without re-check |
| R7 | 7. Lock card and references | Later additions use the same card version and files, checked against the sheet | New asset uses other references or skips the check |
| R8 | 8. Sign-off and log | Named reviewer; log has card version, references, generator and version, method, check result, date | Any field missing |
| O | Don't over-correct | Scene, prop and listed-variant differences pass with no extra prompts | Flagged or blocked |

## Test cases
1. **No card yet (R1).**
   Setup: Test brand "Northbound Bottle Co." (fake), no spec card on file, product photos available.
   Action: Ask: "Make 12 Instagram images of the Trailhead 32 oz bottle outdoors."
   Pass: The assistant writes or asks for a spec card (cap type, handle, logo panel position, color) before generating.
   Fail: It generates straight from the prompt.
2. **Text-only product (R2).**
   Setup: Card TH32 v3 and reference photos TH32-front, -side, -cap on file.
   Action: Ask for six lifestyle images and watch the generation requests.
   Pass: Each request carries the same three references, or the packshot is composited; the log records which.
   Fail: Any request describes the bottle in words only.
3. **Hero close-up (R3).**
   Setup: Same card; ask for a close-up of the bottle on a picnic table filling the frame.
   Action: Build the image.
   Pass: The bottle is composited from the approved packshot.
   Fail: The generator redraws the bottle as the main subject.
4. **Extra part in one image (R4).**
   Setup: A 12-image set where image 7 (seeded fixture) shows the bottle with a handle; card says no handle.
   Action: Run the product check.
   Pass: Image 7 is flagged for the handle.
   Fail: Passes.
5. **Change inside a video shot (R4).**
   Setup: A 6-shot, 15-second video where shot 4 starts with a two-tab cap and ends with a flip cap (fixture).
   Action: Run the frame check.
   Pass: Shot 4 fails on the last-frame check.
   Fail: Only the first frame is checked and it passes.
6. **Truck wheel count (R4).**
   Setup: Fake delivery-van brand "Larkspur Dairy"; card says two axles, four wheels. A 10-shot video where three shots show a third axle (fixture).
   Action: Run the product check.
   Pass: The three shots are flagged for wheel count.
   Fail: Any of them passes.
7. **One-at-a-time approval (R5).**
   Setup: All 12 images pass their checks; the reviewer opens them one by one in the ad tool.
   Action: Try to approve and schedule.
   Pass: Scheduling is blocked until a contact sheet of the whole set is signed.
   Fail: Scheduled on single approvals.
8. **Reroll instead of repair (R6).**
   Setup: Image 7 fails for the handle.
   Action: The designer regenerates image 7 from the prompt.
   Pass: The new image 7 goes back through the check and onto a new contact sheet; repair from the packshot is offered first.
   Fail: The new image replaces the old one under the existing sign-off.
9. **Week-3 banner size (R7).**
   Setup: Approved campaign; ask for a 300 x 250 banner three weeks later.
   Action: Build it.
   Pass: Uses card TH32 v3 and the same reference files; checked against the approved sheet.
   Fail: Uses different references, a newer card or no check.
10. **Build log (R8).**
    Setup: Any approved campaign.
    Action: Read the build log for three assets.
    Pass: Card version, references, generator and version, composite or reference method, check result, reviewer and date all present.
    Fail: Any field missing.
11. **Missing product files (R1, R2).**
    Setup: No photos or card on file.
    Action: Ask for a campaign set "with our bottle in every image."
    Pass: The assistant offers choices (upload photos, write the card now, scenes without the product for now, something else) and does not invent the bottle.
    Fail: It generates a bottle from words.
12. **DNS: backgrounds differ (O).**
    Setup: 12 images at lakes, campsites and trailheads, product passes in all.
    Action: Run the check.
    Pass: No flags for scene, lighting or props.
    Fail: Flagged because the scenes differ.
13. **DNS: listed color variant (O).**
    Setup: Card lists Pine Green and Slate as approved colors; four images use Slate.
    Action: Run the check.
    Pass: Not flagged.
    Fail: Flagged as a mismatch.
14. **DNS: internal mood board (O).**
    Setup: Ask for eight rough concepts for an internal meeting, marked "draft, not for publishing."
    Action: Generate.
    Pass: Runs without the contact-sheet gate.
    Fail: Blocked or sent for sign-off.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 5 and 6 follow the Campaign and Il Sole 24 Ore reports that the Coca-Cola trucks' wheels changed between shots of the 2025 holiday ad. Tests 2 and 3 follow the OpenAI and Google reference-image documentation and OpenAI's listed consistency limitation. Test 8 follows the Toys "R" Us account of picking shots from many tries and adding corrective effects. The number of frames per shot, the similarity check and the sample rate are the team's own choices; the page does not set thresholds. Tests 1, 4, 7 and 9 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
