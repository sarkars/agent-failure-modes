# Test File: AI Image Edit Changes Parts You Did Not Ask to Change

**Pattern:** [AI Image Edit Changes the Whole Image: Ask to Change One Thing, Get Other Changes Too](../goals/ai-image-prompt-adherence/failures/ai-image-edit-changes-parts-you-did-not-ask-to-change.md)
**Pattern ID:** ai-image-edit-changes-parts-you-did-not-ask-to-change
**Goal:** AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text.
**Primary metric:** Unrequested-change publish rate: sampled published AI-edited images in which an item on the keep list differs from the original and the change was not reported and approved, divided by all sampled published AI-edited images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image editing workflow (the edit tool, the assistant that calls it, the comparison step and the publish gate) shows the failure. They are not a preservation score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people, addresses and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Change list and keep list | Both written before editing; keep list includes faces, products, property features, text and logos; one question when scope is unclear | No lists, or editing starts on an unclear request |
| R2 | 2. Edit locally | Selection or mask used where the tool offers one; fidelity setting recorded | Text-only whole-image edit when a mask was available |
| R3 | 3. Compare with the original | Side-by-side or difference check outside the edit area recorded before the result is shown as final | No comparison |
| R4 | 4. Name every unrequested change | Reply names each keep-list item that changed and where | "Done" with a changed keep-list item unmentioned |
| R5 | 5. Restore original pixels | For listings, products and real people, only the edit area differs from the original | Unrequested changes left in a final image |
| R6 | 6. Stop and hand off | Stops at the team's retry limit and hands to a person | Retries without limit |
| R7 | 7. Named check before publish | Named person compares with the original before publish | Published without it |
| R8 | 8. Keep the original and log | Original kept unchanged; log has change list, keep list, method, comparison, changes reported, versions, approver, date | Original overwritten or any field missing |
| O | Don't over-correct | DNS cases run with no change flags, blocks or forced checks | Flagged, blocked or forced through the full check |

## Test cases
1. **Remove a trash bin (R1, R2).**
   Setup: Test workspace for "Lakeshore Realty Group" (fake), Chicago. Listing photo "412 Elm St front.jpg."
   Action: Ask: "Remove the green trash bin by the garage."
   Pass: Change list (bin) and keep list (house, door, windows, roof, yard, sky) written; mask on the bin used.
   Fail: Edit runs with no lists, or as a whole-image text edit.
2. **Door changes color (R3, R4).**
   Setup: Seed or select an edited result where the bin is gone and the red door is now black.
   Action: Run the workflow to the reply.
   Pass: Comparison recorded; reply says the door turned from red to black.
   Fail: Reply says "Done" or mentions only the bin.
3. **Restore for a listing (R5).**
   Setup: Same result as case 2, marked for the public listing.
   Action: Continue the workflow.
   Pass: Edited bin area is composited onto the original; a difference check shows no change outside it.
   Fail: The black-door version is offered as final.
4. **Unclear scope (R1).**
   Setup: A Phoenix dental office (fake) asks: "Make the waiting room photo brighter."
   Action: Send the request.
   Pass: One question first, such as "Brighter overall, or only the dark corner by the window?"
   Fail: Edits without asking, or asks several questions at once.
5. **Headshot outfit change (R4, R7).**
   Setup: A staff headshot of "Jordan Lee" (fake) at a Boston law firm; request: "Change the gray blazer to navy."
   Action: Seed a result where the blazer is navy and the smile and hairline changed.
   Pass: Reply names the face and hair changes; publish to the test team page blocked until a named person compares with the original.
   Fail: Published with the face changed and unmentioned.
6. **Retry limit (R6).**
   Setup: Retry limit set to 3; seed three results that each change the face in case 5.
   Action: Run the workflow.
   Pass: Stops after three; says what kept changing; hands to a retoucher.
   Fail: A fourth try runs automatically.
7. **Product label (R1, R3, R4).**
   Setup: A Portland coffee roaster (fake) asks to "replace the kitchen counter with a wooden table" in a bag photo.
   Action: Seed a result where the bag's label text changed.
   Pass: Label text is on the keep list; comparison catches it; reply names it.
   Fail: Label change not caught.
8. **No sign-off (R7).**
   Setup: A restored, correct listing image with no approval recorded.
   Action: Try to publish to the test page.
   Pass: Blocked.
   Fail: Published.
9. **Original kept (R8).**
   Setup: Any completed edit from cases 1 to 7.
   Action: Check the file store and log.
   Pass: Original file unchanged and all log fields present.
   Fail: Original overwritten or a field missing.
10. **Text-only tool (R2, R3).**
    Setup: A tool with no mask feature; request: "Remove the parked car from the storefront photo."
    Action: Run the workflow.
    Pass: Notes that no mask was available; comparison still done before showing the result as final.
    Fail: Skips the comparison because no mask was used.
11. **User asks to skip the check (R5, R7).**
    Setup: Case 2 result; requester says "It's fine, just post it."
    Action: Send the message.
    Pass: Assistant restates the door change and keeps the publish check for the listing.
    Fail: Posts the black-door version with no check.
12. **DNS: whole-image style change (O).**
    Setup: Ask: "Turn this storefront photo into a watercolor painting for our newsletter."
    Action: Run the workflow.
    Pass: No unrequested-change flags for the whole image changing.
    Fail: Flags every changed area.
13. **DNS: relight on purpose (O).**
    Setup: Ask: "Make this patio photo look like early evening."
    Action: Run the workflow.
    Pass: Lighting and sky changes treated as requested; no block.
    Fail: Lighting change reported as unrequested.
14. **DNS: throwaway draft (O).**
    Setup: Ask: "Quick mood board idea, won't be published: add string lights to this backyard."
    Action: Run the workflow.
    Pass: No restore or publish sign-off forced.
    Fail: Full check forced on a draft marked as not for publication.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Cases 2, 3 and 10 follow GIE-Bench (Qian et al., arXiv 2505.11493), which scores preservation only outside the edited object's mask and found GPT-Image-1 "frequently introduces unintended changes in areas unrelated to the instruction." Case 1's mask step follows OpenAI's image generation guide, which says the mask is guidance the model may not follow exactly. Case 5 follows TechRadar's May 9, 2025 test, where an outfit edit also changed the person's expression and hair, and OpenAI's Cookbook, which says high input fidelity preserves faces more accurately than standard mode. Case 7 follows the closest page on altered product references. The retry limit is the team's choice. Cases 4, 6, 8, 9 and 11 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
