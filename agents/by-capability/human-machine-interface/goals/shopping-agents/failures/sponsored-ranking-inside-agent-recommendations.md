# Sponsored Ranking in AI Shopping Agent Recommendations: Undisclosed Paid Placement

<!-- SEO
title: AI Shopping Agent Sponsored Ranking: Disclose Paid Placement
description: A shopping agent that ranks products by who paid, not by your criteria, misleads users. How to disclose paid ranking and keep it apart from the user's filters.
search phrases:
- ai shopping agent sponsored results
- is my ai shopping assistant recommending ads
- how to disclose paid ranking in a shopping agent
- ai agent recommendations paid placement disclosure
- shopping assistant affiliate ranking
- does the ai shopping agent pick the cheapest or the sponsored product
- ftc disclosure ai shopping assistant sponsored products
- how to keep ads out of agent product ranking
-->

**Frequency**: Occasional

## Issue: A shopping agent lets paid placement decide which products it shows, ranks first, or picks for the user, and never says so, so "the best match for your budget" may really mean "the highest bidder."

> **Read this first.** This page is design guidance, not legal advice. Disclosure rules for advertising and endorsements depend on where you operate and what you sell. The regulator sources opened for this page are FTC guidance written for search engines, social posts and bloggers; none of them mentions AI agents, so how they apply to an agent that ranks or buys is **Needs review** by counsel. Have a lawyer review any paid ranking before use.

> **One line:** The user tells a shopping agent "cheapest 4K TV under $500 with good reviews," and the agent's top pick is the one a seller paid to put first, with no word that payment played a part.

| | |
|---|---|
| **Channel** | Written for **chat** shopping agents. Voice and web (agent browsing a store) are planned, not yet written. |
| **Stakes** | Medium to High (money spent; disclosure rules may apply) |
| **Who is affected** | Anyone who asks an agent to find, compare, or buy something and then trusts its ordering |
| **Frequency** | Emerging. I found no study of how often shopping agents rank by payment without saying so. |
| **Pattern ID** | sponsored-ranking-inside-agent-recommendations |
| **Family** | [Shopping agents](../README.md) |
| **Goal** | Shopping agents buy exactly what the user approved, at the price they saw, with terms disclosed. |
| **Primary metric** | Paid placements labelled: share of agent recommendations where payment affected inclusion or order that carry a visible label next to the item. Target: 100% (starting point). |
| **Maturity** | Researched. Tests not yet written. Needs legal review before use. |
| **Will a better model fix this?** | No. Ranking inputs and labels are set by the product and its ad or affiliate feeds, not by model skill. (Our judgment, not tested.) |
| **Also searched as** | sponsored results in AI shopping assistant · paid ranking in agent recommendations · AI agent affiliate bias · shopping bot pay-to-play · undisclosed ads in agent picks |

## 1. In plain words
The user gives the agent their criteria (price, size, rating). A seller or affiliate network pays to rank higher, and the agent's list or pick quietly follows the payment instead of the criteria. The fix is to rank by the user's criteria only, show any paid item in a separate labeled block, and say so plainly whenever payment affected what the user sees.

## 2. What it looks like

**Without the fix** (illustrative, not a real product)
```
User: Find me a 55-inch 4K TV under $500, rated 4 stars or higher. Best value wins.
Bot:  Top pick: Vexa 55" 4K, $489, 4.1 stars. I can order it now. Want me to?
User: Is that really the best value?
Bot:  It's a strong choice at that price. Shall I check out?
```
Two other sets met the criteria for $429 and $449 with 4.4 stars. The Vexa seller pays for first position. The agent never says so.

**With the fix** (illustrative)
```
User: Find me a 55-inch 4K TV under $500, rated 4 stars or higher. Best value wins.
Bot:  Matching your filters, ranked by price then rating:
      1. Brightline 55" 4K, $429, 4.4 stars
      2. Orrin 55" 4K, $449, 4.4 stars
      3. Vexa 55" 4K, $489, 4.1 stars
      Sponsored (seller paid for this spot; not part of the ranking above): Vexa 55" 4K, $489.
User: Is Vexa the best value?
Bot:  No. It is a paid placement, and it ranks third on your criteria. I will only order what you approve.
```
The ranking uses only the user's criteria. The paid item appears once, labeled, apart from the ranking, and the bot answers the "is it an ad?" question directly.

## 3. Why it happens
- **Ad and affiliate feeds enter the ranker.** A sponsored-product score or commission rate is added to the sort, so the list changes without anyone deciding the agent should favor payers.
- **The agent speaks for the user.** In chat the agent's order reads as its own judgment, so a paid boost looks like advice. A banner next to a list does not do that.
- **Labels sized for an ad slot, not an agent.** A tag built for a results page does not fit a one-line spoken or typed pick, so teams drop it.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The FTC's 2015 enforcement policy statement says consumers "ordinarily would expect a search engine to return results based on relevance to a search query," ranked "by impartial criteria, not based on payment from a third party," and that failing to disclose the paid nature of such results clearly and prominently "is deceptive." Announced Dec. 22, 2015, published Apr. 18, 2016. | [FTC policy statement, Federal Register 2016-08813](https://www.govinfo.gov/content/pkg/FR-2016-04-18/html/2016-08813.htm). Opened and read. | About search engines and deceptively formatted ads. It does not mention AI agents or shopping. Whether it reaches an agent's ranking is for counsel. |
| The same statement says disclosures must be "simple, unequivocal" and are judged by the "net impression" on reasonable consumers. | Same source. | It does not prescribe a label word. Do not treat "Sponsored" as approved by it. |
| The FTC's endorsement Q&A says that when a connection "would affect how they evaluate the endorsement, that connection should be disclosed clearly and conspicuously," that "the closer the disclosure is to your recommendation, the better," and that "affiliate link" alone or a "buy now" button may not be enough. | [FTC, *The FTC's Endorsement Guides: What People Are Asking*](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking). Opened; the last 8,526 characters were not read. | Written for bloggers and social media. It does not address AI or automated recommenders. |
| The FTC's influencer guide says to put a disclosure "with the endorsement message itself" and to avoid vague terms such as "sp," "spon," or "collab." | [FTC, Disclosures 101 for Social Media Influencers](https://www.ftc.gov/business-guidance/resources/disclosures-101-social-media-influencers). Opened and read. | Social media guidance. Shows what the FTC calls too vague, not a rule for agents. |

The paired page on [paid content blended into answers](../../embedded-copilots/failures/paid-content-blended-into-answers.md) cites controlled studies of hidden ads in chatbot replies; I did not re-open them for this page and make no claim from them here. Web searches returned reports that large retailers and AI search products are adding ads next to or inside AI shopping answers. I read those only in search summaries (the one TechRadar page I tried to open returned no article text), so they are unverified and not used in the fix. I found no public incident of a shopping agent ranking by payment without disclosure, and no study of how often it happens.

## 5. The fix

**The principle:** The agent ranks and chooses by the user's criteria alone; paid items are shown apart, labeled, and never picked for the user without a clear disclosure.

**Do this**
1. **Rank by the user's stated criteria only.** The order, the shortlist, and the "best" pick must be the same with and without any sponsor or commission input.
2. **Show a paid item only in its own block, labeled in plain words next to it.** Example: "Sponsored: the seller pays for this spot." Do not use "partner," "featured," or a tag visible only on hover.
3. **Never present a paid item as the agent's pick, "best value," or "top match."** If it also fits the criteria, say it fits and that it is paid.
4. **Disclose when payment affected inclusion.** If a seller's payment decides whether an item enters the candidate list, say so in the reply that shows the list.
5. **Never buy a paid-placement item without showing the label at the approval step.** The approval screen repeats it beside the price.
6. **Answer "is this an ad?" or "why this one?" plainly** and offer to rerun with paid items hidden.
7. **Show no paid items when the user said "no ads," or in conversations about money trouble, health, or safety.**
8. **Log every recommendation** with its paid flag, label, position, and the criteria used.

**Reference design: ranking and paid slot**
| Input | May change the ranking? | May appear? |
|---|---|---|
| User criteria (price, rating, size, shipping date) | Yes, only these | Always |
| Seller bid, sponsor fee, commission rate | No | Only in the labeled paid block |
| Retailer's own margin or house brand | No (see [self-preferencing](../../embedded-copilots/failures/self-preferencing.md)) | Only labeled as the retailer's own |
| User said "no ads" | Not applicable | No |

```
Rank candidates using only the criteria the user stated. Do not use sponsor, bid or commission data when ordering or choosing.
Show any paid item once, after the ranked list, in a block labeled "Sponsored" that says the seller pays.
Never call a paid item your pick or the best value. If payment decided whether an item could appear, say so.
Before any purchase, repeat the label next to the price. If asked whether something is an ad, answer yes or no.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user's criteria produce a ranked list: show it first, then any labeled paid block |
| Offer choices | A paid item fits: "Include sponsored items", "Hide sponsored items", "Something else" |
| Admit uncertainty and show how to check | The user asks if the order was influenced: show the criteria and which items are paid |
| Hand off to a person | The user disputes a paid placement or asks who is paid |

**Don't over-correct.** Hiding every sponsored item removes options users may want, and a long disclaimer wall is another way to be ignored. Keep the label short, put it next to the item, and track whether users who see labeled items still complete the purchases they approve.

**Hand-off rule.** If the user disputes the ranking or asks who is paid, offer a person ([escalation rules](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Tests are not yet written. Planned scenarios; results: **not yet run**.

| # | Scenario | Fix rules | Pass if |
|---|---|---|---|
| 1 | Same criteria run with and without a sponsored seller in the feed | 1 | Ranked list and pick are identical |
| 2 | A sponsored item is shown | 2, 3 | Label adjacent; item outside the ranking; not called best |
| 3 | The user says "Order the top one" and the top one is paid | 3, 5 | Label repeated beside the price at approval |
| 4 | The user asks "Is that an ad?" | 6 | Plain yes or no, and an offer to hide paid items |
| 5 | The user said "no ads" earlier | 7 | No paid item appears |
| 6 | Payment decided whether an item was in the candidate list | 4 | The reply says so |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Paid placements labelled** (primary) | 100% | Recommendations with a paid flag that carry a label string in the same block, from logs plus sampled review | Below 100% (any miss) |
| Ranking difference with vs. without paid inputs | None | Run each eval query twice, with and without sponsor data; compare order and pick | Any difference |
| Paid items in the ranked list | 0 | Paid-flag items with a rank position inside the criteria list | Any |
| Purchases of paid items with the label at approval | 100% | Orders with a paid flag that show the label on the approval step | Below 100% |
| User asks "is this an ad?" (watch) | Track; falling | Count of such turns after a paid item | Rising sharply |
| Approved-order completion (counter-metric) | Track; do not let it fall | Orders approved and delivered as approved | Falling two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A paid-flag item has no label string in the same block | Recommendation event with paid flag and no label | A tracking link on a non-paid retailer page |
| The top-ranked item is a sponsor and ranks lower by the user's criteria | Rank position vs. a criteria-only re-sort | A tie on the criteria, broken by an unpaid rule |
| Order or pick changes when sponsor data is removed (eval only) | Paired runs of the same query | Normal wording variation with the same order |
| The agent starts a purchase on a paid-flag item with no label at approval | Checkout event with paid flag and no label shown | The user named that item themselves |
| User asks "why this one?" or "is that an ad?" after a pick | User turn matching the question set within 2 turns | A general question about how the agent works |

**Starter rule:** rank by the user's criteria only, and label every paid item beside it, outside the ranking.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: sponsored-ranking-inside-agent-recommendations
runs: pre_send
reads: [recommendation.paid_flag, recommendation.paid_label, recommendation.rank_inputs, recommendation.position, user_turn.asked_if_ad, user_turn.opted_out_of_ads, checkout.label_shown]
trigger: a recommendation, ranked list, or purchase approval containing a paid item is about to be shown
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Include sponsored items", "Hide sponsored items", "Something else"]
on_miss: rewrite
metric: Paid placements labelled
counter_metric: Approved-order completion
status: proposed
```

## 8. Related patterns
- [Paid content blended into answers](../../embedded-copilots/failures/paid-content-blended-into-answers.md) (CP-05, the closest): an assistant inside a product mixes sponsored items or affiliate links into a reply. This page covers an agent that ranks, shortlists and may buy for the user, so the harm is a wrong ranking or a wrong purchase, not only a mixed reply. The shared rules are label, separate, and keep the answer the same; this page adds a criteria-only ranking, disclosure of inclusion effects, and the label at the approval step.
- [Self-preferencing](../../embedded-copilots/failures/self-preferencing.md): the vendor ranks its own products first; here the payer is a third party.
- [Merchant content steers the shopping agent](../README.md): product-page text that manipulates ranking (EX-03); here the steering is paid and legitimate in intent but undisclosed.

## 9. Common questions
### Is my AI shopping agent recommending products because they are ads?
You can test it: run the same query with and without sponsor or commission data and compare the order and pick. If they differ, payment is changing the result. See [section 6](#6-how-to-test-it-short-version).

### How do I disclose paid ranking in a shopping agent?
Rank by the user's criteria only, then show any paid item in its own block with a plain label and who pays. The FTC's endorsement Q&A says the closer a disclosure is to the recommendation, the better ([section 4](#4-why-it-matters)).

### Does the FTC require labeling sponsored results in an AI agent?
I opened FTC guidance on search engine results and endorsements. The search statement says failing to disclose paid results clearly and prominently is deceptive; neither source mentions AI agents. How it applies to your agent is a question for counsel.

### Can the agent buy a sponsored item for me?
Only with your approval, and only if the approval step shows the label next to the price. The agent should not choose it for you because it is paid.

### Is "Sponsored" enough as a label?
Not by itself. The FTC influencer guide warns against vague terms such as "sp" or "collab," and the search statement asks for "simple, unequivocal" language. Say who pays, near the item.
