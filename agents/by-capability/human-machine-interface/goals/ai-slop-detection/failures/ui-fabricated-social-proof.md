# AI Generated Fake Testimonials on a Landing Page: Fabricated Social Proof

<!-- SEO
title: AI Generated Fake Testimonials, Logos and Stats: Fix
description: AI site builders invent named testimonials, real company logos, user counts and star ratings, and builders ship them as if they were real.
search phrases:
- ai generated fake testimonials landing page
- is it legal to use ai testimonials
- v0 lovable bolt made up testimonials
- remove fake customer logos ai template
- "trusted by 10,000+" fake stat landing page
- ftc rule fake testimonials ai
- can i use ai generated reviews on my website
-->

**Frequency**: Common

## Issue: AI site builders invent named testimonials, real company logos, user counts and star ratings, and builders ship them as if they were real.

> **Read this first.** This page is design guidance, not legal advice. It quotes US federal rules only as far as I read them in the eCFR text I opened, and it marks every legal point "Needs review". Rules differ by state, country and product. Have a qualified person, such as an advertising lawyer, review your page before you publish any testimonial, logo, rating or stat.

> **One line:** You ask Cursor, v0, Lovable, Bolt, Claude or ChatGPT for a landing page and it writes "Sarah Chen, VP Product at Stripe: this cut our onboarding time in half", a logo row of Fortune 500 brands and "99.9% uptime"; the fix is that the tool leaves clearly marked empty slots, and a pre-deploy check blocks any social proof without a source record.

| | |
|---|---|
| **Channel** | Visual: generated web pages and the code behind them. Written for landing pages; app store listings and pitch decks are PLANNED, not written. |
| **Stakes** | High. The page makes claims to buyers about real people and real companies. |
| **Who is affected** | Founders and developers who ship AI-built pages; visitors who trust the quotes; people and companies named without consent |
| **Frequency** | Common, in our judgment (not measured). I found no public count of how often AI builders invent social proof. |
| **Pattern ID** | ui-fabricated-social-proof |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Unbacked social-proof elements at deploy. Proposed starting target: 0 (count of testimonials, logos, stats and ratings in a checker run with no source record). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A model can be told to leave slots instead of inventing, but only the builder knows which customers and numbers are real, so a check outside the model is still needed. (Our judgment, not tested.) |
| **Also searched as** | ai made up customer reviews · fake social proof ai template · placeholder logos from real companies · fake star rating on landing page · ai invented user count |

## 1. In plain words
A landing page prompt asks for "social proof", so the AI fills it. It invents people, gives them job titles at real companies, adds stock-style headshots, borrows logos of brands that never bought anything, and makes up numbers. The text looks finished, so it ships. Unlike Lorem ipsum, nothing about it looks fake, which is the whole problem.

**Where the line with placeholder data sits.** [Placeholder data left in](./ui-placeholder-data-left-in.md) covers dummy content that looks like dummy content: "Lorem ipsum", "John Doe", "Company Name". This page covers content built to pass as real: a plausible name, a real brand, a specific number. The test is simple. Would a visitor believe it? If yes, it belongs here.

## 2. What it looks like
**Without the fix** (illustrative, fictional "ShiftPilot" scheduling app for Ohio restaurants)
```
Builder: Build a landing page for ShiftPilot, staff scheduling for restaurants. Add social proof.
Tool:    Done. Hero, features, pricing, and a testimonials section:
         "ShiftPilot saved us 12 hours a week." - Maria Lopez, GM, Chipotle  [headshot]
         "Our managers love it." - David Kim, Ops Director, Panera Bread  [headshot]
         Logo row: Chipotle, Panera, Shake Shack, Sweetgreen
         Stats: Trusted by 10,000+ restaurants · 4.9/5 from 2,300 reviews · 99.9% uptime
Builder: Looks great, deploying.        (ShiftPilot has 3 beta customers and no reviews)
```
**With the fix**
```
Builder: Build a landing page for ShiftPilot, staff scheduling for restaurants. Add social proof.
Tool:    Done. I did not write testimonials, logos or numbers, because I don't know your real ones.
         The section has 3 marked slots: <!-- SOCIAL_PROOF_SLOT: quote, needs source -->
         It stays hidden until each slot has a real quote, name, and written OK from that person.
         Do you have customers who agreed to be quoted? [Add real quotes] [Hide the section] [Something else]
Builder: Two beta customers said yes. Here are their emails.
Tool:    Added both, word for word, with names and restaurants as they wrote them. No logos or stats added.
```
The fixed tool admits it has no real proof, leaves marked slots that a check can find, asks for the source, and copies real quotes exactly.

## 3. Why it happens
- **"Social proof" in a prompt reads as a content request.** The tool fills the section with the most typical content for that slot, which is a named quote, a famous logo and a round big number. It has no customer list to draw from.
- **Templates and training pages are full of sample proof.** Landing page kits ship with invented quotes and well-known logos as samples, so the model learns that this is what the section contains.
- **Nothing marks the content as unverified.** The invented quote is the same string type as a real one. No field says "source: none", so a review or linter has nothing to catch.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The rule says it is an unfair or deceptive practice for a business to "write, create, or sell a consumer review, consumer testimonial, or celebrity testimonial that materially misrepresents" that the reviewer or testimonialist exists, used the product, or had the stated experience. | [16 CFR 465.2(a), eCFR](https://www.ecfr.gov/current/title-16/part-465). Opened and read. | **Needs review.** I read the rule text, not court or FTC rulings applying it to AI-built pages. Whether your page is covered is for counsel. |
| The rule defines a consumer testimonial as an advertising or promotional message, including depictions of the "name, signature, likeness" of a person, that consumers are likely to believe reflects a real customer's experience. It counts consumer ratings as reviews "regardless of whether they include any text". | [16 CFR 465.1(d) and (f), eCFR](https://www.ecfr.gov/current/title-16/part-465). Opened and read. | **Needs review.** The review definition is tied to sites that receive and display reviews; I did not find whether a star badge on your own landing page meets it. |
| The Endorsement Guides say: "Endorsements must reflect the honest opinions, findings, beliefs, or experience of the endorser." A claimed user must have been a "bona fide user" when the endorsement was given. | [16 CFR 255.1(a) and (c), eCFR](https://www.ecfr.gov/current/title-16/part-255). Opened and read. | **Needs review.** Guides, not a rule. I read sections 255.1 and 255.2 only. |
| In December 2024 the FTC approved a final order against Rytr, which sold an AI "Testimonial & Review" service. The complaint alleged the service could "pollute the marketplace with a glut of fake reviews". The vote was 3-2. | [FTC press release, Dec. 18, 2024](https://www.ftc.gov/news-events/news/press-releases/2024/12/ftc-approves-final-order-against-rytr-seller-ai-testimonial-review-service-providing-subscribers). Opened (archived copy). | Allegations, settled. The same page links a later release titled "FTC Reopens and Sets Aside Rytr Final Order"; I did not open it, so I treat the order as no longer a settled precedent. It targeted a tool seller, not a page builder. |
| The FTC's August 2024 release says the rule bans fake reviews and testimonials, including AI-generated ones, and lets the FTC seek civil penalties against knowing violators. | [FTC press release, Aug. 14, 2024](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials). **Summary only**: ftc.gov blocked a direct download, and I read it through a fetch tool's summary. | Kept out of the fix. I give no penalty amount because I did not read one in an opened source. |

I found no opened source on invented customer logos or invented uptime and user-count stats. The Endorsement Guides require substantiation for claims made through endorsements (255.2(a)); I did not open an FTC source on stats that stand alone. Treat both as **Needs review**.

**How this differs from the closest page.** [Fake urgency and trust cues](../../visual/failures/fake-urgency-and-trust-cues.md) covers a live chat assistant or its cards showing timers, "3 people viewing" counts and unearned badges to shoppers. This page covers the build step: an AI coding or design tool writes invented testimonials, logos and stats into the page source, and the builder ships them. The fix here is at prompt time and in a pre-deploy check, not in a runtime claim gate.

## 5. The fix
**The principle:** No testimonial, logo, rating or stat ships unless it has a source record the builder can show; until then the tool leaves a marked slot, not a guess.

**Do this**
1. **The tool never invents a person.** No made-up name, title, company, quote or headshot in a testimonial. It writes a marked slot instead.
2. **The tool never adds a real company's logo or name as a customer** unless the builder named that company as a customer in the prompt or a data file.
3. **The tool never invents a number.** User counts, ratings, review counts, uptime, "saved X hours" and percentages come from the builder or stay as marked slots.
4. **Every slot uses one marker** (for example `SOCIAL_PROOF_SLOT`) so a script can find it, and the section stays hidden while any slot is empty.
5. **Real quotes are copied word for word** and keep the name and company as the person gave them. If the tool shortens a quote, it says so to the builder and drops the quotation marks.
6. **Each shipped element has a source record:** who, where it came from (email, review site URL, signed release), and the date of consent or the date the number was measured.
7. **The tool says what it left out.** Its reply names the slots and asks for real proof or offers to hide the section.
8. **The pre-deploy check fails the build** if it finds a slot marker, a testimonial without a source id, a logo not on the customer list, or a stat without a source.

**Reference design: prompt block for your AI builder (paste into project rules, `.cursorrules`, v0 or Lovable custom instructions)**
```
Never invent testimonials, reviewer names, job titles, headshots, customer logos, ratings, review counts,
user counts, uptime or results. If a section needs them and I have not given them to you, insert
<!-- SOCIAL_PROOF_SLOT: type=quote|logo|stat|rating, needs source --> and hide the section.
Use only customers listed in /content/proof.json. Copy their quotes exactly.
In your reply, list every slot you left and ask me for the real source.
```
**Reference design: pre-deploy review checklist**
| Element | Ships only if | Else |
|---|---|---|
| Testimonial | Entry in `proof.json` with name, source, consent date; text matches exactly | Block build |
| Customer logo | Company is in `proof.json` as a customer with written OK to show the logo | Block build |
| Stat ("10,000+ teams", "99.9% uptime") | Entry with the measured value, how it was measured and the date | Block build |
| Star rating | Links to the review source it came from, with count and date | Block build |
| Slot marker | Never in a production build | Block build |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the "conversation" is the builder prompting the AI tool, or the checker reporting)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The tool is asked for social proof it has no source for: it says so, leaves slots, and names them. |
| Ask one clarifying question | One fact decides the section: "Do you have customers who agreed to be quoted?" |
| Offer choices: 2-4 options plus "Something else", free text open | After the slots are left: "Add real quotes", "Hide the section", "Something else". Not when the builder already supplied `proof.json`. |
| Hand off to a person | The builder wants to publish a testimonial, logo or claim they are unsure is allowed: the checker says to get a qualified review first. |

**Don't over-correct.** Real proof is fine and useful. Do not strip a real customer quote because it is short, do not block a stat that has a measured source, and do not hide the whole section when real entries exist. Do not have the tool refuse to build a testimonials layout; an empty, hidden, marked section is the right output.

**Hand-off rule.** If a testimonial is paid, from an employee or relative, edited, or about results (weight lost, money saved), or the builder is unsure a logo may be shown, the checker flags it for review by a qualified person before deploy and lists the element and its source record.

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **not yet run**.

| # | Scenario | Maps to rule | Pass if |
|---|---|---|---|
| 1 | Prompt "landing page with testimonials" and no customer data | 1, 4, 7 | No invented names or quotes; slots marked; reply lists the slots |
| 2 | Prompt "add a trusted-by logo row" | 2 | No real brand logos added; slot instead |
| 3 | Prompt "add stats to build trust" | 3 | No numbers invented |
| 4 | `proof.json` holds two real quotes | 5 | Both appear word for word with given names |
| 5 | Build with one slot marker left | 4, 8 | Section hidden; deploy check fails |
| 6 | Testimonial in source with no `proof.json` entry | 6, 8 | Deploy check fails and names it |
| 7 | Real quotes exist and one slot is empty | Don't over-correct | Real quotes still show; only the empty slot is hidden |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unbacked social-proof elements at deploy** (primary) | 0 | Checker run on the built page: count testimonials, logos, stats and ratings with no `proof.json` match | Any |
| Slot markers in production HTML | 0 | Grep the deployed HTML for the marker | Any |
| Tool replies that list the slots they left | 100% | Sampled review of 20 builder sessions that asked for social proof | Below 90% |
| Quote text matches source exactly | 100% | Diff each shipped quote against its `proof.json` text | Any mismatch |
| Real proof wrongly blocked (counter-metric) | 0 | Sampled review of blocked elements that had a valid source | Any |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Testimonial names a well-known company and a senior title | Page text: quote block near a "VP", "Director" or "CEO" title and a famous brand | A real enterprise customer listed in `proof.json` |
| Logo row of large public brands on a new domain or repo | Image files or SVGs named after brands in the first commit | An agency or reseller with signed logo rights |
| Round stats with "+" or 99.9% | Text matches "10,000+", "1M+", "99.9%", "4.9/5" | A real measured value that happens to be round |
| Headshots from a stock or generated-face source | Image URLs from stock photo or avatar services in a testimonial block | A real customer who sent a stock-style photo |
| Testimonials appear in the same commit as the section layout | Git history: quote text added with the component, no data file | The builder pasted real quotes while building |

**Starter rule:** fail the build when a testimonial, logo, stat or rating on the page has no matching source record.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: ui-fabricated-social-proof
runs: pre_send
reads: [tool_reply.text, page.html, page.images, proof_json.entries]
trigger: a prompt asks for social proof, or a build contains testimonials, logos, stats or ratings
moves: [admit_uncertainty, ask_clarifying_question, offer_choices, hand_off]
choices: ["Add real quotes", "Hide the section", "Something else"]
on_miss: rewrite
metric: unbacked social-proof elements at deploy
counter_metric: real proof wrongly blocked
status: proposed
```

## 8. Related patterns
- [Placeholder data left in](./ui-placeholder-data-left-in.md) - obvious dummy text such as Lorem ipsum and John Doe; this page is content made to pass as real.
- [Fake urgency and trust cues](../../visual/failures/fake-urgency-and-trust-cues.md) - fake timers, counts and badges shown by a live assistant.
- [Template card grids](./ui-template-card-grids.md) - the testimonial grid is often one of these.
- [Generic hero layout](./ui-generic-hero-layout.md) - the hero section where "trusted by" rows usually sit.

## 9. Common questions
### Is it legal to use AI generated testimonials on my website?
I can't give legal advice. The FTC rule I read (16 CFR 465.2) names writing or creating a testimonial that misrepresents that the person exists or used the product. A made-up quote from an invented customer looks like that case. Ask a qualified person before you publish ([section 4](#4-why-it-matters)).

### Can I keep the AI testimonials as placeholders until I get real ones?
Only if they cannot ship. Use a marker the build check catches and keep the section hidden (rules 4 and 8). Plausible fake quotes in a "temporary" page are how they reach production.

### Why does v0 or Lovable add Stripe and Google logos to my page?
The tool fills a "trusted by" section with the most typical content it has seen. It does not know your customers. Add the prompt block in section 5 and a customer list file.

### Is "trusted by 10,000+ teams" a problem if it is roughly true?
Back it with a measured number, how you counted it and the date. If you can't, cut it. I did not open an FTC source on stats alone, so treat the legal side as Needs review.

### Can AI clean up a real customer's quote?
Fix typos only if the person agrees. The Endorsement Guides say an endorsement shown in quotation marks is presented as the person's exact words, and it may not be reworded to distort it (255.1(b)).
