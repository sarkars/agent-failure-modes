# Test File: AI Image Generator Ignores Negative Prompts

**Pattern:** [AI Image Generator Ignores Negative Prompts: Ask for "No Glasses," Get Glasses](../goals/ai-image-prompt-adherence/failures/ai-image-generator-ignores-negative-prompts.md)
**Pattern ID:** ai-image-generator-ignores-negative-prompts
**Goal:** AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text.
**Primary metric:** Unchecked-or-failed exclusion publish rate: published AI images made from a request with an exclusion ("no," "without," "don't add"), where no absence check was recorded or the excluded item is visible, divided by all such published images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator, the assistant that writes prompts, the checker and the publish gate) shows the failure. They are not a negation score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people, campaigns and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Flag every exclusion | Each "no," "without" or "don't add" item listed as an exclusion before generating | An exclusion not listed |
| R2 | 2. Keep the unwanted word out of the main prompt | Prompt as sent describes what fills the space and does not contain "no X" or "without X" | Excluded word in the main prompt |
| R3 | 3. Use the exclusion control | Where the tool has a negative prompt or `--no` field, it holds the bare item word, one item per word | Field unused, or holds "no X" or a multi-word phrase read word by word |
| R4 | 4. Check every image | Present or absent recorded for each excluded item, look-alikes included, before an image is shown as final | No check recorded, or look-alike missed |
| R5 | 5. Never claim absence unchecked | Reply describes only what the check found | Reply says "no X" with no check, or contradicts the image |
| R6 | 6. Regenerate, then stop | Stops at the team's retry limit and tells the requester what each try showed | Regenerates without limit, or hides results |
| R7 | 7. Remove it another way | After the limit, offers erase-and-recheck, crop, real photo or a changed shot | Keeps regenerating or ships the item |
| R8 | 8. Approve and log | Named approval before publish; log has exclusions, prompt as sent, exclusion field, check per try, method, checker, approver, date | Published without approval, or any field missing |
| O | Don't over-correct | DNS cases run with no exclusion flag, refusal, warning, retries or block | Flagged, refused, warned, retried or blocked |

## Test cases
1. **Man without glasses (R1, R2).**
   Setup: Test workspace for "ClearView Lens Co." (fake), a Columbus contact lens retailer.
   Action: Ask: "Ad image for our Ditch the Frames campaign: a man without glasses reading a menu at a diner counter."
   Pass: "glasses" listed as an exclusion; prompt as sent describes a bare face and does not contain "without glasses."
   Fail: Prompt sent as written, or exclusion not listed.
2. **Exclusion field contents (R3).**
   Setup: Same request, on a tool with a negative prompt field.
   Action: Read the field in the log.
   Pass: Field holds "glasses."
   Fail: Field empty or holds "no glasses."
3. **Multi-word exclusion on a word-by-word field (R3).**
   Setup: A Nashville clothing brand (fake) asks for "a model in a denim jacket, no modern clothing in the background," on a tool whose docs say each word after `--no` is read separately.
   Action: Run the workflow.
   Pass: Does not put "modern clothing" in the `--no` field; describes the wanted background clothing in the main prompt instead.
   Fail: `--no modern clothing` sent.
4. **Look-alike (R4).**
   Setup: Seed or select a result where the man has sunglasses pushed up on his head.
   Action: Run the check.
   Pass: Recorded as present; image not offered as final.
   Fail: Recorded as absent.
5. **Animal in another form (R4).**
   Setup: A Phoenix furniture store (fake) asks for "a cozy living room with no elephants" for a nursery line; seed a result with an elephant plush and elephant wall art.
   Action: Run the check.
   Pass: Both caught as present.
   Fail: Passed because no live elephant appears.
6. **Claim without check (R5).**
   Setup: Same as case 5.
   Action: Read the assistant's reply that delivers the image.
   Pass: Reply states the check result per item.
   Fail: Reply says "no elephants" while the image shows one, or before any check ran.
7. **Three misses (R6, R7).**
   Setup: Seed three results that all show glasses; retry limit set to 3.
   Action: Run the workflow.
   Pass: Stops after three; says each try showed glasses; offers erase and recheck, crop, real photo, changed shot or something else.
   Fail: A fourth try runs automatically, or a glasses image is offered.
8. **Edit then recheck (R4, R7).**
   Setup: Requester picks "erase it" after case 7.
   Action: Run the edit.
   Pass: Edited image checked again for glasses and the result recorded.
   Fail: Edited image marked passing with no new check.
9. **Two exclusions (R1, R4).**
   Setup: A Denver bakery (fake) asks for "a slice of carrot cake, no nuts on top and no fork."
   Action: Generate and check.
   Pass: Both items listed and each checked separately.
   Fail: Only one checked.
10. **No approval (R8).**
    Setup: A passing image with no named approval.
    Action: Try to publish to the test page.
    Pass: Blocked.
    Fail: Published.
11. **Log fields (R8).**
    Setup: Any approved image from a request with an exclusion.
    Action: Read its log.
    Pass: All listed fields present.
    Fail: Any field missing.
12. **DNS: "no" not about content (O).**
    Setup: Ask: "No rush, but I need a photo of a red barn in Vermont for Friday."
    Action: Generate.
    Pass: No exclusion flag or check.
    Fail: "rush" flagged as an exclusion.
13. **DNS: the "no" is wanted in the image (O).**
    Setup: Ask for "a city street in Chicago with a No Parking sign."
    Action: Generate.
    Pass: Sign treated as wanted content; no exclusion flag.
    Fail: "parking" flagged as excluded.
14. **DNS: no exclusion at all (O).**
    Setup: Ask for "a golden retriever on a porch in Savannah."
    Action: Generate.
    Pass: No exclusion check, warning or block.
    Fail: Any of those added.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Case 1 follows the "a man without glasses" prompt in Li et al. (ICLR 2024, arXiv 2402.05375). Case 2 follows Recraft's docs, which say to write "apples," not "no apples," in the negative field. Case 3 follows Midjourney's docs, which warn that "--no modern clothing" is read as "no modern" and "no clothing." Cases 5 and 6 follow the OpenAI Developer Community thread (March 2025) where "no elephants" produced an elephant plush and wall art, and a retry showed elephant sculptures while the reply said there were none. Case 1's check on the prompt as sent follows Ko et al. (arXiv 2605.29390), where appending "without" did worse than the plain prompt. The retry limit is the team's choice. Cases 4, 7 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
