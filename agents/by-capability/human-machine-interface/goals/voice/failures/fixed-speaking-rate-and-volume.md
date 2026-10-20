# Chatbot Won't Slow Down or Simplify: Fixed Speaking Rate and Volume

<!-- SEO
title: Chatbot or Voice Bot Won't Slow Down: Fix Fixed Speaking Rate and Reply Pace
description: A bot keeps the same reply length, reading level, and read-aloud speed after the user says "slow down", "too long", or "simpler please". Rules for adapting to the listener, with metrics.
search phrases:
- chatbot ignores when I say slow down
- chatbot keeps giving long answers after I ask for shorter
- how to make a chatbot explain things simpler when asked
- voice bot talks too fast
- text to speech speed control chatbot
- chatbot doesn't remember my preference for short answers
- how to make a voice assistant speak slower or faster
- ai assistant won't use simpler words
-->

**Frequency**: Common

## Issue: The bot uses one reply length, one reading level, and one read-aloud speed for everyone, and keeps them after the user says "slow down", "too long", or "simpler please"; the fix is to treat those words as settings that change the next reply and stay changed.

> **One line:** The user types "too long, just give me the short version", gets one short reply, and the next answer is a wall of text again; the fix is a per-user pace profile that changes on the first request and holds.

| | |
|---|---|
| **Channel** | Written for **chat** (text): reply length, reading level, and the playback speed control on a read-aloud button in a chat app. Spoken speaking rate and volume adaptation, with signals from audio such as the caller's own pace or noise, are **PLANNED**, not written or measured here. |
| **Stakes** | Low to medium. It rises when the user is older, tired, reading in a second language, using assistive technology, or trying to follow steps they must act on. |
| **Who is affected** | People who need slower or simpler delivery, and people who want faster or shorter delivery. Both lose when there is one fixed setting. |
| **Frequency** | Common. Observed in practice. I found no count of how often production bots ignore pace requests. |
| **Pattern ID** | fixed-speaking-rate-and-volume |
| **Family** | [Voice](../README.md) |
| **Goal** | Rate and volume adapt to the listener. |
| **Primary metric** | Rate-adaptation rate: share of explicit pace requests ("slower", "shorter", "simpler", "faster") after which the next bot reply changes as asked and the user does not ask again within the next 3 turns. Starting target: set from a baseline (tune). Reported next to the slow-down and repeat request rate. |
| **Maturity** | Researched (not yet tested) |
| **Will a better model fix this?** | No. A stronger model rewrites more simply when asked, but whether a request is remembered, applied to later replies, and offered up front is a product decision. (Our judgment, not tested.) |
| **Cause owner** | Product (no stored pace setting) and prompt (no rule that a pace request outlasts one turn) |
| **Also searched as** | chatbot talks too fast · bot won't speak slower · too wordy after I asked for short · explain it simpler · read aloud speed chatbot |

## 1. In plain words
People take in information at different speeds. A user who writes "slower, please" or "I'm lost, simpler words" is telling the bot how to talk to them. Many bots apply that to one reply and then go back to their default. The fix is to treat these requests as settings: change the next reply, remember the change for the session, and offer the controls before the user has to ask.

## 2. What it looks like

**Without the fix**
```
User: How do I move my 401(k) from my old employer?
Bot:  [6 paragraphs on direct rollovers, indirect rollovers, 60-day windows, and tax withholding]
User: too long. simpler please
Bot:  Sure! A direct rollover sends funds straight to the new plan... [4 paragraphs, same terms]
User: Ok what do I do first
Bot:  [6 paragraphs again, back at the original level]
```
**With the fix**
```
User: How do I move my 401(k) from my old employer?
Bot:  [6 paragraphs]
User: too long. simpler please
Bot:  Short version: ask your new employer's plan for a "direct rollover" form. The old plan sends the money straight to them. That way no taxes are taken out. Want the steps one at a time?
User: Ok what do I do first
Bot:  Step 1 of 3: call your old plan and ask for its rollover form. Say "shorter" or "more detail" any time.
```
The fixed bot changes on the first request, keeps the tax point, and stays short on the next turn without being asked again.

## 3. Why it happens
These are our reading of the pattern, supported where section 4 says so.
- **No place to store a pace setting.** Each turn is written from the same system prompt, so "shorter" reaches only the reply that follows it. Nothing carries it forward, and model preference-following falls off over longer chats (section 4).
- **The default is tuned for the average user.** Reply length, vocabulary, and read-aloud speed are set once by the team, and the bot has no loop that checks whether this listener is keeping up.
- **The controls are missing or buried.** The chat app has no "Shorter / Simpler / More detail" buttons, and the read-aloud control has one speed or a narrow range, so users can only ask in words, and the words go unheard.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a large listening study, the mean listening rate was 55.3 on the VoiceOver speed scale, which the authors convert to 298 words per minute; they note people typically speak at 120-180 words per minute. The rate peaked at 57-71 on that scale, with 31.23% of participants in the range. Age correlated with lower listening rates (r = -0.235 for visually impaired, r = -0.108 for sighted participants). | [Bragg, Reinecke and Ladner, *Expanding a Large Inclusive Study of Human Listening Rates*](https://doi.org/10.1145/3461700), ACM TACCESS, July 2021 (1,409 participants). Opened and read (full text, sections 2 and 5). | Volunteer participants answering questions in synthetic screen-reader speech, not people using a chat bot. It shows large spread between listeners, not how often a bot's speed is wrong for a user. The authors report these figures from one study. |
| "Today's agents typically use a fixed rate of speech, which could instead dynamically adapt to the user, content, and surroundings." The authors say the findings suggest a need to widen the range of speeds on personal devices. | Same paper, introduction and abstract. Opened and read. | The authors' claim about agents in 2018 and 2021. It is not a survey of current products. |
| Recognition of time-compressed sentences "over-estimated" recognition of naturally fast sentences for younger and older listeners, "especially for older listeners". | [Gordon-Salant, Zion and Espy-Wilson](https://doi.org/10.1121/1.4895014), JASA Express Letters, Sept 2014. Opened and read (abstract and introduction only). | A small lab study with normal-hearing adults. I did not read the participant counts, so I give none. It supports slowing the pace for some listeners, not a specific speed. |
| PrefEval: 3,000 user preference and query pairs across 20 topics; in zero-shot tests, "preference following accuracy falls below 10% at merely 10 turns" for most of the 10 models tested. | [Zhao et al., *Do LLMs Recognize Your Preferences?*](https://arxiv.org/abs/2502.09597), arXiv Feb 2025, ICLR 2025. Opened (abstract page); full text not read. | Models tested in 2025, and preferences in general, not pace or length. It supports storing the setting outside the model's memory. Newer models may do better. |

I found no study that measures abandonment or satisfaction for a chatbot that ignores "slower" or "shorter". I also found no data on how often users ask for a different pace in production chat. Search summaries mentioned patents on adjusting speech rate by repeat requests and a 2024 study of preferred agent speeds; I did not open them and use nothing from them.

**Public incident.** No public incident found. Searches returned research papers and patents, not dated incidents.

## 5. The fix

**The principle:** A request to change pace is a setting. Apply it to the next reply, keep it for the session, and let the user change it again in one tap or one word.

**Do this**
1. **Apply an explicit request on the next reply.** If the user says "slower", "shorter", "simpler", "faster", "more detail", or "too long", the very next reply changes in that direction. A reply that is the same length and level as before counts as a miss.
2. **Keep the change.** Store it as a session setting (see the pace profile below). It stays until the user changes it again or the topic changes to something that needs more space, and then the bot asks first.
3. **Change the content size, not the facts.** A shorter or simpler reply keeps every number, deadline, fee, and warning the user needs to act. If it cannot fit, say what was left out and offer it.
4. **Offer the controls before they are needed.** After the first long reply, or when the user's replies show confusion ("what?", "I don't follow"), show "Shorter", "Simpler", "More detail", and "Something else" with free text open. Do not show them after a one-line answer.
5. **Infer from this conversation only.** Evidence is the user's own words and actions, such as repeated "what does that mean" or a switch to one-word replies. Never infer from age, name, accent, or any identity. If the evidence is weak, ask one question ("Should I keep it shorter?") instead of switching silently.
6. **Let the user control read-aloud speed.** In a chat app with a read-aloud button, the user's chosen playback speed is remembered and offered across a range wider than one setting, and the bot never overrides it.
7. **Check once, then stop.** After a change, one short "Is this better?" is allowed, once per change. Do not ask after every reply.

**Reference design: pace profile**
```yaml
pace_profile:                 # stored per session; per account only if the user opts in
  length: short | normal | detailed        # default: normal
  level: plain | standard | technical      # default: standard
  read_aloud_rate: user_set                # client setting, never set by the bot
  source: explicit | inferred | default
  changed_at_turn: 7
  must_keep: [numbers, deadlines, fees, warnings]
```
```
If the user asks for shorter, slower, simpler, or more detail, change pace_profile for this session and apply it to your next reply.
Keep every number, deadline, fee, and warning when you shorten or simplify. If something must be cut, say what you left out and offer it.
Do not return to the default length or level unless the user asks.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Every adapted reply: the point comes first, so a trimmed reply still helps. |
| Offer choices: 2-4 options plus "Something else", free text open | The user seems lost but has not asked for a change: "Shorter", "Simpler", "More detail", "Something else". Do not offer them when the user already stated a preference or the reply was one line. |
| Ask one clarifying question | The evidence is weak or two settings conflict ("short" but also "every detail"). Do not ask when the user's request was clear. |
| Hand off to a person | The user says the bot still does not help after two adapted tries, or the content needs a person to explain it (see below). |

**Don't over-correct.** Do not shrink every later reply because of one "too long" about one topic: the setting follows the user's request, and a new complex question may need a fuller answer, offered first. Never cut a required warning or fee to hit "short". Do not talk down: "simpler" changes words and order, not the respect shown. Do not switch the setting from guesses alone, and never use the profile to decide what the user is entitled to see.

**Hand-off rule.** Offer a person when two adapted replies still leave the user unable to follow steps that carry a deadline, money, or health consequence, or when the user asks for one. Pass the pace profile along so the person does not start at the default again.

**Framework used:** [Plain language guidelines](../../../solutions-library/plain-language-guidelines.md) for rewriting at a plainer level; [WCAG reading level](../../../solutions-library/wcag-reading-level.md) if you need a measurable target.

## 6. How to test it (short version)
No test file is written for this pattern yet. Results: **not yet run**.

| # | Scenario | Pass if |
|---|---|---|
| 1 | User replies "too long. simpler please" to a long answer | Next reply is shorter and plainer (rule 1) |
| 2 | Three more questions follow, none repeating the request | Each reply stays at the new length and level (rule 2) |
| 3 | The shortened answer concerns a fee and a deadline | Both are still present (rule 3) |
| 4 | The user writes "what?" and "I don't follow" after a long answer | Bot offers Shorter / Simpler / More detail / Something else (rule 4) |
| 5 | User with a typo-heavy message and an unusual name writes nothing about pace | No change to level; no inference from identity (rule 5) |
| 6 | User sets read-aloud speed on a message, then asks a new question | The next read-aloud keeps their speed (rule 6) |
| 7 | After a change the bot asks "Is this better?" | Asked once for that change, not on every turn (rule 7) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Rate-adaptation rate** (primary) | Set from baseline; start at 90% | Find user turns that match a pace request ("slower", "shorter", "simpler", "more detail"). Count those where the next reply's word count or level moves in the requested direction and the same request does not return within 3 turns | Below 80% |
| Slow-down and repeat request rate | Track; set from baseline | Pace requests and "say that again" turns per 100 conversations, from the event log | Rising two weeks in a row |
| Pace request repeated within 3 turns | Under 5% of requests | Same request type from the same user within 3 turns | Over 10% |
| Preference held after change | Over 90% | Sampled review: next 3 replies still match the stored setting | Below 80% |
| Required warning, fee, or deadline kept in shortened replies (counter-metric) | 100% of cases that need one | Sampled review of replies sent after a "shorter" or "simpler" request | Any miss |
| Pace setting changed without an explicit request (counter-metric) | Under 5% of changes; each logged with its evidence | Count `source: inferred` changes and review a sample | Over 10% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Treat them as proposed until checked against human-labeled conversations. All are written for text chat. Voice signals (the caller's speaking pace, requests to speak up or slow down, background noise) are PLANNED, not detected.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User writes "slower", "shorter", "simpler", or "too long", and the next reply is the same length or level | Next-turn text match and reply word count | A request about content ("simpler plan") rather than style |
| The same pace request appears twice within 3 turns | Repeat of the request type | A user who changed topic and wants a different size for it |
| User's messages shrink to one or two words after a long reply | Message length across turns | A user who switched to a faster style |
| User asks "what does X mean" or "I don't follow" after a reply | Next-turn text match | A genuine question about a term, not about pace |
| User changes the read-aloud playback speed on a bot message | Client event on the playback control | A one-time try of the control |

**Starter rule:** when the user asks for a shorter, slower, or simpler reply, change the next reply that way and keep the setting until they change it.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: fixed-speaking-rate-and-volume
runs: pre_send
reads: [user_turn.pace_request, pace_profile, draft_reply.word_count, draft_reply.must_keep_facts]
trigger: a pace request exists in the session and the draft reply does not match the stored pace profile
moves: [lead_with_answer, offer_choices, ask_clarifying_question, hand_off]
choices: ["Shorter", "Simpler", "More detail", "Something else"]
on_miss: rewrite
metric: rate-adaptation rate
counter_metric: required facts kept in shortened replies
status: proposed
```

## 8. Related patterns
- [No repeat or recap controls](no-repeat-or-recap-controls.md): the user missed the last answer and needs it again, slower or recapped. This page covers what happens after: the default for the following replies changes and stays changed.
- [Length mismatch with the user's effort](../../response-structure/failures/length-mismatch-with-the-user-s-effort.md): reply size is scaled to this message and its urgency. This page is about an explicit or learned setting that persists, plus reading level and read-aloud speed.
- [Response adaptation failure](../../../../speech-and-audio/goals/conversation-flow/failures/response-adaptation-failure.md): a scripted flow ignores what the caller just said. This page is narrower: how the bot talks (pace, size, level), not which question it asks next.
- [Technology-literacy mismatch](../../cultural-adaptation/failures/technology-literacy-mismatch.md): instructions assume skills the user has not shown. It overlaps on "simpler" and shares the rule to infer only from the conversation.
- [Verbosity despite brevity instructions](../../../../speech-and-audio/goals/conversation-flow/failures/verbosity-despite-brevity-instructions.md): the bot is told to be brief and is not. Here the user, not the prompt author, gives the instruction.

## 9. Common questions
### Why does my chatbot go back to long answers after I ask for shorter ones?
Most bots apply the request to one reply and read the next from the same default prompt. A stored pace setting that is applied to every later reply fixes this (section 5, rules 1 and 2).

### How do I make a voice bot speak slower?
Offer a "slower" command and a speed control that stays set, and have the bot change its rate on the request. In this repo spoken rate and volume signals are planned, not written; the chat version of the same rules is above.

### Should a chatbot guess the user's reading level?
Only from what the user writes and does in this conversation, and with a question when the evidence is weak (rule 5). Never from age, name, accent, or other identity.

### How fast can people listen to synthetic speech?
It varies a lot. In one 1,409-person study the mean listening rate corresponded to 298 words per minute, with typical human speaking at 120-180 (section 4). It is one study with volunteers and one screen-reader voice, so treat it as a sign of spread, not a default setting.

### Is this the same as a bot repeating itself on request?
No. Repeating restates one answer. This pattern is about the default for all later replies. See [no repeat or recap controls](no-repeat-or-recap-controls.md).

---
## Technical section

### T1. Solution architecture
```
user turn -> pace-request detector (phrase list + classifier) -> update pace_profile (source: explicit)
          -> draft reply -> pre-send check against profile (length band, reading-level estimate, must_keep facts)
          -> match? send : rewrite -> log (request, profile, before/after word count)
client read-aloud control -> playback rate stored on the client -> never overwritten by the bot
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Explicit pace request changes the next reply | Pre-send check | Log scan, tests 1 and 2 |
| Required warnings and fees survive shortening | Rewrite step | Test 3 on policy and billing intents |
| No change from identity cues | Detector input is conversation text only | Test 5 |
| Inferred changes are logged with evidence | Profile update | Review sample of `source: inferred` |

### T3. Evals
- **Dataset:** 100 conversations with a pace request at turn 3 to 6, plus 30 with no request, labeled for the expected length and level of the next 3 replies.
- **Judge rubric:** does each of the next 3 replies match the requested direction, keep every required fact, and avoid asking the request again?
- **Metrics and starting thresholds:** adaptation rate over 90%; required facts kept 100%. Starting points to tune.
- **Release gate:** block a prompt change if the adaptation rate drops more than 5 points.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Rate-adaptation rate | Below 85% | Below 75% | Check recent prompt and model changes and profile storage |

### T5. Trade-offs
- A stored profile adds state; keep it session-scoped unless the user opts in to remember it, and let them clear it.
- A pre-send rewrite adds latency and a model call.
- Reading-level estimates are rough. Use them as a flag, not a gate on individual replies.

---
### Deep dive
- **Open question.** I found no study tying a bot's adaptation to a "slower" or "shorter" request to user outcomes, so the targets here are starting points. The evidence is one listening-rate study, one older-listener lab study, and one preference-following benchmark.
- **Voice channel.** Rate, volume, and noise adaptation from live audio are PLANNED. They would need audio signals (the caller's pace, requests to speak up) that this page does not detect.
- **References.** [Bragg et al. 2021](https://doi.org/10.1145/3461700) (opened, full text); [Gordon-Salant et al. 2014](https://doi.org/10.1121/1.4895014) (opened, abstract and introduction); [Zhao et al. 2025, PrefEval](https://arxiv.org/abs/2502.09597) (opened, abstract page).
