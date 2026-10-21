# Chatbot Accessibility Problems: Poor Contrast, Missing Alt Text, Accessibility Gaps

<!-- SEO
title: Chatbot Accessibility Problems: Contrast, Alt Text, Focus
description: Chat widgets and cards often fail WCAG 2.2 AA on contrast, text alternatives and focus. A visual-layer checklist with pass/fail rules you can test.
search phrases:
- chatbot widget accessibility wcag 2.2
- chatbot color contrast accessibility
- chatbot alt text for images and charts
- chat widget focus indicator not visible
- chatbot rich cards screen reader
- how to test chatbot accessibility
- chat bubble text contrast ratio
- generated image alt text chatbot
-->

**Frequency**: Common

## Issue: The chat widget, rich cards and generated visuals ship with low contrast, no text alternatives, and no visible focus or screen-reader announcements, so critical flows fail WCAG 2.2 AA; the fix is a conformance check on the visual layer of each critical flow.

> **One line:** The chat looks fine to the team, but gray-on-white text, an unlabeled chart and an invisible focus ring make the payment or claim flow unusable for people with low vision or a screen reader.

> **Read this first.** This page is design guidance for testing your own product. It is not legal, clinical, or professional advice, and it has not been reviewed by an accessibility specialist or a lawyer. Have one review it before you rely on it. I cite the W3C's WCAG 2.2 success criteria and one web-scale survey only as sources I opened. I opened no statute, regulation, or case, so I make no claim about which laws (for example the ADA) apply to your product or what they require.

| | |
|---|---|
| **Channel** | Written for **chat** (text widget, rich cards, buttons, images and charts the assistant shows). Voice and web-analytics checks are PLANNED, not written. |
| **Stakes** | Any. High when the flow is a bill, claim, refill or account change. |
| **Who is affected** | People with low vision or color blindness, screen-reader and keyboard users, and anyone using the widget in bright light on a phone |
| **Frequency** | Common, our judgment. A web-wide survey found low-contrast text on most home pages (section 4); I found no count for chat widgets. |
| **Pattern ID** | accessibility-gaps |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. Here: critical flows meet WCAG 2.2 AA. |
| **Primary metric** | Automated plus manual WCAG 2.2 AA pass rate on critical flows. Starting target: 100% (a starting point; tune it). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Colors, alt text, focus order and live regions come from the widget code and card templates, not from the model's words. A better model can still render gray text on a white bubble. (Our judgment, not tested.) |
| **Also searched as** | chatbot not accessible · chat widget low contrast · chatbot image has no alt text · chatbot screen reader can't read cards · WCAG chatbot · chat focus ring missing |

## 1. In plain words
The assistant's window, buttons, cards and pictures have to be readable and usable by people who see poorly, cannot use a mouse, or use a screen reader. In practice, light-gray text, charts with no description, and buttons you cannot see focus on are the usual breaks. The fix is to check the visual layer of each critical flow against WCAG 2.2 AA, by tool and by hand, and fail the release if it does not pass.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Northfield Pharmacy" assistant)
```
User: (keyboard and screen reader) Refill my lisinopril.
Bot:  [card] Refill ready for pickup Friday.   (hint text #9AA0A6 on white; the status icon is color only)
      [chart image: "Your pickups this year"]  (no alt text; screen reader says "image")
      [Confirm pickup]  (Tab skips it; no focus ring when it is reached)
Screen reader: "image ... graphic ... clickable"
User: Is it confirmed?
```
**With the fix**
```
User: (keyboard and screen reader) Refill my lisinopril.
Bot:  [card] Refill ready for pickup Friday, 9 am to 6 pm.   (text 4.5:1 or better; "Ready" shown as text, not color)
      [chart, alt: "Pickups per month, 2 to 4 each month; table below"] [Show as table]
      [Confirm pickup]  (Tab reaches it; 3:1 focus ring; announced as a button)
Screen reader: "Refill ready for pickup Friday. Confirm pickup, button."
User: (presses Enter)
Bot:  Confirmed: pickup Friday. (announced without moving focus)
```
The fixed version keeps the same content but makes every part perceivable: readable contrast, meaning in text and not color alone, a text alternative for the chart, a reachable and visible control, and an announced result.

## 3. Why it happens
- **Brand colors are chosen once, for the page.** A widget inherits a light gray for hints, timestamps and disabled-looking links. Nobody checks the ratio on the chat bubble background.
- **Generated and card content has no alt-text field.** The model returns an image or chart spec, the template renders it, and no step requires a text equivalent.
- **Tests run on the widget shell, not on the flow.** An automated scan passes the empty chat window and never sees the card, the confirm step or the error state where the problems are.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WebAIM's 2026 survey of the top 1,000,000 home pages reports "95.9% of home pages had detected WCAG 2 failures", with low-contrast text on 83.9% of pages and 16.2% of images missing alternative text, an average of 56.1 detected errors per page. | [WebAIM Million](https://webaim.org/projects/million/). Opened and read (raw page text). | Home pages, not chat widgets. Detected by one automated tool (WAVE) only. |
| The same report says "All automated tools, including WAVE, have limitations" and "Absence of detected errors does not indicate that a page is accessible or conformant." | Same WebAIM page. | This is why the metric needs a manual part, not only a scan. |
| WCAG 2.2 SC 1.4.3 (Level AA) requires text and images of text "a contrast ratio of at least 4.5:1", and 3:1 for large-scale text. | [W3C, Understanding 1.4.3](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html). Opened and read. | A standard, not a measured result. Inactive components and pure decoration are exempt. |
| SC 1.4.11 (Level AA) requires 3:1 "against adjacent color(s)" for visual information needed to identify controls and their states, including focus, and for graphics needed to understand content. Values are not rounded: 2.999:1 fails. | [W3C, Understanding 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). Opened and read. | Exceptions exist (disabled controls, browser default styling). |
| SC 1.1.1 (Level A) says non-text content "has a text alternative that serves the equivalent purpose"; pure decoration is implemented so assistive technology can ignore it. | [W3C, Understanding 1.1.1](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html). Opened and read for the quoted text. The chart-description detail was read through a fetch summary and is kept out of the rules. | Standard text. |
| SC 4.1.3 (Level AA) requires that status messages "can be programmatically determined through role or properties" so assistive technology can present them "without receiving focus". SC 2.1.1 (Level A) requires keyboard operability. SC 2.4.7 (Level AA) requires a visible keyboard focus indicator. | W3C Understanding pages for [4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html), [2.1.1](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html), [2.4.7](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html). Opened and read for the first lines. | Standard text. |
| Orange's accessibility guidelines for chatbots say to use a real `<button>` to open the chat, because a `<span>` look-alike is not focusable by Tab and a keyboard user could not open the chatbot. | [Orange, Best practices for a chatbot](https://a11y-guidelines.orange.com/en/articles/chatbot/). Opened and read (first part). | One company's guidance, not a standard. |

**How this differs from the closest pages.** This page is the visual-layer conformance check of the chat UI: contrast, text alternatives, focus appearance and announcements, scored as one pass rate on critical flows. [Accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md) is the chat-wide test plan for whole journeys with real assistive-technology users, including zoom, speech input and reading level. [Controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md) is the deep page on Tab order and focus traps; here keyboard is one row of the check. [No accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md) covers "thinking" and "done" announcements. [Cognitive overload](cognitive-overload.md) is about too much on screen, not whether it is perceivable.

**Public incident.** I found no public incident of a chat assistant failing only through contrast or alt text, and I did not search court records.

## 5. The fix

**The principle:** Every critical flow in the chat passes a WCAG 2.2 AA check at the visual layer, by automated scan and by hand, before release and after each template change.

**Do this**
1. **List the critical flows and check each state.** Name 3 to 5 flows (for example refill, pay a bill, file a claim). For each, test the widget closed, open, a card, a button, an error, and the done state, not only the empty window.
2. **Text meets contrast.** Body text in bubbles, cards, hints and timestamps is 4.5:1 or better against its actual background (3:1 for large text). Check in light and dark themes.
3. **Controls and states meet 3:1.** Button borders or fills, selected chips, input outlines and the focus ring are 3:1 against adjacent colors. Never round: 2.999:1 fails.
4. **No meaning by color alone.** Status such as "Ready", "Failed" or a price change also appears as words.
5. **Every image, chart and generated visual has a text alternative.** A short alt text that states the point, plus the data or a "Show as table" option when the point needs detail. Decoration is marked so a screen reader skips it. A generated image the model cannot describe is not shown in a critical flow.
6. **Every control is a real, labeled, focusable control with a visible focus ring.** Native `<button>` and `<input>`, a label that says the result, and the ring is never removed. Details live in [controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md).
7. **New replies and results are announced without moving focus.** A live region (or equivalent role) announces the bot's message and the result of an action ([status messages, 4.1.3](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)). Streaming behavior is in [the accessibility family](../../accessibility/README.md).
8. **Gate the release.** A critical-flow pass rate under 100% blocks it, or ships with a named exception owner and date.

**Reference design: visual-layer check per flow state**
| State | Automated scan | Manual check |
|---|---|---|
| Widget open | Contrast, labels, roles | Tab order; open and close with keyboard; focus returns to the launcher |
| Reply with a card | Contrast of text and borders, alt present | Screen reader reads the card in order; meaning not by color |
| Image or chart | Alt present | Alt states the point; table or text version exists |
| Button press and result | Focus ring ratio | Result announced; focus not lost |
| Error | Contrast of error text | Error announced and says what to do next |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | State the result as text first; the card or chart supports it, so a user who cannot see it still has the answer |
| Offer choices | A visual cannot be described well: offer "Read it as text", "Show as table", "Something else", free text open |
| Admit uncertainty and show how to check | A generated visual has no reliable description: say so and give the data or a text answer |
| Hand off to a person | The user says the display is unusable or asks for another channel: offer a person or the phone, with a one-line summary |

**Don't over-correct.** Do not strip cards, charts and color from the chat to pass a scan. An accessible card keeps its visuals and adds text. Do not stuff alt text with long descriptions on every decorative image, or announce every small update; announce only what the user needs. A passing scan is not conformance: the WebAIM page above says so.

**Hand-off rule.** When a user reports they cannot read or operate a card, or two attempts at the same control fail, stop sending that visual and give the answer as plain text, then offer a person ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** the W3C WCAG 2.2 success criteria listed in section 4. Rules 2 to 5 map to 1.4.3, 1.4.11, 1.1.1; rule 6 to 2.1.1 and 2.4.7; rule 7 to 4.1.3.

## 6. How to test it (short version)
No test file yet. The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Run an automated scan on each state of each critical flow | Zero contrast, label and alt errors; findings logged | 1, 2 |
| 2 | Measure text and hint colors on bubble and card backgrounds, light and dark | Every pair 4.5:1 (3:1 large) | 2 |
| 3 | Measure button, chip, input and focus-ring colors against neighbors | Every pair 3:1, unrounded | 3 |
| 4 | Look at a status card in grayscale | The status is still readable as words | 4 |
| 5 | Show an image and a chart; read them with a screen reader | Alt states the point; a table or text version exists; decoration skipped | 5 |
| 6 | Complete the flow with Tab, Shift+Tab and Enter only | Every control reached, ring visible, focus returns after close | 6 |
| 7 | Press a button with a screen reader running | The bot's reply and the result are announced without focus moving | 7 |
| 8 | Ship a template change that lowers a pass rate | The release is blocked or has a named exception | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Automated plus manual WCAG 2.2 AA pass rate on critical flows** (primary) | 100% (starting point) | Per release, for each flow state: scan result and manual checklist; passing states divided by tested states | Any state failing |
| Rendered replies with a contrast failure | 0 (starting point) | Run the contrast check on a sample of rendered cards and bubbles per release | Any |
| Images and charts shown with a text alternative | 100% | Log each rendered visual with an `alt` field; count empty `alt` that are not marked decorative | Below 100% |
| Controls with a visible focus ring and a label | 100% | Scan every control in each state | Any miss |
| Visual-related complaints (counter-metric) | Track; do not chase | Count user messages like "can't read", "can't see", "image" after a card | Rising after a fix: the fix may have hidden content |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat** text and render events only; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A rendered visual has an empty `alt` and is not tagged decorative (rule 5) | `message.visual.alt` empty, `decorative` false | A spacer or icon the template marks decorative |
| A card text/background pair is under 4.5:1 (rule 2) | Contrast check on the rendered theme token pair | A disabled control, which is exempt |
| A control has no label or is a non-native element without a role (rule 6) | Render audit of the control's `role` and `name` | A native element whose name comes from the nearby text |
| The user's next turn after a card says "can't read" or "what does it say" (rules 2, 5) | Short user turn after a card render | A user asking for a translation or summary |
| The user repeats a request right after a card with no reply to it (rule 7) | Same intent in the next user turn; no click event on the card | A user who changed their mind |

**Starter rule:** every card, button and visual in a critical flow has readable contrast, a text alternative, a visible focus state and an announced result, and the release fails if any state does not.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: accessibility-gaps
runs: pre_send
reads: [message.type, message.visual.alt, message.visual.decorative, control.role, control.name, theme.contrast_pairs, flow.id]
trigger: a reply with a card, button or visual is about to be sent in a critical flow
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Read it as text", "Show as table", "Something else", "Talk to a person"]
on_miss: rewrite
metric: automated plus manual WCAG 2.2 AA pass rate on critical flows
counter_metric: visual-related complaints
status: proposed
```

## 8. Related patterns
- [Accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md): the chat-wide, user-tested plan; this page is the visual-layer conformance check.
- [Controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md): Tab order, focus traps and focus loss in depth.
- [No accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md): announcing thinking and done states.
- [Streaming text read out token by token](../../accessibility/failures/streaming-text-read-out-token-by-token.md): announcements while a reply streams.
- [Cognitive overload](cognitive-overload.md): too much on screen, not whether it is perceivable.
- [No clear primary action](no-clear-primary-action.md): which button leads; this page checks that every button can be seen and used.

## 9. Common questions
### What contrast ratio does a chatbot need to meet WCAG AA?
Text needs at least 4.5:1 against its background, or 3:1 for large-scale text (SC 1.4.3). Controls, their states and the focus ring need 3:1 against adjacent colors (SC 1.4.11). Check the real bubble and card backgrounds in each theme (rules 2 and 3).

### Does a chatbot image need alt text?
If it carries information, yes: SC 1.1.1 asks for a text alternative that serves the equivalent purpose. Decoration should be marked so assistive technology skips it. For a chart, give the point in a short alt and offer the data as text or a table (rule 5).

### Is passing an automated scan enough?
No. The WebAIM page says automated tools cannot detect every failure and that no detected errors does not mean a page is conformant. That is why the metric combines a scan with a manual check of each flow state.

### Is this the same as the keyboard accessibility page?
No. [Controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md) goes deep on Tab, focus traps and focus loss. This page checks the visual layer of the whole flow, with keyboard as one row.

### Does this make my chatbot legally compliant?
This page does not say. I opened no law or regulation, so I make no claim about what any law requires. Treat the checks as testable design rules and ask a qualified reviewer about legal duties.
