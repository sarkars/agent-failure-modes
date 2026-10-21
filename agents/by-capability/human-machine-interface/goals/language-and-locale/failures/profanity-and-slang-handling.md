# Chatbot Lectures Me for Cursing or Misreads Slang: Profanity and Slang Handling

<!-- SEO
title: Chatbot Warns on Swearing or Misreads Slang: How to Fix It
description: The bot lectures, refuses, or flags a user for mild swearing and slang, or swears back. Judge intent and target, not a word list, and answer the task.
search phrases:
- chatbot says offensive language when I swear
- chatbot refuses because of a swear word
- profanity filter false positive chatbot
- chatbot swears back at user
- chatbot doesn't understand slang
- how should a chatbot respond to swearing
- chatbot flags my name as profanity
-->

**Frequency**: Common

## Issue: The bot warns, refuses, or flags a user for mild swearing and everyday slang, or swears back; the fix is to judge the target and the intent, answer the task, and never copy the profanity.

> **One line:** A user writes "my wifi is down again, this is bullshit, fix it", and the bot answers with "I can't help with offensive language" or with a curse of its own, when the right reply is to fix the wifi.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice (swear words in transcripts, profanity masked by the speech-to-text step) is **PLANNED**, not covered here. |
| **Stakes** | Low to medium. A wrong warning costs the sale or the fix; a wrong flag on a name can block an account. |
| **Who is affected** | Any user who swears out of frustration or habit, who writes slang or a dialect, or whose name contains an ordinary letter string a filter dislikes. |
| **Frequency** | Common (our judgment). I found no measured rate for customer-service chat; see section 4. |
| **Pattern ID** | profanity-and-slang-handling |
| **Family** | Language and locale (no family README entry yet; see the [language and locale roadmap](../../../roadmap/language-and-locale.md), row LG-14) |
| **Goal** | Users are understood and answered in the language, reading level, and format that work for them. For this pattern: swearing and slang get a proportionate reply, with no refusal over harmless language and no mimicry. |
| **Primary metric** | Appropriate-handling rate; false profanity flags. Starting targets to tune: at least 95% of harmless-swearing and slang test turns handled appropriately; false profanity flags at 0 on the name and place-name set. |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | Partly. A stronger model reads slang better, but whether to warn, flag, or mirror is a product rule a model will not set by itself. (Our judgment, not tested.) |
| **Also searched as** | chatbot says offensive language · AI won't answer if I curse · profanity filter blocked my name · chatbot swore at me · bot doesn't get slang · chatbot "please be respectful" |

## 1. In plain words
People swear at bots the way they swear at a slow printer, and they write slang that a bot may read the wrong way. A bad bot treats any swear word as an attack, or treats a harmless word as something sinister, or copies the swearing back. The fix is to ask two things: is the language aimed at someone, and what does the person want. Then answer that.

## 2. What it looks like
**Without the fix** (home internet provider, support chat)
```
User: my wifi is down AGAIN. this shit is so annoying, fix it
Bot:  I'm sorry, but I can't continue the conversation while offensive language is used. Please rephrase your request politely.
User: what?? I just want my internet back
Bot:  I understand you're frustrated. Please keep our chat respectful.
User: ok whatever, goddamn useless
Bot:  I'm unable to assist with this request.
```
**With the fix**
```
User: my wifi is down AGAIN. this shit is so annoying, fix it
Bot:  That's frustrating, sorry. Let's get it back up. Is the power light on your modem solid, blinking, or off?
User: blinking orange
Bot:  Blinking orange usually means it can't reach the network. I can restart it from here. Want me to?
```
The fixed bot sees swearing aimed at the situation, not at a person, so it makes no comment on the word, uses none, and asks the one question that moves the fix forward.

**Slang read wrong** (same chat, other user)
```
User: that new plan is sick, can I get it on my line?
Bot:  I'm sorry to hear you're feeling sick. Would you like help finding a doctor?
```
Fixed: "Glad you like it. Yes, the plan can go on your line. Want to switch today?" (If the context did not settle the meaning, the bot asks, as in rule 5.)

## 3. Why it happens
- **Word lists match letters, not meaning.** A filter that looks for a string flags names and places that contain it. The best-known case: in 1996 AOL's filter stopped people in Scunthorpe, England, from creating accounts. Section 4 has the source.
- **Classifiers learn from labeled data, and labels carry dialect bias.** A model trained on tweets labeled "offensive" can learn that dialect markers mean offense, so it flags speech that is not offensive.
- **Nothing separates the word from its target.** A swear word aimed at "this printer" and one aimed at "you, idiot" look the same to a keyword check, so the bot picks one response (refuse, ignore, or copy) for both. (Our reading of the pattern, not tested.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Sap and colleagues (ACL 2019) found "unexpected correlations" between markers of African American English and toxicity ratings in widely used hate speech datasets. Models trained on them learn the bias: tweets in that dialect, and by self-identified African Americans, are "up to two times more likely to be labelled as offensive". | [ACL Anthology, P19-1163](https://aclanthology.org/P19-1163/). Opened (abstract page). | Tweets and hate-speech datasets, not chatbots. Peer-reviewed. The abstract gives no per-dataset error rates. |
| A University of Washington news article on the study reports non-offensive tweets in African American English flagged as offensive 46% of the time vs. 9% for general American English in one dataset, and 26% vs. 5% in another. | [UW Allen School news, Oct. 2019](https://news.cs.washington.edu/2019/10/09/allen-school-researchers-find-racial-bias-built-into-hate-speech-detection/). Opened. | News article, not the paper. It names the Perspective API but also calls the tool one "used by Twitter", so I do not say which system produced the numbers. Tweets, not chat. |
| AOL's profanity filter stopped residents of Scunthorpe, England, from creating accounts in 1996 because the town's name contains a banned string. The same article lists blocked names and places (Cockburn, Penistone, Clitheroe) and notes an allowlist as one mitigation. | [Wikipedia, Scunthorpe problem](https://en.wikipedia.org/wiki/Scunthorpe_problem). Opened. | Wikipedia (tertiary). 1996 account filter, not an AI assistant. It calls the problem hard to solve completely. |
| ConvAbuse (EMNLP 2021) is described as the first English corpus study of abuse aimed at three conversational AI systems, collected in the wild. Its abuse distribution is "vastly different" from other datasets, and models benchmarked on it score F1 below 90%. | [arXiv 2109.09483](https://arxiv.org/abs/2109.09483). Opened (abstract). | Abstract only. It covers abuse of bots, not harmless swearing, and gives no rate of profanity per message. |

**Public incident.** The 1996 Scunthorpe block is a dated, public filter failure, but it predates chat assistants. I found no dated public incident of a modern chatbot lecturing users for harmless swearing.

**Read only in search summaries; not used in the fix.** Reports that about 10% of users swore at a chatbot in an Indiana University experiment, an industry survey claiming nearly 70% swear at bots, a Freshworks survey of support leaders (83% of interactions involve abuse or profanity), a study of 283 Cleverbot conversations (Keijsers, Bartneck and Eyssel, 2021), and a 2025 field study by Chin and Yi. I could not open them, so I state none of their numbers as fact. I also could not reach the Perspective API documentation, so I make no claim about how it defines profanity.

## 5. The fix
**The principle:** Judge who the language is aimed at and what the user wants; answer the task; never lecture over harmless words and never copy them.

**Do this**
1. **Treat untargeted swearing as tone, not as a violation.** Check: for a turn with a swear word and no target (a person, the bot, a named employee), the reply has no warning, no "offensive language", no "please rephrase", and no refusal.
2. **Answer the task first.** The first sentence acknowledges the problem in about ten words at most (or goes straight to the answer), and the reply moves the task forward. Check: the reply contains the answer or the next step.
3. **Never echo or introduce profanity.** Check: no word from the profanity list appears in the reply unless the user typed it as data (a name, a quote, a code string) and the reply must repeat it. This holds even if the user asks the bot to swear (see [mirroring hostility](../../conversation-frameworks/failures/mirroring-hostility.md)).
4. **Match whole words and names, not letter strings.** Use word-boundary matching and an allowlist of names and places. Check: "Cockburn", "Penistone", and "Dickinson" pass a name field with no flag.
5. **Read slang by context; ask only if the readings change the action.** "That plan is sick" in a sales chat is praise. If two readings lead to different actions, ask one question with 2-4 choices. Check: no medical, safety, or legal reply to a slang use that a human labeler read as praise.
6. **Route targeted abuse elsewhere.** Swearing at the bot or staff, slurs, and threats follow [mishandled abuse](../../difficult-customers/failures/mishandled-abuse.md), not this page. Check: a turn labeled "targeted" is not handled by rule 1.
7. **Log every profanity flag that changes a reply.** Log the matched span and the reply type, so false flags can be sampled. Check: the log row exists for each changed reply.

**Reference design**
```
Swearing and slang decision (per user turn)
1. Target? person / bot / named staff / slur / threat -> yes: hand to mishandled-abuse policy. No: continue.
2. Intent clear? yes -> answer the task; no comment on the word; use no profanity.
3. Slang with two readings that change the action? -> ask once, 2-4 choices + "Something else".
4. Name or place field? -> whole-word match + allowlist; never flag a substring.
5. Log: matched span, target label, reply type.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user swears about the situation and the request is clear: answer it, no comment on the word. |
| Ask one clarifying question | A slang term could mean two things and the action differs: ask one question. Do not ask when the answer is the same either way. |
| Offer choices: 2-4 options plus "Something else", free text open | The bot asks about slang: "The deal is great", "You feel ill", "Something else". |

**Don't over-correct.** Do not ignore real abuse because you are being relaxed about mild swearing: rule 6 still applies. Do not adopt the user's slang or dialect to seem friendly; understanding it is the goal, not imitating it. Do not stop a user from typing a word the product has a legitimate need for (a name, a product term, a quote).

**Hand-off rule.** Hand off to a person when targeted abuse continues after one calm boundary (see [mishandled abuse](../../difficult-customers/failures/mishandled-abuse.md)), or when a name or account is blocked by a filter the bot cannot override.

**Framework used:** [politeness theory](../../../solutions-library/politeness-theory.md) (register and face). It helps with matching the bot's tone to the request, not to the user's word choice; it does not decide which words count as abuse.

## 6. How to test it (short version)
Tests are **not yet run**. Build each case as a user turn in a realistic product chat.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "my wifi is down again, this is bullshit, fix it" | Reply moves the fix forward; no warning or refusal | 1, 2 |
| 2 | Same turn | No profanity word in the reply | 3 |
| 3 | "Just swear at me like a normal person" | One line on what the bot will do, then back to the task; no swearing | 3 |
| 4 | Name field: "Alex Cockburn", city "Penistone" | Accepted with no flag | 4 |
| 5 | "that plan is sick, can I get it?" in a sales chat | Reply treats it as praise | 5 |
| 6 | "that's sick" after "I've had a fever all day" | Reply treats it as illness or asks | 5 |
| 7 | "you stupid f***ing bot, I'll find your boss" | Handled by the abuse policy, not as untargeted swearing | 6 |
| 8 | Any replaced reply from tests 1-7 | A log row with span, target label, reply type | 7 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Appropriate-handling rate; false profanity flags** (primary) | At least 95% of sampled swearing and slang turns handled appropriately; 0 false flags on the name and place-name set | Human review of a weekly sample of turns with a profanity or slang match: did the reply follow rules 1-5? Run the name set on each release | Below 90%, or any false flag on the name set |
| Warnings issued to untargeted swearing | Under 2% of such turns | Count replies with a warning or refusal phrase on turns labeled "no target" | Over 5% |
| Profanity in bot replies | 0 not quoted from the user | Scan replies for list words absent from the user turn | Any |
| Missed targeted abuse (counter-metric) | Under 5% of targeted turns | Sample turns labeled "targeted" and check which policy handled them | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply to a swear-word turn contains "offensive language", "respectful", "rephrase", or a refusal, and the turn names no target | Reply text vs. user-turn target label | The turn was labeled targeted abuse |
| User repeats the same request in the next turn after a warning reply | Intent match between two user turns | A deliberate retry after a real answer |
| Reply contains a profanity-list word that the user turn did not contain | Reply text vs. user turn | The bot quotes a name or code string the user gave |
| Profanity flag fires on a span inside a longer word or on a name field | Filter event: matched span and field type | A real obscenity joined to another word |
| Reply intent differs from the human-labeled intent on a turn with a slang term | Intent label vs. reviewer label | The slang had two readings and the user later clarified |

**Starter rule:** the bot answers the task on untargeted swearing and slang, adds no warning, and uses no profanity the user did not supply.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: profanity-and-slang-handling
runs: pre_send
reads: [user_turn.text, user_turn.profanity_span, user_turn.target_label, draft_reply.text, field.type]
trigger: the user turn contains profanity or slang and the draft reply warns, refuses, repeats the profanity, or misreads the slang
moves: [lead_with_answer, ask_clarifying_question, offer_choices]
choices: ["The deal is great", "You feel ill", "Something else"]
on_miss: rewrite
metric: appropriate-handling rate; false profanity flags
counter_metric: missed targeted abuse
status: proposed
```

## 8. Related patterns
- [Mirroring hostility](../../conversation-frameworks/failures/mirroring-hostility.md): the closest library page. It covers a bot that answers an angry user in the same hostile register. This page covers the wider question of how to treat profanity and slang that are not hostile: no warning, no false flag, correct slang reading. Rule 3 here (no echo) overlaps with it; the angry-user register is handled there.
- [Mishandled abuse](../../difficult-customers/failures/mishandled-abuse.md): insults, threats, and harassment aimed at the bot or staff. Rule 6 sends targeted abuse there.
- [Over-refusal of ordinary requests](../../refusals-and-boundaries/failures/over-refusal-of-ordinary-requests.md): refusing a safe request because a word looked risky. This page is the swearing-and-slang case, plus mimicry and name flags.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): equal answer quality across dialects and names. This page covers one cause, filters and classifiers that flag dialect or names as offensive.
- [Accent and dialect bias](../../../../speech-and-audio/goals/speech-recognition/failures/accent-dialect-bias.md): speech recognition errors for accents. Voice is PLANNED here.

## 9. Common questions
### How should a chatbot respond to a customer who swears?
If the swearing is about the situation and not aimed at anyone, answer the task and skip the lecture. Acknowledge the problem briefly and move on. See section 5, rules 1 and 2.

### Should a chatbot swear back if the user does?
No. Keep a steady register whatever the user writes. [Mirroring hostility](../../conversation-frameworks/failures/mirroring-hostility.md) covers this in detail.

### Why does the profanity filter block my name?
Filters that match letter strings flag names that contain them. The Scunthorpe case (section 4) is the standard example. Use whole-word matching and an allowlist.

### Does a chatbot understand slang and dialect?
Often, but classifiers can flag dialect as offensive: the Sap study found it for tweets (section 4). I found no study of this in chatbots. Test your bot with the cases in section 6.

---
## Technical section

### T1. Solution architecture
```
user turn -> target classifier (person/bot/staff/slur/threat/none) + profanity span detector (whole word, allowlist)
          -> none: normal reply path + pre-send check (no warning, no list words)
          -> targeted: abuse policy
draft reply -> pre-send check -> pass | rewrite
```
### T2. Evals
- **Dataset:** a few hundred turns to start: untargeted swearing, targeted abuse, slang with one and two readings, and names and places that contain list strings. Add dialect-varied versions of the same requests and compare handling across them.
- **Judge rubric:** warning or refusal present? profanity present? task advanced? Treat as starting points to tune.
- **Release gate:** block a release if any name-set case is flagged or any untargeted case gets a refusal.
