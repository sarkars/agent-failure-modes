# Too Many Notifications From an AI Assistant: Notification Overload

<!-- SEO
title: Too Many Notifications From an AI Assistant: How to Fix It
description: An assistant that sends too many pushes, alerts, and badges gets muted or deleted. Set a weekly budget per user, ask first, label urgency, and give real controls.
search phrases:
- ai assistant sends too many notifications
- how to stop chatbot push notifications
- how many push notifications per week is too many
- notification fatigue app design
- how to let users control notification frequency
- chatbot notifications opt out
- notification settings best practices for apps
-->

**Frequency**: Common

## Issue: An assistant that sends too many pushes, alerts, badges, and digests gets muted or uninstalled; cap the volume per user, ask first, label urgency honestly, and make every type easy to turn down.

> **One line:** Each team adds one more alert that seems useful, and nobody counts what one person receives in a week, so the user turns everything off.

> **Read this first.** This is design guidance, not legal advice. Rules on messages and opt-outs vary by channel (email, text, push) and by state, and change. The legal statement in section 4 comes from one FTC page about email only. Have counsel review your consent flow, message types, and opt-out handling before launch.

| | |
|---|---|
| **Channel** | Written for **chat assistants** and the notifications around them: push, badges, in-app alerts, and the cards or widgets that announce themselves. Voice and always-listening devices are PLANNED, not covered. |
| **Stakes** | Low for a tip. Medium to high when noise buries a real alert (a failed payment, a security warning). |
| **Who is affected** | Anyone who installs an assistant app or turns on its alerts; people who use a Focus or Do Not Disturb mode; users with attention or cognitive limits. |
| **Frequency** | Common (our judgment). The surveys in section 4 show many people turn alerts down; I found no count for AI assistants. |
| **Pattern ID** | notification-overload |
| **Family** | Visual ([family README](../README.md)) |
| **Goal** | What an agent shows is clear, honest, accessible, and appropriate to the stakes. (Row goal: notifications are rare, useful, and controllable.) |
| **Primary metric** | Notifications per user per week (all channels together); opt-out rate. Starting target: set a cap per notification type from your baseline, and alert when opt-outs rise after a release. Starting points, not from a source. |
| **Maturity** | Researched |
| **Will a better model fix this?** | No. How many alerts exist, which team owns them, and what the user can switch off are business and product choices, not model skills. (Our judgment, not tested.) |
| **Also searched as** | too many push notifications · notification fatigue · assistant won't stop pinging me · turn off app alerts · notification spam · alert overload |

## 1. In plain words
Every alert is justified by the team that sends it, and together they bury the user. The assistant sends a reminder, a tip, a digest, a "we miss you," and a badge, and the person either mutes the app or removes it. Count what one user receives per week across all channels, cap it, ask before sending, say why each one came, and let people turn down each type separately.

## 2. What it looks like
A budgeting assistant app. Dana installed it to check her balance.

**Without the fix**
```
Mon 8:00   Push: Good morning, Dana! Your weekly insights are ready.
Mon 12:30  Push: You haven't set a goal yet. Tap to start!
Tue 9:15   Push (marked urgent): 20% off Premium, today only
Tue 18:00  Push: Dana, your spending summary is ready
Wed 8:00   Push: Don't forget to check in!
Wed 8:05   Badge: 7 unread
(Dana opens Settings: one switch, "Notifications". She turns it off.)
(Thursday: her card is declined. The assistant's warning never reaches her.)
```
**With the fix**
```
(First launch: no permission request.)
Dana taps the bell on her balance card.
Assistant: Want alerts? Pick what you'd like. [Low balance and declined payments] [Weekly summary, Mondays] [Tips] [Something else]
Dana: Low balance and declined payments
(Week 1: 1 push.)
Thu 14:02  Push: Your card was declined at Metro Gas for $62.40. Open to review. (Sent because you chose "Low balance and declined payments." Mute 1 week | Settings)
```
The fixed assistant asked at a moment of interest, sent only what she chose, said why, and kept a way to mute inside the alert.

## 3. Why it happens
- **Every team owns one alert and nobody owns the total.** A reminder, a promo, and a digest each pass their own review, and no one counts what one user receives (our reading).
- **Teams are rewarded for opens and re-engagement.** Sends and taps count as wins, while mutes and uninstalls show up late or in another report (our reading).
- **Settings are one switch.** With a single on/off control, the only way to reject the tips is to also lose the payment warning.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In a June 2021 YouGov survey of 1,167 US adults, when push notifications from an app are too frequent: 42% would change notification settings, 39% would turn notifications off entirely, 8% would delete the app, 9% would do nothing. Margin of error 4.2%. | [YouGov, *How consumers feel about push notifications*, 2021](https://yougov.com/en-us/articles/36287-how-consumers-feel-about-push-notifications-2021). Opened and read through a fetch-tool summary. | Stated intentions in a survey, not logged behavior. Push notifications in general, not AI assistants. |
| Apple's guidelines: "You need to get permission before sending any notification." People can silence all notifications. Be "as realistic as possible when assigning an interruption level" so people do not feel a high urgency level is used for low-priority information. Do not send marketing notifications unless people explicitly agree, and "never use the Time Sensitive interruption level to send a marketing notification." Provide an in-app settings screen. | [Apple HIG, *Managing notifications*](https://developer.apple.com/design/human-interface-guidelines/managing-notifications). Opened and read. | A platform's design rules, not an experiment. Apple platforms only. |
| Android's guide: to avoid "flooding your users with multiple or redundant notifications," update an existing notification instead of issuing a new one, or group them. Users can disable a specific channel "instead of disabling all your notifications." | [Android Developers, *Notifications*](https://developer.android.com/develop/ui/compose/notifications). Opened and read. | A platform guide, not an experiment. It does not give a per-week limit. |
| On Android 13 and higher, notifications are off by default until the user grants the `POST_NOTIFICATIONS` permission. The guide says to let users "familiarize themselves with your app" first and to ask in context, so it is clear "what the notifications are used for." | [Android Developers, *Notification runtime permission*](https://developer.android.com/develop/ui/views/notifications/notification-permission). Opened and read. | Android platform behavior, not a measure of how many alerts are too many. |
| Notifications that demand attention at inopportune moments are more likely to disrupt than help; intelligent systems try to infer the right time and context. | [Mehrotra and Musolesi, arXiv 1711.10171](https://arxiv.org/abs/1711.10171). Abstract opened; full paper not read. | A 2017 survey of phone and desktop systems, not chat assistants. |
| FTC: CAN-SPAM covers commercial email; "You must honor a recipient's opt-out request within 10 business days"; each separate violating email can bring penalties of up to $53,088. The page does not say whether the Act covers text messages or push notifications. | [FTC, *CAN-SPAM Act: A Compliance Guide for Business*](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business). Opened and read through a fetch-tool summary. | Email only. I did not open any source on push or SMS law; for SMS opt-outs see [proactive outreach overreach](../../relational-and-boundaries/failures/proactive-outreach-overreach.md). |

**Not found.** I found no source that gives a safe number of notifications per week, and I did not open a study that isolates volume as the cause of opt-outs in AI assistants. Vendor-blog figures from search results are not used. I used no incident.

## 5. The fix
**The principle:** Give each user a small weekly budget across all channels, send only what they asked for, say why it came, and let them turn down each type on its own.

**Do this**
1. **Count per user, across channels.** Keep one counter of pushes, badges, in-app alerts, emails, and texts per user per week. Check: the dashboard shows one number per user, not one per team.
2. **Set a cap per notification type and a total cap.** Pick starting numbers from your baseline. Check: no user exceeds the total cap in a week; excess is queued, merged, or dropped.
3. **Ask before the first send, in context.** Do not request notification permission at first launch. Ask after the user does something that signals interest (taps a bell, follows a topic, places an order), and say what the notifications will be (Android guide). Check: the permission request follows a user action and names the types.
4. **One switch per type.** Separate payment and security alerts, reminders, summaries, tips, and promotions. Check: each type can be turned off without turning off the others (Android channels; Apple asks for an in-app settings screen).
5. **Marketing is its own opt-in and never urgent.** Check: promotional sends have a recorded opt-in and an urgency label below "time sensitive" (Apple).
6. **Label urgency honestly.** Use "urgent" only for something happening now that affects the person (a declined payment, a security issue). Check: every urgent send maps to an allowed reason on a short list.
7. **Merge instead of repeating.** If there is a newer update on the same thing, update the existing notification instead of sending another (Android). Check: no two sends about the same item within a day.
8. **Say why this was sent and put mute in it.** Each notification names the setting that caused it and offers "Mute 1 week" and "Settings." Check: both are present in 100% of sends.
9. **Back off when ignored.** After a set number of consecutive notifications with no open (start at 3, to tune), halve that type's frequency, then offer once: "These aren't useful? [Fewer] [Stop]." Check: the sequence is logged.
10. **Honor a mute or off right away.** Check: no send of that type after the user's choice; for email, the FTC page sets 10 business days as a legal outer limit, not a design target.

**Reference design**
```
Notification gate (runs before every send, all channels)
- Input: user, type (alerts | reminder | summary | tip | promo), urgency, item_id, channel
- If the user's setting for this type is off or muted -> drop.
- If promo and no recorded promo opt-in -> drop.
- If urgency = urgent and type not in the allowed-urgent list -> downgrade to normal.
- If an unread notification for item_id exists -> update it, do not add.
- If sends this week for user >= total cap, or for the type >= its cap
    -> urgent from the allowed list goes through; everything else is queued for the digest or dropped.
- Render: one line of value + why ("because you chose ...") + [Mute 1 week] [Settings].
- Log: sent, merged, queued, dropped (with reason), opened, muted, opted out.
```
```
Prompt block (for the assistant's own proactive messages):
Do not message the user first unless they turned that type on. Say in one line why you are writing.
If they have not opened your last 3 messages, stop and ask once whether to send fewer or none.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Offer choices: 2-4 options plus "Something else", free text open | At the first permission ask and after three ignored sends: "Payments only", "Weekly summary", "Tips", "Something else". Do not offer them when the user already set a preference, or when the alert is urgent and safety-related (send it; do not ask). |
| Ask one clarifying question | The user says "too many messages": ask which kind bothers them. Do not ask when "Stop" was clear; just stop. |
| Hand off to a person | The user reports that alerts continue after they turned them off. Do not hand off for a simple "fewer, please". |

**Don't over-correct.** Do not hold back alerts the user needs (a failed payment, a deadline today, a security warning) to stay under the cap. Urgent items on the allowed list go through the gate. Do not hide all controls behind a long ask; the user must be able to mute without a conversation.

**Hand-off rule.** If a user says notifications continue after they turned them off, switch off all non-urgent types for them, confirm in the chat, and route the case (with the send log) to a person or support queue.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Replay a week of send events for a test user through the gate.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Six triggers fire for one user in a week; total cap is 4 | At most 4 sent; the rest queued or dropped with a reason (1, 2) |
| 2 | New install, first launch | No permission request; request follows a bell tap and names the types (3) |
| 3 | User turns off "Tips" | Payment alerts still arrive; no tip arrives (4, 10) |
| 4 | A promo send with no promo opt-in | Dropped (5) |
| 5 | A "20% off" promo marked urgent | Downgraded; not sent as urgent (5, 6) |
| 6 | Two updates on the same item in one day | One notification, updated (7) |
| 7 | Any rendered notification | Shows why and has Mute 1 week and Settings (8) |
| 8 | Three sends in a row, none opened | Frequency drops; user offered "Fewer / Stop" once (9) |
| 9 | Declined-payment alert while at cap | Delivered as urgent (6, reference design) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Notifications per user per week** (primary, with opt-out rate) | At or under the cap you set per type | Count sent notifications per user per week across all channels, from the send log | Any user over the total cap; median rising two weeks in a row |
| **Opt-out rate** (primary, paired) | Set from baseline | Users who turn off a type or all, or deny permission, divided by users sent that type, within 7 days | Rising after a release |
| Sends that pass the gate with a reason shown and mute offered | 100% | Audit rendered notifications | Below 95% |
| Mislabeled urgent sends | 0 | Urgent sends whose reason is not on the allowed list | Any |
| Ignored-streak backoffs triggered | Track; set from baseline | Users with 3+ unopened sends who got a frequency cut | Falling to 0 (the rule may be off) |
| Missed urgent alerts (counter-metric) | 0 | Urgent items queued past a short delay, or dropped by the cap | Any |

### Detection signals (proposed, not yet calibrated)
Proposed until checked against human-labeled event logs. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once published.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User exceeds the weekly cap | Send log, count per user | A week with several user-requested alerts |
| User turns off all notifications within a day of a send | Settings change event after a send | A planned vacation or a Focus the user set |
| Several unopened sends in a row | Send events with no open event | The user reads them on the lock screen |
| Same item notified more than once in a day | Send log by item_id | Different stages of one order the user asked to follow |
| Promo send without a stored opt-in | Send event with consent field empty | A transactional message about a purchase |

**Starter rule:** every notification is sent only for a type the user turned on, stays within that user's weekly cap, says why it was sent, and offers mute.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: notification-overload
runs: pre_send
reads: [user.notification_settings, user.sends_this_week, send.type, send.urgency, send.item_id, user.consent.promo, user.recent_opens]
trigger: a notification or proactive message is about to be sent
moves: [offer_choices, ask_clarifying_question, hand_off]
choices: ["Payments only", "Weekly summary", "Tips", "Something else"]
on_miss: log
metric: notifications per user per week; opt-out rate
counter_metric: missed urgent alerts
status: proposed
```

## 8. Related patterns
- [Interrupts at a bad moment](../../proactive-and-ambient/failures/interrupts-at-a-bad-moment.md): the closest page. It covers the timing of a single proactive message (not while the user is typing). This page covers the total volume per user across channels, and controls.
- [Dismissed suggestions come back](../../proactive-and-ambient/failures/dismissed-suggestions-come-back.md): one dismissed item returns. This page covers volume across all items.
- [Proactive outreach overreach](../../relational-and-boundaries/failures/proactive-outreach-overreach.md): the bot contacts people without consent and ignores "stop" (text and in-app). This page covers people who did opt in but receive too much.
- [Summaries and digests too long to read](../../proactive-and-ambient/failures/summaries-and-digests-too-long-to-read.md): the length of one digest, not how many alerts arrive.
- [Message bursts](../../response-structure/failures/message-bursts.md): many messages inside one reply in a chat.
- [Quiet hours and time zones ignored](../../outbound-messaging-agents/failures/quiet-hours-and-time-zones-ignored.md): when outbound texts arrive, not how many.
- [Dark patterns](dark-patterns.md): a hidden or hard-to-find opt-out is that pattern as well.

## 9. Common questions
### How many notifications per week is too many?
I found no sourced number. A survey (YouGov, 2021) shows 39% would turn notifications off if they were too frequent ([section 4](#4-why-it-matters)). Set a cap per type from your own baseline and watch the opt-out rate.

### How do I let users control notification frequency?
Give one switch per type, a mute inside each notification, and an in-app settings screen (rules 4 and 8). Apple and Android both describe user controls like these.

### Should the assistant ask permission before sending notifications?
Yes. Apple says you need permission before sending any notification, and on Android 13 and higher notifications are off until the user grants it. Ask after a user action, not at first launch (rule 3).

### Can marketing notifications be marked urgent?
No. Apple says never to use Time Sensitive for marketing. Mark urgent only what is happening now and affects the person (rule 6).

### What if a user says they are getting too many messages in the chat?
Ask which kind bothers them, offer "Fewer" or "Stop" for that type, and apply it at once (rule 10). If alerts keep coming, hand off (hand-off rule).

---
## Technical section

### T1. Solution architecture
```
trigger sources (promo, reminder, summary, alert) -> notification gate (settings, consent, cap, merge, urgency)
  -> channel router (push | badge | in-app | email | text) -> render (why + mute) -> send/open/mute log
```
### T2. Guardrails
| Rule | Enforced where | How checked |
|---|---|---|
| Single send gate for all teams and channels | Notification service | No sender bypasses it (code review, log scan) |
| Promo requires stored opt-in | Gate | Test 4 |
| Urgent reasons come from a short list | Gate | Test 5 |

### T3. Evals
- **Dataset:** a week of real or synthetic send events for 50 test users with different settings.
- **Judge rubric:** was each send allowed by settings, within cap, correctly labeled, and rendered with why and mute?
- **Metrics and starting thresholds:** cap breaches 0; mislabeled urgent 0; missed urgent 0. Starting points to tune.
- **Release gate:** block a deploy that adds a send path outside the gate.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Opt-out rate after a release | Rising vs. last 4 weeks | Doubling | Find the new notification type; pause it |

### T5. Trade-offs
- A cap can delay a useful alert; the allowed-urgent list is the safeguard.
- A single gate needs every team to route through it, which takes organizational work.

---
### Deep dive
- **Open questions.** I found no study of AI-assistant notifications and no sourced weekly limit. Voice and wearable versions are PLANNED.
- **References.** [YouGov, 2021](https://yougov.com/en-us/articles/36287-how-consumers-feel-about-push-notifications-2021); [Apple HIG](https://developer.apple.com/design/human-interface-guidelines/managing-notifications); [Android notifications](https://developer.android.com/develop/ui/compose/notifications); [Android permission](https://developer.android.com/develop/ui/views/notifications/notification-permission); [Mehrotra and Musolesi](https://arxiv.org/abs/1711.10171); [FTC CAN-SPAM](https://www.ftc.gov/business-guidance/resources/can-spam-act-compliance-guide-business).
