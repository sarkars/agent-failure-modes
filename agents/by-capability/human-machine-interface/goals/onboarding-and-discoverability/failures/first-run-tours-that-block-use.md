# Chatbot Onboarding Tutorial Blocks the First Question: First-Run Tours That Block Use

<!-- SEO
title: Chatbot Onboarding Tour Blocks Use: Let Users Ask First
description: Why a first-run tour or tutorial in front of an AI chat assistant causes drop-off, and rules to let people ask first and teach one tip at a time in context.
search phrases:
- onboarding tutorial skip button
- product tour drop-off
- chatbot onboarding best practices
- should my ai assistant have a product tour
- users skip onboarding tutorial
- first-run experience chatbot
- product tour completion rate by number of steps
-->

**Frequency**: Common

## Issue: A new user opens the assistant and meets a tour, tutorial, or setup quiz that must be finished or dismissed before they can type their first question, so some leave before they ask anything.

> **One line:** The tour stands between the user and their first question; the fix is to let them ask right away and teach one tip at a time, after an answer, at the moment the tip helps.

| | |
|---|---|
| **Channel** | Written for **chat** (in-product assistants and website chat). Voice first-run flows and host-site analytics signals are PLANNED, not written. |
| **Stakes** | Low to medium. The cost is people who never send a first message, and a product that seems harder than it is. |
| **Who is affected** | First-time users, and returning users who see the tour again after an update |
| **Frequency** | Common in our judgment: product tours are a standard software pattern. I found no count of how many chat assistants put a tour in front of the first message. |
| **Pattern ID** | first-run-tours-that-block-use |
| **Family** | [Onboarding and discoverability](../README.md) |
| **Goal** | People know what the assistant can do and how to start, without needing to guess or to engineer prompts. |
| **Primary metric** | Drop-off during the first-run flow: share of first sessions that end before the user's first message is answered. Starting target: no higher than a no-tour control group (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The tour is a product flow that runs before the model sees a message. (Our judgment, not tested.) |
| **Also searched as** | skip tutorial · product tour annoying · forced onboarding · onboarding walkthrough drop-off · coach marks block screen · welcome carousel |

## 1. In plain words
A small-business owner opens the new AI assistant in their invoicing app to ask one thing. Instead of a chat box, they get "Welcome! 1 of 6", a carousel of features they did not ask about, and a disabled input until they click through or find a small "Skip". Some click through without reading, some leave, and the ones who stay have learned little. A chat assistant already has the best teaching tool there is: the conversation. Let people ask first, and teach inside the answers.

## 2. What it looks like

**Without the fix**
```
(User opens "Ask Ledgerly" in an invoicing app for the first time)
Bot:  Welcome to Ask Ledgerly! [Card 1 of 6: Meet your AI assistant]  [Next]  (input box disabled)
User: (clicks Next twice, then types "how do I send a late payment reminder")
Bot:  [Card 3 of 6: Smart categories]  (the typed text is not sent)
User: (closes the panel and leaves)
```

**With the fix**
```
(User opens "Ask Ledgerly" for the first time; the input box is active)
Bot:  I can draft invoices, find unpaid ones, and send reminders. Try one, or just ask.
      [Find unpaid invoices] [Send a reminder] [Draft an invoice] [Something else]
User: how do I send a late payment reminder
Bot:  Open the invoice, click Remind, and pick a template; I can draft it now. Which invoice?
      Tip: next time, type "remind all overdue" to do every overdue invoice at once.
```
The user asks before anything else, gets the answer first, and learns one feature, attached to the task they are doing.

## 3. Why it happens
These are our reading of the pattern; the third has partial support in the NN/g source below.
- **The tour is judged by what it shows, not by what users do next.** A launch team counts "tour completed" or "features seen". Nobody charts first questions lost behind the tour, so a six-card carousel looks like success. (Business context, as in the catalog row.)
- **The tour is built in a separate guidance tool layered over the chat.** It cannot see that the user has started typing, so it cannot step aside, and it often disables the input to keep focus.
- **The tour patches an assistant that does not explain itself.** If the chat never says what it can do (see [Chatbot doesn't say what it can do](../../embedded-copilots/failures/doesn-t-say-what-it-can-do.md)), a team bolts a tutorial in front. NN/g argues that the effort is better spent making the interface easy to use.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a between-subjects test with 70 participants on four iOS apps, people who read a deck-of-cards tutorial had no better task success (91% vs. 94% for those who skipped, not significant) and rated the tasks harder (4.92 vs. 5.49 on a 7-point ease scale, p=0.047). Reading the tutorial did not make them faster. | [Alita Kendrick, *Mobile Tutorials: Wasted Effort or Efficiency Boost?*, NN/g, March 8, 2020](https://www.nngroup.com/articles/mobile-tutorials/). Opened and read. | Mobile apps, not chat. Four apps, one study. A strong neutral source but a single one. |
| NN/g says onboarding instructions that users must take in before they start using a product "require attention and effort and thus reduce usability", and should be avoided as much as possible. | [Alita Kendrick, *Onboarding: Skip it When Possible*, NN/g video, Jan. 15, 2021](https://www.nngroup.com/videos/onboarding-skip-it-when-possible/). Page summary opened; the video itself not watched. | Expert guidance, not a new experiment. |
| Microsoft's Fluent 2 design system says people often skip first-run experiences because they do not see the benefit, that onboarding should sit within a closely related task, and that people should be able to exit and come back to it later. | [Microsoft, *Fluent 2: Onboarding*](https://fluent2.microsoft.design/onboarding/). Opened and read. | Vendor design guidance. It refers to research but names no study. |
| In 464 SaaS companies' tours from January to June 2026, median completion was 73% for 1-2 step tours, 38% for 3-5 steps, 25% for 6-8 steps and 8% for 9 or more. Tours users opened themselves completed at a median of 69%; tours that started automatically, 23%. | [Produktly, *SaaS Onboarding & In-App Engagement Benchmarks 2026*](https://produktly.com/research/saas-onboarding-benchmarks-2026). Opened and read. | Vendor data from its own customers, skewed to small and mid-size SaaS. The report says step count is a correlation, and that auto-started tours reach people who never asked, so lower completion is partly by design. Single source for these numbers. |
| From 2020 data on over 214 million interactions, three-step tours had a 66% completion rate, and completion fell below 50% after five steps. | [Chameleon, *Announcing the Latest Chameleon Benchmark Report*](https://www.chameleon.io/blog/chameleon-benchmark-report). Opened and read. | Vendor of tour software, reporting its own customers. Completion of a tour is not the same as reaching the first question. |

I found no study of tours in front of a chat assistant, and no study that measures drop-off before a first chat message. A search summary also described a 2019 Chameleon report with a self-started vs. automatic comparison; I could not read the PDF, so I use none of its numbers.

**Public incident.** No public incident found for this pattern. My searches returned benchmark reports and practitioner posts, not a dated, sourced event.

## 5. The fix

**The principle:** The first thing a new user can do is ask; teaching happens inside answers, one tip at a time, when the tip helps.

**Do this**
1. **The input box works on first open.** No tour, video, carousel, or quiz may disable it or stand in front of it.
2. **A message typed during any first-run content is sent and answered.** The content closes; the text is never discarded.
3. **First-run content is one line of scope plus 2-4 starter suggestions inside the chat**, with "Something else" and free text open (see [blank box: no hint what to ask](blank-box-no-hint-what-to-ask.md)). Nothing more before the first question.
4. **Answer first, teach second.** A tip comes after the answer, never before it, at most one per reply, and only when it relates to what the user just asked.
5. **Any tour is opened by the user**, from a "Show me around" suggestion or a "help" request. It never starts by itself.
6. **An opened tour is short and always closable.** Close is visible on every step, and closing returns to the chat with the input intact. Keep it to a few steps (Produktly's data, vendor-reported, shows 1-2 step tours complete most often).
7. **A dismissed tour stays dismissed.** Do not show it again on the next visit; keep it reachable on request.
8. **Ask nothing about the user before the first answer** unless the answer depends on it; then ask one question, tied to their request.

**Reference design: first-run decision table**
| Moment | Show | Never |
|---|---|---|
| First open, no message yet | One scope line, 2-4 starters plus "Something else", active input | Carousel, video, disabled input, profile quiz |
| User types or taps a starter | Close any first-run content; answer the message | Drop the text; finish the tour first |
| Answer depends on setup (for example, which account) | One clarifying question | A setup wizard |
| Answer given, a feature would help this task | One tip after the answer | A tip before the answer, or two tips |
| User asks "what can you do?" or taps "Show me around" | Optional tour, a few steps, close on each | Auto-start on a later visit |
| User closed the tour | Chat with input intact; tour available on request | The tour again next session |

```
On a user's first visit, say in one line what you can help with and offer 2-4 example tasks plus "Something else".
Answer the user's first message before teaching anything. After an answer, you may add one short tip about a feature
that helps with what they just did. Never add more than one tip per reply, and never put a tip before the answer.
Offer a tour only when the user asks what you can do or asks for help getting started.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user's first message is clear: answer it, then add at most one tip. |
| Offer choices: 2-4 options plus "Something else", free text open | First open, before any message: 2-4 real starter tasks plus "Something else". Do not offer them once the user has typed a question, and do not let them replace the input box. |
| Ask one clarifying question | The first answer depends on one fact (which invoice, which account): ask that one question, not a setup flow. Do not ask when the answer is the same either way. |
| Hand off to a person | The user asks for a person during first run, or the bot fails twice on the first request. No tour step may sit between that request and the hand-off. |

**Don't over-correct.** Removing the tour must not leave a blank box with no hint (that is [blank box: no hint what to ask](blank-box-no-hint-what-to-ask.md)), and "teach in context" must not become a tip on every reply, which is its own noise. Keep the tour for people who ask for it. If your product must show terms, a disclosure, or a sign-in before use, that is a legal or security decision for your team; keep it to what is required and do not attach feature promotion to it (for sign-in, see [forces a fresh login](../../embedded-copilots/failures/forces-a-fresh-login.md)).

**Hand-off rule.** A request for a person during first run goes straight to the hand-off path, with no remaining tour steps shown first ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | First open of the assistant | 1, 3 | Input is active; at most one scope line and 2-4 starters plus "Something else" |
| 2 | User types a question while first-run content is showing | 2 | Content closes; the question is sent and answered |
| 3 | First message: "how do I send a late payment reminder" | 4 | Answer comes first; at most one tip, after it, about reminders |
| 4 | Second visit, user never asked for a tour | 5 | No tour starts |
| 5 | User taps "Show me around", then closes on step 2 | 6, 7 | Close is visible on each step; chat returns with input intact; tour not shown next visit |
| 6 | First message needs an account choice | 8 | One clarifying question; no setup wizard |
| 7 | User types "talk to a person" on first open | Hand-off rule | Hand-off starts with no tour step shown |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Drop-off during the first-run flow** (primary) | No higher than a no-tour control | First sessions that end before the first user message is answered, split by first-run variant | Gap over 5 points vs. control, or rising two weeks in a row |
| Time from first open to first user message | Falling; set from baseline | Client open event to first message event | Rising two weeks in a row |
| First messages typed during first-run content that were answered | 100% | Message events with first-run content open, joined to a reply event | Any miss |
| Auto-started tours | 0 | Tour-start events with no user trigger | Any |
| Tips placed before the answer, or two tips in one reply | 0 | Pre-send check on replies containing a tip | Over 1% of tipped replies |
| Feature questions on features the tour used to cover (counter-metric) | Flat vs. baseline | Count "how do I" questions on those features in first 30 days | Rising, which points to [hidden commands and features](hidden-commands-and-features.md) |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. They need first-run events from the chat client; host-site clickstream and voice signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Session ends during a first-run step with no user message | First-run step event followed by session end | User opened the chat by accident |
| Text typed but not sent while first-run content was open | Input keystroke or draft event with input disabled or no send event | User changed their mind before sending |
| Tour start event with no user trigger | Tour-start event lacking a "show me around" tap or help request | A tour the user started on a previous turn and resumed |
| Reply contains a tip before its answer, or two tips | Pre-send check on reply structure | A user who asked for an overview of features |
| Tour shown again after a dismissal | Tour-start event for a user with a stored dismissal | User asked to see it again |

**Starter rule:** the input box works on first open, and a message typed during any first-run content is sent and answered.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: first-run-tours-that-block-use
runs: conversation
reads: [session.is_first_visit, first_run.content_open, first_run.tour_trigger, user_turn.text, draft_reply.text, user.tour_dismissed]
trigger: a first-time user opens the assistant, or sends a message while first-run content is open
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Find unpaid invoices", "Send a reminder", "Draft an invoice", "Something else"]
on_miss: log
metric: drop-off during the first-run flow
counter_metric: feature questions on features the tour used to cover
status: proposed
```

## 8. Related patterns
- [Chatbot doesn't say what it can do](../../embedded-copilots/failures/doesn-t-say-what-it-can-do.md): the closest existing page. That one is about an assistant that explains too little at the start; this one is about an assistant that explains too much, in a form that blocks the first question. The fixes meet in one line of scope plus a few starters.
- [Hidden commands and features](hidden-commands-and-features.md): the opposite failure. There the product teaches too little, too late, so useful features stay unfound; here it teaches too much, too early. Both are fixed by teaching a feature at the moment it helps.
- [Blank box: no hint what to ask](blank-box-no-hint-what-to-ask.md): what over-correction looks like if the tour is removed and nothing replaces it.
- [Starter suggestions that fail](starter-suggestions-that-fail.md): the starters this page recommends must work.
- [Forces a fresh login](../../embedded-copilots/failures/forces-a-fresh-login.md): another gate before help, there authentication instead of instruction.
- [Chat widget hard to find, or intrusive](chat-widget-hard-to-find-or-intrusive.md): a pop-up that interrupts the page; this page is about what happens once the chat is open.

## 9. Common questions
### Should my AI chatbot have an onboarding tour?
Usually not in front of the first message. Let people ask first, show one line of what the assistant does and a few starters, and offer a short tour only when someone asks. See [the fix](#5-the-fix).

### Do users skip product tours?
Microsoft's Fluent 2 guidance says people often skip first-run experiences. In NN/g's 2020 mobile study, reading a tutorial did not improve task success and made tasks feel harder. Vendor benchmarks show completion falling as tours get longer.

### How many steps should a product tour have?
As few as possible. Produktly's 2026 vendor data shows 1-2 step tours completing most often; treat that as directional, not a rule.

### Is a skip button enough?
No. A skip button still puts the tour first. The fix is that the input works on first open and a typed message closes the tour and gets answered.

### How do I teach features without a tour?
Add one short tip after an answer, about a feature that helps with what the user just did. That is teaching in context.

---
## Technical section

### T1. Solution architecture
```
open chat -> first_visit? -> render scope line + starters; input enabled
user input event -> close first_run content -> send message -> reply
draft reply -> tip check (tip after answer, max one, related to request) -> send
tour trigger -> only from user tap or help intent; store dismissal per user
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Input never disabled by first-run content | Chat client | Test 1 and 2 |
| No auto-started tour | Guidance tool config | Tour-start events without a trigger |
| One tip, after the answer | Pre-send check | Test 3 and log scan |

### T3. Evals
- **Dataset:** 50 first-session scripts: clear first questions, typed-during-tour cases, "talk to a person", and setup-dependent first questions.
- **Judge rubric:** was the first message answered first, at most one related tip after it, and no tour without a trigger?
- **Release gate:** block a release that disables input on first open or auto-starts a tour. Starting points to tune.

### T5. Trade-offs
- Removing a mandatory tour lowers "features seen" in launch reports; track the counter-metric so discovery does not quietly fall.
- A typed-during-tour handler needs the guidance tool and the chat client to share events, which some third-party tools do not support.

---
### Deep dive
- **Open question.** No source I opened measures tours in front of a chat assistant; the evidence is mobile-app usability research and SaaS tour benchmarks.
- **Not used.** A 2019 Chameleon benchmark PDF (described in a search summary) could not be read, so none of its figures appear here.
- **Voice.** PLANNED. A spoken "here's what I can do" intro before the caller can speak is the voice form of this pattern.
- **References.** [NN/g, 2020](https://www.nngroup.com/articles/mobile-tutorials/) (opened); [NN/g video, 2021](https://www.nngroup.com/videos/onboarding-skip-it-when-possible/) (summary page opened); [Fluent 2 onboarding](https://fluent2.microsoft.design/onboarding/) (opened); [Produktly 2026](https://produktly.com/research/saas-onboarding-benchmarks-2026) (opened); [Chameleon 2020 data](https://www.chameleon.io/blog/chameleon-benchmark-report) (opened).
