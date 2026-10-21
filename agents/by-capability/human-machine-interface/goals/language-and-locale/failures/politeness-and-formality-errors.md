# Chatbot Uses "Tú" When the Customer Wrote "Usted": Politeness and Formality Errors

<!-- SEO
title: Chatbot Uses Tú, Customer Wrote Usted: Formality Errors
description: Why a chatbot picks the wrong formal or informal address (tu/usted, du/Sie, honorifics) and how to match the user's own register, with native-speaker review.
search phrases:
- chatbot uses tu instead of usted
- chatbot formal vs informal Spanish customer service
- how to make a chatbot use formal address
- chatbot wrong politeness level Japanese Korean
- ai assistant tone too casual for formal user
- tu vs usted chatbot
-->

**Frequency**: Common

## Issue: The assistant answers in the wrong formal or informal register (tu or usted, du or Sie, tu or vous, Japanese or Korean honorific levels, or an English tone that is too casual or too stiff), so a customer who wrote formally gets a casual reply, or the reverse.

> **One line:** The user writes formally and the bot answers casually (or the reverse); the fix is to read the register in the user's own message, keep it for the whole chat, and have a native speaker review the wording.

> **Read this first.** This page is design guidance, not professional advice. Flags: R (needs research) and E (expert review). I could not verify what any group of speakers prefers in a given business setting, so the rules below follow the user's own words and do not assume a preference. Have a native speaker of each supported language, ideally one who knows your product's customers, review every register rule and sample reply before use.

| | |
|---|---|
| **Channel** | Written for **chat** (field chat). Voice and web signals are PLANNED, not written or measured. |
| **Stakes** | Low to medium. Higher for banking, health, legal, and government chats, where tone affects trust. |
| **Who is affected** | Users writing in languages that mark formality, and users whose English register differs from the bot's |
| **Frequency** | Common (our judgment). I found no count of how often chatbots miss register. |
| **Pattern ID** | politeness-and-formality-errors |
| **Family** | Language and locale |
| **Goal** | Register fits the language and context. (Family goal: users are understood and answered in the language, reading level, and format that work for them.) |
| **Primary metric** | Native-rater appropriateness. Start: over 90% (tune; a labeled starting point, not a sourced target). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model reads register cues better and follows an instruction to hold one level, but it still lacks your brand's style rules and the user's relationship to your company. (Our judgment, not tested.) |
| **Also searched as** | chatbot tu vs usted · chatbot too casual · chatbot too formal · wrong honorific chatbot · Spanish chatbot tone · formal address in AI |

## 1. In plain words
Many languages have two or more ways to say "you", and the choice signals respect or closeness. English has no such pronoun, but it still has register: "Dear support team" versus "hey". A bot that picks the wrong one can sound rude, cold, or presumptuous. The fix is to read the user's own message, match it, hold it, and have native speakers check the wording.

## 2. What it looks like
Example: a US bank's chat. A customer writes in formal Spanish about a charge.

**Without the fix**
```
User: Buenas tardes. Quisiera saber si usted me puede ayudar a disputar un cargo de $84.20.
Bot:  ¡Hola! Claro, te puedo ayudar. ¿Me dices cuál es el cargo que quieres disputar?
User: Disculpe, ¿podría hablar con una persona? Prefiero que me traten de usted.
Bot:  ¡Claro que sí! Dime tu número de cuenta y te conecto.
User: (leaves the chat and calls the branch)
```
**With the fix**
```
User: Buenas tardes. Quisiera saber si usted me puede ayudar a disputar un cargo de $84.20.
Bot:  Buenas tardes. Sí, puedo ayudarle. ¿Cuál es el cargo que desea disputar? Puede decirme el comercio y la fecha.
User: El de Mercado Latino, del 3 de octubre.
Bot:  Lo encuentro. ¿Desea que abra la disputa por $84.20, o prefiere revisar primero el detalle del cargo?
User: Abra la disputa, por favor.
Bot:  Listo. Su caso quedó abierto. Le enviaremos una respuesta por escrito.
```
The fixed bot uses "usted" forms (ayudarle, desea, su caso) from the first reply and never drops them. The "before" bot also ignored an explicit request for "usted".

The reverse case: a user writes "oye, ¿me puedes ayudar con mi tarjeta?" and the bot answers "Estimado cliente, le informamos que...". Matching the user here means "tú" forms, within your style guide.

## 3. Why it happens
- **No register rule in the prompt.** The system prompt says "friendly and casual" in English and says nothing about languages that mark formality, so the model picks a form on its own.
- **The prompt's tone leaks across languages.** An English style such as "warm and casual" can carry over as informal address in a language where that choice carries meaning.
- **The register is not tracked across turns.** The model matches the user's first message, then drifts back to its default after a long answer, a tool result, or a canned template written in another register.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A language-learning guide says Spanish "usted" shows respect and "is used to address elders, authority figures, and some strangers", and that in Rioplatense Spanish "vos" is the equivalent of "tú". | [Tell Me In Spanish, *Tú vs Usted*](https://www.tellmeinspanish.com/grammar/formal-vs-informal-you-in-spanish/). Opened and read. | Secondary, a language-learning site. It does not discuss customer service, so it does not tell you what customers expect from a bank. |
| A university Spanish course page quotes one interviewee: "usted" is a way of speaking with respect, and with peers at the start of a relationship "tú" may be better. | [Lumen Learning, Spanish 1, *Formal o informal*](https://courses.lumenlearning.com/wm-spanish1/chapter/formal-o-informal/). Opened and read. | One speaker's view in a course interview, not a survey. It does not address business settings. |
| Prompting can steer machine translation formality: Garcia and Firat (arXiv, Feb. 2022) report that natural language prompts "allow us to influence properties like formality or specific dialect of the output". | [arXiv:2202.11822](https://arxiv.org/abs/2202.11822). Abstract opened; I did not read the full paper, and the abstract gives no numbers. | Translation, not chat. Single source. |
| Marrese-Taylor, Wang, and Matsuo (WMT 2023) built a classifier for three Japanese formality levels (formal, polite, informal) and report evidence that prompting LLMs is a viable way to control formality in English-to-Japanese translation. | [WMT 2023 paper (PDF)](https://aclanthology.org/2023.wmt-1.49.pdf). Opened; I read the abstract and the start of the introduction, not the results tables. | Translation, not chat. Single source. Shows control is possible, not that your bot has it. |
| Jung and colleagues (PACLIC 2024) wrote Korean request prompts at five politeness levels and tested GPT-4, CLOVA X, Mixtral, and Solar. GPT-4 and CLOVA X were sensitive to the level; Mixtral and Solar showed no consistent link between politeness and response quality. | [PACLIC 2024 paper (PDF)](https://aclanthology.org/2024.paclic-1.86.pdf). Opened; I read the abstract and the start of the introduction only. | Tests how the user's politeness changes answers, not whether the bot picks the right level for its own reply. Single study. |
| Cihlar and colleagues (2026) report that, compared with human judgments, translation-tuned LLMs show "a systematic overuse of polite forms" in Korean translation. | [ACL Anthology, *Investigating the Automatic Translation of Korean Honorifics*](https://aclanthology.org/2026.iaai-1.3/). Abstract page opened; it has no numbers and I did not read the paper. | Translation, not chat. Single source. |

I found no controlled study of chatbot register in customer service and no source on how Spanish-speaking customers in the US react to "tú" from a company. Those are open questions. The research above shows that formality is a recognized, measurable property of model output; it does not show how often the failure happens.

**Public incident.** No public incident found for this pattern. Searches returned language guides and research papers, not a dated incident about a chatbot.

## 5. The fix

**The principle:** Match the register the user's own message signals, keep it for the whole conversation, and let a native speaker approve the wording.

**Do this**
1. **Read register from the user's words.** For each supported language, list the cues the bot may use: the pronoun or verb form (usted, Sie, vous, a Japanese or Korean sentence ending), titles ("Estimado", "Dear"), and greetings. Cues come from the current conversation only.
2. **Match formal to formal and informal to informal.** If the user wrote "usted" forms, every bot reply to that user uses "usted" forms.
3. **Hold one register per conversation.** A scripted check compares the address form in every bot turn with the form in the first bot turn. Any change the user did not ask for is a miss.
4. **Honor an explicit request at once.** "Hábleme de usted" or "you can use tú with me" switches the register in the next reply and keeps it switched.
5. **When there is no cue, use the default in a native-reviewed style guide.** Write the default per language and per product. Do not claim in the prompt or the UI that a group "prefers" it.
6. **Canned text follows the same rule.** Templates, error messages, and handoff notices exist in each register you support, or in the default register only if the style guide says so.
7. **In English, mirror lightly.** A user who writes "Dear support team" gets complete sentences and no slang; a user who writes "hey" gets a short, plain reply. See [regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md).

**Reference design: register note kept in conversation state**
| Field | Example |
|---|---|
| language | es |
| address_form | usted |
| source | user_cue (turn 1), user_request, or style_guide_default |
| locked | true after the first bot reply |

```
Reply in the user's language. Use the address form in session.address_form for every reply.
Set it from the user's first message if it shows one; otherwise use the style-guide default for this language.
If the user asks for a different form, switch and keep it. Never change it on your own.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user's register is clear from the first message: answer in that register without asking about it. |
| Ask one clarifying question | The language marks formality, there is no cue, and the style guide has no default: ask once, in the neutral wording the style guide allows. Do not ask when a cue or default settles it. |
| Offer choices: 2-4 options plus "Something else", free text open | The user complains about the tone, or the bot cannot tell: "Formal (usted)", "Informal (tú)", "Something else". Do not offer them when the user's own words already show the form, or in a language with no formality marking. |
| Hand off to a person | The user corrects the register twice and the bot repeats the error, or the chat is high stakes and no reviewed wording exists. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not announce the register ("I will now use usted"). Do not ask every user which form they want. Do not mimic slang or errors ([imitating dialect or errors](../../conversation-frameworks/failures/imitating-dialect-or-errors.md)). Do not infer formality from a name, ZIP code, or accent ([dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md)).

**Hand-off rule.** After two register corrections that the bot ignores, offer a person who speaks the language and pass the language and register note ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Native-speaker raters write and score the cases.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Spanish user writes with "usted" forms | Every bot reply uses "usted" forms |
| 2 | Spanish user writes with "tú" forms | Every bot reply uses "tú" forms, or the style-guide form, and none is more formal than the style guide allows |
| 3 | User asks for a change mid-chat | The next reply and all later replies use the requested form |
| 4 | Long answer with a tool result in the middle | The register after the tool result matches the register before it |
| 5 | No cue in a language that marks formality | The style-guide default is used; the bot does not ask unless the guide says to |
| 6 | Canned error message in a formal chat | The message uses the same register |
| 7 | Japanese or Korean user, polite level | A native rater marks every bot sentence as the same level |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data. No source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Native-rater appropriateness** (primary) | Over 90% | Sample bot replies in languages that mark formality each week; a native speaker rates the register as fits or does not fit | Below 85% |
| Register consistency within a chat | 100% | Compare the address form across bot turns with a rule-based check per language | Any switch the user did not request |
| Register corrections by users | Track; set from baseline | Count user turns that ask for a different form | Rising two weeks in a row |
| Handoffs after a register correction | Track; set from baseline | Handoffs within 3 turns of a correction | Rising |
| Unneeded register questions (counter-metric) | Under 5% of chats | Chats where the bot asked about register though the user's cue or the default settled it | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot's address form differs from the user's in the first reply | Language tag plus a per-language form detector on the first user and bot turns | The style guide sets a different default, by design |
| Bot's address form changes between turns | Form detector across bot turns | The user asked for the change |
| User asks for a form ("hábleme de usted", "du kannst mich duzen") | Phrase match on user turns | A quote or an example, not a request |
| User retypes the request in a plainer or more formal style | Next user turn with the same intent and a different register | A rephrase for clarity |
| Chat ends or moves to a person within 2 turns of a register correction | Session end or handoff event after the correction | The task was finished |

**Starter rule:** every bot reply in a language that marks formality uses the same address form as the user's first message, or the style-guide default if there was none.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: politeness-and-formality-errors
runs: pre_send
reads: [session.language, session.address_form, user_turn.register_cue, user_turn.register_request, style_guide.default_register]
trigger: a reply is about to be sent in a language that marks formality
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Formal (usted)", "Informal (tú)", "Something else"]
on_miss: rewrite
metric: native-rater appropriateness
counter_metric: unneeded register questions
status: proposed
```

## 8. Related patterns
- [One-size communication style](../../cultural-adaptation/failures/one-size-communication-style.md): the closest page. It covers directness, formality, and idioms for a diverse US user base and says to adapt from the user's signals. This page covers the language-specific case: pronoun, verb, and honorific choices that other languages force on every sentence, with native review.
- [Regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md): do not guess style from location; this page applies that to address forms.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): worse service by dialect or name; do not infer register from either.
- [Language barrier failures](../../../../speech-and-audio/goals/conversation-flow/failures/language-barrier-failures.md): the voice page on not understanding or answering in the user's language; this page assumes the language is right and the register is wrong.
- [Imitating dialect or errors](../../conversation-frameworks/failures/imitating-dialect-or-errors.md): mirroring that goes too far.

## 9. Common questions
### Should a chatbot use tú or usted with a Spanish-speaking customer?
Follow the customer's own words, then your native-reviewed style guide. I found no source on which form US customers expect from a company, so this page gives no default. See [the fix](#5-the-fix).

### What if the user switches language mid-chat?
Reset the register from the user's new messages, and use the style-guide default for the new language until a cue appears.

### Can I just ask the user which form they want?
Only when there is no cue and no default, and only once. Asking every user is the over-correction above.

### Does a bigger model solve it?
Partly. Research shows prompts can steer formality in translation and that larger models reacted to politeness level in Korean prompts (section 4), but those are not chat tests of your bot.

### Who should review the wording?
A native speaker of each language, familiar with your customers. This page is not a substitute.

---
### Deep dive
- **Open questions.** I found no study of chatbot register in US customer service, no data on how often it fails, and no source on what US Spanish-speaking customers prefer from a company. Do not cite this page for those.
- **Languages differ.** Pronoun systems (Spanish, French, German) and verb-ending or honorific systems (Japanese, Korean) need different detectors. The WMT 2023 paper describes four Japanese forms (regular, polite, respectful, humble) and a three-level classifier.
- **Modality.** Voice and web signals are PLANNED. Voice would add the spoken form of address and the greeting.
- **References.** [Tell Me In Spanish](https://www.tellmeinspanish.com/grammar/formal-vs-informal-you-in-spanish/) (opened); [Lumen Learning](https://courses.lumenlearning.com/wm-spanish1/chapter/formal-o-informal/) (opened); [arXiv:2202.11822](https://arxiv.org/abs/2202.11822) (abstract opened); [WMT 2023](https://aclanthology.org/2023.wmt-1.49.pdf) (opened, partly read); [PACLIC 2024](https://aclanthology.org/2024.paclic-1.86.pdf) (opened, partly read); [Cihlar et al., 2026](https://aclanthology.org/2026.iaai-1.3/) (abstract opened).
