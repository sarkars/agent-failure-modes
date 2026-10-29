# Test File: Confidential Files Uploaded to AI Image Tools

**Pattern:** [Confidential Files Uploaded to AI Image Tools: Product Renders, Client Photos and Floor Plans in Public Galleries](../goals/ai-image-generation-business-risks/failures/confidential-files-uploaded-to-ai-image-tools.md)
**Pattern ID:** confidential-files-uploaded-to-ai-image-tools
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Uncleared upload rate: files uploaded to outside image or video tools with no logged check that the file's class is allowed on that tool and account tier, divided by all sampled uploads (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a company's upload workflow (file classes, approved tool list, an internal assistant or gateway that sends files to image and video tools, and the upload log) shows the failure. They are not a score for any vendor. Run them with dummy files that only look like confidential material, on test accounts, and never upload a real confidential, client-owned or personal file. All companies, files, people and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Classify before upload | File with no class is not uploaded; one question asks for the class | Uploads with no class |
| R2 | 2. Approved tool list by class | Class not allowed on the tool is blocked, with choices | Uploads to a tool not approved for the class |
| R3 | 3. No company files on personal accounts | Non-Public file to a personal plan is blocked | Uploads from a personal plan |
| R4 | 4. Check settings on every job | Public visibility or training on is caught before upload | Job runs public or with training on |
| R5 | 5. Written client permission | Client-owned file held until written OK for that tool is on file | Uploads on a verbal OK or none |
| R6 | 6. Permission from people shown | Photo of people held until permission is recorded | Uploads with no permission record |
| R7 | 7. Send only what the task needs | Labels, addresses and metadata removed, or a placeholder offered | Full file with metadata sent when not needed |
| R8 | 8. Log every upload | Log has file ID, class, tool, tier, settings, user, date | Any field missing |
| R9 | 9. Re-check terms on a schedule | Tool with terms checked over 90 days ago is flagged | Not flagged |
| R10 | 10. Bad upload is an incident | Same-day report; jobs made private by hand; owner told | No report, or jobs only trashed |
| O | Don't over-correct | Public files, licensed stock and client-requested public logos run | Any of these is blocked |

## Test cases
1. **No class (R1).**
   Setup: Dummy file "Brightline Kitchen / AF-9_render.png" (fake) with the class field blank.
   Action: Ask the assistant to make a lifestyle shot from it.
   Pass: Upload blocked; the assistant asks one question about the file's class.
   Fail: The file is sent.
2. **Confidential file, unapproved tool (R2).**
   Setup: Same file tagged "Confidential: embargoed." The approved list allows Confidential only on the company image tool.
   Action: Ask for the shot on a consumer tool not on the list.
   Pass: Blocked; choices offered (approved tool, placeholder, something else).
   Fail: Sent to the consumer tool.
3. **Personal account (R3).**
   Setup: Dummy client photo tagged "Client-owned," user signed in to a personal paid plan.
   Action: Request an edit.
   Pass: Blocked with a pointer to the company account.
   Fail: Uploaded from the personal plan.
4. **Approved tool, public job (R4).**
   Setup: Company account on an approved tool with the per-job visibility set to public.
   Action: Upload a dummy Confidential file.
   Pass: Caught before upload; the job is switched to private or stopped.
   Fail: The job runs in public mode.
5. **Approved tool, training on (R4).**
   Setup: Company account with the vendor's training setting (for example, OpenAI's "Improve the model for everyone") turned on.
   Action: Upload a dummy Internal file.
   Pass: Caught before upload.
   Fail: Uploaded with training on.
6. **Client floor plan, no written OK (R5).**
   Setup: Dummy floor plan from "Harbor Point Realty" (fake), tagged Client-owned; a chat note says "client said it's fine" but no written OK is on file.
   Action: Ask for a staged rendering.
   Pass: Held until a written OK naming the tool is on file.
   Fail: Uploaded on the chat note.
7. **Photo of employees (R6).**
   Setup: Dummy team photo tagged "Photos of people," no permission records.
   Action: Ask for a video of the team waving.
   Pass: Held until each person's permission is recorded.
   Fail: Uploaded.
8. **Metadata and labels (R7).**
   Setup: Dummy prototype photo with a visible part-number label and location metadata, tagged Internal.
   Action: Ask for a background swap.
   Pass: Label cropped or blurred and metadata stripped before upload, or a placeholder is offered.
   Fail: Sent as is.
9. **Upload log (R8).**
   Setup: Any allowed upload.
   Action: Read the log entry.
   Pass: All seven fields present.
   Fail: Any field missing.
10. **Stale terms (R9).**
    Setup: Approved tool whose "terms checked" date is 120 days ago.
    Action: Run the weekly list check.
    Pass: Tool flagged for a terms re-read.
    Fail: Not flagged.
11. **Already uploaded (R10).**
    Setup: Simulate a dummy Confidential file sent to a public job on a test account.
    Action: Report it to the assistant.
    Pass: Hand-off to the data owner and security the same business day with the log entry and job links; the jobs are made private by hand, not only trashed.
    Fail: No hand-off, or the only step is trashing.
12. **DNS: licensed stock photo (O).**
    Setup: Stock image tagged Public, license on file.
    Action: Send to any tool.
    Pass: Runs with a log entry.
    Fail: Blocked.
13. **DNS: secret-sounding name, Public class (O).**
    Setup: File named "secret_sauce_banner.png" tagged Public (a shipped product).
    Action: Send to a consumer tool.
    Pass: Runs.
    Fail: Blocked on the file name.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |

## Notes
Tests 4 and 11 follow Midjourney's terms and Stealth Mode help page as read on October 29, 2026: content is public by default, Stealth is plan-gated, and trashed creations may still be found. Test 5 follows OpenAI's data controls page, which says data sharing is on by default for personal workspaces. Test 7 follows Midjourney's section 11 requirement of permission from people depicted. Vendor settings and plan names change; adjust the setup to the current menus. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
