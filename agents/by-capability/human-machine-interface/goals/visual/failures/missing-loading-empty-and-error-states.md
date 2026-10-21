# Chatbot Card or Widget Shows a Blank Screen or Endless Spinner: Missing Loading, Empty, and Error States

<!-- SEO
title: Chatbot Widget Blank Screen or Endless Spinner: Fix Missing States
description: A chat card or widget that loads data shows a blank box or a spinner that never ends. Give every async view a loading, empty, and error state.
search phrases:
- chatbot widget blank screen
- chatbot card stuck loading spinner
- empty state design for chatbot cards
- loading state vs empty state vs error state
- ai assistant widget shows nothing
- spinner never stops chatbot
- how to design empty states for an ai assistant
- aria-busy loading state chat widget
-->

**Frequency**: Common

## Issue: A chat card or widget that fetches data shows a blank box or a spinner with no explanation, so the user cannot tell whether it is working, empty, or broken.

> **One line:** Every async view needs three defined states: loading (with a time limit), empty (with a reason and a next step), and error (with a cause and a next step). Without them the user sees a blank box.

| | |
|---|---|
| **Channel** | Written for **chat** assistants and their widgets, cards and generated visuals. Voice and web-page signals are PLANNED. |
| **Stakes** | Low to high. An empty order list that looks like a failed load can send a user to support, or make them reorder. |
| **Who is affected** | Anyone who opens a card, list, chart, or embedded widget that depends on a fetch. Screen reader users are affected most when a change is not announced. |
| **Frequency** | Common. Observed in practice; I found no study that counts how often chat widgets ship without these states. |
| **Pattern ID** | missing-loading-empty-and-error-states |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | States defined on 100% of async views; blank-screen rate 0. Starting targets to tune. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The states come from the widget code and the product's data calls, not from the model. (Our judgment, not tested.) |
| **Also searched as** | chatbot widget blank · spinner never ends · card shows nothing · empty state vs error state · no results message in chat · loading skeleton chatbot |

## 1. In plain words
A chat card that pulls data (orders, appointments, a chart) has more than one way to show nothing. It may still be loading, it may have loaded and found nothing, or it may have failed. If the card looks the same in all three cases, the user guesses. Define all three states for every view that waits on data, and test that none renders a blank area.

## 2. What it looks like

**Without the fix**
```
User: Show my open orders.
Bot:  Here are your open orders:
      [ card: header "Open orders", body empty, spinner turning ]
User: (waits, then types) Hello? Did that work?
Bot:  [ card unchanged ]    (the fetch failed 40 seconds ago; the card never found out)
```

**With the fix**
```
User: Show my open orders.
Bot:  Here are your open orders:
      [ card: "Loading your orders..." ]
      (after 8 seconds) "Still loading. This is taking longer than usual." [Keep waiting] [Cancel]
      (on timeout) "I couldn't load your orders: the order system didn't respond. Nothing was changed.
                    [Try again] [Contact support] [Something else]"
      (or, if the fetch worked and returned nothing) "You have no open orders. Orders you place
                    will appear here. [Browse items]"
```
The fixed card says which state it is in, gives a reason, and offers one next step. The 8-second figure is an example to tune.

## 3. Why it happens
These are our reading of the pattern.
- **Only the success path is built.** Teams design the card with data in it, then ship. The states with no data are left to browser defaults, so they render as blank.
- **Loading, empty and error share one flag.** A single "no items" check treats a failed fetch and a true empty result alike, so a failure can show "nothing here", which is a false status.
- **No timeout on the fetch.** A loading state with no upper limit never turns into an error, so the spinner runs until the user gives up.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| NN/g states that "Totally empty states cause confusion about how and whether the system is working," and advises "Do not default to totally empty states." It also warns that inaccurate system-status messages in empty states are particularly harmful. | [Nielsen Norman Group, empty state interface design](https://www.nngroup.com/articles/empty-state-interface-design/). Opened and read (headings and quoted lines). | Guidance for complex applications, not chat widgets. A design guideline, not an experiment. |
| NN/g advises: "When a process is running, use progress indicators to increase visibility of system status," and, if nothing is found after a process ends, to use the empty space for a system-status message. | Same article. | Same as above. |
| Response-time limits: past about 1 second, "indicate to the user that the computer is working"; for operations over about 10 seconds use a percent-done indicator and a clear way to interrupt; a spinner is a last resort when total work is unknown. | [Nielsen, *Response Times: The 3 Important Limits*](https://www.nngroup.com/articles/response-times-3-important-limits/). Opened; the page text was read through the fetch tool's extraction, so the quotes are the tool's. | Excerpt from a 1993 book, updated in 2014. Based on general interface timing, not AI chat. |
| NN/g says generic messages such as "An error occurred" lack context, and merely stating the problem is not enough: offer remedies. | [NN/g, *Error-Message Guidelines*](https://www.nngroup.com/articles/error-message-guidelines/). Opened; read through the fetch tool's extraction. | Applies to forms and applications generally. |
| WCAG 2.2 SC 4.1.3 (Level AA) requires that status messages "can be programmatically determined through role or properties," so assistive technology can present them without moving focus. Its definition includes the result of an action, "the waiting state of an application," a process's progress, and the existence of errors. | [W3C, Understanding SC 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html). Opened; read through the fetch tool's extraction. | A WCAG understanding document, not legal advice. Whether a given widget is in scope depends on the product and jurisdiction; I did not check any law. |
| MDN: `aria-busy` is a global state meaning an element "is currently being modified"; with live regions, set `aria-busy="true"` until loading is complete, then `"false"`. | [MDN, `aria-busy`](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy). Opened; read through the fetch tool's extraction. | Documentation of the attribute. It does not say how often screen readers honor it. |

I found no study that counts blank states or spinner timeouts in chat widgets. A third-party source warns that leaving `aria-busy="true"` set forever makes a region look permanently loading; I saw that only in a search summary, so I keep it out of the rules.

**Public incident.** No public incident found for this pattern as such.

## 5. The fix

**The principle:** No async view ever renders a blank area: it is loading, empty, or failed, and it says which.

**Do this**
1. **Define all three states before building the success view.** Each async card, list, chart or embedded widget has a loading, an empty, and an error design on its spec.
2. **Show a loading state at once and give it a time limit.** Show it when the fetch starts. After a set wait (start at 8 seconds, tune), say it is taking longer and offer Cancel. At the timeout, switch to the error state. A spinner never runs without a limit.
3. **Separate empty from error.** An empty state is only for a fetch that succeeded and returned zero items. A failed or timed-out fetch always shows the error state, never "nothing here".
4. **Make the empty state say why and what next.** Say that the fetch worked and found nothing, why that is likely, and one action (for example "Browse items" or "Clear filters").
5. **Make the error state say what failed, what is unchanged, and what to do.** Use the pattern from [generic error messages](../../errors-and-recovery/failures/generic-error-messages.md), applied to the view: cause in plain words, whether any data was changed, one next step.
6. **Announce state changes in text.** Put the loading, empty and error messages in a status region (`role="status"` or an `aria-live` region) so they reach a screen reader, and mark a busy region with `aria-busy` while it loads, then clear it. Always clear it, including on error.
7. **Fall back to chat text.** If the widget cannot render, the assistant says the same state in its reply, so the user is never left with only the card.
8. **Do not use a spinner as the only signal for a wait the system knows will be long.** For waits over about 10 seconds, show progress or what is happening, as in [silent long-running work](../../response-time/failures/silent-long-running-work.md).

**Reference design: state table for one async view**
| State | Enter when | Shows | Next step | Announced as |
|---|---|---|---|---|
| Loading | Fetch started | "Loading your orders..." (skeleton or short text) | Cancel after the slow-load wait | Status message; `aria-busy` true |
| Slow | Fetch still running past the slow-load wait | "Still loading. This is taking longer than usual." | Keep waiting, Cancel | Status message |
| Empty | Fetch succeeded, zero items | "You have no open orders." plus why | One action, or none if nothing applies | Status message |
| Error | Fetch failed or timed out | Cause, what is unchanged | Try again, contact support, Something else | Alert or status message |
| Ready | Fetch succeeded, items | The content | Normal actions | `aria-busy` false |

```
Every card or widget that loads data has four rendered states: loading, empty, error, ready. Never render a blank body.
Treat a failed or timed-out fetch as an error, never as empty. Use "empty" only after a successful fetch that returned zero items.
In the error state say what failed, whether anything changed, and one next step. In the empty state say it loaded and found nothing, and offer one action.
Put the state text in a status region. If the widget cannot render, say the same thing in the chat reply.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The fetch failed or timed out and the cause is unknown: say the data is not shown, say nothing was changed only if true, and give one way to check or retry. |
| Offer choices: 2-4 options plus "Something else", free text open | In the error or slow state: "Try again", "Contact support", "Cancel", "Something else". Do not offer them in a plain loading state under the slow-load wait, or in an empty state with one obvious action. |
| Hand off to a person | The same view fails twice in a row, or the data is needed for a high-stakes step. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not add a loading message to a view that appears within a fraction of a second; a flash of text is noise (NN/g: no special feedback is needed for very short delays). Do not announce every update; too many status messages bury the important one. Do not write a paragraph in an empty state.

**Hand-off rule.** After two failures of the same view, offer a person and pass the view name and the error reference ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **Not yet run**.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Block the data call so it never returns | A loading state shows at once, a slow message appears, and the error state shows at the timeout (rules 2, 3) |
| 2 | Return a successful empty list | The empty state says it loaded and found nothing, and offers an action or none (rules 3, 4) |
| 3 | Return an HTTP error and a malformed payload | The error state shows, never "nothing here" (rules 3, 5) |
| 4 | Render each state with a screen reader or an accessibility-tree check | The text sits in a status region and `aria-busy` is cleared after error (rule 6) |
| 5 | Make the widget fail to mount | The chat reply states the same condition in text (rule 7) |
| 6 | Load a view that returns in a fraction of a second | No flash of a loading message (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **States defined on async views; blank-screen rate** (primary) | 100% of async views have loading, empty and error; blank-screen rate 0 | Inventory async views against a spec list; log renders with an empty body and no state tag | Any async view missing a state; any blank render |
| Spinners that outlast the timeout | 0 | Loading renders with no state change after the limit | Any |
| Failed fetches shown as empty | 0 | Empty renders where the fetch event has an error code | Any |
| State changes with a status-region announcement | 100% | Accessibility-tree check in the test suite | Below 100% |
| Repeat prompt after a card (counter-signal check) | Track; set from baseline | User sends "hello?" or the same request within 1 turn of a card render | Rising two weeks in a row |
| Loading messages on fast loads (counter-metric) | Under 5% of loads | Loading renders shorter than 300 ms | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Widget render with an empty body and no state tag | Render event with body length 0 and `state` missing | A deliberately decorative widget |
| Loading state with no end event after the limit | Loading start event with no ready, empty or error event | A long job that shows progress and a cancel option |
| Empty state rendered while the fetch event has an error code | Fetch event and render event for the same view | A retry that succeeded in between |
| User asks "did that work?" or repeats the request after a card | Same intent in the next user turn | A deliberate follow-up question |

**Starter rule:** every async view renders loading, empty, or error text with a reason and next step, never a blank area, and a failed fetch is never shown as empty.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: missing-loading-empty-and-error-states
runs: pre_send
reads: [widget.view_id, widget.state, widget.body_length, fetch_event.status, fetch_event.error_code, fetch_event.elapsed_ms]
trigger: an async card or widget is about to be rendered, or its fetch has run past the limit
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Try again", "Contact support", "Cancel", "Something else"]
on_miss: rewrite
metric: states defined on 100% of async views; blank-screen rate 0
counter_metric: loading messages on fast loads
status: proposed
```

## 8. Related patterns
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): the wording of an error. This page is about the view having a defined state at all, and about not showing a failed fetch as empty.
- [Silent long-running work](../../response-time/failures/silent-long-running-work.md): status during a long task in the conversation. This page covers the states of one card or widget.
- [Silent failure and timeout](../../response-time/failures/silent-failure-and-timeout.md): a chat reply that never arrives or cuts off. This page covers the embedded view.
- [Blank box, no hint what to ask](../../onboarding-and-discoverability/failures/blank-box-no-hint-what-to-ask.md): an empty input box on first use, not an empty data view.
- [No accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md): announcing working and done to assistive technology; rule 6 relies on it.
- [Rich-card misuse](rich-card-misuse.md): choosing cards at all.

## 9. Common questions
### What is the difference between a loading, empty, and error state?
Loading means the fetch has not returned. Empty means it returned and found nothing. Error means it failed or timed out. They need different text and different next steps, and a failed fetch must never be shown as empty ([section 5](#5-the-fix), rule 3).

### Why does my chatbot widget show a blank screen?
The usual cause is that only the success view was built, so a slow, empty or failed fetch renders nothing. Add the three states and a timeout ([reference design](#5-the-fix)).

### How long should a spinner run before I show an error?
I found no sourced number for chat widgets. NN/g's response-time limits give about 1 second before showing that work is in progress and about 10 seconds before showing progress and a way to interrupt, so start with a slow message near 8 seconds and a timeout you tune from your own data.

### What should an empty state say?
That the data loaded and there is nothing to show, why that is likely, and one action. NN/g advises against totally empty states and says to use the space for a system-status message.

### How do I make loading states work with screen readers?
Put the text in a status region and use `aria-busy` while it loads, then clear it. WCAG 2.2 SC 4.1.3 covers waiting-state and progress messages. See [no accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md).

---
## Technical section

### T1. Solution architecture
```
view spec (loading|slow|empty|error|ready text) -> renderer
fetch start -> loading + aria-busy true -> timer
fetch ok, items>0 -> ready | fetch ok, items=0 -> empty | fetch error or timer limit -> error
every transition -> status region text + render log (view_id, state, elapsed_ms)
widget mount failure -> chat reply carries the same state in text
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No render with an empty body and no state tag | Renderer | Log scan; test 1 |
| Error is never rendered as empty | State machine | Test 3 |
| `aria-busy` cleared on every exit from loading | Client | Test 4 |

### T3. Evals
- **Dataset:** for each async view, inject delay, timeout, error, empty and success. Start with every view in the product.
- **Judge rubric:** does the rendered text name the state, give a reason, and give a next step? Is the state announced?
- **Metrics and starting thresholds:** blank renders 0; failed-as-empty 0. Starting points to tune.
- **Release gate:** block a deploy that adds an async view without all four states.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Blank or untagged renders | Any | More than a handful in one hour (set from baseline) | Find the view with the missing state |

### T5. Trade-offs
- Four states per view cost design and test time; a shared state component keeps it low.
- Short timeouts show errors on slow but healthy networks; tune the limit on real latency data.

---
### Deep dive
- **Open question.** I found no chat-specific study of loading or empty states. The evidence is general interface guidance and accessibility documentation, and I did not open Material, Apple, or other design-system pages.
- **Modality notes.** Voice: PLANNED (the spoken equivalent of a blank screen is silence). Generated visuals: a chart with no data should say so in its caption and alt text, not render an empty axis.
- **References.** [NN/g, empty state interface design](https://www.nngroup.com/articles/empty-state-interface-design/) (opened); [NN/g, response times](https://www.nngroup.com/articles/response-times-3-important-limits/) (opened); [NN/g, error-message guidelines](https://www.nngroup.com/articles/error-message-guidelines/) (opened); [W3C, SC 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html) (opened); [MDN, aria-busy](https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Reference/Attributes/aria-busy) (opened).
