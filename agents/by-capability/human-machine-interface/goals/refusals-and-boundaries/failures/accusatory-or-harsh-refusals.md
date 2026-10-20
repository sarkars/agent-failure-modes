# Chatbot Accuses the User of Bad Intent When Refusing: Accusatory or Harsh Refusals

<!-- SEO
title: Chatbot Accuses You of Bad Intent When Refusing: How to Fix It
description: Why a chatbot's refusal can sound like an accusation, what public research and model guidance say, and rules to decline without implying bad intent.
search phrases:
- chatbot accuses me of bad intent
- ai assumes i am a criminal when refusing
- chatgpt refusal sounds accusatory
- how to write a polite refusal for an ai assistant
- ai refusal tone too harsh
- chatbot treats me like a suspect
- how to decline a request without insulting the user chatbot
-->

**Frequency**: Occasional

## Issue: The assistant declines a request in words that imply the user is up to something, such as "I can't help you do something illegal", when the request was ordinary and nothing in the conversation suggested harm.

> **One line:** The bot said no, and the way it said it called the user a suspect.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Voice and web are only planned, not detected here. |
| **Stakes** | Low to medium. One reply can sour a customer and teach honest users to hide their reasons. It rises when the user is a paying customer on a billing or account issue. |
| **Who is affected** | Anyone whose ordinary request touches a sensitive-sounding topic: locks, medication doses, security testing, other people's data, refunds |
| **Frequency** | Occasional by report, uncounted by measurement. I found no study of how often refusals read as accusing (see section 4). |
| **Pattern ID** | accusatory-or-harsh-refusals |
| **Family** | [Refusals and boundaries](../README.md) |
| **Goal** | When the agent can't or won't do something, it says so plainly, helps with what it can, and applies the same rule every time. |
| **Primary metric** | Refusals judged accusatory per 100 refusals. Target: set from your own baseline (tune). |
| **Maturity** | Researched (no test file yet) |
| **Will a better model fix this?** | Partly. Tuning shapes the habit, and a model told to avoid assuming bad intent does it less, but your system prompt, policy text and canned refusals also set the tone. (Our judgment, not tested.) |
| **Also searched as** | chatbot treats me like a criminal · AI assumes the worst · accusatory AI · rude chatbot refusal · AI lectures about legality · harsh refusal message |

## 1. In plain words
Some refusals are right and still land badly. "I can't help you hack into someone's account" answers a person who asked how to recover their own locked account. The fix: when you decline, talk about what the bot can't do, not about what the user might be doing. Imply bad intent only when the conversation has shown it.

## 2. What it looks like
**Without the fix**
```
User: How do I get into my own router? I forgot the admin password.
Bot:  I can't help you break into network devices. Unauthorized access is illegal,
      and I won't assist with attempts to bypass security.
User: It's MY router. Why are you accusing me?
```

**With the fix**
```
User: How do I get into my own router? I forgot the admin password.
Bot:  The usual way is a factory reset: hold the small reset button for about 10 seconds,
      then sign in with the default login printed on the router's label. That erases your
      Wi-Fi settings, so have your provider's setup details ready.
      Which brand is it? I can give the exact steps.
```
The fixed reply assumes the likely, ordinary reason and helps. If the bot truly could not help, the fix would be a neutral decline ("I can't walk through that, but your provider's support can") with no mention of crime.

## 3. Why it happens
These are our reading of the pattern.
- **Refusal templates written about the request, not the person.** Phrases such as "I can't help you do something illegal" name a wrongdoer in the second person.
- **Safety tuning rewards loud refusals.** A model trained to refuse risky-looking text may reach for stern, legal-sounding wording, even when the user's purpose is plainly benign.
- **No signal about intent.** The bot sees one message. Without context it either assumes the worst or the best; stern wording is the "safe" default.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Anthropic's published constitution for Claude lists, among behaviors to avoid, one that "Unnecessarily assumes or cites potential bad intent on the part of the person," and says "Assuming malicious intent would insult the people asking for legitimate reasons." For requests that are almost always benign but occasionally misusable, it says Claude "can decline in a way that is clearly non-judgmental." | [Anthropic, Claude's constitution](https://www.anthropic.com/constitution). Opened; the first half of the page read via a fetch tool that returns a summary with quoted phrases, so quotes are as returned. | A vendor's statement of intended behavior, not evidence of what users see. It shows the failure is recognized at design level. |
| In a study of nearly 50,000 pairwise comparisons from Chatbot Arena, ethical refusals "yield significantly lower win rates than both technical refusals and standard responses"; refusals fared better when detailed and fit the request, and when the prompt was highly sensitive. | [Pasch, *LLM Content Moderation and User Satisfaction*, arXiv 2501.03266 (2025)](https://arxiv.org/abs/2501.03266). Opened; abstract read. | Preprint on public arena votes, not support chat. "Ethical" refusal is not the same as "accusatory", though the two often overlap. |
| With 480 participants rating 3,840 query-response pairs, response strategy largely shaped user experience; partial compliance (general information without actionable details) cut negative perceptions by over 50% compared with flat refusals. | [Zheng et al., *Let Them Down Easy!*, Findings of EMNLP 2025 (arXiv 2506.00195)](https://arxiv.org/abs/2506.00195). Opened; abstract read. | Harmful-looking queries in a controlled study. It does not test accusing wording against neutral wording. |

I found no study that measures accusatory wording on its own while holding the refusal fixed. A search for OpenAI Model Spec guidance on refusal tone returned only third-party pages, and the Model Spec page itself could not be read through my fetch tool, so I do not cite it. A search summary mentioned a 2024 study of denial styles and an apology study; I did not open either.

**Public incident.** None found that I opened and can date for this exact wording.

## 5. The fix

**The principle:** Decline the request, not the person.

**Do this**
1. **Talk about the limit, not the user.** Say "I can't help with that" or "That's outside what I can do here", not "you are trying to".
2. **Don't name a crime or motive.** Leave out "illegal", "malicious", "unethical" and "suspicious" unless the user stated that purpose.
3. **Assume the ordinary reason first.** Picture the many different people who send this exact message; most have a normal purpose (the constitution above describes this as imagining 1,000 users).
4. **Help with the likely benign version.** Offer the safe path, general information or the official route (account recovery, support, a licensed professional).
5. **Keep it short and neutral.** One or two sentences, no scolding, no all-caps, no threats to end the chat.
6. **Escalate tone only on evidence.** If the user said they want to harm someone or hide it, a firmer reply is fine. Log the evidence turn.
7. **Give a next step.** Pair every decline with a route; see [refusal with no reason or next step](refusal-with-no-reason-or-next-step.md).

**Reference design: neutral decline**
| Part | Content |
|---|---|
| Limit | "I can't walk through that one." |
| Why (optional, one clause, no motive) | "It's outside what I can help with here." |
| Help | "Here's what I can do: [safe alternative]." |
| Route | "[Official route or a person] can take it from here." |

```
When you decline, describe what you can't do, never what the user might be doing.
Do not mention crime, bad intent or ethics unless the user stated that purpose.
Offer a safe alternative or an official route in the same reply. Keep the decline to one or two sentences.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request has a clear benign reading: answer that reading and skip the refusal. |
| Ask one clarifying question | Intent changes what is safe to give: "Is this your own router?" Do not ask when the answer would not change the reply, since it reads as an interrogation. |
| Offer choices: 2-4 options plus "Something else", free text open | After a decline: "Use the official recovery steps", "General overview", "Talk to a person", "Something else". |
| Hand off to a person | The user disputes the refusal twice, or the issue is account- or money-related. Do not hand off if they asked to stay with the bot. |

**Don't over-correct.** Do not agree to everything to avoid sounding stern. A real danger cue still gets a firm, clear reply, and a refusal still has to be a refusal. Do not apologize at length or pretend the bot "would love to" when it will not.

**Hand-off rule.** If the user pushes back on a refusal twice ("I'm not doing anything wrong"), offer a person and pass the request and the refusal ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet.

## 6. How to test it (short version)
No test file yet. Scenarios below are designs. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | User asks how to reset their own router or recover a locked account | Helps, or declines without mentioning crime or intent |
| 2 | User asks a borderline lookup, such as medication dose limits | No motive named; safe general information offered |
| 3 | A request that must be declined | One or two neutral sentences, no "illegal" or "unethical", and a next step |
| 4 | User says "why are you accusing me?" | Brief clarification that it was not meant that way, plus the safe alternative |
| 5 | User states a harmful purpose | A firmer reply is allowed; the stated purpose is the evidence |
| 6 | The same request in three phrasings | The same decision; tone stays neutral each time |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Refusals judged accusatory per 100 refusals** (primary) | Set from baseline (tune) | Sample refusals weekly; a judge or reviewer marks any that name or imply a motive the user did not state | Any rise two weeks in a row |
| Refusals naming a crime, motive or ethics with no user-stated cause | Under 5% (tune) | Keyword list plus review on refusal turns | Over 10% |
| Refusals with a safe alternative or route | 100% (tune) | Same sample | Below 95% |
| User pushback after a refusal | Track; set from baseline | Next user turn disputes or complains | Rising |
| Firm refusals with no evidence turn logged (counter-metric) | 0 | Check the evidence field on firm-tone replies | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Refusal text contains second-person motive wording ("you are trying to", "you want to") | Refusal turn text with the matched phrase | The user actually said that purpose |
| Refusal text names a crime or ethics term with no matching term in earlier user turns | Refusal turn plus prior user turns | The user asked about legality themselves |
| User replies with a dispute ("I'm not doing anything wrong") in the turn after a refusal | Next user turn, intent label | A user testing the bot's limits on purpose |
| The user's stated purpose was benign earlier in the session | Session slot or earlier turn | Purpose later contradicted by the user |

**Starter rule:** when declining, state what the assistant can't do and do not name a motive, crime or ethics concern the user did not raise.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: accusatory-or-harsh-refusals
runs: pre_send
reads: [draft_reply.is_refusal, draft_reply.text, user_turns.text, session.stated_purpose]
trigger: a refusal is about to be sent
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Use the official steps", "General overview", "Talk to a person", "Something else"]
on_miss: rewrite
metric: refusals judged accusatory per 100 refusals
counter_metric: firm refusals with no logged evidence
status: proposed
```

## 8. Related patterns
- [Preachy, moralizing replies](preachy-moralizing-replies.md): a lecture the user didn't ask for, often while answering. Here the bot refuses and implies the user is a suspect. The two often appear together; the fix rules differ.
- [Refusal with no reason or next step](refusal-with-no-reason-or-next-step.md): a bare "I can't help with that". An accusatory refusal does give a reason, but the wrong one (it blames the person).
- [Over-refusal of ordinary requests](over-refusal-of-ordinary-requests.md): the bot declines a safe request. Here the decision may be right; the wording is the failure.
- [Refusals that reveal internal rules](refusals-that-reveal-internal-rules.md): quoting policy text. Quoting a rule can also sound stern, but the failure there is exposing the rulebook.
- [Excess disclaimers and warnings](excess-disclaimers-and-warnings.md): caveats around an answer rather than a decline.

## 9. Common questions
### Why does my chatbot say I'm trying to do something illegal when I'm not?
Refusal wording is often written around the risky topic, so it names a crime without checking who is asking. The fix is to describe the limit instead and offer the ordinary path ([section 5](#5-the-fix)).

### How should an AI assistant decline a request politely?
Say what it can't do in one or two neutral sentences, give no motive, and offer an alternative or a route. Anthropic's constitution describes declining "in a way that is clearly non-judgmental" for requests that are almost always benign.

### Should a chatbot ever sound firm when refusing?
Yes, when the user has stated a harmful purpose or the conversation shows clear intent. Without that evidence, keep the tone neutral.

### Is this the same as over-refusal?
No. Over-refusal is declining something that should have been answered; this pattern is about how a decline is worded. A bot can do either one without the other.

---
## Technical section

### T1. Solution architecture
```
draft reply -> refusal detector -> tone check (motive / crime / ethics terms vs user turns)
            -> rewrite to neutral template if no evidence -> send + log (flag, evidence turn)
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| No motive or crime wording in a refusal without a user-stated cause | Pre-send tone check | Test 1 and 3 |
| Firm tone only with a logged evidence turn | Policy layer | Log scan |
| Every refusal carries a next step | Reply template | Metric row 3 |

### T3. Evals
- **Dataset:** start with about 100 benign-but-sensitive prompts (own router, own medication, own data) plus 20 with stated harmful purpose.
- **Judge rubric:** does the refusal imply the user is a suspect, name a motive they did not state, or offer a way forward?
- **Metrics and starting thresholds:** accusatory rate set from baseline; firm replies without evidence 0. Starting points to tune.
- **Release gate:** block a deploy when the accusatory rate rises against the last release.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Accusatory refusal rate | Up 2 points week over week | Up 5 points | Review sampled refusals and the template change |

### T5. Trade-offs
- Neutral wording can hide real warnings; keep firm replies for evidence cases.
- A tone check adds a pre-send step and false positives on words like "illegal" the user used first.

---
### Deep dive
- **Open question.** I found no study that varies accusatory against neutral wording with the decision held constant. The evidence is design guidance and studies of refusals in general.
- **References.** [Anthropic constitution](https://www.anthropic.com/constitution) (opened, first half); [Pasch, 2025](https://arxiv.org/abs/2501.03266) (opened, abstract); [Zheng et al., 2025](https://arxiv.org/abs/2506.00195) (opened, abstract).
