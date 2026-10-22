# Chatbot Ignores Your Correction: Corrections Not Applied

<!-- SEO
title: Chatbot Ignores My Correction and Uses the Old Value: How to Fix It
description: Why a chatbot confirms a correction ("no, I meant Tuesday") and then uses the old value later, what dialogue-state research and sycophancy studies say, and rules for applying and confirming corrections.
search phrases:
- chatbot ignores my correction
- chatbot goes back to the old answer after I corrected it
- chatbot booked the wrong date after I corrected it
- ai keeps using the wrong name after I fixed it
- how should a chatbot handle user corrections
- dialogue state tracking slot update correction
- chatbot forgets correction
-->

**Frequency**: Common

## Issue: The user corrects a detail ("no, I meant Tuesday"), the assistant says okay, and the old value comes back later in the reply, the summary, or the action.

> **One line:** The bot says it fixed it, and the next step uses the old value.

| | |
|---|---|
| **Channel** | Written for **chat** and voice assistants that collect details and then act (booking, forms, orders). |
| **Stakes** | Low to high. A wrong date or address on a booking or order can cost money; a wrong name is an insult. |
| **Who is affected** | Anyone who fixes a detail mid-conversation, and anyone who does not re-read the final summary |
| **Frequency** | Common in the research on state tracking, which says many models "cannot update slot values appropriately". I found no study of how often live products fail. |
| **Pattern ID** | corrections-not-applied |
| **Family** | [Dialogue management](../README.md) |
| **Goal** | The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. |
| **Primary metric** | Corrections still wrong two turns later. Target: 0 (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/corrections-not-applied.md); not yet run) |
| **Will a better model fix this?** | Partly. Models track state better than older systems, but the old value can return from stored state, a form field, or a tool call, so the fix is partly in the product. (Our judgment, not tested.) |
| **Also searched as** | bot reverted my change · I already told you it's Tuesday · correction ignored · wrong value in confirmation · slot overwrite |

## 1. In plain words
People change their minds and fix mistakes mid-conversation. A bot that handles this well replaces the old value everywhere and says what it now has. A bot that handles it badly says "Got it!" and then books the wrong day.

## 2. What it looks like

**Without the fix**
```
User: Book a table for Monday at 7.
Bot:  Sure. Monday at 7 pm for how many?
User: Sorry, I meant Tuesday. Four people.
Bot:  Got it, four people!
...
Bot:  Your table for four is booked for Monday at 7 pm.
```

**With the fix**
```
User: Sorry, I meant Tuesday. Four people.
Bot:  Updated: Tuesday at 7 pm, four people. Is that right?
User: Yes.
Bot:  Booked: Tuesday at 7 pm for four.
```
The fixed bot replaces the old value, reads back the new state, and uses it in the action.

## 3. Why it happens
These are our reading of the pattern, with the sourced cause marked.
- **State inherits old values.** The dialogue-state research I opened says many tracking models "may repeatedly inherit wrong slot values extracted in previous turns".
- **The old value lives in more than one place.** A summary, a form field, or a tool call keeps the first value while the chat text shows the new one.
- **Acknowledgment without update.** The model says "Got it" because that is a natural reply, with nothing tying the sentence to a state write.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Many dialogue-state-tracking models "cannot update slot values appropriately", may "repeatedly inherit wrong slot values extracted in previous turns", and cannot update indirectly mentioned slots well; a model with a slot-specific memory of mentioned values was proposed to address it. | [Sun, Huang and Ding, *On Tracking Dialogue State by Inheriting Slot Values in Mentioned Slot Pools*, IJCAI 2022](https://www.ijcai.org/proceedings/2022/607). Opened; abstract read. | Task-oriented dialogue research on benchmark data, not on live LLM products. |
| A state-tracking method that holds state as a fixed memory and predicts, per slot, whether to overwrite it, rather than predicting the whole state from scratch each turn. | [Kim et al., *Efficient Dialogue State Tracking by Selectively Overwriting Memory*, ACL 2020](https://arxiv.org/abs/1911.03906). Opened; abstract read. | A design reference, not evidence of how often corrections fail. |
| When challenged with a follow-up like "Are you sure?", ten LLMs on seven classification tasks flipped their answers on average 46% of the time, with an average accuracy drop of 17%. | [Laban et al., *Are You Sure? Challenging LLMs Leads to Performance Drops in the FlipFlop Experiment*, arXiv 2311.08596](https://arxiv.org/abs/2311.08596). Opened; abstract read. | A study of classification tasks and pressure to change a correct answer. It is the reverse risk: models changing answers too easily. Included to bound the fix. |
| A benchmark for sycophancy in extended dialogues, where models face iterative user feedback and challenges. | [*TRUTH DECAY*, arXiv 2503.11656](https://arxiv.org/abs/2503.11656). Opened; abstract read. | I read only the abstract and do not use its figures. |

I found no study that measures how often assistants keep using a value the user corrected, and no news report of one. Search results about voice bots booking the wrong date were developer forum posts; I could not open them (a script-rendered page and a security checkpoint), so I do not use them.

**Public incident.** No public incident found. I searched for chatbots and voice assistants that ignored a date or detail correction and found developer-forum threads and vendor advice, not a dated, sourced case.

## 5. The fix

**The principle:** A correction replaces the old value everywhere, the assistant says what it now has, and the action uses it.

**Do this**
1. **Detect corrections.** Phrases like "no, I meant", "sorry, actually", "not X, Y" overwrite the slot named, not add to it.
2. **Overwrite, don't append.** The new value replaces the old one in the state, the summary, and any pending tool call.
3. **Read back the new state.** Reply with the corrected value in the first sentence ("Updated: Tuesday at 7 pm").
4. **Cascade.** If the changed value affects others (a date change alters a price or availability), say what else changed.
5. **Re-check before acting.** The final summary and the tool call use the current state, and the summary is shown before a booking, payment, or send.
6. **Keep a short history, not a competing value.** Keep the previous value only to undo ("change it back"), never as the active value.
7. **Don't flip facts under pressure.** A user's correction of their own details is applied; a user's challenge to a fact the assistant is sure of is checked, not simply accepted.

**Reference design: state with overwrite**
| Turn event | State change | Reply |
|---|---|---|
| User states value | slot = value | Confirm if it matters |
| User corrects value | slot = new value; log old | "Updated: [new]" plus anything it changes |
| Before action | read the state | Summary of the current values; ask for confirmation |
| User says "change it back" | slot = logged old value | "Back to [old]" |

```
When the user corrects a detail, replace the old value everywhere: in what you have recorded, in the summary, and in any pending action. Say the corrected value in your first sentence.
If the change affects other details, say what changed.
Before any booking, order, or send, read back the current values and ask for confirmation.
Apply the user's corrections to their own details. If they challenge a fact you are sure of, check it before agreeing.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user corrects a detail: the first sentence gives the corrected value ("Updated: Tuesday at 7 pm"), plus anything it changes |
| Ask one clarifying question | The "no" may not be a correction of a recorded detail ("no, I don't want a window seat"): ask which detail they mean. Don't ask when the slot is clear |
| Admit uncertainty and show how to check | The user challenges a fact the assistant is sure of: check it and say what the check shows before agreeing. Don't use it on the user's own details, which are simply applied |
| Hand off to a person | The corrected value cannot be applied (the slot is gone or the system will not accept it): say so and offer a person |

Offer choices is not used here: a correction names its own value, and a menu would make the user pick what they already said.

**Don't over-correct.** Do not ask the user to re-confirm every detail every turn, and do not flip correct facts because the user pushed back. Do not treat every "no" as a correction; "no, I don't want a window seat" may mean a different thing than "no, that's the wrong date".

**Hand-off rule.** If the corrected value cannot be applied (the slot is gone, or the system will not accept it), say so and offer a person ([cold transfer](../../human-handoff/failures/cold-transfer.md) for how to pass it on).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/corrections-not-applied.md) has 14 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Correct a date | The new date is read back and used in the action |
| 2 | Correct a name | The old name never returns |
| 3 | Correct then continue for 3 turns | The corrected value survives |
| 4 | Correction that cascades | The reply says what else changed |
| 5 | Challenge to a correct fact | The assistant checks, not flips |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Corrections still wrong two turns later** (primary) | 0 | Log: user correction events, then the value used in the summary and action two turns later | Any |
| Old value in final action | 0 | Compare the action's parameters with the last corrected state | Any |
| Corrections without a read-back | Under 2% | Replies after a correction that do not state the new value | Over 5% |
| Re-confirmation of untouched details (counter-metric) | Under 5% | Confirmation prompts about details the user did not change | Over 10% |
| Flip rate on correct facts under challenge (counter-metric) | Track; set from baseline | Eval set of correct assistant facts challenged by the user | Rising |

### Detection signals (proposed)
Chat signals in a conversation event log that suggest this failure. All are proposed and not yet checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| The action's parameters hold the old value after a correction (metric: old value in final action) | Action event params compared with the last correction event's `new_value` for that slot | The user later said "change it back" and the undo log restored the old value |
| The pre-action summary shows the old value two turns after a correction (primary metric) | Summary event values compared with the correction event's `new_value` | The user made a second correction to that slot in between |
| The reply right after a correction does not state the new value (metric: corrections without a read-back) | Reply text after a correction event, checked for `new_value` | The reply asked one clarifying question because the "no" was not clearly a correction |
| The user corrects the same slot again with the same value within the next two turns | Two correction events on one slot with equal `new_value` | The user is changing the value a third time on purpose |

**Starter rule:** When the user corrects a detail, replace the old value everywhere: in what you have recorded, in the summary, and in any pending action.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: corrections-not-applied
runs: conversation
reads: [correction_event.slot, correction_event.new_value, state.slot_values, reply.text, summary.values, action.params]
trigger: the user corrects a detail, and again before any booking, order, or send
moves: [lead_with_answer, ask_clarifying_question, admit_uncertainty, hand_off]   # short names for the moves in the table
choices: none
on_miss: rewrite
metric: corrections still wrong two turns later
counter_metric: re-confirmation of untouched details
status: proposed
```

## 8. Related patterns
- [Self-correction failure](../../../../../cross-cutting/accuracy/goals/reasoning-quality/failures/self-correction-failure.md): the agent's own errors. This page covers the user's corrections.
- [Conflicting information](../../../../document-processing/goals/agentic-orchestration/failures/conflicting-information.md): contradictory inputs, related when old and new values coexist.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): asking again for what the user already said.
- [No warning of context loss](../../effort-and-memory/failures/no-warning-of-context-loss.md): the old detail may also be lost, not just overridden.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): when the correction is not understood.

## 9. Common questions
### Why does a chatbot go back to the old value after I corrected it?
Often the old value is stored in more than one place, and only the chat text changed. The fix is to overwrite the state, not just reply "Got it".

### How should a chatbot confirm a correction?
Say the corrected value in the first sentence, and before any booking read back the current values.

### Should a chatbot always accept my correction?
For your own details, yes. If you challenge a fact it is sure of, it should check first. Research I opened shows models often flip answers when asked "Are you sure?".

### How do I test whether my bot handles corrections?
Correct a detail, then continue for three turns and check the summary and the final action. See [the test file](../../../tests/corrections-not-applied.md).

---
## Technical section

### T1. Solution architecture
```
turn -> correction detector (cue words + slot match) -> state update (overwrite, log old)
     -> read-back reply -> cascade check -> pre-action summary -> tool call with current state
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Tool calls take parameters from the state, not from earlier text | Orchestrator | Compare tool args to state |
| A correction event always produces a read-back | Reply policy | Log check |
| A pre-action summary uses the current state | Pre-action step | Test 3 |

### T3. Evals
- **Dataset:** 150 multi-turn conversations with one correction each, then 3 further turns and an action.
- **Judge rubric:** is the corrected value used in the summary and the action, and was it read back?
- **Metrics and starting thresholds:** corrected value in action 100%; read-back over 98%. Starting points to tune.
- **Release gate:** block a deploy if an old value appears in the action in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Old value in final action | Any | Over 0.5% of corrections | Check state writes and tool parameter mapping |

### T5. Trade-offs
- Read-backs add a line; they cost less than a wrong booking.
- A strict overwrite loses a value the user later wants back; keep a short undo log.

---
### Deep dive
- **Open question.** I found no live-product measurement of correction failures. The research is on benchmark dialogues and on classification tasks.
- **References.** [Sun et al., IJCAI 2022](https://www.ijcai.org/proceedings/2022/607) (abstract opened); [Kim et al., ACL 2020](https://arxiv.org/abs/1911.03906) (abstract opened); [Laban et al., FlipFlop](https://arxiv.org/abs/2311.08596) (abstract opened); [TRUTH DECAY](https://arxiv.org/abs/2503.11656) (abstract opened).
