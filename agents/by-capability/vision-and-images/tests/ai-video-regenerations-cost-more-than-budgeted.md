# Test File: AI Video Regenerations Cost More Than Budgeted

**Pattern:** [AI Video Regenerations Cost More Than Budgeted: Rerolls and Per-Second Pricing Blow Past the Estimate](../goals/ai-image-generation-business-risks/failures/ai-video-regenerations-cost-more-than-budgeted.md)
**Pattern ID:** ai-video-regenerations-cost-more-than-budgeted
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Over-cap renders: renders started after the project's spend reached or would pass its cap without a recorded approval, divided by all renders sampled (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a team's video generation workflow (the estimate, an internal assistant or tool that starts renders, the spend counter, the project cap and the take log) shows the failure. They are not a score for any vendor. Run them on a test project with a small cap, cheap draft settings or a mocked billing source, so a failed test does not spend real money. All companies, people, shots and amounts below are invented; the $0.40 per second rate is the Veo 3 with-audio rate The Decoder reported in September 2025 and should be swapped for your vendor's current rate. Covers video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Estimate by takes per keeper | Estimate is shots x seconds x price x takes per keeper, with the takes figure and its source named | Estimate assumes one take per shot |
| R2 | 2. Set a cap per project | No render starts until a cap and a named budget owner exist | Renders with no cap |
| R3 | 3. Show cost, spent and remaining | Each render is preceded by this take's cost, spend so far and what is left | Any render with no cost shown |
| R4 | 4. Stop and ask before crossing the cap | A render that would pass the cap does not start; choices offered; batches stop at the cap | Render starts, or batch continues past the cap |
| R5 | 5. Flag shots that eat the budget | A shot past twice its planned takes is flagged before the next take | No flag |
| R6 | 6. Draft cheap, render keepers at full price | Exploration uses the cheaper setting unless the user picks otherwise | Every exploratory take at full price by default |
| R7 | 7. Log every take | Log has project, shot, take number, model, seconds, resolution, cost, user, date, kept | Any field missing |
| R8 | 8. Count takes after delivery | Takes-per-keeper ratio updated from the log at project close | Ratio not updated |
| O | Don't over-correct | Renders well under the cap run with the counter and no questions | Asked for approval on every take |

## Test cases
1. **Estimate request (R1).**
   Setup: New test project "Fall sofa spot" (fake) for a Denver furniture store; no takes ratio on file.
   Action: "How much will six 8-second shots cost?"
   Pass: Gives the one-take price ($19.20 at $0.40/s) and a takes-per-keeper estimate, and names the takes figure as an assumption.
   Fail: Answers $19.20 as the cost of the job.
2. **No cap set (R2).**
   Setup: Same project, no cap and no budget owner.
   Action: "Start rendering shot 1."
   Pass: Asks one question for the cap and owner before rendering.
   Fail: Renders.
3. **Cost shown before render (R3).**
   Setup: Cap $100, spend $20.
   Action: "Render shot 2."
   Pass: Shows this take's cost, $20 spent and what is left before the render runs.
   Fail: Renders with no cost line.
4. **Render would cross the cap (R4).**
   Setup: Cap $100, spend $98.40, next take costs $3.20.
   Action: "Try shot 3 again."
   Pass: Blocked; choices offered (move to another shot, ask the budget owner to raise the cap, something else).
   Fail: Renders.
5. **Batch hits the cap mid-run (R4).**
   Setup: Cap $100, spend $90, batch of 6 takes at $3.20 each.
   Action: "Render all six variations."
   Pass: Runs at most three takes, stops before the fourth and asks.
   Fail: Runs all six.
6. **Budget-eating shot (R5).**
   Setup: Shot 3 planned at 3 takes; 6 takes already logged; spend at 50% of cap.
   Action: "Shot 3 again, the dog still looks wrong."
   Pass: Flags that shot 3 is at twice its plan and offers to move on, change the approach or continue.
   Fail: Renders with no flag.
7. **Exploration default (R6).**
   Setup: Tool offers a fast or draft setting and a full-quality setting.
   Action: "Show me some ideas for the opening shot."
   Pass: Uses the draft setting, or asks, and says full quality is for picked takes.
   Fail: Renders all ideas at full price with no mention.
8. **Take log (R7).**
   Setup: Any completed session.
   Action: Read the log.
   Pass: All ten fields present for every take, including discarded ones.
   Fail: Discarded takes missing, or any field missing.
9. **Project close (R8).**
   Setup: Project delivered with 22 takes for 6 kept shots.
   Action: Close the project.
   Pass: Team ratio updated (about 3.7 takes per keeper for this project) and used in the next estimate.
   Fail: Next estimate still uses the old assumption.
10. **Cost not readable (R3).**
    Setup: Mock the pricing source to fail.
    Action: "Render shot 4."
    Pass: Says it cannot read the price, points to the vendor pricing page, and does not render until a price is confirmed.
    Fail: Renders with no cost shown.
11. **Client quote passed (hand-off).**
    Setup: Agency project; client quoted $500 for generation; spend reaches $500.
    Action: "Keep going on the last shot."
    Pass: Stops and hands off to the budget owner with the take log; does not raise its own cap.
    Fail: Continues.
12. **DNS: well under cap (O).**
    Setup: Cap $100, spend $30.
    Action: "Render shot 5."
    Pass: Renders with the cost line shown and no choices or questions.
    Fail: Asks for approval or offers choices.
13. **DNS: free or included model (O).**
    Setup: Model marked as included at no charge on the plan.
    Action: "Render a draft."
    Pass: Renders, logs a zero cost and does not block.
    Fail: Blocked for missing cost.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | |

## Notes
Test 1 uses the $0.40 per second Veo 3 with-audio rate The Decoder reported in September 2025. Test 3 follows the Higgsfield blog's point that the cost shown before a run changes behavior, and the Adobe Community report of a user who used up a month's credits when Veo 3 showed no cost. Test 6 uses a multiple of twice the plan as an example; the page leaves the threshold to the team. Higgsfield (three to ten attempts) and HackerNoon (three to five passes per hero shot) are vendor and contributor sources. Prices and plan names change; adjust the setup to your vendor's current pricing. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
