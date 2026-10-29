# Test File: AI Images That Break Brand Logo, Color and Font Rules

**Pattern:** [AI Generated Logo Looks Wrong: AI Images That Break Brand Logo, Color and Font Rules](../goals/ai-image-brand-guidelines/failures/ai-images-break-brand-logo-color-and-font-rules.md)
**Pattern ID:** ai-images-break-brand-logo-color-and-font-rules
**Goal:** AI images and video a brand publishes follow its brand guidelines: the right logo, colors, fonts, tone and product, nothing from another brand, and nothing unsafe next to its name.
**Primary metric:** Generated-logo rate: published brand assets whose logo was drawn by the generator instead of placed from the official file, divided by all sampled published brand assets (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's brand asset workflow (the generator, the assistant or design tool that composites, the brand check and the publish gate) shows the failure. They are not a score for any vendor. Run them with a test brand guide, a dummy logo file and a dummy palette, and publish only to a test account. All companies, files, colors, people and IDs below are invented. Covers image and video; for video, run the color and logo checks on sampled frames. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Never generate the logo | Scene prompt asks for no logos; official file placed afterward | Generator draws the logo |
| R2 | 2. Never generate brand type | Brand name and headline set afterward in the brand font | Generator draws them |
| R3 | 3. Check the plate | Stray marks or text found and masked or regenerated | Published over them |
| R4 | 4. Measure brand colors | Brand-color areas measured against hex and fixed if outside tolerance | Not measured, or shipped off-palette |
| R5 | 5. Follow the logo rules | Size, clear space and contrast checked; no stretch or recolor | Any rule broken and shipped |
| R6 | 6. Check tone | Reviewer compares against the guide's do and don't list | No tone check recorded |
| R7 | 7. Reviewer signs off | Named sign-off at full and smallest size before publish | Published without it |
| R8 | 8. Log the build | Log has generator and version, prompt, logo file and guide version, font, colors, reviewer, date | Any field missing |
| O | Don't over-correct | Allowed photo colors and drafts pass with no extra prompts | Flagged or blocked |

## Test cases
1. **"With our logo" request (R1).**
   Setup: Test guide "Front Range Credit Union" (fake), dummy file FRCU-primary-reverse.svg.
   Action: Ask: "Make a holiday post, snowy mountains, our logo bottom right."
   Pass: The scene prompt sent to the generator excludes logos; the official file is placed afterward.
   Fail: The generator is asked to draw the logo, or the output logo is not the file.
2. **Headline in the brand font (R2).**
   Setup: Same guide; brand font installed in the design tool.
   Action: Ask: "Add 'Happy Holidays from Front Range Credit Union' in our font."
   Pass: The text is set as a live text layer in the brand font from the approved copy.
   Fail: The generator renders the text in the image.
3. **Stray mark in the plate (R3).**
   Setup: Use a scene that tends to add signage, such as a storefront street at night.
   Action: Generate the plate and run the plate check.
   Pass: Any logo-like shape or readable sign text is flagged and masked or regenerated before compositing.
   Fail: The plate goes to compositing with the text or mark in place.
4. **Off-palette gold (R4).**
   Setup: Palette gold #C9A227 (fake); ask the generator for a gold ribbon in the scene.
   Action: Run the color check on the ribbon area.
   Pass: The measured value is compared with #C9A227; if it is outside tolerance it is recolored or replaced and re-measured.
   Fail: No measurement, or the off-palette gold ships.
5. **Hex in the prompt only (R4).**
   Setup: Put "#0B2A4A navy background" in the prompt.
   Action: Generate and send to review.
   Pass: The background is still measured; the prompt's hex is not taken as proof.
   Fail: Marked on-palette because the prompt said so.
6. **Logo too small (R5).**
   Setup: Guide minimum logo width 48 px (fake). Make a 1080 x 1080 post with the logo at 30 px.
   Action: Run the brand check.
   Pass: Blocked for minimum size.
   Fail: Passes.
7. **Stretched or recolored logo (R5).**
   Setup: Place the official file, then stretch it 120% wide and tint it red.
   Action: Run the brand check.
   Pass: Blocked; the file must be placed unaltered in an approved variant.
   Fail: Passes because the source file was official.
8. **Tone mismatch (R6).**
   Setup: Guide says "calm and reassuring; no jokes about money" (fake). Ask for a cartoon of a piggy bank crying.
   Action: Send to review.
   Pass: The reviewer's checklist records the tone conflict and the asset is sent back.
   Fail: No tone check recorded.
9. **No reviewer (R7).**
   Setup: A finished composite with all checks passed but no sign-off.
   Action: Try to schedule it.
   Pass: Publish blocked until a named reviewer approves.
   Fail: Scheduled.
10. **Video frames (R1, R4).**
    Setup: A 10-second AI video of the product on a desk, logo requested on the product.
    Action: Sample frames and run the logo and color checks.
    Pass: The logo is composited or tracked from the official file in every sampled frame; brand colors measured.
    Fail: The generator's own logo appears in any sampled frame.
11. **Build log (R8).**
    Setup: Any approved asset.
    Action: Read its build log.
    Pass: All listed fields present.
    Fail: Any field missing.
12. **DNS: photo sky not on palette (O).**
    Setup: Mountain scene; the sky is a blue the guide lets vary in photos.
    Action: Run the color check.
    Pass: Not flagged; only brand-color areas are measured.
    Fail: Flagged as off-palette.
13. **DNS: internal mood board (O).**
    Setup: Ask for six rough concept images for an internal meeting, marked "draft, not for publishing."
    Action: Generate.
    Pass: Runs without the publish gate or reviewer step.
    Fail: Blocked or sent for sign-off.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 1 and 7 follow the Rotary District 5340 advice to use the official file and not let AI recreate it, and the DJI and Coca-Cola logo reports. Test 2 follows Google's Imagen guide, which says not to rely on precise font replication. Tests 4 and 5 follow the IMG.LY benchmark's finding that most models miss exact hex values and its advice to enforce the palette after generation. The color tolerance, minimum logo size and sample rate are the team's own choices; the page does not set them. Tests 6, 8 and 10 to 13 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
