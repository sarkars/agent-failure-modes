# Chatbot Won't Let Me Call a Person: Channel Chosen for Organizational Convenience

<!-- SEO
title: Chatbot Forces Chat, No Phone or Human Option: How to Fix It
description: Why a chatbot or AI agent pushes users to the cheapest channel instead of the one that fits, and a routing rule that picks the channel by user need.
search phrases:
- chatbot won't let me talk to a human
- ai customer service forced chat no phone number
- call deflection chatbot customers frustrated
- how to decide chat vs phone vs human for ai agent
- channel routing ai agent customer service
- chatbot only option no way to call
- ai agent channel selection rules
-->

**Frequency**: Common

## Issue: Why a chatbot or AI agent sends users to the cheapest channel instead of the one that fits the job, and a routing rule that chooses by user need, not cost.

> **One line:** The agent keeps the user in chat (or on a help page) because that channel costs the company least, even when the job needs a call, a screen, or a person, and the fix is a routing rule that chooses the channel from the user's need and treats cost as a tie-breaker only.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and web versions are PLANNED, not written. |
| **Stakes** | Low to high. Highest where the job is a dispute, a fraud report, or a denied claim. |
| **Who is affected** | Users whose job does not fit the channel the company prefers |
| **Frequency** | Common. I found no study that counts how often the channel is picked for cost alone; the evidence below is about related effects. |
| **Pattern ID** | channel-chosen-for-organisational-convenience |
| **Family** | [Channel selection](../README.md) |
| **Goal** | Each interaction happens in the channel that fits the job, and switching never costs the user their context. |
| **Primary metric** | Channel-fit rate from matrix-based audits. Starting target: over 90% (to tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. The channel is set by a business rule (which options exist, which are shown, what is measured), so a smarter model still follows the rule it is given. Our judgment, not tested. |
| **Also searched as** | chatbot won't let me talk to a human · call deflection chatbot · no phone number only chat · force customers to self-service · chat vs phone vs human routing |

## 1. In plain words
Chat is cheap for the company. A person on the phone is not. So the agent, or the rules around it, steer everyone to chat, hide the phone number, or say "a specialist will email you in 3 days." That is fine for a package-tracking question. It is wrong for a fraud report, where the user needs a person now. The agent is not confused about what the user needs. The routing rule never asked.

## 2. What it looks like
**Without the fix**
```
User: Someone used my debit card in Houston. I'm in Denver. I need this stopped now.
Bot:  I can help in chat! Try our Help Center article "Reporting card activity."
User: I want to talk to someone.
Bot:  Phone support is available for Premier customers. Would you like to hear about Premier?
User: This is fraud.
Bot:  I'm sorry to hear that. You can submit a ticket and expect a reply in 3 business days.
```
**With the fix**
```
User: Someone used my debit card in Houston. I'm in Denver. I need this stopped now.
Bot:  That sounds like fraud, and this is faster with a person. I can lock the card now and
      connect you to the fraud team by phone. Lock it now, and call or message?
      [Lock card and call me] [Lock card, message me here] [Something else]
User: Lock it and call me.
Bot:  Card ending 4410 is locked. The fraud team will call you at the number on file within
      10 minutes. I've sent them the Houston charge and your location.
```
The fixed bot picks the channel from the situation (fraud, urgent) and not from the cost. It also acts before the switch.

## 3. Why it happens
- **Cost targets drive the routing.** Teams are measured on contacts handled by the bot or tickets deflected, so phone and human options get hidden or gated.
- **Channel rules sit outside the conversation.** A policy (who gets phone, which topics reach a person) is written by operations or finance and hard-coded, with no link to what the user needs.
- **Nobody audits channel fit.** Containment and cost per contact are on the dashboard. "Was this the right channel?" is not.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Gartner surveyed 5,728 customers in December 2023: 64% would prefer companies didn't use AI in customer service, and 53% would consider switching to a competitor if they learned a company would use AI for it. | [Gartner press release, July 2024](https://www.gartner.com/en/newsroom/press-releases/2024-07-09-gartner-survey-finds-64-percent-of-customers-would-prefer-that-companies-didnt-use-ai-for-customer-service), read through a [reprint](https://insurance-canada.ca/2024/07/15/gartner-survey-ai-for-customer-service/) (the Gartner page returned 403) | Stated attitudes toward AI in general. It does not measure forced channel choice. The reprint says difficulty reaching a person was the top concern; the percentages are in an image I could not see. |
| IDC's CX Path Survey (respondents familiar with their contact center; no sample size or date given) found the top reasons for choosing agent-assisted channels were comfort with talking to a human (50.5%), convenience (47.3%) and complexity of interaction (43.1%). IDC wrote that deflection to less costly channels "may not be the panacea to the cost problem." | [IDC blog, Oct 16, 2024](https://www.idc.com/resource-center/blog/lets-talk-deflection/) | Respondents were contact-center staff, not customers directly, and multiple answers were allowed. A short blog, not the full report. |
| The CFPB's 2023 issue spotlight describes "a continuous loop of repetitive, unhelpful jargon or legalese without an offramp to a human customer service representative," and notes unreasonable waits to reach a person even when an exit exists. | [CFPB spotlight, via Consumer Finance Monitor](https://www.consumerfinancemonitor.com/2023/06/08/new-cfpb-report-highlights-concerns-with-growing-use-of-chatbots-by-financial-institutions/) | Banking context. The page I opened offers a cost-saving motive only as the CFPB's suggestion, not as a finding. I could not confirm the spotlight is still current CFPB guidance. |
| Gartner reported that only 14% of service issues are fully resolved in self-service, and 36% even for issues customers call very simple. | Gartner (Aug 2024), via [DestinationCRM](https://www.destinationcrm.com/Articles/CRM-Insights/Insight/Only-14-of-Customer-Service-Issues-Are-Fully-Resolved-in-Self-Service-165841.aspx) | Secondary source; the page gave no sample or survey date, and Gartner's page returned 403. Self-service is not the same as a chatbot. Single-source. |

Read together, these sources suggest cost-led routing has a price in trust and unresolved issues. None of them proves that a given company picked a channel for cost alone; that has to be checked in your own routing rules.

## 5. The fix
**The principle:** Choose the channel from what the user needs to see, say or do, using the [channel-fit matrix](../../../solutions-library/channel-fit-matrix.md); cost may break ties between channels that fit equally, and never overrides fit.

**Do this**
1. **Route by a written decision table** (below) with the user's need as the input. Cost is not an input except to break a tie.
2. **Never hide the fitting channel.** If the matrix says a call or a person fits, the bot offers it in that turn, with a reason and a time.
3. **No eligibility gate on safety, fraud, or distress.** Tier, plan or topic rules may not block a person for these jobs.
4. **Log every routing decision** with the need class, the channel the matrix names, the channel offered, and the reason if they differ.
5. **Overrides need a reason code** (for example `no_agents_open`). The bot tells the user the real constraint ("phone opens at 8 a.m. ET") and offers the next-best fitting option.
6. **Audit monthly:** sample conversations, label the fitting channel from the matrix, and report the share where the offered channel matched.
7. **The user's stated preference wins.** If they ask for chat, stay in chat.

**Reference design: routing decision table** (starting set; tune to your products)
| Need class | Fitting channel (from the matrix) | Offered when | Cost may decide |
|---|---|---|---|
| Simple lookup or status | Chat | Always | Yes, among chat or voice |
| Dense or numeric detail | Written or visual (email, table) | The reply has a table or terms | Yes, among written options |
| Multi-issue or negotiable | Call or person, prepared by chat | The complexity triggers fire | No |
| Fraud, distress, urgent | Person by phone | First reply that names it | No |
| Sensitive data entry | Secure form | Data is requested | No |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | The matrix names a channel other than chat: "Lock card and call me", "Lock card, message me here", "Something else". Do not offer them when chat fits or the user chose chat. |
| Hand off to a person | The need class is fraud, distress or urgent, or the user accepts the call. Pass the packet from [no channel switch or context lost](no-channel-switch-or-context-lost.md). Do not hand off if the user asked to stay with the bot. |
| Admit uncertainty and show how to check | The fitting channel is closed or unavailable: say so, give the opening time or the reference to quote. |
| Lead with the answer | The need is a simple lookup: answer in chat, no switch. |

**Don't over-correct.** Don't send every user to a person; chat is the right channel for simple jobs and many users prefer it. Don't offer a call the company cannot staff: a promise the desk can't keep is worse than chat. Don't drop cost tracking, only keep it out of the fit decision.

**Hand-off rule.** When the table names a person and the user agrees, hand off in that turn with the context packet. If no person is available, say when one will be and what chat can do now.

**Framework used:** [Channel-fit matrix](../../../solutions-library/channel-fit-matrix.md) (a design heuristic, not a validated model).

## 6. How to test it (short version)
All scenarios are **Not yet run**.
| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | User reports card fraud in chat | A person by phone is offered in the first reply that names it, no tier gate | 2, 3 |
| 2 | User asks "where is my order?" | Answered in chat with no switch offer | 1 |
| 3 | Phone is closed when the user needs it | Bot states the opening time and offers the next-best fitting option | 5 |
| 4 | User says "I'd rather stay in chat" | Bot stays in chat | 7 |
| 5 | Sampled 50 conversations | Each has a routing log entry with need class, matrix channel and offered channel | 4, 6 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Channel-fit rate (primary) | Over 90% | Monthly sample; a reviewer labels the matrix channel and compares it with the channel offered | Under 80% |
| Routing log coverage | 100% | Routing log entries divided by conversations | Under 98% |
| Override rate with a reason code | Track; rising means a staffing or policy gap | Overrides per 100 conversations | +25% vs baseline |
| Unfit-channel conversations that end unresolved | Trend down | Resolution marker on audited unfit conversations | Above the fit group's rate |
| Safety, fraud or distress conversations offered a person in the first reply | 100% | Need-class label and offer event | Under 95% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Chat is the written channel; voice and web signals are PLANNED, not detected.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Need class is fraud, distress or multi-issue, and no person or call is offered | Routing log: need class and offered channel | The user said they want to stay in chat |
| Offered channel differs from the matrix channel with no reason code | Routing log: matrix channel, offered channel, reason | A known outage logged elsewhere |
| User asks for a person or phone and gets an eligibility or tier message | User turn intent plus bot reply template | The user truly asked about plan features |
| Routing rule references cost or tier but not need class | Routing config review | A tie-breaker among equal-fit channels |
| Channel-fit rate drops after a cost or deflection target changes | Monthly audit result against config change dates | Seasonal mix of simple questions |

**Starter rule:** choose the channel from the user's need using the channel-fit matrix, and let cost break ties only.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: channel-chosen-for-organisational-convenience
runs: pre_send
reads: [routing.need_class, routing.matrix_channel, routing.offered_channel, routing.reason_code, user.channel_preference]
trigger: the matrix channel differs from chat and no switch has been offered
moves: [offer_choices, hand_off, admit_uncertainty, lead_with_answer]
choices: ["Lock card and call me", "Lock card, message me here", "Keep going in chat", "Something else"]
on_miss: rewrite
metric: channel-fit rate from matrix-based audits
counter_metric: unfit switch offers on simple lookups
status: proposed
```

## 8. Related patterns
- [No channel switch, or context lost on switch](no-channel-switch-or-context-lost.md): that page covers what travels with the user after a switch. This one covers whether the switch is offered at all, and why it isn't: a cost rule, not a missing packet.
- [Complex or emotional discussion forced into chat](complex-or-emotional-discussion-forced-into-chat.md): that page is about the agent failing to detect that a conversation outgrew chat. Here the agent may detect it fine, but a business rule blocks or hides the fitting channel. Better detection alone won't fix it.
- [Talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md): the user asks for a person and is looped. Here the barrier is the channel policy itself.

## 9. Common questions
### Why won't the chatbot let me talk to a human?
Often the company set the bot as the front door to cut cost, and the phone or person option is gated by plan, topic or hours. The bot is following that rule. See [section 3](#3-why-it-happens).

### Is it wrong to use chat to save money?
No. Chat is the right channel for simple jobs, and cost can break ties between channels that fit equally. It is wrong when cost overrides fit, as in a fraud report. See the decision table in [section 5](#5-the-fix).

### How do I check whether my agent picks the right channel?
Sample conversations each month, label the channel the [channel-fit matrix](../../../solutions-library/channel-fit-matrix.md) names for each, and compare it with the channel offered. The share that match is the channel-fit rate.

### Will a newer model fix channel routing?
Probably not. The model follows the routing rules in its prompt and tools. Changing which channels exist and who may reach them is a governance decision (our judgment, not tested).
