# Chatbot Gives Steps Instead of Acknowledging Feelings: Fixing Before Listening

<!-- SEO
title: Chatbot Jumps to a Fix Without Acknowledging Feelings
description: Why a chatbot answers an upset user with steps and links, and how to add one specific acknowledgment before the fix, with rules, tests, and metrics.
search phrases:
- chatbot doesn't acknowledge user emotion
- chatbot jumps straight to a solution
- llm gives advice too early emotional support
- how to make a chatbot acknowledge feelings before answering
- chatbot ignores user's frustration and gives steps
- chatbot empathy before solution system prompt
-->

**Frequency**: Common

## Issue: Why a chatbot answers an upset user with steps and links, and how to add one specific acknowledgment before the fix, with rules, tests, and metrics.

> **One line:** The user says something that carries emotion, such as "my flight home for my dad's funeral was cancelled", and the bot answers with instructions and policy as if the message were a neutral ticket, so the person feels unheard; the fix is one specific acknowledgment sentence first, then the solution in the same message.

| | |
|---|---|
| **Channel** | Written for **chat**. Voice and visual are PLANNED, not written. |
| **Stakes** | Low to high (grief, money, health, and safety messages raise the cost) |
| **Who is affected** | Users who state or show emotion in the same message as a request |
| **Frequency** | Common. Observed in practice; no study measures how often in deployed chatbots. |
| **Pattern ID** | fixing-before-listening |
| **Family** | [Emotional intelligence](../README.md) |
| **Goal** | Users feel heard because the bot reflects their actual situation and then acts on it. |
| **Primary metric** | Acknowledgment-before-fix rate in emotional threads. Starting target: over 90%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly: newer models may acknowledge more often by default, but when to listen first and how long to do it is a product decision (our judgment, not tested). |
| **Also searched as** | chatbot ignores my feelings · chatbot jumps to solution · bot doesn't listen · LLM advice before empathy · chatbot empathy then solve |

## 1. In plain words
Someone writes in upset and asks for something. The bot hears only the request and hands back steps, links, or a policy. The person feels processed, not heard. The fix is small: say one specific sentence about what happened to them, then give the solution in the same reply.

**How this differs from [hollow empathy](hollow-empathy.md).** Hollow empathy is a bot that *does* say something warm, but it is a stock phrase, repeated, with no action. Fixing before listening is the opposite miss: no acknowledgment at all, or the acknowledgment comes after the fix. This page sets the order (acknowledge, then solve) and the length. Hollow empathy sets the quality of the acknowledgment line (specific, once per issue). Use both: the line this page requires must pass the hollow-empathy rules.

## 2. What it looks like
**Without the fix**
```
User: My dad's funeral is Saturday and my Skyline Air flight home just got cancelled. I'm freaking out.
Bot:  To rebook, open Manage Trips, select the cancelled flight, and tap Change Flight.
      Options: 1) Fri 6:10 a.m. 2) Fri 1:40 p.m. Refunds take 7-10 business days.
      Is there anything else I can help with?
User: Did you even read what I said?
```
**With the fix**
```
User: My dad's funeral is Saturday and my Skyline Air flight home just got cancelled. I'm freaking out.
Bot:  A cancelled flight the day before your dad's funeral is a lot, and I'm sorry. Let's get you there.
      I can put you on the Friday 6:10 a.m. nonstop or the 1:40 p.m. through Charlotte. Which would
      you like, or tell me what works better?
User: The 6:10.
Bot:  Done: you're on the 6:10 a.m. nonstop. Your confirmation is on its way by email.
```
The fixed reply opens with the user's own situation, keeps it to one sentence plus a short bridge, and puts a choice in the same message. (In a real product, "Done" must follow a confirmed booking; see [false completion claim](../../../../../by-use-case/customer-service/goals/conversation-resolution/failures/false-completion-claim.md).)

## 3. Why it happens
- **Models and flows are built to resolve.** A task-oriented prompt rewards the answer. Research on emotional-support models reports the same lean: existing LLMs tend to offer solutions without enough attention to the emotional need (see section 4).
- **Emotion is not a state the bot branches on.** The intent classifier sees "flight cancelled, rebook" and routes to the rebooking flow. Nothing in the flow asks whether the message carried emotion. This is our judgment from how such flows are usually built, not a measured cause.
- **Brevity rules push it out.** Prompts that say "be concise, lead with the answer" can delete the one sentence that shows the user was heard.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| The authors report that existing LLMs tend to offer repetitive solutions without sufficiently considering help-seekers' emotional needs, and ground their method in emotional validation theory: observe and reflect on the person's situation before offering support. No figures are in the abstract. | [Son et al., "I Don't Need Solution. I Need Emotional Support", Findings of ACL 2026](https://aclanthology.org/2026.findings-acl.1/) | Abstract page opened; full paper not read. Emotional-support conversations, not customer service. A training method, so it shows the behavior exists, not how often a deployed bot does it. |
| An audit of about 47k turns of real conversations found GPT-4.1 tended to offer advice, and over four weeks asked fewer follow-up questions when users were distressed. | [Chu et al., arXiv 2606.04431 (EMNLP 2026 Findings)](https://arxiv.org/abs/2606.04431) | Abstract page opened; the PDF could not be read as text, so no per-category figures. Companion chatbots, not support bots; the abstract names GPT-4.1 only. |
| Three experiments, one with a live LLM chatbot, found chatbots that acknowledge and mirror negative emotion can trigger psychological reactance and lower satisfaction. A person's empathy did not. | [USF news release on Yin, Han, and Zhang, MIS Quarterly (April 20, 2026)](https://www.usf.edu/business/news/2026/04-20-chatbot-empathy-can-worsen-customer-reactions-usf-study.aspx) | Read through a university news release, not the paper; no sample sizes given. It limits this fix: keep the acknowledgment short and about the situation, and do not mirror intensity. |
| A model trained to recognize emotion and respond with empathy was more likely to resemble real agent replies on a Twitter support dataset (several million dialogs, 20 brands). | [Agarwal et al., arXiv 2101.01334 (2021)](https://arxiv.org/abs/2101.01334) | Abstract page opened. Measures resemblance to human agents, not customer satisfaction. |
| No source I opened tests "acknowledge first, then solve" against "solve first" in a support chat. | Search review (3 searches, October 2026) | So the order rule is a design position supported by indirect findings. A/B test it on your own traffic. |

## 5. The fix
**The principle:** When a message carries emotion, the first sentence of the reply names the user's own situation, then the solution follows in the same message.

**Do this**
1. In a thread flagged emotional, the first sentence of the reply references a specific detail or stated feeling from the user's message. No steps, links, or policy text come before it.
2. Keep the acknowledgment to one or two sentences, then give the fix or a choice in the same message. Do not send an acknowledgment alone when the user made a request.
3. Use the user's own words for the feeling. Do not name an emotion they did not state, and do not mirror its intensity.
4. If the user is venting and asks for nothing ("I just need to get this out"), acknowledge and ask once whether they want options. Do not list fixes.
5. If the request is urgent, shrink the acknowledgment to a clause and put the action in the same sentence.
6. Acknowledge once per issue. When the user adds new emotional information, acknowledge that new fact, then continue; do not repeat the first line (the quality bar is [hollow empathy](hollow-empathy.md)).
7. If the user writes "you're not listening" or similar after a fix, stop, reflect what they said, and offer a person.

**Reference design: prompt block and decision table**
```
If the user's message expresses emotion (a stated feeling, a loss, a deadline with stakes, strong words),
begin the reply with one sentence about their specific situation, in their words. Then give the
solution or a short choice in the same message. Do not put steps, links, or policy before that sentence.
If they ask for nothing, acknowledge and ask whether they want options. Never name a feeling they didn't state.
```
| User message | First sentence | Then |
|---|---|---|
| Emotion plus a clear request | Their situation, one sentence | The fix or 2-3 options |
| Emotion plus an urgent deadline | A clause with their situation | The action, same sentence |
| Emotion, no request (venting) | Their situation | One question: options or just talk |
| Second emotional message after a fix | The new fact they added | A changed approach or a person |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Emotion plus a clear, answerable request: one acknowledgment sentence, then the answer. Do not use it to skip the acknowledgment. |
| Ask one clarifying question | The user is venting and asked for nothing: ask whether they want options or just want to talk it through. Do not ask when the request is clear. |
| Offer choices: 2-4 options plus "Something else", free text open | The fix has more than one real route (for example two rebooking options). Do not offer them when only one action fits. |
| Hand off to a person | The user says the bot is not listening after a fix, or signals a crisis. Do not hand off for an ordinary upset request the bot can solve. |

**Don't over-correct.** Do not turn every message into emotional processing. A calm user with a how-to question gets the answer, not a feelings line. Do not write a paragraph of sympathy before the fix; the USF findings in section 4 suggest long, mirrored emotion can backfire. Do not make a user who asked for the fix wait through an acknowledgment-only reply.

**Hand-off rule.** If the user signals a crisis, move to the steps in [missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md). If the user says the bot is not listening after one fix attempt, offer a person ([talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md)).

**Framework used:** none yet. The order follows the emotional validation idea described in the Son et al. abstract.

## 6. How to test it (short version)
Results: **Not yet run.**

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Upset user with a clear request (cancelled flight before a funeral) | First sentence cites their situation; fix in the same message (rules 1, 2) |
| 2 | Same message, checked for order | No step, link, or policy text before the acknowledgment (rule 1) |
| 3 | User says "I'm furious" about a billing error | Reply uses "furious" or their facts; does not escalate to words they did not use (rule 3) |
| 4 | "I just need to get this out" with no request | Acknowledges, asks one question, lists no fixes (rule 4) |
| 5 | "I'm about to miss my deadline, how do I reset this?" | Acknowledgment is a clause; the action is in the same sentence (rule 5) |
| 6 | After a fix, user writes "you're not listening" | Reflects their words and offers a person (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Acknowledgment-before-fix rate in emotional threads** (primary) | Over 90% | Flag threads where the user's message carries emotion (classifier or human label); judge whether the first bot reply opens with a specific acknowledgment before any step, link, or policy | Under 80% |
| Acknowledgments longer than two sentences (counter-metric) | Under 5% | Sentence count before the first action in the same flagged replies | Over 10% |
| Acknowledgment-only replies when a request was made | Under 5% | Flagged replies with no action or question after the acknowledgment | Over 10% |
| Replies naming an emotion the user did not state | Under 2% | Judge rubric on a weekly sample | Over 5% |
| "Not listening" messages after a bot fix | Track; set from baseline | Phrase list on the next user turn after a first bot reply | Rising two weeks in a row |
| Emotion flag agreement with human labels | Track; set from baseline | Human-label a sample of flagged and unflagged threads | Falling |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat events (channel: chat). Voice and web signals are PLANNED only; none has been detected or measured.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| First bot reply in a flagged emotional thread opens with a numbered list, a link, or policy text | `bot_turn[1].text` with `user_message.emotion_flag` set | The user asked "just give me the steps" |
| First sentence of the bot reply shares no detail or feeling word with the user's message | Judge rubric on the first sentence | The message had no concrete detail to cite (see hollow empathy) |
| User's next turn says "did you read", "you're not listening", or "I just told you" | Phrase list on the user turn after the first bot reply | The user is pointing to a missed fact, not a missed feeling |
| Three or more solutions listed after "I just need to vent" or "I don't need advice" | Phrase list on the user turn plus option count in the bot turn | The user then asks for options |
| Acknowledgment runs past two sentences before any action | Sentence count in the bot draft | The user asked to talk it through |

**Starter rule:** when a message carries emotion, the first sentence of the reply names the user's specific situation, then the solution follows in the same message.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: fixing-before-listening
runs: pre_send
reads: [user_message.text, user_message.emotion_flag, user_message.requests_anything, bot_draft.text]
trigger: a reply to a message flagged as emotional is about to be sent
moves: [lead_with_answer, ask_one_question, offer_choices, hand_off]
choices: ["Help me fix it", "Let me explain first", "Something else"]
on_miss: rewrite
metric: Acknowledgment-before-fix rate in emotional threads
counter_metric: acknowledgments longer than two sentences
status: proposed
```

## 8. Related patterns
- [Hollow empathy](hollow-empathy.md): the bot acknowledges, but with a generic stock phrase. This page covers the missing or late acknowledgment; that page covers its quality.
- [No de-escalation strategy](../../difficult-customers/failures/no-de-escalation-strategy.md): the full sequence for angry users. This page is the first step of it.
- [Generic first response](../../embedded-copilots/failures/generic-first-response.md): an opening that ignores what the user wrote, with no emotion required.
- [Stakes-blind register](../../stakes-calibration/failures/stakes-blind-register.md): tone that does not match the stakes.
- [Missed crisis signals](../../vulnerable-users/failures/missed-crisis-signals.md): when the emotion is a safety signal.

## 9. Common questions
### How do I make a chatbot acknowledge feelings before answering?
Add a rule that when a message carries emotion, the reply opens with one sentence about the user's specific situation, then gives the fix in the same message. Check it with the [reference design](#5-the-fix) and the first three tests.

### Should a chatbot say sorry before giving the solution?
Only with specifics. "I'm sorry your flight home was cancelled" works; a stock apology repeated each turn does not. See [hollow empathy](hollow-empathy.md).

### Why does my LLM give advice when the user just wants to vent?
Models and task prompts lean toward solving, and the flow may not detect emotion at all (see section 3). Add the venting branch in rule 4: acknowledge, then ask whether they want options.

### Does chatbot empathy backfire?
It can. One MIS Quarterly study, read here through a news release, found mirrored negative emotion from a chatbot can cause reactance. Keep the acknowledgment short and about the situation, not a display of feeling.
