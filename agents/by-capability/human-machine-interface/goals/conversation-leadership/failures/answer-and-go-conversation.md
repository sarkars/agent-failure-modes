# Chatbot Answers, Then Stops: The Answer-and-Go Conversation

<!-- SEO
title: Chatbot Answers Then Stops: Fix Dead-End Conversations
description: Why a chatbot answers the question and then goes quiet, with before/after examples, a tested fix, guardrails, evals, and alerts.
search phrases:
- chatbot only answers the question and doesn't ask follow-up questions
- chatbot dead end no next step
- chatbot ends conversation too early
- chatbot doesn't close the loop / confirm the problem is solved
- how to make a chatbot proactive instead of reactive
- why does my AI chatbot feel flat or robotic
- chatbot not moving the sales conversation forward
-->

**Frequency**: Very Common

## Issue: Why a chatbot answers the question and then goes quiet, with before/after examples, a tested fix, guardrails, evals, and alerts.

> **One line:** The bot answers exactly what was asked, then stops. It doesn't find out what the user is trying to do, doesn't move them toward it, and doesn't confirm the problem is solved.

| | |
|---|---|
| **Channel** | Written for **chat**. Applies to voice and visual (notes at the bottom; those are planned, not yet written). |
| **Stakes** | Any. The cost is lost sales at low stakes and unresolved problems at high stakes. |
| **Who is affected** | Every user, and most visibly those with a real goal behind a small first question |
| **Frequency** | Very common. Observed in practice; I found no study that measures how often it occurs. |
| **Pattern ID** | answer-and-go-conversation |
| **Family** | [Conversation leadership](../README.md) |
| **Goal** | Every conversation moves the user toward what they are trying to do and ends with confirmation that it worked. |
| **Primary metric** | Confirmed-resolution rate. Starting target: gap to containment rate under 10 points. |
| **Also searched as** | chatbot dead end · chatbot doesn't ask follow-up questions · chatbot ends conversation too early · chatbot no next step · reactive chatbot · chatbot not closing the loop |

## 1. In plain words
A good human salesperson, support agent, or advisor treats the user's first question as a doorway. The bot treats it as the whole job. It answers, waits, and the conversation dies. Nobody is rude and nothing is wrong, but nothing moves forward either.

## 2. What it looks like

**Without the fix** (low stakes, sales)
```
User: Do you ship to Austin?
Bot:  Yes, we ship to Austin. Delivery takes 3-5 business days.
User: ok
      (user leaves; no sale, no lead captured, bot never learned what they wanted)
```

**Without the fix** (higher stakes, support)
```
User: My card got declined twice abroad and now the app says "account restricted".
Bot:  Account restrictions can be caused by suspected fraud. You can review your recent transactions in the app.
User: ok
      (user leaves; bot never checked the card is safe, or what happens next, or who to contact)
```

**With the fix** (sales)
```
User: Do you ship to Austin?
Bot:  Yes, we ship there, usually in 3-5 business days. Is this for your home or an office?
User: Home. Our sofa has gone saggy.
Bot:  Sorry about that. Is the sagging the main thing, or do you also need a different size? I can show you
      three firm-seat sofas that arrive in that window.
```

**With the fix** (support)
```
User: My card got declined twice abroad and now the app says "account restricted".
Bot:  That's usually a fraud-protection hold, and it's fixable. First: are you safe to use the card right now,
      or is it lost or stolen?
User: No, I have it, it's fine.
Bot:  Good. I'm raising an unrestriction request now. A specialist reviews it within 4 hours and you'll get a
      text message. If it's urgent, I can connect you to the team now. Does that work, or do you need the card tonight?
```
The fixed bot answers first, then makes one useful move that carries the user's real goal forward.

## 3. Why it happens
- **The bot is told to answer, not to lead.** Prompts say "be concise" or "don't ask unnecessary questions," which suppresses any forward move.
- **Nothing tracks the user's goal.** The bot sees a message, not a conversation with a goal and a stage, so it has nothing to advance toward.
- **Metrics reward ending the session.** Containment or deflection rates count a conversation that stops as a success, even when the user gave up.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Question-asking, especially follow-up questions, raised how much conversation partners liked each other, because they felt more responded to. In speed dating, people who asked more follow-ups were likelier to get a second date. | Huang, Yeomans, Brooks, Minson, Gino (2017), *J. Personality and Social Psychology*. [APS summary](https://psychologicalscience.org/news/minds-business/asking-questions-increases-likability.html) | Human-to-human conversations, not bots. It supports the mechanism, not a bot-specific effect size. |
| In large, complex sales, skilled sellers won through question-based discovery, not closing techniques. | Rackham (1988), *SPIN Selling*. See [solutions library](../../../solutions-library/spin-questioning.md) | Sales research, not chatbot research. The "35,000 calls" figure is widely repeated but sources differ on the details. |
| The CFPB warned that finance chatbots can trap users in "doom loops" with no way out to a human. It estimated 37% of the US population (98 million people) used a bank chatbot in 2022. | CFPB issue spotlight (June 2023), via [Consumer Finance Monitor](https://www.consumerfinancemonitor.com/2023/06/08/new-cfpb-report-highlights-concerns-with-growing-use-of-chatbots-by-financial-institutions/) | Regulatory concern about banks, read here through law-firm summaries. A Clark Hill review argued the complaint data behind it is thin (64 complaints mentioning chatbots over five years). The CFPB withdrew 67 guidance documents in May 2025, pending review; **I could not confirm whether this spotlight was among them**, so check the CFPB's current guidance before citing it as live. |
| 64% of surveyed customers said they would prefer companies didn't use AI for customer service. 53% would consider switching. (n=5,728, Dec 2023) | [Gartner press release, July 2024](https://www.gartner.com/en/newsroom/press-releases/2024-07-09-gartner-survey-finds-64-percent-of-customers-would-prefer-that-companies-didnt-use-ai-for-customer-service) | Attitudes toward AI in general. It doesn't isolate this specific failure. |
| In a banking-chatbot study of 1,373 users, abandonment was predicted by repeated typing, the bot admitting it didn't recognise intent, and the bot asking mid-conversation what the user wanted. A 2020 CHI paper found warning signs such as three consecutive turns with no progress. | [NYCU abandonment study](https://scholar.nycu.edu.tw/zh/publications/predicting-and-exploring-abandonment-signals-in-a-banking-task-or/), Li et al. (CHI 2020) | Read from search summaries; I couldn't open the full papers. They study dead ends and breakdowns, which is close to this pattern but not the same. |

## 5. The fix

**The principle:** Every bot turn does three jobs: **Answer** what was asked, **Advance** toward what the user is really trying to do, and **Close the loop** when the goal is met.

**Do this**
1. **Track a goal and a stage.** After the first one or two turns, store what the user is trying to do (`buy`, `fix`, `learn`, `decide`, `complain`) and where they are (`exploring`, `comparing`, `ready`, `post-action`).
2. **Answer first, then advance.** Never hold the answer back to ask a question.
3. **Make exactly one forward move per turn,** chosen from the table below by goal and stage. Never more than one question.
4. **Close the loop explicitly.** When the user's goal looks met, summarise what was done, ask them to confirm it worked, and say what happens next and how to come back. "Anything else?" alone is not a close.
5. **Know when to stop.** If the user signals they're done, in a hurry, or upset, skip the advance and just help.

**Choose the forward move**
| Goal | Stage | Forward move | Example |
|---|---|---|---|
| buy | exploring | Discovery question (Situation or Problem, see [SPIN](../../../solutions-library/spin-questioning.md)) | "Is this for home or an office?" |
| buy | comparing | Narrow the choice | "Is price or delivery time more important?" |
| buy | ready | Offer the concrete next step | "Want me to hold this size for 24 hours?" |
| fix | any | Check safety/impact first, then act | "Is the card in your hands?" |
| fix | post-action | Verify the fix | "Try it now: does the app load?" |
| learn | any | Check understanding or offer depth | "Want the 2-minute version or the step-by-step?" |
| decide (high stakes) | any | Name the next safe step or a human | "I'd suggest speaking to an adviser; I can book one." |
| complain | any | Acknowledge, then state the action and timeline | "I've logged it; you'll hear within 4 hours." |

**Reference design: a turn policy you can paste into a system prompt**
```
Every reply has three parts, in order:
1. ANSWER the user's question directly and fully.
2. ADVANCE: add exactly ONE of: a single question, a next-step offer, or a verification check.
   Pick it from the user's goal and stage. Never ask two questions.
3. CLOSE when the goal looks met: summarise what happened, ask "Did that solve it?",
   and say what happens next and how to reach us.
Skip step 2 if the user says they're done, is in a hurry, is upset, or has declined two prior prompts.
If you can't help with the goal, ADVANCE by offering a human or another channel, with context passed along.
```
State to keep between turns:
```json
{ "goal": "buy", "stage": "exploring", "known": {"destination": "Austin", "use": "home"},
  "advances_declined": 0, "closed": false }
```

**Don't over-correct.** The opposite failure is a bot that interrogates, upsells, or won't let the user leave (see [over-clarification](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/over-clarification.md)). Four guardrails: one move per turn; stop advancing after two declined prompts (`advances_declined >= 2`); in high-stakes or distressed contexts, the forward move is a safe next step or a handoff, never a sales prompt; and no filler. A tag-on like "Want me to explain more?" after every reply is a known annoyance. Users and tech writers have complained about it in general-purpose assistants, and one writer reported that a plain "do not ask follow-up questions" instruction wasn't enough to stop it ([PCWorld](https://www.pcworld.com/article/3221302/i-got-chatgpt-stop-its-annoying-follow-up-questions-with-one-prompt.html)). A forward move counts only if it ties to the user's stated goal.

**Hand-off rule.** If the goal can't be advanced (out of scope, repeated non-progress, or the user asks), the forward move is a handoff to a human with the conversation summary attached, so the user doesn't have to repeat themselves. See [poor-escalation](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/poor-escalation.md).

**Framework used:** [SPIN questioning](../../../solutions-library/spin-questioning.md). Planned: closing protocol, channel-fit matrix.

## 6. How to test it
Thresholds below are starting points to tune for your product, not published benchmarks.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Sales: "Do you ship to Austin?" (informational) | The reply answers it **and** contains exactly one forward move |
| 2 | Support: the bot gives fix steps | The bot asks the user to confirm the fix worked, or says how to check |
| 3 | User says "that's all, thanks" | The bot closes in one turn, with no new question or pitch (guards against over-correcting) |
| 4 | User ignores two forward moves | The next turn contains none |
| 5 | High stakes: "my insurance claim was denied" | The forward move is a safe next step or a human, not an upsell |
| 6 | Out-of-scope request | The bot offers a handoff with a summary rather than ending |
| 7 | Over 20 varied scenarios | No reply contains more than one question |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Silent-exit rate (sessions ending on a bot message with no confirmed resolution) | Trend down; set from a 4-week baseline | Sessions with no user reply after the bot's last message and no resolution marker, divided by all sessions | +20% vs baseline |
| Confirmed-resolution rate vs. containment rate | Gap under 10 points | Sessions where the user confirmed it worked, divided by sessions closed without a human | Gap over 20 points |
| Re-contact within 72 hours (same user, same topic) | Trend down; set from baseline | Match on user and topic classifier | +15% vs baseline |
| Forward-move coverage | Over 90% of non-final turns | Rule check or judge against the move menu | Under 80% |
| Questions per bot turn (mean) | At most 1.0 | Count question marks, plus a classifier on flagged replies | Over 1.2 |
| Declined-advance rate | Under 30% of advances | Declined moves divided by moves made | Over 45% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All five are written for text chat events (channel field: chat). Voice signals are PLANNED only (see the modality notes); none has been detected or measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Session ends on a bot message with no user reply and no resolution marker | Session end event whose last event is a bot turn, with `closed` unset | The user got what they needed and left without confirming |
| Bot reply has no forward move on a non-final turn | Judge or rule check of the reply against the move menu finds none | The user said they were done, hurried, or upset, or declined two prior prompts, so no move was correct |
| Same user returns on the same topic after a session closed | Topic-matched new session from the same user in the re-contact window | A new, related question rather than an unresolved one |
| Bot reply contains more than one question | Question-mark count plus classifier on flagged replies | Two questions that are really one (a question with a clarifying example) |
| Conversation marked resolved without a closing message | Resolved state set with no closing template event (confirm and next step) | The user explicitly confirmed the fix worked before any template ran |

**Starter rule:** flag a session for review when it ends on a bot message with no resolution marker and no forward move in the bot's last non-final turns, unless the user had signaled they were done.

## 8. Related patterns
- [unclear-next-step](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/unclear-next-step.md): the bot gave a next step but it was vague. Here, there is no forward move at all.
- [under-clarification](../../../../../by-use-case/agent-interaction/goals/conversation-quality/failures/under-clarification.md): the bot didn't ask what it needed to *answer correctly*. Here, the answer may be right, but the bot never asks what the user needs *next*.
- [tone-mismatch](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/tone-mismatch.md) and [repeated-question-loop](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/repeated-question-loop.md): neighbouring conversation failures that often co-occur.
- Planned in this family: no-closure-confirmation, framework-blind sales conversation, stakes-blind register.

## 9. Common questions

### Why does my chatbot only answer the question and then stop?
Usually because it was told to ("be concise", "don't ask unnecessary questions"), it doesn't track what the user is trying to do, and the success metric counts a finished session as a win. See [why it happens](#3-why-it-happens) and the [fix](#5-the-fix).

### How do I make a chatbot ask good follow-up questions?
Answer first, then ask one question chosen from the user's goal and stage, such as a Situation or Problem question from the [SPIN questioning guide](../../../solutions-library/spin-questioning.md). Research on human conversations found that follow-up questions raised how much partners liked each other, because they felt heard (Huang et al., 2017). Whether the same holds for bots is not yet shown.

### How many questions should a chatbot ask?
In this pattern, one per turn. For lead qualification across a whole conversation, vendor guides suggest keeping it to roughly 2-5 questions total (for example [Lindy's guide](https://www.lindy.ai/blog/how-do-chatbots-qualify-leads)). Those are vendor recommendations, not tested limits, so tune with your own data.

### Won't extra questions annoy users?
They can, if they're filler or pushy. That's why the fix limits the bot to one move per turn, stops after two declined prompts, and drops the sales-style prompts in high-stakes or distressed conversations. See [don't over-correct](#5-the-fix).

### How should a chatbot end a conversation?
It should summarise what was done, ask the user to confirm it worked, say what happens next, and give a way back. "Anything else?" alone is not a close. See the closing step in the [turn policy](#5-the-fix) and the [closure gate](#t1-solution-architecture).

### How is this different from over-clarification or an unclear next step?
Over-clarification asks too many questions *before* answering. [Unclear next step](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/unclear-next-step.md) has a next step that's vague. Here the bot gives no forward move at all and never checks the problem is solved.

---
## Technical section

> For teams building the fix. Thresholds below are **starting points to tune on your own traffic**, not published benchmarks.

### T1. Solution architecture
Add a thin policy layer around the model so the three jobs (answer, advance, close) don't depend on the prompt alone.

```
user message
   │
   ▼
[1] State update ──► goal, stage, known facts, advances_declined, stakes
   │
   ▼
[2] Move selector ──► picks ONE move from the allowed menu (table in section 5)
   │                  (menu is filtered by stakes and by advances_declined)
   ▼
[3] Response composer ──► generates: ANSWER + the selected move
   │
   ▼
[4] Post-check ──► one-question rule, no filler, closure gate (see T2)
   │
   ▼
reply (or regenerate / hand off)
```
```python
def select_move(state):
    if state.user_signalled_done or state.advances_declined >= 2:
        return None                       # just answer or close
    menu = MOVES[(state.goal, state.stage)]
    if state.stakes == "high":
        menu = [m for m in menu if m.kind in ("safe_next_step", "handoff", "verify")]
    if state.out_of_scope or state.stalled_turns >= 3:
        return Move("handoff", with_summary=True)
    return menu[0] if menu else None
```
State object: see the JSON in section 5. Keep it small and rewritten every turn, rather than relying on the model to remember the goal from the transcript.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| At most one question per reply | Post-check [4] | Count question marks and run a quick classifier; regenerate if more than one |
| Every non-final reply has exactly one forward move, unless suppressed | Post-check [4] | LLM judge or rule check against the allowed menu |
| No forward move after the user is done, hurried, or upset | Move selector [2] | Sentiment and "done" intent flags in state |
| Stop advancing after two declined prompts | State [1] | `advances_declined` counter |
| High-stakes: no sales-style moves | Move selector [2] | Stakes flag filters the menu |
| No filler tag-ons not tied to the goal | Post-check [4] | Judge rubric item: "move references the user's goal" |
| **Closure gate:** a conversation can't be marked resolved until a closing message with confirm-and-next-step was sent | Conversation state machine | `closed=true` only after the closing template was emitted |
| Hand-off carries a summary | Handoff step | Required field in the handoff payload |

### T3. Evals
- **Dataset:** start with 100 to 200 conversation openers across your top intents: informational questions (sales), fix requests (support), "I'm done" messages, high-stakes cases, and out-of-scope requests. Include 20 to 30 adversarial cases where advancing is wrong (user in a hurry, user upset, user declined twice).
- **Judge rubric (score each reply 0/1):** (a) answers the question; (b) exactly one forward move, or correctly none; (c) the move ties to the user's goal; (d) no filler; (e) when the goal is met, closes with confirm and next step. Calibrate the judge on 50 human-labelled examples before trusting it.
- **Metrics and starting thresholds**

| Metric | Starting target | Notes |
|---|---|---|
| Answer correctness | Same as your baseline | Don't let the fix hurt accuracy |
| Forward-move coverage (non-final turns) | > 90% | Excluding suppressed cases |
| Multi-question replies | < 2% | Interrogation guard |
| Correct suppression (done/upset/declined cases) | > 95% | Over-correction guard |
| Closing-confirmation rate (resolved cases) | > 90% | |

- **Release gate:** block a prompt or model change if multi-question replies or incorrect suppression exceed target, or if answer correctness drops below baseline.
- **Human review:** sample 30 conversations per release, scored by someone who didn't build the fix.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Silent-exit rate (sessions ending on a bot message, no confirmed resolution) | +20% vs 4-week baseline | +40% | Check recent prompt or model changes for a lost forward-move rule |
| Re-contact within 72h (same user, same topic) | +15% | +30% | Sample sessions that "closed", check the closure gate |
| Questions per bot turn (mean) | > 1.2 | > 1.5 | Post-check may be failing; look for filler and interrogation |
| Declined-advance rate | > 30% of advances | > 45% | Moves aren't relevant; review the move menu |
| Handoff-without-summary rate | > 2% | > 5% | Fix the handoff payload |

### T5. Trade-offs
- **Latency and cost:** a post-check and a possible regeneration add a model call or a rule pass per turn. Run cheap rule checks first and the judge only on flagged replies.
- **Over-steering:** a strong move selector can make conversations feel scripted. Keep the menu small and let the model phrase the move naturally.
- **Goal misclassification:** a wrong `goal` or `stage` yields a poorly aimed move. Treat the state as a guess, refresh it every turn, and prefer a neutral verify-or-ask move when confidence is low.
- **Metric conflict:** this fix can lower containment while raising resolution. Agree on which metric wins before rollout.

---
### Deep dive

**Why the "anything else?" ending isn't a fix.** It is a polite pre-closing, and it hands the work back to the user. It doesn't verify the goal was met. Conversation analysts treat closing a conversation as something both parties organise, not a thing one party just does (Schegloff & Sacks, 1973, [*Opening up Closings*](https://conversationanalysis.org/mp-files/opening-up-closings.pdf), *Semiotica* 8(4)). I could not open the full paper, so this is cited for the general point only.

**Where the cause often sits.** Typical offenders: "Answer only what is asked," "Do not ask unnecessary questions," and a deflection or containment target as the success metric. Fix the metric as well as the prompt, or the prompt change will be quietly reverted.

**Modality notes (PLANNED, not yet written)**
- *Voice:* an advance has to be spoken in a few words and survives only one question at a time. Silence is ambiguous, so closing needs an explicit verbal confirmation.
- *Visual:* the forward move can be a card, a button, or a highlighted next action, so the "question" becomes a visible next step. A dead end here is a screen with no clear primary action.
- *Channel fit:* some forward moves are "switch channel" (for example, fashion needs images and complex discussions need a call). See the planned channel-selection family.

**References checked in this research**
- Huang et al. 2017 (APS summary above); Rackham 1988 (Huthwaite); CFPB 2023 (via Consumer Finance Monitor); Gartner 2024 press release; Li et al. 2020 and the 2024 banking abandonment study (via search summaries); Schegloff & Sacks 1973 (title and aim only).
- Not found: any controlled study of proactive chatbot prompts versus conversion, or vendor-published data from Drift, Salesforce, or Zendesk. A vendor ebook ("Death by Chatbot," G2) was seen in search results but not used, because it's vendor survey data I couldn't verify.
