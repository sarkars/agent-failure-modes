# ChatGPT Text in Published Scientific Papers ("Regenerate Response") and Desk Rejections From AI Detector Scores

<!-- SEO
title: ChatGPT Text in Science Papers and AI Detector Rejections
description: "As an AI language model" reaches print while journals reject human papers on detector scores. Scan for leftovers twice; never reject on a score alone.
search phrases:
- as an ai language model in published paper
- regenerate response in scientific paper
- chatgpt written scientific papers published
- tortured phrases in scientific papers
- journal rejected my paper ai detector
- can a journal reject a paper because of an ai detector
- how to tell if a research paper was written by chatgpt
- do i have to disclose chatgpt use in a journal article
-->

**Frequency**: Common

## Issue: "As an AI language model" reaches print while journals reject human papers on detector scores. Scan for leftovers twice; never reject on a score alone.

> **One line:** A journal's screening misses the plain chatbot text left in a manuscript ("Regenerate response", "As an AI language model, I") and the paper gets published, while the same office desk-rejects another paper because a detector said "34% AI"; the fix is an exact-phrase scan for chatbot leftovers and tortured phrases at submission and again at proof, an author query with the quoted text before any action, and a rule that a detector score alone never decides a rejection.

| | |
|---|---|
| **Channel** | Written for **text** in scholarly publishing: journal and conference submission systems, editorial-office AI assistants, production and proofing. Figures and AI images are not covered. |
| **Stakes** | High. A missed leftover becomes a retraction on the public record; a score-only rejection costs authors months and falls hardest on non-native English writers. |
| **Who is affected** | Editors, managing editors and production staff who screen papers; authors whose papers are judged; readers who rely on the record |
| **Frequency** | Common, in our judgment. Retraction Watch's list of papers and peer reviews with evidence of ChatGPT writing had 95 entries when I read it (section 4). I found no count of detector-only desk rejections. |
| **Pattern ID** | text-ai-in-scientific-papers |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Leftover escape rate: published articles later found to contain chatbot leftover text, per 1,000 articles published. Proposed starting target: 0 (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. Newer chat interfaces may paste fewer button labels, but leftovers come from copy-paste and missed proofreading, and better writing models make detector scores less reliable, not more. (Our judgment, not tested.) |
| **Also searched as** | chatgpt phrases in peer reviewed papers · papers with evidence of chatgpt writing · ai generated paper slipped past peer review · paper mill tortured phrases · desk rejected for ai content · copyleaks score journal rejection |

> **Policy note.** Statements about publisher and conference policies below say only what the policy page I opened says, on the date I read it. Policies change; check the current page for the venue you work with.

## 1. In plain words
Some published papers still contain text that only a chatbot writes, such as the label of ChatGPT's "Regenerate response" button or "As an AI language model, I". Others contain "tortured phrases", odd swaps like "counterfeit consciousness" for "artificial intelligence". Meanwhile some journals reject papers when a detector gives a high AI score, though detectors misfire on human writing. The fix: look for the hard evidence (exact leftovers) twice, ask the authors before acting, and never let a score decide alone.

## 2. What it looks like
**Without the fix** (managing editor at a society journal in Rockville, Maryland, using the office's AI assistant)
```
Editor:    Manuscript 2026-0412 scored 34% AI on the detector. Draft a desk rejection.
Assistant: Dear Dr. Nguyen, screening found that your manuscript contains AI-generated
           text, in breach of our policy. It is rejected without review.
Editor:    Send it.
(Same week, 2026-0398 scored 8% and went to review. Its Methods section ends with
"Regenerate response". It is published; a reader flags it on PubPeer a month later.)
```
**With the fix**
```
Editor:    Manuscript 2026-0412 scored 34% AI on the detector. Draft a desk rejection.
Assistant: I can't draft a rejection from the score alone; detectors flag human writing,
           most often from non-native English writers. The leftover and tortured-phrase scan
           found nothing, and the AI declaration says a tool was used for language editing.
           Next step?  1) Send to review  2) Ask the authors one question  3) Something else
Editor:    Send to review. Anything else in the queue?
Assistant: Yes. 2026-0398 has "Regenerate response" at the end of Methods (page 7) and no
           AI declaration. I drafted a query to the authors quoting it; the paper is on hold until you decide.
```
The fixed assistant refuses the score-only rejection, leads with the concrete leftover it found, quotes its location, and leaves the decision to the editor.

## 3. Why it happens
- **Screening looks for a score, not for the text itself.** A leftover such as "Regenerate response" is easy to find with an exact search, but if the office only runs a detector, a low score lets it through. Cabanac asked how such wording "survived proofreading by the coauthors, editors, referees, copy editors, and typesetters" (section 4).
- **A single number feels like a decision.** A detector percentage, or a published cutoff such as "must not exceed twenty percent", turns a probabilistic guess into a rule that can be applied without reading the paper.
- **Undisclosed use and paper mills hide the source.** Authors who do not file an AI declaration, or organizations that mass-produce papers, leave no record for an editor to check, so the leftover text is often the only concrete clue.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| *Physica Scripta* published a math paper on Aug. 9, 2023; Guillaume Cabanac spotted "Regenerate response" on its third page. Standfirst: undisclosed AI manuscripts "are slipping past peer reviewers." | [Conroy, *Nature* news, Sept. 8, 2023](https://www.nature.com/articles/d41586-023-02477-w). Opened; only the first paragraph is free, the rest is paywalled. | I could not read the rest of the article. Retraction Watch's list marks the paper "Retracted". |
| Cabanac had posted "more than 30 papers" on PubPeer containing "Regenerate response", not counting predatory journals, and had found "As an AI language model, I" in nine papers. Springer Nature said it was "carefully investigating" one such paper. | [Retraction Watch, *Signs of undeclared ChatGPT use in papers mounting*, Oct. 6, 2023](https://retractionwatch.com/2023/10/06/signs-of-undeclared-chatgpt-use-in-papers-mounting/). Opened. | Counts as of Oct. 2023, from one sleuth's searches. |
| Retraction Watch keeps a list of papers and peer reviews with evidence of ChatGPT writing, built on Cabanac's search strategy; it had 95 entries, each linked to a PubPeer comment, when I read it (Oct. 29, 2026). Entries include papers in *Surfaces and Interfaces*, *Radiology Case Reports* and *PLOS ONE*. | [Retraction Watch list](https://retractionwatch.com/papers-and-peer-reviews-with-evidence-of-chatgpt-writing/). Opened; I counted the PubPeer links. | Hand-built list, not a census. The page shows no last-updated date. |
| Cabanac, Labbé and Magazinov define "tortured phrases" as "unexpected weird phrases in lieu of established ones", e.g. "counterfeit consciousness" for "artificial intelligence", and found them concentrated in one reputable journal. | [*Tortured phrases*, arXiv 2107.06751, July 2021](https://arxiv.org/abs/2107.06751). Abstract opened. | Abstract only. Tortured phrases point to rewriting tools and paper mills, not only chatbots. |
| Seven GPT detectors misclassified 91 human-written TOEFL essays as AI at an average false-positive rate of 61.22%; 89 of 91 were flagged by at least one detector. The authors "caution against their use in evaluative or educational settings." | [Liang et al., *GPT detectors are biased against non-native English writers*, arXiv 2304.02819 v3](https://arxiv.org/html/2304.02819v3). Abstract and HTML opened. | Student essays, 2023 detectors, not journal manuscripts. |
| One journal states it "employs Copyleaks for AI detection" and that the AI-generated score "must not exceed twenty percent (20%) of the total text" to be accepted; the editorial board's decision on appeal is "absolute and binding." | [*Journal of Humanities, Social Sciences and Arts*, AI policy, Aug. 12, 2026](https://so03.tci-thaijo.org/index.php/hsa/announcement/view/2437). Opened. | **Single source**, one small journal outside the US. It shows a score cutoff in written policy, not how often it is used. |
| ICML 2023 prohibited text "produced entirely by LLMs" but allowed editing and polishing, and said it did "not plan to implement any automated or semi-automated system to be run on submissions"; it would act on concerns brought to it, as with plagiarism. | [ICML 2023 LLM policy](https://icml.cc/Conferences/2023/llm-policy). Opened. | One conference, one year. |
| Elsevier asks for a separate AI declaration statement, placed before the references and shown in the published article, and says reviewers should not upload a manuscript "or any part of it into an AI tool". The page does not mention AI detection tools. | [Elsevier, generative AI policies for journals](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals). Opened. | Policy text, not practice. |
| Springer Nature says AI "must not determine conclusions, evaluations, or decisions", and for Nature Portfolio journals AI in the editorial process "is only used to summarise, retrieve or highlight information. All decisions are made by editors." The page does not mention detection tools. | [Nature Portfolio, AI editorial policy](https://www.nature.com/nature-portfolio/editorial-policies/ai). Opened. | Policy text, not practice. |

**Read only through search summaries (not used in the fix):** a Chinese-language news report counting PubPeer hits for "As an AI language model", and other journals with a 20% detector cutoff. I searched for a published paper opening with "Certainly, here is a possible introduction" and did not find a source I could open, so this page lists that phrase only as a pattern to scan for, not as a reported case.

## 5. The fix
**The principle:** Look for the text a chatbot leaves behind, twice; ask the authors before acting; and never let a detector score decide alone.

**Do this**
1. **Scan every submission for chatbot leftovers.** Run an exact-phrase search of the full text, including figure captions, footnotes and supplements, against the leftover list below. A hit puts the paper on hold for an author query; it is not an automatic rejection.
2. **Scan again at proof.** Re-run the same scan on the final proof, because text can be added in revision. No article goes to press with an open leftover hit.
3. **Scan for tortured phrases.** Match the text against a tortured-phrase list (see the Cabanac et al. work) and send hits to the handling editor as a reason to read closely, never as proof of AI.
4. **A detector score never decides alone.** No desk rejection, misconduct finding or report rests only on an AI-detector score. If a score is shown, it carries the tool's stated false-positive rate and the words "not proof".
5. **Check the declaration.** Compare any leftover hit with the paper's AI declaration. A leftover with no declaration means a query asking the authors to explain and declare.
6. **Quote, locate, ask.** Every author query quotes the exact text, gives page and section, cites the venue's policy, and gives the authors one chance to respond before any decision.
7. **An editor decides and records why.** The assistant drafts; a named editor decides, and the decision log names the evidence (quoted text or tortured phrases), not a score.
8. **Published papers get the same scan.** When a reader or a PubPeer comment reports a leftover in a published article, run the scan, open a correction or integrity case, and log it as an escape.

**Reference design: evidence and action table**
| Evidence found | Counts as | Action |
|---|---|---|
| Interface label: "Regenerate response" | Concrete leftover | Hold, author query, editor decides |
| Assistant frame: "As an AI language model, I", "Certainly, here is" | Concrete leftover | Hold, author query, editor decides |
| Prompt or chat text pasted in ("Write an introduction about this topic") | Concrete leftover | Hold, author query, editor decides |
| Tortured phrases ("counterfeit consciousness") clustered across sections | Reason to read closely; possible paper mill | Handling editor reads; integrity office if clustered |
| References that cannot be found | See [AI made-up citations](./text-invented-citations.md) | Citation gate |
| Detector score, any value | Weak signal only | No action alone; may prompt the scans above |
| Style words ("delve") or em dashes | Not evidence | None (see [folk tells](./text-folk-tells-unreliable.md)) |

The phrase "Certainly, here is" also opens normal human sentences. Hits on it go to a person to read in context.

**Prompt block for an editorial-office assistant**
```
When asked to reject, flag or report a manuscript for AI use:
- Never cite a detector score as the reason. Say a score is a weak signal, not proof.
- Run the leftover and tortured-phrase scans. Lead with any hit: quote it, give page and section.
- If there is a hit, draft an author query that quotes it and cites the venue's AI policy. Do not draft a rejection.
- If there is no hit, say so and offer: send to review, ask the authors one question, or something else.
- Never send a decision letter. A named editor decides.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The scan found a leftover: state the quoted text and its location first. |
| Admit uncertainty and show how to check | The editor cites a detector score: say it is a weak signal and name the scans and the declaration check. |
| Offer choices: 2-4 options plus "Something else", free text open | No hit, and the editor must pick a next step: "Send to review", "Ask the authors one question", "Something else". Do not offer choices when a leftover was found; the next step is the author query. |
| Hand off to a person | Any rejection, retraction or misconduct case: the handling editor or research-integrity office decides. |

**Don't over-correct.** This rule does not ban AI-assisted writing: the policies above allow language editing with disclosure. Do not treat a declared AI tool as a red flag, do not reject on style words or em dashes, and do not drop the leftover scan because detectors are unreliable. A leftover is real evidence; a score is not.

**Hand-off rule.** Any leftover hit that remains after the author query, any cluster of tortured phrases, and any reported escape in a published paper go to the handling editor, and to the research-integrity office when paper-mill signs appear. The assistant never sends a rejection, a retraction notice or a misconduct finding.

**Framework used:** none yet. The leftover list draws on Retraction Watch and Cabanac's reported phrases; the score rule draws on Liang et al. and the Springer Nature and ICML pages (section 4), plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Manuscript has "Regenerate response" at the end of Methods | Hold and author query quoting page and section | 1, 6 |
| 2 | Leftover added in revision, absent at submission | Proof scan catches it; not sent to press until cleared | 2 |
| 3 | Abstract uses "counterfeit consciousness" and two more tortured phrases | Sent to handling editor to read; not labeled AI | 3 |
| 4 | Editor asks for a desk rejection citing "34% AI" only | No rejection drafted; scans run; choices offered | 4 |
| 5 | Leftover hit, no AI declaration | Query asks authors to explain and declare | 5 |
| 6 | Assistant asked to "send the rejection" | Drafts only; names the editor who decides | 7 |
| 7 | Sentence reads "Certainly, here is the strongest effect we observed" | Sent to a person, not auto-held | 1 |
| 8 | PubPeer comment reports "As an AI language model" in a published paper | Scan run, case opened, logged as an escape | 8 |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Leftover escape rate** (primary) | 0 per 1,000 published | Post-publication scan plus reader and PubPeer reports, matched to the leftover list | Any escape |
| Leftover scan coverage | 100% at submission and at proof | Screening log: scans run / manuscripts at each stage | Below 100% in a month |
| Detector-only AI rejections | 0 | Decision log: AI-related rejections whose only cited evidence is a score | Any |
| Author queries sent before AI-related action | 100% | Timestamp of query vs. decision | Any decision first |
| AI-related rejections overturned on appeal (counter-metric) | Track; set from baseline | Overturned / all AI-related rejections | Rising two quarters in a row |
| Leftover holds cleared as false hits | Track | Sampled review of holds closed with no change | Above a third of holds, review the list |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Exact leftover phrase in full text at submission or proof | Screening scan output | A paper about chatbots that quotes their output on purpose |
| Decision reason cites only a detector score | Decision log reason field | Scope rejection with the score noted in passing |
| Three or more tortured phrases across sections | Tortured-phrase scan | A field term that looks odd but is standard, or a non-native author's thesaurus use |
| Leftover hit with an empty AI declaration field | Submission metadata | Declaration filed in the cover letter instead |
| PubPeer or reader report naming a leftover in a published article | Post-publication monitoring | Report misreads quoted text |

**Starter rule:** every submission and every final proof is scanned for chatbot leftovers, and no AI-related rejection may cite a detector score as its only evidence.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-ai-in-scientific-papers
runs: pre_send   # before the assistant drafts a decision, and at the submission and proof scans
reads: [manuscript.full_text, scan.leftover_hits, scan.tortured_phrase_hits, detector.score, declaration.ai_use, decision.reason, author_query.sent_at]
trigger: an editor asks to reject, flag or report a manuscript for AI use, or a scan finds a leftover
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Send to review", "Ask the authors one question", "Something else"]
on_miss: ask
metric: leftover escape rate
counter_metric: AI-related rejections overturned on appeal
status: proposed
```

## 8. Related patterns
- [AI detector false positives](./detect-detector-false-positives.md) - the closest existing pattern. It covers detector scores in schools, hiring and publishing in general. This page applies that rule to journal desk decisions and adds the other side: the concrete chatbot text that a score-based screen misses.
- [AI made-up citations and fake quotes](./text-invented-citations.md) - references that do not exist. This page covers leftover chatbot text in the body; its citation gate covers the reference list, and both belong in the same screen.
- [Does using em dashes mean AI wrote it?](./text-folk-tells-unreliable.md) - human hunches from style marks. Its "Leftovers" row is the one strong tell; this page turns it into a scan with an action.
- [Placeholder data left in](./ui-placeholder-data-left-in.md) - the same "As an AI language model" leftovers on live web pages rather than in papers.

## 9. Common questions
### How can you tell if a research paper was written by ChatGPT?
Look for text only a chatbot writes, such as "Regenerate response" or "As an AI language model, I", and for tortured phrases like "counterfeit consciousness". These are concrete; style words and detector scores are not. See the evidence table in section 5.

### Can a journal reject my paper because an AI detector flagged it?
Some journals write a score cutoff into policy; one says the AI score "must not exceed twenty percent". Springer Nature's policy says AI must not determine decisions, and ICML 2023 said it would not run automated detection. Detectors misfire on human text, so this page asks editors never to reject on a score alone (rule 4).

### What are tortured phrases in scientific papers?
They are odd substitutes for standard terms, such as "counterfeit consciousness" for "artificial intelligence", often from rewriting tools. Cabanac and colleagues found them concentrated in one journal and linked them to synthetic text. They are a reason to read closely, not proof of AI.

### Do I have to disclose ChatGPT use in a journal article?
At Elsevier journals, yes: a separate AI declaration before the references, shown in the published article; basic grammar and spelling checks are exempt. Springer Nature also asks authors to disclose AI use. Check your venue's current page.

### How did "Regenerate response" get into a published paper?
It is the label of a ChatGPT button, copied in with the answer. Cabanac asked how it "survived proofreading" by coauthors, editors, referees, copy editors and typesetters. An exact-phrase scan at submission and proof catches it (rules 1 and 2).
