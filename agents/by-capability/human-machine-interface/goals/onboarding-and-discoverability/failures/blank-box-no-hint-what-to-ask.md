# Chatbot Empty State: Blank Box With No Hint What to Ask

<!-- SEO
title: Chatbot Empty State: Fix the "Ask Me Anything" Blank Box
description: Why a chat widget that opens on "Ask me anything" gets closed before the first message, and how to open with a scope line and 2-4 starting points.
search phrases:
- chatbot welcome message examples
- chatbot empty state design
- users don't know what to ask the chatbot
- chatbot "ask me anything" placeholder
- chatbot conversation starters
- suggested prompts on empty chat screen
- why nobody uses my website chatbot
-->

**Frequency**: Common

## Issue: The chat opens on an empty box and a line like "Ask me anything" or "How can I help you today?", so the person cannot tell what the bot does or how to start, and often closes it without typing.

> **One line:** An empty chat input says nothing about what will work; the fix is to open with one line of scope and 2-4 tappable starting points, with free text always open.

| | |
|---|---|
| **Channel** | Written for **chat** (website widgets, help centers, standalone chat apps). Voice and web-analytics signals are PLANNED, not written. |
| **Stakes** | Low per session. The cost is people who leave before the first message and never learn the bot could have helped. |
| **Who is affected** | First-time visitors, and anyone with a specific task who cannot tell if the bot handles it |
| **Frequency** | Common as a default, by our observation. I found no study that counts how often chats open on a blank box; the sources below describe the effect, not the rate. |
| **Pattern ID** | blank-box-no-hint-what-to-ask |
| **Family** | [Onboarding and discoverability](../README.md) |
| **Goal** | People know what the assistant can do and how to start, without needing to guess or to engineer prompts. |
| **Primary metric** | Share of first sessions with a first message or tap, paired with abandonment before the first message. Starting target: set from your own baseline, then track the lift (no source sets a number). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The opening screen is drawn before the model sees any input, so its words and starters are a design choice, not a model output. (Our judgment, not tested.) |
| **Also searched as** | chatbot blank screen · chatbot welcome message · what should a chatbot say first · chatbot first message ideas · chat widget nobody uses |

## 1. In plain words
You click "Chat with us" on your internet provider's site. The box says "Ask me anything." Can it check an outage? Change your plan? Only link to help articles? Nothing says, so you either guess, type "hi", or close it. The fix costs one sentence and a few buttons: say what the bot does here, and give people a first tap.

## 2. What it looks like

**Without the fix**
```
(Northfield Fiber, Columbus, Ohio. Widget opens on the Support page. Placeholder: "Ask me anything")
Bot:  Hi there! How can I help you today?
(40 seconds, no typing. Widget closed. Log: widget_open, widget_close, no user turn.)
Next visitor:
User: hi
Bot:  Hello! What can I help you with?
User: what can you even do
Bot:  I can help with a wide range of questions!
```

**With the fix**
```
(Same page. Placeholder: "e.g. Is there an outage on Elm St?")
Bot:  Hi, I'm Northfield's virtual assistant (an AI). Here I can check outages at your address,
      explain a charge on your bill, and set up a move or a plan change.
      [Check for an outage] [Explain my bill] [Moving or changing plans] [Something else]
User: (taps "Check for an outage")
Bot:  Sure. What's the service address? A ZIP code is fine to start.
```
The fixed opening says what the bot is, names three things it does on this site, offers four taps including "Something else", and the placeholder is a real example instead of "Ask me anything".

## 3. Why it happens
These are our reading of the pattern; the sources in section 4 report effects, not causes.
- **The opening is a default nobody rewrote.** The widget ships with a stock greeting and an empty input, and the team never replaces them with words about this bot.
- **The team already knows what the bot does.** To the people who built it, the box looks obvious; a first-time visitor has none of that knowledge.
- **Sessions with no first message are invisible.** Resolution and satisfaction are measured on conversations that start, so a person who opens the widget and leaves never shows up in the dashboard.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In qualitative moderated usability tests "with 9 users of varying digital skill levels and AI competency", participants rarely used site AI chatbots and often didn't notice them. The authors write: "Users will not experiment to discover a chatbot's value. If its benefit is not obvious immediately, they will move on." They advise that the prompt and intro message be specific to the situation, "rather than a generic *How can I help you?* or *Ask me anything*". | [Rosala, Kenderova and Kohler, Nielsen Norman Group, *What Is Your Site's AI Chatbot for? Users Can't Tell* (Mar. 20, 2026)](https://www.nngroup.com/articles/site-ai-chatbot/). Opened and read. | Nine participants, qualitative, site chatbots. It shows a mechanism and expert advice, not a rate or a test of the fix. |
| A product designer at Amplitude reports that new users "weren't ready to go headfirst into AI chat", that "a couple of default prompts to click on" helped them discover features, and that "familiar, clickable content outperformed both feature-focused prompts and the empty chat box". Prompts tailored to the user's role converted new users at 2x the original version, by the company's account. | [Amy Lin, Amplitude blog, *Your AI Chat Box Isn't a Strategy. Where You Put It Is.* (Aug. 18, 2026)](https://www.amplitude.com/blog/ai-chat-box-tests). Opened and read. | Vendor blog about its own analytics product, single source. I could not check the test design, sample or statistics. |
| An Adobe-authored paper says "new users often struggle to ask effective questions, especially in emerging systems" and proposes context-aware question suggestions, evaluated on 250 real interactions with the AI Assistant for Adobe Experience Platform by ten annotators in pairwise comparisons. | [Shen et al., arXiv 2412.10933 (Dec. 14, 2024)](https://arxiv.org/abs/2412.10933v1). Abstract and HTML full text opened. | Vendor authors, enterprise setting, preprint. Its suggestions appear after the first question and answer, not on the empty screen, so it supports suggestions in general, not this page's opening rule. Margins over the baseline were small, and I saw no significance test. |

**Public incident.** No public incident found. Four searches (listed in the run report) returned design guides and vendor blogs, not a dated, sourced case.

## 5. The fix

**The principle:** Before the first message, the chat says what it is, what it does here, and offers a first tap, while free text stays open.

**Do this**
1. **Open with a scope line.** One sentence that says it is an AI assistant and names 2-4 things it can do on this site or screen.
2. **Show 2-4 starters plus "Something else".** Draw them from your top intents in the last 30 days of logs (a starting window to tune), and only for tasks the bot completes ([starter suggestions that fail](starter-suggestions-that-fail.md) covers testing each one).
3. **Keep free text open.** The input is never disabled; "Something else" focuses it.
4. **Make the placeholder a real example.** "e.g. Is there an outage on Elm St?", never "Ask me anything" or "How can I help you?".
5. **Match the page.** When the widget opens on a page with a known topic (billing, moving), the first starter is that topic.
6. **Answer "what can you do?" and "hi" with the scope line and the starters,** not with another open question.
7. **Fit the opening in one view.** Scope line plus starters show without scrolling in the widget's default size.

**Reference design: opening config and check**
```json
{ "scope_line": "Hi, I'm Northfield's virtual assistant (an AI). Here I can check outages at your address, explain a charge on your bill, and set up a move or a plan change.",
  "starters": ["Check for an outage", "Explain my bill", "Moving or changing plans"],
  "always_last": "Something else",
  "placeholder": "e.g. Is there an outage on Elm St?",
  "page_overrides": { "/billing": ["Explain my bill", "Check for an outage", "Moving or changing plans"] },
  "starters_source": "top intents, last 30 days, bot-completed only" }
```
| Check on the rendered opening | Pass if |
|---|---|
| Scope line | Says it is an AI and names 2-4 tasks |
| Starters | 2-4, plus "Something else", each mapped to a tested intent |
| Placeholder | Not on the generic list ("Ask me anything", "How can I help you?", "Type a message") |
| Free text | Input enabled |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices | The chat opens with no messages, or the first message is "hi" or "what can you do?": 2-4 starters plus "Something else", free text open. Do not offer them when the first message is already a clear request. |
| Lead with the answer | The first message is a clear request ("is there an outage on Elm St"): answer or act on it; do not push the starters first. |
| Hand off to a person | The first message asks for a person, or names a task the bot cannot do: say so and offer a person. |

**Don't over-correct.** A wall of ten starters or a feature tour is as hard to start from as a blank box (see [first-run tours that block use](first-run-tours-that-block-use.md)). Do not pop the widget open on page load to show off the opening ([chat widget hard to find, or intrusive](chat-widget-hard-to-find-or-intrusive.md)). Do not lock people into the menu: free text stays open and "Something else" is always there. Do not list a task in the scope line that the bot cannot finish.

**Hand-off rule.** If the first message asks for a person, connect them with the page and any typed text passed along ([cold transfer](../../human-handoff/failures/cold-transfer.md)); do not answer with the starters ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)). If a top intent is one only a person can do, say that in the scope line.

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file exists yet. Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Open the widget on the Support page | 1, 2 | Scope line names 2-4 tasks; 2-4 starters plus "Something else" |
| 2 | Tap "Something else" | 3 | Input is focused and accepts free text |
| 3 | Inspect the placeholder | 4 | It is a concrete example, not on the generic list |
| 4 | Open the widget on /billing | 5 | First starter is "Explain my bill" |
| 5 | First message: "what can you do?" | 6 | Reply repeats the scope line and starters |
| 6 | First message: "is there an outage on Elm St" | Moves | Bot acts on it; no starter menu first |
| 7 | Widget at default size on a 375px-wide phone screen | 7 | Scope line and starters visible without scrolling |
| 8 | First message: "I want a real person" | Hand-off | Offers a person; no starters |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Share of first sessions with a first message or tap** (primary) | Set from baseline; track the lift | First sessions (new visitor ID) with a `user_message` or `starter_tap` event after `widget_open` | Falling two weeks in a row |
| Abandonment before the first message (paired) | Set from baseline; falling | Share of `widget_open` events followed by `widget_close` or timeout with no user event | Rising two weeks in a row |
| First messages that ask what the bot does | Falling from baseline | Phrase match plus a sampled review on first user messages ("what can you do", "what is this", "hi" alone) | Rising |
| Openings that pass the opening check | 100% | Automatic check of the rendered opening config on each release | Any miss |
| Starter taps that end in fallback or abandonment (counter-metric) | Set from baseline | Sessions whose first event is `starter_tap` and that hit a fallback or close within two turns | Rising; see [starter suggestions that fail](starter-suggestions-that-fail.md) |

### Detection signals (proposed, not yet calibrated)
Chat signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Web-analytics signals (scroll, hover, time on page) are PLANNED, not detected.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Widget opened and closed with no message or tap (primary metric) | `widget_open` then `widget_close`, no `user_message` or `starter_tap` | An accidental click, or a visitor who only wanted the hours shown in the header |
| First user message asks what the bot does | Phrase match on turn 1 of the session | A greeting typed out of habit before a real question in turn 2 |
| Opening text matches the generic list and has no scope line | Opening render event text | A scope line shown in the widget header instead of the message |
| Opening shows no starters, or none labeled "Something else" | Opening render event, starter list | A first message carried over from a page search box |
| Starter list not refreshed from recent top intents | Starter config timestamp compared with the intent report | A site with stable, unchanging top tasks |

**Starter rule:** Open with a scope line and 2-4 starters plus "Something else", with free text open.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: blank-box-no-hint-what-to-ask
runs: pre_send
reads: [widget.page_path, opening.scope_line, opening.starters, opening.placeholder, intent_stats.top_intents, user_turn.text]
trigger: the chat opens with no messages, or the first user message is "hi" or asks what the bot can do
moves: [offer_choices, lead_with_answer, hand_off]
choices: ["Check for an outage", "Explain my bill", "Moving or changing plans", "Something else"]
on_miss: rewrite
metric: share of first sessions with a first message or tap
counter_metric: starter taps that end in fallback or abandonment
status: proposed
```

## 8. Related patterns
- [Doesn't say what it can do](../../embedded-copilots/failures/doesn-t-say-what-it-can-do.md): the closest existing page. It covers an assistant inside a product: a capability card built from the tool registry, honest limits, and first-task success. This page covers any chat entry, including public website widgets, and the moment before the first message: whether the person starts at all. The two overlap on the opening screen; a reviewer may want to merge them.
- [Starter suggestions that fail](starter-suggestions-that-fail.md): the closest sibling. This page is about having no hint at all; that one is about hints that exist but lead to a weak or wrong answer.
- [Generic first response](../../embedded-copilots/failures/generic-first-response.md): an opener that ignores what the product knows about the user; rule 5 here is the page-level version.
- [Users must engineer prompts to get good results](users-must-engineer-prompts-to-get-good-results.md): what happens after the person starts typing.
- [Hidden commands and features](hidden-commands-and-features.md): features found later in the conversation, not at the start.
- [Does the chatbot say it's a bot?](../../trust-and-rapport/failures/undisclosed-bot-identity.md): the "(an AI)" part of the scope line.

## 9. Common questions
### What should a chatbot welcome message say?
That it is an AI assistant, and the two to four things it can do on this site, followed by tappable starting points. One usability study advises an intro specific to the situation instead of a generic offer of help ([section 4](#4-why-it-matters)).

### Should I use "Ask me anything" as the chat placeholder?
No. It tells the person nothing about what will work. Use a real example question from your top intents, such as "e.g. Is there an outage on Elm St?".

### How many suggested prompts should a chatbot show?
This page uses two to four plus "Something else", which is the library's rule for offering choices, not a tested number. More than that turns the opening into a menu; test on your own users.

### How do I know if users don't know what to ask my chatbot?
Log widget opens that close with no message or tap, and first messages like "what can you do?". Both rise when the opening says too little ([section 7](#7-metrics-how-to-spot-it-in-production)).

### Do starter prompts actually help?
One vendor reports that clickable defaults beat an empty box for its new users; I could not check its test. Treat it as a reason to run your own A/B test, not as proof.

---
## Technical section

### T1. Solution architecture
```
intent report (last 30 days, bot-completed intents) -> starter ranker -> top 2-4 per page path
page path -> page_overrides -> opening config -> opening check (CI) -> widget render
widget events (widget_open, starter_tap, user_message, widget_close) -> primary metric and signals
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Opening has scope line, 2-4 starters, "Something else" | Opening config schema | CI check on every release |
| Placeholder not on the generic list | Opening config schema | CI check |
| Each starter maps to a tested intent | Starter ranker | Join with the [starter suggestions that fail](starter-suggestions-that-fail.md) test results |

### T3. Evals
- **Dataset:** every page path where the widget can open, plus 50 real first messages from logs (greetings, "what can you do?", clear requests, requests for a person).
- **Judge rubric:** does the opening name what the bot does here, and does the first reply follow the Moves table?
- **Release gate:** block a deploy on any opening that fails the check. No threshold beyond that is set; tune once you have a baseline.

---
### Deep dive
- **Voice.** PLANNED. A phone or smart-speaker bot has no box to leave empty, but "How can I help?" with no scope is the same failure in audio.
- **Open question.** I found no controlled study comparing first-message rates with and without a scope line and starters. The Amplitude result is one company's own, and the arXiv paper tests suggestions after the first turn.
- **References.** [NN/g, Mar. 2026](https://www.nngroup.com/articles/site-ai-chatbot/) (opened); [Amplitude, Aug. 2026](https://www.amplitude.com/blog/ai-chat-box-tests) (opened); [arXiv 2412.10933](https://arxiv.org/abs/2412.10933v1) (abstract and full text opened).
