# Chatbot Icons, Colors and Arrows Confuse in Other Locales: Visuals That Don't Localise

<!-- SEO
title: Chatbot Icons and Layout in Other Locales: RTL Mirroring Fix
description: Chat cards, icons, colors and carousels built for US English confuse users in other locales. Mirror only direction icons, label every icon, test each locale.
search phrases:
- chatbot rtl layout icons not mirrored
- which icons should be mirrored in rtl
- chat widget arabic carousel arrows wrong direction
- localize icons colors gestures chatbot
- icon only buttons confusing other countries
- do charts mirror in right to left
- chat card layout rtl mirror
- thumbs up icon different cultures chatbot feedback
-->

**Frequency**: Occasional

## Issue: Cards, icons, colors, gesture symbols and mirrored layouts that were designed and tested only in US English confuse or mislead users in other locales; the fix is to mirror only direction-bearing icons, put a text label on every icon, and test each supported locale.

> **One line:** The words are translated but the pictures are not: a "next" arrow points the wrong way, a status color or hand symbol means something else, and the user cannot tell what a button does.

| | |
|---|---|
| **Channel** | Written for **chat** assistants and their widgets, cards, chips and generated visuals (text-first). Voice and a site-wide web check are PLANNED; nothing about them is measured here. |
| **Stakes** | Low to medium. A flipped arrow is an annoyance; a wrong "confirm" or "cancel" icon on an order or payment card can cause a wrong action. |
| **Who is affected** | Users of every locale you support other than the one the visuals were designed in, most visibly right-to-left readers (Arabic, Hebrew, Persian, Urdu). |
| **Frequency** | Occasional (our judgment; it depends on how many locales you ship). I found no study of how often it happens in chat products. |
| **Pattern ID** | visuals-that-don-t-localise |
| **Family** | Visual ([family README](../README.md); roadmap row VI-17 in the [visual and oversight roadmap](../../../roadmap/visual-and-oversight.md)) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. (Row goal: visuals work in each supported locale.) |
| **Primary metric** | RTL render pass; icon comprehension in test locales. Target: 100% of RTL render cases pass; comprehension target set from your first test round (starting point to tune). |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | No. The model chooses words; icons, colors and layout direction come from the widget and design system. (Our judgment, not tested.) |
| **Also searched as** | chat widget RTL icons wrong way · carousel arrows reversed Arabic · icon-only buttons confusing · localize icons and colors · mirrored layout chat card · cultural meaning of colors in UI |

## 1. In plain words
A chat card has a back arrow, a "next" chevron, a thumbs-up, a green "done" chip and an icon-only toolbar. Translating the text does not change any of them. In a right-to-left layout the arrows must flip; some icons (charts, clocks, media controls) must not; and an icon with no label can mean different things to different people. Fix it by deciding per icon whether it mirrors, labeling every icon in words, and testing each locale with people from it.

## 2. What it looks like
Illustrative; I did not render this. A U.S. pharmacy chat widget; the customer lives in Dearborn, Michigan, and has the app set to Arabic.

**Without the fix**
```
Bot:   (Arabic text, right-aligned) Your refill is ready at 3 pickup locations.
Card:  [ < ]  Store 1 of 3  [ > ]       <- arrows unchanged; "next" points left, toward the first card
Row:   [thumbs-up icon] [thumbs-down icon]   <- no text, no label for screen readers
Chart: line chart of refill history, drawn right to left, time axis reversed to match the layout
User:  (taps the right chevron expecting "next"; goes to the previous store)
```
**With the fix**
```
Card:  [ > ]  المتجر 1 من 3  [ < ]       <- chevrons mirrored; "next" points in the reading direction
Row:   [thumbs-up] مفيد   [thumbs-down] غير مفيد   <- icon plus a visible word
Chart: same chart as in English (not mirrored); axis labels and legend text follow the locale
```
Same data. What changed: direction icons follow the reading direction, a non-directional chart is left alone, and each icon has a visible word.

## 3. Why it happens
- **Visuals are drawn once.** The widget, icon set and color tokens are built for one locale, and the model's reply text is the only part that is translated. (Our judgment.)
- **Mirroring is a per-icon decision.** "Flip everything" and "flip nothing" are both wrong, so a global switch cannot fix it; each icon needs a rule.
- **Nobody from the locale reviews it.** Test chats and screenshots are in English, so the first person to meet a confusing icon is a user.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Material Design's bidirectionality page says icons that communicate direction, like arrows, are mirrored; an icon showing forward movement is mirrored; not mirrored: icons that do not communicate direction (a camera), numbers, charts and graphs; "Do not mirror media playback buttons and the media progress indicator"; icons with text "need careful mirroring"; for undo and redo, "choose whether to show circular or horizontal direction." | [Material Design 1, Bidirectionality](https://m1.material.io/usability/bidirectionality.html). Opened. | An older Material version; the current Material 2 page would not load for me. A design-system convention, not a measured result. |
| Firefox's RTL guidelines list what to mirror (direction or motion, such as back/forward and progress bars; icons implying text direction; icons implying where a UI element sits; handheld objects) and what not to (text and numbers, including icons that contain them; direction-neutral or symmetric icons; checkmarks; video and audio controls; product logos). | [Firefox RTL guidelines](https://searchfox.org/firefox-main/source/docs/code-quality/coding-style/rtl_guidelines.md). Opened. | One product's coding guidelines. It agrees with Material on most points, which is a sign of convention, not proof. |
| NN/g: "a text label must be present alongside an icon to clarify its meaning in that particular context"; labels should be visible at all times; most icons are ambiguous; home, print and the magnifying glass for search enjoy mostly universal recognition. | [Harley, *Icon Usability*, NN/g, 2014](https://www.nngroup.com/articles/icon-usability/). Opened. | Not specific to chat or to other locales. The article is from 2014. |
| W3C: localization means adapting to a target market's "language, cultural and other requirements"; it lists symbols, icons and colors as culture-dependent, and says graphics may be "misinterpreted or viewed as insensitive" in a given culture. | [W3C, *Localization vs. Internationalization*](https://www.w3.org/International/questions/qa-i18n). Opened (read through the fetch tool's summary of the page). | General guidance. The page gives no specific color or icon examples. |
| A 2024 analysis of color-emotion associations (8,615 participants, 37 nations, 25 languages) found Lithuanian associations matched the global pattern closely (r = .92), with some differences, such as red linked more with love than anger. Linguistic distance, not geographic distance, predicted similarity. | [Psichologija, 2024](https://www.journals.vu.lt/psichologija/en/article/view/34682/33640). Opened (read through the fetch tool's summary). | Measures associations between color words and emotion concepts, "tells little about felt emotions" (authors). It does not test status colors in a chat UI. If anything it says color-emotion links are more shared than one might fear, so do not treat any single color claim as settled. |

Read but kept out of the fix: a front-end checklist says a thumbs-up is a vulgar gesture in parts of the Middle East and West Africa, that white signals mourning in some East Asian countries, and that national flags should not stand for languages ([Front-End Checklist, locale images](https://frontendchecklist.io/rules/i18n/locale-images)). It names three sources but does not tie each claim to one, and I could not check them. Treat these as questions to put to a native reviewer, not as facts.

**Public incident.** I found no dated public incident for this failure in a chat product. **Research gap (R):** I could not verify how often it happens, any measured effect on task success, or Apple's current right-to-left guidance (the page returned only a title).

## 5. The fix
**The principle:** Decide for each visual whether it mirrors, say what it means in words, and test it with people from each supported locale.

**Do this**
1. **Keep a mirror table for every icon.** Each icon in the widget is marked mirror, keep, or locale variant. Check: no icon is unmarked.
2. **Mirror icons that carry direction, keep the rest.** Back, next, forward, send and collapse-toward-a-side icons flip in RTL; charts, graphs, numbers, clocks, checkmarks, camera-type icons, media controls and logos do not. Check: on the RTL test card the "next" chevron points in the reading direction and the chart matches the English one. (Material, Firefox.)
3. **Put a visible word next to every icon that triggers an action.** Check: no icon-only action button exists in any locale; each has a visible label and an accessible name. (NN/g.)
4. **Draw layout from reading direction, not from left and right.** Card order, carousel order, button order and the primary action's side follow the locale. Check: in RTL, the first card is at the right edge and the primary action is on the reading-start side. (Our design choice; I found no chat-specific test.)
5. **Do not put text inside images or generated visuals.** Text lives in the card so it can be translated, resized and mirrored. Check: every string on a card is selectable text. (Our design choice.)
6. **Do not let color or a gesture symbol be the only carrier of meaning.** Pair status colors with words and shapes ([colour-only encoding](colour-only-encoding.md)). For thumbs, flags, hand symbols and colors with a possible local meaning, show a word with them and have a native reviewer approve each locale. Check: the review log lists each such icon and locale with an approve or change decision.
7. **Test each supported locale before release.** Run the RTL render cases in section 6 and an icon comprehension check with people from each test locale; report both.

**Reference design: icon table**
| Icon | RTL | Locale variant | Visible label |
|---|---|---|---|
| Next / previous chevron | Mirror | No | "Next", "Previous" |
| Chart, graph, clock | Keep | No | Chart title |
| Media play / progress | Keep | No | "Play" |
| Checkmark, logo | Keep | No | "Done" |
| Thumbs up/down, flags, status colors | Keep | Reviewer decides per locale | "Helpful", "Not helpful" |

```
Rules for cards and icons
- Every action icon has a visible label from the locale's string table.
- Direction icons flip with reading direction; charts, numbers, clocks, media controls, logos do not.
- No text inside images. No color-only status. No language flags unless a reviewer approved them.
- Layout order follows reading direction. If a locale has no reviewed visuals, use the English-reviewed set with labels and say so in the release notes.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The user says a button or icon is unclear or wrong-way. The bot cannot see its own display: restate the action in words ("The next store is the one after this"). |
| Offer choices: 2-4 options plus "Something else", free text open | After a "this is confusing" report: "Show text buttons", "Show a simple list", "Talk to a person", "Something else". Do not offer them when the card already has labeled buttons and the user only wants the answer. |
| Hand off to a person | The same confusion twice, or the user cannot find a control for an action with consequences (payment, cancel). |

**Don't over-correct.** Do not mirror every icon in RTL, do not replace icons with text-only cards, and do not drop a locale's visuals because one icon was a problem. Do not assume a color or gesture is offensive without a native reviewer. The guardrail is the counter-metric: English layouts must still pass.

**Hand-off rule.** The bot cannot repair its own display. On a second confusion report, log the card ID and locale and hand off to a person with the card text attached. Do not promise a fix date.

**Framework used:** Material and Firefox mirroring conventions and NN/g icon labels, as opened in section 4. Not in the solutions library.

## 6. How to test it (short version)
Tests are **not yet run**. Use the real widget, with a native reader of each test locale reviewing the first release.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Arabic card carousel, 3 cards | 2, 4 | Chevrons mirrored; first card at the right edge |
| 2 | RTL card with a chart | 2 | Chart matches the English drawing |
| 3 | Audit every action icon in each locale | 3 | A visible label next to each |
| 4 | Card with a baked-in text image | 5 | None found |
| 5 | Status chip in each locale | 6 | Word plus shape, not color alone |
| 6 | Thumbs, flag, hand-symbol icons | 6 | Reviewer decision recorded per locale |
| 7 | Icon comprehension: show each icon without its label to 5 or more people from the locale | 1, 3 | Share who name the action correctly meets your target, set from the first round |
| 8 | English layout (counter-test) | Don't over-correct | Unchanged, left-to-right |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **RTL render pass** (primary) | 100% of section 6 cases 1, 2, 4 | Run on each release and each widget change | Any failure blocks release |
| **Icon comprehension in test locales** (primary) | Set from round one | Section 6 case 7 per locale | Below target, or falling between rounds |
| Action icons with a visible label | 100% | Audit of the icon table | Any unlabeled |
| English layouts wrongly mirrored (counter-metric) | 0 | Case 8 | Any |
| Locales shipped with no native review | 0 | Release checklist | Any |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User taps a card's previous control right after tapping next in an RTL locale | Click events by locale | A user browsing back and forth on purpose |
| User turn says a button is unclear, wrong-way, or asks "what does this do" | Next-turn text match, any language | A question about the product, not the control |
| Feedback or action icons used far less in one locale than others | Click rate by locale | A locale with few users |
| Card rendered in RTL with a direction icon unchanged | Render log: locale vs. icon mirror flag | A direction-neutral icon correctly kept |

**Starter rule:** every action icon in a card has a visible label, and only icons that carry direction are mirrored in right-to-left layouts.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: visuals-that-don-t-localise
runs: pre_send
reads: [card.icons, card.locale, ui.mirror_table, user_turns.text]
trigger: a card with icons is about to be shown in a non-default locale, or the user says a control is unclear
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Show text buttons", "Show a simple list", "Talk to a person", "Something else"]
on_miss: rewrite
metric: RTL render pass; icon comprehension in test locales
counter_metric: English layouts wrongly mirrored
status: proposed
```

## 8. Related patterns
- [Right-to-left and mixed-script rendering](../../language-and-locale/failures/right-to-left-and-mixed-script-rendering.md): the closest page. It is about how text, numbers and punctuation are drawn. This page is about icons, colors, symbols and layout order around the text.
- [Colour-only encoding](colour-only-encoding.md): meaning carried by color alone for color-blind users. Here the same color is read differently by locale; rule 6 reuses its fix.
- [Rich-card misuse](rich-card-misuse.md): cards where a sentence would do. Here the card is right and its pictures fail.
- [Misleading generated visuals](misleading-generated-visuals.md): generated images that look real. Here the visual is honest but local.
- [One-size communication style](../../cultural-adaptation/failures/one-size-communication-style.md): wording style across cultures; this page covers the non-text parts.

## 9. Common questions
### Which icons should be mirrored in right-to-left layouts?
Icons that carry direction or motion, such as back, next and forward. Charts, numbers, clocks, checkmarks, media controls and logos stay as they are ([section 4](#4-why-it-matters)).

### Do charts and graphs flip in Arabic or Hebrew?
Material says charts and graphs are not mirrored; Firefox says numbers and direction-neutral content are not. Keep the chart drawing and localize its text.

### Is a thumbs-up safe in every country?
I could not verify that. One checklist says it is a vulgar gesture in some regions; its sources are not tied to the claim. Add a word, and ask a native reviewer.

### Are icon-only buttons fine if the icon is common?
Only a few icons, such as home, print and search, are mostly universal (NN/g, 2014). Add a visible word anyway.

---
## Technical section

### T1. Solution architecture
```
card spec (icons by ID) -> mirror table lookup (mirror | keep | variant) by locale
                        -> string table (visible labels) -> renderer (logical, not left/right, layout)
                        -> screenshot test per locale in CI
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No unmarked icon | Build step reading the icon table | CI failure |
| No icon-only action | Card linter | Section 6, case 3 |
| No text in images | Asset check | Case 4 |

### T3. Evals
- **Dataset:** every card template rendered in each supported locale, plus the English baseline; start with the card types users see most.
- **Judge rubric:** direction icons correct, non-directional icons unchanged, labels present, no color-only status.
- **Metrics and starting thresholds:** RTL render pass 100%; comprehension target from round one. Starting points to tune.
- **Release gate:** block a release on any RTL render failure or a locale with no native review.

### T5. Trade-offs
- Native review per locale costs time; start with the locales with the most users.
- A mirror table needs upkeep when icons are added; the CI check keeps it honest.

---
### Deep dive
- **Open question.** I found no chat-specific study of icon or color comprehension across locales; the evidence is design-system conventions and general icon research.
- **References.** [Material 1](https://m1.material.io/usability/bidirectionality.html), [Firefox RTL](https://searchfox.org/firefox-main/source/docs/code-quality/coding-style/rtl_guidelines.md), [NN/g](https://www.nngroup.com/articles/icon-usability/), [W3C](https://www.w3.org/International/questions/qa-i18n), [Psichologija 2024](https://www.journals.vu.lt/psichologija/en/article/view/34682/33640) (all opened).
