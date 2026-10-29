# AI-Generated Models That Look Like Real People: No Release, No Record, No Check

<!-- SEO
title: AI-Generated Model Looks Like a Real Person: Likeness Risk in Ads
description: A business runs an AI-made person in an ad, the face looks like a real person, and there is no release or record. How a pre-publish check stops it.
search phrases:
- ai generated model looks like a real person
- can i be sued if my ai model looks like someone
- do ai generated people need a model release
- ai model resembles celebrity in ad
- shein ai model looks like luigi mangione
- ai fashion model looks like real model lawsuit
- right of publicity ai generated person
- does adobe firefly indemnity cover publicity rights
-->

**Frequency**: Unknown

## Issue: A business publishes an AI-generated "synthetic" person in an ad or product shot on the belief that nobody real needs to sign a release, and the face turns out to look like a real, identifiable person. Before an AI-made person goes out, save the prompt and inputs, run a blind resemblance check, stop any match and send it to legal, and pull the asset fast when someone says "that's me."

> **Read this first:** This page is design guidance for a review workflow. It is not legal advice. Statements about likeness, publicity rights, consent and vendor indemnity summarize the cited news reports and vendor pages as read on October 29, 2026. Lawsuits and complaints named here are allegations, not findings. Whether a given image infringes anyone's rights is for a qualified lawyer to decide.

> **One line:** A marketing team runs an AI-made hiker in a paid ad, believing "she isn't real, so there's nobody to get a release from," and nine days later commenters name the local TV anchor she looks like; nobody saved the prompt or the reference images, so nobody can show how the face was made. The fix is a source record for every AI-made person, a blind resemblance review before publishing, a hold and legal route on any named match, and a same-day takedown path.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The Shein, Life8 and Huffer reports are still images; the Lisa AI ad that used Scarlett Johansson's likeness was a video (section 4). |
| **Channel** | Ads, product listings, catalogs and social posts that show an AI-generated person, including images supplied by agencies and marketplace sellers |
| **Stakes** | High. The person who resembles the image may claim publicity or portrait rights; the business pulls the asset and apologizes in public (Shein, Life8, Huffer in section 4). |
| **Who is affected** | The real person the face resembles, the brand that published it, and the agency or seller that made it |
| **Frequency** | Unknown. No opened source gives a rate. We found no public case where an accidental resemblance was confirmed; in the cases we read, how the face was made was disputed or unknown. |
| **Pattern ID** | ai-generated-people-resemble-real-people-without-release |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Unchecked synthetic-person publish rate: published assets showing an AI-generated person with no logged source record and resemblance review, divided by all published assets showing an AI-generated person. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Whether a face looks like a real person is a fact about the world, not the image, and Adobe's FAQ says outputs are not guaranteed to be unique. It needs a record and a human check. (Our judgment, not tested.) |
| **Also searched as** | AI model resembles real person · synthetic model likeness rights · AI influencer looks like celebrity · do I need a release for an AI person · AI face matches real model |

Tests: [AI-generated people resemble real people without release test file](../../../tests/ai-generated-people-resemble-real-people-without-release.md).

## 1. In plain words
Brands use AI-made people because they skip the shoot and the release. The release exists to prove the person shown agreed. With an AI person, the team assumes no one exists to agree. But a generated face can still look like someone real: a celebrity, a former model, a local anchor. When that person or their fans notice, the brand has no release and often no record of how the face was made, so it cannot show the likeness was not copied. This differs from [deepfake celebrity endorsement ads](../../ai-deepfakes-of-real-people/failures/deepfake-celebrity-endorsement-ads.md), where a scammer names a celebrity on purpose. Here the business meant to show nobody, and the risk comes from not checking.

## 2. What it looks like
The brand, assets, reviewers and IDs are invented. "Firefly" is named only as an example tool.

**Without the fix**
```
Designer:  Final for the Denver trailhead ad: AI hiker, asset SUMMIT-04. Push to Meta and the billboard vendor.
Ad tool:   Exported 3 sizes. Scheduled on Meta for Monday; billboard file sent.
           (Nine days later, a comment on the ad)
Commenter: "Why is the Channel 9 weather anchor in a boot ad? Did she sign with you?"
Marketing: "She isn't real, she's AI. There's nobody to get a release from."
Legal:     "Then show me the prompt and the reference images." Nobody saved them.
```
**With the fix**
```
Designer:  Final for the Denver trailhead ad: AI hiker, asset SUMMIT-04. Push to Meta and the billboard vendor.
Ad tool:   SUMMIT-04 shows an AI-generated person. Before I schedule:
           Source record: Firefly, prompt saved, no names in prompt, no reference photos. Pass.
           Blind review: 1 of 3 reviewers wrote "looks like the Channel 9 weather anchor." Held.
           1) Make a new face and review again  2) Send to legal with the record  3) Something else
Designer:  1.
Ad tool:   SUMMIT-05 made. Blind review: 0 of 3 named anyone. Logged RL-118 with prompt, model, reviewers. Scheduled.
```
In the fixed version the source is recorded before review, one named match holds the asset, and the new face is reviewed again before it runs.

## 3. Why it happens
- **"No real person, no release" is taken as settled.** The release step is skipped for AI people. A disclaimer is used in its place: the Lisa AI ad that featured Johansson's likeness said "It has nothing to do with this person" (section 4). Nightjar, a vendor that sells AI models, writes that calling an image AI-generated "does not supply consent."
- **Nobody can say how the face was made.** Agencies, freelancers and marketplace sellers make the image; the brand gets a file. Shein said the image "was provided by a third-party vendor," and Huffer had to commission a forensic probe to answer whether models' photos were used as inputs.
- **Nobody looks for a resemblance before launch.** Creative review checks the product, the copy and the hands. No step asks "does anyone recognize this person?" The public asks it first.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Shein removed a men's shirt listing that used an image of a man resembling Luigi Mangione. Shein: "The image in question was provided by a third-party vendor and was removed immediately upon discovery," and it would "take appropriate action against the vendor in line with our policies." How the image was made was unclear; social media users speculated it was AI-generated. | [Yahoo News / Nexstar (WPIX), Sept. 3, 2025](https://www.yahoo.com/news/articles/shein-taking-action-against-vendor-171751279.html). Opened and read. | Not shown to be AI-made or accidental. Decrypt's report that a researcher called it a likely Midjourney image and that face matching confirmed it returned 403 and was seen only in a search summary; not used. |
| Life8, a Taiwanese fashion brand, used AI-generated ad images that "closely resembled a real male model," including tattoos and eye shape. "The model alleged violation of his portrait rights and professional harm." Life8 apologized, removed the images and started talks. | [OECD AI Incidents Monitor, 2026-07-18](https://oecd.ai/en/incidents/2026-07-18-2fa7). Opened and read. | Non-US (Taiwan). An aggregator summary; the Chinese-language news originals were not opened. The page does not say whether the copying was deliberate. |
| Models said Huffer, a New Zealand clothing brand, ran AI campaign images resembling them. Elijah Timmins-Scanlon: "As I zoomed in, it wasn't me." Akshay Raju: "It kind of looks like a hybrid between me, Elijah and a few other people." The managing director declined to say directly whether real models' images were used. | [1News, June 2026](https://www.1news.co.nz/2026/06/05/huffer-accused-of-using-ai-to-recreate-real-models-without-permission/). Opened and read. | Non-US (New Zealand). Allegations by the models. |
| Huffer said an "independent forensic investigation" it commissioned found "no evidence" that it or its agency used models' photos "as prompts, inputs or reference material." It said: "Aspects of our public response fell short of the standard we expect of ourselves, and for that we are genuinely sorry." | [1News, July 4, 2026](https://1news.co.nz/2026/07/04/huffer-says-probe-found-no-evidence-of-ai-model-recreation-claims). Opened and read. | The company's own claim; the investigator was not named and the report had not been released. If true, this is the closest case we found to an accidental resemblance. |
| A 22-second ad for the Lisa AI app showed real footage of Scarlett Johansson, then AI images resembling her with an imitated voice. Disclaimer: "Images produced by Lisa AI. It has nothing to do with this person." Her attorney: "we will deal with it with all legal remedies that we will have." | [Variety Australia, Nov. 2, 2023](https://au.variety.com/2023/digital/news/scarlett-johansson-legal-action-ai-app-likeness-11749/); [AV Club, Nov. 1, 2023](https://avclub.com/scarlett-johansson-sues-ai-app-over-use-of-likeness-1850983316). Both opened and read. | Deliberate use, not accidental. AV Club says she is suing; Variety's text reports only stated intent. Used here only to show a disclaimer standing in for consent. |
| Adobe's Firefly enterprise indemnity covers claims that output infringes "patent, copyright, trademark, publicity rights or privacy rights," for customers with "the appropriate entitlement." It excludes claims arising from "your modification of the Firefly output," "the context in which you use the Firefly output" and other customer actions. Outputs "are not guaranteed to be exclusive or unique." | [Adobe, Firefly Legal FAQs for Enterprise Customers (2024-06-11 file)](https://www.adobe.com/cc-shared/assets/pdf/enterprise/firefly-legal-faqs-enterprise-customers-2024-06-11.pdf). Opened; text extracted from the PDF. | Vendor FAQ from 2024; may be outdated. One vendor only. Whether "context" excludes an ad use is a contract question. |
| "Yes, you can be sued, but a resemblance alone is not automatically unlawful." Risk rises when a real person is recognizable and used commercially without consent. It advises a blind recognition check before publishing and keeping source, consent and generation records together. | [Nightjar Help Center, Dec. 9, 2025, reviewed Aug. 19, 2026](https://nightjar.so/help-desk/can-i-be-sued-if-my-ai-fashion-model-resembles-a-celebrity-or-influencer). Opened and read. | Vendor content from a seller of AI models; not legal analysis. |

**No public case of accidental resemblance found.** We found no case where a court or an independent party confirmed that a business's AI-made person matched a real person by accident. Searches run: "AI-generated model in ad looks like real person lawsuit accidental resemblance"; "Getty Images generative AI terms people likeness model release indemnification"; "Shutterstock Adobe Stock AI-generated images people model release resemble real person policy"; "Shein removed shirt AI model resembling Luigi Mangione third-party vendor statement"; "Shutterstock AI image generator terms indemnification likeness people generated". The risk on this page rests on the disputed cases and vendor documents above.

**Not used in the fix.** A search summary said Adobe Stock requires a model release for AI content based on an identifiable person and a "fictional" checkbox for AI people who only look real; the Adobe pages returned 403, so this is unverified. Summaries of Getty's "no name and likeness concerns" marketing and Shutterstock's 2023 indemnity were not opened in a form we could check. The Tom Hanks dental ad ([The Fader, Oct. 2, 2023](https://thefader.com/2023/10/02/tom-hanks-artificial-intelligence-dental-plan-ad), opened) is a deliberate fake and belongs to the deepfake page.

## 5. The fix
**The principle:** No AI-made person goes out until the business can show how the face was made and that reviewers who did not make it named nobody real.

**Do this: brands, agencies, marketplaces and creative tools**
1. **Tag every person in an asset at intake.** Real person with a release on file, real person AI-edited, or AI-generated person. "Unknown" blocks publishing.
2. **Keep a source record for every AI-generated person.** Tool, model version, account, prompt, seed if the tool shows one, every reference or input image, and who made it. An asset with no source record does not publish. Agencies and marketplace sellers deliver the record with the file.
3. **No real names or real faces as inputs without a release.** A prompt that names a real person, or a reference image of a real person, needs a release that covers AI use, or the asset is rejected. Brand-owned shoot photos count as real faces.
4. **Run a blind resemblance review before publishing.** At least three reviewers who did not make the asset see it without context and answer one question: "Does this person look like anyone you can name?" (Three is a starting point, not a sourced number.) Any face-matching tool is used only after counsel approves it.
5. **Any named match holds the asset.** One reviewer naming a specific real person holds it. The choices are: make a new face and review again, get a release from that person, or send to legal. A hold is never cleared by adding a disclaimer.
6. **A disclaimer is not a release.** Wording like "AI-generated, not a real person" may be needed for disclosure, but it never replaces rules 3 to 5.
7. **Record the tool's coverage.** Note whether the tool's indemnity names publicity or privacy claims and what it excludes, using the checklist on [AI image vendor indemnity gaps](../../ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md). "The vendor covers us" is not assumed.
8. **Take down fast on a resemblance complaint.** A message saying "that's me" or naming a real person pauses the asset in every placement within one business day (starting point), and legal gets the source record. Staff do not argue the point in public comments.
9. **Log every decision.** Asset, source record ID, reviewers and answers, outcome, decided by, date, and every placement where it ran.

**Reference design: source record and review log**
```yaml
source_record:
  id: SR-0412
  asset: SUMMIT-05
  person_type: ai_generated
  tool: {name: Firefly, model: "as shown in tool", account: brand-enterprise}
  prompt: "woman in her 30s hiking, red jacket, golden hour, Colorado trail"
  names_in_prompt: none
  reference_images: none
  made_by: designer@brand.example
  coverage_check: {publicity_claims_named: yes, checklist_version: 2026-10, read_on: 2026-10-01}
review_log:
  id: RL-118
  reviewers: [r1, r2, r3]        # not on the project
  answers: [no_one, no_one, no_one]
  outcome: pass
  decided_by: brand creative lead
  date: 2026-10-27
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A reviewer named a real person: new face, get a release, send to legal, something else |
| Ask one clarifying question | Person type is blank: "Is the person in this image real, AI-edited, or AI-generated?" |
| Admit uncertainty and show how to check | No source record: say "we cannot show how this face was made," not "it's AI, so it's fine" |
| Hand off to a person | A named match the team wants to keep, or any "that's me" complaint |

**Don't over-correct.** AI-made people are not banned; an asset with a full source record and a clean blind review runs. "She looks like someone" with no name is not a match. Do not run face searches on every image without counsel. Do not hold real-shoot photos with a release on file. Do not replace the review with a stock "not a real person" caption.

**Hand-off rule.** Every named match the team wants to keep, and every resemblance complaint, goes to a named person in legal with the asset, its source record, the review log and the list of live placements. Legal, not the tool or the designer, decides whether it runs again.

**Framework used:** none yet. Rules 4 and 9 follow Nightjar's advice (blind recognition check; keep source, consent and generation records together), a vendor source. The rest is our judgment from the cases in section 4.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-generated-people-resemble-real-people-without-release.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Asset with a person, person type blank | Blocked; one clarifying question | 1 |
| 2 | AI person from an agency with no source record | Blocked | 2 |
| 3 | Prompt names a celebrity, no release | Rejected | 3 |
| 4 | Clean asset sent to publish | Blind review runs first | 4 |
| 5 | One reviewer names a real person | Held with choices | 5 |
| 6 | Team adds "not a real person" caption to clear a hold | Still held | 6 |
| 7 | Tool coverage unknown | Recorded as unknown, not assumed | 7 |
| 8 | "That's me" message on a live ad | Paused everywhere within a business day; legal notified | 8 |
| 9 | Vague "looks like someone" with no name | Not held | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unchecked synthetic-person publish rate** (primary) | 0 (proposed) | Weekly sample of published assets with an AI person: no source record or no review log / all sampled | Any |
| Assets with a real name or face as input and no release | 0 (proposed) | Source records joined to the release register | Any |
| Time from resemblance complaint to pause in all placements | Under 1 business day (proposed) | Complaint timestamp to last placement paused | Over 2 business days |
| Named-match holds per 100 AI-person assets | Track; no target | Review log | A sudden rise for one tool or agency |
| Holds that legal cleared as no real resemblance (counter-metric) | Under 50% of holds (proposed) | Review log, monthly | Over 75% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Comments on a live ad name a real person ("is that [name]?") | Social comment export, search for "is that" plus a name | A joke about a generic look, with no consistent name |
| An AI-person asset has no source record ID | Asset library joined to source records | A real-shoot photo mis-tagged as AI |
| A prompt contains a capitalized full name | Source record text scan | A product or place name |
| The same AI face reused across many sellers' listings | Marketplace image hash report | A licensed stock asset sold to many sellers |
| A reviewer's answer names a person, but the asset was published | Review log joined to placements | Legal cleared it, with a logged decision |

**Starter rule:** no asset showing an AI-generated person is published without a source record and a blind review in which no reviewer named a real person.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-generated-people-resemble-real-people-without-release
runs: [pre_publish, on_complaint]
reads: [asset.person_type, source_record, review_log, release_register, placements]
trigger: person type unknown, no source record, real name or face as input without release, named match, or resemblance complaint
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Make a new face and review again", "Get a release from this person", "Send to legal", "Something else"]
on_miss: hold_asset_or_pause_all_placements
metric: unchecked synthetic-person publish rate
counter_metric: holds that legal cleared as no real resemblance
status: proposed
```

## 8. Related patterns
- [Deepfake celebrity endorsement ads](../../ai-deepfakes-of-real-people/failures/deepfake-celebrity-endorsement-ads.md) - the closest existing page. There, someone uses a named star on purpose and the fix sits in generators and ad platforms. Here, a business meant to show no real person, and the fix is its own source record and resemblance check.
- [Photo-upload deepfakes without a consent check](../../ai-deepfakes-of-real-people/failures/photo-upload-deepfakes-without-consent-check.md) - a real person's photo used as input; rule 3 here applies the same idea to brand assets.
- [AI image vendor indemnity gaps](../../ai-image-copyright-and-trademark/failures/ai-image-vendor-indemnity-gaps.md) - what vendor coverage includes; rule 7 links to it instead of repeating it.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - the approval step this check plugs into.
- [AI-generated ad disclosure rules not met](./ai-generated-ad-disclosure-rules-not-met.md) - labeling laws for AI people, which is a separate question from likeness.
- [Governance](../../../../../cross-cutting/governance/goals/governance/README.md) - ownership of release and source records.

## 9. Common questions
### Do AI-generated people need a model release?
No opened source gives a legal rule. The risk is that the face looks like someone real who never agreed. Keep a source record and run a resemblance check; ask counsel about releases.

### Can I be sued if my AI model looks like a real person?
Nightjar, a vendor, says yes, though resemblance alone is "not automatically unlawful." In the cases we read, Shein and Life8 removed the images, Life8 apologized, and Huffer apologized for its response. Ask a lawyer.

### Does a "not a real person" disclaimer protect us?
Not by itself. The Lisa AI ad carried one and still drew legal threats. Treat disclosure and consent as separate questions.

### Does my AI vendor's indemnity cover likeness claims?
Check your contract. Adobe's 2024 Firefly FAQ names publicity and privacy claims but excludes edits and "the context in which you use" the output.
