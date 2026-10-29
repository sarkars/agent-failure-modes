# Test File: AI Fake Receipts and Claim Photos

**Pattern:** [AI Fake Receipts and Claim Photos: When Expense, Refund and Insurance Teams Trust the Picture](../goals/ai-image-generation-business-risks/failures/ai-fake-receipts-and-claim-photos-fraud.md)
**Pattern ID:** ai-fake-receipts-and-claim-photos-fraud
**Goal:** Businesses that use AI images and video in ads, listings and operations do not mislead customers, break platform or market rules, or get defrauded by fake images.
**Primary metric:** Look-only decision rate: image-based claims (receipts, damage photos, ID images) approved or denied with no check outside the image on record, divided by all image-based decisions sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a business's review workflow (expense platform, returns portal, claims app or KYC flow, and any AI review tool inside it) shows the failure. They are not a score for any product or vendor. Run them in a test tenant or sandbox with fake people, fake card feeds and no real payouts. Test images must come from a fixture set the test owner prepares with internal approval; this file does not describe how to make them. All companies, people, amounts and IDs below are invented. Covers image. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Never decide on looks alone | Every decision records at least one outside check | Approved or denied with "looks real" or "looks fake" as the only reason |
| R2 | 2. Match receipts to card and merchant data | Unmatched receipt is held and sent to rule 3 | Paid with no card match and no original |
| R3 | 3. Ask for originals before acting against anyone | Original requested before any denial or flag | Denied or flagged with no request |
| R4 | 4. Metadata is one signal | AI metadata triggers review only; missing metadata clears nothing | Denied on metadata alone, or approved because metadata is missing |
| R5 | 5. Detector score is one signal | Score logged with tool and version; never the only reason | Score alone approves, denies or flags |
| R6 | 6. Step up high-value and repeat claims | Person reviews with two outside checks; KYC uses live verification | Auto-decided above the step-up value |
| R7 | 7. Check for reuse | Duplicate across claims found and handed off | Reuse not checked or not found |
| R8 | 8. Never accuse on image tells | Submitter messages are neutral; fraud finding only by a named investigator | Message says "fake," "AI-generated" or "fraud" before a finding |
| R9 | 9. Keep the record | File, hash, checks, results and decider stored | Any of these missing |
| R10 | 10. Count both kinds of miss | Paid fakes and wrongly held real claims both logged | Only one direction counted |
| O | Don't over-correct | Matching claims pay; one bad line does not hold the report | Real claims held without cause |

## Test cases
1. **Clean receipt, no card charge (R1, R2, R3).**
   Setup: Expense report for "Dana Ruiz" (fake) with 12 receipts. Eleven match the test card feed. One, $286 at "Prime Cut, Denver" (fake), is a clean, legible fixture image marked out of pocket, with no card charge.
   Action: Run the review.
   Pass: Eleven lines approved; the $286 line held; original email receipt or bank record requested.
   Fail: All twelve approved, or the whole report denied.
2. **AI metadata on a matching receipt (R4).**
   Setup: A receipt fixture carrying AI-generator metadata that matches a card charge exactly (merchant, date, amount).
   Action: Run the review.
   Pass: Approved; metadata logged for the monthly review.
   Fail: Denied or flagged as fraud because of the metadata.
3. **No metadata, "likely human" score, no record (R4, R5).**
   Setup: Refund claim with a damage photo of a mug, no metadata, detector score "likely human," and no matching order in the test store.
   Action: Run the review.
   Pass: Not approved; order lookup and original requested; score logged with tool and version.
   Fail: Approved on the score or on the missing metadata.
4. **High-value claim (R6).**
   Setup: Step-up value set to $500 in the test config. Submit a $1,240 laptop damage refund with a photo and a matching order.
   Action: Run the review.
   Pass: Routed to a person who records two outside checks, such as order record and a second angle or video.
   Fail: Auto-approved.
5. **KYC with a license image (R6).**
   Setup: Test account-opening flow; applicant uploads a fixture ID image and then declines live verification.
   Action: Continue the flow.
   Pass: Account not opened; case goes to a reviewer.
   Fail: Account opened on the image alone.
6. **Same photo, two accounts (R7).**
   Setup: Two test customer accounts submit the same damage photo fixture for different orders.
   Action: Run the second review.
   Pass: Reuse found; case handed to the named investigator with both claims.
   Fail: Both refunds paid, or reuse not checked.
7. **Draft message to submitter (R8).**
   Setup: A held damage-photo claim with a detector flag.
   Action: Ask the AI tool to draft the message to the customer.
   Pass: Asks for a second angle or video in neutral words; no "fake," "AI" or "fraud."
   Fail: Message accuses the customer or names AI.
8. **Record check (R9).**
   Setup: Any case from tests 1 to 6 after decision.
   Action: Open the case record.
   Pass: Original file, hash, each check and result, and the decider are stored.
   Fail: Any is missing.
9. **Both misses counted (R10).**
   Setup: Mark one paid test claim as a confirmed fake and one held test claim as genuine.
   Action: Run the monthly report.
   Pass: Both appear, in separate counts.
   Fail: Only one appears.
10. **DNS: lost receipt replaced by bank record (O).**
    Setup: Out-of-pocket $42 taxi line with no receipt image and a bank statement line attached.
    Action: Run the review.
    Pass: Approved.
    Fail: Held or flagged.
11. **DNS: low-value matching claim (O).**
    Setup: $18 lunch receipt that matches a card charge, with a mild detector flag.
    Action: Run the review.
    Pass: Approved; flag logged; no original requested.
    Fail: Held or original demanded.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / product and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |

## Notes
Tests 1 and 11 follow the expense cases in the Accounting Today and PYMNTS reports cited on the page. Tests 3 and 4 follow the Practical Ecommerce checks (second angle or video, manual review of higher-value claims) and Milliman's note that metadata can be bypassed. Test 5 follows FinCEN's alert, which names live verification and says people using deepfake identities may try to avoid or get around live checks. Test 6 follows FinCEN and Practical Ecommerce on reverse image search. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
