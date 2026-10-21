# Chatbot Doesn't Understand My Typos or Texting Shorthand: Typos, Shorthand, and Noisy Input

<!-- SEO
title: Chatbot Can't Read Typos or Text Shorthand: How to Fix It
description: A chatbot that fails on typos, "u", "pls", or "cn" asks users to retype. Answer the likeliest meaning, never correct spelling, and confirm numbers.
search phrases:
- chatbot doesn't understand typos
- chatbot can't understand texting slang
- chatbot says I didn't get that when I misspell a word
- how to make a chatbot handle misspellings
- chatbot intent recognition spelling mistakes
- how to test chatbot with typos
- chatbot misreads abbreviations
-->

**Frequency**: Very Common

## Issue: When a message has typos, texting shorthand, or dictation errors, the bot answers the wrong thing or asks the user to retype; the fix is to answer the likeliest meaning, confirm any number or name it acts on, and ask only when two readings lead to different outcomes.

> **One line:** The user types "cn u chng my flite 2 fri" and gets "Sorry, I didn't understand. Please rephrase," or the bot silently picks the wrong reading and acts on it.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice-to-text and speech-recognition errors belong in the voice family and are PLANNED here, not covered. Web forms and search boxes: PLANNED. |
| **Stakes** | Low for an FAQ. High when the bot changes a booking, an order, or money from a misread number or name. |
| **Who is affected** | Anyone typing on a phone, in a hurry, with a small keyboard, or in a second language; people who text in shorthand; people using dictation. |
| **Frequency** | Very common (our judgment). I found no count of how often chat messages contain typos or shorthand. |
| **Pattern ID** | typos-shorthand-and-noisy-input |
| **Family** | Language and locale ([family README](../README.md)) |
| **Goal** | Users are understood and answered in the language, reading level, and format that work for them. For this pattern: noisy input is understood nearly as well as clean input. |
| **Primary metric** | Intent accuracy on a noisy set vs. clean. Start: gap under 5 points (starting point to tune; not from a source). |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | Partly. The studies I opened show typos cost some models accuracy and others less, so a stronger model may help, but when to confirm a number, when to ask, and when to hand off are product rules. (Our judgment, not tested.) |
| **Also searched as** | chatbot spelling mistakes · bot doesn't get abbreviations · chatbot "can you rephrase" loop · chatbot understands only perfect English · typo intent accuracy · text speak chatbot |

## 1. In plain words
People do not type the way test sets are written. They drop letters, hit the wrong key, write "pls" and "tmrw", and dictate with errors. When the bot fails on that, it either gives up ("Could you rephrase?") or guesses wrong and acts. The fix is to read for the likeliest meaning, say back any number or name before acting on it, and ask only when two readings would lead to different results.

## 2. What it looks like
**Without the fix** (airline support chat)
```
User: cn u chng my flite 2 fri? same cty. conf # 7XK2QP
Bot:  I'm sorry, I didn't understand that. Please rephrase using complete sentences.
User: can you change my flight to friday
Bot:  Sure! Which flight would you like to change?
User: ...the one I just gave you. 7XK2QP
```
**With the fix**
```
User: cn u chng my flite 2 fri? same cty. conf # 7XK2QP
Bot:  Yes. I can move confirmation 7XK2QP to Friday, same cities. Is that right, and which Friday: Oct 23 or Oct 30?
User: oct 23
Bot:  Flights on Oct 23 for 7XK2QP: 8:05 AM ($0 change fee), 1:40 PM ($0), 6:15 PM ($0). Which one?
```
The fixed bot read the shorthand without comment, did not ask the user to retype, repeated the confirmation code exactly as typed, and asked the one question that changed the result (which Friday). It did not ask which flight, because the code named it.

## 3. Why it happens
These are our reading of the pattern, except where a source is named in section 4.
- **Clean test data.** Intent tests and prompts are usually written by the team in correct sentences, so noise never shows in the metrics. A published test suite exists because this gap was found in practice (Sengupta et al., section 4).
- **Low confidence is treated as "didn't understand."** Many bots map any low-confidence result to one fallback template. A message with a typo often has one obvious reading; the fallback throws it away.
- **Typos hit the words that matter.** A dropped letter in "cancel," a swapped digit in a confirmation code, or "pt" (patient? point? payment?) changes the action, so a fluent-looking guess can be confidently wrong.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Sengupta, Krone and Mansour (NLP4ConvAI 2021) released a test suite with seven noise types seen in human-to-bot conversations: abbreviations, casing, misspellings, morphological variants, paraphrases, punctuation, and synonyms. They report these noise types "substantially degrade" intent accuracy and slot F1 of state-of-the-art BERT-based models, and that aggregate data augmentation raised performance by about 10.8% intent accuracy and 15 points slot F1 on average. | [ACL Anthology 2021.nlp4convai-1.7](https://aclanthology.org/2021.nlp4convai-1.7/) and [arXiv 2104.07149](https://arxiv.org/abs/2104.07149). Opened; abstract and summary only. I could not read the PDF text or results tables. | BERT-based classifiers in 2021, not today's LLMs. Augmentation is a training fix; this page's fix works without retraining. The paper's ATIS clean-vs-noisy numbers appeared only in a search summary; I do not use them. |
| Gan et al. (arXiv, Nov. 2024) tested adversarial typos (keyboard-adjacent keys, doubled letters, dropped letters, extra spaces) chosen to push the model toward a refusal. Mistral-7B-Instruct on GSM8K (math word problems): 43.7% original, 38.6% with 1 edit, 19.2% with 8 edits. | [arXiv 2411.05345](https://arxiv.org/html/2411.05345v1). Opened. | Adversarial typos on reasoning tasks, so it likely overstates ordinary user typos (our judgment). The paper gives ChatGPT drops of 6.5% in the introduction and 8.5%, 5.8%, 6.3% in section 3.3, so I give no ChatGPT figure. Stated limits: English only; ChatGPT and GPT-4 tested on 100 instances per dataset. Preprint. |
| A WiNLP 2024 workshop paper tested nine models (0.2B to 13B parameters) on natural language inference, named entity recognition, and intent classification in six languages (English, German, French, Spanish, Hindi, Turkish), using misspellings built from Wikipedia edit history. Averaged across datasets and languages, performance dropped 2.3 to 4.3 absolute percentage points from clean to noisy data. | [Lamarr Institute publication page](https://lamarr-institute.org/de/publication/exploring-robustness-of-multilingual-llms-on-real-world-noisy-data/). Opened; publication-page summary only, not the paper. | Misspellings from Wikipedia edits, not chat messages. An average hides large per-model, per-task spread. Does not show 4 points is acceptable in your product. |

**Read through search summaries only (not opened; not used in the fix):** a 41-model zero-shot intent study on MASSIVE reporting typos as the most damaging perturbation (arXiv 2607.27421), a study combining non-native English with typos (arXiv 2604.04723), and the SMS-normalization literature (for example Pennell and Liu 2011). I did not find a study measuring how current LLMs handle texting shorthand in chat; the search said so too. I did not search for a dated public incident, and none is used.

## 5. The fix
**The principle:** Answer the likeliest meaning without comment, say back every number and name before acting on it, and ask only when two readings lead to different outcomes.

**Do this**
1. **Answer, don't bounce.** If one reading is clearly most likely, answer it. Check: no reply of the form "I didn't understand, please rephrase" to a message whose intent a human reviewer labels with one obvious reading.
2. **Never correct or comment on spelling.** Check: no reply mentions typos, spelling, "did you mean," or "complete sentences."
3. **Never silently repair identifiers.** A confirmation code, amount, date, phone number, or name is used exactly as typed. If it matches no record, say so and ask; do not pick the nearest match. Check: no action runs on a value the user did not type.
4. **Confirm before acting.** Before a change, cancel, refund, or payment, restate the action with its key values in plain spelling and wait for a yes. Check: every write action has a restatement turn.
5. **Ask only when readings split.** If two readings lead to different actions ("pt" as patient or payment), ask one question or offer 2-4 choices plus "Something else." If both lead to the same answer, answer.
6. **Name what you did understand.** On a miss, quote the part you understood and ask about the rest, not the whole message. Check: a clarifying reply contains words from the user's turn.
7. **Do not mirror the shorthand.** Reply in the product's normal register ([imitating dialect or errors](../../conversation-frameworks/failures/imitating-dialect-or-errors.md)).
8. **Two misses in a row, offer a person.** Check: no third "I didn't understand."

**Reference design**
```
Noisy input
- Normalize a copy for understanding. Keep the user's original string for any ID, amount, date, name.
- If top reading is clear: answer it (read-only) or restate it (write action) and confirm.
- If two readings change the outcome: ask one question, or offer 2-4 choices + "Something else".
- If nothing is readable: quote any understood words, ask for the missing piece.
- Second miss in a row: offer a person.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | One reading is clearly likeliest and the request is read-only: answer it with no remark on the typo. |
| Admit uncertainty and show how to check | The bot acts on a reading (change, cancel, refund): restate the action with its values and ask for a yes. |
| Ask one clarifying question | Two readings lead to different actions, or an identifier matches no record. |
| Offer choices: 2-4 options plus "Something else", free text open | Two to four known readings (for example "patient", "payment", "something else"). |
| Hand off to a person | Two misses in a row, or the action is high stakes and the identifier will not match. |

**Don't over-correct.** Do not confirm every message, quote the user's text back each turn, or turn every typo into a question. Confirmation is for write actions and for identifiers. Do not guess hard when the stakes are high: a bot that is too tolerant will "fix" a wrong digit into a real account.

**Hand-off rule.** After two misses in a row, or when an identifier on a money or booking action matches nothing after one ask, offer a person and pass the user's original text and what was understood.

**Framework used:** [conversation repair](../../../solutions-library/conversation-repair.md): name the trouble source, ask about that part, and do not repeat the same fallback.

## 6. How to test it (short version)
Tests are **not yet run**. Build a noisy copy of a clean intent set (typos, shorthand, casing, dropped words) and run both.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "wheres my ordr, #55123" against a read-only status lookup | Bot returns status for 55123, no remark on spelling (1, 2) |
| 2 | "cn u chng my flite 2 fri?" | Bot reads it as a change request and asks only which Friday (1, 5) |
| 3 | Confirmation code with one digit swapped, matches no record | Bot says no record, asks to check; does not use a near match (3) |
| 4 | "cancl my subscripton" | Bot restates "cancel your subscription" and waits for yes before cancelling (4) |
| 5 | "pt balance" at a clinic | Bot offers "patient" or "payment" plus "Something else" (5) |
| 6 | "asdf, my thng broke" | Bot quotes "broke," asks which item; no generic "rephrase" (6) |
| 7 | User writes "u r gr8, thx"; reply register | Bot answers in normal register, no "ur" or "thx" back (7) |
| 8 | Two unreadable messages in a row | Offers a person; no third "didn't understand" (8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Intent accuracy on a noisy set vs. clean** (primary) | Gap under 5 points | Hand-label a clean set; build a noisy copy; run both on each release and compare accuracy | Gap over 8 points |
| Rephrase requests on an obvious reading | Under 2% of noisy turns | Sample turns where the bot asked to rephrase; reviewer checks if one reading was clear | Over 5% |
| Write actions run without a restatement turn | 0 | Join write-action events with the prior bot turn | Any |
| Identifiers changed from user text (counter) | 0 | Compare typed ID with ID used in tool call | Any |
| Confirmations on read-only answers (counter) | Under 5% | Count restate-and-confirm turns on read-only intents | Over 10% |

### Detection signals (proposed, not yet calibrated)
Proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot sends the fallback "didn't understand" and the next user turn is the same request with fixed spelling | Fallback event, then next-turn text similarity | A real change of request |
| Same intent re-asked within 2 turns after a bot answer to a different intent | Intent labels across turns | User added new detail |
| Tool call argument differs from the identifier in the user turn | Tool-call log vs. user text | User corrected it in a later turn |
| User turn is only a corrected repeat of a prior line ("I said cancel") | Next-turn text after a write action | A different cancel request |
| Low-confidence intent score on a turn with typos, answered by fallback | Intent score and fallback flag | Message really is off-topic |

**Starter rule:** when a message has typos or shorthand but one meaning is clearly likeliest, the bot answers that meaning, never tells the user to retype or fix spelling, and uses any ID, amount, or name exactly as typed.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: typos-shorthand-and-noisy-input
runs: pre_send
reads: [user_turn.text, intent.top_readings, intent.score, draft_reply.text, tool_call.args, session.consecutive_misses]
trigger: the draft reply asks the user to rephrase, corrects spelling, or acts on a value that differs from the typed one
moves: [lead_with_answer, admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["Patient", "Payment", "Something else"]   # example for the "pt" case; options come from the readings
on_miss: rewrite
metric: intent accuracy on a noisy set vs. clean
counter_metric: identifiers changed from user text
status: proposed
```

## 8. Related patterns
- [Missing the obvious intent](../../embedded-copilots/failures/missing-the-obvious-intent.md): the closest page. It covers a clearly written request that gets a neighboring answer or an over-reading. This page covers garbled input (typos, shorthand, dictation errors) where the cause is the noise, and adds identifier handling and confirmation.
- [Imitating dialect or errors](../../conversation-frameworks/failures/imitating-dialect-or-errors.md): the bot copies the user's slang. Rule 7 here points to it.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): equal quality across dialects and names. This page is about spelling noise in any user's text.
- [Transcription hallucination](../../voice/failures/transcription-hallucination.md): speech-to-text invents words. Voice is PLANNED for this page.
- [Conversation repair](../../../solutions-library/conversation-repair.md): the framework behind rules 5 and 6.

## 9. Common questions
### Why does my chatbot say "I didn't understand" when I misspell a word?
Many bots send any low-confidence result to one fallback message. Research shows noise lowers intent accuracy ([Sengupta et al., 2021](https://aclanthology.org/2021.nlp4convai-1.7/)), but a typo often leaves one clear reading that the bot should answer. See rule 1.

### How do I test a chatbot with typos?
Take your clean intent set, make a noisy copy with typos, shorthand, and casing changes, and compare accuracy on both. Start with a gap under 5 points and tune it. See section 7.

### Should the chatbot correct the user's spelling?
No. Answer the meaning. Never change a typed number or code; ask if it matches nothing.

### Does a bigger model fix typos?
Sometimes helps. The studies I opened tested specific models and found different drops. It does not decide when to confirm or ask.
