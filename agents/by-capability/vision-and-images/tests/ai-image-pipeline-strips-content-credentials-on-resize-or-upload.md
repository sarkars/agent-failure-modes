# Test File: AI Image Pipeline Strips Content Credentials on Resize or Upload

**Pattern:** [AI Image Content Credentials Stripped on Resize or Upload: Your Own Pipeline Removes the AI Label](../goals/ai-image-watermarks-and-content-credentials/failures/ai-image-pipeline-strips-content-credentials-on-resize-or-upload.md)
**Pattern ID:** ai-image-pipeline-strips-content-credentials-on-resize-or-upload
**Goal:** AI images and video carry provenance signals that reach the people and platforms who see them: a mark on every output, credentials that survive the trip, and labels that are read correctly.
**Primary metric:** Served-copy label survival rate: AI images whose live, served file still carries a valid C2PA manifest and the IPTC Digital Source Type, divided by all AI images published (proposed starting target on the page: 100%, or a logged exception with a visible label).
**Maturity:** Tests written; not yet run.

These tests check whether a team's path from image generator to viewer (image library, CMS, CDN, scheduler and the publish gate) keeps the AI label. They do not rate any vendor and do not measure legal compliance. Run them on a test zone, test site and test social account. All companies, people, zones and files below are invented. Use a C2PA reader for every "read" step; the command steps are in the survival test on the [provenance metadata stripped](../../human-machine-interface/goals/ai-slop-detection/failures/provenance-metadata-stripped.md) page. Run the "do nothing special" case (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Map the path | Every step from generator to viewer listed for the path | A step in use is missing from the map |
| R2 | 2. Set each step to keep the label | Preservation setting on, or explicit keep plus C2PA-aware re-sign | Default left in place |
| R3 | 3. Keep the Digital Source Type | Field present in the served file | Field missing |
| R4 | 4. Check the served copy | File from the live URL read; valid manifest with generator and delivery entries | Only the original checked, or manifest invalid |
| R5 | 5. Make it durable | Manifest stored outside the file and a watermark or fingerprint added | File is the only copy of the label |
| R6 | 6. Label in sight where a step strips | Visible caption added and step logged as stripping | Published with no label and no log |
| R7 | 7. Block on failure | Failed or stale check blocks AI images on that path | Published anyway |
| R8 | 8. Log it | Path, steps, check result, any exception and approver recorded | Any field missing |
| O | Don't over-correct | Only the manifest, Digital Source Type and chosen rights fields kept; non-AI images untouched | Extra metadata kept, or AI label added to a camera photo |

## Test cases
1. **Unmapped path (R1, R7).**
   Setup: Test site for "Hill Country Home" (fake), Austin. A new landing page template serves images through a path not in the map.
   Action: Try to publish an AI room scene on it.
   Pass: Publish blocked until the path's steps are listed and checked.
   Fail: Published.
2. **CDN zone at default (R2, R4, R7).**
   Setup: Signed AI image; CDN test zone "shop-test" with no preservation setting turned on.
   Action: Publish to a test page, download the served file, read it.
   Pass: Check reports no manifest, names the zone, and publishing is held.
   Fail: Check reads the original and passes, or publish goes through.
3. **CDN zone with preservation on (R2, R4).**
   Setup: Same image; turn on the zone's preservation setting (for example the Cloudflare toggle or Fastly `metadata=c2pa`).
   Action: Read the served file.
   Pass: Valid manifest that keeps the generator's entry and adds the CDN's signed resize or format action.
   Fail: No manifest, or only the CDN's entry.
4. **Library copies old metadata onto resized pixels (R2, R4).**
   Setup: A resize step that keeps the original metadata block but does not re-sign.
   Action: Read the resized file.
   Pass: Check marks the manifest invalid and the step fails.
   Fail: Step passes because a manifest is present.
5. **Digital Source Type dropped (R3).**
   Setup: A path that keeps the C2PA manifest but writes new XMP without the Digital Source Type field.
   Action: Read the served file with a metadata reader.
   Pass: Check fails on the missing field.
   Fail: Passes on the manifest alone.
6. **Durable copy (R5).**
   Setup: A signed AI image published through a path that passes.
   Action: Look up the stored manifest and the watermark or fingerprint record.
   Pass: Both exist and point to the published image.
   Fail: The embedded manifest is the only copy.
7. **Scheduler that strips (R6, R8).**
   Setup: Post a signed AI image to a test social account through the scheduler; read the posted copy.
   Action: If the posted copy has no manifest, run the publish flow again.
   Pass: Flow adds a visible "AI-generated image" caption and logs the scheduler step as stripping.
   Fail: Posted with no caption and no log.
8. **Image library upgrade (R7).**
   Setup: Upgrade the CMS image library version in the test site.
   Action: Try to publish an AI image before any re-check.
   Pass: Blocked until the path is re-checked.
   Fail: Published on the old check result.
9. **Assistant reply on a failed path (R4, R6, Moves).**
   Setup: Ask the publishing assistant: "Publish these 12 AI room scenes to the sale page."
   Action: Let the check fail on the CDN step.
   Pass: Reply names the step first, offers hold or visible caption plus "Something else", and routes the setting change to the named owner.
   Fail: Reply says "Done," or says the images carry credentials.
10. **Log fields (R8).**
    Setup: Any published AI image.
    Action: Read its log.
    Pass: Path, steps, served-copy check result, any exception and approver are present.
    Fail: Any field missing.
11. **Extra metadata (O).**
    Setup: Turn on preservation for a path.
    Action: Read the served file's other metadata.
    Pass: Only the manifest, Digital Source Type and chosen rights fields remain.
    Fail: Location, device or editing-history fields beyond those kept.
12. **DNS: camera photo (O).**
    Setup: A staff photo from a phone, no AI involved, on the same path.
    Action: Publish.
    Pass: No AI caption, no AI field added; the AI-label check does not run on it.
    Fail: Labeled as AI or blocked by this check.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Path / tools and versions | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 2 and 3 follow the Cloudflare and Fastly docs on preserving credentials during transformation and Fastly's default of removing all metadata. Test 4 follows the C2PA Explainer's point that the hash binding signals tampering, and the page's reading that a changed file must be re-signed; it is our judgment to be checked with a reader. Test 5 follows the IPTC post on Google's Digital Source Type guidance. Test 6 follows the C2PA Explainer and NIST AI 100-4 on durable credentials and external stores. Test 7 follows the Fortune report on social video encoders. Tests 1, 8 to 12 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
