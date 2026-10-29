# Test File: AI-Generated People Resemble Real People Without a Release

**Pattern:** [AI-Generated Models That Look Like Real People: No Release, No Record, No Check](../goals/ai-image-generation-business-risks/failures/ai-generated-people-resemble-real-people-without-release.md)
**Pattern ID:** ai-generated-people-resemble-real-people-without-release
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unchecked synthetic-person publish rate: published assets showing an AI-generated person with no logged source record and resemblance review, divided by all published assets showing an AI-generated person (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a creative workflow (asset intake, source records, blind review, publish gate and complaint path) shows the failure. They do not test whether any image infringes anyone's rights; that is counsel's call. Run them in a test asset library and a test ad account with no spend, and never publish a test asset. Use only invented people and consenting staff volunteers as "real person" fixtures; never use a real celebrity's photo or name outside a fixture string the workflow should reject. All brands, assets, people and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Tag every person at intake | Blank or "unknown" person type blocks publishing | Asset publishes with no person type |
| R2 | 2. Source record for every AI person | AI-person asset with no source record is blocked, including agency and seller files | Publishes without a record |
| R3 | 3. No real names or faces as inputs without a release | Prompt naming a real person, or a real reference photo, with no AI-use release is rejected | Accepted |
| R4 | 4. Blind resemblance review | Three reviewers not on the project answer before publishing | Published with no review, or reviewers include the maker |
| R5 | 5. Named match holds | One named real person holds the asset with the choices listed | Published, or the hold cleared without a choice |
| R6 | 6. Disclaimer is not a release | Adding an "AI, not a real person" caption does not clear a hold | Caption clears the hold |
| R7 | 7. Record tool coverage | Coverage is recorded from the checklist, or as "unknown" | Recorded as covered with no checklist entry |
| R8 | 8. Fast takedown | Complaint pauses every placement within one business day and routes to legal with the record | Asset stays live, or only one placement paused |
| R9 | 9. Log every decision | Log has asset, source record ID, reviewers and answers, outcome, decider, date, placements | Missing log or fields |
| O | Don't over-correct | Clean AI-person assets run; vague "looks like someone" is not held; real-shoot photos with releases are not held | Held "to be safe," or AI people blocked outright |

## Test cases
1. **Blank person type (R1).**
   Setup: Upload "Ridgeline Outfitters / fall-banner-03" (fake) showing a person, person type left blank.
   Action: Send to publish.
   Pass: Blocked; the tool asks one question: real, AI-edited or AI-generated.
   Fail: Publishes, or the tool guesses the type.
2. **Agency file with no source record (R2).**
   Setup: Agency delivers "fall-banner-04," tagged AI-generated person, no source record attached.
   Action: Send to publish.
   Pass: Blocked with the message that the source record is missing; the tool says it cannot show how the face was made.
   Fail: Publishes.
3. **Celebrity name in prompt (R3).**
   Setup: Source record prompt reads "hiker who looks like [fixture celebrity name]." No release on file.
   Action: Send to publish.
   Pass: Rejected for a real name used as input without a release.
   Fail: Accepted or sent to review.
4. **Staff photo as reference (R3).**
   Setup: Source record lists a reference image from a past brand shoot of a volunteer employee; the release on file does not mention AI use.
   Action: Send to publish.
   Pass: Rejected until a release covering AI use is on file.
   Fail: Accepted because the photo is brand-owned.
5. **Review runs before publish (R4).**
   Setup: AI-person asset with full source record.
   Action: Send to publish.
   Pass: Three reviewers who are not the maker see the image without context and answer the one question before scheduling.
   Fail: Scheduled first, or the maker is one of the reviewers.
6. **One named match (R5).**
   Setup: Same asset; reviewer 2 answers "looks like the Channel 9 weather anchor" (fixture answer).
   Action: Complete review.
   Pass: Held; choices shown: new face, get a release, send to legal, something else.
   Fail: Published because 2 of 3 named no one.
7. **Disclaimer to clear a hold (R6).**
   Setup: Asset from test 6 is held. A user adds the caption "AI-generated, not a real person."
   Action: Send to publish again.
   Pass: Still held.
   Fail: Hold cleared.
8. **Unknown tool coverage (R7).**
   Setup: Source record names a tool with no entry in the indemnity checklist.
   Action: Save the record.
   Pass: Coverage saved as "unknown" and flagged; not "covered."
   Fail: Saved as covered, or left blank with no flag.
9. **"That's me" complaint (R8).**
   Setup: AI-person asset live in three test placements. A test message arrives: "That's me in your ad. I never agreed."
   Action: Log the complaint.
   Pass: All three placements paused within one business day; legal gets the asset, source record, review log and placement list; no public reply argues the point.
   Fail: Any placement stays live, or legal gets no record.
10. **Log completeness (R9).**
    Setup: Run tests 1 to 9 and 11 to 13.
    Action: Export the review log.
    Pass: Every decision has all fields listed in R9.
    Fail: Any decision missing or blank.
11. **DNS: clean AI person (O).**
    Setup: Full source record, no names or references, three reviewers answer "no one."
    Action: Send to publish.
    Pass: Scheduled with no extra hold.
    Fail: Held or sent to legal.
12. **DNS: vague resemblance (O).**
    Setup: Reviewer writes "she looks like a lot of people," no name.
    Action: Complete review.
    Pass: Not held.
    Fail: Held as a named match.
13. **DNS: real shoot with release (O).**
    Setup: Photo of a real model, tagged real person, release on file covering ads.
    Action: Send to publish.
    Pass: No source record or blind review required.
    Fail: Held for the AI-person checks.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Test 2 follows Shein's statement that the image "was provided by a third-party vendor" (Yahoo News / Nexstar, Sept. 3, 2025), cited on the page. Test 5 follows Nightjar's advice to run a blind recognition check before publishing (vendor source). Test 7 follows the Lisa AI ad's disclaimer, "It has nothing to do with this person" (Variety Australia, AV Club). Test 8 follows Adobe's 2024 Firefly FAQ, which names publicity claims but lists exclusions. The three-reviewer count and the one-business-day pause are the page's proposed starting points, not sourced numbers. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
