# Test File: AI Image Ads Missing or Unreadable Disclaimers

**Pattern:** [AI Image Ads With Missing or Garbled Disclaimers: When the Generator Draws the Fine Print](../goals/ai-image-generation-business-risks/failures/ai-image-ads-missing-or-unreadable-disclaimers.md)
**Pattern ID:** ai-image-ads-missing-or-unreadable-disclaimers
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Disclosure mismatch rate: live ad placements whose required disclosures are missing, generator-drawn, or not matching the approved disclosure sheet in wording, size or duration, divided by all live placements sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether an ad production workflow (AI generator, layout or video tool, disclosure sheet and pre-launch check) shows the failure. They do not test whether any disclosure meets any law; that is compliance's call, and the sheets, wording and minimum sizes used here are fixtures, not legal conclusions. Run them in a test ad account or on paused placements with no spend, and never let a test ad reach the public. All brands, people, sheets and IDs below are invented. Covers image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Disclosure sheet per ad | A claim that needs a disclosure with no sheet is held and routed to compliance | Ad launches with no sheet ID |
| R2 | 2. No required text in prompts | Disclosure text is stripped from the prompt; art is requested with no text and clear space | Generator receives the fine print |
| R3 | 3. Overlay from the sheet | Disclosure is a live text layer or super inserted from the sheet | Disclosure is retyped by hand or lives in the raster |
| R4 | 4. Remove generator-drawn fine print | Small text in the disclosure zone is cleared or the art is regenerated | Generator text left under or beside the overlay |
| R5 | 5. Check every size and cut | Wording matches letter for letter; size, contrast, placement and video duration meet the sheet | Any size or cut ships unchecked or below minimum |
| R6 | 6. Re-check after change | Resize, crop, new cut or platform variant re-runs R5 | Changed version runs on the old check |
| R7 | 7. Change the ad, not the font | Failing placement dropped, claim shortened or sent to compliance | Font shrunk below minimum, or disclosure used to rescue a false claim |
| R8 | 8. Log every check | Log has ad version, size, sheet ID and version, OCR text, measures, result, approver, date | Missing log or fields |
| O | Don't over-correct | Approved slogans and brand names pass; no extra disclaimers added; OCR misreads checked against the text layer | Decorative text blocked, unlisted disclaimers added, or correct type failed on an OCR misread |

## Test cases
1. **Fine print in the prompt (R2).**
   Setup: Prompt for "Lakeshore Bank / home equity banner" (fake) with the headline and full fine print typed into it.
   Action: Generate.
   Pass: The tool says it will not draw the fine print, strips it, and generates art with no text and clear space.
   Fail: The generator receives the fine print and draws it.
2. **No sheet (R1).**
   Setup: Headline "Save $500 on any treadmill*" with no disclosure sheet in the system.
   Action: Request export.
   Pass: Held; one question asks whether the asterisk text is a required disclosure; routed to the compliance reviewer.
   Fail: Exports with any footnote the tool writes itself.
3. **Generator drew text anyway (R4).**
   Setup: Art from a generator that put a line of small pseudo-text in the bottom band despite a "no text" prompt.
   Action: Run the post-generation check.
   Pass: The text is detected and cleared, or the art is regenerated.
   Fail: The overlay is placed on top of the garbled line.
4. **One word off (R3, R5).**
   Setup: Sheet D1 reads "with approved credit"; the overlay reads "with credit approval."
   Action: Run the export check.
   Pass: Blocked with the mismatch shown.
   Fail: Passes.
5. **Small placement (R5, R7).**
   Setup: Sheet sets a minimum size that the 320x50 banner cannot meet with the full D1 text.
   Action: Run the export check on all sizes.
   Pass: 320x50 held with choices (drop, send to compliance, something else); larger sizes pass.
   Fail: 320x50 ships with smaller type, or every size is held.
6. **Video super too short (R5).**
   Setup: 15-second social video; sheet sets a minimum on-screen time for D2; the super holds for less.
   Action: Run the export check.
   Pass: Blocked with the measured and required times shown.
   Fail: Passes.
7. **Disclosure in a different scene (R5).**
   Setup: Video claim "Clinically shown*" appears at 0:03; its disclosure appears only in the end card at 0:14, and the sheet says "same scene as claim."
   Action: Run the export check.
   Pass: Blocked for placement.
   Fail: Passes because the text exists somewhere.
8. **Platform variant after approval (R6).**
   Setup: Approved 1200x628 image; the ad platform makes a 1:1 crop that cuts the bottom band.
   Action: Import the variant into the check.
   Pass: Check re-runs and blocks the crop.
   Fail: The crop runs on the original approval.
9. **Disclosure contradicts the claim (R7).**
   Setup: Headline "No credit check"; sheet's disclosure says "credit check required."
   Action: Run the check.
   Pass: Held and routed to compliance to change the claim.
   Fail: Ships with the contradicting footnote.
10. **Log completeness (R8).**
    Setup: Run tests 1 to 9.
    Action: Export the check log.
    Pass: Every check has all fields listed in R8.
    Fail: Any check is missing or has blank fields.
11. **DNS: approved slogan in the art (O).**
    Setup: Art with the approved slogan "Ride Further" drawn as a large headline, approved by the creative lead; no claim needs a disclosure.
    Action: Run the checks.
    Pass: Passes with no disclaimer added.
    Fail: Blocked as a disclosure, or a generic disclaimer added.
12. **DNS: OCR misread (O).**
    Setup: Correct overlay text in a light font that OCR reads as "Annua1."
    Action: Run the export check.
    Pass: The tool compares against the text layer and passes.
    Fail: Blocked on the OCR misread alone.
13. **DNS: sheet lists one disclosure (O).**
    Setup: Sheet lists only D1 for the ad.
    Action: Export.
    Pass: Only D1 is added; no extra legal text.
    Fail: The tool adds disclaimers the sheet does not list.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Tests 5 to 7 follow the FTC staff factors (size relative to the claim, proximity, sufficient duration) and the ASA's Omnipod ruling (small print not legible and not on screen long enough), cited on the page. Test 9 follows the FTC staff statement that a disclosure cannot cure a false claim. Tests 1, 3 and 4 follow the page's rule that required text is never generator-drawn, consistent with Liu et al. on character-blind models. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
