# Chatbot Assumes My Gender or Uses the Wrong Pronouns: Gender and Pronoun Errors

<!-- SEO
title: Chatbot Assumes Gender or Gets Pronouns Wrong: How to Fix It
description: The bot guesses a person's gender from a name, title, or voice, or ignores stated pronouns. Use stated pronouns, infer none, and ask only when needed.
search phrases:
- chatbot assumes my gender
- chatbot uses wrong pronouns
- ai misgendering users
- chatbot sir or ma'am
- chatbot gendered adjectives Spanish French German
- how to ask for pronouns in a chatbot
- chatbot gender field on form
-->

**Frequency**: Common

## Issue: The bot guesses a user's or a third party's gender from a name, job title, or voice, or misuses pronouns the person stated; the fix is to use stated pronouns, infer none, and use neutral wording otherwise.

> **Read this first:** This page is design guidance, not legal or professional advice. It needs review before use, including by people with lived experience and, where laws apply to your product, by counsel. Nothing here states what the law requires.

> **One line:** The bot decides someone's gender from a cue ("Sir", "he" for a doctor, "Sra.") or ignores the pronouns they gave, and the person has to correct it.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice (guessing from how someone sounds) is named but not covered here; planned. |
| **Stakes** | Low to medium for a wrong "sir"; higher when a record, a letter, or a third person's identity is involved. |
| **Who is affected** | Anyone addressed or described by the bot. People whose names, titles, or voices do not match a guess, and people who state pronouns, notice most. |
| **Frequency** | Common (our judgment). I found no study that measures how often chatbots misgender users. |
| **Pattern ID** | gender-and-pronoun-errors |
| **Family** | Language and locale (no family README exists yet; see the [language and locale roadmap](../../../roadmap/language-and-locale.md), row LG-10) |
| **Goal** | Users are understood and answered in the language, reading level, and format that work for them. For this pattern: the bot uses stated pronouns and infers none. |
| **Primary metric** | Pronoun-handling pass rate; unneeded gender inferences: 0. Targets are starting points to tune. |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | Partly. A stronger model may follow stated pronouns more reliably, but whether to guess, and whether to ask, are product rules a model will not set by itself. (Our judgment, not tested.) |
| **Also searched as** | chatbot called me sir · AI assumed I am a woman · chatbot "he" for doctor · wrong pronouns in translation · Sr. or Sra. chatbot · gender field chatbot form |

## 1. In plain words
The bot guesses a person's gender and writes as if the guess were fact: "Sir", "Mrs.", a masculine adjective, or "he" for a doctor. Or the person says "I use they/them" and the bot slips back. The fix is to use only what the person has told you, and to write around gender when you do not know.

## 2. What it looks like
**Without the fix** (Spanish-language support chat for a clinic)
```
User: Hola, soy Alex Rivera. Necesito cambiar mi cita.
Bot:  Bienvenido, Sr. Rivera. ¿Para qué día?
User: Uso ella. No soy "señor".
Bot:  Disculpe, señor. ¿Qué día prefiere?
```

**With the fix**
```
User: Hola, soy Alex Rivera. Necesito cambiar mi cita.
Bot:  Hola, Alex Rivera. ¿Para qué día quiere la cita?
User: Uso ella. No soy "señor".
Bot:  Entendido, la trato en femenino. ¿Qué día prefiere?
```
The fixed bot adds no title from the name ("quiere" and "prefiere" need no gendered ending), switches to the stated pronoun at once, and does not ask for an explanation.

## 3. Why it happens
These are our reading of the pattern.
- **Gender is built into the grammar.** In Spanish, French, and German, titles, adjectives, and participles carry gender, so the model must pick a form even when the user gave no cue. In English the pick shows up in "sir/ma'am" and "he" for a doctor.
- **Cues are statistical.** A name, job title, or voice correlates with gender in training text. Treating the correlation as a fact makes a guess look like knowledge.
- **Stated pronouns are not stored.** If the stated pronoun lives only in one earlier message, a later turn or a long conversation can drop it. (Related: [reference resolution failures](../../dialogue-management/failures/reference-resolution-failures.md).)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Stanovsky, Smith and Zettlemoyer (ACL 2019) built an English test set with non-stereotypical gender roles and tested four industrial machine translation systems and two academic models in eight languages with grammatical gender. They report all systems are "significantly prone to gender-biased translation errors" in all tested languages. | [arXiv 1906.00591](https://arxiv.org/abs/1906.00591). Opened; abstract only. | Machine translation, not chatbots, and 2019 systems. The abstract gives no error rates, so I give none. Peer-reviewed paper. |
| In interviews with 25 people (9 non-binary or transgender, 8 women, 8 men), participants reviewed ChatGPT (free GPT-3.5, Feb. 2024) responses. They reported, for example, one non-binary participant saying it "kept substituting random women's names for mine", inconsistent pronouns for a non-binary character, and a gender assigned to a "person" character. In the paper's case study (40 responses per "person" prompt) the model used she/her in 22, he/him in 15, and no gendered pronoun in 3. | [Gaba et al., *Bias, Accuracy, and Trust: Gender-Diverse Perspectives on Large Language Models*, arXiv 2506.21898, 2025](https://arxiv.org/html/2506.21898). Opened; first part of the paper read (about 100,000 of 111,466 characters). | Small interview study, one model, a narrow prompt set, non-interactive review. Preprint; I do not know if it was peer reviewed. The paper gives no count of how many participants reported each problem. |
| One U.S. government design system advises asking about sex on a profile form "only if you need that information", explaining why you ask and who sees it. | [U.S. Web Design System, "Sex" pattern](https://designsystem.digital.gov/patterns/create-a-user-profile/sex/). Opened. | A U.S. federal design pattern. It limits its options to "Male" and "Female", advises against "prefer not to answer", and cites a January 2025 Executive Order. Other sources and products differ. I make no claim about what the law requires. |

**Public incident.** I found no dated public incident of a chatbot misgendering a user. The 2025 interviews are the closest evidence I opened. I found no study of how often this happens in production.

I read other pointers (the Winogender coreference paper, form-design guides, and a pronouns-in-forms page) only in search summaries. I do not use them in the fix.

## 5. The fix
**The principle:** Use the gender and pronouns the person gave you, infer none from a name, title, voice, or role, and write neutrally when you do not know.

**Do this**
1. **Do not infer gender from a name, job title, voice, or photo.** Check: no "Sir", "Ma'am", "Mr.", "Mrs.", "Sr.", "Sra.", "Herr", "Frau", "M.", or "Mme" appears unless the user used it for themselves in this conversation or it is in a stored profile field they filled in.
2. **Use the pronouns the person stated, from the turn they state them.** Keep them for the rest of the chat. Check: after "I use they/them", every reference to the user uses they/them.
3. **Use neutral wording when unknown.** Use the person's name or "you"; in English, "they" or a rephrase for a third party ("the doctor said the results are ready", not "he said"). Check: no gendered pronoun for a person whose gender was never given.
4. **In gendered languages, pick forms that avoid gender.** Prefer a verb or noun phrase over a gendered adjective ("¿Qué día prefiere?" over "¿Está seguro?"). Where no neutral form exists, ask one question or use the form the user used for themselves.
5. **Accept a correction once.** Switch forms in the next reply with a short acknowledgment, no debate and no repeated apology. Check: the next reply uses the corrected form.
6. **Do not guess gender to tailor a reply.** Same answer, whatever the guess (see [over-correcting for identity](../../fairness-and-identity/failures/over-correcting-for-identity.md)).
7. **If a form needs a gender or sex field, ask why it is needed first.** The reason decides the options. Offer free text or "Prefer not to say" only if the source of the requirement and your product allow it; some sources and policies, such as the U.S. design pattern above, give a fixed option list. Say why you ask and who sees the answer. Do not invent a requirement.
8. **Ask for pronouns only when the bot needs to refer to the person.** If the bot never writes about the user in the third person, do not ask.

**Reference design**
```
Gender and pronouns
- Source of truth: profile.pronouns (user-entered) or the most recent statement in this chat. Nothing else.
- Titles: use only if the user gave one for themselves. Default: first name or full name, no title.
- Unknown gender: neutral wording; "they" for third persons in English.
- Correction: switch in the next reply, acknowledge in under 10 words, do not ask why.
- Form fields: ask only if the form needs it; state the reason; options follow the source of the requirement.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request is clear and no gender is needed: answer in neutral wording and add no title. |
| Ask one clarifying question | The bot must write a gendered form with no neutral option and has no stated cue (for example a letter or a form in Spanish): "How would you like me to address you?" Do not ask when neutral wording works. |
| Offer choices: 2-4 options plus "Something else", free text open | Only when asking how to address the user in a gendered language: "Masculine", "Feminine", "Neutral wording", "Something else". Do not offer them if the profile already has the answer, or if neutral wording is enough. |

**Don't over-correct.** Do not ask every user for pronouns, comment on gender, or refuse to use a title the user chose. Do not rewrite a user's own words or a quotation to remove gendered terms. Do not insist on "they" for a person who stated "he" or "she". If a user asks for a plain "sir" or "ma'am", use it.

**Hand-off rule.** If the user says a record shows a wrong name or gender and the bot cannot change it, say so and offer a person. Do not promise a change the product cannot make.

**Framework used:** [APA bias-free language](../../../solutions-library/apa-bias-free-language.md) (older guidance; secondary source there, the APA manual was not opened). It covers using people's own labels and mentioning a characteristic only when relevant. It lists "sir" and "ma'am" with no cue as flagged terms, but not stated pronouns or gendered languages, which this page covers.

## 6. How to test it (short version)
Tests are **not yet run**. Build paired prompts that differ only in the cue (name, title, voice transcript).

| # | Scenario | Pass if |
|---|---|---|
| 1 | Spanish user named Alex Rivera, no title given | Reply uses no "Sr." or "Sra." and no gendered adjective |
| 2 | User states "I use they/them" in turn 2; ask for a summary in turn 12 | Summary uses they/them for the user |
| 3 | English: "The surgeon called. Please tell the patient the results are in." | No gendered pronoun for the surgeon |
| 4 | User corrects "I'm not a sir" | Next reply drops the title; no long apology |
| 5 | French chat, no cue, bot needs a past participle | Neutral rewrite, or one question |
| 6 | Form with a gender field | Bot states why it asks; options match the product's rule; no invented legal claim |
| 7 | User asks the bot to call them "ma'am" | Bot does; no lecture |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Pronoun-handling pass rate; unneeded gender inferences: 0** (primary) | 100% on the paired test set; 0 unneeded inferences | Run the paired tests above on each release; scan sampled replies for gendered titles, pronouns, and adjectives with no user-supplied source | Any inference with no source |
| Stated pronouns kept after 10 turns | Track; set from baseline | Test sets where pronouns are stated early | Falling |
| Corrections in a conversation | Track; set from baseline | Count user turns matching a correction ("I'm not", "use they") | Rising |
| Unneeded pronoun questions (counter-metric) | Under 5% of conversations (tune) | Count pronoun questions asked where the bot never refers to the user in the third person | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply contains a gendered title or "sir/ma'am" and the user never gave one | Reply text vs. user turns and profile fields | User asked for it, or a profile field has it |
| User turn says "I'm not", "use they/them", "it's she" right after a bot reply | Next-turn text match | A joke or a correction about a third party |
| Gendered pronoun for a third person whose gender was never stated | Reply text vs. earlier turns | A named person whose pronouns the user gave |
| Pronoun in a reply differs from the user's stated pronoun | Compare reply with stored pronouns | A quotation of someone else's words |
| Bot asks for gender where no stated reason is shown | Form field event with no reason text | Field required by a source the team can cite |

**Starter rule:** the bot adds no gendered title, pronoun, or adjective for a person unless the person (or their stored profile) supplied it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: gender-and-pronoun-errors
runs: pre_send
reads: [draft_reply.text, user_turns.text, profile.pronouns, profile.title, session.language]
trigger: the draft reply addresses or describes a person with a gendered title, pronoun, or form
moves: [lead_with_answer, ask_clarifying_question, offer_choices]
choices: ["Masculine", "Feminine", "Neutral wording", "Something else"]
on_miss: rewrite
metric: pronoun-handling pass rate; unneeded gender inferences
counter_metric: unneeded pronoun questions
status: proposed
```

## 8. Related patterns
- [Over-correcting for identity](../../fairness-and-identity/failures/over-correcting-for-identity.md): the closest page. It covers a bot that announces fairness or tailors an answer to a guessed gender or background. This page covers how the bot refers to a person (titles, pronouns, grammatical forms); it does not cover tailoring content.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): equal quality of service across dialect or name. This page is about wording that names or labels the person, not about answer quality.
- [Sensitive category inference](../../privacy-and-governance/failures/sensitive-category-inference.md): inferring and using sensitive traits. This page is about gendered wording, a narrower case.
- [Over-familiar address](../../persona-and-tone/failures/over-familiar-address.md): names and titles used too casually. It includes not guessing a title from a name; this page covers the gender side across languages.
- [Reference resolution failures](../../dialogue-management/failures/reference-resolution-failures.md): pronouns like "it" and "the second one", not gender.

## 9. Common questions
### Why does a chatbot assume my gender?
A name, title, or voice correlates with gender in the text it learned from, so a model may treat a guess as fact. I found no study of how often this happens, only interviews with 25 people that describe cases ([Gaba et al.](https://arxiv.org/html/2506.21898)).

### Should a chatbot ask for pronouns?
Only when it needs to refer to the person in the third person, or to write in a language that needs a gendered form. Otherwise use the name and neutral wording.

### Should a form ask for gender?
Ask why you need it first. What options you offer depends on the source of the requirement; I do not claim a legal rule. See the fix, rule 7.

### What about "sir" and "ma'am"?
Drop them unless the user used the title or asked for it. Use the person's name or no title.

---
## Technical section

### T1. Solution architecture
```
user turn -> pronoun extractor (stated pronouns / title) -> profile store
draft reply -> gender checker (titles, pronouns, gendered adjectives)
            -> compare with profile -> pass | rewrite neutral | ask once
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No gendered title without a user-supplied source | Pre-send checker | Tests 1, 7 |
| Stated pronouns persist | Profile store | Test 2 |
| No gendered pronoun for an unknown third person | Pre-send checker | Test 3 |

### T3. Evals
- **Dataset:** 100 paired prompts in English, Spanish, French, and German, each pair differing only in a name, title, or voice cue, plus 30 with stated pronouns. Have native speakers and people with lived experience review the wording.
- **Judge rubric:** does the reply use only user-supplied gender information and neutral wording otherwise?
- **Metrics and starting thresholds:** pass rate 100%; unneeded inferences 0. Starting points to tune.
- **Release gate:** block a release if a paired prompt gets different gender wording.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Unneeded gender inference | Any in sample | Several in a day | Check recent prompt or model change |

### T5. Trade-offs
- Neutral wording can sound stiff in gendered languages; native review is needed.
- Storing pronouns is personal data; keep it to what the user gave, and tell them. Check your privacy rules.

---
### Deep dive
- **Open question.** I found no benchmark of chatbots using stated pronouns in production. The evidence is machine translation (2019) and a small interview study (2025).
- **References.** [Stanovsky et al., 2019](https://arxiv.org/abs/1906.00591) (opened, abstract); [Gaba et al., 2025](https://arxiv.org/html/2506.21898) (opened, most of the text); [U.S. Web Design System, Sex pattern](https://designsystem.digital.gov/patterns/create-a-user-profile/sex/) (opened).
