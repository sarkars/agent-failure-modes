# AI Image Model Update Changed My Style: When the Vendor's New Version Breaks the Approved Look

<!-- SEO
title: Midjourney Update Changed My Style? Keep an Approved AI Image Look Across Model Versions
description: An image vendor ships a new default model or retires the old one, and the campaign's approved look changes with no prompt edit. Pin the version and re-test.
search phrases:
- midjourney update changed my style
- new midjourney version looks different same prompt
- how to keep midjourney on an older version
- sref code looks different in new version
- dall-e 3 shut down what happens to my images
- gpt-image-1 shut down replacement looks different
- keep ai image style consistent across model updates
- ai image brand style changed after update
-->

**Frequency**: Unknown

## Issue: A team approves an AI image look, and weeks later the vendor makes a new model the default or shuts the old one down, so the same prompt and style codes give a different look with no warning inside the workflow. Record the exact model version with every approved asset, pin it on every job, and re-run a saved reference set against any new version before it is used for that campaign.

> **One line:** A coffee chain approves a warm, film-grain fall look in Midjourney, the vendor switches its default to a version it describes as "more creative, bold, sophisticated, and edgy," and the November social posts come out glossier than the September ones; the fix is that each approved style records its model version and style settings, every job sends that version explicitly, and a new version is used only after a person compares it against the approved reference set.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Both opened vendor pages are about image models. We opened no source on video model updates. |
| **Channel** | Hosted image generators used for brand work (web apps, Discord bots, APIs) and the internal tools and agents that call them |
| **Stakes** | Medium. A campaign's images stop matching each other, and work stops when a retired model can no longer be called (our judgment; no opened source reports a business case). |
| **Who is affected** | Brand and design teams, agencies holding a client's approved look, and developers whose apps call a named image model |
| **Frequency** | Unknown. No opened source gives a rate. Midjourney's default changed three times between June 2025 and July 2026 (section 4). |
| **Pattern ID** | ai-image-model-update-changes-approved-style |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unpinned job rate: generation jobs for a campaign with an approved style that ran without the approved model version set explicitly, divided by all sampled jobs for such campaigns. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is vendor documentation and one user forum thread; no business incident was found. |
| **Will a better model fix this?** | No. A new model is the cause. Better models will keep shipping, and each one may look different. Pinning, records and re-tests are workflow steps. (Our judgment, not tested.) |
| **Also searched as** | Midjourney V8 looks different · default version changed · style reference broke after update · DALL-E 3 retired · keep AI style consistent |

Tests: [AI image model update changes approved style test file](../../../tests/ai-image-model-update-changes-approved-style.md).

## 1. In plain words
A designer finds a look the brand team loves: warm light, soft film grain, muted orange. The team signs off on six images in September. In November she types the same prompt with the same style code to make six more. The vendor has a new default model by then. The new images are sharper and more saturated. Nobody changed anything on purpose, so nobody thinks to check the version. The old and new posts sit side by side on the brand's feed.

## 2. What it looks like
The company, people and IDs below are invented. The version names and dates are from Midjourney's Version page (section 4).

**Without the fix**
```
Designer:  Make 6 more fall posts. Same prompt and style code as the September set.
Assistant: Done. 6 images generated.
Designer:  These look shinier than September. Did I change something?
Assistant: Your prompt and style code match the September jobs.
Designer:  OK, they're close enough. Sending to social.
           (Two weeks later, the brand manager compares the feed)
Manager:   Why do the November posts look like a different brand?
```
**With the fix**
```
Designer:  Make 6 more fall posts. Same prompt and style code as the September set.
Assistant: The approved style FALL-26 was made on V7. Your account default is now V8.2.
           I can't tell you how close V8.2 will look until we test it. Choose one:
           1) Generate on V7, as approved  2) Run the 4 reference prompts on V8.2 for review
           3) Something else
Designer:  1.
Assistant: 6 images generated with --v 7 and style FALL-26. Each record lists model V7.
```
In the fixed version the version is read from the approved style record, the change in default is caught before generation, and moving to the new version goes through a review.

## 3. Why it happens
- **The default model changes under the team.** Midjourney says a default set in settings "will apply to all your future prompts," and the vendor moves its own default from version to version. A prompt with no version named runs on whatever is current.
- **The vendor says new versions look different.** Midjourney's page says each version "might handle prompts differently, have unique artistic styles." Style settings can be tied to versions too: a June 2025 blog post says the same style code gives "completely different aesthetics" under different style versions.
- **Old models are retired.** OpenAI's deprecations page says that at shutdown "the model or endpoint will no longer be accessible." Midjourney says its V8.0 alpha "is no longer available for use." A pinned version only works while it exists, so the team needs a re-test before the date, not after.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "Each version might handle prompts differently, have unique artistic styles, or offer improved image quality." The current default is V8.2, released as default on July 24, 2026; its images are "more creative, bold, sophisticated, and edgy." V8.1 was the default from June 10 to July 23, 2026; V7 from June 17, 2025 to June 9, 2026; V6.1 until June 16, 2025. | [Midjourney, Version](https://docs.midjourney.com/docs/models) (redirects to the help center Version article). Read October 29, 2026; WebFetch returned 403, so we read the page with a direct download. Quotes string-matched. | Vendor's own description. It shows defaults change often; it does not show any business harmed. |
| Users set a version with `--v` at the end of a prompt or choose a default in settings, which "will apply to all your future prompts." V8.0 "is no longer available for use." V8.2 adds an Edit Model that "replaces Omni Reference, Character Reference, and the Retexture tool." | Same Midjourney page. | Tools a style depends on can change between versions, not only the look. |
| Niji 7 "is more literal, so broad or 'vibey' prompts may not behave the same as before." | Same Midjourney page. | About Midjourney's anime-focused model only. |
| "When we announce that a model or endpoint is being deprecated, it immediately becomes deprecated." DALL-E 2 and DALL-E 3 users were notified November 14, 2025 of removal from the API on May 12, 2026. `gpt-image-1` was shut down on October 23, 2026. `gpt-image-1-mini`, `gpt-image-1.5` and `chatgpt-image-latest` are set for removal on December 1, 2026. | [OpenAI API, Deprecations](https://platform.openai.com/docs/deprecations) (redirects to developers.openai.com). Read October 29, 2026; quotes and dates string-matched. | Retirement dates only. The page does not say how the replacements' images differ. |
| Legacy style codes "need --sv 4 to work properly," "--sv 6 is now the default for V7," and new codes under `--sv 4` "generate completely different aesthetics." | [Geeky Curiosity, Midjourney style references in V7, June 17, 2025](https://geekycuriosity.substack.com/p/midjourney-complete-overview-of-the). Opened and read. | Independent blog, not Midjourney. Describes 2025 behavior and may be out of date. |
| A user wrote of a `gpt-image-1` edit workflow, "It was working great before but it's not working the same now." Others in the thread reported lower quality; no OpenAI reply appears. | [OpenAI Developer Community, May 9, 2025](https://community.openai.com/t/gpt-image-1-nerfed-for-anyone-else/1255916). Opened and read. | Anecdotal and unconfirmed; it does not show a version change caused it. |

**No public incident found.** We searched "Midjourney V7 default model change style different from V6 prompts," "brand consistency AI image generator model update changed look campaign," "gpt-image-1 shutdown images look different migration complaint developer community" and "Midjourney new version default changed my style sref codes don't work anymore personalization reset." Results were vendor docs, how-to guides and blogs; none reported a named business whose approved look changed after an update.

## 5. The fix
**The principle:** An approved style is a model version plus settings, not just a prompt. It changes only when a person approves the change.

**Do this: brand teams, agencies and tool builders**
1. **Record the version with the approval.** Every approved style record holds the model name and exact version (for example `--v 7` or a dated API snapshot), the style codes and their style version, and key parameters. A record with no version cannot be approved.
2. **Send the version on every job.** Every job for a campaign with an approved style sets the version explicitly. Never rely on the account or API default.
3. **Check the default before each batch.** If the account default differs from the approved version, say so before generating and offer choices (approved version, test the new one, something else).
4. **Keep a reference set.** Each approved style keeps 4 to 8 reference prompts with their approved outputs, version and settings, stored outside the vendor's gallery.
5. **Re-test before switching.** A new version is used for a campaign only after the reference set is re-run on it and a named person compares the results side by side and approves.
6. **Watch retirement dates.** Track each vendor's deprecation or version pages for every model in use. When a retirement is announced, schedule the re-test at once, well before the shutdown date.
7. **Don't use moving aliases for approved work.** Names that point to "the latest" model (such as `chatgpt-image-latest`) are not allowed in approved style records.
8. **Log the version on every output.** Each generated asset's record stores the model and version that made it, so a mismatch in a set can be found.

**Reference design: approved style record**
```yaml
style_id: FALL-26
vendor: midjourney
model_version: "7"              # sent as --v 7 on every job
style_codes: [{code: "1234567", style_version: "6"}]
parameters: {stylize: 250, raw: false}
reference_set: [ref-01, ref-02, ref-03, ref-04]   # prompts + approved outputs, stored in the DAM
approved_by: L. Chen
approved_on: 2026-09-08
retirement_watch: {source: vendor_version_page, last_checked: 2026-10-27}
next_version_test: {version: "8.2", status: not_started}
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The account default differs from the approved version: approved version, test the new one, something else. Not when the job already names the approved version; just run it. |
| Admit uncertainty and show how to check | Asked "will V8.2 look the same?": say it is unknown and offer the reference-set test |
| Ask one clarifying question | A campaign has no approved style record: "Which approved style should these match?" |
| Hand off to a person | The reference-set results differ, or the approved version has a shutdown date |

**Don't over-correct.** A new version is not banned; new campaigns can start on it. Exploration and drafts with no approved style do not need pinning. Do not block a batch because two images from the same version differ a little; that is the [same-prompt variation](../../generation-artifacts/failures/consistency-failure.md) problem, not a version change. Do not re-test on every minor vendor news post; re-test when the version you use changes or is retired.

**Hand-off rule.** When reference-set results on a new version differ from the approved outputs, or a model in use gets a shutdown date, the style owner gets the side-by-side images, the version names and the date. Only that person can move the style to a new version, and the record is updated with the new approval.

**Framework used:** none yet. Rules 1, 2 and 6 follow Midjourney's version settings and OpenAI's deprecation terms; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-model-update-changes-approved-style.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Approve a style with no version recorded | Blocked | 1 |
| 2 | Job for an approved style, default differs | Version sent explicitly; change flagged with choices | 2, 3 |
| 3 | Switch a campaign to a new version without a re-test | Blocked until reference set is approved | 5 |
| 4 | Vendor announces retirement of the version in use | Re-test scheduled, owner told | 6 |
| 5 | Style record uses a "latest" alias | Rejected | 7 |
| 6 | Draft exploration on the new default, no approved style | Runs | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unpinned job rate** (primary) | 0 (proposed) | Weekly sample of jobs for campaigns with an approved style: no explicit version / all sampled | Any |
| Approved styles with no version recorded | 0 (proposed) | Query of the style records | Any |
| Published sets mixing model versions | 0 without a recorded approval (proposed) | Asset records grouped by campaign and version | Any |
| Models in use with a shutdown date and no re-test scheduled | 0 (proposed) | Style records joined to the retirement watch list | Any |
| Batches stopped for a version check that matched the approved version (counter-metric) | Under 5% of stops (proposed) | Assistant log review, monthly | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A job for an approved style has no version parameter | Generation job log | A draft job not tied to the approved style |
| The account or API default changed since the style was approved | Vendor version page vs. style record date | The team already approved the new version |
| Assets in one campaign carry different model versions | Asset records grouped by campaign | An approved switch partway through, on record |
| A reviewer writes "looks different" or "off-brand" on a regenerated set | Review comments | A changed prompt or brief, not a version |
| A model in a style record appears on a deprecation page | Retirement watch | The re-test is already done |

**Starter rule:** no job for an approved style runs unless it names the approved model version, and no new version is used for that style until a person approves the reference-set comparison.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-model-update-changes-approved-style
runs: [pre_generation, scheduled]
reads: [style.model_version, job.version_param, account.default_version, vendor.deprecations, asset.model_version]
trigger: job lacks the approved version, default differs, mixed versions in a set, or a version in use is retired
moves: [offer_choices, admit_uncertainty, ask_clarifying_question, hand_off]
choices: ["Generate on the approved version", "Run the reference set on the new version for review", "Something else"]
on_miss: block_job_or_flag_owner
metric: unpinned job rate
counter_metric: batches stopped that already matched the approved version
status: proposed
```

## 8. Related patterns
- [Consistency failure: identity loss across generations](../../generation-artifacts/failures/consistency-failure.md) - the closest existing page. It covers the same model giving different results from sample to sample. Here the model itself changes. Pinning a seed does not help when the version under it is gone. Merge proposal for a person to review.
- [Quality drift in generated images](../../generation-artifacts/failures/quality-drift.md) - covers quality dropping across repeated generation steps inside one model. This page is about a vendor release changing the look between jobs. Merge proposal for a person to review.
- [Approved AI image cannot be reproduced](./approved-ai-image-cannot-be-reproduced.md) - the sibling page. It covers the same prompt giving a different image on the same model. This page covers the model itself changing or being retired.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - a platform tool changes an approved image after approval. Here the vendor's model changes before the next batch.
- [AI image vendor indemnity gaps](../../ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md) - another case where a vendor's terms and products decide what the business can rely on.

## 9. Common questions
### Why does my Midjourney image look different with the same prompt?
If the whole look shifted, check for a new default version; Midjourney says each version may "have unique artistic styles." Add `--v` with the number your original job used. If only details vary on the same version, see [approved AI image cannot be reproduced](./approved-ai-image-cannot-be-reproduced.md).

### How do I keep Midjourney on an older version?
Add `--v` and the version number to the end of the prompt, or set a default version in the settings panel. Retired versions, such as the V8.0 alpha, cannot be used.

### Do my style reference codes still work in a new version?
Not always the same way. A June 2025 blog post says one code can give very different looks under different style versions. Re-run your reference prompts before trusting it.

### What happens to my DALL-E 3 workflow?
OpenAI's page lists DALL-E 2 and DALL-E 3 for removal from the API on May 12, 2026, with GPT Image models as replacements. Re-test your approved prompts on the replacement and get sign-off.

### Should we stop upgrading to new models?
No. Pin approved campaigns, and move each one only after a person compares the reference set on the new version.
