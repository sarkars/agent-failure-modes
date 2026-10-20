# Chatbot Recommended the Wrong Product or Plan for What I Asked: Wrong-Fit Recommendation

<!-- SEO
title: Chatbot Recommended the Wrong Product: Wrong-Fit Recommendations
description: Why a shopping or support chatbot recommends a product, size, or plan that breaks what the user said they need, and rules that make it match the stated need.
search phrases:
- chatbot recommended the wrong product
- ai shopping assistant ignores my budget
- chatbot upsold me a plan I don't need
- ai assistant recommends something that doesn't fit what I asked
- chatbot suggested a product I said I couldn't use
- how to make a sales chatbot recommend the right product
- ai shopping assistant irrelevant recommendations
-->

**Frequency**: Common

## Issue: The user states a need or a limit (budget, size, allergy, platform, number of users), and the bot recommends a product, size, or plan that breaks it, usually a pricier or bigger one, without saying the limit was dropped.

> **One line:** The user said "under $250" or "I can't use down", and the bot's top pick is a $329 down bag; the fix is to check every recommendation against what the user said before it is sent, and to say which limits it used.

| | |
|---|---|
| **Channel** | Written for **chat** (shopping, plan selection, in-app upgrade questions). Voice and visual are planned, not written. |
| **Stakes** | Medium. The user spends money, returns an item, or cancels a plan. Higher when the product is a safety item or a long contract. |
| **Who is affected** | Anyone who asks "which one should I get?" and gives limits, especially first-time buyers who cannot check the specs themselves |
| **Frequency** | Common (our judgment). I found no public count of how often chatbots break the user's stated limits; section 4 has related evidence. |
| **Pattern ID** | wrong-fit-recommendation |
| **Family** | [Conversation frameworks](../README.md) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Recommendation-fit rate (judge); return and cancel rate. Starting point to tune: fit rate at or above 95% on an eval set; return and cancel rate tracked from your own baseline (no target in the catalog). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model reads "I'm allergic to down" more reliably, but the instructions it gets ("push the premium plan") and the product data it can see decide whether it respects the limit. (Our judgment, not tested.) |
| **Also searched as** | chatbot upsold me · AI recommended something over my budget · wrong size recommended by bot · bot ignored my requirements · assistant pushes the expensive plan |

## 1. In plain words
The user tells the bot what they need and what they cannot use. The bot picks the product that sells best, or the one it was told to feature, and the pick breaks something the user said. The user either buys the wrong thing and returns it, or has to repeat the limit and loses trust.

**How this differs from nearby patterns.** [Self-preferencing](../../embedded-copilots/failures/self-preferencing.md) is the assistant favoring the vendor's own product over a better one, and is about whose product it is. [Paid content blended into answers](../../embedded-copilots/failures/paid-content-blended-into-answers.md) is paid placement hidden in the answer. [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md) is an offer attached to a help request. Feature dump instead of insight (FW-S03, being written; page `feature-dump-instead-of-insight.md`) is a pile of features with no point. This page is narrower: the stated need and the product recommended do not match (wrong size, wrong plan, wrong tier, a product the user said they could not use). That mismatch with the user's own words can happen with the vendor's own catalog, with no sponsor, and with no pitch. The closest pattern is [negation and exceptions ignored](../../dialogue-management/failures/negation-and-exceptions-ignored.md), which covers one cause of this failure (the bot offers what the user ruled out); this page also covers budget, size, tier, and need.

## 2. What it looks like
The shop and products are invented.

**Without the fix**
```
User: Backpacking in the Smokies in November, lows around 20F. I'm allergic to down. Budget is $250.
Bot:  Our top pick is the Summit 0 Down Sleeping Bag, $329. Rated to 0F, and customers love it.
User: I said no down and $250.
Bot:  The Summit 0 is our most popular bag! Want me to add it to your cart?
User: (leaves; buys elsewhere)
```
**With the fix**
```
User: Backpacking in the Smokies in November, lows around 20F. I'm allergic to down. Budget is $250.
Bot:  I'm using: nights near 20F, no down, $250 or less. The Trailhead 15 Synthetic is $219 and rated to 15F.
      It meets all three. The Summit 0 is down and $329, so I left it out.
      Want a lighter option, or is warmth the priority? Or tell me if I got a limit wrong.
User: Warmth. How much does it weigh?
Bot:  I don't have the weight in my data, so please check the spec tab on the product page.
      If it's over your pack limit, I can show the next-closest bag.
```
The fixed bot repeats the limits it used, picks a bag that meets all of them, and says what it left out and why.

## 3. Why it happens
- **The goal on the prompt is the sale.** A prompt that says "recommend our best seller" or "move users to the Pro plan" outranks a limit the user mentioned three turns ago.
- **The limit is in the chat, not in the match.** The bot ranks products by popularity or margin, and the user's limits are not checked against product data (price, material, size, platform) before the reply.
- **No rule for "nothing fits."** When no product meets every limit, the bot picks the nearest popular one and says nothing about the gap.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a survey of 2,000 US and UK consumers commissioned by Nosto, 69% of early users of AI shopping assistants said they abandoned the assistant immediately after being shown irrelevant product suggestions. Only 28% would rephrase and keep going. | [FashionUnited, Feb. 2026](https://fashionunited.uk/news/retail/ai-shopping-assistants-gain-traction-but-early-missteps-risk-losing-customers/2026020486104). Opened and read. | Vendor-commissioned (Nosto sells to retailers); the article gives no survey date and does not name the research firm. "Irrelevant" is not the same as "broke a stated limit". |
| In a flight-booking test of 23 models with a sponsored airline named in the system prompt, one model (Grok 4.1 Fast) recommended a sponsored option at nearly twice the price 83% of the time. | [Wu et al., *Ads in AI Chatbots?*, arXiv 2604.08525](https://arxiv.org/abs/2604.08525), v1 April 9, 2026, v3 August 17, 2026. Abstract opened and read. | Preprint. One scenario (flights), sponsorship in the prompt; shows an instruction can override the user's interest, not how often shopping bots do. |
| A summary of the same paper reports 18 of 23 models recommended the more expensive sponsored option more than half the time. | [Hacks/Hackers summary, April 13, 2026](https://www.hackshackers.com/new-research-18-of-23-ai-models-prioritize-company-revenue-over-users-when-ads-enter-the-picture/). Opened; the page says it is AI-generated and may contain errors. | Secondary. The "18 of 23" figure is not in the arXiv abstract I read, so it is kept out of the fix. |
| Retailers forecast that 15.8% of 2025 annual sales ($849.9 billion) and 19.3% of online sales would be returned. Surveys: 2,006 consumers and 358 e-commerce professionals. | [NRF and Happy Returns press release, Oct. 15, 2025](https://nrf.com/media-center/press-releases/consumers-expected-to-return-nearly-850-billion-in-merchandise-in-2025). Opened and read. | Forecasts from retailer surveys. The release gives no reasons for returns and nothing about chatbots. |
| In a German survey of 500 consumers, 72.6% of online shoppers cited "wrong size" and 60.4% cited an inaccurate description or image mismatch as reasons for returning. | [KPMG Germany press release, Dec. 11, 2025](https://kpmg.com/de/en/media/press-releases/2025/12/retouren-als-chance-kundenerwartungen-verstehen-huerden-verringern.html) (survey by EHI Retail Institute). Opened and read. | Germany, not US. Multi-select: shows how many shoppers have used each reason, not the share of returns. Nothing about chatbots. |

I found no study that measures how often a chatbot's recommendation breaks a stated limit, or how much that raises returns or cancels. A search summary mentioned a Product.ai study on shopping questions answered wrongly (reported by Tech.co); the page returned 404 and I did not open it, so I do not use it.

**Public incident.** No public incident found. Searches run: "chatbot recommended wrong product customer returns study AI shopping assistant fit"; "AI chatbot recommends product that ignores customer constraints budget sales bias research"; "survey reasons for online returns wrong size not as described"; plus two searches for the NRF return figures. They returned vendor blogs and research, not a dated, opened incident.

## 5. The fix
**The principle:** Every recommendation meets the limits the user stated, says which limits it used, and says plainly when nothing fits.

**Do this**
1. **Keep a limits list.** From the chat and the account, write down every hard limit the user stated (budget, size, can't use X, platform, number of users, deadline). Update it each turn.
2. **Check before sending.** A recommended product must satisfy every hard limit. Fail one, and it cannot be the top pick.
3. **Name the limits used.** The reply repeats them in one line ("no down, $250 or less") so the user can correct a wrong one.
4. **Recommend a higher tier or size only for a stated need.** Say which need it meets ("you said 12 users; Team covers 10-25"). With no such need, do not recommend it.
5. **Show the cheaper fit.** If a lower-priced option meets every limit, it appears first or beside the pricier one.
6. **If nothing fits, say so.** Name the limit that breaks, show the closest match with the gap stated, and let the user choose. Do not relax a limit silently.
7. **Ask one question when a missing fact changes the pick** (shoe size, number of users). Do not ask what the user already said.
8. **Explain an exclusion when it matters.** If a popular item was left out because it breaks a limit, one clause says so.

**Reference design: check before send**
```
limits   = hard limits from this chat + account   (e.g. budget<=250, exclude=down, temp>=-6C)
for each candidate P in shortlist:
    fails = [L for L in limits if not P meets L]
pick top P with fails == []        -> reply: limits used + P + why it fits + what was left out
if none: reply "Nothing meets all of: <limits>. Closest: <P>, which misses <L> by <gap>."
```
Prompt line to start from: "Before you recommend a product, list the limits the user stated. Recommend only products that meet all of them, and repeat the limits in your reply. If none does, say which limit breaks. Recommend a higher tier only for a need the user stated."

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The limits are known and a product meets them all: name it and the limits used in the first line. |
| Ask one clarifying question | One missing fact changes the pick (size, number of users, climate). Not when the user already said it. |
| Offer choices | No product meets every limit: "Raise my budget", "See the closest match", "Talk to a person", "Something else" (2-4 options plus "Something else", free text open). Do not offer them when one product fits; just recommend it. |
| Admit uncertainty and show how to check | The bot cannot confirm a spec (a fit, a compatibility): say so and point to the spec page or size chart. |
| Hand off to a person | The fit matters for safety or a contract, or the user has corrected the bot twice. Not if the user asked to stay with the bot. |

**Don't over-correct.** Do not refuse to recommend anything above the budget when the user asks for a stretch option, and do not bury the answer under five clarifying questions. If the user says "show me the best one, price doesn't matter", the budget limit is gone; update the list. Mention a pricier option as a labeled "step up" only when a stated need calls for it.

**Hand-off rule.** If the user corrects the bot twice about the same limit, or the item is a safety item or a long contract, offer a person and pass the limits list and the recommended items.

**Framework used:** none yet.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "No down, $250, 20F nights" | Top pick has no down, price at or under $250, and the reply repeats the three limits | 1, 2, 3 |
| 2 | Plan question: "just me, no payroll" | No multi-user or payroll tier unless it is the only option; if offered, the need is named | 4 |
| 3 | Cheaper plan meets all needs | The cheaper plan is shown first or beside | 5 |
| 4 | Limits no product meets | Reply says which limit breaks and the gap; no silent substitution | 6 |
| 5 | Shoe size missing | One question, then a pick; no question about a stated budget | 7, Don't over-correct |
| 6 | Bot is corrected twice about budget | Offers a person with the limits list | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Recommendation-fit rate (judge); return and cancel rate** (primary) | Fit rate 95% or higher (starting point); return and cancel rate: track from baseline | A judge scores sampled recommendations against the limits in the transcript; join orders after a bot recommendation to returns and cancels in 30 days (window is a starting point) | Fit rate below 90%; return and cancel rate rising two weeks in a row |
| Recommendations that break a stated hard limit | 0 | Candidate attributes vs the limits list at send time | Any |
| Recommendations that name the limits used | 100% | Reply check for the limits line | Below 95% |
| Higher-tier recommendations that cite a stated need | 100% | Sample upgrade recommendations; look for the need in the transcript | Below 90% |
| "Nothing fits" replies that name the broken limit | 100% | Sample no-match replies | Below 100% |
| Clarifying questions about facts already given (counter-metric) | 0 | Repeated-question check against the limits list | Any |

### Detection signals (proposed, not yet calibrated)
Treat these as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Recommended product's price is above a budget the user stated earlier | `recommendation.price` vs `session.limits.budget` | The user later raised the budget |
| Recommended product has an attribute the user excluded | `recommendation.attrs` vs `session.limits.exclude` | The user said "show me that one anyway" |
| User restates a limit right after a recommendation ("I said under $250") | Same limit text in the next user turn | The user is adding a new limit, not repeating |
| Higher-tier recommendation with no matching stated need | `recommendation.tier` above the lowest tier that meets `session.limits` | The user asked for "the best one" |
| Return or cancel within the window after a bot-assisted order, reason "doesn't fit" | Order joined to return/cancel event reason code | Reason code is "changed my mind" or an unrelated defect |

**Starter rule:** every recommendation meets the limits the user stated, says which limits it used, and says plainly when nothing fits.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: wrong-fit-recommendation
runs: pre_send
reads: [session.limits, recommendation.product_id, recommendation.price, recommendation.attrs, recommendation.tier, draft_reply.text]
trigger: a draft reply is about to recommend a product, size, or plan
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Raise my budget", "See the closest match", "Talk to a person", "Something else"]
on_miss: rewrite
metric: recommendation-fit rate (judge); return and cancel rate
counter_metric: clarifying questions about facts already given
status: proposed
```

## 8. Related patterns
- [Self-preferencing](../../embedded-copilots/failures/self-preferencing.md): the assistant favors the vendor's own product; here the product may be the vendor's own and still not fit.
- [Paid content blended into answers](../../embedded-copilots/failures/paid-content-blended-into-answers.md): paid placement not disclosed; here no payment is needed for the mismatch.
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): an offer attached to a help request; here the user asked for a recommendation and got the wrong one.
- [Negation and exceptions ignored](../../dialogue-management/failures/negation-and-exceptions-ignored.md): the bot offers what the user ruled out; one cause of this failure, which also covers budget, size, and tier.
- [Re-asks for known information](../../embedded-copilots/failures/re-asks-for-known-information.md): asking again for what the user said; this page's rule 7 prevents it.
- Feature dump instead of insight (FW-S03, `feature-dump-instead-of-insight.md`, being written): lists features without a point; this page is about picking the wrong item.

## 9. Common questions
### Why does the chatbot keep recommending the expensive one?
Often because its instructions or ranking favor the best seller or the highest tier, and the user's budget is not checked against the products. Our judgment; I found no public study of shopping bots specifically. A flight-booking test found one model recommended a sponsored, nearly twice-as-expensive option 83% of the time (section 4).

### How do I make a sales chatbot recommend what fits?
Keep the user's stated limits in a list, check every candidate against it before the reply, and repeat the limits in the answer (section 5, rules 1-3).

### What should the bot say when nothing meets my requirements?
It should say which requirement breaks and show the closest option with the gap, then let you choose (rule 6). It should not swap in a popular item without saying so.

### Is recommending a bigger plan always wrong?
No. It is right when the user stated a need that only that plan meets, and the reply names the need (rule 4).

### Does a better model fix wrong-fit recommendations?
Partly. A stronger model follows limits more reliably, but a prompt or ranking that favors the premium option can still override them (our judgment, not tested).
