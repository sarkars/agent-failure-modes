# AI Ignores My Design System: No Locked Design Tokens, So Every Page Drifts to Defaults

<!-- SEO
title: AI Ignores My Design System: Lock Design Tokens in the Repo
description: AI coding tools invent hex and px values on every page when no token file is locked. Lock tokens, point the rules file at them, lint raw values.
search phrases:
- ai coding tool ignores design system
- cursor not using my design tokens
- claude code hardcoded hex colors
- how to make ai follow design tokens
- stylelint disallow hex colors outside variables
- tailwind remove default colors theme
- design tokens in CLAUDE.md or cursor rules
- ai generated components inconsistent spacing
-->

**Frequency**: Common

## Issue: When a codebase has no single locked source of design tokens, each AI-generated page invents its own hex, spacing and radius values and drifts toward the tool's defaults. Lock tokens in the repo, point the tool's rules file at them, and lint for raw values outside the token file.

> **One line:** The settings page an AI tool built in March uses `#1D4ED8` and 16px padding; the appointments page it built in May uses `#2563EB`, `p-[18px]` and `rounded-xl`, and nobody chose either; the fix is one token file the tool must read, a rules file that names it, and a lint step that fails any raw color, size or radius outside it.

| | |
|---|---|
| **Channel** | **Visual**: web UIs built over weeks or months with AI coding tools (Cursor, Claude Code, GitHub Copilot and similar) in a shared repo. Native mobile is PLANNED, not written. |
| **Stakes** | Low to medium. Pages look slightly off from each other, then visibly unbranded. Stakes rise when drift breaks contrast or makes a primary button look like a secondary one. |
| **Who is affected** | Developers and designers maintaining an AI-assisted codebase; users who see two shades of "brand blue" on one screen |
| **Frequency** | Common, in our judgment. Design-tool vendors describe it as a common failure (section 4); I found no count across teams or tools. |
| **Pattern ID** | ui-no-locked-design-tokens |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Share of merged UI pull requests that add a raw color, spacing, font-size or radius value outside the token file with no recorded exception. Proposed starting target: 0%, alert above 2% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. A stronger model follows a rules file more often, but Claude Code's own docs say instruction files are "context, not enforced configuration", so only a lint or build check makes the tokens binding. (Our judgment, not tested.) |
| **Also searched as** | ai keeps hardcoding colors · cursor rules design system · tailwind theme only custom colors · lint for hex values · design tokens json ai |

## 1. In plain words
A design token is a named value, such as `color.brand` or `space.4`, that every screen uses instead of a raw number. If your repo has no single token file, or has one the AI tool is never told about, each new page is a blank. The tool fills it with whatever value looks right in that moment, often a framework default. Each page looks fine alone. Side by side, the colors, gaps and corners no longer match, and the site starts to look like a stock AI build.

**How this differs from the closest pattern.** [The default gradient look](./ui-default-gradient-look.md) says "give the tool brand tokens" so one generated screen is not purple. This page is about the codebase over time: where the tokens live, how every tool session is pointed at them, and what check stops the fortieth page from drifting after everyone has forgotten the first prompt.

## 2. What it looks like
**Without the fix** (Lakeview Dental, a Chicago clinic chain; colors live in old components and a Figma file)
```
Dev:   Add an appointments page that matches the rest of the app.
Tool:  Done. Header text-[#2563EB], cards p-[18px] rounded-xl shadow-md,
       body text-[15px] text-gray-600.
Dev:   Looks close enough. Merge.
       (Settings page, built in March: #1D4ED8, p-4, rounded-lg, text-base.
       Lint passes; no rule checks values. The practice manager asks why
       the "Book" button is a different blue on two pages.)
```
**With the fix** (tokens locked in `styles/tokens.css`, rules file names it, lint in CI)
```
Dev:   Add an appointments page that matches the rest of the app.
Tool:  Using tokens from styles/tokens.css per CLAUDE.md: text-brand, p-4,
       rounded-card, text-body. I need a spacing of 18px for the time grid;
       it is not in the scale. Use space-4 (16px) or add a token?
Dev:   Use space-4.
CI:    stylelint and eslint: 0 raw colors, 0 arbitrary values. Pass.
```
The tool was pointed at one file, asked instead of inventing a value, and CI checked what came back.

## 3. Why it happens
- **No single source exists.** Colors sit in a Figma file, a few old components and someone's memory. The tool can only copy what it reads, so it copies the nearest component, or the framework default when none is open.
- **The rules file does not name the tokens, or is not read.** Each session starts fresh. If `CLAUDE.md`, `AGENTS.md` or `.cursor/rules` does not say "use only `styles/tokens.css`", the tool has no reason to. Claude Code's docs say these files are context, not enforcement; a stray `.md` in `.cursor/rules` is ignored because Cursor needs `.mdc` (section 4).
- **The framework still offers every default, and nothing fails on raw values.** Tailwind ships a full palette and allows arbitrary values like `p-[18px]`. Unless the default namespace is reset and a lint rule bans raw values, an off-token class builds, renders and passes review.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Claude Code loads CLAUDE.md at the start of every session, treats it "as context, not enforced configuration", says specific and concise instructions are followed more consistently, and recommends under 200 lines per file. Files can import others with `@path/to/import`, and `.claude/rules/` files can be scoped to paths. | [Anthropic, *How Claude remembers your project*](https://code.claude.com/docs/en/memory). Opened and read (Oct. 2026). | Vendor docs for one tool. Supports "rules file is not enough", not a failure rate. |
| Cursor project rules live in `.cursor/rules`, must use the `.mdc` extension (a plain `.md` there is ignored), can apply always or by file glob, and should stay under 500 lines. Cursor also reads `AGENTS.md`. Referenced files are not inlined into the prompt. | [Cursor docs, *Rules*](https://cursor.com/docs/context/rules). Opened and read (Oct. 2026). | Vendor docs; behavior can change between releases. |
| Tailwind calls theme variables its store for design tokens. Setting `--color-*: initial` in `@theme` removes default utilities like `bg-red-500`; `--*: initial` removes all theme-driven defaults. | [Tailwind CSS docs, *Theme variables*](https://tailwindcss.com/docs/theme). Opened and read. | Framework docs. That arbitrary values such as `p-[18px]` still work after a reset is our reading, not stated there. |
| The W3C Design Tokens Community Group published its first stable format, 2025.10, on Oct. 28, 2025, and names Style Dictionary, Tokens Studio and Terrazzo as reference implementations. The report itself says it "is not a W3C Standard nor is it on the W3C Standards Track" and recommends `.tokens` or `.tokens.json` files. | [DTCG announcement](https://www.w3.org/community/design-tokens/2025/10/28/design-tokens-specification-reaches-first-stable-version/) and [Format Module 2025.10](https://www.w3.org/community/reports/design-tokens/CG-FINAL-format-20251028/). Both opened; the format report read in part (first 100,000 of 113,144 characters). | A community spec, not a W3C standard; says nothing about AI tools. |
| Stylelint's core `color-no-hex` rule disallows hex colors. The `stylelint-declaration-strict-value` plugin flags raw values such as `color: #FFF` on chosen properties and passes `var(--color-white)`. | [Stylelint, color-no-hex](https://stylelint.io/user-guide/rules/color-no-hex/); [stylelint-declaration-strict-value README](https://github.com/AndyOGo/stylelint-declaration-strict-value). Both opened and read. | Tool docs. A third-party plugin; check it supports your Stylelint version. |
| `eslint-plugin-tailwindcss` has a `no-arbitrary-value` rule, off by default, for teams that want developers to "stick with the values" in the theme. | [no-arbitrary-value rule docs](https://github.com/francoismassart/eslint-plugin-tailwindcss/blob/master/docs/rules/no-arbitrary-value.md). Opened and read. | Community plugin. It bans all arbitrary values, not only colors. |
| A designer who sells a Figma token plugin writes that AI coding tools without token structure produce "UI that guesses spacing, color, and type", that spacing is missed more often than color, and that semantic aliases often collapse to a literal hex. | [Vitalina Makus, Atomize, May 12, 2026 (updated July 27, 2026)](https://atomize.tools/blog/figma-design-tokens-vibe-coding/). Opened and read. | Vendor, single source. The article says its patterns "reflect team reports, not a published benchmark". No numbers. |

**Read only in search summaries.** Biome's `noTailwindArbitraryValue` rule (in its nursery group) and several vendor posts (UXMagic, DEV Community, a Substack) recommending token lint plus a rules file. I did not open them and make no claim from them. **Not found:** any study counting off-token values in AI-generated code, or a dated public incident.

## 5. The fix
**The principle:** Tokens live in one file in the repo, every tool session is told to use only that file, and CI fails anything that bypasses it.

**Do this**
1. **One token source, in the repo.** Colors, type scale, spacing, radius and shadows live in one file (for example `styles/tokens.css`, a Tailwind `@theme` block, or a `.tokens.json` built by Style Dictionary). Figma and old components are not sources.
2. **Remove the framework defaults you do not use.** In Tailwind v4, reset the namespaces you own (`--color-*: initial`, and spacing or radius if you define your own scale) so `bg-blue-600` no longer exists.
3. **The rules file names the token file.** `CLAUDE.md`, `AGENTS.md` and `.cursor/rules/*.mdc` each say "use only tokens from `styles/tokens.css`" in one short, specific line. Because Cursor does not inline referenced files, put the token names themselves in the rule, or keep the list short enough to paste.
4. **No raw value outside the token file.** Any hex, `rgb()`, `px` or `rem` literal for color, spacing, font-size or radius in a component fails lint. In CSS, use `color-no-hex` plus `declaration-strict-value`; in Tailwind markup, enable `no-arbitrary-value`.
5. **A missing value is a question, not an invention.** When no token fits, the tool asks: use the nearest token, or add a new one to the token file in its own commit.
6. **Exceptions are written down.** A raw value can stay only with an inline lint-disable comment that gives a reason, and CI counts them.
7. **Recheck after rules or model changes.** When the rules file, the tool or the model changes, regenerate one sample page and confirm zero lint flags.

**Reference design: rules block** (same text in `CLAUDE.md`, `AGENTS.md` and `.cursor/rules/tokens.mdc` set to Always Apply)
```
Design tokens: styles/tokens.css is the only source of colors, type sizes, spacing, radius and shadows.
Use token utilities only: text-ink, text-brand, bg-paper, p-2 p-4 p-6, rounded-card, text-body, text-title.
Never write hex, rgb(), px or rem values for these, and never use Tailwind arbitrary values like p-[18px].
If no token fits, stop and ask: nearest token, or add a token in a separate commit.
```

**Reference design: lock and lint** (copy and adjust names)
```css
/* styles/tokens.css */
@import "tailwindcss";
@theme {
  --color-*: initial;
  --color-ink: #1B2430;  --color-paper: #F7F8FA;  --color-brand: #1D4ED8;
  --radius-card: 0.5rem;
}
```
`.stylelintrc.json`: raw hex fails everywhere except the token file.
```json
{ "plugins": ["stylelint-declaration-strict-value"],
  "rules": { "color-no-hex": true,
    "scale-unlimited/declaration-strict-value": [["/color$/", "font-size", "border-radius"],
      { "ignoreValues": ["inherit", "transparent", "currentColor", "0", "1px", "100%"] }] },
  "overrides": [{ "files": ["styles/tokens.css"], "rules": { "color-no-hex": null } }] }
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Here the "conversation" is the builder prompting the AI tool, or CI reporting to the builder. The moves are adapted, and the fit is our judgment.
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The tool needs a value that is not a token: "Use space-4 or add a token?" |
| Offer choices: 2-4 options plus "Something else", free text open | CI flags a raw value: "Swap to nearest token", "Add a token in its own commit", "Keep it: record the reason", "Something else". |
| Admit uncertainty and show how to check | The tool cannot read the token file (wrong path, not loaded): it says so and names the file it expected, instead of guessing values. |
| Hand off to a person | A new color or a change to the scale is requested (see hand-off rule). |

**Don't over-correct.** Do not ban every number: `0`, `1px` hairlines, `100%` and grid fractions are fine, so list them in `ignoreValues`. Do not tokenize one-off values for a single chart or illustration; scope the lint to UI components. Do not let the token file grow a new entry for every value the tool asks for, or the drift just moves into the token file.

**Hand-off rule.** Adding or changing a color, a type size or a step in the spacing scale needs a named designer or design-system owner to approve the token-file commit. The tool and CI never add tokens on their own.

**Framework used:** none yet.

## 6. How to test it (short version)
Catalog tier: no full test file yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Fresh session, "add a billing page", rules file present | Output uses only token utilities; zero lint flags | 1, 3, 4 |
| 2 | Generated component with `text-[#2563EB]` and `p-[18px]` | CI fails and names both lines | 4 |
| 3 | Markup uses `bg-blue-600` after the color namespace reset | No style is generated for it; the sample-page review catches the unstyled element | 2 |
| 4 | Design needs an 18px gap with no matching token | Tool asks before writing; no raw value lands | 5 |
| 5 | Raw value kept with a lint-disable comment and reason | CI passes and counts one exception | 6 |
| 6 | Rules file renamed to `.cursor/rules/tokens.md` | Sample page regenerated; drift caught and file fixed to `.mdc` | 3, 7 |
| 7 | `1px` border and `100%` width in a component | No flag (over-correction check) | 4 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Merged UI PRs adding raw values with no recorded exception** (primary, proposed) | 0% | CI lint log per PR: PRs with any raw color, size or radius flag merged without a reason, divided by merged UI PRs | Above 2% |
| Distinct color values in shipped CSS | No more than the token count | Parse built CSS; count unique color values not defined in the token file | Any above token count |
| Lint exceptions per 1,000 lines of UI code | Track; set from baseline | Count `stylelint-disable` and `eslint-disable` comments for token rules | Rising three releases in a row |
| Tool asks before adding a value | 100% of off-scale needs | Sampled review of 20 tool sessions a month | Any silent raw value |
| New tokens added without owner approval (counter-metric) | 0 | Token-file commits with no approval from the design-system owner | Any |

### Detection signals (proposed, not yet calibrated)
Signals in generated code, CI logs and the repo. Treat them as proposed until checked against human-labeled diffs.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Hex or `rgb()` literal in a component file | Diff of the generated change | A chart or illustration file scoped out of the lint on purpose |
| Tailwind arbitrary values (`p-[18px]`, `text-[15px]`) in markup | Class list in the diff | A one-off layout value with a recorded exception |
| Two near-identical brand colors in built CSS (for example `#1D4ED8` and `#2563EB`) | Built CSS color inventory | A documented hover or pressed state token |
| Rules file lacks the token path, or sits in an ignored location | Repo scan of `CLAUDE.md`, `AGENTS.md`, `.cursor/rules` | The team uses a design-system package that its rules name instead |
| Default palette utilities (`bg-blue-600`, `gray-*`) in new code | Class list in the diff | The team adopted Tailwind defaults as its tokens on purpose |

**Starter rule:** every merged UI change uses only values from the token file, and any raw color, size or radius value fails CI until it carries a written reason.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ui-no-locked-design-tokens
runs: pre_send   # in the tool session before code is written, and in CI before merge
reads: [rules_file, design_tokens, generated_css, class_names, lint_report, pr_note.reason]
trigger: generated UI code is about to be written or merged
moves: [ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Swap to nearest token", "Add a token in its own commit", "Keep it: record the reason", "Something else"]
on_miss: ask
metric: merged UI PRs adding raw values with no recorded exception
counter_metric: new tokens added without owner approval
status: proposed
```

## 8. Related patterns
- [AI generated website purple gradient](./ui-default-gradient-look.md): the closest existing pattern. It fixes one screen's default look by handing the tool a palette. This page makes the palette binding across the whole codebase: one file, rules that point at it, and CI that fails on bypasses.
- [Generative UI instability](../../visual/failures/generative-ui-instability.md): components a chat model picks at run time that jump or break. This page is about code generated at build time across many sessions.
- [Identical card grids and icon-in-circle rows](./ui-template-card-grids.md): the layout default that often ships alongside off-token values.
- [Needless abstraction in AI code](./code-needless-abstraction.md): the code-side cousin, where the tool adds structure instead of reusing what the repo has.
- [Brand consistency in content marketing](../../../../../by-use-case/content-marketing/goals/brand-consistency/README.md): the same drift for voice and wording rather than visual values.

## 9. Common questions
### Why does Cursor or Claude Code ignore my design system?
Usually because nothing tells it where the system is, or the instruction is not loaded. Name the token file in `CLAUDE.md`, `AGENTS.md` or a `.mdc` rule, and remember these files guide the tool but do not enforce anything (section 4).

### How do I make AI use my design tokens?
Keep one token file in the repo, list the token names in the tool's rules file, and tell it to ask when no token fits. Then add lint rules so a raw value fails CI (section 5).

### How do I stop hardcoded hex colors in CSS?
Turn on Stylelint's `color-no-hex` and the `declaration-strict-value` plugin for color properties, with the token file excluded. For Tailwind markup, enable `no-arbitrary-value` in `eslint-plugin-tailwindcss`.

### How do I remove Tailwind's default colors?
In Tailwind v4, put `--color-*: initial;` in your `@theme` block, then define your own colors. The default color utilities such as `bg-red-500` are removed (Tailwind docs).

### Is there a standard format for design tokens?
The W3C Design Tokens Community Group published a stable format, 2025.10, in October 2025. It is a community group report, not a W3C Standard, and tools such as Style Dictionary implement it.
