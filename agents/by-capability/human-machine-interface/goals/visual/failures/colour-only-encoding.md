# Chatbot Status Colors: Color-Only Encoding in Cards, Chips, Charts and Tables

<!-- SEO
title: Chatbot Status Colors: Don't Rely on Color Alone
description: A chatbot card, chip, chart or table that shows success, error, risk or stock by color alone is unreadable to color-blind and screen-reader users. Add text and an icon.
search phrases:
- chatbot color only status accessibility
- color blind accessible chatbot cards
- wcag use of color chatbot
- red green status chip accessibility
- chatbot chart color blind
- screen reader chatbot status badge
- don't use color alone to convey meaning
- ai generated table color coding accessibility
-->

**Frequency**: Common

## Issue: A chat assistant's cards, status chips, charts or generated tables show success, error, risk, stock or priority by color alone, so color-blind users and screen-reader users miss the meaning.

> **Read this first.** This page is design guidance, not legal or accessibility-compliance advice. An accessibility expert should review it before you rely on it, and your own users with color vision deficiency and screen readers should test it. It quotes WCAG success criteria only as far as the opened W3C pages do; it makes no claim about which law applies to you.

> **One line:** A green dot means "in stock" and a red dot means "late", with no word or shape beside it; the fix is to put the meaning in text first, add an icon or shape as a second cue, and keep color as decoration.

| | |
|---|---|
| **Channel** | Written for **chat** (rich cards, status chips, generated tables and chart images in a text assistant). Voice and web-page variants are PLANNED, not written. |
| **Stakes** | Low for a color-coded tag. Medium to high when the color carries a risk, a payment state, a medication or a deadline. |
| **Who is affected** | Users with color vision deficiency, users of screen readers, users on low-contrast or monochrome displays, and anyone reading in glare |
| **Frequency** | Common as a design default. I found no study that counts how often chat products ship color-only status. |
| **Pattern ID** | colour-only-encoding |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Share of status, risk and priority items (chips, card badges, chart series, table cells) that carry a non-color cue: visible text or a distinct shape. Starting target: 100% (a starting point; tune it). |
| **Maturity** | Researched. No test file yet; the scenarios in section 6 are designs and are **Not yet run**. |
| **Will a better model fix this?** | No. Whether a chip has a label is decided by the card template and the renderer, not by how well the model writes. A model can still write "in stock" in the sentence, which helps. (Our judgment, not tested.) |
| **Also searched as** | color blind chatbot · red green status indicator · color coded table accessibility · don't use color alone · status badge screen reader · chart legend color only |

## 1. In plain words
The assistant shows a card with a green dot or a red chip and expects the user to know what it means. About 1 in 12 men have color vision deficiency (NEI), and a screen reader reads words, not the fill color of a dot. The fix is to say the status in words ("Late", "In stock") and add an icon or shape, so color only reinforces it.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional store "Northfield Outfitters")
```
User: Is the Ridgeline 40L pack in stock near me?
Bot:  Here's what I found:
      Denver, CO       [green dot]
      Boulder, CO      [yellow dot]
      Fort Collins, CO [red dot]
      (card: three colored dots, no legend, no text)
User: Which one is the green one? I can't tell them apart.
```
**With the fix**
```
User: Is the Ridgeline 40L pack in stock near me?
Bot:  Yes, at Denver. Two other stores are close:
      Denver, CO       In stock (12)       check-mark icon
      Boulder, CO      Low stock (2)       warning-triangle icon
      Fort Collins, CO Out of stock        cross icon
      [Reserve at Denver] [Something else]
```
The fixed version leads with the answer in the sentence, writes each status as a word with a count, adds a distinct icon, and keeps color as a bonus. A screen reader reads "Denver, CO, In stock, 12".

## 3. Why it happens
- **The status component takes a color prop, not a label.** The card or chip template is built from a design token such as "success" or "danger", and the visible text and accessible name are optional fields nobody fills.
- **The chart or table is generated as an image or as styled cells.** A model asked for "a table with red for overdue" writes cell colors or a chart with series told apart only by hue, with no labels, patterns or text in the cells.
- **Nobody tests in grayscale or with a screen reader.** The designers who review the card can see the colors, so the gap shows only when someone looks at the card without color or listens to it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 2.2 success criterion 1.4.1 (Level A): "Color is not used as the only visual means of conveying information, indicating an action, prompting a response, or distinguishing a visual element." | [W3C, Understanding SC 1.4.1: Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html). Opened and read. | A web-content standard, not a chat standard. A chat widget on a web page is web content; a chat inside a native app or messaging channel may fall under other rules. Check with your accessibility reviewer. |
| The intent: all sighted users can access information conveyed by color differences, because "the color may not be seen by users with color deficiencies." The page says those who benefit include users with partial sight, some older users, users with color vision deficiency, and people on limited-color monochrome displays. It adds that users who have problems distinguishing colors "can look or listen for text cues". | Same W3C page. Opened and read. | Informative page; the W3C says its listed techniques are sufficient, not the only way to comply. |
| "About 1 in 12 men have color vision deficiency." The most common type makes red and green hard to tell apart. The page gives no number for women and says only that men have a much higher risk. | [National Eye Institute, Color Blindness](https://www.nei.nih.gov/learn-about-eye-health/eye-conditions-and-diseases/color-blindness). Opened and read. | A general prevalence figure, not a measure of chat users. I found no figure for women on the opened page and give none. |
| For graphics, WCAG 2.2 SC 1.4.11 (Non-text Contrast) asks that parts of graphics needed to understand the content have a contrast ratio of at least 3:1 against adjacent colors. For a chart, you must be able to discern the lines or slices for each condition; the page says a graphic with text embedded or overlaid that conveys the same information is exempt. | [W3C, Understanding SC 1.4.11](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html). Opened and read. | A separate criterion from 1.4.1: contrast against the background is not the same as telling series apart without color. Use it for the 3:1 floor only. |
| One design system's status-badge guidance says "Color is never the only signal", treats an icon as the second channel, allows tone-only chips in dense tables only where the text label already disambiguates, asks standalone chips for an `aria-label`, and requires 4.5:1 contrast on every tone. | [MiHCM design system, status badge accessibility](https://designsystem.mihcm.com/components/status-badge/accessibility). Opened and read. | One vendor's design-system page, not a standard. I use it as an example of a working rule, and the 4.5:1 figure is theirs. |

**What the evidence does not show.** I found no study that measures how often chat assistants use color-only status, or how many chat users are affected. The prevalence line is a general population figure. The claim that a screen reader reads words and accessible names, not the color of a dot, is our judgment from how assistive technology works, not a figure from an opened source; test it with your own screen reader.

**How this differs from the closest pages.** Accessibility gaps (VI-04, planned/in progress, no page to link yet) is the broad WCAG 2.2 AA pass rate across critical flows: contrast, text alternatives, keyboard and screen-reader support. This page is one narrow rule inside that area: meaning carried by color alone. [Accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md) is the chat-wide test plan. [No accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md) is about a screen reader hearing "working" and "done". Misleading generated visuals (VI-08, planned, not written) is about charts that do not match the data; here the data can be right and the encoding still unreadable.

## 5. The fix

**The principle:** Say the meaning in words first, add a shape or icon as a second cue, and let color only reinforce it.

**Do this**
1. **Every status, risk or priority item has visible text.** "In stock", "Late", "High risk", "Due Friday". A dot, bar or chip with no word fails.
2. **Add a second non-color cue.** An icon with a different shape per state (check, triangle, cross), or a position or pattern. Do not give two states the same shape in different colors.
3. **Give a standalone chip or icon an accessible name.** If the chip is not next to its text, set the accessible label (for example `aria-label`) to the state, such as "Out of stock".
4. **Put the answer in the message text, not only in the card.** The sentence says which option is in stock or which invoice is overdue, so a user who skips the card still gets it.
5. **In tables, write the state in the cell.** Do not rely on a red or green cell fill. If you color rows, the text column still says the state.
6. **In charts, label directly or add a pattern.** Put series names on the lines or slices, or add a different marker shape or line style, and add a plain-text summary of the main finding. Keep the 3:1 contrast floor for graphic parts (SC 1.4.11).
7. **Keep a legend only as a backup.** A color legend is not enough on its own, because it asks the user to match hues.
8. **Check text contrast on every tone.** A starting target is 4.5:1 for chip text against its background (the figure the opened design-system page uses); confirm the number with your accessibility reviewer.

**Reference design: status line**
| Part | Content |
|---|---|
| Word | State in plain text, with the deciding number ("Low stock (2)") |
| Shape | A distinct icon per state, not only a different hue |
| Name | Accessible label that matches the visible word |
| Color | Optional, same meaning as the word, never the only carrier |

```
Whenever you show a status, risk, priority or availability, write the state as a word with its key number.
Add a different icon shape for each state. Never use color as the only signal.
In tables, write the state in each cell. In charts, label the series or give a text summary.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The message text states the result (which store has it, which invoice is late) before or beside the card |
| Offer choices | The user says they cannot read the colors: offer a text-only list or a table with words, plus "Something else". Do not offer choices when the answer is already clear in words |
| Ask one clarifying question | Only when a user reports a problem you cannot place: "Which part is hard to read, the dots or the chart?" |
| Hand off to a person | The user cannot get the information in any format the assistant offers |

**Don't over-correct.** Do not strip all color; color helps users who see it and speeds scanning. Do not pile on icons, badges and bold text until the card becomes cluttered ([cognitive overload](cognitive-overload.md)). Do not make every state equally loud: a card still needs one clear primary action ([no clear primary action](no-clear-primary-action.md)). One word plus one icon per item is enough.

**Hand-off rule.** If the user says they still cannot read the status after you have given a text version, offer a person or another channel with the same facts in a summary. A user who tells you they are color blind or use a screen reader should get the text-first version for the rest of the session, without being asked again.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file exists yet. The scenarios below are designs. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Render a stock or status card and look at it in grayscale | Every status is still readable from text and shape | 1, 2 |
| 2 | Open the card with a screen reader | Each status is announced as a word, with its item | 1, 3 |
| 3 | Read only the message text, ignore the card | The key result is stated in the text | 4 |
| 4 | Ask for "a table with overdue invoices in red" | Each row's cell says "Overdue" (or the state), not only a red fill | 5 |
| 5 | Ask for a chart with three series | Series are labeled or have distinct markers, and a text summary follows | 6 |
| 6 | Check that no two states share an icon shape | All states are distinguishable by shape | 2 |
| 7 | Measure chip text contrast on each tone | Meets the target your reviewer sets (starting point 4.5:1) | 8 |
| 8 | User says "I can't tell the dots apart" | Next reply gives a text version and keeps it for the session | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data and user tests, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Status items with a non-color cue** (primary) | 100% | Lint the card and table payloads: each status, risk or priority element has a non-empty text field and an icon or shape field | Any item without both |
| Standalone chips with an accessible label | 100% | Check the rendered payload for a label field on chips that sit without adjacent text | Any miss |
| Generated tables where color is the only state marker | 0 | Scan assistant table output for styled cells whose text does not contain a state word | Any |
| Charts with direct labels or a text summary | 100% | Check for series labels or a following summary sentence | Any miss |
| Users who say they cannot read colors, per 1,000 conversations (counter-signal) | Track; do not push to zero | Count matched phrases (see signals below) | Rising: a template is failing |
| Card clutter: elements per status item (counter-metric) | Track against baseline | Count text, icon and color elements per item | Rising: over-correction |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. They are written for chat text and rendered-payload events; none has been measured. Voice and web-analytics signals are PLANNED and not listed.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A status element has a color field but an empty text field (rule 1) | Render payload for a card or chip | A decorative dot beside an item whose text already states the state |
| Two states in one message share an icon shape and differ only by color (rule 2) | Icon field per element | States that mean the same thing |
| A user message says "which one is green", "I can't see the colors" or "what does the red mean" (rule 1) | Intent match on the next user turn | A sincere question about what the state means, not how it looks |
| A generated table has cell styles but no state word in the cells (rule 5) | Table payload scan | A table where the state is in an adjacent column of the same row |
| A chart is sent with no series labels and no summary text (rule 6) | Chart payload fields | A single-series chart where color carries no meaning |

**Starter rule:** write every status, risk or priority as a word plus a distinct icon, and never let color be the only signal.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: colour-only-encoding
runs: pre_send
reads: [reply.cards.status.text, reply.cards.status.icon, reply.cards.status.accessible_label, reply.tables.cells.text, reply.charts.series_labels, session.user_reported_color_issue]
trigger: a reply with a status, risk, priority or availability element is about to be sent
moves: [lead_with_answer, offer_choices, ask_one_question, hand_off]
choices: ["Show as a text list", "Show as a table with words", "Something else"]
on_miss: rewrite
metric: status items with a non-color cue
counter_metric: elements per status item
status: proposed
```

## 8. Related patterns
- Accessibility gaps (VI-04): planned/in progress, no page to link. The broad WCAG 2.2 AA pass rate for critical flows; this page is the narrow color-alone rule.
- [Accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md): the chat-wide accessibility test plan; this page is one cause inside it.
- [No accessible working or done signal](../../accessibility/failures/no-accessible-working-or-done-signal.md): screen readers missing the working and done states.
- [Controls unreachable by keyboard](../../accessibility/failures/controls-unreachable-by-keyboard.md): buttons a keyboard user cannot reach.
- [Cognitive overload](cognitive-overload.md): too many elements; the limit on adding icons and labels in rule 2.
- [No clear primary action](no-clear-primary-action.md): one primary action per message, which status styling must not blur.
- [Stale price or stock at checkout](../../shopping-agents/failures/stale-price-or-stock-at-checkout.md): a stock figure that is wrong, where this page covers a stock figure that is right but unreadable.
- Misleading generated visuals (VI-08): planned, not written; charts that do not match the data.

## 9. Common questions
### Is it OK to use red and green for status in a chatbot?
Yes, as a second signal. NEI says the most common type of color vision deficiency makes red and green hard to tell apart, so a red or green chip must also say its state in words and, ideally, have its own icon shape. See rules 1 and 2.

### What does WCAG say about color-coded status?
WCAG 2.2 SC 1.4.1 says color must not be the only visual means of conveying information, indicating an action, prompting a response or distinguishing a visual element. Whether it applies to your chat product, and at which level, is a question for your accessibility reviewer.

### Do I need an icon if the chip already has a text label?
Not always. The one design system I opened allows tone-only chips in dense tables where the text label already makes the state clear, and asks for an icon when a chip stands alone. Test it with your users and a screen reader.

### How do I make a chart from a chatbot accessible without color?
Label the lines or slices directly or use different marker shapes, keep 3:1 contrast on the graphic parts, and add a one-sentence text summary. The W3C page on non-text contrast says a graphic with embedded text that conveys the same information is exempt from that contrast rule.

### Will a screen reader read the color of my status dot?
In our judgment, no: it reads the text and the accessible name, so a dot with neither is silent or unclear. Confirm with the screen readers your users run. Set the accessible name to the state (rule 3).

### How is this different from the general accessibility pattern?
Accessibility gaps (planned/in progress) covers the whole WCAG pass rate. This page is one specific, easy-to-lint rule: no meaning by color alone. It is also quick to fix in a card template.
