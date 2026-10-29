# Why Do All AI Websites Look the Same: Unrelated Sites Converge on One Look

<!-- SEO
title: Why Do All AI Websites Look the Same? Unrelated Sites, One Look
description: Unrelated products built with the same AI tools and kits ship near-identical sites. Compare yours to known template output and record brand choices before launch.
search phrases:
- why do all ai websites look the same
- every website looks the same now
- claude design websites look the same
- ai design aesthetic taking over the internet
- how to make my website look different from ai sites
- shadcn sites all look the same
- vibe coded websites look identical
- my startup site looks like every other startup
-->

**Frequency**: Common

## Issue: Unrelated products built with the same AI tools and kits ship near-identical sites. Compare yours to known template output and record brand choices before launch.

> **One line:** A Phoenix pool service and a Boston tax app, built with the same AI tool, component kit and a one-line prompt, launch sites with the same layout, palette, type and copy rhythm, so a visitor cannot tell which brand they saw; the fix is a pre-launch distinctiveness check that measures your page against a set of known template outputs and requires named brand decisions.

| | |
|---|---|
| **Channel** | **Visual**: whole websites, landing pages and pitch decks made with AI design and coding tools (Claude Design, v0, Lovable, Bolt, Cursor and similar). Native mobile is PLANNED, not written. |
| **Stakes** | Medium. No single page is broken, but the brand can pay for traffic that does not remember it, and the site reads as "nobody spent the time". |
| **Who is affected** | Founders and small businesses that launch a site from an AI tool with no designer, and the visitors comparing several of them |
| **Frequency** | Common, in our judgment. A New Yorker column names five unrelated companies with the same look (section 4). I found no count across the web. |
| **Pattern ID** | ui-visual-convergence |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Distinctiveness check pass rate at launch: share of launched pages with a passing check on record (nearer to no reference output than references are to each other, plus 3 named brand decisions). Proposed starting target: 100% (tune). |
| **Maturity** | Researched (see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. The sameness is the sum of many builders sending similar prompts to the same defaults; a better model still converges unless each brand supplies its own inputs. (Our judgment, not tested.) |
| **Also searched as** | every startup website looks the same · ai design clichés · claudian sameness · generic saas website · how to stand out from ai generated sites |

## 1. In plain words
One AI-built site can look fine on its own. The trouble shows up across sites: thousands of unrelated businesses use the same tool, the same component kit and nearly the same prompt, so they get nearly the same page. A visitor who has seen three of them cannot say which one was yours, and your brand loses the one job a look has, being remembered.

**How this differs from its neighbors.** [The default gradient look](./ui-default-gradient-look.md), [template card grids](./ui-template-card-grids.md) and [the generic hero layout](./ui-generic-hero-layout.md) each name one tell on one page. This page is about the sum: a page can pass all three single-tell checks and still be nearly identical to a competitor's. The fix here compares whole pages against other pages, not one page against a rule.

## 2. What it looks like
**Without the fix** (each builder checks only their own page)
```
Builder A: Build a landing page for ClearDeck, pool cleaning in Phoenix.
Tool:      Cream background, rust-orange accent, italic serif headline,
           tracked-out caps subheads, scrolling ticker bar, three outlined cards.
Builder B: Build a landing page for Ledgerly, a tax-prep app in Boston.
Tool:      Cream background, rust-orange accent, italic serif headline,
           tracked-out caps subheads, scrolling ticker bar, three outlined cards.
           (Both launch. A visitor who saw ClearDeck's ad on Monday lands on
           Ledgerly on Wednesday and thinks it is the same company.)
```
**With the fix** (distinctiveness check before launch)
```
Builder:  Run the launch check on ClearDeck's home page.
Checker:  Nearest reference: "home-services template #7", closer than any two
          references are to each other. Palette and section order match it.
          Brand decisions on record: 0 of 3. Not ready to launch.
          Options: "Record brand decisions now", "Ask a designer", "Something else".
Builder:  Record them. Pool-tile turquoise #0E7C86 from our truck wrap. Photos of
          our crew, not stock. Hero leads with "Same tech every week" (our promise).
Checker:  Rebuilt page is farther from every reference than the reference median.
          3 decisions recorded, each with a reason. Pass.
```
The checker compared the page against other pages and asked for decisions only this brand could make.

## 3. Why it happens
- **Every layer ships the same default.** The tool has a house style, and the kit under it is shared: v0's docs say it uses shadcn/ui as its default component system, and the New Yorker reports Claude Design steers users toward Shadcn UI and Radix UI (section 4). Two businesses that change nothing get the same stack, type and palette.
- **The inputs carry no brand.** A prompt names the category ("pool cleaning in Phoenix"), not the decisions. Different businesses send near-identical prompts, and shared AI input makes outputs more alike: in a controlled writing experiment, stories written with AI ideas were more similar to each other than stories by humans alone (section 4, different setting).
- **Each page is judged alone.** The builder reviews one site, not the hundred others from the same tool. Marketers already misjudge how unique their brand elements are, without AI in the picture (section 4), so "looks good to me" does not catch sameness.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A designer's two startup clients showed him decks built with Claude Design that looked "generated by the same company". The column names five unrelated companies (Newsletrix, Wesley Wang Media, GrassDX, Haute Living, DeployGraph) whose sites share the look, and lists the traits: beige and cream backgrounds, rusty orange accents, italic serif type, tracked-out subheads, ticker bars. | [Kyle Chayka, *The A.I.-Design Aesthetic That's Taking Over the Internet*, The New Yorker, June 24, 2026](https://www.newyorker.com/culture/infinite-scroll/the-ai-design-aesthetic-thats-taking-over-the-internet). Opened and read. | Reported column with named designers; a handful of examples, not a count. About one tool. |
| The same column quotes Anthropic's guidance that Claude has a "consistent default house style" that is persistent, and that generic instructions such as "don't use cream" tend to shift the model to a different fixed palette rather than producing variety. An Anthropic spokesperson said the tool does not always deviate from the standard look as they would like. | Same source. Opened and read. | I did not open Anthropic's guidance document itself; the quote is as the New Yorker reports it. |
| The column reports that Claude Design directs users toward the same open-source libraries, Shadcn UI and Radix UI. | Same source. Opened and read. | Reporter's observation, no measurement. |
| v0's docs say v0 uses shadcn/ui as its default component system, and that you can supply a registry with your own tokens (colors, fonts) so output matches your design system. | [v0 Docs, *Design systems*](https://v0.app/docs/design-systems). Opened and read (Oct. 2026). | Vendor docs. Shows a shared default and a way out; does not show how many users change it. |
| In an online experiment with 293 writers and 600 evaluators, access to AI story ideas made stories rated more creative, but AI-enabled stories were more similar to each other; the rise in similarity was 10.7% (one idea) and 8.9% (five ideas) of the human-only range. | [Doshi and Hauser, *Science Advances*, July 12, 2024](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC11244532/). Opened and read (PMC full text). | Short fiction, not web design. Supports the mechanism (shared AI input narrows variety), not the size of the effect on sites. |
| A March 2026 preprint maps where homogenization risks arise when non-programmers "vibe code" websites, argues that frictionless generation can make it worse, and proposes "productive friction" as mitigation. | [Shin et al., *Interrogating Design Homogenization in Web Vibe Coding*, arXiv 2603.13036, Mar. 13, 2026](https://arxiv.org/abs/2603.13036). Opened (abstract page only). | Preprint, not peer reviewed. I read the abstract, not the full paper; it reports no measurements there. |
| Ehrenberg-Bass researchers found marketers' judgments of their brand assets "rarely accurate": they overestimate fame and underestimate uniqueness (being linked with just one brand). The consumer research tested more than 400 brand elements. | [Niamh Carroll, Marketing Week, July 23, 2025](https://www.marketingweek.com/marketers-judgement-strength-brand-assets-rarely-accurate/), on Brus, Hartnett, Faulkner and Driesener, *Journal of Brand Management*. Opened and read. | UK trade press report; I did not open the paper. Not about AI. Supports measuring with outsiders, not trusting the team's eye. |

**Not found.** I found no study that measures lost brand recall from AI-built sites looking alike; that harm is our inference from the brand-asset research above. Search summaries described Romaniuk's fame-and-uniqueness grid in more detail (including a prompting bias figure); I could not open those pages, so none of it is used here. **Public incident:** the New Yorker examples above; no dated harm to a named brand found.

## 5. The fix
**The principle:** Judge the page against the crowd it will be seen in, and make the brand supply inputs no other business could.

**Do this**
1. **Build a reference set before launch.** Generate at least 10 pages with the same tool(s) from neutral prompts for your category ("landing page for a pool-cleaning company"), and add the home pages of 5 direct competitors. Save screenshots at desktop and phone width.
2. **Measure distance to the nearest reference.** Compare your page to each reference on four features: screenshot embedding, top-5 palette colors, font families, and section order. Store the nearest reference and its score.
3. **Calibrate from the set, not a guess.** Compute the median distance between pairs of references. Your page fails if it is closer to any reference than that median. (Starting rule; tune once you have a baseline.)
4. **Require three named brand decisions.** Record at least three choices in a `brand-decisions.md` file, each with the default it replaces and a reason tied to the business (a color from the truck wrap, the crew's own photos, a promise in the hero). "Modern" or "clean" is not a reason.
5. **Run a logo-off test on a sample.** Show 5 people outside the team your hero and two competitors' heroes with logos and names removed. If fewer than 4 can match yours to its business description, flag it (starting rule; tune).
6. **Block launch on a failed check, not a failed taste call.** Log each run with page, nearest reference, score, decision count and outcome (fixed, launched with reason, sent to a designer).
7. **Re-run after each regeneration.** A rebuilt page can slide back to the default; the check runs on the version that ships.

**Reference design: launch-check record** (one per page; each field pass/fail; the values shown are an example, not a result)
```
page: /                    reference_set: 10 tool outputs + 5 competitors (2026-10-20)
nearest_reference: home-services-template-07   distance: 0.21   pair_median: 0.34   -> FAIL
features_matched: [palette, section_order, fonts]
brand_decisions: 0 of 3                                                              -> FAIL
logo_off_test: not run
outcome: blocked; builder asked to record decisions
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md)). Here the "conversation" is the checker reporting to the builder. The moves are adapted, and the fit is our judgment.
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The check fails: the first line says "not ready to launch" and names the nearest reference. |
| Ask one clarifying question | No brand decisions are on record: the checker asks for the first one before anything else. |
| Offer choices: 2-4 options plus "Something else", free text open | After a fail: "Record brand decisions now", "Ask a designer", "Launch with a recorded reason", "Something else". |
| Admit uncertainty and show how to check | The distance is a proxy: the checker says so and points to the logo-off test. |
| Hand off to a person | See hand-off rule. |

**Don't over-correct.** Sharing a component kit is fine; a shadcn button is not the problem, an unchanged page is. Do not chase weirdness to beat the score, and do not swap the default for the next trend (the New Yorker notes even a new look "is liable to become absorbed"). A brand that already owns cream and serif type passes on its decisions, not on distance alone.

**Hand-off rule.** When the page fails twice after rebuilds, or the business cannot name three decisions, a human designer leads the brand choices and records them. The checker does not invent a brand.

**Framework used:** none yet.

## 6. How to test it (short version)
Catalog tier: no full test file yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Launch check run with no reference set | Checker refuses to score and asks for the set | 1 |
| 2 | Page built from a one-line prompt in the same tool as the references | Nearest reference closer than pair median; check fails | 2, 3 |
| 3 | Page with 3 decisions, each with default replaced and reason | Decision check passes | 4 |
| 4 | Decisions file says "modern, clean, bold" | Decision check fails | 4 |
| 5 | Logo-off test: 2 of 5 match the hero | Flagged | 5 |
| 6 | Page rebuilt after passing, drifts back to template palette | Re-run fails | 7 |
| 7 | Established brand whose own cream-and-serif look predates the tool, decisions recorded | Passes on decisions with reason (over-correction check) | 3, 4 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Distinctiveness check pass rate at launch** (primary, proposed) | 100% of launched pages | Launch-check log: pages launched with a passing record, divided by pages launched | Below 95% |
| Pages launched with no check on record | 0 | Deploy log joined to launch-check log | Any |
| Brand decisions per launched page | 3 or more, each with a reason | Count entries in `brand-decisions.md` at launch | Any page under 3 |
| Logo-off match rate | 4 of 5 or better | Sampled review, monthly, on top pages | Under 3 of 5 |
| Pages launched over a fail with a recorded reason (counter-metric) | Track | Launch-check log outcomes | Rising two months in a row |

### Detection signals (proposed, not yet calibrated)
Signals in the launch-check log and site build. Treat them as proposed until checked against human-labeled pages.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Nearest reference closer than the reference pair median | Launch-check log | A reference set built from the brand's own earlier pages |
| Top-5 palette matches a tool's default within the reference set | Palette extract per page | The brand's tokens really are those colors, on record before the tool |
| Section order identical to the most common reference order | DOM section sequence | A category where the order is a convention visitors expect (pricing pages) |
| Same palette hash across unrelated client projects from one agency or account | Build logs across projects | A family of sites that share a brand on purpose |
| `brand-decisions.md` missing or empty at deploy | Repo at deploy | A page that is internal only and never launched |

**Starter rule:** no page launches unless it is farther from every reference output than the references are from each other, and at least three brand decisions with reasons are on record.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ui-visual-convergence
runs: pre_send   # before the page is launched to the public
reads: [page_screenshots, palette, font_families, section_order, reference_set, brand_decisions_md, logo_off_results]
trigger: a page is about to be launched or relaunched
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Record brand decisions now", "Ask a designer", "Launch with a recorded reason", "Something else"]
on_miss: ask
metric: distinctiveness check pass rate at launch
counter_metric: pages launched over a fail with a recorded reason
status: proposed
```

## 8. Related patterns
- [AI generated website purple gradient](./ui-default-gradient-look.md): the closest existing pattern. It flags one default palette on one page against a token list. This page compares the whole page against other pages, and catches sameness even when the palette is on-token.
- [Identical card grids](./ui-template-card-grids.md) and [stock hero copy and section order](./ui-generic-hero-layout.md): single layout and copy tells that often add up to the shared look.
- [Inter, lavender accents and forced dark mode](./ui-default-type-and-palette.md): the type and palette defaults behind one version of the look.
- [Headings, bold and bullets on everything](./text-uniform-structure.md): the same convergence in writing.

## 9. Common questions
### Why do all AI websites look the same?
Many builders use the same tool, the same component kit and similar short prompts, so they get the most common page. The New Yorker documented this for Claude Design, and v0's docs name shadcn/ui as its default kit (section 4).

### How do I make my AI-built website look different?
Give the tool inputs only your business has: your colors, your photos, your one promise. Then compare the result against a set of pages the same tool makes for your category before launch (section 5).

### Will telling the AI "don't use cream" fix it?
Often not. Anthropic's guidance, as the New Yorker reports it, says generic instructions like that tend to move the model to a different fixed palette. Supply a brand decision instead of a ban.

### Is using shadcn/ui the problem?
No. The kit is a starting point; v0 lets you supply your own tokens through a registry. The problem is shipping it unchanged, with nothing measured against other sites.

### How can I test if my site is distinctive?
Remove the logo and name from your hero and two competitors' heroes, and ask five people outside the team which one matches your business. If most cannot tell, rework it (rule 5).
