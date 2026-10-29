# AI Image Generator Ignores Negative Prompts: Ask for "No Glasses," Get Glasses

<!-- SEO
title: AI Image Generator Ignores Negative Prompts: Why "No" Fails
description: Ask an AI image tool for a man without glasses and it often draws glasses. Rewrite exclusions, use the no-field, and check each image before it ships.
search phrases:
- ai image generator ignores negative prompt
- ai image generator adds what i said not to
- chatgpt draw a room without an elephant
- dall-e ignores no in prompt
- midjourney --no parameter not working
- how to remove something from ai image prompt
- stable diffusion negative prompt vs without
-->

**Frequency**: Common

## Issue: Ask an AI image tool for "a man without glasses" or "a room with no elephants" and it often draws the very thing you ruled out, and a team that does not look for it ships an ad or listing that shows what the brief said to leave out. Mark every exclusion in the request, keep the unwanted word out of the main prompt, use the tool's exclusion control where it has one, and check each image for each excluded item before anyone uses it.

> **One line:** A Columbus contact lens retailer asks for "a man without glasses reading a menu" for an ad about going glasses-free and gets a man in glasses; the fix is to rewrite the request as what should be there ("bare face, clear view of his eyes"), put "glasses" in the exclusion field instead, check the result for glasses and record the check, and edit or rebuild the image when retries keep missing.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. All opened studies measure still images. A video prompt that says "no" can fail the same way, but no opened source measures it in AI video. |
| **Channel** | Text-to-image tools, chat assistants that draw images, and design tools with built-in generators, used for ads, listings, menus and social posts |
| **Stakes** | Medium. An excluded item that shows up can contradict the ad's own message (glasses in a contact lens ad) or show a product, animal or object the business said must not appear (our judgment). |
| **Who is affected** | Customers who see the image, the brand whose message it contradicts, and the team that published it |
| **Frequency** | Common in tests: Stable Diffusion drew glasses for "a man without glasses" at a 0.819 detection score over 1,000 images, and two Stable Diffusion models got about 30% of negation-prompt images right in a model-graded test (section 4). No opened source gives a rate in real business use. |
| **Pattern ID** | ai-image-generator-ignores-negative-prompts |
| **Family** | [AI Images That Ignore the Prompt](../README.md) |
| **Goal** | AI images and video show what the prompt asked for: the right number of objects, in the right places, with the right attributes and readable text. |
| **Primary metric** | Unchecked-or-failed exclusion publish rate: published AI images made from a request with an exclusion ("no," "without," "don't add"), where no absence check was recorded or the excluded item is visible, divided by all such published images. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is four arXiv papers (one ICLR 2024, one accepted to ICCV 2025, two preprints), two vendor help pages and two user reports. |
| **Will a better model fix this?** | Partly. Swapping in a text encoder trained on negation raised SDXL's score from 0.308 to 0.421, still under half, and a chat-based image tool still drew elephants for "no elephants" in a March 2025 user report (our judgment, drawing on the cited sources). |
| **Also searched as** | AI image without something · AI keeps adding what I said no to · negative prompt not working · ChatGPT image elephant in the room · Midjourney exclude object |

Tests: [AI image generator ignores negative prompts test file](../../../tests/ai-image-generator-ignores-negative-prompts.md).

## 1. In plain words
A contact lens shop wants an ad with the line "See clearly, no glasses needed." The marketer asks an image tool for "a man without glasses reading a menu." The man in the picture wears glasses. The ad says one thing; the photo says the opposite. The word "glasses" in the prompt pulled glasses into the image, and nobody looked for them before it ran.

## 2. What it looks like
The store, people and campaign below are invented.

**Without the fix**
```
Marketer:  Ad image for our "Ditch the Frames" campaign: a man without glasses
           reading a menu at a diner counter.
Assistant: Here is your image. (One generation; the man wears black-rimmed glasses.)
Marketer:  Great, sending it to the ad team.
Ad manager (next day): Our contact lens ad shows a guy in glasses. It ran in
           the Columbus market overnight.
```
**With the fix**
```
Marketer:  Ad image for our "Ditch the Frames" campaign: a man without glasses
           reading a menu at a diner counter.
Assistant: Your request excludes one item: glasses. I wrote the prompt as what should
           be there ("bare face, clear view of his eyes") and put "glasses" in the
           exclusion field. I checked each result for glasses: try 1 had them, try 2 did not.
           Here is try 2. Checked: no glasses, no sunglasses, nothing pushed up on his head.
           Sent to Priya Shah (brand) to confirm and approve before it runs.
```
The fixed version names the exclusion, keeps the unwanted word out of the main prompt, uses the exclusion control, checks every result, says what it found and ends with a person approving.

## 3. Why it happens
- **Naming the item pulls it in.** The text encoder most image tools rely on handles "no" poorly. Park et al. found only about 0.704% of captions in a large image-text dataset contain negation words, so "a man not wearing a hat" can come out with a hat. SpaceVLM's authors write that CLIP's "limited handling of negation often causes generated images to exhibit objects explicitly excluded in the prompt."
- **The scene already expects it.** Li et al. found that even the prompt "a man" often produces glasses, partly because many training images of men show glasses without labeling them. Saying "without glasses" does not undo that pull.
- **Adding "without X" can make it worse.** In a 2026 FLUX-dev test, appending "without {target}" removed the target less often than the plain prompt (3.88% vs 14.38%), and in some cases it drew the target when the plain prompt had not.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| For "a man without glasses," Stable Diffusion and DeepFloyd-IF still drew glasses. Over 1,000 images, a glasses detector gave SD a DetScore of 0.819, versus 0.122 for "a face without glasses." The authors say it also happens in Ideogram and Midjourney. | [Li et al., "Get What You Want, Not What You Don't," ICLR 2024, arXiv 2402.05375](https://arxiv.org/abs/2402.05375) (Feb 8, 2024). Abstract and HTML full text opened Oct 29, 2026. | DetScore is a detector score, not a share of images. Older open models. The Ideogram and Midjourney claim rests on a figure, not a measured rate. |
| Only about 0.704% of LAION-400M captions contain negation, and negation words are 0.083% of all words. On 107 negation prompts (5 seeds each), an image-reading model scored an image 1 only if the subject was present and the negated item absent: SD-1.4 averaged 0.295 and SDXL-1.0 0.308. A negation-trained text encoder raised them to 0.449 and 0.421; SDXL's general prompt score fell from 0.849 to 0.802. | [Park et al., "Know 'No' Better," arXiv 2501.10913](https://arxiv.org/abs/2501.10913) (v1 Jan 19, 2025; accepted to ICCV 2025 per arXiv). Abstract and HTML full text opened Oct 29, 2026. | Prompts written by ChatGPT and graded by a model (mPLUG), not people. Two older Stable Diffusion models only. |
| On FLUX-dev, the plain prompt removed the unwanted item in 14.38% of cases; adding "without {suppression target}" dropped that to 3.88%. The authors write that prompt-level negation "may even lead to the generation of the suppression target." | [Ko et al., "Orthogonal Negative Guidance," arXiv 2605.29390](https://arxiv.org/abs/2605.29390) (May 28, 2026). HTML full text opened Oct 29, 2026. | Preprint. The authors' own benchmark and method (which scored 86.88%), so the comparison favors their approach. |
| CLIP text encoders are "widely used in modern T2I models," and their limited handling of negation lets excluded objects appear. | [SpaceVLM, arXiv 2511.12331](https://arxiv.org/abs/2511.12331) (Nov 15, 2025). HTML full text opened Oct 29, 2026. | Preprint mainly about image search; used here only for this cause. |
| Midjourney's docs list "still life gouache painting without any fruit" and "please don't add fruit!" as bad prompts and "--no fruit, apple, pear" as the good one. They warn the system reads each word after `--no` on its own, so "--no modern clothing" reads as "no modern" and "no clothing." | [Midjourney docs, "No"](https://docs.midjourney.com/docs/no). Opened Oct 29, 2026 through a text reader, since the site blocks direct download. | Vendor page, undated. It does not say negation fails; it steers users to `--no`. |
| Recraft tells users to write "apples" in the negative prompt, not "no apples," warning that "no" "can confuse the model and lead to the opposite effect." | [Recraft docs, negative prompts](https://www.recraft.ai/docs/recraft-studio/image-generation/working-with-text-and-prompts/negative-prompts). Opened Oct 29, 2026. | Vendor page about its own exclusion field. |
| A user asked ChatGPT for a room with no elephants and got an elephant plush and elephant wall art. Another tried "without a bear rug" and got "a bear and a rug in the pic." On a retry, the image showed elephant sculptures while the text reply said there were none. | [OpenAI Developer Community, March 8-9, 2025](https://community.openai.com/t/why-cant-chatgpt-draw-a-room-without-an-elephant/1138265). Opened Oct 29, 2026. | User reports, not OpenAI staff. A blog post ([Explainable, Jan 25, 2024](https://veryexplainable.substack.com/p/ai-image-tools-and-the-elephant-in)) reports the same with ChatGPT-4; single author. |

**Incident:** No public incident found where a business published an AI image showing something its brief excluded and was called out for it. Searches run: "text-to-image negation 'without' prompt ignored benchmark," "CLIP text encoder does not understand negation study," "AI image generator ignores 'no' in prompt news article elephant," "AI generated image 'no' prompt still included backlash ad 2025 negative prompt failure news." Papers seen only in search summaries (Neg-TtoI, NEGATE, an ASU student project) were not opened and are not used. Runway's old prompting guide, which a search summary said warned against negative prompts, now shows only a retirement notice, so it is not used.

## 5. The fix
**The principle:** An exclusion in a request is a claim about what the image does not show. Describe what should be there, and then look for what should not.

**Do this: teams and assistants that make images from requests with "no" or "without"**
1. **Flag every exclusion.** Before generating, list each item the request rules out ("without glasses," "no elephants," "don't add fruit") as an exclusion to check.
2. **Keep the unwanted word out of the main prompt.** Describe what fills the space instead ("bare face, clear view of his eyes," "empty pine floor"). Do not append "without X"; Ko et al. found that did worse than saying nothing.
3. **Use the tool's exclusion control when it has one.** Put the bare item in the negative prompt or `--no` field ("glasses," not "no glasses"), one item per word where the tool reads words separately, as Midjourney's docs warn.
4. **Check every image for every excluded item before showing it as final.** Record present or absent for each item, including look-alikes (sunglasses for glasses, a plush or painting for an animal). A person does the final check for anything published. A vision model may pre-screen (proposed), but not as the only check, since the opened studies used model graders with no measured accuracy against people.
5. **Never say an item is absent without checking.** The reply describes what the check found, not what the prompt asked for.
6. **Regenerate, then stop.** If the item appears, regenerate and check again, up to a limit the team sets (3 tries is our proposed starting point), and tell the requester what each try showed.
7. **Remove it another way after the limit.** Erase or edit the item out and recheck, crop it out, use a real photo, or change the shot so the item cannot appear.
8. **A named person approves and it is logged.** Log the exclusions, prompt as sent, exclusion-field contents, check result per try, method, checker, approver and date.

**Reference design: exclusion check before sign-off**
| Check | Pass | Example |
|---|---|---|
| Exclusions listed | Each "no" or "without" item recorded | glasses |
| Prompt as sent | Excluded word absent; positive description present | "bare face, clear view of his eyes" |
| Exclusion field | Bare item word | glasses |
| Check per try | Present or absent recorded, look-alikes included | try 1 present, try 2 absent |
| Method | Generated, edited or real photo | Generated, try 2 |
| Approval | Named, dated | P. Shah, Oct 29, 2026 |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every request with an exclusion: name the excluded items and what the check found before anything else |
| Offer choices: 2-4 options plus "Something else", free text open | The retry limit is reached: erase it and recheck, crop, use your photo, change the shot, something else. Do not offer them when the check passes. |
| Ask one clarifying question | It is unclear what the exclusion covers: "Should 'no glasses' also rule out sunglasses on his head?" |
| Hand off to a person | Always for the final check on published ads, listings, menus and social posts |

**Don't over-correct.** Do not flag "no" or "without" that is not about the image's content ("no rush," "without a deadline," "a No Parking sign" when the sign is wanted). Do not refuse or warn on a request just because it has an exclusion; rewrite it and check. Do not drop the exclusion from the record when you remove the word from the prompt. Do not check for items the request never excluded. Do not regenerate without limit.

**Hand-off rule.** If a customer, reviewer or ad platform reports an excluded item in a published image, send it to the approver and content owner the same day with the log. They decide whether to pull or replace it.

**Framework used:** none yet. Rule 2 follows Ko et al. and the vendor guidance; rule 3 follows Midjourney's and Recraft's docs; rule 5 follows the forum report where the reply denied elephants the image showed; rules 1, 4 and 6-8 are our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-generator-ignores-negative-prompts.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "A man without glasses" | Exclusion flagged; prompt as sent has no "glasses" | 1, 2 |
| 2 | Tool has a negative prompt field | Field holds "glasses," not "no glasses" | 3 |
| 3 | Result shows sunglasses on his head | Caught as present | 4 |
| 4 | Reply says "no glasses" before any check | Fails | 5 |
| 5 | Three tries all show glasses | Stops; edit or photo offered | 6, 7 |
| 6 | "Make it with no rush" | Not flagged | Over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked-or-failed exclusion publish rate** (primary) | 0 (proposed) | Monthly sample of published images from requests with exclusions: no recorded absence check, or excluded item visible on review / all sampled | Any |
| Excluded word in prompt as sent | 0 (proposed) | Generation log: exclusion-flagged requests whose prompt as sent contains the excluded noun outside the exclusion field / all flagged | Above 5% |
| Tries per exclusion request | Track, no target | Generation log: tries before a passing check or the switch to editing | Rising for 2 months |
| False exclusion flags (counter-metric) | Track, no target | Sample of flagged requests where the "no" was not about image content | Rising for 2 months |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Request has "no," "without" or "don't add" before a noun, one generation, image published, no absence field | Generation log plus publish log | The "no" was not about image content ("no rush") |
| Prompt as sent contains "without X" or "no X" in the main prompt | Generation log | The tool has no exclusion field and the item was also checked |
| Requester's next turn repeats the exclusion ("I said no elephants") | Chat log | A new exclusion added on purpose |
| Image tags from a vision model include the excluded noun on an approved image | Tagging log plus approval log | A look-alike the requester said is fine |

**Starter rule:** no AI image made from a request with an exclusion is published unless its log shows each excluded item checked as absent and a named person's approval.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-generator-ignores-negative-prompts
runs: [pre_generation, post_generation, pre_publish]
reads: [request.text, request.exclusions, prompt.as_sent, prompt.exclusion_field, image.exclusion_check, generation.tries, image.method, review.signoff]
trigger: exclusion in request with excluded word in main prompt, or no recorded absence check, or excluded item present, or retry limit reached, or no approval at publish
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Erase it and recheck", "Crop it out", "Use our photo", "Change the shot", "Something else"]
on_miss: block_publish
metric: unchecked-or-failed exclusion publish rate
counter_metric: false exclusion flags
status: proposed
```

## 8. Related patterns
- [Semantic drift in generated images](../../generation-artifacts/failures/semantic-shift.md) - the closest older page. It covers an image drifting from the prompt over repeated generations; here the first image already shows the item the prompt ruled out.
- [Token limit artifacts](../../generation-artifacts/failures/token-limit-artifacts.md) - details dropped because a long prompt was cut off; "a man without glasses" fails in five words, well inside the limit.
- [AI image generator wrong number of objects](ai-image-generator-wrong-number-of-objects.md) - the sibling check for counts; both treat a detail of the request as a claim to verify, but a count check counts items while this one looks for items that should be missing.
- [AI image generator puts colors on the wrong object](ai-image-generator-puts-colors-on-the-wrong-object.md) - attributes land on the wrong object; here the attribute or object should not appear at all.
- [AI images in ads published without review](../../ai-image-generation-business-risks/failures/ai-images-in-ads-published-without-review.md) - the missing review that lets an excluded item run in an ad.

## 9. Common questions
### Why does AI add the thing I said not to include?
The text encoder most tools use handles "no" poorly, since negation is rare in the captions it learned from, so naming the item pulls it into the image. Some scenes, like "a man," already lean toward items such as glasses.

### How do I get an AI image without something in it?
Describe what should be there instead, put the bare item in the tool's negative prompt or `--no` field if it has one, and check the result yourself. If it keeps appearing, edit it out or use a real photo.

### Should I write "no glasses" in the negative prompt?
No. Recraft's docs say to write "apples," not "no apples," in the negative field, and Midjourney's docs show `--no fruit, apple, pear`.

### Does adding "without" to the prompt help?
Not reliably. In a 2026 FLUX-dev test, adding "without" plus the item removed it less often than leaving it out of the prompt.

### Will ChatGPT tell me if the item is still there?
Do not count on it. In one March 2025 forum report, the image showed elephant sculptures while the reply said there were none.
