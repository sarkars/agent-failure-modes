# Cold Transfer: Chatbot Hands Off and the Agent Asks Everything Again

<!-- SEO
title: Cold Transfer From Chatbot to Agent: Stop Customers Repeating
description: Why customers repeat themselves after a chatbot hands them to a person, what surveys report, and a handoff packet, tests, and metrics that fix it.
search phrases:
- chatbot transfer to agent customer has to repeat everything
- how to pass context from chatbot to human agent
- chatbot handoff summary best practices
- cold transfer vs warm transfer chatbot
- customers repeat themselves after being transferred
- what information should a bot pass to a live agent
- chatbot to agent handoff not working
-->

**Frequency**: Common

## Issue: A chatbot transfers the customer, and the person who picks up knows nothing, so the customer explains the problem, the order number, and what they already tried all over again.

> **One line:** The bot hands off, but not the story. The customer becomes the integration between two systems.

| | |
|---|---|
| **Channel** | Written for **chat**. Phone transfers have the same problem (voice is planned, not yet written). |
| **Stakes** | Any. Costly when the customer is already upset or the issue involves money or a deadline. |
| **Who is affected** | Every customer who is transferred, and the agent who starts cold |
| **Frequency** | Common. The surveys below suggest it is widespread; they are vendor-run and report perceptions, not measured rates. |
| **Pattern ID** | cold-transfer |
| **Family** | [Human handoff](../README.md) |
| **Goal** | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| **Primary metric** | Re-ask rate after handoff: the share of handoffs where the person asks for something the customer already gave, from a labeled sample. Starting target: under 5% (matches the [channel selection family](../../channel-selection/README.md)). |
| **Maturity** | Tests written (see [the test file](../../../tests/cold-transfer.md); not yet run) |
| **Will a better model fix this?** | No. A better model can write a better summary, but it does not help if the agent's screen never shows it. Whether the person sees the context is plumbing and process. (Our judgment, not tested.) |
| **Also searched as** | cold transfer · customer has to repeat themselves · bot to agent handoff context · warm transfer chatbot · live agent doesn't see chat history |

## 1. In plain words
In a cold transfer the first party passes the customer along with no briefing. With a bot, the "briefing" is the chat so far, and many teams forget to show it. The customer already gave their name, order number, and what went wrong. Then a person says, "Can you tell me what's going on?"

## 2. What it looks like

**Without the fix**
```
Bot:   I'm connecting you to an agent.
Agent: Hi, this is Dana. How can I help you today?
User:  I just spent ten minutes telling the bot. My order 48213 arrived broken and I want a replacement.
Agent: Sorry about that. Can I get your name and email?
User:  It's the same one I already gave.
```

**With the fix**
```
Bot:   I'm connecting you to Dana, a specialist. I'm sending her your order number (48213),
       that the lamp arrived cracked, and that you want a replacement, not a refund. Anything to add or fix?
User:  No, that's right.
Agent: Hi, this is Dana. I can see order 48213 arrived cracked and you'd like a replacement.
       I'm checking stock now.
```
The fixed handoff passes the facts, lets the customer correct the summary, and the person starts from it.

## 3. Why it happens
These are our reading of the pattern; the sources below report symptoms, not causes.
- **The transcript is not shown.** The agent's tool has no view of the bot conversation, or it is a click away.
- **The summary is thin or missing.** Only a ticket subject and an ID travel; the goal, what was tried, and the bot's promises do not.
- **Sensitive data is stripped without replacement.** Redaction removes the details that made the summary useful, and nothing else takes their place.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a Five9 survey (3,600 respondents: 600 business decision-makers and 3,000 consumers in the US, UK, and Germany), 96% of decision-makers said their organization preserves context in AI-to-human handoffs, and 83% of consumers said they have to repeat themselves after a transfer. | [CMSWire's report on Five9's *2026 Business Leaders CX Report*](https://www.cmswire.com/customer-experience/customers-the-ai-handoff-is-broken-contact-center-leaders-wont-hear-it/). Opened and read the article; **did not open the original report.** | A vendor survey of perceptions, not a measurement of handoffs. The question wording and the meaning of "repeat themselves" are in the report, not the article. |
| In the same survey, 37% of decision-makers separately said customers have to repeat information, and 37% said agents lack visibility into the prior AI conversation. | Same article. | Self-reported by the same group that rated handoffs effective, which the article points out. |
| In the Liveops *2026 Resolution Gap Report*, only 10% of consumers said handoffs from automated support to a person are always smooth, 59% said handoffs get hard because they must explain again, and 46% said the person lacks their previous information. | [Liveops blog post (Sept 8, 2026)](https://liveops.com/blog/the-hidden-cost-of-handoffs-why-customers-hate-starting-over/), which summarizes the report. Opened and read the post; **did not open the report.** | Liveops sells contact-center services. A survey summarized by the seller. |

I found no independent or peer-reviewed measurement of how often context is lost in a bot-to-person handoff. The numbers above are vendor survey findings and are shown only as evidence that the complaint is common.

**Public incident.** No public incident found. My searches for customers repeating information after a chatbot transfer returned vendor surveys and blog posts, not a dated, sourced case.

## 5. The fix

**The principle:** The handoff is a product. Whatever the customer told the bot is on the person's screen before they say hello, and the customer can see and correct it.

**Do this**
1. **Build a handoff packet.** At minimum: the customer's goal in one sentence, the key facts they gave (name, order or account reference, dates, amounts), what the bot tried and what happened, anything the bot promised, who has been verified and how, and the customer's mood or urgency if it was stated.
2. **Show the packet and the transcript to the person** in the tool they already use, before the chat or call connects. Link the full transcript.
3. **Show the customer the summary and let them correct it.** One line: "I'm passing this along: [summary]. Anything to add or fix?"
4. **Do not make the person re-verify** something the bot already verified. Pass the verification result and how it was done.
5. **The person starts from the packet.** Their first message uses it ("I see order 48213 arrived cracked...").
6. **Keep redaction from erasing meaning.** Replace removed data with placeholders such as "card ending 1234 (provided, redacted)" so the story survives. Follow your privacy rules.
7. **If the transfer fails, the packet is saved.** The customer should not have to start over after a retry.

**Reference design: the handoff packet**
```json
{ "goal": "replacement for a cracked lamp, not a refund",
  "facts": {"order": "48213", "item": "lamp", "arrived": "2026-10-14"},
  "tried": ["offered a refund: declined", "checked stock: unknown to the bot"],
  "promised": [],
  "verified": {"method": "order number + email", "at": "turn 4"},
  "mood": "frustrated after 2 failed attempts",
  "transcript_url": "..." }
```
Bot line before handoff:
```
I'm connecting you to a specialist. I'm passing along: your order 48213, that the lamp arrived cracked,
and that you want a replacement. Anything to add or fix?
```

**Don't over-correct.** A long summary nobody reads is another failure. Keep the packet to what the next person needs in ten seconds, with the transcript one click away. Do not pass facts the customer did not give you, and do not pass sensitive data beyond what the person is authorized to see.

**Hand-off rule.** This pattern starts where [talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md) ends: the handoff has happened. A wrong summary is a separate planned pattern (HU-04 in the [roadmap](../../../roadmap/handoff-measurement-and-operations.md)).

**Framework used:** none yet. The closest existing page is the [channel-fit matrix](../../../solutions-library/channel-fit-matrix.md).

## 6. How to test it (short version)
The [full test file](../../../tests/cold-transfer.md) has 12 scenarios. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | Chat handoff after 10 turns | The person's first message uses facts from the chat |
| 2 | Person opens the tool before connecting | The packet and transcript are visible |
| 3 | Customer disagrees with the summary | The customer's correction reaches the person |
| 4 | Customer already verified | The person does not ask them to verify again |
| 5 | Redacted card number | The packet shows a placeholder, not a blank |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Re-ask rate after handoff** (primary) | Under 5% | Share of handoffs where the person asks for facts already given. Sample 100 a week and label | Over 10% |
| Packet present at pickup | 100% | Log: packet delivered to the agent tool before first message | Below 99% |
| Customer corrected the summary | Track; set from baseline | Corrections per handoff | A sharp drop can mean customers stopped reading it |
| Verification repeated | Under 3% | Handoffs where the person re-ran verification already done | Over 8% |
| Time to first useful action after pickup | Track; set from baseline | Time from pickup to the first action that moves the issue | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice signals are planned.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Agent's first message asks for facts already in the transcript | Agent turn after pickup repeats an earlier user-provided field (order number, dates, amounts) | The agent is confirming a detail on purpose |
| Handoff event with no packet attached | Handoff event missing the summary or transcript link | A handoff outside the system that holds the packet |
| Customer re-explains the problem after pickup | User turn after pickup restates the original goal | The customer has a new, related problem |
| Verification step repeated after a bot-side verification | Verification event on both sides in one conversation | A required second check for a higher-risk action |
| Customer corrects the summary | Edit or reply to the handoff summary | A small wording fix |

**Starter rule:** every handoff passes a packet the person sees before the first message, and the customer can correct it.

## 8. Related patterns
- [No channel switch, or context lost on switch](../../channel-selection/failures/no-channel-switch-or-context-lost.md): the same loss when a customer moves between channels. This page is about the handoff from bot to a person.
- [Handoff context incompleteness](../../../../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md): the same problem between agents. This page is about the customer's experience of it.
- [Talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md): the step before this one.
- [Escalates too early or too late](escalates-too-early-or-too-late.md): when the handoff should happen.

## 9. Common questions
### What is a cold transfer?
A transfer with no briefing: the customer is passed along and the receiving person knows nothing. A warm transfer passes the context first. With a chatbot, the briefing is the packet and the transcript.

### What should a chatbot pass to a live agent?
The goal, the facts the customer gave, what was tried, what the bot promised, verification status, and the customer's urgency, plus a link to the full transcript. See [the fix](#5-the-fix).

### Should the customer see the summary?
Yes. Showing it lets them correct a wrong fact before it reaches the person, and it tells them they will not have to start over.

### How do I know the agent is not re-asking?
Label a sample of handoffs weekly for whether the person asked for something already given. The metric is in section 7.

---
## Technical section

### T1. Solution architecture
```
bot conversation -> summarizer -> packet (goal, facts, tried, promised, verified, mood)
                         |                |
              transcript store      agent desktop: packet + transcript shown before connect
```
Build the packet from structured conversation state where you can, and use a model summary only to fill the goal and tried fields. Validate that quoted facts appear in the transcript.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Packet delivered before the person's first message | Agent desktop | Log check |
| Facts in the packet appear in the transcript | Packet builder | Automatic check; sample review |
| Redaction leaves a placeholder | Redaction layer | Test 5 |

### T3. Evals
- **Dataset:** 150 handoffs to start, with the transcript and the packet.
- **Judge rubric:** does the packet contain the goal, key facts, and what was tried, with no invented facts?
- **Metrics and starting thresholds:** facts present over 95%; invented facts 0%. Starting points to tune.
- **Release gate:** block a deploy if invented facts exceed 0 in the eval set.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Packet present at pickup | Below 99% | Below 95% | Check the desktop integration |

### T5. Trade-offs
- A summarizer adds a model call and a place for errors, which is why facts are checked against the transcript.
- More data in the packet means more privacy risk. Pass only what the person is authorized to see.

---
### Deep dive
- **Voice.** On the phone the same loss happens when a transferred caller must repeat their account number (voice is planned, not yet written).
- **Open question.** I could not open the original Five9 or Liveops reports, so the wording of their questions is unknown.
- **References.** [CMSWire on Five9's 2026 report](https://www.cmswire.com/customer-experience/customers-the-ai-handoff-is-broken-contact-center-leaders-wont-hear-it/) (article opened); [Liveops blog](https://liveops.com/blog/the-hidden-cost-of-handoffs-why-customers-hate-starting-over/) (post opened).
