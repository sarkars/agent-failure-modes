# AI Video Physics Mistakes: Rigid Objects That Bend, Liquids That Pour Wrong, Motion With No Cause

<!-- SEO
title: AI Video Physics Mistakes: How to Catch Them Before You Post
description: AI video bends rigid objects, pours liquid wrong and moves things with no cause. List each interaction, check it frame by frame and fix it before posting.
search phrases:
- ai video physics wrong
- ai video bad physics
- why does ai video get physics wrong
- sora physics mistakes
- ai video liquid pouring wrong
- ai generated video objects bend
- ai video unnatural movement
- how to check ai video for physics errors
-->

**Frequency**: Common

## Issue: In AI-generated video, things move in ways that could not happen: a steel can bends like rubber in a hand, coffee pours into a glass and the level never rises, ice passes through the glass wall, or a body goes limp like jelly mid-fall. A team that judges the clip on "looks real" posts it, and viewers notice the motion. Before generating, list every contact, pour, drop and collision in the shot; after, check each one frame by frame against how the materials really behave, and fix, cut or replace any shot that fails before a named person signs off.

> **One line:** A Chicago cold brew brand posts a 6-second AI clip where its steel can bends as a hand squeezes it and the coffee in the glass never rises; the fix is an interaction list written before generation, a frame-by-frame physics check of each interaction, live footage for any product feature the clip claims, and a named reviewer's sign-off.

Status: Needs review

| | |
|---|---|
| **Covers** | Video. Motion and material behavior inside a clip: rigid objects that bend, liquids that flow, fill or splash wrongly, objects that pass through each other, and motion that starts or stops with no cause. Objects that appear, vanish or change count are covered by the [goal C page on objects between frames](../../ai-video-consistency/failures/ai-video-objects-appear-vanish-or-change-between-frames.md). |
| **Channel** | Text-to-video and image-to-video tools, and assistants that call them, used for product clips, social ads and explainer videos |
| **Stakes** | Medium. A pour, grip or drop that breaks physics shows the product doing something it does not do, and unnatural motion is one of the signs reporters and viewers use to spot an AI ad (our judgment, drawing on section 4). |
| **Who is affected** | Viewers, the brand whose product is shown, and the team that approved the clip |
| **Frequency** | Common in tests: in VideoPhy, the best 2024 model followed both the caption and physics in 39.6% of videos (section 4). No opened source gives a rate in published business video. |
| **Pattern ID** | ai-video-motion-breaks-physics |
| **Family** | [AI Image Artifacts: Hands, Anatomy and Physics](../README.md) |
| **Goal** | AI images and video show bodies, objects and motion that could exist: correct hands and anatomy, shadows and reflections that match, and physics that holds. |
| **Primary metric** | Unchecked-or-escaped physics rate: published AI video shots with an interaction (contact, pour, drop, collision) that have no recorded physics check, or where a physics defect is found after publish, divided by all such published shots. Proposed starting target: 0. |
| **Maturity** | Researched; tests written, not yet run. Evidence is one vendor technical report, one news article relaying a vendor page, four arXiv papers and two news reports. |
| **Will a better model fix this?** | Partly. Models are improving, but the PhyGenBench authors found that "simply scaling up models or employing prompt engineering techniques is insufficient," and Physics-IQ found visual realism unrelated to physical understanding, so a clip that looks real still needs a physics check (our judgment, drawing on section 4). |
| **Also searched as** | AI video weird motion · AI video liquid looks fake · AI ad unnatural movement · objects melt in AI video · AI video glass bends |

Tests: [AI video motion breaks physics test file](../../../tests/ai-video-motion-breaks-physics.md).

## 1. In plain words
A cold brew brand asks a video tool for a pour shot: a hand lifts its steel can and fills a glass of ice. At full speed it looks slick, so it goes up. Then people rewatch it. The can dents and bends like rubber when the hand grips it. Coffee streams out, but the glass never gets fuller. One ice cube slides through the glass wall. Every frame looks like a photo. The motion between them is what could not happen, and nobody checked it.

## 2. What it looks like
The brand, people and timecodes below are invented.

**Without the fix**
```
Marketer:  Make a 6-second clip: a hand lifts a can of Lakeshore Cold Brew and pours
           it into a glass of ice on a bar top.
Assistant: Here is your clip. (One take. At 0:02 the steel can bends under the grip;
           from 0:03 the level in the glass stays the same; at 0:04 an ice cube
           slides through the glass wall.)
Marketer:  Gorgeous. Posting it with the launch tonight.
Commenter (next day): Why is the can made of rubber? And the glass never fills up.
```
**With the fix**
```
Marketer:  Make a 6-second clip: a hand lifts a can of Lakeshore Cold Brew and pours
           it into a glass of ice on a bar top.
Assistant: Interactions in this shot: hand grips can (can stays rigid), coffee pours
           (falls, level rises), coffee meets ice (ice moves, stays inside the glass).
           No product feature claim is shown, so a generated take can work. Anything to add?
Marketer:  OK.
Assistant: Checked 3 takes frame by frame. Take 1: can bends at 0:02. Take 2: level
           flat from 0:03. Take 3: all three interactions hold, 0:00 to 0:06.
           Take 3 sent to Dana Reyes (brand lead) with stills at each interaction.
```
The fixed version lists each interaction and how the materials should behave before generating, checks each one frame by frame, names each defect with a timecode, offers only the take that passed and ends with a person signing off.

## 3. Why it happens
- **The models copy what training video looked like; they do not apply physical laws.** In a controlled test, Kang et al. found models "fail to abstract general physical rules" and instead mimic "the closest training example." Their test used a 2D simulator and models the authors trained, not a product.
- **Looking real and moving correctly are different skills.** Physics-IQ found that the model whose videos were hardest to tell from real ones did not understand physics better; "visual realism does not imply physical understanding." A reviewer who asks "does it look real?" misses the defect.
- **Contacts between solids, and fluids, are the hardest cases.** VideoPhy found every model it tested did worst on solid-solid interactions such as "bottle topples off the table," and lists rigid objects deforming, unnatural fluid flow and objects that "unnaturally penetrate each other" as common failures.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "Sora currently exhibits numerous limitations as a simulator. For example, it does not accurately model the physics of many basic interactions, like glass shattering." | [OpenAI, "Video generation models as world simulators," Feb 15, 2024](https://openai.com/index/video-generation-models-as-world-simulators/). Opened Oct 29, 2026. | Vendor technical report on its first Sora model; no rates. |
| OpenAI's Sora page said the model "may struggle with accurately simulating the physics of a complex scene" and "may not understand specific instances of cause and effect." The writer adds that "Feet and hands can be bent in the wrong direction." | [Ben Dickson, BD TechTalks, Feb 19, 2024](https://bdtechtalks.com/2024/02/19/what-will-come-after-openais-sora/). Opened Oct 29, 2026. | Secondary: the vendor page was not opened in this run (the Wayback Machine blocked the request and the live page returns 403). The limbs line is the writer's own view. |
| VideoPhy: 688 captions of solid-solid, solid-fluid and fluid-fluid interactions, judged by people. The best model, CogVideoX-5B, made videos that follow the caption and physics "for 39.6% of the instances." In the first version, all models did worst on solid-solid interactions, where the best (Pika) reached 13.6%. | [Bansal et al., "VideoPhy," arXiv 2406.03520](https://arxiv.org/abs/2406.03520) (v1 June 5, 2024; v2 Oct 3, 2024). Abstract (v2) and v1 HTML opened Oct 29, 2026. | Preprint; the authors' own tests on 2024 models. The 39.6% is from v2, the 13.6% from v1, which tested a different set of models. |
| VideoPhy's failure examples include "the metal spoon should not deform," "the tea flows through the cup," a stream of water "floating upwards," and juice that increases "without new substances being added." | Bansal et al., v1 appendix, as above. | Qualitative examples picked by the authors; no rate per type. |
| PhyGenBench: 160 prompts across 27 physical laws. The best model, Gen-3, scored 0.51; "simply scaling up models or employing prompt engineering techniques is insufficient." | [Meng et al., "PhyGenBench," arXiv 2410.05363](https://arxiv.org/abs/2410.05363) (Oct 7, 2024). Abstract and HTML opened Oct 29, 2026. | Preprint. Scores come from the authors' automated evaluator built on vision-language models, which they report aligns with human feedback. |
| Physics-IQ: 396 real videos across 66 scenarios. The best model scored 24.1% of the possible 100%. Sora's videos were the hardest for Gemini 1.5 Pro to tell from real (55.6%, chance is 50%), yet realism was "uncorrelated with physical understanding" (r = -0.46, p = .247). | [Motamed et al., "Physics-IQ," arXiv 2501.09038](https://arxiv.org/abs/2501.09038) (v1 Jan 14, 2025; v3 Feb 27, 2025). Abstract and v1 HTML opened Oct 29, 2026. | Preprint. Models continue a real video rather than make one from text, so it is not the ad workflow. Few models, and the correlation is not significant either way. |
| Kang et al. trained video models in a 2D simulator of moving and colliding objects: "perfect generalization within the distribution" but "failure in out-of-distribution scenarios"; "scaling alone is insufficient." | [Kang et al., arXiv 2411.02385](https://arxiv.org/abs/2411.02385) (v1 Nov 4, 2024; v2 June 22, 2025). Abstract opened Oct 29, 2026. | Abstract only. A lab simulator, not a product. Used only for the cause in section 3. |
| Some AI ads show people who "look too polished and move in unnatural ways," naming McDonald's and DoorDash ads. The article relays a November 2025 Kantar study in which consumers were put off by "distracting or unnatural visuals." | [Jess Weatherbed, The Verge, Jan 24, 2026](https://www.theverge.com/report/866775/ai-generated-ads-slop-human-creativity). Opened Oct 29, 2026. | A reporter's view. The Kantar study was not opened and is not used in the fix. |

**Incident (Netherlands, US production company):** In December 2025, McDonald's Netherlands removed an AI-generated Christmas ad after backlash. The Verge noted "a person falling while ice skating, only for their limbs to turn jellylike halfway through," and quoted the studio's AI division saying the ad took "seven intense weeks." Sources: [Stevie Bonifield, The Verge, Dec 9, 2025](https://www.theverge.com/news/841220/mcdonalds-ai-generated-christmas-ad) and [Elmira Aliieva, NBC News, Dec 11, 2025](https://www.nbcnews.com/world/europe/mcdonalds-ai-generated-christmas-advert-social-media-backlash-rcna248590), which says it was made by "the U.S. production company The Sweetshop Films" and Dutch agency TBWA/Neboko; both opened Oct 29, 2026. Caveat: the backlash was mostly about using AI and the ad's message; the skater is one shot a reporter pointed out. No US incident centered on physics was opened (searches in the run notes). The Coca-Cola truck wheels case is on the [objects between frames page](../../ai-video-consistency/failures/ai-video-objects-appear-vanish-or-change-between-frames.md) and is not repeated here.

## 5. The fix
**The principle:** A video is a set of claims about how things move. Each contact, pour and fall must behave the way its material does, and "it looks real" does not check that.

**Do this: teams and assistants that make AI video**
1. **List every interaction before generating.** For each shot, name each contact, grip, pour, drop, collision and splash, and how each material should behave ("steel can stays rigid; coffee falls and the level rises; ice stays inside the glass"). Ask the requester to confirm it.
2. **Product claims are not generated.** If the shot shows a feature the brand claims (a seal that does not leak, a towel that soaks up a spill, a lid that stays on when dropped), use live footage or a composite of real footage for that moment. A generated clip may show the setting and ordinary use, not proof of performance.
3. **Keep risky interactions few and short.** Prefer one interaction per shot, cut away from contacts and pours, or show the result instead of the action, since every VideoPhy model did worst on solid-solid contact.
4. **Check each listed interaction frame by frame.** Step through it and record pass or fail on: rigid things keep their shape; liquids fall, fill and stay inside containers; nothing passes through anything solid; motion starts and stops for a reason; bodies bend only at joints.
5. **Do not pass a shot on realism alone.** A "looks real" rating, from a person or a model, is not a physics check, because Physics-IQ found realism unrelated to physical understanding.
6. **Fix, cut or replace, then stop.** Trim before the defect, regenerate up to the team's retry limit, rewrite the shot to avoid the interaction, or use live footage. After the limit, offer those options; never post a take with a known defect.
7. **A named person signs off, and it is logged.** Log per shot: interaction list, takes checked, defects with timecodes, fix used, reviewer and date.

**Reference design: physics check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Interaction list | Written and confirmed before generation | Grip, pour, coffee meets ice |
| Rigid objects | Keep shape through contact | Can rigid 0:01-0:03 |
| Liquids | Fall, fill, stay inside | Level rises 0:03-0:06 |
| Contacts | Nothing passes through a solid | Ice inside glass |
| Product claim | Live footage, or none shown | No feature claim in this shot |
| Sign-off | Named, dated | D. Reyes, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every result: say which takes passed and name each physics defect with its timecode first |
| Ask one clarifying question | Before generating, to confirm the interaction list and how each material should behave |
| Offer choices: 2-4 options plus "Something else", free text open | The retry limit is reached or a product claim is in the shot: trim, rewrite the shot, live footage, something else |
| Hand off to a person | Always for the final frame-by-frame sign-off before publish |

**Don't over-correct.** Do not flag soft materials that should bend (fabric, foam, dough, a squeezed sponge) or a deliberate style such as cartoon squash-and-stretch. Do not flag physics the prompt asked to break on purpose (a product floating in a dream sequence), as long as the clip makes no claim about the product. Do not require an interaction list for clips with no contact or motion between objects (a slow pan over a still landscape). Do not regenerate without limit; each video run costs time and money (see [AI video regenerations cost more than budgeted](../../ai-image-generation-business-risks/failures/ai-video-regenerations-cost-more-than-budgeted.md)).

**Hand-off rule.** If a viewer, client or reviewer reports impossible motion in a published clip, send it to the approver and content owner the same day with the timecode and the log; if the defect is in a product claim, pull the clip the same day. [AI ad mistakes that go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) covers the public response.

**Framework used:** none yet. Rules 3 and 4 follow VideoPhy's failure types and its solid-solid result; rule 5 follows Physics-IQ; rules 1, 2, 6 and 7 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-video-motion-breaks-physics.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Can of cold brew poured into ice | Interaction list written and confirmed first | 1 |
| 2 | Steel can bends under the grip | Caught with timecode; take not offered | 4 |
| 3 | Glass level stays flat during the pour | Caught as a liquid failure | 4 |
| 4 | Realism score high, no physics check | Publish blocked | 5, 7 |
| 5 | Shot shows a bottle's leak-proof seal | Live footage required for that moment | 2 |
| 6 | Towel bends as it is folded | Not flagged | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked-or-escaped physics rate** (primary) | 0 (proposed) | Monthly: published AI shots with an interaction and no physics check in the log, plus shots with a physics defect reported after publish / all published AI shots with an interaction | Any |
| Product-claim shots made fully by AI | 0 (proposed) | Shot log: product-claim flag set and footage source "generated" | Any |
| Takes per approved shot | Track, no target | Generation log | Rising for 2 months |
| False physics flags (counter-metric) | Track, no target | Sample of flags on soft materials, intended styles or requested fantasy | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| AI shot with a pour, grip, drop or collision in the prompt published with no interaction list or physics check | Prompt log plus publish log | The motion was cut in editing and the final shot has no interaction |
| Shot approved with only a realism score or a "looks real" note | Review log | A physics check was recorded in a separate field |
| Shot flagged "product claim" with footage source "generated" | Shot log | The flag was wrong: the product is only used, with no feature claimed |
| Viewer comments with a timecode plus words like "rubber," "melts," "through the" or "physics" | Social comments on the post | A joke about an intended cartoon style |

**Starter rule:** no AI video shot with a contact, pour, drop or collision is published unless its log shows a confirmed interaction list, a frame-by-frame physics check with no open defects, and a named person's sign-off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-video-motion-breaks-physics
runs: [pre_generation, post_generation, pre_publish]
reads: [request.text, interaction_list, interaction_list.confirmed, shot.product_claim, shot.footage_source, shot.takes, shot.physics_check, shot.defects_with_timecode, review.realism_only, shot.fix_method, review.signoff, style.intended]
trigger: no confirmed interaction list, or shot without physics check, or open defect, or product claim generated, or retry limit reached, or no sign-off at publish
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Trim the shot before the defect", "Rewrite the shot to avoid the interaction", "Use live footage for this moment", "Something else"]
on_miss: block_publish
metric: unchecked-or-escaped physics rate
counter_metric: false physics flags
status: proposed
```

## 8. Related patterns
- [AI video objects appear, vanish or change between frames](../../ai-video-consistency/failures/ai-video-objects-appear-vanish-or-change-between-frames.md) - the closest existing page. It checks whether listed objects stay present and the same (count, shape, markings); this page checks how objects that are present move and interact (bending, pouring, passing through, motion with no cause).
- [AI video flickering between frames](../../ai-video-consistency/failures/ai-video-flicker-between-frames.md) - detail, light and texture that shimmer frame to frame; the motion can be correct and still flicker.
- [AI image generator wrong hands, fingers and anatomy](ai-image-generator-wrong-hands-fingers-and-anatomy.md) - wrong bodies in still images; a limb that bends where there is no joint during motion is checked here.
- [Quality drift](../../generation-artifacts/failures/quality-drift.md) and [artifact accumulation](../../generation-artifacts/failures/artifact-accumulation.md) - older pages on quality that degrades over many generations; a physics defect can appear in the first take.
- [AI product photos showing features the product does not have](../../ai-image-generation-business-risks/failures/ai-product-images-show-features-it-does-not-have.md) - the claims side of rule 2, when a generated product does something the real one does not.

## 9. Common questions
### Why does AI video get physics wrong?
The models learn what video tends to look like, not the laws behind it. In a lab test, Kang et al. found models copy the closest training example instead of a general rule, and OpenAI said its first Sora model did not model "many basic interactions, like glass shattering."

### How do I check an AI video for physics mistakes?
List every contact, pour, drop and collision first. Then step through each one frame by frame: rigid things keep their shape, liquids fall and fill, nothing passes through a solid, and motion has a cause.

### Can I use AI video to show how my product works?
Not to prove a feature. Use live footage or a composite of real footage for anything the ad claims the product does, such as a seal that does not leak, and use AI for the setting and ordinary use.

### If the video looks real, is the physics right?
No. Physics-IQ found that the model whose videos looked most real did not understand physics better, so check the motion separately.

### Will newer models fix AI video physics?
They are improving, but the PhyGenBench authors found that bigger models and better prompts alone were not enough. Keep the check whatever model you use.
