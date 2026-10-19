# Chatbot Ignores "Not": Negation and Exceptions Ignored

<!-- SEO
title: Chatbot Ignores Negation ("Not the Red One"): Why LLMs Return What You Excluded and How to Fix It
description: Why a chatbot offers exactly what the user ruled out ("anything but Monday", "no peanuts"), what negation research says about LLMs, and rules for honoring exclusions and saying what was excluded.
search phrases:
- chatbot ignores negation
- LLM fails negation
- chatbot gave me the thing I said I didn't want
- ai ignores "do not" instructions
- chatbot suggests options I excluded
- how should a chatbot handle "anything but" requests
- negative constraints in chatbots and recommenders
-->

**Frequency**: Common

## Issue: The user rules something out ("not the red one", "anything but Monday"), and the assistant offers or acts on exactly what was excluded, without saying it dropped the exclusion.

> **One line:** You said "not that", and "that" is the first thing the bot shows you.

| | |
|---|---|
| **Channel** | Written for **chat** assistants that search, recommend, book, or filter. Voice and web are planned, not covered. |
| **Stakes** | Low for a wrong suggestion. High when the excluded item is an allergen, a blocked date, or a recipient, or when the bot acts on it. |
| **Who is affected** | Anyone who says what they do not want, especially people with a hard limit (diet, budget, schedule) |
| **Frequency** | Common as a model weakness in research (section 4). I found no study of how often live products offer excluded options. |
| **Pattern ID** | negation-and-exceptions-ignored |
| **Family** | [Dialogue management](../README.md) |
| **Goal** | The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. |
| **Primary metric** | Excluded options offered, per 100 requests with a negation. Target: 0 (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Research finds models weak on negation, and a larger model helps, but a hard exclusion is safer enforced outside the model. (Our judgment, not tested.) |
| **Also searched as** | bot ignored my "not" · LLM can't handle negation · "don't" instruction ignored · excluded item recommended anyway · negative constraint ignored |

## 1. In plain words
People say what they want by saying what they do not want: "not the red one", "nothing with nuts", "any day except Monday". A good bot treats that as a rule for every option it shows. A bad bot hears the topic ("red", "nuts", "Monday") and brings it back.

## 2. What it looks like
Illustrative transcript (invented scenario, not from a real product).

**Without the fix**
```
User: I need a rental car pickup in Denver. Anything but a minivan, please.
Bot:  Here are three options: a Chrysler Pacifica minivan, a Toyota Camry, and a Ford Escape.
User: I said no minivan.
Bot:  Sorry! The minivan is our most popular pick for families. Want me to book it?
```

**With the fix**
```
User: I need a rental car pickup in Denver. Anything but a minivan, please.
Bot:  Skipping minivans. Three options: a Toyota Camry (sedan), a Ford Escape (SUV), a Jeep Cherokee (SUV). Want one of these, or a different type?
```
The fixed bot honors the exclusion in every option, says what it excluded, and keeps the next step open.

## 3. Why it happens
These are our reading of the pattern; the research in section 4 supports the first two.
- **Models attend to the excluded topic, not the "not".** Studies of GPT-style and open models report insensitivity to the presence of negation and shortcut behavior, so "minivan" pulls minivans in.
- **The exclusion is not stored as a rule.** The system keeps "vehicle type = minivan" as a search value, with no way to say "not this value", so a filter or tool call receives the term as a match.
- **Exclusions fade over turns.** A "not" stated once is a single sentence; later turns, tool results, and ranked lists pull the item back with nothing re-checking it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The authors built a dataset of about 400,000 commonsense sentences, about two-thirds with negation. In zero-shot tests, large open LLMs classified affirmative sentences well but struggled with negative ones and often relied on superficial cues. Fine-tuning on negation helped but generalized poorly. | [García-Ferrero et al., *This is not a Dataset*, EMNLP 2023 (arXiv 2310.15941)](https://arxiv.org/abs/2310.15941). Opened; abstract read. | True or false classification of sentences with 2023-era open models, not requests in a product. |
| Testing GPT-neo, GPT-3, and InstructGPT on negation benchmarks, the authors report "insensitivity to the presence of negation", trouble with the lexical semantics of negation, and failures to reason with it, across model sizes and prompts. | [Truong, Baldwin, Verspoor and Cohn, *Language models are not naysayers*, arXiv 2306.08189](https://arxiv.org/abs/2306.08189). Opened; abstract read. A preprint with no venue listed on the page. | Benchmarks and models from 2023. It does not test chat products. |
| On Mistral-7B and Llama-3.1-8B, open models often answer negation questions wrongly although they contain components that process negation correctly. The authors trace the errors to late-layer attention that favors simple shortcuts; ablating those modules improves accuracy. | [Zhou, Zhou, Jia and May, *How Language Models Process Negation*, ICML 2026 listing](https://icml.cc/virtual/2026/poster/65982). Opened; abstract read. | Two small open models and question answering. It explains a mechanism; it is not a rate in products. |

A fourth search, for studies of recommenders and dialogue-state trackers that honor "not X", found no study that measures it directly. I do not claim a rate for live products.

**Public incident.** No public incident found. I searched for chatbots that recommended an item the user had excluded and found general write-ups on negation, not a dated, sourced case.

## 5. The fix

**The principle:** Treat an exclusion as a rule on every option and action, say what was excluded, and check the output against it before showing it.

**Do this**
1. **Detect exclusions.** Cues such as "not", "no", "anything but", "except", "without", "don't", and "other than" create an exclusion on the thing they name.
2. **Store it as a rule, not a search term.** Keep a list of excluded values per slot ("vehicle type: not minivan"), separate from the values the user wants.
3. **Filter before you show.** Check every option, search result, and tool-call parameter against the exclusion list, outside the model when you can. A list in the prompt alone is not a filter.
4. **Say what you excluded.** Open the reply with it ("Skipping minivans."), so a misheard exclusion is caught at once.
5. **Keep exclusions for the whole conversation** until the user lifts one ("minivan is fine after all"). Re-check them on every new list, summary, and action.
6. **Handle exceptions as narrow rules.** "All sizes except small" excludes only small. "No nuts, but almonds are fine" excludes nuts and allows almonds, so keep the exception with the rule.
7. **Admit when you cannot honor it.** If nothing is left after filtering, or the source cannot filter, say so and do not slip the excluded item in. Example: "Every option left is a minivan. Want to see them anyway, or change something else?"

**Reference design: exclusion list**
| Turn event | State change | Reply |
|---|---|---|
| User states an exclusion | add value to the slot's excluded list | "Skipping [value]." plus options that pass |
| Any list or action | check against every excluded list | Show only passing items |
| User lifts an exclusion | remove from the list | "Okay, [value] is back in." |
| Nothing passes the filter | no change | Say so; offer to relax one rule |

```
When the user says they do not want something ("not", "no", "anything but", "except", "without", "don't"), record it as an exclusion for the whole conversation.
Before you show any option or take any action, check it against the exclusions and leave out anything excluded.
Begin your reply by saying what you left out. If nothing is left, say so and ask what to relax.
Never offer an excluded item unless the user lifts the exclusion.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | An exclusion was given and options exist: the first sentence names what was excluded, then the options that pass |
| Ask one clarifying question | The scope of the "not" is unclear ("not Monday" could mean this week or always): ask once. Don't ask when the exclusion is plain |
| Admit uncertainty and show how to check | The source cannot filter or the filter may miss items: say what may slip through and how the user can check it |
| Offer choices | Nothing passes the filter: 2 to 4 ways to relax one rule, plus "Something else" with free text open. Don't offer them when options exist |
| Hand off to a person | The exclusion is safety-critical (an allergen) and the bot cannot verify the result: say so and offer a person |

**Don't over-correct.** Do not read every "no" as an exclusion. "No, that's wrong" may be a correction, covered by [corrections not applied](corrections-not-applied.md). Do not hide whole categories after one off-hand remark, or recite the full exclusion list every turn. Do not ask the user to confirm an exclusion that is clear.

**Hand-off rule.** If a missed exclusion could harm the user (a food allergen, a medication) and the bot cannot check the result against a trusted source, say so and offer a person ([cold transfer](../../human-handoff/failures/cold-transfer.md) for how to pass it on).

**Framework used:** none yet.

**How this differs from corrections not applied.** [Corrections not applied](corrections-not-applied.md) is about a value the user replaced ("Tuesday, not Monday"): the old value returns later. This page is about a value the user ruled out and never replaced ("anything but Monday"): there is no new value to store, so the failure is that the rule is not kept or enforced, even on the first answer. The fix there is overwrite; the fix here is a filter.

## 6. How to test it (short version)
No test file exists yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Anything but a minivan" on a search | No minivan in the list; the reply names the exclusion | 1, 3, 4 |
| 2 | Exclusion in turn 1, a new list in turn 5 | The excluded item is still absent | 5 |
| 3 | "All sizes except small" | Only small is left out | 6 |
| 4 | "No nuts, but almonds are fine" | Almonds can appear; other nuts cannot | 6 |
| 5 | Every available option is excluded | The reply says so and asks what to relax | 7 |
| 6 | "No, that's wrong" with no object | Treated as a correction or asked about, not stored as an exclusion | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Excluded options offered, per 100 requests with a negation** (primary) | 0 | Tag requests with an exclusion cue; count options shown or actions taken that match the exclusion list | Any |
| Excluded value in a tool call or final action | 0 | Compare action parameters with the exclusion list | Any |
| Replies with options that do not state the exclusion | Under 5% | Replies after an exclusion event that omit the excluded value | Over 10% |
| User repeats the exclusion within 3 turns | Under 3% | Same exclusion value in two user turns | Over 8% |
| Wrongly stored exclusions (counter-metric) | Under 2% | Exclusions the user later lifted or called a misreading | Over 5% |

### Detection signals (proposed)
Chat signals in a conversation event log that suggest this failure. All are proposed and not yet checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| An option shown or an action taken matches an exclusion the user stated earlier | Option and action events compared with exclusion events | The user lifted the exclusion in a later turn |
| The user repeats the exclusion ("I said no minivans") within 3 turns | Two user turns with the same excluded value, or a cue like "I said" | The user is adding a second, different exclusion |
| The reply after an exclusion does not mention the excluded value | Reply text after an exclusion event, checked for the value | A short reply to a plain list with every option passing |
| The excluded value appears in the next tool-call arguments as a match term | Tool-call params compared with the exclusion list | A search used to confirm an item is absent |

**Starter rule:** When the user says they do not want something, record it as an exclusion for the whole conversation, leave it out of every option and action, and say what you left out.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: negation-and-exceptions-ignored
runs: conversation
reads: [exclusion_event.slot, exclusion_event.value, state.excluded_values, option.values, reply.text, action.params]
trigger: the user states an exclusion, and again before any list, summary, or action
moves: [lead_with_answer, ask_clarifying_question, admit_uncertainty, offer_choices, hand_off]   # short names for the moves in the table
choices: 2-4 ways to relax one rule plus "Something else" (free text open); only when nothing passes the filter
on_miss: rewrite
metric: excluded options offered, per 100 requests with a negation
counter_metric: wrongly stored exclusions
status: proposed
```

## 8. Related patterns
- [Corrections not applied](corrections-not-applied.md): the user replaced a value and the old one returns. Closest pattern; differences in section 5.
- [Guessing instead of asking](guessing-instead-of-asking.md): an ambiguous "not" (scope unclear) may need one question.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): asking again for what the user already said.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): when the bot has nothing useful to say after filtering.

## 9. Common questions
### Why does my chatbot ignore "not" and give me what I excluded?
Research I opened found language models weak on negation and prone to shortcuts, and many products store only what the user wants. The fix is to keep exclusions as rules and filter every option against them.

### Can I fix this with a better prompt?
It helps, but a line in the prompt is not a guarantee. For hard limits, filter the options in code before the model writes the reply.

### What should a chatbot do when everything left is excluded?
Say so, and offer to relax one rule. It should not slip the excluded item in.

### How do I test whether my bot honors exclusions?
Give an exclusion, then ask for a new list five turns later and check the excluded value is absent. Scenarios are in section 6.

---
## Technical section

### T1. Solution architecture
```
turn -> exclusion detector (cue words + slot match) -> state.excluded[slot] += value
     -> candidate generation -> exclusion filter (code) -> reply with "Skipping [value]" -> action check
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Options are filtered against the exclusion list before display | Post-retrieval filter | Test 1, 2 |
| Tool calls never receive an excluded value as a match term | Orchestrator | Compare args to the list |
| Safety-critical exclusions trigger a hand-off when unverifiable | Reply policy | Test with an allergen |

### T3. Evals
- **Dataset:** 150 multi-turn conversations with one exclusion each, a later list request, and an action (build from your own logs).
- **Judge rubric:** does any shown option or action match the exclusion, and did the reply name it?
- **Metrics and starting thresholds:** excluded options offered 0 per 100; naming rate over 95%. Starting points to tune.
- **Release gate:** block a deploy if an excluded option appears in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Excluded value in a tool call or final action | Any | Over 0.5% of exclusion requests | Check the filter step and tool parameter mapping |

### T5. Trade-offs
- A code filter needs metadata on each option. Without it, use an admit-uncertainty reply for hard limits.
- A naming line adds a few words; it costs less than the user repeating the "not".

---
### Deep dive
- **Open question.** I found no live-product measurement of how often excluded options are offered, and no study of recommenders or dialogue trackers that tests "not X" directly. A search on negated slot values returned general slot-filling papers only.
- **Informal source, not used as evidence.** A prompt-engineering blog argues that fuzzy exclusions ("no horror") are weaker than tight ones. I saw it only in a search summary and did not open it.
- **References.** [García-Ferrero et al., EMNLP 2023](https://arxiv.org/abs/2310.15941) (abstract opened); [Truong et al., 2023](https://arxiv.org/abs/2306.08189) (abstract opened); [Zhou et al., ICML 2026 listing](https://icml.cc/virtual/2026/poster/65982) (abstract opened).
