# Why Does AI Use Emojis in READMEs and UI Icons? Emoji as Icons and Decorative Bullets

<!-- SEO
title: Why Does AI Use Emojis in README and UI Code? How to Stop It
description: AI tools put rockets and sparkles on headings, bullets and buttons. Screen readers read the names. Use real icons, hide decoration, scan each diff.
search phrases:
- why does ai use emojis in readme
- why does chatgpt use so many emojis
- stop claude code from using emojis
- emoji icons accessibility screen reader
- emoji in commit messages ai
- should i use emoji as icons in react
- ai generated readme emoji headings
-->

**Frequency**: Common

## Issue: AI tools put emoji on headings, bullets and buttons in UIs, READMEs and commits; screen readers read their names, and the output looks unreviewed.

> **One line:** The AI uses a rocket or a check mark where a real icon, a word, or nothing belongs, and nobody checks before it ships.

| | |
|---|---|
| **Channel** | Written for **generated UI code, docs, commit messages and code comments**. Chat replies are covered by [accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md) (rule 4). |
| **Stakes** | Low to medium. Higher when an emoji is the only sign of status or severity, or when the file must run on a Windows console. |
| **Who is affected** | Screen-reader users, readers of docs sent to customers, and developers whose scripts break on emoji |
| **Frequency** | Common. Reported by users in the Claude Code issue tracker and named as a sign of AI text in a Wikipedia editors' guide (section 4). I found no count across tools. |
| **Pattern ID** | ui-emoji-as-icons |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Emoji-clean file rate: share of generated UI files, docs and commit messages in a checker run with no emoji used as an icon, bullet, heading prefix or status mark. Target 100%. A proposed starting point; there is no catalog row yet. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. The Wikipedia guide says the habit is rarer in newer chatbots, but a 2026 issue reports emoji written into files on a current Claude Code version despite a project rule. A diff check is what makes it hold. (Our judgment, not tested.) |
| **Also searched as** | AI README rocket emoji · emoji bullets AI tell · Cursor adds emojis to code · emoji icon button accessible name · aria-hidden emoji · emoji UnicodeEncodeError Windows |

## 1. In plain words
You ask v0, Lovable, Bolt, Cursor, Claude or ChatGPT for a page or a README. It comes back with a sparkles emoji on every heading, a rocket on "Getting Started", check marks as bullets, and a trash-can emoji as the delete button. Sighted readers see a template nobody edited. Screen-reader users may hear "rocket" before each line, or nothing useful on a button. The fix: use the project's icon set, hide decorative icons, name icon-only buttons, write words for status, and scan every diff for emoji before it ships.

## 2. What it looks like
**Without the fix**
```
Builder: Build a features section and README for TaskFlow, our to-do app.
Tool:    <h2>✨ Why TaskFlow?</h2>
         <li>🚀 Fast sync</li>
         <li>✅ Works offline</li>
         <button>🗑️</button>
         README.md:  ## 🚀 Getting Started   ## ✨ Features   | Offline | ✅ |
         git commit -m "✨ Add features section 🎉"
Checker: (none; it ships)
```
**With the fix**
```
Builder: Build a features section and README for TaskFlow. Follow the emoji rules in CLAUDE.md.
Tool:    <h2>Why TaskFlow?</h2>
         <li><SyncIcon aria-hidden="true" /> Syncs between your phone and laptop</li>
         <li><OfflineIcon aria-hidden="true" /> Works offline</li>
         <button aria-label="Delete task"><TrashIcon aria-hidden="true" /></button>
         README.md:  ## Getting started   ## Features   | Offline | Yes |
         git commit -m "Add features section to home page"
Checker: Emoji scan: 0 found in 3 changed files and 1 commit message.
```
The fixed output uses the icon set, hides decorative icons, names the icon-only button by its action, writes "Yes" in the table, and the checker reports the scan result.

## 3. Why it happens
Our reading of the pattern, with the issue reports in section 4 as support.
- **An emoji is the cheapest icon.** It is one text character: no import, no icon package, no asset path. A tool asked for a working page in one shot can "add icons" without touching dependencies.
- **Chat style leaks into files.** The same model writes the chat reply and the file. One Claude Code issue asks for an ASCII default on file writes, separate from chat style, because a user who likes emoji in chat rarely wants them in a Python comment.
- **The rule is an instruction, not a check.** Issue reporters say a "no emoji" rule in CLAUDE.md holds early in a session and then drifts, and nothing scans the diff.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| WCAG 1.1.1 says pure decoration must be "implemented in a way that it can be ignored by assistive technology." | [W3C, *Understanding SC 1.1.1 Non-text Content*](https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html). Opened and read. | A standard, not a study. It does not name emoji. |
| Browsers do not always expose an emoji as an image or give it a name, so a screen-reader user may not know it is there; the fix is `role="img"` plus an `aria-label`. | [Léonie Watson, *Accessible emoji*, 2016](https://tink.uk/accessible-emoji/). Opened and read. | An expert's post from 2016. Browser behavior may have changed since. |
| A screen reader reads the emoji's official name, not the intent (a "thank you" emoji is read as "Hands pressed together"); long emoji strings add listening load; icon-only buttons need a name that says the action; an `aria-label` on a `span` needs `role="img"`; labels should be five words or less. | [Pope Tech, *Making emojis and icons screen reader accessible*, April 2026](https://blog.pope.tech/2026/04/01/making-emojis-and-icons-screen-reader-accessible/). Opened and read. | Vendor blog (Pope Tech offers accessibility scanning). The five-word limit is their advice, not a standard. |
| The jsx-a11y `accessible-emoji` lint rule, which required `role="img"` and a label on emoji, is marked deprecated; it cites WCAG 1.1.1. | [eslint-plugin-jsx-a11y docs](https://github.com/jsx-eslint/eslint-plugin-jsx-a11y/blob/main/docs/rules/accessible-emoji.md). Opened and read. | The doc does not say why it was deprecated. Do not rely on it as your check. |
| Wikipedia's editor guide says AI chatbots sometimes decorated section headings or bullet points by putting emoji in front of them, and that this is rarer now. | [Wikipedia, *Signs of AI writing*, "Emoji as formatting"](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing). Opened (page source) and read. | A volunteer guide about Wikipedia edits, not UI code. It cites a Washington Post analysis I did not open. |
| A vendor delivering docs to a bank reports about 370 emoji across eight documents in one session, including severity shown as colored circles and Yes/No as tick and cross marks, all stripped before the docs could be sent. | [anthropics/claude-code issue #82257, July 2026](https://github.com/anthropics/claude-code/issues/82257). Opened and read. | One customer's report. Closed; I did not see the resolution. |
| A user reports Claude Code wrote emoji into a Python comment, a doc and commit messages despite an explicit CLAUDE.md ban; one 420-line file collected five; each failed on a cp1252 Windows console. | [anthropics/claude-code issue #84197, August 2026](https://github.com/anthropics/claude-code/issues/84197). Opened and read. | One reporter. Open when I read it. |
| Emoji in generated Python print statements, comments and strings caused `UnicodeEncodeError` on Windows cp1252. | [anthropics/claude-code issue #7582, September 2025](https://github.com/anthropics/claude-code/issues/7582). Opened and read. | One feature request; closed. |

I found no study that measures how often v0, Lovable, Bolt, Cursor or Copilot output contains emoji icons. A search result said GitHub drops emoji from heading anchor IDs; I read that only in a summary, so it is not used here.

## 5. The fix
**The principle:** Icons come from the icon set, decoration is hidden from screen readers, meaning is carried by words, and a scan of every diff proves it.

**Do this**
1. **No emoji as UI icons.** Every icon in generated UI is a component or SVG from the project's icon set. Check: no emoji character in a JSX or HTML text node next to a label, or alone inside a `button` or `a`.
2. **Hide decorative icons.** An icon next to visible text has `aria-hidden="true"`.
3. **Name icon-only controls by their action.** A button with no visible text has an `aria-label` that states the action ("Delete task", not "Trash"), five words or less.
4. **Label an emoji that must stay as content.** If an emoji is real content (a reaction the user picked, a brand mark in copy), wrap it as `<span role="img" aria-label="Thumbs up">`, with the label naming what it means.
5. **No emoji as list markers, heading prefixes or separators** in READMEs, docs, release notes, code comments, log strings or commit messages.
6. **Words for status.** Write "Yes", "No", "Passed", "High". Never a check mark, cross or colored circle as the only sign. See [color-only encoding](../../visual/failures/colour-only-encoding.md).
7. **Enforce with a check, not only a prompt.** Run an emoji scan on changed files and the commit message at pre-commit and in CI; the scan result is reported in the PR.

**Reference design: project rule plus scan table**
```
Emoji rules (put in CLAUDE.md, .cursorrules, AGENTS.md or the tool's custom instructions):
- Never use emoji in code, UI, docs, comments, logs or commit messages. Say the word instead.
- For icons, import from src/icons. Add aria-hidden="true" when text is next to the icon.
- An icon-only button gets aria-label naming the action in five words or less.
- Status in tables and lists is a word: Yes, No, Passed, Failed, High, Low.
- In chat with me, match my style: use emoji only if I do.
```
| Check | Where | Fails when |
|---|---|---|
| Emoji scan of added lines (JS regex `/\p{Extended_Pictographic}/u`) | Pre-commit and CI, on `*.tsx`, `*.jsx`, `*.html`, `*.md`, `*.py` | Any match outside an allow-listed file (Unicode test fixtures, user-content seed data) |
| Commit message scan | `commit-msg` hook | Any match |
| Icon-only control has a name | Component test or axe run | `button` or `a` with no text and no `aria-label` |
| Decorative icon hidden | Review or lint | Icon next to text without `aria-hidden="true"` |
| Status cell is a word | Doc review | A cell holds only a check mark, cross or colored circle |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Adapted: here the "conversation" is the builder prompting the AI tool, or the checker reporting to the builder.
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The checker report opens with the count and the file:line of each emoji, then the fix, not a lecture. |
| Offer choices: 2-4 options plus "Something else", free text open | For each hit: "Replace with icon from src/icons", "Delete it", "Keep and label it (content emoji)", "Something else". |
| Ask one clarifying question | The brand guide uses emoji on purpose in marketing copy: the tool asks once whether that applies here, instead of stripping or adding by guess. |
| Hand off to a person | An emoji carries meaning in user content or in a status design: send it to the accessibility reviewer. |

**Don't over-correct.** Emoji are fine in casual chat when the user uses them; do not lecture a user who sends one. Do not strip emoji from user content, reactions, names or messages people wrote; label them instead. Do not delete emoji from Unicode test fixtures or data the app must handle; allow-list those files. Do not replace every emoji with an icon; often the right fix is no icon at all.

**Hand-off rule.** When an emoji is real content or a brand asks to keep emoji in the UI, a person who uses or tests with a screen reader checks the labeled result before release. See the [accessibility family](../../accessibility/README.md).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Ask the tool for a features section "with icons" | Icons come from the icon set; no emoji in text nodes | 1 |
| 2 | Same output, icon beside a label | Icon has `aria-hidden="true"` | 2 |
| 3 | Ask for a delete button with only an icon | `aria-label` names the action in five words or less | 3 |
| 4 | Build a chat where users pick emoji reactions | Reactions keep their emoji, wrapped with `role="img"` and a label | 4 |
| 5 | Ask for a README for a new CLI | No emoji on headings, bullets or separators | 5 |
| 6 | Ask for a test-results table | Cells say Passed or Failed, no check marks alone | 6 |
| 7 | Long session: 20 edits after the rule is set | Pre-commit scan blocks any emoji; PR shows the scan result | 7 |
| 8 | User writes to the tool with emoji in chat | Chat reply may use emoji; written files still pass the scan | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Emoji-clean file rate** (primary) | 100% | Emoji scan over changed UI files, docs and commit messages per PR; files with no hit / files scanned | Below 95% |
| Icon-only controls with no accessible name | 0 | axe run or component test on generated pages | Any |
| Decorative icons not hidden | 0 | Lint or sampled review of 20 generated components a month | Any in a sample |
| Status shown only by a symbol | 0 | Sampled review of generated tables and docs | Any |
| Late-session emoji hits | Track; set from baseline | Scan hits per commit, by commit order in the session | Rising after the first 10 commits |
| Content emoji stripped (counter-metric) | 0 | Diffs that remove emoji from user content or allow-listed fixtures | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a diff or checker run that suggest this failure. Proposed until checked against human-labeled reviews.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Emoji as the first character of a Markdown heading or list item | Added lines in `*.md` | A changelog style the team chose on purpose |
| Emoji alone inside a `button` or `a` with no `aria-label` | Added JSX or HTML | A labeled reaction picker the builder asked for |
| Emoji in a commit message or code comment | `commit-msg` hook, added comment lines | A commit that fixes emoji handling and quotes one |
| Check mark, cross or colored circle as a table cell's only content | Added Markdown or HTML tables | A legend nearby that also gives the word |
| Scan hits rise later in a session after a no-emoji rule | Hits per commit by order | One large late commit that touches many files |

**Starter rule:** no emoji in generated UI code, docs, comments or commit messages, enforced by a scan of every diff.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ui-emoji-as-icons
runs: pre_send
reads: [diff.added_lines, diff.file_type, commit.message, element.aria_label, element.aria_hidden, allowlist.files, session.user_used_emoji]
trigger: the AI tool writes a file or commit, and the scan finds an emoji outside an allow-listed file
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Replace with icon from src/icons", "Delete it", "Keep and label it", "Something else"]
on_miss: rewrite
metric: emoji-clean file rate
counter_metric: content emoji stripped
status: proposed
```

## 8. Related patterns
- [Accessibility in chat](../../fairness-and-identity/failures/accessibility-in-chat.md): the closest existing page. Its rule 4 limits emoji in **chat replies** for screen-reader users. This page covers emoji written into **UI code, docs and commits** as an AI tell, and the diff check that catches it.
- [Color-only encoding](../../visual/failures/colour-only-encoding.md): status by color alone; colored-circle emoji are one form of it.
- [Visual accessibility gaps](../../visual/failures/accessibility-gaps.md): missing text alternatives across the visual layer.
- [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md): too much structure in replies; emoji bullets often ride along.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): emoji and cheer on serious topics.
- Siblings in this family: [default gradient look](./ui-default-gradient-look.md), [template card grids](./ui-template-card-grids.md) (icon-in-circle rows), [generic hero layout](./ui-generic-hero-layout.md), [placeholder data left in](./ui-placeholder-data-left-in.md), [fabricated social proof](./ui-fabricated-social-proof.md).

## 9. Common questions
### Why does AI use so many emojis in READMEs?
An emoji is a one-character "icon" that needs no assets, and chat-style habits carry into files. A Wikipedia editors' guide lists emoji on headings and bullets as a sign of AI writing. Ask for none, then scan the diff (section 5).

### How do I stop Claude Code or Cursor from adding emojis?
Put the rule in CLAUDE.md, .cursorrules or AGENTS.md, and add a pre-commit and commit-msg scan. Users report the instruction alone drifts during long sessions, so the scan is what holds.

### Are emoji icons bad for accessibility?
They can be. A screen reader may read the emoji's name, which often does not match the intent, or may skip it. A decorative icon should be hidden, and an icon-only button needs a name that says the action.

### Should I use emoji as icons in React?
Use your icon set instead. If an emoji is real content, wrap it in a `span` with `role="img"` and an `aria-label`. The old jsx-a11y emoji rule is deprecated, so do not count on it.

### Is it fine to use emoji in chat?
Yes, when the user does and the topic is light. Keep them out of files, and out of serious topics ([stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md)).
