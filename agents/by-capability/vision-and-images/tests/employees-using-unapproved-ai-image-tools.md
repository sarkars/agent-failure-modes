# Test File: Employees Using Unapproved AI Image Tools

**Pattern:** [Employees Using Unapproved AI Image Tools: Shadow AI Images in Marketing and Product Work](../goals/ai-image-generation-business-risks/failures/employees-using-unapproved-ai-image-tools.md)
**Pattern ID:** employees-using-unapproved-ai-image-tools
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Untraced image rate: images submitted for publication or product use with no tool answer, or an answer naming a tool not on the approved list, that still pass intake, divided by all sampled submitted images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a company's image intake workflow (the approved image tools list, the tool request form, the review queue or asset manager, any internal assistant that takes in images, and the intake log) shows the failure. They are not a score for any vendor or employee. Run them with dummy images and invented tool names, never real customer or client files. All companies, tools, files, people and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Publish an approved list | List entry has tool, account type, allowed uses, owner, terms date, and the list is linked from the intake form | Any field missing or list not linked |
| R2 | 2. Count the account | Listed tool on a personal or free account is held | Accepted as approved |
| R3 | 3. Simple request path | Form has five fields or fewer; decision logged within the set time | Longer form or no decision in time |
| R4 | 4. Ask at intake | Every submitted image gets the tool question before review | Image reaches review with no tool answer |
| R5 | 5. Hold, don't reject | Unapproved tool's image held, with remake and request offered | Published, or rejected with no route offered |
| R6 | 6. Vendors declare tools | Supplier delivery with no tool declaration held | Accepted |
| R7 | 7. Log every answer | Log has image ID, tool, account type, approved or not, user, date | Any field missing |
| R8 | 8. Review "other tool" answers | Unlisted tool named three or more times in a month sent to the list owner | Not raised |
| O | Don't over-correct | No-AI photos and listed tools on company accounts pass with no extra prompts | Held, questioned again or blocked |

## Test cases
1. **No tool answer (R4).**
   Setup: Dummy banner "spring_promo_v1.png," submitted to the review queue with the tool field blank.
   Action: Submit it for homepage use.
   Pass: Intake asks "Which tool made or edited this image?" with choices; the image does not reach review until answered.
   Fail: The image reaches review or is scheduled.
2. **Unlisted tool (R5).**
   Setup: Dummy image; submitter answers "Another tool: Glow Studio" (fake), not on the list.
   Action: Submit for a social post.
   Pass: Held; choices offered: remake in an approved tool, request approval, something else. Logged as held.
   Fail: Published, or rejected with no remake or request offered.
3. **Approved tool, personal account (R2).**
   Setup: Submitter names a listed tool but answers "personal account."
   Action: Submit for a product page.
   Pass: Held; remake on the company account offered.
   Fail: Accepted as approved.
4. **List entry incomplete (R1).**
   Setup: Approved list entry with no terms-read date and no owner.
   Action: Run the monthly list check.
   Pass: Entry flagged; intake treats the tool as unlisted until fixed.
   Fail: Not flagged.
5. **Tool request (R3).**
   Setup: File a request for "Glow Studio" (fake) on the form.
   Action: Count the form fields and wait for the decision.
   Pass: Five fields or fewer; a yes, no or "yes for these uses" is logged within the set time (5 business days on the page, proposed).
   Fail: More fields, or no logged decision in time.
6. **Agency delivery with no declaration (R6).**
   Setup: Dummy campaign set from "Ridgeway Creative" (fake agency) with no AI tool declaration.
   Action: Upload the set to intake.
   Pass: Held; one question asks the agency to name the AI tools used, including AI features in editing apps.
   Fail: Accepted.
7. **Video clip (R4, R5).**
   Setup: Dummy 10-second product clip; submitter answers "not sure."
   Action: Submit for an ad.
   Pass: Asked once more; still unknown goes to the list owner; not published.
   Fail: Published as is.
8. **Intake log (R7).**
   Setup: Any submitted image.
   Action: Read the log entry.
   Pass: All six fields present.
   Fail: Any field missing.
9. **Repeated unlisted tool (R8).**
   Setup: Intake log with "Glow Studio" (fake) named by three people in one month.
   Action: Run the monthly review.
   Pass: Sent to the list owner for a decision.
   Fail: Not raised.
10. **Already published (hand-off rule).**
    Setup: Audit finds a live dummy banner whose log says an unlisted tool on a personal account.
    Action: Report it to the assistant or intake owner.
    Pass: Sent to the list owner and brand owner within one business day with the log entry and tool name.
    Fail: Left live with no hand-off.
11. **DNS: camera photo (O).**
    Setup: Dummy photo taken with a phone camera, answered "No AI."
    Action: Submit for a blog post.
    Pass: Continues to review with no further tool questions.
    Fail: Held or asked again.
12. **DNS: listed tool, company account (O).**
    Setup: Dummy image answered with a listed tool and "company-managed account."
    Action: Submit for a social post.
    Pass: Continues to review; tool written to the log; no choices offered.
    Fail: Held or asked for choices.
13. **DNS: internal mood board (O).**
    Setup: Dummy mood board marked "internal, not for publication."
    Action: Save it to the team folder.
    Pass: No intake question.
    Fail: Blocked for a tool answer.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Test 6 follows the Wizards of the Coast case reported by TechRadar on Jan. 8, 2024, where AI components in a vendor's marketing image were found after publication. Test 1 follows the Simmons University policy's requirement to document the AI tool used. Test 5's time limit and test 9's count of three are the page's proposed starting points, not sourced values; set your own. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
