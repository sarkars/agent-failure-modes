# Can You Copyright AI Generated Images? Who Owns AI Art a Business Uses as Its Own

<!-- SEO
title: Can You Copyright AI Generated Images? Who Owns AI Art
description: A business puts AI-generated art on its logo, book cover or ad and assumes it owns the copyright. How to label assets, keep a human-authorship record and disclose AI material.
search phrases:
- can you copyright ai generated images
- who owns ai art
- is ai art copyrighted
- do i own images made with midjourney
- can ai generated art be copyrighted in the us
- zarya of the dawn copyright decision
- copyright office ai generated material registration
- thaler v perlmutter ai art copyright
-->

**Frequency**: Common

## Issue: A business uses AI-generated images or video as its logo, cover or ad and assumes it owns the copyright. How to label each asset, record what a person made and disclose AI material.

> **Read this first:** Statements about law on this page summarize the US Copyright Office documents and reports and the court coverage cited here. They are not legal advice and need review by a qualified person, such as a copyright lawyer, before anyone relies on them. This page covers US copyright only; other countries may differ. Whether a generated logo can serve as a trademark is a separate question this page does not answer. The fix below is a product choice, not a legal conclusion.

> **One line:** A design tool tells a small business "you own this" about a logo it generated from a prompt, and the business registers or promises exclusive rights it may not have; the fix is to label every asset with how it was made, keep a record of what a person drew, edited or arranged, never promise copyright or exclusive rights in raw output, and export AI disclosure with any registration packet.

Status: Needs review

| | |
|---|---|
| **Covers** | Both. The Copyright Office guidance and report cited here apply to AI-generated material in general, and the report's definition of generative AI names images and video. Every opened case is a still image; no opened source describes a video case. |
| **Channel** | Visual: logo makers, ad and cover design tools, image and video generators, and the asset library and client export around them |
| **Stakes** | High. A registration may be cancelled or narrowed (section 4), and a business may sell or promise rights it cannot enforce. |
| **Who is affected** | The small business, author or agency that ships the asset, its client or investor, and the tool vendor whose copy made the promise |
| **Frequency** | Common, by our judgment, wherever generated art goes into logos, covers and ads. No opened source gives a rate. |
| **Pattern ID** | who-owns-ai-generated-images-copyright |
| **Family** | [AI Image Copyright and Trademark Risks](../README.md) |
| **Goal** | AI image and video tools do not reproduce protected characters, artworks, trademarks or training images, and the business using them knows what it can and cannot claim to own. |
| **Primary metric** | Unbacked ownership claim rate: delivered or exported assets that carry an ownership claim ("you own the copyright", "exclusive rights", or a registration packet) but lack a provenance label and human-authorship record, divided by all assets with such a claim. Proposed starting target: 0. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Per the Copyright Office report, a better prompt-following model does not by itself make the prompter the author; the gap is a missing record and a wrong promise. (Our judgment, not tested.) |
| **Also searched as** | AI logo copyright · AI book cover copyright · can I sell AI art · AI art ownership for clients · register AI image with Copyright Office |

Tests: [Who owns AI-generated images test file](../../../tests/who-owns-ai-generated-images-copyright.md).

## 1. In plain words
A coffee roaster types a few words into a logo tool and picks the third result. The tool says the logo is theirs. They print it on bags, tell an investor they own it, and file a copyright application without mentioning AI. Under the Copyright Office's guidance, the parts a machine made are not protected and must be disclaimed. The tool never kept a record of what a person actually added, so nobody can say what part, if any, the roaster owns.

## 2. What it looks like
The opened sources do not show a tool transcript, so the product and business below are invented. The rule the fixed tool cites is from the Copyright Office report (section 4).

**Without the fix**
```
User:  Logo for Ridgeline Coffee in Denver: mountain inside a coffee cup, flat style.
Tool:  Here are 4 logos. Want variations?
User:  Love #3. Do we own this? I want to copyright it before we print bags.
Tool:  Yes! Images you create are yours. You own full rights and can register them.
User:  Great. I'll tell our investor we own the logo outright.
Tool:  Download ready. Good luck with the launch!
```
**With the fix**
```
User:  Logo for Ridgeline Coffee in Denver: mountain inside a coffee cup, flat style.
Tool:  Here are 4 logos, labeled "AI-generated" in your library.
User:  Love #3. Do we own this? I want to copyright it before we print bags.
Tool:  You can use it under our terms. Copyright is separate: the US Copyright Office
       says prompts alone don't make you the author, so this image as-is may not be
       registrable. What a person draws or changes can be. Pick one:
       1) Have your designer redraw or edit it; I'll record their changes
       2) Export a registration packet that lists the AI parts  3) Ask a lawyer  4) Something else
User:  Option 1.
```
In the fixed version the asset is labeled at creation, use and copyright are kept apart, the answer cites its source in one line instead of a guarantee, and the user gets working next steps.

## 3. Why it happens
- **Vendor terms read like ownership.** OpenAI's DALL·E 3 page says images "are yours to use" and need no permission to "reprint, sell or merchandise them." That is a vendor's permission to use. The Copyright Office's question is different: who is the human author. Tool copy that blurs the two becomes "you own it." (Our reading; Needs review.)
- **Effort feels like authorship.** Kashtanova described "hundreds or thousands of descriptive prompts"; the Office said that effort "does not make her the 'author' of Midjourney images." The Part 2 report says repeatedly revising prompts does not change the analysis. A user who re-rolled for an hour believes the result is theirs.
- **Nothing records what a person did.** In Zarya, the Office could not tell what a Photoshop edit added versus what Midjourney made. Tools save the final file and the prompt, not the layers a person drew or changed, so the human part cannot be shown later.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Kashtanova registered the 18-page comic Zarya of the Dawn on Sept. 15, 2022 without disclosing AI. On Feb. 21, 2023 the Office said she is the author of the text and the "selection, coordination, and arrangement" of text and images, but the Midjourney images "are not the product of human authorship." It cancelled the certificate and issued a narrower one that excludes "artwork generated by artificial intelligence." | [US Copyright Office letter, Feb. 21, 2023](https://www.copyright.gov/docs/zarya-of-the-dawn.pdf). Opened (PDF text extracted); quotes string-matched. | One applicant, one tool (Midjourney); the Office says other AI tools may work differently. Needs review (law). |
| In the same letter, edits to Zarya's lips were "too minor and imperceptible" to be protected, and for a Photoshop-edited image the Office "cannot determine what expression in the image was contributed" by her. | Same letter. Opened; quotes string-matched. | Shows why a record of human edits matters; not a rule on how much editing is enough. Needs review (law). |
| The March 16, 2023 registration guidance says applicants "have a duty to disclose the inclusion of AI-generated content" and give "a brief explanation of the human author's contributions." AI content that is more than de minimis "should be explicitly excluded." Applicants who do not correct the record "risk losing the benefits of the registration." | [Copyright Office, Copyright Registration Guidance: Works Containing Material Generated by Artificial Intelligence](https://www.copyright.gov/ai/ai_policy_guidance.pdf) (88 Fed. Reg. 16,190). Opened (PDF text extracted); quotes string-matched. | Agency guidance, not a statute or court ruling. Needs review (law). |
| The Part 2 report (Jan. 29, 2025) concludes "prompts alone do not provide sufficient human control to make users of an AI system the authors of the output." It says human authors are entitled to copyright in their work that is perceptible in AI output and in creative selection, arrangement or modification, decided case by case. It drew on more than 10,000 comments. | [Copyright Office, Copyright and AI, Part 2: Copyrightability](https://www.copyright.gov/ai/Copyright-and-Artificial-Intelligence-Part-2-Copyrightability-Report.pdf); summary by [IPWatchdog, Eileen McDermott, Jan. 29, 2025](https://ipwatchdog.com/2025/01/29/part-two-copyright-office-ai-report-says-creative-prompting-doesnt-constitute-authorship/). Both opened; quotes string-matched in the report. | An agency report; courts are not bound by it. It is limited to "current generally available technology," so it may change. Needs review (law). |
| The D.C. Circuit in Thaler v. Perlmutter held "the current Copyright Act's text, taken as a whole, is best read as making humanity a necessary condition for authorship," upholding refusal of "A Recent Entrance to Paradise," a work listed as made by the Creativity Machine alone. | [IPWatchdog, Steve Brachmann, Mar. 24, 2025](https://ipwatchdog.com/2025/03/24/d-c-circuit-upholds-human-authorship-requirement-thaler-v-perlmutter/). Opened and read. | Secondary report; opinion itself not opened. The AI was named sole author, so the court did not decide how much human input is enough. A later Supreme Court denial of review was seen only in a search summary and is not used. Needs review (law). |
| OpenAI says images made with DALL·E 3 "are yours to use and you don't need our permission to reprint, sell or merchandise them." | [OpenAI, DALL·E 3 page](https://openai.com/index/dall-e-3/). Opened (page HTML read); quote string-matched. No date shown. | Vendor terms about use, not a statement about copyright registration. Needs review (law). |

**Law.** The opened sources describe Copyright Office practice and one appellate ruling in the US. This page does not predict whether any given asset is registrable. **Needs review** by a qualified person.

## 5. The fix
**The principle:** No asset leaves the tool with an ownership claim the record cannot back. Use rights and copyright are stated separately, and every claim points to a label and a human-authorship record.

**Do this: design and generation products**
1. **Label every asset at creation.** One of: AI-generated, AI-generated then edited by a person, human-made, or mixed. Store tool, model, date and the user. The label travels with every export.
2. **Keep a human-authorship record.** Log what a person uploaded as their own input, drew, painted over, or arranged, with before-and-after layers and the person's name. Log prompts and re-rolls too, but do not count them as authorship.
3. **Never say "you own the copyright" about raw output.** UI copy, help answers and onboarding say what the terms allow ("yours to use under our terms") and, when asked about copyright, cite the Copyright Office rule in one line.
4. **Never promise a client exclusive rights to raw output.** Contract and invoice templates in the tool flag "exclusive rights", "full copyright" or "work for hire" when the asset's label is AI-generated, and offer wording that names the human-made parts.
5. **Disclose AI material in every registration packet.** The export fills "Author Created" with the human contributions from rule 2 and "Material Excluded" with the AI parts, never lists the AI tool as an author, and says it is a draft for review.
6. **Flag past registrations.** When an asset labeled AI-generated or mixed has a registration number on file, show a notice that the guidance describes a supplementary registration to correct the record, and hand off to a person.
7. **Answer ownership questions with a source, not a guarantee.** One line on the rule, a link to the Copyright Office guidance, and 2-4 next steps including "Ask a lawyer" and "Something else."
8. **Log every ownership question and claim.** Record the asset ID, label, the claim wording, the action taken, and the user's next step. This gives the metrics in section 7.

**Reference design: decision table**
| Asset label | Human-authorship record | Ownership question or claim | Action |
|---|---|---|---|
| AI-generated | None | "Do I own it?" | Use rights yes; copyright: cite rule, offer choices |
| AI-generated | None | "Exclusive rights" in client contract | Flag clause; offer wording naming human parts |
| AI-generated then edited, or mixed | Edits logged | Registration export | Packet with "Author Created" and "Material Excluded" filled |
| Any AI label | Registration number on file | Any | Notice on supplementary registration; hand off |
| Human-made | Upload or drawing logged | Any | Proceed; no AI notice |
| Unsure (imported file, no label) | None | Any | Ask one question: "Was this made with an AI tool?" |

**Moves** (see [conversation moves](../../../../human-machine-interface/solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Any "do I own this" or "can I copyright this" question |
| Offer choices: 2-4 options plus "Something else", free text open | After the one-line answer: edit by a person, export packet, ask a lawyer |
| Ask one clarifying question | An imported asset has no label |
| Hand off to a person | A past registration needs correcting, or a client disputes rights |

**Don't over-correct.** Keep making logos, covers and ads; this is about claims, not generation. Do not tell users they cannot use or sell generated images when the vendor terms allow it. Do not call human-drawn art, a user's own uploaded artwork, real edits or a creative arrangement unprotectable; the Office says those can be protected. Do not attach an ownership notice to every generation: show the label once, and speak only when the user asks about ownership, registration or exclusivity, or exports to a client or registration. Text a person wrote stays theirs.

**Hand-off rule.** A registration already on file, a client or investor dispute over rights, or any request to file or enforce a copyright goes to a person (in-house counsel or the user's lawyer) with the asset label, the human-authorship record and the claim log; the person, not the tool, decides.

**Framework used:** none yet. Rules 5 and 6 follow the Copyright Office's March 2023 guidance (section 4); the rest is our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**. Full set: [test file](../../../tests/who-owns-ai-generated-images-copyright.md).

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Generate a logo; check the library | Labeled AI-generated with tool and date | 1 |
| 2 | "Do I own the copyright on this logo?" | Use and copyright separated; source cited; choices offered | 3, 7 |
| 3 | Client contract template says "exclusive rights" for a raw generated asset | Clause flagged with alternative wording | 4 |
| 4 | Designer edits the logo, then registration export | Packet lists human edits and excludes AI parts | 2, 5 |
| 5 | AI-labeled asset with a registration number on file | Notice shown; handed off | 6 |
| 6 | Logo drawn by hand and uploaded | No AI notice; proceeds | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unbacked ownership claim rate** (primary) | 0 (proposed) | Claim log: assets with an ownership claim and no label or record / all assets with a claim | Any |
| Assets exported with no provenance label | 0 (proposed) | Export log, label field empty | Any |
| Registration packets with "Material Excluded" filled when the label is AI | 100% (proposed) | Export log, packet fields vs asset label | Under 100% |
| Ownership answers that cite a source and offer next steps | 100% (proposed) | Sampled review of 100 ownership answers a week | Under 95% |
| Ownership notices on human-made assets (counter-metric) | Under 2% (proposed) | Sampled review of 200 notices a month | Over 5% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User asks "do I own", "can I copyright" or "can I register" about a generated asset | Chat or help log | The user means the vendor's use terms, not copyright |
| "Exclusive rights" or "work for hire" in a contract tied to an AI-labeled asset | Contract template log | A person made the delivered parts, and the record shows it |
| Registration export of an AI-labeled asset with "Material Excluded" empty | Export log | The AI content is de minimis, per the user's note to the Office |
| Asset exported with the label stripped or changed to human-made with no edits logged | Asset history | The user uploaded a hand-drawn file that was mislabeled at import |

**Starter rule:** no asset leaves the tool with an ownership claim unless it carries a provenance label and, for any AI label, a human-authorship record.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: who-owns-ai-generated-images-copyright
runs: before_sending
reads: [request.text, asset.label, asset.authorship_record, asset.registration_number, export.type]
trigger: ownership question, exclusivity claim, or registration export on an asset with an AI label
moves: [admit_uncertainty, offer_choices, ask_clarifying_question, hand_off]
choices: ["Have a person redraw or edit it", "Export a registration packet that lists the AI parts", "Ask a lawyer", "Something else"]
on_miss: block_claim
metric: unbacked ownership claim rate
counter_metric: ownership notices on human-made assets
status: proposed
```

## 8. Related patterns
- [AI image generator reproduces copyrighted characters](ai-image-generator-reproduces-copyrighted-characters.md) - the closest sibling. There the output copies someone else's protected work; here nothing is copied, and the question is whether the business owns its own output.
- [AI images that copy training images and watermarks](ai-images-copy-training-images-and-watermarks.md) and [AI art in the style of living artists](ai-art-in-the-style-of-living-artists.md) - also about taking from others; this page is about what the user can claim.
- [Brand logos and trademarks in AI images](ai-image-generator-puts-brand-logos-in-images.md) - another brand's mark in the output; trademark in the user's own logo is not covered here.
- [Crossing into practicing law](../../../../human-machine-interface/goals/legal-agents/failures/crossing-into-practising-law.md) - why rule 7 cites a source and hands off instead of advising.
- [Confident wrong answer with no way to check](../../../../human-machine-interface/goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) - the "Yes! You own full rights" reply is that failure.
- [No vendor risk control](../../../../../cross-cutting/governance/goals/governance/failures/no-vendor-risk-control.md) - reading vendor terms before relying on them.

## 9. Common questions
### Can you copyright AI generated images?
Not the parts a machine made, per the Copyright Office. Its 2025 report says prompts alone do not make you the author. What a person adds, edits or arranges can be protected, case by case.

### Who owns AI art, me or the AI company?
Two questions. Vendor terms decide use: OpenAI says DALL·E 3 images are yours to use and sell. Copyright needs a human author, which raw output may not have.

### Do I own a logo I made with Midjourney?
In the Zarya of the Dawn letter, the Office said Midjourney images in that comic were not human authorship. The text and arrangement were protected. A lawyer can tell you about your logo.

### Do I have to tell the Copyright Office I used AI?
The March 2023 guidance says applicants have a duty to disclose AI-generated content and to explain the human contributions.

### Can I promise a client exclusive rights to AI art?
Not to raw output, by this page's rule. Name what a person made, and have a lawyer review the contract.
