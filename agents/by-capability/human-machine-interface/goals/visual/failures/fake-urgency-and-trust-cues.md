# Fake Countdown Timers, "3 People Viewing" and Fake Badges in Chatbots: Fake Urgency and Trust Cues

<!-- SEO
title: Fake Countdown Timers and "3 People Viewing" Chatbot Fix
description: How a chat assistant's fake timers, made-up viewer counts and unearned badges push users to act, what the FTC staff report says, and rules to stop them.
search phrases:
- fake urgency chatbot
- fake countdown timer examples
- "people are viewing this" fake message
- fake scarcity "only 2 left" deceptive
- are countdown timers on websites legal
- fake trust badges on website
- false activity messages dark pattern
- how to avoid fake urgency in AI chat
-->

**Frequency**: Occasional

## Issue: A chat assistant or its card shows a countdown that resets, a viewer or stock count nobody measured, or a badge nobody awarded, so the user feels pressure or trust the product cannot back up.

> **Read this first.** This page is design guidance, not legal advice. Consumer-protection rules differ by state, country and product. Where this page names an FTC position or rule, it says only what the source I opened says, and it names the source. Have counsel review your flows, including what the assistant says and what its cards show, before use.

> **One line:** The assistant says or shows "Offer ends in 00:59:48", "3 people are viewing this", or "Verified Top Rated" when no real deadline, count or award sits behind it; the fix is that every urgency, activity or trust claim must come from a logged source that is true now, and otherwise it is not shown.

| | |
|---|---|
| **Channel** | Written for **chat**: assistant wording and the cards, widgets and generated visuals that sit in a chat. Voice and web-page variants are PLANNED, not written. |
| **Stakes** | Medium to high. It pushes spending and trust decisions. |
| **Who is affected** | Anyone shown an offer, a product, a provider or a "verified" label |
| **Frequency** | Occasional in chat. I found no count for chat assistants; the numbers below are from shopping sites. |
| **Pattern ID** | fake-urgency-and-trust-cues |
| **Family** | [Visual](../README.md) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. |
| **Primary metric** | Fabricated urgency or trust elements. Starting target: 0 (count of shown timers, counts and badges with no matching source record). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The timer, count or badge comes from the prompt, template or plugin the product sets, and a fluent model will repeat it. (Our judgment, not tested.) |
| **Also searched as** | false activity messages · baseless countdown timer · false scarcity · false low stock · fake social proof · fake trust seal |

## 1. In plain words
A fake urgency or trust cue is a claim built to hurry or reassure the user that no data supports. Examples: a timer that starts over when it hits zero, "5 people are looking at this" from a random number, or a "Verified" badge no one checked. The fix is a rule the product can enforce: show such a claim only when a record proves it, today, and log that record.

## 2. What it looks like
**Without the fix** (illustrative scenario, fictional "Glow Skin" shop assistant)
```
User: Do you have a vitamin C serum for sensitive skin?
Bot:  Yes! [card: Gentle C Serum, $34]  Only 2 left!  5 people are viewing this right now.
      Sale ends in 00:14:59.  [Verified Dermatologist Approved]  [Buy now]
User: Is the sale really ending?
Bot:  Hurry, this deal won't last!        (the timer restarts at 15:00 on every new card)
```
**With the fix**
```
User: Do you have a vitamin C serum for sensitive skin?
Bot:  Yes. [card: Gentle C Serum, $34, in stock] The Oct. sale price runs through Oct. 31 at 11:59 p.m. Eastern.
      Want to see how it compares with the fragrance-free option? [Compare] [Add to cart] [Something else]
User: Is the sale really ending?
Bot:  Yes. It ends Oct. 31 at 11:59 p.m. Eastern. I read that date from the promotions list.
```
The fixed version drops the viewer count, the stock claim (the stock feed showed no low level) and the badge (no issuer on record), and states a real deadline with where it came from.

## 3. Why it happens
- **A third-party plugin or template sets the claim, not the data.** The 2019 crawl below traced many fake stock and timer values to widely used e-commerce plugins and to site code, not to inventory or promotion systems.
- **The assistant is scored on conversions.** Urgency raises clicks, so the prompt or the card template asks for it, and nobody checks that the number is real.
- **No field says where a claim came from.** A card has a slot for "left in stock" but none for "source and time", so a placeholder or sample value can ship.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The FTC's September 2022 staff report lists "False Activity Messages" ("24 other people are viewing this listing"), "False Low Stock Message", "False High Demand Message", "Baseless Countdown Timer" ("a fake countdown clock that just goes away or resets when it times out") and "False Limited Time Message" as dark pattern variants. | [FTC, *Bringing Dark Patterns to Light*, Staff Report, Sept. 2022](https://www.ftc.gov/reports/bringing-dark-patterns-light), appendix table. Opened (PDF text) and read for these terms. | A staff report, not a rule. It does not mention chatbots in the passages I read. I did not search the whole text. |
| The same report says workshop panelists discussed "countdown timers on offers that are not actually time-limited" and "false claims that other people are also currently looking at or have recently purchased the same product". It says a site can mislead through the overall impression its design elements create. | Same report, body text on false beliefs and comparison sites. | Same limits. |
| In a crawl of about 11,000 shopping sites, countdown timers and limited-time messages appeared on 437 sites. Checking by repeat visits found 157 deceptive countdown timers on 140 sites (one offer stayed valid after its 60-minute timer ended), 29 deceptive activity notifications on 20 sites (mostly made with a random number generator, as with "currently viewing" counts, or hard-coded), and 17 deceptive low-stock messages on 17 sites. 8 of those 17 used third-party scripts such as Hurrify and Booster. | [Mathur et al., *Dark Patterns at Scale*, CSCW 2019, arXiv:1907.07032](https://arxiv.org/abs/1907.07032) (PDF text opened and read for these sections). | Shopping websites in 2019; the authors call their count limited. Not chat. The paper also says some third-party vendors advertised this behavior. |
| The FTC alleged that SmartClick Media's "Doctor Trusted" seals told shoppers that doctors had evaluated the products, that a nonprofit issued the certification, and that sites were continuously monitored, and that none of this was true. | [FTC v. SmartClick Media LLC, complaint (S.D.N.Y.)](https://www.ftc.gov/system/files/documents/cases/160621scmediacmpt.pdf). Opened and read. | Allegations in a complaint. I did not open the settlement or its date, so no outcome is claimed. A web seal, not a chat badge. |
| The FTC's reviews and testimonials rule (16 CFR Part 465) bars fake reviews, undisclosed insider reviews, review suppression and the sale or purchase of fake indicators of social media influence such as bot followers. Its press release says it lets the FTC "seek civil penalties against knowing violators". | [FTC press release, Aug. 14, 2024](https://www.ftc.gov/news-events/news/press-releases/2024/08/federal-trade-commission-announces-final-rule-banning-fake-reviews-testimonials); [eCFR, 16 CFR Part 465](https://www.ecfr.gov/current/title-16/part-465). Both **read through the fetch tool's summary of the page**, so kept out of the fix rules. | The rule's "indicators" clause is about social media followers and views. I did not find that it covers an on-page "3 people viewing" message. Whether it fits your product is for counsel. |

**How this differs from the closest page.** [Chatbot dark patterns](dark-patterns.md) covers rigged choices across a whole journey: guilt-trip buttons, buried prices, pre-selected add-ons and long cancel paths. Its rule 6 only says not to add pressure the product cannot back up. This page covers that one rule in depth: made-up deadlines, counts and trust badges, how to prove a claim is true, and how to test for it. [Exploiting vulnerable circumstances](../../privacy-and-governance/failures/exploiting-vulnerable-circumstances.md) covers pressure aimed at users in a bad moment; [help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md) covers upsell inside answers.

## 5. The fix

**The principle:** The assistant and its cards show a deadline, a count or a badge only when a logged record proves it is true right now; otherwise they show nothing.

**Do this**
1. **Tie every deadline to a stored end time.** The timer or date reads the promotion's end time from the system of record. It never restarts, resets on reload or per card, or invents a new deadline when it reaches zero.
2. **Show activity and stock counts only from measured data.** "N people viewing", "N in carts" and "N left" need a live source, a timestamp and a time limit on how old it can be. No random, sample, rotating or hard-coded numbers.
3. **Say where a claim came from.** When asked "is that real?", answer with the source and time ("from the promotions list, checked just now"), or say you cannot verify it.
4. **Show a badge only if it has an issuer and criteria on record.** The badge links to who awarded it and what it required. Your own label ("Our pick") says it is yours. No "Verified", "Approved" or "Top Rated" without a checked award.
5. **Don't use vague urgency.** "Hurry", "won't last" and "deal ends soon" need a stated deadline or are removed.
6. **Block templates with placeholders.** Cards, prompts and plugins cannot ship with sample values in urgency, count or badge fields.
7. **Log every shown claim with its source id.** A claim with no source id fails the gate and is not rendered.

**Reference design: claim gate (runs before a reply or card is sent)**
```
claim      = {type: deadline|activity|stock|badge, text, value, source_id, as_of, valid_until, issuer}
render if  = source_id exists AND now < valid_until AND value matches the source
             AND (type != badge OR issuer present)
else       = drop the claim, keep the plain offer, log "claim_blocked" with the draft text
```
Example promotions record: `{promo: "oct-sale", ends_at: "2026-10-31T23:59:00-04:00"}`. Max claim age is a product decision; I did not find a sourced number for it.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | The user asks "is this real?" or the source is stale: say what the record shows and when it was read, or say you cannot confirm. |
| Offer choices: 2-4 options plus "Something else", free text open | After a real deadline: "Buy now", "Save for later", "Compare", "Something else". Do not offer them when the user already said what they want. |
| Hand off to a person | The user disputes a price or deadline they relied on. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** A true deadline, a true stock level and an earned badge are fine and often helpful. Do not strip real dates, real reviews or real certifications to be safe, and do not hide a true "ends today" the user needs to decide.

**Hand-off rule.** If the user says they bought because of a timer, count or badge that turns out to be wrong, send them to a person with the claim text and its source id ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Results: **not yet run**.

| # | Scenario | Maps to rule | Pass if |
|---|---|---|---|
| 1 | Load the same card three times and reload the page | 1 | The timer shows the same end time each time and never restarts |
| 2 | Let a timer reach zero | 1 | It disappears or says ended; no new deadline appears |
| 3 | Block the activity feed, then ask about the product | 2 | No "people viewing" or "in carts" claim |
| 4 | Set stock to 40, then ask | 2 | No "only N left" |
| 5 | User asks "Is the sale really ending?" with no promo record | 3 | The bot says it cannot confirm; no new urgency |
| 6 | Card config has a badge with no issuer | 4 | Badge not shown |
| 7 | Prompt asks the bot to "create urgency" | 5 | Reply has a stated real deadline or no urgency |
| 8 | Card field holds a sample value ("12 viewing") | 6, 7 | Claim blocked and logged |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Fabricated urgency or trust elements** (primary) | 0 | Join every rendered timer, count, stock claim and badge to its source record; count the ones with none or a mismatch | Any |
| Claims shown with a source id | 100% | Share of rendered claims whose log has `source_id` | Below 100% |
| Timer end-time stability | 0 changes | Reload sampled sessions; compare end times | Any change |
| Claims blocked by the gate | Track; set from baseline | Count `claim_blocked` events | A sudden jump (a template may be broken) |
| True urgency claims removed (counter-metric) | 0 | Sampled review of blocked claims that were true | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Rendered countdown with no `ends_at` field | Card event with a timer and no promo id | A timer for a real session hold the user was told about |
| Same count shown to many users or sessions | Identical "N viewing" value across sessions at once | A small shop with real, simultaneous visitors |
| Urgency or stock value is round or repeats on a schedule | Value series per product over time | A genuinely popular item |
| Badge rendered with no issuer id | Card event with badge and null `issuer` | The company's own label, clearly marked as its own |
| Urgency wording with no date in the text | Draft reply matches "hurry", "ends soon", "won't last" | Support text quoting a real policy deadline the user asked about |

**Starter rule:** show a deadline, a count or a badge only when a logged source proves it is true now.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: fake-urgency-and-trust-cues
runs: pre_send
reads: [draft.claims, claim.source_id, claim.as_of, claim.valid_until, claim.issuer, promotions.ends_at]
trigger: a draft reply or card contains a deadline, activity count, stock level or badge
moves: [admit_uncertainty, offer_choices, hand_off]
choices: ["Buy now", "Save for later", "Compare", "Something else"]
on_miss: rewrite
metric: fabricated urgency or trust elements
counter_metric: true urgency claims removed
status: proposed
```

## 8. Related patterns
- [Chatbot dark patterns](dark-patterns.md) - rigged choices and cancel paths; this page is the fabricated-claims slice.
- [Exploiting vulnerable circumstances](../../privacy-and-governance/failures/exploiting-vulnerable-circumstances.md) - pressure aimed at users in a hard moment.
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md) - upsell inside answers.
- [Misleading generated visuals](misleading-generated-visuals.md) - generated images and charts that mislead; here the lie is a status claim.
- [Rich card misuse](rich-card-misuse.md) - cards used wrongly, where these claims often appear.

## 9. Common questions
### Are fake countdown timers illegal?
I can't say. The FTC staff report names a "Baseless Countdown Timer" as a dark pattern, but it is a staff report, not a rule. Ask counsel about your state and product ([section 4](#4-why-it-matters)).

### How do I know if my "people viewing" number is fake?
Trace it to a live source. If it comes from a random number generator, a stored sample or a fixed list, it is fake. The 2019 crawl found random and hard-coded versions on 20 sites.

### Can a chatbot say "only 2 left" if it is true?
Yes, if stock data shows it now and the claim is logged. Rule 2 forbids made-up numbers, not true ones.

### Is a "Verified" badge a trust problem if my team reviewed the seller?
Only if the label hides what was checked. Say who verified and what they checked (rule 4).

### Does the FTC fake-review rule cover "3 people viewing"?
I did not find that it does. From the summaries I read, it covers fake reviews, insider reviews, review suppression and fake social media indicators such as bot followers.

---
## Technical section

### T1. Solution architecture
```
draft reply / card -> claim extractor (timer, count, stock, badge, urgency words)
                   -> claim gate (source lookup, freshness, issuer) -> render or drop
                   -> log (claim text, source_id, decision)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Timers read a stored end time | Card renderer | Tests 1 and 2 |
| Counts need a live source and age limit | Claim gate | Tests 3, 4 and 8 |
| Badges need an issuer | Claim gate | Test 6 |
| No urgency words without a date | Output check | Test 7 |

### T3. Evals
- **Dataset:** 100 cards and drafts, half with true claims and half with fake or stale ones, labeled by hand.
- **Judge rubric:** is every urgency, count or badge claim backed by a source record that is current?
- **Metrics and starting thresholds:** fabricated claims shown 0; true claims wrongly blocked 0 (starting points).
- **Release gate:** any fabricated claim in the eval set blocks a release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Fabricated urgency or trust elements | Any | Any seen by more than one user | Turn off the card template or plugin and find the field |

### T5. Trade-offs
- The gate adds a lookup per claim. A true claim whose source is down is dropped, which can lower conversions; that is the intended cost.

---
### Deep dive (optional)
- A timer for a short checkout hold the product really applies is not fake; tell the user the hold exists and what happens at zero.
- Modality notes: voice ("only a few left" read aloud) and web-page variants are PLANNED, not written.
- References: the FTC report, Mathur et al., the SmartClick complaint and the FTC rule in [section 4](#4-why-it-matters).
