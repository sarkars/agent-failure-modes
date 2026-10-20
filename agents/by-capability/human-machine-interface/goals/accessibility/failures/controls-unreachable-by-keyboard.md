# Chatbot Widget Not Keyboard Accessible: Controls Unreachable by Keyboard

<!-- SEO
title: Chatbot Widget Not Keyboard Accessible: Fix Tab and Focus
description: Chat buttons, chips, copy, and stop can't be reached with Tab. See why it happens, the WCAG rules that apply, and a fix you can test.
search phrases:
- chatbot widget keyboard accessible
- chat widget can't tab to buttons
- chat widget focus trap
- chat widget focus lost after clicking button
- how to make a chatbot keyboard accessible
- chat widget close button not reachable with keyboard
- chatbot suggested reply buttons not focusable
- chat widget no visible focus indicator
-->

**Frequency**: Common

## Issue: Chat buttons, chips, copy, stop, and feedback controls can't be reached with Tab, or lose focus when used, so keyboard-only users can't finish a conversation.

> **One line:** If a person can't use a mouse, parts of the chat simply aren't there for them.

| | |
|---|---|
| **Channel** | Chat (web chat widget) is written here. Voice is planned; nothing here covers it. |
| **Stakes** | Any. Higher when the chat is the only route to a refill, a claim, or a cancellation. |
| **Who is affected** | People who use a keyboard, switch device, or screen reader instead of a mouse, and anyone whose mouse fails. |
| **Frequency** | Common, our judgment. Public audits and accessibility statements report it (section 4); I found no count for chat widgets. |
| **Pattern ID** | controls-unreachable-by-keyboard |
| **Family** | [Accessibility](../README.md) |
| **Goal** | People who use screen readers, keyboards, captions, relay services, or plain-language support can use every part of the agent. |
| **Primary metric** | Keyboard-only task completion in testing. Target: 100% (starting point). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Tab order, focus, and button markup come from the widget code, not from the model. (Our judgment, not tested.) |
| **Also searched as** | chat widget keyboard navigation · chatbot tab order · chat widget focus trap · focus lost after clicking chat button · chatbot WCAG 2.1.1 · keyboard accessible chat |

This page is design guidance, not a conformance claim and not legal advice. Passing the tests below does not make a product WCAG-conformant.

## 1. In plain words
The chat looks fine to a mouse user. A keyboard user presses Tab and skips the suggestion chips, the copy button, the stop button, and the thumbs. Or they press one and focus jumps to the top of the page. Or the focus ring is invisible and they can't tell where they are. The fix: every control is a real button, reachable in a sensible order, with a visible focus mark, and focus never disappears or gets trapped.

## 2. What it looks like
**Without the fix** (pharmacy chat widget, keyboard-only user, Tab and Enter only)
```
User: (Tab through the page; the chat launcher is a clickable <div>, so Tab skips it)
User: (finds the panel only through a screen-reader shortcut and opens it)
Bot:  Hi! Refill, transfer, or store hours? [Refill] [Transfer] [Hours]
User: (Tab: focus goes to the page footer behind the panel; the chips are not in the tab order)
User: (types "refill" and presses Enter)
Bot:  Which prescription? [Stop] [Copy] [thumbs up] [thumbs down]
User: (Tab: no visible focus; presses Enter on an unseen button; focus drops to the top of the page)
```
**With the fix**
```
User: (Tab to "Chat with us", focus ring visible; presses Enter)
Bot:  (focus moves to the message box) Hi! I can help with refills, transfers, or hours.
      [Refill] [Transfer] [Hours] [Something else]  Or type below.
User: (Tab to [Refill], focus ring visible; presses Enter)
Bot:  (focus moves to the start of the reply, announced once) Which prescription? Type the name, or pick one.
User: (presses Esc) The panel closes. Focus returns to "Chat with us".
```
The fixed widget can be opened, used, and closed with the keyboard alone, and the user always knows where focus is.

## 3. Why it happens
These are our reading of the pattern.
- **Controls built from non-buttons.** Chips, launchers, and icon buttons are `<div>` or `<span>` with click handlers, so they have no focus stop and no Enter or Space behavior.
- **Controls that remove themselves.** A button disables or disappears on press (chips after a choice, thumbs after a vote, Stop when the reply ends), so focus falls back to the page. Milly Software reported exactly this in its own widget (section 4).
- **Overlay with no focus plan.** A closed panel stays in the tab order, or an open panel lets Tab wander to the page behind it, and nobody decided where focus goes on open and close.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| SC 2.1.1 Keyboard is Level A: content must be operable through a keyboard interface. The only exception is input that depends on the path of movement, such as freehand drawing. | [W3C, *Understanding SC 2.1.1*](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html). Opened and read. | A standard, not a measure of how often chat widgets fail. |
| SC 2.4.7 Focus Visible is Level AA: "Any keyboard operable user interface has a mode of operation where the keyboard focus indicator is visible." | [W3C, *Understanding SC 2.4.7*](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html). Opened and read. | Same. |
| SC 2.1.2 No Keyboard Trap is Level A: focus must be movable away using only a keyboard. Restricting focus (a modal dialog) is acceptable if the user knows how to leave. | [W3C, *Understanding SC 2.1.2*](https://www.w3.org/WAI/WCAG22/Understanding/no-keyboard-trap.html). Opened and read. | Same. |
| SC 2.4.11 Focus Not Obscured (Minimum), Level AA: a focused component must not be "entirely hidden due to author-created content". W3C names chatbots and a chat popover non-modal dialog as risks. | [W3C, *Understanding SC 2.4.11*](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html). Opened and read. | Partly covered is allowed at AA. |
| In one vendor's own audit of its Shopify chat widget (13 shopper-facing defects, Aug. 2026): buttons that disabled on press dropped focus to the page top, about 37 Tab presses to return, in 4 places; the thumbs vote left the tab order and the author counted past 120 presses without reaching it; a closed panel left 7 invisible tab stops; 6 controls stayed reachable under a non-modal quiz. | [Milly Software, *Making a Shopify Chat Widget Actually Usable With a Keyboard and a Screen Reader*](https://www.millysoftware.com/writing/accessible-shopify-chat-widget-keyboard-screen-reader). Opened and read. | Vendor self-report about one product, single source. Shows the failure types, not how common they are. |
| AudioEye's rule says that when the close control in a chat window is used, keyboard focus "should return to the chat widget activation button which originally opened the chat window". | [AudioEye, *Manual_ModalRefocus_Missing*](https://developer.audioeye.com/rules/Manual_ModalRefocus_Missing). Opened and read. | Vendor test rule, not a WCAG requirement. |
| Biel's chat docs describe a modal chat that keeps focus inside while open, closes on Escape, and returns focus to the opener; its inline mode does not trap focus or respond to Escape. | [Biel docs, *Accessibility*](https://docs.biel.ai/customization/accessibility). Opened and read. | One vendor's design choice, not a standard. |

I used no percentage about keyboard failures from the search summaries, because I could not open a primary source for them. A search summary said the WebAIM Million is automated and does not test keyboard operability directly; I did not open it, so I make no claim from it.

**Public incident.** No public incident found. Searches run: "chat widget keyboard accessibility focus management open close focus returns to launcher"; "chatbot widget not keyboard accessible WebAIM Million buttons without keyboard"; "WCAG focus appearance 2.4.11 focus not obscured live chat widget covers focus". They returned vendor docs, an accessibility statement, and forum threads, not a dated incident. A Zendesk community thread about missing focus on its chat widget turned up in search, but the page returned 404 when I tried to open it, so I do not rely on it.

## 5. The fix
**The principle:** Every control in the chat is a real button, reachable and visibly focused, and focus always lands somewhere sensible.

**Do this**
1. **Use native controls.** Launcher, chips, send, stop, copy, thumbs, and close are `<button>` elements (or have an equivalent role) and respond to Enter and Space. Test: Tab reaches each one in a logical order (SC 2.1.1).
2. **Show focus on every control.** A visible focus mark on each, at normal and 200% zoom, in light and dark themes (SC 2.4.7). Test: screenshot each control while focused.
3. **Keep focus out of hiding.** A focused control is never entirely behind the widget, a sticky bar, or a banner (SC 2.4.11). Test: Tab through the host page with the widget closed and open.
4. **On open, move focus in. On close, move it back.** Open puts focus in the message box (or the panel heading). Close (button or Esc) returns focus to the launcher.
5. **Closed means out of the tab order.** A closed or hidden panel has zero focusable controls (use `hidden` or `inert`).
6. **No traps, and say how to leave.** If the open panel holds focus, Esc closes it and the hint is visible. An inline chat does not trap (SC 2.1.2).
7. **Never drop focus when a control changes.** If a control disables, hides, or is replaced, focus moves to the next logical control, never to the page top. Prefer `aria-disabled` plus a text confirmation over removing the control (a thumbs vote says "Thanks" and stays reachable).
8. **Don't steal focus for new messages.** A new bot reply is announced to assistive tech, not focused. Exception: after the user activates a chip, focus goes to the start of the reply it produced.
9. **Chips never replace typing.** Offered chips are 2-4 options plus "Something else", and the message box stays open and reachable.

**Reference design**
| Moment | Focus goes to | Announced |
|---|---|---|
| Launcher activated | Message box | Name of the chat dialog or region |
| Chip activated | Start of the reply it produced | Reply text, once |
| Stop activated | Message box | "Stopped" |
| Copy activated | Stays on Copy | "Copied" |
| Thumbs activated | Stays on the thumb, now marked chosen | "Thanks for the feedback" |
| Esc or Close | Launcher | Panel closed |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md))
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | Chips are reachable and operable by keyboard like any button. Do not offer chips when the next step is one obvious action or when the options would hide the message box. |
| Hand off to a person | A user says they can't reach or press something. Offer a phone number, email, or callback in the same message. Do not hand off if they asked to stay in chat and the control now works. |

**Don't over-correct.** Don't give every chip its own custom shortcut key (it clashes with screen readers and host pages). Don't trap focus in an inline chat. Don't announce every streamed token; announce a finished reply. Don't add a separate "keyboard mode" that hides features: one UI must work for everyone.

**Hand-off rule.** If a keyboard user reports they can't reach a control, or the same control fails twice in testing, give them a non-widget route (phone, email, or callback) and log the broken control id.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** Manual, with the mouse unplugged, plus a screen reader pass.

| # | Scenario (rule) | Pass if |
|---|---|---|
| 1 | Complete a refill with Tab, Shift+Tab, Enter, Space, Esc only (1) | The task finishes with no mouse |
| 2 | Tab through all controls at 200% zoom (2, 3) | Each shows a visible focus mark, none fully hidden |
| 3 | Open and close the panel (4, 5) | Focus enters the message box, returns to the launcher; closed panel has 0 tab stops |
| 4 | Open the panel, press Tab 30 times, press Esc (6) | Focus never lands on the page behind; Esc closes it |
| 5 | Activate a chip, Stop, Copy, and a thumb in turn (7) | Focus is never on `body`; Copy and the thumb stay reachable |
| 6 | Receive a bot reply while typing (8) | Focus stays in the box; the reply is announced |
| 7 | Read the chip set (9) | 2-4 chips plus "Something else"; message box reachable |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Keyboard-only task completion** (primary) | 100% | Scripted tasks in each release, mouse disabled, pass or fail per task | Any failure |
| Controls with a visible focus mark | 100% | Count controls in the focus-screenshot test (test 2) | Below 100% |
| Tab stops while the panel is closed | 0 | Automated check on page load: count focusable elements inside the closed widget | Any |
| Focus lost to `body` after a control is activated | 0 per test run | Test 5; in production, the proposed client event below | Any |
| Tab presses from reply to message box | Track; set from baseline | Count in test runs | Rising across releases |
| Keyboard-reported problems (sampled) | Track | Tag support contacts that mention Tab, keyboard, or "can't click" | Any in two weeks |

### Detection signals (proposed, not yet calibrated)
A server log cannot see focus order, tab stops, or focus rings. Manual testing (section 6) is the primary check. A client could record the events below (proposed, not built). All are for the text-chat widget; voice signals are planned only and not defined. Log element ids and roles, never message text.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Focus lands on `body` right after a widget control is activated | Client event `focus_lost` (proposed) with control id | The user clicked outside the widget on purpose |
| Many Tab presses between a bot reply and the next focus in the message box | Client event with keydown count (proposed) | A long reply with many links the user is reading |
| Focusable elements exist in the closed widget | Client check at page load (proposed) | A visible "skip chat" link that is meant to be focusable |
| Support contact tagged "keyboard" or "can't click" | Sampled contact review (text chat) | A mouse or touch problem, not a keyboard one |
| A control is never activated by keyboard across many sessions | Client field `activation_source` (proposed) | Few keyboard users in that audience |

**Starter rule:** every chat control is a native button that Tab reaches in order, shows focus, and never drops focus when used.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: controls-unreachable-by-keyboard
runs: post_turn
reads: [client_event.focus_lost, client_event.activation_source, widget.closed_tab_stops, widget.control_ids]
trigger: a chip is shown, or a user reports a control they cannot reach
moves: [offer_choices, hand_off]
choices: ["Refill", "Transfer", "Store hours", "Something else"]
on_miss: log
metric: keyboard-only task completion in testing
counter_metric: tab presses from reply to message box
status: proposed
```

## 8. Related patterns
- [Accessibility gaps (VI-04, queued, page not yet written)](../../../roadmap/visual-and-oversight.md): accessibility problems in general (contrast, text alternatives, screen readers). This page covers only keyboard reach and focus in the chat widget.
- [Generic error messages](../../errors-and-recovery/failures/generic-error-messages.md): a failed send must also keep focus and the typed text; that page covers the wording.

## 9. Common questions
### How do I make a chatbot widget keyboard accessible?
Use native buttons, keep a logical tab order, show focus, and decide where focus goes on open, on close, and after each control is used (section 5). Test with the mouse unplugged.

### Should a chat widget trap focus?
Only a modal overlay holds focus, and then Esc must close it (SC 2.1.2 allows restricting focus if the user knows how to leave). An inline chat should not trap focus. Biel's docs describe both modes.

### Where should focus go when the chat closes?
Back to the button that opened it. AudioEye's rule says the same.

### Does my chat widget need to pass WCAG?
This page doesn't answer that, and it is not legal advice. The criteria it uses (2.1.1, 2.1.2, 2.4.7, 2.4.11) come from WCAG 2.2; ask your counsel or accessibility lead which standard binds your product.
