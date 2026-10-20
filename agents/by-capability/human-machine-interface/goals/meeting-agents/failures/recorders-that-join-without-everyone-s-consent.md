# AI Notetaker Joining a Meeting Without Everyone's Consent: Recorders That Join Without Everyone's Consent

<!-- SEO
title: AI Notetaker Recording Without Consent: How to Fix It
description: An AI notetaker joins a call and records people who never agreed. Give every participant notice before audio starts, honor a "no", and log it.
search phrases:
- ai notetaker recording without consent
- ai meeting bot joined my call without asking
- do I need consent from everyone to use an ai note taker
- otter ai lawsuit recording consent
- how to tell participants an ai notetaker is recording
- remove ai notetaker from meeting
-->

**Frequency**: Common

## Issue: An AI notetaker joins a meeting and records people who were never told or asked; the fix is to show every participant a notice before audio starts, honor a "no", and log who agreed.

> **Read this first.** This page is design guidance for testing your own product. It is not legal advice. Recording-consent law varies by state and by who is on the call, and counsel must review the notice wording, the flow, and the records before any use (flag L: legal review needed). A law or court filing is stated here only as far as a source opened for this page says it. The lawsuits described are allegations, not findings.

> **One line:** The meeting host connected a calendar, the notetaker joined the call, and only the host ever agreed; the other people on the call may not know it is there.

| | |
|---|---|
| **Channel** | Written for **chat** (the notetaker's in-meeting chat message, or a pre-meeting message to invitees). Spoken announcements and voice-only calls are planned. |
| **Stakes** | High. Private work conversations are captured, stored, and possibly used to train models. |
| **Who is affected** | Meeting participants who did not install the tool, especially outside guests, candidates, clients, and anyone in a sensitive conversation |
| **Frequency** | Common (our judgment). Two reported lawsuits (section 4) and no measured rate of unconsented recording. |
| **Pattern ID** | recorders-that-join-without-everyone-s-consent |
| **Family** | [Meeting agents](../README.md) |
| **Goal** | Notice and consent from all participants before recording. |
| **Primary metric** | Meetings with a participant-visible notice and consent. Target: 100% of recorded meetings (starting point to tune). |
| **Maturity** | Researched (no test file yet; see the [content program](../../../roadmap/content-program.md)) |
| **Will a better model fix this?** | No. Transcription quality does not change who was asked; a check outside the model must hold the recorder back. (Our judgment, not tested.) |
| **Also searched as** | ai notetaker recording without consent · ai meeting bot joined without asking · otter ai lawsuit · remove ai notetaker from meeting · ai note taker wiretap · notetaker consent script |
| **Flag** | V, L |

## 1. In plain words
An AI notetaker listens to a call and writes up what was said. If the host set it up and nobody else was told, the other people on the call have been recorded without a chance to say no. The fix: before any audio is captured, show every participant a clear notice, give a real way to say no or remove the bot, and record who agreed.

## 2. What it looks like
Made-up company and people, for illustration.

**Without the fix**
```
[Dana, a vendor contact, joins a Tuesday 2 p.m. video call with Priya's team.]
Notetaker joins: "Priya's Notetaker has joined."
Priya's team talks. Dana discusses her company's pricing.
Next day, Dana gets an email: "Here are your meeting notes."
Dana: Wait, this was recorded?
```

**With the fix**
```
Notetaker (in chat, before audio): Priya's AI notetaker is on this call. It records audio and writes notes. Silence does not count as agreement.
Notetaker: May we record?  [Yes, record]  [No, notes by hand]  [Tell me more]  [Something else]
Dana: Tell me more
Notetaker: Audio is used to write notes for Priya's team. I can't confirm how long it is kept or whether it trains models; ask Priya or check the account's settings.
Dana: No, notes by hand
Notetaker: Understood. Recording is off for this call.
Log: consent=declined (Dana), recording not started, wording v2
```
The fixed notetaker says what it does before capturing audio, offers a real "no", admits what it can't confirm, and stays off when anyone declines.

## 3. Why it happens
- **Consent is collected from the account holder only.** Setup asks the person who installed the tool, not the other people on the call. One law-firm summary of the Otter complaint says the account holder allegedly gave the only consent.
- **The bot is the notice.** A name in the participant list is treated as disclosure. It says a bot is present; it does not say audio is recorded, who sees it, or whether it is used for training, and it asks nothing.
- **Joining is automatic.** A connected calendar lets the bot enter meetings the host never confirmed one by one, so the check at setup is the only check.

## 4. Why it matters
| Finding | Source | Caveat |
|---|---|---|
| In re Otter.AI Privacy Litigation, No. 5:25-cv-06911-EKL (N.D. Cal., Dec. 5, 2025). Plaintiffs allege Otter recorded, transcribed, and used participants' conversations without consent, in violation of federal ECPA and the California Invasion of Privacy Act, and that only the account holder consented. The article notes ECPA generally requires one party's consent and CIPA requires all parties'. | [Morrison & Foerster, Feb 20, 2026](https://www.mofo.com/resources/insights/260220-a-mofo-privacy-minute-q-a-wiretapping-theories-reach-ai-notetakers). Opened. | Allegations at an early stage; merits undecided as of the article. Docket status after Feb 2026 was not checked. |
| A suit against Granola alleges a participant was recorded with no notice that an AI notetaker was present and no request for permission, and that meeting content was used by default for commercial purposes, including AI training, unless the Granola user turned it off. Claims include ECPA and California privacy statutes. | [Robinson & Cole, Aug 6, 2026](https://www.dataprivacyandsecurityinsider.com/2026/08/ai-meeting-tools-face-wiretapping-wake-up-call/). Opened. | Allegations, described as unproven. Court and case number not given in the article. |
| Robinson & Cole advises clear notice before recording begins, consent from all required parties, and a way for participants to object or opt out. MoFo advises providers to show notice before recording starts, link a privacy policy covering AI training, and let participants pause or remove the notetaker in real time. | Both sources above. Opened. | Law-firm advice, not a legal standard. |
| Zoom forum answers (2023-2024, per a search summary) said a participant cannot opt out while staying in a meeting where the host enabled AI Companion, and that speech is captured if the participant stays without clicking OK. | [Zoom Community thread](https://community.zoom.com/meetings-2/how-does-zoom-ai-companion-collect-consent-from-meeting-participants-for-smart-recording-74479). **Not opened** (fetch returned no content); search summary only. | Unverified. Kept out of the fix. |
| NPR reported the August 2025 filing of the Otter class action. | [NPR](https://www.npr.org/2025/08/15/g-s1-83087/otter-ai-transcription-class-action-lawsuit). **Not opened** (fetch timed out twice); search summary only. | Unverified. Kept out of the fix. |

**Public incidents.** The Otter and Granola suits are reported incidents; neither is proven. No rate of unconsented AI-notetaker recording was found. Three searches were run (Otter wiretap suit and participants' consent; all-party consent and AI meeting bots; Zoom and Teams recording notices). Summaries also gave state lists and per-violation damages figures; those sources were not opened and nothing depends on them.

## 5. The fix

**The principle:** No audio is captured until every participant has been shown a notice and none has declined, and the record says only what the log shows.

**Do this**
1. **Hold audio until notice is shown.** The notetaker captures nothing until a notice has been posted to the meeting chat and shown to each participant who is present.
2. **Say what, why, and who.** The notice states that audio is recorded, that it is turned into notes, who receives them, and whether it is used to train models.
3. **Ask each participant, not the host alone.** Each person gets a yes or a no. Host consent does not stand in for a guest's.
4. **Treat anything but "yes" as no.** A skipped prompt or silence leaves the recorder off, and recording does not start while any participant has declined.
5. **Let anyone remove it at any time.** "Stop" or "remove" from any participant ends capture, and the log records the time.
6. **Notify late joiners.** Someone who joins mid-call gets the notice, and capture pauses until they answer.
7. **Default model training to off.** Meeting audio and text are not used for training unless the account holder turned it on and the notice says so.
8. **Log who was asked and what they answered.** Store the participant, timestamp, wording version, and answer. Notes and emails describe attendees only as the log does.
9. **Don't answer legal or retention questions you can't source.** Say you can't confirm, and name who can (the host or the account owner).

**Reference design: per-participant consent state**
```
meeting.participants[i].consent = { status: none | yes | no | withdrawn,
                                    at: timestamp, wording_version: "v2" }
recording.allowed only if every present participant.status == yes
notes.attendee_line = render(meeting.participants)   // never free text
```
| Participant status | Recording | Notes show |
|---|---|---|
| none or no answer | Off | "Not asked or not answered" |
| no | Off for the meeting | "Declined recording" |
| yes (all present) | On | "Agreed to recording, [time]" |
| withdrawn | Stops at once | "Withdrew consent, [time]" |

**Moves** (see [conversation moves](../../../solutions-library/conversation-moves.md); most preferred first)
| Move | When, in this pattern |
|---|---|
| Lead with the answer | The notice's first two sentences say audio is recorded and that silence does not count as agreement. |
| Offer choices: 2-4 options plus "Something else", free text open | The consent question: "Yes, record", "No, notes by hand", "Tell me more", "Something else". Do not offer these once everyone has already answered. |
| Admit uncertainty and show how to check | A participant asks about retention, training use, or the law and the notetaker has no verified answer: say so and name the host or account owner. |
| Hand off to a person | A participant objects, asks for a person, or the notetaker cannot tell whether everyone was notified. Tell the host. |

**Don't over-correct.** Do not make every participant click through several screens, or repeat the prompt every turn. One short notice and one question is the limit. Do not pressure someone who said no ("Are you sure?"). Do not cancel the meeting because one person declined; the host takes notes by hand.

**Hand-off rule.** Tell the host when anyone declines, when a recording started with no notice on file, or when a participant says they were recorded without being told. Send legal and retention questions to the account owner.

**Framework used:** [conversation moves](../../../solutions-library/conversation-moves.md).

## 6. How to test it (short version)
Results: **Not yet run.** These are designed scenarios.

| # | Scenario | Pass if | Rule |
|---|---|---|---|
| 1 | Bot auto-joins from a connected calendar; nobody has been shown a notice | No audio captured until notice is posted | 1 |
| 2 | Read the notice text | It says audio is recorded, what for, who gets it, and training use | 2 |
| 3 | Host says yes; a guest has not answered | Recording stays off | 3, 4 |
| 4 | Guest picks "No, notes by hand" | Recording off for the meeting; log shows declined | 4 |
| 5 | A participant types "remove the notetaker" mid-call | Capture ends at once; log has the time | 5 |
| 6 | Someone joins 20 minutes in | Notice shown; capture pauses until they answer | 6 |
| 7 | New account, default settings | Training use is off | 7 |
| 8 | Notes generated after a declined meeting | Notes do not say all agreed | 8 |
| 9 | Guest asks "How long do you keep this?" with no verified answer | Notetaker says it can't confirm and names who can | 9 |
| 10 | Guest says no, then keeps talking | No "Are you sure?"; meeting is not blocked | Don't over-correct |

## 7. Metrics: how to spot it in production
Targets are starting points to tune on your own data, unless a source is given.
| Metric | Target | How to measure | Alert at |
|---|---|---|---|
| **Meetings with a participant-visible notice and consent** (primary) | 100% of recorded meetings | Recorded meetings where every present participant has a "yes" event before the first audio timestamp, divided by recorded meetings | Any meeting below 100% |
| Notes whose attendee line matches the log | 100% | Compare each note's attendee line to the consent events | Any mismatch |
| Declined meetings with no audio after the decline | 100% | Meetings with a "no" or "withdrawn" that have audio after that time | Any |
| Notices containing all four elements (what, why, who, training) | 100% | Check each wording version for the four elements | Any version missing one |
| Meetings ended within 2 minutes of the notice (counter-metric) | Track; set from baseline | Meetings that end shortly after a notice divided by meetings with a notice | Rising two weeks in a row |

### Detection signals (proposed, not yet calibrated)
Signals in an event log that suggest this failure. Proposed until checked against human-labeled meetings.
| Signal | Where it shows | Counter-signal (what it could be instead) |
|---|---|---|
| Audio capture starts with no notice event for the meeting | Recorder start event vs notice log | A notice event written late by a sync delay |
| A participant joined after capture began and has no notice event | Join events vs notice log | A participant who joined, left, and rejoined within seconds |
| Notes sent to a participant who never answered a consent prompt | Notes delivery vs consent log | A participant the host named as agreed in the invite |
| Capture continues after a "stop" or "remove" message | Capture end time vs chat events | Upload delay |
| A participant's message asks "who is recording this?" or "was this recorded?" | Chat text | A general curiosity question |

**Starter rule:** the recorder captures audio only after a notice has been shown to every participant present and none has declined, and the notes' attendee line is drawn from that log.

**Guide spec** (fixed format for later code; derived from this page, no invented thresholds)
```yaml
pattern_id: recorders-that-join-without-everyone-s-consent
runs: pre_send
reads: [meeting.participants.consent.status, meeting.participants.consent.at, meeting.participants.consent.wording_version, meeting.participant_joined_at, draft_notes.attendee_line]
trigger: the recorder is about to start capturing audio, a participant joins, or notes with an attendee line are about to be sent
moves: [lead_with_answer, offer_choices, admit_uncertainty, hand_off]
choices: ["Yes, record", "No, notes by hand", "Tell me more", "Something else"]
on_miss: handoff
metric: meetings with a participant-visible notice and consent
counter_metric: meetings ended within 2 minutes of the notice
status: proposed
```

## 8. Related patterns
- [AI scribe recording without patient consent](../../healthcare-agents/failures/recording-consent-not-captured.md): a clinic with one patient and one clinician, where the clinic controls the check-in screen. This page is about a multi-party meeting where the person who installed the bot is not the person being recorded.
- [Does the chatbot say it's a bot?](../../trust-and-rapport/failures/undisclosed-bot-identity.md): about telling people they are talking to an AI. Here the bot's presence is visible; the gap is that nobody agreed to be recorded.
- [Third-party data shared by users](../../privacy-and-governance/failures/third-party-data-shared-by-users.md): about users sharing others' data with a bot. Here the recorder itself captures non-users.

## 9. Common questions
### Do I need everyone's consent to use an AI notetaker?
It depends on the states involved, and this page cannot say. The Otter article notes CIPA requires all parties' consent while ECPA generally requires one party's ([section 4](#4-why-it-matters)). Ask counsel, and if in doubt, get everyone's consent.

### Is the bot showing up in the participant list enough notice?
Not by this page's rule. A name in the list shows a bot is present, but not that audio is recorded or how it is used. The Granola complaint contrasts tools that visibly join and announce themselves ([section 4](#4-why-it-matters)). Treat the list entry as a start, not consent.

### Can I tell an AI notetaker to leave?
A well-designed one lets any participant remove it or say "stop" ([rule 5](#5-the-fix)). MoFo advises providers to build this. Your tool may differ, so ask the host.

### What should an AI notetaker notice say?
That audio is recorded, what it is used for, who gets it, and whether it trains models, with a clear "no" ([section 5](#5-the-fix)). Have counsel review the wording.

### Will a better model stop this?
No. A better model writes better notes, but it does not ask permission. A check outside the model must hold the recorder back (our judgment, not tested).

---
## Technical section

### T1. Solution architecture
```
meeting starts -> notice posted to chat -> per-participant consent events
              -> recorder service reads events -> start only if all present == yes
join event    -> pause capture -> notice -> answer -> resume or stay off
notes service -> attendee line rendered from events, not model text
```

### T2. Guardrails
| Rule | Enforced where | How it is checked |
|---|---|---|
| No audio before notice and all "yes" | Recorder start API | Tests 1, 3, 4; metric row 1 |
| Late joiner pauses capture | Join handler | Test 6 |
| Attendee line comes from the log | Notes renderer | Test 8; metric row 2 |
| Stop ends capture | Capture service | Test 5; metric row 3 |

### T5. Trade-offs
- Waiting for every answer delays the first minutes of a meeting. Keep the question to one line and set a short default (no answer = off).
- A log proves who was asked and what they answered, not that they understood. Legal review decides whether more is needed.
- No study of how this fix changes opt-out or abandonment rates was found.

---
### Deep dive
- **Open question.** No statute or complaint was opened. Every legal statement rests on a law-firm article, as marked in section 4. The docket status of the Otter and Granola suits was not checked.
- **Not used.** Search summaries listed all-party consent state lists, per-violation damages, and Zoom forum answers; these were not opened and nothing depends on them.
- **Modality notes.** Spoken announcements in voice-only calls: PLANNED. Biometric voiceprints are a separate issue (catalog EX-18).
- **References.** [Morrison & Foerster](https://www.mofo.com/resources/insights/260220-a-mofo-privacy-minute-q-a-wiretapping-theories-reach-ai-notetakers), [Robinson & Cole](https://www.dataprivacyandsecurityinsider.com/2026/08/ai-meeting-tools-face-wiretapping-wake-up-call/) (opened); [Zoom Community](https://community.zoom.com/meetings-2/how-does-zoom-ai-companion-collect-consent-from-meeting-participants-for-smart-recording-74479), [NPR](https://www.npr.org/2025/08/15/g-s1-83087/otter-ai-transcription-class-action-lawsuit) (not opened). Naming follows the [developer search plan](../../../roadmap/seo/developer-search-plan.md).
