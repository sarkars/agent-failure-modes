# Test File: AI Image Model Update Changes the Approved Style

**Pattern:** [AI Image Model Update Changed My Style: When the Vendor's New Version Breaks the Approved Look](../goals/ai-image-generation-business-risks/failures/ai-image-model-update-changes-approved-style.md)
**Pattern ID:** ai-image-model-update-changes-approved-style
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unpinned job rate: generation jobs for a campaign with an approved style that ran without the approved model version set explicitly, divided by all sampled jobs for such campaigns (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's generation workflow (approved style records, an internal assistant or tool that sends jobs to an image vendor, the asset log and the retirement watch list) shows the failure. They are not a score for any vendor. Run them on test accounts with test campaigns. All companies, styles, people and IDs below are invented. Covers image. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Record the version with the approval | Style with no model version cannot be approved | Approved with no version |
| R2 | 2. Send the version on every job | Job for an approved style carries the version explicitly | Job relies on the default |
| R3 | 3. Check the default before each batch | Default mismatch named before generating, with choices | Runs silently on the new default |
| R4 | 4. Keep a reference set | Style record links 4-8 reference prompts and outputs stored outside the vendor gallery | No reference set, or only in the vendor gallery |
| R5 | 5. Re-test before switching | New version used only after a named person approves a side-by-side | Switched without review |
| R6 | 6. Watch retirement dates | Announced retirement of a version in use triggers a re-test and owner notice | Not flagged |
| R7 | 7. No moving aliases | "Latest" alias rejected in a style record | Accepted |
| R8 | 8. Log the version on every output | Every asset record shows model and version | Any record missing it |
| O | Don't over-correct | Drafts and new campaigns run on the new default; small same-version variation is not blocked | Any of these is blocked |

## Test cases
1. **No version on approval (R1).**
   Setup: Style "PINE-SPRING" (fake) with prompt and style code filled, model version blank.
   Action: Submit for approval.
   Pass: Blocked until the version is filled.
   Fail: Approved.
2. **Job without a version (R2).**
   Setup: Approved style FALL-26 recorded on V7. Account default V7.
   Action: Ask the assistant for 4 images "in the FALL-26 style."
   Pass: Job log shows `--v 7` (or the pinned API snapshot) sent explicitly.
   Fail: No version parameter in the job.
3. **Default changed since approval (R3).**
   Setup: Same style; set the test account default to a newer version.
   Action: Ask for 6 more posts "same as September."
   Pass: The assistant names both versions before generating and offers: approved version, test the new one, something else.
   Fail: Generates on the new default without saying so.
4. **Reference set present (R4).**
   Setup: Any approved style.
   Action: Open the style record.
   Pass: 4-8 reference prompts with approved outputs, version and settings, stored in the company asset system.
   Fail: Missing, or only links to the vendor's gallery.
5. **Switch without review (R5).**
   Setup: Designer edits FALL-26 to use the newer version.
   Action: Save and generate.
   Pass: Blocked until the reference set is re-run on the new version and a named person approves.
   Fail: Saved and used.
6. **Retirement announced (R6).**
   Setup: Add the version in a style record to the watch list as "shutdown date announced, 60 days out."
   Action: Run the weekly watch check.
   Pass: Re-test scheduled and the style owner told the same day, with the date.
   Fail: Not flagged, or flagged only after the date.
7. **Moving alias (R7).**
   Setup: API style record with model `chatgpt-image-latest`.
   Action: Submit for approval.
   Pass: Rejected with a request for a fixed model name or snapshot.
   Fail: Accepted.
8. **Asset log (R8).**
   Setup: Any completed batch.
   Action: Read the asset records.
   Pass: Each record lists model and version.
   Fail: Any record missing it.
9. **Mixed versions in one set (R8, R5).**
   Setup: Campaign with 3 assets on V7 and 3 on a newer version, no switch approval.
   Action: Run the weekly set check.
   Pass: Flagged to the style owner.
   Fail: Not flagged.
10. **DNS: draft exploration (O).**
    Setup: No approved style; designer is exploring ideas.
    Action: Generate on the account default.
    Pass: Runs with no version prompt.
    Fail: Blocked or asked to pin.
11. **DNS: new campaign on the new version (O).**
    Setup: New style "WINTER-27" approved on the current default with its version recorded.
    Action: Generate.
    Pass: Runs.
    Fail: Blocked because the version is new.
12. **DNS: same-version variation (O).**
    Setup: Two batches of FALL-26, both on V7, slightly different compositions.
    Action: Submit both for the set check.
    Pass: Not flagged as a version problem.
    Fail: Flagged as a version change.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 2, 3 and 5 follow Midjourney's Version page as read on October 29, 2026: the version is set with `--v` or a default in settings, and the default moved from V7 to V8.1 to V8.2 between June and July 2026. Tests 6 and 7 follow OpenAI's deprecations page, which lists shutdown dates for DALL-E 2, DALL-E 3 and several GPT Image models, including the `chatgpt-image-latest` alias. Vendor menus and version names change; adjust the setup to the current ones. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
