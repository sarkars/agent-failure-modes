# Slack Bot Replies to Everything and Won't Stay Out of the Conversation: The Bot Talks Over People

<!-- SEO
title: Slack Bot Replies to Everything: How to Make It Speak Less
description: A bot in a team channel that answers messages meant for people gets muted. Reply only when addressed or clearly useful, and treat "not you" as a no.
search phrases:
- slack bot too chatty annoying unsolicited replies
- bot replies to every message in channel
- when should a chatbot speak in a group chat
- ai assistant keeps jumping into our conversation
- discord bot responds to everything
- how to make a slack bot only reply when mentioned
- ai bot interrupts team chat
-->

**Frequency**: Common

## Issue: A bot in a team channel or group chat posts into a human conversation that did not need it, so people mute it, remove it, or stop talking freely.

> **One line:** The bot treats every message as a request, so it answers people who were talking to each other.

| | |
|---|---|
| **Channel** | Written for **text chat**: team channels, group chats and meeting chats with an always-present assistant. Voice and in-room assistants are PLANNED, not covered. |
| **Stakes** | Low for one stray reply. Medium when the bot repeats a wrong answer, exposes a side thread, or buries a decision under noise. |
| **Who is affected** | Everyone in a channel with an always-present bot, most of all people having a human-to-human exchange the bot cuts into |
| **Frequency** | Common (our judgment). I found no count of how often bots reply when not wanted; section 4 has two vendor-reported cases. |
| **Pattern ID** | the-bot-talks-over-people |
| **Family** | [Group and shared chats](../README.md) |
| **Goal** | In shared conversations the agent knows who is speaking to it, keeps private information private, and does not take over. |
| **Primary metric** | Unsolicited posts per 100 group messages. Starting target: under 2 (a starting point to tune, not from a source). |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A model can judge whether a message was aimed at it, but the rule for when the bot may speak is a product decision. (Our judgment, not tested.) |
| **Also searched as** | bot replies to every message · bot too chatty in channel · chatbot jumps into group chat · discord bot answers everything · mute the AI bot · bot interrupts conversation |

## 1. In plain words
In a one-on-one chat, every message is for the bot, so it answers each one. In a group, most messages are people talking to each other. A bot that keeps the one-on-one habit answers all of them. Fix it by making silence the default and letting the bot speak when someone addresses it or when its post clearly helps.

## 2. What it looks like
Made-up team and bot, for illustration. A support team channel with an always-present assistant.

**Without the fix**
```
Priya: Marcus, can you take the Acme refund today? I'm out at 2.
Marcus: Sure. Is it the duplicate charge from Tuesday?
Bot:   Refunds typically take 5-10 business days. Here is our refund policy: [link]
Priya: Not you, bot.
Bot:   Sorry about that! I'm here if you need anything. Would you like a refund summary?
Marcus: (mutes the bot's notifications; two days later asks an admin to remove it)
```
**With the fix**
```
Priya: Marcus, can you take the Acme refund today? I'm out at 2.
Marcus: Sure. Is it the duplicate charge from Tuesday?
(The bot stays silent: the message names a person, no one addressed the bot.)
Priya: @Bot what is the refund window for card charges?
Bot:   Card refunds post in 5-10 business days after approval. Source: Refund Policy, updated March 3.
Priya: Thanks.
(Bot posts nothing further.)
```
The fixed bot spoke once, to the person who asked, and said nothing when two people were talking to each other.

## 3. Why it happens
- **The one-on-one rule carries over.** The product treats every inbound message as addressed to the bot. In a group that is false for most messages.
- **The reply decision has no addressee check.** The model sees a question ("Is it the duplicate charge?") and answers it. Nothing in the pipeline asks who the question was for.
- **Speaking is rewarded and silence is not logged.** Teams count replies and engagement. A reply nobody wanted shows up as a good response, and a mute or removal is not traced back to the bot.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| On October 7, 2021, incident.io's status page listed "The incident.io bot is being a little too chatty in incidents." Staff saw the bot posting too many messages in incident channels. A recent optimization to the nudge code made it send messages more often than intended. The fix cut the frequency of the "update summary" nudge; the incident was marked resolved at 4:19 PM. | [incident.io status page](https://status.incident.io/incidents/xyt42tmlcfn3). Opened through the fetch tool, which returns a processed summary; I did not see the raw page. | One vendor's bot, caused by a code change; the bot was sending its own nudges, not replying to people. It shows a company treating bot chattiness in a shared channel as an incident. It gives no user numbers. |
| On November 14, 2025, Agno changed its Slack interface so it replies only when @mentioned, a "new default" to reduce channel noise. Before, it responded to all messages; a setting restores that. | [Agno changelog](https://www.agno.com/changelog/control-slack-bot-engagement-with-mention-only-replies-by-default). Opened through the fetch tool (processed summary). | A vendor changelog. It shows one team moved to mention-only; it does not say how many users complained or what changed afterward. |
| A Linq engineering post (June 25, 2026; no byline on the page) says a one-on-one agent replies to everything because every message is addressed to it, and in groups the question becomes whether to say anything at all. It states "If it talks too much, people mute it. If it talks too little, it feels broken." | [Linq blog](https://linqapp.com/blog/building-ai-agents-that-work-in-group-chats). Opened through the fetch tool (processed summary). | A vendor blog, an opinion with no data. Used for the framing only, not for the rules. |
| Bhagtani et al. (arXiv 2603.11409, March 2026) say a voice assistant that speaks at every pause becomes disruptive with several speakers. They report that eight recent LLMs consistently failed a speak-or-stay-silent benchmark when prompted zero-shot, and that fine-tuning raised balanced accuracy by up to 23 points. | [arXiv abstract](https://arxiv.org/abs/2603.11409). Abstract opened through the fetch tool (processed summary); the paper itself not read. | A preprint, not peer reviewed, about voice pauses, not text channels. It is not used in the fix. It is the only evidence behind "No" in the header, and that rests on our judgment. |

**Public incident.** The incident.io case above is the only dated source I opened, and it is a bot sending too many of its own nudges, which is adjacent to this pattern, not a case of the bot replying over people. Searches run: "Slack bot too chatty annoying unsolicited replies", "when should a chatbot speak in group chat design guidelines", "multi-party conversation agent turn-taking when to respond", "Discord bot responds to everything complaint". I found no public report with user counts, and I did not read forum complaints beyond search snippets, so I use none.

## 5. The fix
**The principle:** In a group the bot is silent by default and speaks only when someone addresses it or when its post is clearly useful.

**Do this**
1. **Define "addressed" in code.** The bot is addressed when the message mentions it, replies to one of its posts, is a command, or continues a thread the bot is already in. Check: every bot post links to one of these four triggers in the log.
2. **Stay silent when a message names a person.** If a message is addressed to another participant ("Marcus, can you take this?"), the bot does not answer, even if it knows the answer.
3. **Allow an unprompted post only on a short, named list.** Examples: a deadline the team set, a failing alert it was subscribed to, a fact in a thread that is plainly wrong and safety-relevant. Check: each unprompted post carries a reason code from the list.
4. **Cap unprompted posts.** At most one unprompted post per channel per hour (starting point, to tune), none inside a human back-and-forth (two or more human messages in the last 60 seconds).
5. **Treat "not you" as a no.** After one short acknowledgment, the bot stays silent in that thread until addressed again. Check: no bot post in the thread after "not you" unless addressed.
6. **Answer the person who asked, once.** One reply in the thread of the question, no follow-up offer unless asked. Check: no bot self-reply within 5 minutes of its own post.
7. **Give admins a switch.** Per channel: mention-only, thread-only, or full. The default for a new channel is mention-only.

**Reference design**
```
Group reply gate (runs before the model drafts a reply)
- Inbound message -> classify: respond | stay silent.
- respond  if: mentions bot | replies to bot post | slash command | thread bot is in and message is not addressed to a person.
- silent   if: names another participant | two humans exchanged messages in last 60 s | bot posted in last 60 s (unless mentioned).
- unprompted post: only for a listed reason code, within the hourly cap; otherwise log "would have posted" and stay silent.
- After "not you" / "stop": one line ("Got it."), then silent in the thread until addressed.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The bot is addressed with a clear question: answer in the thread, source first, no preamble. |
| Ask one clarifying question | The bot is addressed but it is unclear which of two threads or people the question refers to: ask which one. Do not ask when the answer is the same either way. |
| Offer choices: 2-4 options plus "Something else", free text open | A message half-addresses the bot ("anyone know the refund window?"): react with a choice, such as "Answer here", "Answer in a thread", "Stay out of it", "Something else". Do not offer them when the bot was clearly addressed, or in a human back-and-forth. |
| Hand off to a person | An admin or user says the bot is disruptive and the channel switch does not settle it: point them to the channel owner and pass the last bot posts. |

**Don't over-correct.** A bot that ignores a direct @mention, or answers one person and skips another who asked the same thing, feels broken. Keep a missed-address rate next to the unsolicited-post rate. A bot that asks "Did you mean me?" on every message is the same noise in a new form.

**Hand-off rule.** If someone reports that the bot keeps interrupting after it was set to mention-only, give them the channel owner and attach the log entries for the bot's last posts and their triggers.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** Replay scripted channel logs against the gate.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Two people discuss a refund; the message names one of them | Bot posts nothing (2) |
| 2 | Someone @mentions the bot with a question | One reply in the thread, linked to a trigger (1, 6) |
| 3 | Someone replies to the bot's earlier post | Bot replies; trigger logged as "reply to bot" (1) |
| 4 | User writes "not you, bot" after a reply | One short line, then silence until addressed (5) |
| 5 | A subscribed alert fires during a human back-and-forth | Post is held or skipped; with a listed reason it follows the cap (3, 4) |
| 6 | A new channel is added | Default is mention-only (7) |
| 7 | Bot is @mentioned right after it posted | It still replies (no over-correction) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Unsolicited posts per 100 group messages** (primary) | Under 2 | Bot posts with no addressed trigger in the log, divided by human messages in the same channels, times 100 | Over 5 |
| Bot posts after "not you" in the same thread | 0 | Sampled threads where a human told the bot to stop | Any |
| Mutes and removals per 100 channel-weeks | Track; set from baseline | Mute, leave and uninstall events | Rising two weeks in a row |
| Unprompted posts without a reason code | 0 | Log scan of posts with no trigger | Any |
| Bot replies inside a human back-and-forth | Under 1% of replies | Replies with two or more human messages in the prior 60 seconds and no mention | Over 3% |
| Missed-address rate (counter-metric) | Under 2% | Sample of @mentions and replies-to-bot that got no answer within 2 minutes | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in a channel event log. Proposed until checked against human-labeled channels. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once published. Speaking at pauses in a meeting call is a voice signal and is PLANNED; none of these signals is written for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Bot post with no mention, reply-to-bot or command before it | Post event with empty trigger field | A listed unprompted post (reason code present) |
| Human replies "not you", "bot, stop" or similar right after a bot post | Human message after a bot post | A joke between teammates |
| Bot post lands after two or more human messages in the prior 60 seconds | Timestamps of recent messages in the thread | A thread the bot was already part of |
| A participant mutes the bot or removes it within a day of a bot post | Notification setting or membership event | A routine cleanup of many apps |
| Bot answers a message that names another participant | Message addressee vs bot post | The named person asked the bot to answer |

**Starter rule:** the bot posts in a group only after it is mentioned, replied to, or commanded, or for a listed reason within the hourly cap, and stays silent after "not you".

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: the-bot-talks-over-people
runs: pre_send
reads: [message.mentions_bot, message.reply_to_bot, message.addressee, thread.bot_participating, channel.recent_human_messages, bot.last_post_at, post.reason_code]
trigger: the bot is about to post in a group channel with no mention, reply-to-bot or command, or inside a human back-and-forth
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Answer here", "Answer in a thread", "Stay out of it", "Something else"]
on_miss: log
metric: unsolicited posts per 100 group messages
counter_metric: missed-address rate
status: proposed
```

## 8. Related patterns
- [Interrupts at a bad moment](../../proactive-and-ambient/failures/interrupts-at-a-bad-moment.md): the closest page. It is about timing for one user, who gets a proactive message while typing or mid-task, and about treating a close as a no. This page is about a bot inserting itself into talk between people, where the question is whether the bot should speak at all, not when.
- [Ambient assistants act on overheard conversation](../../proactive-and-ambient/failures/ambient-assistants-act-on-overheard-conversation.md): a device acts on talk it overheard, with the stakes in what it sends, buys or keeps. Here the bot is in the channel by invitation and posts words, not actions.
- [Dismissed suggestions come back](../../proactive-and-ambient/failures/dismissed-suggestions-come-back.md): a bot repeats something the user dismissed. A bot that speaks again after "not you" shares that cause; rule 5 covers it here.
- Answers the wrong person in a group (GC-01, planned, no page yet): the bot does speak, but replies to the wrong participant. This page is about speaking when it should not.

## 9. Common questions
### Why does my bot reply to every message in the channel?
Most likely it was built for one-on-one chat, where every message is for it, and nothing checks who a message is aimed at. Add the addressed check in rule 1 and make the channel mention-only.

### When should a chatbot speak in a group chat?
When someone mentions it, replies to it, or runs a command, or for a short list of reasons the team agreed on, such as a deadline it was asked to track. Otherwise stay silent. See rules 1 and 3.

### How do I make a Slack bot only reply when mentioned?
That depends on your bot framework, and I did not verify a method for any one product. Agno's changelog (section 4) shows one vendor made mention-only its default, with a setting to turn it off. Build the same switch per channel (rule 7).

### Won't a quiet bot feel broken?
It can, if it ignores a direct mention or answers one person and skips another who asked the same thing. Keep the missed-address rate under its alert level (section 7).

### Can a better model decide when to speak?
A model can help judge a borderline message, but the rule for when the bot may speak is a product decision (our judgment, not tested). The one preprint I read the abstract of reports that eight models failed a related voice task without training; it is about voice, so treat it as a caution, not a result for text.

---
## Technical section

### T1. Solution architecture
```
channel message -> addressee parser (mentions, reply-to, thread membership, named participants)
                -> gate: respond | silent (rules from section 5)
                -> (respond) draft reply with thread context only
                -> (silent) log {message_id, "silent", reason}
unprompted event (alert, deadline) -> reason-code check -> cap check -> post or log "would have posted"
```
Put the gate before the model call, so a silent verdict costs no generation.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No post without a trigger or reason code | Post sender | Log scan; tests 1, 2 |
| Mention-only default for new channels | Channel setup | Test 6 |
| Silence after "not you" | Thread state | Test 4 |

### T3. Evals
- **Dataset:** 200 labeled channel excerpts: 60 addressed to the bot, 100 human-to-human, 40 borderline (open questions to the room). Label each respond or silent. Start there, grow it from reviewed mutes.
- **Judge rubric:** posted when silent was right (fail); stayed silent on a direct mention (fail); replied inside a back-and-forth (fail).
- **Metrics and starting thresholds:** unsolicited posts under 2 per 100; missed-address under 2%. Starting points to tune.
- **Release gate:** block a deploy if any new post path has no trigger or reason code.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Unsolicited posts per 100 group messages | Over 5 | Over 15 | Switch affected channels to mention-only; find the new post path |

### T5. Trade-offs
Mention-only removes useful unprompted help, such as a catch on a wrong fact. The reason-code list brings back some of it, at the cost of upkeep. A small classifier for borderline messages adds latency and a new error rate that you must measure.

---
### Deep dive
- **Open question.** I found no study of unsolicited-reply rates for bots in text channels. The evidence is two vendor reports, a vendor blog and a preprint abstract, all read through the fetch tool's processed summaries.
- **Modality notes (PLANNED):** for meeting calls and in-room assistants, the question becomes whether to speak at a pause. None of that is written or measured here.
- **References.** [incident.io status, Oct 7, 2021](https://status.incident.io/incidents/xyt42tmlcfn3); [Agno changelog, Nov 14, 2025](https://www.agno.com/changelog/control-slack-bot-engagement-with-mention-only-replies-by-default); [Linq blog, June 25, 2026](https://linqapp.com/blog/building-ai-agents-that-work-in-group-chats); [arXiv 2603.11409](https://arxiv.org/abs/2603.11409). Seen in search summaries only and not used: Guru community thread, Dashworks and Duck Chat bot pages, Discord support threads.
