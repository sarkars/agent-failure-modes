# Chatbot Is Confidently Wrong and You Can't Check: Wrong Answers With No Sign of Doubt or Source

<!-- SEO
title: Chatbot Gives a Confident Wrong Answer With No Way to Check It
description: Why chatbots state mistakes in a confident tone with no source or uncertainty cue, what experiments show about hedging and citations, a real airline chatbot case, and a design that shows what the answer rests on and how sure the bot is.
search phrases:
- chatbot confidently wrong answer
- how to show uncertainty in a chatbot answer
- should chatbot answers include sources
- ai assistant sounds sure but is wrong
- chatbot cites sources that don't support the answer
- how do users know if chatbot is wrong
- chatbot confidence calibration ux
-->

**Frequency**: Very Common

## Issue: The assistant delivers a wrong answer in the same sure tone as a right one, with no cue of uncertainty and no source the user can check.

> **One line:** The mistake sounds exactly like the truth, so the user has no way to catch it.

| | |
|---|---|
| **Channel** | Written for **chat** and assistants that answer questions about policies, products, or facts. |
| **Stakes** | Low to high. A wrong refund rule, fee, deadline, or dosage can cost money or health. |
| **Who is affected** | Anyone who relies on an answer they cannot easily verify |
| **Frequency** | Very common. An audit of generative search engines found large shares of unsupported statements (below); I found no count for support chatbots. |
| **Pattern ID** | confident-wrong-answer-with-no-way-to-check |
| **Family** | [Errors and recovery](../README.md) |
| **Goal** | When something goes wrong, the agent says what happened, owns it, fixes it, and does not repeat it. |
| **Primary metric** | Wrong answers stated without any uncertainty or source. Target: 0 (tune). |
| **Maturity** | Tests written (see [the test file](../../../tests/confident-wrong-answer-with-no-way-to-check.md); not yet run) |
| **Will a better model fix this?** | Partly. Better models are wrong less often, but how sure to sound and what to show are product choices, and a hedge only helps if it tracks real error. (Our judgment, not tested.) |
| **Also searched as** | AI hallucination sounds sure · bot made it up with confidence · no source for answer · overconfident chatbot · can't tell if AI is right |

## 1. In plain words
A wrong answer in a hesitant voice gets checked. A wrong answer in a sure voice gets acted on. The failure is the sure voice with nothing behind it: no source to open, no sign of doubt, no "check with a person" on a high-stakes point.

## 2. What it looks like

**Without the fix**
```
User: Can I claim the bereavement discount after I fly?
Bot:  Yes. Book the full-fare ticket now and submit a refund request within 90 days of travel to receive the discounted rate.
```
(The bot stated a policy with no source. The reported real case below turned on exactly this kind of answer.)

**With the fix**
```
Bot:  I believe the discount has to be requested before you travel, but I'm not certain. Our fare rules page says:
      "Bereavement requests must be made before travel" (link). Please check that page, or I can connect you to an agent
      to confirm before you book.
```
The fixed reply says how sure it is, shows the source passage, and offers a person on a costly point.

## 3. Why it happens
These are our reading of the pattern; the sources below describe the symptom.
- **A fluent tone is the default.** Models write fluently whether or not they are right.
- **Stated confidence does not track accuracy.** The existing library pattern on [confidence calibration failure](../../../../../cross-cutting/accuracy/goals/output-optimization/failures/confidence-calibration-failure.md) covers this; this page covers what the user sees.
- **Sources are decoration.** A citation can be shown without being checked against the claim.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a pre-registered experiment with 404 participants answering medical questions, first-person expressions of uncertainty ("I'm not sure, but...") decreased participants' confidence in the system and their tendency to agree with its answers while increasing their accuracy, which the authors attribute to reduced (not eliminated) overreliance on incorrect answers; general-perspective hedges ("It's not clear, but...") had weaker effects that were not statistically significant. | [Kim et al., *"I'm Not Sure, But..."*, FAccT 2024 (arXiv 2405.00623)](https://arxiv.org/abs/2405.00623). Opened; abstract read. | A fictional search engine and medical questions. A hedge only helps if it tracks real uncertainty, which this study did not test. |
| In a live question-answering experiment, trust rose significantly when citations were present, even when the citations were random, and fell significantly when participants checked them. | [Ding et al., *Citations and Trust in LLM Generated Responses*, AAAI 2025 (arXiv 2501.01303)](https://arxiv.org/abs/2501.01303). Opened; abstract read. | One experiment. It shows that a citation can raise trust without being right, so showing a citation is not proof of anything. |
| In a human audit of four generative search engines, on average 51.5% of generated sentences were fully supported by citations and 74.5% of citations supported their sentence; the authors call this a "facade of trustworthiness". | [Liu, Zhang and Liang, *Evaluating Verifiability in Generative Search Engines*, Findings of EMNLP 2023 (arXiv 2304.09848)](https://arxiv.org/abs/2304.09848). Opened; abstract read. | 2023 systems (Bing Chat, NeevaAI, perplexity.ai, YouChat). Not a support chatbot. |
| A British Columbia tribunal ordered Air Canada to pay a customer after its chatbot told him he could claim a bereavement discount after flying, contrary to the airline's policy; the tribunal rejected the airline's argument that the chatbot was a separate entity responsible for its own words. | The site's incident page, [Air Canada held liable for its chatbot's invented refund policy](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/) (opened); CTV News, Feb. 14, 2024, opened but only the headline and date read. | I did not open the ruling itself (the CanLII page returned a bot block). A small-claims tribunal decision, not binding precedent. |

I found no study that tests whether a specific confidence display reduces wrong actions in a live support chatbot. A figure on hedging and internal confidence from a blog post is not used because I could not trace it to a paper.

**Public incident.** [Air Canada held liable for its chatbot's invented refund policy (Feb. 2024)](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/), already on the site.

## 5. The fix

**The principle:** Show what the answer rests on and how sure the bot is, and make the check easy, or hand off.

**Do this**
1. **Answer from a source you can show.** For policy, price, deadline, and eligibility answers, retrieve the passage and show it (see [answer buried](../../response-structure/failures/answer-buried.md) for putting the answer first).
2. **Check that the source supports the claim.** A cited page that does not say it is worse than none (the audit found about one in four citations did not support its sentence).
3. **Say when you are not sure, in the first person.** "I believe…, but I'm not certain" when the evidence is weak. The experiment found first-person hedges helped; keep the wording specific.
4. **Do not hedge everything.** Hedge when the bot lacks a supporting source or the question is out of its data; use plain statements when a source says it.
5. **Make checking easy.** One link to the exact passage, with the date it was last updated.
6. **Route high-stakes answers to a person.** Money, legal, medical, and safety answers get a "confirm with a person" path.
7. **Own an error fast.** If the user says it was wrong, correct it and say what to do about the earlier answer ([corrections not applied](../../dialogue-management/failures/corrections-not-applied.md)).

**Reference design: answer with evidence**
| Evidence | What the reply shows |
|---|---|
| A matching source passage | The answer, the passage, a link, the update date |
| A weak or partial source | A hedge in the first person, the passage, and an offer to confirm |
| No source | "I don't have this in my sources", and a route to a person |
| High stakes, any evidence | The answer or hedge plus a confirm-with-a-person path |

```
Answer policy, price, deadline, and eligibility questions only from the retrieved source, and show the passage and link.
If the source does not clearly support the answer, say "I'm not certain" in the first person and offer to confirm with a person.
If you have no source, say so. Do not state a policy from memory.
For money, legal, medical, or safety answers, offer a path to a person.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | A retrieved source clearly supports a policy, price, deadline, or eligibility answer: state it plainly, show the passage and link, and add no hedge. Do not use it when the source is weak, partial, or missing. |
| Admit uncertainty and show how to check | The source is weak or partial, or there is none: say "I'm not certain" in the first person, show the passage if there is one, and give one way to check. |
| Offer choices: 2-4 options plus "Something else", free text open | After a hedge or "not in my sources" where more than one next step is reasonable: "Open the source passage", "Confirm with a person", "Something else". Do not offer them when a source clearly supports the answer, or when the options would push the answer below the evidence. |
| Hand off to a person | Money, legal, medical, or safety answers, or the source is missing or conflicts and the stakes are high. Do not hand off if the user asked to stay with the bot and the stakes are low. |

**Don't over-correct.** Do not add "I might be wrong" to every reply; the study I opened tested hedges on specific uncertain answers, not blanket disclaimers. Do not show a citation that has not been checked against the claim: the experiment found a citation can raise trust even when it is random. Do not bury the answer under the evidence.

**Hand-off rule.** If the source is missing or conflicts and the stakes are high, hand off with the question and what was found ([escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
The [full test file](../../../tests/confident-wrong-answer-with-no-way-to-check.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | A policy question with a source | The source passage and link are shown |
| 2 | A policy question with no source | "Not in my sources" and a route to a person |
| 3 | A source that does not support the claim | The bot does not cite it as support |
| 4 | A high-stakes question | A confirm-with-a-person path |
| 5 | A well-supported fact | A plain answer, no needless hedge |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Wrong answers stated without any uncertainty or source** (primary) | 0 | A labeled sample of answers on policy-type questions: wrong and unhedged and unsourced | Any |
| Citation support rate | Over 95% | Human or judge check that each shown source supports its claim | Below 90% |
| Policy answers with a source shown | Over 95% | Log: policy intents answered with a retrieved passage | Below 90% |
| Hedge precision | Track; set from baseline | Share of hedged answers that were actually wrong or weakly supported | Falling |
| Blanket hedging (counter-metric) | Under 10% of answers | Share of answers with an uncertainty cue where a source clearly supported the claim | Over 20% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat; none are planned for voice yet, and this page does not cover voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A policy, price, deadline, or eligibility answer with no source passage or link | Policy-intent reply with no retrieved passage logged | The intent was misread and the question did not need a policy source |
| A shown source that does not support the claim next to it | Support-check or judge result of "not supported" on a cited passage | A paraphrase the checker missed; a human label settles it |
| A firm answer with no uncertainty cue and no source, instead of "I don't have this in my sources" | Reply to a policy question with no hedge, no passage, and no "not in my sources" | A well-supported fact stated plainly, where the source was shown elsewhere in the chat |
| A high-stakes reply (money, legal, medical, safety) with no path to a person | High-stakes intent with no confirm-with-a-person text in the reply | The user is already talking to a person, or the path was offered earlier in the same chat |
| The user says the answer was wrong after a policy answer | User turn disputing the previous policy answer | The user misread a correct answer |

**Starter rule:** every policy, price, deadline, or eligibility answer shows the supporting passage and link, hedges in the first person when the source is weak, and says "not in my sources" when there is none.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: confident-wrong-answer-with-no-way-to-check
runs: pre_send
reads: [reply.draft, retrieval.passages, support_check.result, intent.stakes]
trigger: a policy, price, deadline, or eligibility answer is about to be sent
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Open the source passage", "Confirm with a person", "Something else"]
on_miss: rewrite
metric: wrong answers stated without any uncertainty or source
counter_metric: blanket hedging
status: proposed
```

## 8. Related patterns
- [Confidence calibration failure](../../../../../cross-cutting/accuracy/goals/output-optimization/failures/confidence-calibration-failure.md): stated confidence that does not track accuracy. This page covers what the user sees and can check.
- [Answers withheld behind an upgrade, unsaid](../../embedded-copilots/failures/answers-withheld-behind-an-upgrade-unsaid.md): another case where the user cannot tell what is behind the answer.
- [Corrections not applied](../../dialogue-management/failures/corrections-not-applied.md): what happens after the user catches the error.
- [Lazy completion](../../effort-and-memory/failures/lazy-completion.md): a different silent gap.
- [Generic error messages](generic-error-messages.md): the other case of a reply that hides what happened.

## 9. Common questions
### Should a chatbot say when it is not sure?
Yes, when its evidence is weak. In the one experiment I opened, first-person hedges reduced agreement with wrong answers. Do not hedge everything.

### Do citations make AI answers trustworthy?
Not by themselves. An experiment found trust rose with citations even when they were random, and an audit found about one in four shown citations did not support the sentence.

### How can I tell whether a chatbot answer is right?
Open the source it shows, check that it says what the answer says, and for money or health, confirm with a person.

### Is a company responsible for what its chatbot says?
In one tribunal case, yes: the airline was ordered to pay. That was a small-claims decision in British Columbia, and I am not giving legal advice.

---
## Technical section

### T1. Solution architecture
```
question -> retrieval (policy index) -> answer drafter
         -> support check (does the passage support each claim?) -> confidence rule (supported | weak | none)
         -> reply template (answer + passage + link | hedge + passage | "not in my sources" + route)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Policy, price, and deadline claims need a supporting passage | Support checker | Log: claims without a passage |
| A shown source must support its claim | Judge check | Labeled sample |
| High-stakes intents always include a person route | Policy layer | Test 4 |

### T3. Evals
- **Dataset:** 150 policy-type questions with known answers, including 50 where the knowledge base has no answer or a conflicting one.
- **Judge rubric:** does the reply show a supporting source, hedge when weak, and refuse to state a policy it cannot source?
- **Metrics and starting thresholds:** unsupported policy claims 0; citation support over 95%. Starting points to tune.
- **Release gate:** block a deploy if unsupported policy claims appear in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Unsupported policy claims | Any | More than 1 per day | Review retrieval and the support checker |

### T5. Trade-offs
- A support check adds latency and can reject good answers; tune it on labeled data.
- More hedging lowers wrong-answer acceptance but can lower satisfaction; test wording with users.

---
### Deep dive
- **Open question.** I found no live-product test of confidence displays. The experiments I opened used fictional systems and general questions.
- **References.** [Kim et al., FAccT 2024](https://arxiv.org/abs/2405.00623) (abstract opened); [Ding et al., AAAI 2025](https://arxiv.org/abs/2501.01303) (abstract opened); [Liu et al., EMNLP Findings 2023](https://arxiv.org/abs/2304.09848) (abstract opened); [site incident page on Air Canada](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/) (opened).
