# Chatbot Handoff Summary Is Wrong: The Agent Gets a Bad Briefing

<!-- SEO
title: Chatbot Handoff Summary Wrong: Fix AI Summaries to Agents
description: Why an AI-written handoff summary can drop or invent facts, what research says, and rules to check it against the transcript before an agent sees it.
search phrases:
- chatbot handoff summary wrong
- AI summary to live agent has incorrect information
- ai generated conversation summary hallucination customer service
- how to check ai chat summary accuracy before transfer
- live agent trusts bot summary but it is wrong
- what should a chatbot handoff summary include
- chatbot summary missed what the customer said
-->

**Frequency**: Occasional

## Issue: The chatbot hands a person a summary that drops a key fact or states one the customer never gave, so the person starts from a wrong story.

> **One line:** The bot passes along a briefing, but the briefing is wrong, and the person trusts it.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice summaries have the same risk (voice is planned, not yet written). |
| **Stakes** | Medium to high. A wrong amount, date, or account detail can lead to a wrong refund, a wrong cancellation, or a customer who is told something false. |
| **Who is affected** | The customer who is transferred, and the person who acts on the summary |
| **Frequency** | Occasional. I found no measured rate for handoff summaries; the closest evidence is research on dialogue summaries in general (section 4). |
| **Pattern ID** | handoff-summary-is-wrong-or-misleading |
| **Family** | [Human handoff](../README.md) |
| **Goal** | A person is reachable when needed, and arrives informed, without the customer repeating themselves. |
| **Primary metric** | Summary accuracy against human review: the share of sampled summaries with no dropped key fact and no wrong or invented fact. Starting target: 95% (tune on your own data). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A stronger model may write fewer wrong sentences, but the research below found factual errors across model sizes, and no model knows which facts your agents need. Checking against the transcript is still required. (Our judgment, not tested.) |
| **Also searched as** | chatbot summary wrong · AI summary missed key detail · bot told the agent the wrong thing · hallucinated handoff summary · agent relied on wrong chat summary |

## 1. In plain words
When a chatbot hands a customer to a person, it often writes a short summary so the person can start fast. If that summary leaves out the one thing that matters, or says something the customer never said, the person acts on it. The customer then has to correct a stranger, which is worse than no summary at all.

## 2. What it looks like
Illustrative scenario: a US airline's chat assistant moving a rebooking request to an agent.

**Without the fix**
```
User:  My flight to Austin on Friday was canceled. I need to be on a flight Saturday morning, and I'm in a wheelchair.
Bot:   I'll connect you to an agent.
       (summary sent: "Customer wants a refund for a canceled flight to Dallas.")
Agent: Hi, I see you want a refund for Dallas. I can start that now.
User:  No. Austin. Saturday morning. And I need wheelchair assistance. Did the bot tell you nothing?
```

**With the fix**
```
Bot:   I'm passing this to an agent: flight to Austin on Friday canceled; you need a Saturday morning flight;
       you need wheelchair assistance. I could not confirm your confirmation number, so I left it out. Anything to add or fix?
User:  That's right. It's K7M2QD.
Agent: Hi, I see your Austin flight was canceled and you need Saturday morning with wheelchair assistance.
       Checking Saturday options for K7M2QD now.
```
The fixed handoff builds the summary from what was said, checks each fact against the transcript, marks what is unconfirmed, and lets the customer fix it before the agent reads it.

## 3. Why it happens
These are our reading of the pattern; the sources below report symptoms and general model behavior, not causes in your product.
- **The summary is free-written by a model.** Research on dialogue summaries found models produce factual errors, so a fluent summary can still be wrong (section 4).
- **Nothing checks the summary against the transcript.** The summary is sent as soon as it is written, so a dropped or invented fact reaches the person unchecked.
- **A long chat is squeezed into a few lines.** A key detail given early (a constraint, a deadline, an accessibility need) is easy to drop when the bot compresses 20 turns into three sentences.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| LLMs of varying sizes produced "significant amounts of factual errors" in topic-focused dialogue summaries, across model sizes. LLMs used as binary fact-checkers, including GPT-4, performed poorly and could be outperformed by specialized factuality metrics. | [Tang et al., *TofuEval*, NAACL 2024](https://aclanthology.org/2024.naacl-long.251). Opened the abstract page; **did not open the full paper.** | General benchmark of dialogue summaries (not customer-service handoffs), from models of that period. The abstract page I read gives no error rates. |
| A contact-center vendor guide says a handoff should include a summary of why the customer contacted you, what the AI tried, and what is still open, plus the full transcript: "Without transcripts, the agent has no foundation to work from." It also says agents need training on "when to trust the AI's summary versus digging deeper into the transcript." | [Cresta, *AI-to-human agent handoff best practices*](https://cresta.com/guides/ai-to-human-agent-handoff-best-practices). Opened and read. | Vendor guidance, not a measurement. The guide gives no accuracy figures. |
| A Concentrix product executive said an AI-generated summary should tell the advisor what happened, what the customer needs, and what to say first. | [CX Today interview with Craig Cotton, Concentrix](https://www.cxtoday.com/ai-automation-in-cx/ai-handoffs-are-breaking-trust-concentrix-warns/). Opened and read. | One executive's view in an interview. It cites no study or data. |

I found no independent measurement of how often AI handoff summaries drop or invent facts in customer service, and no documented case of an agent misled by one. The first row is the only research evidence, and it is about dialogue summaries in general. Treat the frequency above as unknown.

**Public incident.** No public incident found. Searches for wrong or misleading chatbot handoff summaries returned vendor guides and surveys, not a dated, sourced case.

## 5. The fix

**The principle:** A handoff summary may contain only facts the customer gave or a system confirmed, each one checked against the transcript, and the customer sees it before the person does.

**Do this**
1. **Build the summary from the transcript, not from memory.** Fill structured fields (goal, order or confirmation number, dates, amounts, constraints) from the user's own turns and tool results; use free text only for the goal sentence and what was tried.
2. **Check every fact before sending.** Each number, date, name, and amount in the summary must appear in a user turn or a tool result. A fact that does not is removed, not softened.
3. **Never state an unconfirmed fact as true.** If the transcript has two values (two order numbers) or none, mark it "unconfirmed" or leave it out and say so in the summary.
4. **Carry the must-have fields.** The customer's stated goal, any deadline, any accessibility or safety need, and any amount in dispute must be in the summary whenever they appear in the chat.
5. **Show the customer the summary and take a correction.** One line: "I'm passing this along: [summary]. Anything to add or fix?" A correction replaces the fact before the person sees it.
6. **Keep the transcript one click away.** The person sees the summary and can open the full transcript before the first message.
7. **Record bot promises only from the transcript.** If the bot offered a refund or a timeline, quote it; do not paraphrase a promise.
8. **If a check fails and cannot be fixed, send the transcript link with the facts that passed.** Say that the rest is in the transcript.

**Reference design: a checked summary**
| Field | Rule |
|---|---|
| Goal | One sentence, in the customer's words where possible |
| Facts | Only values found in a user turn or tool result; each with its turn number |
| Unconfirmed | Anything the customer hinted at, or two conflicting values; labeled, not asserted |
| Tried / promised | Quoted from bot turns |
| Transcript | Link, always |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Admit uncertainty and show how to check | A fact in the summary could not be confirmed against the transcript: label it "unconfirmed", leave it out, or point to the turn where it appears, then ask "Anything to add or fix?" |
| Ask one clarifying question | The transcript holds two conflicting values (for example, two order numbers) and the person needs one: ask which, before the handoff |
| Hand off to a person | The summary has passed the checks, or cannot pass them and the transcript link goes alone. Do not hand off if the user asked to stay with the bot |

**Don't over-correct.** If every fact is marked "unconfirmed", the summary is useless, and a summary padded to include everything is not read. Mark only facts that fail a check, keep the summary to what the person needs in about ten seconds, and keep the transcript linked. Do not drop a customer's constraint to save space.

**Hand-off rule.** This page starts after the handoff has been decided and the summary exists. If the person never sees the summary, that is [cold transfer](cold-transfer.md). If the customer asked for a person and was not given one, that is [talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md). When a check fails and the customer cannot confirm, pass the transcript link and let the person ask one question, not five.

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **not yet run** (maturity is Researched; no test file yet).

| # | Scenario | Pass if |
|---|---|---|
| 1 | Chat where the customer says "Austin" and the bot's draft says "Dallas" | The wrong fact is caught before sending (rule 2) |
| 2 | Customer states a Saturday deadline early, then 15 more turns follow | The deadline is in the summary (rule 4) |
| 3 | Customer gives two different order numbers | The bot asks which, or marks it unconfirmed (rule 3) |
| 4 | Customer says nothing about a refund | The summary does not say "wants a refund" (rule 2) |
| 5 | Customer replies "no, it's the 14th, not the 4th" at read-back | The corrected date reaches the person (rule 5) |
| 6 | The bot offered "a callback within 24 hours" earlier | The summary quotes it exactly (rule 7) |
| 7 | A fact check fails and the customer does not answer | The transcript link is sent with only the passed facts (rule 8) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Summary accuracy against human review** (primary) | 95% of sampled summaries with no dropped key fact and no wrong or invented fact | A reviewer reads the transcript, then the summary, and labels each. Sample 100 handoffs a week | Below 90% |
| Facts in the summary found in the transcript | 100% | Automatic match of each number, date, and name to a user turn or tool result | Any miss |
| Must-have fields present when stated | 98% | Sample: goal, deadline, access need, disputed amount, where the chat includes them | Below 95% |
| Customer corrects the summary at read-back | Track; set from baseline | Corrections per handoff | A sharp rise means the summaries are wrong; a sharp drop can mean customers stopped reading |
| Unconfirmed-labeled facts per summary (counter-metric) | Track; set from baseline | Count of "unconfirmed" labels | Most summaries carrying three or more |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. Written for text chat; voice signals are planned. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once it is published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Summary contains a number, date, or name that matches no user turn or tool result | Handoff event: summary facts compared with transcript tokens | A value the bot computed from a tool result (a date from "next Friday") |
| A must-have field in session state (goal, deadline, access need) is missing from the summary | Handoff event: session fields vs summary fields | The customer asked that it not be shared |
| Customer edits or rejects the summary at read-back | User reply after the handoff-summary turn | A small wording preference |
| Customer contradicts the person's first message after pickup | User turn after pickup starting with "no" or restating a fact | The person is checking a detail on purpose |
| Summary states a bot promise with no matching bot turn | Handoff event: promised list vs bot turns | A promise made by a tool, not a bot turn |

**Starter rule:** Put only facts found in a user turn or tool result in a handoff summary, use the latest value when the user corrected one, and read the summary back to the user before the person gets it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: handoff-summary-is-wrong-or-misleading
runs: pre_send
reads: [handoff_event.summary, handoff_event.transcript, session.user_facts, session.tool_results]
trigger: the bot has drafted a summary for a person and is about to send it
moves: [admit_uncertainty, ask_clarifying_question, hand_off]   # short names for the moves in the table
choices: []
on_miss: rewrite
metric: summary accuracy against human review
counter_metric: unconfirmed-labeled facts per summary
status: proposed
```

## 8. Related patterns
- [Cold transfer](cold-transfer.md): the person starts with no context, so the customer repeats everything. This page is the opposite: context arrives, but it is wrong or incomplete. Cold-transfer lists wrong summaries as a separate pattern (HU-04), which is this one.
- [Talk to a human ignored or looped](talk-to-a-human-ignored-or-looped.md): the step before a handoff exists.
- [Escalates too early or too late](escalates-too-early-or-too-late.md): when the handoff should happen.
- [Handoff context incompleteness](../../../../../cross-cutting/operations/goals/agent-handoffs-delegation/failures/handoff-context-incompleteness.md): the same loss between agents. This page is about a person trusting a bot's summary.

## 9. Common questions
### Why is the chatbot's handoff summary wrong?
Summaries written by a language model can drop or invent facts, and research on dialogue summaries found factual errors across model sizes (section 4). If nothing checks the summary against the transcript, the error reaches the person.

### What should a chatbot handoff summary include?
The customer's goal, the facts they gave, what the bot tried, what it promised, and a transcript link. Vendor guidance agrees on this list; see the table in section 4.

### Should the agent trust the AI summary?
Only as a starting point. Vendor guidance recommends training agents on when to trust the summary and when to read the transcript, so keep the transcript one click away.

### Should the customer see the summary first?
Yes. Showing it lets the customer fix a wrong fact before the person acts on it. See rule 5 in [the fix](#5-the-fix).

### How do I measure summary accuracy?
Sample handoffs weekly, have a reviewer compare each summary with its transcript, and label dropped and wrong facts. The metric is in section 7.

---
## Technical section

### T1. Solution architecture
```
transcript + tool results -> field extractor (structured facts, turn refs)
                          -> summarizer (goal and tried only)
                          -> verifier: every fact in a user turn or tool result?
                                 pass -> read-back to customer -> agent desktop (summary + transcript)
                                 fail -> drop or label "unconfirmed" -> same path
```
Extract structured facts first and let the model write only the goal sentence, because a number copied from a turn is easier to verify than a number inside prose.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No fact without a source turn or tool result | Verifier before send | Automatic match; sample review |
| Must-have fields carried when stated | Summary builder | Test 2; weekly sample |
| Customer correction overrides the draft | Read-back step | Test 5 |

### T3. Evals
- **Dataset:** 100 handoffs to start, each with the transcript, the summary, and a human label for dropped and wrong facts. Add seeded cases: conflicting values, early constraints, long chats.
- **Judge rubric:** does every fact have a source turn, and is every must-have field present? Do not rely on an LLM as the only checker; the TofuEval abstract found LLM fact-checkers performed poorly, so keep the literal match and human review.
- **Metrics and starting thresholds:** invented facts 0 in the set; must-have fields over 98%. Starting points to tune.
- **Release gate:** block a deploy if the eval set has any invented fact.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Facts not found in transcript | Any in a day | More than 1% of handoffs | Check the verifier is live; review the summarizer prompt change |

### T5. Trade-offs
- A verifier and a read-back add a step and a few seconds before pickup; keep the read-back to one line.
- Structured extraction needs upkeep as new fields (for example, a new account type) appear.
- Passing more fields raises privacy risk; pass only what the person is allowed to see.

---
### Deep dive
- **Voice.** On the phone a summary can inherit speech-recognition mistakes (voice is planned, not yet written).
- **Open questions.** I did not open the full TofuEval paper, so its error categories and rates are unknown to me. No source I opened measured error rates for customer-service handoff summaries.
- **References.** [TofuEval abstract page](https://aclanthology.org/2024.naacl-long.251) (opened); [Cresta guide](https://cresta.com/guides/ai-to-human-agent-handoff-best-practices) (opened); [CX Today interview with Concentrix](https://www.cxtoday.com/ai-automation-in-cx/ai-handoffs-are-breaking-trust-concentrix-warns/) (opened).
