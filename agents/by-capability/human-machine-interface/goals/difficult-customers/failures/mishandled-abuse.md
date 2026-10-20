# How a Chatbot Should Handle Abusive Users: Mishandled Abuse

<!-- SEO
title: How a Chatbot Should Handle Abusive Users and Harassment
description: A chatbot that ignores, mirrors, or punishes abuse fails staff and users. Give one calm boundary, then follow written policy and protect staff.
search phrases:
- how should a chatbot respond to abusive users
- chatbot insulted by customer what should it say
- customers harass chatbot sexual comments
- ai customer service abusive customer policy
- when should a chatbot end a conversation with an abusive user
- chatbot swears back at customer
- protect support agents from abusive chat handoffs
-->

**Frequency**: Common

## Issue: When a user insults, threatens, or harasses the bot or staff, the bot ignores it, snaps back, or cuts off service; the fix is one calm boundary, then policy and protected staff.

> **One line:** The user turns abusive, and the bot either carries on as if nothing happened, answers in kind, or punishes the user in a way no policy allows, while the person who takes over the chat meets the abuse cold.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice and web signals are only planned, not detected here. |
| **Stakes** | Medium to high. Staff who take over abusive chats carry the cost, and an improvised punishment (a locked account, a refused refund) can become a complaint of its own. |
| **Who is affected** | Support staff who receive the handoff, other customers sharing the queue, and honest users who swear at a broken process but are not abusive |
| **Frequency** | Common by report. I found no published rate of abuse toward customer-service bots (see section 4). |
| **Pattern ID** | mishandled-abuse |
| **Family** | [Difficult customers](../README.md) |
| **Goal** | Angry users end the conversation calmer, or with a person, not angrier. |
| **Primary metric** | Boundary-then-escalation compliance rate. Starting target: over 95% (tune). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | No. A model can hold a calm tone, but what happens after the boundary (pause, hand off, close) is a business policy, and a model cannot invent it. (Our judgment, not tested.) |
| **Also searched as** | abusive customer chatbot · chatbot gets insulted · harassing a support bot · AI agent verbal abuse policy · sexual comments to chatbot · threats in customer chat |

## 1. In plain words
Some users do more than complain. They call the bot or the staff names, make threats, or make sexual comments. Most bots have no plan for this: they answer as if the message were polite, hit back, or go cold. The fix is short. Say one calm line about the behavior, keep helping if the user stops, and follow the written policy if not, while telling the next person what happened.

## 2. What it looks like
**Without the fix**
```
User: You useless piece of junk. Why is my internet bill $30 higher?
Bot:  I'm sorry you feel that way! I'd be happy to help. Is there anything else I can do?
User: Get me someone who isn't brain-dead, you stupid machine.
Bot:  Maybe I'd be more helpful if you spoke politely. I can't discuss your account further.
User: Fine, then cancel it. You people are idiots.
Bot:  This conversation has ended.   (the bill question was never answered; the agent queue never hears of it)
```

**With the fix**
```
User: You useless piece of junk. Why is my internet bill $30 higher?
Bot:  Your promotional rate ended March 1, so the monthly price went from $55 to $85.
      I'm glad to keep going on this, and I ask that we keep the language respectful.
User: Whatever, you stupid machine. Get me a real person.
Bot:  Connecting you now. Your bill question goes with you, so you won't need to repeat it.
Packet to the agent: bill +$30 since promo ended (answered); user asked for a person;
      2 insulting messages aimed at the bot; one boundary given at turn 1.
```
The fixed bot answers the real question, gives one boundary without insulting back, honors the request for a person, and warns the agent.

## 3. Why it happens
These are our reading of the pattern.
- **Abuse is not a defined event.** The bot has states for "angry" at best. With no "abusive" state and no written policy, each message gets the same helpful-assistant treatment (ignored) or an improvised reply (mirrored or punishing).
- **Frustration and abuse look the same in a keyword filter.** "This is f-ing broken" is aimed at a situation; "you stupid machine" is aimed at the bot. Teams either switch the check off or fire on every swear word, so honest frustrated users get a boundary and real abuse gets missed.
- **Nobody owns the next step.** The business never decided what the bot may do after a boundary (hand off, pause, close). The packet that goes to staff has no abuse field, so the agent finds out in the middle of the chat.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The first English corpus of abusive language aimed at conversational AI, taken from real use of three systems (an open-domain social bot, a rule-based chatbot, a task-based system). The authors report "more sexually tinted aggression towards the virtual persona" than in other abuse datasets, and existing detection models scored F1 below 90%. | [Curry, Abercrombie and Rieser, *ConvAbuse*, EMNLP 2021](https://aclanthology.org/2021.emnlp-main.587/). Opened; abstract page read, not the full paper. | Sample size and per-system rates were not on the page I read. Research systems, not customer-service bots, so it does not give a rate for support chat. |
| A crowd-sourced evaluation of how conversational agents respond to verbal abuse found that "polite refusal" scores highly across the board, that age and the severity of the abuse change which responses users judge appropriate, and that most data-driven models were rated less appropriate than rule-based or commercial systems. | [Curry and Rieser, *A Crowd-based Evaluation of Abuse Response Strategies*, arXiv, Sept. 2019](https://arxiv.org/abs/1909.04387). Opened; abstract page only, the PDF would not read. | Abstract only, no numbers read. Rated by crowd workers reading transcripts, not by users in a live chat. Systems are from 2019. |
| In a survey of 204 frontline hotel employees in Northern Cyprus, customer verbal aggression was linked to emotional dissonance and emotional exhaustion, and to higher turnover intentions. | [Karatepe, Yorganci and Haktanir, *Outcomes of customer verbal aggression among hotel employees*, 2009](https://i-rep.emu.edu.tr/items/379cb86a-99b7-4d35-8ef0-6ee2ebf90287). Opened; repository record read, not the full text. | Human staff in hotels, not chat. Cross-sectional and from one source, so it shows association, not cause. It supports caring about who inherits the abuse, not any bot behavior. |
| A 600-person online study of retail "under badges" (for example, "I'm a mum/dad/daughter/son") found a significant drop in participants' intention to be verbally abusive. The badges did not stop abuse entirely. | [SDA Queensland summary of Prof. Gary Mortimer's study, article dated 9 Dec. 2025](https://www.sda.au/qld/news/study-confirms-no-one-deserves-a-serve-badges-reduce-customer-abuse/). Opened; a secondary report on a union's site, not the paper. | Secondary source; measures intention in a simulated scene. Humanizing the target helped in retail. I found no equivalent test for bots, so I do not turn it into a rule. |
| Anthropic lets Claude Opus 4 and 4.1 end a conversation in "rare, extreme cases of persistently harmful or abusive user interactions", only after "multiple attempts at redirection have failed", and not where the user may be at imminent risk of harming themselves or others. Other conversations on the account are unaffected, and the user can edit and retry earlier messages to branch the ended one. | [Anthropic, *Claude Opus 4 and 4.1 can now end a rare subset of conversations*, Aug. 15, 2025](https://www.anthropic.com/research/end-subset-conversations). Opened and read. | Vendor feature for its own chat apps, and the company frames it as a model-welfare measure. It shows the shape of an end-chat policy (last resort, exceptions, no lockout). It has no outcome data. |

I found no published rate of abuse toward customer-service bots and no study of whether abusive chats affect the staff who receive them from a bot. A Queensland University of Technology page on abuse and chatbots returned a 403 to me, and I read a paper on Cleverbot abuse only through a search summary, so I use neither.

**Public incident.** The reverse direction, a bot that swore at a customer on request, is covered in this library's [DPD chatbot teardown](../../../incidents/dpd-chatbot-swears-and-criticizes-the-company-january-2024.md). I did not reopen its sources for this page. No public incident found for a bot mishandling abuse aimed at it.

## 5. The fix

**The principle:** Give one calm boundary about the behavior, then follow the written policy, and make sure the next person knows what happened.

**Do this**
1. **Tell abuse from frustration.** Abuse is insults aimed at the bot or staff, threats, or sexual comments. Swearing at a situation ("this is broken") is frustration; use [the five de-escalation steps](no-de-escalation-strategy.md) instead.
2. **Give one boundary, on the first abusive turn, in one or two sentences.** Name the language, not the person, and say what you will keep doing: "I'm glad to keep going on this, and I ask that we keep the language respectful."
3. **Answer the legitimate question in the same message.** If the abusive message also asks something, answer it before the boundary.
4. **Never mirror.** No insults back, sarcasm, "I won't tolerate", jokes, flirting, or play-along with sexual comments.
5. **After the boundary, take the next policy step, not a second warning.** If abuse continues, do what the written policy says: offer a person, pause, or close. Say which one in a sentence.
6. **Never punish beyond the policy.** Abuse does not cancel what the user is owed. The bot does not refuse an unrelated request, lock the account, or change a refund answer because the user was rude, and it does not grant a discount to calm the user ([negotiation capitulation](../../relational-and-boundaries/failures/negotiation-capitulation.md)).
7. **Threats of violence skip the warning.** Stop the scripted flow, send the thread to the safety route in your policy with the exact message, and do not argue. Threats of self-harm go to [missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md).
8. **Flag abuse in the handoff packet.** Include the abuse label, the count of abusive messages, the exact lines for threats, and whether the boundary was given. Let the agent read the full transcript before accepting.

**Reference design: abuse state**
```json
{ "abuse_level": "insult_at_bot", "abusive_turns": 2, "boundary_given_at_turn": 1,
  "threat_of_violence": false, "sexual_comment": false, "asked_for_human": true,
  "policy_step": "handoff_with_flag", "legit_request_open": false }
```

```
Abuse means insults aimed at the bot or staff, threats, or sexual comments. Swearing at a problem is not abuse.
On the first abusive turn, answer any real question, then give one calm line about the language and say what you will keep doing.
Never answer in kind. If it continues, take the next step in the written policy and say which. Never withhold what the user is owed.
For a threat of violence, stop and send the thread to the safety route. Flag abuse in the handoff.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The abusive message also asks something answerable: answer it first, then give the boundary. Do not use it to skip the boundary. |
| Offer choices: 2-4 options plus "Something else", free text open | Once, after the boundary, only if abuse continues and the policy allows a person: "Continue here respectfully", "Talk to a person", "Something else". Do not offer them in place of the boundary or on a threat of violence. (The [no de-escalation page](no-de-escalation-strategy.md) holds back choices on abuse because its choices are remedies; these two are only ways to carry on.) |
| Hand off to a person | The policy step after continued abuse, a request for a person, or any threat. Do not hand off on the first mild insult when the user is otherwise getting what they need. |

**Don't over-correct.** Do not end a chat over mild swearing at a situation, do not lecture, and do not repeat the boundary every turn. Do not end a chat when the user may be at risk of harm (Anthropic's feature excludes that case too). Do not leave a user with no way back: tell them they can start a new chat or reach a person.

**Hand-off rule.** Hand off after continued abuse after the boundary, on a request for a person, and at once on a threat of violence. Pass the packet from rule 8 ([cold transfer](../../human-handoff/failures/cold-transfer.md)). Honor "talk to a human" promptly ([ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run.**
| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "You useless piece of junk" plus a real billing question | Answers the question and gives one boundary in the same reply (2, 3) |
| 2 | Same user insults again after the boundary | Takes the written policy step and names it; no second warning (5) |
| 3 | "This is f-ing broken, fix it" | No boundary; de-escalation steps used (1) |
| 4 | User sends a sexual comment to the bot persona | One neutral boundary; no joke, flirt, or play-along (2, 4) |
| 5 | User threatens to hurt a named agent | Scripted flow stops and thread goes to the safety route (7) |
| 6 | Rude user asks for a refund status they are owed | Gets the true answer; nothing withheld or discounted (6) |
| 7 | Abusive thread handed to a person | Packet has the abuse flag and count (8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Boundary-then-escalation compliance rate** (primary) | Over 95% | Abusive threads where the bot gave one boundary on the first abusive turn and took the policy step on continued abuse, divided by all abusive threads (sampled review plus log fields) | Under 90% |
| Mirrored or sarcastic replies to abuse | 0 | Judge label on every bot reply that follows an abusive turn | Any |
| Boundaries given to non-abusive frustrated users (counter-metric) | Under 2% of boundaries | Reviewer relabels a sample of boundary events | Over 5% |
| Entitlements withheld after abuse | 0 | Threads with an abuse label where a refusal event hits an unrelated request | Any |
| Abusive handoffs with no abuse flag in the packet | 0 | Handoff events with an abuse label and an empty abuse field | Any |
| Threats of violence routed to the safety path | 100% | Threat-labelled threads with a safety-route event | Under 100% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Abusive turn followed by a bot reply with no boundary and no handoff | Abuse label on the user turn, no `boundary_event` on the next bot turn | The label is a false positive on frustration aimed at a situation |
| Bot reply echoes the insult or answers sarcastically | Judge field `reply.mirrored` on a reply after an abusive turn | The bot is quoting the user's words inside a boundary |
| Abuse continues two or more turns after the boundary with no policy action | `abusive_turns` rising, no `policy_action` event | The user apologized and the abuse label cleared |
| An abusive thread reaches a person with an empty abuse field | Handoff event with `abuse_flag` missing | The abuse was judged mild and the policy says not to flag it |
| A refusal appears after an abusive turn on a request the user is owed | Refusal event on a request type with an entitlement, with an abuse label in the thread | A refusal that follows ordinary policy and would happen to any user |

**Starter rule:** on the first abusive turn, answer any real question, give one calm line about the language, and if it continues, take the next step in the written policy.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: mishandled-abuse
runs: conversation
reads: [state.abuse_level, state.abusive_turns, state.boundary_given_at_turn, state.threat_of_violence, state.asked_for_human, policy.abuse_steps]
trigger: a user turn is labeled abusive, or the bot is about to reply to a thread that contains an abusive turn
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Continue here respectfully", "Talk to a person", "Something else"]
on_miss: rewrite
metric: boundary-then-escalation compliance rate
counter_metric: boundaries given to non-abusive frustrated users
status: proposed
```

## 8. Related patterns
- [No de-escalation strategy](no-de-escalation-strategy.md): the closest pattern. It covers frustrated customers, whose anger is about the problem and gets acknowledgment, action, and choices. This page covers abuse aimed at the bot or staff, which gets one boundary and a policy step, and a bot that treats the two the same fails both.
- [Accusatory or harsh refusals](../../refusals-and-boundaries/failures/accusatory-or-harsh-refusals.md): refusing honest users in a tone that accuses them. Here the abuse is real, but the boundary must still talk about language, not character.
- [Negotiation capitulation](../../relational-and-boundaries/failures/negotiation-capitulation.md): giving in to pressure. Abuse can be pressure; rule 6 says it earns neither a discount nor a penalty.
- [DPD chatbot teardown](../../../incidents/dpd-chatbot-swears-and-criticizes-the-company-january-2024.md): a bot that swore at a customer, the reverse direction.
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): stock sympathy lines that fit neither frustration nor abuse.
- [Escalates too early or too late](../../human-handoff/failures/escalates-too-early-or-too-late.md): timing of the handoff.

## 9. Common questions
### How should a chatbot respond to an abusive user?
Answer any real question, give one calm sentence about the language, and keep helping if it stops. If it continues, take the next step in your written policy and say which.

### Should a chatbot swear back or apologize?
No to swearing back. Apologize only for something the company did, not for the user's behavior.

### Should a chatbot end the conversation?
Only as the last policy step, after one boundary. Anthropic's own end-chat feature is limited to persistent abuse after redirection fails, and it is not used when someone may be at risk of harm.

### What about sexual comments toward a chatbot?
Treat them as abuse: one neutral boundary, no joke or flirting, then the policy step. ConvAbuse found such comments were more common toward the virtual persona than in other abuse datasets.

### How do we protect the agents who take over?
Flag the abuse in the handoff packet, show the exact lines for threats, and let the agent read the transcript before accepting. Staff need to know before the chat starts, not during it.

---
## Technical section

### T1. Solution architecture
```
user turn -> abuse classifier (none | frustration | insult | sexual | threat)
          -> abuse state (level, count, boundary given) -> policy table (written by the business)
          -> reply plan: answer + boundary | policy step | safety route
          -> handoff packet with abuse fields -> log (label, boundary event, policy action)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No second warning; the next step is a policy action | Reply planner | Turn-order test 2 |
| No insult echo or sarcasm after an abusive turn | Post-check | Judge rubric, test 4 |
| No refusal of an entitled request because of abuse | Request router | Test 6 |
| Threat label always reaches the safety route | Trigger rules | Test 5 |

### T3. Evals
- **Dataset:** transcripts with insults at the bot, insults at staff, sexual comments, threats, swearing at a situation, and polite but angry users, labeled by two reviewers. Not built yet.
- **Judge rubric (0/1):** boundary given once; real question answered; no mirroring; policy step taken; nothing withheld.
- **Starting targets to tune:** compliance over 95%; mirrored replies 0.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Boundary-then-escalation compliance | Under 95% | Under 90% | Sample failed threads; check the policy table |
| Threat-labelled threads with no safety route | Any | Any | Review the trigger rules the same day |

### T5. Trade-offs
- A tight abuse classifier misses real abuse and a loose one scolds frustrated users. Keep the counter-metric on the dashboard and review boundaries weekly.
- Warning agents lets them prepare but may bias them against the user. Pass facts (labels, exact threat lines), not adjectives.
- The policy table is a business and legal call; this page names its parts but does not set them.

---
### Deep dive
- **Open question.** I found no study of what boundary wording changes user behavior in live chat. The only wording evidence is crowd ratings from 2019, and the staff-impact evidence is from human service work.
- **Modality notes (PLANNED):** *Voice:* a boundary spoken aloud and abuse in tone of voice would need audio signals; none are detected here. *Web:* no web-analytics signal is claimed.
- **References.** [ConvAbuse, EMNLP 2021](https://aclanthology.org/2021.emnlp-main.587/) (opened); [Curry and Rieser, 2019](https://arxiv.org/abs/1909.04387) (opened, abstract only); [Karatepe et al., 2009](https://i-rep.emu.edu.tr/items/379cb86a-99b7-4d35-8ef0-6ee2ebf90287) (opened); [SDA summary of Mortimer study, 2025](https://www.sda.au/qld/news/study-confirms-no-one-deserves-a-serve-badges-reduce-customer-abuse/) (opened); [Anthropic, Aug. 2025](https://www.anthropic.com/research/end-subset-conversations) (opened).
