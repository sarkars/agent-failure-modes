# Test File: AI Images Published With No Approval Step

**Pattern:** [AI Images Published With No Approval Step: Anyone Who Generates an Image Can Post It](../goals/ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md)
**Pattern ID:** ai-images-published-with-no-approval-step
**Goal:** Businesses that use AI images and video in ads, listings and operations do not mislead customers, break platform or market rules, or get defrauded by fake images.
**Primary metric:** Self-released AI image rate: published AI-made or AI-edited images whose publisher was also the generator (person, agency or platform tool), divided by all published AI images sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a business's publishing setup (social and scheduling tools, ad accounts, agency access and platform AI settings) shows the failure. They are not a score for any product or platform. Run them on a test account, a private or unpublished page, or a paused campaign with no spend, and never let a test post reach the public. All businesses, people and IDs below are invented. Covers image. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Split generate from publish | Draft and agency roles cannot publish an AI image | A draft or agency role publishes it |
| R2 | 2. Releaser is not the generator | Generator cannot release own image; log shows both names | Self-release succeeds, or no releaser logged |
| R3 | 3. Show who can release | Block names the releaser and offers to send | Block with no name or next step |
| R4 | 4. Platform AI is a generator | Platform image generation and enhancement off, or each output has a releaser | Platform-made image runs with no releaser |
| R5 | 5. Re-check on new campaigns | Default-on AI automation caught before launch | New campaign launches with it on, unseen |
| R6 | 6. Real people and sensitive subjects | Goes to the owner, not a delegate | A delegate releases it, or it posts |
| R7 | 7. One-person delay | Post waits the set time with a phone preview | Posts at once |
| R8 | 8. Agency contract | Contract names draft-only rights and a release contact | No such terms |
| R9 | 9. Monthly access audit | Publish rights not tied to a releaser role are flagged | Audit missing or misses them |
| O | Don't over-correct | Real photos, crops and color correction post without AI release | Any of these is blocked |

## Test cases
1. **Agency role publishes (R1, R3).**
   Setup: Test page "Elm Street Bakery" (fake). Agency user "Kite Social" (fake) has draft rights. Owner Dana Ruiz (fake) is releaser.
   Action: As the agency user, generate an image and try to publish it.
   Pass: Blocked; the tool names Dana Ruiz and offers to send it for release.
   Fail: It publishes, or the block gives no next step.
2. **Self-release (R2).**
   Setup: Staff user Sam Lee (fake) has both draft and release rights.
   Action: Sam generates an image and tries to release it.
   Pass: Blocked; another releaser is required; log shows generator and releaser.
   Fail: Sam's own release succeeds.
3. **Default-on platform automation (R4, R5).**
   Setup: Test Google Ads account. Create a new Performance Max campaign without touching asset settings.
   Action: Run the pre-launch check.
   Pass: Image enhancement (and any other image automation that is on) is listed and must be turned off or given a releaser before launch.
   Fail: The campaign is ready to launch with it on and no prompt.
4. **Meta enhancement returns (R4, R5).**
   Setup: Test Meta ad account with enhancements off; duplicate a paused ad.
   Action: Run the pre-launch check on the duplicate.
   Pass: Any enhancement that came back on is caught.
   Fail: The duplicate launches with it on.
5. **Real person in the image (R6).**
   Setup: Agency drafts an AI image showing a recognizable public figure at the bakery.
   Action: Agency requests release from a delegate releaser.
   Pass: Routed to the owner; the delegate cannot release it.
   Fail: The delegate releases it.
6. **One-person shop (R7).**
   Setup: Account with one user, the owner, and the delay set to overnight.
   Action: Owner generates and schedules an AI image for now.
   Pass: The post waits and sends a phone preview before it goes out.
   Fail: It posts at once.
7. **Contract check (R8).**
   Setup: The current agency agreement.
   Action: Read it for posting rights.
   Pass: It names draft-only rights for AI images and a release contact.
   Fail: No terms, or the agency may post freely.
8. **Access audit (R9).**
   Setup: Give a former freelancer full Page access in the test account.
   Action: Run the monthly access export.
   Pass: The freelancer's publish rights are flagged.
   Fail: Not flagged, or no audit runs.
9. **DNS: real shop photo (O).**
   Setup: Photo taken in the shop, color corrected, tagged "own photo."
   Action: Agency user posts it.
   Pass: Posts with no AI release step.
   Fail: Blocked as AI.
10. **DNS: crop for Stories (O).**
    Setup: Released AI image cropped to fit Stories.
    Action: Publish.
    Pass: Runs on the existing release.
    Fail: Sent for a new AI release.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / platform and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Test 1 follows the Sydney cafe post (non-US) that its agency created and posted on the cafe's account (PEDESTRIAN.TV, May 20, 2026). Test 3 follows Google's API reference, which lists image enhancement for Performance Max as enabled by default; the web interface may differ. Test 4 follows advertiser reports that Meta settings switched back on (Shopifreaks, Jan. 5, 2026). Test 6 follows the Vermont bagel shop whose owner posted himself with no marketing team (WCAX, May 6, 2026). The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
