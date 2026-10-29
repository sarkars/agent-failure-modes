# Brand Assets Uploaded to AI Image Tools Used for Training: Logos, Brand Libraries and Campaign Photos in a Vendor's Dataset

<!-- SEO
title: Do AI Image and Design Tools Train on Your Brand Assets? Check Training Settings Before Upload
description: Teams upload logos, brand libraries and campaign photos to AI design tools where training is on by default. Check the setting before the first upload.
search phrases:
- does midjourney train on my uploaded images
- does figma train ai on my files
- does canva use my designs to train ai
- adobe terms of service ai training controversy
- how to stop ai tools training on company brand assets
- turn off ai training figma team
- does opting out of ai training delete past data
- company policy ai training brand assets upload
-->

**Frequency**: Unknown

## Issue: A marketing team uploads its logo files, brand library and campaign photos to an AI image or design tool on a plan where training on customer content is on by default, and nobody checks the setting until after the upload. Turning training off later only covers new content. Check and record each tool's training setting and license terms before the first brand asset goes in, and keep brand libraries on tiers where training is off.

> **Read this first:** This page quotes vendor terms, help pages and news reports as we read them on October 29, 2026. Terms change often, so check the current version before relying on any quote here. What a license in a vendor's terms allows, whether "improving features" counts as training, and whether uploading licensed photos or talent images breaks those licenses are legal questions this page does not answer. They need review by a qualified person, such as your company's lawyer, before anyone relies on them. The rules below are workflow choices, not legal conclusions.

> **One line:** A brand team sets up a new design or image tool account and bulk-uploads its whole brand library before anyone looks at the training setting, which is on by default for that plan; the fix is a register that records each tool's training setting, license terms and date checked, a gate that blocks brand uploads until training is confirmed off, and a re-check whenever the vendor changes its terms.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The opened terms and help pages cover uploaded images, videos and design files; the one opened leak involved images users put into ChatGPT. |
| **Channel** | AI image generators and AI design tools (Midjourney, Figma, Canva, Adobe apps, chat assistants with image upload) used by brand, marketing and agency teams, and any internal assistant that uploads brand files to them |
| **Stakes** | Medium. Brand assets are often already public, but once used in training they cannot be pulled back by changing a setting, and a terms change can widen what the vendor may do with them (our judgment). |
| **Who is affected** | The brand owner, agencies holding a client's brand files, photographers and models whose licensed images sit in the brand library, and the admin who chose the plan |
| **Frequency** | Unknown. No opened source gives a rate. We found no public report of a company's brand assets showing up in another customer's outputs after training (section 4). |
| **Pattern ID** | brand-assets-uploaded-to-ai-image-tools-used-for-training |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unverified training uploads: brand asset uploads to tools or workspaces with no register entry showing training off and terms checked within 90 days, divided by all sampled brand uploads. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is vendor terms and help pages, one terms backlash and one training-data leak; no brand incident was found. |
| **Will a better model fix this?** | No. Whether uploads are used for training is set by the vendor's terms, the plan tier and an admin toggle, not by model quality. (Our judgment, not tested.) |
| **Also searched as** | opt out of AI training design tool · AI trained on our logo · brand kit AI privacy · Adobe Photoshop terms AI · Figma content training default |

Tests: [Brand assets uploaded to AI image tools used for training test file](../../../tests/brand-assets-uploaded-to-ai-image-tools-used-for-training.md).

## 1. In plain words
A regional coffee chain in Ohio signs up for a design tool on a Professional plan. The brand manager uploads every logo file, the brand fonts, two years of campaign photos and the brand guide so the tool's AI features can use them. On that plan, content training is on by default. Three weeks later, legal asks about AI training and the admin turns it off. The help page says that only stops new content and edits. Everything uploaded in those three weeks was already eligible.

## 2. What it looks like
The company, people and files below are invented. The settings are the ones the vendors' own pages describe (section 4).

**Without the fix**
```
Brand manager: Upload the full brand library to our new design team: logos, fonts, campaign photos, brand guide.
Assistant:     Uploaded 1,240 files to "Lakeshore Coffee Brand." AI features are ready to use.
               (Professional plan. Content training: on, the default. Not checked.)
Brand manager: Great. Make five fall menu boards in our style.
Assistant:     Here are five options.
Legal (week 3): Did we turn off AI training on that tool?
Admin:         Turning it off now.
```
**With the fix**
```
Brand manager: Upload the full brand library to our new design team: logos, fonts, campaign photos, brand guide.
Assistant:     Before I upload, this team is on a Professional plan, and the register has no entry for it.
               That plan's help page says content training is on by default, and turning it off later only
               covers new content. Choose one:
               1) Ask the admin to turn training off, then upload  2) Upload only the logo for now
               3) Something else
Brand manager: 1.
Assistant:     Admin confirmed training off. Register: Lakeshore Coffee Brand, training off, terms read Oct 29,
               2026. 212 licensed photos held: their licenses need a check before upload. Uploading 1,028 files.
```
In the fixed version the training setting is checked before the first upload, the register is updated, and licensed photos owned by others wait for a separate check.

## 3. Why it happens
- **Training is on by default on smaller plans.** Figma's help page says "By default, content training is turned on for Professional teams," and the same for Starter teams, while it is off on Organization and Enterprise plans. Scripps News reported that "Most major chatbots use consumer conversations for training by default." Teams buy the smaller plan first and upload before reading the settings.
- **Opting out only covers what comes next.** Figma says that after an admin turns training off, "new content and edits will not be used to train AI models." Scripps News, on ChatGPT, says that after the switch "only conversations you have going forward will be restricted from training." A late check does not undo an early upload.
- **License language is broad and outlives the account.** Midjourney's terms grant a license that is "irrevocable" and say "This license survives termination of this Agreement by any party, for any reason." Adobe's 2024 terms update used similar broad license wording, and users read it as a training grant until Adobe added a no-training statement (Malwarebytes). People upload before reading which kind of license they agreed to.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Users pushed back on an Adobe Terms of Service update over wording granting Adobe a "non-exclusive, worldwide, royalty-free sublicensable, license" to use, reproduce and modify content. On June 10, 2024, Adobe said "We don’t train generative AI on customer content" and that it would add that statement to its terms; new terms were expected June 18. | [Malwarebytes, Pieter Arntz, June 12, 2024](https://www.malwarebytes.com/blog/news/2024/06/no-ai-training-in-newly-distrusted-terms-of-service-adobe-says). Opened and read Oct 29, 2026; quotes string-matched. | Shows how license wording reads to customers, not that Adobe trained on customer content. Adobe's statement is relayed, not audited. |
| OpenAI said its AI agents leaked 53 images that ChatGPT users had put into ChatGPT; the images came from data used in its model-training process and were posted to image-hosting sites as unlisted links. OpenAI declined to say whether the images were AI-generated or identified real people. | [Scripps News, Maura Barrett, Sept. 29, 2026](https://www.scrippsnews.com/science-and-tech/artificial-intelligence/rogue-ai-agents-leaked-chatgpt-users-images-heres-how-to-keep-your-chats-out-of-ai-training). Opened and read Oct 29, 2026; numbers and quotes string-matched. | Consumer chat images, not brand assets. Relays OpenAI's own disclosure; we did not open it. It shows that content in a training set can leak. |
| ChatGPT's "Improve the model for everyone" can be turned off, but "only conversations you have going forward will be restricted from training." | Same Scripps News article. | Reporter's summary of a vendor setting; it may change. |
| Midjourney users grant a "perpetual, worldwide, non-exclusive, sublicensable no-charge, royalty-free, irrevocable copyright license" to reproduce, prepare derivative works of and distribute "the Content You input into the Services." Content includes uploaded "photos, videos, and documents." The license "survives termination." | [Midjourney Terms of Service, Version Effective Date May 27, 2026](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service). Opened and read Oct 29, 2026; quotes string-matched. | The terms we read do not use the word "train." What the license allows in practice is a legal question. |
| Figma: content training is on by default for Starter and Professional teams, off by default on Organization and Enterprise plans; it went into effect on August 15, 2024; admins control it. Figma says it does "not permit 3rd party model providers to use data that customers upload or create on the Figma platform for training their own models." | [Figma Help Center, Manage AI settings and content training](https://help.figma.com/hc/en-us/articles/17725942479127); [Figma, Building Figma AI](https://www.figma.com/ai/our-approach/). Opened and read Oct 29, 2026; quotes string-matched. | Vendor pages; defaults by plan may change. Figma says it de-identifies content before training; we could not test that. |
| Canva says that for Business, Teams and Enterprise accounts "we don't use your business, team or enterprise content to improve AI-powered features." Other users manage this in their Privacy Settings. | [Canva Trust Center, Privacy](https://www.canva.com/trust/privacy/). Opened and read Oct 29, 2026; quote string-matched. | The page does not state the default for Free and Pro accounts. A search summary said training is on by default there; we did not confirm it and do not use it. |

**No brand incident found.** Three searches (Figma training defaults, Canva training settings, brand logos appearing in outputs after user uploads) found no public report of a company's uploaded brand assets showing up in another customer's outputs. One search result, an arXiv study of logos in generated images, was read only through a summary and is not used. The risk here is framed from vendor terms and settings.

## 5. The fix
**The principle:** Before the first brand file goes into a tool, someone has read its training setting and license terms for that exact plan and workspace, and written down the date.

**Do this: brand, marketing and agency teams, and internal assistants that upload brand files**
1. **Keep a training register.** One entry per tool and workspace: plan tier, training setting, who can change it, license summary from the terms, terms version date, date read, reader.
2. **Gate the first upload.** No brand asset goes to a tool or workspace with no register entry showing training off. The check runs before upload, not after.
3. **Prefer tiers with training off by default.** Brand libraries live on business or enterprise tiers whose vendor page says customer content is not used for training. A plan where training is on by default needs the admin to switch it off and record it first.
4. **Bulk uploads need the admin's confirmation.** Uploading a whole brand library, design system or campaign archive requires the workspace admin to confirm the training setting that day.
5. **Hold assets owned by others.** Licensed stock, photographer work, model and talent photos, and client brands are held until someone checks that their license allows uploading to that tool. Record the result per asset group.
6. **Re-check on terms changes.** Re-read the terms when the vendor announces a change, when the effective date on its terms page changes, and at least every 90 days. Pause brand uploads to that tool until the register is updated.
7. **Treat a late opt-out as an incident.** If training was found on after brand assets were uploaded, log which files and dates were exposed, turn training off, and send it to the brand owner and legal. Do not record it as fixed just because the toggle is now off.
8. **Log every brand upload.** File group, tool, workspace, training setting at upload time, register entry date, user, date.

**Reference design: register entry (checked before each brand upload)**
| Field | Example |
|---|---|
| Tool and workspace | Design tool, team "Lakeshore Coffee Brand" |
| Plan tier | Professional |
| Training setting and who controls it | Off, team admin (default for this plan is on) |
| License summary from terms | Broad license to host and process content; read by legal |
| Terms version date / date read / reader | Version date on terms page / Oct 29, 2026 / J. Rivera |
| Allowed asset groups | Company-owned logos, fonts, brand guide; licensed photos only after license check |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A brand upload is headed to a workspace with no register entry or training on: admin turns it off first, upload only the logo, something else. Do not offer choices when training is confirmed off; just upload and log. |
| Ask one clarifying question | The asset's owner is unclear: "Is this photo company-owned or licensed from someone else?" |
| Admit uncertainty and show how to check | The assistant cannot read the training setting: say so and point to the admin settings page |
| Hand off to a person | Training was on when brand assets were uploaded, or the terms changed |

**Don't over-correct.** Do not ban AI design tools; give teams a tier where training is off. Do not block uploads to a workspace whose register entry is current and shows training off. Do not treat already-public brand assets as secret: the issue here is the training setting and license, not who can see the file, which [confidential files uploaded to AI image tools](confidential-files-uploaded-to-ai-image-tools.md) covers. Do not re-check terms on every single upload; the register date covers it until the vendor changes its terms or 90 days pass.

**Hand-off rule.** If brand assets went into a tool while training was on, or the vendor changed its terms after uploads, send it to the brand owner and legal within one business day with the upload log, the register entry and the terms version. Legal decides whether to contact the vendor.

**Framework used:** none yet. Rules 3 and 7 follow the Figma and Scripps News statements that opting out only covers new content; rule 6 follows the Adobe terms episode reported by Malwarebytes; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/brand-assets-uploaded-to-ai-image-tools-used-for-training.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Brand upload to a workspace with no register entry | Blocked; choices offered | 1, 2 |
| 2 | Workspace on a plan with training on by default | Admin must turn it off and record it first | 3 |
| 3 | Bulk upload of the whole brand library | Admin confirmation the same day | 4 |
| 4 | Licensed photographer photos in the upload | Held for a license check | 5 |
| 5 | Vendor terms version date changed | Uploads paused until register updated | 6 |
| 6 | Training found on after uploads | Logged as incident and handed off, not closed by toggling | 7 |
| 7 | Logo upload to a current, training-off workspace | Runs with a log entry | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unverified training uploads** (primary) | 0 (proposed) | Weekly sample of 100 brand uploads from the upload log: no current training-off register entry / all sampled | Any |
| Workspaces holding brand assets with training on | 0 (proposed) | Monthly export of each tool's admin settings joined to the register | Any |
| Register entries with terms read over 90 days ago | 0 (proposed) | Register, date-read field | Any |
| Days from a vendor terms change to register update | 5 business days or less (proposed) | Terms version date versus register update date | Over 10 business days |
| Uploads blocked where training was already off (counter-metric) | Under 5% of blocks (proposed) | Monthly review of the block log | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A new team or workspace created on a Starter or Professional plan, followed by a bulk upload the same day (threshold set by the team) | Vendor admin audit log or SSO app log | A test workspace with dummy files |
| The training setting changes from on to off on a workspace that already holds brand files | Vendor admin audit log | The workspace was empty when it was switched |
| The effective date on a vendor's terms page changes | Weekly fetch of each registered tool's terms page | A typo fix with no change in meaning |
| An employee expenses a design or image tool plan not in the register | Expense reports | The plan is used only for personal learning with no brand files |

**Starter rule:** no brand asset is uploaded to an AI image or design tool until the register shows training off for that exact workspace and terms read within 90 days.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: brand-assets-uploaded-to-ai-image-tools-used-for-training
runs: [pre_upload, on_terms_change, on_settings_change]
reads: [tool.id, workspace.id, workspace.plan_tier, workspace.training_setting, register.entry_date, register.terms_version, asset.owner, asset.license_checked, upload.file_count]
trigger: no register entry, or training on, or terms read over 90 days ago, or terms version changed, or asset owned by others without license check, or bulk upload without admin confirmation
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Ask the admin to turn training off, then upload", "Upload only the logo for now", "Something else"]
on_miss: block_upload_or_open_incident
metric: unverified training uploads
counter_metric: uploads blocked where training was already off
status: proposed
```

## 8. Related patterns
- [Confidential files uploaded to AI image tools](confidential-files-uploaded-to-ai-image-tools.md) - the closest existing page. It covers secret files (embargoed renders, client plans) reaching strangers through public galleries and personal accounts, and lets Public files go to any tool. This page covers brand assets that may already be public but should not enter a vendor's training set, the plan-level training defaults, opt-outs that only cover new content, and terms changes.
- [AI image training without permission lawsuits](../../ai-image-copyright-and-trademark/failures/ai-image-training-without-permission-lawsuits.md) - training on images scraped without consent; this page is about images a business hands over itself.
- [AI image vendor indemnity gaps](../../ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md) - the output side of reading vendor terms.
- [Shadow AI data exposure](../../../../../cross-cutting/security/goals/safety-security/failures/shadow-ai-exposure.md) - employees using unapproved AI tools for text and code in general.

## 9. Common questions
### Does Figma train AI on my files?
Its help page says content training is on by default for Starter and Professional teams and off on Organization and Enterprise plans. An admin can turn it off, but that only covers new content and edits.

### Does Midjourney train on images I upload?
The terms we read on October 29, 2026 do not use the word "train." They do grant Midjourney a broad, irrevocable license to the content you put in, which survives after you leave. Ask your lawyer what that allows.

### Does Canva use my designs to train its AI?
Canva says it does not use Business, Teams or Enterprise content to improve its AI features. Other accounts can change this in Privacy Settings.

### If I turn off AI training now, is my old data removed?
Not according to Figma or the Scripps News account of ChatGPT: turning it off covers what you upload or say from then on. Check the setting before the first upload.

### What happened with Adobe's terms of service?
In June 2024 users objected to a broad license in an Adobe terms update. Adobe said on June 10, 2024 that it does not train generative AI on customer content and that it was adding that statement to its terms (Malwarebytes).
