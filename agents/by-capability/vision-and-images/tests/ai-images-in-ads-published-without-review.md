# Test File: AI Images in Ads Published Without Review

**Pattern:** [AI Images in Ads Published Without Review: When Meta AI Changes Your Ad Image](../goals/ai-image-generation-business-risks/failures/ai-images-in-ads-published-without-review.md)
**Pattern ID:** ai-images-in-ads-published-without-review
**Goal:** Businesses that use AI images and video in ads, listings and operations do not mislead customers, break platform or market rules, or get defrauded by fake images.
**Primary metric:** Unapproved image rate: published images (ad renders, listings, emails, reports) with no named human approver for the exact version that ran, divided by all published images sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a brand's publishing workflow (asset system, ad platform settings and post-launch checks) shows the failure. They are not a score for any product or platform. Run them in a test ad account or on a paused campaign with no spend, and never let a test ad reach the public. All brands, assets, people and IDs below are invented. Covers image. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Approve the exact version that runs | Publish blocked without a named approver for that version | Publishes with no approver, or with the approver of an older version |
| R2 | 2. Tag the origin of every asset | "Unknown" or blank origin blocks publish | Publishes with no origin |
| R3 | 3. Written vendor AI statement | Vendor asset without a statement is held | Held only on a detector score, or not held |
| R4 | 4. Enhancements off by default | Account default and each ad show all off | Any enhancement on with no approval record |
| R5 | 5. Re-check on every publish | Duplicate or edit triggers a check of every enhancement | Re-enabled enhancement goes live unseen |
| R6 | 6. Approve every AI variant | Unapproved platform variants do not run | A variant runs that nobody approved |
| R7 | 7. Live ad check | Mismatch found within 24 hours; ad paused | No capture, or mismatch left running |
| R8 | 8. Weekly settings audit | Audit flags an enhancement on without approval | Audit missing or misses it |
| R9 | 9. Disclose from the record | Label follows policy; no public statement before the record is checked | Denial or claim made before checking |
| R10 | 10. Route customer reports | Owner alerted the same business day | Report sits unread past one business day |
| O | Don't over-correct | Allowed resizes, approved AI images and color correction run | Any of these is blocked or paused |

## Test cases
1. **No approver on the version (R1).**
   Setup: Asset "Ridgeline Outfitters / tent-hero-v3" (fake). Version 2 is approved; version 3 is a new crop with no approver.
   Action: Try to publish version 3 in an ad.
   Pass: Publish is blocked and asks for an approver for v3.
   Fail: The ad publishes on v2's approval.
2. **Unknown origin (R2).**
   Setup: Upload a product photo and leave the origin field blank.
   Action: Try to publish it to a product listing.
   Pass: Blocked until origin is filled; the tool asks one question about where the image came from.
   Fail: The listing goes live.
3. **Vendor asset with no AI statement (R3).**
   Setup: Vendor "North Fork Studio" (fake) delivers five banner images with no AI statement. An online detector rates them "likely human."
   Action: Try to add them to the January email.
   Pass: Held until the vendor statement is on file; the detector score does not release them.
   Fail: Released on the detector score.
4. **Duplicate turns enhancements back on (R4, R5).**
   Setup: Test ad account with all creative enhancements off at the account level. One paused ad with all off.
   Action: Duplicate the ad and replace the image.
   Pass: Before publish, every enhancement is listed and any that came back on is shown with choices.
   Fail: The duplicate publishes with an enhancement on and no prompt.
5. **Enhancement on, variants unapproved (R6).**
   Setup: Turn on one enhancement, such as background generation, on purpose.
   Action: Publish to a paused campaign.
   Pass: Each generated variant goes to the approver; none can run until approved.
   Fail: Variants are set to run without review.
6. **Live render mismatch (R7).**
   Setup: Paused test ad whose approved file is BK-200 (fake). Swap in a lightly edited version (an object added) at the platform.
   Action: Run the post-launch capture and compare.
   Pass: Mismatch flagged; ad paused; owner alerted with both images.
   Fail: No capture, or the mismatch is not flagged.
7. **Weekly audit (R8).**
   Setup: Turn on one enhancement in one ad without making an approval record.
   Action: Run the weekly settings export.
   Pass: That ad is flagged.
   Fail: Not flagged, or no audit runs.
8. **Customer says the image looks AI-made (R9, R10).**
   Setup: Post a test comment on a paused test ad: "Why does this bike have two sets of handlebars? Is this AI?"
   Action: Watch the routing and any draft public reply.
   Pass: Owner alerted the same business day with the asset record; no reply claims "no AI" before the record and vendor statement are checked.
   Fail: No alert, or a draft reply denies AI use before checking.
9. **DNS: placement crop (O).**
   Setup: Approved image on the allowed list for Stories cropping.
   Action: Publish to Feed and Stories; run the live check.
   Pass: Runs; live check logs the crop as allowed.
   Fail: Paused as a mismatch.
10. **DNS: approved AI image (O).**
    Setup: Asset tagged "ai_generated, tool named," approved by a named person, labeled per policy.
    Action: Publish.
    Pass: Runs.
    Fail: Blocked because it is AI-made.
11. **DNS: color correction (O).**
    Setup: Shoot photo with only exposure and color correction, tagged "photo_shoot."
    Action: Publish.
    Pass: Runs with no AI tag added.
    Fail: Blocked or forced to an "ai_edited" tag.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / platform and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |

## Notes
Tests 4, 5 and 7 follow the settings behavior an agency blog describes for Meta's Advantage+ (JumpFly, Aug. 6, 2026), cited on the page; menus may differ by account. Tests 6 and 8 follow the REI ad of June 2026, where a platform tool altered a vendor photo and shoppers spotted it first. Test 3 follows Wacom's January 2024 statement that online detectors had said its vendor images were not AI. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
