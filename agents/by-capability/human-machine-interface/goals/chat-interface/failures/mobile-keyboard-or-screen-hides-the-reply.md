# Chatbot Answer Hidden by the Phone Keyboard: Mobile Keyboard or Screen Hides the Reply

<!-- SEO
title: Chatbot Reply Hidden by Phone Keyboard: Fix Mobile Layout
description: On a phone, the keyboard or input bar covers the chatbot's answer, or text is cut off. Keep the latest reply visible and test on real small screens.
search phrases:
- chat input covered by keyboard mobile
- chatbot reply hidden behind keyboard
- chat widget keyboard covers messages ios
- fixed chat input jumps when keyboard opens android
- chat window cut off on small phone screen
- viewport height 100vh keyboard chat
- interactive-widget resizes-content chat
- chat widget not readable landscape mobile
-->

**Frequency**: Common

## Issue: On a phone, the on-screen keyboard or the input bar covers the bot's latest answer, or text and buttons are cut off on a small screen, so the person cannot read the answer they asked for.

> **One line:** The bot answered, but the phone's keyboard, the input bar, or a small or zoomed screen hides the answer; the fix is to test the chat window on real devices and small viewports (keyboard open, landscape, larger text) and keep the latest reply fully visible.

| | |
|---|---|
| **Channel** | Written for **chat** (web chat windows and widgets on phones). Native-app behavior and voice are PLANNED, not written. |
| **Stakes** | Low to medium. Usually a retry; higher when the hidden part is a warning, a price, or a confirmation. |
| **Who is affected** | People chatting on phones, most of all on small screens, in landscape, with enlarged text, or with the keyboard open |
| **Frequency** | Common. The browser behavior behind it differs by browser and is documented (section 4). I found no count of how many chat products have this defect. |
| **Pattern ID** | mobile-keyboard-or-screen-hides-the-reply |
| **Family** | [Chat interface](../README.md) |
| **Goal** | The chat window itself works: messages arrive, drafts and attachments are kept, history is findable, and nothing is silently lost. |
| **Primary metric** | Layout defects per device in release testing. Starting point: 0 open defects on every device and viewport in the test matrix (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model's text is fine; the page layout decides what the person can see. (Our judgment, not tested.) |
| **Also searched as** | keyboard covers chat input · chat box hidden behind keyboard · chat widget cut off on phone · can't see the bot's answer on mobile · 100vh keyboard bug · chat input jumps on iPhone |

## 1. In plain words
On a phone, the keyboard takes about half the screen. Depending on the browser, the page either shrinks to fit above it or the keyboard slides over the page. If the chat window was built assuming the first and the browser does the second, the input bar or the newest reply ends up behind the keyboard. Small screens, landscape mode, and larger text sizes cut off more.

## 2. What it looks like
A traveler on an iPhone SE asks an airline's chat widget whether she can change a flight to Denver without a fee. She taps the box, the keyboard opens, and she types her question.

**Without the fix**
```
Screen with keyboard open (visible area ~ 3 lines):
  You: Can I change my Denver flight for free?
  Bot: Yes, within 24 hours of booking. After that a $75 fee applies unless the fare is Basic Economy.
  [Type a message  ] [Send]    <- input bar sits on top of the answer
  [ keyboard ]                      <- the rest of the answer is behind it
She sees "$75 fee" but not the end of the sentence, scrolls the page, and the whole widget moves off-screen.
```
**With the fix**
```
Screen with keyboard open: the message list shrinks above the keyboard and scrolls to the newest reply.
  Bot: Yes, within 24 hours of booking. After that a $75 fee applies unless the fare is Basic Economy.
  [Type a message  ] [Send]    <- sits directly above the keyboard, nothing overlaps
She can scroll the list; "Jump to latest" appears if she has moved up.
```
The fixed version resizes the message list to the space above the keyboard, keeps the newest reply in view, and does not overlap the input bar.

## 3. Why it happens
- **Browsers handle the keyboard differently, and the default can change.** The keyboard may shrink only the visual viewport, shrink both viewports, or overlay the page (section 4). A layout tested on one behavior breaks on another.
- **Fixed positioning and viewport-relative heights assume a stable screen.** An input pinned to the bottom, or a window sized to the full viewport height, can be obscured or moved when the keyboard opens.
- **Testing happens on a desktop browser.** A narrowed desktop window does not open a keyboard, does not change the visual viewport, and does not show landscape plus enlarged text together.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Since Chrome 108, Chrome on Android resizes only the Visual Viewport when the keyboard opens, unless the page sets `interactive-widget`. Values: `resizes-visual` ("Resize only the Visual Viewport but not the Layout Viewport"), `resizes-content` ("Resize both the Visual Viewport and Layout Viewport"), `overlays-content` ("Do not resize any viewport"). Default: `resizes-visual`. The article warns that "elements that use `position: fixed` remain in place and can be obscured by the OSK." | [Chrome for Developers, *Prepare for viewport resize behavior changes coming to Chrome on Android*](https://developer.chrome.com/blog/viewport-resize-behavior). Opened 2026-10-20. | Vendor documentation. Covers Chrome on Android; other browsers may differ (see MDN row and the unverified note below). |
| "User-interface features like the on-screen keyboard (OSK) can shrink the visual viewport without affecting the layout viewport." The `resize` event fires when the visual viewport is resized. | [MDN, *Visual Viewport API*](https://developer.mozilla.org/en-US/docs/Web/API/Visual_Viewport_API). Opened 2026-10-20. | Reference documentation. It does not say which browsers do this for the keyboard. |
| WCAG 2.2 SC 1.4.10 Reflow (Level AA): content can be presented "without loss of information or functionality, and without requiring scrolling in two dimensions" at a width equivalent to 320 CSS pixels for vertically scrolling content. "320 CSS pixels is equivalent to a starting viewport width of 1280 CSS pixels wide at 400% zoom." | [W3C, *Understanding SC 1.4.10 Reflow*](https://www.w3.org/WAI/WCAG22/Understanding/reflow). Opened 2026-10-20. | A standard, not a measure of how often chats fail it. Exceptions apply to content that needs two-dimensional layout (maps, data tables). |
| SC 1.4.4 Resize Text: text can be resized "without assistive technology up to 200 percent" and "without loss of content or functionality." | [W3C, *Understanding SC 1.4.4 Resize Text*](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html). Opened 2026-10-20; I read only an extract of the criterion text. | Same as above. Excerpt only; check the page for exceptions. |
| One 2022 Chromium proposal says Firefox for Android and Chrome for Android resized the layout viewport for the keyboard while Safari on iOS did not. | [Chromium blink-dev thread](https://groups.google.com/a/chromium.org/g/blink-dev/c/ge7xTu-VhJ0/m/hq_kcusHAQAJ). **Not opened**; read only through a search summary. | Unverified. The fix does not rely on it; it is why the tests cover real devices. |

**Public incident.** None found. I found no study counting hidden-reply defects in chat products.

## 5. The fix
**The principle:** Whatever the keyboard, orientation, or text size, the newest reply and the input bar are both fully visible and nothing overlaps.

**Do this**
1. **Size the chat window to the visible area.** Choose the viewport behavior on purpose: set `interactive-widget` in the viewport meta tag (for example `resizes-content`), or follow the visual viewport and its `resize` event, so the message list shrinks above the keyboard.
2. **Never overlap the reply with the input bar.** The message list ends where the input bar begins, including the area under a notch or home bar.
3. **Scroll to the newest reply after the keyboard opens**, but only if the person was already at the bottom (see [auto-scroll fights the reader](auto-scroll-fights-the-reader.md)).
4. **Reflow, don't clip.** At a 320 CSS pixel width and at 200 percent text size, no text, button, or quick-reply chip is cut off, and nothing needs horizontal scrolling.
5. **Test the matrix before release.** At least one small iPhone, one mid-size Android phone, and one tablet, each with keyboard open, landscape, and enlarged text.
6. **Make the failure recoverable.** If the newest reply is not fully visible, show "Jump to latest" or "Show full reply", not silence.

**Reference design: release test matrix (starting point)**
```
Devices:   small iPhone, mid-size Android phone, tablet (real devices where possible)
States:    portrait / landscape x keyboard closed / open x text 100% / 200%
Check:     last bot message fully visible; input bar visible; no overlap; no horizontal scroll;
           quick-reply buttons reachable; send works with keyboard open
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); this fix is mostly a layout change, so few moves apply)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Keep the key fact in the first line so the visible part holds it even if the rest is cut off. |
| Offer choices: 2-4 options plus "Something else", free text open | Only when the reply cannot be shown in full: "Show full reply", "Send it to my email", "Something else". Not as a replacement for fixing the layout. |
| Hand off to a person | The person reports the chat is unreadable on their device and the layout cannot be fixed in session. |

**Don't over-correct.** Do not lock the page so it cannot scroll or zoom to avoid the issue, since that breaks Reflow and Resize Text. Do not shorten replies to fit a small screen at the cost of the answer.

**Hand-off rule.** If a person says they cannot read the reply on their phone and "Show full reply" does not work, offer a person or another channel (email or a web link), and pass the conversation id and device and browser details.

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Small phone, portrait, keyboard open, send a message and receive a long reply | The newest reply and input bar are both visible with no overlap | 1, 2 |
| 2 | Same, in landscape | Newest reply readable by scrolling the list; input bar visible | 1, 2, 5 |
| 3 | Text at 200 percent, 320 CSS pixel width | No clipped text or buttons; no horizontal scrolling | 4 |
| 4 | Person scrolled up, keyboard opens | View does not jump; "Jump to latest" is offered | 3, 6 |
| 5 | Quick-reply buttons at narrow width with keyboard open | All buttons reachable and tappable | 4, 5 |
| 6 | Desktop browser, normal window | Layout unchanged; no extra "Show full reply" prompts | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Layout defects per device in release testing** (primary) | 0 open on each device in the matrix (starting point) | Test run log: one row per device, state, and defect | Any open defect at release |
| Matrix coverage | 100% of the listed devices and states run each release | Test run log | Below 100% |
| Reports of hidden or cut-off replies | Track; set from baseline | Tagged support tickets and feedback comments | Rising two weeks in a row |
| "Show full reply" taps per 1,000 mobile replies | Track; set from baseline | UI event count | Rising |
| Reflow failures in automated check at 320 CSS pixels | 0 | Automated or manual check on the chat page | Any |
| Extra prompts on desktop (counter-metric) | Track; set from baseline | "Show full reply" shown while the reply is fully visible | Rising |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Newest reply's bottom edge is outside the visible area after render | Client event `reply.visible_ratio` below 1 on a mobile client | Person scrolled up on purpose |
| Person taps "Show full reply" or "Jump to latest" right after a reply | UI event after a bot turn | A long reply the person wanted to re-read |
| Person asks to repeat or says "I can't see it" on a mobile client | User turn text on a mobile client | A reply that really was unclear |
| Send fails while the keyboard is open | Client event with keyboard state and send error | Network error |
| Horizontal scroll event inside the chat window | Client scroll event with nonzero horizontal offset | A wide table the person chose to pan |

**Starter rule:** whatever the keyboard, orientation, or text size, the newest reply and the input bar are both fully visible and nothing overlaps.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: mobile-keyboard-or-screen-hides-the-reply
runs: post_turn
reads: [client.device_class, client.keyboard_open, reply.visible_ratio, ui.show_full_reply_tap]
trigger: a bot reply is rendered on a mobile client and part of it is not visible (lead with the answer; offer "Show full reply")
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Show full reply", "Send it to my email", "Talk to a person", "Something else"]
on_miss: log
metric: layout defects per device in release testing
counter_metric: extra prompts on desktop
status: proposed
```

## 8. Related patterns
- [Auto-scroll fights the reader](auto-scroll-fights-the-reader.md): the closest page. It covers the view moving while a reply streams on any screen; this one covers the reply being covered or cut off by the keyboard, input bar, or small screen. The two interact in rule 3.
- [Lost drafts and failed sends](lost-drafts-and-failed-sends.md): a sibling chat-interface pattern where the person's own message is lost; here the bot's message is unreadable.
- [Silent attachment failures](silent-attachment-failures.md): another case where the content exists but the person cannot see it.
- [Accessibility family](../../accessibility/README.md): this page overlaps it on Reflow and Resize Text, but covers layout defects any phone user hits, not only users of assistive technology.

## 9. Common questions
### Why does the keyboard cover my chatbot's answer on my phone?
Browsers differ on whether the keyboard shrinks the page or draws over it, and a bottom-pinned input or full-height window can end up behind it (section 4). The fix is on the chat window's side, not yours.

### What does `interactive-widget` do?
It is a viewport meta key, shipped in Chrome 108, that sets whether the keyboard resizes the visual viewport, both viewports, or neither. See the Chrome source in section 4.

### What devices should we test on?
Start with the matrix in section 5 and add the devices most common in your own traffic. Real devices catch keyboard behavior that a narrowed desktop window does not.

### Is this an accessibility problem?
Partly. Text that is cut off at 320 CSS pixels or 200 percent text size fails WCAG success criteria 1.4.10 and 1.4.4, but the keyboard-overlap case affects every phone user.

---
## Technical section

### T1. Solution architecture
```
viewport meta (interactive-widget) -> message list height = visible area (rule 1)
visualViewport 'resize' -> keep input bar above keyboard, no overlap (rule 2)
if at bottom before resize -> scroll to newest reply (rule 3)
release: run matrix, log defects per device (rule 5)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Reply and input bar both visible | Chat window CSS and viewport handling | Tests 1-2 |
| No clipped text at 320 px and 200% | Layout | Tests 3, 5 |
| Matrix run each release | Release checklist | Matrix coverage metric |

### T3. Evals
- **Dataset:** the device-and-state matrix in section 5 with one long reply and one short reply each (starting point).
- **Judge rubric:** a reviewer checks screenshots for the last reply, the input bar, overlap, and horizontal scroll.
- **Release gate:** block a deploy while any device in the matrix has an open layout defect (starting point).

### T5. Trade-offs
- Real-device testing costs time; a device cloud or a small in-house set keeps it affordable.
- Browsers may change keyboard defaults again, so the matrix must be rerun after browser releases.
