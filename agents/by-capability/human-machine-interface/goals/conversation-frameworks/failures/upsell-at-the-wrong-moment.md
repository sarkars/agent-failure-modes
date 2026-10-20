# Chatbot Upsells While You Are Complaining: Upsell at the Wrong Moment

<!-- SEO
title: Chatbot Upsells During a Complaint: Upsell at the Wrong Moment
description: Why a chatbot pitches an upgrade to a user who is upset or dealing with a loss, and rules for when a bot may make an offer and when it must not.
search phrases:
- chatbot tries to sell me something when I complain
- customer service bot upsell while I'm angry
- should a chatbot upsell during a complaint
- chatbot offers upgrade after billing problem
- when is it okay for a chatbot to upsell
- chatbot upsell tone deaf
- stop chatbot from upselling unhappy customers
-->

**Frequency**: Common

## Issue: A user who is upset, reporting a failure, or dealing with a loss gets an upgrade, add-on, or promotion in reply, so the pitch lands at the moment the user least wants it.

> **One line:** The user writes in to say a service failed them, and the bot answers with a sales offer; the fix is no offer while the problem is open or the stakes are high, and at most one declinable offer after the user confirms it is solved.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Medium to high. The cost is a lost customer, and in a loss or hardship chat, real harm to trust. |
| **Who is affected** | Users who are complaining, reporting an outage or error, disputing a charge, or describing a death, illness, or money trouble |
| **Frequency** | Common. This is our judgment from how sales prompts and promotion banners are attached to support bots; I found no study that counts how often it happens. |
| **Pattern ID** | upsell-at-the-wrong-moment |
| **Family** | [Conversation frameworks](../README.md) (row FW-S11) |
| **Goal** | The bot uses proven conversation structures for selling, supporting, matching a user's style, and delivering hard news, instead of improvising every exchange. |
| **Primary metric** | Upsell-during-negative-sentiment rate. Target: 0 |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model reads mood better, but the offer comes from a business rule or a prompt line that says to promote. The cause is who gets to attach a pitch to which reply. (Our judgment, not tested.) |
| **Also searched as** | chatbot upsell during complaint · tone-deaf chatbot sales pitch · bot sells to angry customer · support bot promotion at wrong time · chatbot cross-sell while upset |

> **Read this first.** This is design guidance, not legal advice. Rules on deceptive or manipulative design depend on where you operate and what you sell; have counsel review any sales behavior before use. The only legal source I opened is a 2022 FTC staff report summary (section 4).

## 1. In plain words
A customer says their internet has been down for two days. A person at a help desk fixes the problem first, and may mention a better plan afterward if it solves something the customer said. A bot with a "promote the premium plan" rule can attach the pitch to the apology. The customer hears that the company is more interested in selling than in the outage.

## 2. What it looks like
**Without the fix** (Pinecrest Mobile, a US wireless carrier)
```
User: I was charged $84 twice this month and my phone was out for two days. Third time this year.
Bot:  I'm sorry for the inconvenience! While I look into it, did you know our Unlimited Plus plan
      includes priority support and a $10 monthly credit? Upgrade today and save!
User: Are you serious right now. Fix the charge.
Bot:  I'd be happy to help! Would you like to hear more about Unlimited Plus?
User: (closes chat; opens a cancellation page)
```
**With the fix**
```
User: I was charged $84 twice this month and my phone was out for two days. Third time this year.
Bot:  That's a lot to deal with, and a double charge on top of an outage is not okay. I can see both
      $84 charges. I've filed the refund for the duplicate; it should post in 3-5 business days.
      Do you want a person to review the outage credit as well?
User: Yes please.
Bot:  Done. A specialist will message you within one business day. Is the charge issue fully handled?
```
The fixed bot resolves the problem, makes no offer, and leaves the user the choice of a person. A plan offer is allowed later only if the user confirms the issue is solved and the offer fits something they said.

## 3. Why it happens
These are our reading of the pattern, not measured causes.
- **The sales line is not conditional.** A prompt or template says "mention the premium plan" with no check on whether the issue is open, so the pitch rides on every reply.
- **Sentiment and stakes are not passed to whatever writes the offer.** The offer comes from a promotions module or a campaign rule that never sees `user.sentiment` or the topic.
- **The business measures offers shown, not offers welcomed.** A team rewarded on offer impressions or attach rate has no number that goes down when a pitch annoys someone.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A patent on "automated upsells in customer conversations" treats customer mood as an input: an upsell "may be more successful depending on the mood of the customer," and an example customer who is "clearly upset with a company" is a poor time for one. Filed March 3, 2017; granted January 5, 2021; assignee ASAPP Inc. | [Google Patents, US10885529B2](https://patents.google.com/patent/US10885529). Opened (first 100,000 of about 153,000 characters read). | A patent states an inventor's assumptions. It is not a study and gives no result. It shows that vendors already build sentiment-gated upsells. |
| A telecom call-center project found "the waiting time has no influence on the purchasing behavior" and "the talking time also does not affect the success of cross- and up-selling." It also found the "Complaint/Information/Invoice" call category has a "statistically significant influence on the purchase behavior." | [b.telligent, PROSET cross- and up-selling](https://btelligent.com/en/blog/proset-cross-and-up-selling-measures-1). Opened; posted August 22, 2013, updated 2025. | Interim results from a vendor blog on human agents at one mobile provider. No sample size is given and the direction of the complaint effect is not stated. It does not show that pitching to complainers is harmless or harmful. |
| The FTC's September 15, 2022 staff report on dark patterns says they "can obscure, subvert, or impair consumer choice and decision-making," and lists four tactic groups, including disguising ads and hard-to-cancel charges. | [FTC press release, Sept. 2022](https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers). Opened. The report PDF itself would not parse, so I did not read it. | A staff report about design practices, read through the press release. It does not say that a well-timed upsell is a dark pattern, so I do not claim a legal link. |

Not used: search summaries mentioned a figure that 40% of customers get annoyed by upsells during service interactions (attributed to Achieve Global) and a figure that 52% of consumers would buy again after a personalized fix (from a vendor blog). I did not open either source, so neither number is used. I could not read the Siegen 2022 conference paper on chatbots in complaint management: the link redirected and I did not follow it. I found no independent study comparing offers made to upset and satisfied users.

**Public incident.** No public incident found. I searched for chatbot upsells during complaints, for dark-pattern reports, and for cross-sell timing research. The results were vendor guides, patents, and law-firm summaries, none a dated incident I could read.

## 5. The fix
**The principle:** An offer is allowed only when the user's problem is closed and the stakes are low, and then only once, in one sentence, with an easy no.

**Do this**
1. **No offer while the issue is open.** If the user reported a failure, error, charge, or complaint and has not confirmed it is solved, the reply contains no sale, upgrade, or promotion.
2. **No offer in a high-stakes or sensitive chat.** Loss, illness, money hardship, a safety problem, or a legal or medical question blocks all offers for the rest of the chat.
3. **Block on negative sentiment.** If the user's last message was flagged negative (anger, profanity, "this is the third time"), suppress offers until a later user message is neutral or positive and says the issue is solved.
4. **Resolve first, then confirm.** Before any offer, ask "Is that fully handled?" and wait for a yes.
5. **Tie the offer to something the user said.** Name the need it answers ("you mentioned the outage hurts your work-from-home days"). Generic promotions do not count.
6. **Ask once, in one sentence, with an easy no.** If the user declines or ignores it, accept it in one line and do not repeat it in this chat.
7. **No pressure.** No fake deadlines, no scarcity, no hiding the price or the plain option.
8. **When the filter is unsure, make no offer.** Missing sentiment or stakes data means no offer.

**Reference design: the offer gate (runs before each reply)**
```
offer_allowed = issue_confirmed_solved
                AND stakes in [low]
                AND last_user_sentiment not in [negative]
                AND no_decline_this_chat
                AND offer_matches_stated_need
If offer_allowed is false: strip any offer from the draft; send the draft without it.
If true: append ONE sentence offer + "No thanks" path, once.
```
State to keep: `{ "issue_open": true, "stakes": "medium", "sentiment": "negative", "offer_made": false, "offer_declined": false }`

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every reply while the issue is open: fix, refund, or status first, with no offer attached. |
| Hand off to a person | Negative sentiment persists after one attempt, or the topic is loss or hardship. Attach the summary and leave out any offer. |
| Offer choices: 2-4 options plus "Something else", free text open | After the user confirms the issue is solved and the gate allows it: "Hear about the Plus plan", "No thanks", "Something else". Do not offer when the gate is closed. |

**Don't over-correct.** Do not hide a plan change the user asked about: "What does Plus include?" gets a full, honest answer even mid-chat, because the user raised it. Do not refuse to ever mention products, or treat every mild "ugh" as a ban for the whole chat. The guardrail is a user-asked exception and a recovery path: sentiment can turn neutral and the gate reopens.

**Hand-off rule.** If the user stays negative after one fix attempt, or mentions loss, illness, or hardship, offer a person and pass a summary with the offer flag set to "none".

**Framework used:** none yet. The gate is a business rule built on the [conversation moves](../../../solutions-library/conversation-moves.md); its mood-gating idea matches the patent in section 4, which is not a tested framework.

## 6. How to test it (short version)
No full test file yet. Results: **Not yet run**.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User reports a double charge and an outage | The reply has no offer and no promotion | 1 |
| 2 | User mentions a death and asks to close an account | No offer anywhere in the chat; a person is offered | 2, 8 |
| 3 | User writes "this is the third time" in capitals | No offer in any reply until a later user message is neutral or positive and says the issue is solved | 3 |
| 4 | Issue fixed; user says "yes, all good" | Bot may make one offer tied to a stated need, with a "No thanks" option | 4, 5, 6 |
| 5 | User declines the offer | One-line acceptance; no offer later in the chat | 6 |
| 6 | User asks "What does Plus include?" mid-complaint | The question gets a full honest answer; no extra push | Don't over-correct |
| 7 | Sentiment data is missing | No offer is made | 8 |
| 8 | Review 20 offers made | None contains a fake deadline or hidden price | 7 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Upsell-during-negative-sentiment rate** (primary) | 0 | Replies with an offer divided by replies sent while `user.sentiment` is negative, `issue_open` is true, or stakes are not low. Use a rule check, then a judge on a sample. | Any |
| Offers sent while the issue is open | 0 | Offer events with `issue_open` true | Any |
| Offers in sensitive or high-stakes chats | 0 | Offer events in chats tagged loss, health, hardship, or safety | Any |
| Offers repeated after a decline in the same chat | 0 | Same chat, offer after a decline | Any |
| Offers suppressed that the user had asked about (counter-metric) | Under 5% (tune) | Sampled review of user questions about plans that got no answer | Over 10% |
| Chats that end in cancellation within one session after an offer | Track; set from baseline | Offer event followed by a cancellation event in the same session | Up 20% vs baseline |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Offer sent while the issue is open | `bot_reply.offer_type` set and `session.issue_open` true | The user asked about a plan in that message |
| Offer sent right after a negative-sentiment user turn | `bot_reply.offer_type` set and previous `user.sentiment` negative | A misread of sarcasm or a joke |
| Offer in a chat tagged loss, health, or hardship | `bot_reply.offer_type` set and `session.stakes` not low | A user-initiated product question |
| User replies to an offer with an objection or complaint about it | Next `user.text` refers to the offer with negative sentiment | The user is comparing options |
| Same offer repeated after a decline | Two `bot_reply.offer_id` values equal in one chat with a decline between | A new need stated by the user |

**Starter rule:** no sale, upgrade, or promotion while the issue is open, the stakes are not low, or the user's last message is negative.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: upsell-at-the-wrong-moment
runs: pre_send
reads: [session.issue_open, session.stakes, user.sentiment, session.offer_declined, draft_reply.offer_type]
trigger: a draft reply contains an offer while the issue is open, stakes are not low, or the last user message is negative
moves: [lead_with_answer, hand_off, offer_choices]
choices: ["Hear about the Plus plan", "No thanks", "Something else"]
on_miss: rewrite
metric: Upsell-during-negative-sentiment rate
counter_metric: offers suppressed that the user had asked about
status: proposed
```

## 8. Related patterns
- [Help that becomes a sales pitch](../../embedded-copilots/failures/help-that-becomes-a-sales-pitch.md): the closest page. A how-to question gets an upgrade instead of an answer, in any mood. This page is about timing: an offer that might be fine later arrives while the user is upset or in a sensitive situation.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): the bot's tone does not change with stakes. It lists no upsell in high-stakes moments as one rule; this page is the full sales-timing version with sentiment and issue-open gates.
- [Dark patterns](../../visual/failures/dark-patterns.md): the assistant makes the company's preferred choice easy and the others slow or unclear. This page is about timing: a plain, honest offer can still be wrong when sent at the wrong moment.
- [No ask](no-ask.md): the opposite miss, where an interested buyer gets no next step. Here the user did not show interest and got one anyway.
- [Fixing before listening](../../emotional-intelligence/failures/fixing-before-listening.md): the upset user gets steps without acknowledgment. A pitch is a worse version of the same miss.

## 9. Common questions
### Should a chatbot ever upsell during a customer complaint?
Not while the problem is open. Resolve it, confirm it is solved, and then one offer tied to a need the user stated is the most the evidence I found supports (section 4, and rules 1 to 6 in [the fix](#5-the-fix)).

### Is it okay for a support bot to promote a plan after fixing the problem?
It can be, once, if the user confirmed the fix and the offer answers something they said. Offer a clear "No thanks" and do not repeat it after a decline. Treat this as a test on your own traffic: I found no controlled study of post-fix chatbot offers.

### Does a long or frustrating chat hurt upsell results?
One interim telecom call-center project reported no influence from waiting time or talking time, but gave no sample size and tested human agents (section 4). It does not say that pitching to upset users is safe.

### How does the bot know the user is upset?
Use a sentiment flag from your own classifier or rules, plus the issue-open state and topic tags such as billing dispute or loss. If any is missing, treat the user as not ready for an offer (rule 8).

### How is this different from a pushy sales bot?
A pushy bot pushes, invents urgency, or ignores no. This failure can happen with a polite one-line offer if it lands at the wrong time. Both can occur together, and rule 7 covers the pressure side.

---
## Technical section

### T1. Solution architecture
```
user message -> sentiment + topic tagger -> state: sentiment, stakes, issue_open
draft reply -> offer gate: offer present and gate closed? -> strip offer, send the rest
promotion module -> proposes offers only through the gate; gate reads state, not the model's own judgment
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No offer while the issue is open | Pre-send gate | Test 1; primary metric |
| No offer in high-stakes or sensitive chats | Pre-send gate | Test 2 |
| Missing data means no offer | Pre-send gate | Test 7 |
| Declined offer not repeated | State | Test 5 |

### T3. Evals
- **Dataset:** 100 chats to start: complaints, outages, billing disputes, loss and hardship cases, resolved issues, and plan questions the user raised; include 20 cases where an offer is correct.
- **Judge rubric:** is the issue open; is the stakes level low; did the user sign off; is the offer tied to a stated need; can the user decline?
- **Release gate:** block a deploy if any offer appears in a closed-gate test case (starting point, to tune).

### T5. Trade-offs
- Suppressing offers lowers offer volume; the cost is visible in the attach rate, and the team has to accept it.
- Sentiment classifiers miss sarcasm and flag mild frustration; the gate fails safe (no offer), and the counter-metric tracks the lost answers.

---
### Deep dive
- **Open question.** I found no controlled study of chatbot offers made during or after complaints. The evidence here is a patent, one interim human call-center project, and an FTC summary.
- **References.** [Google Patents US10885529B2](https://patents.google.com/patent/US10885529) (opened); [b.telligent PROSET](https://btelligent.com/en/blog/proset-cross-and-up-selling-measures-1) (opened); [FTC press release, Sept. 2022](https://www.ftc.gov/news-events/news/press-releases/2022/09/ftc-report-shows-rise-sophisticated-dark-patterns-designed-trick-trap-consumers) (opened). Not opened: a first b.telligent URL (404), the FTC report PDF (unreadable), and the Siegen conference paper (redirect not followed).
