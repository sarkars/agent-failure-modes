# Chatbot Buttons Too Small to Tap on a Phone: Small Targets and Small Screens

<!-- SEO
title: Chatbot Buttons Too Small to Tap on Mobile: Fix Target Size
description: Quick-reply chips, card buttons and links in a chat widget are too small or too close on a phone. Size and space them, and test at 320 px wide.
search phrases:
- chatbot buttons too small on mobile
- quick reply buttons too close together mobile
- chat widget tap target size
- chatbot carousel mobile swipe not working
- wcag 2.5.8 target size chat widget
- chatbot horizontal scroll on phone
- chat widget links hard to tap
- chatbot card buttons overlap on small screen
-->

**Frequency**: Common

## Issue: Quick-reply chips, card buttons, links and carousels in a chat widget are too small or too crowded to tap on a phone, or the layout overflows the screen, so users mis-tap or cannot read the options.

> **One line:** The bot offers chips and card buttons, but on a phone they are tiny or packed together, so the user taps the wrong one or has to scroll sideways to read them; the fix is minimum target sizes with spacing, wrapping layouts, and a typed-answer fallback, tested at 320 CSS pixels wide.

| | |
|---|---|
| **Channel** | Written for **chat** (web chat widgets and rich cards on phones). Native-app and voice variants are PLANNED, not written. |
| **Stakes** | Low to medium. A mis-tap on "Cancel order" or "Confirm payment" can cost money; most are a retry. |
| **Who is affected** | Phone users, and most of all people with hand tremors or limited dexterity, large fingers, or one-handed use on the move |
| **Frequency** | Common as a design default (desktop-first widgets squeezed onto a phone). I found no count of how many chat products have this defect. |
| **Pattern ID** | small-targets-and-small-screens |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Target-size pass rate: share of interactive elements in the chat widget that meet WCAG 2.5.8 (24 by 24 CSS pixels, or the spacing exception) in a render at 320 CSS pixels wide. Starting target: 100% (a starting point; tune it). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The model's words are fine; the widget's CSS decides how big and how close the controls are. (Our judgment, not tested.) |
| **Also searched as** | chatbot buttons too small · can't tap chatbot options on phone · chat suggestion chips overlap · chatbot carousel hard to use on mobile · chat widget cut off · chat links too close together |

## 1. In plain words
On a desktop, a row of small chips is easy to click with a mouse. On a phone, a fingertip is much bigger than a mouse pointer, so small chips that sit close together get tapped by mistake, and a row that is wider than the screen forces sideways scrolling. The fix is to make each control big enough with room around it, let rows wrap, and always let the user type the answer instead.

## 2. What it looks like
A customer on an iPhone SE is rescheduling a delivery with a fictional "Harbor Furniture" assistant.

**Without the fix**
```
Bot:  When should we deliver your sofa?
      [Tue 3] [Wed 4] [Thu 5] [Fri 6] [Sat 7] [Mon 9] →   (chips are ~18 px tall, 2 px apart,
                                                             row runs off the right edge)
User: (taps "Thu 5"; the widget registers "Wed 4")
Bot:  Great, Wednesday, October 4. Your delivery is booked.
User: no I wanted thursday
Bot:  Sorry, I can't change a booked delivery. Please call us.
```
**With the fix**
```
Bot:  When should we deliver your sofa? Pick a day or type one.
      [Thursday, Oct 5]   [Friday, Oct 6]   [Saturday, Oct 7]     (each full-width, 48 px tall, 8 px apart)
      [More days]  [Something else]
User: (taps "Thursday, Oct 5")
Bot:  Delivery set for Thursday, Oct 5. Reply "change" to pick another day.
```
The fixed version uses fewer, bigger, wider-spaced buttons that wrap on a narrow screen, keeps typing open, and shows the exact date before booking, so one mis-tap is cheap to fix.

## 3. Why it happens
- **The widget was designed and tested on a desktop.** Mouse pointers are precise, so 18-pixel chips looked fine in review and nobody opened the page on a 320-pixel-wide phone.
- **Content drives the layout.** Long option labels, a fixed-width card, or a carousel sized in pixels overflow when the screen narrows, and the fix is left to the browser (which scrolls sideways).
- **Chips are packed to fit more options.** Teams reduce padding to show 6 options at once, because the page template has no rule for minimum size or spacing.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA: "The size of the target for pointer inputs is at least 24 by 24 CSS pixels, except when" one of five exceptions applies (spacing, equivalent control, inline, user agent control, essential). Intent: help ensure "targets can be easily activated without accidentally activating an adjacent target." | [W3C, Understanding SC 2.5.8](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html). Opened through WebFetch (a fetch tool's page extract, so read through a summary). | A standard, not a measure of how often chat widgets fail it. Wording came from the tool's extract; check the page. |
| Spacing exception: undersized targets pass if a 24 CSS pixel circle centered on each does not intersect another target or another undersized target's circle. Examples on the page: 20 by 20 px targets with a 4 px gap pass; with no gap they fail; two rows of 16 px buttons with a 1 px gap fail. | Same W3C page. Read through a summary. | Examples only. Do not treat 20 px with 4 px gap as a design goal; it is the floor. |
| SC 2.5.5 Target Size (Enhanced), Level AAA: "at least 44 by 44 CSS pixels", with exceptions for an equivalent target, inline text, user agent control, and essential presentation. It cites "hand tremors, limited dexterity" and says touch input is especially imprecise. | [W3C, Understanding SC 2.5.5](https://www.w3.org/WAI/WCAG22/Understanding/target-size-enhanced.html). Read through a summary. | AAA is optional. Used here as a reference for important controls, not a requirement. |
| Google's Android accessibility help: "Consider making touch targets at least 48x48dp, separated by 8dp of space or more." It adds that 48x48dp "results in a physical size of about 9mm, regardless of screen size." | [Google Accessibility Help, Touch target size](https://support.google.com/accessibility/android/answer/7101858). Read through a summary. | Android guidance ("consider"), not a web or chat-specific rule. |
| web.dev: "A minimum recommended touch target size is around 48 device independent pixels", and "Touch targets should also be spaced about 8 pixels apart, horizontally and vertically." | [web.dev, Accessible tap targets](https://web.dev/articles/accessible-tap-targets). Read through a summary. | Guidance for web pages. It gives no outcome data. |
| WCAG 1.4.10 Reflow (AA): content must be presented without loss of information or functionality and without scrolling in two dimensions at a width equivalent to 320 CSS pixels (vertically scrolling content), except parts that need two-dimensional layout. | [W3C, Understanding SC 1.4.10](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). Read through a summary. | Whether a carousel inside a chat counts as an exception is a judgment call; this page does not rely on it (rule 4 gives a text alternative). |

**Not verified.** Apple's Human Interface Guidelines were requested but the fetch returned only the page title, so I cite no Apple number. Nielsen Norman Group carousel findings were seen only in secondary search summaries and are not used.

**Public incident.** None found. I found no study that measures mis-taps on chat widgets.

## 5. The fix

**The principle:** Every control in the chat is big enough to hit with a thumb, far enough from its neighbors that one tap cannot hit two, and still usable when the screen is 320 CSS pixels wide.

**Do this**
1. **Meet the floor on every control.** Chips, card buttons, "send", and "close" are at least 24 by 24 CSS pixels (WCAG 2.5.8), or pass the spacing exception. For chips and the primary button on a card, use a larger starting size of 44 to 48 pixels tall (from the 44 and 48 figures in section 4; tune on your devices).
2. **Space targets apart.** Leave at least 8 pixels between adjacent tappable controls, horizontally and vertically (starting point from the 8dp and 8 px guidance).
3. **Let rows wrap or stack; never force a sideways scroll to read options.** Chips wrap to the next line; card buttons go full width on a narrow screen. Nothing needed to answer is clipped at the right edge at 320 CSS pixels wide.
4. **If you use a carousel, give it a way to avoid swiping.** Show a peek of the next card, give next and previous buttons that meet rule 1, and offer the same options as a plain list ("Show all as a list" or typed answers). Keep a carousel to the number of cards a user needs to compare (a starting point of 5 or fewer).
5. **Keep links from crowding.** Put one link per line or per button when a message has several; do not put two links in adjacent words. A link inside a sentence is exempt from the size rule (WCAG inline exception) but still needs a distinct style.
6. **Label with short, distinct text that fits.** A label wraps to two lines or is shortened ("Thu, Oct 5"), never truncated to the point that two chips look identical.
7. **Keep typing open and confirm risky taps.** The user can always type the answer ([quick-reply buttons that don't match what was typed](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md)). After a tap that books, pays or deletes, show what was chosen and offer an undo or "change".
8. **Test the real thing.** Check at 320 CSS pixels wide, with text enlarged, in portrait and landscape, on at least one small physical phone.

**Reference design: chip and card spec**
| Part | Starting value (tune on your devices) |
|---|---|
| Chip or button hit area | 44-48 px tall, at least 24 by 24 px for any control |
| Gap between targets | 8 px or more, both directions |
| Layout at 320 px wide | Wrap or stack; no horizontal page scroll |
| Options per message | 2-4 shown, plus "Something else" and open typing |
| Carousel | Next and previous buttons, peek of next card, list alternative |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices | The reply needs a pick: 2-4 options plus "Something else", sized and spaced as in rules 1-3. Do NOT offer 8 tiny chips because they fit on a desktop |
| Ask one clarifying question | The user taps the wrong chip or says "no, the other one": confirm the intended choice in words |
| Hand off to a person | The user mis-taps twice in a row or says they cannot press the options: offer typing or a person |

**Don't over-correct.** Bigger controls take space. Do not drop to one option per screen so the user must scroll through six messages, and do not hide needed options to make the layout tidy. Show the likeliest 2-4, keep typing open, and offer "More" where more exist.

**Hand-off rule.** When the user mis-taps twice, types that they cannot tap or see the options, or abandons a step after cards, stop showing buttons for that step, ask the question in words, and offer a person if it still fails.

**Framework used:** none yet. Rules 1-2 follow the size and spacing figures in section 4; rule 3 follows the Reflow criterion; rule 7 follows the library's [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
No test file yet. The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Render a chip row and a card in the widget; measure each control | Every control is at least 24 by 24 CSS px or passes the spacing exception; chips and primary buttons meet your 44-48 px target | 1 |
| 2 | Measure the gap between adjacent controls | 8 px or more in both directions | 2 |
| 3 | Open the widget at 320 CSS px wide with a 6-option reply | Chips wrap or stack; no horizontal scroll to read or tap an option | 3 |
| 4 | Open a carousel at 320 px wide | Next and previous buttons work; a list alternative exists; the next card peeks | 4 |
| 5 | Send a message with three links | Each link is on its own line or button; none touches another | 5 |
| 6 | Use two options with similar labels ("Thu, Oct 5" vs "Thu, Oct 12") | Labels are distinct and not cut off | 6 |
| 7 | Tap a booking chip, then type "change" | The chosen value is shown; the change works without starting over | 7 |
| 8 | Run it at 200% text size, in landscape, on a small phone | No clipped options; targets still pass scenarios 1-2 | 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Target-size pass rate** (primary) | 100% (starting point) | In CI, render widget states at 320 CSS px wide and check each interactive element's box and spacing against the 24 px rule (for example with an automated accessibility checker) | Any failing control |
| Horizontal-overflow rate | 0 widget states | In the same render, flag any widget whose scroll width exceeds its client width | Any overflow |
| Mis-tap corrections: user changes a choice within 2 turns of a tap | Track; set from your baseline | Log taps with `action.id` and a following correction turn | Rising |
| Tap-then-type rate on option messages (counter-metric) | Track; do not chase | Share of option messages where the user types instead of tapping | Rising on phones only: targets may still be too small |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Written for **chat** text and button events only; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User taps a chip, then within 2 turns says "no", "wrong one", or picks a neighboring chip | `action.tap` followed by a correction turn | User changed their mind |
| Mobile sessions show more tap-then-correct events than desktop sessions | `device.class` split of the correction rate | Different user mix on phones |
| A message with 5 or more chips of the same style on a viewport under 400 px | `message.actions` count and `viewport.width` | A carousel of one-button cards |
| User asks "what are the options" or "I can't see the buttons" | User turn after an option message | The user wants a plain-language list |
| Carousel next card never viewed (no scroll or next event) after 3 renders in a session | `carousel.view` events | A single-card carousel |

**Starter rule:** every chip and card button is at least 24 by 24 CSS pixels (44-48 for chips and primary buttons), has 8 pixels of space around it, and wraps instead of scrolling at 320 CSS pixels wide.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: small-targets-and-small-screens
runs: pre_send
reads: [message.actions, action.label, viewport.width, device.class, action.tap_correction]
trigger: a reply with chips, card buttons, links, or a carousel is about to be sent
moves: [offer_choices, ask_clarifying_question, hand_off]
choices: ["Thursday, Oct 5", "Friday, Oct 6", "Saturday, Oct 7", "Something else"]
on_miss: rewrite
metric: target-size pass rate
counter_metric: tap-then-type rate on option messages
status: proposed
```

## 8. Related patterns
- [Mobile keyboard or screen hides the reply](../../chat-interface/failures/mobile-keyboard-or-screen-hides-the-reply.md): the closest page. It covers the keyboard or input bar covering the bot's latest reply; this page covers the size, spacing and overflow of the controls (chips, buttons, links, carousels) inside the reply.
- [No clear primary action](no-clear-primary-action.md): how many buttons and which is primary; this page covers how big and how far apart they are.
- [Cognitive overload](cognitive-overload.md): too much on screen at once; crowding here is a physical, not a reading, problem.
- [Quick-reply buttons that don't match what was typed](../../chat-interface/failures/quick-reply-buttons-that-don-t-match-what-was.md): keeping typed answers next to buttons.
- [Controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md): the same widget controls for keyboard users; this page is about touch.
- [Auto-scroll fights the reader](../../chat-interface/failures/auto-scroll-fights-the-reader.md): the view moving while the user tries to tap.
- Planned visual patterns (not yet written): accessibility gaps, rich-card misuse.

## 9. Common questions
### How big should chatbot buttons be on a phone?
WCAG 2.5.8 sets a floor of 24 by 24 CSS pixels, with a spacing exception. Larger starting sizes come from other guidance: 44 by 44 CSS pixels in WCAG 2.5.5 (AAA), and 48dp with 8dp spacing from Google's Android accessibility help. This page uses 44-48 pixels for chips and primary buttons as a starting point to tune.

### Do I have to meet WCAG 2.5.8 for a chat widget?
This page does not give legal advice. 2.5.8 is a Level AA success criterion in WCAG 2.2; whether it is required for your product depends on your own legal and procurement context, which I did not research. It is also a reasonable test on its own merits.

### Are carousels bad in chatbots?
Not necessarily, but they hide later cards and need swiping. Give them next and previous buttons that meet the size rule, show part of the next card, and offer the same options as a list (rule 4). I did not find an opened source with numbers on carousel engagement, so none is cited.

### Can I make the visible chip small but the tap area large?
Secondary sources describe this trick, and Google's help says the touch area can extend beyond the drawn element, but I did not open a source that states how it should be built. Make sure the enlarged hit area does not overlap its neighbors (rule 2) and test it on a device.

### What is the quickest check?
Open the widget at 320 CSS pixels wide with text enlarged and tap every option with your thumb. If you mis-tap, scroll sideways, or cannot read a label, a user will too (rules 1-3, 8).
