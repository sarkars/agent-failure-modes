# Test File: AI Image Generator Puts Objects in the Wrong Position

**Pattern:** [AI Image Generator Puts Objects in the Wrong Position: Left and Right, On and Under, In Front and Behind](../goals/ai-image-prompt-adherence/failures/ai-image-generator-puts-objects-in-the-wrong-position.md)
**Pattern ID:** ai-image-generator-puts-objects-in-the-wrong-position
**Goal:** AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text.
**Primary metric:** Unchecked-placement rate: published AI images whose prompt or copy states a placement, with no recorded check of each placement in the final image, divided by all such published images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator, the assistant that writes and checks prompts, the reviewer and the publish gate) shows the failure. They are not a placement-accuracy score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people, products and files below are invented. Where a test needs a wrong placement, select or seed an image set that has one; do not assume any tool will produce one on demand. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. List the placements | Every placement in the prompt listed as A, relation, B | Any placement missed |
| R2 | 2. Generate a set | More than one image (team's chosen size) before picking | One image generated and used |
| R3 | 3. Check each placement | A person marks each placement in each image; vision-model result confirmed by a person | No marks, or vision-model result used alone |
| R4 | 4. Say what failed | Failed placement and image named to the requester | Image presented as matching |
| R5 | 5. Offer a fix the person picks | Options shown; flip refused when image has text, logos or handed objects; edits re-checked | Fix applied without choice, unsafe flip, or edit not re-checked |
| R6 | 6. Word order once | At most one rewrite, shown before it runs | Silent rewrite, or repeated rewrites |
| R7 | 7. Copy matches final image | Position words in copy checked after any flip or edit | Copy not checked, or checked before the flip |
| R8 | 8. Named sign-off | Recorded approval before publish | Published without it |
| R9 | 9. Log it | Log has prompt, placements, set size, per-placement result, fix, copy check, reviewer, date | Any field missing |
| O | Don't over-correct | DNS cases run with no placement check or block | Checked, blocked or rewritten |

## Test cases
1. **Two placements listed (R1).**
   Setup: Test workspace for "Front Range Home" (fake furniture store), Denver.
   Action: Ask: "A brass floor lamp to the left of a green armchair, a jute rug under the coffee table."
   Pass: Log lists "lamp LEFT OF armchair" and "rug UNDER coffee table" before generation.
   Fail: Either placement missing.
2. **Set generated (R2).**
   Setup: Same prompt.
   Action: Generate.
   Pass: A set is generated before any image is offered as final.
   Fail: One image offered as final.
3. **Per-placement marks (R3, R4).**
   Setup: A set of 4 where the lamp is right of the chair in 3 images.
   Action: Run the check step.
   Pass: Each image has a mark for each placement; the requester is told which images fail and why.
   Fail: No marks, or the set is called "matching."
4. **Vision model as checker (R3).**
   Setup: A vision model pre-screens and wrongly marks a swapped image as correct.
   Action: Complete the check.
   Pass: A person confirms each mark and catches the swap.
   Fail: The vision model's mark is final.
5. **Flip refused (R5).**
   Setup: The only near-correct image has the store's logo on a pillow and the lamp on the wrong side.
   Action: Requester asks to flip it.
   Pass: Assistant explains the logo would mirror and offers the other options.
   Fail: Image flipped.
6. **Edit re-checked (R5).**
   Setup: Requester picks "edit the rug area" with a mask.
   Action: Run the edit.
   Pass: Both placements re-checked on the edited image.
   Fail: Edited image accepted without a check.
7. **One rewrite, shown (R6).**
   Setup: No image in the set passes "a dog in front of the sofa."
   Action: Let the assistant try again.
   Pass: One rewrite (anchor first, one placement per sentence) shown before it runs; if it still fails, choices are offered.
   Fail: Rewrite runs unseen, or the assistant loops on rewrites.
8. **Copy after flip (R7).**
   Setup: Image with no text is flipped; caption says "The lamp on the left is $89."
   Action: Run the pre-publish check.
   Pass: Caption checked against the flipped image.
   Fail: Caption checked against the original or not at all.
9. **Ambiguous left (R3, O).**
   Setup: Ask for "a cat on the chair's left."
   Action: Generate.
   Pass: The assistant asks one question: viewer's left or the chair's left?
   Fail: Picks one silently, or asks more than one question.
10. **No sign-off (R8).**
    Setup: A checked image with no approval.
    Action: Try to publish to the test page.
    Pass: Blocked until a named reviewer approves.
    Fail: Published.
11. **Log fields (R9).**
    Setup: Any approved image with placements.
    Action: Read its log.
    Pass: All listed fields present.
    Fail: Any field missing.
12. **DNS: no placements (O).**
    Setup: Ask for "a cozy reading nook with warm light."
    Action: Generate.
    Pass: No placement check runs; normal flow.
    Fail: Placement check or block triggered.
13. **DNS: placement in prompt, image right first time (O).**
    Setup: Ask for "a mug on a desk"; the set's chosen image shows it.
    Action: Run the check.
    Pass: Marked correct with no choices or rewrites offered.
    Fail: Choices forced on the requester.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Tests 1-3 follow the per-relation scoring in VISOR (Gokhale et al., arXiv 2212.10015) and GenEval (Ghosh et al., arXiv 2310.11513). Test 4 follows the existing relative position confusion page on vision models misreading left and right. Test 6 follows OpenAI's image generation guide, which says masked edits may not follow the mask's exact shape. Test 7 follows the first-object bias reported by VISOR and GenEval; the page marks the rewrite as unproven. Tests 5 and 8-13 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph. The set size is the team's choice; the page does not set it.
