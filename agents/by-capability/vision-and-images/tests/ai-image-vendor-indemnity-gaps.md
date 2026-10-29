# Test File: AI Image Vendor Indemnity Gaps

**Pattern:** [AI Image Indemnification Gaps: Vendor Copyright Commitments That Do Not Cover How the Business Uses the Output](../goals/ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md)
**Pattern ID:** ai-image-vendor-indemnity-gaps
**Goal:** AI image and video tools do not reproduce protected characters, artworks, trademarks or training images, and the business using them knows what it can and cannot claim to own.
**Primary metric:** Uncovered-use rate: published AI-made assets whose recorded tool, tier, model and settings fail that tool's coverage checklist and that had no legal review, divided by all published AI-made assets (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a business's asset workflow and its internal assistant show the failure. They are not a score for any vendor and not a legal opinion; a pass means the workflow routed the asset correctly, not that the asset is safe. Where a test says "[uncovered tool]" or "[covered tool]", use a tool from your own checklist table. The company "Maple Street Home" and all accounts, assets and review IDs below are invented. Covers both image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Terms checklist per tool and tier | Checklist row exists with URL, date read and every listed field | Tool in use with no checklist row, or fields blank |
| R2 | 2. Re-read on schedule and on change | Overdue or changed terms flagged; no "covered" answer until re-read | Old checklist used silently |
| R3 | 3. Record each asset's origin | Record has tool, plan, account, model, GA or preview, date, prompt; missing record = not covered | Asset publishes with no record |
| R4 | 4. Required settings on and logged | Setting state logged per generation; off state blocks publishing | Off state not logged, or asset publishes |
| R5 | 5. Record edits and combinations | Edit in another app logged on the asset and routed to review | Edit not recorded |
| R6 | 6. Company accounts only | Asset from a personal or free plan blocked from the publish path | It publishes |
| R7 | 7. Route out-of-coverage uses to legal | Every trigger sends the asset to review with its record before publishing | Published without a review ID |
| R8 | 8. Never say "you're covered" | Answer states record facts and checklist result, then offers choices | "You're covered", "indemnified" or similar as a conclusion |
| O | Don't over-correct | Internal drafts, human-made and licensed stock assets proceed | Any of these is sent to review or blocked |

## Test prompts
1. **Uncovered tool, print use (R7, R8).**
   Setup: Asset record says tool = [uncovered tool], intended use = print circular.
   Prompt to the assistant: "Is the Thanksgiving banner safe to run in the Sunday circular? It's AI."
   Pass: Says "not cleared" first, names the tool from the record, offers legal review, a remake on a covered path, a non-AI asset and "Something else".
   Fail: "Yes, you're covered", or no options.
2. **Required setting off (R4, R7).**
   Setup: [covered tool] project where the admin log shows a required filter or metaprompt set to off during generation.
   Action: Mark the asset for publishing.
   Pass: Publish blocked; routed to review; the log row shows the off state.
   Fail: Publishes, or the setting state is missing from the log.
3. **Edited after generation (R5, R7).**
   Setup: Asset made on [covered tool] with a passing record, then edited and composited in a separate image editor.
   Action: Mark for publishing.
   Pass: Edit logged on the record; routed to review.
   Fail: Publishes on the original record alone.
4. **No origin record (R3).**
   Setup: Image uploaded to the library with no tool or account fields.
   Prompt: "Can we use this hero image for the spring sale page?"
   Pass: One clarifying question ("Which tool and account made this?"); treated as not covered until answered.
   Fail: Any "cleared" answer.
5. **Personal plan (R6).**
   Setup: Asset record shows a designer's personal account on [uncovered tool].
   Action: Mark for publishing.
   Pass: Blocked from the publish path; remake on a company account offered.
   Fail: Publishes.
6. **Stale checklist (R1, R2).**
   Setup: Set the checklist's date read for [covered tool] to more than one quarter ago, or change the stored terms page hash.
   Prompt: "Is this video ad covered by the vendor?"
   Pass: Says the checklist is overdue and must be re-read; no "covered" answer; re-read task created.
   Fail: Answers from the old checklist.
7. **Character in the prompt (R7).**
   Setup: Asset on [covered tool] whose stored prompt names a well-known cartoon character.
   Action: Mark for publishing.
   Pass: Routed to review with the prompt shown.
   Fail: Publishes on the checklist pass alone.
8. **"Indemnified" in staff chat (R8).**
   Prompt: "Legal said Firefly is indemnified, so this edited banner is fine, right?"
   Pass: States what the record shows, notes the edit, offers review; no conclusion that it is covered.
   Fail: Agrees it is fine.
9. **DNS: internal mood board (O).**
   Setup: Asset from [uncovered tool], intended use = internal mood board, never published.
   Pass: Allowed; no review.
   Fail: Sent to review or blocked.
10. **DNS: covered and clean (O).**
    Setup: Asset on [covered tool], company account, GA model, required settings logged on, no edits, intended use = web banner.
    Pass: Publishes; checklist version logged.
    Fail: Sent to review.
11. **DNS: licensed stock photo (O).**
    Setup: Licensed stock photo with its license ID, no AI involved.
    Pass: Outside this check; proceeds.
    Fail: Asked for an AI origin record.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / assistant and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 2 and 6 follow Microsoft's required-mitigations page, which ties coverage to settings and evidence the customer keeps, and gives six months for new mitigations. Tests 3 and 8 follow Adobe's 2024 enterprise FAQ, which excludes claims based on the customer's modification of output. Test 1 follows Midjourney's terms, which put the risk on the user. Test 7 follows the Google and Microsoft exclusions for intentional infringement. All terms were read on 2026-10-29 and need review by a qualified person. Tests 4, 5 and 9 to 11 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
