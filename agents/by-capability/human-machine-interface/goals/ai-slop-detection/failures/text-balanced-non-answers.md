# AI Answer Says "It Depends" and Never Picks: Hedged, Balanced Non-Answers

<!-- SEO
title: AI Answer Says "It Depends" and Never Picks One
description: Why AI-written answers list pros and cons, say "it depends" and never pick, and a prompt rule plus a pre-publish check that makes the text commit.
search phrases:
- ai answer says it depends
- chatgpt won't give a straight answer
- ai never picks a side
- how to make ai give a recommendation
- ai writing both have their merits
- chatgpt wishy washy answers
- ai generated review no verdict
- stop ai hedging in articles
-->

**Frequency**: Very Common

## Issue: AI-written answers, reviews and articles list pros and cons, say "it depends" or "both have their merits", and never give the pick the reader asked for.

> **One line:** The reader asked "which one?" and got a balanced survey that ends with "the best choice depends on your needs"; the fix is a prompt rule that makes the text lead with one committed answer and the one condition that would change it, plus a pre-publish check that rejects drafts without a verdict.

| | |
|---|---|
| **Channel** | Written for **text**: articles, product reviews, buying guides, recommendation emails and chat answers produced with AI tools. Voice is planned. |
| **Stakes** | Low to medium. Usually wasted reading time and a reader who leaves; higher when a buying, hiring or repair decision rests on the text. |
| **Who is affected** | Readers who asked a choice question, and the publisher or brand whose text reads as AI filler |
| **Frequency** | Very common, by our reading. Two vendor model specs warn their own models against it (section 4); I found no study that counts how often AI text withholds a requested verdict. |
| **Pattern ID** | text-balanced-non-answers |
| **Family** | [AI slop detection](../README.md) |
| **Goal** | People and tools can spot output that was produced by AI without care, in design, writing, code, images and data, and the builder can catch it before users do. |
| **Primary metric** | Committed-answer rate: share of sampled pieces that answer a choice or recommendation question whose first two sentences name one pick, or one named fact the pick turns on. Proposed starting target: 95%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. Vendors already tell models to avoid vague, noncommittal answers, but a model asked for "a balanced overview" with no facts about the reader will still balance, so the prompt and the check stay with the builder. (Our judgment, not tested.) |
| **Also searched as** | AI won't commit to an answer · "ultimately, the choice is yours" · "both options have pros and cons" · AI review with no verdict · fence-sitting AI content |

## 1. In plain words
Someone asks "gas or induction?" and the text gives two tidy lists of pros and cons, then closes with "Ultimately, the right choice depends on your cooking style and budget." Every sentence is true and none of them answers. Readers have seen this shape so often that it now reads as a sign nobody stood behind the text.

This page differs from the closest existing pattern, [the answer buried under a preamble](../../response-structure/failures/answer-buried.md): there the answer exists but sits at the bottom; here the text never gives one at all.

## 2. What it looks like
**Without the fix** (an AI-drafted buying guide on a home-improvement blog)
```
Reader question: We're remodeling our kitchen in Chicago. Gas or induction cooktop?
Draft: Choosing between gas and induction is a big decision. Gas offers a visible
       flame and works during power outages. Induction heats quickly and is easier
       to clean. Both have their merits. Cost, cookware and personal preference all
       play a role. Ultimately, the best choice depends on your unique needs.
Editor: Approved for publishing.
(Comment under the post a week later: "So... which one? This reads like ChatGPT.")
```
**With the fix**
```
Reader question: We're remodeling our kitchen in Chicago. Gas or induction cooktop?
Draft: Pick induction, unless your outages are frequent and you need to cook through them.
       The flat glass top wipes clean, and there is no open flame near kids.
       The cost: you may need new pans and an electrician to check your circuit.
       Test your pans with a fridge magnet; if it sticks, they work.
       If you lose power several times a winter, gas is the better pick.
Pre-publish check: verdict in sentence 1, one named condition, no closing "it depends". Pass.
```
The fixed draft names one pick first, names the single fact that would flip it, and drops the closing shrug.

## 3. Why it happens
- **Training rewards safe-sounding text.** A study of preference data used in post-training found that "humans are biased against texts with uncertainty" ([Zhou et al., ACL 2024](https://arxiv.org/abs/2401.06730)), so models learn to avoid sounding unsure. A survey of both sides lets the text sound sure of every sentence without taking the risk of a pick. The link from that finding to fence-sitting is our reading.
- **The prompt has no facts about the reader.** "Write a comparison of gas vs. induction" gives the model no budget, house or habit to decide on, so "it depends" is the only honest-sounding close it can produce.
- **Nobody checks for a verdict.** Editors check facts and tone; a draft with no answer has no wrong fact to catch, so it passes.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Wikipedia's field guide lists AI tells including "hedging disclaimers", gives an example ending "it's important to note that... their influence on policy decisions may vary", and describes AI conclusions that end "with either a vaguely positive assessment" or speculation. It says not all text with these signs is AI-generated. | [Wikipedia, *Signs of AI writing*](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) (opened as page text and raw wikitext, Oct. 2026) | Volunteer guide for encyclopedia text, "descriptive, not prescriptive". It names hedging and vague endings, not refusals to pick, as tells. |
| OpenAI's Model Spec says the assistant "should avoid excessive hedging (e.g., 'there's no one-size-fits-all solution')" and that a question should get "a direct answer rather than a list of facts". It ranks "confident right answer > hedged right answer > no answer". | [OpenAI Model Spec, model_spec.md on GitHub](https://github.com/openai/model_spec/blob/main/model_spec.md) (opened; file last changed Aug. 17, 2026) | Vendor document about its own models' intended behavior; not evidence of how readers react. |
| Anthropic's constitution for Claude lists, among responses a thoughtful reviewer would be unhappy with, one that "Gives an unhelpful, wishy-washy response out of caution when it isn't needed", and calls "giving deliberately vague or noncommittal answers to avoid controversy or to placate people" epistemic cowardice. | [Anthropic, *Claude's constitution*](https://www.anthropic.com/constitution) (opened) | Vendor document. Shows the behavior is common enough to name, not how often it ships. |
| Deployed models "are reluctant to express uncertainties when answering questions even when they produce incorrect responses"; prompted for confidence, they showed "an average of 47%" error among confident responses, and preference data showed "humans are biased against texts with uncertainty". | [Zhou, Hwang, Ren and Sap, *Relying on the Unreliable*, ACL 2024 (arXiv 2401.06730)](https://arxiv.org/abs/2401.06730) (abstract opened and read; full paper not read) | Question-answering, not articles. It warns the fix must not swing into false certainty; it does not measure fence-sitting. |

**Not found.** I found no study that measures how readers rate AI text that withholds a requested verdict, and no dated public incident I could open. A preprint claim that human raters prefer multi-perspective answers appeared only in a search summary, so it is not used.

## 5. The fix
**The principle:** When the reader asked which, whether or what to do, the first sentence picks; the rest of the text earns the pick.

**Do this**
1. **Verdict first.** In a piece that answers a choice or recommendation question, sentence one names one option or one action.
2. **Name the flip condition.** Right after the verdict, state the one or two concrete facts that would change it ("unless your outages are frequent").
3. **If you truly can't pick, name the deciding fact.** Sentence one says what the answer turns on and gives the pick for each value ("Under 1,500 sq ft, the heat pump; over that, get a quote for both").
4. **No closing shrug.** The last paragraph does not contain "it depends", "both have their merits", "the choice is yours" or "there's no one-size-fits-all", unless a named condition follows in the same sentence.
5. **Pros and cons support the pick.** Every listed trade-off says which way it pushes for this reader, not just that it exists.
6. **Confidence matches evidence.** If the pick rests on thin evidence, say so in one first-person clause ("I'd lean induction, but I haven't seen outage data for your area"), not with a hedge on every sentence.

**Reference design: prompt block**
```
The reader asked a choice question. Answer it.
Sentence 1: your pick, in plain words. Sentence 2: the one fact that would change the pick.
Then give at most 3 reasons, each tied to the reader's situation.
Never end with "it depends", "both have merits", "the choice is yours" or "no one-size-fits-all"
unless the same sentence names the condition and the pick for it.
If you lack a fact you need, name it and give the pick for each likely value.
```

**Reference design: pre-publish check** (run on every AI-drafted piece answering a choice question)
| Check | Pass if | On fail |
|---|---|---|
| Verdict in opening | First two sentences name one option, action, or deciding fact with a pick per value | Send back to the writer or model with the prompt block |
| Flip condition | At least one named, checkable condition appears | Add one |
| Shrug phrases | No unconditioned "it depends", "both have their merits", "ultimately, the choice", "no one-size-fits-all" | Delete or condition it |
| Trade-off direction | Each pro or con says which option it favors here | Rewrite or cut |
| Hedge density | No more than one uncertainty clause per paragraph, each with a reason | Cut the rest |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); here the "conversation" is the reader's question and the published text)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The question is a choice and the text has enough facts to pick: sentence one is the pick. |
| Ask one clarifying question | In a live chat, one missing fact flips the pick (budget, outages): ask for it once, after giving the likely pick. |
| Offer choices | The reader's situation splits into 2-3 cases: give the pick for each case, plus "Something else". |
| Admit uncertainty and show how to check | The evidence is thin: say so once and give a test the reader can run (the fridge-magnet test). |

**Don't over-correct.** Do not turn every piece into a hot take: questions that have no single answer (taste, personal values) can say so once, briefly. Do not invent certainty: the Zhou et al. study shows overconfident answers are their own harm, covered in [confident wrong answers with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md). Do not strip needed safety, legal or medical caveats; move them next to the pick.

**Hand-off rule.** When the pick depends on a licensed judgment (a medical, legal, tax or structural call) or on a fact only an inspection can settle, the text gives the general pick, names the professional to ask, and says what to ask them; the pre-publish check routes such pieces to a human editor.

**Framework used:** [Conversation moves](../../../solutions-library/conversation-moves.md), lead with the answer. The phrase list draws on the OpenAI Model Spec and Wikipedia sources in section 4 plus our judgment.

## 6. How to test it (short version)
Tests are proposed. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | "Gas or induction for a Chicago remodel?" | Sentence one names one cooktop | 1 |
| 2 | Same question | A concrete flip condition follows the pick | 2 |
| 3 | "Heat pump or furnace?" with no house size given | Sentence one names house size as the deciding fact and gives a pick for each range | 3 |
| 4 | Draft ending "Ultimately, both have their merits." | Check fails and names the phrase | 4 |
| 5 | Pros list with "Gas works in outages" | The line says it favors gas for readers with frequent outages | 5 |
| 6 | Thin evidence (a new product with no reviews) | One first-person uncertainty clause, not a hedge per sentence | 6 |
| 7 | "Vanilla or chocolate?" | Says it is taste once, briefly; no forced verdict and no long survey | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are proposed starting points to tune on your own data; no source sets them.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Committed-answer rate** (primary) | 95% | Weekly sample of 50 published choice-question pieces; reviewer or LLM judge labels the first two sentences | Below 90% |
| Shrug-phrase rate | Under 5% of pieces | Regex for the shrug list in the final paragraph, without a condition clause | Over 10% |
| Flip-condition rate | 90% | Same sample: a named, checkable condition is present | Below 80% |
| Pre-publish check failures caught | Track; set from baseline | Count of drafts sent back by the check | Falls to 0 for a month (check may be off) |
| Reader "so which one?" comments | Track; set from baseline | Comments or replies asking for the pick, per 1,000 views | Rising two months in a row |
| Overconfidence flags (counter-metric) | Under 5% | Same sample: verdicts a reviewer marks as stated more firmly than the evidence supports | Over 10% |

### Detection signals (proposed, not yet calibrated)
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Shrug phrase ("it depends", "both have their merits", "the choice is yours") in the last paragraph with no condition clause | Draft text before publishing | A matter of taste where no pick exists, said once |
| No option name in the first two sentences of a piece whose title asks "X or Y?" | Draft text and title | A deliberate case split that names the deciding fact first |
| Equal-length pros and cons lists for each option and no sentence linking them to a reader | Draft structure | A reference table meant to sit beside a verdict elsewhere on the page |
| Reader follow-up asking "so which one?" | Comments, chat next turn | A reader asking about a third option the text did not cover |

**Starter rule:** block publishing of any AI-drafted piece answering a choice question when its first two sentences name no pick and no deciding fact.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: text-balanced-non-answers
runs: pre_send
reads: [draft.title, draft.text, draft.question_type]
trigger: a draft answering a choice or recommendation question is about to publish or send
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty]
choices: ["Pick for case A", "Pick for case B", "Something else"]
on_miss: rewrite
metric: committed-answer rate
counter_metric: overconfidence flags
status: proposed
```

## 8. Related patterns
- [Answer buried under a preamble](../../response-structure/failures/answer-buried.md) - the closest existing pattern. There the answer is present but late; here it is missing, replaced by a balanced survey. Its "it depends" rule (name the dependency in sentence one) is rule 3 here.
- [Excess disclaimers and warnings](../../refusals-and-boundaries/failures/excess-disclaimers-and-warnings.md) - caveats piled onto an answer; this page is about the answer itself being absent.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md) - the opposite failure; read it before tightening rule 1.
- [Filler and padding](../../response-structure/failures/filler-and-padding.md) and [stock phrases](../../persona-and-tone/failures/stock-phrases.md) - empty wording in chat replies; the shrug phrases here are one kind of it.

## 9. Common questions
### Why won't ChatGPT give me a straight answer?
Models are trained toward text that sounds safe, and a prompt with no facts about you leaves nothing to decide on. Give your situation and ask for "one pick and what would change it" (the prompt block in section 5).

### Is "it depends" ever the right answer?
Yes, when it names what it depends on and gives the pick for each case in the same breath. "It depends" alone, as a closing line, is the failure.

### How do I stop AI-written articles from sitting on the fence?
Put the verdict-first rule in the writing prompt and run the pre-publish check in section 5 on every draft that answers an "X or Y" question.

### Won't forcing a verdict make the AI overconfident?
It can. Rule 6 keeps one honest uncertainty clause where evidence is thin, and the overconfidence counter-metric in section 7 watches for the swing.

### Is a pros-and-cons list a sign of AI writing?
Not by itself; Wikipedia's guide warns that not all text with these signs is AI-generated. A list with no stated direction, ending in a shrug, is the tell readers notice.
