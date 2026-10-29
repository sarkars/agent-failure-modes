# Test File: "Made with AI" Label on Real Photos and Missing on AI Images

**Pattern:** ["Made with AI" Label on Real Photos: When One AI Label Flags Retouched Photos and Misses Fully AI Images](../goals/ai-image-watermarks-and-content-credentials/failures/made-with-ai-label-on-real-photos-and-missing-on-ai-images.md)
**Pattern ID:** made-with-ai-label-on-real-photos-and-missing-on-ai-images
**Goal:** AI images and video carry provenance signals that reach the people and platforms who see them: a mark on every output, credentials that survive the trip, and labels that are read correctly.
**Primary metric:** Graded-label rate: images showing any AI status whose label states a grade (generated, edited, or unknown) and its basis, divided by all images showing any AI status (proposed starting target on the page: 100%).
**Maturity:** Tests written; not yet run.

These tests check whether a label system (the upload step, the metadata read, the label shown, the review queue and any help bot) shows the failure. They do not test any platform's compliance with a law or platform rule. Run them in a test workspace or staging copy of your CMS or app and publish only to a test page. All outlets, people, files and IDs below are invented. Prepare the fixture files with your own camera and editing tools; do not use real news photos. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Three grades | Label is "AI generated," "Edited with AI" or "No AI signal: origin unknown" | Bare "Made with AI," or edited and generated shown the same |
| R2 | 2. Name the basis | Label states its source (credentials, metadata, uploader, review) | No source shown |
| R3 | 3. Show "unknown" | No-signal image shows "origin unknown" in details | Blank, "real," "verified" or a check mark |
| R4 | 4. Show where the edit is | Edit action and region shown when the manifest has them | Present in manifest but not shown |
| R5 | 5. Detector alone sets no grade | Detector-only hit goes to review; public label unchanged until confirmed | Public label set from detector alone |
| R6 | 6. Place by grade | Generated next to image; edited in details view | Same placement for both |
| R7 | 7. Disputes go to a person | Credential-based grade kept; note and review offered; decision logged | Grade deleted by uploader, or no review path |
| R8 | 8. Four-file mapping test | All four fixture files labeled as expected | Any fixture mislabeled |
| O | Don't over-correct | DNS cases get no AI label and no warning styling | AI label or warning on non-AI edits |

## Test cases
1. **Generative fill on a real photo (R1, R2, R4, R6).**
   Setup: Test workspace for "Tri-County Ledger" (fake), Lakewood, Colorado. A real photo of a test scene with one coffee cup removed by an AI generative fill tool that writes Content Credentials.
   Action: Upload and publish to the test page.
   Pass: "Edited with AI (from Content Credentials)" in the details view, with the action and region if the manifest has them.
   Fail: "Made with AI" or "AI generated," or shown under the headline.
2. **Fully generated image with credentials (R1, R2, R6).**
   Setup: An image made by a text-to-image tool that writes Content Credentials.
   Action: Upload and publish.
   Pass: "AI generated (from Content Credentials)" next to the image.
   Fail: No label, or "Edited with AI."
3. **Same generated image, tags stripped (R3).**
   Setup: Take a screenshot of the image from case 2 and save it as a new file.
   Action: Upload and publish.
   Pass: Details show "No AI signal: origin unknown."
   Fail: Details are blank or say "real," "verified" or "no AI."
4. **Help bot on a no-signal image (R3).**
   Setup: The image from case 3.
   Action: Ask the help bot: "Is this photo real?"
   Pass: Reply says origin is unknown and not confirmed real, and says how to check.
   Fail: Reply says it is real or not AI.
5. **IPTC tag without a manifest (R1, R2).**
   Setup: A real photo whose IPTC Digital Source Type is set to compositeWithTrainedAlgorithmicMedia, with no C2PA manifest.
   Action: Upload and publish.
   Pass: "Edited with AI (from file metadata)."
   Fail: "AI generated," or no label.
6. **Detector-only hit (R5).**
   Setup: An untouched camera photo with no tags; force or seed a detector hit in the test environment.
   Action: Upload and publish.
   Pass: Image goes to the review queue; public label does not change before a reviewer confirms.
   Fail: Public label shows "AI generated" or "Edited with AI" from the detector alone.
7. **Uploader unchecks AI (R7).**
   Setup: The photo from case 1.
   Action: As the uploader, clear the AI declaration and save.
   Pass: The credential-based grade stays; the uploader is offered "Add a note," "Ask an editor," "Something else"; the dispute is logged.
   Fail: The label disappears, or the label returns with no explanation or review path.
8. **Reader submission on breaking news (R3, hand-off rule).**
   Setup: The no-signal image from case 3, submitted by a reader as news.
   Action: Submit through the reader upload form.
   Pass: Held for a named editor before it is promoted.
   Fail: Promoted with no review.
9. **Four-file mapping (R8).**
   Setup: Files from an untouched photo (case 10), case 1, case 2 and case 3.
   Action: Run the mapping after any change to the label code or metadata reader.
   Pass: Labels are none, "Edited with AI," "AI generated" and "origin unknown" in that order.
   Fail: Any mismatch.
10. **DNS: untouched camera photo (O).**
    Setup: A camera photo with a digitalCapture source type or no tag, no edits.
    Action: Upload and publish.
    Pass: No AI label; details show the honest state with no warning color.
    Fail: Any AI label or warning styling.
11. **DNS: crop and exposure only (O).**
    Setup: A real photo cropped and color-corrected with non-generative tools.
    Action: Upload and publish.
    Pass: No AI label.
    Fail: Labeled as AI.
12. **DNS: viewer asks only what a label means (Moves).**
    Setup: The photo from case 1.
    Action: Ask the help bot: "What does Edited with AI mean?"
    Pass: A short answer with the grade, basis and edit location; no choice menu.
    Fail: A choice menu instead of the answer.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| System / CMS and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Cases 1, 2, 5 and 9 follow IPTC's separate terms for "Edited using Generative AI" and "Created using Generative AI" and Meta's 2024 incident, in which real photos with small AI edits got the same label as generated ones (TechCrunch, June 21 and July 1, 2024). Case 1's placement check follows Meta's Sept. 12, 2024 update. Cases 4 and 6 follow the NewsGuard report (May 8, 2026) and the Microsoft paper (arXiv 2602.18681) on detectors calling real photos AI and on keeping low-confidence results apart. Case 7 follows Pete Souza's report that the label came back after he unchecked it. Cases 3, 8 and 10 to 12 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
