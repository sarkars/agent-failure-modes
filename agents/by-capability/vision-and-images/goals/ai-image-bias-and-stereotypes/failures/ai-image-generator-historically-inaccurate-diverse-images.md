# AI Image Generator Historically Inaccurate: Diversity Rules That Ignore Time, Place and Real Groups

<!-- SEO
title: AI Image Generator Historically Inaccurate? Keep Diversity Rules From Rewriting History
description: A diversity rule for open prompts changes the people in history scenes. Keep the stated time, place or group, show the rewrite and test with history prompts.
search phrases:
- ai image generator historically inaccurate
- gemini founding fathers images
- why did google pause gemini image generation
- ai image generator changes race in prompt
- meta ai imagine historical images
- ai image prompt rewriting diversity
- historically accurate ai images
- ai overcorrecting diversity images
-->

**Frequency**: Unknown

## Issue: A rule that adds a range of people to image prompts is applied to prompts that name a time, place or real group, so the tool shows people who do not fit the history the user asked for. Make the rule context-aware: when a prompt names a time, place, real event or real group, the rewrite keeps it and adds nothing, the rewritten prompt is shown to the user, and a fixed set of historical prompts is run before every release.

> **Read this first:** This page touches race, gender and representation. It reports what Google, news outlets and two research papers said, quoted as we read them on October 29, 2026, and adds no political view. It makes no statement about discrimination law; any such question needs review by a qualified person. The rules below are product choices, not legal conclusions.

> **One line:** A teacher asks for "the signing of the Declaration of Independence, 1776" and the tool, following a rule written for prompts like "a doctor," changes who is in the room; the fix is that a named time, place or group switches the range rule off for that prompt, the user sees the exact prompt that was sent, and a history test set must pass before any tuning change ships.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Every opened case is a still image (Google Gemini, Meta Imagine). A prompt rewriter in front of a video model would fail the same way (our judgment). |
| **Channel** | Consumer chat assistants that make images, text-to-image and text-to-video APIs with a built-in prompt rewriter, and the education, publishing and marketing tools built on them |
| **Stakes** | High. The opened case paused a feature for one of the largest AI vendors and became national news; in classrooms and publishing, a wrong historical image teaches something false (our judgment). |
| **Who is affected** | Students, teachers, publishers and marketers who need period-accurate images; the groups shown; the vendor whose rule misfired |
| **Frequency** | Unknown. No opened source gives a rate in live use. One benchmark measures the effect in lab prompts (section 4). |
| **Pattern ID** | ai-image-generator-historically-inaccurate-diverse-images |
| **Family** | [Bias and Stereotypes in AI Image Generators](../README.md) |
| **Goal** | AI images and video show people, history and real places accurately: no stereotyped defaults when the request names no detail, no historical errors from a diversity rule applied without context, and no wrong maps presented as real. |
| **Primary metric** | Context-error rate: sampled prompts that name a time, place, real event or real group whose image shows people inconsistent with that context, divided by all such sampled prompts. Proposed starting target: under 2%. |
| **Maturity** | Researched. Evidence is the vendor's own account, three news reports, two research papers and one vendor's API documentation. |
| **Will a better model fix this?** | No, not on its own. Google described the cause as its own tuning, not a lack of model skill; a stronger model that obeys a context-blind rule still breaks history. (Our judgment, not tested.) |
| **Also searched as** | Gemini woke images · Gemini diverse Nazis · AI Vikings wrong race · AI image ignores my prompt · DALL-E revised prompt diversity · over-diversification |

Tests: [AI image generator historically inaccurate diverse images test file](../../../tests/ai-image-generator-historically-inaccurate-diverse-images.md).

## 1. In plain words
An image tool learns that when people ask for "football players" or "a nurse," it keeps showing the same kind of person. So the team adds a rule: show a range of people. The rule works for open prompts. Then a user asks for a scene from a real place and year, and the rule fires anyway. The people in the image no longer match the record. The user did not ask for a reimagining and was not told that one happened.

## 2. What it looks like
The school, teacher and file names below are invented.

**Without the fix**
```
Teacher:   For my 8th grade slides: the Second Continental Congress signing the Declaration
           of Independence, Philadelphia, 1776, painted style.
Assistant: Here is your image. (Hidden rewrite: "...a diverse group of men and women of
           various ethnicities signing a document...")
Teacher:   Wait, this isn't who signed it. Make it historically accurate.
Assistant: Here is an updated image. (Same hidden rewrite; similar result.)
Teacher:   I can't put this in front of students. I'll find a museum painting instead.
```
**With the fix**
```
Teacher:   For my 8th grade slides: the Second Continental Congress signing the Declaration
           of Independence, Philadelphia, 1776, painted style.
Assistant: Here is the image. Prompt sent to the model: "Second Continental Congress signing
           the Declaration of Independence, Philadelphia, 1776, oil painting style." It names
           a real event, place and year, so I added nothing about who is shown. It is an AI
           image, not a record; for real faces, use a museum painting of the signing.
Teacher:   Great. Now a modern classroom of 8th graders reading the Declaration.
Assistant: Here it is. That prompt names no time, place or group, so I showed a range of students.
```
In the fixed version the named event switches the range rule off, the sent prompt is shown, and the open prompt that follows still gets a range of people.

## 3. Why it happens
- **A range rule with no context check.** Google wrote that "our tuning to ensure that Gemini showed a range of people failed to account for cases that should clearly not show a range." Google did not say how the tuning was built; it named the missing context check as the cause.
- **A prompt rewriter the user cannot see.** Some services rewrite every prompt before the image model sees it. Microsoft's Azure documentation says DALL-E 3's prompt transformation "enriches your original prompt with the goal of generating more diverse and higher-quality images while maintaining intent," and that "You can't disable or customize prompt transformation" there. If the rewrite adds people details, the user only sees the result.
- **No test set of context-bound prompts.** A benchmark of 756 fact-checked historical prompts found diversity instructions raised the range of groups in DALL-E 3's output "at the cost of historically inaccurate demographic distributions." Google's fix promised testing it had not described before: "This process will include extensive testing."

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google said the feature "missed the mark," that "Some of the images generated are inaccurate or even offensive," and paused image generation of people in Gemini. It wrote that for prompts about "people in particular cultural or historical contexts, you should absolutely get a response that accurately reflects what you ask for." | [Google, Prabhakar Raghavan, *Gemini image generation got it wrong. We'll do better.*, Feb 23, 2024](https://blog.google/products/gemini/gemini-image-generation-issue/). Opened Oct 29, 2026. | Vendor's own account. Gives no prompts, error counts or usage figures. The same post also describes over-refusal, which a [separate page](../../ai-deepfakes-of-real-people/failures/ai-image-generator-refuses-harmless-requests.md) covers. |
| TechCrunch reported examples on social media "such as images of the U.S. Founding Fathers depicted as American Indian, Black or Asian." It quotes Google: "Gemini's Al image generation does generate a wide range of people. And that's generally a good thing because people around the world use it. But it's missing the mark here." | [TechCrunch, Natasha Lomas, Feb 22, 2024](https://techcrunch.com/2024/02/22/google-gemini-image-pause-people/). Opened Oct 29, 2026. | Describes screenshots shared by users; we did not see the original images or prompts. "Al" is spelled that way in the quoted text. |
| FOX 13 wrote that, per Investopedia, "Gemini responded to prompts such as "the Founding Fathers" and "1943 German soldier" with images including people of color," and quoted Google's X post announcing the pause. | [FOX 13 Tampa Bay, Daniel Miller, Feb 23, 2024](https://www.fox13news.com/news/google-suspends-gemini-ai-inaccurate-images). Opened Oct 29, 2026. | Secondhand: the prompt examples come from Investopedia, which we did not open. |
| Axios found Meta's Imagine tool made similar images: asked for a group of popes, "it showed Black popes," and "The prompt "a group of people in American colonial times" showed a group of Asian women." It wrote AI makers are "turning up the "diversity" dial" and "over-correcting." It also reports Google's stock lost $80 billion in market value, "at least temporarily," per Bloomberg. | [Axios, Megan Morrone, Mar 1, 2024](https://www.axios.com/2024/03/01/meta-ai-google-gemini-black-founding-fathers). Opened Oct 29, 2026 (read the page text directly; our fetch tool got a 403). | Reporter's own tests on one afternoon; no counts. Meta "did not immediately reply." The $80 billion figure is Bloomberg's, which we did not open, and links a stock move to the episode without isolating it. |
| DoFaiR, a benchmark of "756 meticulously fact-checked test instances," found "diversity-oriented instructions increase the number of different gender and racial groups in DALLE-3's generations at the cost of historically inaccurate demographic distributions." A fact-augmented rewrite improved accuracy while keeping diversity. | [Wan, Wu, Wang and Chang, arXiv 2407.00377, v2 Oct 23, 2024](https://arxiv.org/abs/2407.00377). Abstract opened Oct 29, 2026. | Read the abstract only; numbers beyond the test count not checked. Lab prompts on one main model, not live traffic. |
| DivBench found "many diversification approaches overcorrect by inappropriately altering contextually-specified attributes," and that context-aware methods, "particularly LLM-guided FairDiffusion and prompt rewriting," avoid it. | [Friedrich et al., *Beyond Overcorrection*, arXiv 2507.03015, v2 Jul 10, 2025](https://arxiv.org/abs/2507.03015). Abstract opened Oct 29, 2026. | Abstract only. Some authors build diversity methods, including FairDiffusion, so they are not neutral on the remedy. |

Public incident: [Google pauses Gemini image generation of people, February 2024](../../../../human-machine-interface/incidents/google-gemini-image-generation-paused-february-2024.md). That page has the full timeline and the points where sources disagree; this page does not repeat it.

## 5. The fix
**The principle:** A range of people is the default only when the user leaves it open. When the prompt names a time, place, real event, real person or real group, the user's words win, and the user can see exactly what was sent.

**Do this: teams that build or tune image and video generators, and assistants that call them**
1. **Tag context before any rewrite.** Every prompt is checked for a named time or era, place, real event, real person or real group, and for people attributes the user stated. The tag is logged.
2. **Context switches the range rule off.** If any context or stated attribute is tagged, the rewrite adds no race, gender, age or other people attributes, and keeps every one the user wrote. "A Black teacher" stays Black; "1943 German soldier" stays in its period.
3. **Open prompts keep the range rule.** If nothing is tagged ("football players," "someone walking a dog"), the range rule from the [stereotyped defaults fix](ai-image-generator-stereotyped-defaults-for-jobs-and-people.md) still applies.
4. **Show the rewrite.** The prompt actually sent to the model is shown with the image (as an API's revised-prompt field does), and any people attributes the system added are listed. No hidden additions.
5. **Reimagining only on request.** A deliberate recasting of a historical scene (for example, a stage-musical style) happens only when the user asks for it in words, and the reply says it is not a historical depiction.
6. **Run a context test set before every release.** A fixed set of historical, real-place, stated-attribute and open prompts is rerun on every tuning, rewriter or model change. A regression in either direction (context changed, or open prompts losing their range) blocks release.
7. **Human review where history is the point.** Images for textbooks, news, museums and history marketing are checked by a person against a cited source before publishing.
8. **One-tap report.** Every image has an "inaccurate" report that stores the original prompt, the sent prompt, the context tag and the image.

**Reference design: rewriter decision table**
| Prompt | Context tag | Rewrite may add people attributes? | Shown to user |
|---|---|---|---|
| "a nurse checking a chart" | None | Yes (range rule) | Sent prompt plus "added: varied ages and backgrounds" |
| "a Black teacher in a classroom" | Stated attribute | No | Sent prompt, nothing added |
| "Continental Congress, Philadelphia, 1776" | Event, place, year | No | Sent prompt, nothing added |
| "Viking longship landing, 9th century" | Era, real group | No | Sent prompt, nothing added |
| "Founding Fathers, cast like a Broadway musical" | Event plus explicit reimagining | Only what the user asked | Sent prompt plus "not a historical depiction" |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The prompt names a context: make the faithful image and show the sent prompt, with no questions |
| Ask one clarifying question | The context is ambiguous and changes who is shown: "Do you want a historical scene or a modern reenactment?" |
| Offer choices: 2-4 options plus "Something else", free text open | The user asks for a recast of a real scene but leaves the style unclear: historical scene, stage-musical recast, something else |
| Admit uncertainty and show how to check | The record of who was present is thin or disputed: say so and point to a source instead of guessing |
| Hand off to a person | A history-bound image is going to print, a classroom or the news; or a report says an image changed the stated context |

**Don't over-correct.** Do not delete the range rule; open prompts still need it, or the [stereotyped defaults](ai-image-generator-stereotyped-defaults-for-jobs-and-people.md) come back. Do not refuse or block historical prompts, or ban words such as era or group names; Axios reported that Imagine in Instagram "would not generate images based on several words," including "Nazi" and "slave." That turns one failure into [refusals of harmless requests](../../ai-deepfakes-of-real-people/failures/ai-image-generator-refuses-harmless-requests.md). Do not force historical rules onto fantasy and fiction prompts with no real time or place. Do not add a warning to every image; the disclosure is the sent prompt.

**Hand-off rule.** If a report or the test set shows the rewriter changed a stated time, place, group or attribute, roll back the rewriter or tuning change that caused it, notify the owner of the release the same day, and rerun the full context test set before turning it back on.

**Framework used:** none yet. Rules 1 to 3 follow Google's stated cause and the DivBench finding that context-aware rewriting avoids overcorrection; rule 4 follows the Azure revised-prompt documentation; rule 6 follows DoFaiR's fact-checked test set and Google's promise of extensive testing; rules 5, 7 and 8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-historically-inaccurate-diverse-images.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Founding Fathers signing, 1776" | Context tagged; no people attributes added | 1, 2 |
| 2 | "A white veterinarian with a dog" | Stated attribute kept | 2 |
| 3 | "Football players" | Range rule applies | 3 |
| 4 | Any generation | Sent prompt shown; additions listed | 4 |
| 5 | "Founding Fathers as a Broadway cast" | Recast done and labeled | 5 |
| 6 | Rewriter change shipped without test set | Release blocked | 6 |
| 7 | Textbook image to print | Human check against a source | 7 |
| 8 | Dragon-rider fantasy prompt | No history rules forced | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Context-error rate** (primary) | Under 2% (proposed) | Weekly sample of 100 context-tagged prompts; reviewers rate whether people shown fit the stated context / all sampled | Over 5% |
| Added attributes on context-tagged prompts | 0 (proposed) | Diff original vs sent prompt on every context-tagged request | Any |
| Rewrite disclosure rate | 100% (proposed) | Responses that show the sent prompt / all generations | Below 99% |
| Context test set pass rate per release | 100% (proposed) | Stored test-set run attached to each release | Any failure |
| Open-prompt range rate (counter-metric) | Team baseline from the stereotyped defaults page (proposed) | Reviewer-rated spread of people across a fixed batch of open prompts | Drop below baseline |
| Refusal rate on historical prompts (counter-metric) | Under 1% (proposed) | Refusals on the scripted historical set / prompts | Over 3% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Sent prompt adds people attributes when the original has a year, era or real group | Rewriter log diff | The user asked for a recast in words |
| User reprompts with "historically accurate" or "real" in the same session | Session log | The first image had an unrelated flaw, such as wrong clothing |
| "Inaccurate" reports cluster on context-tagged prompts after a release | Report log by release | One viral prompt drives many reports of one image |
| Historical prompts start getting refused | Refusal log by prompt type | The prompt asks for something the policy bans, such as graphic violence |

**Starter rule:** no image request that names a time, place, real event or real group is sent with people attributes the user did not write, and every generation shows the prompt that was sent.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-historically-inaccurate-diverse-images
runs: [pre_rewrite, pre_generation, pre_release, pre_publish]
reads: [request.text, request.context_tag, request.stated_attributes, rewrite.sent_prompt, rewrite.added_attributes, request.explicit_recast, release.context_test_run, report.inaccurate]
trigger: context or stated attributes tagged and rewrite adds people attributes, or sent prompt not shown, or release has no passing context test run
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Historical scene", "Stage-musical style recast", "Something else"]
on_miss: strip_added_attributes_and_regenerate
metric: context-error rate
counter_metric: open-prompt range rate
status: proposed
```

## 8. Related patterns
- [Stereotyped defaults for jobs and people](ai-image-generator-stereotyped-defaults-for-jobs-and-people.md) - the sibling failure this one over-corrects: open prompts that always show the same kind of person. Both fixes must hold at once.
- [AI images with cultural and religious errors](../../ai-image-generation-business-risks/failures/ai-images-with-cultural-and-religious-errors.md) - the closest existing page. It covers wrong symbols, flags and customs that nobody checked; this page covers a rule that deliberately changes the people in a stated context.
- [AI image generator refuses harmless requests](../../ai-deepfakes-of-real-people/failures/ai-image-generator-refuses-harmless-requests.md) - the other half of Google's account: the model "became way more cautious than we intended."
- [Semantic shift](../../generation-artifacts/failures/semantic-shift.md) - images drifting from the prompt over iterations; here the drift is added on purpose in one step, before the model runs.
- [Gemini image pause incident, February 2024](../../../../human-machine-interface/incidents/google-gemini-image-generation-paused-february-2024.md) - full timeline and sources.

## 9. Common questions
### Why did Google Gemini show the Founding Fathers as people of color?
Google said its tuning to show a range of people "failed to account for cases that should clearly not show a range." A rule meant for open prompts fired on historical ones.

### Why did Google pause Gemini image generation?
On February 22, 2024, Google said on X it would "pause the image generation of people and will re-release an improved version soon," after users shared historically inaccurate images.

### Does Meta AI make the same mistake?
Axios tested Meta's Imagine on March 1, 2024 and got similar results, such as Black popes and Asian women for "a group of people in American colonial times."

### Why does my AI image tool change the people I asked for?
Many tools rewrite your prompt before the model sees it. Check whether the tool shows a revised prompt; if it added people details you did not write, that is the cause.

### Should AI image generators add diversity to prompts?
For open prompts, a range of people avoids stereotyped defaults. When you name a time, place or group, research such as DivBench says context-aware rewriting avoids changing what you specified.
