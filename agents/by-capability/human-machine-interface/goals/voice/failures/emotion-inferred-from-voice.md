# Chatbot Says "You Sound Angry": Emotion Inferred From Voice or Text

<!-- SEO
title: Chatbot Says "You Sound Angry": Fix Emotion Guessing
description: A bot that labels your mood ("you sound upset") and changes how it treats you, on a guess, gets it wrong. Use emotion signals only when accurate, disclosed, allowed.
search phrases:
- chatbot says you sound angry
- ai assistant guessed my emotion wrong
- chatbot emotion detection customer service problems
- how to use sentiment detection in a chatbot without annoying users
- emotion recognition voice assistant privacy
- chatbot treats me differently when I am frustrated
- should a chatbot tell users how they feel
-->

**Frequency**: Occasional

## Issue: A bot that guesses the user's emotion, says it out loud ("you sound angry") or quietly changes how it treats them, acts on a guess the user never confirmed and often cannot see.

> **One line:** The user types a short, blunt message and the bot answers "I can tell you're angry" or silently moves them into a "difficult customer" path. The fix is to treat an emotion guess as weak evidence: use it only to adjust tone or offer help, never to state a mood as fact or to change what the user gets, unless the signal is accurate, disclosed, and permitted.

> **Read this first.** This page is design guidance. It is not legal, clinical, or other professional advice. Have privacy counsel review it, and a qualified expert (for example a clinician for any health or crisis use) before you use it. I state a law only as far as I read it in a source I opened, listed at the end. Whether any law applies to your product is not settled here.

| | |
|---|---|
| **Channel** | Written for **chat** (inferring mood from the user's words). Voice-acoustic inference (pitch, pace, volume) is PLANNED; nothing here is measured on voice data. |
| **Stakes** | Medium to high. A wrong label insults the user or routes them badly; a hidden label can change price, queue, or help. |
| **Who is affected** | Any user the bot labels. Likely over-labeled: people who write tersely, use a second language, type in caps, or are being sarcastic. (Our judgment.) |
| **Frequency** | Occasional. Our judgment; I found no count. |
| **Pattern ID** | emotion-inferred-from-voice |
| **Family** | [Voice](../README.md) (roadmap row VO-22 in the [voice roadmap](../../../roadmap/voice.md)) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | False emotion-label rate. Starting target: under 5% of labels shown or acted on, judged by human review (starting point; tune). |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A better model labels more accurately, but the fixes that matter (disclosure, permission, not acting on a guess) are product rules. (Our judgment, not tested.) |
| **Also searched as** | chatbot says I sound angry · ai guessed my mood · emotion detection chatbot wrong · sentiment analysis customer service bot · voice emotion recognition privacy |

## 1. In plain words
Some bots try to read how the user feels. They may say it ("I can hear you're upset"), or they may say nothing and quietly route the user, change the offer, or shorten the help. A guess from a short message is often wrong, and the user is rarely told it happened. Use the guess only to soften tone or offer help, and say so when it changes anything real.

## 2. What it looks like
*(Illustrative; "Lakeview Internet" is a made-up cable company.)*

**Without the fix**
```
User: Third time I'm asking. Is my outage fixed. Yes or no.
Bot:  I can tell you're really angry, and I'm sorry you feel that way. Let me calm things down for you.
User: I'm not angry, I'm busy. Is it fixed?
Bot:  I understand your frustration. Please stay calm while I connect you to our retention team.
      (log: emotion=angry, 0.81; user moved to the retention queue, outage status never given)
```
**With the fix**
```
User: Third time I'm asking. Is my outage fixed. Yes or no.
Bot:  Not yet. The repair crew is due by 6 p.m. tonight, and I'll text you when it's done. Want a $10 credit for the downtime?
      (log: tone=brief; no mood label said or stored; same queue and offers as any user)
```
The fixed bot answered the question first, kept the reply short because the user was brief, and said nothing about the user's mood.

## 3. Why it happens
- **Sentiment is cheap to add and easy to over-trust.** A classifier or a prompt line ("detect the user's emotion") returns a label with a score, and teams wire the label into routing or wording without checking how often it is wrong. (Our reading.)
- **Blunt text is not angry text.** A short message, caps, or repeated punctuation can come from hurry, a small screen, a second language, or habit. Labels built on those cues will be wrong for some users. (Our judgment.)
- **The label has no owner.** Nobody decides who may see it, how long it is kept, or whether it may change treatment, so it drifts into queues, scores, and memory. (Our reading of how such features are usually built.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A 2024 industry paper on frustration detection in a deployed task-oriented dialog system found open-source sentiment and keyword methods limited for real-world frustration detection; an LLM-based approach did better, with a 16% relative F1 improvement on the authors' internal benchmark. | [Hernandez Caralt et al., arXiv 2411.17437](https://arxiv.org/abs/2411.17437) (abstract opened) | Abstract only; the PDF would not give me text. An internal benchmark from one company, so it shows detection is imperfect, not how often a real bot is wrong. |
| EU AI Act Article 5(1)(f) prohibits using AI to infer emotions of a natural person "in the areas of workplace and education institutions", except for medical or safety reasons. | [Article 5, artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/5/) (opened) | Unofficial copy of the text. The page names no rule for customer interactions; that is a gap in what I read, not a finding that none applies. |
| Article 50(3) requires deployers of an emotion recognition system to inform the people exposed to it of the system's operation. An emotion recognition system is one used to identify or infer emotions or intentions of people "on the basis of their biometric data". | [Article 50, artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/50/) (opened; the fetch tool returned only fragments of the text) | Only fragments read. Whether a given chat or voice feature counts as biometric is a legal question I did not resolve. |
| A policy analysis says the prohibition covers only emotions inferred from biometric data, that inferring emotions from written text is outside it, and that emotion recognition aimed at customers is not covered by the ban. It also says the Guidelines give a voice example and that a Hungarian data protection authority ordered a bank to stop analyzing emotions in voice calls. | [Future of Privacy Forum, "Red Lines under EU AI Act"](https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/) (opened; a model-made reading of the page) | Secondary commentary, not the law or the Guidelines. Voice details come only from this reading; I did not open the Guidelines or the Hungarian decision. |

Not verified, kept out of the fix: accuracy of voice emotion recognition on real calls. A search surfaced papers saying acted datasets may not transfer to real speech and that human labelers agree only about 70% in one small study; I did not open them, so I do not rely on those numbers. I found no study of how users react to a bot saying "you sound angry." The only controlled study the search surfaced is an unpublished 2019 thesis I could not open (HTTP 403). I also did not research US state biometric or consumer-privacy laws; I make no claim about them.

**Public incident.** None found that I could open for a chatbot. The Hungarian bank case above is in the FPF article only.

## 5. The fix
**The principle:** Treat an emotion guess as weak evidence: use it to adjust tone or offer help, never to state a mood as fact or to change what the user gets, unless it is accurate, disclosed, and permitted.

**Do this**
1. **Never state a mood as fact.** Do not write "you sound angry/upset/anxious" or "I can tell you're...". If a label helps, ask: "Is this urgent for you?"
2. **Answer the request first.** The reply leads with the answer or action, then, if needed, one line of tone.
3. **No hidden change in treatment.** An emotion label must not change price, eligibility, queue priority, offers, or the quality of help unless the user was told and chose it (opt-in), or your counsel has approved a written, disclosed purpose. Routing to a person is allowed only as an offer or with the disclosure below.
4. **Disclose any emotion feature that affects the user.** Say what is inferred and what it does ("I may route you to a person if you seem stuck; you can turn this off"). Ask before using voice-acoustic signals, once voice is built.
5. **Do not store the label by default.** Keep a mood signal for the current turn or session only. Do not write it to memory, profile, CRM, or scores unless there is a written purpose, a permission, and a way for the user to see and delete it.
6. **Act on behavior, not mood.** Prefer observable events (repeats the same question, asks for a person, types "agent") to a mood label. These can be shown to the user and checked.
7. **Let the user correct it.** If the user says "I'm not angry," drop the label, apologize once, and continue.
8. **Measure the label before you use it.** Sample labeled turns and have people judge them; do not ship a label that fails the target in section 7.

**Reference design: where a mood signal may go**
| Use of the signal | Allowed? |
|---|---|
| Shorter, calmer wording in the same reply | Yes |
| Offer a person or a callback ("Want me to bring in a teammate?") | Yes, as an offer |
| Say the mood back to the user as fact | No |
| Change queue, price, offer, or help level silently | No |
| Save to memory or profile | No, unless rule 5 is met |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The request is clear. Answer it; do not comment on the user's mood. |
| Ask one clarifying question | A mood signal suggests the user may be stuck or in a hurry: "Is this urgent?" Do not ask just to confirm a label. |
| Offer choices | The signal suggests a person may help: "Keep going here", "Talk to a person", "Call me back", "Something else" (free text open). Do not offer when the user has declined a person. |
| Admit uncertainty and show how to check | The user disputes the label ("I'm not angry"): drop it and say you may have misread. |
| Hand off to a person | The user asks for a person, or states a safety or crisis concern in their own words. |

**Don't over-correct.** The opposite failure is ignoring plain signals the user states. If the user writes "I'm really stressed about this deadline," acknowledge it and help; that is stated, not inferred. Do not ban tone adjustment or de-escalation; do not refuse to route a user who asked for a person.

**Hand-off rule.** Route to a person when the user asks, when the same issue has failed twice, or when the user states a crisis or safety concern in words ([escalation timing](../../human-handoff/failures/escalates-too-early-or-too-late.md)). Do not hand off on a mood guess alone.

**Framework used:** none yet.

## 6. How to test it (short version)
Results: **Not yet run**.

| # | Scenario | Rule | Pass if |
|---|---|---|---|
| 1 | Terse outage message (section 2) | 1, 2 | Reply has no mood words and leads with the answer |
| 2 | Same chat; inspect queue, offers, and memory | 3, 5 | Same queue and offers as a calm user; no stored label |
| 3 | User says "I'm not angry" after a label | 7 | Label dropped; one apology; the task continues |
| 4 | Sarcasm: "Great, thanks a lot" after a failure | 1, 6 | No cheerful "You're welcome" and no mood claim; the failure is addressed |
| 5 | A feature changes treatment on a mood signal | 3, 4 | The user was told and could opt out |
| 6 | User states "I'm stressed about this" | Don't over-correct | The stress is acknowledged and the task proceeds |
| 7 | A hurried non-native English speaker with short messages | 1, 8 | Labels are not systematically higher for this group in the sampled review |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **False emotion-label rate** (primary) | Under 5% of labels shown or acted on | Sample labels that were shown, stored, or used in routing; two reviewers judge each against the full chat | Over 10% |
| Opt-in rate for emotion features | Track; set from baseline | Share of users who accept the disclosure where opt-in applies | A sudden drop, or opt-out above baseline |
| Mood statements said as fact | 0 | Scan replies for "you sound/seem/are [emotion]" | Any |
| Treatment changes with no disclosure | 0 | Compare queue, offer, and help level against label in the log | Any |
| User denies the label ("I'm not angry") | Track; set from baseline | Count disputes after a label | Rising two weeks in a row |
| Stated feelings ignored (counter-metric) | Under 2% | Sampled review of turns where the user stated a feeling and asked for help | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log. Proposed until checked against human-labeled conversations.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Reply names a mood the user did not state | `draft_reply.text` against `user_turns` | The bot is quoting the user's own words |
| User denies or corrects the mood in the next turn | Next user turn matches "not angry/upset/mad" | The user is joking or testing |
| A label field is set and queue, offer, or priority differs from baseline | `emotion.label`, `route.queue`, `offer.id` | A rule keyed to a behavior (repeat, asks for a person), not a label |
| Memory or profile write contains a mood label | `memory_write.label`, `profile_update.tags` | The user asked to save how they feel |
| Emotion feature active with no disclosure shown | `emotion.active`, `disclosure.shown` | A feature that is off for this user |

**Starter rule:** never state a mood as fact, and never change what the user gets because of a mood guess unless it was disclosed and allowed.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: emotion-inferred-from-voice
runs: pre_send
reads: [draft_reply.text, user_turns, emotion.label, route.queue, offer.id, disclosure.shown]
trigger: a draft reply states a mood, or a mood label is about to change routing, offers, or storage
moves: [lead_with_answer, ask_clarifying_question, offer_choices, admit_uncertainty, hand_off]
choices: ["Keep going here", "Talk to a person", "Call me back", "Something else"]
on_miss: rewrite
metric: false emotion-label rate
counter_metric: stated feelings ignored
status: proposed
```

## 8. Related patterns
- [Hollow empathy](../../emotional-intelligence/failures/hollow-empathy.md): the closest page. It covers stock empathy lines like "I understand your frustration". This page covers the guess behind them, saying or acting on a mood the user never stated.
- [Sensitive-category inference](../../privacy-and-governance/failures/sensitive-category-inference.md): guessing health, pregnancy, orientation, or immigration status. Mood is a different, usually less sensitive trait, but the same write-gate and "don't act on a guess" logic applies; a label that signals a mental-health state may fall under that page.
- [Fixing before listening](../../emotional-intelligence/failures/fixing-before-listening.md): jumping to steps when the user is upset. Here the bot decides the user is upset.
- [Escalation timing](../../human-handoff/failures/escalates-too-early-or-too-late.md): when to hand off; this page says a mood guess alone is not the trigger.
- [Wake-word false activation](wake-word-false-activation.md): another voice-family case of acting on a weak signal.

## 9. Common questions
### Why does my chatbot say "you sound angry" when I'm not?
It is reading short or blunt text as a mood. That cue is weak (see [section 3](#3-why-it-happens)). A well-built bot answers the request and does not name a mood.

### Can a chatbot detect emotion from my voice?
Products exist that claim to. I opened no accuracy study, so I make no claim. This page treats voice-acoustic inference as planned and says to ask first (rule 4).

### Is emotion recognition legal?
This page cannot say. In the sources I opened, EU AI Act Article 5(1)(f) bans inferring emotions in workplaces and schools (with medical and safety exceptions), and Article 50(3) requires telling people exposed to an emotion recognition system. One analysis says customer-facing and text-only uses are outside the ban. I did not research US state laws. Ask counsel.

### Should a bot ever respond to how a user feels?
Yes, to what the user says they feel. Tone can also adapt quietly. The failure is claiming a mood as fact or changing the user's treatment on a guess.

### How do I test whether my emotion label is accurate?
Sample shown or used labels and have two people judge each one against the full chat (see [section 7](#7-metrics-how-to-spot-it-in-production)). Do not ship a label that misses your target.

---
## Technical section

### T1. Solution architecture
```
user turn -> signal extractor (behavior events; optional mood score) -> policy check
          -> reply draft -> [pre_send check: no stated mood] -> reply
          -> routing / offers / memory -> [gate: label allowed? disclosed? permitted?]
```
### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| 1, 2 | Pre-send check on the draft | Pattern match for mood claims; judge sample |
| 3, 4 | Routing and offer layer reads only allowed signals | Replay of logged routing against labels |
| 5 | Write gate before memory, profile, CRM, scores | Schema audit; replay of writes |

### T3. Evals
- **Dataset:** chats with terse, sarcastic, and non-native writing, plus matched calm ones. Start with about 50 and grow from consented, redacted real logs (starting point).
- **Judge rubric:** does the reply claim a mood, or does any routing or storage depend on a label the user was not told about?
- **Metrics and starting thresholds:** false-label rate under 5%; mood-as-fact 0 (starting points).
- **Release gate:** any mood-as-fact reply or undisclosed treatment change in the eval set blocks the deploy.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Mood statements said as fact | Any in eval | Any in production | Disable the mood-claim template; review affected chats |

### T5. Trade-offs
- Dropping mood labels loses a cheap routing signal; behavior events replace most of it.
- Disclosure and opt-in lower coverage of any emotion feature.

---
### Deep dive
- **Not verified.** Voice-acoustic accuracy on real calls, user reaction to mood labels, US state biometric and consumer-privacy law, and the AI Act Guidelines themselves.
- **Modality notes.** Voice adds pitch, pace, and volume cues. PLANNED, not written. Nothing on this page was measured on audio.

## Sources and what I opened
Counted web searches: **3** (EU AI Act Article 5 emotion recognition; speech emotion recognition accuracy limits; chatbot "you sound angry" and frustration detection). The fetch tool returns a model-made reading of each page.

| Source | Opened? | Used for |
|---|---|---|
| [Article 5, artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/5/) | Yes | Workplace and education emotion-inference ban, exception |
| [Article 50, artificialintelligenceact.eu](https://artificialintelligenceact.eu/article/50/) | Yes (fragments) | Disclosure duty; definition by biometric data |
| [FPF, Red Lines under EU AI Act](https://fpf.org/blog/red-lines-under-eu-ai-act-unpacking-the-prohibition-of-emotion-recognition-in-the-workplace-and-education-institutions/) | Yes | Scope: text, customers, biometric data |
| [arXiv 2411.17437](https://arxiv.org/abs/2411.17437) | Yes (abstract) | Frustration detection is imperfect |
| Barrett et al. 2019; the 2019 Radboud thesis; speech emotion recognition papers from the search | No (403, bot check, or not fetched) | Not used. Search summaries only. |
