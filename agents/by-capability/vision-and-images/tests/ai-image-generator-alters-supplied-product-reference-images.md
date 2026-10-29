# Test File: AI Image Generator Alters Supplied Product Reference Images

**Pattern:** [AI Changed My Product Photo: AI Image Tools That Alter the Product Reference Image You Supplied](../goals/ai-image-brand-guidelines/failures/ai-image-generator-alters-supplied-product-reference-images.md)
**Pattern ID:** ai-image-generator-alters-supplied-product-reference-images
**Goal:** AI images and video a brand publishes follow its brand guidelines: the right logo, colors, fonts, tone and product, nothing from another brand, and nothing unsafe next to its name.
**Primary metric:** Altered-reference rate: sampled published assets built from a supplied product or brand reference image in which the product fails any item on its locked list (shape, part count, color variant, logo, label text), divided by all sampled assets built from a reference (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's workflow (the image tool, the assistant that calls it, the product check, the ad platform settings and the publish gate) changes a supplied product image and lets it run. They are not a score for any vendor. Run them with a dummy product record, dummy packshots and a test ad account. All companies, products, files, people and IDs below are invented. For video, run the same checks on sampled frames. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Write a locked list | Locked list exists from the product record before generating | Generation starts with no list |
| R2 | 2. Composite the product | Product pixels come from the supplied file, or product is masked; scene generated | Whole image regenerated when compositing was possible |
| R3 | 3. Right reference type | Image or object reference used for the product; style reference only for look | Product passed only as a style reference |
| R4 | 4. Check against the supplied file | Every locked item checked against the original file | Not checked, or checked against an earlier output |
| R5 | 5. Fix once, then real photo | One targeted fix, then authentic image in a layout | Repeated re-rolls, or failing item shipped |
| R6 | 6. Platform edits are new outputs | Product-editing enhancements off; any variant checked; live render compared | Variant runs unchecked |
| R7 | 7. Reviewer signs off | Named sign-off with locked-list result attached | Published without it |
| R8 | 8. Log the build | Reference file and source, locked list, tool and version, method, results, reviewer, date | Any field missing |
| O | Don't over-correct | Scene, shadows, allowed crops and drafts pass | Flagged or blocked |

## Test cases
1. **Packshot with no product record (R1).**
   Setup: Upload NW-Tandem-Yellow.png (fake) with no product record linked.
   Action: Ask: "Put this kayak on a lake at sunrise."
   Pass: The assistant asks for the variant or record, or builds the locked list from it, before generating.
   Fail: Generates with no locked list.
2. **New scene request (R2).**
   Setup: Product record: 2 seats, yellow hull, logo on bow.
   Action: Same request with the record linked.
   Pass: Kayak cut out or masked from the packshot; only the lake and sky generated.
   Fail: The whole image, kayak included, is regenerated.
3. **Style reference misuse (R3).**
   Setup: A tool with both style and image reference options.
   Action: Ask: "Use my bottle photo as the style reference and make a beach scene."
   Pass: The bottle goes in as an image or object reference; the assistant says style reference does not carry the product.
   Fail: Bottle passed only as a style reference.
4. **Extra part (R4).**
   Setup: Seed an output where the bike has two sets of handlebars (fake Halverson road bike).
   Action: Run the product check.
   Pass: Part count fails against the supplied file; blocked.
   Fail: Passes.
5. **Chained comparison (R4).**
   Setup: Variation 2 is checked only against variation 1, which already had a slightly wrong cap.
   Action: Run the check.
   Pass: Check re-runs against the original packshot and catches the cap.
   Fail: Variation 2 passes because it matches variation 1.
6. **Label text drift (R4, R5).**
   Setup: Packshot label "Cedar Ridge Cold Brew 12 fl oz" (fake); output label reads differently.
   Action: Run the check, apply one fix, check again.
   Pass: Text mismatch caught; after a second failure the real packshot is placed in a layout.
   Fail: Shipped, or re-rolled more than the team's limit.
7. **Color variant (R4).**
   Setup: Supplied file is the sage green variant; output hull or body drifts to teal.
   Action: Sample product colors.
   Pass: Flagged against the supplied file's sampled color.
   Fail: Passes.
8. **Platform enhancement edits product (R6).**
   Setup: Upload the approved file to a test ad account with image-editing enhancements on.
   Action: Launch to a test audience and capture the live render.
   Pass: Enhancements were turned off before launch, or the live render is compared with the file and the ad paused on a product change.
   Fail: The altered variant runs with no comparison.
9. **Duplicated ad (R6).**
   Setup: Duplicate an approved ad whose enhancements were off.
   Action: Check enhancement settings before publish.
   Pass: Settings re-checked on the duplicate.
   Fail: Not checked.
10. **No reviewer (R7).**
    Setup: Finished asset, all checks passed, no sign-off.
    Action: Try to schedule it.
    Pass: Blocked until a named reviewer approves.
    Fail: Scheduled.
11. **Build log (R8).**
    Setup: Any approved asset.
    Action: Read its build log.
    Pass: All listed fields present.
    Fail: Any field missing.
12. **Video frames (R4).**
    Setup: 8-second AI video made from the kayak packshot.
    Action: Sample frames and run the locked-list check.
    Pass: Every sampled frame checked; any changed seat count or logo caught.
    Fail: Only the first frame checked.
13. **DNS: generated shadow and reflection (O).**
    Setup: Composited kayak with a generated water reflection that shows no logo.
    Action: Run the check.
    Pass: Not flagged; reflection is scene, not product.
    Fail: Flagged as a missing logo.
14. **DNS: placement crop (O).**
    Setup: Platform crops the approved image to 4:5 with the product whole and unchanged.
    Action: Compare live render with the file.
    Pass: Passes as an allowed crop.
    Fail: Ad paused.
15. **DNS: internal mood board (O).**
    Setup: Six rough scene ideas marked "draft, not for publishing."
    Action: Generate.
    Pass: Runs without a locked list or sign-off.
    Fail: Blocked.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 4 and 8 follow the REI case as TechSpot reported it (a vendor image altered by a Meta AI tool to show two sets of handlebars). Tests 1, 5 and 6 follow the Dreamina FAQ's advice to separate what must stay from what may change, compare with the original rather than the previous output, and fall back to the authentic asset. Test 3 follows Midjourney's statement that style reference does not copy objects. Test 2 follows OpenAI's note that masks are guidance only, which is why test 4 still runs after compositing. Test 9 and the color tolerance, re-roll limit and 24-hour live check are the team's own choices; the page does not set them. Tests 7 and 10 to 15 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
