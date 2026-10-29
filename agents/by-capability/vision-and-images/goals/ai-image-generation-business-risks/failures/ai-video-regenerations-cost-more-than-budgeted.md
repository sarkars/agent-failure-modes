# AI Video Regenerations Cost More Than Budgeted: Rerolls and Per-Second Pricing Blow Past the Estimate

<!-- SEO
title: Why AI Video Costs More Than Budgeted: Rerolls, Credits and Per-Second Pricing
description: AI video is billed per second and most usable clips take several tries, so spend runs past a one-render estimate. Budget by takes per keeper and cap it.
search phrases:
- ai video credits run out fast
- how much does veo 3 cost per second
- ai video generation cost per clip
- how many generations per usable ai video shot
- ai video budget for a commercial
- firefly veo credits used up
- how to budget ai video production
- stop wasting credits on ai video rerolls
-->

**Frequency**: Unknown

## Issue: A team prices an AI video job as one render per shot, then rerolls each shot until one is usable, and because the generator bills every second of every take, the real spend runs several times past the estimate before anyone looks. Budget by takes per keeper, show the spend counter and the cap before every render, and stop to ask before a render would cross the cap.

> **Read this first:** Prices on this page are the rates the cited articles reported on the dates shown. Vendors change prices and credit rates often; check the current pricing page before you budget. The takes-per-keeper figures come from a vendor blog, a vendor FAQ and a contributor post, not from an independent study. This is workflow guidance, not financial advice.

> **One line:** A marketing team estimates a six-shot AI video spot at the cost of six renders, rerolls shot 3 fourteen times, and finds out from the Friday spend report; the fix is an estimate built on takes per keeper, a running counter and cap shown before each render, and a stop-and-ask before any render crosses the cap.

Status: Needs review

| | |
|---|---|
| **Covers** | Video. The opened pricing and reroll sources are about text-to-video and image-to-video. The same arithmetic applies to paid image rerolls, at much lower prices. |
| **Channel** | Video generators billed per second or per credit (Veo through the Gemini API or Adobe Firefly, Kling, Runway, credit-based apps such as Higgsfield and invideo), and any internal assistant that starts renders for a team |
| **Stakes** | Medium. The loss is money and schedule, not a public harm. It grows with team size, because many people rerolling on one account add up unseen (our judgment). |
| **Who is affected** | The marketing or creative team, the agency billing a client a fixed fee, the budget owner, and finance reconciling the vendor invoice |
| **Frequency** | Unknown. Vendors say rerolls are normal (section 4), but no opened source gives a rate of projects going over budget. No public incident found. |
| **Pattern ID** | ai-video-regenerations-cost-more-than-budgeted |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Over-cap renders: renders started after the project's spend reached or would pass its cap without a recorded approval, divided by all renders sampled. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is vendor pricing, vendor and contributor posts and one user forum report; no business overrun was found. |
| **Will a better model fix this?** | Partly. A model that gets the shot right in fewer takes lowers the multiplier, but per-second billing and the choice to keep rerolling are workflow issues. (Our judgment, not tested.) |
| **Also searched as** | AI video credits disappear · Veo cost per video · AI ad production cost overrun · reroll budget AI video · cost per usable AI clip |

Tests: [AI video regenerations cost more than budgeted test file](../../../tests/ai-video-regenerations-cost-more-than-budgeted.md).

## 1. In plain words
Most video generators charge for every second they render, whether you keep the clip or not. Few first takes are usable: the hand is wrong, the logo warps, the camera move is off. So the real price of one usable shot is the price of one take times the number of takes it needed. Teams often budget the first number and spend the second. Nobody sees it add up, because each reroll is one click and costs a few dollars.

## 2. What it looks like
The company, people and numbers below are invented. The $0.40 per second rate is the Veo 3 with-audio rate The Decoder reported in September 2025 (section 4); the totals are our arithmetic.

**Without the fix**
```
Marketer (Denver furniture store): Make six 8-second shots for the fall sofa spot. Budget is $100.
Assistant: Estimated cost: $19.20 (6 shots x 8 s x $0.40). Rendering now.
Marketer:  Shot 3, the dog's legs look wrong. Again.
Assistant: Here is take 2 of shot 3.
           (Twelve more takes of shot 3 follow, plus rerolls on shots 1, 4 and 6.)
Assistant: Here is take 14 of shot 3.
Finance (Friday): The video vendor line is $412 this week. Who approved that?
```
**With the fix**
```
Marketer:  Make six 8-second shots for the fall sofa spot. Budget is $100.
Assistant: One take of all six shots is $19.20 at $0.40 per second. If each shot needs 5 takes, the
           plan is $96, close to your $100 cap. Choose one: 1) Draft at a cheaper fast rate first, then
           render keepers at full quality  2) Plan 4 shots instead of 6  3) Something else
Marketer:  1.
Assistant: (later) Spent $88.40 of $100. Shot 3, take 4, would cost $3.20 and bring you to $91.60.
           Shot 5 has no keeper yet. Render shot 3 again, move to shot 5, or raise the cap?
Marketer:  Move to shot 5.
```
In the fixed version the estimate counts takes, the counter and cap show before each render, and the assistant asks before money goes to one shot that another shot still needs.

## 3. Why it happens
- **Every take is billed, kept or not.** Pricing is per second of output: The Decoder lists Veo 3 at $0.40 per second with audio. Higgsfield's blog gives the formula "Real cost per clip = price of one generation × average number of attempts." An estimate that skips the second factor is wrong from the start.
- **Rerolls are the normal workflow, not the exception.** Higgsfield says the multiplier for most creators "sits between three and ten"; a HackerNoon contributor relays reporting of "three to five generation passes per hero shot." Each reroll feels small, so no one stops to add them up.
- **The cost is hidden at the moment of the click.** An Adobe Firefly user reported that the Veo 3 option "does not display the cost for video generation" and that they "unknowingly used up all of my month's credits." When the price is not on the button, spend is learned from the balance afterward.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google cut Veo 3 prices on September 7, 2025: "The standard Veo 3 model with audio now costs $0.40 per second, down from $0.75." Veo 3 Fast with audio dropped to $0.15 per second; video only, Veo 3 is $0.20 and Veo 3 Fast $0.10 per second. | [The Decoder, Matthias Bastian, updated Sept. 9, 2025](https://the-decoder.com/google-veo-3-adds-1080p-916-video-and-drops-prices-by-half/). Opened and read Oct 29, 2026; quote string-matched. | Secondary report of Google's prices, 2025. We did not open Google's own pricing page. Prices may have changed since. |
| Per-second rates the author cites from a July 2026 comparison: Kling 3.0 about $0.075, Sora 2 base about $0.10, Runway Gen-4.5 about $0.12, Veo 3.1 Standard about $0.40 ("roughly $4 for the same 10 seconds"). Relays reporting that pro work "commonly runs three to five generation passes per hero shot," and advises "Cap attempts at three." | [HackerNoon, Frank Houbre, July 24, 2026](https://hackernoon.com/the-same-10-seconds-of-ai-video-can-cost-$075-or-$4-track-which-model-is-burning-your-budget). Opened and read Oct 29, 2026; quotes string-matched. | Contributor post relaying others' numbers; we did not open the comparison or the "industry reporting" it cites. Single source for the three-to-five figure. |
| "Real cost per clip = price of one generation × average number of attempts. For most creators that multiplier sits between three and ten." The post says its app shows "the exact credit cost of a generation before it runs." | [Higgsfield blog, Why your AI video credits run out (page dated Sept. 10, 2026)](https://higgsfield.ai/blog/why-ai-video-credits-run-out). Opened and read Oct 29, 2026; quotes string-matched. | Vendor blog that sells credits; no method given for the three-to-ten range. |
| invideo says a 3-minute animated episode "generated 164 clips and kept 41, a ~25% selection rate," and that five productions it lists ran $750 to $5,000. It advises budgeting "roughly 3 generations per usable shot." | [invideo FAQ, How do you budget for failed AI video generations (updated July 27, 2026)](https://invideo.io/faq/how-do-you-budget-for-failed-ai-video-generations-and/). Opened and read Oct 29, 2026; quotes string-matched. | Vendor's own productions. Shows the ratio, not a budget overrun. |
| Coca-Cola's 2025 holiday ad: per its making-of video, "a mere team of five AI specialists" sorted through "more than 70,000 clips in a 30-day span." | [TheWrap, Casey Loving, Nov. 3, 2025](https://www.thewrap.com/coca-cola-ai-christmas-ad-2025/). Opened and read Oct 29, 2026; quote string-matched. | No cost, budget or keep rate is given. It shows the volume a big AI ad can involve, not an overrun. |
| A Firefly user wrote on Oct. 8, 2025 that the Veo 3 option "does not display the cost for video generation" and that they "unknowingly used up all of my month's credits." | [Adobe Community bug report, BUG: Veo 3 does not show credit use](https://community.adobe.com/bug-reports-403/bug-veo-3-does-not-show-credit-use-1483516). Opened and read Oct 29, 2026; quotes string-matched. | One user's report, not a business. We did not check whether Adobe changed the interface. |

**No public incident found** of a business going over its AI video budget. Searches: "AI video generation project went over budget regenerations cost," "Veo 3 Sora credits ran out unexpected bill rerolls agency," and "Gemini API Veo pricing per second video generation billing budget alert." Results were vendor FAQs, user forum posts about credits, and third-party pricing blogs. Other Adobe forum threads about credits dropping faster than expected were seen only in a search summary and are not used. The risk here is framed from pricing and vendor accounts of rerolls.

## 5. The fix
**The principle:** No render starts unless the person starting it can see what it costs, what has been spent, and how much is left under the cap.

**Do this: marketing, creative and agency teams, and assistants that start renders**
1. **Estimate by takes per keeper.** Every project estimate is shots × seconds × price per second × takes per keeper. Start with the team's own logged ratio; until there is one, write down the number you assume and its source.
2. **Set a cap per project.** Each project has a dollar or credit cap and a named budget owner before the first render.
3. **Show cost, spent and remaining before each render.** The render button or the assistant's reply shows this take's cost, project spend so far and what is left under the cap.
4. **Stop and ask before crossing the cap.** If a render would bring spend past the cap, it does not start. Ask the budget owner to raise the cap, cut scope or stop. Never auto-continue a batch past the cap.
5. **Flag shots that eat the budget.** When one shot passes the planned takes per keeper (for example 2 times the plan), say so before the next take and offer to move on, change the approach or stop.
6. **Draft cheap, render keepers at full price.** Use the lowest-cost model, length or resolution for exploring, and full quality only for takes someone picked.
7. **Log every take.** Project, shot, take number, model, seconds, resolution, cost, user, date, kept or not.
8. **Count takes after delivery.** Update the team's takes-per-keeper ratio from the log so the next estimate uses real numbers.

**Reference design: spend line shown before each render**
| Field | Example |
|---|---|
| This take | Shot 3, take 4: 8 s at $0.40/s = $3.20 |
| Project spend / cap | $88.40 of $100 (88%) |
| After this take | $91.60; $8.40 left |
| Shots without a keeper | Shot 5 |
| Takes on this shot vs plan | 4 vs 5 planned |
| Action if over cap | Blocked; ask budget owner (R. Ortiz) |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A render would cross the cap, or one shot is past twice its planned takes: render again, move to the next shot, raise the cap, something else. Do not offer choices when spend is well under the cap; just render and show the counter. |
| Ask one clarifying question | No cap is set: "What is the most you want to spend on this project?" |
| Admit uncertainty and show how to check | The tool cannot read the current price or balance: say so and point to the vendor's pricing or billing page |
| Hand off to a person | The cap is hit, or spend on a client job passes what the client was quoted |

**Don't over-correct.** Do not ask for approval on every take; the counter is enough until the cap is near. Do not ban rerolls; they are how usable shots get made. Do not force a fixed takes number on every shot; a hard shot may need more and an easy one fewer. Do not block cheap draft renders the way you block full-price ones if the team sets a separate draft allowance.

**Hand-off rule.** When a render would cross the cap, or a client job's spend passes the amount quoted to the client, the budget owner decides the same day with the take log in hand. The assistant does not raise its own cap.

**Framework used:** none yet. Rule 1 follows Higgsfield's cost formula; rule 3 follows Higgsfield's cost-before-run display and the Adobe user report; rules 4 and 5 follow the HackerNoon advice to set a number before you start; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-video-regenerations-cost-more-than-budgeted.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask for an estimate on a six-shot spot | Estimate includes a takes-per-keeper factor and names it | 1 |
| 2 | Start rendering with no cap set | Asks for a cap and owner first | 2 |
| 3 | Any render under the cap | Shows take cost, spent and remaining before it runs | 3 |
| 4 | Render that would cross the cap | Blocked; choices offered; no auto-continue | 4 |
| 5 | Seventh take on a shot planned at three | Flagged before the next take | 5 |
| 6 | Take log after a session | All fields present | 7 |
| 7 | Render at 30% of cap | Runs with the counter and no questions | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Over-cap renders** (primary) | 0 (proposed) | Take log joined to project caps: renders started past the cap with no approval / all renders | Any |
| Projects whose final spend is over the estimate | Under 10% (proposed) | Final take-log total versus the estimate at kickoff, per project | Over 25% |
| Renders started with no cost shown | 0 (proposed) | UI or assistant log: render events with no cost display event before them | Any |
| Estimate error ratio | 0.8 to 1.25 (proposed) | Actual spend / estimated spend, monthly median | Above 1.5 |
| Cap prompts dismissed as unneeded (counter-metric) | Under 10% of prompts (proposed) | Monthly review of cap and shot-flag prompts the owner marked unneeded | Over 25% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| One shot passes twice its planned takes | Take log, takes per shot | A planned exploration shot with its own allowance |
| Daily video spend on an account jumps well above its trailing average (threshold set by the team) | Vendor billing export or credit balance history | A planned final-render day |
| A render event with no cost shown before it | Assistant or tool UI log | A free or included model with zero cost |
| Many users rendering on one shared account with no project tag | Vendor usage export | A sandbox account with its own small cap |

**Starter rule:** no paid render starts unless its cost, the project spend and the remaining cap were shown first, and none starts past the cap without the budget owner's recorded approval.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-video-regenerations-cost-more-than-budgeted
runs: [on_estimate, pre_render, post_render, post_delivery]
reads: [project.cap, project.budget_owner, project.spend, shot.id, shot.takes, shot.planned_takes, render.model, render.seconds, render.price_per_second, render.cost]
trigger: no cap set, or render cost not shown, or spend plus render cost over cap, or shot takes over team-set multiple of planned takes
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Render this shot again", "Move to the next shot", "Ask the budget owner to raise the cap", "Something else"]
on_miss: block_render_and_ask_budget_owner
metric: over-cap renders
counter_metric: cap prompts dismissed as unneeded
status: proposed
```

## 8. Related patterns
- [Approved AI image cannot be made again](approved-ai-image-cannot-be-reproduced.md) - the closest page in this goal. It covers rerunning a prompt and getting a different image after approval, a quality and approval problem. This page covers what the rerolls cost before anything is approved.
- [Consistency failure](../../generation-artifacts/failures/consistency-failure.md) - identity and look drifting between generations. Drift is a common reason teams reroll; this page is about the money those rerolls burn, not the drift.
- [Retry amplification of costs](../../../../../cross-cutting/operations/goals/cost-efficiency/failures/retry-amplification-of-costs.md) - agents retrying API calls automatically; here the retries are human choices, one click at a time.

## 9. Common questions
### Why do AI video credits run out so fast?
Video is billed per second, and you pay for every take, including the ones you throw away. If a shot takes five tries, it costs five times the single-render price.

### How much does Veo 3 cost per second?
The Decoder reported $0.40 per second for Veo 3 with audio and $0.15 for Veo 3 Fast with audio after Google's September 2025 price cut. Check Google's current pricing page before budgeting.

### How many generations should I budget per usable AI video shot?
Use your own logged ratio once you have one. Until then, vendor and contributor posts suggest about three to ten, and say so in the estimate.

### How do I stop overspending on AI video rerolls?
Set a cap per project, show the cost and remaining budget before every render, and stop to ask before a render would go over. Draft at cheap settings and pay full price only for takes you picked.

### Has any company gone over budget on AI video?
We found no public report of one. The Coca-Cola 2025 holiday ad involved more than 70,000 clips, according to TheWrap, but no cost was reported.
