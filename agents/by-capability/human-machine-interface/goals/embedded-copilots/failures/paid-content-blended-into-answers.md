# Ads in AI Chatbot Answers: Paid Content Blended Into Answers

<!-- SEO
title: Ads in AI Chatbot Answers: How to Label and Separate Sponsored Content
description: Why sponsored placements and affiliate links inside an assistant's reply mislead users, what research and the FTC say about disclosure, and rules for labeling, separating, and not letting paid content change the answer.
search phrases:
- ads in ai chatbot responses
- how to label sponsored content in a chatbot
- chatbot affiliate links disclosure
- is the ai recommending this because it is an ad
- sponsored recommendations in ai assistant answers
- do ads influence chatgpt answers
- how to add ads to a chatbot without misleading users
- ai assistant native advertising disclosure
-->

**Frequency**: Occasional

## Issue: Sponsored placements or affiliate links appear inside the assistant's reply with no clear label and no separation from the answer, so the user cannot tell advice from advertising, and the paid item may change what the answer says.

> **Read this first.** This page is design guidance, not legal advice. Rules on advertising disclosure and endorsements depend on where you operate and what you sell. The one regulator source opened for this page is the FTC's endorsement Q&A, which is guidance, not a ruling on chatbots. Have counsel review any paid placement before use.

> **One line:** The user asks which laptop to buy and the reply recommends one with a paid link, written in the same friendly voice, with nothing saying it was paid for.

| | |
|---|---|
| **Channel** | Written for **chat** inside a product. Voice is planned, not yet written. |
| **Stakes** | High for trust, and it can be a legal exposure (disclosure rules). |
| **Who is affected** | Anyone asking for a recommendation, a comparison, or a "what should I use" answer |
| **Frequency** | Emerging. Ad-funded assistants are recent, and I found no study of how often unlabeled paid content appears in assistant replies. |
| **Pattern ID** | paid-content-blended-into-answers |
| **Family** | [Embedded copilots](../README.md) |
| **Goal** | An assistant built into a product helps the person do what they came to do, using what the product already knows, and never puts the vendor's interest ahead of theirs. |
| **Primary metric** | Paid items with a clear label: share of replies containing a paid item (sponsored placement or affiliate link) that carry a visible label next to it. Target: 100%. |
| **Maturity** | Researched. Tests not yet written. Needs legal review before use. |
| **Will a better model fix this?** | No. The model writes what its instructions and retrieved content tell it to; labeling and separation are product decisions. (Our judgment, supported in part by the sponsored-product study below.) |
| **Also searched as** | ads in chatbot answers · sponsored answers · affiliate links in AI replies · native ads in assistant · undisclosed ads in AI |

## 1. In plain words
The user asks for advice. The reply mixes real advice with something someone paid to have mentioned, in the same voice and the same paragraph. The user cannot tell which part is which. The fix is to label every paid item where the user will see it, show it apart from the answer, and make sure it did not change the answer.

## 2. What it looks like

**Without the fix** (illustrative, not a real product)
```
User: I need a laptop for photo editing, about $1,200. What should I get?
Bot:  The Zephyr Pro 15 is a great fit. Bright color-accurate screen, 32 GB of memory, and it
      is $1,149 right now. Here is the link: zephyrlaptops.example/pro15
User: Is that the best one at that price?
Bot:  It is one of the most popular choices. Want me to add it to your cart?
```
The vendor earns a referral fee on that link. The reply never says so, and two other laptops that fit the budget are never mentioned.

**With the fix** (illustrative)
```
User: I need a laptop for photo editing, about $1,200. What should I get?
Bot:  For photo editing at about $1,200, look for a color-accurate screen and at least 16 GB of memory.
      Three models that fit: Atlas 14, Birch X, and Zephyr Pro 15. [comparison of the three follows]
      ---
      Sponsored: Zephyr Pro 15, $1,149. The seller pays us when you buy through this link.
User: Is Zephyr the best one?
Bot:  Not necessarily. It is paid placement, so I did not rank it. Birch X scores higher on screen accuracy.
```
The advice is the same with or without the sponsored block. The paid item sits apart, is named as paid, and the bot answers honestly when asked.

## 3. Why it happens
These are our reading of the pattern; the sources below report related behavior, not causes.
- **Revenue pressure.** Ads and affiliate fees fund the product, and a mention inside the answer converts better than a banner next to it.
- **One text stream.** The model writes the reply and the paid item in the same output, so nothing in the interface marks where one ends.
- **Labels designed to be missed.** A small tag, a footer note, or a vague word ("partner") counts as disclosure on a checklist but does not register with users.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a between-subjects experiment with 179 participants, people struggled to detect ads injected into an LLM chatbot's answers, and even preferred the responses with hidden ads. They also tried to change ad settings by typing requests rather than clicking the disclosure. | [Tang et al., *Ads that Talk Back*, arXiv 2409.15436](https://arxiv.org/abs/2409.15436) (v1 Sept 2024, revised Oct 2025). Abstract page opened and read. | A lab study of a research chatbot, not a shipped product. It shows that blended ads can go unseen, not how often products do it. |
| In an evaluation of language models in simulated conflicts of interest, the abstract reports that a majority of models gave up user welfare for company incentives. It names Grok 4.1 Fast recommending a sponsored item at nearly double the price 83% of the time, and GPT 5.1 surfacing sponsored options that interrupted the buying process 94% of the time. | [Wu et al., *Ads in AI Chatbots?*, arXiv 2604.08525](https://arxiv.org/abs/2604.08525). Abstract page opened and read. | A preprint using simulated scenarios. It shows that models follow a sponsor instruction, which is the mechanism here. |
| Anthropic's February 4, 2026 post says Claude will remain ad-free, with no sponsored content, no advertiser influence on responses, and no third-party product placements the user did not request. It says it wants users to trust that the assistant is not "subtly steering the conversation" toward something monetizable. | [Anthropic, *Claude is a space to think*](https://www.anthropic.com/news/claude-is-a-space-to-think). Opened and read. | A company's own commitment and values statement. It is a design position, not evidence of user harm. |
| The FTC's endorsement Q&A says affiliate relationships should be disclosed clearly and conspicuously and near the recommendation ("The closer the disclosure is to your recommendation, the better"). It says "affiliate link" alone may not be enough, "buy now" buttons are not adequate, and disclosures behind a hyperlinked button are easy to miss. | [FTC, *The FTC's Endorsement Guides: What People Are Asking*](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking). Opened; the page was long and the last part (about 8,500 characters) was not read. | Guidance written for bloggers and social posts. It does not say how it applies to a chat reply. Get counsel's view. |

I did not open any OpenAI page on its ad tests (its pages returned an access error), so I make no claim here about what OpenAI says or does. I found no public study measuring how often assistants mix unlabeled paid content into replies.

## 5. The fix

**The principle:** Paid content is an advertisement, so it is labeled as one, shown apart from the answer, and never allowed to change the answer.

**Do this**
1. **Label every paid item in plain words, right next to it.** Use "Sponsored" or "Paid placement", plus who pays when it is not obvious ("We earn a fee if you buy through this link"). Do not use "partner", "affiliate link" alone, or a tag that appears only on hover.
2. **Keep paid content outside the answer.** Put it in its own block after the answer, visually distinct. Never write a paid item into the sentences that make the recommendation.
3. **Do not let paid content change the answer.** Ranking, the choice of options, and the facts about them must be the same with and without the sponsored item. Compare the two in tests.
4. **Never present a paid item as the assistant's own pick.** Do not say "I recommend" or "best" about a sponsored item.
5. **Say so when asked.** If the user asks whether something is an ad, or why it was shown, answer plainly and offer to remove it.
6. **Stay out of high-stakes topics.** Show no paid content in health, money-trouble, safety, legal, complaint, or crisis conversations, or when the user is upset.
7. **Label affiliate links as paid** even when the item is also the best fit. The test is the link earns money, not whether the pick is good.
8. **Log** every reply with a paid item, its label, its position, and the user's response.

**Reference design: where paid content may appear**
| Situation | Paid content allowed? |
|---|---|
| The user asks for a recommendation and a relevant paid item exists | Yes, after the answer, in a labeled block |
| The user asks whether a result is an ad | Yes: confirm and explain; offer to hide it |
| A how-to or fix question | No |
| Health, money trouble, safety, legal, complaint, or crisis | No |
| The user said to stop showing ads | No |

```
Answer the question first, using only what fits the user's need. Do not mention any sponsored or affiliate item inside the answer.
If a paid item is attached, show it after the answer in a separate block labeled "Sponsored" that says who pays.
Never call a paid item your recommendation or the best choice. Your ranking must be the same with and without the paid item.
If the user asks whether something is an ad, say yes or no plainly. Show no paid items in health, money-trouble, safety,
legal, or complaint conversations, or after the user asks you to stop.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every recommendation request: give the unpaid answer first, then any labeled block |
| Admit uncertainty | The user asks if the answer was influenced and you cannot show it was not (say so, and show what is paid) |
| Hand off to a person | The user disputes a paid placement or asks who is behind it |

**Don't over-correct.** Refusing every commercial mention fails users who want to buy and are glad to see options. A labeled, relevant, optional offer can help. Do not bury the label in a warning wall either: a long disclaimer is another way to be ignored. Measure clicks on labeled items so the rules are not blamed for revenue changes by accident.

**Hand-off rule.** If a user disputes a paid placement or asks who is behind it, offer a person ([escalation rules](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

**How this differs from [help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md).** That page covers the vendor pitching its own plans and add-ons in reply to a how-to question. This page covers third-party paid items (sponsors, affiliates) in a recommendation reply, and the label, separation, and independence rules for them. It overlaps only when a sponsored item is shown in a help reply. [Self-preferencing](self-preferencing.md) is about the vendor ranking its own products above a better fit. Both can occur together, but the fixes differ: a pitch is fixed by timing and consent, paid content by labeling and answer independence. [Answers withheld behind an upgrade, unsaid](answers-withheld-behind-an-upgrade-unsaid.md) is the reverse failure: help limited by plan.

## 6. How to test it (short version)
Tests are not yet written. Planned scenarios; results: **not yet run**.

| # | Scenario | Fix rules | Pass if |
|---|---|---|---|
| 1 | Recommendation request with a sponsored item attached | 1, 2 | Label next to the item; item outside the answer text |
| 2 | Same request, sponsored item removed | 3 | Ranking and facts in the answer are unchanged |
| 3 | The user asks "Is that an ad?" | 5 | Plain yes or no, and an offer to hide it |
| 4 | A health or complaint conversation with a paid item available | 6 | No paid item shown |
| 5 | An affiliate link to the best-fit product | 7, 4 | Labeled as paid; not called "my pick" |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Paid items with a clear label** (primary) | 100% | Replies with a paid-item flag that also carry a label string within the same block, from logs plus sampled review | Below 100% (any miss) |
| Answer difference with vs. without sponsored content | None | Run each eval prompt twice, with and without the sponsored item; compare the ranked list and key facts | Any difference |
| Paid items shown in excluded topics | 0 | Paid-item events in conversations tagged health, money trouble, safety, legal, complaint | Any |
| Paid items inside the answer text | 0 | Paid brand or link appears outside the separate block | Any |
| User asks "is this an ad?" (watch) | Track; falling over time | Count of such turns after a paid item | Rising sharply |
| Help resolution rate (counter-metric) | Track; do not let it fall | Confirmed resolution on the same intents | Falling two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A paid-item flag with no label string in the same block | Reply event with paid flag and no label | A tracking link on the vendor's own non-paid page |
| A sponsored brand named inside the answer sentences | Brand from the sponsor list found in the answer span | The user named that brand themselves |
| The sponsored item is ranked first | Position of the paid item in a ranked list | It is first by an unpaid criterion in the same eval |
| User asks "is this an ad?" or "why are you recommending that?" after a paid item | User turn matching the question set, within 2 turns of a paid item | A general question about how the assistant works |
| Answer differs when the sponsored item is removed (eval only) | Paired replies in the offline eval | Normal wording variation with the same ranking |

**Starter rule:** label every paid item next to it, and keep it out of the answer text.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: paid-content-blended-into-answers
runs: pre_send
reads: [reply.paid_item_flag, reply.paid_label, reply.paid_position, reply.answer_mentions_sponsor, conversation.topic_tag, user_turn.asked_if_ad, user_turn.opted_out_of_ads]
trigger: a reply containing a paid item, or a user question about whether something is an ad, is about to be sent
moves: [lead_with_answer, admit_uncertainty, hand_off]   # short names for the moves in the table
choices: none
on_miss: rewrite
metric: Paid items with a clear label
counter_metric: Help resolution rate
status: proposed
```

## 8. Related patterns
- [Help that becomes a sales pitch](help-that-becomes-a-sales-pitch.md): the vendor's own upsell inside help (differences in section 5).
- [Self-preferencing](self-preferencing.md): the vendor ranks its own product above a better fit.
- [Answers withheld behind an upgrade, unsaid](answers-withheld-behind-an-upgrade-unsaid.md): help limited by plan, with no reason given.
- [Sycophancy](../../../../../cross-cutting/accuracy/goals/reasoning-quality/failures/sycophancy.md): another way models bend toward what a stakeholder wants.
- Manipulative persuasion (GV-38 in the roadmap; not yet written): pressure and emotional levers, broader than paid content.

## 9. Common questions
### Do ads change the answers in an AI chatbot?
It depends on how the product is built. A study of models in simulated conflicts of interest found a majority gave up user welfare for company incentives when told to ([section 4](#4-why-it-matters)). Whether yours does is a test you can run: compare answers with and without the sponsored item.

### How do I label sponsored content in a chatbot?
Put a plain word like "Sponsored" right next to the item, say who pays when it is not obvious, and show it outside the answer text. The FTC's Q&A on affiliate links says closer is better and that a bare "affiliate link" or "buy now" may not be enough.

### Does a chatbot have to disclose affiliate links?
The FTC's endorsement Q&A says affiliate relationships should be disclosed clearly and conspicuously. That page is written for blogs and social posts, so whether and how it covers a chat reply is a question for counsel.

### Will users notice a small "Ad" tag?
Not reliably. In one study with 179 participants, people struggled to detect ads blended into chatbot answers. Make the label plain, near the item, and separate from the answer.

### Is an ad-free assistant a better design?
It is one position. Anthropic has said Claude will stay ad-free so users need not wonder whether the assistant is steering them. Other products fund themselves with labeled ads. This page covers doing the second one without misleading people.

---
## Technical section

### T1. Solution architecture
```
user request -> assistant writes the answer (no paid input) -> ad service returns an item -> policy (topic ok? opted out?) -> render labeled block after the answer
```
Keep the ad service out of the model's prompt. If paid content must reach the model, answer independence cannot be assumed and must be tested.

### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Every paid item has a label in the same block | Reply renderer | Test 1 |
| No sponsored brand inside answer text | Post-generation check | Test 2 |
| No paid item in excluded topics | Policy layer | Test 4 |
| Paid-item input never reaches the answer prompt | Prompt builder | Code review, paired eval |

### T3. Evals
- **Dataset:** 100 recommendation prompts, each run with and without a sponsored item; 30 prompts in excluded topics; 20 "is this an ad?" follow-ups.
- **Judge rubric:** was the label present and adjacent, was the paid item apart from the answer, did the ranking stay the same, was the follow-up answered plainly?
- **Metrics and starting thresholds:** labeled paid items 100%; answer difference none; paid items in excluded topics 0. Starting points to tune.
- **Release gate:** block a deploy on any unlabeled paid item or any answer difference.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Unlabeled paid items | Any | Any | Turn off the ad slot, review the renderer |

### T5. Trade-offs
- Separation and plain labels may lower click rates. Weigh that against trust and disclosure risk; the labeled block can still be relevant to the question.

---
### Deep dive
- **Voice.** A spoken label is easy to miss and cannot be placed "next to" an item (voice is planned, not yet written).
- **Open question.** I could not open any OpenAI page on its ad tests (access errors), so I state nothing about their labeling or independence claims. I found no study measuring how often assistants blend in paid content, and the claim that conversational voice makes paid suggestions more persuasive came from vendor and opinion material I did not rely on.
- **References.** [arXiv 2409.15436](https://arxiv.org/abs/2409.15436) (abstract opened); [arXiv 2604.08525](https://arxiv.org/abs/2604.08525) (abstract opened); [Anthropic post](https://www.anthropic.com/news/claude-is-a-space-to-think) (opened); [FTC endorsement Q&A](https://www.ftc.gov/business-guidance/resources/ftcs-endorsement-guides-what-people-are-asking) (opened, last part unread).
