# Test File: Approved AI Image Cannot Be Made Again

**Pattern:** [Approved AI Image Cannot Be Made Again: Same Prompt, Different Output](../goals/ai-image-generation-business-risks/failures/approved-ai-image-cannot-be-reproduced.md)
**Pattern ID:** approved-ai-image-cannot-be-reproduced
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unmastered approval rate: approved AI images with no stored master file (original output at full resolution plus its generation record) linked to the approval, divided by all approved AI images sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's asset workflow (master storage, generation record, approval link, variant path, regeneration handling and model-retirement check) shows the failure. They are not a score for any image generator, and they do not test whether a generator returns identical pixels. Run them in a sandbox project with draft assets that never publish. All brands, people and IDs below are invented. Covers image. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Save the master at approval | Original output at full resolution stored before approval is recorded | Screenshot, preview or resized download stored as the master |
| R2 | 2. Save the generation record | Prompt, references, tool, model and version, seed or "not offered", settings, mode, date; library versions and device for self-hosted | Any field missing with no "not offered" note |
| R3 | 3. Approve the master | Approval points at a master ID | Approval points at nothing, or at a preview |
| R4 | 4. Variants from the master | Resize, crop, upscale, extend made from the master with a child ID and changes marked | Variant made by rerunning the prompt |
| R5 | 5. Regeneration is a new image | Rerun gets a new ID with no approval | Rerun inherits the old approval |
| R6 | 6. Sizes in the brief | Listed sizes produced from the master before close | Sizes left for "rerun later" |
| R7 | 7. Re-approve changed areas | Content-changing variant goes back with changes marked | Ships under the old approval |
| R8 | 8. Model retirement check | Live masters on the retiring model listed and confirmed stored | No check run |
| H | Hand-off | Lost master on a live campaign goes to the brand owner; nothing ships as "approved" | Designer regenerates and ships |
| O | Don't over-correct | Plain crops and resizes ship without re-approval; new concepts regenerate freely; seeds allowed for prompt testing | Any of these blocked |

## Test cases
1. **Screenshot as the master (R1, R3).**
   Setup: Designer uploads a 1080-pixel screenshot of image "Harlow Home / HH-101" (fake) and asks for approval.
   Action: Brand lead clicks approve.
   Pass: Blocked; the tool asks for the original output file.
   Fail: Approval recorded against the screenshot.
2. **Record missing the model version (R2).**
   Setup: Master stored with prompt and seed but model field blank.
   Action: Submit for approval.
   Pass: Flagged incomplete; approval waits for the field or a "not offered" note.
   Fail: Accepted.
3. **Tool offers no seed (R2).**
   Setup: Master made on a tool with no seed setting; seed field reads "not offered."
   Action: Submit.
   Pass: Accepted; the note counts as complete.
   Fail: Blocked for a missing seed.
4. **Print size needed (R4).**
   Setup: Approved master HH-101 at 2048 x 2048; printer asks for 300 dpi at 10 x 10 inches.
   Action: Request the print file.
   Pass: Upscaled from the master; child ID HH-101-v2 created.
   Fail: Prompt rerun to get a bigger image.
5. **Same prompt, same seed rerun (R5).**
   Setup: Designer copies the prompt and seed from HH-101 and generates again.
   Action: Try to attach the result to the catalog layout as HH-101.
   Pass: Result gets a new ID with no approval; the tool says a seed may not bring the image back.
   Fail: Attached under HH-101's approval.
6. **Sizes listed in the brief (R6).**
   Setup: Brief lists 1:1, 9:16 and print.
   Action: Close the project after approval.
   Pass: All three exist as children of the master before close.
   Fail: Project closes with only the 1:1.
7. **Canvas extension adds content (R7).**
   Setup: 9:16 extension of HH-101 adds a bookshelf and a second window.
   Action: Send to the ad team.
   Pass: Held; sent to the brand lead with the new area marked.
   Fail: Ships under the old approval.
8. **Model retirement notice (R8).**
   Setup: Vendor announces the model behind three live masters will shut down in 30 days.
   Action: Run the retirement check.
   Pass: All three listed; each confirmed stored or escalated.
   Fail: No list produced.
9. **Lost master on a live campaign (H).**
   Setup: Approved image AD-77 has only a compressed preview; the media buyer needs a new size tomorrow.
   Action: Designer requests the size.
   Pass: Tool stops and sends it to the brand owner with the preview and record; nothing ships as approved.
   Fail: Designer regenerates and ships as AD-77.
10. **DNS: plain crop (O).**
    Setup: 4:5 crop of HH-101 with no new content.
    Action: Send to social.
    Pass: Ships with no new approval.
    Fail: Sent back for approval.
11. **DNS: new concept (O).**
    Setup: Designer starts a winter version with a new prompt.
    Action: Generate several options.
    Pass: Generates freely as new unapproved assets.
    Fail: Blocked because a related approved image exists.
12. **DNS: seed used for prompt testing (O).**
    Setup: Designer locks a seed to compare two prompt wordings.
    Action: Generate both.
    Pass: Allowed with no warning beyond the record.
    Fail: Blocked.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / generator and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | H | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Test 5 follows the Midjourney seeds page, which says seeds "shouldn't be relied on for the same results over different prompting sessions," and the Diffusers reproducibility page. Test 3 follows the Microsoft Q&A answers that DALL-E 3 offered no seed. Test 8 follows the OpenAI developer forum notice of the DALL-E 2 and DALL-E 3 shutdown on May 12, 2026. Test 12 follows Midjourney's advice to lock a seed when testing prompt changes. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
