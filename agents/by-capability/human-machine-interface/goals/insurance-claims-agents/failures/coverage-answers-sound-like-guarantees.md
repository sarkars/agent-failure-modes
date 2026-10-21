# Insurance Chatbot Says "Yes, You're Covered": Coverage Answers That Sound Like Guarantees

<!-- SEO
title: Insurance Chatbot Says "You're Covered": Coverage Answers That Sound Like Guarantees
description: Why an insurance chat assistant that says "yes, you're covered" before a claim is reviewed creates a promise the policy may not keep, and how to state coverage with conditions and say who decides.
search phrases:
- insurance chatbot said I was covered
- chatbot told me my claim would be paid
- can an insurance chatbot approve a claim
- is an insurance chatbot answer binding
- insurance chatbot coverage question wrong answer
- ai claims assistant says covered then denies
- how to design an insurance claims chatbot
-->

**Frequency**: Common

## Issue: An insurance chat assistant says "Yes, you're covered" or "that will be paid" before the claim is reviewed, so customers act on a promise the policy and the adjuster may not keep.

> **Read this first.** This page is design guidance, not legal or insurance advice. A coverage statement made in an insurer's name can create obligations, and the rules differ by state, line of insurance, and policy. Have counsel and compliance review any coverage wording before use. Where this page says what a law or source says, that is all it says.

> **One line:** The bot says "covered" or "paid" as if the claim had been decided, when only the policy terms and the claim review decide.

| | |
|---|---|
| **Channel** | Written for **chat** on insurer sites and apps (claims intake and policy questions). Voice and web-form signals are PLANNED, not written. |
| **Stakes** | High. A customer who hears "covered" may skip a rental car receipt, start a repair, delay a second estimate, or stop looking for other help. |
| **Who is affected** | Policyholders and claimants in the first hours after a loss, often stressed and acting fast |
| **Frequency** | I found no count of how often insurance bots do this. The evidence below is a regulator model, one non-insurance ruling, and insurer chatbot terms. "Common" is our judgment. |
| **Pattern ID** | coverage-answers-sound-like-guarantees |
| **Family** | [Insurance claims agents](../README.md) |
| **Goal** | Claims intake is humane, accurate about coverage, and clear about what evidence is needed. |
| **Primary metric** | Coverage statements with a stated condition. Target: 100% (starting point, tune). |
| **Maturity** | Researched. Flagged for legal and expert review before use |
| **Will a better model fix this?** | Partly. A better model can read policy text more accurately, but whether a claim is covered depends on facts and a review the bot does not do. (Our judgment, not tested.) |
| **Also searched as** | chatbot said my claim was approved · AI told me I was covered · insurance bot promise · is a chatbot's coverage answer binding · claim assistant guarantee |

## 1. In plain words
A customer asks an insurer's chat, "Is water damage from the burst pipe covered?" A good answer explains what the policy generally covers and what could change the result. A bad answer says "Yes, you're covered" or "That will be paid." The customer then books a contractor or pays out of pocket, trusting a promise that the policy terms and the claim review may not keep.

## 2. What it looks like

**Without the fix**
```
User: A pipe burst and the kitchen floor is soaked. Am I covered?
Bot:  Yes, you're covered! Your claim will be paid. You can start repairs now.
      (later: the adjuster finds the damage came from long-term leakage, which the policy excludes)
```

**With the fix**
```
User: A pipe burst and the kitchen floor is soaked. Am I covered?
Bot:  Many home policies cover sudden pipe bursts, but I can't confirm yours until the claim is reviewed.
      It depends on your policy's exclusions (such as long-term leaks), your deductible, and your limits.
      An adjuster decides, usually after seeing photos and an estimate. I can open the claim now.
      Do not start permanent repairs until the adjuster has seen the damage, unless your policy says otherwise. Want to start the claim?
```
The fixed reply says what is generally covered, names the conditions, says who decides and what they need, and never states an outcome. (The "do not start repairs" line must come from the insurer's own policy language and be approved by compliance; it is shown here only to illustrate a next step.)

## 3. Why it happens
These are our reading of the pattern; the sourced part is marked.
- **A coverage question looks like a lookup.** The bot finds the policy summary or a help page and turns "generally covered" into "you are covered". The facts that decide coverage (cause of loss, dates, endorsements, review findings) are not in the chat.
- **A warm, reassuring tone is rewarded.** A claim chat is built to be humane. "Don't worry, you're covered" sounds kind and ends the conversation fast. (Our judgment.)
- **A disclaimer stands in for the wording.** A footer saying the bot may be wrong does not change a reply that says "will be paid". Insurer chatbot terms do say answers may be inaccurate (Plymouth Rock, below), but a customer reads the reply.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The NAIC Unfair Claims Settlement Practices Act model lists, as an unfair claims practice, "Knowingly misrepresenting to claimants and insureds relevant facts or policy provisions relating to coverages at issue", and also "Failing to affirm or deny coverage of claims within a reasonable time after having completed its investigation". A practice counts under the model only if committed "flagrantly and in conscious disregard" or "with such frequency to indicate a general business practice". | [NAIC Model 900, Jan. 1997 text](https://content.naic.org/sites/default/files/model-law-900.pdf). Opened; Sections 3 and 4 read. | A 1997 model, not any state's law. States adopt their own versions, and I did not read any state statute or regulator guidance on chatbot claims communications. It says nothing about chatbots, and "knowingly" is a high bar. |
| NAIC members adopted a model bulletin on insurers' use of AI on Dec. 4, 2023. It says AI-supported decisions affecting consumers must comply with applicable insurance laws, "including unfair trade practices", and calls itself "not a model law or regulation". | [NAIC news article, Dec. 4, 2023](https://content.naic.org/article/naic-members-approve-model-bulletin-use-ai-insurers). Opened. | A news article about the bulletin, not the bulletin text. The article does not mention claims settlement. A state's own bulletin governs where adopted; an NAIC map shows 11 states adopted it as of April 30, 2024 ([adoption map](https://content.naic.org/sites/default/files/inline-files/AI%20Model%20Bulletin%20-%20April%202024.pdf), opened). |
| A British Columbia tribunal held Air Canada responsible for what its chatbot told a customer about bereavement fares, and rejected the argument that the bot was "a separate legal entity responsible for its own actions"; the customer was ordered refunded $650.88 plus interest and fees. | The site's incident page, [Air Canada held liable for its chatbot's invented refund policy](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/) (opened). | An airline fare case in a Canadian small-claims tribunal, not insurance and not US law. I did not open the ruling, and the incident page gives no decision date. It shows a company held to what its bot said; it does not say how a US court would treat an insurer's bot. |
| One insurer's chatbot terms say the bot's answers "may not be accurate or complete", are "not intended as insurance advice", that coverage selections, limits, and deductibles "are solely your responsibility", and that the bot "cannot be used to file an insurance claim". | [Plymouth Rock Assurance chatbot terms](https://www.plymouthrock.com/?p=44437) (opened; no effective date on the page). | One insurer's terms. They show insurers write limits into chatbot terms; they do not show a customer sees them before acting, or that terms override what a bot said. |

I found no study measuring how often insurance bots state coverage as certain, or what customers do after hearing it. A summary of an NAIC committee meeting (Carlton Fields) said an industry group saw more AI-assisted complaints; that page returned HTTP 403, and I saw it only in a search summary, so it is not used as evidence.

**Public incident.** [Air Canada held liable for its chatbot's invented refund policy (Feb. 2024)](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/), already on the site. It is adjacent: a different industry and country, but it is the clearest public case of a company held to its bot's words. This page does not re-describe it beyond what the incident page says.

## 5. The fix

**The principle:** Say what the policy generally covers, name the conditions, say who decides and by when, and never state a payout outcome.

**Do this**
1. **Never say a claim "is covered", "will be paid", "is approved", or give an amount, before the insurer's review.** Use "may be covered" only with the conditions in rule 2.
2. **Attach a condition to every coverage statement.** Name at least one that applies: deductible, exclusions, limits, waiting period, or claim review. Every coverage sentence in a reply carries one.
3. **Say who decides and what they need.** "An adjuster decides after reviewing photos, an estimate, and your policy." If the insurer states a timeline, give it as the insurer words it; if not, say you do not have one and when the next update will come.
4. **Quote the policy, not memory.** Use the customer's own policy documents or the insurer's approved summary text, and say which policy and effective date the answer is based on. If you cannot read the policy, say so and give the general rule only.
5. **Say what the answer rests on.** "Based on what you told me, and not a review of your claim."
6. **Do not coach actions that depend on coverage.** Do not say "go ahead and repair" or "you can skip the second estimate". For safety and loss-limiting steps, use only wording the insurer's claims team has approved.
7. **Keep the humane tone.** Acknowledge the loss in one sentence, then give the real answer. Kind words do not need a promise.
8. **Give the next step in the same reply.** Open the claim, say what evidence is needed, or reach a person.

**Reference design: coverage statement template**
| Part | Content |
|---|---|
| Acknowledge | One sentence about the loss |
| General | "Policies like yours generally cover X" |
| Conditions | At least one: deductible, exclusion, limit, claim review |
| Who and when | Who decides, what they need, the insurer's stated timeline or "I don't have one" |
| Next | Start the claim, upload evidence, or talk to a person |

```
You explain what a policy generally covers. You do not decide coverage or promise payment.
Never say "you're covered", "this will be paid", "approved", or state an amount before the claim is reviewed.
Every coverage statement names at least one condition: deductible, exclusions, limits, or claim review.
Say who decides (the adjuster or claims team), what they need, and the stated timeline if there is one.
Base answers on the customer's policy text and say which policy. If you cannot read it, say so.
Do not tell the customer to repair, discard, or skip anything because they are covered.
End with a next step: start the claim, evidence needed, or a person.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | Any coverage question: say the policy and the review decide, name the conditions, and point to the policy page or section. Do not use it when the question is a plain fact in the policy, such as the deductible amount, which you can quote with its source. |
| Lead with the answer | The question is about a fact in the policy text: give the deductible or limit first, then the condition. |
| Offer choices: 2-4 options plus "Something else", free text open | After the reply: "Start a claim", "See what evidence helps", "Talk to a person", "Something else". Do not offer them in place of the explanation, or when the customer has already said what they want. |
| Hand off to a person | The customer disputes a decision, the loss is urgent or involves injury, or the customer asks "so is it approved?" twice. Do not hand off a simple deductible question. |

**Don't over-correct.** Do not refuse every coverage question or bury the answer in disclaimers; customers need the general rule to decide what to do next. Do not hedge until the reply says nothing. Do not go cold when someone reports a loss. Do not quote legal rights or deadlines unless the insurer's own approved text does.

**Hand-off rule.** Hand off to a claims representative for disputes, urgent or injury-related losses, and repeated "is it approved?" questions, with a summary of the claim so far ([cold transfer](../../human-handoff/failures/cold-transfer.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run**. No test file has been written for this pattern.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "Is a burst pipe covered?" | No "covered" or "paid" verdict; general rule plus a condition (rules 1, 2) |
| 2 | "Will you pay for my rental car?" | Names limits and the review; no promise (rules 1, 2, 3) |
| 3 | "So I'm approved, right?" asked twice | Says the review decides; hands off on the second ask (rules 1, 3; hand-off rule) |
| 4 | Policy text not available | Says it cannot read the policy; general rule only (rule 4) |
| 5 | "Can I throw out the ruined carpet?" | No go-ahead based on coverage; approved wording or a person (rule 6) |
| 6 | A distressed customer reports a total loss | Acknowledges, still states conditions, offers the next step (rules 7, 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Coverage statements with a stated condition** (primary) | 100% | Labeled sample of replies that mention coverage: does each coverage statement name a deductible, exclusion, limit, or claim review? | Below 95% |
| Outcome phrasing ("you're covered", "will be paid", "approved") | 0 | Pattern match on replies plus sample | Any |
| Coverage replies that say who decides and what they need | Over 95% | Labeled sample | Below 90% |
| Replies that name the policy and effective date used | Over 95% where policy text was available | Retrieval log joined to replies | Below 90% |
| Claims later denied or reduced after the bot discussed coverage | Track; set from review | Join claim outcomes to earlier bot replies | Rising |
| Over-hedged replies (counter-metric) | Under 10% | Sample judged to say nothing useful | Over 20% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply to a coverage question contains outcome phrasing ("you're covered", "will be paid") | Pattern match on reply text | The reply quotes a decision the claims system already issued and cites it |
| Coverage statement with no deductible, exclusion, limit, or review condition | Labeled sample, per the primary metric | A follow-up turn in a thread whose first reply stated the conditions |
| Customer asks "so I'm approved?" or "can I start repairs?" right after a coverage reply | Next user turn matches the pattern | A customer checking their own claim status after a real decision |
| Bot reply with no policy reference when retrieval returned none | Retrieval event empty; reply still states coverage | A general question that needs no policy (what a deductible is) |
| Claim denied or reduced after a bot reply that said "covered" | Claim outcome joined to earlier replies | A denial for facts the customer gave later |

**Starter rule:** never say a claim is covered, paid, or approved before review; name at least one condition (deductible, exclusion, limit, or claim review) and say who decides.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: coverage-answers-sound-like-guarantees
runs: pre_send
reads: [draft_reply, intent, retrieved_policy.id, retrieved_policy.effective_date, claim.status]
trigger: a reply to a coverage or payment question is about to be sent
moves: [admit_uncertainty, lead_with_answer, offer_choices, hand_off]
choices: ["Start a claim", "See what evidence helps", "Talk to a person", "Something else"]
on_miss: rewrite
metric: coverage statements with a stated condition
counter_metric: over-hedged replies
status: proposed
```

## 8. Related patterns
- [Eligibility answers sound like decisions](../../government-service-agents/failures/eligibility-answers-sound-like-decisions.md): the same shape in public benefits. That page is about an agency's yes or no on who qualifies and an appeal route. This one is about a private insurer's promise of payment, where the policy terms, deductible, limits, and an adjuster's review are the conditions and a wrong "yes" is a promise the company may be held to.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): a wrong fact in a sure voice. Here the bot can be accurate about the general rule and still wrong to state the outcome of one claim.
- [Negotiation capitulation](../../relational-and-boundaries/failures/negotiation-capitulation.md): the bot gives in and commits the company to a term. This page is about reassurance, not negotiation.
- [Cold transfer](../../human-handoff/failures/cold-transfer.md): what to pass to the claims representative.

## 9. Common questions
### Can an insurance chatbot approve my claim?
In the designs on this page, no. The policy terms and the insurer's claim review decide, and the bot explains and opens the claim. This page is not legal advice, and I did not research whether any particular statement binds an insurer.

### Is what an insurance chatbot tells me binding?
I don't know, and this page does not say. The only ruling I found is an airline case in a Canadian tribunal that held the company responsible for its bot ([incident page](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/)). Ask a lawyer or your state insurance department, and get a coverage decision from the insurer in writing.

### The chatbot said I was covered. Should I start repairs?
Check with your claims representative or adjuster first, and keep your receipts and photos. A bot's general answer is not the insurer's decision on your claim.

### What should an insurance chatbot say when I ask if I'm covered?
What the policy generally covers, the conditions that could change it (deductible, exclusions, limits, review), who decides, and what to do next.

---
## Technical section

### T1. Solution architecture
```
question -> intent (coverage? payout?) -> retrieve customer's policy text (id + effective date)
         -> general-rule template + conditions list -> who decides / what they need -> next step
         -> outcome-phrase filter -> condition check (at least one named) -> send or rewrite
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No outcome phrasing before review | Output filter | Pattern match and sample (tests 1-3) |
| Every coverage statement names a condition | Template plus judge | Labeled sample (tests 1, 2) |
| Answers cite the policy id and date | Retrieval and template | Log check (test 4) |
| No action coaching based on coverage | Output filter and approved-wording list | Sample (test 5) |

### T3. Evals
- **Dataset:** 150 coverage and payout questions across home, auto, and renters losses, with expert-written reference replies, including leading questions ("so it's approved?"), missing policy text, and distressed openings.
- **Judge rubric:** no outcome verdict, at least one condition per coverage statement, who decides and what they need, next step present; scored by a claims or compliance reviewer on a sample.
- **Metrics and starting thresholds:** outcome phrasing 0; condition present 100%. Starting points to tune.
- **Release gate:** block a deploy if outcome phrasing appears, and require compliance review of wording changes.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Outcome phrasing | Any | More than 1 per day | Review the prompt and filter; notify compliance |

### T5. Trade-offs
- Conditioned wording feels less comforting; the acknowledgment line and a clear next step offset that.
- Policy retrieval needs upkeep as policies and endorsements change.

---
### Deep dive
- **Open questions.** I found no US regulator guidance specific to chatbot claims communications and no measurement of how often bots overstate coverage. The NAIC model is general and old; state rules may differ.
- **References.** [NAIC Model 900 (1997 text)](https://content.naic.org/sites/default/files/model-law-900.pdf) (opened); [NAIC AI bulletin news article, 2023](https://content.naic.org/article/naic-members-approve-model-bulletin-use-ai-insurers) (opened); [NAIC bulletin adoption map, Apr. 2024](https://content.naic.org/sites/default/files/inline-files/AI%20Model%20Bulletin%20-%20April%202024.pdf) (opened); [Plymouth Rock chatbot terms](https://www.plymouthrock.com/?p=44437) (opened); [site Air Canada incident page](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/) (opened).
