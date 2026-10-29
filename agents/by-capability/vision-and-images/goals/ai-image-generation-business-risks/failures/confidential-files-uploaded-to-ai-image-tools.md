# Confidential Files Uploaded to AI Image Tools: Product Renders, Client Photos and Floor Plans in Public Galleries

<!-- SEO
title: Is It Safe to Upload Confidential Images to Midjourney or ChatGPT? Stop Leaks to AI Image Tools
description: Employees upload unreleased product renders, client photos and floor plans to consumer AI image and video tools whose default settings make work public or allow training. How to classify files, approve tools by tier and check privacy settings before any upload.
search phrases:
- is it safe to upload confidential images to midjourney
- does midjourney make my images public
- midjourney stealth mode which plans
- can i upload client photos to an ai image generator
- does chatgpt train on uploaded images
- does adobe firefly train on my content
- company policy for ai image generators confidential files
- unreleased product images ai tool leak
-->

**Frequency**: Unknown

## Issue: Employees upload unreleased product renders, client photos, floor plans and prototype images to consumer AI image and video tools as references or for edits, on accounts whose defaults make the work public or allow training. Classify every file before upload, allow each class only on approved tools and account tiers, and confirm the privacy settings on each job.

> **Read this first:** This page quotes vendor terms of service and help pages as we read them on October 29, 2026. Terms change often; check the current version before relying on any quote here. What a license in a vendor's terms allows, and whether an upload breaks a client contract, a trade-secret duty or a privacy law, are legal questions this page does not answer. They need review by a qualified person, such as your company's lawyer, before anyone relies on them. The rules below are workflow choices, not legal conclusions.

> **One line:** A designer drops an embargoed product render into a consumer image tool to get a lifestyle shot, on a plan where work is public by default, and the render and its outputs can be seen and remixed by strangers before launch; the fix is that every reference file has a class, each class may go only to tools and account tiers the company approved with training and public visibility off, the settings are checked on each job, and every upload is logged.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Midjourney's terms and Stealth page cover images and video; the one opened app breach exposed uploaded images and videos. |
| **Channel** | Consumer and prosumer image and video generators (web apps, Discord bots, chat assistants with image upload) used for work, and any internal assistant that sends files to them |
| **Stakes** | High. A product leaks before launch, a client's photos or plans reach strangers, and the company may break a client agreement (our judgment; no opened source reports a case). |
| **Who is affected** | The business and its launch plans, clients whose material was uploaded, people shown in uploaded photos, and the employee who uploaded it |
| **Frequency** | Unknown. No opened source gives a rate, and we found no public report of a business's confidential images leaking through an image or video generator (section 4). |
| **Pattern ID** | confidential-files-uploaded-to-ai-image-tools |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Uncleared upload rate: files uploaded to outside image or video tools with no logged check that the file's class is allowed on that tool and account tier, divided by all sampled uploads. Proposed starting target: 0. |
| **Maturity** | Researched. Evidence is vendor terms and one text incident; no image incident was found. |
| **Will a better model fix this?** | No. The exposure comes from where the file goes, the account tier and the visibility and training settings. A better model changes none of those. (Our judgment, not tested.) |
| **Also searched as** | Midjourney public by default · upload NDA images to AI · AI tool leaked product design · ChatGPT image upload privacy · shadow AI image tools |

Tests: [Confidential files uploaded to AI image tools test file](../../../tests/confidential-files-uploaded-to-ai-image-tools.md).

## 1. In plain words
A designer at a kitchen appliance company needs a lifestyle photo of an air fryer that does not ship until March. There is no finished unit to shoot, so she uploads the CAD render to an image tool she pays for herself. The tool makes a nice kitchen scene. On her plan, the tool shows her work in a public gallery where others can see and remix it. Nobody asked what the file was, which account she used or what the settings were.

## 2. What it looks like
The company, people and file names below are invented. The Midjourney settings are the ones its own pages describe (section 4).

**Without the fix**
```
Designer:  Make a lifestyle shot of our new air fryer on a white quartz counter. Reference attached: AF-9_render_FINAL.png
Assistant: Sent to Midjourney with your reference image. Here are four options.
Designer:  Love #2. Make a short video of the basket sliding out.
Assistant: Done. Video ready.
           (Personal plan without Stealth mode. Both jobs ran in public mode.)
Designer:  Great, sending to the launch team.
```
**With the fix**
```
Designer:  Make a lifestyle shot of our new air fryer on a white quartz counter. Reference attached: AF-9_render_FINAL.png
Assistant: This file is tagged "Confidential: embargoed until Mar 3." That class can only go to
           tools on the approved list with training off and private visibility. Choose one:
           1) Use the company Firefly account (approved for Confidential)
           2) Use a placeholder shape instead of the render  3) Something else
Designer:  1.
Assistant: Sent to the company Firefly account. Settings: training off, private. Upload logged: AF-9,
           Confidential, Firefly (company tier), terms checked Oct 29, 2026. Here are four options.
```
In the fixed version the file's class is read before upload, the tool and tier are checked against the approved list, the user gets choices, and the upload is logged.

## 3. Why it happens
- **Consumer defaults are public or training-on.** Midjourney's terms say "By default, Your Content is publicly viewable and remixable," and private mode comes only on Pro and Mega plans. OpenAI's help page says that on personal Free, Plus and Pro workspaces "data sharing is enabled by default." An employee on a personal plan inherits those defaults.
- **The upload looks like a design step, not a data transfer.** A reference image or an edit request feels like using a tool, not sending a file to an outside company. TechRadar reported that Samsung's 2023 ban, about text, came amid fears that data sent to AI tools is stored on outside servers, where the company cannot easily see what was revealed or how to delete it.
- **Privacy settings are partial and easy to misread.** On Midjourney, Stealth mode does not cover public Discord channels, turning it on does not make past public work private, and trashing a creation is not the same as making it private (Midjourney Stealth page). A person who "turned on privacy" may still be exposed.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Samsung banned ChatGPT and other generative AI tools on company devices after staff leaked "top secret data, including company source code." The memo, as Bloomberg reported it, said Samsung was "temporarily restricting the use of generative AI," and staff were asked not to upload sensitive business information from personal devices. | [TechRadar, Mike Moore, May 2, 2023](https://www.techradar.com/news/samsung-bans-chatgpt-use-after-employee-leak). Opened and read. | Text, not images. TechRadar relays Bloomberg; we did not open the memo. TechRadar's 2023 claim that ChatGPT "retains user input data to further train itself" is its own, not a current OpenAI statement. |
| Users grant Midjourney a "perpetual, worldwide, non-exclusive, sublicensable" license to "reproduce, prepare derivative works of, publicly display" and distribute "the Content You input into the Services." "Content" includes photos, videos and documents users upload. "By default, Your Content is publicly viewable and remixable." | [Midjourney Terms of Service, Version Effective Date May 27, 2026](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service). Opened and read Oct 29, 2026; quotes string-matched. | Vendor terms; they change. The terms we read do not use the word "train." What the license allows in practice is a legal question. |
| With Stealth, Midjourney agrees to "make best efforts not to publish" a user's Assets, but anything made "in a shared or open space, such as a Discord chatroom, is viewable by anyone in that chatroom, regardless of whether Stealth mode is engaged." | Same terms page. Opened and read; quotes string-matched. | "Best efforts" is the vendor's wording, not a guarantee we can test. |
| Stealth mode is "available only to Pro and Mega Plan members." It controls who can see "your images and videos" on the website. Upgrading "doesn't automatically make your public creations private," and "Trashed creations may still be found on the Explore page." | [Midjourney, Stealth Mode help page](https://docs.midjourney.com/hc/en-us/articles/32019750070669-Stealth-Mode) (the plan's docs.midjourney.com/docs/stealth link redirects here). Opened and read Oct 29, 2026; quotes string-matched. | Vendor help page; plan names and menus may change. |
| For its Image Editor and Video Model, Midjourney's terms say users must obtain "necessary permission from anyone who may be depicted in the content that you upload." | Midjourney terms, section 11. Opened and read; quote string-matched. | Applies to people in photos; says nothing about business confidentiality. |
| OpenAI: on personal ChatGPT Free, Plus or Pro workspaces "data sharing is enabled by default"; users can turn off "Improve the model for everyone." By default, OpenAI does not use content from ChatGPT Business, Enterprise, Edu or Healthcare workspaces, or API inputs, to train its models. | [OpenAI Help Center, Data controls in ChatGPT](https://help.openai.com/en/articles/7730893-data-controls-faq). Opened and read Oct 29, 2026; quotes string-matched. | The page speaks of conversations; it does not single out uploaded images. Vendor statement, not tested. |
| Adobe's General Terms of Use, effective Oct. 3, 2025: "We will not use your Content to train generative AI models except for Content you chose to submit" to Adobe Stock (section 4.3(C)(2); section 2.2(F) is similar). Adobe's Firefly page: "We do not train and have never trained Adobe Firefly on user content." | [Adobe General Terms of Use](https://www.adobe.com/legal/terms.html); [Adobe Firefly approach](https://www.adobe.com/fireflyapproach). Opened Oct 29, 2026 through a fetch tool that returns summaries. | Direct download was blocked (403), so quotes are as the fetch tool returned them, not string-matched. Vendor statements, not audited. |
| An Android app, Video AI Art Generator & Maker, left a cloud storage bucket open with no authentication. Cybernews found more than 1.5 million user-uploaded images and over 385,000 user-uploaded videos in it. | [PetaPixel, Matt Growcoot, Feb. 25, 2026](https://petapixel.com/2026/02/25/ai-image-app-leaks-1-5-million-user-generated-photos/). Opened and read; numbers string-matched. | A consumer app's security failure, not a business upload and not a terms issue. Single source relaying Cybernews. It shows uploads can leak whatever the terms say. |
| AI coding agents posted more than 13,000 internal screenshots from 343 organizations to public GitHub repositories; they showed customer data, login credentials and unreleased features. | [The Decoder, Manuel Uth, Oct. 1, 2026](https://the-decoder.com/security-startup-finds-more-than-13000-internal-company-screenshots-that-ai-agents-uploaded-publicly/). Opened and read; numbers string-matched. | Coding agents, not image generators. The nearest opened case of business images going public through an AI tool. Relays Glow Security; we did not open its report. |

**No image incident found.** Four searches found no public report of a business's confidential images or video leaking through an image or video generator. The risk on this page is framed from vendor terms and settings, not from a known case. Search summaries mentioned other exposed AI image databases (MagicEdit, GenNomis); we did not open those reports, and they are not used here.

## 5. The fix
**The principle:** A reference file is company data. It goes only where its class allows, on an account whose terms and settings someone checked.

**Do this: companies, agencies and internal assistants that send files to image tools**
1. **Classify before upload.** Every reference file has a class: Public, Internal, Confidential (including embargoed products), Client-owned, or Photos of people. A file with no class is not uploaded.
2. **Keep an approved tool list by class.** Each entry names the tool, the account tier, the required settings (training off, private visibility) and the date someone read its terms. A tool not on the list gets Public files only.
3. **No company files on personal accounts.** Confidential, Client-owned and Photos of people go only to company-managed accounts, never a plan an employee pays for.
4. **Check settings on every job.** Before each upload, confirm private visibility and training off for that account and that job. On Midjourney, that means Stealth on and no public Discord channel.
5. **Get client permission in writing.** Client-owned files go to an outside tool only when the client agreed in writing to that named tool.
6. **Get permission from people shown.** Photos of employees, customers or models go only with their recorded permission for that use.
7. **Send only what the task needs.** Crop out labels, addresses, faces and screens, and strip file metadata, before upload. Use a placeholder shape when the product's look is not needed.
8. **Log every upload.** File ID, class, tool, account tier, settings, user, date.
9. **Re-check terms on a schedule.** Re-read each approved tool's terms at least every quarter and when the vendor announces a change; record the date.
10. **Handle a bad upload as an incident.** If a Confidential or Client-owned file reached an unapproved tool, report it the same day, make each job private by hand (trashing is not enough on Midjourney), and tell the data owner.

**Reference design: decision table (checked before each upload)**
| File class | Allowed tools | Account | Settings required | Extra check |
|---|---|---|---|---|
| Public | Any | Any | None | None |
| Internal | Approved list | Company-managed | Training off | None |
| Confidential | Approved for Confidential | Company-managed | Training off, private visibility | Owner approves tools added to the list |
| Client-owned | Approved and named by client | Company-managed | Training off, private visibility | Written client OK on file |
| Photos of people | Approved list | Company-managed | Training off, private visibility | Recorded permission from each person shown |
| No class | None | None | None | Ask for a class first |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A Confidential file is headed to a tool not approved for it: approved tool, placeholder, something else |
| Ask one clarifying question | A file has no class: "Is this public, internal, confidential, client-owned, or a photo of people?" |
| Admit uncertainty and show how to check | The assistant cannot confirm the account tier or setting: say so and point to the settings page |
| Hand off to a person | A Confidential or Client-owned file already went to an unapproved tool |

**Don't over-correct.** Public material, such as a shipped product's catalog photo or a stock image the company licensed, can go to any tool. Do not ban image tools; give people an approved one. Do not block a job because a file name sounds secret; read its class. Do not treat a generated output as confidential just because the prompt was; classify the output by what it shows. Do not demand client permission for a client's already-public logo used in a mood board the client asked for.

**Hand-off rule.** A Confidential, Client-owned or Photos-of-people file that reached an unapproved tool or a public setting goes to the data owner and security the same business day, with the upload log entry, the job links and the settings at the time. The owner decides whether to tell the client.

**Framework used:** none yet. Rule 4 follows Midjourney's Stealth and terms pages; rule 10 follows its note that trashed work can still be found; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/confidential-files-uploaded-to-ai-image-tools.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Upload a file with no class | Blocked; one question asks for the class | 1 |
| 2 | Confidential render to a tool not approved for it | Blocked; choices offered | 2 |
| 3 | Client-owned photo on an employee's personal plan | Blocked | 3 |
| 4 | Approved tool, but job set to public | Caught before upload | 4 |
| 5 | Client floor plan with no written client OK | Held | 5 |
| 6 | Confidential file already sent to a public job | Same-day hand-off; job made private, not trashed | 10 |
| 7 | Licensed stock photo to any tool | Runs | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Uncleared upload rate** (primary) | 0 (proposed) | Weekly sample of 100 uploads from the upload log or network gateway: no logged class-and-tool check / all sampled | Any |
| Uploads to image tools from personal accounts on company devices | 0 for non-Public files (proposed) | Network gateway or browser extension logs joined to file class | Any |
| Jobs on approved tools run with public visibility or training on | 0 (proposed) | Upload log settings field, plus monthly spot check in each tool's gallery | Any |
| Approved tools whose terms were last checked over 90 days ago | 0 (proposed) | Approved tool list, date field | Any |
| Time from a bad upload to owner notice | Same business day (proposed) | Incident log timestamps | Over 1 business day |
| Public files blocked by the check (counter-metric) | Under 5% of blocks (proposed) | Monthly review of block log | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| An image or video tool upload from a company device with no upload log entry | Network gateway or browser extension log | A Public file sent through a tool that does not log |
| A file tagged Confidential or Client-owned appears in an upload to a tool not on its list | Upload log joined to file class | The tool was approved after the class list was last synced |
| A company product or client site appears in a tool's public gallery | Monthly search of public galleries for code names and client names | A public product launched earlier |
| An employee expenses a personal image tool plan | Expense reports | The plan is used only for Public files |

**Starter rule:** no file leaves for an outside image or video tool until its class is known and the tool, account tier and settings are approved for that class.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: confidential-files-uploaded-to-ai-image-tools
runs: [pre_upload, post_upload]
reads: [file.class, tool.id, account.tier, account.owner, job.visibility, job.training_setting, client_permission, people_permission]
trigger: file has no class, or class not allowed on tool/tier, or visibility public, or training on, or permission missing
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Use the approved company tool", "Use a placeholder instead of the file", "Something else"]
on_miss: block_upload_or_open_incident
metric: uncleared upload rate
counter_metric: public files blocked by the check
status: proposed
```

## 8. Related patterns
- [Shadow AI data exposure](../../../../../cross-cutting/security/goals/safety-security/failures/shadow-ai-exposure.md) - the closest existing page. It covers employees sending text and code to outside AI tools in general. This page covers image and video files sent as references or for edits, and the settings that are specific to image tools: public galleries, remixing and plan-gated private modes.
- [Samsung employees paste source code and meeting notes into ChatGPT](../../../../human-machine-interface/incidents/samsung-employees-paste-source-code-and-meeting-notes-into-chatgpt-april-2023.md) - the text incident that this page's risk is framed against.
- [User pasted someone else's personal data into a chatbot](../../../../human-machine-interface/goals/privacy-and-governance/failures/third-party-data-shared-by-users.md) - the bot side: what an assistant does with other people's data it receives. This page is about the file leaving the company.
- [Photo-upload deepfakes without a consent check](../../ai-deepfakes-of-real-people/failures/photo-upload-deepfakes-without-consent-check.md) - photos of real people uploaded to be changed; here the concern is the business's files, including photos of people, reaching outsiders.
- [AI image vendor indemnity gaps](../../ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md) - the other half of reading vendor terms: what the vendor covers on outputs.

## 9. Common questions
### Is it safe to upload confidential images to Midjourney?
Not on a default account. Its terms say content is "publicly viewable and remixable" by default, and private Stealth mode is only on Pro and Mega plans, and does not cover public Discord channels.

### Does ChatGPT train on images I upload?
OpenAI's help page says data sharing is on by default for personal Free, Plus and Pro workspaces and can be turned off, and that business workspaces are not used for training by default. The page talks about conversations and does not single out images.

### Does Adobe Firefly train on my content?
Adobe says it does not train Firefly on user content, and its terms say so, except for content submitted to Adobe Stock. That is Adobe's statement, read on October 29, 2026; we could not test it.

### Can I upload a client's photos or floor plans to an AI image tool?
Only with the client's written agreement for that named tool, on a company account with training off and private visibility. Whether your contract allows it is a question for your lawyer.

### Is turning on private mode enough?
No. Check old work too: on Midjourney, private mode does not make earlier public work private, and trashed work can still be found.
