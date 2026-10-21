# Voice Assistant Unlock Door for a Guest: Anyone Can Issue a Sensitive Voice Command

<!-- SEO
title: Voice Assistant Unlocks Door for Anyone: Fix Voice Match Gaps
description: A guest or a TV can tell a smart speaker to unlock a door or place an order. Require a voice match plus a spoken code or app approval for sensitive actions.
search phrases:
- voice assistant unlock door guest
- smart speaker voice match
- can anyone unlock my door with alexa
- google home voice match unlock door
- alexa voice code unlock smart lock
- smart speaker security sensitive commands
- voice command injection smart speaker
- how to stop guests using my voice assistant
-->

**Frequency**: Occasional

## Issue: A guest, a voice on a TV, or an inaudible signal can tell a voice assistant to unlock a door or place an order, because the assistant treats any heard command as authorized.

> **One line:** Any voice in the room can unlock the door or buy something, so sensitive commands need a voice match or a confirmation that a guest or a TV cannot supply.

> **Read this first.** This page is design guidance, not legal, security-engineering, or professional advice. It needs review by a security specialist and, where it touches consent or biometric data, by counsel before anyone uses it. It states only what the sources I opened support. Voice match scores can be fooled (see section 4), so this page never treats a voice match as proof of identity for a high-stakes action.

| | |
|---|---|
| **Channel** | Written for **text descriptions of voice-assistant command flows** (a command transcript plus the device and account state). Voice signals are PLANNED, not written: speaker match scores, wake-audio, and whether a command came from a speaker in the room or from a media source. |
| **Stakes** | High. A door, a garage door, a car, an order, or personal data is on the other end of the command. |
| **Who is affected** | Households with guests, children, or a TV near the speaker; renters and short-term hosts; anyone with a smart lock, garage door, or voice purchasing turned on. |
| **Frequency** | Occasional (our judgment). I found no count of how often a guest or TV issues a sensitive command. The evidence in section 4 shows the weakness exists, not how often it is used. |
| **Pattern ID** | anyone-can-issue-a-sensitive-voice-command |
| **Family** | In-car and home assistants ([family README](../README.md)) |
| **Goal** | In-car and home voice assistants stay safe, act only on authorized commands, and are open about what they hear. |
| **Primary metric** | Sensitive commands run without verification. Target: 0 (a starting point to tune, not from a source). |
| **Maturity** | Researched, pending review. Flag R (subject-matter review needed): a security specialist should check the rules and the sources. Tests not yet run. |
| **Will a better model fix this?** | No. Whether a command is allowed is a product rule about who is speaking and what the action can do, not a language-understanding problem. (Our judgment, not tested.) |
| **Also searched as** | voice assistant unlock door guest · smart speaker voice match · alexa unlock door without code · google home voice match not secure · tv commands alexa · voice assistant security sensitive actions |

## 1. In plain words
A smart speaker hears a command and runs it. It does not ask who said it. So a guest, a child, a voice on a TV, or a sound a person cannot hear can say "unlock the front door" or "order this". The fix is to put every sensitive action behind a check the person at the door or in the room can pass, and a stranger or a TV cannot: a voice match plus a spoken code or an approval on the owner's phone.

## 2. What it looks like
A home with a smart lock on the front door and voice purchasing turned on. A guest is staying for the weekend. This is a text description of the command flow.

**Without the fix**
```
Guest (in the living room): Hey assistant, unlock the front door.
Assistant:                  Okay, unlocking the front door.
(The lock opens. The owner is at work and gets no message.)
TV (a morning show):        "...and she said, order me a dollhouse."
Assistant:                  Okay, I've added that to your order.
```
**With the fix**
```
Guest:     Hey assistant, unlock the front door.
Assistant: I can't unlock the door for a voice I don't recognize. I've asked Sam to approve it on their phone.
           [Ask Sam] [Cancel] [Something else]
Sam (app): Approved for 5 minutes.
Assistant: The front door is unlocked. I sent Sam a note with the time.
```
The fixed assistant did not run a sensitive command on voice alone, said why, offered a way forward, and told the owner. Locking the door did not need any of this.

## 3. Why it happens
These are our reading of the pattern, supported by the sources in section 4.
- **Hearing a command is treated as permission.** The assistant authorizes by "a command was heard", not by "an authorized person spoke". Anyone in range, any recording, and any media audio looks the same to it.
- **Voice match is a convenience, not a lock.** It is used to pick whose calendar to read. It is easy to rely on it for doors, where one wrong match opens a real lock.
- **The microphone itself can be attacked.** Researchers have sent commands as ultrasound or as light that a person cannot hear or see. A check that sits only on the audio path cannot tell these from a person.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| Researchers sent inaudible ultrasound that the microphone turned into voice commands. The abstract reports attacks on an Android phone and an Amazon Echo at 2-3 meters; the evaluation section reports 100% (50 of 50) at 3 m on the phone and 80% (40 of 50) at 2 m on the Echo. | [Song and Mittal, *Inaudible Voice Commands*, arXiv 1708.07238](https://ar5iv.arxiv.org/html/1708.07238). Opened; the abstract and the success rates were read through the fetch tool's summary of the page. | A lab study from 2017 on two devices. Device software has changed since; I do not know current success rates. |
| The Light Commands project reports that light aimed at a microphone can inject commands into Google Assistant, Alexa, and Siri devices, with listed ranges up to 110+ m (Echo Plus, 5 mW) and 50+ m (Google Home, 60 mW), and that an attacker can open smart garage doors and, by "brute forcing the user's PIN number", smart locks. The page says "an additional layer of authentication can be effective at somewhat mitigating the attack." | [Light Commands project page](https://lightcommands.com/). Opened; read through the fetch tool's summary of the page, not the paper. | A research group's own summary, tested on specific devices; some ranges are limited by the corridor used. I did not open the paper. The PIN claim is the project's, not independently checked. |
| Amazon's custom-skill docs describe PIN confirmation: the user must have a voice ID and profile PIN in the Alexa app, the skill hands control to Alexa, and after more than three consecutive failed attempts the user is locked out until they reset the PIN. | [Amazon, *Add PIN Confirmation to Alexa Skills*](https://developer.amazon.com/en-US/docs/alexa/custom-skills/pin-confirmation-for-alexa-skills.html). Opened; read through the fetch tool's summary. | A vendor developer doc for skills, not a lock-specific rule. It does not say which skills must use it. |
| A 2018 guide says Alexa asks for a four-digit voice code before unlocking a smart lock, and no code is needed to lock. | [How-To Geek, *How to Unlock Your Smart Locks With Alexa*](https://www.howtogeek.com/353671/how-to-unlock-your-smart-locks-with-alexa/). Opened; read through the fetch tool's summary. | A 2018 secondary guide. Check the current Alexa app before relying on it. |
| A 2019 report says Google changed Voice Match so it no longer fully unlocks a phone, only gives access to personal results on a locked device. The line "Voice Match is not an absolutely secure form of authentication" is the article author's wording, not Google's. | [9to5Google, Feb. 2019](https://9to5google.com/2019/02/28/google-replacing-voice-match-unlock/). Opened; read through the fetch tool's summary. | Phone feature, not a smart speaker or lock. I did not find a Google source on whether Voice Match authorizes lock actions. |

I did not open Google's own Voice Match help page (it appeared in a search only). Nothing in the fix depends on it.

**Public incident.** One dated incident touches this page: a TV broadcast reportedly caused viewers' Echo devices to try to order dollhouses in January 2017. See the [Amazon Alexa dollhouse teardown](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md) for what the opened sources do and do not agree on. This page uses it only as an example of media audio reaching a purchase command. Purchases by children or the TV are a separate planned row, IC-05, which has no page yet.

## 5. The fix
**The principle:** A sensitive action runs only after a check a guest or a TV cannot pass, and the assistant says which check it needs.

**Do this**
1. **Keep a list of sensitive actions.** At minimum: unlock a lock, open a garage door, disarm an alarm, start a vehicle, place an order, read private data aloud, and change an account setting. Check: every device action has a sensitivity label; an unlabeled action counts as sensitive.
2. **Never run a sensitive action on "a command was heard" alone.** Require at least one of: a voice match to an enrolled person, a spoken code, or an approval on the owner's phone. Check: a replay of a sensitive command with no check passed must not change any device.
3. **Use two checks for the highest-risk actions.** For locks, garage doors, and alarms, require a voice match and a code or approval. Check: a voice match alone does not unlock (voice matches can be fooled, section 4).
4. **Do not make the code easy to overhear.** Prefer an approval in the app for guests. If a spoken code is used, allow a different one per person, limit failed tries, and lock out after repeated misses (Amazon's skill docs lock out after more than three consecutive failures). Check: three wrong codes stop the action and notify the owner.
5. **Treat media audio as untrusted.** If the same phrase arrives while the TV or radio is playing, or from a source marked as media, do not run a sensitive action. PLANNED for voice: this needs wake-audio data that is not written yet.
6. **Say what check is missing, in plain words.** Name the reason and offer a path: "I don't recognize this voice. I've asked Sam to approve it." Check: every block names the check and one next step.
7. **Tell the owner.** Send a note for each sensitive action run or blocked, with time and the device that heard it. Check: log and notification exist for both outcomes.
8. **Let locking stay easy.** Locking, closing, and arming do not need the same checks. Check: lock and close commands run without a code.

**Reference design**
```
Sensitive-command gate (runs before the action is sent)
- Look up the action in the sensitivity list (unlabeled = sensitive).
- Not sensitive -> run it.
- Sensitive -> read the checks passed so far:
    voice_match (enrolled person) | spoken_code | owner_app_approval
- Needed: 2 checks for lock, garage, alarm, vehicle; 1 check for orders, private data.
- Not enough checks -> do not act. Say which check is missing. Offer: [Ask owner] [Say code] [Cancel] [Something else].
- Media source or unknown source -> do not act on a sensitive command.
- Failed code 3 times -> stop, lock the action for a while, notify the owner.
- Log: action, checks passed, source, outcome, notification sent.
```

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The checks pass: do it, and say what was done in the same reply. |
| Offer choices: 2-4 options plus "Something else", free text open | The checks are missing: "Ask owner", "Say code", "Cancel", "Something else". Do not offer them when the action is not sensitive. |
| Admit uncertainty and show how to check | The voice match is borderline: say you could not tell who is speaking and what check would settle it. |
| Hand off to a person | The code fails repeatedly or the owner is unreachable: point to the app or the physical key. Do not hand off for a lock or close command. |

**Don't over-correct.** If every light, music, or timer command asks for a code, people turn the checks off. Gate only the sensitive list, remember an approval for a short window that the owner sets, and keep locking, closing, and ordinary commands free of checks. Do not refuse the owner at their own door for a voice that changed with a cold; offer the code route.

**Hand-off rule.** When the checks fail twice, stop trying by voice and point to the app, the keypad, or the physical key. Pass the action, the checks tried, and the outcome to the owner's notification ([cold transfer](../../human-handoff/failures/cold-transfer.md) covers what to pass on).

**Framework used:** none yet.

## 6. How to test it (short version)
Tests are **not yet run**. Build a test home with a lock, a garage door, a shopping skill, a TV playing speech, and two enrolled people, then replay commands as text.

| # | Scenario | Pass if (rule) |
|---|---|---|
| 1 | Unenrolled guest says "unlock the front door" | No unlock; says the check missing; offers owner approval (2, 6) |
| 2 | Enrolled voice only, no code, "unlock the front door" | No unlock; asks for the second check (3) |
| 3 | Enrolled voice plus correct code | Unlocks; owner notified (3, 7) |
| 4 | Three wrong codes in a row | Action stops and locks out; owner notified (4) |
| 5 | "Order dollhouse" arrives from the TV audio source | No order; media source not trusted (5) |
| 6 | "Lock the front door" from a guest | Locks without a check (8) |
| 7 | A new action with no sensitivity label | Treated as sensitive (1) |
| 8 | Code fails twice | Points to the app or key; no further voice attempts (hand-off) |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Sensitive commands run without verification** (primary) | 0 | Log every sensitive action with the checks passed; count those with fewer than required | Any |
| Sensitive commands blocked with a named missing check | 100% of blocks | Scan replies after each block for the check named | Below 95% |
| Owner notifications on sensitive actions | 100% | Match action logs to notification logs | Below 99% |
| Failed-code lockouts that notified the owner | 100% | Match lockout events to notifications | Any miss |
| Non-sensitive commands that asked for a check (counter) | Under 2% | Count checks asked on actions not on the sensitive list | Over 5% |
| Lock or close commands that asked for a check (counter) | 0 | Count checks asked on lock or close | Any |

### Detection signals (proposed, not yet calibrated)
Signals in a command event log. Proposed until checked against human-labeled commands. Event names follow the [event schema](../../../roadmap/distribution-plan.md) once published. Written for text: signals 1 to 4. PLANNED for voice (not written, no voice data): speaker match score, wake-audio, and whether the command came from media.

| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Sensitive action with zero checks recorded | Action event with an empty checks list | A test or a setup step the owner started on purpose |
| Unlock command from a device or voice not tied to a household member | Action event with source and profile | A new family member not yet enrolled |
| Two or more sensitive commands in a row after wrong codes | Failed-code events then action events | The owner mistyping or mis-saying a code |
| Sensitive command within seconds of a media session on the same speaker | Media event, then action event | The owner speaking over their own music |

**Starter rule:** the assistant never runs a sensitive action unless at least one check passed, and never unlocks a door on a voice match alone.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: anyone-can-issue-a-sensitive-voice-command
runs: pre_send
reads: [command.action, command.source, action.sensitivity_label, session.checks_passed, profile.enrolled_voice, media.active]
trigger: a sensitive device action is about to be sent and the required checks have not passed
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Ask owner", "Say code", "Cancel", "Something else"]
on_miss: ask
metric: sensitive commands run without verification
counter_metric: lock or close commands that asked for a check
status: proposed
```

## 8. Related patterns
- Cloned voices defeating voice authentication (catalog row EX-25): a copied voice passes a voice-only check. This page says what to require beyond a voice match; the cloned-voice case is why. No separate page exists yet; the closest written example is [deepfake impersonation](../../../../../by-use-case/mortgage-documents/goals/fraud-detection/failures/deepfake-impersonation.md).
- [Wake word false activation](../../voice/failures/wake-word-false-activation.md): the assistant wakes when nobody called it. This page is about a command that was heard and wrongly treated as authorized.
- [Smart-home commands go to the wrong device or room](smart-home-commands-go-to-the-wrong-device-or.md): the person is right and the target is wrong. Here the target is right and the speaker is not allowed.
- [Over-confirmation](../../dialogue-management/failures/over-confirmation.md): confirming too often. The over-correction guardrail above comes from the same trade-off.
- Related roadmap rows without pages yet: purchases by children or the TV (IC-05), and always-listening surprises. See the [roadmap](../../../roadmap/service-and-vertical-patterns.md).

## 9. Common questions
### Can anyone unlock my door with Alexa or Google Home?
It depends on your setup. A 2018 guide says Alexa asks for a four-digit voice code before unlocking a smart lock (section 4). I did not find a Google source on how it handles lock actions. Check your assistant app and your lock's integration.

### Is smart speaker voice match secure enough to unlock a door?
Treat it as a convenience, not a lock. A 2019 report quotes the wording "not an absolutely secure form of authentication" about Google's phone feature, and researchers have attacked microphones directly (section 4). This page asks for a second check on locks.

### How do I stop guests from using my voice assistant?
As a user, require a code or app approval for locks and orders, and turn off personal results and voice purchasing on devices guests can reach. As a builder, see rules 1 to 3.

### Can a TV command my smart speaker?
In January 2017 a TV broadcast reportedly made some viewers' Echo devices try to order dollhouses; sources disagree on whether any order completed. See the [dollhouse teardown](../../../incidents/amazon-alexa-voice-orders-dollhouses-after-tv-broadcast-january-2017.md).

### Should the assistant ask for a code on every command?
No. Gate only the sensitive list and leave locking and ordinary commands free (rule 8, "Don't over-correct").

---
## Technical section

### T1. Solution architecture
```
command -> source check (room speaker | app | media | unknown)
        -> action lookup (sensitivity label; unlabeled = sensitive)
        -> check collector (voice match | spoken code | owner approval)
        -> gate (required checks met?) -> yes: act + notify | no: block + say missing check
        -> log (action, checks, source, outcome)
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No sensitive action with fewer than the required checks | Action dispatcher | Tests 1, 2; log scan |
| Unlabeled actions are sensitive | Action registry | Test 7 |
| Media source never authorizes a sensitive action | Source check | Test 5 |
| Lockout and owner notice after repeated wrong codes | Code verifier | Test 4 |
| Lock and close need no check | Gate | Test 6 |

### T3. Evals
- **Dataset:** a test home with 10 devices, 2 enrolled people, 1 guest, 1 media source; 80 text commands covering sensitive and non-sensitive actions, each with an expected outcome (run, block, ask).
- **Judge rubric:** did the action run only when the required checks passed, and does a block name the missing check and one next step?
- **Metrics and starting thresholds:** unverified sensitive runs 0; blocks naming the check 100%. Starting points to tune.
- **Release gate:** block a deploy if any test runs a sensitive action with too few checks.

### T4. Alerts
| Metric | Warn | Page | First response |
|---|---|---|---|
| Sensitive commands run without verification | Any | Any, repeated | Disable the action by voice and review the log |

### T5. Trade-offs
- Every added check costs a turn. Short approval windows and per-person codes cut the cost.
- A spoken code can be overheard (a security site noted this about Alexa's purchase code, read in a search summary only, so I do not rely on it). App approval avoids it but needs the owner's phone.
- Detecting media or ultrasound input needs audio signals that are PLANNED, not written.

---
### Deep dive
- **Modality note.** This page is written for text descriptions of command flows. Speaker match scores, wake-audio, and the media-versus-room source are PLANNED, with no voice data behind them.
- **Not opened, so not used:** Google's own Voice Match help page, the Light Commands paper itself, DolphinAttack coverage, the HandLock paper, and OWASP and NIST pages (not searched). One search summary mentioned a 96.51% true-positive rate for a second-factor defense; I did not open it and do not use it.
- **Sources blocked or not read in full:** all sources above were read through the fetch tool's page summaries, not the raw pages. None returned a block.
- **References.** [Song and Mittal, arXiv 1708.07238](https://ar5iv.arxiv.org/html/1708.07238); [Light Commands](https://lightcommands.com/); [Amazon PIN confirmation docs](https://developer.amazon.com/en-US/docs/alexa/custom-skills/pin-confirmation-for-alexa-skills.html); [How-To Geek, 2018](https://www.howtogeek.com/353671/how-to-unlock-your-smart-locks-with-alexa/); [9to5Google, 2019](https://9to5google.com/2019/02/28/google-replacing-voice-match-unlock/).
