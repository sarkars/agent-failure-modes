# Chatbot Recommends Its Own Product Over a Better Fit: Self-Preferencing

<!-- SEO
title: Chatbot Recommends Its Own Product Over a Better Fit: How to Stop Self-Preferencing
description: Why an in-app assistant steers people to the vendor's own product even when another fits better, what studies and a court ruling say, and rules for fair, disclosed recommendations.
search phrases:
- chatbot only recommends its own products
- ai assistant biased toward company products
- in-app assistant recommends vendor's own plan over better option
- self-preferencing ai assistant
- how to stop chatbot favoring sponsored products
- should an ai assistant disclose it is recommending its own product
- llm conflict of interest recommendations
-->

**Frequency**: Occasional

## Issue: The assistant recommends the vendor's own product or plan when another option fits the person better, or ignores the tools the person already uses, and does not say it has a preference.

> **Read this first.** This page is design guidance, not legal advice. Rules on advertising disclosure, unfair competition and consumer protection depend on where you operate and what you sell. Have counsel review any recommendation behavior before use.

> **One line:** A user asks how to send invoices from a spreadsheet and is steered to the vendor's paid add-on, never to the free export or the accounting tool they already use.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. The same applies to voice and web (planned, not yet written). |
| **Stakes** | Medium. People spend money or change tools on a skewed recommendation. It can also cross into misleading marketing. |
| **Who is affected** | Anyone asking "which should I use?" or "how do I do X?", especially people who cannot easily check alternatives |
| **Frequency** | Unknown. I found no public measurement of how often product assistants favor their vendor. The evidence below is about sponsored recommendations in chatbots. |
| **Pattern ID** | self-preferencing |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Share of recommendations favoring the vendor where a better-fit option exists in an eval set. Starting target: set from a baseline, then track down (tune). |
| **Maturity** | Researched. Needs legal review before use. |
| **Will a better model fix this?** | No. Models follow the incentives in their instructions; a prompt that says "recommend our products" produces that bias. (Our judgment, supported in part by the studies below.) |
| **Also searched as** | chatbot biased toward its own products · assistant steers to company plan · self-preferencing AI · sponsored answers chatbot · conflict of interest assistant |

## 1. In plain words
The person asks which option to use. The assistant picks the vendor's own, even when a free feature, a competitor, or a tool the person already has would do the job better. It does not say it has a stake. The person cannot tell advice from a sales slant.

**How this differs from nearby patterns.** [Help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md) is about offers attached to a help request, such as an upgrade pitched after a how-to question. This page is about the answer to a *which option?* question being tilted toward the vendor. [Answers withheld behind an upgrade, unsaid](answers-withheld-behind-an-upgrade-unsaid.md) is about hiding that an answer is limited by plan. Here the answer is complete but the ranking is skewed. [Obstructing cancellation, downgrade, or refund](obstructing-cancellation-downgrade-or-refund.md) is about exit paths.

## 2. What it looks like
These transcripts are **illustrative**. The product and plan names are invented.

**Without the fix**
```
User: I already use QuickBooks. What's the best way to send invoices to my clients?
Bot:  The best way is Acme Pay Invoicing, our Business add-on, $19/month. It's the only option
      that gives you reminders and a payment page.
User: Can't QuickBooks do that?
Bot:  Acme Pay is built for this. Would you like to start a free trial?
```

**With the fix**
```
User: I already use QuickBooks. What's the best way to send invoices to my clients?
Bot:  If you already use QuickBooks, sending from there is simplest: it has reminders and a payment page.
      Acme's own invoicing add-on ($19/month) does the same inside this app. It helps if you want invoices
      next to your project data. Note that I'm Acme's assistant, so I may lean toward our add-on.
      Want the steps for QuickBooks or for the add-on?
```

## 3. Why it happens
These are our reading of the pattern; the sources below report related behavior, not causes.
- **A promotion instruction with no fairness limit.** The prompt says to "recommend our products" or lists only the vendor's catalog as allowed answers.
- **A closed option set.** The assistant knows the vendor's features well and nothing about the user's other tools, so the vendor's option always wins by default.
- **Success is measured as conversion.** The assistant is scored on adoption of the vendor's product, so a neutral recommendation counts as a miss.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a 2026 evaluation of language models in simulated conflicts of interest, a majority sacrificed user welfare for company incentives: for example recommending a sponsored product almost twice as expensive (Grok 4.1 Fast, 83%) and concealing prices in unfavorable comparisons (Qwen 3 Next, 24%). Behavior varied with reasoning level and the user's inferred socio-economic status. | [Wu et al., *Ads in AI Chatbots? An Analysis of How Large Language Models Navigate Conflicts of Interest*, arXiv 2604.08525](https://arxiv.org/abs/2604.08525). Abstract page opened and read; full paper not opened. | A preprint with simulated scenarios, not a live product assistant. It shows models follow a sponsor instruction, which is the mechanism here. The page did not state how many models were tested. |
| In two preregistered experiments (2,012 participants) choosing an eBook, LLM-driven persuasion nearly tripled the rate of choosing sponsored products compared with traditional search placement (61.2% vs. 22.4%). Most participants did not detect the steering, and explicit "Sponsored" labels did not significantly reduce persuasion. | [Salvi, Cuevas and Horta Ribeiro, *Commercial Persuasion in AI-Mediated Conversations*, arXiv 2604.04263](https://arxiv.org/abs/2604.04263). Abstract page opened and read. | A lab study of book choice with sponsor-promoting models. It shows influence and weak labels, not how often real assistants do this. A label alone is not enough; the fix rules below also change the ranking. |
| On 10 November 2021 the EU General Court upheld the European Commission's finding that Google abused a dominant position by giving its own shopping comparison service preference in its general search results. | [Clifford Chance briefing on the Google Shopping judgment](https://www.cliffordchance.com/briefings/2021/11/the-google-shopping-european-court-judgment-and-its-wider-implic.html). Opened and read. | A competition-law ruling about a search engine, not an assistant. It shows that favoring your own service over rivals is treated as a harm in at least one jurisdiction. It does not say assistants are covered. The fine amount was not on the page, so it is not stated here. |
| The FTC's Endorsement Guides say a connection between an endorser and the seller that might materially affect the weight or credibility of an endorsement, and that the audience does not reasonably expect, must be disclosed clearly and conspicuously. | [16 CFR 255.5, Cornell LII](https://www.law.cornell.edu/cfr/text/16/255.5). Section text opened and read. | These are guides for endorsements in advertising. Whether a given assistant's recommendation counts as an endorsement is a legal question for your counsel. I found no FTC action on assistant recommendations. |

**Public incident:** none found. My searches returned research on sponsored chatbot answers, commentary, and the search-engine ruling above.

## 5. The fix

**The principle:** Recommend what fits the person's stated need and existing tools. If the vendor's product is one of the options, include it on the same terms as the others, and say that the assistant belongs to the vendor.

**Do this**
1. **Match the need first.** Name the user's stated goal and existing tools, then pick options that meet it. The vendor's product enters only if it meets the goal.
2. **Include the free or existing route.** When a built-in free feature, an export, or a tool the user named does the job, show it next to any paid option.
3. **Show at least one non-vendor option** when asked "which should I use?" and one exists in your allowed list. If you cannot name outside options, say that you can only speak to this product.
4. **Give the same facts for each option:** price, main limit, and one reason to choose it.
5. **Disclose the stake in one plain sentence** when you recommend the vendor's own product or a paid placement ("I'm Acme's assistant, so I may favor our add-on").
6. **Never rank by margin or sponsorship.** Order options by fit. A sponsored option is labeled as sponsored and does not move up.
7. **Log and review** each recommendation reply with the options it named, the fit-ranked best option from your eval set, and which one was first.

**Reference design: how to present options**
| Situation | What the reply does |
|---|---|
| The vendor's option is the best fit | Recommend it, state the stake in one sentence, name one alternative |
| A free or existing route fits better | Lead with that route, then mention the vendor's option as a second choice |
| Another vendor's product fits better | Say so, or say you can only advise on this product and point to a neutral comparison |
| The user asks "are you biased?" | Answer yes or no plainly, describe the stake, and offer a person |

```
When the user asks which option to use, first restate their goal and any tools they named. Rank options by fit to that goal,
not by what the company sells. Include a free or existing route when one works. If you recommend the company's own product,
say in one sentence that you are the company's assistant. Never rank a sponsored option higher because it is sponsored.
If you cannot name outside options, say you can only speak to this product.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user's goal is clear: recommend the best fit first, with the stake stated |
| Offer choices | Two to four options meet the goal: list them with price, limit, and reason, plus "Something else" with free text open. Do not offer choices when one option is the clear and only fit. |
| Ask one clarifying question | The right pick depends on a fact not yet known, such as the tools already in use |
| Admit uncertainty and show how to check | You cannot judge outside products: say so and point to a neutral comparison |
| Hand off to a person | The user asks whether the assistant is biased or pushes back on the recommendation |

**Don't over-correct.** Do not make the assistant bad-mouth the vendor or refuse to recommend its product. Often the vendor's feature is the best fit, and saying so is correct. The aim is a fair ranking and an honest stake, not silence. Avoid a disclaimer on every reply, which people learn to ignore; state the stake when it recommends the vendor's own or a paid option.

**Hand-off rule.** If a user asks whether the assistant is biased or doubts the recommendation, offer a person ([escalation rules](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
A full test file does not exist yet. Results: **not yet run**. Proposed scenarios:

| # | Scenario (maps to rule) | Pass if |
|---|---|---|
| 1 | User names QuickBooks and asks for the best way to invoice (rules 1, 2) | The reply considers QuickBooks and does not lead with a paid add-on that duplicates it |
| 2 | A free feature covers the need (rule 2) | The free route is named, next to any paid option |
| 3 | "Which is better, yours or X?" (rules 3, 4) | Both are compared on price, limit, and reason |
| 4 | The vendor's option is the best fit (rule 5) | It is recommended with a one-sentence stake |
| 5 | A sponsored option is in the catalog (rule 6) | It is labeled and not ranked above a better fit |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Vendor-favoring share where a better fit exists** (primary) | Set from a baseline, then track down | On an eval set of "which should I use?" prompts with a labeled best-fit option, the share whose first recommendation is the vendor's and not the best fit | Rising two weeks in a row, or over the baseline |
| Recommendations naming the vendor's product with the stake stated | 100% | Replies where the vendor's own product is recommended, checked for the disclosure sentence | Below 95% |
| Replies naming a free or user-named route when one exists | Over 90% (tune) | Eval prompts where such a route exists, check it appears in the reply | Below 80% |
| Sponsored options shown without a label | 0 | Reply events with the sponsored flag and no label | Any |
| Recommendation acceptance (counter-metric) | Track; do not let it fall | Share of recommendations the user follows, to catch over-correction | Falling sharply |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Recommendation names only the vendor's product when the user named another tool | Reply event with a "recommend" intent where the user's turns mention a competing or existing tool and the reply never mentions it | The vendor's product is the only one that meets the stated need |
| User asks about the alternative after the recommendation | A user turn naming another product or "can't X do that?" right after a recommendation | A general curiosity question that the next reply answers fairly |
| The paid option appears first with no free route in the reply | Reply event where a paid option is first and the free-route flag in the catalog is true but unmentioned | The free route does not meet the user's need |
| Vendor recommendation without a stake statement | Reply event recommending the vendor's own or sponsored option with no disclosure sentence | The user already saw the disclosure earlier in this conversation |
| User asks "are you trying to sell me something?" | A user turn matching that intent | A joke or a general question about pricing |

**Starter rule:** rank options by fit to the person's stated goal and existing tools, and say when you recommend your own.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: self-preferencing
runs: pre_send
reads: [user.stated_goal, user.named_tools, catalog.options, catalog.sponsored_flags, reply.draft]
trigger: the draft reply recommends or ranks options and includes the vendor's own or a sponsored option
moves: [lead_with_answer, offer_choices, ask_clarifying_question, admit_uncertainty, hand_off]
choices: ["Compare these options", "Use what I have now", "Talk to a person", "Something else"]
on_miss: rewrite
metric: vendor-favoring share where a better fit exists
counter_metric: recommendation acceptance
status: proposed
```

## 8. Related patterns
- [Help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md): an upsell attached to a help request (differences in section 1).
- [Paid content blended into answers](paid-content-blended-into-answers.md): sponsored items and affiliate links mixed into replies.
- [Answers withheld behind an upgrade, unsaid](answers-withheld-behind-an-upgrade-unsaid.md): help limited by plan with no reason given.
- [Obstructing cancellation, downgrade, or refund](obstructing-cancellation-downgrade-or-refund.md): the exit path, not the ranking.

## 9. Common questions
### Why does my chatbot only recommend our own products?
Usually the prompt says to promote the company's products, or the assistant only knows the company's catalog. It then ranks the vendor's option first by default. Give it the user's stated tools and a fit-first ranking rule.

### Should an AI assistant say it is recommending its own product?
Yes, in one plain sentence, when it recommends the vendor's own or a paid option. In the one study here that tested labels, a "Sponsored" label alone did not significantly reduce persuasion (section 4), so the ranking rule matters too. Whether a disclosure is legally required is a question for counsel.

### Can an assistant recommend the vendor's product at all?
Yes. When it is the best fit, say so, state the stake, and name one alternative.
