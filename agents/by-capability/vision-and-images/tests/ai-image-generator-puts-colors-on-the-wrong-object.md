# Test File: AI Image Generator Puts Colors on the Wrong Object

**Pattern:** [AI Image Generator Mixes Up Colors: Attributes Attached to the Wrong Object](../goals/ai-image-prompt-adherence/failures/ai-image-generator-puts-colors-on-the-wrong-object.md)
**Pattern ID:** ai-image-generator-puts-colors-on-the-wrong-object
**Goal:** AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text.
**Primary metric:** Unchecked-binding rate: published images from prompts that give two or more objects their own color, material or texture, where no per-object check is logged, divided by all such published images (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's image workflow (the generator, the assistant that writes prompts, the per-object check, the reviewer and the publish gate) shows the failure. They are not a score for any vendor's model. Run them in a test workspace and publish only to a test page. All companies, people, SKUs and IDs below are invented. Where a case needs a specific bad output, seed it or pick it from a generated set; do not wait for the model to fail on its own. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. List the pairs | Every object with its own attribute listed; prompt with 2+ pairs flagged | Pairs not listed or prompt not flagged |
| R2 | 2. Write each pair plainly | Any rewrite keeps each attribute next to its object and is shown to the user | Rewrite hidden, or attributes moved away from objects |
| R3 | 3. Check each object | Each pair checked on its own; swap, missing attribute, merged colors and leakage all count as misses | Only "are both colors present" checked |
| R4 | 4. Generate more than one | Set generated for flagged prompts; only all-pass images kept | One image used with no check |
| R5 | 5. Fix the region, then re-check | Whole image re-checked after any edit | Edited image delivered unchecked |
| R6 | 6. Say what did not match | Misses named to the user (object, asked, found) | Image delivered as matching despite a miss |
| R7 | 7. Product images get a person | Named reviewer checks against the SKU before listing | Listed without review |
| R8 | 8. Log it | Prompt as written and as sent, pair list, per-pair result, edits, reviewer, date | Any field missing |
| O | Don't over-correct | DNS cases run with no extra checks, rewrites or blocks | Flagged, rewritten or blocked |

## Test cases
1. **Two colors, two objects (R1).**
   Setup: Test workspace for "Front Range Home" (fake), Denver.
   Action: Ask: "A navy blue sofa and a mustard yellow armchair, light oak floor, morning light."
   Pass: Pairs listed (sofa: navy blue; armchair: mustard yellow; floor: light oak); prompt flagged.
   Fail: No pair list, or prompt not flagged.
2. **Swapped colors (R3, R6).**
   Setup: Same prompt; seed or select an output with a mustard sofa and a navy armchair.
   Action: Run the check and delivery step.
   Pass: Both objects marked as misses; the user is told "sofa came out mustard, asked navy" or similar; image not called ready.
   Fail: Passed because both colors appear, or delivered without comment.
3. **Common-pairing pull (R3).**
   Setup: Ask for "a golden car and a red watch" (example from Trusca et al.); select an output with a golden watch and a red car.
   Action: Run the check.
   Pass: Both pairs fail.
   Fail: Passed.
4. **Material swap (R3).**
   Setup: Ask for "a wooden table and a metal chair"; select an output with a metal table.
   Action: Run the check.
   Pass: Material miss recorded for the table.
   Fail: Only colors checked; material ignored.
5. **Leakage (R3).**
   Setup: Ask for "a navy blue sofa and a white lamp"; select an output where the lamp is also navy.
   Action: Run the check.
   Pass: Lamp marked as a miss.
   Fail: Passed because the sofa is right.
6. **Set, keep only all-pass (R4).**
   Setup: Flagged prompt from case 1.
   Action: Generate.
   Pass: A set is generated (team's size); only images where every pair passes are offered as final.
   Fail: One image generated and delivered.
7. **No image passes (R4, R6).**
   Setup: Seed a set where every image misses at least one pair.
   Action: Run delivery.
   Pass: The user is told no image matched and is offered choices, including "Something else."
   Fail: The closest image is delivered as matching.
8. **Edit changes another area (R5).**
   Setup: Recolor the sofa with a masked edit; seed an edit that also changes the floor.
   Action: Run the re-check.
   Pass: Floor miss caught; image not delivered as matching.
   Fail: Only the edited sofa re-checked.
9. **Rewrite shown (R2).**
   Setup: The assistant rewrites case 1 into separate clauses.
   Action: Compare prompt as written with prompt as sent.
   Pass: Rewrite shown to the user; each attribute still next to its object.
   Fail: Rewrite not shown, or a color moved to the wrong object.
10. **Product variant (R7).**
    Setup: Image for SKU 4410 in navy, passed by the automatic check, no reviewer.
    Action: Try to list it on the test product page.
    Pass: Blocked until a named reviewer checks it against the SKU.
    Fail: Listed.
11. **Log fields (R8).**
    Setup: Any delivered image from a flagged prompt.
    Action: Read its log.
    Pass: All listed fields present.
    Fail: Any field missing.
12. **DNS: one colored object (O).**
    Setup: Ask for "a red apple on a table."
    Action: Generate.
    Pass: No per-object binding check or extra regeneration forced.
    Fail: Flagged as a multi-pair prompt.
13. **DNS: unassigned colors (O).**
    Setup: Case 1 output that passes every pair and has a green plant in the corner.
    Action: Run the check.
    Pass: Plant not counted as a miss.
    Fail: Flagged for a color the prompt never assigned.
14. **DNS: unclear owner of a color (O).**
    Setup: Ask for "a red and white kitchen with a table and chairs."
    Action: Generate.
    Pass: The assistant asks one question ("Which items should be red?") or generates without forcing a pair check; it does not invent pairs.
    Fail: Invents pairs and fails images against them.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Cases 1, 2 and 6 follow the two-object color task in GenEval (arXiv 2310.11513) and the attribute-binding prompts in T2I-CompBench++ (arXiv 2307.06350). Case 3 uses the example from Trusca et al. (arXiv 2404.13766). Case 4 follows T2I-CompBench++'s texture category. Case 5 follows the leakage examples in Trusca et al. and Color Bind (arXiv 2508.19791). Case 8 follows the planned page on edits that change parts the user did not ask to change. Cases 7 and 9 to 14 are my own fixtures built from the page's rules and its "Don't over-correct" paragraph. Set size and retry limits are the team's choices; the page does not set them.
