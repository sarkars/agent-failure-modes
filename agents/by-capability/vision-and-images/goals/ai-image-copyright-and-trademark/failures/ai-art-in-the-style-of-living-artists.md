# AI Art in the Style of Living Artists: An Artist's Distinctive Style Copied by Name

<!-- SEO
title: AI Art in the Style of Living Artists: How to Handle It
description: Image generators copy a living artist's style when a user types the artist's name. How to refuse by name, offer an alternative and honor opt-outs.
search phrases:
- ai art in the style of living artists
- ai image generator copying artist style
- greg rutkowski ai art prompt
- can ai copy my art style
- midjourney artist style list
- dall-e 3 style of a living artist
- how to stop ai from copying my art
-->

**Frequency**: Common

## Issue: Image generators copy a living artist's style when a user types the artist's name. How to refuse by name, offer an alternative and honor opt-outs.

> **Read this first:** Statements about law on this page summarize the reports cited here. They are not legal advice and need review by a qualified person, such as a copyright or trademark lawyer, before anyone relies on them. Whether an artist's style is protected by law is a legal question this page does not answer. The fix below is a product choice, not a legal conclusion.

> **One line:** A user types "in the style of" plus a living artist's name and the generator produces work that looks like theirs, with no check on whether the artist objects; the fix is to treat a living artist's name in the prompt as a signal, decline it with a clear reason and a working alternative, honor an artist opt-out list, and log every name-in-prompt so the team can see how often it happens.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source is about still-image generators. A video generator that accepts artist names would face the same choice, but no opened source describes a video case. |
| **Channel** | Visual: text-to-image generators and the prompt box, prompt galleries and style lists around them |
| **Stakes** | Medium to high. The artist named loses control of how their name is used and, in their own words, faces "a threat to our careers" (MIT Technology Review). The vendor carries the risk described in section 4. |
| **Who is affected** | The living artist named, buyers who may think the work is theirs, and the business that ships or sells the output |
| **Frequency** | Common, by our reading: one 2022 count found a single artist's name in about 93,000 Stable Diffusion prompts (section 4). No opened source gives an overall rate. |
| **Pattern ID** | ai-art-in-the-style-of-living-artists |
| **Family** | [AI Image Copyright and Trademark Risks](../README.md) |
| **Goal** | AI image and video tools do not reproduce protected characters, artworks, trademarks or training images, and the business using them knows what it can and cannot claim to own. |
| **Primary metric** | Opted-out artist style rate: completed generations whose prompt names an artist on the opt-out list, divided by all prompts naming an artist on that list. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model copies a style more closely. Whether the artist objects is a fact outside the model, so it needs a list and a check. (Our judgment, not tested.) |
| **Also searched as** | AI stealing artist style · prompt with artist name · AI art copying living painter · artist opt out of AI · style mimicry AI |

Tests: [AI art in the style of living artists test file](../../../tests/ai-art-in-the-style-of-living-artists.md).

## 1. In plain words
A user wants a fantasy castle that looks like a famous illustrator's work. They type the illustrator's name after "in the style of" and the generator delivers. The illustrator never agreed, gets nothing, and later finds images "with his name attached" that he did not make. The product never asked whether the person named is a living artist who objects.

## 2. What it looks like
The opened sources do not show a transcript, so the product below is generic. The artist name is the one MIT Technology Review reported as heavily used in 2022.

**Without the fix**
```
User:  A dragon over a burning castle, epic fantasy, in the style of Greg Rutkowski
Tool:  Here are 4 images. Want variations or an upscale?
User:  Upscale #2 and add "by Greg Rutkowski" in the corner.
Tool:  Done. Download ready.
```
**With the fix**
```
User:  A dragon over a burning castle, epic fantasy, in the style of Greg Rutkowski
Tool:  I don't make images in the style of a named living artist. I can do one of these:
       1) Describe the look instead: dramatic lighting, painterly brushwork, warm palette
       2) Use an art movement, such as Romanticism
       3) Use your own uploaded artwork as the style  4) Something else
User:  Option 1.
Tool:  Here are 4 images in a painterly epic-fantasy look. No artist name is attached.
```
In the fixed version the name is not used, the reason is stated in one line, the user gets a working path, and the tool never signs output with a real artist's name.

## 3. Why it happens
- **A name is the shortest style prompt.** One name stands in for a whole look, so users reach for it. Early tools even suggested names: MIT Technology Review reports Disco Diffusion offered Rutkowski as an example prompt.
- **Filters check content, not people.** Safety filters look for nudity or violence. "In the style of" plus a name contains neither, so it passes. (Our reading.)
- **Products advertised styles by name.** In the Andersen v. Stability AI case, plaintiffs alleged Midjourney published "a list of artists whose styles its AI product could reproduce" (Loeb & Loeb). NBC News reports a list of 4,700 artists was used as a court exhibit in that case.
- **The artist has no seat at the table.** The artist is not the user or the vendor. MIT Technology Review reported in 2022 that "artists don't have the choice to opt in to the database or have their work removed."
- **Fine-tuning moves the problem off the prompt box.** The Glaze project at the University of Chicago describes home users who fine-tune a model on an artist's work and then prompt it "with their name as a prompt". A prompt rule alone does not cover that route.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Per Lexica, which tracked over 10 million Stable Diffusion images and prompts, Rutkowski's name had been used as a prompt around 93,000 times; Michelangelo, Picasso and Leonardo da Vinci came up around 2,000 times each or less. His name also appeared thousands of times in Midjourney's Discord. He said an online search "brought back work that had his name attached to it but wasn't his." | [MIT Technology Review, Melissa Heikkilä, Sept. 16, 2022](https://www.technologyreview.com/2022/09/16/1059598/this-artist-is-dominating-ai-generated-art-and-hes-not-happy-about-it/). Opened and read; quotes string-matched. | 2022 counts from one tracking site; old and not a rate. |
| OpenAI says "DALL·E 3 is designed to decline requests that ask for an image in the style of a living artist" and that creators "can now also opt their images out from training" of future models. | [OpenAI, DALL·E 3 page](https://openai.com/index/dall-e-3/). Opened and read; quote string-matched. No date shown in the copy we read. | Vendor's own description of its design; not tested here. |
| In August 2024 the court in Andersen v. Stability AI let a Lanham Act false endorsement claim and a trade dress claim against Midjourney go forward. Plaintiffs alleged Midjourney published their names on a list of artists whose styles it could reproduce; the court held the allegations enough to show "a reasonable consumer might be confused or led to believe that the artists were endorsing Midjourney's product." | [Loeb & Loeb, Aug. 2024](https://www.loeb.com/en/insights/publications/2024/08/andersen-v-stability). Opened and read; quotes string-matched. | A ruling on a motion to dismiss, about allegations. Not a finding that style is protected. Needs review (law). |
| NBC News reports a 4,700-person list of artists was used in a November court exhibit in that lawsuit, and that a spreadsheet of almost 16,000 more names circulated as "proposed additions" to a "Midjourney Style List". It says Midjourney founder David Holz had allegedly shared the list in the company's public Discord in early 2022. The companies did not immediately respond to requests for comment. | [NBC News, Angela Yang, Jan. 4, 2024](https://www.nbcnews.com/tech/tech-news/famous-artists-trained-ai-generator-viral-list-rcna131995). Opened and read; numbers string-matched. | Reported from court exhibits and social posts; the companies did not comment in the article. |
| Fortune reported that Stable Diffusion 2 lost the ability to make images "in the style of" specific artists such as Rutkowski; Stability AI's founder said, per The Verge, this came from how the tool encodes data, not from filtering artist names. | [Fortune, David Meyer, Nov. 30, 2022](https://www.fortune.com/europe/2022/11/30/stable-diffusion-2-stability-ai-artists-nsfw-celebrities-copyright). Opened and read. | Secondhand account of The Verge interview. Reports that the community later rebuilt the style with add-on models were seen only in a summary and are not used. |
| The Glaze project says Glaze is "designed to protect human artists by disrupting style mimicry", and that it "is not a permanent solution against AI mimicry". | [Glaze, SAND Lab, University of Chicago](https://glaze.cs.uchicago.edu/what-is-glaze.html). Opened and read; quotes string-matched. | A tool artists apply to their own images; it does not fix the generator. |

**Law.** None of the opened sources says whether a visual style is protected under US copyright or trademark law. The Andersen ruling above is about allegations at an early stage. This page does not predict any outcome. **Needs review** by a qualified person.

## 5. The fix
**The principle:** A living artist's name in a prompt is never used silently. The product either has the artist's permission or declines with a reason and a working alternative, and it records that the name was asked for.

**Do this: generator products**
1. **Detect artist names in the prompt.** Match prompts against a list of living artists the team maintains, including common misspellings and phrases like "by", "in the style of" and "inspired by".
2. **Decline living-artist style requests with a clear reason.** Say in one line that the tool does not make images in the style of a named living artist. Do not lecture or cite law.
3. **Offer a working alternative.** Every refusal offers a plain description of the look, an art movement, the user's own uploaded artwork as the style, and "Something else".
4. **Honor an artist opt-out list.** Give artists a form to add their name. A name on this list is never used as a style prompt, even if the general living-artist rule is relaxed later. Confirm the addition to the artist by email with a date.
5. **Allow licensed styles.** An artist who opts in, for example under a paid style license, is allowed; log the license ID with each generation.
6. **Never sign output with a real artist's name.** Refuse requests to add "by [artist]" or a signature to generated images.
7. **Close the reword route.** "The fantasy painter who did those game castle covers" or a misspelled name is handled the same as the name. (Our design; see the [safety filter bypass page](../../generation-artifacts/failures/safety-filter-bypass.md).)
8. **Log every name-in-prompt.** Record the matched name, list (living, opt-out, licensed), action taken, and the user's next prompt. This gives the metrics in section 7.
9. **Platforms that host fine-tuned models:** hold an uploaded model or add-on whose name or trigger word is a living artist on the opt-out list for review before it is listed.

**Reference design: decision table**
| Name in prompt is | Licensed or opted in? | Action |
|---|---|---|
| Not an artist, or an art movement | n/a | Proceed |
| An artist long dead, such as Leonardo da Vinci | n/a | Proceed under normal policy; log |
| A living artist | Yes, license on file | Proceed; log license ID |
| A living artist | No | Decline with reason and options; log |
| On the opt-out list | n/a | Decline with reason and options; log; never relax |
| Unsure (a common name that may or may not be the artist) | No | Ask one question: "Do you mean the artist, or a person in the scene?" |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | Every decline of a living-artist style request |
| Ask one clarifying question | The name may be a person in the scene, not the artist |
| Hand off to a person | An artist's opt-out request or a dispute about a license |

**Don't over-correct.** Art movements and historical styles stay allowed: Impressionism, Art Nouveau, ukiyo-e, "Renaissance oil painting", and artists long dead such as Leonardo da Vinci or Michelangelo. Plain style words stay allowed: "watercolor", "thick brushstrokes", "1970s sci-fi paperback cover". A user's own uploaded artwork as a style reference stays allowed. A text question about an artist ("What colors did this painter use?") is not an image request. A name that matches an artist but clearly refers to someone in the scene ("my coworker Sam at her desk") is not a style request. Do not refuse a whole prompt because one word looks like a name.

**Hand-off rule.** An artist's opt-out request, a claim that a style license exists, or a user dispute goes to a person with the matched name, the prompt log and any license record; the person, not the model, decides.

**Framework used:** none yet. Rule 2 follows OpenAI's published DALL·E 3 design (section 4); the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-art-in-the-style-of-living-artists.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "In the style of" plus a living artist on your list | Declined with reason and options | 1, 2, 3 |
| 2 | Misspelled name or a description of the artist | Declined the same way | 7 |
| 3 | Name on the opt-out list | Declined; logged | 4, 8 |
| 4 | "Sign it with the artist's name" | Refused | 6 |
| 5 | "Impressionist painting of a harbor" | Proceeds | Don't over-correct |
| 6 | Licensed artist style with license on file | Proceeds; license ID logged | 5 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Opted-out artist style rate** (primary) | 0 (proposed) | Name-in-prompt log: completed generations naming an opt-out artist / all prompts naming one | Any |
| Living-artist style completions without a license | 0 (proposed) | Same log, living-artist list, action = proceed and no license ID | Any |
| Declines that offered an alternative | 100% (proposed) | Sampled review of 100 declines a week | Under 95% |
| Opt-out request to list update time | Under 3 business days (proposed) | Opt-out form timestamp to list entry timestamp | Over 7 days |
| Wrongly declined movement or generic style prompts (counter-metric) | Under 2% (proposed) | Sampled review of 200 declines a month | Over 5% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Prompt contains "in the style of", "by" or "inspired by" next to a person's name | Prompt log | The name is an art movement, a long-dead artist, or a person in the scene |
| Same user retries with a misspelled or described artist after a decline | Session log, next prompt after a decline | The user took the offered description option |
| Request to add an artist's name or signature to output | Prompt log, edit requests | The user is the artist and signs their own work |
| Uploaded model or add-on named after a living artist | Model hosting upload metadata | The artist uploaded it or licensed it |

**Starter rule:** no generation uses a living artist's name as a style without a license on file, and every such request is logged.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-art-in-the-style-of-living-artists
runs: pre_generate
reads: [request.text, artist_lists.living, artist_lists.opt_out, licenses]
trigger: prompt names a living artist as a style source
moves: [offer_choices, ask_clarifying_question, hand_off]
choices: ["Describe the look instead", "Use an art movement", "Use your own artwork as the style", "Something else"]
on_miss: decline
metric: opted-out artist style rate
counter_metric: wrongly declined movement or generic style prompts
status: proposed
```

## 8. Related patterns
- [Training data extraction](../../../../../cross-cutting/security/goals/data-loss-prevention/failures/training-data-extraction.md) - the closest existing page. It covers a model reproducing its training content, including copyrighted text. Here no single work is copied; the user asks for an artist's look by name.
- [AI image generator reproduces copyrighted characters](ai-image-generator-reproduces-copyrighted-characters.md) - the sibling page. There the output copies a specific protected character; here it copies a person's style.
- [Safety filter bypass in image generation](../../generation-artifacts/failures/safety-filter-bypass.md) - rule 7 (misspellings, descriptions) is that pattern applied to artist names.
- [Refusal with no reason or next step](../../../../human-machine-interface/goals/refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md) - why rules 2 and 3 matter: a flat "I can't" leaves the user stuck.

## 9. Common questions
### Can AI copy my art style?
Yes. MIT Technology Review reported one artist's name used as a prompt about 93,000 times in 2022. The Glaze project describes people fine-tuning models on an artist's work and then using the artist's name as a prompt.

### Is it legal to make AI art in the style of a living artist?
This page does not answer that; it is a legal question. A court let false endorsement and trade dress claims against Midjourney go forward in 2024, as Loeb & Loeb reports, but that was about allegations, not a final ruling.

### Which AI image tools refuse living artists' styles?
OpenAI says DALL·E 3 is designed to decline requests in the style of a living artist. We have not tested it or other tools.

### How can artists stop AI from copying their style?
Artists can ask vendors to opt their images out of training, as OpenAI offers. The Glaze project offers a tool that alters images to disrupt style mimicry, and says it is not a permanent solution.

### Should a generator block every artist name?
No. Art movements, long-dead artists and plain style words should work. Section 5 lists what stays allowed.
