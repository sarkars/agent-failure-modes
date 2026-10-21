# Generative UI Layout Shifts and Broken Components: Generative UI Instability

<!-- SEO
title: Generative UI Layout Shifts and Broken Components in Chat
description: A chat assistant builds its own cards and widgets, and the layout jumps or the component breaks. Rules to validate every component and keep the layout still.
search phrases:
- generative UI layout shift
- generative UI inconsistent components
- chatbot widget jumps while streaming
- LLM generated UI invalid props
- generative UI fallback when component fails
- AI SDK generative UI tool output error
- chatbot card changes layout every time
- structured output schema validation UI component
-->

**Frequency**: Occasional

## Issue: A chat assistant that picks or fills its own cards and widgets shows a layout that jumps while it streams, or a component that differs or breaks from one reply to the next.

> **One line:** When a model decides which component to render and with what fields, the card can appear late and push text around, arrive with missing or wrong fields, or look different for the same request; the fix is to let the model choose only from a fixed set of components, validate every one against a schema before it is shown, reserve its space, and fall back to plain text.

> **Read this first (flag R).** This page is design guidance from vendor documentation and our judgment. I found no study that measures how often chat products show unstable generated interfaces, so the frequency and the starting targets are not sourced. See "Not found" in section 4.

| | |
|---|---|
| **Channel** | Written for **chat** (cards, widgets and generated components inside a chat window, text fallback). Voice and full web-app variants are PLANNED, not written. |
| **Stakes** | Low to medium. A jumping card costs a mis-tap; a broken price or date field in a booking or payment card can cost money. |
| **Who is affected** | Anyone using a chat that renders model-chosen components; people on slow connections, small screens or screen readers feel it most |
| **Frequency** | Occasional. No count found (our judgment). |
| **Pattern ID** | generative-ui-instability |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. (Row goal: generated interfaces are stable and valid.) |
| **Primary metric** | Layout-shift measure; component-schema validity. Target: 100% (starting point; tune it). Schema validity is the share of rendered components that pass their schema; the shift measure is the score defined in section 7. |
| **Maturity** | Researched. No test file yet; section 6 scenarios are designs and are **Not yet run**. |
| **Will a better model fix this?** | Partly. A stronger model fills fields more reliably, but layout shift comes from how the UI renders late content, and no model setting removes it. (Our judgment, not tested.) |
| **Also searched as** | chatbot card jumps while loading · AI generated UI breaks · generative UI different every time · LLM returns wrong component props · streaming widget layout shift · chat UI flicker |

## 1. In plain words
Some assistants build their own screen pieces: a weather card, a flight list, a chart. If the model picks the piece and its fields freely, the card may show up late and shove the text down, arrive half filled, or look different each time you ask. The fix is a short list of approved components, a check on every one before it appears, and a plain-text answer when the check fails.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Northwind Air" assistant)
```
User: Find me a flight to Denver on Friday.
Bot:  Here are some options for you:
      [text keeps streaming; a flight card pops in above it, pushing the text off screen]
      [card shows: "Departs: undefined   Price: $NaN"]
User: (taps "Book", but the card has moved; the tap lands on "Cancel")
Bot:  [asks again; this time a table, not a card]
```
**With the fix**
```
User: Find me a flight to Denver on Friday.
Bot:  [Skeleton card holds a fixed-size slot under "Looking up Friday flights..."]
Bot:  Two nonstop options on Friday. The 7:05 a.m. is $212, the 1:40 p.m. is $189.
      [Flight card fills the reserved slot: same layout both times; each field checked first]
      Want the cheaper one?
```
The fixed version reserves the card's space, shows it only after every field passes its schema, repeats the key facts in text, and uses the same component for the same task.

## 3. Why it happens
- **The model chooses the shape at run time.** In generative UI the model's tool call decides which component appears and with what fields, so two similar requests can end in different components, or in fields the component never expected.
- **Components arrive after the text.** Text streams first, and a tool result or a streamed component lands later. If its space was not reserved, everything under it moves.
- **Schema checks are often missing or end in an error state.** A schema describes the fields, but a reply can still fail to match (a refusal, a cut-off at the token limit), and a UI without a fallback shows blank, "undefined" or an error.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| web.dev defines Cumulative Layout Shift as impact fraction times distance fraction, rates 0.1 or less as good and above 0.25 as poor, and suggests judging it at the 75th percentile of page loads, split by mobile and desktop. Shifts within 500 ms of user input can be excluded from the calculation. | [web.dev, Cumulative Layout Shift](https://web.dev/articles/cls) (last updated 2023-04-12 on the page). Opened. | Written for web pages, not chat widgets. I borrow the score as a measure; the thresholds are not validated for a chat window. |
| web.dev advises reserving space for late content (width and height, aspect-ratio, min-height), using a placeholder or skeleton for dynamic UI, not inserting content above existing content without user input, and animating with transforms. | [web.dev, Optimize Cumulative Layout Shift](https://web.dev/articles/optimize-cls) (page dated Feb 2025). Opened. | General web guidance. It does not mention chat or streamed model output. |
| Vercel's AI SDK 3.0 launch post describes generative UI as moving beyond plain text and markdown chatbots to component-based interfaces; the model's tool call determines which component is displayed, and the render function can show a spinner first. | [Vercel, AI SDK 3.0 generative UI](https://vercel.com/blog/ai-sdk-3-generative-ui) (Mar 1, 2024). Opened. | **Vendor** launch post. It describes the idea; it does not report instability. The RSC-based API it describes is reported elsewhere as paused, which I did not open. |
| The current AI SDK docs say generative UI "is the process of connecting the results of a tool call to a React component", with a tool defined by a description and an input schema. The example page switches on tool state: loading, output available, and an error state that shows the error text. | [AI SDK, Generative User Interfaces](https://ai-sdk.dev/docs/ai-sdk-ui/generative-user-interfaces). Opened. | **Vendor** docs. Fetched through a summarizing tool, so I treat wording as paraphrase. The page does not describe validating the output beyond the input schema. |
| OpenAI's Structured Outputs guide says JSON mode guarantees valid JSON but only Structured Outputs ensure schema adherence. It also warns that the model might not return a valid match when it refuses or is cut off at a token limit, and that the first request with a schema has extra latency. | [OpenAI, Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs). Opened (first 100,000 of about 136,000 characters read). | **Vendor** docs for one API. Other providers differ. It addresses data shape, not whether a card looks stable. |

**Not found.** I found no independent study of how often chat products shift layout, break components or vary them between identical requests, and no study of user harm from these. Search results for the AI SDK pointed to mirrored README copies and a paused RSC template; I did not open them and use none of that. Rows above come from vendor and standards documentation only.

**How this differs from the closest pages.** [Rich-card misuse](rich-card-misuse.md) asks whether a card should be used at all for the task; this page assumes a component is right and asks whether it is stable and valid. [Misleading generated visuals](misleading-generated-visuals.md) is about an unlabeled or unfaithful image or chart; this page is about a component that moves, varies or breaks. [Auto-scroll fights the reader](../../chat-interface/failures/auto-scroll-fights-the-reader.md) covers the scroll position moving in a chat; a late card is one cause, and rule 3 below is the fix on the component side.

## 5. The fix

**The principle:** The model chooses from a fixed set of approved components, and nothing is shown until it passes its schema and has its space reserved; otherwise the user gets plain text.

**Do this**
1. **Use a closed component registry.** The model can name only components on the list (for example `flight_card`, `price_table`). An unknown name is never rendered; the reply falls back to text.
2. **Give every component a schema and check it before render.** Required fields present, types correct, enum values allowed. A failed check blocks the component (rule 6), not the whole reply.
3. **Reserve the space first.** Each component has a fixed minimum height or aspect ratio and a skeleton. Content never lands above text the user has started reading, unless the user asked for it.
4. **Render a component once, complete.** Show it after its schema passes. Do not stream partial fields into it, and do not swap it for another component type after it appears.
5. **Same task, same component.** Map each intent to one component and one field order. A repeat of the same request returns the same layout.
6. **Fall back to text on failure.** If validation fails, the model refuses, or the output is cut off, send a plain-text answer with the key facts. Never show "undefined", "NaN" or an empty card.
7. **Repeat the key facts in text, and label for a screen reader.** The answer is readable if the component never loads (see [accessibility gaps](accessibility-gaps.md)).
8. **Keep tap targets still.** Buttons do not move within 500 ms before a tap lands; disable a control until its card is final.

**Reference design: component contract**
```
component: flight_card            # one registry entry per approved component
required: [origin, destination, depart_time, price_usd, book_action]
types:    {price_usd: number >= 0, depart_time: ISO time, book_action: enum[book]}
slot:     min_height 168px, skeleton: yes, width: 100% of message
on_invalid: send text summary + log component_invalid
on_unknown_component: send text + log component_unknown
fallback_text: "{origin} to {destination}, {depart_time}, ${price_usd}"
```
```
Choose a component only from the registry. Fill every required field from tool results, never from memory.
If a field is missing, say so in text and do not render the component.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The component fails or is slow: state the key facts in text first, so nothing depends on the widget |
| Admit uncertainty and show how to check | A field is missing or unverified: say which one, and link to the source or the full page |
| Offer choices | The component cannot render and the next step has 2-4 meanings: "Show as text", "Open the full page", "Try again", "Something else"; free text stays open. Do not offer when the text answer already covers the request |
| Hand off to a person | The same component fails twice in a row on a transaction (booking, payment): offer a person with a summary |

**Don't over-correct.** Do not lock every reply to text, or freeze components that should update. A live status card may change; it should change inside its reserved slot, and in response to the user or a clear event. Do not block a whole reply because one optional field is missing; show text instead.

**Hand-off rule.** When the same component fails validation twice in one conversation for a booking, payment or other consequential step, stop rendering it, give the facts in text, and offer a route to a person ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet. The rules follow the web.dev layout-shift guidance and the vendor schema docs in section 4, plus our judgment; the numbers in the contract are placeholders to tune.

## 6. How to test it (short version)
No test file yet. The scenarios are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Make the model name a component not on the list | Nothing unknown renders; a text answer appears | 1, 6 |
| 2 | Return a tool result with a missing required field | The component is blocked; the text says which fact is missing | 2, 6 |
| 3 | Send a wrong type (price as text) | Validation fails; no "NaN" or "undefined" on screen | 2, 6 |
| 4 | Delay the component 3 seconds on a throttled connection | The reserved slot holds; text above and below does not move | 3 |
| 5 | Cut the response off at a low token limit | The partial component is never shown; fallback text appears | 4, 6 |
| 6 | Ask the same request five times | The same component and field order each time | 5 |
| 7 | Load the reply with the widget script blocked | The key facts are still in the message text | 7 |
| 8 | Tap "Book" as the card finishes loading | The control was disabled until final; the tap does not land elsewhere | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Component-schema validity** (primary, with the shift measure) | 100% of rendered components pass | Validate every component payload before render; log `component.valid`; report rendered-and-valid over rendered | Any rendered invalid component |
| **Layout-shift measure** (primary) | 0.1 or less at the 75th percentile (the web.dev "good" level, borrowed for chat; not validated for it) | Log layout-shift entries for the chat view by message, with `hadRecentInput` to exclude shifts within 500 ms of a user action; sum per message | Above 0.1 |
| Fallback-to-text rate | Track; set from your baseline | Share of replies where a component was planned but text was sent | Rising week over week |
| Same-intent layout consistency | 100% (starting point) | Replay a fixed set of intents; compare component name and field order across runs | Any difference |
| Taps lost to a moving control (counter-metric) | Track | Taps on a control within 500 ms after a layout change | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat**; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A component payload fails its schema or names an unknown component (rules 1, 2) | `component.valid = false` or `component.unknown` | A new component shipped before the registry update |
| A layout shift above the target while a message streams (rule 3) | Layout-shift entry tied to a message id | A shift the user caused by expanding a section |
| Same intent returns a different component than before (rule 5) | Component name differs across turns for one intent | The user changed the request, such as adding a filter |
| The user repeats the request right after a card | Same intent in the next user turn | A deliberate refinement |
| A visible "undefined", "NaN" or empty field in a rendered card (rule 6) | Text scan of rendered component strings | A product named "NaN" or an intentional blank |

**Starter rule:** the model chooses only from a fixed component list, and nothing renders until it passes its schema and has its space reserved; otherwise the reply is plain text.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: generative-ui-instability
runs: pre_send
reads: [message.components, component.name, component.payload, component.schema, registry.allowed, channel.supports]
trigger: a reply with a model-chosen component is about to be rendered
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Show as text", "Open the full page", "Try again", "Something else"]
on_miss: rewrite
metric: layout-shift measure; component-schema validity
counter_metric: taps lost to a moving control
status: proposed
```

## 8. Related patterns
- [Rich-card misuse](rich-card-misuse.md): whether a card belongs at all; here the card is right but unstable.
- [Misleading generated visuals](misleading-generated-visuals.md): an unlabeled or unfaithful image or chart.
- [Auto-scroll fights the reader](../../chat-interface/failures/auto-scroll-fights-the-reader.md): scroll position moving; a late card is one cause.
- [Accessibility gaps](accessibility-gaps.md): the text and labels that keep a failed component usable.
- [Streaming text read out token by token](../../accessibility/failures/streaming-text-read-out-token-by-token.md): another cost of content that arrives in pieces.

## 9. Common questions
### Why does my chatbot's layout jump while the answer loads?
Usually a card or image arrives after the text and its space was not reserved. Give the component a fixed slot and a skeleton, as web.dev advises for late content (rule 3).

### How do I stop an LLM from returning invalid props for a UI component?
Constrain the output with a schema and check it before rendering. OpenAI's guide says only Structured Outputs ensure schema adherence, and that a refusal or a token cutoff can still produce a non-match, so keep a text fallback (rules 2 and 6).

### What is a good layout shift score for a chat window?
web.dev rates 0.1 or less as good for web pages at the 75th percentile. I found no source for chat windows, so treat 0.1 as a starting point (section 7).

### Should the model decide which component to show?
It can pick from a short approved list. It should not invent components, and the same task should map to the same one (rules 1 and 5).

### Does a better model fix generative UI problems?
Partly. It fills fields more reliably, but reserving space, validating and falling back are UI work (section 3; our judgment, not tested).
