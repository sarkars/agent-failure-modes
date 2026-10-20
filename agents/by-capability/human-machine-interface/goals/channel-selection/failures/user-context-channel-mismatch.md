# Chatbot Channel Selection by User Context: Offering Text, Voice, or a Callback That Fits

<!-- SEO
title: Chatbot Channel Mismatch: Offer Text, Voice or Callback
description: Why a chatbot gives chat to a driver or phone-only help to a Deaf user, and how to offer fitting channels from what the user says, with rules and tests.
search phrases:
- chatbot channel selection based on user context
- chatbot accessibility for deaf and hard of hearing users
- hands-free chatbot while driving
- voice assistant noisy environment fall back to text
- how to offer text or voice option in a chatbot
- multimodal chatbot channel fallback
- ai agent offer callback instead of chat
-->

**Frequency**: Occasional

## Issue: Why a chatbot gives chat to a driver or phone-only help to a Deaf user, and how to offer fitting channels from what the user says, with rules and tests.

> **One line:** The user says something about their situation ("I'm driving," "I'm deaf," "it's too loud to hear you"), and the bot keeps pushing the one channel it started with; the fix is to offer 2-4 channels that fit what the user said and let them choose.

> **Read this first.** This page is design guidance, not legal, medical, or professional advice. Have a qualified person (a lawyer, an accessibility specialist, or a safety reviewer) review any flow before you rely on it. It states a law or standard only as far as the sources I opened say (section 4), and it makes no claim about what applies to your company. It does not say how drivers, or Deaf or hard-of-hearing people, behave or what they prefer.

| | |
|---|---|
| **Channel** | Written for **chat** (text chatbots). Voice and web signals are PLANNED, not detected or measured. |
| **Stakes** | Medium. It can block a task, and for a driver it touches safety. |
| **Who is affected** | A user who says their situation rules out the current channel: driving, a loud place, a hearing or speech limit, a meeting |
| **Frequency** | Occasional. I found no count of how often this happens. |
| **Pattern ID** | user-context-channel-mismatch |
| **Family** | [Channel selection](../README.md) |
| **Goal** | Each interaction happens in the channel that fits the job, and switching never costs the user their context. |
| **Primary metric** | Context-aware channel-offer rate: of conversations where the user states a situation cue, the share whose next bot turn offers a fitting channel. Starting target: 90%. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. A stronger model reads the cue better, but it still can only offer channels the product has and is told to offer. (Our judgment, not tested.) |
| **Also searched as** | chatbot for deaf users · hands-free chatbot while driving · voice bot in a noisy place · chatbot channel fallback · offer text or call option · multimodal channel selection |

## 1. In plain words
A user tells the bot something about where they are or what they can do. The bot ignores it and carries on in the same channel: chat for someone driving, a phone number for someone who can't hear a call, a voice prompt in a loud room. The fix is to treat that statement as a routing input. Offer a few channels that fit, let the user pick, and never guess from who the user is.

## 2. What it looks like
**Without the fix** (a delivery company's support chat)
```
User: I'm driving right now. Can I move my delivery to Saturday?
Bot:  Sure! Please type your order number and the new date.
User: Can't type. Is there another way?
Bot:  Please type your order number and the new date.
```
**With the fix**
```
User: I'm driving right now. Can I move my delivery to Saturday?
Bot:  I can do that. Since you're on the road, which works better?
      1) Short answers now, nothing to type but "yes" or "no"
      2) I text you a link to finish when you're parked
      3) A person calls you
      Or something else.
User: 2
Bot:  Done. The link is on its way. Your order and the Saturday request are saved, so you won't repeat anything.
```
**Without the fix** (a claims line)
```
User: I'm deaf. Can someone help with my claim?
Bot:  Our specialists are available by phone at 1-800-555-0100.
```
**With the fix**
```
User: I'm deaf. Can someone help with my claim?
Bot:  Yes. We can keep this in text. Which do you want?
      1) Keep going here in chat
      2) A person messages you here
      3) A relay call (we accept them)
      Or something else.
```
What changed: the bot read the user's own words, offered options that fit, did not decide for the user, and kept the current channel open.

## 3. Why it happens
- **The channel is fixed by the product, not by the conversation.** The route is set at the start (chat widget, phone line), and nothing reads later turns for a situation cue. (Our judgment.)
- **A cue is treated as small talk.** "I'm driving" or "it's loud in here" is passed to the model as content, not as a signal that changes the offer. (Our judgment.)
- **Fear of guessing wrong.** Teams avoid any context handling to avoid stereotyping, so the bot never uses what the user plainly said. (Our judgment.)

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| ADA.gov says "Covered entities must provide aids and services when needed to communicate effectively," and that covered entities "are required to accept telephone calls placed through TRS and VRS." For businesses (title III) the entity is encouraged to consult with the person about which aid is appropriate. Opened. | [ADA.gov, Effective Communication](https://www.ada.gov/resources/effective-communication/) | The page says guidance documents "have no legally binding effect." It does not address chat or email as aids and says nothing about AI agents. Not a statement about your company. |
| WCAG 2.5.6 (Level AAA) says content does not restrict "use of input modalities available on a platform" unless essential, and its intent is that people "can use and switch between different modes of input." Opened. | [W3C Understanding SC 2.5.6](https://www.w3.org/WAI/WCAG22/Understanding/concurrent-input-mechanisms.html) | Level AAA, written for web content, with motor-impairment examples. I use it only as design reasoning for letting users pick and switch. |
| In a web-assistant benchmark, Whisper Large-V3 word error rate rose from 1.4% on original speech to 28.1% on speech with injected background noise; task success on the benchmark moved from 8.4% to 6.5%. Opened. | [RealWebAssist, arXiv 2504.10445](https://arxiv.org/html/2504.10445) | Preprint; I did not check peer review. Noise was simulated with background talking and typing files, one model, a web-agent task. Not a customer-service result. Voice is PLANNED here. |
| The library's own matrix lists voice for "hands or eyes busy (driving, cooking)" and "the user's choice" for accessibility needs. | [Channel-fit matrix](../../../solutions-library/channel-fit-matrix.md) | The matrix calls itself a design heuristic, not a validated model. |

**Not opened:** NHTSA distracted-driving pages and a PDF returned access errors (HTTP 403). Nothing on this page states what is known about distraction while driving. The driving case rests on the library's heuristic above. A 2014 survey of adults with limited hearing and a vendor blog on chat for Deaf users appeared only in search summaries, so they are not used.

**Public incident:** none found. Four searches (driving distraction, Deaf and hard-of-hearing text preference, speech recognition in noise, WCAG and voice alternatives) returned no incident of a bot ignoring a stated situation.

## 5. The fix
**The principle:** When the user states a situation, offer channels that fit it, let them choose, and carry the context across.

**Do this**
1. **Log a cue only from the user's own words or actions in this conversation.** Examples: "I'm driving," "I'm deaf," "too loud to hear," "I'm in a meeting," or "can you text me instead?" Never from name, location, age, device, or a guess about a disability. Pass if every logged cue points to a user turn.
2. **Offer fitting channels in the next bot turn after a cue.** Show 2-4 options the product really has, plus "Something else," with free text open. Pass if the next bot turn has the options and "Something else."
3. **Offer, don't decide.** The user's current channel stays open, and the bot changes channel only after the user picks. Pass if no channel change happens without a user choice turn.
4. **Never refer the user only to a channel their cue rules out.** No phone-only referral after "I can't hear," no voice prompt after "it's too loud." Pass if the offer has at least one channel that fits the cue.
5. **Don't name a condition the user didn't name.** Don't write "since you're deaf" unless they said it, and don't ask about disability or health. Describe the situation: "if that's easier." Pass if no bot turn names or asks about a condition the user didn't raise.
6. **Remember the choice.** Use it for the rest of the session and don't offer again unless the user changes the situation. Pass if the same offer appears once per cue.
7. **Say so when no channel fits.** If the product has no text route, voice route, or callback that fits, say that and what happens next, then hand off. Pass if the bot never ends on a channel the cue rules out.

**Reference design** (cue to offer, a decision table; options are only those the product has)
| Cue the user stated | Options to offer (pick 2-4) | Must not be the only option |
|---|---|---|
| Driving, hands busy | Short replies, a text or link for later, a callback | Long typed forms |
| Can't hear, or hard to hear a call | Stay in chat, a person messages here, a relay call | A phone number, a voice prompt |
| Loud place | Stay in chat, a text summary, a callback later | A voice-only step |
| Can't talk right now (meeting, shared space) | Stay in chat, a text summary, a callback later | A voice-only step |
| Asks for another channel | That channel, with a one-line reason and what carries over | Staying in the old one |

State kept per session (proposed): `context_cue` (text and user turn id), `offered_channels`, `channel_choice`, `cue_cleared`.

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices | The user states a cue: "Keep going in chat," "Text me a summary," "A person messages or calls me," "Something else" |
| Ask one clarifying question | The cue is unclear ("It's a bit loud"): "Would a text summary be easier?" |
| Hand off to a person | No fitting channel exists, or the user asks for a person; send the [handoff packet](no-channel-switch-or-context-lost.md) |

**Don't over-correct.** Don't ask every user about their situation, and don't offer channels with no cue. Offer once per cue. Don't remove chat or push a switch. Don't lecture. Treat "I've parked" or "I'm home" as the end of the cue. A user may be driving and still choose to chat.

**Hand-off rule.** Hand off to a person who accepts text or relay when no fitting channel exists, after two declined offers that did not help, or when the user asks. Send what has been said so far. If no person is available, say when one will be and offer a text callback.

**Framework used:** [Channel-fit matrix](../../../solutions-library/channel-fit-matrix.md), the "Offer, don't force" step.

## 6. How to test it (short version)
All tests: **Not yet run.**

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | The user says "I'm driving" in turn 2; the name and location in the profile hint at nothing | The cue log cites turn 2; no cue comes from the profile | 1 |
| 2 | The user says "I'm deaf" | Next bot turn offers 2-4 channels plus "Something else" | 2 |
| 3 | After the offer, the user types an ordinary chat question | The bot answers in chat; no channel switch | 3 |
| 4 | The user says it's too loud to hear; the bot has a phone line and chat | The offer includes chat or a text summary, not only the phone line | 4 |
| 5 | Scan bot turns after "I can't hear" | No turn names or asks about a condition the user didn't name | 5 |
| 6 | The user picks "text me a summary," then asks two more questions | The offer is not repeated | 6 |
| 7 | The product has no text route and the user says they can't hear | The bot says so, says the next step, and hands off | 7 |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given. None is sourced.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Context-aware channel-offer rate (primary) | 90% | Cue events with a fitting offer in the next bot turn, divided by cue events | Below 80% |
| Offers that include "Something else" | 100% | Check the offer event's option list | Any miss |
| Channel changes without a user choice | 0 | Channel-change events with no preceding user choice turn | Any |
| Referrals only to a channel the cue rules out | 0 | Sampled review of cue conversations | Any |
| Repeat offers after a choice | Under 5% | Offer events after a channel_choice is set | Over 10% |
| Accessibility complaints tied to channel | Trend down | Count tagged complaints per 1,000 conversations; review each | Any new one |

### Detection signals (proposed, not yet calibrated)
Written for chat events. Voice and web versions are PLANNED only.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User states a cue and the next bot turn has no channel offer | Cue event, then the next bot turn's option list | The user's request ends in one short reply |
| Bot gives only a phone number or a voice step after the user said they can't hear or can't talk | Bot turn text after the cue event | The user later asks for a call |
| User repeats the cue ("I told you I'm driving") | User turn text after an earlier cue | The user is adding new detail |
| Channel changes with no user choice turn before it | Channel-change event | The user asked for the change in the same turn |

**Starter rule:** Rule 2: after a user states a situation, the next bot turn offers 2-4 fitting channels plus "Something else."

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: user-context-channel-mismatch
runs: pre_send
reads: [user_turn_text, session.context_cue, product.available_channels, session.channel_choice]
trigger: the user has stated a situation cue and the bot is about to reply
moves: [offer_choices, ask_clarifying_question, hand_off]
choices: ["Keep going here in chat", "Text me a summary", "A person messages or calls me", "Something else"]
on_miss: rewrite
metric: context-aware channel-offer rate
counter_metric: channel changes without a user choice
status: proposed
```

## 8. Related patterns
- [Voice-only flows with no text alternative](../../accessibility/failures/voice-only-flows-with-no-text-alternative.md) - that page is a product gap: a voice flow with no text route at all, found by auditing journeys. This page is about the live conversation: reading what the user said and offering fitting channels, for drivers and noisy places as well as Deaf and hard-of-hearing users.
- [No channel switch or context lost](no-channel-switch-or-context-lost.md) - covers a switch that loses context. This page covers whether the right channel is offered at all; rule 6 here relies on that page's handoff packet.
- [Complex or emotional discussion forced into chat](complex-or-emotional-discussion-forced-into-chat.md) - the topic outgrows chat. Here the user's situation, not the topic, drives the offer.

## 9. Common questions
### How should a chatbot offer a voice or text option?
Offer it in the next turn after the user states a situation, as 2-4 choices plus "Something else," and keep the current channel open (rules 2 and 3).

### Can a chatbot tell that a user is driving or Deaf?
Not from who they are, and it shouldn't try. Use only what the user says or does in the conversation (rule 1), and never name a condition they didn't name (rule 5).

### What if the product has no text or relay option?
Say so, say what happens next, and hand off to a person who accepts text or relay (rule 7). Whether the law requires more is for your own reviewer; see the note at the top.
