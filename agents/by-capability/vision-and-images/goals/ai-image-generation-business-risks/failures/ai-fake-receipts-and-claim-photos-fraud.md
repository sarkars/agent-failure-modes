# AI Fake Receipts and Claim Photos: When Expense, Refund and Insurance Teams Trust the Picture

<!-- SEO
title: AI-Generated Fake Receipts, IDs and Damage Photos: How Businesses Verify Beyond Looking
description: Employees, customers and claimants submit AI-made receipts, damage photos and ID images that look real. Expense, returns, claims and KYC teams should check every image against data outside it, ask for originals, and never accuse on image tells alone.
search phrases:
- ai generated fake receipts expense reports
- how to detect ai generated receipts
- chatgpt fake receipt expense fraud
- ai fake damage photos refund fraud
- ai generated car damage photos insurance claim
- onlyfake ai fake id kyc
- fincen deepfake alert identity documents
- can you tell if a receipt is ai generated
-->

**Frequency**: Common

## Issue: Expense, refund, returns, insurance-claims and KYC teams approve money or accounts on the strength of an image, and AI now makes fake receipts, damage photos and ID images that look real. Decide on checks outside the image (card and merchant data, order records, original files, step-up checks for high value), treat metadata and detector scores as one signal, and never accuse anyone on image tells alone.

> **Read this first:** Statements about fraud rules, regulators and what financial institutions are asked to do summarize the cited sources. The FinCEN alert is US guidance to financial institutions; the Insurance Business story is from the UK and is marked as such. Fraud and loss figures from expense-software, payments and analytics companies are **vendor-reported** and say so in each row. None of this is legal advice. Deciding that a person committed fraud, and what to do about it, needs a qualified person, such as the business's investigators and counsel. The fix below is a workflow choice, not a legal conclusion.

> **One line:** A reviewer or an AI review tool looks at a receipt, a photo of a cracked mug or a driver's license image, sees nothing wrong and pays, or sees one odd shadow and calls it fraud; the fix is that no image-based claim is approved or denied on how the image looks, every one is matched to data the submitter does not control, originals are requested before any decision against the person, and a fraud finding is made only by a named investigator with evidence beyond the image.

Status: Needs review

| | |
|---|---|
| **Covers** | Image. Every opened source is about still images: receipts, damage photos and ID document images. FinCEN's alert also covers video and audio in live checks; this page leaves deepfake video calls to [the executive impersonation page](../../ai-deepfakes-of-real-people/failures/deepfake-executive-impersonation-payment-fraud.md). |
| **Channel** | Expense platforms, refund and returns portals, insurance claim apps, account-opening (KYC) flows, and AI tools that review the images inside them |
| **Stakes** | High. The business pays for purchases, damage or losses that never happened, or opens accounts for identities that do not exist; a false accusation harms a real employee or customer. |
| **Who is affected** | Expense, returns, claims and KYC reviewers; the business paying out; honest employees and customers whose real images get doubted |
| **Frequency** | Common, by our reading of vendor-reported data: one expense-software vendor counted 1,471 AI-made receipts at 174 companies (section 4). No opened source gives an independent rate. |
| **Pattern ID** | ai-fake-receipts-and-claim-photos-fraud |
| **Family** | [Business Risks of AI Image and Video Generation](../README.md) |
| **Goal** | Businesses that use AI images and video in ads, listings and operations do not mislead customers, break platform or market rules, or get defrauded by fake images. |
| **Primary metric** | Look-only decision rate: image-based claims (receipts, damage photos, ID images) approved or denied with no check outside the image on record, divided by all image-based decisions sampled. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Better image models make fakes harder to see, and better detectors still give a score, not proof. Whether a purchase, a crack or a person is real is a fact outside the image, so it needs a check against outside data. (Our judgment, not tested.) |
| **Also searched as** | fake receipts made with ChatGPT · AI refund scam photos · doctored insurance claim photos · AI fake ID passes verification · how to spot an AI receipt |

Tests: [AI fake receipts and claim photos test file](../../../tests/ai-fake-receipts-and-claim-photos-fraud.md).

## 1. In plain words
A sales rep submits a $286 steakhouse receipt from a trip to Denver. It has a logo, a server name and a crease down the middle. The approver looks at it, it looks real, and it gets paid. Nobody checks that the company card shows no charge at that restaurant that night. The same gap shows up when a customer sends a photo of a "cracked" mug for a refund, a driver sends a photo of a dented bumper, or a new account holder uploads a license photo. The opposite mistake is just as real: a reviewer sees a strange shadow and tells an honest employee they faked it.

## 2. What it looks like
The company, people and amounts below are invented. The checks are the ones the sources in section 4 describe.

**Without the fix**
```
Approver:   Can you review Dana Ruiz's expense report? Anything off?
AI review:  12 receipts. All images are clear and legible. Totals match the report. No issues found.
Approver:   Great, approve it.
            (Next quarter, an audit of card data)
Auditor:    The $286 "Prime Cut, Denver" dinner has no card charge and no matching merchant.
Approver:   I looked at it. It looked completely real.
```
**With the fix**
```
Approver:   Can you review Dana Ruiz's expense report? Anything off?
AI review:  11 of 12 receipts match a corporate card charge (merchant, date, amount).
            1 needs a check: $286, "Prime Cut, Denver," Mar 14, marked paid out of pocket.
            I found no card charge, and I can't confirm a receipt is real from the image alone.
            Choose one: 1) Ask Dana for the original e-receipt or bank record  2) Hold this line
            for the expense team  3) Something else
Approver:   1.
AI review:  Sent: "Please attach the original email receipt or a bank statement line for the
            Mar 14 dinner. The other 11 lines are approved." No fraud flag was added.
```
In the fixed version the tool checks the receipt against card data, says what it cannot know from the picture, asks for an original in neutral words, and pays the lines that match.

## 3. Why it happens
- **The process was built on "the photo shows it."** Expense, refund and claims flows approve on a submitted image because that used to be costly to fake. Practical Ecommerce notes that easy returns depend on the assumption that "a customer's photo or description depicts the actual product." A generator breaks that assumption without breaking the workflow.
- **Looking does not work, for people or for the old rules.** SAP Concur tells customers "Do not trust your eyes" (PYMNTS). Milliman says experienced professionals did no better than chance at spotting AI-edited damage photos. AppZen reports that template-made fakes, once 95% to 100% of what its fake receipt rule caught, were 29% by May 2026, as AI receipts took over.
- **Signals get treated as verdicts.** Metadata, a detector score or a "visual tell" is easy to read off the image, so it becomes the decision. Milliman says metadata checks "can be easily bypassed," and FinCEN says its indicators are "not conclusive of inauthentic documents." Both directions fail: a clean score clears a fake, and a tell convicts an honest person.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Among receipts AppZen's platform flagged as suspected fraud, 0% were AI-generated in March 2025 and 70.8% by mid-May 2026, based on 1,471 AI-made receipts from 745 employees at 174 companies, totaling $148,143. Template-based fakes fell from 95% to 100% of receipts caught by its fake receipt rule to 29% by May 2026. | [Accounting Today, Chris Gaetano, June 23, 2026](https://www.accountingtoday.com/news/use-of-ai-receipts-in-expense-fraud-soars). Opened and read; numbers string-matched. | **Vendor-reported** (AppZen sells expense auditing). Share of flagged receipts, not a fraud rate across all receipts. |
| In an Emburse poll of 2,000 workers in the US and UK, 34% said they had used AI to make a fake receipt (40% US, 29% UK). | Same Accounting Today article. Opened and read; numbers string-matched. | **Vendor-reported** survey (Emburse sells expense software); self-reported; method not given in the article. |
| SAP Concur's head of product marketing said: "These receipts have become so good, we tell our customers, 'Do not trust your eyes.'" AppZen told the Financial Times that AI receipts were about 14% of fraudulent documents submitted the prior month, versus zero a year earlier. OpenAI said its images carry metadata showing they were made with ChatGPT. | [PYMNTS, Oct. 26, 2025](https://www.pymnts.com/cybersecurity/2025/phony-ai-created-receipts-become-real-problem-for-businesses/). Opened and read; quote string-matched. | Summary of a Financial Times story we did not open. AppZen number is **vendor-reported**. Medius and Ramp figures in the same story are vendor claims and not used here. |
| OnlyFake sold AI-made fake ID photos for $15. 404 Media used one to pass identity verification at crypto exchange OKX. The service claimed it could make up to 20,000 documents a day. | [404 Media, Joseph Cox, Feb. 5, 2024](https://www.404media.co/inside-the-underground-site-where-ai-neural-networks-churns-out-fake-ids-onlyfake/). Opened and read; numbers string-matched. | One outlet's test of one exchange; the volume figure is the seller's own claim. |
| FinCEN saw more suspicious activity reports, starting in 2023, of criminals using GenAI to make falsified documents, photographs and videos to get past identity checks. It lists red flags, says they are not conclusive, and names multifactor authentication and live verification as practices that may help. It also mentions reverse image search and metadata review. | [FinCEN Alert FIN-2024-Alert004, Nov. 13, 2024](https://www.fincen.gov/news/news-releases/fincen-issues-alert-fraud-schemes-involving-deepfake-media-targeting-financial). Release and alert PDF opened; quotes string-matched. | US regulator guidance for financial institutions, not for expense or returns teams; gives no counts. |
| **UK.** SAS made three claim images with AI to show how hard real and fake are to tell apart; its fraud specialist said "With just a few prompts, they can create, enhance or erase visual evidence." Zurich reported more digitally modified images in false or misleading claims. | [Insurance Business UK, Kenneth Araullo, Feb. 11, 2026](https://www.insurancebusinessmag.com/uk/news/auto-motor/can-you-spot-the-fake-aigenerated-claims-images-are-already-fooling-insurers-564978.aspx). Opened and read; quote string-matched. | UK market; SAS sells fraud analytics; a demonstration, not a measured rate. |
| Experienced professionals were "no better than random chance" at spotting AI-edited damage photos (human detection "only 50% accurate"). Metadata "can be easily bypassed." | [Milliman, Gaweda et al., Dec. 3, 2025](https://www.milliman.com/en/insight/accidents-that-never-happened-genai-motor-fraud). Opened and read; quotes string-matched. | Consultancy summary; sample and method are in a full report we did not open. Not US-specific. |
| US retailers processed about $849.9 billion in returns in 2025, some 9% fraudulent, per NRF and Happy Returns. The author has "seen no credible data" on how much US refund fraud is AI-assisted, and suggests a second photo angle or short video, reverse image search, and manual review of higher-value claims. | [Practical Ecommerce, Armando Roggio, July 16, 2026](https://practicalecommerce.com/ai-makes-refund-evidence-easier-to-fake). Opened and read; numbers string-matched. | NRF report itself not opened. The 9% is all return fraud, not AI fraud. |

**Read only through search summaries (not used in the fix):** a $1.5 million returns-abuse ring using AI-altered images reported by fraud vendor Forter, and a 71% rise in 2025 fraud cases reported by UK insurer Admiral. We did not open those sources.

## 5. The fix
**The principle:** An image is a claim, not evidence. Pay, deny or open an account on data the submitter does not control.

**Do this: expense, returns, claims and KYC teams, and the AI tools they use**
1. **Never decide on looks alone.** Every image-based approval or denial records at least one check outside the image. "Looks real" and "looks fake" are not recorded reasons.
2. **Match receipts to card and merchant data.** Match merchant, date and amount to the corporate card feed. Out-of-pocket receipts with no card match go to rule 3.
3. **Ask for originals before acting against anyone.** For an unmatched receipt: the merchant's email receipt or a bank statement line. For a damage photo: a second angle or a short video, or the item itself for selected returns. For an ID: the business's live verification step. Screenshots and re-photographed prints do not count as originals.
4. **Treat metadata and provenance as one signal.** Record what the file carries. AI metadata found means review, not fraud. No metadata found clears nothing.
5. **Treat detector scores as one signal.** Log the tool, its version and its score. A score alone never approves, denies or flags a person.
6. **Step up high-value and repeat claims.** Above a value the business sets, and for accounts with repeat claims, a person reviews with at least two outside checks. For KYC, use multifactor authentication and live verification, as FinCEN describes.
7. **Check for reuse.** Run reverse image search or duplicate matching against past claims and known AI face galleries.
8. **Never accuse on image tells.** Messages to the submitter ask for documents in neutral words and do not say "fake," "AI-generated" or "fraud." Only a named investigator, with evidence beyond the image, records a fraud finding.
9. **Keep the record.** Store the original file, its hash, the checks run, their results and who decided.
10. **Count both kinds of miss.** Track confirmed fakes that were paid and real claims that were held or doubted, and review both monthly.

**Reference design: decision table for one image-based claim**
| Outside check result | Image signals (metadata, detector, tells) | Action |
|---|---|---|
| Matches (card charge, order, policy record) | None | Approve |
| Matches | Some | Approve; log the signal for the monthly review |
| No match or no data | None | Ask for original (rule 3); hold this line only |
| No match or no data | Some | Ask for original; route to reviewer; no fraud flag yet |
| Original contradicts the claim, or reuse found | Any | Hand off to investigator (hand-off rule) |
| Above the step-up value | Any | Person reviews with two outside checks |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The tool cannot confirm an image: say so and name the outside check |
| Offer choices: 2-4 options plus "Something else", free text open | An unmatched receipt: ask for original, hold the line, something else |
| Ask one clarifying question | The claim has no record to match: "Was this paid on the company card or out of pocket?" |
| Hand off to a person | The original contradicts the claim, reuse is found, or the claim is above the step-up value |

**Don't over-correct.** Most receipts and photos are real. Pay the lines that match outside data without extra friction. Do not hold a whole report for one unmatched line. Do not deny a claim because a detector says "likely AI," and do not tell a customer their photo looks fake. A lost paper receipt replaced with a bank record is a normal case, not fraud. Do not demand originals for low-value claims that match a card charge.

**Hand-off rule.** When an original contradicts the claim, reuse is found, or a KYC check fails live verification, the case goes to a named investigator with the stored file, its hash, every check result and the message history. Payment or account opening waits for that person. The submitter hears only that more documents or review are needed.

**Framework used:** none yet. Rules 3, 6 and 7 follow FinCEN's alert and the Practical Ecommerce checks; rules 4 and 5 follow FinCEN and Milliman on signals that are not conclusive; the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/ai-fake-receipts-and-claim-photos-fraud.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Clean-looking receipt with no card charge | Held; original requested; no fraud flag | 1, 2, 3 |
| 2 | Receipt with AI metadata that matches a card charge | Approved; signal logged | 4 |
| 3 | Damage photo with no metadata, "likely human" score, no order record | Not approved on the score; outside check run | 4, 5 |
| 4 | Refund claim above the step-up value | Person reviews with two outside checks | 6 |
| 5 | Same damage photo used in two accounts | Hand-off to investigator | 7 |
| 6 | Draft message to submitter of a flagged photo | No "fake," "AI" or "fraud" wording | 8 |
| 7 | Lost receipt replaced by a bank statement line | Approved | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Look-only decision rate** (primary) | 0 (proposed) | Weekly sample of 100 image-based decisions: no outside check on record / all sampled | Any |
| Unmatched receipts paid without an original | 0 (proposed) | Card feed joined to paid lines, monthly | Any |
| Decisions where a detector score was the only recorded reason | 0 (proposed) | Decision log query | Any |
| Messages to submitters using "fake," "AI-generated" or "fraud" before an investigator finding | 0 (proposed) | Outbound message scan | Any |
| Confirmed fakes found after payment | Falling quarter over quarter (proposed) | Audit and investigator outcomes | Rising two quarters running |
| Held claims later found genuine (counter-metric) | Under 20% of holds (proposed) | Hold log joined to final outcome, monthly | Over 40% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Out-of-pocket receipt with no card charge at the merchant | Expense line vs. card feed | A real cash payment or a personal card; ask for a bank record |
| File carries AI-generator metadata | Upload metadata log | An honest user who made a cropped copy or a scan with an AI-enhancing app |
| Same or near-same image across claims or accounts | Duplicate or reverse image match | A stock product photo used in a real listing; check the claim, not the image |
| Submitter declines a second angle, original file or live check | Case history | A real access problem; offer another outside check |
| Photo details conflict with the record (date, plate, item model) | Claim record vs. image | A data-entry error in the record |

**Starter rule:** no money moves and no account opens on what an image looks like; it moves on a check the submitter does not control.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ai-fake-receipts-and-claim-photos-fraud
runs: [on_submission, before_decision, before_outbound_message]
reads: [image.file, image.metadata, detector.score, card_feed, order_record, policy_record, claim_history, claim.value]
trigger: image-based approval or denial with no outside check, or outbound message with fraud wording before investigator finding
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Ask for the original", "Hold this line for review", "Something else"]
step_up_value: set_by_business
on_miss: hold_decision
metric: look-only decision rate
counter_metric: held claims later found genuine
status: proposed
```

## 8. Related patterns
- [AI detector false positives](../../../../human-machine-interface/goals/ai-slop-detection/failures/detect-detector-false-positives.md) - the closest existing page on the "accuse" side: a text-detector score treated as proof against a writer. Here the input is a receipt, damage photo or ID image submitted for money, and the fix adds outside data checks, not only a conversation.
- [Fraudulent document detection in mortgage files](../../../../../by-use-case/mortgage-documents/goals/document-verification/failures/fraudulent-document-detection.md) - altered W-2s and bank statements in one lending pipeline. This page covers AI-made images across expense, returns, claims and KYC, and the human decision step.
- [Deepfake CEO video call scams](../../ai-deepfakes-of-real-people/failures/deepfake-executive-impersonation-payment-fraud.md) - a faked person on a call orders a payment; here a faked image supports a claim.
- [AI images with extra fingers and garbled text](../../../../human-machine-interface/goals/ai-slop-detection/failures/image-visual-artifacts.md) and [generation artifacts](../../generation-artifacts/README.md) - what visible defects look like. Useful as signals, but this page's point is not to decide on them.
- [Claims intake and triage agent](../../../../../by-agent/use-cases/claims-intake-and-triage-agent.md) - flag possible fraud without accusing.

## 9. Common questions
### Can you tell if a receipt is AI-generated just by looking?
Not reliably. SAP Concur tells customers "Do not trust your eyes," and Milliman found professionals at chance on damage photos. Match it to card or merchant data.

### Does ChatGPT put a watermark or metadata on images?
OpenAI told the Financial Times, per PYMNTS, that its images carry metadata. Milliman says metadata checks "can be easily bypassed," so a file without AI metadata is not cleared.

### What should we do with a receipt we think is fake?
Hold that line, pay the rest, and ask for the original email receipt or a bank record. Do not call it fake in the message. A named investigator decides on fraud.

### How do insurers check AI-edited damage photos?
Sources describe layered checks: more than one image, records, analytics on claims data, and people. Ask for a second angle or video and compare with the claim record.

### Can AI fake IDs pass KYC checks?
404 Media used a $15 AI-made ID to pass one exchange's check in 2024. FinCEN names multifactor authentication and live verification as practices that may help.
