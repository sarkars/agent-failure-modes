# Chatbot Arabic or Hebrew Text Shows Backwards or Left-Aligned: Right-to-Left and Mixed-Script Rendering

<!-- SEO
title: Chatbot Arabic Text Backwards or Misaligned: RTL Fix
description: Arabic or Hebrew chat replies show left-aligned, with numbers and punctuation on the wrong side. Set direction per message and isolate mixed text.
search phrases:
- chatbot arabic text backwards
- chat ui rtl support
- arabic hebrew mixed with english numbers wrong order chat
- punctuation on wrong side rtl text
- dir auto chat messages
- bdi element user generated content
- bidi text bug chat interface
- rtl text in code block renders ltr
-->

**Frequency**: Occasional

## Issue: Arabic or Hebrew chat replies show left-aligned, with numbers, punctuation, and English words on the wrong side; the fix is to set direction per message block, isolate mixed-in text, and run an RTL render test.

> **One line:** The bot's words are right, but the chat window draws them in a left-to-right box, so an Arabic or Hebrew reply is misaligned and its numbers and punctuation land in the wrong place.

| | |
|---|---|
| **Channel** | Written for **chat** (text shown in a chat window). Voice and a site-wide web check are planned; nothing about them is measured here. |
| **Stakes** | Low to medium. A misplaced period is an annoyance; a scrambled order number, amount, or step list can mislead. |
| **Who is affected** | Users who read or write Arabic, Hebrew, Persian, Urdu, or any right-to-left script, and anyone whose reply mixes such text with English names, numbers, or links. |
| **Frequency** | Occasional (our judgment; it depends on whether you support these scripts). I found no study of how often it happens; one forum report is below. |
| **Pattern ID** | right-to-left-and-mixed-script-rendering |
| **Family** | Language and locale ([family README](../README.md); roadmap row LG-16 in the [language and locale roadmap](../../../roadmap/language-and-locale.md)) |
| **Goal** | Text displays correctly in every supported script. |
| **Primary metric** | RTL render-test pass rate. Target: 100% (starting point to tune). |
| **Maturity** | Researched (tests: not yet run) |
| **Will a better model fix this?** | No. The model can send correct text and the screen can still draw it wrong, because direction is set by the display layer. (Our judgment, not tested.) |
| **Also searched as** | chatbot Arabic backwards · RTL support in chat UI · Hebrew with English words scrambled · numbered list period on wrong side · chat bubble alignment RTL · bidi bug in AI chat |

## 1. In plain words
Arabic and Hebrew read right to left, but English words, digits, and URLs inside them read left to right. A chat window that forces everything left to right draws the Arabic reply against the left edge and puts commas, periods, and list numbers on the wrong side. The fix is to let each message block pick its own direction, wrap anything that runs the other way so it cannot scramble its neighbors, and test those cases before every release.

## 2. What it looks like
Illustrative; I did not render this. The text below is shown in stored (logical) order. Your terminal or viewer may reorder it.

**Without the fix** (a U.S. online retailer; the customer lives in Dearborn, Michigan)
```
User: أين طلبي رقم 4471؟
Bot:  طلبك رقم 4471 سيصل يوم الثلاثاء. رقم التتبع: 1Z999AA10123456784
Screen: the bot message sits at the left edge of the bubble. The period and
        colon can land beside the wrong word. The tracking number sits in the
        middle of the sentence, so the user cannot tell where it starts.
User: لا أستطيع نسخ الرقم
```
("I can't copy the number.")

**With the fix**
```
User: أين طلبي رقم 4471؟
Bot:  طلبك رقم 4471 سيصل يوم الثلاثاء.
      رقم التتبع:
      1Z999AA10123456784
Screen: the message is right-aligned, because its first strong character is Arabic.
        Order number 4471 is isolated. The tracking number is on its own
        left-to-right line, so it can be selected and copied.
```
Same words. What changed: direction comes from the message itself, the number is isolated, and the code-like value gets its own left-to-right line.

## 3. Why it happens
- **The container forces left to right.** One Cursor user reports that Arabic chat replies show left to right even though the letters are shaped correctly, and a reply on that thread calls it a "known, long-standing issue." A forced direction on the whole chat panel is a common cause.
- **Punctuation and numbers have no direction of their own.** The Unicode algorithm gives neutral characters the direction of the surrounding text, and in a conflict the direction of the container. Chat replies are full of them: list numbers, colons, parentheses, names, order numbers.
- **Nobody tests it.** Our judgment: test conversations and review screenshots are in English, and the model's output is plain text with no direction information, so the first person to see the problem is the Arabic-speaking user.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The Unicode Bidirectional Algorithm decides display order from character types. "Generally, NIs take on the direction of the surrounding text. In case of a conflict, they take on the embedding direction." Isolates keep inner text from affecting outer order. The standard says markup should be used instead of explicit formatting characters where available. | [Unicode UAX #9](https://www.unicode.org/reports/tr9/). Opened (first 100,000 of 134,171 characters). | A standard, not evidence of how often chat products fail. I did not read the last part of the text. |
| An exclamation mark after an Arabic title in an English sentence shows on the wrong side. A rating like "AZZIP ELPRUP - 5 reviews" in a left-to-right page displays as "5 - AZZIP ELPRUP reviews." The fix is to set base direction and isolate names and numbers. | [W3C, Unicode Bidirectional Algorithm basics](https://www.w3.org/International/articles/inline-bidi-markup/uba-basics). Opened. | Web-page examples, not chat. The page does not mention `bdi` or `dir=auto`. |
| The HTML `bdi` element isolates text from its surroundings, its `dir` defaults to auto, and it is made for content like usernames. Without it, an Arabic username would move the colon and the number "3" next to the wrong word. | [W3C HTML author guide, bdi](https://www.w3.org/TR/html-author/the-bdi-element.html). Opened. | An older snapshot of the HTML guide; check the current HTML spec for exact wording. |
| One user reported Arabic chat replies in Cursor 3.7.19 on Windows 10 (posted June 9, 2026): left-aligned paragraphs, bullets on the left, numbered-step periods on the wrong side, misplaced commas, colons, dashes, and parentheses. The same text displays correctly when copied into Word or a browser. A reply the same day called it "a known, long-standing issue." | [Cursor forum thread](https://forum.cursor.com/t/arabic-rtl-chat-text-renders-with-broken-bidi-layout-on-windows/162815). Opened. | One user's report about one product. It shows the symptom exists, not how common it is. |
| Bidi control characters can make code display in a different order than it runs. The authors (Boucher and Anderson, USENIX Security 2023) track it as CVE-2021-42574 and advise making these characters visible or warning on unterminated ones. | [Trojan Source](https://trojansource.codes/). Opened. | About source code, not chat. I use it only as a reason to treat invisible direction characters in text as untrusted. I found no chat-specific case. |

Read through search summaries only, and not used in the fix: Claude Code issue reports about RTL text in code blocks, and suggestions to use `dir="auto"` or `unicode-bidi: plaintext` on chat messages. They are community reports and I did not open them.

**Public incident.** No dated public incident beyond the single forum report above. I ran four searches and found no incident report, study, or outage tied to this failure.

## 5. The fix
**The principle:** Each message block takes its direction from its own content, anything that runs the other way is isolated, and the result passes a render test.

**Do this**
1. **Set direction per block, not for the whole chat.** Each paragraph, list item, heading, and table cell gets its own base direction from its first strong character (for example `dir="auto"`). Check: an Arabic paragraph is right-aligned and its bullet and list number sit on the right; an English paragraph in the same reply stays left-aligned.
2. **Isolate embedded opposite-direction text.** Names, order numbers, product names, and amounts inside a sentence of the other direction are wrapped in an isolating element (for example `<bdi>`) or Unicode isolates. Check: in the test message "طلبك رقم 4471…", the number stays in place and the colon and period stay with the words they follow.
3. **Show code, URLs, commands, and IDs on a left-to-right line of their own.** Use a block or an inline code span that is itself left-to-right. Check: the tracking number reads left to right, is selectable, and does not split a sentence. (Our design choice. The standard's note that source code needs higher-level protocols supports it; I found no chat-specific test.)
4. **Use markup, not hidden direction characters, and strip stray ones.** Do not ask the model to insert U+202A through U+202E (embedding and override) or isolates to fix layout. Remove or flag unpaired ones in user input, model output, and retrieved text before display. Check: a message with an unterminated override character is shown with it removed or visible, and the rest of the layout is unchanged.
5. **Keep stored text in logical order.** Never reverse a string to make it look right. Check: the stored text and the text sent to the model equal what the user typed, character for character.
6. **Keep direction when text leaves the window.** Copy, share, and export carry the block direction and the isolated values (see [copy, share, and export lose content](../../chat-interface/failures/copy-share-and-export-lose-content.md)). Check: paste into a plain-text note and a document; the order of words and numbers matches the chat.
7. **Test every supported right-to-left script on each release.** Use the render cases in section 6 and report the pass rate.

**Reference design**
```
Render rules for chat messages
- Message container: no fixed direction. Chat chrome (menus, buttons) follows the UI language.
- Each block (p, li, h1-h6, td): dir=auto.
- Inline names, IDs, numbers, amounts from data or users: <bdi> or isolates.
- Code, URLs, tracking numbers, shell commands: left-to-right block or code span.
- Input and output sanitizer: remove or flag unpaired bidi controls (U+202A-202E, unterminated U+2066-2069).
- Do not convert digit style (1234 vs ١٢٣٤) unless the user asks.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The user says text looks scrambled. The bot cannot see its own display: say so, restate the key values on separate lines, and say where they are. |
| Offer choices: 2-4 options plus "Something else", free text open | After a "looks wrong" report: "Resend on separate lines", "Send as plain text", "Talk to a person", "Something else". |
| Hand off to a person | The same complaint a second time, or the user cannot read a value they must act on (an amount, a date, a code). |

**Don't over-correct.** Do not force right-to-left on the whole chat because the user's language is Arabic, and do not wrap every word in an isolate. A reply that is mostly English with one Arabic word stays left-aligned. Do not reverse or "fix" code, URLs, or numbers by hand. Do not change digit style on your own. The guardrail is the counter-metric: left-to-right messages must still pass.

**Hand-off rule.** The bot cannot repair its own display. On a second "looks wrong" report, log the message ID and hand off to a person with the stored text attached. Do not promise a fix date.

**Framework used:** [Unicode UAX #9](https://www.unicode.org/reports/tr9/) and the [W3C bidi guidance](https://www.w3.org/International/articles/inline-bidi-markup/uba-basics) for the rules above (opened; see section 4). They are not in the solutions library.

## 6. How to test it (short version)
Tests are **not yet run**. Run each with the real chat UI and a screenshot or DOM check, with a native reader reviewing the first release.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Reply fully in Arabic, 3-item numbered list | 1 | Right-aligned; numbers and bullets on the right |
| 2 | Arabic sentence with order number 4471 and a dollar amount | 2 | Number and amount stay in place; punctuation stays with its words |
| 3 | Hebrew sentence ending with an English product name and "!" | 1, 2 | The "!" sits at the sentence end side |
| 4 | Arabic reply with a 20-character tracking number | 3 | The number is on a left-to-right line and copies intact |
| 5 | User text containing an unterminated override character | 4 | Character removed or shown; neighboring text unaffected |
| 6 | Round-trip: type, send, read stored text | 5 | Stored text equals typed text |
| 7 | Copy the reply to a plain-text note | 6 | Order of words and numbers matches the chat |
| 8 | English-only reply (counter-test) | Don't over-correct | Left-aligned; no isolates added |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **RTL render-test pass rate** (primary) | 100% | Run the section 6 cases on each release and on any change to the chat UI; count passes | Any failure blocks release |
| Left-to-right messages wrongly shown right-to-left (counter-metric) | 0 in the test set | The English-only and mostly-English cases in the test set | Any occurrence |
| "Looks wrong" reports per 100 conversations with right-to-left text | Track; set from baseline | Count user turns matching the signals below | Rising |
| Unpaired bidi controls reaching the display | 0 | Sanitizer log of removed or flagged characters, shown vs. raw | Any shown unpaired |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A message with right-to-left characters renders with computed direction `ltr` | Render event: `computed_direction` vs. the message's script | A mostly English message with one Arabic word |
| User turn after a bot reply says text is backwards, scrambled, or "I can't copy the number" | Next-turn text match, in any language | A complaint about a wrong translation, not the layout |
| Unpaired U+202A-202E or U+2066-2069 in user, model, or retrieved text | Sanitizer log | A correctly paired isolate from a trusted source |
| User asks for the same value again, right after a reply that contained it | Same entity (order number, amount) requested in the next turn | The user wants it in another format |

**Starter rule:** every message block that contains right-to-left characters takes its own base direction, and every embedded number, name, or URL is isolated from the surrounding text.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: right-to-left-and-mixed-script-rendering
runs: pre_send
reads: [draft_reply.text, draft_reply.script, ui.render_profile, user_turns.text]
trigger: a draft reply contains right-to-left characters, or the user reports scrambled text
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Resend on separate lines", "Send as plain text", "Talk to a person", "Something else"]
on_miss: rewrite
metric: RTL render-test pass rate
counter_metric: left-to-right messages wrongly shown right-to-left
status: proposed
```

## 8. Related patterns
- [Copy, share, and export lose content](../../chat-interface/failures/copy-share-and-export-lose-content.md): the closest page in the library. It covers tables, code, and links lost when a reply leaves the chat window. This page covers how text is drawn inside the window, and only touches export in rule 6.
- [Input locale mismatch](../../../../../cross-cutting/operations/goals/input-output-handling/failures/input-locale-mismatch.md): the agent reads a date or number with the wrong locale rules. Here the value is right and the display is wrong.
- [Multilingual code-switching](../../../../speech-and-audio/goals/conversation-flow/failures/multilingual-code-switching.md): the bot misunderstands a message that mixes languages. Here it understands and still displays it wrongly.
- [Mobile keyboard or screen hides the reply](../../chat-interface/failures/mobile-keyboard-or-screen-hides-the-reply.md): layout hides the reply. Here the reply is visible but wrongly laid out.
- Neighbors in the [language and locale roadmap](../../../roadmap/language-and-locale.md): locale format errors (LG-08) and name and transliteration errors (LG-09) are about content, not drawing.

## 9. Common questions
### Why does my chatbot show Arabic or Hebrew text backwards or left-aligned?
Most often the chat container has a fixed left-to-right direction, so punctuation and numbers take their direction from it. Set the direction per block (see [rule 1](#5-the-fix)). One reported case is in [section 4](#4-why-it-matters).

### Should I set the whole chat to right-to-left for Arabic users?
No. Interface chrome can follow the UI language, but each message should follow its own content, or a mixed or English reply will be wrong.

### Can the model fix this by adding special characters?
Not reliably, and it is risky. The standard says markup is preferred over explicit formatting characters, and invisible direction characters can make displayed text differ from stored text. Strip stray ones instead (rule 4).

### How do I test right-to-left text in a chat UI?
Use the cases in [section 6](#6-how-to-test-it-short-version) with real screenshots or DOM checks, and have a native reader review the first release.

---
## Technical section

### T1. Solution architecture
```
model/user/retrieved text -> sanitizer (strip or flag unpaired bidi controls)
                          -> markdown renderer (dir=auto per block, bdi for data values,
                                                LTR code spans and blocks)
                          -> chat UI (no fixed container direction)
                          -> render test (screenshot or DOM assertion) in CI
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Direction per block | Renderer | Tests 1, 3 |
| Isolate embedded data | Template and renderer | Tests 2, 3 |
| LTR for code and IDs | Renderer | Test 4 |
| No stray bidi controls | Sanitizer | Test 5 |
| Logical order stored | Storage layer | Test 6 |

### T3. Evals
- **Dataset:** start with the 8 cases in section 6, then add 30-50 real-shaped replies (lists, tables, links, amounts, code) in each supported right-to-left script. These counts are my suggestion, not sourced.
- **Judge rubric:** a native reader checks alignment, order of words and numbers, and punctuation side.
- **Metrics and starting thresholds:** pass rate 100%; counter-metric 0. Starting points to tune.
- **Release gate:** block a release on any failed case.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Render-test failure | Any in CI | Failure on production build | Roll back the UI change |
| Unpaired bidi control shown | Any | Repeated | Check sanitizer and source of the text |

### T5. Trade-offs
- Per-block direction needs a renderer you control; a third-party chat widget may not allow it.
- Browsers and apps differ; test on the ones your users have, including mobile.

---
### Deep dive
- **Open question.** I found no benchmark of how often production chat UIs get this wrong, and no test of the proposed fixes on a real chat UI.
- **Edge cases not covered:** tables with mixed columns, right-to-left text in code blocks, and bidi in voice transcripts (voice is PLANNED).
- **References.** [Unicode UAX #9](https://www.unicode.org/reports/tr9/) (opened, partly); [W3C bidi basics](https://www.w3.org/International/articles/inline-bidi-markup/uba-basics) (opened); [W3C bdi](https://www.w3.org/TR/html-author/the-bdi-element.html) (opened); [Cursor forum report](https://forum.cursor.com/t/arabic-rtl-chat-text-renders-with-broken-bidi-layout-on-windows/162815) (opened); [Trojan Source](https://trojansource.codes/) (opened).
