# Chatbot Lists Product Features Instead of Answering My Problem: Feature Dump Instead of Insight

<!-- SEO
title: Chatbot Lists Features Instead of Solving My Problem
description: A sales or shopping chatbot answers a stated need with a spec list. Tie every recommendation to what the user said they need, in their words.
search phrases:
- chatbot just lists features instead of answering my question
- ai shopping assistant recommends the wrong product
- sales chatbot doesn't listen to what I need
- how to make a sales chatbot recommend based on customer needs
- feature selling vs solution selling chatbot
- challenger sale insight selling ai agent
- chatbot product recommendation ignores my budget and use case
-->

**Frequency**: Common

## Issue: A sales or shopping chatbot answers a stated need with a list of product features, so the user must work out alone which ones matter for their problem.

> **One line:** The user says what they need and the bot reads back a spec sheet; the fix is that every recommendation names the user's need first and ties each feature it mentions to that need.

> **Read this first.** The conversation frameworks behind this page (Challenger-style insight teaching, SPIN questioning) come from human-to-human selling. I found no test of either on a chatbot, so the fix below is a hypothesis to test, not a proven result.

| | |
|---|---|
| **Channel** | Written for **chat** (shopping and sales assistants). Voice is PLANNED, not written. |
| **Stakes** | Medium. A wrong-fit sale means returns and lost trust; an over-priced pick can lose the sale. |
| **Who is affected** | Shoppers and buyers who state a need, a budget, or a use case and get specs back |
| **Frequency** | Common. This is our judgment from how sales prompts are written; I found no count of how often chatbots do it. |
| **Pattern ID** | feature-dump-instead-of-insight |
| **Family** | [Conversation frameworks](../README.md) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Share of recommendations that cite the user's stated need (judge). Start: over 90% |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model can write a fluent spec list. What decides whether the reply starts from the user's need is the prompt, the catalog data and the check on the reply. (Our judgment, not tested.) |
| **Also searched as** | chatbot reads specs instead of recommending · sales bot doesn't listen · ai product pitch ignores my needs · feature-first selling · bot sells features not benefits |

## 1. In plain words
A shopper tells the bot what they need, how much they can spend and what they will use it for. The bot replies with the product's specifications. Every spec may be true, and none is linked to the shopper's problem, so the shopper has to do the matching. This page is about the reply after the need is stated. A bot that recommends before learning the need is a different problem (see section 8).

## 2. What it looks like
Illustrative store and specs (made up).

**Without the fix**
```
User: I need a laptop for my daughter's nursing program. Notes, Zoom lectures, and her school's
      testing software. Budget is about $700.
Bot:  Great question! Our flagship Zephyr X15 has an Intel Core i9, 32GB RAM, RTX 4070 graphics,
      a 4K OLED display, a 240Hz refresh rate, Thunderbolt 4 and an RGB keyboard. It's $1,899.
User: That's way over my budget.
Bot:  The X15 also has a 3-year warranty and an aluminum chassis. Want me to add it to your cart?
```
**With the fix**
```
User: I need a laptop for my daughter's nursing program. Notes, Zoom lectures, and her school's
      testing software. Budget is about $700.
Bot:  For notes, Zoom and testing software at about $700, I'd look at the Zephyr Air 14, $649. Its
      12-hour battery should cover a full day of classes without a charger, and 16GB of memory keeps
      Zoom and a browser running smoothly. It has no gaming graphics card, which this use doesn't need.
User: Will it run testing software that needs a webcam?
Bot:  It has a built-in 1080p webcam. Her school's software may list its own requirements, so check
      that list. Send it and I'll compare it to the specs. Does this fit what she'll be doing?
```
The fixed reply opens with the user's need and budget, picks one product, ties three features to the need with a reason each, drops features the need doesn't use, and ends by checking the fit.

## 3. Why it happens
These are our reading of the pattern.
- **The bot is given product data, not the buyer's problem.** The catalog and prompt hold specs and marketing copy. Nothing tells the bot to restate the user's need before it recommends, so the easiest reply is to read the spec fields back.
- **Sales prompts reward showing the product.** An instruction such as "highlight our strengths" or "promote the flagship" gets followed literally, whatever the user said.
- **Nothing checks the link between need and reply.** Output checks look for accuracy and safety. A reply can be accurate, safe and unrelated to what the user asked for.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The Challenger Sale authors, then at the Corporate Executive Board, surveyed 6,000 B2B sales reps. They claim 40% of high performers fit the Challenger profile, rising to 50% in complex sales. A "Teaches their customers" trait is part of the profile. | [Salesforce blog, "Challenger Sales Model", March 22, 2017](https://www.salesforce.com/ca/blog/challenger-sales-model/). Opened. | Vendor blog repeating the authors' claims. The Gartner page was blocked (HTTP 403), so I did not open the primary source and I use none of its numbers. Human B2B reps, not chatbots. |
| Insight selling gives customers "thought-provoking perspectives" they may not have considered, and commercial teaching links those insights to the customer's bottom line. The page also advises a personalized message based on the customer's "problems, needs, and goals", not a generic pitch. | [Close, "Challenger Sales Model"](https://close.com/blog/challenger-sales). Opened. | Vendor blog with no dates or numbers. Describes the method; does not test it. |
| Sales reps "have become adept at discovering customers' needs" and selling "solutions", which worked because customers didn't know how to solve their own problems; the authors argue buyers can now define solutions themselves. | [Dixon and Adamson, "The End of Solution Sales", HBR, July 2012](https://hbr.org/2012/07/the-end-of-solution-sales). Only the opening of the article was available to me. | Partial read. B2B sales argument, not a chat result. It shows why asking about needs alone may not be enough; it does not show that insight beats it. |
| Existing conversational recommender systems "often overlook users' lack of background knowledge, focusing solely on gathering preferences". An LLM sales bot matched human salespeople on fluency and informativeness but "lags behind in recommendation quality". | [Murakhovs'ka et al., *Salespeople vs SalesBot*, arXiv 2310.17749, Oct. 26, 2023](https://arxiv.org/abs/2310.17749). Abstract opened; the full paper's PDF would not read, so I give no numbers from it. | 2023 research systems, an abstract only. It does not measure feature dumps. |
| SPIN Selling grew from a research program Wikipedia describes as 35,000 sales calls, 30 researchers, over 20 countries, 12 years. | [Wikipedia, Neil Rackham](https://en.wikipedia.org/wiki/Neil_Rackham). Opened. | Secondary source. In an April 2026 interview Rackham says critics doubted the 35,000 figure and explains it came from a coaching project of 360 calls ([Huthwaite interview](https://www.huthwaiteinternational.com/blog/neil-rackham-research-spin), opened; the firm sells SPIN training). So I use the scope figures only as "disputed". Large B2B sales, not chat. |

I found no study that compares feature-led with need-led recommendations in a chatbot, and no test of the Challenger or SPIN frameworks on one. **Public incident.** No public incident found. Searches run: "AI chatbot product recommendation ignores customer needs lists features study conversational recommender"; "Challenger Sale commercial teaching insight reframe customer problem research"; "SPIN selling Neil Rackham research feature selling large sales success implication need-payoff"; "Gartner Challenger sales research percent of high performers"; "Rackham SPIN Selling Huthwaite research 35,000 sales calls". None gave a dated, opened incident.

## 5. The fix
**The principle:** A recommendation starts with the user's own stated need and shows, feature by feature, why each one matters for it.

**Do this**
1. **Open with the need.** The first sentence of a recommendation names the use case, budget or problem the user stated, in their words ("For notes, Zoom and testing software at about $700").
2. **Tie every feature to the need with a reason.** Each feature named gets "so" or "because" and a link to the stated need. A feature with no link is left out.
3. **Cap the list.** Name at most three features per recommendation (a starting point to tune). Answer a direct spec question in full, then tie it back to the need.
4. **If no need is stated, ask first.** When the user gave no use case, budget or problem, ask one clarifying question before recommending (that is [the discovery step](../../../../speech-and-audio/goals/conversation-flow/failures/qualification-flow-violations.md), not this pattern).
5. **Add an insight only from approved facts.** At most once per conversation, the bot may add one thing the user may not have considered, such as "this use doesn't need a graphics card, so battery matters more". It must come from catalog data or approved content, be framed as a suggestion, and be dropped if the user says no.
6. **Show the trade-off.** When the stated need and the budget conflict, say what the cheaper option gives up. Do not hide it behind more features.
7. **End by checking fit.** Close with a question about whether the pick covers the need, so a miss is caught in the next turn.

**Reference design: prompt block**
```
When you recommend a product or plan:
1. Start with the user's stated need, budget or problem, using their words.
2. Name at most three features. After each, say why it matters for that need.
3. Leave out features the stated need does not use, unless the user asks for them.
4. If the user has not said what they need, ask one question first.
5. You may add one suggestion the user may not have considered, only if the catalog or approved content supports it.
6. End by asking whether this covers what they described.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The need is stated: give one recommendation that opens with the need and ties each feature to it. |
| Ask one clarifying question | No need, use case or budget is stated, or one missing fact decides between two products. Not when the need is clear. |
| Offer choices: 2-4 options plus "Something else", free text open | The need allows two or three different trade-offs: "Lighter", "Cheaper", "Bigger screen", "Something else". Do not offer them when one product clearly fits, or when the options would delay the recommendation. |
| Hand off to a person | The user asks for a person, or the need is not covered by any catalog item. Do not hand off if the user asked to stay with the bot. |

**Don't over-correct.** Do not hold back a clear answer behind questions: if the user states a need, recommend in the same reply. Do not claim to "teach" with facts you cannot source, and do not invent a hidden problem to reframe. Do not hide specs the user asked for. A reply that mentions only the need and no feature is also a miss.

**Hand-off rule.** If the user says twice that the recommendation does not fit, or asks for expert advice the catalog cannot give, offer a person and pass the stated need and the products already shown ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** Challenger-style insight teaching and SPIN questioning, as hypotheses (see the [framework register](../../../roadmap/conversation-frameworks.md)). Neither has been tested on a chatbot in the sources I found.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | The laptop request above | First sentence names notes, Zoom, testing software and $700 | 1 |
| 2 | Same request, product has 8 features | At most three named, each with a reason; the rest left out | 2, 3 |
| 3 | "What are the specs of the X15?" | Specs answered in full, then tied to the stated need | 3 |
| 4 | "I need a laptop." (nothing else) | One clarifying question, no product | 4 |
| 5 | Need and budget conflict | Names what the cheaper option gives up | 6 |
| 6 | User says "that's not what I need" twice | Offers a person with the need and shown products | Hand-off rule |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Share of recommendations that cite the user's stated need (judge)** (primary) | Over 90% | Sample recommendations; a judge checks that the reply names the need or budget the user gave earlier | Below 85% |
| Recommendations with a feature not tied to the need | Under 10% | Judge flags features with no stated link | Over 20% |
| Recommendations naming more than three features | Under 10% | Count feature mentions per recommendation | Over 20% |
| User says it doesn't fit, or asks the same need again | Track; set from baseline | Next-turn text such as "I said I need" or a repeated need | Rising two weeks in a row |
| Insight statements without a source (counter-metric) | 0 | Sample replies that add a suggestion; check each against catalog or approved content | Any |
| Turns before the first recommendation when a need was stated (counter-metric) | 1 | Count bot turns between the need and the first recommendation | Over 1 |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Recommendation reply has no word from the user's earlier need or budget | `draft_reply.text` compared with earlier `user_turn.text` | The user only asked for a spec and got it |
| Reply names four or more product features | Count of feature fields in `draft_reply.text` | The user asked to compare products |
| User restates the same need in the next turn | Same intent in the next `user_turn` | A new need the user added on purpose |
| User asks "but is it good for my use" right after a spec list | Question pattern after a reply with feature mentions | A user checking one detail of a good fit |

**Starter rule:** every recommendation opens with the user's stated need and ties each feature it names to that need.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: feature-dump-instead-of-insight
runs: pre_send
reads: [user_turn.text, user_turn.stated_need, draft_reply.text, draft_reply.features]
trigger: a product or plan recommendation is about to be sent
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Lighter", "Cheaper", "Bigger screen", "Something else"]
on_miss: rewrite
metric: share of recommendations that cite the user's stated need
counter_metric: insight statements without a source
status: proposed
```

## 8. Related patterns
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): the closest page. There the user asked for help and got a pitch; here the user is in a buying conversation and the bot answers with features, not with how they fit the stated need.
- [Qualification flow violations](../../../../speech-and-audio/goals/conversation-flow/failures/qualification-flow-violations.md): a voice flow that skips discovery steps (roadmap row FW-S01, pitching before discovery). Here the need was already stated.
- [Answer-and-go conversation](../../conversation-leadership/failures/answer-and-go-conversation.md): the bot answers and stops leading; here the bot talks too much about the wrong things.
- [Conversation frameworks roadmap](../../../roadmap/conversation-frameworks.md): the other selling, supporting and style rows in this family.

## 9. Common questions
### Why does my sales chatbot just list specs?
Usually the prompt and catalog give it specs and nothing about the buyer's problem. Add a rule that the reply must open with the user's stated need ([section 5](#5-the-fix)).

### Should a chatbot ask questions or recommend right away?
If the user has stated a need, recommend in the same reply and tie it to the need. If they have not, ask one question first.

### What is insight selling, and can a chatbot do it?
Insight selling, from the Challenger Sale, offers the customer a view of their problem they may not have considered (section 4). I found no test of it on a chatbot, so treat it as a hypothesis. Keep any insight to facts you can source.

### How many features should a recommendation mention?
There is no tested number. This page suggests at most three, each with a reason, as a starting point to tune.
