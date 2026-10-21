# Smart Home Assistant Turns Off the Wrong Light: Commands Go to the Wrong Device or Room

<!-- SEO
title: Smart Home Assistant Turns Off the Wrong Light or Room: Fix
description: Why "turn off the light" hits a TV or another room's light on Alexa or Google Home, and a fix: resolve the target by room and ask when it is unclear.
search phrases:
- alexa turns off wrong light
- alexa turned on the tv when i said lights
- google home turns on every light in the room
- google home controls devices in the wrong house
- smart speaker turns off wrong room
- alexa wrong room device group
- chatbot controls the wrong smart home device
-->

**Frequency**: Common

## Issue: A smart home assistant sends a command such as "turn off the light" to a different light, device, or room than the one the person meant, and does not say which one it acted on.

> **One line:** "Turn off the light" hits another room's light, a TV, or every light in the house, and the assistant never says which device it picked.

| | |
|---|---|
| **Channel** | Written for **chat**: a text assistant that controls smart home devices through an app or chat window. Smart speakers and home hubs (Alexa, Google Home, HomeKit) are the setting for the examples; the voice-specific signals are PLANNED, not written (see the signals table). |
| **Stakes** | Low for a lamp. Medium when the target is a heater, a lock, a garage door, or a device that someone else in the house is using. |
| **Who is affected** | Anyone with more than one room, more than one light, or devices with similar names; households with two homes on one account; people who cannot easily check by looking (low vision, or away from home using the app). |
| **Frequency** | Common (our judgment). The forum threads I opened show it recurs across platforms; I found no count of how often it happens. |
| **Pattern ID** | smart-home-commands-go-to-the-wrong-device-or |
| **Family** | In-car and home assistants ([family README](../README.md)) |
| **Goal** | In-car and home voice assistants stay safe, act only on authorized commands, and are open about what they hear. |
| **Primary metric** | Wrong-target commands per 1,000 commands. Starting target: under 5 (a starting point to tune, not from a source). Counted from sampled review and from user corrections such as "no, the other one". |
| **Maturity** | Needs review (every source was read only through a fetch summary; tests not yet run) |
| **Will a better model fix this?** | Partly. Better language understanding helps with phrases like "the one by the couch", but the device and room registry and which speaker heard the command matter more. (Our judgment, not tested.) |
| **Also searched as** | alexa turned off wrong light · alexa turns on tv instead of light · google home turns on all lights in room · smart speaker controls wrong room · assistant picked the wrong device · wrong house lights google home |

## 1. In plain words
A person says "turn off the light" and the assistant has to pick one device out of dozens. When it guesses wrong, the wrong lamp goes out, a TV switches on, or every light in the room changes. The fix is to pick the target from where the person is and what they said, say aloud which device was changed, and ask a short question when two or more targets fit.

## 2. What it looks like
A home with a living room, a bedroom, and a TV and receiver. The user is in the bedroom, typing to the home assistant app.

**Without the fix**
```
User: Turn off the light
Bot:  Done.
(The living room light goes off. Someone is reading there. The bedroom light stays on.)
User: No, THIS room
Bot:  Done.
(The assistant turns the living room light back on and the TV on with it.)
```
**With the fix**
```
User: Turn off the light
Bot:  You're in the bedroom, so I turned off the bedroom ceiling light. Undo?
User: Also the lamp
Bot:  Two lamps fit: bedside lamp or reading lamp. Which one? [Bedside] [Reading] [Both] [Something else]
User: Bedside
Bot:  Bedside lamp is off.
```
The fixed assistant picked by the user's room, named the device it changed, offered undo, and asked only when two targets fit.

## 3. Why it happens
These are our reading of the pattern, supported by the forum reports in section 4.
- **Names and rooms overlap.** A room called "Kitchen" and a light called "Kitchen Light" look like the same word. In one SmartThings thread the platform read "kitchen light" as the whole room and replied that it was turning on 13 lights.
- **The assistant falls back to everything.** When the command does not match a room or the speaking device has no room, the assistant can act on every device of that type, and a TV counts as a switch. One openHAB reply said room awareness needs an Alexa-enabled device in the room group, and otherwise a voice command falls back to any matching device on the account.
- **No record of where the person is.** The command goes to a hub that knows the device list but not which speaker heard it, so "the light" has no room attached. Amazon's docs describe this case for speaker groups: when the user does not name the group, Alexa acts on the group that the speaking device belongs to.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| A user's Google Home turned on about 13 devices after "kitchen light" while Alexa turned on one; replies said the room name overlapped the device name, the Activity Log showed Google had understood the words correctly, and Google's default maps "room lights" to every light in the room. Feb. 2019, replies to 2023. | [SmartThings Community thread, Feb. 2019](https://community.smartthings.com/t/google-home-keeps-turning-on-every-device-in-the-room/154649). Opened with the fetch tool; I read the tool's summary of the page, not the raw page. | One household's report plus replies from other users, not from Google. The "can't be turned off" remark is one replier's belief. |
| A user put a TV and lights in one Alexa room; "turn the light on" also turned on the TV, and removing the TV from the room solved it. A reply said room awareness needs an Alexa-enabled device in the room group, otherwise the command falls back to any matching device. Jan. 2020. | [openHAB Community thread, Jan. 2020](https://community.openhab.org/t/alexa-treats-tv-like-a-light/90511). Opened with the fetch tool; summary of the page. | A hobbyist setup (openHAB, Hue skill); the thread did not confirm the technical cause. |
| Amazon's Alexa Smart Properties docs define "implicit targeting": when the user does not name the group, "Alexa turns on all lights in the group" that the speaking device belongs to. An Alexa Built-in device can be in only one group; smart home devices can be in several. | [Amazon, Device Group Management REST API Reference](https://developer.amazon.com/en-GB/docs/alexa/alexa-smart-properties/device-group-mgt-api.html). Opened with the fetch tool; summary of the page. | This is the commercial Alexa Smart Properties product (hotels, senior living), not the consumer app. The page does not say how an implicit command is resolved when a device is in more than one group. |

I found no controlled study of how often voice assistants send commands to the wrong smart home device. A search turned up patents and a 2019 conference demo paper on resolving ambiguous voice commands; I did not open them and do not use them in the fix.

**Public incident.** No public incident found for this failure as such. Searches run: "Alexa turns off wrong light wrong room"; "Google Home assistant controls wrong device room groups"; "Alexa default room device group developer documentation smart home"; "smart home voice command ambiguous device name disambiguation design". The results were forum threads, not a dated, sourced incident. For a different failure (a TV broadcast triggering orders), see the [Amazon Alexa dollhouse teardown](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md).

## 5. The fix
**The principle:** Pick the target from the room and the device the person is using, say which device was changed, and ask a short question when more than one target fits.

**Do this**
1. **Keep one registry of devices and rooms.** Every device has a unique name, one room, and a type. Check: no two devices in a home share the same full name.
2. **Flag name collisions when a device or room is added.** If a room name appears inside a device name (a "Kitchen" room and a "Kitchen Light" device), ask the owner to rename one. Check: the registry rejects or warns on the overlap.
3. **Resolve the target in a fixed order.** (a) The device or room the user named; (b) the room of the speaker, app screen, or chat that sent the command; (c) the room the user used last, within the last few minutes. Check: a transcript replay shows which step picked the target.
4. **Never fall back to "all devices of that type."** If no rule picks one target, ask. Check: no command changes more than one device unless the user said "all", named a group, or confirmed the list.
5. **Ask when two or more targets fit.** Name the options by room and device ("bedside lamp or reading lamp"). Check: an ambiguous command produces a question, not an action.
6. **Say which device was changed, every time.** One short phrase naming room and device, with an undo. Check: the confirmation includes both names.
7. **Do not mix device types.** "Light" matches lights only; a TV, fan, heater, or plug needs its own name. Check: a "light" command never touches a non-light device.
8. **Confirm before a risky target.** For a lock, garage door, heater, or oven, or when the home is not the one the user is usually in, confirm before acting. Check: those types are on a confirm list.

**Reference design**
```
Smart home command resolver (runs before the action is sent)
- Parse: action, device type, any room or device name the user said.
- Named device or room found in the registry, one match -> use it.
- Not named -> room of the speaker/app/chat (if known) -> else last room used in the past few minutes.
- Candidates after filtering by type and room:
    exactly 1 -> act, then say "<room> <device> is off. Undo?"
    2-4       -> ask: "<option A> or <option B>?" with Something else
    0 or 5+   -> ask which room or device; do not act
- Type is lock, garage door, heater, oven, or the home differs from the user's usual one -> confirm first.
- Log: command, candidates, rule that chose the target, user correction within 2 turns.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | Exactly one target fits: act, and state the room and device changed in the same reply. |
| Offer choices: 2-4 options plus "Something else", free text open | Two to four devices fit ("Bedside", "Reading", "Both", "Something else"). Do not offer them when one target clearly fits, or when there are more than four candidates; ask which room instead. |
| Ask one clarifying question | No rule picks a target, or more than four fit: "Which room?" |
| Admit uncertainty and show how to check | The device did not confirm the change: say it may not have worked and offer to check its status. |
| Hand off to a person | The home keeps picking the wrong device after two corrections: point to the app's device and room setup, or support. Do not hand off if the user only wants an undo. |

**Don't over-correct.** If the assistant asks "Which light?" on every command, people stop using it. Ask only when the candidate list has more than one entry after room and type filtering, and remember the answer for the same room (with an easy way to change it). Never refuse a clear command because a similar name exists elsewhere.

**Hand-off rule.** After two corrections in one session ("no, the other one"), show the device and room list for the user to fix, or offer support, and pass the last command and the candidates that were considered.

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Build a test home with rooms, a TV, a fan, two lamps, and one name collision, then replay commands.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | "Turn off the light" from the bedroom app screen | Only the bedroom light changes; reply names room and device (3, 6) |
| 2 | Room "Kitchen" and device "Kitchen Light" both exist | Registry flags the overlap when added (2) |
| 3 | "Turn off the light" in a room with two lamps | Asks which, with the lamp names (5) |
| 4 | TV in the same room as the lights; "turn off the light" | TV is untouched (7) |
| 5 | No room known for the sender | Asks which room; changes nothing (3, 4) |
| 6 | "Turn off all the lights" | Acts on all lights, says how many (4) |
| 7 | "Unlock the front door" from a chat | Confirms before acting (8) |
| 8 | User says "no, the other one" twice | Offers the device and room list or support (hand-off) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Wrong-target commands per 1,000 commands** (primary) | Under 5 | Sampled review of commands labeled by a person, plus user corrections within 2 turns, divided by commands | Over 10 |
| Commands that changed more than one device without "all" or a named group | 0 | Compare devices changed with the parsed command | Any |
| Confirmations that name room and device | 100% | Scan replies after each action | Below 95% |
| Ambiguous commands answered with a question | Over 90% | Sampled review of commands with 2 or more candidates | Below 80% |
| Questions asked on clear commands (counter) | Under 5% | Questions asked when exactly 1 candidate fit | Over 10% |
| Undo taps per 1,000 commands (counter and signal) | Track; set from baseline | Count undo events | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in an event log. Proposed until checked against human-labeled commands. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once published. Written for text/chat: signals 1 to 4. PLANNED for voice (not written, no voice data): which speaker heard the command, speech-recognition confidence, and the user repeating the command louder.

| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| User corrects within 2 turns ("no, the other one", "not that room") | Next user turn after an action event | A change of mind, not a wrong target |
| User undoes the action right away | Undo event within a minute of the action | A guest or a second person in the house reversing it |
| Same command repeated with a room name added | Two commands, second has a room and the same action | The user is being more precise for a new request |
| One command changed 3 or more devices without "all" or a group | Action event with device count | A scene or routine the user set up on purpose |

**Starter rule:** the assistant never changes more than one device unless the user said "all" or named a group, and every confirmation names the room and device it changed.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: smart-home-commands-go-to-the-wrong-device-or
runs: pre_send
reads: [command.parsed_action, command.device_type, command.named_target, sender.room, session.last_room, registry.devices, registry.rooms]
trigger: a device command is about to be sent and the candidate list is not exactly one device
moves: [lead_with_answer, offer_choices, ask_clarifying_question, admit_uncertainty]
choices: ["Bedside lamp", "Reading lamp", "Both", "Something else"]
on_miss: ask
metric: wrong-target commands per 1,000 commands
counter_metric: questions asked on clear commands
status: proposed
```

## 8. Related patterns
- [Reference resolution failures](../../dialogue-management/failures/reference-resolution-failures.md): a chat loses what "it" or "the second one" means. This page is about physical targets, where the answer is a device and a room in a registry, and a wrong guess changes something in a home.
- [Guessing instead of asking](../../dialogue-management/failures/guessing-instead-of-asking.md): the general rule of asking when one missing fact changes the answer. This page applies it to device targets.
- [Order mix-ups at the speaker](../../drive-thru-agents/failures/order-mix-ups-at-the-speaker.md): a voice agent records the wrong item. Here the wrong thing is a real device that changes state.
- [Wake word false activation](../../voice/failures/wake-word-false-activation.md): the assistant wakes when nobody called it (voice). This page is about a command that is heard correctly and sent to the wrong place.
- Related roadmap rows in this family without pages yet: replies too long or visual for a driver, and other safety and authorization rows.

## 9. Common questions
### Why did Alexa turn on my TV when I said "turn on the light"?
In one openHAB thread I opened, a TV in the same room as the lights was switched on by "turn the light on", and removing the TV from the room fixed it. A reply said Alexa falls back to any matching device when room awareness does not apply. See section 4.

### Why does Google Home turn on every light in the room when I name one?
In the SmartThings thread I opened, the room name matched the device name ("Kitchen" and "Kitchen Light"), and replies said Google treated the request as a room command. Renaming the room was the suggested workaround. See rule 2.

### How do I stop my assistant from controlling the wrong room?
As a user, give every device a unique full name and check which room each device is assigned to in the app. As a builder, resolve by the sender's room and ask when two devices fit (rules 3 to 5).

### Should the assistant ask every time?
No. Ask only when two or more devices still fit after filtering by room and type. If it asks on clear commands, people stop using it (see "Don't over-correct").

### Can a better AI model fix this?
Partly. Better language understanding helps with phrases like "the one by the couch", but a model cannot name a device that is missing from the registry or know which speaker heard the command. (Our judgment, not tested.)

---
## Technical section

### T1. Solution architecture
```
command -> parser (action, type, named target)
        -> resolver (named -> sender room -> last room) over registry
        -> candidate filter (type, room) -> 1: act | 2-4: ask | 0 or 5+: ask room
        -> risk gate (lock, garage, heater, oven, other home) -> confirm
        -> action + confirmation text (room and device) + undo + log
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No multi-device action without "all" or a group | Action dispatcher | Test 6; log scan |
| Name collisions flagged on add | Registry write path | Test 2 |
| Confirmation names room and device | Reply template | Reply scan |
| Risky types confirm first | Risk gate | Test 7 |

### T3. Evals
- **Dataset:** a test home with 3 rooms and 20 devices, including one name collision and one non-light on a light's switch type; 100 commands written to cover named, room-implied, ambiguous, and "all" cases, each with an expected target or expected question.
- **Judge rubric:** did the assistant change the expected device, or ask when two or more fit, and does the reply name room and device?
- **Metrics and starting thresholds:** wrong-target under 5 per 1,000; ambiguous commands asked over 90%. Starting points to tune.
- **Release gate:** block a deploy if any test changes more than one device without "all" or a group.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Wrong-target commands per 1,000 | Over 10 | Over 25 | Review corrected commands for a new name collision or registry change |

### T5. Trade-offs
- More questions cost a turn; a good default room and a remembered answer cut them.
- A cleaner registry takes setup work from the owner. Flagging overlaps when a device is added is cheaper than fixing them later.

---
### Deep dive
- **Modality note.** Voice adds the speaker that heard the command, speech-recognition errors, and overheard speech. These are PLANNED for this family and not covered here.
- **Not opened, so not used:** patent applications on resolving ambiguous commands (search results only) and a 2019 IJCAI demo paper on a disambiguation framework (search result only).
- **References.** [SmartThings Community, Feb. 2019](https://community.smartthings.com/t/google-home-keeps-turning-on-every-device-in-the-room/154649); [openHAB Community, Jan. 2020](https://community.openhab.org/t/alexa-treats-tv-like-a-light/90511); [Amazon Device Group Management REST API Reference](https://developer.amazon.com/en-GB/docs/alexa/alexa-smart-properties/device-group-mgt-api.html). All opened with the fetch tool (page summaries).
