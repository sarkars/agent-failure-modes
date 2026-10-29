# Test File: AI Product Shots With Garbled Packaging and Label Text

**Pattern:** [AI Product Photo Text Is Garbled: Misspelled Packaging, Labels and Signs in AI Product Shots](../goals/ai-image-brand-guidelines/failures/ai-product-shots-with-garbled-packaging-and-label-text.md)
**Pattern ID:** ai-product-shots-with-garbled-packaging-and-label-text
**Goal:** AI images and video a brand publishes follow its brand guidelines: the right logo, colors, fonts, tone and product, nothing from another brand, and nothing unsafe next to its name.
**Primary metric:** Label-text mismatch rate: published product images in which any readable word on the packaging, label or in-scene signage differs from the approved label copy, divided by all sampled published product images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's product-image workflow (the generator or AI photo editor, the assistant or design tool that composites, the text check and the publish gate) shows the failure. They are not a score for any vendor. Run them with dummy label files, dummy approved copy and a test account only. All companies, products, files, people and IDs below are invented. Covers still images; for video, run the OCR and pixel checks on sampled frames. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting. These tests do not check whether any label meets a law; that needs a qualified reviewer.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Never generate packaging text | Package from label file or real photo; generator makes the scene only | Generator draws the package or its text |
| R2 | 2. Lock the package | Mask applied; no label-area pixel change after edit or combine | Label repainted |
| R3 | 3. Check every readable word | OCR words compared with approved copy; any mismatch blocks | Mismatch published |
| R4 | 4. Regulated panels real or not visible | Panel from label file and legible, or not visible; regulatory reviewer told | Generated panel shown |
| R5 | 5. No invented words on scene signs | Signs blank, masked or approved copy | Generated price or claim left in |
| R6 | 6. Chatbot label copy approved | Copy approved and free of assistant leftovers before art | Leftover line reaches art |
| R7 | 7. Zoomed sign-off | Named reviewer at 100% and marketplace zoom, before publish | Published without it |
| R8 | 8. Log the build | Label file and version, mask, generator and version, OCR result, regulatory review, reviewer, date | Any field missing |
| O | Don't over-correct | Real photos, turned-away panels and drafts pass with no extra prompts | Flagged or blocked |

## Test cases
1. **Lifestyle shot request (R1).**
   Setup: Dummy brand "Crunch Club" (fake), label file CC-wrapper-choc-v7.pdf.
   Action: Ask: "Make a lifestyle shot of our chocolate bar on a picnic blanket."
   Pass: The prompt sent to the generator excludes the product; the wrapper is placed from the label file.
   Fail: The generator draws the wrapper.
2. **Combine three product photos (R2).**
   Setup: Three real product photos, one bar each.
   Action: Ask: "Put all three bars together on a pink counter."
   Pass: Each package is masked; a pixel diff of each label area shows no text change.
   Fail: Any label is repainted by the combine step.
3. **One swapped letter (R3).**
   Setup: Edit a composite so one wrapper reads "0g suger" instead of "0g sugar."
   Action: Run the pre-publish text check.
   Pass: OCR flags the word as not in approved copy; publish blocked.
   Fail: Passes.
4. **Fused words in small print (R3).**
   Setup: A generated bottle whose claim line reads "glutenfreeNon GMO" in small type.
   Action: Run the text check at full size.
   Pass: Flagged as a mismatch against "Gluten Free · Non-GMO."
   Fail: Missed because the front name is correct.
5. **Generated nutrition panel (R4).**
   Setup: A scene where the back of the box faces the camera and the generator drew a Nutrition Facts panel.
   Action: Send to review.
   Pass: Blocked; the panel is replaced from the label file or turned away, and the regulatory reviewer is noted.
   Fail: Published with the drawn panel.
6. **Supplement facts visible from the real file (R4).**
   Setup: A real Supplement Facts panel placed from the label file at legible size.
   Action: Send to review.
   Pass: Passes the text check and is routed to the regulatory reviewer before publish.
   Fail: No regulatory review recorded.
7. **Generated shelf tag (R5).**
   Setup: A grocery-aisle scene where the generator added a price card reading "$1.99 SALE."
   Action: Run the plate and text check.
   Pass: Card masked, blanked or set from approved copy.
   Fail: The generated price ships.
8. **Chatbot leftover in label copy (R6).**
   Setup: Back-panel brand story copy ending "Let me know if you want a version tailored to a specific flavor."
   Action: Submit the copy for label art.
   Pass: The leftover line is caught at copy approval.
   Fail: It reaches the art file.
9. **No reviewer (R7).**
   Setup: A finished product image with all checks passed but no sign-off.
   Action: Try to schedule it and upload it to a marketplace listing.
   Pass: Both blocked until a named reviewer approves at 100% and zoom size.
   Fail: Scheduled or uploaded.
10. **Video frames (R1, R3).**
    Setup: An 8-second AI video of the bar on a desk.
    Action: Sample frames and run OCR on the wrapper.
    Pass: Every sampled frame matches approved copy; the wrapper is composited or tracked from the label file.
    Fail: Any frame shows a drawn or changed word.
11. **Build log (R8).**
    Setup: Any approved product image.
    Action: Read its build log.
    Pass: All listed fields present.
    Fail: Any field missing.
12. **DNS: real photo, OCR misread (O).**
    Setup: A real studio photo of a curved can; OCR reads "Sparklng."
    Action: Run the text check.
    Pass: Flag goes to a person, who confirms against the label file and clears it without regenerating.
    Fail: Blocked outright or sent back to the generator.
13. **DNS: back panel turned away (O).**
    Setup: Scene shows only the front of the box.
    Action: Run the regulated-panel check.
    Pass: Passes; no panel required.
    Fail: Blocked for missing nutrition panel.
14. **DNS: internal concept board (O).**
    Setup: Six rough concepts marked "draft, not for publishing."
    Action: Generate.
    Pass: Runs without the publish gate.
    Fail: Blocked or sent for sign-off.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 1 and 3 follow the Adobe Community reply that text generation is a known limitation and the Google and OpenAI guides' text limits. Test 2 follows the TechSpot report that HallPass used AI to combine product images and the typos came from that step. Test 8 follows the Attack of the Fanboy report of chatbot text printed on a wafer label. Tests 4 to 7 and 9 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph. The OCR tool, sample size and any regulatory requirement are the team's own choices; the page does not set them.
