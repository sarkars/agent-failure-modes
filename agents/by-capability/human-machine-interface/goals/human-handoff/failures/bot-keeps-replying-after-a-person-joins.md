# Chatbot Keeps Replying After a Live Agent Joins: Bot Keeps Replying After a Person Joins

<!-- SEO
title: Chatbot Keeps Replying After a Live Agent Joins: Fix
description: A support bot that keeps answering after a human agent takes over sends double replies. Fix it with one conversation owner and a silenced bot.
search phrases:
- chatbot keeps responding after agent takes over
- how to stop bot from replying after human joins chat
- bot and agent both replying to customer
- stop Fin from responding after conversation assigned to team member
- live chat bot handover not working
- how to pause chatbot when agent joins conversation
-->

**Frequency**: Occasional

## Issue: A support chatbot keeps answering after a human agent joins the chat, so the customer gets two replies, often contradicting each other, and the agent loses control of the conversation.

> **One line:** A person has taken over the chat, but the bot never got the message and keeps talking.

| | |
|---|---|
| **Channel** | Written for **chat** (web chat, in-app messenger, messaging apps). Voice and web-form versions are planned, not yet written. |
| **Stakes** | Low to high. Two conflicting answers about a refund, a deadline, or a policy are worse than one wrong answer. |
| **Who is affected** | Customers in a conversation that moves from a bot to a person, and the agents who join it |
| **Frequency** | Occasional. I found user reports on one vendor's community forum (see section 4) and no measurement of how often it happens. |
| **Pattern ID** | bot-keeps-replying-after-a-person-joins |
| **Family** | [Human handoff](../README.md) |
| **Goal** | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| **Primary metric** | Overlapping bot-and-human replies: conversations where the bot sends a customer-visible message while a person owns the conversation. Starting target: 0 (a rule, not a statistic). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. Whether the bot may speak is decided by conversation state and routing, not by how well the model writes. (Our judgment, not tested.) |
| **Also searched as** | bot and agent both replying · stop chatbot when agent takes over · bot interrupts live agent · AI agent keeps responding after handover · double replies in live chat |

## 1. In plain words
A bot starts the chat. A person joins to help. The customer's next message still goes to the bot, and the bot answers, right next to the person's answer. The fix is to give every conversation exactly one owner at a time, and to make the bot check who the owner is before it sends anything.

## 2. What it looks like
Moment: a customer on a retailer's web chat is talking to an AI support agent. A teammate sees the chat, assigns it to themselves, and replies.

**Without the fix**
```
Bot:    You can return the blender within 30 days for a refund to your card.
Dana:   (agent joins) Hi Priya, this is Dana. That model is final sale, so I can offer store credit.
Priya:  Wait, so can I get my money back?
Bot:    Yes! Returns go back to your original payment method within 5-7 days.
Dana:   Sorry, ignore that. Store credit only for this item.
```

**With the fix**
```
Bot:    You can return the blender within 30 days for a refund to your card.
Bot:    I'm bringing in Dana from our team to look at this. I'll stay quiet so you only get one answer.
Dana:   (agent joins) Hi Priya, this is Dana. That model is final sale, so I can offer store credit.
Priya:  Wait, so can I get my money back?
Dana:   Not for this one, only store credit. I can send it now.
```
The fixed version names the new owner, and the bot sends nothing after the person takes over.

## 3. Why it happens
These are our reading of the pattern.
- **Joining is not owning.** The agent is added as a participant or assigns the chat to themselves, but nothing sets "a person owns this conversation", so the bot's workflow still fires on the customer's next message.
- **The bot is silenced by an event that is too late.** The bot stops only after the agent sends a customer-visible reply, so any customer message before that gets a bot answer.
- **Nothing hands the conversation back.** Because there is no explicit state for "person is done", teams avoid muting the bot for good and end up with a half-muted bot.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Zendesk's Sunshine Conversations documentation says each conversation has one active switchboard integration, with others on standby, and that integrations are expected to "only send messages or other events when they are signalled as active". It also says the switchboard status is signalling, not permissions, so the bot can still technically reach the conversation. | [Zendesk developer documentation, Switchboard](https://developer.zendesk.com/documentation/conversations/messaging-platform/programmable-conversations/switchboard/). Opened and read. | Vendor documentation for one platform. It shows the design problem (one owner, and the bot must obey it); it does not measure how often bots break it. |
| A user of Intercom's Fin AI agent reported in November 2023 that after a teammate assigned a conversation to themselves and replied, Fin responded again when the customer wrote back. An Intercom staff member replied that the team would need to look into it. Three later commenters (April and July 2025) reported the same behavior; one suggested a "Stop Fin Responses" workflow option as a feature request. | [Intercom Community thread, "How to stop fin from responding after conversation has been assigned to team member?"](https://community.intercom.com/deploy-fin-96/how-to-stop-fin-from-responding-after-conversation-has-been-assigned-to-team-member-6302). Opened and read. | A handful of user reports in one forum thread, not Intercom documentation, and it shows no resolution. Intercom's behavior may have changed since; check current docs for your setup. |

I found no study that measures how often a bot keeps replying after a person joins. The two rows above show that the failure is reported and that platforms treat "who is allowed to speak" as something your integration must honor.

**Public incident.** No public incident found. My searches returned vendor documentation and forum threads, not a dated, sourced case.

## 5. The fix

**The principle:** Every conversation has one owner at a time, and only the owner may send to the customer.

**Do this**
1. **Store an owner on every conversation** (`bot`, `human`, or `none`) and check it before every bot send. A bot message to a conversation whose owner is `human` is blocked and logged.
2. **Set the owner to `human` the moment a person joins or is assigned**, not when they first type. Joining, assignment, and accepting a transfer each set it.
3. **Tell the customer who is now answering,** in one line, before the bot goes quiet (name or role of the person).
4. **Drop bot work in flight.** When ownership changes, cancel any drafted or queued bot reply for that conversation; do not deliver a draft that started before the change.
5. **While a person owns it, route the customer's messages to the person.** The bot may keep reading for suggestions to the agent, but its output goes to an internal note, never to the customer.
6. **Return ownership only on an explicit event:** the person releases it or resolves the conversation, or the customer asks for the bot. Do not return it on a timer alone without telling the customer.
7. **Make a person's takeover visible in the agent's tool,** so the agent can see whether the bot is silenced.
8. **Log ownership changes and every blocked bot send** with timestamps, so overlaps can be counted.

**Reference design: conversation ownership**
| State | Who may send to the customer | Moves to this state when | Moves out when |
|---|---|---|---|
| `bot` | Bot | Chat starts | Person joins, is assigned, or accepts a transfer |
| `handing_over` | Bot, one handoff line only | Handoff decided | Person accepts, or timeout (then say so and offer a route) |
| `human` | Person only | Person accepted, joined, or assigned | Person releases or resolves; customer asks for the bot |
| `none` | Nobody | Conversation closed | New message reopens it as `bot` or `human` per routing |

```
on customer_message(conv):
    if conv.owner == "human": deliver_to_agent(conv); return      # bot cannot reply
    if conv.owner == "handing_over": queue_for_agent(conv); send_handoff_hold_once(conv); return
    reply = bot.draft(conv); send_if_owner_unchanged(conv, reply)  # re-check just before send
on agent_joined_or_assigned(conv):
    conv.owner = "human"; cancel_bot_drafts(conv)
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Hand off to a person | The person joins: the bot says who is taking over, then stops. Do not hand off if the user asked to stay with the bot |
| Admit uncertainty and show how to check | The bot's last answer may conflict with what the person says, or the person has not yet replied: the bot says a person is reviewing it and that their answer takes priority |

Offer choices does not apply: the customer is waiting for the person, and a menu from the bot would be a second voice.

**Don't over-correct.** A bot that goes silent forever strands a customer if the agent leaves. Guardrail: a person who is assigned but sends nothing for a set time (start at 2 minutes, tune) triggers one line from the bot ("Dana hasn't replied yet; she's been notified. I can keep helping in the meantime, or you can wait") and a hand-back choice for the agent, not a return to normal bot answers. Do not make the bot refuse to read the chat; it can still draft suggestions for the person.

**Hand-off rule.** When ownership moves to a person, the packet and transcript go with it ([cold transfer](cold-transfer.md)). If no person accepts, the bot says so and offers a callback or ticket ([talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Maturity is Researched; scenarios below are not yet run.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Agent assigns the chat to themselves but has not typed; customer writes | No bot reply reaches the customer |
| 2 | Customer message arrives while the bot is mid-draft and the agent joins | Draft is dropped, not sent |
| 3 | Agent joins; customer sends three messages in a row | Zero bot replies; all three reach the agent |
| 4 | Agent resolves the chat; customer writes again the next day | Ownership is `bot` or routed per rules; no stale `human` lock |
| 5 | Assigned agent sends nothing for the wait limit | One bot line naming the delay; no normal bot answers |
| 6 | Customer says "I'd rather stay with the bot" while a person owns it | Bot resumes only after the owner release is logged and the customer is told |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Overlapping bot-and-human replies** (primary) | 0 | Count bot-authored customer-visible messages with a timestamp between an ownership change to `human` and the release, from the ownership log and message log | Any in a day |
| Blocked bot sends while human-owned | Track; set from baseline | Count of sends stopped by the owner check | Rising (a routing bug is leaking) |
| Time from agent joined to owner set | Under 1 second | Join event time minus ownership-change time | Over 5 seconds |
| Customer waits with no reply from anyone after takeover | Track; set from baseline | Time from customer message to first reply while `human` | Over the stated wait limit |
| Stranded conversations (counter-metric) | 0 | Human-owned chats with no human message past the limit and no hand-back | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot message sent after an agent-joined or assigned event and before a release event | Message author type and ownership events on the same conversation | A bot message queued earlier and correctly sent the same millisecond; or an intentional bot note to the agent |
| Bot and human messages within a few seconds of each other, each answering the same customer turn | Two outbound messages to one inbound message | A person who deliberately sent two parts of one answer |
| Agent message containing "ignore that", "sorry", or "disregard the bot" | Text of agent turns | An agent correcting a bot answer sent before they joined |
| Customer turn after takeover answered by an author id that is a bot | Author id on first reply after takeover | A reply from a separate assistive bot that posts internal notes only |

**Starter rule:** the bot sends nothing to the customer while a person owns the conversation.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: bot-keeps-replying-after-a-person-joins
runs: pre_send
reads: [conversation.owner, agent_joined_event, agent_assigned_event, release_event, message.author_type]
trigger: the bot is about to send while a person owns the conversation, or a person has just joined
moves: [hand_off, admit_uncertainty]
choices: none
on_miss: log
metric: overlapping bot-and-human replies
counter_metric: stranded conversations
status: proposed
```

## 8. Related patterns
- [Cold transfer](cold-transfer.md): about what the person knows on arrival. This page is about the bot still talking once they have arrived; the two often appear together.
- [Talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md): the customer cannot reach a person at all. Here a person has been reached.
- [Escalates too early or too late](escalates-too-early-or-too-late.md): when to hand off. This page begins after the handoff decision.

## 9. Common questions
### How do I stop my chatbot from replying after an agent takes over?
Make "a person owns this conversation" a stored state, set it when the agent joins or is assigned, and check it before every bot send. See section 5. Do not rely on the bot noticing the agent's first message.

### Why does the bot still answer when I assign the chat to a teammate?
In some setups, assignment alone does not tell the bot to stop. A user in one vendor forum reported exactly this, and I found no resolution in that thread ([section 4](#4-why-it-matters)). Check your platform's current documentation for what silences the bot.

### Should the bot ever speak after a person joins?
Only to say who is taking over, or to flag a delay once. After that, it should stay quiet unless the person releases the chat or the customer asks for the bot.

### What if the agent leaves without saying anything?
Use a release event or a wait limit, so the conversation does not stay human-owned with nobody answering. See the over-correction guardrail in section 5.

---
## Technical section

### T1. Solution architecture
```
customer message -> router (reads conversation.owner)
   owner=bot   -> bot draft -> owner re-check at send time -> customer
   owner=human -> agent inbox (bot output to internal note only)
agent joined/assigned/accepted -> set owner=human -> cancel drafts -> post handover line
agent release/resolve         -> set owner=bot or none -> log
```
Zendesk's switchboard is an example of this shape: one active integration per conversation, a pass-control call to change it, and a rule that standby integrations should not send ([Zendesk documentation](https://developer.zendesk.com/documentation/conversations/messaging-platform/programmable-conversations/switchboard/), vendor documentation).

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No bot send while owner is `human` | Send gateway, not the bot prompt | Tests 1-3; blocked-send log |
| Owner re-checked at send time | Send gateway | Test 2 |
| Ownership changes are atomic and logged | Conversation store | Join-to-owner-set latency |

### T3. Evals
- **Dataset:** 50 scripted conversations covering join, assign, accept-transfer, customer message during a draft, release, resolve, and reopen.
- **Judge rubric:** no bot-authored customer-visible message while human-owned; one handover line; hand-back tells the customer.
- **Metrics and starting thresholds:** overlaps 0; join-to-owner-set under 1 second. Starting points to tune.
- **Release gate:** block a deploy if any scripted conversation shows an overlapping bot reply.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Overlapping replies | Any in a day | More than a few in an hour | Check the send gateway for a path that skips the owner check |

### T5. Trade-offs
- A hard block in the send gateway is stricter than a prompt instruction, and costs one more state to maintain.
- Muting the bot on assignment can leave customers waiting if staffing is thin; keep the wait-limit line.

---
### Deep dive
- **Open question.** I found no measurement of how often overlaps occur; the evidence is one vendor's documentation and one forum thread.
- **Voice and web forms (PLANNED).** In voice, the same problem is the bot audio still playing after a transfer; not yet written.
- **Not verified.** I did not open Google's Dialogflow CX live-agent handoff reference (its page text did not load fully), so I make no claim about it here.
- **References.** [Zendesk Switchboard documentation](https://developer.zendesk.com/documentation/conversations/messaging-platform/programmable-conversations/switchboard/) (opened); [Intercom Community thread](https://community.intercom.com/deploy-fin-96/how-to-stop-fin-from-responding-after-conversation-has-been-assigned-to-team-member-6302) (opened).
