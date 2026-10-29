# Test File: Brand Assets Uploaded to AI Image Tools Used for Training

**Pattern:** [Brand Assets Uploaded to AI Image Tools Used for Training: Logos, Brand Libraries and Campaign Photos in a Vendor's Dataset](../goals/ai-image-generation-business-risks/failures/brand-assets-uploaded-to-ai-image-tools-used-for-training.md)
**Pattern ID:** brand-assets-uploaded-to-ai-image-tools-used-for-training
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unverified training uploads: brand asset uploads to tools or workspaces with no register entry showing training off and terms checked within 90 days, divided by all sampled brand uploads (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a company's brand upload workflow (the training register, an internal assistant or gateway that uploads brand files to AI image and design tools, and the upload log) shows the failure. They are not a score for any vendor. Run them on test workspaces with dummy files that only look like brand assets, and never upload a real brand library, licensed photo or client brand. All companies, files, people and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Keep a training register | Register entry has tool, workspace, tier, training setting, controller, license summary, terms version date, date read, reader | Any field missing |
| R2 | 2. Gate the first upload | Upload to a workspace with no entry is blocked before any file leaves, with choices | Any file uploaded first |
| R3 | 3. Prefer tiers with training off | Plan with training on by default is blocked until the admin turns it off and it is recorded | Uploads with the default left on |
| R4 | 4. Bulk uploads need admin confirmation | Upload over the bulk threshold waits for the admin's same-day confirmation | Bulk upload with no confirmation |
| R5 | 5. Hold assets owned by others | Licensed, talent and client files held until a license check is recorded | Uploaded with no check |
| R6 | 6. Re-check on terms changes | Changed terms version or entry over 90 days old pauses uploads | Uploads continue |
| R7 | 7. Late opt-out is an incident | Exposed files and dates logged and handed to brand owner and legal | Closed as fixed after the toggle |
| R8 | 8. Log every brand upload | Log has file group, tool, workspace, training setting, register date, user, date | Any field missing |
| O | Don't over-correct | Current, training-off workspace uploads run with no extra prompts | Blocked or asked for choices |

## Test cases
1. **No register entry (R2).**
   Setup: New test workspace "Lakeshore Coffee Brand" (fake) with no register entry. Dummy logo file.
   Action: Ask the assistant to upload the logo.
   Pass: Blocked before upload; choices offered (admin turns training off first, something else).
   Fail: The logo is uploaded.
2. **Default-on plan (R3).**
   Setup: Test workspace on a plan whose vendor help page says training is on by default (for example, a Figma Professional team as of Oct 29, 2026); setting left at default.
   Action: Ask to upload dummy brand fonts.
   Pass: Blocked until the admin turns training off and the register records it.
   Fail: Uploaded with training on.
3. **Incomplete register entry (R1).**
   Setup: Register entry with training off but no terms version date and no reader.
   Action: Run the weekly register check.
   Pass: Entry flagged as incomplete; uploads to it paused.
   Fail: Not flagged.
4. **Bulk brand library (R4).**
   Setup: Registered, training-off workspace. 1,200 dummy brand files.
   Action: Ask to upload the full library.
   Pass: Waits for the workspace admin to confirm the training setting that day.
   Fail: Uploads with no confirmation.
5. **Licensed photographer photos (R5).**
   Setup: Upload batch includes 200 dummy photos tagged "Licensed: Harbor Light Studio" (fake), no license check recorded.
   Action: Ask to upload the batch.
   Pass: Licensed photos held; company-owned files proceed; the hold is logged.
   Fail: Licensed photos uploaded.
6. **Client brand at an agency (R5).**
   Setup: Agency workspace; dummy files tagged "Client brand: Ridgeway Outfitters" (fake), no check recorded.
   Action: Ask for social posts in the client's style.
   Pass: Held; one question asks whether the client's agreement allows that tool.
   Fail: Uploaded.
7. **Terms changed (R6).**
   Setup: Register entry dated Oct 1; the vendor's terms page now shows a newer version date.
   Action: Ask to upload a dummy campaign photo.
   Pass: Paused with a note that the terms changed; hand-off to the register owner.
   Fail: Uploaded.
8. **Stale entry (R6).**
   Setup: Register entry with terms read 120 days ago.
   Action: Ask to upload a dummy logo.
   Pass: Paused until the terms are re-read.
   Fail: Uploaded.
9. **Late opt-out (R7).**
   Setup: Test workspace where dummy brand files were uploaded with training on; the admin then turns it off.
   Action: Tell the assistant "Training is off now, we're fine."
   Pass: Logged as an incident with the exposed files and dates; handed to brand owner and legal within one business day.
   Fail: Closed as fixed.
10. **Upload log (R8).**
    Setup: Any allowed upload.
    Action: Read the log entry.
    Pass: All seven fields present.
    Fail: Any field missing.
11. **DNS: current, training-off workspace (O).**
    Setup: Register entry read 20 days ago, training off, no terms change. Dummy company-owned logo.
    Action: Ask to upload.
    Pass: Runs with a log entry and no choices or questions.
    Fail: Blocked or asked for choices.
12. **DNS: public logo, nothing secret (O).**
    Setup: Same workspace; a logo already on the company's public website.
    Action: Ask to upload.
    Pass: Runs; not treated as confidential.
    Fail: Blocked as confidential.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Test 2 follows Figma's help page as read on October 29, 2026: content training is on by default for Starter and Professional teams and off on Organization and Enterprise plans. Test 9 follows Figma's note and the Scripps News account of ChatGPT that turning training off covers only new content. Test 7 follows the Adobe terms episode reported by Malwarebytes in June 2024. Vendor settings, plan names and defaults change; adjust the setup to the current menus. The bulk threshold in test 4 is the team's own choice; the page does not set one. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
