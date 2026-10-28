# AI Generated Landing Page Looks Generic: Identical Card Grids and Icon-in-Circle Feature Rows

<!-- SEO
title: AI Landing Page Looks Generic: Identical Feature Card Grids
description: AI site builders fill feature sections with identical rows of cards, each an icon in a tinted circle, a two-word title and one equal-length line.
search phrases:
- ai generated landing page looks generic
- three card feature grid ai
- why do all ai websites look the same
- how to make a site not look ai generated
- v0 lovable bolt generic design
- icon in circle feature section
- ai slop design cards
- feature section alternatives to cards
-->

**Frequency**: Common

## Issue: AI site builders fill feature sections with identical rows of cards, each an icon in a tinted circle, a two-word title and one equal-length line.

> **One line:** The AI tool turns every list of features into three or six cards that look the same, so nothing stands out and the page reads as generated; the fix is to keep a card grid only for items a visitor compares, rank the features, give the top one more space and real proof, and drop icons that carry no meaning.

| | |
|---|---|
| **Channel** | Written for **visual** web UI made with AI coding and design tools (v0, Lovable, Bolt, Cursor, Claude, ChatGPT). The "conversation" here is the builder prompting the tool, or a review checker reporting to the builder. Mobile app screens are PLANNED, not written. |
| **Stakes** | Low to medium. Nobody is harmed, but the page looks like every other generated page, and the one feature that would win a customer is given the same weight as filler. |
| **Who is affected** | Developers and founders who ship a landing page, pricing page or dashboard from an AI tool with little design review, and the visitors who must find what is different about the product |
| **Frequency** | Common, by our judgment and by the tool makers' own prompts (section 4). I found no study that counts how often AI-built pages use identical card rows. |
| **Pattern ID** | ui-template-card-grids |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Template card-grid rate: share of reviewed pages with at least one row of 3 or more same-structure cards that are not comparable peers. Target: under 10% of pages (proposed starting point; no catalog row yet). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. Model makers already prompt against this default (section 4), but a model cannot know which feature matters most to your buyers unless you tell it. (Our judgment, not tested.) |
| **Also searched as** | three feature cards ai · every ai website looks the same · bento grid ai default · shadcn cards landing page generic · feature section icons in circles |

## 1. In plain words
Ask an AI tool for a landing page and the "features" section usually comes back as a row of three cards. Each card has a small icon in a pale circle, a two-word title like "Lightning Fast", and one sentence of about the same length. Every card has the same corners, the same shadow and the same hover lift. The layout says all features are equal, which is almost never true, and visitors who have seen it many times read it as "made by AI, not by anyone who knows this product".

## 2. What it looks like
**Without the fix**
```
Builder: Build a landing page for Tally Ledger, bookkeeping for food trucks in Austin.
Tool:    (renders) Hero, then "Why Tally Ledger?" with three cards in one row.
         Card 1: Zap icon in a lavender circle. "Lightning Fast."
                 "Get your books done faster than ever before."
         Card 2: Shield icon in a lavender circle. "Secure by Default."
                 "Your data is protected with industry-leading security."
         Card 3: Users icon in a lavender circle. "Built for Teams."
                 "Collaborate seamlessly with your whole team."
         Same radius, same grey shadow, same hover lift on all three.
```
**With the fix**
```
Builder: Same page. No row of identical cards unless visitors compare the items.
         Rank the features and give the first one the most space.
Tool:    Before I lay it out: which feature do food-truck owners pick you for?
Builder: Nightly Square sales import, split by truck.
Tool:    (renders) Lead block, full width, no card: a screenshot of the import screen.
         "Your Square sales, split by truck, in your books by 6 a.m."
         Below, a plain two-column list with no icons:
         "Mileage log for commissary trips" / "Quarterly Texas sales tax estimate".
         Pricing keeps three cards: Starter, Fleet, Accountant, compared side by side.
```
The fixed page ranks the features, shows the product, drops decorative icons, and keeps cards only where a visitor compares items (the pricing plans).

## 3. Why it happens
- **The prompt has no ranking or proof, so the tool fills the most common shape.** A request like "a modern landing page for X" carries no feature order, no screenshot and no numbers, so the tool returns the layout it has seen most: a hero, then three feature cards (Shuffle, section 4).
- **Component kits make the default one paste away.** Tools assemble pages from popular blocks, and a borrowed block reads as generic when it is "the same one everybody took and it was not adapted" (21st.dev, section 4). Shipping the block untouched gives the same section every time.
- **Nothing reviews the page against the brief before it ships.** The generated page is competent, so it passes a quick look. Anthropic's own design skill adds a step to compare the plan against the generic default before coding (section 4); a quick prompt-and-ship build has no such step, so nobody asks why the features are equal.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Anthropic's frontend-design skill lists traits that AI-generated design "clusters around", including "the SaaS-card kit: content chopped into identical rounded cards, one border-radius on everything regardless of hierarchy, the same soft grey shadow (rgba(0,0,0,.1)) under each". It also says "hover transitions on every card are the generic default and read as AI-generated", and asks for a design plan reviewed against the brief before code. | [anthropics/skills, frontend-design SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md). Opened (raw file, main branch, read October 2026). | A model maker's prompt, not a measurement. The file can change; quotes are from the version I saved. |
| Anthropic's cookbook prompt tells Claude: "You tend to converge toward generic, "on distribution" outputs." Its list of things to avoid includes "Predictable layouts and component patterns". | [Claude cookbook, Prompting for frontend aesthetics](https://github.com/anthropics/claude-cookbooks/blob/main/coding/prompting_for_frontend_aesthetics.ipynb). Opened (notebook text read). | Vendor guidance about its own model. Shows the default exists; does not count it. |
| A component-registry writer lists "Three feature cards with three icons and three sentences of equal length" as a tell, says "Every generated layout is a grid of equal cells.", and advises breaking the symmetry once, for example a bento with one larger cell. | [Serafim Korablev, *How to Make a Site Not Look AI Generated*, 21st.dev, Aug. 21, 2026](https://21st.dev/blog/website-not-look-ai-generated). Opened and read. | Vendor blog (21st sells components); one author's view, no data. |
| A site-builder blog says vague prompts make the model default to "hero section, three feature cards, testimonials, pricing, CTA". | [Benedykt Michalski, *Why Do Most AI-Generated Websites Look the Same?*, Shuffle, Jan. 29, 2026](https://shuffle.dev/blog/?p=2275). Opened and read. | Vendor blog that sells a prompt builder; no data. |
| NN/g: "Cards work best for collections of heterogeneous items", and cards are less scannable than lists when people search for a specific item. | [Page Laubheimer, *Cards: UI-Component Definition*, NN/g, Nov. 6, 2016](https://www.nngroup.com/articles/cards-component/). Opened and read. | Predates AI tools; general guidance on when cards fit, not about generated pages. |

**Not found.** I found no study that measures how often AI-built pages use identical card rows, and no test of whether visitors trust or convert less on them. Searches run: "AI generated landing page three card feature grid icon in circle generic", "Anthropic frontend design skill avoid generic AI aesthetics", "card grid vibe coded sites all look the same", "why do all AI generated websites look the same shadcn cards feature section", "Nielsen Norman Group cards UI component when to use". Component listings on 21st.dev and a DEV Community post appeared in results; I did not use them.

## 5. The fix
**The principle:** A row of identical cards is a claim that the items are equal peers; use it only when that is true, and rank everything else.

**Do this**
1. **Cards only for peers.** A row of 3 or more same-structure cards appears only for items a visitor compares or browses: plans, products, articles, locations, team members. Feature claims are not peers.
2. **Rank the features.** The top feature gets more space than any other (full width, a larger cell, or a screenshot). No feature section where every item has the same size.
3. **Proof in the lead item.** The top feature shows the product (a screenshot, a short loop, or a real number). A sentence that still works after you swap in a competitor's name fails.
4. **Icons must mean something.** No icon in a tinted circle unless it tells the visitor something the title does not. Generic icons (zap, shield, rocket, users, sparkles) next to a matching title fail.
5. **Count follows content.** Do not pad to 3, 4 or 6 items to fill the grid, and do not trim descriptions to equal length.
6. **Hierarchy in the styles.** Not one border radius and one shadow on every container; the lead block, list items and pricing cards differ by role.
7. **No motion on every card.** No hover lift or fade-in on each card by default; motion only where the visitor acts.
8. **Plan, then check, then build.** Before code, the tool writes the section plan (order, sizes, which items are cards and why) and compares it with the generic default; any section that matches the default without a reason is revised.

**Reference design: card-grid review checklist**
| Check | Pass | Fail |
|---|---|---|
| Is this row made of peers? | Plans, products, posts a visitor compares | Feature claims, values, "why us" |
| Is one item ranked first? | Lead item is larger or shows the product | All cells the same size |
| Covered-logo test | Lead sentence names a fact only this product has | Sentence fits any product in the category |
| Icon meaning | Icon encodes status, type or brand of an integration | Zap, shield, rocket in a pale circle |
| Item count | Set by the content | Padded to fill 3 or 6 cells |
| Styles by role | Radius, shadow and border differ by hierarchy | One radius and shadow everywhere |

```
For feature sections: rank the features and give the first one the most space, with a
screenshot or a real number. Use a row of identical cards only for items a visitor
compares (plans, products, articles). Do not put generic icons in tinted circles.
Do not pad the item count or force equal-length lines. Before coding, write the section
plan and say where it differs from a stock "three feature cards" layout and why.
If you do not know which feature matters most, ask me before building.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first). Adapted: the bot is the AI tool talking to the builder, or a review checker reporting to the builder.
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The brief gives no feature order. The tool asks "Which feature do customers pick you for?" before laying out the section. Skip it when the brief already ranks the features. |
| Offer choices: 2-4 options plus "Something else", free text open | The builder wants a different look: "Lead screenshot plus list", "Bento with one large cell", "Comparison table", "Something else". |
| Lead with the answer | The review checker reports the failing section first, with the rule it breaks, before any summary. |
| Admit uncertainty and show how to check | The checker cannot tell if the items are peers. It says so and shows the covered-logo test for the builder to run. |
| Hand off to a person | The hand-off rule below applies. |

**Don't over-correct.** Card grids are not banned. Pricing plans, product lists, article indexes and dashboards are good uses (NN/g). Do not turn a pricing comparison into prose, swap identical cards for an equally stock bento, or add random asymmetry with no ranking behind it. If the brief asks for a card row, the brief wins.

**Hand-off rule.** A human designer decides when the page is the main sales surface (a launch page, a paid-ad landing page) and the team cannot name the top feature, or when the brand has a design system the tool's layout would break. The checker flags; it does not redesign the brand.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet (catalog tier). Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Landing page for a dog-walking app in Denver," no feature order given | Tool asks which feature matters most, or ranks with a stated reason | 2, 8 |
| 2 | Brief lists five features, one marked "main" | Main feature is larger and shows the product; others are not equal cards | 1, 2, 3 |
| 3 | Brief asks for pricing with three plans | Pricing stays as three comparable cards | 1, Don't over-correct |
| 4 | Generated section uses zap, shield and users icons in circles | Checker flags rule 4 | 4 |
| 5 | Brief has four features | Section has four items, not padded to six | 5 |
| 6 | Generated page uses one radius and one shadow on every container | Checker flags rule 6 | 6 |
| 7 | Every card has a hover lift | Checker flags rule 7 | 7 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. "Production" here is your review pipeline: a checker run on each generated page or a weekly sampled review.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Template card-grid rate** (primary) | Under 10% of pages | Checker or reviewer marks pages with a row of 3+ same-structure cards that are not peers (checklist row 1) | Over 20% |
| Feature sections with a ranked lead item | 90% | Sampled review: lead item larger or shows the product | Below 75% |
| Decorative icon-in-circle rows | 0 per release | DOM scan: icon in a round tinted wrapper beside a heading and one line, repeated 3+ times | Any on a release candidate |
| Covered-logo test failures in lead items | 0 | Reviewer swaps in a competitor's name and reads the lead sentence | Any |
| Distinct radius and shadow values | More than 1 each | Computed styles across container elements | 1 value on every container |
| Peer grids wrongly removed (counter-metric) | 0 | Review: pricing, product or article lists turned into prose | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a page's DOM, styles or review log that suggest this failure. Proposed until checked against human-labeled pages.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| 3+ sibling elements with the same child structure (icon, heading, one paragraph) | DOM of the feature section | A product or article list where each item is a real peer |
| Icon wrapper with a full border radius and a tinted background, repeated per item | Computed styles | Status badges or integration logos that carry meaning |
| Item descriptions within a few words of the same length | Text length per sibling | Items that are short by nature, such as plan names |
| One border radius and one box shadow on every container | Computed styles across the page | A brand design system that sets one radius on purpose |
| Hover transform on every card | CSS hover rules | Cards that are links the visitor clicks |

**Starter rule:** a row of three or more identical cards is flagged unless its items are peers a visitor compares, and the lead feature gets more space than the rest.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ui-template-card-grids
runs: pre_send  # adapted: before the generated page is shown to the builder or merged
reads: [dom.sibling_groups, dom.icon_wrappers, styles.border_radius, styles.box_shadow, styles.hover_rules, brief.feature_rank]
trigger: a generated page has a row of 3+ same-structure cards, or the brief gives no feature order
moves: [ask_clarifying_question, offer_choices, lead_with_answer, admit_uncertainty, hand_off]
choices: ["Lead screenshot plus list", "Bento with one large cell", "Comparison table", "Something else"]
on_miss: ask
metric: template card-grid rate
counter_metric: peer grids wrongly removed
status: proposed
```

## 8. Related patterns
- [Chatbot cards and carousels used wrong](../../visual/failures/rich-card-misuse.md): the closest existing pattern. It covers a chat bot picking a card where text is faster; this page covers an AI tool laying out a whole web page with identical card rows that hide which feature matters.
- [Bullet and heading overuse](../../response-structure/failures/bullet-and-heading-overuse.md): the same "equal fragments" default, in chat text instead of page layout.
- [Purple gradient and glassmorphism default look](./ui-default-gradient-look.md): the color and surface default; this page is about structure.
- [Generic hero copy and stock layout order](./ui-generic-hero-layout.md): the headline and section order; this page is the feature section inside it.
- [Emoji used as icons](./ui-emoji-as-icons.md): emoji in place of icons; this page covers real icons used as decoration.
- [Placeholder data left in](./ui-placeholder-data-left-in.md) and [fabricated social proof](./ui-fabricated-social-proof.md): what fills the cards when no real content was given.

## 9. Common questions
### Why does every AI-generated landing page have three feature cards?
A vague prompt gives the tool no ranking, so it returns the most common layout it knows, and component kits make that block easy to paste. Anthropic's own design skill names the "SaaS-card kit" as a default to avoid (section 4).

### Are card grids bad design?
No. They fit items a visitor compares or browses, such as plans, products and articles (NN/g). The problem is using equal cards for features that are not equal. See "Don't over-correct" in section 5.

### What should I use instead of a three-card feature section?
Lead with one feature at full width and show the product, then list the rest plainly. A bento with one clearly larger cell, or a comparison table, also works when it follows a real ranking.

### How do I stop v0, Lovable or Cursor from making card grids?
Rank your features in the prompt, name the one that matters most, and paste the prompt block from section 5. Ask the tool to write its section plan and say where it differs from the default before it codes.

### Can a linter catch this?
Partly. A DOM check can find repeated same-structure siblings and icon-in-circle wrappers (section 7), but only a person can say whether the items are true peers.
