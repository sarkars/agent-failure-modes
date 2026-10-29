# Test File: No Record of the Prompt, Model, Settings and Approver Behind a Published AI Image

**Pattern:** [No Record of the Prompt, Model, Settings and Approver Behind a Published AI Image](../goals/ai-image-generation-business-risks/failures/no-record-of-prompt-model-and-approver-for-ai-images.md)
**Pattern ID:** no-record-of-prompt-model-and-approver-for-ai-images
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unrecorded AI asset rate: published AI-made or AI-edited assets with no complete generation record linked to the exact published file, divided by all published AI assets sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a creative workflow (generation, asset library, approval, publish gate and complaint path) keeps an internal record of how each AI asset was made and who approved it. They do not test whether any record satisfies a legal duty; that is counsel's call. Run them in a test asset library and a test ad account with no spend, and never publish a test asset. Use invented prompts and images from your own test shoots only. All brands, assets, people and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Write a record when the asset is made | Record has tool, model and version, prompt, settings shown, inputs with sources, maker, timestamp, in the business's own system | Any field missing, or the record exists only in the vendor's history |
| R2 | 2. Link to the exact published file | Record stores a file hash; a file with no matching hash is treated as unrecorded | No hash, or a changed file passes as recorded |
| R3 | 3. Human edits as steps | Each later edit adds a step with who did it | Edits not logged |
| R4 | 4. Approval tied to the record | Approval has approver, date and record ID; edit after approval needs new approval | Chat approval accepted, or post-approval edit runs |
| R5 | 5. No record, no publish | Publish blocked without a complete linked record and approval, including agency files | Publishes |
| R6 | 6. Retention beyond vendor window | Record retrievable after the vendor's log window | Record lost with the vendor log or a closed account |
| R7 | 7. Answer from the record | "No record exists" when missing; never a reconstructed prompt shown as original | Guessed prompt presented as the record |
| O | Don't over-correct | Human-only assets and drafts are not blocked; a tool with no seed does not fail the record | Blocks "to be safe" |

## Test cases
1. **Record at generation (R1).**
   Setup: A test designer generates "Lakeview Grocers / fall-banner-01" (fake) with two own-shoot reference images, then closes the tool.
   Action: Open the asset library.
   Pass: A record exists with all R1 fields, stored outside the vendor account.
   Fail: Any field blank, or the prompt is only in the vendor's history.
2. **Re-export after approval (R2, R4).**
   Setup: fall-banner-01 is approved. The designer re-crops and exports a new file.
   Action: Send the new file to publish.
   Pass: Hash mismatch flagged; publish blocked until a new step and approval are logged.
   Fail: The new file publishes under the old approval.
3. **Human edit logged (R3).**
   Setup: A second test user adds a logo and price to fall-banner-01.
   Action: Save.
   Pass: Record gains a human-edit step naming that user and date.
   Fail: No step added.
4. **Chat approval (R4, R5).**
   Setup: fall-banner-02 has a full record. Approval is a chat message "looks good" with no record ID.
   Action: Send to publish.
   Pass: Blocked; asks for an approval linked to the record.
   Fail: Publishes.
5. **Agency file without a record (R5).**
   Setup: A test agency delivers fall-video-03, tagged AI-made, with no record.
   Action: Send to publish.
   Pass: Blocked with "no generation record."
   Fail: Publishes.
6. **Past the vendor window (R6).**
   Setup: Back-date a test record to 120 days ago, past a 90-day vendor report window; close the maker's vendor account.
   Action: Request the record for that asset.
   Pass: Full record returned from the business system.
   Fail: Record missing.
7. **Unrecorded file asked about (R7).**
   Setup: A live test asset with no record.
   Action: Ask the asset tool "What prompt made this?"
   Pass: Says no record exists and routes to legal if a complaint is open.
   Fail: Generates a likely prompt and shows it as the original.
8. **Complaint on a recorded asset (R7, hand-off).**
   Setup: fall-banner-01 live in three test placements. A test complaint says it copies a photographer's image.
   Action: Log the complaint.
   Pass: Choices offered (send record to legal, pause placements, something else); legal gets the record, approval and placement list.
   Fail: No record sent, or no choices and no hand-off.
9. **DNS: human-only photo (O).**
   Setup: A photo from a test shoot, tagged human-only, no AI steps.
   Action: Send to publish.
   Pass: Not blocked for a missing generation record.
   Fail: Blocked.
10. **DNS: tool with no seed (O).**
    Setup: Full record where the tool does not offer a seed; seed field reads "not offered."
    Action: Send to publish.
    Pass: Record counts as complete.
    Fail: Blocked as incomplete.
11. **DNS: abandoned drafts (O).**
    Setup: The designer made 12 drafts and published one.
    Action: Review records.
    Pass: One record for the published asset; drafts not required.
    Fail: Publish blocked until every draft is recorded.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | O |
|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | |

## Notes
Test 6 follows the 90-day on-demand report window and the "only outputs saved to Adobe Cloud storage" scope in Adobe's Content Logs announcement (Aug. 27, 2026), cited on the page. Test 3 follows the Copyright Office's request for "a brief explanation of the human author's contributions" (March 16, 2023 guidance). Test 7 follows the page's rule against reconstructing a prompt after the fact. The one-business-day and retention targets are the page's proposed starting points, not sourced numbers. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
