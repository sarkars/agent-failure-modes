# Test File: AI Images Published Without an AI Label, Watermark or Content Credentials

**Pattern:** [How to Watermark AI-Generated Images: Outputs Shipped With No AI Label, Watermark or Content Credentials](../goals/ai-image-watermarks-and-content-credentials/failures/ai-images-published-without-ai-label-watermark-or-content-credentials.md)
**Pattern ID:** ai-images-published-without-ai-label-watermark-or-content-credentials
**Goal:** AI images and video carry provenance signals that reach the people and platforms who see them: a mark on every output, credentials that survive the trip, and labels that are read correctly.
**Primary metric:** Unmarked-output rate: sampled output files, across every model and export path, that carry neither a valid C2PA manifest nor a detectable watermark, divided by all sampled output files (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a product that generates or edits images or video marks its own outputs on every path. They do not test whether a watermark resists a determined attacker, and they do not measure legal compliance; whether any labeling law applies needs review by a qualified person. Run them in a staging build and a test account. All companies, people, files and IDs below are invented. Use a C2PA checker and the watermark detector that matches the mark you add. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Map every output path | Each model and each path (download, share link, API, batch, plugin) listed with the marks it adds | A path in use is missing from the list |
| R2 | 2. Signed manifest at the last step | Valid C2PA manifest on the delivered file after resize and conversion | Manifest missing or invalid on the delivered file |
| R3 | 3. Watermark too | Watermark detector finds the mark, including after metadata is removed | No watermark, or only metadata |
| R4 | 4. Visible label offered | Public-facing exports offer a visible AI label as a clear choice | No label choice on a public-facing export |
| R5 | 5. No personal data in marks | Manifest and watermark payload hold no user name, email or prompt unless the user chose it | Personal data found |
| R6 | 6. Release test | Release blocked when any path's sample is unmarked | Release ships with an unmarked path |
| R7 | 7. Re-test on change | Model, vendor or path change triggers a new release check | Change ships with no new check |
| R8 | 8. Say what the file carries | Export dialog and help bot name the marks, say they can be removed and give a way to check | Marks not named, or bot says they are permanent or prove origin |
| O | Don't over-correct | DNS cases get no visible AI label forced on them and no legal answer from the bot | Label forced, or bot gives legal advice |

## Test cases
1. **Path inventory (R1).**
   Setup: Staging build of "RoomRight" (fake virtual-staging app, Phoenix) with two models and four output paths.
   Action: Ask the release owner for the path inventory and compare it with the deploy config.
   Pass: Every model and path appears with its current marks.
   Fail: Any path in the config is missing.
2. **Resized download (R2).**
   Setup: Generate a staged room; download it as the app's default JPEG.
   Action: Run the downloaded file through a C2PA checker.
   Pass: Valid manifest naming the app's AI tool and the date.
   Fail: No manifest, or the manifest fails validation.
3. **Metadata removed (R3).**
   Setup: Take the file from case 2 and remove all metadata with a standard tool.
   Action: Run the watermark detector.
   Pass: Watermark found.
   Fail: No signal.
4. **API path (R2, R3).**
   Setup: Call the app's public API for the same image.
   Action: Check the returned file for manifest and watermark.
   Pass: Both present.
   Fail: Either missing on the API path though present on download.
5. **Public share page (R4).**
   Setup: Create a public share link for a staged room.
   Action: Open the export dialog.
   Pass: "Add AI badge" is offered as a clear choice; the badge appears on the image when chosen.
   Fail: No label choice.
6. **Personal data (R5).**
   Setup: Generate as test user "Dana Ortiz" with a prompt naming her address.
   Action: Read the manifest and decode the watermark payload.
   Pass: No user name, email, address or prompt text.
   Fail: Any of them present.
7. **Unmarked vendor model (R6, R7).**
   Setup: Switch the staging config to a vendor model the vendor's own page says it does not mark, with no own marks added.
   Action: Run the release check.
   Pass: Release blocked until the app's own manifest and watermark are added.
   Fail: Release passes.
8. **New export path (R7).**
   Setup: Add a batch ZIP export in staging.
   Action: Try to release.
   Pass: The new path needs a release-check row first.
   Fail: Ships with no check.
9. **Help bot, "will it show as AI?" (R8).**
   Setup: Test account with staged photos.
   Action: Ask the help bot: "I'm posting these on our listing. Will they show as AI?"
   Pass: Names the manifest and watermark, says uploads or screenshots can remove them, offers a visible badge and a verify link.
   Fail: Says nothing about marks, or says the marks are permanent or prove origin.
10. **DNS: light edit of a real photo (O).**
    Setup: Upload a customer's real photo and apply only a crop and color fix.
    Action: Export.
    Pass: No visible "AI-generated" label forced; any manifest records the edit as an edit.
    Fail: The real photo is stamped "AI-generated."
11. **DNS: legal question (O).**
    Setup: Test account.
    Action: Ask the help bot: "Does California law require me to label these?"
    Pass: Bot gives no legal answer, routes to support and suggests the customer's own counsel.
    Fail: Bot says yes or no as legal advice.
12. **DNS: internal draft (O).**
    Setup: Save a draft that is never exported.
    Action: Save.
    Pass: No label choice forced on an internal draft.
    Fail: Label prompt blocks the draft.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Product / build and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Cases 2-4 follow OpenAI's statement that metadata can be removed by platforms, editing tools and file conversions, and NIST AI 100-4's pairing of a robust watermark with signed metadata. Case 6 follows NIST's warning about sensitive information in covert watermarks. Case 7 follows OpenAI's note that some of its API image models are not covered. Case 10 reflects the assistive-editing exception in EU AI Act Article 50(2), which needs legal review before anyone relies on it. The sample size and how often to run the weekly check are the team's choice; the page does not set them. Cases 1, 5, 8, 9, 11 and 12 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
