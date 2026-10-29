# Test File: AI Image Vendor Retires Model or Changes Terms Mid-Campaign

**Pattern:** [AI Image or Video Tool Shut Down Mid-Campaign: When the Vendor Retires the Model or Changes Its Terms](../goals/ai-image-generation-business-risks/failures/ai-image-vendor-retires-model-or-changes-terms-mid-campaign.md)
**Pattern ID:** ai-image-vendor-retires-model-or-changes-terms-mid-campaign
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Campaigns at risk: live campaigns with an asset made on a model or app that has an announced shutdown date and no tested exit plan, divided by all live campaigns (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a company's campaign workflow (the dependency register, an internal assistant or tool that calls image and video models, the asset store and the generation log) shows the failure. They are not a score for any vendor. Run them on a test campaign with dummy assets. You can simulate a retired model by pointing the tool at a model name the vendor no longer serves, or by mocking a model-not-found error. All companies, files, people and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Record the source per asset | Asset record has vendor, product, model, version, terms version date, plan tier; publish blocked if missing | Any field missing and publish allowed |
| R2 | 2. Name dependencies at kickoff | Brief lists every model and app and whether new assets are needed later | Dependency missing from the brief |
| R3 | 3. Watch deprecation notices | Shutdown date logged against every campaign using the model within a week of the notice | Not logged |
| R4 | 4. Keep masters outside the vendor | Master, prompt, settings and inputs saved to company storage at generation | Only copy in the vendor library |
| R5 | 5. Export on notice | Export from the vendor library within 5 business days of notice, count confirmed | Late, or count not checked |
| R6 | 6. Exit plan before launch | Fallback and approver written; replacement output treated as new and sent for approval | Silent swap to another model |
| R7 | 7. Re-check terms on change | New terms version pauses new assets until re-read and logged | Assets keep being made |
| R8 | 8. Don't promise what the vendor controls | Brief or client text promising future work "in the same model" is flagged unless a fallback exists | Not flagged |
| O | Don't over-correct | Current model with no notice runs with a log entry and no extra prompts | Blocked or asked for choices |

## Test cases
1. **Missing asset record (R1).**
   Setup: Dummy hero image in the test campaign "Spring Trail" (fake) with no model or terms fields.
   Action: Ask the assistant to publish it.
   Pass: Blocked; asks for the model and terms record.
   Fail: Published.
2. **Brief with an unlisted tool (R2).**
   Setup: Test brief lists one image API; the asset log shows clips from a video app.
   Action: Run the kickoff check.
   Pass: The video app is flagged as a missing dependency.
   Fail: Not flagged.
3. **Request on a retired model (R6).**
   Setup: Asset record says the spring set was made on `dall-e-3` (removed from OpenAI's API on May 12, 2026, per its deprecations page). Masters stored.
   Action: "Make 3 more summer hero images like the spring set, same prompt."
   Pass: Says the model is retired; offers edit from masters, a replacement re-test for review, or something else.
   Fail: Generates on another model without saying so.
4. **Silent fallback (R6).**
   Setup: Tool configured with an automatic fallback model.
   Action: Send a job naming a model that returns model-not-found.
   Pass: Job stops; any replacement output is marked as a new asset needing approval.
   Fail: Fallback output is delivered under the old approval.
5. **New shutdown notice (R3).**
   Setup: Register lists a model; add a dummy shutdown date for it on the watched page or feed.
   Action: Run the weekly check.
   Pass: Shutdown date logged on every campaign using the model; campaign owner told.
   Fail: Not logged.
6. **Clips only in the vendor library (R4, R5).**
   Setup: 12 dummy clips recorded as stored only in a vendor app library; a shutdown notice is logged.
   Action: Run the export check 5 business days later.
   Pass: Export done, 12 of 12 confirmed in company storage.
   Fail: Clips still only in the vendor library, or count not confirmed.
7. **Master not saved at generation (R4).**
   Setup: Any allowed generation job.
   Action: Read the asset record afterward.
   Pass: Company storage path for master, prompt, settings and inputs present.
   Fail: Only a vendor gallery link.
8. **Terms version changed (R7).**
   Setup: Register entry read Oct 1; the vendor terms page now shows a newer version date.
   Action: Ask for a new campaign image.
   Pass: Paused with a note that terms changed; handed to the register owner, legal for license questions.
   Fail: Generated.
9. **Shutdown inside a live campaign, no exit plan (hand-off).**
   Setup: Campaign ends Aug 31; logged shutdown date is Jul 15; exit plan field empty.
   Action: Run the weekly at-risk check.
   Pass: Sent to the campaign owner within one business day with the register and unexported asset list.
   Fail: Not sent.
10. **Client promise (R8).**
    Setup: Draft client brief says "summer extensions will be made in the same model."
    Action: Ask the assistant to review the brief.
    Pass: Flags the line unless a fallback is written down.
    Fail: Not flagged.
11. **DNS: current model, no notice (O).**
    Setup: Model in the register with no shutdown notice; terms read 20 days ago, no change.
    Action: Ask for 3 new images.
    Pass: Runs with a log entry and no choices or questions.
    Fail: Blocked or asked for choices.
12. **DNS: resize from stored masters (O).**
    Setup: Model retired; masters stored.
    Action: "Resize the 4 spring masters for Instagram Stories."
    Pass: Resizes from masters with no model call and no re-approval prompt for a plain resize.
    Fail: Refuses, or tries to regenerate.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Test 3 follows OpenAI's deprecations page as read on October 29, 2026: DALL-E 2 and DALL-E 3 were removed from the API on May 12, 2026. Test 6 follows OpenAI's Sora help page, which says data is permanently deleted after shutdown and any final export window. Test 8 follows the Adobe terms episode reported by Malwarebytes in June 2024. The 5-business-day export window and weekly check are the page's proposed starting points, not sourced. Price changes are not tested: the page found no opened source on them. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
