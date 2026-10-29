# AI Image or Video Tool Shut Down Mid-Campaign: When the Vendor Retires the Model or Changes Its Terms

<!-- SEO
title: AI Image Tool Shut Down Mid-Campaign? Plan for Model Retirement
description: A campaign depends on one AI model or app, the vendor retires it or changes terms, and assets cannot be remade. Record the model, keep masters, plan an exit.
search phrases:
- dall-e 3 shut down what now
- dall-e api deprecated may 12 2026
- sora app shutting down what happens to my videos
- how to export sora videos before shutdown
- ai image model retired mid project
- openai model deprecation replacement image
- ai tool terms of service changed commercial use
- backup plan if ai image generator shuts down
-->

**Frequency**: Occasional

## Issue: A campaign is built on one AI image or video model or app, and partway through the vendor retires it or changes its terms, so the team cannot remake, extend or resize its assets, and files left in the vendor's library may be deleted. Record the model, version and terms for every asset, watch the vendor's deprecation notices, keep master files outside the vendor, and write an exit plan before launch.

> **Read this first:** This page quotes vendor pages and news reports as we read them on October 29, 2026. Whether a vendor's terms still let you use assets made before a change, and what a contract with a client says about it, are legal questions. They need review by a qualified person, such as your company's lawyer. The rules below are workflow choices, not legal conclusions.

> **One line:** A retailer's spring campaign uses DALL-E 3 for hero images and the Sora app for short clips; DALL-E 3 leaves the API on May 12, 2026 and the Sora app closes April 26, 2026, so the summer extension cannot be made the same way and unexported clips are at risk; the fix is an asset record that names the model and terms, a watch on deprecation pages, masters stored outside the vendor and a written exit plan.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. DALL-E 2 and DALL-E 3 are image models; Sora is a video app and API. |
| **Channel** | Hosted image and video generators used for campaign work (consumer apps, web apps, APIs) and the internal tools and agents that call them |
| **Stakes** | Medium. Work stops or must be redone on another tool, and files kept only in the vendor's library can be deleted after shutdown (our judgment, based on the Sora help page in section 4). |
| **Who is affected** | Brand and marketing teams, agencies holding a client's campaign, and developers whose apps call a named model |
| **Frequency** | Occasional. Two OpenAI media products were retired in 2026 (section 4). No opened source gives a rate across vendors. |
| **Pattern ID** | ai-image-vendor-retires-model-or-changes-terms-mid-campaign |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Campaigns at risk: live campaigns with an asset made on a model or app that has an announced shutdown date and no tested exit plan, divided by all live campaigns. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is vendor notices, two news reports, one secondary report and one user forum thread; no named business incident was found. |
| **Will a better model fix this?** | No. Retirement and terms are vendor business decisions; a better model is often the reason the old one is retired. (Our judgment, not tested.) |
| **Also searched as** | DALL-E retired · Sora discontinued · export Sora library · AI vendor lock-in · model sunset plan |

Tests: [AI image vendor retires model or changes terms mid-campaign test file](../../../tests/ai-image-vendor-retires-model-or-changes-terms-mid-campaign.md).

## 1. In plain words
A Denver outdoor retailer plans a spring-to-summer campaign. Its in-house tool makes hero images with DALL-E 3 through the API, and the social team makes short clips in the Sora app and leaves them in the Sora library. In May the summer team asks for new sizes and two more clips. The image calls fail because the model is gone, and the Sora app has closed. Nobody wrote down which assets came from which tool, or where the only copies live.

## 2. What it looks like
The company, people and IDs below are invented. The dates are from OpenAI's pages (section 4).

**Without the fix**
```
Designer:  Make 3 more summer hero images like the spring set, same prompt.
Assistant: The image request failed: the model "dall-e-3" is not available.
Designer:  What? Use whatever replaced it.
Assistant: Done. 3 images generated on a newer model.
Designer:  These look nothing like spring. And where are the Sora clips?
Social:    They were in the Sora library. I never downloaded them.
```
**With the fix**
```
Designer:  Make 3 more summer hero images like the spring set, same prompt.
Assistant: The spring set was made on dall-e-3. OpenAI removed it from the API on May 12, 2026,
           so I can't remake it. Our exit plan says: edit from the stored masters, or test a
           replacement model and get sign-off first. Choose one:
           1) Resize the 4 stored spring masters  2) Run the reference prompts on a new model for review
           3) Something else
Designer:  1.
Assistant: Resized from masters in the brand drive. Sora clips: all 12 exported on April 2.
```
In the fixed version the asset record names the model, the shutdown was known before the request, and the masters and clips were already stored outside the vendor.

## 3. Why it happens
- **Shutdown is final.** OpenAI's deprecations page says "At the time of the shut down, the model or endpoint will no longer be accessible." A campaign that plans to remake or extend assets later cannot, on that model.
- **The vendor's library is not an archive.** OpenAI's Sora help page says that after shutdown and any final export window "we will permanently delete any data associated with your use of Sora." Teams that keep clips only in the app lose them.
- **The record does not say which tool made what.** Assets are saved with a campaign name but no model, version or terms date, so nobody can list what a retirement or terms change touches.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| "On November 14th, 2025, we notified developers using DALL·E model snapshots of their deprecation" and "removal from the API on May 12, 2026." The page lists `gpt-image-2`, `gpt-image-1` or `gpt-image-1-mini` as replacements. "When we announce that a model or endpoint is being deprecated, it immediately becomes deprecated." | [OpenAI API, Deprecations](https://platform.openai.com/docs/deprecations) (redirects to developers.openai.com). Opened Oct 29, 2026. | Vendor page; we cite only the DALL-E 2 and DALL-E 3 entry. It gives notice dates, not effects on customers. |
| An April 9, 2026 reminder said OpenAI was "deprecating the following models on May 12, 2026," naming DALL-E 2 and DALL-E 3, and pointed to "gpt-image-1.5 or gpt-image-1- mini." | [OpenAI Developer Community, Deprecation Reminder](https://community.openai.com/t/deprecation-reminder-dall-e-will-be-shut-down-on-may-12-2026/1378754). Opened Oct 29, 2026. | Posted by a forum user (PaulBellow), not on OpenAI's own page. Its replacement names differ from the deprecations page as read today, so the recommended replacement itself moved. |
| A user wrote that gpt-image-1 "cannot do what DALL-E-3 does," and later that "Two of my DALL-E-3 images are now under consideration for Album Art for a known artist." Another wrote, "Many creators relied on this model in their workflows." | [OpenAI Developer Community thread, Nov 22 to Dec 21, 2025](https://community.openai.com/t/openai-is-making-a-huge-mistake-by-deprecating-dall-e-3/1367228). Opened Oct 29, 2026. | Anecdotal user posts; not a business incident and not verified. |
| On March 24, 2026 OpenAI posted "We're saying goodbye to Sora." A spokesperson told Engadget: "We've decided to discontinue Sora in the consumer app and API." No dates were given that day. | [Engadget, Igor Bonifacic, March 24, 2026](https://engadget.com/ai/openai-is-shutting-down-its-sora-video-generation-app-211023358.html). Opened Oct 29, 2026. | News report relaying OpenAI statements. |
| OpenAI said it would share "timelines for the app and API and details on preserving your work." The article says OpenAI gave no reason. | [9to5Google, Ben Schoon, March 24, 2026](https://9to5google.com/2026/03/24/openai-shutting-down-sora-video-generation-app-but-without-explaining-why/). Opened Oct 29, 2026. | News report. At announcement, users had no date to plan around. |
| "The Sora web and app experiences were discontinued on April 26, 2026." "The Sora API was discontinued on September 24, 2026." After any final export window, OpenAI "will permanently delete any data associated with your use of Sora." | [OpenAI Help, What to know about the Sora discontinuation](https://help.openai.com/en/articles/20001152-what-to-know-about-the-sora-discontinuation). WebFetch returned 403; read with a direct download Oct 29, 2026; quotes string-matched. | Vendor page. The same dates appear in [The Decoder, March 28, 2026](https://the-decoder.com/openai-sets-two-stage-sora-shutdown-with-app-closing-april-2026-and-api-following-in-september/) (secondary, opened). |
| Users objected to an Adobe terms update granting a "non-exclusive, worldwide, royalty-free sublicensable, license" to content. Adobe said on June 10, 2024 "We don’t train generative AI on customer content" and planned new terms for June 18, 2024. | [Malwarebytes, Pieter Arntz, June 12, 2024](https://www.malwarebytes.com/blog/news/2024/06/no-ai-training-in-newly-distrusted-terms-of-service-adobe-says). Opened Oct 29, 2026. | Shows terms of a tool in daily use can change twice in about a week; not a campaign that broke. |

**No public business incident found.** Four searches (Sora shutdown export, DALL-E 3 shutdown migration, AI image tool terms of service changes for commercial use, the Sora help page) found vendor notices, news and blogs, but no named business whose campaign broke. **Price changes are not covered:** we opened no source on an image vendor raising prices mid-campaign and make no claim about it. Search summaries about other vendors' terms were not opened and are not used.

## 5. The fix
**The principle:** Every campaign asset knows which model, version and terms made it, and the team can finish the campaign if that vendor disappears tomorrow.

**Do this: brand teams, agencies and tool builders**
1. **Record the source per asset.** Each asset record holds the vendor, product (app or API), model name and exact version, terms version date and plan tier. No record, no publish.
2. **Name dependencies at kickoff.** The campaign brief lists every model and app it relies on and whether the campaign needs to make new assets on it later (extensions, new sizes, new cuts).
3. **Watch deprecation notices.** For each listed model, someone checks the vendor's deprecations or status page weekly and reads vendor emails. A shutdown date is logged against every campaign that uses the model the day it is seen.
4. **Keep masters outside the vendor.** The full-resolution output, prompt, settings and any input images are saved to the company's own storage at generation time. A vendor gallery or library never holds the only copy.
5. **Export on notice.** When a shutdown is announced, export everything from that vendor's library within 5 business days, well before the cutoff, and confirm the count.
6. **Write an exit plan before launch.** For each dependency: the fallback (edit from masters, or a named replacement model), who approves a replacement, and how long a re-test takes. A replacement's output is a new asset and needs new approval.
7. **Re-check terms on change.** When a vendor's terms version date changes, re-read the commercial-use and license sections and log the result before making more campaign assets on it.
8. **Don't promise what the vendor controls.** Client contracts and briefs do not promise future extensions "in the same model" unless a fallback is written down.

**Reference design: dependency register (one row per model or app per campaign)**
| Field | Example |
|---|---|
| Campaign / assets | Spring Trail 2026 / 4 hero images, 12 clips |
| Vendor, product, model, version | OpenAI API, dall-e-3; OpenAI Sora app |
| Terms version date / date read | Date on the vendor's terms page / Mar 2, 2026 |
| Needs new assets later? | Yes: summer sizes and two more clips |
| Shutdown notice seen / shutdown date | Nov 14, 2025 / May 12, 2026; Mar 24, 2026 / Apr 26, 2026 |
| Masters stored / export confirmed | Brand drive, 4 of 4; 12 of 12 exported Apr 2 |
| Exit plan / approver | Edit from masters; replacement model only after re-test, approver M. Lopez |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A request needs a model that is retired or has a shutdown date: edit from masters, test a replacement for review, something else. Do not offer choices when the model is current and no notice is logged; just run and log. |
| Admit uncertainty and show how to check | The assistant cannot tell whether a model still exists or what the terms now say: say so and link the vendor's deprecations or terms page |
| Hand off to a person | A shutdown date falls inside a live campaign with no exit plan, or terms changed while assets were in production |

**Don't over-correct.** Do not ban a vendor because it might retire a model someday; every vendor can. Do not move a live campaign to a new model just because one was announced; edit from masters until the campaign ends. Do not re-read terms on every job; the register date covers it until the version date changes. Do not treat a model's new default or changed look as this failure: that is [the model update page](ai-image-model-update-changes-approved-style.md).

**Hand-off rule.** When a shutdown date or terms change hits a live campaign with no tested exit plan, send it to the campaign owner within one business day with the dependency register and the list of assets not yet exported. Terms questions go to legal.

**Framework used:** none yet. Rules 4 and 5 follow the Sora help page on deletion after shutdown; rule 3 follows the OpenAI deprecations page; rule 7 follows the Adobe terms episode; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-vendor-retires-model-or-changes-terms-mid-campaign.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Asset with no model or terms record | Publish blocked | 1 |
| 2 | Request on a retired model | Says it is retired, offers masters or a reviewed replacement | 3, 6 |
| 3 | Shutdown notice posted for a model in use | Logged against every campaign within a week | 3 |
| 4 | Clips held only in the vendor library after notice | Export within 5 business days, count confirmed | 4, 5 |
| 5 | Silent swap to a replacement model | Refused; new output needs approval | 6 |
| 6 | Terms version date changes | New assets paused until terms re-read and logged | 7 |
| 7 | Current model, no notice | Runs with a log entry, no choices | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Campaigns at risk** (primary) | 0 (proposed) | Weekly join of the dependency register with logged shutdown dates; campaigns with no tested exit plan / live campaigns | Any |
| Assets with no model and terms record | 0 (proposed) | Monthly sample of 100 published assets | Over 2% |
| Assets whose only copy is in a vendor library | 0 (proposed) | Asset records with no company storage path | Any |
| Days from shutdown notice to export complete | 5 business days or less (proposed) | Notice date versus export confirmation date | Over 10 business days |
| Jobs blocked on models with no notice (counter-metric) | Under 5% of blocks (proposed) | Monthly review of the block log | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Generation call fails with a model-not-found error | API error log | A typo in the model name |
| Model name in a job is different from the one in the asset's record | Generation log versus asset record | A planned, approved move to a new model |
| A model listed in the register appears on the vendor's deprecations page | Weekly fetch of the page | The listed date is past the campaign's end |
| A vendor's terms page shows a new version date | Weekly fetch of each registered vendor's terms page | A wording fix with no change in meaning |

**Starter rule:** no live campaign uses a model or app with an announced shutdown date unless its masters are stored outside the vendor and its exit plan names an approver.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-vendor-retires-model-or-changes-terms-mid-campaign
runs: [pre_generate, pre_publish, on_deprecation_notice, on_terms_change]
reads: [asset.vendor, asset.model, asset.model_version, asset.terms_version, asset.master_path, register.shutdown_date, register.exit_plan, register.approver, campaign.end_date]
trigger: model retired or has a shutdown date before campaign end, or asset has no master outside the vendor, or terms version changed since last read, or job model differs from record
moves: [offer_choices, admit_uncertainty, hand_off]
choices: ["Edit from the stored masters", "Test a replacement model for review", "Something else"]
on_miss: block_job_or_open_ticket
metric: campaigns at risk
counter_metric: jobs blocked on models with no notice
status: proposed
```

## 8. Related patterns
- [AI image model update changes the approved style](ai-image-model-update-changes-approved-style.md) - the closest existing page and an overlap. It covers a new default or version changing the look, and mentions retirement as one cause. This page covers losing access entirely (model, app or library gone) and terms changing, where the fix is masters, exports and an exit plan rather than pinning a version. A merge proposal goes to a person to review.
- [Approved AI image cannot be made again](approved-ai-image-cannot-be-reproduced.md) - the same model gives a different image; its "keep the master" rule is the backbone of the exit plan here.
- [Quality drift in generated images](../../generation-artifacts/failures/quality-drift.md) - output quality degrading over repeated steps; here quality is fine but access ends.
- [No record of the prompt, model and approver](no-record-of-prompt-model-and-approver-for-ai-images.md) - the record this page needs to list what a retirement touches.
- [AI image vendor indemnity gaps](../../ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md) - another case where vendor terms decide what the business can rely on.

## 9. Common questions
### Can I still use DALL-E 3 in 2026?
Not through the API. OpenAI's deprecations page says DALL-E 2 and DALL-E 3 were removed from the API on May 12, 2026, and lists gpt-image models as replacements. Images a replacement makes are new images; get them approved again.

### What happened to my Sora videos?
OpenAI's help page says the Sora app and web closed April 26, 2026 and the API on September 24, 2026, and that data is permanently deleted after any final export window. Check the help page for any export option still open.

### How do I protect a campaign from an AI tool shutting down?
Save every master file, prompt and setting to your own storage when you make it, record the model per asset, and write down a fallback before launch. See [the fix](#5-the-fix).

### Do I have to switch to the replacement model?
Only if you need new assets. Resizing or cropping stored masters needs no model. A replacement is a new tool: re-test and get sign-off before using it.

### Does a terms change affect images I already made?
It can; that depends on the old and new terms and your contract. Log the terms version per asset and ask your lawyer.
