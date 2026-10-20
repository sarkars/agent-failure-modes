# Chatbot Instructions Too Technical for the User: Technology-Literacy Mismatch

<!-- SEO
title: Chatbot Instructions Too Technical for the User: Fix It
description: A chatbot tells users to "clear the cache" or "open Settings" when they can't. Match the steps to the skill the user shows in the chat, never to who they are.
search phrases:
- chatbot instructions too technical for users
- how to make a chatbot explain things to non-technical users
- chatbot assumes user knows tech terms
- chatbot step by step instructions for beginners
- AI agent adapt to user skill level
- chatbot jargon confuses customers
- chatbot novice vs expert users
-->

**Frequency**: Common

## Issue: A chatbot gives instructions that assume skills and vocabulary the user has not shown; the fix is to read the user's own words and actions, match the steps and terms to that, and offer a simpler or a faster path.

> **One line:** The bot says "clear your cache and re-authenticate in the admin console" to a user who just asked where the "Settings" button is, so the user can't finish the task, and an expert gets the opposite problem: a slow tour of things they already know.

> **Read this first.** This page is design guidance, not legal, clinical, or professional advice. Review it with your own team (and accessibility specialists) before use. It cites no law. **Do not infer skill from age, accent, name, spelling, or any identity.** Infer it only from what the user says and does in this conversation.

| | |
|---|---|
| **Channel** | Written for **chat** (text). Screen-share, voice, or web click-path signals are **PLANNED**, not written. |
| **Stakes** | Low to high (a stuck password reset is low; a failed benefits form or bank step is high) |
| **Who is affected** | Any user whose demonstrated skill differs from the skill the instructions assume, in either direction. |
| **Frequency** | Common. Observed in practice; I found no count of how often bots do this. |
| **Pattern ID** | technology-literacy-mismatch |
| **Family** | [Cultural adaptation](../README.md) |
| **Goal** | Each user gets communication that fits how they communicate, with no stereotype-based assumptions. |
| **Primary metric** | Task-completion parity by signalled skill level: completion rate of conversations where the user signalled low skill, divided by the rate for users who signalled high skill, same task types. Starting target to tune: 0.9 or higher. |
| **Maturity** | Researched |
| **Will a better model fix this?** | Partly. A better model writes plainer steps and notices more cues, but the product still has to confirm the skill with the user, keep the steps small, and offer a person (our judgment, not tested). |
| **Also searched as** | chatbot too technical · chatbot jargon · chatbot assumes I know how · bot instructions for beginners · chatbot explain like I'm new |

## 1. In plain words
People differ in how much they know about phones, apps, settings, and technical terms. A bot that writes every answer for a power user loses the beginner, and one that explains everything slowly annoys the expert. The fix is to listen to what this user says ("I can't find it", "what is a browser tab") or does (names a command, pastes an error code), match the steps to that, and check with them.

## 2. What it looks like
**Without the fix** (a bank's web chat, evening)
```
User: I cant get into my account on my phone, it says something about verifying
Bot:  Please clear the app cache, reinstall the app, then re-enroll your device via
      Settings > Security > Device Management and approve the push notification.
User: where is settings
Bot:  Settings is under the Security tab in Device Management.
User: i dont know what that is. never mind
```
**With the fix**
```
User: I cant get into my account on my phone, it says something about verifying
Bot:  I can help. Which is closer to what you see: a screen asking for a code, a screen
      saying "verify this device", or something else?
User: verify this device. where is settings
Bot:  That's fine, I'll go one small step at a time. Step 1 of 3: find the app named
      "Settings" on your phone. It has a gear icon. Tell me when you see it, or tell me
      what you see instead. If you'd rather, I can connect you to a person.
```
The fixed bot answers the question the user asked, uses the user's own words, sends one step, and keeps a person one message away. It did not guess anything about who the user is. "Where is settings" was the signal.

## 3. Why it happens
- **The prompt writes for one reader.** The system prompt and help content come from people who know the product well, so the default answer is the expert's runbook.
- **No skill state.** Nothing in the conversation records what this user has shown they can do, so the same level repeats after the user says "I don't know what that is".
- **Rewording is not simplifying.** When a user is lost, the bot swaps synonyms for the same steps instead of cutting the number of steps or the assumed knowledge.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a 2015 Pew survey, 26% of internet users age 65 and older said they feel very confident using computers, smartphones or other devices to do what they need online; 23% said a little confident and 11% not at all. On a separate item, 48% of adults 65 and older said needing someone to show them how to use new devices describes them very well and 25% somewhat well. | [Pew Research Center, 2017](https://www.pewresearch.org/internet/2017/05/17/barriers-to-adoption-and-attitudes-towards-technology/) (opened) | Self-reported, 2015 data, one age group. The page gives no sample size or field dates. It shows confidence varies; it must not be used to guess any user's skill from age. |
| Pew's 2016 Digital Readiness Gaps report sorted US adults into five groups on digital skills and trust; 14% were "Unprepared" (low skills and trust, and in this report the least digitally ready) and 17% "Digitally Ready". | [Pew Research Center, 2016](https://www.pewresearch.org/internet/2016/09/20/digital-readiness-gaps/) (opened) | Built around online learning only, and the report says the findings may not apply to other digital tasks. Group edges are fluid. A 2015 snapshot, and no sample size was visible on the page I opened. |
| In 25,000 Bing Copilot conversations, the agent answered at a "proficient or expert" level in 77% of them. User experience got worse when the agent answered below the user's own expertise level, more so on complex tasks, and users wrote more when levels matched. | [Palta et al., arXiv 2502.18685, 2025](https://arxiv.org/abs/2502.18685) (abstract only) | Domain expertise in a general assistant, not technology literacy in support chat. The abstract as I read it describes answers pitched *below* the user; I did not read the paper, so I make no claim about answers pitched above the user. A preprint. |

**What I did not find:** a count of how often support bots lose users to jargon, and a public incident of this failure, so there is no `incidents/` page. I searched for OECD adult problem-solving results; that page returned 403 and I did not open it. Treat any figure about adult technology skills not in the table as unverified.

## 5. The fix
**The principle:** Pitch each step at the skill the user has shown in this conversation, check with them when it matters, and never from who they are.

**Do this**
1. **Infer skill only from this conversation.** Allowed signals: what the user asks ("where is settings"), terms they use or ask about, steps they report doing or failing, and what they say about themselves ("I'm not good with phones", "I'm a developer"). Never use age, name, accent, location, spelling or grammar, or typing speed.
2. **Start with plain defaults:** common words, no unexplained term, one action per sentence, and name where something is ("the app with the gear icon").
3. **Define a needed term once, in the same message,** in a few words, and use the same word after that ("text message", not "SMS" then "OTP").
4. **Step down on a low-skill signal.** When the user asks where something is, asks what a word means, or does a different step than asked, cut to one step per message with "Step 1 of N" and wait for a reply. Rewording the same steps does not count as stepping down.
5. **Step up on a high-skill signal.** When the user names a tool, pastes an error code, or says they already tried a step, drop the explanations and give the shortest correct path. Never repeat a step the user said they did.
6. **Ask once, don't announce.** If the signals are mixed and the next step is risky or costly to redo, ask one question ("Do you see a gear icon, or should I describe where to look?"). Never say "since you seem new to this".
7. **Offer a person after two steps in a row go wrong,** with a summary of the steps done and where the user stopped. The summary lists steps, not a skill label.
8. **Keep the skill estimate editable.** Any "just tell me the steps" or "slow down" overrides it at once, and the bot never records it as a trait of the user across sessions.

**Reference design: skill signal state** *(per conversation; starting point, never from identity)*
```json
{ "level": "unknown | low | high", "evidence": ["asked where Settings is", "asked what 'cache' means"],
  "terms_defined": ["cache"], "failed_steps": 1, "user_override": null }
```
| Level | Steps per message | Terms | Extras |
|---|---|---|---|
| unknown | One or two | Plain, defined once | One check question only if the step is risky |
| low | One, with "Step 1 of N" | Plain, defined once, same word every time | Person offered after two failed steps |
| high | Full path | Names allowed | No repeats of what the user did |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); list only the moves that apply, most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The user asks where something is or what to do: answer that first, in plain words, before any background. Do not open with a tour. |
| Ask one clarifying question | Signals are mixed and the next step is risky or costly to redo: one question about what they see. Do not ask when a wrong guess is harmless. |
| Offer choices: 2-4 options plus "Something else", free text open | The user is lost and the bot can pitch the next step more than one way: "Short steps", "Show me where to tap", "Talk to a person", "Something else". Do not offer them when the user's words already show the level. |
| Hand off to a person | Two steps in a row went wrong, or the user asks. Do not hand off a user who is progressing and wants to stay with the bot. |

**Don't over-correct.** Do not slow down or simplify for every user, add "simple words" to everyone, or talk down ("Great job tapping that!"). Do not assume low skill from a typo or a short message. Do not state or log a level as a label for the person. Do not hide the advanced path: a user who steps up should get it with no friction. Keep one pitch per user; do not swing between turns.

**Hand-off rule.** Two failed steps in a row, a request for a person, or a failed step at a money, health, or benefits task goes to a person with a summary of steps done. See [talk to a human ignored or looped](../../human-handoff/failures/talk-to-a-human-ignored-or-looped.md) and [cold transfer](../../human-handoff/failures/cold-transfer.md).

**Framework used:** None yet. Planned: a skill-signal review with usability specialists.

## 6. How to test it (short version)
Tests are designs, **Not yet run**. A full test file is not yet written.
| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | User asks "where is settings" after a jargon-heavy reply | Next reply is one step in plain words with "Step 1 of N" (2, 4) |
| 2 | User asks what "cache" means | The term is defined once in a few words and used the same way after (3) |
| 3 | User pastes an error code and says they already restarted | Short path, no restart step repeated (5) |
| 4 | Same typo-filled, short message sent under four different names, ages stated or not | Same pitch for all; no skill inferred from spelling or name (1) |
| 5 | Mixed signals before a step that is hard to undo | One clarifying question, no label said aloud (6) |
| 6 | Two steps fail in a row | Person offered with a steps-done summary and no skill label (7) |
| 7 | Fast user who needs no help | No simplified mode, no extra explanations (Don't over-correct) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| Task-completion parity by signalled skill level (primary) | 0.9 or higher | Completion rate of conversations with a low-skill signal, divided by the rate for high-skill-signal conversations, same task types; signals from message text only | Below 0.8 |
| Replies with an undefined technical term after a low-skill signal | Under 5% | Term-list lint on bot replies following a signal | Over 15% |
| "Where is" or "what is" follow-ups to the bot's steps | Trend down | Intent classifier on user turns right after a step message | +25% vs baseline |
| Repeated steps sent to users who said they did them | 0 | Sampled review or step-log match | Any |
| Skill levels set from non-message input | 0 | Audit that the estimator reads message text only | Any |
| Person offered after two failed steps | 100% | Conversations with two failed steps and a person offer | Under 95% |
| Step-down offers declined or overridden within 2 turns | Under 20% | Overrides over step-down moves | Over 35% |

### Detection signals (proposed, not yet calibrated)
Signals in a conversation event log that suggest this failure. Proposed until checked against human-labeled conversations. All are written for text.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User asks where something is or what a word means right after a bot step message (`turn.where_or_what_followup`) | Intent in the next user turn, quoting a term from the bot reply | A user checking a detail, not lost; or a question about a product term |
| User reports a different step than the one asked (`step.mismatch`) | Flow state versus user turn | A user skipping ahead because they already know the step |
| Bot reply contains a technical term not on the plain-word list, after a low-skill signal (`bot_draft.undefined_terms`) | Term-list lint hit | The user used the term first |
| Bot repeats a step the user said they did (`step.repeat_after_done`) | Step log versus user turn | The user's claim failed a check, so the repeat is needed |
| User ends with "never mind" or "forget it" within two turns of a step message (`turn.abandon_phrase`) | User turn text | The user got help elsewhere or changed their mind for a new reason |

**Starter rule:** Pitch each step at the skill the user has shown in this conversation, never at who they are, and define any needed term once. *(Pattern ID: technology-literacy-mismatch)*

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: technology-literacy-mismatch
runs: pre_send
reads: [user_messages.text, session.skill_signals, step.mismatch, bot_draft.undefined_terms, step.failed_count]
trigger: a step reply is about to be sent and the user's messages show a skill signal or the draft holds an undefined term
moves: [lead_with_answer, ask_clarifying_question, offer_choices, hand_off]
choices: ["Short steps", "Show me where to tap", "Talk to a person", "Something else"]
on_miss: rewrite
metric: task-completion parity by signalled skill level
counter_metric: step-down offers declined or overridden within 2 turns
status: proposed
```

## 8. Related patterns
- [One-size communication style](one-size-communication-style.md): the same family. It adapts directness, formality and idioms to how the user writes. This one adapts the steps and technical content to what the user can do, so a user can write formally and still need one step at a time.
- [Older or cognitively impaired users](../../vulnerable-users/failures/older-or-cognitively-impaired-users.md): a user who needs more time or simpler steps, triggered by repeats and confusion, with an opt-in slower mode. It is built around cognitive and age-related need and a person offer. This page is about skill and know-how with a tool, which fits a young expert in an unfamiliar app as well as a user with no tech background, and it also steps up for experts. A user can need both.
- [Language that is hard for people with cognitive disabilities](../../accessibility/failures/language-that-is-hard-for-people-with-cognitive-disabilities.md): about wording accessibility; this page is about the steps and prior knowledge assumed.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the "ask one question" move when signals are mixed.
- [Blames the user](../../errors-and-recovery/failures/blames-the-user.md): "you should have known" wording that makes a skill gap worse.
- [Dialect and name quality gap](../../fairness-and-identity/failures/dialect-and-name-quality-gap.md): the fairness check behind the "never infer from spelling or name" rule.

## 9. Common questions
### How should a chatbot explain things to non-technical users?
Use plain words, define a needed term once, and send one step at a time when the user shows they are lost (rules 2 to 4). Check with a question when the step is hard to undo, and offer a person after two failed steps.

### How does a bot know a user's tech skill without asking?
It reads what they say and do in the chat: asking where a button is, asking what a word means, naming a command, pasting an error. It does not use age, accent, name, or spelling. Section 4 shows self-reported confidence varies widely, which is why the bot should not guess from who someone is.

### Should I add a "beginner mode" and an "expert mode"?
Offer choices tied to what they do ("Short steps", "Just the steps") and let any user pick or switch. A fixed label sorts people by assumption and fails the user who is expert in one app and new in another.

### Does matching the answer to the user's level improve results?
One 2025 Bing Copilot analysis found worse experience when answers were pitched below the user's expertise (section 4). That is domain expertise in a general assistant, so this page's targets are starting points that still need testing on your own data.
