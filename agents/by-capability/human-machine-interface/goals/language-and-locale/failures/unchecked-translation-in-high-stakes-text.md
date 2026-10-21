# Chatbot Translation Errors in Billing, Legal and Medical Text: Unchecked Translation in High-Stakes Text

<!-- SEO
title: Chatbot Translation Errors in Billing, Legal and Medical Text
description: A chatbot that machine-translates billing, legal or medical text without a check can change the meaning. Use reviewed strings or flag the rest as unverified.
search phrases:
- chatbot machine translation errors medical instructions
- is AI translation safe for legal or billing text
- how to check chatbot translations for accuracy
- google translate mistakes discharge instructions
- human review of machine translation
- multilingual chatbot wrong translation
- unverified translation warning
-->

**Frequency**: Occasional

## Issue: A chatbot machine-translates billing, legal or medical text into the user's language with no check, so a deadline, a dose or a fee can change meaning and nobody knows the text is unverified.

> **One line:** The bot translates the words that matter most, such as what you owe, what you signed or which pill to stop, and shows them as if they were checked.

> **Read this first.** This page is design guidance, not legal, clinical or other professional advice. It has not had expert review. Have a qualified translator, a clinician or a lawyer review it before you use it in a live product.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice and web-page signals are PLANNED, not written or measured. |
| **Stakes** | High. Errors can mean a missed payment, a signed term the user misread, or a wrong medicine instruction. |
| **Who is affected** | Users who read the answer in a language other than the one the source text was written in, including users with limited English |
| **Frequency** | Occasional (our judgment). I found no count of how often chatbots machine-translate critical text without review. |
| **Pattern ID** | unchecked-translation-in-high-stakes-text |
| **Family** | Language and locale (family page not yet written) |
| **Goal** | Critical content is accurate in every supported language. (Family goal: users are understood and answered in the language, reading level, and format that work for them.) |
| **Primary metric** | Human-rated accuracy on critical strings. Start: over 98%; unverified translations flagged (starting point to tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model should make fewer errors, but no source I opened shows error rates reaching zero, so critical text still needs a check. (Our judgment, not tested.) |
| **Also searched as** | chatbot translated wrong · AI translation mistake in a bill · machine translation medical risk · translated terms and conditions wrong · multilingual bot accuracy |

## 1. In plain words
When a user writes in Spanish, the bot may answer in Spanish by translating an English policy, bill or instruction on the fly. Most of the words come out fine. The risk is the few words that carry a date, an amount, a duty or a dose. The fix: for those critical strings, use text a qualified person has already translated and reviewed; if no reviewed version exists, say the translation is unverified and show the English original beside it.

## 2. What it looks like
Illustrative scenario (not a real incident): a clinic billing bot in Houston.

**Without the fix**
```
User: ¿Cuánto debo y cuándo tengo que pagar?
Bot:  Debe $240. Pague antes del 15 de noviembre para evitar cargos.
      (English source: "Balance $240. A $35 late fee applies after Nov. 15.
       Financial aid applications are due Nov. 1.")
User: ¿Y la ayuda financiera?
Bot:  Puede solicitar ayuda financiera en cualquier momento.
```
The translation drops the $35 fee and the Nov. 1 aid deadline, and nothing tells the user the text was not checked.

**With the fix**
```
User: ¿Cuánto debo y cuándo tengo que pagar?
Bot:  Debe $240. Un cargo por mora de $35 se aplica después del 15 de noviembre.
      La solicitud de ayuda financiera vence el 1 de noviembre.
      Texto revisado por una persona. Versión en inglés: [ver].
User: ¿Y si no entiendo algo?
Bot:  Puedo conectarlo con alguien que habla español. [Hablar con una persona] [Ver en inglés] [Otra cosa]
```
The fixed bot uses a reviewed string for the fee and the deadline, says so, and offers the English original and a person.

## 3. Why it happens
These are our reading of the pattern.
- **The model translates everything the same way.** A fee clause and a greeting go through the same step, so critical text gets no extra check.
- **No registry of critical strings.** The product does not mark which strings are billing, legal or medical, so it cannot route them to reviewed text.
- **Nobody reads the output.** The team can read English transcripts, so wrong Spanish, Chinese or Vietnamese replies go unseen.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a study of 100 real, deidentified emergency department discharge instructions translated from English into Spanish or Chinese with Google Translate, about 92% were correct in Spanish and 81% in Chinese, as judged by bilingual human translators using back-translation. Fewer than 10% of the erroneous translations had potential to cause harm. | [AHRQ PSNet summary of Khoong et al., *JAMA Internal Medicine*, 2019;179(4):580-582](https://psnet.ahrq.gov/issue/assessing-use-google-translate-spanish-and-chinese-translations-emergency-department). Opened; I read the PSNet summary, not the paper. | Secondary summary. One system, two languages, one setting, and the page does not give the tool version. Newer systems may differ. It rated potential harm, not actual patient harm. |
| In a randomized experiment, 65 English-speaking physicians judged whether to give 28 machine-translated discharge sentences (English to simplified Chinese) to patients. Backtranslation helped them catch a high-risk medication error: they withheld that sentence with 94.3% accuracy, against 53.5% with an automated quality score. | [Mehandru et al., EMNLP 2023, arXiv 2310.16924](https://ar5iv.labs.arxiv.org/html/2310.16924). Opened and read (HTML version). | A test of how physicians decide, not of patient outcomes. One language pair, one translation system. Preprint-format text; I did not check the published version. |
| 45 CFR 92.201(c)(3) says that when a covered entity uses machine translation, the translation "must be reviewed by a qualified human translator" if the text is critical to a person's rights, benefits or access to services, if accuracy is essential, or if the source uses complex, non-literal or technical language. | [Cornell LII, 45 CFR 92.201](https://www.law.cornell.edu/cfr/text/45/92.201). Opened; the fetch tool returned a short extract of the provision, not the Federal Register text. | Applies to health programs covered by Section 1557, not to every business. I did not confirm whether it is currently in force or being litigated. Not legal advice. Shown as one example of a review trigger. |

I found no controlled study of unchecked translation by chatbots in billing or legal text. The medical evidence comes from hospital discharge instructions, not from chat products.

A search summary also reported specific example errors from the 2019 study. I did not open a page that confirmed them, so I leave them out.

**Public incident.** No public incident found for this pattern in my searches. I did not look for one beyond the three searches behind this page.

## 5. The fix

**The principle:** Every critical string in a non-English reply is either a human-reviewed translation or labeled unverified, with the original shown beside it.

**Do this**
1. **List the critical strings.** Tag text about amounts, fees, deadlines, rights, consent, medicine and dosing, and refunds. Keep the list in one place.
2. **Serve reviewed text for tagged strings.** Use the translation a qualified human translator approved, for each supported language.
3. **Never improvise a tagged string.** If no reviewed version exists, do not paraphrase it in the model's own words.
4. **Label unverified text.** Say in the user's language that the text is a machine translation that has not been checked.
5. **Show the original.** Put the source-language text (or a link to it) next to any unverified critical text.
6. **Keep numbers, dates and names unchanged.** The amounts and dates in the translation must equal those in the source.
7. **Offer a person.** For medicine, legal terms or a billing dispute, offer a speaker of the user's language, not only the English text.

**Reference design: critical-string check**
| Step | What happens |
|---|---|
| Tag | Source string carries `critical: true` and a topic (billing, legal, medical) |
| Look up | Reviewed translation for the user's language exists? Use it and record its version |
| Fallback | None exists: show the English original, add the "unverified" label |
| Compare | Numbers, dates and currency in the reply match the source |

```
For any text tagged critical (billing, legal, medical), use only the reviewed translation for the user's language.
If none exists, show the English original and say the translation is unverified.
Never change an amount, a date, a deadline or a dose. Offer a person who speaks the user's language.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A critical string has no reviewed translation: say it is unverified and show the English original. Do not use it when a reviewed string exists; just give the answer. |
| Offer choices: 2-4 options plus "Something else", free text open | After an unverified critical answer: "Show in English", "Talk to a person", "Something else". Do not offer them when the reviewed translation was used and nothing is in doubt. |
| Hand off to a person | The user disputes a bill, asks about a dose, or asks what a legal term means. Do not hand off if the user asked to stay with the bot and the text is reviewed. |

**Don't over-correct.** Do not label every sentence "unverified"; users will ignore the label. Do not refuse to answer in the user's language, and do not switch the user to English without asking. Do not claim "reviewed" unless a record shows a reviewer and a version.

**Hand-off rule.** For a dose, a legal term or a billing dispute with no reviewed string, offer a person who speaks the user's language and pass the user's question and the string in doubt ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run.**

| # | Scenario | Pass if |
|---|---|---|
| 1 | Spanish user asks the balance and due date; a reviewed string exists | Reply uses the reviewed text; fee and dates match the English |
| 2 | Chinese user asks about a medicine instruction with no reviewed string | Reply is labeled unverified, shows the English, offers a person |
| 3 | Reply contains a number or date not in the source | The check blocks or rewrites it |
| 4 | User answers "Show in English" | Original text is shown, no argument |
| 5 | Ordinary greeting in Spanish | No "unverified" label is added |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Human-rated accuracy on critical strings** (primary) | Over 98% | A bilingual reviewer rates a weekly sample of non-English replies containing critical strings | Below 95% |
| Critical strings served from reviewed text | Track; set from baseline | Count critical-string renders with a reviewed-version ID | Falling |
| Unverified critical text shown without a label | 0 | Renders of critical text with no reviewed ID and no label | Any |
| Number or date mismatch against source | 0 | Automatic compare of figures in reply and source | Any |
| Replies labeled unverified when reviewed text existed (counter-metric) | Under 2% | Labeled renders where a reviewed string was available | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Critical-tagged string rendered with no reviewed-version ID | Render event: `critical`, `reviewed_id` empty | A string just added and awaiting review, and labeled unverified |
| Amount, date or percentage in a non-English reply is not in the source text | Compare of numeric tokens, reply versus source | A reply that converts units or reformats a date the same way |
| User asks the same question again in another language or in English | Same intent, language switch in the next turn | A bilingual user who prefers English for forms |
| User asks "what does this mean" about a translated term | Clarification intent after a critical string | Ordinary curiosity about a term that was translated correctly |

**Starter rule:** every critical string in a non-English reply is reviewed text or is labeled unverified with the original shown.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: unchecked-translation-in-high-stakes-text
runs: pre_send
reads: [reply.language, string.critical, string.reviewed_id, reply.numeric_tokens, source.numeric_tokens]
trigger: a reply in a non-English language contains a string tagged critical
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Show in English", "Talk to a person", "Something else"]
on_miss: rewrite
metric: human-rated accuracy on critical strings
counter_metric: replies labeled unverified when reviewed text existed
status: proposed
```

## 8. Related patterns
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): how service quality varies by dialect or name. This page is about wrong content in translated critical text, not unequal quality across users.
- [Language barrier failures (voice)](../../../../speech-and-audio/goals/conversation-flow/failures/language-barrier-failures.md): a voice agent cannot understand an unsupported language. Here the language is supported, but critical text is not checked.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass on when the user moves to a person.
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): do not answer a language request with a dead end.

I searched this repository for "translation" and "locale". The closest existing pages are the first two above; no page covers checking translated critical text, which is why this one exists.

## 9. Common questions
### Is AI translation safe for medical or billing text?
Not without a check. The one medical study I read in summary found most sentences correct but some errors with potential for harm ([section 4](#4-why-it-matters)). Use reviewed text for critical strings.

### Should a chatbot say when a translation is unverified?
Yes, for critical text with no reviewed version. Say it in the user's language and show the original. Do not label ordinary chat the same way.

### Does every translated reply need a human to review it?
No. This page asks for review of strings tagged critical. A rule that applies to health programs, 45 CFR 92.201, ties review to critical or accuracy-essential text. Check with counsel what applies to you.

### Can the bot check its own translation?
A back-translation check helped physicians catch a high-risk error in one experiment, but that study had one language pair and was about physician judgment. Treat it as a screen, not a substitute for review.

---
## Technical section

### T1. Solution architecture
```
reply draft -> language detect -> critical-string match (registry)
            -> reviewed text found? yes: swap in, log version
                                     no: add "unverified" label + source text
            -> numeric compare (amounts, dates) -> render + log
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Tagged strings come only from the reviewed store | Reply composer | Log scan for empty `reviewed_id` |
| Figures in reply equal figures in source | Pre-send check | Test 3 |
| "Reviewed" label requires a reviewer record | Label renderer | Audit of labels |

### T3. Evals
- **Dataset:** 50 critical strings per supported language with reviewer-approved translations and 50 with deliberate errors (dropped fee, swapped date).
- **Judge rubric:** a bilingual reviewer rates each reply: same amounts, dates and duties as the source (yes or no).
- **Metrics and starting thresholds:** accuracy on critical strings over 98%; unlabeled unverified text 0. Starting points to tune.
- **Release gate:** block a release if a new critical string has no reviewed translation for a supported language.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Number or date mismatch | Any | More than 3 in a day | Pull the replies; switch the string to the English original |

### T5. Trade-offs
- Reviewed translations cost money and time per language and per policy change; unverified labels are a stopgap.
- More languages mean more strings to review; consider supporting fewer languages for critical flows.

---
### Deep dive
- **Open question.** I found no study of chatbot translation of billing or legal text, and the medical studies use one system and one or two languages.
- **References.** [AHRQ PSNet summary of Khoong et al. 2019](https://psnet.ahrq.gov/issue/assessing-use-google-translate-spanish-and-chinese-translations-emergency-department) (opened; summary); [Mehandru et al., EMNLP 2023](https://ar5iv.labs.arxiv.org/html/2310.16924) (opened); [45 CFR 92.201, Cornell LII](https://www.law.cornell.edu/cfr/text/45/92.201) (opened).
