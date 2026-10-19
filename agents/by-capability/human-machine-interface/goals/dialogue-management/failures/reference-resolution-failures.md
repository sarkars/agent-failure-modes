# Chatbot Loses Context on "That One" and "The Second One": Reference Resolution Failures

<!-- SEO
title: Chatbot Loses Context on Pronouns and "the Second One": How to Fix Reference Resolution
description: Why a chatbot resolves "it", "that", or "the second one" to the wrong thing, or asks what you mean right after listing the options itself, what coreference research says, and rules for resolving references to what the person just saw.
search phrases:
- chatbot coreference resolution
- chatbot loses context pronoun
- chatbot doesn't understand "the second one"
- chatbot asks which one after listing the options
- ai assistant picks the wrong item when I say "that one"
- how to resolve pronouns in a chatbot conversation
- anaphora resolution chatbot follow-up question
-->

**Frequency**: Common

## Issue: The user says "the second one", "that", or "it", and the assistant picks the wrong item, or asks "which one?" right after listing the options itself.

> **One line:** The bot shows you three options, you pick one by position, and it acts on a different one.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web are PLANNED, not covered here. |
| **Stakes** | Low when the wrong item is only described; medium to high when the bot then acts on it (cancels, buys, sends, deletes). |
| **Who is affected** | Anyone who answers a list or a card by position or pronoun, which is how people talk |
| **Frequency** | Common in follow-up turns, judging by how much research exists on it. I found no study of how often live products resolve references wrong. |
| **Pattern ID** | reference-resolution-failures |
| **Family** | [Dialogue management](../README.md) |
| **Goal** | The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. |
| **Primary metric** | Wrong-referent rate on a labelled set of follow-ups with pronouns and ordinals. Starting target: set from a baseline on your own test set (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Models read context better than older systems, but a model cannot resolve "the second one" if the product never told it what was on screen or in what order. (Our judgment, not tested.) |
| **Also searched as** | bot lost context · chatbot forgot what "it" was · wrong item selected · "which one?" after I just chose · anaphora · pronoun resolution · ordinal reference |

## 1. In plain words
People point instead of repeating names: "the second one", "that", "the cheaper one", "it". A listener who watched the same list knows what they mean. A bot that does not keep track of what it just showed will guess, grab the wrong item, or ask a question it already answered.

## 2. What it looks like

**Without the fix** (illustrative)
```
Bot:  I found three plans: 1) Basic, $10/mo. 2) Plus, $20/mo. 3) Pro, $35/mo.
User: Tell me more about the second one.
Bot:  The Pro plan includes unlimited seats, priority support, and ...
User: No, the second one.
Bot:  Which plan do you mean?
```

**With the fix** (illustrative)
```
Bot:  I found three plans: 1) Basic, $10/mo. 2) Plus, $20/mo. 3) Pro, $35/mo.
User: Tell me more about the second one.
Bot:  Plus, $20/mo: 5 seats and email support. Want to compare it with Pro?
User: Yes, and cancel that.
Bot:  Cancel what: the Plus plan, or your current Basic subscription?
```
The fixed bot ties "second" to the list it just showed, names the item in its reply so the user can catch an error, and asks only when two real candidates remain for an action.

## 3. Why it happens
These are our reading of the pattern; the sources in section 4 describe the symptom.
- **The product never records what was shown.** The model sees text, but the order and the IDs of a list, card carousel, or search result live in the product. Without a stored "last displayed" list, "the second one" has no anchor.
- **Several candidates compete.** "It" can point to the last answer, the main topic, or an item from three turns back, and a rewrite step can pick the wrong one.
- **Early assumptions stick.** Research I opened found models make assumptions in early turns and then rely on them, so one wrong referent carries into later turns.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Questions in human conversations often depend on earlier turns through pronouns or omitted words, which can make them hard for automated systems to interpret. A corpus of about 4.5K conversations and roughly 53K follow-up question-answer pairs has two or three standalone rewrites per question, and rewriting worked well as a preprocessing step for question answering. | [Brabant, Lecorve and Rojas-Barahona, *CoQAR: Question Rewriting on CoQA*, LREC 2022 (arXiv 2207.03240)](https://arxiv.org/abs/2207.03240). Opened; abstract read. | Text question answering, not shopping or support chat. It shows the problem and one fix, not how often products fail. |
| Task-based dialogue systems must work out which objects a user refers to, and this gets harder in visually grounded scenes. Existing methods generalize poorly across domains. LLMs that reason over object metadata plus dialogue history did better than supervised encoder methods in cross-domain few-shot tests on SIMMC 2.1. | [Ijurco and Lopez de Lacalle, *Reasoning over Object Descriptions Improves Coreference Resolution in Task-Based Dialogue Systems*, arXiv 2604.27850, to appear at LREC 2026](https://arxiv.org/abs/2604.27850). Opened; abstract read. The abstract gives no accuracy figures. | A preprint on a shopping dataset. I do not use its numbers. It supports "give the model the object metadata", not a size of effect. |
| A shopping-domain dataset for task-oriented dialogs grounded in scenes has 11K dialogs (117K utterances), with people paraphrasing generated utterances to create diverse referring expressions. | [Kottur et al., *SIMMC 2.0*, arXiv 2104.08667](https://arxiv.org/abs/2104.08667). Opened; abstract read. | Shows a public dataset for building a labelled set. The abstract does not describe the coreference labels, so check the paper before reusing them. |
| Across 15 LLMs on six generation tasks, performance was on average 39% lower in multi-turn than single-turn conversations, mostly from unreliability. Models often make assumptions early, answer too soon, and do not recover from a wrong turn. | [Laban et al., *LLMs Get Lost In Multi-Turn Conversation*, arXiv 2505.06120](https://arxiv.org/abs/2505.06120). Opened; abstract read. | Underspecified instructions revealed over turns, not reference resolution. It supports "a wrong early reading persists", not a rate for pronouns. |

I found no study that measures how often live assistants resolve "it" or "the second one" to the wrong item, and no dated public incident. I searched for news and complaints about a chatbot acting on the wrong list item and found developer discussions and research, not a sourced case. The rights and safety risk is indirect: a wrong referent becomes a harm only when the bot acts on it, so the rules below tie confirmation to the cost of the action.

**Public incident.** No public incident found.

## 5. The fix

**The principle:** Resolve a reference to what the person is looking at or just heard, say which item you chose, and ask only when two real candidates remain and a wrong pick is costly.

**Do this**
1. **Store what you showed.** When you present a list, cards, or search results, save the items with their position and ID as the "last displayed" set for that turn.
2. **Resolve ordinals against that set.** "The second one" means position 2 in the most recent list the user could see, not the second item in your internal ranking.
3. **Resolve pronouns to the most recent salient item.** "It" and "that" go to the item you just described or the one the user just chose. Prefer an item over a topic when the user is asking about a detail.
4. **Name the item in your reply.** Start with it ("Plus, $20/mo: ...") so a wrong pick is visible in one glance.
5. **Ask only when candidates really compete.** If two items fit and the action is costly or hard to undo, ask one question that lists the candidates you already have. Never ask "which one?" about a list you just showed; point to it.
6. **Confirm before acting on a resolved reference.** Before cancel, buy, send, or delete, restate the item and wait for a yes. For read-only answers, answer and name the item.
7. **Handle a changed list.** If the list changed (re-sorted, filtered, refreshed) after the user's last look, resolve against the list they saw and say so, or ask.
8. **Keep one live referent per slot.** A new reference replaces the old one in state, as in [corrections not applied](corrections-not-applied.md).

**Reference design: resolve, name, confirm**
| Reference | Resolve to | Reply |
|---|---|---|
| "the second one" | Position 2 of the last displayed list | Name the item, then answer |
| "it" / "that" | Most recent single salient item | Name the item, then answer |
| "it" with two salient items | Ask, with both named | One question, options named |
| Reference plus a costly action | Resolved item | Restate the item, ask for a yes |

```
When the user refers to something by position or pronoun ("the second one", "it", "that"), resolve it against the list or item you most recently showed, and name that item in your reply.
If two items could be meant and the action is costly or hard to undo, ask one short question that names both. Never ask which one they mean about a list you just showed.
Before you cancel, buy, send, or delete something chosen by a reference, restate the item and ask for a yes.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | One referent is clear: answer about it and name it in the first sentence. Don't use it when two items compete and the action is costly |
| Offer choices: 2-4 options plus "Something else", free text open | Two or three candidates compete, for example "cancel that" with a current plan and a pending order. Name them from state. Don't offer them for a list the user just saw, when the ordinal is clear, or for more than four candidates |
| Ask one clarifying question | No candidate fits ("the third one" when only two were shown): say what was shown and ask. Don't ask when one referent is clear |
| Hand off to a person | The user and the bot disagree about what was meant twice in a row, or the action is high stakes and still unclear |

**Don't over-correct.** Do not ask which item they mean every time a pronoun appears, and do not make the user confirm each read-only answer. Do not tie "it" to the first item ever mentioned just to avoid a question. If every follow-up gets a confirmation, users stop trusting the bot to follow them.

**Hand-off rule.** If two attempts to settle the referent have failed, hand off with a summary of the items shown and what the user said ([cold transfer](../../human-handoff/failures/cold-transfer.md) for how to pass it on).

**Framework used:** none yet.

## 6. How to test it (short version)
There is no full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | List of three, user says "the second one" | The reply names item 2 and answers about it (rules 2, 4) |
| 2 | One item just described, user says "how much is it?" | The reply names that item (rules 3, 4) |
| 3 | List re-sorted after the user's last look | The bot resolves against the old list or asks (rule 7) |
| 4 | "Cancel that" with two candidates in state | One question naming both, no action yet (rules 5, 6) |
| 5 | "The third one" when two were shown | The bot says what it showed and asks (rule 5) |
| 6 | Clear ordinal after a list the bot just gave | No "which one?" question (rule 5) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Wrong-referent rate on a labelled set of follow-ups with pronouns and ordinals** (primary) | Set from baseline; lower is better | Labelled test set: each follow-up has the intended item ID; compare to the item the reply named or acted on | Rising after a change |
| Actions on a wrong item | 0 | Log the item ID in the action and compare it with the item the user's reference pointed to in labelled samples | Any |
| "Which one?" questions about a list shown in the previous turn | Under 2% of reference turns | Log: clarifying question in the turn after a list event | Over 5% |
| Resolved-item name missing from the reply | Under 5% | Check that the reply text includes the resolved item name | Over 10% |
| Confirmations on read-only references (counter-metric) | Under 5% | Confirmation prompts after a read-only reference | Over 10% |

### Detection signals (proposed, not yet calibrated)
Chat signals in a conversation event log that suggest this failure. Proposed and not yet checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The user repeats the reference right after the bot's reply ("no, the second one") | Next user turn contains an ordinal or "no" plus the same reference | The user is adding a new detail, not repeating |
| The bot asks "which one?" or "what do you mean?" within one turn of a list event | Clarifying question after a list or card event | Two of the listed items were really both candidates, such as items from two lists |
| The item ID in the reply or action differs from the item at the referenced position in the last display | Display event positions compared with the reply's item ID | The list was refreshed and the reply said so |
| The next user turn corrects the item ("not that one, the other plan") | Next-turn label of correction after a reference turn | The user changed their mind |

**Starter rule:** resolve "the second one", "it", and "that" against the list or item you most recently showed, name the chosen item in your reply, and ask only when two items could be meant and a wrong pick is costly.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: reference-resolution-failures
runs: conversation
reads: [display_event.items, display_event.positions, state.last_referent, user_turn.reference, reply.text, action.params]
trigger: the user turn contains a pronoun or ordinal reference, and again before any action on a referenced item
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]   # short names for the moves in the table
choices: ["<candidate A from state>", "<candidate B from state>", "Something else"]
on_miss: rewrite
metric: wrong-referent rate on a labelled set of follow-ups with pronouns and ordinals
counter_metric: confirmations on read-only references
status: proposed
```

## 8. Related patterns
- [Guessing instead of asking](guessing-instead-of-asking.md): the request has several readings. This page is narrower: the words point to an item the bot already showed or named, so the answer is usually in the display and state, and the bot should look there before asking.
- [Corrections not applied](corrections-not-applied.md): the user fixes a value and the old one returns. This page is about picking the item a reference means, not about overwriting a value; the two meet when the user says "no, the other one".
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): asking for what the user already said, close to asking "which one?" after listing the options.
- [Missing the obvious intent](../../embedded-copilots/failures/missing-the-obvious-intent.md): misreading a plain request.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): how to pass the items on when handing off.

## 9. Common questions
### Why does my chatbot lose context when I say "it" or "that"?
Often the product never saved what was on screen, so the model has only text and guesses. Keep the last displayed items in state and pass them to the model.

### Why does the bot ask "which one?" after it just listed the options?
It has no record of the list or its order, or it treats every pronoun as ambiguous. A bot that showed the list can resolve a clear ordinal without asking.

### How should a chatbot resolve "the second one"?
Against the list the user most recently saw, by position, and then name the item in the reply so a wrong pick is easy to catch.

### Should the bot confirm every time?
No. Confirm before an action that is hard to undo; for a read-only answer, name the item and go on.

### How do I test pronoun and ordinal handling?
Build a labelled set of follow-ups with the intended item ID, run it, and compare the item the reply named. Public datasets such as SIMMC 2.0 can seed it; check their labels first.

---
## Technical section

### T1. Solution architecture
```
reply with list -> store display_event (items, positions, IDs)
user turn -> reference detector (ordinal | pronoun | demonstrative) -> resolver (display set, last referent)
          -> 0 candidates: ask | 1: proceed | 2+: cost check -> ask with options | answer + name
          -> action only after restating the item if costly
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Ordinals resolve against the last displayed list | Resolver | Test 1 |
| The reply names the resolved item | Reply policy | Log check |
| Costly actions restate the item first | Policy layer | Test 4 |

### T3. Evals
- **Dataset:** 150 follow-ups with pronouns and ordinals, each with the intended item ID and context (list, card, single item), plus 50 clear requests with no reference.
- **Judge rubric:** was the intended item named or acted on, was a question asked only when needed, and was a costly action restated first?
- **Metrics and starting thresholds:** wrong-referent rate set from baseline; actions on a wrong item 0. Starting points to tune.
- **Release gate:** block a deploy if an action runs on a wrong item in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Actions on a wrong item | Any | More than 1 per day | Check display-event storage and the resolver |

### T5. Trade-offs
- Restating the item adds a line; a wrong cancellation costs more.
- Storing display state costs engineering time; without it, the model can only guess.
- Rewriting follow-ups into standalone questions can help, but a rewrite can also pick the wrong antecedent; log the rewrite next to the raw turn.

---
### Deep dive
- **Open question.** I found no measurement of reference errors in live products. The sources I opened cover text question answering, a shopping dataset, and multi-turn generation tasks.
- **Unverified.** A search summary mentioned a TREC CAsT report noting that "it" can point to the last answer or the main topic. I could not read that PDF, so it is not used above.
- **References.** [Brabant et al., CoQAR, LREC 2022](https://arxiv.org/abs/2207.03240) (abstract opened); [Ijurco and Lopez de Lacalle, arXiv 2604.27850](https://arxiv.org/abs/2604.27850) (abstract opened); [Kottur et al., SIMMC 2.0](https://arxiv.org/abs/2104.08667) (abstract opened); [Laban et al., arXiv 2505.06120](https://arxiv.org/abs/2505.06120) (abstract opened).
