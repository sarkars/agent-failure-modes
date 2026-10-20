# Chatbot Suggested Questions That Give Bad Answers: Starter Suggestions That Fail

<!-- SEO
title: Chatbot Suggested Questions That Fail: Test Every Starter
description: Why a chatbot's suggested questions and conversation starters lead to weak or wrong answers, and how to test every chip and pull any that fail.
search phrases:
- chatbot suggested questions
- chatbot conversation starters best practices
- suggested prompts give wrong answer
- how to test chatbot conversation starters
- chatbot quick reply buttons don't work
- AI assistant follow-up suggestions it can't answer
-->

**Frequency**: Common

## Issue: The chatbot shows a suggested question or conversation starter, the user taps it, and the reply is weak, out of date, or wrong, because nobody tests the chips against the live bot.

> **One line:** A suggestion chip is a promise that the bot can answer that question; the fix is to run every chip through the live bot as a test, show only the ones that pass, and pull any that start failing.

| | |
|---|---|
| **Channel** | Written for **chat** (starter chips, suggested prompts, follow-up suggestions). Voice "try saying" hints and web-analytics signals are PLANNED, not written. |
| **Stakes** | Low to medium. The cost is a failed first impression, and a wrong answer the product itself put in the user's mouth. |
| **Who is affected** | New users, who tap starters most because they don't yet know what to type |
| **Frequency** | Common, in our judgment. I found no study that counts how often shown suggestions fail; one public example is in section 4. |
| **Pattern ID** | starter-suggestions-that-fail |
| **Family** | [Onboarding and discoverability](../README.md) |
| **Goal** | People know what the assistant can do and how to start, without needing to guess or to engineer prompts. |
| **Primary metric** | Suggestion success rate: replies rated resolved. Target: 100% for shown chips |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model doesn't know that a help article was deleted, a tool was disconnected, or a promotion ended; only a test of each chip against the live system catches that. (Our judgment, not tested.) |
| **Also searched as** | suggested prompts not working · conversation starters wrong answer · chatbot quick replies broken · suggested follow-up questions bot can't answer · example prompts that fail |

## 1. In plain words
The chat window opens with three buttons: "Track my order", "Change my delivery address", "Is the Fall Sale still on?". You tap one, because the bot suggested it. The answer is wrong, or the bot says it can't help with the very thing it just offered. Each chip is a small promise. The fix is to treat every chip as a test case, run it against the real bot on every change, and show only the chips that pass.

## 2. What it looks like

**Without the fix**
```
(Home-goods store help widget. Chips: [Track my order] [Change my delivery address] [Is the Fall Sale still on?])
User: Change my delivery address
Bot:  Go to Account > Orders and click Edit address.
User: There's no edit button. My bookshelf already shipped.
Bot:  I'm sorry, I can't help with that. Please contact support.
User: Is the Fall Sale still on?
Bot:  Yes! The Fall Sale runs through October 31.   (it ended October 18)
```

**With the fix**
```
(Same widget. The address chip failed its nightly test after the address tool was disconnected, so it is hidden.)
Chips: [Track my order] [Start a return] [Something else]   (text box open)
User: Track my order
Bot:  Your oak bookshelf (order MP-48213) shipped Friday, Oct 16 with UPS and is due Friday, Oct 23. [Track on UPS]
User: can I change the delivery address?
Bot:  I can't change an address from chat once an order has shipped. UPS lets you request a change on the tracking page, or I can connect you with our support team.
      [Open UPS tracking] [Talk to a person] [Something else]
```
Only chips that passed their test are shown, the chip reply leads with the answer, and when the user asks for something the bot can't do, it says so and gives two real routes.

## 3. Why it happens
These are our reading of the pattern; the sources below support parts of it, not the causes as a whole.
- **Chips are written as copy, not as test cases.** Product or marketing writes the starters at launch. They live in a widget config, outside the eval set, so nobody grades the answer each chip produces.
- **The system changes under fixed chips.** A chip that worked at launch breaks when a help article is removed, a promotion ends, a tool is disconnected, or the prompt or model is swapped. Without a re-run on each change, the chip stays up.
- **Generated follow-ups are not checked for answerability.** When the model writes its own suggested questions, nothing confirms that retrieval or a tool can answer them. In the Adobe study below, answerability was judged by human reviewers, not enforced by the system.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Use-case prompt suggestions help novice users learn what the tool can do; "Broad or generic prompt suggestions are rarely effective"; the authors advise manual selection because it "helps maintain a high standard of quality", and analytics to see which suggestions are used or ignored. | [Neusesser and Moran, *Designing Use-Case Prompt Suggestions*, Nielsen Norman Group, June 27, 2025](https://www.nngroup.com/articles/designing-use-case-prompt-suggestions/). Opened and read. | Expert design guidance, no statistics. It does not discuss suggestions that produce wrong answers or how to test them. |
| Following a suggested prompt on the New Bing homepage to make a pop music trivia game produced a fifth question that has no correct answer (three albums by three different artists), with Bing marking "Dua Lipa" as correct. | [Nick Heer, *Bing Also Flubs Its Demos*, Pixel Envy, Feb. 13, 2023](https://pxlnv.com/linklog/bing-flubs-its-demos/). Opened and read. | Single source: a blog post based on a reader's tip. I could not find it in the Brereton post the blog links to. It is one example of a product's own suggestion leading to a wrong answer, not a rate. |
| Suggested-question study on 250 randomly selected real interactions with Adobe's AI Assistant, with ten annotators comparing suggestion sets; "Validity" asked whether suggestions are valid questions and, "if possible to determine, whether they are answerable". | [Shen et al., *Enhancing Discoverability in Enterprise Conversational Systems with Proactive Question Suggestions*, arXiv 2412.10933](https://arxiv.org/html/2412.10933v1). Opened and read (HTML full text). | Vendor authors (Adobe), a preprint, GPT-3.5 suggestions. Answerability was a reviewer judgment, not a system check; the paper does not measure whether suggested questions got good answers. |
| An online A/B test in Bing found that "more useful question suggestions receive 8% more user clicks than the previous system". | [Rosset et al., *Leading Conversational Search by Suggesting Useful Questions*, The Web Conference 2020](https://www.microsoft.com/en-us/research/?p=630582). Abstract opened and read; the PDF did not render. | Vendor (Microsoft) on its own search product. It shows suggestion quality changes behavior; "useful" there is not the same as "answered correctly". |
| A vendor's batch-test tool runs real customer questions through its AI agent before release and has reviewers rate answers "Good, Acceptable, or Poor". | [Intercom, *Batch Test* update, Mar. 2025](https://fin.ai/updates/batch-test). Opened and read. | Vendor feature page, no results. It shows the test this page asks for can be run with existing tooling. |
| A chatbot builder's docs tell owners to open the site in a private window, select a starter, and confirm the chatbot answers it, and to pick starters from questions visitors often ask. | [SiteGPT docs, *Conversation starters*](https://sitegpt.ai/docs/features/conversation-starters). Opened and read. | Vendor docs. A one-time manual check; it says nothing about re-testing after changes. |

**Public incident.** The Bing trivia example above is the only one I found and opened. Search summaries also described other launch-demo errors (Google Bard, Gemini); those were demos, not in-product suggestions, and I did not open them, so they are not used.

## 5. The fix

**The principle:** A chip is shown only if the exact message it sends has passed a graded test against the live bot since the last change to the model, prompt, content, or tools.

**Do this**
1. **Give every chip a test case.** Store the exact payload the chip sends, the user state it is shown in (logged in or out, page), and the facts or action a resolved reply must contain.
2. **Gate display on a pass.** A chip is shown only if its test was rated resolved after the most recent change to the model, prompt, knowledge base, or tools. A rewording counts as a new chip and needs a new pass.
3. **Re-run on every change and on a schedule.** Run all chip tests on each deploy and content publish, and nightly as a starting point, so expired promotions and removed articles are caught.
4. **Pull failing chips automatically.** A failed test hides the chip until it passes again; it does not wait for a person to notice.
5. **Show a chip only where it can succeed.** A chip that needs an account, order, or tool is shown only to users in the state its test covered.
6. **Check generated suggestions before display.** A model-written follow-up is shown only if retrieval returns a supporting source or a tool exists that can do it; otherwise it is dropped.
7. **Show 2-4 chips plus "Something else", and keep the text box open.** Tapping a chip is never the only way forward.
8. **Watch chips live.** Track each chip's live success from ratings and sampled review; a chip whose live conversations fail is pulled and re-tested, as in rule 4.

**Reference design: chip registry entry and display gate**
```yaml
chip_id: track-order
label: "Track my order"
sends: "Track my order"            # exact payload, tested as sent
shown_when: {auth: logged_in, pages: [help, orders]}
resolved_if:                        # graded by reviewer or judge rubric
  - states carrier and expected delivery date from the order record
  - offers a tracking link
last_passed_at: 2026-10-20T03:10Z
last_system_change_at: 2026-10-19T22:40Z   # model, prompt, content, or tool change
status: shown                        # shown only if last_passed_at > last_system_change_at
```
| Check before display | If it fails |
|---|---|
| Test passed since the last system change | Hide the chip; queue a re-run |
| User's state matches `shown_when` | Hide it for this user |
| Generated suggestion has a source or tool | Drop it |
| Fewer than 2 chips pass | Show the passing ones and "Something else", or a one-line scope statement; never pad with untested chips |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | At the start, only tested chips. Do not offer them when no chip passes, or when the user has already typed a clear request |
| Lead with the answer | The reply to a tapped chip gives the answer or the result first |
| Admit uncertainty and show how to check | A chip-started request the bot can't finish live: say what it can't do and give a real route |
| Hand off to a person | A chip-started conversation hits a fallback twice, or the user rephrases the chip twice |

**Don't over-correct.** Removing every chip brings back the empty box (see [blank box: no hint what to ask](blank-box-no-hint-what-to-ask.md)). Keeping only chips that can never fail ("What are your hours?") hides what the bot is for; chips should come from the most common real requests. Do not let a passing test become a reason to stop watching: content changes daily.

**Hand-off rule.** If a conversation that started from a chip reaches a fallback reply twice, or the user rephrases the chip's question twice, offer a person and pass the chip ID and transcript along ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No full test file exists yet for this pattern. Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Every chip in the registry is sent to the live bot in its `shown_when` state | 1, 2 | Each shown chip's reply meets its `resolved_if` list |
| 2 | Knowledge base article behind a chip is unpublished, then the run is repeated | 3, 4 | The chip fails and is hidden without manual action |
| 3 | A chip is reworded | 2 | The new text is hidden until its own test passes |
| 4 | Logged-out user opens the widget | 5 | No chip that needs an order or account is shown |
| 5 | Model writes a follow-up question with no retrieval hit | 6 | The suggestion is not displayed |
| 6 | Any rendered chip set | 7 | 2-4 chips plus "Something else"; text box active |
| 7 | Live chip conversations are rated failed after a content change | 8 | The chip is pulled and queued for re-test |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. The 100% target is the catalog's target for shown chips, not a sourced benchmark.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Suggestion success rate: replies rated resolved** (primary) | 100% for shown chips | Chip test runs graded against `resolved_if`, plus a weekly sample of live chip-started conversations rated by a reviewer | Any shown chip below 100% |
| Chips shown without a pass since the last system change | 0 | Compare `last_passed_at` with `last_system_change_at` at render time | Any |
| Chip-started conversations that hit a fallback reply | Set from your baseline; track down | `chip_clicked` event followed by a fallback-intent reply in the next 2 turns | Rising two weeks in a row |
| Time from failed test to chip hidden | Under 1 test cycle | Timestamp of failed run vs. status change in the registry | Any chip shown after a failed run |
| Top intents covered by a passing chip (counter-metric) | Set from your baseline | Share of the top 10 first-message intents in logs that have a passing chip | Falling after a removal wave |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are for text chat; voice and web-analytics signals are PLANNED.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Chip tap followed by a fallback or "I can't help with that" reply | `chip_clicked` event, then reply intent = fallback | A chip correctly routing to a person by design |
| User rephrases or contradicts right after a chip reply ("there's no edit button") | Next user turn after `chip_clicked` with high overlap to the chip, or a negation | The user adding a detail the chip could not know |
| Session ends with a thumbs-down within 1 turn of a chip reply | `chip_clicked`, rating event, session end | User got the answer and disliked the policy, not the reply |
| Chip rendered after a deploy or content publish with no newer test pass | Registry `last_passed_at` older than `last_system_change_at` | A change that cannot affect the chip (e.g., a style tweak), if your gate excludes it on purpose |
| Generated suggestion shown with no retrieval hit or tool match | Suggestion payload with empty `sources` and no `tool_id` | None; this is a defect |

**Starter rule:** a chip is shown only if the exact message it sends has passed a graded test against the live bot since the last change to the model, prompt, content, or tools.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: starter-suggestions-that-fail
runs: pre_send
reads: [chip_registry.last_passed_at, chip_registry.last_system_change_at, chip_registry.shown_when, user.auth_state, suggestion.sources, suggestion.tool_id]
trigger: a set of starter chips or generated suggestions is about to be shown
moves: [offer_choices, lead_with_answer, admit_uncertainty, hand_off]   # short names for the moves in the table
choices: ["Track my order", "Start a return", "Something else"]   # example only; only chips that passed their test
on_miss: rewrite   # drop the failing chip before render; log it
metric: "suggestion success rate: replies rated resolved"
counter_metric: top intents covered by a passing chip
status: proposed
```

## 8. Related patterns
- [Blank box: no hint what to ask](blank-box-no-hint-what-to-ask.md): no suggestions at all. This page is the next step: suggestions are shown, then fail. Fixing the blank box with untested chips creates this pattern.
- [No likely-next-action suggestions](../../embedded-copilots/failures/no-likely-next-action-suggestions.md): the closest existing page. It is about an in-app assistant that offers no next steps after an answer; this page is about whether the suggestions that are shown, at the start or later, actually lead to a resolved reply.
- [Doesn't say what it can do](../../embedded-copilots/failures/doesn-t-say-what-it-can-do.md): a missing capability statement. A failing chip is a capability statement that turns out false.
- [Users must engineer prompts to get good results](users-must-engineer-prompts-to-get-good-results.md): quality depends on wording. Chips are meant to remove that burden, so a failing chip fails the user who did exactly what was suggested.
- [Dead-end "I don't understand" replies](../../conversation-leadership/failures/dead-end-i-don-t-understand-replies.md): the fallback a failing chip often lands on.

## 9. Common questions
### How do I test chatbot conversation starters?
Send each starter's exact text to the live bot, in the same user state it is shown in, and grade the reply against a short list of facts it must contain. Re-run on every deploy or content change. See [the fix](#5-the-fix).

### How many suggested questions should a chatbot show?
This page uses 2-4 plus "Something else", following the library's [conversation moves](../../../solutions-library/conversation-moves.md). I found no study that tested the right number for starter chips, so tune it on your own data.

### Should I let the AI generate its own suggested follow-up questions?
You can, but check each one before it is shown: it needs a source from retrieval or a tool that can do it. Otherwise the bot can suggest questions it cannot answer.

### What if fewer than two starters pass their tests?
Show the ones that pass plus "Something else", or a one-line statement of what the bot covers. Don't fill the gap with untested chips.

---
## Technical section

### T1. Solution architecture
```
chip registry -> test runner (on deploy, content publish, nightly) -> live bot -> grader (rubric or reviewer)
             -> registry status (shown / hidden)
widget render -> display gate (passed since last change? user state matches?) -> 2-4 chips + "Something else"
generated suggestion -> answerability check (source or tool) -> show or drop
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No chip shown without a fresh pass | Display gate | Test 2, metric 2 |
| Reworded chip needs its own pass | Registry (new chip_id per text) | Test 3 |
| Generated suggestion needs a source or tool | Suggestion filter | Test 5 |
| "Something else" and text box present | Renderer | Test 6 |

### T3. Evals
- **Dataset:** every chip in the registry, each in every user state it is shown in.
- **Judge rubric:** does the reply contain each `resolved_if` item, and is anything in it false against the source of truth?
- **Metrics and starting thresholds:** suggestion success rate 100% for shown chips (catalog target).
- **Release gate:** a deploy may ship, but a chip that fails is hidden before the deploy goes live.

### T5. Trade-offs
- Each test run costs model calls; the chip set is small, so nightly runs are cheap compared with a full eval.
- An LLM judge can pass a wrong answer; keep a weekly human-reviewed sample of live chip conversations.

---
### Deep dive
- **Open question.** No source I opened measures how often shown suggestions fail. The evidence shows that suggestions shape behavior (Bing A/B) and that one product's own suggestion led to a wrong answer (Bing trivia), not a failure rate.
- **Read only in part.** An Atlassian Community thread titled "How do I disable suggestions and guesses in the CSM chat bot responses?" was opened, but only the title was readable; a search summary of its body is not used.
- **Voice.** PLANNED. "Try saying" hints in voice assistants are the same promise and need the same test gate.
- **References.** [NN/g 2025](https://www.nngroup.com/articles/designing-use-case-prompt-suggestions/) (opened); [Pixel Envy 2023](https://pxlnv.com/linklog/bing-flubs-its-demos/) (opened); [arXiv 2412.10933](https://arxiv.org/html/2412.10933v1) (opened); [Rosset et al. 2020](https://www.microsoft.com/en-us/research/?p=630582) (abstract opened); [Intercom Batch Test](https://fin.ai/updates/batch-test) (opened); [SiteGPT docs](https://sitegpt.ai/docs/features/conversation-starters) (opened).
