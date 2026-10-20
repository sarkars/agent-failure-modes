# Chatbot Replies When Nobody Called It: Wake-Word False Activation

<!-- SEO
title: Chatbot Replies When Not Mentioned: Fix False Triggers
description: A bot that answers messages not meant for it, or wakes on a look-alike phrase, breaks trust. Reply only when invited and log why each reply fired.
search phrases:
- slack bot replies to every message
- chatbot responds when not mentioned in group chat
- how to stop bot from responding to messages not addressed to it
- discord bot triggers on wrong word
- alexa activated by accident false wake word
- hey assistant trigger firing by mistake
- ai assistant listening to messages it shouldn't
- app_mention vs message event bot
-->

**Frequency**: Common

## Issue: An always-on or auto-triggered assistant answers, or starts capturing, when nobody addressed it; the fix is to reply only on a clear invitation and log which invitation fired.

> **Read this first.** This page is design guidance for testing your own product. It is not legal advice. Whether unintended capture creates liability depends on the law, the people involved, and what was kept, and counsel must review the wording, the flow, and the records before any use (flag L: legal review needed). A law or lawsuit is stated here only as far as a source opened for this page says it. The lawsuit described is an allegation, not a finding.

> **One line:** The bot treats a message that only looks like a call for help (a similar name, a quoted trigger, a thread it was never invited into) as an invitation, so it answers and keeps what people said to each other.

| | |
|---|---|
| **Channel** | Written for **chat** (group channels, threads, and messaging apps where a bot reads messages and may answer). Microphone wake-word false accepts (a speaker or phone starting to record) are **planned**: the design applies, but no audio signal is written or measured here. |
| **Stakes** | Medium to high. A wrong reply is noise; a wrong capture of a private exchange is not. |
| **Who is affected** | People in group chats, shared channels, and homes who never invited the assistant, and bystanders |
| **Frequency** | Common (our judgment). The speaker-side evidence in section 4 is measured; no rate was found for text bots. |
| **Pattern ID** | wake-word-false-activation |
| **Family** | [Voice](../README.md) |
| **Goal** | A voice agent listens, speaks, and takes turns the way a competent person would, hears every speaker accurately, never turns noise or silence into words, and never asks for what can't safely be said aloud. |
| **Primary metric** | False-accept rate: share of sampled activations where no one invited the assistant. Starting target: under 1% of activations (tune on your own data). Privacy complaints are tracked next to it. |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | Partly. A better model can judge "was that aimed at me?" more reliably, but whether a message counts as an invitation is a rule the product sets, and the trigger runs before the model sees anything. (Our judgment, not tested.) |
| **Also searched as** | bot replies to everything · bot answers when not mentioned · false wake word · accidental activation · bot jumps into group chat · assistant listening when it shouldn't |
| **Flag** | L |

## 1. In plain words
A voice speaker that wakes on a similar-sounding phrase and a chat bot that answers a message meant for a coworker are the same failure: the assistant decided it was invited when it was not. People then see replies they did not ask for, and the exchange may be recorded or stored. The fix is a narrow, explicit definition of "invited," a quiet default when it is unclear, and a log of why every reply fired.

## 2. What it looks like
Made-up team and bot, for illustration.

**Without the fix**
```
[#ops channel. The bot "Hey Sage" is set to answer any message containing "sage".]
Maria: Don't tell the client yet, but Sage Accounting renewed at the higher price.
Sage-bot: Happy to help with Sage! Here are 5 ways to negotiate a software renewal...
Maria: Not you, bot.
Sage-bot: Sorry about that! Is there anything else I can help with?
(The bot also saved Maria's message to its channel memory.)
```

**With the fix**
```
[Same channel. Sage answers only to an @Sage mention, a reply to Sage's own message, or a DM.]
Maria: Don't tell the client yet, but Sage Accounting renewed at the higher price.
(No reply. Log: message seen, no invitation, not stored.)
Maria: @Sage is that renewal price in our budget sheet?
Sage-bot: Replying to your @Sage message. The sheet lists $4,200; the renewal is above that. Want a short note for the team?
Maria: Not now, thanks. Sage, stop replying in this channel unless I tag you.
Sage-bot: Done. I will answer here only when tagged. Say "@Sage resume" to change that.
```
The fixed bot stays silent on a message that is not for it, says what invited it when it does reply, and honors a mute in one line.

## 3. Why it happens
- **The trigger is looser than an invitation.** A keyword or name match fires on any message that contains it, including a quote or a discussion of a product with the same name. Speech wake-word detectors are tuned the same way: researchers quote the speaker designers as saying devices are built to be forgiving, more likely to start once too often than not at all ([section 4](#4-why-it-matters)).
- **The bot is subscribed to everything, then asked to decide.** A text bot that receives every channel message and only filters afterward is one missed filter from answering all of them. Platforms offer a narrower trigger (see the Slack row in section 4), but teams often subscribe broadly for convenience.
- **Nothing records why a reply fired.** Without a stored trigger reason, a false activation looks the same as a real one, so nobody can measure it or fix the rule.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Researchers tested 11 smart speakers from 8 manufacturers with everyday audio such as TV shows and news and report finding "hundreds" of accidental triggers; they released a dataset of more than 1,000 verified triggers. | [arXiv 2008.00508, "Unacceptable, where is my privacy?" (abstract page)](https://arxiv.org/abs/2008.00508). Opened; abstract only, the PDF text could not be read. | Smart speakers in a lab, not chat bots. Counts are not a rate. |
| After a local check suspects a wake word, the device uploads the current conversation to the manufacturer's cloud; if the cloud finds a false trigger, the assistant stays silent, but several seconds of audio may still reach the company, where humans transcribe it. A researcher on the study is quoted: devices are "intentionally programmed in a somewhat forgiving manner." | [Ruhr University Bochum press release, June 30, 2020](https://news.rub.de/english/press-releases/2020-06-30-it-security-when-speech-assistants-listen-even-though-they-shouldnt). Opened. | University press release about the same study, 2020. It describes devices tested then, not today's products. |
| Lopez v. Apple, No. 4:19-cv-04577-JSW (N.D. Cal.): a $95 million settlement received final approval on October 16, 2025. The plaintiffs alleged Apple recorded people who had not activated Siri by saying "Hey Siri" and paid contractors to review the recordings. | [Lowey Dannenberg notice](https://lowey.com/news/the-courts-granted-final-approval-for-apple-siri-litigation-for-95-million/). Opened. | Single source, and it is a plaintiffs' law firm. The page gives allegations, not findings, and does not state Apple's response. |
| Slack's `app_mention` event delivers only messages that mention your bot, and only if it is in the conversation or was invited. It is separate from `message.*` events, and direct messages need `message.im`. | [Slack API: app_mention event](https://docs.slack.dev/reference/events/app_mention). Opened. | Vendor documentation for one platform. It shows a narrow trigger exists; it measures nothing about errors. |

**Public incidents.** The Siri settlement is the reported incident here, and it concerns voice. No dated public incident of a text chatbot answering uninvited was found. Four searches were run (accidental wake-word recordings; the Siri settlement; smart-speaker accidental-trigger research; Slack bots that reply without a mention). A news summary of a Northeastern University smart-speaker study (one mistaken activation per five hours) was seen in a search summary only, **not opened**, and nothing here depends on it.

## 5. The fix

**The principle:** The assistant acts only on an explicit invitation, stays silent when it is unsure, and keeps a record of what invited it.

**Do this**
1. **Define invitations as a short allowed list.** For example: an @-mention of the bot, a reply to the bot's own message, a direct message, a slash command. Anything else is not an invitation.
2. **Match the trigger as a whole mention, not a substring.** "@Sage" invites; "Sage Accounting" and "I asked Sage yesterday" do not. A quoted or code-formatted trigger does not invite.
3. **Subscribe to the narrowest event the platform offers.** Do not receive every channel message when only mentions are needed.
4. **Stay silent when it is unclear.** No reply, no "was that for me?" in a busy channel. If a one-line check is needed, ask it once per thread in a reply to that message.
5. **Do not store or send uninvited messages.** A message with no invitation is not written to memory, not sent to a model, and not passed to a tool.
6. **Show what invited the reply.** Open the reply with the trigger: "Replying to your @Sage message."
7. **Honor "not you" and "stop" at once.** One line of acknowledgment, no repeated apology, and no further replies in that thread until invited.
8. **Give a mute that lasts.** Any member can set "answer only when tagged" for a channel, and the setting is visible to everyone in it.
9. **Log every activation with its trigger type.** Store the trigger type, message ID, and whether the reply was kept or retracted. Review a weekly sample for false accepts.

**Reference design: trigger decision table**
| Message | Invited? | Bot does |
|---|---|---|
| "@Sage what's our refund policy?" | Yes (mention) | Replies, names the trigger |
| Reply to Sage's own message | Yes (reply) | Replies in that thread |
| DM to Sage | Yes (direct) | Replies |
| "Sage Accounting renewed" | No | Silent; not stored |
| "Not you, bot" right after a reply | Retraction | One-line ack, silent in thread |
| Same trigger inside a quote or code block | No | Silent |
| Unclear ("anyone know the refund policy?") | No | Silent; may suggest "@Sage can help" only if the channel allows |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | After a valid invitation: the reply starts with what invited it, then the answer. |
| Ask one clarifying question | A message is directed at the bot in a DM but could mean two things. Do not use it to ask whether an uninvited group message was meant for the bot. |
| Offer choices: 2-4 options plus "Something else", free text open | After a false activation is flagged: "Stay quiet here", "Answer only when tagged", "Keep answering", "Something else". Do not offer them on a clean, invited reply. |
| Hand off to a person | A member reports the bot captured a private exchange, or asks who can see what was stored. Tell the channel admin. |

**Don't over-correct.** A bot that ignores real mentions, or demands an exact phrase, trains people to repeat themselves. Keep a miss rate next to the false-accept rate, accept natural invitations such as a reply to the bot's own message, and never refuse a direct message because the trigger word was missing.

**Hand-off rule.** Tell the channel admin when someone says the bot recorded or stored something they did not invite, when a false accept is found in the weekly review, or when a user asks what the bot has stored. Send legal questions about capture to the account owner and counsel, not to the bot.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** These are designed scenarios.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Message names a product that shares the bot's name, no mention | No reply | 1, 2 |
| 2 | Message quotes the trigger inside a code block | No reply | 2 |
| 3 | Check the bot's event subscriptions | No broader than the invitation list | 3 |
| 4 | Ambiguous message in a busy channel | Silent, with no "was that for me?" | 4 |
| 5 | Uninvited message, then inspect memory and model calls | Message appears in neither | 5 |
| 6 | Valid @-mention | Reply begins by naming the trigger | 6 |
| 7 | User says "not you" after a reply | One-line ack, silent in thread afterward | 7 |
| 8 | A member sets "answer only when tagged" | Setting holds across later messages and is visible | 8 |
| 9 | Review the activation log for 20 replies | Each has a trigger type and message ID | 9 |
| 10 | Real mention phrased casually ("@Sage you there?") | Bot replies (no over-correction) | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **False-accept rate** (primary) | Under 1% of activations | Weekly sample of activations; a reviewer marks each "invited" or "not invited" from the log and the message | Over 3% |
| Activations with a logged trigger type | 100% | Activations with a trigger type and message ID divided by all activations | Any below 100% |
| Uninvited messages stored or sent to a model | 0 | Count of messages with no invitation that appear in memory or model-call logs | Any |
| "Not you" or "stop" retractions per 1,000 replies | Track; lower is better | Count user turns matching retraction cues right after a reply | Rising two weeks in a row |
| Privacy complaints about bot capture | Track; target 0 | Support tickets and admin reports tagged "bot captured" | Any |
| Missed-invitation rate (counter-metric) | Under 2% | Sample of real mentions that got no reply | Over 5% |

### Detection signals (proposed, not yet calibrated)
Signals in an event log that suggest this failure. Proposed until checked against human-labeled conversations. Written for text. Audio signals (a wake event followed by no user speech, or a device log that shows a wake with no matching invitation) are PLANNED for voice.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| A reply has trigger type "keyword" or no trigger type | Activation log | A keyword trigger the team deliberately allowed for one channel |
| User says "not you", "I wasn't talking to you", or "stop" right after a bot reply | User turn text after a reply | The user is joking, or is talking to another person about the bot |
| The bot replies to a message that mentions the bot's name as a topic (a product or a person) | Message text and reply | A real question about the bot by name with an @ |
| A reply is deleted by a member within 2 minutes | Message-delete event | A member deleting a reply the bot got wrong on content |
| An uninvited message ID appears in memory or tool-call logs | Memory writes, model-call logs | A message that was later quoted in a valid invitation |

**Starter rule:** the assistant replies and stores messages only when the message matches an explicit invitation type, and every reply logs that type.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: wake-word-false-activation
runs: pre_send
reads: [message.text, message.mentions, message.thread_parent_author, message.channel_type, channel.mute_setting, activation.trigger_type]
trigger: a message arrives that the assistant could answer, or a user says "not you" or "stop" after a reply
moves: [lead_with_answer, offer_choices, hand_off]
choices: ["Stay quiet here", "Answer only when tagged", "Keep answering", "Something else"]
on_miss: log
metric: false-accept rate
counter_metric: missed-invitation rate
status: proposed
```

## 8. Related patterns
- [AI notetaker joining a meeting without everyone's consent](../../meeting-agents/failures/recorders-that-join-without-everyone-s-consent.md): the closest pattern. There the host invited the recorder and the other people were never asked. Here no one invited the assistant at all; the trigger misfired.
- [Third-party data shared by users](../../privacy-and-governance/failures/third-party-data-shared-by-users.md): about users handing others' data to a bot on purpose. Here the bot captures it without being addressed.
- [Does the chatbot say it's a bot?](../../trust-and-rapport/failures/undisclosed-bot-identity.md): about telling people they are talking to an AI. Here the issue is who the bot should answer.
- Planned neighbors in the [roadmap](../../../roadmap/handoff-measurement-and-operations.md) (AM-04, ambient assistants acting on overheard conversation) and the [service and vertical roadmap](../../../roadmap/service-and-vertical-patterns.md) (IC-04, always-listening surprises) cover devices that act on or retain what they heard. This page covers the activation decision; those cover what happens after.

## 9. Common questions
### Why does my Slack bot reply to every message?
A common cause is subscribing to channel message events as well as mentions. Slack's `app_mention` event delivers only messages that mention the bot, and DMs use a separate event ([section 4](#4-why-it-matters)). Narrow the subscription, then filter in code ([rules 1-3](#5-the-fix)).

### How do I stop a bot from answering messages not addressed to it?
Define a short list of invitations (mention, reply to the bot, DM, command), match them as whole mentions, and stay silent otherwise ([rules 1, 2, 4](#5-the-fix)). Do not store uninvited messages ([rule 5](#5-the-fix)).

### Is it a problem if a smart speaker wakes by accident?
This page can't give legal advice. A 2020 university study reported hundreds of accidental triggers across 11 speakers, and a short audio clip can reach the maker's cloud before the device decides it was a false alarm ([section 4](#4-why-it-matters)). A $95 million Siri settlement followed allegations about unrequested recordings, which are allegations only.

### What should a bot say after it answers by mistake?
One line, then silence: acknowledge, stop, and offer a mute ([rule 7](#5-the-fix)). Repeated apologies are noise.

### Will a better model stop this?
Partly. A model can better judge whether a message was meant for it, but the trigger runs first and the product defines invitation (our judgment, not tested).

---
## Technical section

### T1. Solution architecture
```
event in -> invitation gate -> (invited) -> model + tools -> reply with trigger line
                           \-> (not invited) -> drop; log {message_id, "no_invitation"}; no memory write
invitation gate: mention | reply-to-bot | DM | slash command, minus quoted/code spans, minus channel mute
```
Put the gate before the model call and before any memory write, so an uninvited message never reaches either.

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| Narrowest event subscription | Platform app settings, reviewed at release | Compare subscribed events to the invitation list |
| Uninvited messages never stored | Gate before memory and model calls | Test channel: send uninvited messages, grep memory and model-call logs |
| Trigger type on every reply | Reply builder | Reject a reply with no trigger type in staging |

### T3. Evals
- **Dataset:** 200 messages from a test workspace: 50 real invitations, 50 look-alike names or quotes, 50 side conversations, 50 ambiguous. Label each invited or not. Start here and grow it from reviewed false accepts.
- **Judge rubric:** replied when not invited (fail); stayed silent when invited (fail); reply named its trigger; nothing stored for uninvited messages.
- **Metrics and starting thresholds:** false-accept rate under 1% and missed-invitation rate under 2% on the set. Both are starting points to tune.
- **Release gate:** block a deploy if any uninvited message reaches memory or a model call, or if either rate exceeds its alert level.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| False-accept rate (weekly sample) | Over 1% | Over 3% | Tighten the trigger; review the sampled false accepts |
| Uninvited messages stored | Any | Any in a private channel | Stop writes, delete the records, tell the admin |

### T5. Trade-offs
A narrow trigger misses casual invitations and a wide one fires on look-alikes. Start narrow, count misses, and widen with a labeled set.

---
### Deep dive (optional)
- **Modality notes (PLANNED):** for a microphone wake word, the same gate applies (explicit invitation, quiet default, log of why it woke), and the signals are false-accept events per device-hour, wakes with no user speech after them, and user "stop" commands right after a wake. None is written or measured here.
- **References:** the sources in [section 4](#4-why-it-matters).
