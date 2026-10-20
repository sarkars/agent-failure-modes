# Chatbot Passes Tests but Fails on Real Messages With Typos: Clean-Lab Testing

<!-- SEO
title: Chatbot Works in Testing but Fails on Real User Typos
description: Chatbot tests use tidy typing, so real messages with typos, slang, and pasted text fail. How to test with field-style input and measure the gap.
search phrases:
- chatbot works in testing but not in production
- how to test a chatbot with typos
- chatbot can't understand misspelled words
- chatbot fails on real user messages
- test chatbot with messy user input
- llm robustness to typos
- chatbot evaluation realistic user inputs
-->

**Frequency**: Common

## Issue: The chatbot is tested on clean, well-typed messages, so it looks fine on the dashboard and then fails on real messages full of typos, fragments, slang, pasted text, and autocorrect damage.

> **One line:** The team tests with tidy sentences, real users type messy ones, and nobody measures the difference; the fix is to run every test in clean and field-style form and track the gap.

| | |
|---|---|
| **Channel** | Written for **text chat** (web, app, messaging). Voice noise and accents: PLANNED, see the note in section 5. |
| **Stakes** | Any. It rises when a misread drug name, amount, or date is acted on. |
| **Who is affected** | Everyone who types on a phone, and most of all people typing in a second language, in a hurry, or with autocorrect on |
| **Frequency** | Common (our judgment). I found no count of how many chatbots are tested only on clean input. |
| **Pattern ID** | clean-lab-testing |
| **Family** | [Measurement and feedback](../README.md) |
| **Goal** | Teams can tell whether conversations really work, and users can tell the team when they don't. |
| **Primary metric** | Performance gap between lab and field inputs. Starting target: under 5 percentage points of task success between the clean and field-style versions of the same intents (tune; not from a source). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A paper on typo robustness found typos hurt open-source models and that instruction tuning may add brittleness (section 4), so a newer model is not a safe assumption. You still have to measure the gap on your own traffic. (Our judgment.) |
| **Also searched as** | chatbot works in testing not production · chatbot can't read typos · test chatbot with messy input · autocorrect breaks chatbot · lab vs field accuracy · chatbot fails on slang |

## 1. In plain words
A team writes test messages like "I would like to refill my prescription." Real users write "need refil of lisinoprl 10mg, pick up tmrw after 5". The bot scores 95% on the first kind and stalls on the second, and the dashboard never shows it. The fix: build the test set from real messy messages, run each intent in clean and field form, and treat the gap as the number to watch.

## 2. What it looks like
Example: a US pharmacy chain's refill chat, tested only on clean sentences.

**Without the fix**
```
User: need refil of lisinoprl 10mg, pick up tmrw after 5
Bot:  I'm sorry, I didn't understand that. I can help with refills, transfers, and store hours.
User: refill
Bot:  Please enter the full name of the medication you would like to refill.
User: lisinopril 10 mg. also my insurance changed
Bot:  I'm sorry, I didn't understand that. I can help with refills, transfers, and store hours.
      (test report: refill intent 96% on the team's clean test set)
```

**With the fix**
```
User: need refil of lisinoprl 10mg, pick up tmrw after 5
Bot:  I read that as a refill of lisinopril 10 mg, pickup tomorrow after 5 pm. Is that right?
      [Yes, refill it] [Different medicine] [Something else]
User: yes. also my insurance changed
Bot:  Done: refill requested for tomorrow after 5 pm. A pharmacist has to update insurance before pickup.
      Want me to ask one to call you today?
      (test report: refill intent 96% clean, 91% field-style, gap 5 points; the gap is the number reviewed)
```
The fixed bot copes with the typos, repeats the drug and time back before acting, and the team's report shows the gap, not just the clean score. (Invented example, not a real product; the percentages are illustrative.)

## 3. Why it happens
These are our reading of the pattern.
- **Test sets are written by the team.** People who know the product type complete sentences with the right product words, so the set misses fragments, slang, and pasted order numbers.
- **Clean data is easy to label and to score.** A messy set needs real logs, review, and a privacy decision, so it gets put off.
- **One headline number.** A single pass rate averages the easy and hard inputs together, and no release gate looks at the field-style slice.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A 2025 paper (MulTypo) tested 18 open-source language models from 3 families on 5 tasks with generated human-like typos. It reports that typos hurt performance, most on generative and reasoning-heavy tasks, that instruction tuning improves clean-input scores but may increase brittleness under noise, and that natural language inference held up comparatively well. | [Liu et al., *Evaluating Robustness of Large Language Models Against Multilingual Typographical Errors*, arXiv 2510.09536](https://arxiv.org/abs/2510.09536). Opened and read (abstract). | Generated typos, open-source models, benchmark tasks, not customer chat. Preprint. |
| In that paper's body, noise was applied at 0%, 10%, 40%, and 70% across 12 languages. For one model family (Qwen) on a math benchmark (MGSM), accuracy fell from about 40 clean to about 27 at 70% noise. | [Same paper, HTML version](https://arxiv.org/html/2510.09536v1). Opened; figures read from the fetched text, not checked in the PDF. | One model on one task at the heaviest noise level. The text I read gives no single average drop, so I give none. |
| NoiseQA (EACL 2021) built question-answering test sets with noise from typing, speech, and character recognition. Its abstract says upstream components can add "considerable" error and performance can degrade substantially from these noise sources. | [Ravichander et al., *NoiseQA*, arXiv 2102.08345](https://arxiv.org/abs/2102.08345). Opened; abstract only. | Question answering, not dialogue, and a 2021 setup with older models. I did not read the tables, so I give no numbers. |

I found no study that measures the lab-to-field gap on a production customer-service chatbot. These papers justify running the test; they do not predict the size of your gap.

**Public incident.** No public incident found where the cause was a bot tested only on clean input. Searches run: "robustness of large language models to typos noisy user input evaluation paper"; "chatbot evaluation noisy user utterances typos performance drop dialogue benchmark"; "intent classification robustness to spelling errors and typos chatbots study"; "NoiseQA keyboard noise F1 drop natural noise question answering". They returned research papers, not a dated incident.

## 5. The fix
**The principle:** Run every test in clean and field-style form, and judge a release on the gap as well as the clean score.

**Do this**
1. **Build a field set from real messages.** For each of your top intents, hold at least 20 field-style messages (starting point, tune) taken from redacted production logs or, before launch, typed by staff on phones. Test: count field messages per intent.
2. **Cover named kinds of mess.** The set must include typos and autocorrect damage, fragments ("refill?"), abbreviations and slang ("tmrw", "rx"), pasted text (an order email, an address block), mixed English and Spanish, and missing information. Test: each kind appears in the set.
3. **Report the gap.** For each intent, score the clean version and the field-style version of the same request, and report both and the difference in percentage points.
4. **Gate the release on the gap.** A change that widens the gap past your alert level blocks the deploy, even if the clean score rises.
5. **Keep the field set out of tuning.** Do not tune prompts on the exact messages used to score; refresh at least a third of the field set every quarter (starting point). Test: no scored message appears in the prompt or training data.
6. **Read back risky details before acting.** When a message needed correcting to be understood, and it contains a drug, amount, date, or account detail, the bot repeats its reading and waits for a yes.
7. **Review real traffic.** A person reads a weekly random sample of production conversations (starting point: 50) and labels turns where noisy input led to a wrong or stalled reply; add them to the field set.

**Reference design: test matrix**
| Intent | Clean version | Field-style version | Kind of mess | Pass if |
|---|---|---|---|---|
| Refill | "I would like to refill my lisinopril 10 mg." | "need refil of lisinoprl 10mg tmrw after 5" | typo, abbreviation | Correct drug and time read back |
| Order status | "Where is order 48213?" | "wheres my thing" + pasted confirmation email | fragment, pasted text | Finds the order number in the paste |
| Return | "I want to return a jacket." | "quiero devolver this jacket, too small" | mixed English and Spanish | Intent recognized, reply in the user's language or asks which |

```
When a message is hard to read, do not say "I didn't understand". Say what you think the user meant, in plain words.
If it contains a medicine, amount, date, or account detail, repeat your reading and wait for a yes before acting.
Never comment on how the user types. If you cannot tell, ask one question.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | One detail is unreadable and it changes the action: "Is that lisinopril 10 mg?" Do not ask when the reading is clear and the action is low risk. |
| Offer choices: 2-4 options plus "Something else", free text open | The message has two likely readings: "Refill", "Check refill status", "Something else". Do not offer them when a single reading is clear, or when options would only restate the user's words. |
| Hand off to a person | Two turns in a row stay unreadable, or the detail is high stakes and unconfirmed. Do not hand off if the user asked to keep typing. |

**Don't over-correct.** Do not make the bot confirm every message; confirm only when the reading was uncertain and the detail is risky, and track confirmation prompts on clean messages as a counter-metric. Do not fix the user's spelling out loud or imply the mess is their fault. Do not build the field set from synthetic typos alone: generated noise can be heavier or lighter than what people type, so keep real messages in it.

**Hand-off rule.** After two unreadable turns in a row, offer a person and pass the message history so the user does not retype ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Voice (PLANNED, not written).** Audio noise and accents will be covered in later voice work. This page has no voice data.

**Framework used:** none yet.

## 6. How to test it (short version)
Full test file: not written. Results: **not yet run**. Each test maps to a rule in section 5.
Test conversations follow the [tests rule](../../../tests/README.md): keep user turns realistic, with typos, short replies, and incomplete information.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Count field-style messages per top intent | 1 | Each intent has at least 20 |
| 2 | List mess kinds in the field set | 2 | All six kinds are present |
| 3 | Score one intent in clean and field form | 3 | Both scores and the gap are reported |
| 4 | Ship a change that widens the gap past the alert level | 4 | The deploy is blocked |
| 5 | Search the prompt and training data for scored messages | 5 | No match |
| 6 | "need refil of lisinoprl 10mg tmrw" | 6 | The bot repeats drug, dose, and time and waits for a yes |
| 7 | "refill 10mg lisinopril tomorrow after 5pm" (clean, clear) | 6 | No read-back prompt; the bot proceeds (do-nothing-special case) |
| 8 | Weekly review of 50 production conversations | 7 | Labeled turns are added to the field set |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Performance gap between lab and field inputs** (primary) | Under 5 percentage points | Task success on the clean set minus task success on the field-style set, same intents, each release | Over 8 points, or widening release over release |
| Top intents with a field set of at least 20 messages | 100% | Count field messages per intent in the eval repo | Any intent below 20 |
| Field-set messages taken from real logs | Over 50% | Source tag on each eval item | Below 30% |
| Noisy-turn failure rate in production | Track; set from baseline | Weekly human sample; share of turns with typos, slang, or pasted text that got a wrong or "didn't understand" reply | Rising two weeks in a row |
| Risky details read back before action | 100% of uncertain readings | Log read-back events against actions taken on drug, amount, date, or account fields | Any action without a read-back |
| Confirmation prompts on clean messages (counter-metric) | Under 5% of clean turns | Count read-back prompts where the parse was confident | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| "Didn't understand" reply right after a message with a low share of dictionary words | Fallback reply event after a user turn with a spelling-error score | The user wrote in a language the bot does not support |
| User retypes the same request with fewer typos in the next turn | Two user turns with the same intent and a lower error score | A deliberate rewording for clarity |
| User sends only a short fragment ("refill") after a fallback | Next user turn under 3 words after a fallback event | A user who prefers short messages and was understood |
| Eval items with no source tag or all marked "synthetic" | Eval repo metadata | A new intent not yet seen in logs |

**Starter rule:** every release is scored on clean and field-style versions of each top intent, and the gap is reported with the score.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: clean-lab-testing
runs: pre_send
reads: [turn.parse_confidence, turn.detail_type, turn.user_text, eval.release_gap]
trigger: a message was hard to read and carries a drug, amount, date, or account detail
moves: [ask_clarifying_question, offer_choices, hand_off]
choices: ["Yes, that's it", "Something different", "Something else"]
on_miss: ask
metric: performance gap between lab and field inputs
counter_metric: confirmation prompts on clean messages
status: proposed
```

## 8. Related patterns
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): closest. It compares service across groups with identity cues changed in paired tests. This page is about whether the tests look like real input at all, for every user, and the gap between clean and field scores.
- [Satisfaction metric gaming](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/satisfaction-metric-gaming.md): the score is pushed up by tuning against a proxy. Here the score is honest but measured on input that is too clean.
- [No way to report bad behaviour](no-way-to-report-bad-behaviour.md): users cannot tell the team when a reply is wrong. This page is about the team's own tests missing the same failures before users hit them; reports from that path are a good source for the field set (rule 7).
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): what the bot says when something fails, including "I didn't understand".

## 9. Common questions
### Why does my chatbot work in testing but fail with real users?
Test messages are usually cleaner than real ones. Real users make typos, send fragments, paste text, and mix languages. Score each intent on both versions and look at the gap (rules 1 to 3).

### How do I test a chatbot with typos?
Start with real, redacted messages from your logs, or have staff type test messages on phones. Add generated typos only as a supplement, since generated noise may differ from what people type (rule 2 and the Don't over-correct paragraph).

### Will a newer model handle typos by itself?
Not safely. In the typo-robustness paper in section 4, instruction tuning improved clean scores but may make models more brittle under noise. Measure the gap on your own field set after every model change.

### Should the bot correct the user's spelling?
No. Say what you think they meant and ask for a yes if the detail is risky (rule 6). Comments on how someone types read as blame.

---
### Deep dive
- **Open question.** I found no study of the lab-to-field gap in a production customer-service chatbot, and no public incident tied to clean-only testing.
- **Read through search summaries only, kept out of the page.** Reported figures from a Yorùbá question-answering typo study (a drop of over 50% for one model at 40% noise), a real-noise multilingual study built from Wikipedia edit history (accuracy gaps of a few points), a behavioral-test error analysis of an intent classifier (failure rates of about 22 to 25% on typo tests), and NoiseQA's F1 drops reached me only through search summaries. The PDFs for NoiseQA, the error-analysis paper, and a 41-model intent-classification paper could not be read by my tool. The 41-model paper's abstract, which I did open, does not mention typos.
- **Modality notes.** Voice: audio noise and accents are PLANNED, with no data here.
- **References.** [MulTypo, arXiv 2510.09536](https://arxiv.org/abs/2510.09536) (opened); [MulTypo HTML](https://arxiv.org/html/2510.09536v1) (opened); [NoiseQA, arXiv 2102.08345](https://arxiv.org/abs/2102.08345) (opened, abstract).
