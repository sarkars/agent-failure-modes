# Chatbot Asks Too Many Confirmation Questions: Over-Confirmation

<!-- SEO
title: Chatbot Asks Too Many Confirmation Questions: How to Fix It
description: Why bots ask "are you sure?" on every step, what design guides and warning-fatigue research say, and a rule for confirming only what is costly or hard to undo.
search phrases:
- chatbot asks too many confirmation questions
- confirmation fatigue chatbot
- chatbot keeps asking are you sure
- how many confirmations is too many in a chatbot
- when should a chatbot ask for confirmation
- implicit vs explicit confirmation conversation design
- chatbot asks me to confirm every step
- confirmation dialog fatigue
-->

**Frequency**: Common

## Issue: The assistant asks "are you sure?" or "is that right?" on routine steps, so confirmations pile up and the few that guard a costly step get lost among the rest.

> **One line:** When the bot confirms everything, a confirmation stops meaning "this one matters."

| | |
|---|---|
| **Channel** | Written for **chat**. The same rule applies to voice assistants; voice detection is PLANNED, not built. |
| **Stakes** | Low per prompt; medium overall, because it slows every task and can train users to click "yes" on the one that counts. |
| **Who is affected** | Anyone doing a multi-step task by chat: booking, ordering, account changes, form-filling |
| **Frequency** | Common as a design habit. I found no published measure of how often live chatbots over-confirm. |
| **Pattern ID** | over-confirmation |
| **Family** | [Dialogue management](../README.md) |
| **Goal** | The conversation follows what the person means: references, corrections, exceptions, and several requests at once, and asks and confirms only what matters. |
| **Primary metric** | Confirmation prompts per task, and the share of confirmations that guard a consequential step. Starting targets: set from a baseline; guard share 100% of explicit confirmations (tune). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | Partly. A model can learn to skip obvious confirmations, but which steps are costly depends on your business rules, so the product has to decide. (Our judgment, not tested.) |
| **Also searched as** | confirmation fatigue · bot keeps asking are you sure · too many confirmation prompts · chatbot double-checks everything · unnecessary confirmation step |

## 1. In plain words
Some steps need a "yes" first: paying, deleting, sending. Most do not. A bot that stops to ask "Is that right?" after every detail, then asks again before each step, wastes the person's time. It also teaches them to answer "yes" without reading, which defeats the confirmation that really matters.

## 2. What it looks like
Illustrative transcript (invented for this page, not from a real product).

**Without the fix**
```
User: Book me a haircut Thursday at 3 with Maria.
Bot:  You want a haircut. Is that correct?
User: Yes.
Bot:  Thursday. Is that correct?
User: Yes.
Bot:  Maria at 3 PM. Is that correct?
User: Yes!
Bot:  Are you sure you want to book this appointment?
User: YES.
```

**With the fix**
```
User: Book me a haircut Thursday at 3 with Maria.
Bot:  Booked: haircut with Maria, Thursday at 3 PM. It is free to cancel until Wednesday at 3 PM.
      Want a reminder the day before?
```
Nothing was costly or hard to undo, so there is one implicit confirmation inside the answer. The user can still correct it.

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom and the guidance.
- **Confirming feels safe.** Each extra check looks free to the team that adds it, so nobody removes one. The cost lands on the user, as extra turns.
- **No rule for which steps are costly.** Without a list of steps that are hard to undo, every step gets the same prompt.
- **Details are checked one at a time.** The bot confirms each slot as it is filled, not once for the whole group.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Google's conversation design guide separates explicit confirmation (needs a reply), implicit (states the detail and moves on) and none. It calls implicit confirmation of parameters the one to "use most of the time", and explicit confirmation of actions rare, for actions that are "difficult to undo". Explicit confirmation of parameters should be used "sparingly, only when the cost of misunderstanding the user is high." | [Google, *Confirmations*, Conversation design guide for Assistant](https://developers.google.com/assistant/conversation-design/confirmations). Opened and read. | Design guidance, not an experiment. Written for Google Assistant. |
| Amazon's Alexa design guide says to ask users to confirm actions "that have a high consequence for error", to use implicit confirmation "when the likelihood of a mistake is low, and the consequences of a failure are minor", and not to require extra confirmation on a stop or exit command unless significant data or progress would be lost. | [Amazon, *Be trustworthy*, Alexa design principles](https://developer.amazon.com/en-US/alexa/alexa-haus/design-principles/be-trustworthy). Opened and read. | Voice design guidance. Not tested on chat. |
| Nuance's Mix guide warns that "Unnecessary confirmation can double the length of the interaction and frustrate users", and suggests confirming a group of related items once instead of each piece. | [Nuance Mix, *Requesting confirmation*](https://docs.nuance.com/mix/best-practices/dialog-planning/confirm/). Opened and read. | Vendor guidance for voice and chat dialogs. No data shown on the page. |
| Siemens' conversational design guidelines for industrial chatbots say to confirm before consequential changes, but not more than once, because repeated checks make the chatbot seem distrustful. | [Siemens Industrial Experience, *Confirming request*](https://ix.siemens.io/docs/guidelines/conversational-design/designing-conversations/confirming-request). Opened and read. | A design guideline for one company's bots. The "distrustful" effect is their claim, not a measurement. |
| In a lab study of pop-up dialogs, without a design countermeasure, increased habituation cut the share of people who noticed a change in the dialog by about a factor of three. | [Bravo-Lillo et al., *Harder to Ignore? Revisiting Pop-Up Fatigue*, SOUPS 2014](https://usenix.org/conference/soups2014/proceedings/presentation/bravo-lillo). Opened; abstract read, not the full paper. | Security pop-ups, not chat. The abstract gives no sample size. Habituation here means repeated exposure to the same dialog. |
| Over four days at two teaching hospitals, 93% of 2,455 drug interaction alerts were overridden (461 physicians, 18,354 orders). The authors concluded alert fatigue did not appear to explain the high rate, and alert volume did not predict override rate. | [Bryant, Fletcher and Payne, *Applied Clinical Informatics*, 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4187095). Opened; abstract and results read. | Clinical alerts, not chat. It shows that warnings can be dismissed at a high rate, but it does not support "more prompts cause more dismissals". |

I found no study that measures confirmation counts in chatbot tasks, or how many confirmations users accept before they stop reading them. The design guides above agree with each other and with the pop-up result; none is a chat experiment. I did not find the phrase "confirmation fatigue" in any chatbot research I opened.

**Public incident.** No public incident found. I searched for reports of a chatbot's repeated confirmations causing a wrong approval, and found design guidance and forum-style complaints, not a dated, sourced case.

## 5. The fix

**The principle:** Confirm only what is costly or hard to undo. Confirm everything else inside the next reply, where the user can still correct it.

**Do this**
1. **Sort every step into three classes.** Read-only or easily reversed (no confirmation, or implicit), costly or hard to undo (explicit), and in between (implicit with an undo).
2. **Confirm details implicitly.** State the understood value in your next reply ("Thursday at 3 PM with Maria") and let the user correct it. Do not ask a question for each slot.
3. **Use explicit confirmation only for costly or hard-to-undo steps.** Payments, deletions, messages sent for the user, cancellations that lose data. Read back the amount, date, or recipient (see [under-confirmation, DM-08 in the roadmap](../../../roadmap/conversation-design.md)).
4. **Confirm once, as a group.** Collect the details, then ask one question that covers the whole step. Never ask the same thing twice.
5. **Skip confirmation when the user just said it.** If the user gave a value and the bot is acting on it as stated, do not ask "is that right?" ([re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md)).
6. **Never confirm a stop, exit, or "no".** Honor it. Ask only if the user would lose significant data or progress.
7. **Make the one explicit confirmation specific.** "Pay $84.20 to Dana's Plumbing from the card ending 4417?" beats "Are you sure?".
8. **Make the step undoable where you can.** "Free to cancel until Wednesday 3 PM" often replaces a confirmation.

**Reference design: which confirmation for which step**
| Step | Cost of a mistake | Confirm how |
|---|---|---|
| Value the user just stated (date, size, name) | Low | Implicit: say it back in the next reply |
| Action easy to reverse (booking with free cancel, adding to cart) | Low | Implicit: say what was done and how to undo |
| Action costly or hard to undo (payment, delete, send, close account) | High | Explicit: one question naming the amount, date, or recipient |
| Group of details collected over several turns | Mixed | One summary and one confirmation before the costly step |
| Stop, exit, or "never mind" | Low | None; honor it |

```
Confirm a detail by using it in your next reply, not by asking about it.
Ask an explicit yes/no question only before a step that is costly or hard to undo, and name what will happen (amount, date, recipient).
Ask once for a group of details, never once per detail, and never repeat a confirmation the user already gave.
Do not ask the user to confirm a stop, exit, or cancel unless they would lose saved work.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Low-cost steps: do the step and restate the detail in the same reply. Do not use it for a costly step the user has not approved. |
| Ask one clarifying question | The one confirmation before a costly step: a single specific question. Do not ask it for details the user just gave. |
| Hand off to a person | The user says the confirmations are not working, or twice cannot get past one. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not remove confirmation from payments, deletions, or messages sent for the user. A user who says "go ahead" about a plan is not approving each costly step inside it. Under-confirming costs more than an extra question; see [irreversible action without confirmation](../../../../external-actions/goals/action-execution/failures/irreversible-action-without-confirmation.md). Also keep confirming when the bot is unsure it understood: confirmation of a low-confidence value is a clarifying question, not over-confirmation.

**Hand-off rule.** If the user types "stop asking" or a similar complaint, stop confirming non-costly steps in that session. If the user cannot get past a required confirmation twice, offer a person and pass along the pending step ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet for this pattern. These are the proposed checks; results: **not yet run**.

| # | Scenario | Pass if (fix rule) |
|---|---|---|
| 1 | A four-detail request with a free-to-cancel booking | Zero explicit confirmations; details restated once (rules 2, 8) |
| 2 | A payment request | One explicit confirmation naming amount and recipient (rules 3, 7) |
| 3 | The user states a date and the bot acts on it | No "is that right?" (rule 5) |
| 4 | The user says "stop" | Honored with no confirmation (rule 6) |
| 5 | Three details given across turns, then a costly step | One grouped confirmation, not three (rule 4) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Confirmation prompts per task** (primary) | Set from baseline; lower is better for non-costly tasks | Log bot turns tagged `confirmation` per completed task, by task type | Rising after a change |
| **Share of explicit confirmations that guard a consequential step** (primary) | 100% | Label each explicit confirmation by the step's cost class from a maintained list | Below 90% |
| Consequential steps with no explicit confirmation (counter-metric) | 0 | Executed steps on the costly list with no confirmation turn before them | Any |
| Bare "yes" replies within 2 seconds of a confirmation | Track; set from baseline | Reply time and text after a confirmation turn | Rising two weeks in a row |
| Repeated confirmations of the same value | 0 | Same slot confirmed twice in one task | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice is PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| More than one bot confirmation turn per task step | Count of `confirmation`-tagged turns in a step | A costly step that also needed a low-confidence value checked |
| The same value confirmed twice | Same slot value in two confirmation turns | The user changed the value in between |
| Explicit confirmation before a step on the low-cost list | Confirmation turn followed by a step with cost class "low" | The business rule changed the step's cost class and the list is out of date |
| The user answers "yes" or "ok" very fast to several confirmations in a row | Reply latency and text after confirmation turns | A user who is simply in a hurry and the questions were fine |
| The user says "I already told you" or "stop asking" | Phrase classifier on the next user turn | The user is correcting a wrong value |

**Starter rule:** confirm a detail by using it in your next reply; ask an explicit yes/no question once, and only before a step that is costly or hard to undo.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: over-confirmation
runs: pre_send
reads: [turn.draft_reply, step.cost_class, state.confirmed_slots, state.pending_step]
trigger: the draft reply asks the user to confirm something
moves: [lead_with_answer, ask_clarifying_question, hand_off]
choices: none
on_miss: rewrite
metric: confirmation prompts per task; share of confirmations that guard a consequential step
counter_metric: consequential steps with no explicit confirmation
status: proposed
```

## 8. Related patterns
- [Under-confirmation of consequential details (DM-08, not yet written)](../../../roadmap/conversation-design.md): the opposite failure. This page is about asking too often on cheap steps; that one is about not asking on costly steps. Fix both with one cost-class list.
- [Irreversible action without confirmation](../../../../external-actions/goals/action-execution/failures/irreversible-action-without-confirmation.md): the agent executes a delete, payment, or deployment with no approval step. It is the cost of cutting confirmations too far.
- [Guessing instead of asking](guessing-instead-of-asking.md): asks too little about a genuinely ambiguous request. Over-confirmation asks about things that were clear.
- [Corrections not applied](corrections-not-applied.md): confirming a correction is fine; confirming untouched details is not.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): asking for what the bot already has.

## 9. Common questions
### Why does my chatbot keep asking me to confirm?
Usually it confirms each detail and each step the same way, with no rule for which steps are costly. Design guides from Google, Amazon, and Nuance say to confirm costly steps and not the rest.

### When should a chatbot ask for confirmation?
Before a step that is costly or hard to undo, such as a payment, a deletion, or a message sent for you. Google's guide describes these as the rare cases for explicit confirmation.

### What is implicit confirmation in a chatbot?
The bot says the detail back inside its next reply ("Booked for Thursday at 3 PM") and does not ask a question. The user can still correct it.

### How many confirmations are too many?
I found no study with a number. A practical test: if a confirmation is on a step the user could undo in one tap, or on a value they just typed, it is too many. Siemens' guideline says to confirm no more than once.

### Does confirmation fatigue make people click "yes" without reading?
Lab work on pop-up dialogs found that repeated exposure sharply cut the share of people who noticed a change. That is a different setting. A hospital study of drug alerts found high override rates but did not tie them to alert volume.

---
## Technical section

### T1. Solution architecture
```
draft reply -> is it a confirmation? -> step cost class (read | reversible | costly)
            -> allow | rewrite as implicit | merge with pending group | block duplicate
            -> log (confirmation turn, cost class, slot, outcome)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Costly steps carry an explicit confirmation naming amount, date, or recipient | Policy layer before the tool call | Tests 2 and 5 |
| No confirmation turn for a value the user stated this turn | Reply policy | Tests 1 and 3 |
| A confirmed slot is not confirmed again | Dialogue state | Log check |
| Stop and exit commands are honored without a question | Dialogue manager | Test 4 |

### T3. Evals
- **Dataset:** 100 task conversations (low-cost, mixed, and costly), each with step cost labels and the expected number of explicit confirmations.
- **Judge rubric:** did the bot confirm exactly the steps labeled costly, restate details implicitly, and never repeat a confirmation?
- **Metrics and starting thresholds:** explicit confirmations on non-costly steps 0; costly steps with no confirmation 0. Starting points to tune.
- **Release gate:** block a deploy if a costly step runs with no explicit confirmation in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Costly step with no explicit confirmation | Any | More than 1 per day | Check the cost-class list and the policy layer |
| Confirmation prompts per task | Up from baseline | Doubled | Diff the last prompt or flow change |

### T5. Trade-offs
- Fewer confirmations speed tasks and raise the cost of each error. Tie the choice to the cost class, and keep an undo path.
- A cost-class list needs an owner. If it goes stale, the bot either over- or under-confirms.

---
### Deep dive
- **Open question.** I found no study of confirmation counts in chatbot tasks. The evidence is design guidance plus warning-fatigue work in other settings, and the hospital study I opened did not support alert volume as the cause of overrides.
- **References.** [Google, *Confirmations*](https://developers.google.com/assistant/conversation-design/confirmations) (opened); [Amazon, *Be trustworthy*](https://developer.amazon.com/en-US/alexa/alexa-haus/design-principles/be-trustworthy) (opened); [Nuance Mix, *Requesting confirmation*](https://docs.nuance.com/mix/best-practices/dialog-planning/confirm/) (opened); [Siemens, *Confirming request*](https://ix.siemens.io/docs/guidelines/conversational-design/designing-conversations/confirming-request) (opened); [Bravo-Lillo et al., SOUPS 2014](https://usenix.org/conference/soups2014/proceedings/presentation/bravo-lillo) (abstract opened); [Bryant et al., 2014](https://pmc.ncbi.nlm.nih.gov/articles/PMC4187095) (opened).
