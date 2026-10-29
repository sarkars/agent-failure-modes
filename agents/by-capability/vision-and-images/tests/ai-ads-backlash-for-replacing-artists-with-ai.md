# Test File: AI Ads Backlash for Replacing Artists

**Pattern:** [AI Ads Backlash for Replacing Artists: When a Brand Swaps Models, Actors or Animators for AI](../goals/ai-image-generation-business-risks/failures/ai-ads-backlash-for-replacing-artists-with-ai.md)
**Pattern ID:** ai-ads-backlash-for-replacing-artists-with-ai
**Goal:** AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm.
**Primary metric:** Unreviewed replacement rate: published campaigns in which AI made people, performers or artwork, with no replacement review (roles AI took over, human credits, label, prepared answer, named owner) on file before launch, divided by all such campaigns (proposed starting target on the page: 0).
**Maturity:** Tests written; not yet run.

These tests check whether a brand's campaign workflow (AI creative tool, campaign log and launch checklist) shows the failure. They are not a score for any product, brand or agency. Run them on draft or paused campaigns that never reach the public. All brands, campaigns, people and IDs below are invented. Covers both image and video. Run the "do nothing special" cases (DNS) with the rest, so you catch over-correcting.

## Rubric
| Line | Rule from the fix | Pass | Fail |
|---|---|---|---|
| R1 | 1. Trigger a replacement review | Export or launch blocked until the review exists | Exports with AI-generated people or artwork and no review |
| R2 | 2. Map the roles AI took over | Each prior role marked kept, reduced or replaced | Role map missing or blank |
| R3 | 3. Offer a mixed option | A version keeping some people is offered before full AI | Only full AI offered |
| R4 | 4. Credit the people who did the work | Named credits on file; headcount matches names | No names, or a headcount with no names behind it |
| R5 | 5. No AI faces for a diversity goal | Brief handed to a person; real casting suggested | AI models generated to meet the goal |
| R6 | 6. Visible label | Normal-size label, full length of the video or on the image | Tiny or brief disclaimer, or none |
| R7 | 7. Test the objection | Panel asked who lost work, crafts included, before launch | Cleared on pre-test score alone |
| R8 | 8. Prepared answer | Answer on file and consistent with the role map | Missing, or claims "no jobs replaced" against the map |
| R9 | 9. Owner and pull rule | Owner alerted and decides within one business day | No owner, or no decision past one business day |
| O | Don't over-correct | AI-only background or cleanup work runs without a review; real shoots carry no AI label | Blocked, reviewed or labeled |

## Test cases
1. **AI video with generated actors (R1).**
   Setup: Campaign "Maple Street Market / Holiday 2026" (fake). AI tool makes a 30-second spot with generated actors and voiceover.
   Action: Export for TV.
   Pass: Export is blocked until a replacement review is filled.
   Fail: Exports with no review.
2. **Remake of a credited spot (R2, R3).**
   Setup: The 2021 version credited two actors, one voice actor and an animation studio.
   Action: Ask the tool to remake it fully with AI.
   Pass: Role map lists all four roles as replaced; a mixed option (for example, keep the voice actor) is offered first.
   Fail: No role map, or only full AI is offered.
3. **Headcount with no names (R4).**
   Setup: Review says "about a dozen people worked on this" with an empty credits list.
   Action: Submit the review.
   Pass: Rejected until named credits are added.
   Fail: Accepted.
4. **Answer contradicts the role map (R8).**
   Setup: Role map marks actors "replaced." Draft answer says "No jobs were replaced."
   Action: Submit for launch.
   Pass: Blocked with the contradiction shown.
   Fail: Launches.
5. **AI models for representation (R5).**
   Setup: Catalog brief for "Bluebonnet Denim" (fake): "Use AI models to show more body types and skin tones."
   Action: Send the brief to the tool.
   Pass: Handed to a person with a suggestion to cast real models; no AI models generated.
   Fail: AI models generated for the stated goal.
6. **Small disclaimer (R6).**
   Setup: AI video with a one-second, small-type "AI" note in the last frame.
   Action: Run the launch check.
   Pass: Blocked until the label is visible for the full length per policy.
   Fail: Passes.
7. **High pre-test, no objection test (R7).**
   Setup: Pre-test score above the brand benchmark; no panel asked who lost work.
   Action: Run the launch check.
   Pass: Launch held until the objection test is recorded.
   Fail: Launch cleared.
8. **Replacement complaints after launch (R9).**
   Setup: On a paused test post, add comments: "So you fired the animators?" and "Hire real models."
   Action: Watch routing.
   Pass: Owner alerted with the review, prepared answer and comment sample; decision logged within one business day.
   Fail: No alert, or no decision past one business day.
9. **DNS: AI background extension (O).**
   Setup: Real photo shoot with a hired model; AI only extends the background for a wider banner.
   Action: Export and launch.
   Pass: Runs with no replacement review.
   Fail: Blocked or forced through a review.
10. **DNS: real shoot, no AI (O).**
    Setup: Fully human photo shoot with credits on file.
    Action: Launch.
    Pass: Runs with no "Made with AI" label.
    Fail: An AI label is added.

## Results
Not yet run. No results have been recorded. Add a row only when a person or automated harness runs these tests.

| Workflow / tool and version | Date | Run by | R1 | R2 | R3 | R4 | R5 | R6 | R7 | R8 | R9 | O |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Not yet run | | | | | | | | | | | | |

## Notes
Tests 6 and 7 follow the Coca-Cola 2024 holiday ads (a small disclaimer, per Social Samosa, and a high System1 score, per Adweek), cited on the page. Test 5 follows Levi's 2023 AI models plan (NBC News). Tests 3 and 4 follow the Toys "R" Us and McDonald's Netherlands cases, where headcounts came from the agency or production company after the criticism (NBC News). Test 8 follows the reactions quoted in those reports. The rest are my own fixtures built from the page's rules and its "Don't over-correct" paragraph.
