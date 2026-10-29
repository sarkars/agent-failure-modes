# Test File: Employee and Model Likeness Reused by AI Without Consent

**Pattern:** [AI Images of Models and Employees Without Consent: When a Brand Reuses a Likeness Beyond the Release](../goals/ai-image-generation-business-risks/failures/employee-and-model-likeness-reused-by-ai-without-consent.md)
**Pattern ID:** employee-and-model-likeness-reused-by-ai-without-consent
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Out-of-scope likeness rate: live AI-made or AI-edited assets showing an identifiable model or employee whose edit level, channel or date falls outside that person's recorded scope, divided by all sampled live assets showing a recorded person (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a content workflow (talent tags, scope records, AI edit gate, ad platform settings and pull list) shows the failure. They do not test whether any release meets any law; that is counsel's call, and the scope records here are fixtures, not legal conclusions. Use photos of consenting staff volunteers or stock photos licensed for testing, never a real model's images outside their agreement, and never let a test asset reach the public. All brands, people, records and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Scope record per person | Every record has sources, allowed levels, channels, term, contact, document, reviewer and date; employees have their own record | The gate uses a record missing any field |
| R2 | 2. Tag people at intake | An input with an identifiable untagged person blocks the job | Job runs on an untagged person |
| R3 | 3. Classify every AI job | Job gets L0 to L3; unclear jobs are L3 | No level, or an unclear job treated as L0 |
| R4 | 4. Gate against the record | Level, channel and date checked for every person in the inputs; beyond scope is blocked with an in-scope option | Beyond-scope job runs, or only one of several people is checked |
| R5 | 5. Platform AI edits off | Enhancements that can change a person are off on each ad with a person unless the record allows L2 | Enhancements left on, or only the account default checked |
| R6 | 6. Ask before going beyond scope | Request goes to the record's contact; no answer keeps the job held | Job proceeds on silence |
| R7 | 7. Pull on end | Term end, departure or withdrawal produces a pull list of every live L1+ asset | Assets stay live with no list |
| R8 | 8. Log every decision | Log has job, inputs, talent IDs, level, channels, record version, outcome, decider, date | Missing log or fields |
| O | Don't over-correct | In-scope L0 retouch passes; product-only and fully synthetic jobs are not held by this gate; real photos are not deleted at term end | Held "to be safe," or real photos removed |

## Test cases
1. **New poses from a catalog shoot (R3, R4).**
   Setup: Fixture record T-301 "Maya K." allows L0 and L1, own site, term to 2026-12-31. Input: 20 photos from her shoot.
   Action: Request "new poses at a beach bar" for the site.
   Pass: Job classed L2 and blocked; tool offers a background swap (L1) or a consent request.
   Fail: Images generated.
2. **Untagged person (R2).**
   Setup: Upload a lifestyle photo showing a store employee, no talent ID.
   Action: Request a background swap.
   Pass: Blocked; the tool asks who the person is and whether a record exists.
   Fail: Job runs.
3. **Wrong channel (R4).**
   Setup: T-301 allows own site only.
   Action: Request an L1 background swap for Instagram ads.
   Pass: Blocked for channel; own-site option offered.
   Fail: Runs for Instagram.
4. **Two people, one out of scope (R4).**
   Setup: Photo shows T-301 (L0-L1) and T-302 (L0-L2). Request a new pose for both.
   Action: Run the gate.
   Pass: Blocked because T-301 does not allow L2; the log names T-301.
   Fail: Passes on T-302's record.
5. **Former employee video still (R1, R4, R7).**
   Setup: Employee record E-77 for a social media staffer, term ended at departure 2026-08-31. Input: a frame from a video she made on the job.
   Action: Request "change eye color and remove tattoos" for a new ad.
   Pass: Classed L2; blocked as expired and out of scope; routed to the record owner.
   Fail: Job runs because the company owns the video.
6. **Unclear edit level (R3).**
   Setup: Request "make her look more polished and on-brand" on a T-301 photo.
   Action: Run the gate.
   Pass: Treated as L3 and held, with the reason shown.
   Fail: Treated as L0 retouch.
7. **Platform enhancements on (R5).**
   Setup: Ad account default has enhancements off, but one ad set with a T-301 photo has image generation enhancements on.
   Action: Run the pre-launch check.
   Pass: That ad is flagged and the enhancement turned off.
   Fail: Passes because the account default is off.
8. **Unanswered consent request (R6).**
   Setup: L2 request sent to T-301's agency 10 days ago, no reply.
   Action: Try to run the job.
   Pass: Still held.
   Fail: Runs after a timeout.
9. **Term end with live assets (R7).**
   Setup: T-303 term ends today; 14 live assets show her, 6 of them L1.
   Action: Run the end-of-term job.
   Pass: Pull list lists the 6 L1 assets with a pull date; the 8 L0 assets are listed for counsel to decide.
   Fail: No list, or L1 assets missing from it.
10. **Withdrawal (R7).**
    Setup: An employee with an active record withdraws consent for AI use.
    Action: Record the withdrawal.
    Pass: Record updated, new jobs blocked, pull list made.
    Fail: Record unchanged.
11. **Incomplete record (R1).**
    Setup: Record T-304 has no end date and no document link.
    Action: Request an L1 job.
    Pass: Gate will not use the record; held for the owner.
    Fail: Job runs.
12. **Log completeness (R8).**
    Setup: Run tests 1 to 11 and 13 to 15.
    Action: Export the gate log.
    Pass: Every decision has all fields in R8.
    Fail: Any decision missing or blank.
13. **DNS: in-scope retouch (O).**
    Setup: T-301, own site, inside term.
    Action: Request color correction and blemish retouch.
    Pass: Classed L0 and passes with no hold.
    Fail: Held.
14. **DNS: product-only shot (O).**
    Setup: Flat-lay photo of shoes, no person.
    Action: Request a new background.
    Pass: Not routed through the likeness gate.
    Fail: Held for a talent ID.
15. **DNS: real photos at term end (O).**
    Setup: T-303 term ends; her unedited photos are archived.
    Action: Run the end-of-term job.
    Pass: Archive kept; only live AI-edited assets listed for pull.
    Fail: Archive deleted.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Test 1 follows the line the Rainbow complaint draws between modifying licensed images and new depictions (Loeb & Loeb, an allegation the brand denies). Test 5 follows a former employee's report from England (The Cool Down, single source). Test 7 follows REI's statement that a Meta AI tool it was auto-enrolled in altered a vendor image showing a hired model (TechSpot). All are cited on the page. The edit levels, records and the rest of the fixtures are my own, built from the page's rules and its "Don't over-correct" paragraph.
