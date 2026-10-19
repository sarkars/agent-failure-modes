# Chatbot Doesn't Say What It Can Do: Empty Chat Box and Unclear Capabilities

<!-- SEO
title: Chatbot Doesn't Say What It Can Do: How to Fix It
description: Why users face an empty chat box and don't know what an in-app AI assistant can do, and how to show real capabilities, examples, and limits.
search phrases:
- how do I know what the AI assistant can do
- chatbot blank chat box users don't know what to ask
- how to show chatbot capabilities to users
- AI assistant onboarding best practices
- suggested prompts for in app AI assistant
- chatbot says it can do things it can't
- what can this chatbot help me with
-->

**Frequency**: Common

## Issue: An in-app assistant opens to an empty box and never says what it can and cannot do, so users guess, ask the bot about itself, or give up.

> **One line:** A blank box with "Ask me anything" tells the user nothing about what will actually work.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. Voice assistants have the same problem (voice is planned, not yet written). |
| **Stakes** | Low to medium. The cost is unused features and users who try once and leave. |
| **Who is affected** | New users, and anyone with little experience of AI tools |
| **Frequency** | Common. I found no study of how often assistants ship an empty box; the evidence below shows the effect on users. |
| **Pattern ID** | doesn-t-say-what-it-can-do |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Share of new users who complete a successful first task with the assistant. Starting target: set from your own baseline, then track the lift. |
| **Maturity** | Tests written (see [the test file](../../../tests/doesn-t-say-what-it-can-do.md); not yet run) |
| **Will a better model fix this?** | No. A stronger model does not tell users what is connected to it. What it can do depends on the tools and data you wire in, and someone must say so. (Our judgment, not tested.) |
| **Also searched as** | what can this bot do · chatbot blank screen · AI assistant discoverability · chatbot capabilities list · bot doesn't tell me what it can do |

## 1. In plain words
You open the help assistant and see "Ask me anything". Can it change your plan? Read your invoices? Only answer questions from the help center? Nothing says. So you try something, it fails, and you stop. Or you ask the bot "what can you do?" and its answer is wrong.

## 2. What it looks like

**Without the fix**
```
(Empty box: "Ask me anything")
User: can you change my billing date?
Bot:  I can help with a wide range of questions! What would you like to know?
User: can you change my billing date
Bot:  I'm sorry, I'm not able to help with that.
```

**With the fix**
```
Bot:  I'm the Acme assistant (an AI). I can look up your invoices, explain a charge, and change your billing date.
      I can't change your plan; for that I'll connect you to someone.
      Try: [Why is my invoice higher?] [Change billing date] [Download an invoice]
User: Change billing date
Bot:  Sure. Your date is the 3rd now. Which day would you like?
```
The fixed assistant says what it does, what it doesn't, and offers starting points drawn from the screen.

## 3. Why it happens
These are our reading of the pattern; the sources below report effects, not causes.
- **The box is the interface.** A blank chat input is quick to ship and assumes users already know what to ask.
- **Capabilities change.** The tool list grows or shrinks and nobody updates the greeting, so it either says too little or promises too much.
- **Fear of limiting it.** Teams avoid naming limits because it feels like admitting weakness.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a qualitative usability study of 3 Chinese AI chatbots with 6 participants (3 with no prior AI experience), participants asked the bot about its own capabilities (for example whether it could access the internet or process a 100-page PDF). When the bot answered inaccurately, users' understanding of what the tool could do was hurt. | [Nielsen Norman Group, *New Users Need Support with Generative-AI Tools* (Mar 29, 2024)](https://www.nngroup.com/articles/new-ai-users-onboarding/). Opened and read. | Six participants, Chinese-language consumer chatbots, qualitative. It shows a mechanism, not a rate. |
| In Amplitude's own tests of its AI chat, new users did better with a few default clickable prompts than with an empty chat box; users who asked the agent three questions in their first seven days were more likely to retain; and prompts tailored to a user's role and job-to-be-done converted new users at twice the rate of the original version, by the company's account. | [Amplitude blog, *AI chat box tests*](https://www.amplitude.com/blog/ai-chat-box-tests.md). Opened and read. | A company blog about one product's tests. The results are the company's own and I could not check the test design or statistics. |
| In a within-subject experiment with 16 participants, adding prompt guidelines and domain context to an LLM help assistant made no significant difference in usage or perceptions, and most users struggled to connect their prompts to the answers and often followed suggestions verbatim even when wrong. | [Why and When LLM-Based Assistants Can Go Wrong, arXiv 2402.08030](https://arxiv.org/abs/2402.08030). Abstract opened and read. | A small study of software help-seeking. It cautions that prompt hints alone may not be enough. |

**Public incident.** No public incident found. My searches for assistants that did not explain their capabilities returned design articles and small studies, not a dated, sourced case.

## 5. The fix

**The principle:** Tell users, in the first screen, what the assistant can do and what it cannot, with starting points from the current context, and keep that description tied to what is actually connected.

**Do this**
1. **Say what it is and what it does** in two lines: that it is an AI assistant, and the three or four things it can do here.
2. **Say what it cannot do,** and what to do instead (a person, a page).
3. **Offer clickable starting points from context.** Use the screen and account state to pick them ([generic first response](generic-first-response.md)). Three to five is enough.
4. **Generate the capability list from what is wired in.** Build it from the tool registry so it cannot promise a tool that is not connected.
5. **Answer "can you...?" truthfully.** The assistant must know its own tool list. Test it.
6. **Do not rely on hints alone.** Pair examples with feedback after the first task, since one small study found hints alone changed little.
7. **Refresh on change.** When tools change, update the description and re-run the tests.

**Reference design: a capability card built from the tool list**
```json
{ "can": ["look up invoices", "explain a charge", "change billing date"],
  "cannot": ["change plan (a person can)", "give legal or tax advice"],
  "starters": ["Why is my invoice higher?", "Change billing date", "Download an invoice"] }
```
```
At the start of a chat, show: who you are (an AI assistant), up to four things you can do here (from the tool list),
one thing you cannot do and what to do instead, and up to three one-tap starting points chosen from the current screen.
If asked "can you ...?", answer from the tool list. Never claim an ability that is not on the list.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices | First open: up to three starting points from the current screen, plus "Something else", free text open. Do not offer them when the user's first message is already a clear request; answer it instead. |
| Lead with the answer | The user asks "can you ...?" and the tool list has the answer: say yes or no first, from the tool list |
| Admit uncertainty and show how to check | The ability is not on the tool list, or needs a setting the user has not turned on: say so, and point to the page or setting that settles it |
| Hand off to a person | The user asks for something it cannot do: offer a person with the context passed along |

**Don't over-correct.** A long list of features is as unhelpful as an empty box. Keep it to a few lines; put the rest behind "What else can you do?". Do not list abilities that need a setting the user has not turned on without saying so.

**Hand-off rule.** For things it cannot do, offer a person with the context passed along ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/doesn-t-say-what-it-can-do.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | First open | A capability line and starting points are shown |
| 2 | "Can you change my plan?" (cannot) | The assistant says no and offers the alternative |
| 3 | "Can you change my billing date?" (can) | The assistant says yes and does it |
| 4 | A tool removed from the registry | The card no longer lists it |
| 5 | "What else can you do?" | A short, accurate expansion |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **First-task success rate for new users** (primary) | Set from baseline; track the lift | New users who complete a task with the assistant in their first session, from event logs | Falling two weeks in a row |
| Capability-question accuracy | Over 95% | A set of "can you ...?" questions with known answers; scored by reviewers | Below 90% |
| Unsupported-request rate | Track; set from baseline | Requests that hit "I can't" | Rising |
| Starter click-through | Track | Share of sessions where a starting point is tapped | Falling |
| Card matches tool list | 100% | Automatic diff of the card against the registry | Any mismatch |

### Detection signals (proposed, not yet calibrated)
Chat signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A new user's session ends with no task-complete event (primary metric) | Session end event and first-task event for a user flagged new | The user came only to look around |
| A user request in the first turns gets an "I can't" reply (unsupported-request rate) | Assistant turn tagged as a refusal or "can't help", with turn index | A request that is truly out of scope and was answered with an alternative |
| No starting point is tapped in a session that opened on the card (starter click-through) | Starter-click event absent after the card-shown event | The user typed a clear request straight away |
| A "can you ...?" answer disagrees with the tool registry (capability-question accuracy) | Capability-question turn, with the answer compared to the registry entry | The ability needs a setting the user has not turned on, and the answer said so |
| The card lists a tool that is not in the registry (card matches tool list) | Card-render event with its tool list, diffed against the registry | A registry change shipped moments ago and the card has not refreshed yet |

**Starter rule:** Never claim an ability that is not on the tool list.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: doesn-t-say-what-it-can-do
runs: pre_send
reads: [session.is_new_user, tool_registry.tools, screen.context, user_turn.text]
trigger: a chat opens for the first time, or the user asks "can you ...?"
moves: [offer_choices, lead_with_answer, admit_uncertainty, hand_off]
choices: ["Why is my invoice higher?", "Change billing date", "Download an invoice", "Something else"]
on_miss: rewrite
metric: share of new users who complete a successful first task with the assistant
counter_metric: over-claim rate (card or answer names an ability not in the registry)
status: proposed
```

## 8. Related patterns
- [Generic first response](generic-first-response.md): the opener, which should carry context-based starters.
- [Missing the obvious intent](missing-the-obvious-intent.md): what happens after the user types.
- [Re-asks for known information](re-asks-for-known-information.md): another way the assistant ignores the product.
- [Does the chatbot say it's a bot?](../../trust-and-rapport/failures/undisclosed-bot-identity.md): the identity and limits disclosure.

## 9. Common questions
### How do users find out what an AI assistant can do?
They should be told on the first screen, with examples. If the interface does not say, they ask the bot, and an inaccurate answer makes things worse (NN/g study, [section 4](#4-why-it-matters)).

### Should the chatbot list what it can't do?
Yes, briefly, with what to do instead. It prevents failed attempts and builds trust.

### Do suggested prompts work?
In one company's tests, clickable defaults beat an empty box. A small academic study found prompt hints alone made little difference, so test them on your own users.

### How do I keep the list accurate?
Generate it from the tool registry and diff it on every release. See rule 4.

---
## Technical section

### T1. Solution architecture
```
tool registry -> capability card generator -> first-screen card
screen/account context -> starter ranker -> up to 3 starters
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Card lists only registered tools | Card generator | Diff in CI |
| "Can you ...?" answers come from the registry | Orchestration | Test 2 and 3 |

### T3. Evals
- **Dataset:** 100 "can you ...?" questions, half true, half false, from the real tool list.
- **Judge rubric:** is the answer correct and does it offer an alternative when no?
- **Metrics and starting thresholds:** accuracy over 95%; over-claim rate 0%. Starting points to tune.
- **Release gate:** block a deploy on any over-claim.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Over-claims | Any | Any | Pull the claim; fix the registry |

### T5. Trade-offs
- A generated card can read dryly; edit the wording once and keep the generator for the list.

---
### Deep dive
- **Voice.** A voice assistant cannot show a card; it needs a short spoken summary (voice is planned, not yet written).
- **Open question.** I found no controlled study of first-task success with and without a capability card. The Amplitude figures are one company's own.
- **References.** [NN/g](https://www.nngroup.com/articles/new-ai-users-onboarding/) (opened); [Amplitude](https://www.amplitude.com/blog/ai-chat-box-tests.md) (opened); [arXiv 2402.08030](https://arxiv.org/abs/2402.08030) (abstract opened).
