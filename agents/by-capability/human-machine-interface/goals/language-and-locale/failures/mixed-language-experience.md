# Chatbot Replies in Two Languages at Once: Mixed-Language Experience

<!-- SEO
title: Chatbot Mixes Languages in One Reply: How to Fix It
description: Buttons, errors, or scripted lines stay in English while the reply is in Spanish. Cover every string in a supported language or fall back for the whole reply.
search phrases:
- chatbot replies in two languages
- chatbot mixing english and spanish in same response
- chatbot buttons not translated
- chatbot system messages not translated
- chatbot partially translated
- untranslated strings in multilingual chatbot
- ai answers translated but predefined messages stay in original language
- chatbot falls back to english for some messages
-->

**Frequency**: Common

## Issue: Part of a chat reply is in the user's language and part is not (buttons, errors, scripted lines, retrieved articles); the fix is full string coverage for every supported language, one reply language per message, and a whole-reply fallback with a notice.

> **One line:** The user writes in Spanish and gets a Spanish answer wrapped in English buttons, an English error, or an English paragraph pasted from a help article.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice (spoken replies that switch language) is covered by an older page, linked in section 8; any voice signal here is PLANNED, not detected or measured. Web widget chrome is PLANNED. |
| **Stakes** | Low to medium. Higher when the English part is a deadline, a fee, a consent line, or an error with the next step. |
| **Who is affected** | Users of any language the product lists as supported, other than the default. English-only users rarely see it. |
| **Frequency** | Common in multilingual deployments (our judgment). I found public user reports on several platforms but no study that measures how often it happens. |
| **Pattern ID** | mixed-language-experience |
| **Family** | Language and locale ([family README](../README.md)) |
| **Goal** | Users are understood and answered in the language, reading level, and format that work for them. For this pattern: a supported language is fully supported. |
| **Primary metric** | Localization coverage of strings. Target: 100%; mixed-language reply rate under 1%. Targets are starting points to tune. |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | Partly. A stronger model helps when the model itself drifts into another language in a generated reply, but scripted strings, missing translations, and retrieved English articles are product and content problems a model will not fix. (Our judgment, not tested.) |
| **Also searched as** | chatbot partly in English · chatbot widget half translated · bot answers in Spanish but buttons in English · multilingual chatbot default language fallback · chatbot error message in English · chatbot Spanglish reply |

## 1. In plain words
The bot answers in the user's language, but some pieces around the answer are in another one: the quick-reply buttons, the "I didn't understand" line, a greeting, or a help article pasted in whole. The user has to read two languages to finish one task. The fix is to treat "supported" as "every string the bot can show exists in that language," and when one is missing, to switch the whole reply, say so, and offer a choice.

## 2. What it looks like
**Without the fix** (illustrative: Spanish-language chat for a U.S. electric utility)
```
User: Hola, necesito pagar mi factura de luz antes del viernes.
Bot:  Con gusto le ayudo. Puede pagar con tarjeta o con su cuenta bancaria.
      [Pay now] [View bill] [Talk to an agent]
User: ¿Cuándo se aplica el pago? Mi fecha límite es el viernes.
Bot:  Sorry, I didn't understand that. Please choose an option below.
User: Quiero hablar con una persona.
Bot:  Transferring you to an agent. Please hold.
```
**With the fix**
```
User: Hola, necesito pagar mi factura de luz antes del viernes.
Bot:  Con gusto le ayudo. Puede pagar con tarjeta o con su cuenta bancaria.
      [Pagar ahora] [Ver factura] [Hablar con una persona]
User: ¿Cuándo se aplica el pago? Mi fecha límite es el viernes.
Bot:  No tengo esa información confirmada. Puede verla en "Ver factura", o puedo pasarle con una persona.
      [Ver factura] [Hablar con una persona] [Otra cosa]
```
The buttons, the fallback line, and the handoff are all in Spanish, and the "I don't know" line says what the bot cannot confirm and gives next steps. (The bot's answer to the payment-date question depends on the company's rules, so the fixed bot does not invent one.)

## 3. Why it happens
- **Scripted text and generated text come from different systems.** Generated answers can follow the user's language while buttons, system topics, and canned messages come from string files that someone has to translate. Microsoft's docs say that after secondary languages are added, you must supply translations for topic messages, while generated messages are translated automatically (section 4). A user of one chatbot widget reported exactly this split.
- **A missing or stale string falls back, often per string.** Fallback usually fills the one missing key with the default language, so one reply can be half and half. Edited source text can leave the old translation in place, out of sync with the new source (section 4).
- **The model itself can switch language inside a reply.** Research on language confusion found models that wrote some lines, or single words, of a response in an unintended language (section 4). This is the smaller of the three causes for most products (our judgment).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In Copilot Studio, the agent picks the language from the browser; with no match it uses its primary language. After you add secondary languages you provide translations for messages in your topics, while generated messages are translated automatically. Messages added in the primary language but not translated show in the primary language. Changed primary-language strings keep their old translation, so the two can drift apart. | [Microsoft Learn, Configure and create multilingual agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/multilingual) (page dated 2026-04-14). Opened. | One vendor's product documentation. It documents behavior, not how often users see it. Other platforms differ. |
| An Elfsight AI ChatBot user on a hotel website (post dated Sept. 30, 2025) reported that answers followed the visitor's language but predefined messages stayed in Italian. An Elfsight staff reply said multilingual versions of the widgets were not supported then; it was on a wish list. | [Elfsight Community thread](https://community.elfsight.com/t/how-to-make-predefined-chatbot-messages-multilingual/140139). Opened. | One user report and one vendor reply. It shows the split exists, not how common it is. The product may have changed since. |
| Marchisio, Ko, Bérard, Dehaze and Ruder (Cohere) tested 15 languages. Line-level pass rates (no line in the wrong language) in the monolingual test averaged 98.6 to 99.3 for the Command and GPT models and 48.3 to 73.0 for the Llama 2, Llama 3, and Mistral models. In the cross-lingual test (prompt in one language, reply requested in another), Llama 3 70B Instruct averaged 30.3 and GPT-4 Turbo 90.3. Higher sampling temperature increased confusion. | [Understanding and Mitigating Language Confusion in LLMs, arXiv 2406.20052v3](https://arxiv.org/html/2406.20052v3). Opened; I read the first 100,000 of about 116,689 characters, and the figures come from the page's tables as returned by the fetch tool. | arXiv version; I saw no venue named on the page. Authors work at a model vendor. Models are from 2024 and earlier; current models are not covered. It measures model-generated text, not scripted strings. Single source for these numbers. |
| An Apple engineer said, in a Sept. 2024 developer forum reply, that fallback happens for the whole app bundle and not per string. They added that a language you support should be fully supported, not partly localized. | [Apple Developer Forums thread 764972](https://developer.apple.com/forums/thread/764972). Opened. | A forum answer about iOS String Catalogs, not a chatbot. I use it only for the "fully supported" principle. |
| A localization vendor's glossary says a fallback chain is an ordered list of locales tried when a string is missing, keeps chains to two or three levels, and says fallback fires only when the key is absent, so an empty or null value shows as blank. | [Localazy, Fallback chain](https://localazy.com/dictionary/fallback-chain). Opened. | Vendor glossary page, no study. Used only for the "empty value is not a missing key" check. |
| Canva's developer docs warn that bad localization can give a "confusing mix of languages," and say not to render untranslated strings returned by your backend; map error codes to predefined messages instead. | [Canva Apps SDK, Bad practices](https://www.canva.dev/docs/apps/localization/bad-practices/). Opened. | Developer advice for app interfaces built on one SDK, not a chatbot study. |

**Public incident.** I found no dated public incident of a named company's chatbot. The Elfsight thread above and the Apple thread are individual developer reports, not incidents.

**Read only in search summaries, not used in the fix:** user reports about Zoho SalesIQ (Portuguese and English in one widget), Mibew (German and English in one chat window), and Pega (default system replies outside localization by default), and a SharePoint Europe write-up on Copilot localization. I did not open them.

## 5. The fix
**The principle:** A language is either fully supported (every string, button, error, and retrieved snippet exists in it) or it is not offered; when something is missing, change the whole reply, say so, and let the user choose.

**Do this**
1. **No language ships as "supported" below 100% string coverage.** Before a language appears in a language list or is auto-selected, every user-visible string key has a non-empty, current translation. Check: coverage = translated non-stale keys / total keys, 100% for each listed language in the release build.
2. **One reply language per message.** Buttons, quick replies, scripted lines, and generated text in one message use the same language. Check: language ID on each line and each button label matches the reply language, except for the allowed items in the "Don't over-correct" paragraph.
3. **A missing string never fills in silently from another language.** If any string for this message is missing in the user's language, send the entire message in the fallback language (the default, or one the user chose), with a one-line notice written in a string that exists in every supported language. Check: no message contains two languages; a `string_fallback` event is logged.
4. **Label anything from outside.** Knowledge-base text, backend errors, and tickets in another language are not pasted in unlabeled. Say in the user's language that the source is in English, and offer it. Check: every cross-language excerpt follows a notice naming its language.
5. **Mark a translation stale when its source changes.** Edited source text invalidates the old translation until it is re-reviewed. Check: a build with stale keys for a listed language fails the release.
6. **Empty is missing.** A key with an empty or null value counts as untranslated. Check: coverage counts these.
7. **Scripted and fallback paths are in the test set.** Tests walk the "I didn't understand," timeout, handoff, and error paths in each language, not only the happy path. Check: the test set lists these paths per language.

**Reference design**
```
Reply assembly (per message)
- reply_language = session language (user's last stated or detected language, else default)
- parts = generated text + scripted lines + button labels + attachments
- if any part lacks a current string in reply_language:
    reply_language = fallback_language (never mix)
    prepend notice_key "language_fallback" (exists in every supported language)
    log string_fallback {key, wanted, used}
- external excerpt in another language: label it, then offer it as a choice
- offer_choices: ["Read it in English", "Switch to English", "Talk to a person", "Something else"]
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The reply can be fully written in the user's language: answer in it, buttons included. |
| Admit uncertainty and show how to check | A needed string or article exists only in another language: say so in the user's language and name what is available. |
| Offer choices: 2-4 options plus "Something else", free text open | After that notice: "Read it in English", "Switch to English", "Talk to a person", "Something else". |
| Hand off to a person | The user says twice they cannot read the reply, or the text is a deadline, fee, or consent line (see [unchecked translation in high-stakes text](unchecked-translation-in-high-stakes-text.md)). |

**Don't over-correct.** Do not flag brand and product names, people's names, street addresses, code, quoted user text, or loanwords as mixing. If the user writes in a blend of languages, or asks for an English term, keep their terms. Do not refuse to answer because the only source is in another language: label it and offer it. Do not hide a language from users who need it because it is below 100%; instead fix the gap or show the whole-reply fallback.

**Hand-off rule.** Hand off to a person when the user asks twice for a language the bot cannot fully serve, or when the missing text carries money, deadline, legal, or health meaning. Say that in the user's language.

**Framework used:** [Conversation repair](../../../solutions-library/conversation-repair.md) for the admit-and-offer step. The coverage gate and fallback come from localization practice in the sources above; I found no standard that sets a target.

## 6. How to test it (short version)
Tests are **not yet run**. Run each in at least two non-default languages (for example Spanish and Vietnamese).

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | List every string key for a language and mark empty or stale values | Coverage 100% before the language is listed (rules 1, 5, 6) |
| 2 | Spanish user asks a normal question; check the reply and its buttons | Every line and label is Spanish (rule 2) |
| 3 | Delete one button translation in a test build | Whole message falls back, a notice appears, and `string_fallback` is logged (rule 3) |
| 4 | Ask something whose only help article is in English | Reply says so in Spanish and offers the article as a choice (rule 4) |
| 5 | Edit a source string and keep the old translation | Release check fails on the stale key (rule 5) |
| 6 | Send nonsense to trigger "I didn't understand," then ask for a person | Both messages are in the user's language (rule 7) |
| 7 | User writes "Quiero un refund de mi last bill" | Reply keeps the user's terms and is not flagged (Don't over-correct) |
| 8 | User says twice "No leo inglés" after an English-only article | Handoff offered in Spanish (hand-off rule) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Localization coverage of strings. Target: 100%; mixed-language reply rate under 1%** (primary) | 100% coverage; under 1% mixed replies | Coverage from the string catalog per language each build; mixed rate from a language-ID check on each line and button label of a sample of sent replies, reviewed by a native speaker | Any listed language under 100%; mixed rate over 2% |
| String fallbacks per 1,000 replies | Track; set from baseline | Count `string_fallback` events | Rising week over week |
| Stale keys at release | 0 | Compare source-text hash with the hash stored at translation time | Any |
| Users who switch language right after a fallback | Track; set from baseline | Language change within 2 turns of a notice | Rising |
| False mixed-language flags (counter-metric) | Under 5% of flags | Native reviewer checks flagged replies for names, loanwords, quoted text | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A reply or button label whose language ID differs from the session language | Per-line language ID on the draft reply | Brand name, address, code, or the user's own words |
| User asks "in Spanish please" or "no entiendo" after a bot reply | Next user turn matches a language request | A real change of language preference (see LG-03, language switch ignored) |
| The next user turn repeats the same request | Same intent in the next user turn | A deliberate retry that succeeds |
| `string_fallback` event, or a key with an empty value | Reply assembly log; catalog scan | A planned fallback with a notice shown |
| User clicks a button but then types the same thing | Button click followed by a typed message with the same intent | The user wanted to add detail |

**Starter rule:** every part of one bot message, buttons included, is in a single language, and a missing string switches the whole message to the fallback language with a notice.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: mixed-language-experience
runs: pre_send
reads: [draft_reply.segments, draft_reply.language_id, session.reply_language, string_catalog.coverage, retrieved_doc.language]
trigger: a part of the draft reply is in a language other than the session reply language, or a needed string is missing
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Read it in English", "Switch to English", "Talk to a person", "Something else"]
on_miss: rewrite
metric: localization coverage of strings; mixed-language reply rate
counter_metric: false mixed-language flags
status: proposed
```

## 8. Related patterns
- [Multilingual code-switching failures](../../../../speech-and-audio/goals/conversation-flow/failures/multilingual-code-switching.md): the closest page. It is a voice page about an agent that drifts between languages or over-mixes within spoken lines, and it includes no string-coverage or fallback fix. This page is for text chat and is about parts of the product (buttons, scripted lines, retrieved articles) that lack a translation.
- [Language barrier failures](../../../../speech-and-audio/goals/conversation-flow/failures/language-barrier-failures.md): an unsupported language, or the whole reply in the wrong language (catalog rows LG-01, LG-03). Here the right language is used for part of the reply.
- [Input locale mismatch](../../../../../cross-cutting/operations/goals/input-output-handling/failures/input-locale-mismatch.md): date, number, and currency formats, not the language of the words.
- [Unchecked translation in high-stakes text](unchecked-translation-in-high-stakes-text.md): translated text that is wrong or unreviewed. Here the problem is text that is not translated at all.
- [Language mismatch misroute](../../../../../by-use-case/support-services/goals/ticket-routing/failures/language-mismatch-misroute.md): tickets sent to a team that cannot read the language.

## 9. Common questions
### Why does my chatbot answer in Spanish but show English buttons?
Usually the answer is generated and follows the user's language, while the buttons come from a string file that was never translated or was filled in from the default language. One user thread I opened describes this split (section 4). Fix it with rules 1 to 3.

### Should a chatbot fall back to English when a translation is missing?
Fall back for the whole message and say so, rather than one string at a time. A per-string fallback gives a half-translated reply. Fallback also does not cover empty values (rule 6).

### Is it a problem if the user mixes English and Spanish?
No. Keep the user's own terms and do not flag them (see "Don't over-correct").

### How do I check my multilingual bot for untranslated strings?
Export every string key for each language, mark empty and stale values, and count coverage. Then run the error, timeout, and handoff paths in each language (section 6, tests 1 and 6).

---
## Technical section

### T1. Solution architecture
```
string catalog (key, source_hash, translated_hash, value)
  -> release gate: coverage = 100% per listed language, 0 stale, 0 empty
draft reply (generated + scripted + buttons)
  -> language-ID per line and label (sample)
  -> mismatch or missing key? -> whole-message fallback + notice + log
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| 100% coverage to list a language | Build step | Test 1 |
| One language per message | Pre-send check | Tests 2, 3 |
| Whole-message fallback with notice | Reply assembly | Test 3 |
| External excerpts labeled | Retrieval step | Test 4 |
| No stale keys | Build step | Test 5 |

### T3. Evals
- **Dataset:** 50 prompts per supported language covering normal answers, "I didn't understand," timeout, error, handoff, and an English-only help article; have native speakers write and rate them.
- **Judge rubric:** is every line and button in the reply language, apart from names and quoted user text?
- **Metrics and starting thresholds:** coverage 100%; mixed-language reply rate under 1%. Starting points to tune; I found no source for them.
- **Release gate:** block a release if a listed language is under 100% or any test message contains two languages.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Mixed-language reply rate | Over 1% | Over 2% | Check the last string, prompt, or model change |
| `string_fallback` events | Rising | Spike after a deploy | Find the missing keys |

### T5. Trade-offs
- A 100% gate can delay a language launch; show only complete languages, or ship with a clear whole-message fallback.
- Language ID is weak on short text and on names; sample and have a native speaker review flagged items.
- Fallback to English may not be useful for every user; the choice set lets them pick.

---
### Deep dive
- **Open question.** I found no study that measures how often chatbot users see mixed-language replies in production. The evidence is product documentation, forum reports, and one model-level study.
- **Voice.** PLANNED. Mixed-language handling in spoken replies is in the older code-switching page; nothing here was measured on voice.
- **References.** [Microsoft Learn multilingual agents](https://learn.microsoft.com/en-us/microsoft-copilot-studio/multilingual); [Elfsight thread](https://community.elfsight.com/t/how-to-make-predefined-chatbot-messages-multilingual/140139); [Language confusion paper](https://arxiv.org/html/2406.20052v3); [Apple forum](https://developer.apple.com/forums/thread/764972); [Localazy](https://localazy.com/dictionary/fallback-chain); [Canva](https://www.canva.dev/docs/apps/localization/bad-practices/). All opened.
