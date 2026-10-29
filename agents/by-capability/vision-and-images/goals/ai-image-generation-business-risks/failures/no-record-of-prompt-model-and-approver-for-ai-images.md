# No Record of the Prompt, Model, Settings and Approver Behind a Published AI Image

<!-- SEO
title: No Record of the Prompt, Model and Approver Behind an AI Image
description: A business publishes an AI image or video and later cannot show the prompt, model, settings or who approved it. How an internal generation record fixes it.
search phrases:
- how to keep records of ai generated images
- audit trail for ai generated marketing content
- should we save prompts for ai images
- who approved this ai image
- ai content governance prompt log
- adobe firefly content logs prompt
- copyright office disclose ai generated content human contribution
- prove how an ai image was made
-->

**Frequency**: Unknown

## Issue: A business publishes an AI-made image or video, and when a complaint, a regulator, a copyright filing or a remake request arrives, nobody can show the prompt, the model and version, the settings, the inputs or the person who approved it. Write one generation record per published asset at the moment it is made, link it to the approval, and block publishing when the record is missing.

> **Read this first:** This page is design guidance for an internal record-keeping workflow. It is not legal advice. Statements about the US Copyright Office, regulators and disclosure duties summarize the opened sources as read on October 29, 2026. Whether a business must keep any record, for how long, and what a filing must say needs review by a qualified person.

> **One line:** A complaint says a store's AI-made holiday ad copies a rival's photo, legal asks "what did we type, into which tool, with which reference images, and who signed off?", and the answer is a designer's memory and a chat thread; the fix is a generation record written when the asset is made, tied to the approval, kept as long as the asset is live, and required before publishing.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Adobe's Content Logs cover image and video generations (section 4); the rules apply to any generator. |
| **Channel** | Ads, product pages, social posts, catalogs and reports that use images or video made or edited with a generator, by staff, agencies or freelancers |
| **Stakes** | Medium to High. With no record, the business cannot answer a likeness or copying complaint, fill in a copyright application's description of human versus AI work, decide disclosure, or remake an approved asset (sections 3 and 4). |
| **Who is affected** | Legal and compliance teams answering a complaint, the brand, the agency that made the asset, and anyone whose image or work the asset is said to copy |
| **Frequency** | Unknown. No opened source gives a rate. |
| **Pattern ID** | no-record-of-prompt-model-and-approver-for-ai-images |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unrecorded AI asset rate: published AI-made or AI-edited assets with no complete generation record (tool, model and version, prompt, settings, inputs, maker, approver, date) linked to the exact published file, divided by all published AI assets sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The gap is in the workflow around the model: who saves what, where, and for how long. A better generator does not record who approved its output. (Our judgment, not tested.) |
| **Also searched as** | AI image paper trail · prompt logging for marketing · AI asset provenance internal · who signed off on the AI ad · AI generation audit log |

Tests: [No record of prompt, model and approver for AI images test file](../../../tests/no-record-of-prompt-model-and-approver-for-ai-images.md).

## 1. In plain words
When a photographer shoots an ad, there is a shoot date, a contract, raw files and a sign-off email. When an AI tool makes the image, the "raw file" is a prompt typed into a browser tab, a model that may be retired next year, and a few reference images dragged in from a desktop. If nobody saves them when the image is made, they are gone. Months later someone asks how the image was made, and the business has only the final JPEG. This page is about the **internal** record the business keeps for itself. It is not about the public "made with AI" label inside the file, which is covered on [provenance metadata stripped](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-metadata-stripped.md).

## 2. What it looks like
The store, assets, people and IDs are invented. "Firefly" is named only as an example tool.

**Without the fix**
```
Legal:     A photographer in Ohio says our holiday banner HOL-22 copies her photo. What was the prompt?
Marketing: Priya made it in Firefly in October. She left in December.
Legal:     Which model? Did she upload any reference images? Who approved it?
Marketing: It was approved in a Slack thread, I think. The final PNG is in the shared drive.
Legal:     So we can't show whether her photo was an input.
           (The vendor's own log only keeps 90 days for a report, and only for saved cloud files.)
```
**With the fix**
```
Legal:     A photographer in Ohio says our holiday banner HOL-22 copies her photo. What was the prompt?
Asset tool: HOL-22 links to generation record GR-3381:
           Firefly Image (version as logged), prompt saved, seed not offered, 2 reference images:
           both from our own 2024 store shoot. Made by P. Shah, approved by J. Ortiz on Oct 14.
           1) Send the record to legal  2) Pause HOL-22 in all placements  3) Something else
Legal:     1 and 2.
Asset tool: Record sent. HOL-22 paused in 4 placements. Logged as complaint C-77.
```
In the fixed version the record was written when the image was made, so the answer is a lookup, not a memory test.

## 3. Why it happens
- **The record lives in the tool, not with the asset.** The prompt sits in a vendor's history page tied to one person's account. Adobe's enterprise Content Logs, for example, cover only outputs saved to Adobe Cloud storage, and the on-demand report covers the past 90 days (section 4). When the person leaves, the account closes or the window passes, the record is gone.
- **Approval and generation are separate systems.** The generation happens in the image tool; the sign-off happens in email, chat or a project board. Nothing ties the approved file to the prompt that made it, and an approved file can be re-edited after sign-off.
- **Nobody owns the record.** Agencies deliver a final file, not the inputs. Creative review checks how the asset looks, not whether its history is kept. The question "how was this made?" comes up only after something goes wrong.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Adobe added generative AI activity to its enterprise Content Logs: they "now capture the prompt and model name and version behind Firefly generative actions," with up to 2,000 characters of the prompt. It covers Firefly Web, Adobe Express and Firefly Workspace in Photoshop, "only outputs saved to Adobe Cloud storage." The on-demand report covers the past 90 days; streaming to a SIEM is offered. | [Adobe Community announcement, Aug. 27, 2026](https://community.adobe.com/announcements-623/now-available-genai-activity-visibility-in-content-logs-1639057). Opened and read. | Vendor announcement, one vendor. The post does not list an approver field, and we could not confirm user or date fields from it. Shows that vendors now log prompt and model, and where that log stops. |
| Content Credentials metadata "is cryptographically secure but easily stripped," and "it is still common for social media and content platforms to remove metadata." The post proposes watermarking and fingerprinting to recover it. | [Content Authenticity Initiative blog, John Collomosse, Jan. 22, 2026](https://contentauthenticity.org/blog/three-pillars-of-provenance). Opened and read. | Written by an Adobe researcher. About the label inside the file, not about an internal record; used here to show why the file alone is not a safe place to keep the record. |
| Google says its Content Credentials include "information about the creation process, the tools used, and edits," and that "C2PA doesn't guarantee the truthfulness of the assertions." | [Google Cloud, Content Credentials docs, updated Oct. 28, 2026](https://docs.cloud.google.com/vertex-ai/generative-ai/docs/content-credentials). Opened and read. | The page does not say the prompt is included. Vendor docs. |
| The US Copyright Office says applicants "have a duty to disclose the inclusion of AI-generated content in a work submitted for registration and to provide a brief explanation of the human author's contributions." Those who fail to correct the record after registration "risk losing the benefits of the registration." | [US Copyright Office, Registration Guidance, published March 16, 2023](https://www.copyright.gov/ai/ai_policy_guidance.pdf). Opened; text extracted from the PDF. | 2023 guidance; may have been updated. It does not require keeping prompts; we use it only to show that a business needs to know which parts were AI-made and which were human. Needs legal review. |
| At a Venable law firm event, Shahin Rothermel said regulators have moved from asking for search terms to asking "what were the prompts?" Justin Pierce advised tracking whether an asset came from a human, an AI system or both. | [Venable, Event in Review, Sept. 4, 2026](https://www.venable.com/insights/publications/2026/09/event-in-review-ai-for-marketing-and-brands). Opened and read. | Law firm event recap, not a regulator. It also warns that prompts can become evidence, so a record cuts both ways. |
| ContentGrip writes that "Approval alone is too thin" and lists a record of asset source, model or tool, human edits, reference inputs, rights status, disclosure decision, reviewer name and approval rationale. | [ContentGrip, Kai Indra, July 10, 2026](https://www.contentgrip.com/ai-creative-provenance/). Opened and read. | Trade blog opinion. Its survey numbers come from other reports we did not open; not used. |
| Huffer, a New Zealand clothing brand accused of AI-recreating models, said a forensic investigation found "no evidence" its agency used the models' images "as prompts, inputs or reference material." It had not released the report or named the investigator. | [1News, July 4, 2026](https://www.1news.co.nz/2026/07/04/huffer-says-probe-found-no-evidence-of-ai-model-recreation-claims/). Opened and read. | Non-US. The article does not say whether Huffer had generation records. Shows the question a record answers, not that a record was missing. |

**Weak evidence: vendor docs and advice only, no incident.** We found no public case where a business was harmed because it could not show the prompt, model or approver behind an AI asset. Searches run: "brand could not prove how AI-generated ad image was made prompt record audit trail"; "Copyright Office registration guidance AI-generated material disclose human authorship"; "C2PA content credentials actions digitalSourceType trainedAlgorithmicMedia softwareAgent manifest fields". An eMarketer article titled "Midjourney's Hollywood fight shows why creative brands need an AI paper trail" returned 403 and was seen only in search results; not used. A search summary said the C2PA 2.4 spec has an AI disclosure assertion with model information; read through a summary only, not used in the fix.

## 5. The fix
**The principle:** Every published AI asset can answer "what made this, from what, and who said yes?" from a record the business owns.

**Do this: brands, agencies and creative tools**
1. **Write a generation record when the asset is made.** Tool, model name and version, prompt and negative prompt, settings the tool shows (seed, guidance, aspect ratio, style preset), every input or reference image with its source, maker, and timestamp. Copy it out of the vendor's history into the business's own system the same day.
2. **Link the record to the exact published file.** Store a file hash with the record. A file whose hash matches no record is treated as unrecorded.
3. **Record human edits as their own steps.** Each retouch, composite or AI edit after generation adds a step with who did it. This is what tells legal which parts are human-made.
4. **Tie the approval to the record.** The approver's name, date and the record ID go in one log entry. An approval in chat with no record ID does not count. A file edited after approval needs a new approval.
5. **No record, no publish.** The publish step checks for a complete, linked record and approval. Agency and freelancer files arrive with their records, or they do not run.
6. **Keep records as long as the asset is live, plus a retention period set by legal.** Do not rely on a vendor's log window.
7. **Answer from the record, not from memory.** When asked how an asset was made, the tool shows the record or says "no record exists." It never reconstructs a prompt after the fact and presents it as the original.

**Reference design: generation record**
```yaml
generation_record:
  id: GR-3381
  asset: HOL-22
  file_sha256: "stored at export"
  tool: {name: Firefly, model: "name and version as logged", account: brand-enterprise}
  prompt: "cozy storefront at dusk, snow, warm window light, wreath on door"
  settings: {seed: not_offered, aspect_ratio: "16:9", style_preset: none}
  inputs: [{file: shoot-2024-117.jpg, source: own_shoot}, {file: shoot-2024-121.jpg, source: own_shoot}]
  human_edits: [{step: "added logo and price", by: p.shah, date: 2026-10-13}]
  made_by: p.shah
  approval: {by: j.ortiz, date: 2026-10-14, record_version: 2}
  retention: "live + period set by legal"
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | An asset has no record: say "no record exists for this file," never guess the prompt |
| Ask one clarifying question | An input image has no source: "Where did this reference image come from?" |
| Offer choices: 2-4 options plus "Something else", free text open | A complaint arrives on a recorded asset: send the record to legal, pause placements, something else. Do not offer choices when the record is complete and nothing is wrong. |
| Hand off to a person | Any complaint, regulator question or copyright filing that needs the record |

**Don't over-correct.** Do not log every draft and abandoned generation; record what is published and what it was made from. Do not block human-only assets for lacking an AI record. Do not paste the record into the public file or caption; the public label is a separate question. Do not keep prompts that contain personal data longer than legal allows. A missing seed on a tool that does not offer one is not an incomplete record.

**Hand-off rule.** Any complaint, regulator request or copyright filing about an AI asset goes to a named person in legal with the generation record, the approval entry and the list of live placements. If no record exists, legal is told that plainly on day one.

**Framework used:** none yet. Rule 3 follows the Copyright Office's request to describe human contributions; rule 6 follows the 90-day window in Adobe's post. The rest is our judgment from the sources in section 4.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/no-record-of-prompt-model-and-approver-for-ai-images.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Asset generated, maker closes the tab | Record with all fields exists in the business system | 1 |
| 2 | Published file re-exported with a new crop | Hash mismatch flagged; new record step or approval required | 2, 4 |
| 3 | Logo added after generation | Edit logged as a human step | 3 |
| 4 | Approval given in chat with no record ID | Publish blocked | 4, 5 |
| 5 | Agency file with no record | Publish blocked | 5 |
| 6 | Asset older than the vendor log window | Record still retrievable | 6 |
| 7 | "How was this made?" on an unrecorded file | Says no record exists; no guessed prompt | 7 |
| 8 | Human-only photo sent to publish | Not blocked | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unrecorded AI asset rate** (primary) | 0 (proposed) | Monthly sample of published AI assets: no complete linked record / all sampled | Any |
| Published files whose hash matches no record | 0 (proposed) | Placement export hashed and joined to records | Any |
| Approvals with no record ID | 0 (proposed) | Approval log scan | Any |
| Time to produce the record after a complaint | Under 1 business day (proposed) | Complaint timestamp to record sent | Over 2 business days |
| Human-only assets blocked as unrecorded (counter-metric) | Under 2% of blocks (proposed) | Block log, reviewed monthly | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A live AI-tagged asset has no record ID | Asset library joined to records | A human-only asset mis-tagged as AI |
| A record's approver field is blank or names the maker | Record store | A one-person team with a logged exception |
| A record's model field reads "unknown" | Record store | A tool that does not show its model, noted as such |
| The final file was modified after its approval date | File timestamps vs. approval log | A metadata-only change, such as renaming |
| Legal asks the creative team "how was this made?" in a ticket | Legal ticket text | A routine copyright filing that already has the record |

**Starter rule:** no AI-made or AI-edited asset publishes unless its file hash matches a complete generation record with a named approver who is not the maker.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-record-of-prompt-model-and-approver-for-ai-images
runs: [on_generate, pre_publish, on_complaint]
reads: [generation_record, approval_log, file_hash, placements]
trigger: AI asset with no record, hash mismatch, approval without record ID, or a request for how an asset was made
moves: [admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["Send the record to legal", "Pause in all placements", "Something else"]
on_miss: block_publish_or_report_no_record
metric: unrecorded AI asset rate
counter_metric: human-only assets blocked as unrecorded
status: proposed
```

## 8. Related patterns
- [Provenance metadata stripped](../../../../human-machine-interface/goals/ai-slop-detection/failures/provenance-metadata-stripped.md) - the closest existing page. It covers the public label inside the file (C2PA, IPTC) that platforms strip. This page covers the business's own internal record of prompt, model, settings and approver, which never leaves the company and does not depend on the file.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the approval step; this page makes that approval traceable.
- [AI-generated people that resemble real people](./ai-generated-people-resemble-real-people-without-release.md) - uses a source record for AI people; this page makes that record the rule for every AI asset.
- [Who owns AI-generated images](../../ai-image-copyright-and-trademark/failures/who-owns-ai-generated-images-copyright.md) - why the human-edit steps in rule 3 matter.
- [Governance](../../../../../cross-cutting/governance/goals/governance/README.md) - who owns the records and how long they are kept.

## 9. Common questions
### Do we have to save the prompts for AI images?
No opened source says a business must. The Copyright Office asks applicants to describe human versus AI work, and a Venable speaker said regulators now ask "what were the prompts?" Ask counsel about your own duty and retention.

### Isn't the vendor's history enough?
Usually not. Adobe's Content Logs keep prompt and model for saved cloud files, with a 90-day on-demand report, and the post lists no approver field. Copy the record into your own system.

### Doesn't Content Credentials already record this?
It records some creation details inside the file, but it is "easily stripped," and Google's docs do not say the prompt is included. Keep your own record too.

### Could keeping prompts hurt us?
Venable notes prompts can become evidence. That is a reason to write careful prompts and set retention with legal, not to keep no record.
