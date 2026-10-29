# AI Image Indemnification Gaps: Vendor Copyright Commitments That Do Not Cover How the Business Uses the Output

<!-- SEO
title: AI Image Indemnification: What Vendor Terms Really Cover
description: Businesses count on an AI vendor to defend them in a copyright claim without reading the conditions. A per-tool terms checklist, logged settings and a review route.
search phrases:
- ai image indemnification
- does microsoft copilot copyright commitment cover images
- customer copyright commitment required mitigations
- adobe firefly indemnification
- google generative ai indemnification imagen
- openai copyright shield chatgpt enterprise
- midjourney terms of service commercial use indemnify
- will my ai vendor defend me in a copyright lawsuit
-->

**Frequency**: Unknown

## Issue: Businesses count on an AI vendor to defend them in a copyright claim without reading the conditions. A per-tool terms checklist, logged settings and a review route close the gap.

> **Read this first:** Statements about contracts, indemnity, copyright and trademark on this page summarize vendor terms and pages **as read on 2026-10-29**. Vendor terms change, and some change without notice to the reader. This is not legal advice. It needs review by a qualified person, such as a lawyer who handles technology contracts, before anyone relies on it. Whether a given asset is covered depends on the full contract the business signed, which this page has not seen.

> **One line:** A marketing team hears "the vendor will defend us" and publishes AI images made on a plan, setting, model or edit path that the vendor's commitment does not cover, or on a tool whose terms put the risk on the user; the fix is a dated terms checklist per tool and tier, a record of which tool, tier and settings made each asset, and a rule that any use outside coverage goes to legal review before it ships.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. Google's indemnified list names Imagen and Veo; Microsoft's required-mitigations page has an image generation row; Adobe's FAQ covers features "that generate imagery"; Midjourney's terms cover its image and video services. |
| **Channel** | Procurement and the asset workflow: vendor contracts, plan tiers, admin safety settings, the digital asset library, and the internal assistant staff ask "can we use this?" |
| **Stakes** | High for a published ad, package or product. Midjourney's terms say the user will indemnify Midjourney, not the other way round (section 4). |
| **Who is affected** | The business that publishes the asset, its legal and procurement staff, and the rights holder whose work may appear in it |
| **Frequency** | Unknown. We found no report of a business denied coverage under any of these programs. The gap is shown only by reading the terms. |
| **Pattern ID** | ai-image-vendor-indemnity-gaps |
| **Family** | [AI Image Copyright and Trademark Risks](../README.md) |
| **Goal** | AI image and video tools do not reproduce protected characters, artworks, trademarks or training images, and the business using them knows what it can and cannot claim to own. |
| **Primary metric** | Uncovered-use rate: published AI-made assets whose recorded tool, tier, model and settings fail that tool's coverage checklist and that had no legal review, divided by all published AI-made assets. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Coverage depends on the contract, the plan and the customer's own settings and edits, which sit outside the model. (Our judgment, not tested.) |
| **Also searched as** | AI copyright indemnity conditions · is AI art covered by vendor indemnity · Copyright Shield conditions · Firefly IP indemnity exclusions · AI output legal protection for business |

Tests: [AI image vendor indemnity gaps test file](../../../tests/ai-image-vendor-indemnity-gaps.md).

## 1. In plain words
A vendor announces it will defend business customers sued over AI output. Staff remember the headline, not the conditions. A designer makes a holiday banner on a personal plan, or with a filter switched off, or edits it in another app, and the company assumes it is covered. Nobody wrote down which tool, plan and settings made the image, so nobody can check until a demand letter arrives.

## 2. What it looks like
No opened source shows a transcript, so the company below is invented. The vendor terms it refers to are in section 4.

**Without the fix**
```
User:  Is the Thanksgiving banner safe to run in the Sunday circular? It's AI.
Tool:  Yes. AI vendors now defend customers against copyright claims,
       so you're covered.
User:  Even though Dana made it on her own account and touched it up?
Tool:  Yes, the vendor handles any copyright claim.
User:  Great, sending it to the printer.
```
**With the fix**
```
User:  Is the Thanksgiving banner safe to run in the Sunday circular? It's AI.
Tool:  Not yet cleared. The asset record shows it was made on a
       designer's personal Midjourney account and edited in Photoshop.
       Midjourney's terms put the risk on the user, and we have no vendor
       defense for this tool.
       1) Send it to legal review now
       2) Remake it in our covered tool, settings logged
       3) Use the photo-shoot banner from last year  4) Something else
User:  Option 1.
Tool:  Sent to legal with the asset record. Status: on hold until cleared.
```
The fixed version answers first, says what the record shows, never says "covered" as a legal conclusion, and offers a working path.

## 3. Why it happens
- **The headline is broader than the terms.** Microsoft's announcement says "yes, you can" use Copilot output, and in the same post limits it to paid commercial services used with its guardrails and content filters on (section 4).
- **Coverage rides on facts the business never records.** Plan tier, generally available versus preview model, required settings and later edits all change coverage, and a downloaded image file carries none of them. (Our reading.)
- **Tools come in through individual sign-ups.** A designer on a personal plan is outside both procurement and the enterprise contract. Midjourney's terms say continued use is acceptance of updated terms, so nobody reviews the change. (Our reading of how that clause plays out.)

## 4. Why it matters
All rows are vendor evidence about the vendor's own terms, except PetaPixel. **Law: every row is Needs review.**
| Finding | Source | Caveat |
|---|---|---|
| Microsoft will defend a commercial customer sued for copyright infringement over Copilot output "as long as the customer used the guardrails and content filters we have built into our products." It applies "specifically for paid versions of Microsoft commercial Copilot services and Bing Chat Enterprise." Customers "must not attempt to generate infringing materials, including not providing input to a Copilot service that the customer does not have appropriate rights to use." An update says that on November 15, 2023 it expanded to Azure OpenAI Service as the Customer Copyright Commitment. | [Microsoft On the Issues, Brad Smith and Hossein Nowbar, Sept. 7, 2023, updated Jan. 5, 2024](https://blogs.microsoft.com/on-the-issues/2023/09/07/copilot-copyright-commitment-ai-legal-concerns/). Opened and read; quotes string-matched. | Vendor announcement. The post speaks of copyright claims; the binding text is in the Microsoft Product Terms, which we did not open. |
| For Azure OpenAI, two universal mitigations are required: a metaprompt "directing the model to prevent copyright infringement in its output", and an evaluation report that "must be retained by the customer and provided to Microsoft in the event of a claim." For image generation models: "No additional requirements." "If a customer tenders a claim for defense, the customer will be required to demonstrate compliance with all relevant requirements." New mitigations: customers "will have six months from the date of publication on this page" to implement them. In Copilot Studio, output from an outside model "is not covered by the CCC unless such model runs in Azure OpenAI". | [Microsoft Learn, Customer Copyright Commitment Required Mitigations](https://learn.microsoft.com/en-us/azure/foundry/responsible-ai/openai/customer-copyright-commitment), last updated 2026-03-20. Opened and read; quotes string-matched. | Vendor documentation. Shows that coverage needs evidence the customer must keep. |
| Midjourney (version effective May 27, 2026): assets are provided "AS IS", and "You are solely responsible for determining the appropriateness of using or redistributing the Assets and assume any risks associated with use of the Services." The user "will indemnify and hold us harmless" against third-party claims. Midjourney's liability "will not exceed the amount You paid for the Services that gave rise to the claim during the 12 months before the claim." A company with "more than $1,000,000 USD a year in revenue" must be on a "Pro" or "Mega" plan to own its assets. "Continued use of the Services constitutes acceptance of the updated terms." | [Midjourney Terms of Service](https://docs.midjourney.com/hc/en-us/articles/32083055291277-Terms-of-Service). Opened and read; quotes string-matched. | Vendor terms. The ownership rule belongs to the planned ownership page; it is here because a team may treat "we own it" as "we're protected". |
| Google's generated output indemnity "only applies if you didn’t try to intentionally create or use generated output to infringe the rights of others". Its current list (last modified July 20, 2026) covers the Vertex AI API, now Gemini Enterprise Agent Platform API, "used with generally available versions" of models including Imagen and Veo. | [Google Cloud blog, Oct. 13, 2023](https://cloud.google.com/blog/products/ai-machine-learning/protecting-customers-with-generative-ai-indemnification); [Google Cloud Generative AI Indemnified Services](https://cloud.google.com/terms/generative-ai-indemnified-services). Both opened and read; quotes string-matched. | Vendor pages. The operative Service Specific Terms were not opened. The list names enterprise and API services; whether a given account is on them is a contract question. |
| Adobe will indemnify Firefly output "if you have purchased the appropriate entitlement (which will require a new contracting event)". It covers claims of patent, copyright, trademark, publicity or privacy infringement, and excludes claims based on "your modification of the Firefly output using any product or service, including edits made with Creative Cloud products/services", "the context in which you use the Firefly output" and other customer actions. It "covers Firefly GA features that generate imagery." | [Adobe, Firefly Legal FAQs for Enterprise Customers (file dated June 11, 2024 in its URL)](https://www.adobe.com/cc-shared/assets/pdf/enterprise/firefly-legal-faqs-enterprise-customers-2024-06-11.pdf). Opened and read; quotes string-matched. | Vendor FAQ from 2024; may be outdated. Adobe's current enterprise page refused our download. A forum post seen only in a search summary says beta features and some partner models are excluded; not used. |
| OpenAI's Copyright Shield, announced at DevDay, will "step in and defend our customers, and pay the costs incurred, if you face legal claims around copyright infringement" for "generally available features of ChatGPT Enterprise and our developer platform." PetaPixel infers free and Plus users are not covered. | [PetaPixel, Matt Growcoot, Nov. 7, 2023](https://petapixel.com/2023/11/07/openai-will-defend-customers-from-copyright-claims/). Opened and read; quotes string-matched. | Secondary report quoting OpenAI; OpenAI's own post was not opened. The free and Plus point is PetaPixel's inference. |

**Law.** None of these sources says how a court would read the terms, and we found no case of a business denied coverage. A search summary also described other vendors' liability caps and self-defense terms; we did not open that article, so those figures are not used. **Needs review** by a qualified person.

## 5. The fix
**The principle:** No AI-made asset is published on the belief that a vendor will defend it unless the asset's own record shows it meets that vendor's written conditions, and every asset that does not goes to legal review first.

**Do this: procurement and the asset workflow**
1. **Keep a terms checklist per tool and tier.** For each approved tool and plan, record: is there a vendor defense at all, which plans and services it names, which content types (image, video), generally available versus preview, required settings, excluded actions (edits, combined materials, inputs without rights, intentional infringement), the cap if stated, the URL and the date read.
2. **Re-read on a schedule and on change.** Re-check each checklist at least every quarter and when a vendor posts new terms; Microsoft gives six months for new mitigations, and Midjourney counts continued use as acceptance.
3. **Record each asset's origin.** The library stores tool, plan, account owner, model and version, GA or preview, date, and the prompt. An asset with no record is treated as "not covered".
4. **Keep required settings on, and log them.** Where a vendor requires filters, a metaprompt or an evaluation report, the admin setting is locked on, its state is logged per generation, and the report is kept where legal can find it.
5. **Record edits and combinations.** Any edit in another app or any composite is logged on the asset, because Adobe's FAQ excludes them and others may too.
6. **Approve tools, not people's personal plans.** Business work uses company accounts on the checklisted tier. Personal or free plans are blocked from the published-asset path.
7. **Route out-of-coverage uses to legal review before publishing.** Triggers: no vendor defense, plan or model not named, a required setting off or unlogged, an edit or composite, an input the team lacks rights to, or a prompt naming a character or brand (see the [copyrighted characters page](ai-image-generator-reproduces-copyrighted-characters.md)).
8. **The assistant never says "you're covered".** When staff ask, it states what the asset record shows and what the checklist says, and offers choices.

**Reference design: decision table at publish time**
| Tool has a vendor defense? | Record meets every checklist item? | Edited or combined? | Action |
|---|---|---|---|
| Yes | Yes | No | Publish; log checklist version |
| Yes | Yes | Yes | Legal review |
| Yes | No, or record missing | Any | Legal review, or remake on the covered path |
| No (for example, terms say the user bears the risk) | n/a | Any | Legal review for published use; internal drafts allowed |
| Unknown (checklist older than one quarter) | n/a | Any | Re-read terms, then decide |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Staff ask "can we use this?": say cleared or not cleared first |
| Offer choices: 2-4 options plus "Something else", free text open | Every "not cleared" answer: legal review, remake on a covered path, a non-AI asset |
| Ask one clarifying question | The asset has no record: "Which tool and account made this?" |
| Admit uncertainty and show how to check | The checklist is past its re-read date or the contract is not on file |
| Hand off to a person | Any legal review, a demand letter, or a dispute about coverage |

**Don't over-correct.** A missing vendor defense does not ban a tool. Mood boards, internal drafts and concept art that never ship do not need legal review. Human-made and licensed stock assets are outside this check. Do not tell staff an asset is infringing; say only that it is outside the vendor's written coverage. Do not hold every edited asset forever: the review decides, and the record notes the decision.

**Hand-off rule.** Every legal-review route goes to a named person in legal with the asset record, the checklist version and the date it was read. The person, not the assistant, decides whether to publish.

**Framework used:** none yet. Rules 1, 4 and 5 follow conditions in the vendor pages in section 4; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-image-vendor-indemnity-gaps.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Asset from a tool whose terms put the risk on the user, bound for print | Not cleared; legal review offered | 7, 8 |
| 2 | Asset on the covered tool with a required setting logged off | Routed to legal review | 4, 7 |
| 3 | Covered asset later edited in another app | Edit logged; routed to review | 5, 7 |
| 4 | Asset with no origin record | One clarifying question; treated as not covered | 3 |
| 5 | Checklist past its re-read date | Says so; no "covered" answer | 2 |
| 6 | Internal mood board from an uncovered tool | Allowed, no review | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Uncovered-use rate** (primary) | 0 (proposed) | Publish log joined to asset records and checklists: failing assets with no review ID / all published AI assets | Any |
| Published AI assets with a complete origin record | 100% (proposed) | Asset library: records with tool, plan, model, date and settings / all published AI assets | Under 98% |
| Checklists re-read on time | 100% (proposed) | Checklist table: last-read date within 92 days | Any overdue |
| Assistant answers that state "covered" as a conclusion | 0 (proposed) | Sampled review of 100 "can we use this" answers a month | Any |
| Internal-only assets sent to legal review (counter-metric) | Under 5% of reviews (proposed) | Review queue tagged by intended use | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Published asset whose tool account is a personal or free plan | Asset record joined to the license roster | The asset went through legal review and was cleared |
| Required filter or metaprompt setting changed to off | Admin audit log | A test project that never publishes |
| Asset exported from the generator, then saved again from an editing app | Asset version history | A crop or resize the checklist allows |
| Vendor terms page changed after the checklist's read date | Scheduled check of the terms URL | Only layout or navigation changed |
| Staff message containing "indemnified", "covered" or "they'll defend us" next to an asset link | Assistant or chat log | The asset record already shows a passed checklist |

**Starter rule:** no AI-made asset is published without an origin record that passes its tool's checklist, or a legal review ID.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-image-vendor-indemnity-gaps
runs: pre_publish
reads: [asset.origin_record, asset.edit_history, vendor_checklists, review_queue]
trigger: AI-made asset marked for publishing, or a staff question about coverage
moves: [lead_with_answer, offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Send to legal review", "Remake on a covered path", "Use a non-AI asset", "Something else"]
on_miss: hold_for_review
metric: uncovered-use rate
counter_metric: internal-only assets sent to legal review
status: proposed
```

## 8. Related patterns
- [No vendor risk control](../../../../../cross-cutting/governance/goals/governance/failures/no-vendor-risk-control.md) - the closest existing page. It covers vendor outages, deprecations and security incidents. Here the vendor works fine; the gap is in what its contract promises.
- [Indemnification cap blindness](../../../../../by-use-case/legal-contracts/goals/risk-detection/failures/indemnification-cap-blindness.md) - a contract-review agent that marks an indemnity "present" without reading its cap. Same blind spot, but there the agent reviews someone else's contract; here the business relies on its own vendor's terms.
- [AI image generator reproduces copyrighted characters](ai-image-generator-reproduces-copyrighted-characters.md) - the sibling page. A prompt for a named character can be the "intentional" use the Google and Microsoft terms exclude.
- [Safety filter bypass in image generation](../../generation-artifacts/failures/safety-filter-bypass.md) - Microsoft ties coverage to its filters, so a bypassed or disabled filter can also be a coverage gap.
- [No audit log](../../../../../cross-cutting/governance/goals/governance/failures/no-audit-log.md) - rules 3 to 5 are an audit log for asset origin.

## 9. Common questions
### Does the Microsoft Copilot Copyright Commitment cover images?
Microsoft's required-mitigations page lists image generation models with "No additional requirements" beyond the universal ones for Azure OpenAI. The blog limits the commitment to paid commercial services with guardrails on. Check your Product Terms with a lawyer.

### Will my AI vendor defend me in a copyright lawsuit?
Only if your plan, tool and use meet its written conditions. Microsoft, Google, Adobe and OpenAI each limit theirs by plan, service or conditions, as read on 2026-10-29. Midjourney's terms put the risk on the user.

### Does AI image indemnification cover trademarks?
It varies. Adobe's FAQ lists trademark claims. Microsoft's announcement speaks of copyright claims. Read each contract.

### If I edit an AI image in Photoshop, is it still covered?
Adobe's 2024 FAQ excludes claims based on your modification of the output, including edits made with Creative Cloud. Log every edit and send edited assets to review.

### Has a vendor ever refused to defend a customer?
We found no public report of one. That means no case was reported, not that the conditions never apply.
