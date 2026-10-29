# Test File: AI-Generated People Who Look Underage in Alcohol, Vape and Gambling Ads

**Pattern:** [AI-Generated People Who Look Underage in Alcohol, Vape and Gambling Ads: Checking Apparent Age Before Launch](../goals/ai-image-generation-business-risks/failures/ai-ads-for-age-restricted-products-show-young-looking-people.md)
**Pattern ID:** ai-ads-for-age-restricted-products-show-young-looking-people
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unrated age-restricted ad rate: live ads for age-restricted products that show an AI-generated or AI-edited person and have no logged apparent-age rating (prompt age floor, rater, rating, market rule) for that exact creative, divided by all such live ads sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether an advertiser's creative workflow (product tags, prompt step, apparent-age rating, market rule table, partner intake and complaint routing) shows the failure. They are not a score for any image or video generator. Run them on draft or paused ads with no spend, and never let a test ad reach the public or target anyone under 21. Never generate, request or keep images meant to look like minors; the fixtures below that test youth words must be blocked at the prompt step, and if a generator returns a youthful person anyway, delete it after logging the result. All brands, people and IDs below are invented. Covers image and video. Rules were read on October 29, 2026; re-read the market rule table before running. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Tag the product class | Untagged creative cannot be attached to an ad; class and markets recorded | Attached and published untagged |
| R2 | 2. Age floor in every prompt | Age floor present or added; youth words rejected | Prompt runs with no age, or with youth words |
| R3 | 3. Person rates apparent age | Named rater, not the prompt author, logs a range per prominent person | No rating, or the prompt author rates their own output, or the prompt is taken as proof |
| R4 | 4. Check against each market row | Strictest bar of all markets applied to shared creative | Only one market's bar checked |
| R5 | 5. Fail near the line | A range that touches the bar fails | Passed because the midpoint is above the bar |
| R6 | 6. Styling check | School, cartoon, toy, candy or juvenile cues fail | Passed on face alone |
| R7 | 7. Re-rate edits and frames | Any edit or new frame re-rated; youngest frame used | Old rating reused after an edit |
| R8 | 8. Partner creative | Partner creative held until a log is shown or the brand runs the check | Runs under the brand with no log |
| R9 | 9. Log every check | Row has creative ID, class, markets, prompt, floor, rater, range, rule row and date, decision | Any field missing |
| R10 | 10. Complaint hand-off | Creative paused in every market the same day; owner and counsel get the log | Left running, or paused in one market only |
| O | Don't over-correct | Clear adults pass with no extra steps; products that are not age-restricted skip the check; detector guess not used as the rating | Any of these blocked or added |

## Test cases
1. **Untagged beer creative (R1).**
   Setup: Image "Ridgeline Brewing / RB-201" (fake) with a person, product class blank.
   Action: Attach it to an Instagram ad.
   Pass: Blocked; the tool asks one question about whether the product is age-restricted and in which markets.
   Fail: Saved ready to publish.
2. **Betting prompt with no age (R2).**
   Setup: Brief tagged "sports betting; US." Prompt: "a guy cheering at his phone in a sports bar."
   Action: Send to the generator through the ad tool.
   Pass: The tool adds an adult age floor before generating and shows the edited prompt.
   Fail: Prompt runs unchanged.
3. **Youth words in a vape prompt (R2).**
   Setup: Brief tagged "vape; US." Prompt contains "college students on spring break."
   Action: Submit.
   Pass: Rejected at the prompt step with the reason; nothing is generated.
   Fail: Any image is generated.
4. **Prompt author rates their own output (R3).**
   Setup: Designer A writes the prompt and enters the rating "30 to 35."
   Action: Try to publish.
   Pass: Rating not accepted; a second named person must rate.
   Fail: Publishes.
5. **Prompt cited as proof (R3).**
   Setup: Rating field holds "prompt said 35-year-old."
   Action: Try to publish.
   Pass: Rejected; an observed range is required.
   Fail: Accepted.
6. **Shared US and UK alcohol creative (R4, R5).**
   Setup: Whiskey ad for US and UK; rated range "23 to 28."
   Action: Run the check.
   Pass: Fails against the UK 25 bar; offers regenerate older, background role, no person, something else.
   Fail: Passes because the US code bar is 21.
7. **Range touches the bar (R5).**
   Setup: UK cider ad; rated range "24 to 30."
   Action: Run the check.
   Pass: Fails.
   Fail: Passes on the midpoint.
8. **Adult face, juvenile styling (R6).**
   Setup: Hard seltzer ad; person rated "30 to 35" standing in a school hallway with a backpack.
   Action: Run the check.
   Pass: Fails on styling.
   Fail: Passes on the face rating.
9. **Platform enhancement after rating (R7).**
   Setup: Rated image "34 to 40" is then smoothed by a platform AI enhancement.
   Action: Publish.
   Pass: The edit triggers a new rating before publish.
   Fail: Old rating reused.
10. **Video with one young-looking frame (R7).**
    Setup: 8-second betting video; most frames rate "30s," one close-up rates "early 20s."
    Action: Run the check.
    Pass: The youngest frame is rated and the video fails.
    Fail: Passes on an average or first frame.
11. **Affiliate creative with no log (R8).**
    Setup: Partner uploads a brand-name betting video with no check log.
    Action: Partner requests launch.
    Pass: Held until the partner's log is supplied or the brand runs the check.
    Fail: Runs under the brand name.
12. **Log completeness (R9).**
    Setup: Any passing check from cases 1 to 11.
    Action: Read the log row.
    Pass: All fields in R9 present.
    Fail: Any field missing.
13. **Complaint about apparent age (R10).**
    Setup: Mock complaint: "The man in your beer ad looks about 17." Ad runs in three US states and the UK.
    Action: Watch routing.
    Pass: Paused in all markets the same day; owner and counsel get the log.
    Fail: Left running, or paused in one market only.
14. **DNS: clear adults in a wine ad (O).**
    Setup: Wine ad, two people rated "45 to 55," adult setting.
    Action: Run the check.
    Pass: Publishes with no extra steps.
    Fail: Blocked or sent for extra review.
15. **DNS: product that is not age-restricted (O).**
    Setup: Sparkling water ad tagged "not age-restricted," young adults shown.
    Action: Publish.
    Pass: The apparent-age check does not run.
    Fail: Blocked by the age check.
16. **DNS: detector guess as the rating (O).**
    Setup: A face-age tool says "38"; no person rated.
    Action: Try to publish.
    Pass: Held until a person rates; the tool's guess is shown only as a hint.
    Fail: Publishes on the tool's guess.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / generator and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |

## Notes
Tests 2, 4, 5 and 12 follow the ASA's September 16, 2026 ruling on Midnite, which found the prompt did not refer to the character's age and listed the affiliate's new safeguards (age-related prompts, perceived-age review, records). Tests 6 and 7 use the UK under-25 bar from the ASA/CAP advice and the "reasonably appear to be 21" wording in the DISCUS code. Test 8 follows the ASA advice on people "behaving in an adolescent or juvenile way." Test 10 follows the ruling's finding on a video ad. Test 11 follows the ruling's account that an affiliate made the ad. Test 3 reflects the Tech Transparency Project prompt for "smiling young people using vape pens." The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
