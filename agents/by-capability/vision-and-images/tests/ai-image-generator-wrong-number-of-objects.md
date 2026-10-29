# Test File: AI Image Generator Wrong Number of Objects

**Pattern:** [AI Image Generator Wrong Number of Objects: Ask for Four Chairs, Get Five](../goals/ai-image-prompt-adherence/failures/ai-image-generator-wrong-number-of-objects.md)
**Pattern ID:** ai-image-generator-wrong-number-of-objects
**Goal:** AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text.
**Primary metric:** Uncounted-or-wrong-count publish rate: published AI images made from a prompt that states a number that matters, where no count was recorded or the recorded count differs from the request, divided by all such published images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator, the assistant that writes prompts, the counter and the publish gate) shows the failure. They are not a counting score for any vendor. Run them in a test workspace and publish only to a test page. All companies, people, SKUs and files below are invented. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Flag count-bearing prompts | Number next to a countable object marked "count matters" before generating | Not flagged |
| R2 | 2. Write the count once, plainly | Prompt as sent states the count once per object type, with no grid or math rewrite | Count missing, or rewritten as "3 times 4" or a grid |
| R3 | 3. Count every image | Counted number recorded for each image before it is shown as final | No count recorded |
| R4 | 4. Regenerate, then stop | Stops at the team's retry limit and tells the requester each count | Regenerates without limit, or hides the counts |
| R5 | 5. Build exact counts another way | After the limit, or for counts above 5, offers compositing, a real photo or a count-free image | Keeps regenerating or ships a wrong count |
| R6 | 6. Never change text to match | Listing or caption text keeps the true count | Text edited to match a wrong image |
| R7 | 7. Named recount | Recorded recount and approval before publish | Published without it |
| R8 | 8. Log it | Log has requested count, count per try, method, counter, approver, date | Any field missing |
| O | Don't over-correct | DNS cases run with no count check, retries or blocks | Flagged, retried or blocked |

## Test cases
1. **Set of four stools (R1, R3).**
   Setup: Test workspace for "Front Range Home" (fake), a Denver furniture store.
   Action: Ask: "Listing image for SKU 4410: a set of four oak counter stools at a white kitchen island."
   Pass: Prompt flagged; each generated image has a recorded stool count before one is offered.
   Fail: One image offered with no count.
2. **Prompt as sent (R2).**
   Setup: Same request as case 1.
   Action: Read the prompt as sent in the log.
   Pass: "four" appears once next to "stools"; no grid, "2 plus 2" or "exactly 2 by 2" wording added.
   Fail: Count dropped or rewritten into a layout or math phrase.
3. **Three misses (R4, R5).**
   Setup: Seed or select three results showing 5, 3 and 5 stools; retry limit set to 3.
   Action: Run the workflow.
   Pass: Stops after three; tells the requester "5, 3 and 5"; offers composite, product photo, one stool with "Set of 4" in text, or something else.
   Fail: A fourth try runs automatically, or a 5-stool image is offered.
4. **Large count (R5).**
   Setup: A Columbus bakery (fake) asks for "a tray of twelve cupcakes for the menu."
   Action: Run the workflow.
   Pass: Goes straight to compositing or a real photo, since the count is above 5.
   Fail: Regenerates hoping for twelve.
5. **Two counts in one image (R1, R3).**
   Setup: A teacher asks for a worksheet image: "2 apples on the table and 3 apples on the floor."
   Action: Generate and count.
   Pass: Both counts recorded separately (table and floor); mismatch on either is caught.
   Fail: Only the total counted, or not counted.
6. **Text edit request (R6).**
   Setup: A 5-stool image exists; requester says "just change the listing to set of 5."
   Action: Send the request.
   Pass: Assistant says the set has four and offers to fix the image instead.
   Fail: Listing text changed.
7. **Detector only (R3, R7).**
   Setup: A vision-model count says 4 stools; no person has recounted.
   Action: Try to publish to the test page.
   Pass: Blocked until a named person recounts.
   Fail: Published on the detector count alone.
8. **No recount (R7).**
   Setup: A composited 4-stool image with no approval.
   Action: Try to publish.
   Pass: Blocked.
   Fail: Published.
9. **Log fields (R8).**
   Setup: Any approved count-bearing image.
   Action: Read its log.
   Pass: All listed fields present.
   Fail: Any field missing.
10. **DNS: no number (O).**
    Setup: Ask for "a bowl of apples on a farmhouse table."
    Action: Generate.
    Pass: No count flag or recount required.
    Fail: Flagged as count-bearing.
11. **DNS: number that is not a count (O).**
    Setup: Ask for "a 1950s diner with a Route 66 sign, 3D render."
    Action: Generate.
    Pass: No count flag.
    Fail: Flagged on "1950s," "66" or "3D."
12. **DNS: approximate on purpose (O).**
    Setup: Ask for "about a dozen balloons, it's a mood shot, the exact number doesn't matter."
    Action: Generate.
    Pass: Marked approximate; no retries or block.
    Fail: Retries or block for a count of twelve.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Case 2 follows Guo et al. (arXiv 2503.06884), who found grid and math-style prompt rewrites did worse than the plain prompt. Case 4 follows the same paper's drop in accuracy above 5 objects; the cutoff of 5 is the page's proposal. Case 5 follows the OpenAI Developer Community thread where a user's "2 apples on the table; 3 apples on the floor" prompt came out wrong. Case 7 follows GenEval (arXiv 2310.11513), whose detector agreed with humans on 82.3% of counting checks, so it is not used as the only check. The retry limit and sample rate are the team's choices. Cases 1, 3, 6 and 8 to 12 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
