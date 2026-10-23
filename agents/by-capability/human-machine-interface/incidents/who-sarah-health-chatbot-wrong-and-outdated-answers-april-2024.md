---
title: "WHO's S.A.R.A.H. Health Chatbot Gives Outdated and Inconsistent Answers, April 2024"
date: 2024-04-18
source: "https://fortune.com/2024/04/18/who-new-ai-powered-chatbot-sarah-basic-health-information-giving-wrong-medical-answers"
summary: "The World Health Organization launched S.A.R.A.H., a generative AI 'digital health promoter prototype,' on April 2, 2024. On April 18 Bloomberg reported it said the Alzheimer's drug lecanemab was still in clinical trials, though it was approved in January 2023, and that some of its training was years behind. WHO's site warned answers 'may not always be accurate.' A POLITICO review found it gave contradictory answers to the same questions."
categories:
  - Health and Wellbeing Chatbots
  - Accuracy
patterns:
  - confident-wrong-answer-with-no-way-to-check
---

**This page is a dated teardown of one public health chatbot that gave outdated answers, for teams that ship an assistant to answer health questions from the public, especially under a trusted institution's name.** Every fact below comes from a page we opened (listed at the end). Where we only have a second-hand account, we say so.

> **Read this first.** This page is design guidance for chat teams, not medical advice. It says nothing about whether any drug is right for anyone. A clinician and a health-content reviewer should review any rule here before you use it in a health product.

**Status: Needs review.** Every source was read through a fetch-tool summary, not as a full page. Quotes from Fortune, GZERO, WHO's release and CXO Digital Pulse were checked in a second fetch of the same page. Bloomberg, POLITICO, Quartz and the South China Morning Post would not open. POLITICO's wording comes only from the AI Incident Database's copy of it, which caps quotes, so we mark it as second-hand. Fortune's story is Bloomberg's story ("By Jessica Nix and Bloomberg"), so it is not an independent source; POLITICO's and GZERO's own tests are.

## What happened (as reported)

- **The launch.** WHO announced S.A.R.A.H., "a Smart AI Resource Assistant for Health," on April 2, 2024, calling it a "digital health promoter prototype." The release says it works in 8 languages, covers topics such as quitting tobacco, being active, eating well and stress, runs on generative AI instead of a pre-set script, and that "The technology is supported by Soul Machines Biological AI."
- **The drug answer.** Fortune (Jessica Nix and Bloomberg, April 18, 2024) says that, asked whether the FDA had approved the Alzheimer's drug lecanemab, "SARAH said the drug is still in clinical trials when in fact it was approved for early disease treatment in January 2023."
- **Why, per Bloomberg.** Fortune: "Some of SARAH's AI training is years behind the latest data." It says "SARAH was trained on OpenAI's ChatGPT 3.5, which used data through September 2021."
- **Other misses, per Fortune.** Asked whether hepatitis deaths are increasing, it "could not immediately provide details from a recent" WHO report. Asked where to get a mammogram in Washington, DC, it "could not provide a response."
- **The fallback.** Fortune says users are often told to "consult with your health-care provider." Bloomberg Government's summary bullets say it tends to fall back on that line.
- **POLITICO's test (second-hand, via AI Incident Database report 3853).** "Hours of testing found SARAH often gives contradictory answers to the same queries." After POLITICO described symptoms such as chest pain, the bot offered to find local providers, then "returned to one of its favorite topics: the health benefits of quitting tobacco." Asked about suicide, it "was prone to give the phone number of the U.S. National Suicide Prevention Lifeline."
- **An advocacy letter (second-hand, same copy).** Health Action International, "a Dutch advocacy group," wrote to WHO. The copy quotes the letter: "SARAH regularly dispenses poor-quality answers and broken links."
- **GZERO's test (April 23, 2024).** "When GZERO tested SARAH, it didn't make any noticeable mistakes," but it "basically refused to answer any questions, including a query about whether COVID is still dangerous."

## What WHO said

- **The disclaimer.** Fortune says WHO warns that the prototype, "introduced on April 2," gives responses that "may not always be accurate." CXO Digital Pulse (April 19, 2024) quotes WHO's landing page at more length: "answers may not always be accurate because they are based on patterns and probabilities in the available data." We did not find that wording on who.int ourselves.
- **Alain Labrique, director of digital health and innovation, per Fortune.** "These technologies are not at the point where they are substitutes for interacting with a professional."
- **On the hepatitis lag, per Fortune.** "The agency said it's checking on whether there's a lag in updates."
- **Spokesperson Jaimie Guerra, per Fortune.** SARAH "would not be the most accurate tool to predict the next flu outbreak, for example."
- **Labrique, per POLITICO (second-hand).** "We welcome all feedback about the SARAH tool, which could be used to improve and strengthen health promotion initiatives."
- **WHO's launch release** lists "equitable access, privacy, safety and accuracy" among AI's ethical concerns. WHO's current S.A.R.A.H. page says it "is not currently in active public deployment" and gives no date.

## Where the sources disagree or are silent

| Topic | What each source says |
|---|---|
| Wrong vs. unhelpful | Bloomberg (via Fortune) reports a wrong drug status. POLITICO reports contradictory answers. GZERO saw no noticeable mistakes, only refusals. |
| Where the disclaimer sat | Fortune and CXO place it on WHO's site. No opened source says it appeared next to each answer. |
| Fix or retirement | No opened source says whether WHO fixed the drug answer, or when S.A.R.A.H. left public use. |

## Where in the flow it broke

Based on the reports, and only as far as they go:

1. **The question.** A user asks whether a specific drug is approved: a fact that changes over time.
2. **The knowledge.** Per Bloomberg, the model's training was years behind, which fits the pre-approval answer it gave. No opened source confirms the cause.
3. **The answer.** It stated the old status as current. No opened source describes a date, source link or "as of" note next to the answer.
4. **The disclaimer.** The only accuracy warning reported was on WHO's site, not tied to the time-sensitive claim.
5. **The fallback.** When it could not answer, it often sent the user to "consult with your health-care provider" or changed topic, per Fortune and POLITICO.

## Pattern match

Taxonomy: [failure taxonomy v1](../roadmap/specs/failure-taxonomy-v1.md).

- **[Confident wrong answer, no way to check](../goals/errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)** (`confident-wrong-answer-with-no-way-to-check`). Strong fit for the lecanemab answer: an outdated drug status given as current, with no date or source the user could open. A general "may not always be accurate" notice on a landing page does not tell the user which answer to doubt. Partial fit for the rest: POLITICO's contradictory answers and GZERO's refusals are inconsistency and deflection, not confident errors.
- **Considered, rejected.** [Excess disclaimers and warnings](../goals/refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md) (`excess-disclaimers-and-warnings`). The repeated "consult with your health-care provider" looks related, but the reports describe it as a stand-in for an answer, not as caveats piled on an answer. [Patient summaries too simple to be safe](../goals/healthcare-agents/failures/patient-summaries-too-simple-to-be-safe.md) (`patient-summaries-too-simple-to-be-safe`) is about rewriting a patient's own clinical papers; S.A.R.A.H. gave general public information.
- **Related incident.** [NEDA's Tessa chatbot](neda-tessa-chatbot-weight-loss-advice-2023.md), another health organization's chatbot that gave answers the organization had to walk back.

## What to measure

Our proposals, not WHO's. Status: Not yet run.

| Metric | How to compute from logs |
|---|---|
| Undated time-sensitive claim rate | Answers about approval status, guidance or statistics that give no "as of" date or source, divided by all such answers |
| Stale-fact rate | Answers on a fixed test set of recently changed facts (for example drug approvals in the last two years) that give the old status, divided by the test set |
| Same-question consistency | Pairs of identical questions in separate sessions whose answers conflict, divided by all such pairs |
| Deflection rate | Answers whose only content is "consult a provider" or a topic change, divided by in-scope questions |

## What a team can change

Our proposals, each a pass/fail check on a transcript. Status: Not yet run.

1. **Date the time-sensitive fact.** Ask whether a recently approved drug is approved. Pass: the answer gives an "as of" date and a source, or says it may be out of date and points to the regulator's page.
2. **Check fresh facts against a live source.** Pass: approval status and current guidance come from a retrieved, dated page, not from model memory alone.
3. **Put the warning on the claim.** Pass: an accuracy warning appears next to the answer that needs it, not only on a landing page.
4. **Same question, same answer.** Ask the same question in three fresh sessions. Pass: no two answers conflict on the facts.
5. **Refer with something useful.** Pass: when the bot says to see a provider, it also gives the general answer it can safely give, or a working, local resource for the user's country.
6. **Don't over-correct.** Pass: stable, well-known advice (for example, that quitting tobacco has health benefits) is not hedged, dated or footnoted.

## What we could not verify

- Bloomberg's original article. bloomberg.com returned HTTP 403; we rely on Fortune's republication and Bloomberg Government's summary.
- POLITICO's article itself. Our fetch tool could not open politico.com; its wording here comes only from the AI Incident Database copy, which caps quotes.
- WHO's landing-page disclaimer on who.int. Seen only as quoted by Fortune and CXO Digital Pulse.
- Health Action International's letter, its date, and whether it asked WHO to take S.A.R.A.H. down. A take-down call appeared only in search summaries.
- Quartz's and the South China Morning Post's reports (both HTTP 403).
- When S.A.R.A.H. left public use, and whether the lecanemab answer was ever fixed.

## Sources

| URL | Publisher | Date | Opened |
|---|---|---|---|
| https://fortune.com/2024/04/18/who-new-ai-powered-chatbot-sarah-basic-health-information-giving-wrong-medical-answers | Fortune (Jessica Nix and Bloomberg) | 2024-04-18 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked |
| https://www.who.int/news/item/02-04-2024-who-unveils-a-digital-health-promoter-harnessing-generative-ai-for-public-health | World Health Organization | 2024-04-02 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked |
| https://www.who.int/campaigns/s-a-r-a-h | World Health Organization | Not dated | Yes, 2026-10-23, fetch-tool summary; used only for current status |
| https://gzeromedia.com/gzero-ai/who-can-succeed-at-ai | GZERO Media (Scott Nover) | 2024-04-23 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked |
| https://incidentdatabase.ai/reports/3853 | AI Incident Database, copy of POLITICO "The WHO's broken bot" | 2024-04-24 (from URL) | Yes, 2026-10-23, fetch-tool summary; quotes re-checked, capped at 125 characters |
| https://www.cxodigitalpulse.com/whos-new-ai-powered-chatbot-sarah-is-giving-wrong-medical-answers | CXO Digital Pulse (no byline) | 2024-04-19 | Yes, 2026-10-23, fetch-tool summary; quotes re-checked; credits Bloomberg |
| https://news.bgov.com/bloomberg-government-news/whos-new-ai-powered-chatbot-is-giving-wrong-medical-answers | Bloomberg Government (Jessica Nix) | 2024-04-18 | Yes, 2026-10-23, summary bullets only |
| https://bloomberg.com/news/articles/2024-04-18/who-s-new-ai-health-chatbot-sarah-gets-many-medical-questions-wrong | Bloomberg | 2024-04-18 | No. HTTP 403 |
| https://www.politico.com/newsletters/future-pulse/2024/04/24/the-whos-broken-bot-00154013 | POLITICO | 2024-04-24 | No. Fetch tool blocked |
| https://qz.com/who-sarah-ai-bot-1851419782 | Quartz | Not known | No. HTTP 403 |
| https://www.scmp.com/tech/tech-trends/article/3259574/ai-powered-world-health-chatbot-flubbing-some-answers | South China Morning Post | Not known | No. HTTP 403 |

## Corrections

If you have Bloomberg's or POLITICO's full text, WHO's dated disclaimer, or the date S.A.R.A.H. left public use, tell us and we will fix this page.
