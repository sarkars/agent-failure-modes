# AI Video Objects Appear, Vanish or Change Between Frames: Extra Cups, Missing Props, Shifting Wheels

<!-- SEO
title: AI Video Objects Appear, Vanish or Change Between Frames: How to Catch It
description: AI video adds, drops or changes objects mid-clip: a third cup appears, a truck gains wheels. List what must stay, then check each shot frame by frame.
search phrases:
- ai video objects disappear between frames
- ai video objects appear out of nowhere
- sora objects spontaneously appear
- ai generated video continuity errors
- object permanence ai video
- coca cola ai ad wheels change
- how to check ai video for continuity mistakes
-->

**Frequency**: Common

## Issue: In an AI-generated video, an object that should stay put appears from nowhere, vanishes, or changes shape or count partway through a clip: a third latte slides into view, a tip jar is gone after a hand passes it, a truck gains a row of wheels. The team watches the clip once at full speed and posts it, and viewers find the mistake by pausing. Before generating, write down every object that must stay the same; after, check each shot frame by frame against that list and fix or drop any shot where something appears, vanishes or changes without a reason.

> **One line:** A Phoenix coffee shop posts an 8-second AI clip of a barista sliding two iced lattes across the counter, and at 0:05 a third cup appears; the fix is a continuity list written before generation, a frame-by-frame check of every shot against it, and a named reviewer who signs off before the clip goes out.

Status: Needs review

| | |
|---|---|
| **Covers** | Video. Objects that appear, vanish or change inside one clip or between shots of one video. A product or character that changes across a set of still images is covered by the pages in section 8. |
| **Channel** | Text-to-video and image-to-video tools, and assistants that call them, used for social clips, ads, explainer videos and product demos |
| **Stakes** | Medium. The clip shows something that did not happen (an extra product, a missing one), and a defect viewers find by pausing becomes the story, as in the Coca-Cola coverage in section 4 (our judgment). |
| **Who is affected** | Viewers, the brand named in the video, and the team that approved it |
| **Frequency** | Common, by our judgment: OpenAI listed spontaneous appearances as a known weakness of its first video model, and a 2026 benchmark of eight models calls the disappear-and-reappear case an open challenge (section 4). No opened source gives a rate in real business use. |
| **Pattern ID** | ai-video-objects-appear-vanish-or-change-between-frames |
| **Family** | [AI Video and Character Consistency Failures](../README.md) |
| **Goal** | AI video and image sets keep the same people, objects and look from frame to frame and image to image. |
| **Primary metric** | Unchecked-or-escaped continuity rate: published AI video shots with no recorded frame-by-frame continuity check, or with an object that appears, vanishes or changes found after publish, divided by all published AI video shots. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is one vendor page (read through the Wayback Machine), two news reports of that page, one arXiv survey, two arXiv abstracts or definitions, and one trade press incident. |
| **Will a better model fix this?** | Partly. In February 2024 OpenAI said it had "solved" keeping a subject the same when it briefly leaves view, yet listed spontaneous appearances as a weakness on the same page; in June 2026 MemoBench still called the disappear-and-reappear case an open challenge, and the November 2025 Coca-Cola trucks changed wheels between shots (our judgment, drawing on section 4). |
| **Also searched as** | AI video continuity error · object pops into AI video · AI video extra person appears · prop disappears AI clip · AI video glitch between frames |

Tests: [AI video objects appear, vanish or change between frames test file](../../../tests/ai-video-objects-appear-vanish-or-change-between-frames.md).

## 1. In plain words
A coffee shop asks a video tool for a short clip: a barista slides two iced lattes to a customer. It looks great at full speed. The marketer posts it. The next morning someone comments, "Where did the third latte come from? Pause at 0:05." Another says the tip jar vanished. Every frame looked real. The frames just did not agree with each other, and nobody checked them one by one.

## 2. What it looks like
The shop, people and handles below are invented.

**Without the fix**
```
Marketer:  Make an 8-second clip for Instagram: our barista slides two iced lattes
           across the counter to a customer.
Assistant: Here is your clip. (One generation; at 0:05 a third cup appears, and the
           tip jar is gone after the barista's arm passes it at 0:03.)
Marketer:  Looks great. Posting tonight.
Commenter (next morning): Where did the third latte come from? Pause at 0:05.
Commenter: The tip jar disappears too.
```
**With the fix**
```
Marketer:  Make an 8-second clip for Instagram: our barista slides two iced lattes
           across the counter to a customer.
Assistant: Continuity list before I generate: 2 iced lattes, 1 barista, 1 customer,
           1 tip jar, Copper Kettle logo on both cups. Anything else that must stay?
Marketer:  That's it.
Assistant: I stepped through three takes frame by frame. Take 1: a third cup appears
           at 0:05. Take 2: the tip jar is gone after 0:03. Take 3: all five items hold
           from 0:00 to 0:08, and nothing unlisted appears.
Assistant: Take 3 sent to Luis Ortega (social lead) with timecoded stills for his
           frame-by-frame sign-off before it posts.
```
The fixed version writes the list first, checks every frame of every take against it, names each defect with a timecode, offers only the take that passed, and ends with a person signing off.

## 3. Why it happens
- **The model keeps no list of what is in the scene.** OpenAI's own page says "Animals or people can spontaneously appear, especially in scenes containing many entities." Sun et al. describe "object mixing and disappearance" as distinct objects blending, which gives "inaccurate object counts."
- **Objects that leave view have to be remembered.** OpenAI described keeping a subject the same "even when it goes out of view temporarily" as "a challenging problem." MemoBench's authors note that most benchmarks check consistency "only while the target remains in view," and that the disappear-and-reappear case remains an open challenge.
- **State changes are not carried forward.** OpenAI's example: "a person might take a bite out of a cookie, but afterward, the cookie may not have a bite mark." An object can stay present and still change back.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Listed weaknesses of the current model: "Animals or people can spontaneously appear, especially in scenes containing many entities" (on a "Five gray wolf pups" sample); "unnatural object 'morphing'" (a basketball sample); and the cookie with no bite mark. | [OpenAI, Sora page, Wayback Machine snapshot of Feb 17, 2024](https://web.archive.org/web/20240217003848/https://openai.com/sora). Opened Oct 29, 2026; quotes string-matched. The live page ([openai.com/index/sora](https://openai.com/index/sora/)) returned 403. | Vendor statement about its first Sora model, February 2024. Not a test of later versions or other tools. |
| OpenAI also said: "we've solved a challenging problem of making sure a subject stays the same even when it goes out of view temporarily," and "Sora can also create multiple shots within a single generated video that accurately persist characters and visual style." | [PetaPixel, Jaron Schneider, Feb 15, 2024](https://petapixel.com/2024/02/15/openais-sora-turns-short-text-prompts-into-photo-realistic-video). Opened Oct 29, 2026. | Vendor claim relayed by the outlet; PetaPixel did not test it. Shown here because the same vendor listed appearances as a weakness. |
| In one of OpenAI's samples, after the hoop explodes, "a new basketball appears out of nowhere from the sky and passes through the hoop's ring like a ghost." The article also notes "animals or people spontaneously appearing." | [designboom, Feb 16, 2024](https://designboom.com/?p=1047872). Opened Oct 29, 2026. | The outlet's description of OpenAI's own weakness samples, not an independent test. |
| Describing the wolf pup sample: "Despite the prompt specifying 'five wolf pups' initially, only three are visible"; then "a new wolf unexpectedly appears," and later the first wolf "disappears from the scene." | [Sun et al., "From Sora What We Can See," arXiv 2405.10674](https://arxiv.org/abs/2405.10674) (May 17, 2024). Abstract and HTML full text opened Oct 29, 2026. | Preprint survey. It describes OpenAI's published sample; it does not measure a rate. |
| A proposed video metric includes "object permanence," which penalizes "'magic' disappearances or appearances of objects," computed with open-source object trackers. | [Rakheja et al., "World Consistency Score," arXiv 2508.00144](https://arxiv.org/abs/2508.00144) (July 31, 2025). Abstract and section 3.1 opened Oct 29, 2026. | Preprint. Used only for the definition and method; the paper outlines a validation plan, and no results are used here. |
| MemoBench builds 360 clips in which an object "disappears from view, and must be correctly recovered in its updated state upon reappearance"; testing eight models "reveals key insights and open challenges." | [MemoBench, arXiv 2606.27537](https://arxiv.org/abs/2606.27537) (June 25, 2026). Abstract opened Oct 29, 2026. | Abstract only; no per-model scores are used. |

**Incident:** Coca-Cola's November 2025 AI remake of "Holidays Are Coming," made with AI studio Silverside. Campaign reported that viewers found "visual inconsistencies linked to the appearance of the trucks": in some shots "an extra row of wheels in the middle," in others "three wheels are clustered in the front or back of the vehicle where only two had previously appeared." "Coca-Cola declined to comment on the creative inconsistencies." [Campaign US, Shannon Miller, Nov 5, 2025](https://campaignlive.com/article/coca-cola-reignites-ai-ad-debate-new-holiday-campaign/1938664), opened Oct 29, 2026. Caveat: viewer observations relayed by Campaign, not counted by it; the wheels change between shots more than within one. Complaints about wheels in the 2024 ad were seen only in a search summary and are not used. A 2026 benchmark called WROP was seen only in a search summary and is not used.

## 5. The fix
**The principle:** Every frame of a clip makes the same claims about what is in the scene. Check the frames against each other, not just each one against reality.

**Do this: teams and assistants that make AI video**
1. **Write a continuity list before generating.** Name every person, product and prop that must stay the same, with its count and key features ("2 cups, logo facing out, 1 tip jar"). Ask the requester to confirm it.
2. **Keep crowded shots short or split them.** When a shot needs many similar people or animals, generate fewer at once, shorten the shot, or composite groups, since OpenAI says spontaneous appearances happen "especially in scenes containing many entities" (cutoff for "many" is the team's choice).
3. **Check every shot frame by frame against the list.** Step through each take, not just play it. For each listed item record: present from start to end, same count, same shape and markings. Also record any person, animal or object that appears without entering from the edge or from behind something.
4. **Check items that leave view and come back.** When a listed item is covered or leaves frame, confirm it returns the same, in the same place unless the action moved it.
5. **Check that changes stick.** If the action changes an object (a bite, a pour, a door opened), confirm it stays changed for the rest of the shot.
6. **Fix, or drop, then stop.** Trim the shot before the defect, regenerate it up to the team's retry limit, or composite a real or locked object. Never post a take with a known defect because "nobody will notice."
7. **Use a tracker as a pre-screen only.** An object tracker can flag tracks that start or end mid-shot (the method WCS describes). A named person still does the final frame-by-frame check and signs off before publish.
8. **Log it.** Continuity list, takes checked, defects found with timecodes, fix used, reviewer and date.

**Reference design: continuity check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Continuity list | Written and confirmed before generation | 2 lattes, barista, customer, tip jar, logo |
| Per-item record | Present, same count and shape, start to end | Tip jar: 0:00-0:08 |
| Unlisted arrivals | None, or each enters from edge or cover | None |
| Out-of-view items | Return unchanged | Tip jar after arm passes: present |
| State changes | Stay changed | Lid off at 0:04 stays off |
| Sign-off | Named, dated | L. Ortega, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every result: say which takes passed and name each defect with its timecode before anything else |
| Ask one clarifying question | Before generating, to confirm the continuity list: "Anything else that must stay the same?" |
| Offer choices: 2-4 options plus "Something else", free text open | The retry limit is reached: trim before the defect, composite the object, use live footage, something else. Not when a take already passed. |
| Hand off to a person | Always for the final frame-by-frame sign-off before publish |

**Don't over-correct.** Do not flag objects that enter from the edge of the frame or from behind something, or leave the same way. Do not flag changes the action calls for (the customer picks up a cup, the barista adds ice). Do not require a continuity list for abstract or texture-only clips with no objects to track, or for drafts never published. Do not reject a shot for background crowd changes the request never listed, unless a person or object pops in or out in plain view. Do not regenerate without limit; each video run costs time and money (see [AI video regenerations cost more than budgeted](../../ai-image-generation-business-risks/failures/ai-video-regenerations-cost-more-than-budgeted.md)).

**Hand-off rule.** If a viewer, client or reviewer reports an object appearing, vanishing or changing in a published clip, send it to the approver and content owner the same day with the timecode and the log. They decide whether to pull or replace it; [AI ad mistakes that go viral](../../ai-image-generation-business-risks/failures/ai-image-mistakes-in-ads-go-viral.md) covers the public response.

**Framework used:** none yet. Rule 2 follows OpenAI's weakness statement; rules 4 and 5 follow OpenAI's cookie example and MemoBench's disappear-and-reappear setup; rule 7 follows the WCS tracker method; rules 1, 3, 6 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-video-objects-appear-vanish-or-change-between-frames.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Barista slides two lattes | List written and confirmed first | 1 |
| 2 | Third cup appears at 0:05 | Caught with timecode; take not offered | 3 |
| 3 | Tip jar gone after an arm passes | Caught as an out-of-view failure | 4 |
| 4 | Lid comes off, then is back on | Caught as a state change that did not stick | 5 |
| 5 | Tracker passes, no person checked | Publish blocked | 7 |
| 6 | Customer picks up a cup and walks out of frame | Not flagged | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked-or-escaped continuity rate** (primary) | 0 (proposed) | Monthly: published AI video shots whose log has no frame-by-frame check, plus shots with a continuity defect reported after publish / all published AI video shots | Any |
| Defects caught before publish per 100 takes | Track, no target | Continuity log: defects recorded with timecodes / takes checked | Falling to 0 while escapes rise (check is being skipped) |
| Takes per approved shot | Track, no target | Generation log | Rising for 2 months |
| False continuity flags (counter-metric) | Track, no target | Sample of flags where the object entered or left from the edge or cover, or the action changed it | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| AI clip published with no continuity list or per-shot check in the log | Generation log plus publish log | Clip marked abstract or texture-only, with no objects to track |
| Tracker shows an object track that starts or ends mid-shot away from the frame edge and with nothing covering it | Automated pre-screen | The storyboard has the object placed or removed by a hand |
| Count of a listed item differs between the first and last frame of a shot | Per-shot check record | The action adds or removes the item on purpose |
| Viewer comments with a timecode plus words like "where did," "disappears" or "extra" | Social comments on the post | A joke about the content, not a defect |

**Starter rule:** no AI video shot is published unless its log shows a confirmed continuity list, a frame-by-frame check of that shot with no open defects, and a named person's sign-off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-video-objects-appear-vanish-or-change-between-frames
runs: [pre_generation, post_generation, pre_publish]
reads: [request.text, continuity_list, continuity_list.confirmed, shot.takes, shot.frame_check, shot.defects_with_timecode, tracker.flags, shot.fix_method, review.signoff]
trigger: no confirmed continuity list, or shot without frame check, or open defect, or retry limit reached, or no sign-off at publish
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Trim the shot before the defect", "Composite the object", "Use live footage for this shot", "Something else"]
on_miss: block_publish
metric: unchecked-or-escaped continuity rate
counter_metric: false continuity flags
status: proposed
```

## 8. Related patterns
- [Consistency Failure: Identity Loss Across Generations](../../generation-artifacts/failures/consistency-failure.md) - the closest older page. It covers a character's look changing across separate generations; this page covers any object, including props and products, appearing, vanishing or changing inside one clip, checked frame by frame.
- [AI product looks different in every shot](../../ai-image-brand-guidelines/failures/ai-campaign-product-looks-different-across-images.md) - the brand's own product changing across a campaign's images and shots, checked against a product spec; it also uses the Coca-Cola trucks. This page is the frame-level check that catches the same defect inside a shot. Overlap noted for a person.
- [AI image generator wrong number of objects](../../ai-image-prompt-adherence/failures/ai-image-generator-wrong-number-of-objects.md) - a still image with the wrong count from the start; here the count is right at first and changes mid-clip.
- [Artifact accumulation](../../generation-artifacts/failures/artifact-accumulation.md) and [quality drift](../../generation-artifacts/failures/quality-drift.md) - quality that degrades over regenerations or long sequences; this page is about objects, not overall image quality.
- [AI images published with no approval step](../../ai-image-generation-business-risks/failures/ai-images-published-with-no-approval-step.md) - the missing sign-off that lets a defective clip ship.

## 9. Common questions
### Why do objects disappear or appear out of nowhere in AI video?
The model does not keep a list of what is in the scene. OpenAI said in 2024 that people or animals "can spontaneously appear, especially in scenes containing many entities," and objects that leave view are hard to bring back the same.

### How do I check an AI video for continuity mistakes?
Write down every item that must stay the same, then step through each shot frame by frame, not just at full speed. Note any item that appears, vanishes or changes without entering, leaving or being moved.

### What went wrong with the Coca-Cola AI trucks?
Viewers of the November 2025 ad pointed out trucks with an extra row of wheels in some shots and three wheels clustered where two had been, according to Campaign. Coca-Cola declined to comment on the inconsistencies.

### Can software catch objects vanishing in AI video?
It can help. Object trackers can flag tracks that start or end mid-shot, the method behind the proposed World Consistency Score, but a person should still check frame by frame before publishing.

### Do newer AI video models still have this problem?
A 2026 benchmark, MemoBench, tested eight models on objects that leave view and return and reported open challenges. Check every shot no matter which model made it.
