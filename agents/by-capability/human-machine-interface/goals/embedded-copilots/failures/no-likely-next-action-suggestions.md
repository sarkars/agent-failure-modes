# AI Assistant Suggested Next Actions: No Likely-Next-Action Suggestions

<!-- SEO
title: AI Assistant Suggested Next Actions: Why Bots Skip Them
description: Why an in-app AI assistant never offers likely next steps, and how to suggest two or three actions from the page, account state, and history without upselling.
search phrases:
- AI assistant suggested next actions
- chatbot suggested replies best practices
- suggested prompts for in app AI assistant
- chatbot doesn't suggest what to do next
- follow-up suggestion chips chatbot
- how to add suggested actions to a copilot
- chatbot quick replies based on page context
-->

**Frequency**: Common

## Issue: The in-app assistant answers and stops, never offering the two or three likeliest next steps that the current page, account state, or history already point to.

> **One line:** The user finishes a refund request, and the assistant says "Anything else?" instead of offering "Track the refund" or "Update your card".

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. Voice has the same gap (voice is planned, not yet written). |
| **Stakes** | Low. The cost is extra typing, missed features, and users who stop after one answer. |
| **Who is affected** | Users with a vague next step, and anyone who does not know what the assistant can do here |
| **Frequency** | Common as a design default. I found no study of how often products ship without suggestions. |
| **Pattern ID** | no-likely-next-action-suggestions |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Suggestion accept rate (share of shown suggestion sets where one is clicked), read next to the irrelevant-suggestion rate. Starting targets: set from your own baseline. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Good suggestions need the page, account state, and history, which the model is only given if the product sends them. (Our judgment, not tested.) |
| **Also searched as** | chatbot suggested replies · suggested prompts · quick reply buttons · follow-up chips · next best action chatbot · bot doesn't tell me what to do next |

## 1. In plain words
You finish a task with the assistant, and it goes quiet. It knows which page you are on, that your last invoice failed, and what you asked ten minutes ago. It still waits for you to think of the next question. The fix is to offer two or three likely next steps, picked from what the product knows, while leaving the text box open.

## 2. What it looks like

**Without the fix**
```
(User is on Billing; the last payment failed yesterday)
User: How do I download my invoice?
Bot:  Open Billing, choose the invoice, and click Download PDF.
User: ok thanks
Bot:  Is there anything else I can help you with?
(User closes the chat. The failed payment is still unpaid.)
```

**With the fix**
```
(User is on Billing; the last payment failed yesterday)
User: How do I download my invoice?
Bot:  Open Billing, choose the invoice, and click Download PDF.
      Your payment on May 3 failed. Next:
      [Update payment method] [Retry payment] [Something else]
User: Update payment method
Bot:  Sure. Your card ending 4821 expired in April. Do you want to add a new card?
```
The fixed bot answers first, then offers two actions drawn from the account state, and "Something else" plus the text box stay open.

## 3. Why it happens
These are our reading of the pattern; the sources below report effects, not causes.
- **The model is not given the state.** The prompt has the user's message but not the current page, the failed payment, or the last three actions, so there is nothing to base a suggestion on.
- **No owner for the suggestion list.** Someone must decide which actions are allowed, in what order, and when to stop. Without an owner the bot defaults to "Anything else?".
- **Fear of looking pushy.** After complaints about upsell prompts, teams switch suggestions off entirely, which removes the useful ones too.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In Google's Smart Reply for email, the system was "responsible for assisting with 10% of all mobile responses" in Inbox by Gmail. When the diversity component was disabled and the top three scored suggestions were shown, click-through "decreased by roughly 7.5% relative". | [Kannan et al., *Smart Reply: Automated Response Suggestion for Email*, arXiv 1606.04870](https://arxiv.org/pdf/1606.04870). Opened and read (PDF text). | Suggested email replies, not product next actions, and from a vendor describing its own system. It shows that suggestions get used and that varied sets get more clicks. |
| In a random sample of Alexa Prize TacoBot conversations from the quarterfinals, of the 74.5% in which a task was initiated, "approximately 44% of the tasks were sample tasks suggested in the welcome prompt". | [TacoBot paper, arXiv 2207.05223](https://arxiv.org/pdf/2207.05223). Opened and read (PDF text). | A voice taskbot in a university competition, with suggestions in the welcome prompt rather than from user state. The authors conclude recommending tasks is likely to improve satisfaction; they did not run a controlled test. |
| In an online study of 282 analyzed participants (300 recruited), users of a chatbot whose answers ended with a suggestive hint asked more questions (about 4.27 vs 3.56 per task) and referenced more perspectives (47.0% vs 42.1%) than users of a plain chatbot. | [Yamamoto, *Frontiers in Psychology* 2024](https://www.frontiersin.org/articles/10.3389/fpsyg.2024.1382234/full). Opened and read (first 100,000 of 144,024 characters). | Crowdsourced, Japanese-only, decision tasks, one model, and hints written by the researcher. The author warns that suggestions could feel intrusive and may limit critical engagement. It is not about product next actions. |
| Nielsen Norman Group says that for active users "system-generated prompt suggestions must be context-aware", and describes predefined examples shown "regardless of user context" as push revelations that can annoy users, get overlooked, and be forgotten quickly (paraphrase). | [NN/g, *Designing Use-Case Prompt Suggestions* (June 27, 2025)](https://www.nngroup.com/articles/designing-use-case-prompt-suggestions/). Opened and read. | Expert design guidance with no statistics. It is mainly about prompt suggestions for new users. |

**Counter-evidence worth knowing.** In a between-subjects chatbot study on investment advice, reply-suggestion buttons increased users' inclination to follow the chatbot's advice (Milana et al., ACM CUI 2023). **I read this only through a search summary and did not open the paper**, so it is not used in the fix. It is a reason to keep suggestions honest and free text open.

**Public incident.** No public incident found. I searched for suggestion features that failed or misled and found vendor feature pages and studies, none measuring this failure. Vendor claims of engagement lifts for suggestion chips were not traced to a source and are not used.

## 5. The fix

**The principle:** After answering, offer two or three actions the user is likely to want next, chosen from the page, account state, and history, never from the sales goal, and always with free text left open.

**Do this**
1. **Answer first, suggest second.** A suggestion set never replaces or delays the answer.
2. **Offer two or three actions.** Never more than four, and never a single one presented as the only path.
3. **Pick from product state.** Each suggestion must trace to a named input: the page, an account event, or something the user did in this session.
4. **Only suggest what the assistant can do or open.** Every suggestion maps to a tool or a link that exists today and that the user's plan allows.
5. **Always include "Something else" and keep the text box active.** A click must never be the only way forward.
6. **Mark commercial suggestions.** A suggestion that promotes a plan, add-on, or partner is labeled as an offer and follows the rules in [help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md).
7. **Retire what the user declines.** If the user types free text or ignores a set, do not repeat the same suggestions next turn. Refresh from the new state.
8. **Log every shown set** with its inputs, so accepts and misses can be measured.

**Reference design: a decision table for choosing suggestions**
| Signal in state | Candidate suggestion | Allowed? |
|---|---|---|
| Payment failed in the last 7 days | "Update payment method" | Yes, if the user can edit billing |
| User just exported a report | "Schedule this export" | Yes, if scheduling exists on the user's plan |
| User asked a how-to the plan supports | Next step in the same task | Yes |
| Feature needs a higher plan | Offer, labeled, after the answer, at most once | Yes, per rule 6 |
| User is upset, disputing, or cancelling | A person, or the task they asked for | No promotions |
| No state signal at all | No suggestion set; leave the box open | Yes |

```
After answering, offer up to three next actions the user is likely to want, using only: the current page,
account events from the last 30 days, and this conversation. Each must be something you can do or open now.
Add "Something else". If nothing in the state points to a next step, offer none.
Never promote a plan or product as a next action unless the answer needed it, and label any offer as an offer.
Do not repeat a suggestion the user ignored.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every turn: the answer comes before any suggestion |
| Offer choices: 2-4 options plus "Something else", free text open | After the answer, when product state points to likely next steps. Do not offer them when state gives no signal or the request is already fully done and clear |
| Hand off to a person | The user declines two suggestion sets and still looks stuck, or is in a dispute or cancellation |

**Don't over-correct.** Suggestions can turn into upsells (see [help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md)) or into a menu that traps the user. Guardrails: suggestions come from the user's task and state, not from revenue targets; commercial ones are labeled and limited to one; every set has "Something else" and a live text box; and the bot offers no set when it has no signal. A bot that shows a menu every turn is as bad as one that shows none.

**Hand-off rule.** If the user ignores two sets and repeats a question, or the topic is a dispute, billing error, or cancellation, offer a person with the context passed along ([escalation rules](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **not yet run.**

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Answer plus failed payment on the Billing page | Answer comes first, then one or two suggestions tied to the failure (1, 3) |
| 2 | Suggestion needs a tool the assistant does not have | It is never shown (4) |
| 3 | Any shown set | It includes "Something else" and the text box stays active (5) |
| 4 | User types free text instead of clicking | Next turn does not repeat the ignored suggestions (7) |
| 5 | A suggestion that promotes a paid plan | It is labeled as an offer, and appears at most once (6) |
| 6 | Page with no state signal | No suggestion set is shown, or at most a general one (2, 3) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. I have not set a numeric accept-rate target because I found no public benchmark for product next-action suggestions.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Suggestion accept rate** (primary) | Set from your own baseline, then track the lift | Clicks on a suggestion divided by suggestion sets shown, from the suggestion-shown and suggestion-clicked events | Falling two weeks in a row |
| Irrelevant-suggestion rate (counter) | Set from sampled review; track it down | A reviewer labels a sample of shown sets as relevant or not to the page and state | Rising, or any week above the baseline |
| Suggestions for actions the assistant cannot perform | 0 | Diff each shown suggestion against the tool registry and the user's plan | Any |
| Sets with "Something else" and a live text box | 100% | Check the rendered payload | Below 100% |
| Commercial suggestions without an offer label | 0 | Tag each suggestion as commercial or not; check for the label | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Say "proposed" until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply ends with a generic closer ("Anything else?") on a page with an open account event (failed payment, expiring trial) | Final assistant turn text plus account events at that time | The event is unrelated to the user's task |
| Assistant turn follows a completed task with no suggestion set, and the user's next turn asks what to do next | Next user turn contains "what now", "what next", or "then what" | The user was changing topic |
| User asks the assistant about its own abilities right after an answer | User turn matching "can you" or "what else" | Curiosity about a different feature, with no earlier gap |
| Shown suggestion sets that are never clicked and are followed by free text | suggestion-shown without suggestion-clicked; next user turn is free text | The user wanted something the set could not predict, which is normal for some share of sets |
| A suggestion appears for an action not in the tool registry | Suggestion payload against the registry | None; this is a defect |

**Starter rule:** After answering, offer two or three next actions drawn from the current page, account state, or history, each one something the assistant can do now, with "Something else" and free text left open.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: no-likely-next-action-suggestions
runs: pre_send
reads: [session.current_page, account.recent_events, session.recent_actions, tool_registry, user.plan]
trigger: an answer is about to be sent and product state points to likely next steps
moves: [lead_with_answer, offer_choices, hand_off]   # short names for the moves in the table
choices: ["Update payment method", "Retry payment", "Something else"]   # example only, built from state each turn
on_miss: rewrite
metric: suggestion accept rate
counter_metric: irrelevant-suggestion rate
status: proposed
```

## 8. Related patterns
- [Generic first response](generic-first-response.md): the opener. This page covers every turn after an answer, not the first message; the two can share the same state inputs.
- [Doesn't say what it can do](doesn-t-say-what-it-can-do.md): a one-time capability card at the start. This page is turn-by-turn suggestions based on what the user just did.
- [Help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md): the risk this page must not become. Suggestions here follow the user's task; offers there follow the vendor's goal.
- [Missing the obvious intent](missing-the-obvious-intent.md): misreading what the user typed. This page is about what to offer once the request is understood and answered.

## 9. Common questions
### Should a chatbot suggest next steps or wait for the user?
Suggest, but only when the page, account state, or history point to a real next step, and only after the answer. If there is no signal, offer nothing. See [the fix](#5-the-fix).

### How many suggested replies or prompts should an AI assistant show?
Two or three is the working rule here, never more than four. I found no study that tested the right number for product next actions, so tune it on your own accept and irrelevant rates.

### Are suggested prompts just upsells in disguise?
They can be. Keep suggestions tied to the user's task, label any offer, and cap it at one. The rules are in [help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md).

### Can suggestion buttons trap people in a menu?
Yes, when there is no way out. Every set needs "Something else" and an active text box, and the bot should stop showing sets the user keeps ignoring.

---
## Technical section

### T1. Solution architecture
```
page + account events + session history -> candidate generator -> filter (tool registry, user plan)
-> ranker (top 2-3) -> labeler (commercial flag) -> rendered set + "Something else"
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Suggestion maps to an available tool or link | Filter step | Diff against registry in CI and at runtime |
| Commercial suggestions labeled, at most one | Labeler | Test 5 |
| "Something else" and text box present | Renderer | Test 3 |
| Ignored suggestions not repeated | Session state | Test 4 |

### T3. Evals
- **Dataset:** sampled real conversations with page and account state, each labeled by reviewers for the likely next actions; start with a small set across your top pages.
- **Judge rubric:** is each suggestion relevant to the page and state, doable now, and non-promotional unless labeled?
- **Metrics and starting thresholds:** irrelevant-suggestion rate and unavailable-action rate from section 7; thresholds are set from your baseline, not from a source.
- **Release gate:** block a deploy on any suggestion for an unavailable action or an unlabeled commercial one.

### T5. Trade-offs
- Needs a data feed from the product to the assistant, plus an owner for the allowed-action list.
- More suggestions raise clicks but also the chance of an irrelevant one; fewer, better ones are easier to trust.

---
### Deep dive
- **Open question.** No public study I found measures accept rate for product next-action suggestions. The evidence above shows that suggestions are used (email replies, a voice taskbot) and that context matters (NN/g), not the size of the lift for your product.
- **References.** [arXiv 1606.04870](https://arxiv.org/pdf/1606.04870) (opened); [arXiv 2207.05223](https://arxiv.org/pdf/2207.05223) (opened); [Frontiers 2024](https://www.frontiersin.org/articles/10.3389/fpsyg.2024.1382234/full) (opened, partial); [NN/g 2025](https://www.nngroup.com/articles/designing-use-case-prompt-suggestions/) (opened).
