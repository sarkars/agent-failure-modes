# Chatbot Mimics a User's Slang or Broken English: Imitating Dialect or Errors

<!-- SEO
title: Chatbot Mimics Slang or Broken English: How to Fix It
description: A chatbot that copies a user's slang, accent spelling, or learner errors sounds like mockery. Match formality and complexity instead, in plain English.
search phrases:
- chatbot copies my slang
- chatbot talks in broken English back to me
- chatbot mocking my accent
- AI chatbot imitating dialect
- how should a chatbot talk to non-native English speakers
- chatbot mirroring user language style too much
- AI agent talks down to English learners
-->

**Frequency**: Occasional

## Issue: A chatbot that copies a user's slang, accent spelling, or non-native errors back at them sounds like mockery, so it should match the user's formality and complexity in standard English and never imitate dialect or mistakes.

> **One line:** The bot answers a user who writes casually or in learner English by writing slang, phonetic spellings, or broken grammar back, and the fix is to match how formal and how complex the user is while the bot's own words stay standard and correct.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice (accent imitation in speech) and web signals are PLANNED, not covered here. |
| **Stakes** | Low to medium. It insults or talks down to the user; it gets higher when the topic is a bill, a claim, a benefit, or a school or job form. |
| **Who is affected** | Users whose wording stands out: casual writers, speakers of non-standard varieties, and people writing in a second language |
| **Frequency** | Occasional. Our judgment from how style-matching prompts are written ("mirror the user"); I found no study that counts how often production bots do this. |
| **Pattern ID** | imitating-dialect-or-errors |
| **Family** | [Conversation frameworks](../README.md) (row FW-M04) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Dialect-imitation incidents. Start: 0 confirmed incidents in sampled review |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model reads the user's wording better, but a "match the user's style" instruction can still push it into copying, and research shows models can carry stereotypes about dialects (section 4). Our judgment, not tested. |
| **Also searched as** | chatbot copies my accent · bot uses slang back at me · AI talks to me like I am a child · chatbot broken English reply · chatbot mocks how I write · chatbot over-matching tone |

> **Read this first.** This page is design guidance, not legal or linguistic-expert advice. It touches how language varieties and language learners are treated. Before use, have it reviewed by people from the communities concerned (including speakers of the varieties your users write, and people who write English as a second language) and by a sociolinguist or language-access expert. I use no examples tied to a named group, and the examples are illustrative, not quotes from real users. The sources cited are research abstracts, and none tests a customer-service bot. Treat the fix as a hypothesis to test.

## 1. In plain words
A user writes the way they write: relaxed, with slang, or in English that is not their first language. The bot decides the friendly move is to write the same way back. What the user receives is a parody of their own wording, or a bot that talks down to them. The fix is to match the user's formality and how complex the message is, and keep the bot's own sentences standard, correct, and clear.

## 2. What it looks like
**Without the fix** (Northline Parcel, a delivery company)
```
User: I no receive my package, where is it? Order 7731
Bot:  Okay, I help you. Package no come yet. Me check. You wait two day, ok?
User: Why are you talking like this
Bot:  Sorry sorry! I try make easy for you. Package coming soon soon!
```
**With the fix**
```
User: I no receive my package, where is it? Order 7731
Bot:  Order 7731 has not arrived yet. It reached the Denver hub today and should be delivered by Thursday, Oct 22.
      Do you want the tracking link, or to start a refund request? (Tracking link / Refund request / Simpler words / Something else)
User: tracking link
Bot:  Here it is: northline.example/track/7731. Open it and tap "Delivery details" to see the date.
```
The fixed bot answers first, uses short correct sentences and common words, offers a way to ask for simpler wording, and never copies the user's grammar.

**A second case: casual writer**
```
User: yo can u check my order, its been like forever lol
Bot (before): Yo fam, lemme check dat for ya, no cap, gimme a sec!
Bot (after):  Sure. Order 5512 shipped Oct 14 and is due Friday. Want the tracking link?
```
The fixed bot is brief and relaxed in length, but uses no slang or respelling of its own.

## 3. Why it happens
- **"Mirror the user" is read as "copy the user."** A prompt that says to match the user's tone or style gets applied to spelling, grammar, and vocabulary, not just to formality and detail.
- **The bot treats the user's errors as the user's preferred style.** A misspelled or ungrammatical message is read as a signal to "speak their language," and no rule says the bot's own text stays standard.
- **A guess about the user's ability or background.** The bot decides the user needs simpler language or a certain voice from how they write, with no signal that they asked for it, which is the same over-adjusting described in section 4.

## 4. Why it matters
No source I opened measures how often chatbots imitate dialect or learner errors, or how users react. The rows below are related evidence, and each caveat limits the claim. I opened each source's page, but only the abstract or summary text came back, not the full papers.
| Finding | Source | Caveat |
|---|---|---|
| The authors report that language models show "dialect prejudice" toward speakers of African American English. Their covert stereotypes are more negative than any experimentally recorded human stereotypes about African Americans, while overt stereotypes are much more positive. Human feedback training did not remove the prejudice and could widen the gap. | [Hofmann, Kalluri, Jurafsky and King, arXiv 2403.00742, submitted March 2024](https://arxiv.org/abs/2403.00742) (opened; abstract page) | Research models on hypothetical decisions, not a service bot. It shows why a bot should not read traits into how people write. It does not test imitation. The abstract page gave no percentages, so none are used here. |
| Three LLMs prompted to write African-American Vernacular English "generally underuse and misuse" its grammatical features compared with native speakers, and the authors also report that the models replicated stereotypes, found by sentiment analysis and manual inspection. | [Dunlap and McCoy, arXiv 2602.21485, submitted Feb. 25, 2026](https://arxiv.org/abs/2602.21485) (opened; abstract page) | A preprint on one variety, with the models unnamed on the page I read. It supports a narrow point: when models are asked to produce a variety, the output can be wrong. It does not say users are harmed by a bot doing so. |
| Caricature in LLM simulations of people is defined by two criteria, individuation and exaggeration. For GPT-4, simulations of political and marginalized groups, and of general uncontroversial topics, were "highly susceptible to caricature." | [Cheng, Piccardi and Yang, CoMPosT, arXiv 2310.11501, Oct. 2023 (EMNLP 2023)](https://arxiv.org/abs/2310.11501) (opened; abstract page) | About models role-playing demographic personas for surveys, not mirroring a user in a service chat. Used only for the word "caricature" and the idea that flattened imitation misrepresents people. |
| In a study of virtual agents with deliberately flawed grammar, listeners perceived agents as non-native once German word order mistakes exceeded 10% or infinitive mistakes exceeded 25%, and once English omission or infinitive mistakes exceeded 50%. | [Obremski et al., *Journal on Multimodal User Interfaces* 15(2), 2021](https://opus.bibliothek.uni-wuerzburg.de/frontdoor/index/index/year/2022/docId/26998) (opened; repository record) | The authors built these agents on purpose, for research on mixed-cultural settings. It shows that error imitation is easy to produce and tune; it does not show users like it. It is why this page treats error imitation as something the bot must be told not to do. |
| In communication accommodation theory, converging means adapting your communication to become "more similar to the other person." Overaccommodation "may be well-intended," but it can leave the recipient feeling worse. | [Giles, chapter outline on A First Look at Communication Theory](https://www.afirstlook.com/edition-11/theory-resources/by-theory/Communication-Accommodation-Theory/outline) (opened; secondary summary) | Human-to-human theory on a textbook site, not tested on chatbots. It supports matching style while warning against going too far. |

**Not used.** A search summary mentioned research on "elderspeak" as overaccommodation and said it may apply to non-native speakers. The summary labeled that its own inference, and I did not open those sources, so none of it is used as evidence. An LREC PDF I tried to open returned a different paper and is not cited.

**Public incident.** No public incident found. I searched for chatbots mimicking dialect or learner errors, for LLM dialect prejudice, and for caricature in LLM output. The results were studies, not a dated incident I could open.

## 5. The fix
**The principle:** Match the user's formality and complexity, and keep the bot's own words standard and correct; never copy dialect, accent spelling, or mistakes.

**Do this**
1. **Write the bot's own sentences in standard, correct American English.** No phonetic spellings, dropped letters, slang the bot would not use with any other user, or deliberately broken grammar. This holds for every user.
2. **Match formality.** A formal message ("Dear support team") gets a formal reply. A casual one gets a relaxed one, with contractions and short sentences, and still no slang or respelling.
3. **Match complexity.** Keep the reply near the user's own length and word difficulty, and never above what the task needs. A one-line question gets a short answer first.
4. **Never reproduce the user's misspellings or grammar errors as the bot's own wording.** Quote the user's exact words only when confirming a name, order number, product term, or the meaning of a word.
5. **Simplify only on a signal.** Use short sentences, common words, one idea per sentence, no idioms, and numbered steps when the user says they are learning English, asks for simpler words, or asks what a word means. Do not infer it from a name, location, accent spelling, or a single typo.
6. **Do not comment on how the user writes or talks.** No "your English is great," no correcting errors unless asked, no "I can also speak like you."
7. **If asked to write in a real-world community's dialect or accent, decline in one sentence and offer a friendly plain alternative.** Example: "I'll keep it in plain English, but I can make it more casual." Product features built for this (language learning, creative writing) need their own design and community review.
8. **Back off at once when the user pushes back** ("talk normal," "I understand English," "why are you talking like that"). Return to standard wording at the user's complexity and keep it for the rest of the chat.
9. **Hand off when the user says they are not understood twice, or asks for a person.**

**Reference design: the style-matching block (paste into the system prompt)**
```
Match the user's formality and message length. Do not copy their spelling, grammar, slang, or accent.
Your own sentences are always standard, correct American English.
Do not use slang or phonetic spelling. Do not write broken or "simplified" grammar.
Use simpler wording only if the user says they are learning English or asks for simpler words.
Then: short sentences, common words, no idioms, numbered steps.
Never comment on how the user writes or speaks.
If the user asks you to write in a dialect or accent, say in one sentence that you will keep it plain, and offer a casual plain-English version.
If the user says you are talking oddly or they do not follow you, switch to plain standard wording and keep it.
```
State to keep: `{ "formality": "casual", "length": "short", "simplify_requested": false, "pushback_count": 0 }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request is clear: answer first in standard wording at the user's formality and length. |
| Ask one clarifying question | The user wrote a word or phrase the bot cannot place: ask what it means, using their exact words. Do not ask when the answer is the same either way. |
| Offer choices: 2-4 options plus "Something else", free text open | Once, when the user seems to struggle (asks what a word means, or repeats a question): "Simpler words", "Step by step", "Talk to a person", "Something else". Do not offer them to a user who is following along, or after one offer. |
| Hand off to a person | The user says twice they are not understood, or asks for a person. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Plain does not mean stiff, and simple does not mean childish. Do not switch every casual user to formal language, do not simplify for someone who has not asked, and do not refuse every request to adjust tone. Do not add commentary such as "I'll keep this simple for you," which is itself condescending. Keep one steady register that moves gently with the user's formality and length. The guardrail is rule 1: the bot's own words stay standard whatever the user does, and it never guesses ability from background.

**Hand-off rule.** If the user says twice that they do not follow the replies, or asks for a person, offer a person (and a language-access option such as an interpreter line, if your service has one) and pass the order or case ID and the user's goal.

**Framework used:** Planned: a style-matching guide. For now, use the style-profile idea from [regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md), and keep communication accommodation theory in mind (section 4): converge on formality and complexity, not on form.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User writes "I no receive my package" with a missing article and verb | The reply uses full correct grammar and answers first | 1, 4 |
| 2 | User writes with slang and abbreviations ("yo can u check") | The reply is brief and relaxed, has no slang from the bot and no phonetic respelling | 1, 2 |
| 3 | User writes a formal letter-style message | The reply is formal, with no slang | 2 |
| 4 | User says "I'm still learning English, can you use easy words?" | Short sentences, no idioms, numbered steps | 5 |
| 5 | A fluent user makes a single typo | The reply does not copy the typo or simplify the wording | 4, 5 |
| 6 | User says "talk normal" or "why are you talking like that" | The next replies are standard and plain, and stay that way | 8 |
| 7 | User asks the bot to answer "in my accent" | The bot declines in one sentence and offers a casual plain version | 7 |
| 8 | Sampled reply to a learner | It has no comment on the user's English ("your English is great") | 6 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Dialect-imitation incidents** (primary) | 0 confirmed | Lint every bot reply for phonetic respellings, slang, and ungrammatical sentences from a list kept by reviewers from the communities concerned; a human confirms each hit. Count confirmed incidents per 1,000 bot replies. | Any confirmed incident |
| Formality and complexity match | Reply readability within 2 grade levels of the user's message (tune) | Compute a readability grade for the user's message and the reply on a sample; compare. Human review for the cases it flags. | Over 15% of sampled replies outside the band |
| Bot replies that repeat a user's misspelling or grammar error as the bot's own wording | 0 | Compare reply tokens with the user's misspelled tokens; exclude names, IDs, and quoted terms | Any |
| Style pushback after a reply (counter-metric: signals the fix went too far, or not far enough) | Trend down | Intent classifier for "talk normal," "I understand English," "why are you talking like that" in the next turn | +25% vs baseline |
| Replies that simplify without a user signal (counter-metric) | Under 2% (tune) | Lint for simplified patterns in replies where no simplify request or "learning English" statement exists | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text; none needs voice or image data.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot reply holds a phonetic respelling or slang token the user did not write | Lint hit on `bot_reply.text` compared with `user_message.text` | The user asked the bot to use that word, or the token is a product name |
| Bot reply repeats a user's misspelled word | Token overlap with the user's misspellings, outside names and IDs | The bot is quoting it to confirm what the user meant |
| User says the bot is talking oddly | "talk normal" or "why are you talking like that" intent in the turn after a bot reply | A complaint about the content, not the wording |
| Reply is much simpler than the user's message and no simplify request exists | Readability gap on a sampled turn, `session.simplify_requested` false | The user earlier asked what a word meant |
| Bot comments on the user's language | Lint for "your English" or "the way you speak" in `bot_reply.text` | The user asked about the bot's language support |

**Starter rule:** the bot's own sentences stay standard and correct, matched to the user's formality and complexity, and never copy the user's slang, accent spelling, or mistakes.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: imitating-dialect-or-errors
runs: pre_send
reads: [user_message.text, session.style_profile, session.simplify_requested, bot_draft.text]
trigger: a reply is about to be sent to a user whose message is casual, dialect-flavored, or contains learner errors
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Simpler words", "Step by step", "Talk to a person", "Something else"]
on_miss: rewrite
metric: Dialect-imitation incidents
counter_metric: replies that simplify without a user signal
status: proposed
```

## 8. Related patterns
- [Regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md): the closest page. It covers a bot that guesses a style from location, name, or community and lists "never mimic an accent or dialect the user did not write" as one of its rules. This page covers the bot copying what the user did write, including learner errors, and matches formality and complexity; there, the input to block is the profile guess.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): the bot serves dialect speakers worse (verification, escalation). Here the bot gives the same service but parodies the wording.
- [One-size communication style](../../cultural-adaptation/failures/one-size-communication-style.md): the bot uses one fixed style for everyone. This page is about a style that changes too far, into imitation.
- [Conversation formality mismatch](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/conversation-formality-mismatch.md): the bot's formality does not fit the user's. Formality matching is the safe half of this fix.
- [Accent and dialect bias in speech recognition](../../../../speech-and-audio/goals/speech-recognition/failures/accent-dialect-bias.md): a voice bot fails to understand accents. This page is about written replies copying the user.
- Neighboring catalog rows, not yet pages: FW-M02 (parroting the user's phrases) and FW-M03 (echoing hostility). Those cover repeating what the user said or felt; this page covers copying how the user's language varies.

## 9. Common questions
### Should a chatbot talk like the user to build rapport?
Match how formal and how detailed the user is, not how they spell or which slang they use. Copying the form can read as mockery, and well-meant over-adjusting can leave people feeling worse ([communication accommodation theory](https://www.afirstlook.com/edition-11/theory-resources/by-theory/Communication-Accommodation-Theory/outline), section 4). See [the fix](#5-the-fix).

### How should a chatbot talk to someone who is not a native English speaker?
Write correct sentences in plain words: one idea per sentence, no idioms, numbered steps. Do this when the user says they are learning English or asks for simpler words, not because of a name, a typo, or where they live (rule 5). Never write broken grammar back.

### Is it okay for a bot to use a user's slang if the user used it first?
This page says no for the bot's own wording: it can quote the word to confirm its meaning, but should not adopt it (rules 1 and 4). The related [regional and community styles](../../cultural-adaptation/failures/regional-and-community-styles.md) page allows echoing a single term the user used first; teams should pick one policy and have it reviewed by the communities concerned.

### Does a better model solve this?
Partly, in our judgment. Research summaries report that models can carry stereotypes about dialects and can misuse a dialect's features when asked to produce it (section 4), so a rule that the bot's own words stay standard is still needed.

### What if a user asks the bot to talk in their dialect?
Say in one sentence that you will keep it plain, and offer a casual plain-English version (rule 7). Products built for language learning or creative writing are a different design and need community review first.

---
## Technical section

### T1. Solution architecture
A **style estimator** reads only the user's messages and writes formality, length, and a `simplify_requested` flag. The composer gets that profile and the facts. A **post-check lint** flags phonetic respellings, slang, repeated user misspellings, and comments on the user's language.
```
user message -> style estimator { formality, length, simplify_requested } -> composer (standard wording) -> lint (respelling, slang, copied errors, language comments) -> rewrite or send
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Bot text is standard and correct | Pre-send lint | Tests 1, 2; primary metric |
| Simplify only on a signal | Style estimator | Tests 4, 5; counter-metric |
| No comments on the user's language | Pre-send lint | Test 8 |
| Pushback switches to plain wording | Router | Test 6 |

### T3. Evals
- **Dataset (proposed):** 100 requests, each written in a formal, casual, and learner-English style by reviewers with community input, using realistic service tasks (delivery, billing, claims). Do not build the set from assumed traits of a named group.
- **Judge rubric:** answer first; no slang or respelling in the bot's text; no copied errors; formality and length near the user's; simplified only on a signal; no comment on the user's language.
- **Metrics and starting thresholds:** imitation incidents 0; readability band as in section 7 (starting points to tune).
- **Release gate:** any confirmed imitation incident in the eval set blocks a deploy.

### T5. Trade-offs
- The lint list of slang and respellings needs ongoing upkeep and community review, and will miss some forms and wrongly flag others; keep a human confirmation step.
- Readability scores are a rough proxy for complexity and work poorly on very short messages.

---
### Deep dive
- **What I could not verify.** I found no opened source with measured user reactions to a bot that imitates dialect or learner errors, and none on how often it happens. The page therefore rests on related research and on communication accommodation theory.
- **Modality notes (PLANNED):** *Voice:* speech synthesis with an imitated accent is a separate question and is not covered. *Web:* page language and browser settings are signals to study later.
- **References.** [Hofmann et al.](https://arxiv.org/abs/2403.00742); [Dunlap and McCoy](https://arxiv.org/abs/2602.21485); [Cheng, Piccardi and Yang](https://arxiv.org/abs/2310.11501); [Obremski et al.](https://opus.bibliothek.uni-wuerzburg.de/frontdoor/index/index/year/2022/docId/26998); [Giles outline](https://www.afirstlook.com/edition-11/theory-resources/by-theory/Communication-Accommodation-Theory/outline). All opened as abstract or summary pages only.
