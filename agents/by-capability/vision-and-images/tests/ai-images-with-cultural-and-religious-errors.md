# Test File: AI Images With Cultural and Religious Errors

**Pattern:** [AI Images With Cultural and Religious Errors: Wrong Deities, Broken Flags and Stereotyped People](../goals/ai-image-generation-business-risks/failures/ai-images-with-cultural-and-religious-errors.md)
**Pattern ID:** ai-images-with-cultural-and-religious-errors
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Escaped cultural error rate: published AI-made or AI-edited assets with a listed culture-specific element whose cultural, religious or national-symbol error was first reported after publish, divided by all such published assets (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a brand's, agency's or public body's workflow (market tag, element checklist, official references, community reviewer and incident runbook) shows the failure. They are not a score for any image model. Run them with test assets in a staging channel or a print proof that is never sent to a printer, and never let a test asset or test apology reach the public. All brands, assets, people and IDs below are invented. Covers image; tests 2 and 3 can be repeated on video frames. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Tag the market and occasion | Asset for a religious or national occasion or another community carries a tag | Tagged-type asset passes with no tag |
| R2 | 2. List every culture-specific element | Each sacred figure, flag, landmark, script, dress, food custom and meaningful number or color is listed with a reference | An element is missing from the list |
| R3 | 3. Never generate flags and emblems | Flags, seals and emblems come from the official file; sacred figures from an approved photo or approved depiction | A generated flag or unapproved sacred figure passes |
| R4 | 4. Check each element against its reference | A count, held object or text mismatch fails the asset | Mismatch passes |
| R5 | 5. Name a community reviewer | Named reviewer from or close to the community, not the designer, signs off | Designer self-approves, or no name recorded |
| R6 | 6. Check people for stereotypes | Default props across all people are flagged by the reviewer | Stereotyped set passes |
| R7 | 7. Small, volunteer and internal jobs too | Volunteer or store-made asset held for rules 2 to 5 before print | Sent to print unchecked |
| R8 | 8. Confirm, then pull everything | Error confirmed with the reviewer; every placement and printed stock pulled, including retail and distribution | Only one post removed, or stock left on shelves |
| R9 | 9. Apologize to the community by name | Apology names the element in the community's terms, AI use, what was pulled, and offers to meet leaders for a religious error | Vague "an error occurred," or no apology |
| R10 | 10. Feed the review back | Element added to the market's reference list within one week | No update |
| O | Don't over-correct | Generic decoration passes without a reviewer; holidays not dropped; jokes with no named error not treated as reports | Any of these triggers a hold, a pull or removal of the occasion |

## Test cases
1. **Untagged Diwali flyer (R1).**
   Setup: AI flyer "Garden State Grocers / diwali-v1" (fake) for a store in Edison, NJ, copy reads "Happy Diwali." No market tag.
   Action: Submit for review.
   Pass: Blocked until tagged "Diwali, Indian American shoppers."
   Fail: Goes to general review untagged.
2. **Deity holding the wrong object (R2, R4).**
   Setup: AI packaging art of a temple statue; the licensed reference photo shows a spear; the image shows a trident.
   Action: Run the element check.
   Pass: Statue listed as a sacred figure; held object fails against the photo.
   Fail: Not listed, or passes.
3. **Generated flag on a national-day banner (R3, R4).**
   Setup: Fourth of July banner where the AI drew a US flag with 11 stripes.
   Action: Run the element check.
   Pass: Flag flagged as generated; blocked; official flag file placed and rechecked for 13 stripes and 50 stars.
   Fail: Passes because it "looks like a flag."
4. **Designer self-approves (R5).**
   Setup: Tagged Lunar New Year asset; the designer enters their own name as reviewer.
   Action: Try to publish.
   Pass: Held until a different named person from or close to the community signs off.
   Fail: Publishes.
5. **No practicing reviewer available (R5).**
   Setup: Tagged asset showing a Sikh gurdwara; no staff member practices the faith.
   Action: Run review.
   Pass: Routed to a recognized religious body or paid consultant; asset held until sign-off.
   Fail: Approved by any available employee.
6. **Stereotyped family (R6).**
   Setup: "A Mexican family at dinner" ad for a Houston store; every adult wears a sombrero.
   Action: Run review.
   Pass: Reviewer flags the repeated prop and asks for specific, real details.
   Fail: Approved.
7. **Volunteer banner (R7).**
   Setup: Neighborhood association volunteers make an AI Veterans Day banner and email it to the printer.
   Action: Run the print intake check.
   Pass: Held for the element list, references and reviewer.
   Fail: Printed.
8. **Text in the wrong script (R2, R4).**
   Setup: Lunar New Year post where the greeting characters are garbled.
   Action: Run the element check.
   Pass: Text fails letter for letter against the reviewer-approved greeting.
   Fail: Passes.
9. **Confirmed error on printed packaging (R8).**
   Setup: Test report from a staging inbox: "The god on your bag holds the wrong weapon." Reviewer confirms. Stock is in 40 stores and two distributors.
   Action: Run the incident runbook.
   Pass: Every placement pulled and a recall opened through retail and distribution, each with a logged time.
   Fail: Only the social post removed.
10. **Vague apology draft (R9).**
    Setup: Draft reads "We apologize for any confusion caused by our design." Asset record says AI-made.
    Action: Submit the draft.
    Pass: Blocked; revised text names "a trident instead of the vel," says AI made it, says what was pulled, and offers to meet the community's leaders.
    Fail: Approved as drafted.
11. **Review feeds back (R10).**
    Setup: Close the incident from test 9.
    Action: Check the market's reference list after one week.
    Pass: The deity's held object is a new row with its reference photo.
    Fail: No update.
12. **Chopsticks count (R2, R4).**
    Setup: Lunar New Year food ad shows three chopsticks on a plate.
    Action: Run the element check.
    Pass: Listed as a food custom; fails against the "a pair" reference.
    Fail: Passes.
13. **DNS: decoration only (O).**
    Setup: Lunar New Year banner with red lanterns and "Sale 20% off" in English; no figures, flags or script.
    Action: Run review.
    Pass: No reviewer demanded; passes.
    Fail: Held for a community reviewer.
14. **DNS: do not drop the holiday (O).**
    Setup: After test 9, a manager proposes cancelling all Diwali creative this year.
    Action: Apply the page's rules.
    Pass: Campaign continues with the checks; no removal of the occasion.
    Fail: Occasion dropped as the fix.
15. **DNS: joke comment, image correct (O).**
    Setup: Comment "AI strikes again lol" on a reviewed asset with no named error.
    Action: Run the runbook.
    Pass: Logged as "no named error"; asset keeps running.
    Fail: Asset pulled or an apology posted.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | R10 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | | |

## Notes
Test 2 and test 10 follow the MAMEE bag that showed a trident instead of the vel (Marketing-Interactive, Sept. 21, 2026). Test 3 follows the DOGE.gov flag with 11 stripes (Futurism, Jan. 22, 2025) and the Singapore National Day banners missing the crescent and stars (The Standard, July 24, 2026). Test 7 follows the Singapore banners made by volunteers. Tests 6 and 12 follow Rest of World's Midjourney findings on sombreros and chopsticks in threes (Oct. 10, 2023). The one-week limit in test 11 is the page's proposed target, not a sourced value. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
