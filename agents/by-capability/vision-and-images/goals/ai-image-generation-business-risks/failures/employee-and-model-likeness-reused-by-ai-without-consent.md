# AI Images of Models and Employees Without Consent: When a Brand Reuses a Likeness Beyond the Release

<!-- SEO
title: AI Images of Models and Employees Without Consent: Likeness Reused Beyond the Release
description: A brand feeds photos of its own models or staff into AI tools and publishes poses or faces they never agreed to. How a scope record and edit gate stop it.
search phrases:
- brand used ai to change my photos model consent
- can a company use my photo for ai after i leave
- model sues brand ai generated images
- rainbow shops ai model lawsuit
- model release ai generated images clause
- digital twin model consent contract
- ai altered employee photo in ad
- california ab 2602 digital replica contract
-->

**Frequency**: Occasional

## Issue: A brand puts photos of its own models or employees into AI image or video tools and publishes new poses, scenes, bodies or faces the person never agreed to, often after the contract or job ended. Record what each person agreed to, classify every AI edit of their photos, block edits beyond that scope, and pull live assets when the scope ends.

> **Read this first:** This page is design guidance for a content workflow. It is not legal advice. Every legal statement below is what the cited source says, read on October 29, 2026. Lawsuits and complaints named here are allegations: no court has found that any brand named here broke a law or a contract, and the brands deny wrongdoing or have not commented. Several cases are outside the US and are marked as such. Whether a given release covers a given AI edit is for a qualified lawyer to decide.

> **One line:** A retailer that shot a model in a skirt against a white background later uses an AI tool to put "her" on a barstool in a pose she never struck, or an ad platform's AI feature reworks a hired athlete's face, or a former social media employee finds her old video still in a new ad with different eyes; the fix is a likeness scope record per person, an edit-level tag on every AI job that uses their photos, a gate that blocks anything beyond the recorded scope, platform AI edits off for assets with people, and a pull list when the term ends.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Every opened incident is a still image. Video is in scope because the Rainbow license covered "photographs and videos," H&M's planned digital twins are avatars, and California's statute covers audiovisual works (section 4). |
| **Channel** | E-commerce product shots, social ads, store windows, newsletters and brand video made from a company's own shoot library, employee-made content, and ad platform AI enhancements |
| **Stakes** | High. The person sees a version of themselves they never agreed to, sometimes sexualized or with a changed skin tone; the brand faces claims, takedowns and a public story about how it treats the people it hires. |
| **Who is affected** | Hired models, employees and former employees shown in company content, their agencies, and the brand and its creative and media teams |
| **Frequency** | Occasional, by our reading: opened sources report five cases between May and October 2026 (US, US/Meta, New Zealand, Australia, England). No rate found. |
| **Pattern ID** | employee-and-model-likeness-reused-by-ai-without-consent |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | AI images and video a business publishes show only what its real products, events and results deliver, carry the labels and records the business needs, and do not expose the business to legal or reputational harm. |
| **Primary metric** | Out-of-scope likeness rate: live AI-made or AI-edited assets showing an identifiable model or employee whose edit level, channel or date falls outside that person's recorded scope, divided by all sampled live assets showing a recorded person. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A better model keeps a face more recognizable in a new pose, which makes the problem worse. What the person agreed to is a contract fact the tool cannot see. (Our judgment, not tested.) |
| **Also searched as** | AI doppelganger of model · brand AI clone of me · model release AI clause · employee image rights after leaving · AI lightened model skin ad |

Tests: [employee and model likeness reused by AI test file](../../../tests/employee-and-model-likeness-reused-by-ai-without-consent.md).

## 1. In plain words
A store hires a model for a product shoot. Her contract lets the store use those photos and make small edits. Months later, the content team runs the photos through an AI tool to make new poses and new settings, because it is cheaper than another shoot. The new images still look like her. Nobody checked what she agreed to, and nobody pulled the images when her contract ended. The same happens to staff who appear in company videos and to people in vendor photos that an ad platform's AI quietly reworks.

## 2. What it looks like
The brand, people and asset IDs are invented. The edit levels are the ones in section 5.

**Without the fix**
```
Designer:    Need 12 summer looks by Friday. No shoot budget.
Image tool:  Loaded 40 photos from shoot "Spring-24 / Dana R." Generating new poses and beach scenes.
Designer:    Great, these look like her. Push to the site and the Instagram ads.
             (Two months later, an email from Dana's agency)
Agency:      "Dana's term ended in March and she never posed on a beach. Why is she in your ads?"
Designer:    "We just edited the photos we already had."
```
**With the fix**
```
Designer:    Need 12 summer looks by Friday. No shoot budget.
Image tool:  These 40 photos show Dana R. (talent ID T-218). Her scope record, reviewed 2026-04-02:
             allowed L0 retouch and L1 background swap, site only, until 2026-12-31.
             New poses and beach scenes are L2 (new depiction). Not in her scope. Blocked.
             1) Background swap only (L1), site only  2) Request L2 consent from her agency  3) Something else
Designer:    2.
Image tool:  Request sent to Dana's agency with the 12 briefs. Job held. Gate log LG-0412 saved.
```
In the fixed version the tool reads who is in the photos, names the edit level, says what the record allows, and offers a path that stays inside it.

## 3. Why it happens
- **Releases were written for retouching, not generation.** Loeb & Loeb notes that talent licenses often allow edits but "rarely contemplate" making new depictions that keep a person's face. The team reads "may edit" as "may generate."
- **The shoot library loses who is in it.** Photos move into an AI tool as files with no talent ID, term or scope attached, so the person's limits never reach the person running the job. Former employees' content stays in the library after they leave.
- **Edits happen outside the team.** REI said a Meta AI tool it was "auto-enrolled" in altered a vendor image; the model in that photo said she was hired for an official shoot (section 4). Nobody on the brand's side made a likeness decision at all.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Model Francheska Pujols sued Rainbow in New York state court, alleging it exceeded a license for "specified photographs and videos" by using "AI-generated, AI-assisted, synthetic, derivative, composited or materially altered images" in poses and settings she never authorized. Claims: New York Civil Rights Law Sections 50 and 51, Lanham Act Section 43(a), unfair competition and defamation. The firm says talent agreements "were never drafted to address" this and that the case "remains at its earliest stages." | [Loeb & Loeb, Brian L. Heidelberger, July 22, 2026](https://www.loeb.com/fr/insights/passle/2026/07/when-does-an-ai-alteration-become-a-new-depiction-rainbow-usa-lawsuit-highlights-risks-for-talent-li). Opened and read. | Law-firm summary of a complaint; allegations, not findings. We did not open the complaint. |
| Per the New York Post as reported by PetaPixel, the contract allowed "minor edits" but not entirely new images; Pujols sent a cease and desist in March when it expired. Rainbow said: "we used our images properly and there's no violation of her rights." | [PetaPixel, Matt Growcoot, June 1, 2026](https://petapixel.com/2026/06/01/model-sues-fashion-brand-after-it-ai-generated-pictures-of-her/). Opened and read. | Secondary report of another outlet; we did not open the New York Post. |
| Pujols withdrew on May 29 to seek a private settlement and refiled on June 15. Rainbow's studio manager had emailed models in June 2025 that it was "generating avatars, with the assistance of AI." Rainbow's chief digital officer said it "has acted appropriately and in accordance with its commitments, including contracts signed by models." | [PetaPixel, Pesala Bandara, June 24, 2026](https://petapixel.com/2026/06/24/models-claim-fashion-brand-used-ai-to-create-their-doppelgangers/). Opened and read. | Relays Business Insider reporting, which we did not open. |
| REI's ad was altered by a Meta AI tool REI said it was "auto-enrolled" in. Fitness model Amity Rockwell said the woman in the ad was generated from her likeness: "this was an official shoot. That I got hired for." Van Rysel confirmed the original came from its shoot with her. | [TechSpot, Rob Thubron, June 25, 2026](https://www.techspot.com/news/112895-rei-pulls-ai-generated-bike-ad-after-meta.html). Opened and read. | News report. Rockwell's post was not opened. The edit was the platform's, per REI. |
| New Zealand brand Huffer was accused of AI images resembling former models "without their knowledge or consent." Model Akshay Raju said that, as far as he was aware, his agency contract required AI use to be disclosed. Huffer's managing director declined to answer directly. | [1News, Ed O'Driscoll, June 2026](https://www.1news.co.nz/2026/06/08/huffer-accused-of-using-ai-to-recreate-real-models-without-permission/). Opened and read. | Non-US. Accusations; the brand did not confirm AI use. |
| Model Elii Emeghebo filed a complaint with the Australian Human Rights Commission alleging retailer Peter Jackson made an AI version of him with lightened skin and eyes; his contract allowed original photos on digital platforms only. The company acknowledged "AI-assisted tools" and denied race played any role. | [Black Enterprise, Sidnee Michelle, July 4, 2026](https://www.blackenterprise.com/nigerian-australian-model-ai-lightened-skin-eyes/). Opened and read. | Non-US. A complaint, not a finding. Relays an Australian outlet we did not open. |
| A former employee in England said her ex-employer used a still from a video she made on the job in an AI-altered ad after she left: "my eyes are a different colour and tattoos are gone." | [The Cool Down, Oct. 14, 2026](https://www.thecooldown.com/?p=808435). Opened and read. | Non-US, single source, based on a social media post; no company named. |
| H&M told CNN it plans 30 "digital twins" of its models; models "would own the rights to their digital twin." Model Alliance's Sara Ziff said it "raises critical questions about consent and compensation." | [ABC30 / CNN, Issy Ronald, April 1, 2025](https://abc30.com/amp/post/fashion-giant-hm-plans-use-ai-clones-human-models-not-everyone-is-happy/16115370/). Opened and read. | A plan, not an incident. Shows the consented version of the same practice. |
| California Labor Code 927: a services contract term allowing a "digital replica" in place of work the person would have done in person is unenforceable for new performances fixed on or after January 1, 2025, if it lacks "a reasonably specific description of the intended uses" and the person had no qualifying lawyer or union representation. | [California Legislative Information, Lab. Code 927](https://leginfo.legislature.ca.gov/faces/codes_displaySection.xhtml?lawCode=LAB&sectionNum=927.). Opened and read. | Statute text; exceptions apply (927(a)(2)(B)). Applies to California contracts only. |
| New York's Fashion Workers Act took effect June 19, 2025. For future use of a model's image, the management company must get written consent, separate from the representation agreement, detailing "the creation, use, duration, scope and rate" of a digital replica. | [Polsinelli, Tina Tellado and Emily C. Heimbecker, Jan. 14, 2025](https://www.polsinelli.com/polsinelli-at-work/new-york-states-fashion-workers-act-effective-summer-2025). Opened through a fetch tool. | Law-firm summary; the statute was not opened. It puts the duty on management companies; what it requires of brands is for counsel. |

**Not used in the fix.** Search summaries mentioned a Chinese company making an AI avatar of a former HR employee and a Polish review saying consent to image use does not end automatically with employment. We could not open these in a usable form, so they are not stated as fact here.

## 5. The fix
**The principle:** No AI job may change a recorded person's photo beyond the edit level, channels and dates that person agreed to, and the record shows the check.

**Do this: brands, content teams and image tools**
1. **Keep a likeness scope record per person.** Talent ID, source shoots or videos, allowed edit levels, channels, markets, start and end date, pay terms for AI use, contact (agency or the person), signed document link, reviewer and review date. Employees get their own record, separate from the job offer.
2. **Tag people at intake.** Every shoot and every employee-made asset carries the talent IDs of everyone identifiable in it. An untagged asset showing a person cannot go into an AI job.
3. **Classify every AI job by edit level.** L0: retouch, color, crop. L1: background, garment or prop swap with the same pose and face. L2: new pose, body, scene, expression or changed facial features or skin tone (a new depiction). L3: digital twin, animation into video, or voice. Unknown counts as L3.
4. **Gate the job against the record.** Each person in the inputs must allow the job's level, channel and date. Otherwise the job is blocked and the tool offers what the record does allow.
5. **Turn platform AI edits off for assets with people.** Ad platform enhancements that can change a person stay off unless the record allows L2. Recheck each ad, not only the account default.
6. **Ask before going beyond scope.** A request for a higher level goes to the contact on the record with the briefs, the channels and the pay offer. No answer means no.
7. **Pull on end.** When a term ends, an employee leaves, or a person withdraws consent, list every live asset showing them at L1 or above and pull or replace it by the date counsel sets.
8. **Log every gate decision.** Job ID, inputs, talent IDs, edit level, channels, record version, outcome, decided by, date.

**Reference design: scope record and gate log**
```yaml
likeness_scope:
  talent_id: T-218
  person: "Dana R. (via agency)"
  sources: [shoot Spring-24]
  allowed_levels: [L0, L1]          # L2 new depiction and L3 twin/video not allowed
  channels: [own_site]
  term: {start: 2026-01-15, end: 2026-12-31}
  ai_pay_terms: none
  document: contracts/T-218-release.pdf
  reviewed: {by: M. Chen, on: 2026-04-02}
gate_log:
  id: LG-0412
  job: summer-looks-12
  talent: [T-218]
  level: L2
  channels: [own_site, instagram_ads]
  outcome: blocked_out_of_scope
  next: consent_request_sent
  decided_by: tool
  date: 2026-10-26
```

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | A job is beyond scope: stay within the allowed level, request consent, something else |
| Ask one clarifying question | An input shows a person with no talent ID: "Who is this, and do we have their record?" |
| Admit uncertainty and show how to check | The edit level is unclear: treat it as L3 and say why |
| Hand off to a person | A record is missing, expired, or the person has withdrawn consent |

**Don't over-correct.** An L0 retouch of a recorded person in an allowed channel and term is a pass; do not hold it "to be safe." Do not block AI jobs on product-only shots or on fully synthetic people with no source photo of a real person (resemblance to someone real is covered by [AI-generated people who resemble real people](./ai-generated-people-resemble-real-people-without-release.md)). Do not delete a person's real photos when their AI scope ends; pull only what the record says.

**Hand-off rule.** Any missing, expired or withdrawn record, or an untagged person, goes to the record owner with the job, the inputs and the requested level. The job stays held until the owner logs a decision; other jobs proceed.

**Framework used:** none yet. The edit levels follow the line the Rainbow complaint draws between modifying licensed images and making new depictions (Loeb & Loeb), and rule 1's fields echo the "creation, use, duration, scope and rate" items in Polsinelli's summary of New York's act. The rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/employee-and-model-likeness-reused-by-ai-without-consent.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | New-pose job on a model whose record allows L0-L1 | Blocked; L1 option offered | 3, 4 |
| 2 | Asset with an untagged person sent to an AI job | Blocked until tagged | 2 |
| 3 | Platform enhancements on for an ad with a person | Flagged and turned off | 5 |
| 4 | Former employee's video still used in a new AI ad | Blocked; record shows ended | 1, 4 |
| 5 | Term ends with assets live | Pull list made with every L1+ asset | 7 |
| 6 | Unclear edit level | Treated as L3 | 3 |
| 7 | Consent request unanswered | Job stays held | 6 |
| 8 | Allowed L0 retouch in term | Passes, no hold | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Out-of-scope likeness rate** (primary) | 0 (proposed) | Monthly sample of live assets showing recorded people: level, channel or date outside record / all sampled | Any |
| AI jobs on people with no talent ID | 0 (proposed) | Gate log: jobs whose inputs had an untagged face | Any |
| Live assets of people past term | 0 (proposed) | Scope records joined to live asset index | Any |
| Ads with people and platform AI edits on | 0 (proposed) | Ad account export per ad | Any |
| Days from term end to assets pulled | Within counsel's date (proposed) | End date to pull log | Past counsel's date |
| Allowed jobs wrongly held (counter-metric) | Under 5% of holds (proposed) | Monthly review of holds | Over 15% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| An image-to-image or video job uses shoot photos of a person and changes pose or scene | AI tool job log | The record allows L2 for that channel |
| A face in a new asset matches a talent ID whose term has ended | Asset index joined to scope records | A real photo from inside the term, still allowed |
| A model, agency or ex-employee emails about an image they "never posed for" | Talent and legal inbox | A real outtake from the shoot they forgot |
| Shoot bookings for a model stop while new assets showing a similar face keep appearing | Booking system and asset index | A different model with a similar look |
| An ad with a person runs with platform AI enhancements on | Ad account export | Enhancements limited to text or cropping |

**Starter rule:** no AI job may change a recorded person's photo or video beyond the edit level, channel and term in that person's scope record.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: employee-and-model-likeness-reused-by-ai-without-consent
runs: [pre_job, pre_launch, on_term_end]
reads: [inputs.talent_ids, job.edit_level, job.channels, scope.records, ad.platform_enhancements]
trigger: untagged person, level or channel beyond scope, expired or withdrawn record, platform AI edit on a person
moves: [offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Stay within the allowed edit level", "Request consent from the person", "Something else"]
on_miss: block_job_and_hold_assets
metric: out-of-scope likeness rate
counter_metric: allowed jobs wrongly held
status: proposed
```

## 8. Related patterns
- [Uploaded photos edited with no consent check](../../ai-deepfakes-of-real-people/failures/photo-upload-deepfakes-without-consent-check.md) - the closest page. It covers a tool editing any uploaded photo of a real person with no consent check. This page is about a business that holds a real release and uses its own people's photos beyond it.
- [AI-generated people who resemble real people](./ai-generated-people-resemble-real-people-without-release.md) - a synthetic person who turns out to look like someone real, with no release at all; here the person is known, signed a release, and the AI use goes beyond it.
- [Deepfake celebrity endorsement ads](../../ai-deepfakes-of-real-people/failures/deepfake-celebrity-endorsement-ads.md) - a stranger's likeness with no agreement at all; here an agreement exists and its scope is exceeded.
- [AI ads backlash for replacing artists with AI](./ai-ads-backlash-for-replacing-artists-with-ai.md) - the public reaction to AI models taking jobs; this page is about the person whose own face was reused.
- [AI images in ads published without review](./ai-images-in-ads-published-without-review.md) - also uses the REI case, for the product error and approval; this page uses the model's side of it.
- [Confidential files uploaded to AI image tools](./confidential-files-uploaded-to-ai-image-tools.md) - its rule 6 asks for permission before uploading photos of people; this page defines what that permission covers.
- [Consistency failure: identity loss across generations](../../generation-artifacts/failures/consistency-failure.md) - why a reused face may drift; not a consent question.
- [Governance](../../../../../cross-cutting/governance/goals/governance/README.md) - ownership of shared records.

## 9. Common questions
### Can a brand use AI to change my modeling photos?
It depends on your contract. In the Rainbow case the model alleges her license allowed edits but not new depictions; the brand denies wrongdoing. Ask a lawyer to read your release.

### Can my company use my photo or video in AI ads after I leave?
Opened sources do not settle this. One former employee in England reported it happening. Check your employment contract and any image policy, and ask a lawyer.

### Does California limit digital replica clauses?
Labor Code 927 makes some digital replica terms in services contracts unenforceable for new performances fixed on or after January 1, 2025, when the uses are not reasonably specific and the person had no qualifying lawyer or union. Counsel decides how it applies.

### What should a model release say about AI?
Name the edit levels allowed, the channels, the term, the pay for AI use and how to withdraw. Have counsel write it.
