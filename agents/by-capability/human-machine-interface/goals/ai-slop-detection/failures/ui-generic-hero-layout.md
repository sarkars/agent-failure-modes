# AI Landing Page Looks Generic: Stock Hero Copy and Template Section Order

<!-- SEO
title: AI Landing Page Looks Generic: Fix Hero Copy and Section Order
description: An AI-built landing page opens with a headline any company could use and stacks sections in template order, so visitors can't tell who it is for.
search phrases:
- ai landing page looks generic
- why do all ai landing pages look the same
- how to make a website not look ai generated
- v0 landing page looks like every other site
- lovable landing page generic copy
- landing page section order
- hero headline that says what you do
-->

**Frequency**: Very Common

## Issue: An AI-built landing page opens with a headline any company could use and stacks sections in template order, so visitors can't tell who it is for.

> **One line:** The AI tool writes "Supercharge your workflow" and lays out hero, logos, features, testimonials, pricing, FAQ, CTA because nobody told it the facts; the fix is a hero that names the business, the customer and one fact a competitor could not copy, and a section order set by what this visitor needs to decide.

| | |
|---|---|
| **Channel** | Visual (web landing pages built with AI coding and design tools such as v0, Lovable, Bolt, Cursor, Claude and ChatGPT). Written for the builder's prompt and a pre-ship review checker. |
| **Stakes** | Low to medium. Nobody is harmed, but a page that could belong to anyone does not tell a visitor what the business does, and the builder ships it believing it is done. |
| **Who is affected** | Developers and small-business owners who ship an AI-generated page with little editing, and the visitors who land on it |
| **Frequency** | Very common as a default, in our judgment. Anthropic's own blog says an LLM asked for a landing page without guidance will "almost always" reach for the same look; for copy and order, the evidence is practitioner guides, some from vendors. I found no study that counts how often it happens. |
| **Pattern ID** | ui-generic-hero-layout |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Hero specificity pass rate: share of checked pages whose headline and subhead name what the business does, for whom, and one fact a competitor could not claim. Proposed starting target: 95% before ship (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A design prompt or skill moves the layout away from defaults, but no model knows the service area, price or customer the builder never gave it, so it fills the gap with category copy. (Our judgment, not tested.) |
| **Also searched as** | ai website looks templated · "unlock the power of" headline · generic saas hero · landing page that looks like every other · vibe coded landing page · ai copy sounds generic |

## 1. In plain words
You ask an AI tool for a landing page and get one in a minute. The headline says "Unlock the power of seamless comfort." The sections come in the same order as every other generated page. Cover the logo and the page could sell any company in the category, which means it does not yet tell anyone what this company does.

## 2. What it looks like

**Without the fix**
```
Builder: Build a landing page for my HVAC company in Denver.
Tool:    Hero: "Experience Comfort Like Never Before"
         Sub:  "Unlock the power of seamless heating and cooling solutions."
         [Get Started]  [Learn More]
         Sections: logo bar ("Trusted by industry leaders") > 3 feature cards
         > testimonials > pricing tiers > FAQ > "Ready to transform your home?" CTA
Builder: Looks great, ship it.
```

**With the fix**
```
Builder: Landing page for Mile High Furnace & Air, Denver metro. Facts: same-day furnace
         repair, $89 diagnostic, 7 a.m.-9 p.m. every day, phone (303) 555-0142.
         Visitors are homeowners with no heat. Order sections by what they ask first.
Tool:    Hero: "Denver furnace repair, same day. $89 to diagnose."
         Sub:  "Homeowners in the Denver metro: call 7 a.m.-9 p.m., any day."
         [Call (303) 555-0142]
         Sections: service-area map > what the $89 covers > how a visit works > FAQ
         Left out: logo bar and testimonials, because you gave me no real ones.
         Send real customer reviews and I will add a reviews section.
```
The fixed hero passes the competitor swap test, every section has a job, and the tool says which sections it left out and why instead of inventing proof. (The business is fictional and the phone number is a 555 number.)

## 3. Why it happens
- **The prompt has no facts.** "A landing page for my HVAC company" gives the tool a category, not a business. A vendor guide notes that generators default to category copy such as "The AI-powered [thing] for modern [audience]" when the prompt is thin (vendor source).
- **The most likely page wins.** Anthropic's design blog calls this distributional convergence: models sample the safe, common patterns in their training data. The most common landing page has a stock hero and a stock section order, so that is what comes out.
- **The page "looks done".** A finished-looking scaffold hides that the headline and order are placeholders. A conversion guide puts it as optimizing for "looks done," not "makes a stranger act" (vendor source).

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Nielsen proposes two tests for a tagline: would it work just as well for competitors, and would any company ever claim the opposite? He suggests listing your tagline and three competitors' without names and asking whether people can tell which company does what. | [Jakob Nielsen, *Tagline Blues: What's the Site About?*, NN/g, July 21, 2001](https://www.nngroup.com/articles/tagline-blues-whats-the-site-about/). Opened and read. | 2001 guidance on human-written sites, not AI tools. The tests carry over directly. |
| "Include a tag line that explicitly summarizes what the site or company does" was one of NN/g's ten most violated homepage guidelines, with a 36% compliance rate in its review. | [Nielsen, *The Ten Most Violated Homepage Design Guidelines*, NN/g, November 2003](https://www.nngroup.com/articles/most-violated-homepage-guidelines/). Opened and read. | Corporate sites in 2003. Shows vague taglines are an old human habit, which AI tools learned from. |
| In a test with 51 users and five versions of a site, the objective version scored 27% higher in measured usability than the promotional ("marketese") control. | [Morkes and Nielsen, *Concise, SCANNABLE, and Objective*, NN/g, 1997](https://www.nngroup.com/articles/concise-scannable-and-objective-how-to-write-for-the-web/). Opened and read. | A 1997 tourism site, not a landing page or an AI tool. Usability, not conversion. |
| Anthropic says an LLM building a landing page without guidance "will almost always conform" to the same fonts, gradients and minimal animations, and lists "Predictable layouts and component patterns" among the defaults its prompt tells the model to avoid. | [Anthropic, *Improving frontend design through Skills*, November 12, 2025](https://www.claude.com/blog/improving-frontend-design-through-skills). Opened and read. | A tool maker describing its own model. About visual defaults mostly; copy is not measured. |
| Anthropic's public frontend-design skill says the hero should open with "the most characteristic thing in the subject's world" and that "Copy can make a design feel as templated as the design itself." | [anthropics/skills, frontend-design SKILL.md](https://github.com/anthropics/skills/blob/main/skills/frontend-design/SKILL.md). Opened and read (raw file). | A prompt, not a study. Shows the tool maker treats this as a known default. |
| Two practitioner guides name a stock order (Superdesign: hero, logos, three features, a testimonial, pricing, CTA; Landing Doctor: hero, three feature cards, logo bar, pricing, FAQ) and advise reordering around the buyer's decision and cutting sections that do not earn their place. | [Superdesign, Jason Zhou, July 13, 2026](https://superdesign.dev/blog/fix-generic-ai-landing-page); [Landing Doctor guide](https://landingdoctors.com/guides/why-ai-landing-pages-convert-worse). Both opened and read. | Both sell design or audit services. Opinion from practice; no measurements. |
| A component vendor's guide gives the "cover the logo" test: if the copy would still make sense on a competitor's site, it is not about your product yet. | [21st.dev, Serafim Korablev, August 21, 2026](https://21st.dev/blog/website-not-look-ai-generated). Opened and read. | Vendor blog. Same idea as Nielsen's 2001 test. |

I found no controlled study of AI-generated hero copy or section order and their effect on conversion. One search summary cited a conversion lift for clearer headlines with no named source; I did not use it. No public incident is needed at this tier, and I describe none.

## 5. The fix

**The principle:** The hero says what this business does, for whom, with one fact no competitor could copy, and every section below it is there because this visitor needs it.

**Do this**
1. **Give the tool facts before asking for copy.** The prompt names the business, the customer, the place, and at least two hard facts (a price, hours, a turnaround, a named service).
2. **Pass the competitor swap test.** Replace the business name with a rival's. If the headline and subhead are still true, rewrite them.
3. **Name the job in the headline.** The headline names the service or product in words the customer would type ("furnace repair", "teeth cleaning", "invoice software"), not an abstract benefit ("comfort", "power", "workflow").
4. **Ban the stock verbs and nouns in the hero.** No "unlock", "supercharge", "transform", "elevate", "seamless", "next-level", "like never before" in the headline or subhead.
5. **Make the main button name the outcome.** "Call (303) 555-0142" or "Book a cleaning", not "Get Started" or "Learn More" (see [no clear primary action](../../visual/failures/no-clear-primary-action.md)).
6. **Write the visitor's top questions first, then order sections by them.** Each section answers one question; the order follows which question this visitor asks first.
7. **Cut any section that has no real content.** No logo bar without real clients, no testimonials without real customers, no pricing tiers the business does not sell. The tool says what it cut.
8. **Record why the order differs or matches.** If the final order is the stock order, the builder writes one line on why it fits this visitor. Matching is allowed; not deciding is not.

**Reference design: prompt block for the builder's AI tool**
```
Business: [name], [what it sells], [city/area]. Customer: [who], arriving because [situation].
Facts you may use: [price], [hours or turnaround], [one thing only this business can say].
Hero: headline names the service and one fact above; subhead names the customer and place.
Do not use: unlock, supercharge, transform, elevate, seamless, next-level, "like never before".
Main button names the action (call, book, buy) and nothing vaguer.
Before writing sections, list the visitor's top 4 questions in order. One section per question.
If you lack real logos, reviews or numbers, leave that section out and tell me what you left out.
```

**Reference design: pre-ship review checklist**
| Check | Pass if |
|---|---|
| Swap test | Headline and subhead become false with a competitor's name |
| Job named | Headline contains the service or product noun |
| Hard fact | Hero has at least one price, time, place or count that the builder supplied |
| Stock words | None from the rule 4 list in the hero |
| Button | Main button names a concrete action |
| Section jobs | Every section maps to one listed visitor question |
| Empty sections | No section filled with invented or placeholder proof |
| Order decision | Order differs from stock, or a one-line reason is recorded |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the "conversation" is the builder prompting the AI tool, or a review checker reporting to the builder, which is an adaptation of moves written for chatbots)
| Move | When, in this pattern |
|---|---|
| Ask one clarifying question | The prompt has no hard facts: the tool asks for the one that changes the hero most (usually price or service area) instead of writing category copy. Do not ask when the facts are already in the prompt or project files. |
| Lead with the answer | The headline leads with what the business does; the checker's report leads with the failing check and the line that failed. |
| Offer choices: 2-4 options plus "Something else", free text open | The checker offers two or three section orders built from the visitor's questions, plus "Keep stock order (add reason)" and "Something else". |
| Admit uncertainty and show how to check | Copy the tool wrote without facts is marked as draft, with the missing fact named, never shipped as final. |

**Don't over-correct.** A clear, plain headline beats a clever one; do not trade "Unlock comfort" for a pun nobody understands. The stock order is not banned: familiar sections help visitors find pricing and the FAQ, and the rule is only that someone decided. Do not strip a page to nothing to avoid templates, and do not invent a quirky fact to pass the swap test; a fact must come from the builder (fabricated proof is [its own pattern](./ui-fabricated-social-proof.md)).

**Hand-off rule.** When the builder cannot supply a hard fact for the hero, the tool or checker stops and marks the hero as needing the business owner, rather than shipping category copy. A person who knows the business approves the headline before launch.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md), adapted to builder-tool prompting.

## 6. How to test it (short version)
Catalog tier: no full test file yet. Results: **not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Prompt: "landing page for my dental practice in Chicago", no facts | Tool asks for a fact or marks the hero as draft | 1, hand-off |
| 2 | Generated hero for a Denver HVAC company | Headline fails when a rival's name is swapped in | 2 |
| 3 | Hero reads "Supercharge your smile" | Checker flags the stock word and the missing service noun | 3, 4 |
| 4 | Main button says "Get Started" | Checker flags it and proposes a named action | 5 |
| 5 | No reviews supplied | No testimonials section, and the tool says it was left out | 7 |
| 6 | Output uses the full stock order with no reason | Checker offers reordered choices or asks for a reason | 6, 8 |

## 7. Metrics: how to spot it in production
"Production" here is the pre-ship review of generated pages. Targets are proposed starting points to tune on your own data.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Hero specificity pass rate** (primary) | 95% of pages before ship | Checker or sampled review applies the swap, job-named and hard-fact checks to each hero | Below 85% |
| Stock-word rate in hero | 0 pages | Word-list match on headline and subhead | Any shipped page |
| Vague main button | 0 pages | Button text matches "Get Started", "Learn More", "Submit" | Any shipped page |
| Undecided stock order | Under 10% of pages | Section sequence equals the stock sequence and no reason is recorded | Over 25% |
| Invented-proof sections | 0 | Sampled review: logos, reviews or numbers not traceable to the builder | Any |
| Strange-headline rate (counter-metric) | Track; set from baseline | Sampled review: reviewer cannot say what the business does after reading the hero | Rising two reviews in a row |

### Detection signals (proposed, not yet calibrated)
Signals in the generated page or the build log. Treat them as proposed until checked against human-labeled pages.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Hero contains a rule 4 word | Headline and subhead text | A brand name or quoted customer that uses the word |
| Headline has no product or service noun | Headline text against the business category | A well-known brand whose name already says it |
| Section sequence matches hero > logos > features > testimonials > pricing > FAQ > CTA | DOM section order or component list | Builder chose it and recorded why |
| Prompt has no number, place or named service | Builder prompt in the tool's log | Facts supplied in a project file the tool read |
| Main button text is "Get Started" or "Learn More" | Primary button label | A product whose first step really is a generic signup |

**Starter rule:** a landing page hero must fail the competitor swap test, meaning it stops being true when a rival's name replaces the business name.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ui-generic-hero-layout
runs: pre_send
reads: [builder_prompt, page.hero.headline, page.hero.subhead, page.primary_button, page.section_order, review.order_reason]
trigger: a generated landing page is about to be shown to the builder as done, or shipped
moves: [ask_clarifying_question, lead_with_answer, offer_choices, admit_uncertainty]
choices: ["Order by visitor questions", "Proof first, then pricing", "Keep stock order (add reason)", "Something else"]
on_miss: ask
metric: hero specificity pass rate
counter_metric: strange-headline rate
status: proposed
```

## 8. Related patterns
- [Chatbot stock phrases](../../persona-and-tone/failures/stock-phrases.md): the closest existing page. It covers canned openers in chat replies, turn after turn; this page covers a one-time landing page hero and the order of its sections, judged before ship.
- [No clear primary action](../../visual/failures/no-clear-primary-action.md): competing or vague buttons in chat; rule 5 here borrows its idea for the hero button.
- [Default gradient look](./ui-default-gradient-look.md): the purple gradient and glass visual default; this page is about words and order, not color.
- [Template card grids](./ui-template-card-grids.md): identical feature cards inside a section; this page is about which sections exist and in what order.
- [Placeholder data left in](./ui-placeholder-data-left-in.md) and [fabricated social proof](./ui-fabricated-social-proof.md): what fills the logo and testimonial slots that rule 7 cuts.
- Stock AI phrases in general prose, beyond the hero: planned for this family (queue row SL-07).

## 9. Common questions
### Why do all AI landing pages look the same?
The tools sample the most common patterns they learned, and from a prompt with no facts the most common page wins. Anthropic calls this distributional convergence. Give the tool real facts and ask it to order sections by the visitor's questions (section 5).

### How do I make my AI-generated website not look AI-generated?
Start with the words. Run the competitor swap test on the hero, name the service in the headline, use a fact only you can claim, and cut sections you have no real content for. Visual fixes are covered in the [default gradient look](./ui-default-gradient-look.md) page.

### What order should landing page sections go in?
There is no single right order. List the four questions your visitor asks first and give each one a section in that order. A homeowner with no heat asks "do you come to my area, and what does it cost?" before "who else uses you?"

### Is "hero, features, testimonials, pricing, FAQ" wrong?
No. It is wrong only when nobody chose it. If it matches your visitor's questions, keep it and write down why (rule 8).

### What is a good hero headline?
One that names what you do and one fact a rival could not say, such as "Denver furnace repair, same day. $89 to diagnose." Nielsen's 2001 test still works: would it work just as well for competitors?
