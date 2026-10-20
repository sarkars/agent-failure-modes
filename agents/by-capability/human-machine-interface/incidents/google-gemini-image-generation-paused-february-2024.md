---
title: "Google Pauses Gemini's Image Generation of People After Inaccurate Historical Images"
date: 2024-02-23
source: "https://blog.google/products/gemini/gemini-image-generation-issue/"
summary: "In February 2024, users shared Gemini images of historical scenes that showed people Google and the press described as inaccurate. On Feb 22 Google paused image generation of people. On Feb 23, Google's Prabhakar Raghavan posted that tuning for a range of people and a model that grew too cautious caused the errors. Google's causes are its own account and were not independently checked."
categories:
  - Image generation
patterns:
  - over-refusal-of-ordinary-requests
  - tone-changes-shipped-with-no-regression-test
---

**This page is a dated teardown of one public image-generation incident, for teams that tune an AI product to avoid one kind of bad output and then ship it.** Every fact below comes from a source we opened (listed at the end). The cause is Google's own account; we found no independent test of it. The topic touches race and representation, so we describe it as Google and the press do and add no view of our own.

## What happened (as reported)

- **About three weeks before Feb 23, 2024.** Google's post says it launched image generation of people in the Gemini app, built on its Imagen 2 model. Reuters (Feb 23) says Google began offering image generation through Gemini earlier that month, and that Bard had been renamed Gemini earlier in February.
- **Feb 21, 2024 (Wednesday).** The AP (Feb 22) says Google said it was aware of inaccuracies in some historical image depictions and was working to improve them, and that Gemini's ability to generate a wide range of people was generally good but "missing the mark." Reuters quotes Google saying it was aware Gemini was offering inaccuracies in some historical image generation depictions.
- **What users showed.** The AP says users posted screenshots of historically white-dominated scenes that showed racially diverse characters, and that critics asked whether Google was overcorrecting for racial bias. The AP piece gives no specific prompts. Engadget (Feb 28) lists described outputs: Founding Fathers and Nazis shown as people of color, people of color as Vikings, and Native American Catholic Popes. TechCrunch (Aug 28) mentions racially diverse Roman soldiers. We did not see the original screenshots.
- **Feb 22, 2024 (Thursday).** Per the AP, Google posted on X that it was pausing image generation of people while it worked on an improved version. Reuters quotes Jack Krawczyk, Gemini's senior director of product, saying historical contexts have more nuance and Google would tune further.
- **Feb 23, 2024.** Google published "Gemini image generation got it wrong. We'll do better," by Prabhakar Raghavan, a senior vice president. It says the feature "missed the mark" and that some images were inaccurate or offensive.
- **Feb 27-28, 2024.** Engadget reports, citing an internal memo Semafor published, that CEO Sundar Pichai called the problems "unacceptable," said the team was working "around the clock," and that image generation stayed paused. We did not open the memo.
- **Aug 28, 2024.** TechCrunch (Kyle Wiggers) reports the people feature was returning as an early-access, English-only test for Gemini Advanced, Business and Enterprise users, with Imagen 3. It says Demis Hassabis had promised a fix within about two weeks and it took much longer.

## What Google said

From Google's post (our paraphrase):

- **Cause 1.** Tuning meant to show a range of people did not account for prompts where a range was clearly inappropriate, such as people from a specific historical context.
- **Cause 2.** Over time the model became more cautious than intended and refused some harmless prompts, treating them as sensitive.
- **Effect.** Together these led the model to overcompensate in some cases and be over-conservative in others.
- **Action.** Google turned off image generation of people and said it would improve it significantly, with extensive testing, before turning it back on. It said it does not want Gemini to refuse to depict any group or to produce inaccurate historical images, and that it cannot promise no more errors.

For the August return, TechCrunch reports Google said Imagen 3 has mitigations meant to make generated people more diverse, training on AI-written captions, filtered data and extensive red-teaming including outside experts. Google gave no dataset detail.

## Where the sources disagree or are silent

| Topic | What the sources say |
|---|---|
| Refusals | Engadget lists "refusals to generate images of white people" and links it to the model being overly cautious. Google's own post says only that the model refused some harmless prompts and does not name a group. The AP quotes a University of Washington researcher, Sourojit Ghosh, saying social media claims that Gemini refuses to generate white people contradicted his research, which largely found the opposite. We cannot settle this; we saw no systematic test. |
| Dates | The AP dates Google's X post to Feb 22; the blog post is dated Feb 23. These are two posts, not a conflict. |
| Examples | Different outlets list different examples. None reproduces prompts and outputs in full. |

## What the sources do not say

- How many images were wrong, or how many people used the feature. The Google post, AP and Engadget pages give no usage or error figures.
- What testing happened before launch, or why it missed these prompts.
- How the diversity tuning was built, or how the refusal behavior arose.
- Whether the August version fixed the problems. We opened no independent test.
- How much of the public reaction rested on real outputs versus altered screenshots. No opened source addresses it.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- [Over-refusal of ordinary requests](../goals/refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md) (`over-refusal-of-ordinary-requests`). Partial fit. Google says the model refused harmless prompts because it treated them as sensitive, which is the pattern's core. The pattern is about text assistants declining requests; the larger public problem here was wrong images, which it does not cover.
- [Tone changes shipped with no regression test](../goals/measurement-and-feedback/failures/tone-changes-shipped-with-no-regression-test.md) (`tone-changes-shipped-with-no-regression-test`). Weak, partial fit, on the fix side only. Google says a tuning change did not account for some prompt types and that it would add extensive testing. That is a behavior change, not a tone change, and no source says what regression tests existed.

No existing pattern covers "a correction for one bias applied where it does not belong." We do not force a match.

## Where in the flow it broke

Based on Google's account, and only as far as it goes:

1. **Tuning.** A rule meant to widen the range of people applied to prompts with a clear historical context.
2. **Caution.** The model grew more conservative over time and refused some harmless prompts.
3. **Pre-launch testing.** The sources do not say what was tested. Google promised extensive testing before return.
4. **Response.** Users posted examples, Google acknowledged them, paused the feature a day later, and explained a day after that.

The reported cost is public criticism, a CEO memo and a months-long pause of one feature. Reuters also notes an earlier Bard error that was followed by a share drop of up to 9%; no opened source ties the Gemini episode to a share price.

## What to measure

Our proposals, not Google's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Context-fit rate | Reviewer-rated images for prompts with a stated time or place, divided by all such prompts, counting images that match the stated context |
| Range rate on open prompts | For prompts with no context ("a doctor"), the spread of people shown across a fixed batch, as rated by reviewers |
| Refusal rate on harmless prompts | Refusals on a scripted set of ordinary people prompts, divided by prompts, split by group named in the prompt |
| Report rate | "Inaccurate or offensive" clicks per 1,000 images |

## What a team can change

Our proposals, not Google's. Status: Not yet run.

1. **Test rules by prompt type before shipping.** A fixed set of historical, open and group-specific prompts. Check: every tuning change reruns the set and the result is stored with the release.
2. **Make the range rule conditional.** If a prompt names a time, place or person, the range rule is off. Check: scripted historical prompts return images consistent with the stated context.
3. **Compare refusals across groups.** The same ordinary prompt with different groups named gets the same answer. Check: refusal counts match across the set.
4. **Say what is paused and why.** Show a plain notice when a feature is off, with a date to check back. Check: the notice names the feature.
5. **Give a one-tap report on every image** that stores the prompt and image. Check: the tap writes a record.
6. **Don't over-correct.** Removing the range rule everywhere would bring back the problem it was added for. Run rule 2 with the open-prompt set and require that it still shows a spread.

## Sources

| URL | Publisher | Date | Status |
|---|---|---|---|
| https://blog.google/products/gemini/gemini-image-generation-issue/ | Google (Prabhakar Raghavan) | 2024-02-23 | Opened 2026-10-20 (fetch tool returned a summary of the page) |
| https://www.clickorlando.com/business/2024/02/22/google-suspends-gemini-chatbots-ability-to-generate-pictures-of-people/ | Associated Press, via WKMG News 6 | 2024-02-22 | Opened 2026-10-20 (summary) |
| https://interaksyon.philstar.com/trends-spotlights/2024/02/23/270973/google-pause-gemini-ai-model-image-generation-people-inaccuracies/ | Reuters (Akash Sriram), via Interaksyon | 2024-02-23 | Opened 2026-10-20 (summary) |
| https://www.engadget.com/google-ceo-says-gemini-image-generation-failures-were-unacceptable-163748934.html | Engadget (Lawrence Bonk) | 2024-02-28 | Opened 2026-10-20 (summary) |
| https://techcrunch.com/2024/08/28/google-says-its-fixed-geminis-people-generating-feature/ | TechCrunch (Kyle Wiggers) | 2024-08-28 | Opened 2026-10-20 (summary) |

Not opened / unverified, and not used above: Semafor's text of the Pichai memo (known only through Engadget); Demis Hassabis's Mobile World Congress remarks (search summaries only; the "about two weeks" wording comes from TechCrunch); Google's X post (known only through the AP); Gulf News, Investopedia, Quartz, Fox stations and other outlets seen only in search summaries; and the original user screenshots. A Reuters reprint was read, not the Reuters site. Page summaries came from our fetch tool, so quotes are limited to words each article attributes to Google or others.

## Corrections

If you have the original screenshots, Google's X post, the Pichai memo, or a better date, tell us and we will fix this page.
