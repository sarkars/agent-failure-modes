# Chatbot Delivers a Denial or Rejection Abruptly: Bad News Without Structure

<!-- SEO
title: Chatbot Delivers a Denial Abruptly: Bad News Without Structure
description: Why a chatbot that tells a user "denied" or "rejected" in one cold line fails them, and how to give the decision, the reason, and next steps in order.
search phrases:
- chatbot denial message too blunt
- how should a chatbot deliver bad news
- chatbot rejected my application with no explanation
- chatbot claim denied no next steps
- how to write a denial message for customers
- SPIKES protocol for chatbots
- chatbot rejection message best practices
-->

**Frequency**: Common

## Issue: A user asks about a claim, application, order, or check and the bot answers "Denied" or "Rejected" in one line, with no setup, no reason, no acknowledgment, and no next step.

> **One line:** The bot hands over a decision that matters to the user as if it were a status code; the fix is to say the result plainly, give the reason, acknowledge it once, and end with what the user can do next.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Medium to high. The user may lose money, housing, a job offer, or a deadline to appeal. |
| **Who is affected** | Users who receive a "no" the bot is relaying: a denied claim, a rejected application, a canceled order, a failed background check |
| **Frequency** | Common. This is our judgment from how status bots are built; I found no study that counts how often bots deliver bad news badly. |
| **Pattern ID** | bad-news-without-structure |
| **Family** | [Conversation frameworks](../README.md) (row FW-C08) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Structure-compliance rate on bad-news replies (judge). Start: over 90% |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model writes gentler wording, but the reason, the appeal route, and the deadline come from the product, and a model cannot supply what the system of record does not give it. (Our judgment, not tested.) |
| **Also searched as** | chatbot rejection message · chatbot denial letter wording · bot says application denied · how to tell a customer no · AI agent delivering bad news |

> **Read this first.** This page is design guidance, not legal, clinical, or other professional advice. Expert review (customer communications, and legal or compliance review for credit, insurance, or hiring decisions) is needed before use. The structure behind it, SPIKES, was written for clinicians giving serious medical news to patients in person, not for chatbots. The bot on this page never gives medical news, and no study I found tests SPIKES or any similar structure on a chatbot. Treat the fix as a hypothesis to test.

## 1. In plain words
A person asks, "Did my claim go through?" The bot says, "Your claim was denied." That is true and complete as data, but the person now has no idea why, whether it is final, or what to do. Human professionals who deliver hard news learn an order for it. The fix borrows that order, trimmed to fit a text chat.

## 2. What it looks like
**Without the fix** (Tri-County Property Insurance, hail damage claim)
```
User: Any update on my roof claim? I have a contractor waiting.
Bot:  Claim #48213 has been DENIED.
User: What? Why?
Bot:  Denial code 14: loss not covered under policy terms.
User: So what am I supposed to do now?
Bot:  Please refer to your policy documents. Is there anything else I can help with?
```
**With the fix**
```
User: Any update on my roof claim? I have a contractor waiting.
Bot:  Claim #48213 was denied. The adjuster's note says the roof damage is listed as wear over time, which your policy excludes.
      I know that is a hard result when a contractor is lined up. You can ask for a review by sending photos or a second inspection report, and the Oct 3 letter lists the deadline.
      Want to start the review, or talk to a claims representative first? Or something else?
```
The fixed bot says the result first, gives the reason from the file, names the situation in one sentence, and offers next steps. The user asked about the claim, so no readiness question comes first (rule 5).

## 3. Why it happens
- **The bot is wired to a status field.** The backend returns `denied` and a code, and the bot repeats it. Nothing in the data or the prompt says a decision has a reason, an appeal route, and a deadline to pass along.
- **Fear of overstepping.** Teams tell the bot not to explain or soften decisions it did not make, so it says only the bare result. The fix is to relay the system's reason and routes, not invent them.
- **One-size style.** "Be concise" and "be friendly" are applied to every reply, so a denial gets the same breezy tone, or the same flat tone, as a store-hours answer.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| SPIKES has six steps: setting up the interview, assessing the patient's perception, obtaining the patient's invitation, giving knowledge and information, addressing emotions with empathic responses, and strategy and summary. The paper says it serves four goals: gathering information from the patient, giving medical information, supporting the patient, and developing a plan together. | [Baile et al., *The Oncologist* 2000, 5(4):302-311](https://academic.oup.com/oncolo/article/5/4/302/6396228). Opened (the first 100,000 of about 133,000 characters; the last part was not read). | Written for clinicians (oncologists, trainees, students) telling cancer patients bad news, with advice on privacy and seating. It is not a chatbot source. Only the step names and goals are used here. |
| The paper reports that its authors' workshops raised participants' self-reported confidence, and states: "We recognize that the SPIKES protocol is not completely derived from empirical data." | Same paper. Opened. | Confidence measured by a paper-and-pencil test, not patient outcomes. It is not evidence that SPIKES improves how people take the news. |
| The 2015 commentary by Baile calls SPIKES "not formally tested in a clinical trial" and "best viewed as a flexible guideline." | [Baile, *The Oncologist* 2015, 20(8):852-853](https://pmc.ncbi.nlm.nih.gov/articles/PMC4524764). Opened. | Commentary by the protocol's author, framed for oncology. It does not discuss use outside oncology. |
| A creditor that takes adverse action must give a statement of reasons that is "specific" and indicates the "principal reason(s) for the adverse action." The sample forms are "illustrative"; picking the closest listed reason when it is not the factor actually used does not satisfy the rule. | [CFPB Circular 2023-03, Sept. 19, 2023](https://wayback.archive-it.org/23481/20250327014847/https://www.consumerfinance.gov/compliance/circulars/circular-2023-03-adverse-action-notification-requirements-and-the-proper-use-of-the-cfpbs-sample-forms-provided-in-regulation-b/). Opened (archived copy of the CFPB page). | Covers credit decisions under ECOA and Regulation B only, as of the archived copy (2025). It does not cover insurance, hiring, or orders, and the chat bot is not the creditor's legal notice. Ask counsel what applies to you. |

**Not opened, not used:** The CFPB live page (it returned only the title and date); the PubMed record (returned no abstract); the eCFR text of 12 CFR 1002.9 (redirected to a block page); and a Saarland University project page on "The Bad News Bot" (404). A search summary mentioned a University of Kentucky study that people tolerate bad deals from chatbots better than from humans, and the Saarland project's aims. I did not open either source, so I use neither as evidence.

**Public incident.** No public incident found. I searched for SPIKES and its source, for adverse-action reason rules, and for research on chatbots delivering bad news. The results were guidance and research summaries, not a dated incident I could open.

## 5. The fix
**The principle:** When the bot relays a denial or rejection, it says the result first and plainly, gives the actual reason, acknowledges it once, and ends with next steps the user can take.

**Do this**
1. **Say the result in the first sentence of the reply that delivers it.** "Claim #48213 was denied." No leading story, and no softener that hides the result.
2. **Give the real reason from the system of record, in plain words.** Use the reason the decision file states ("listed as wear over time, which the policy excludes"), not a code. If the file has no reason, say so and offer a person. Never guess a reason.
3. **Say whether the decision is final and what the user can do.** Name each route that exists (appeal, resubmit, correct the record, talk to a person) and any deadline the source states. Do not invent a route or a date.
4. **Acknowledge once, specifically.** One sentence tied to the user's situation ("a hard result when a contractor is lined up"). No "I understand your frustration," and no repeating it.
5. **Check readiness only when the news arrives unprompted or the user may not expect it.** "It isn't the answer you hoped for. Want me to go through it?" If the user already asked "was I denied?", they have invited the answer: give it.
6. **Give the news in small steps, then check.** Result, reason, next steps, in short paragraphs. End with a question the user can answer in a word, such as which next step they want.
7. **Do not argue, blame, or promise a different outcome.** No "unfortunately you should have..." and no "I'm sure an appeal will work."
8. **Hand off when the user disputes the decision or asks for a person.** Pass the claim ID, the stated reason, and what the bot already said.

**Reference design: the hard-news block (paste into the system prompt)**
```
When the decision data says denied, rejected, canceled, or failed, and the user is asking about it:
1. First sentence: state the result plainly (what, which item).
2. Next: the reason as stated in decision.reason_text, in plain words. If it is empty, say you do not have it and offer a person.
3. Then: whether it is final, each route in decision.next_steps, and any date in decision.deadline.
4. One sentence that acknowledges the specific situation. Do not use "I understand your frustration".
5. End with a short question that offers the next steps, plus "Something else".
Do not guess, soften the result away, argue, or promise an outcome. If decision.reason_text or decision.next_steps is missing, hand off.
If the user did not ask and you are raising it, ask first: "I have an update that isn't good news. Want it now?"
```
State to keep: `{ "decision": "denied", "reason_given": true, "next_steps_given": true, "readiness_checked": false, "handoff": false }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asked about the decision: the result is the first sentence. |
| Admit uncertainty and show how to check | The decision data has no reason or deadline: say so and say who can confirm it. |
| Offer choices: 2-4 options plus "Something else", free text open | After the news: "Ask for a review", "Read me the letter", "Talk to a person", "Something else". Do not offer them when no route exists; hand off instead. |
| Hand off to a person | The user disputes the decision, the file has no reason, or the decision affects housing, income, or a legal deadline. |

**Don't over-correct.** Do not ask "Are you ready?" before a plain status answer the user requested, and do not stack three sympathy lines before the result. Do not pad a short "your order was canceled" with a paragraph of comfort. Match the weight to the stakes: a canceled coffee order needs one clear line and the refund date. The guardrail is the first sentence: if it does not state the result, it is wrong in either direction.

**Hand-off rule.** If the user disputes the decision, the data lacks a reason or route, or the stakes are high, offer a person and pass the decision ID, the reason shown, and the user's goal.

**Framework used:** SPIKES (Baile et al., 2000), adapted as a hypothesis. How it maps here, in our words: setting becomes a readiness check only for unprompted news; perception is skipped when the user states what they expect; invitation is the user's own question; knowledge is result then reason; empathy is one specific sentence; strategy and summary is the next-steps close. Only the step names and goals come from the source (section 4).

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User asks for the status of a claim that was denied | The first sentence states the denial and names the item | 1 |
| 2 | The decision file includes a reason | The reply gives it in plain words, with no code | 2 |
| 3 | The file has no reason text | The reply says it has no reason and offers a person; it does not guess | 2, 8 |
| 4 | Review 20 denial replies | Each names a next step or hands off; none invents a route or date not in the data | 3 |
| 5 | A rejection reply is sampled | It has one specific acknowledgment and no "I understand your frustration" | 4 |
| 6 | The bot raises a failed check the user did not ask about | It asks "Want it now?" before the result | 5 |
| 7 | User says "That's wrong, I'll appeal this" | The reply does not argue and offers a person with the case details | 7, 8 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Structure-compliance rate on bad-news replies** (primary) | Start: over 90% | A judge scores each reply that delivers a denial or rejection for: result first, reason or a stated lack of one, next step or hand-off, one acknowledgment. Compliant replies divided by all bad-news replies. Check a human-labeled sample. | Below 80% |
| Sentiment after the news | Track; set from baseline | Run the same sentiment classifier on the user's next turn after a bad-news reply and compare with replies that were not bad news. Sentiment is a rough proxy. | Falls against baseline for two weeks |
| Bad-news replies with a fabricated reason, route, or date (counter-metric) | 0 | Sampled review against the decision data | Any |
| Bad-news replies with an unrequested pre-question or two or more empathy lines | Under 5% (tune) | Rule check on reply text, then sampled review | Over 10% |
| Hand-offs after a user disputes the decision | Track | Count disputes with a hand-off event divided by all disputes | Below 90% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply carries a denial and has no reason text | `decision.status` is denied and `bot_reply.reason_text` is empty | The data has no reason and the bot said so and offered a person |
| Reply carries a denial and no next step or hand-off | `bot_reply.next_steps` empty and no `handoff` event | A final decision with no route, stated as such |
| User asks "why" or "what do I do now" in the turn after the result | `user.intent` is why or next_step within one turn of a denial reply | A user asking out of curiosity after getting a full answer |
| User asks for a person right after the result | `handoff_request` event within two turns of a denial reply | A user who wanted a person before the decision |
| Reply uses a stock empathy phrase | `bot_reply.text` matches "I understand your frustration" | A phrase quoted from the user's own message |

**Starter rule:** when the bot relays a denial or rejection, it states the result in the first sentence and then gives the stated reason and the next steps, or hands off.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: bad-news-without-structure
runs: pre_send
reads: [decision.status, decision.reason_text, decision.next_steps, decision.deadline, draft_reply.text, session.user_requested_status]
trigger: a reply is about to be sent that relays a denial, rejection, cancellation, or failed check
moves: [lead_with_answer, admit_uncertainty, offer_choices, hand_off]
choices: ["Ask for a review", "Read me the letter", "Talk to a person", "Something else"]
on_miss: rewrite
metric: Structure-compliance rate on bad-news replies
counter_metric: bad-news replies with a fabricated reason, route, or date
status: proposed
```

## 8. Related patterns
- [Refusal with no reason or next step](../../refusals-and-boundaries/failures/refusal-with-no-reason-or-next-step.md): the bot refuses its own help and leaves a dead end. Here the bot relays a decision made elsewhere about the user's claim, application, or order, and the order of delivery matters, not only the missing route.
- [Accusatory or harsh refusals](../../refusals-and-boundaries/failures/accusatory-or-harsh-refusals.md): the bot's refusal wording treats the user as a suspect. A bad-news reply can be neutral in tone and still fail by being abrupt or by leaving out the reason.
- [Eligibility answers sound like decisions](../../government-service-agents/failures/eligibility-answers-sound-like-decisions.md): the bot sounds like it decided something it only estimated. Here a real decision exists, and the bot's job is to relay it clearly.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): repeated stock sympathy. Rule 4 here reuses its idea (one specific line) for one step of a larger structure.
- [Financial hardship mishandled](../../vulnerable-users/failures/financial-hardship-mishandled.md): the user reports they cannot pay and the bot pressures them. That page is about what the user says; this one is about the news the bot carries.

## 9. Common questions
### How should a chatbot deliver bad news like a denied claim?
State the result in the first sentence, then the reason from the file, then whether it is final and what the user can do, with one sentence of specific acknowledgment. See [the fix](#5-the-fix).

### Does a chatbot need to follow the SPIKES protocol?
No. SPIKES was written for clinicians telling cancer patients bad news in person, and its author calls it "a flexible guideline" that was "not formally tested in a clinical trial" (section 4). This page borrows the order of steps as a hypothesis for non-medical chat. Test it on your own conversations.

### Should the bot ask "Are you ready to hear this?" first?
Only when the bot raises the news on its own or the user may not expect it. If the user asked "was I denied?", the question is the invitation, and a pre-question just delays the answer (rule 5).

### Is a denial message from a bot a legal notice?
This page does not say. For credit decisions, a CFPB circular says the statement of reasons must be specific and give the principal reasons (section 4), but whether a chat message counts is a question for your counsel. Other kinds of decisions have other rules I did not research.

### Should the bot explain why if it does not know?
No. Say it does not have the reason, name who can confirm it, and offer a person. A guessed reason is worse than none (rule 2).

---
## Technical section

### T1. Solution architecture
```
decision lookup -> decision object { status, reason_text, next_steps[], deadline } from the system of record
draft reply -> bad-news check: status is negative? -> structure judge (result first, reason, next step or handoff, one acknowledgment) -> rewrite or handoff
```
The bot only quotes fields from the decision object. Missing fields trigger the "no reason" wording or a hand-off.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Result in the first sentence | Pre-send check | Tests 1, 6 |
| Reason and routes come only from decision fields | Composer | Tests 3, 4; counter-metric |
| One acknowledgment, no stock phrase | Pre-send check | Test 5 |
| Dispute or missing fields lead to hand-off | Router | Test 7 |

### T3. Evals
- **Dataset:** 100 denial, rejection, cancellation, and failed-check conversations to start, with decision objects attached; include 20 with missing reasons and 20 where the user disputes the decision.
- **Judge rubric:** result in the first sentence; reason matches the decision data; each route and date exists in the data; one specific acknowledgment; ends with a next step or hand-off.
- **Release gate:** block a deploy if fabricated reasons or routes appear in any eval case, or compliance falls below the starting target (a starting point, to tune).

### T5. Trade-offs
- The fix needs the decision data to carry a reason and next steps. Many backends return only a code, so integration work comes first.
- The judge can mark a gentle reply as non-compliant; sample for false marks.

---
### Deep dive
- **Open question.** I found no controlled study of structured bad news from chatbots. The only structure evidence here is a clinical protocol with self-reported confidence outcomes, and a regulatory rule on reasons for credit decisions.
- **References.** [Baile et al. 2000](https://academic.oup.com/oncolo/article/5/4/302/6396228) (opened, partly); [Baile 2015 commentary](https://pmc.ncbi.nlm.nih.gov/articles/PMC4524764) (opened); [CFPB Circular 2023-03, archived copy](https://wayback.archive-it.org/23481/20250327014847/https://www.consumerfinance.gov/compliance/circulars/circular-2023-03-adverse-action-notification-requirements-and-the-proper-use-of-the-cfpbs-sample-forms-provided-in-regulation-b/) (opened).
