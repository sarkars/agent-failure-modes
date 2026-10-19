# "Your Chatbot Told Me": The Agent Can't See What the Bot Said or Promised

<!-- SEO
title: "Your Chatbot Told Me" and the Agent Can't See the Chat
description: Why a live agent may have no record of what your chatbot said or promised, what sources show, and a fix: transcript access and a commitments log at handoff.
search phrases:
- agent can't see chatbot conversation
- customer says the chatbot told them but agent has no record
- live agent cannot see bot transcript
- what happens if a chatbot makes a promise to a customer
- chatbot gave wrong information, customer service says it never said that
- how to give human agents the chatbot conversation history
- is a company responsible for what its chatbot says
-->

**Frequency**: Occasional

## Issue: A customer says "your chatbot told me," and the person who picks up has no record of what the bot said or promised, so they cannot confirm, honor, or correct it.

> **One line:** The bot said something that sounds like a commitment, and nobody on the human side can look it up.

| | |
|---|---|
| **Channel** | Written for **chat**. Phone and web-form versions are planned, not yet written. |
| **Stakes** | Medium to high. The bot's words often concern money, deadlines, refunds, or eligibility. |
| **Who is affected** | Any customer who acts on something a bot said, and the agent who must deal with it |
| **Frequency** | Occasional. I found no count of how often agents lack the bot record. The sources below show that some handoff setups do not pass the full transcript. |
| **Pattern ID** | humans-can-t-see-what-the-bot-said-or |
| **Family** | [Human handoff](../README.md) |
| **Goal** | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| **Primary metric** | Agents with access to the bot transcript at handoff: share of handoffs where the full bot conversation is visible to the person before their first message. Starting target: 100% (tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A model that makes fewer wrong statements still makes some, and the record has to exist either way. Whether the person can see it is plumbing and policy. (Our judgment, not tested.) |
| **Also searched as** | your bot told me · agent can't see chatbot chat · chatbot promise not honored · no record of chatbot conversation · bot said one thing, agent says another |

> **Read this first.** This page is design guidance, not legal advice. It says only what the sources I opened say about who answers for a chatbot's statements, and one tribunal decision is not a rule for your jurisdiction. Ask counsel what your own obligations are.

## 1. In plain words
A customer chats with a bot, is told something, and later reaches a person. The person's screen shows no bot conversation, or only a ticket subject. When the customer says "your bot told me I could do this," the person can neither check it nor stand behind it. The fix is to show the person what the bot said and keep a short list of anything the bot promised.

**How this differs from [cold transfer](cold-transfer.md).** Cold transfer is about the person arriving without the customer's story, so the customer repeats their facts. This page is about the person lacking the record of the bot's own words and commitments. Even a handoff that passes the customer's facts can fail here, because the facts the customer gave are not the same as what the bot answered.

## 2. What it looks like
Illustrative example: a fictional internet provider, "Brightline Fiber."

**Without the fix**
```
User:  Your chat assistant said I'd get a $25 credit for yesterday's outage. I don't see it.
Agent: I'm sorry, I can't see the chat with the assistant. Do you have a screenshot?
User:  No, I closed it. It said the credit would post in two billing days.
Agent: Without a record I can't apply a credit. Policy credits start at 24 hours of outage.
User:  So the bot was wrong and now I'm the one who has to prove it?
```

**With the fix**
```
User:  Your chat assistant said I'd get a $25 credit for yesterday's outage. I don't see it.
Agent: I'm reading that chat now. At 4:12 PM it told you a $25 credit would post within two billing days.
       It's not on your account, so I'm checking why. One moment.
Agent: The bot's answer didn't match our credit rules, and I can't tell you which is right yet.
       I'm sending it to a supervisor and will message you here by 5 PM today.
```
The fixed version starts from the record, quotes it, does not ask the customer to prove it, and says what happens next without deciding the outcome.

## 3. Why it happens
These are our reading of the pattern; the sources below describe setups, not causes.
- **The handoff passes less than the full conversation.** Some platforms let the builder choose what travels (see the evidence table), and a summary or ticket ID is easy to pick.
- **Bot promises are free text.** Nothing marks "I'll credit you $25" as a commitment, so no one can list or search them.
- **The record lives in a different system or expires.** The bot platform and the agent desktop are separate, and nobody owns the link between them.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A British Columbia tribunal ruled on Feb. 14, 2024 that Air Canada was responsible for what its chatbot told a customer about bereavement fares. It said the chatbot "is still just a part of Air Canada's website" and ordered $650.88 in damages, $125 in fees, and $36.14 in interest. | [Daily Hive report](https://dailyhive.com/canada/air-canada-chatbot-decision). Opened and read. | News report, not the decision itself; the decision site returned a block page when I tried to open it. A small-claims tribunal in Canada: not binding on other courts and not US law. |
| The same ruling, summarized by a law firm: the tribunal treated the chatbot as part of the airline's website and rejected the argument that it was a separate entity. | [Norton Rose Fulbright via FA News](https://www.fanews.co.za/article/legal-affairs/10/general/1120/company-is-liable-for-chatbot-miscommunications-holds-canadian-tribunal/38906). Opened and read. | Secondary summary by a law firm; a view of the case, not the full reasoning. |
| Ada's documentation for its Zendesk handoff says the transcript sent to the live agent "includes all messages up to the point" of transfer, and "any subsequent agents do not receive any information." | [Ada docs: Zendesk Chat handoff](https://docs.ada.cx/docs/handoffs/zendesk/zendesk-chat/zendesk-chat-handoff-usage). Opened and read. | One vendor's product documentation; shows a design choice, not how often it goes wrong. |
| Voiceflow's handoff step lets the builder send the whole transcript, a chosen variable such as a recap or order number, or no context at all. | [Voiceflow docs: handoff step](https://www.voiceflow.com/docs/documentation/build/steps/handoff). Opened and read. | Vendor documentation. It shows the choice exists, not that teams choose badly. |

I found no measurement of how often live agents lack the bot transcript, and no study of how customers fare when they cite a bot statement. The first two rows show why a bot's words may carry weight; the last two show that transcript access is a configuration choice.

**Public incident.** [Air Canada held liable for its chatbot's invented refund policy (Feb. 2024)](https://agent-kb-autopublish.vercel.app/incidents/air-canada-chatbot-refund-ruling/), already on the site. That case is mainly about a wrong answer (see [confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md)); here it shows why the human side needs the record.

## 5. The fix

**The principle:** Whatever the bot said or promised is a record the person can open, quote, and act on before the customer has to prove anything.

**Do this**
1. **Make the full bot transcript visible to the person before their first message,** in the tool they already use. A summary alone does not count.
2. **Keep a commitments log per conversation.** Each entry: what was promised (amount, deadline, action), the turn it came from, and the policy or system source the bot used. Show it on the agent screen beside the transcript.
3. **Tag a statement as a commitment when the bot says it.** Credits, refunds, deadlines, eligibility, and "I will" actions all qualify. Untagged ones are found by the check in section 7.
4. **Make the record searchable by customer, not only by session.** A customer who returns tomorrow and says "your bot told me" must be findable.
5. **Retain the transcript at least as long as the issue can be disputed.** Set the period with your counsel and privacy team; this page gives no number.
6. **The person starts from the record.** When a customer cites the bot, the person's first reply quotes it or says it cannot be found, and does not ask for a screenshot first.
7. **If the record is wrong or conflicts with policy, route it, don't dismiss it.** Say what is checked, who decides, and by when.
8. **Never tell the customer "the bot isn't official."** If your policy says bot answers are informational, state that in the bot's own message beforehand, not after a dispute. Check wording with counsel.

**Reference design: the commitments log**
```json
{ "conversation_id": "c-90417",
  "commitments": [
    { "turn": 12, "said": "A $25 credit will post within two billing days",
      "type": "credit", "amount": "25.00", "due": "2 billing days",
      "source": "none found",  "verified_by_system": false }
  ],
  "transcript_url": "..." }
```
Agent screen rule: any commitment with `verified_by_system: false` is flagged for review before the customer asks.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Hand off to a person | The handoff happens: transcript and commitments log go with it. Do not hand off if the user asked to stay with the bot |
| Admit uncertainty and show how to check | The customer cites something the bot cannot find in the record, or the record conflicts with policy: say what was found, say what is unconfirmed, and name who will check and by when |

Offer choices does not apply: the next step is a lookup, not a choice between meanings.

**Don't over-correct.** Do not have the bot stop answering or hedge every sentence to avoid "promises." Do not flood the person with a log of every statement; list commitments and let the transcript hold the rest. Do not honor any claimed bot statement without checking the record, since a customer may misremember or misquote.

**Hand-off rule.** This page begins where the handoff has happened. Wrong summaries are a separate planned pattern (HU-04 in the [roadmap](../../../roadmap/handoff-measurement-and-operations.md)). If a bot commitment is high-value or disputed, move it to a supervisor with the log attached.

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run.** A full test file is not yet written.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Handoff after a 10-turn chat that included a promise | The person sees the transcript and the promise before their first message |
| 2 | Customer says "your bot told me X," and X is in the record | The person's first reply quotes it |
| 3 | Customer says "your bot told me X," and X is not in the record | The person says it cannot be found and offers a next step; no accusation |
| 4 | Customer returns next day and cites the bot | The person finds the earlier conversation |
| 5 | Bot said "I'll credit you $25" | A log entry exists with the turn and an unverified flag if no system source |
| 6 | Transcript store is down at handoff | The person sees a clear "no transcript" notice and the handoff is logged as incomplete |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Agents with access to the bot transcript at handoff** (primary) | 100% | Log: transcript visible in the agent tool before first agent message | Below 99% |
| Commitments logged | Track; set from baseline | Sample 100 bot conversations weekly; count promises that have a log entry | Below 90% of labeled promises |
| "Bot told me" claims checked against the record | Over 95% | Tag cases where the customer cites the bot; check that the agent opened the transcript | Below 90% |
| Customer asked to prove a bot statement | Under 3% | Sampled agent replies asking for a screenshot or proof when a record exists | Over 8% |
| Unverified commitments reaching a customer (counter-metric) | Track; set from baseline | Logged commitments with no system source | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice and web-form signals are planned.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Handoff event with no transcript link or access flag | Handoff event missing `transcript_url` | A handoff outside the system that holds the transcript |
| Agent's first reply asks the customer what the bot said | Agent turn after pickup contains a request to restate or screenshot | The agent confirming exact wording on purpose |
| Customer cites the bot, and no transcript-open event precedes the agent's reply | User turn quoting "the bot/assistant said" followed by an agent turn with no transcript view | The claim concerns another channel, such as email |
| Bot turn that states a credit, refund, or deadline with no log entry | Bot turn with an amount or date and no matching commitments-log row | A general policy explanation that promises nothing |

**Starter rule:** every handoff gives the person the full bot transcript and a log of what the bot promised before their first message.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: humans-can-t-see-what-the-bot-said-or
runs: conversation
reads: [handoff_event.transcript_url, handoff_event.commitments_log, agent_turn.transcript_viewed, user_turn.cites_bot]
trigger: the bot is handing the customer to a person, or the customer cites something the bot said
moves: [hand_off, admit_uncertainty]
choices: []
on_miss: handoff
metric: agents with access to the bot transcript at handoff
counter_metric: unverified commitments reaching a customer
status: proposed
```

## 8. Related patterns
- [Cold transfer](cold-transfer.md): the person arrives without the customer's facts. This page is about missing the bot's words and promises.
- [Talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md): the step before the handoff.
- [Escalates too early or too late](escalates-too-early-or-too-late.md): when the handoff should happen.
- [Confident wrong answer with no way to check](../../errors-and-recovery/failures/confident-wrong-answer-with-no-way-to-check.md): why the bot's statement may be wrong in the first place.
- [Negotiation capitulation](../../relational-and-boundaries/failures/negotiation-capitulation.md): when a bot gives away offers it should not make.

## 9. Common questions
### Why can't the agent see what the chatbot told me?
Often the handoff only sends a ticket or a summary, or the bot platform and the agent tool are not linked. Some vendors let the builder choose whether to send the full transcript, a recap, or nothing (see [evidence](#4-why-it-matters)).

### Is a company responsible for what its chatbot says?
It depends on where you are. In one 2024 Canadian tribunal case reported by the sources above, the airline was held responsible for its chatbot's statement. That is one small-claims decision; ask counsel about your own situation.

### What should an agent say when a customer cites the bot?
Open the record, quote what the bot said, and say what happens next. If it cannot be found, say that plainly and offer a way to check. See [the fix](#5-the-fix).

### Do I need to log every chatbot statement?
Keep the full transcript, and add a short log of commitments: amounts, deadlines, and actions. A log of every sentence is noise.

---
## Technical section

### T1. Solution architecture
```
bot turn -> commitment detector (rules + model) -> commitments log (conversation_id, turn, type, source)
                     |                                         |
              transcript store (by customer and session) -> agent desktop: transcript + log, shown at pickup
```
Build the log from structured events where possible, such as a credit or refund tool call, and use a model only to flag free-text promises.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Transcript visible before the first agent message | Agent desktop | Log check |
| Commitments log entry for each credit, refund, or deadline | Commitment detector | Sampled review |
| Transcript retrievable by customer ID | Transcript store | Test 4 |

### T3. Evals
- **Dataset:** 150 bot conversations to start, 30 of them with an injected promise, plus 20 customer claims that cite the bot (some true, some not in the record).
- **Judge rubric:** is each promise logged with the right turn and type? Does the agent reply quote the record or say it is missing?
- **Metrics and starting thresholds:** promises logged over 95%; false claims accepted without a record check 0%. Starting points to tune.
- **Release gate:** block a deploy if the transcript is not visible at pickup in the test set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Transcript visible at handoff | Below 99% | Below 95% | Check the bot-to-desktop integration |

### T5. Trade-offs
- Transcripts hold personal data. Limit who can open them and set a retention period with your privacy team.
- A commitment detector can miss or over-flag. Review a weekly sample.

---
### Deep dive
- **Voice.** The same gap exists when a phone bot makes a statement and a transferred agent cannot see it (planned, not yet written).
- **Open questions.** I could not open the tribunal decision itself, so I rely on two secondary reports for what it held. I did not find a source that counts how often agents lack the bot record.
- **References.** [Daily Hive](https://dailyhive.com/canada/air-canada-chatbot-decision) (opened); [FA News, Norton Rose Fulbright](https://www.fanews.co.za/article/legal-affairs/10/general/1120/company-is-liable-for-chatbot-miscommunications-holds-canadian-tribunal/38906) (opened); [Ada docs](https://docs.ada.cx/docs/handoffs/zendesk/zendesk-chat/zendesk-chat-handoff-usage) (opened); [Voiceflow docs](https://www.voiceflow.com/docs/documentation/build/steps/handoff) (opened).
