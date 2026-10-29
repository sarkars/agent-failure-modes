# Test File: Ad Platforms That Reject or Label AI-Generated Ads

**Pattern:** [Ad Platforms That Reject or Label AI-Generated Ads: Meeting Google, Meta and TikTok AI Rules Before Launch](../goals/ai-image-generation-business-risks/failures/ad-platforms-reject-or-label-ai-generated-ads.md)
**Pattern ID:** ad-platforms-reject-or-label-ai-generated-ads
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unchecked platform launch rate: live ads with AI-made or AI-edited creative and no logged per-platform check (rule version read, disclosure setting chosen, who decided) for that exact ad, divided by all live AI-creative ads sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether an advertiser's launch workflow (asset tags, ad platform settings, rule table and rejection routing) shows the failure. They are not a score for any platform. Run them in test ad accounts or on paused campaigns with no spend, and never let a test ad reach the public. Do not submit test political or social issue ads to a live review queue; use a paused draft or a mock of the platform's settings. All brands, assets, people and IDs below are invented. Covers image and video. Platform rules were read on October 29, 2026 (TikTok through an archived copy of May 19, 2026); re-read them before running. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Tag every creative's AI use | Untagged creative cannot be attached to an ad | Attached and published untagged |
| R2 | 2. Classify the ad on each platform | Category recorded per platform (election, social issue, Spark or regular) | Category missing or copied from another platform |
| R3 | 3. Dated rule table | Rule row date logged; row older than 90 days re-read first | No date, or a stale row used |
| R4 | 4. Set each platform's own disclosure field | Required checkbox or toggle set; own in-ad disclosure on non-auto Google formats | Field left off, or only a label burned into the video |
| R5 | 5. No barred platform AI tools | Meta gen AI creative blocked for political or social issue ads | Uploaded |
| R6 | 6. Re-check on duplicate or swap | Reset toggle caught before publish | Duplicate publishes with the toggle off |
| R7 | 7. Do not wait for a platform label | Platform label not counted as the advertiser disclosure | Check passed because the platform "will label it" |
| R8 | 8. Live ad check | Disclosure confirmed on each placement within 24 hours | No capture, or missing disclosure not flagged |
| R9 | 9. Route rejections and labels | Owner alerted same business day with reason, tag and log; no unchanged re-upload | Alert late, or same creative re-uploaded unchanged |
| R10 | 10. Log every check | Log row has ad ID, platform, category, rule date, tag, setting, decider, date | Any field missing |
| O | Don't over-correct | No disclosure added where no rule applies; out-of-scope edits pass; platform label on a disclosed ad does not pause it | Any of these blocked, paused or labeled |

## Test cases
1. **Untagged creative (R1).**
   Setup: Video "Lakeshore Coffee / LC-301" (fake) uploaded with the AI field blank.
   Action: Attach it to a TikTok ad.
   Pass: Blocked; the tool asks one question about whether AI made or changed it and whether it shows a realistic person.
   Fail: The ad is saved ready to publish.
2. **Fully AI-made video, regular TikTok ad (R2, R4, R10).**
   Setup: LC-207 tagged "AI-generated: realistic person." Regular (non-Spark) TikTok ad in a paused campaign.
   Action: Run the pre-launch check.
   Pass: The check names TikTok's rule, the toggle "This ad contains AI-generated content" is set, and a full log row is written.
   Fail: Toggle off, or no log row.
3. **Duplicate resets the TikTok toggle (R6).**
   Setup: Paused TikTok campaign with the AI toggle on for LC-207.
   Action: Duplicate the campaign and keep the same ad.
   Pass: The check finds the toggle off in the duplicate and offers choices before publish.
   Fail: The duplicate is ready to publish with the toggle off and no prompt.
4. **Meta social issue ad made with Meta's gen AI tool (R5).**
   Setup: Mock Meta ad flow for a fake nonprofit's ad about a local transit levy, with an image made in Meta's generative AI ad tool.
   Action: Try to upload.
   Pass: Blocked before upload, with the reason.
   Fail: Uploaded.
5. **Google election ad on a non-auto format (R4).**
   Setup: Mock Google election ad with a synthetic crowd scene, display format (not mobile Feeds, Shorts or in-stream).
   Action: Run the check.
   Pass: "Altered or synthetic content" checkbox set and the advertiser's own prominent disclosure added to the creative.
   Fail: Checkbox only, or neither.
6. **Stale rule row (R3).**
   Setup: Set the TikTok rule row's read date to 120 days ago.
   Action: Launch a TikTok AI ad.
   Pass: Launch waits for a re-read of the rule; the new date is logged.
   Fail: Launches on the stale row.
7. **Relying on the platform label (R7).**
   Setup: Meta political ad (mock) with a realistic AI-generated person made in a third-party tool; disclosure field off; note says "Meta auto-detects AI."
   Action: Run the check.
   Pass: Fails the check until the advertiser disclosure is set.
   Fail: Passes because a platform label may appear.
8. **Live ad check (R8).**
   Setup: Paused TikTok test ad with the toggle on.
   Action: Run the post-launch capture on each placement.
   Pass: Capture logged; a placement with no visible disclosure is flagged.
   Fail: No capture, or the gap is not flagged.
9. **Rejection notice (R9).**
   Setup: Inject a mock rejection: "Ad rejected: missing AI-generated content disclosure."
   Action: Watch routing and the next upload.
   Pass: Owner alerted the same business day with the reason, the AI tag and the check log; the same creative cannot be re-uploaded with no change.
   Fail: No alert, or an unchanged re-upload goes through.
10. **DNS: commercial Google ad with color correction (O).**
    Setup: Real product photo with only color correction, tagged "AI: none," in a non-election Google ad.
    Action: Run the check.
    Pass: Publishes with no disclosure added.
    Fail: Checkbox or AI label added.
11. **DNS: platform label on a disclosed ad (O).**
    Setup: TikTok test ad with the toggle on; the live ad shows "advertiser labeled as AI-generated."
    Action: Run the live check.
    Pass: Logged as expected; ad keeps running.
    Fail: Paused as a mismatch.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / platform and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |

## Notes
Tests 2 and 3 follow TikTok's help page as archived on May 19, 2026, which says duplication resets the AI toggle. Test 4 follows Marketing Brew's November 2023 report that Meta bars its own generative AI tools for political and social issue ads. Tests 5 and 10 follow Google's Political content policy, read October 29, 2026. Test 7 follows Meta's June 2026 statement that third-party AI detection is only beginning. Test 11 uses the label text The Verge reported on Cazoo's TikTok ads. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
